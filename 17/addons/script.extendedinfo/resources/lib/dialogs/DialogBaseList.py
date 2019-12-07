# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcgui
from ..Utils import *
from ..ImageTools import *
from ..TheMovieDB import *
from ..WindowManager import wm
from T9Search import T9Search
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer

PLAYER = VideoPlayer.VideoPlayer()
ch = OnClickHandler()


class DialogBaseList(object):

    def __init__(self, *args, **kwargs):
        super(DialogBaseList, self).__init__(*args, **kwargs)
        self.listitem_list = kwargs.get('listitems', None)
        self.search_str = kwargs.get('search_str', "").decode("utf-8")
        self.filter_label = kwargs.get("filter_label", "").decode("utf-8")
        self.mode = kwargs.get("mode", "filter")
        self.filters = kwargs.get('filters', [])
        self.color = kwargs.get('color', "FFAAAAAA")
        self.page = 1
        self.column = None
        self.last_position = 0
        self.total_pages = 1
        self.total_items = 0

    def onInit(self):
        super(DialogBaseList, self).onInit()
        HOME.setProperty("WindowColor", self.color)
        self.window.setProperty("WindowColor", self.color)
        if SETTING("alt_browser_layout") == "true":
            self.window.setProperty("alt_layout", "true")
        self.update_ui()
        xbmc.sleep(200)
        if self.total_items > 0:
            xbmc.executebuiltin("SetFocus(500)")
            self.getControl(500).selectItem(self.last_position)
        else:
            xbmc.executebuiltin("SetFocus(6000)")

    @ch.action("parentdir", "*")
    @ch.action("parentfolder", "*")
    def previous_menu(self):
        onback = self.window.getProperty("%i_onback" % self.control_id)
        if onback:
            xbmc.executebuiltin(onback)
        else:
            self.close()
            wm.pop_stack()

    @ch.action("previousmenu", "*")
    def exit_script(self):
        self.close()

    @ch.action("left", "*")
    @ch.action("right", "*")
    @ch.action("up", "*")
    @ch.action("down", "*")
    def save_position(self):
        self.position = self.getControl(500).getSelectedPosition()

    def onAction(self, action):
        ch.serve_action(action, self.getFocusId(), self)

    def onFocus(self, control_id):
        old_page = self.page
        if control_id == 600:
            self.go_to_next_page()
        elif control_id == 700:
            self.go_to_prev_page()
        if self.page != old_page:
            self.update()

    @ch.click(5005)
    def reset_filters(self):
        if len(self.filters) < 2 and self.type != "movie" and self.type != "tv":
            self.filters = []
        elif len(self.filters) > 0:
            listitems = ["%s: %s" % (f["typelabel"], f["label"]) for f in self.filters]
            listitems.append("%s %s" % (LANG(32078), LANG(32023).lower()))
            if self.order == "asc": order_label = LANG(584)
            if self.order == "desc": order_label = LANG(585)
            if self.type == "movie": fav_name = "%s - %s - %s %s - %s" % (LANG(20342), self.filter_label, "[COLOR FFAAAAAA]%s:[/COLOR] %s" % (LANG(21429), self.sort), order_label.lower(), "[COLOR FFAAAAAA]page:[/COLOR] %s" % self.page)
            elif self.type == "tv": fav_name = "%s - %s - %s %s - %s" % (LANG(20343), self.filter_label, "[COLOR FFAAAAAA]%s:[/COLOR] %s" % (LANG(21429), self.sort), order_label.lower(), "[COLOR FFAAAAAA]page:[/COLOR] %s" % self.page)
#            elif self.type == "video": fav_name = "%s - %s" % (LANG(1212), self.filter_label)
#            elif self.type == "playlist": fav_name = "%s - %s" % (LANG(559), self.filter_label)
#            elif self.type == "channel": fav_name = "%s - %s" % (LANG(19029), self.filter_label)
            if self.type == "movie" or self.type == "tv":
                faves = get_kodi_json(method="Favourites.GetFavourites", params='{"type":"window", "properties":["window", "windowparameter", "thumbnail", "path"]}')
                status = ""
                if faves["result"]["favourites"]:
                    for item in faves["result"]["favourites"]:
                        if item["title"] == fav_name:
                            status = "present"
                if status == "present": message = LANG(14077)
                else: message = LANG(14076)
                listitems.append(message)
            index = xbmcgui.Dialog().select(heading=ADDON.getLocalizedString(32077), list=listitems)
            if self.type == "movie" or self.type == "tv":
                if index == -1:
                    return None
                elif index == len(listitems) - 2:
                    self.filters = []
                elif index == len(listitems) - 1:
                    if SETTING("include_adults").lower() != "true":
                        url = urllib.quote_plus("%s?sort_by=%s&%slanguage=%s&page=%i" % (self.type, self.sort + "." + self.order, self.filter_url, SETTING("LanguageID"), int(self.page)))
                    else:
                        url = urllib.quote_plus("%s?sort_by=%s&%slanguage=%s&page=%i&include_adult=%s" % (self.type, self.sort + "." + self.order, self.filter_url, SETTING("LanguageID"), int(self.page), include_adult))
                    if status != "present" and FAVTHUMB == "true":
                        posters = [i.getProperty("poster") for i in self.listitems if i.getProperty("poster") != "" and i.getProperty("poster") != None]
                        if   len(posters) > 15: poster = concatenate(posters[:16], url)
                        elif len(posters) >  8: poster = concatenate(posters[:9], url)
                        elif len(posters) >  3: poster = concatenate(posters[:4], url)
                        elif len(posters) >  0: poster = posters[0]
                        else: poster = ""
                    else: poster = ""
                    get_kodi_json(method="Favourites.AddFavourite", params='{"title":"%s", "type":"window", "window":"Videos", "windowparameter":"%s", "thumbnail":"%s"}' % (fav_name, 'plugin://script.extendedinfo/?info=filtered&type=%s&filters=%s&label=%s&sort=%s&sort_label=%s&order=%s&page=%s&url=%s' % (self.type, urllib.quote_plus(str(self.filters)), urllib.quote_plus(fav_name), self.sort, urllib.quote_plus(LANG(550) % self.sort_label), self.order, self.page, url), poster.replace("\\","\\\\")))
                    return notify(header="%s:" % message, message=fav_name, icon=poster, time=1500, sound=False)
                else:
                    del self.filters[index]
            elif self.type != "movie" and self.type != "tv":
                if index == -1:
                    return None
                elif index == len(listitems) - 1:
                    self.filters = []
            else:
                del self.filters[index]
        else:
            self.filters = []
        self.page = 1
        self.mode = "filter"
        self.update()

    @ch.click(6000)
    def open_search(self):
        if SETTING("classic_search") == "true":
            result = xbmcgui.Dialog().input(heading=LANG(16017),
                                            type=xbmcgui.INPUT_ALPHANUM)
            if result and result > -1:
                self.search(result)
        else:
            dialog = T9Search(u'%s-T9Search.xml' % ADDON_ID, ADDON_PATH,
                              call=self.search,
                              start_value="",
                              history=self.__class__.__name__ + ".search")
            dialog.doModal()
        if self.total_items > 0:
            self.setFocusId(500)

    def onClick(self, control_id):
        ch.serve(control_id, self)

    def search(self, label):
        if not label:
            return None
        self.search_str = label
        self.mode = "search"
        self.filters = []
        self.page = 1
        self.update_content()
        self.update_ui()

    def set_filter_url(self):
        filter_list = []
        for item in self.filters:
            filter_list.append("%s=%s" % (item["type"], item["id"]))
        self.filter_url = "&".join(filter_list)
        if self.filter_url:
            self.filter_url += "&"

    def set_filter_label(self):
        filter_list = []
        for item in self.filters:
            filter_label = item["label"].replace("|", " | ").replace(",", " + ").replace(":", "")
            filter_list.append("[COLOR FFAAAAAA]%s:[/COLOR] %s" % (item["typelabel"], filter_label))
        self.filter_label = "  -  ".join(filter_list)

    def update_content(self, add=False, force_update=False):
        if add:
            self.old_items = self.listitems
        else:
            self.old_items = []
        data = self.fetch_data(force=force_update)
        self.listitems = data.get("listitems", [])
        self.total_pages = data.get("results_per_page", "")
        self.total_items = data.get("total_results", "")
        self.next_page_token = data.get("next_page_token", "")
        self.prev_page_token = data.get("prev_page_token", "")
        self.listitems = self.old_items + create_listitems(self.listitems)

    def update_ui(self):
        if not self.listitems and self.getFocusId() == 500:
            self.setFocusId(6000)
        self.getControl(500).reset()
        if self.listitems:
            self.getControl(500).addItems(self.listitems)
            if self.column is not None:
                self.getControl(500).selectItem(self.column)
        self.window.setProperty("TotalPages", str(self.total_pages))
        self.window.setProperty("TotalItems", str(self.total_items))
        self.window.setProperty("CurrentPage", str(self.page))
        self.window.setProperty("Filter_Label", self.filter_label)
        self.window.setProperty("Sort_Label", self.sort_label)
        if self.page == self.total_pages:
            self.window.clearProperty("ArrowDown")
        else:
            self.window.setProperty("ArrowDown", "True")
        if self.page > 0:
            self.window.setProperty("ArrowUp", "True")
        else:
            self.window.clearProperty("ArrowUp")
        if self.order == "asc":
            self.window.setProperty("Order_Label", LANG(584))
        else:
            self.window.setProperty("Order_Label", LANG(585))

    def get_column(self):
        for i in range(0, 10):
            if xbmc.getCondVisibility("Container(500).Column(%i)" % i):
                self.column = i
                break

    @busy_dialog
    def update(self, force_update=False):
        self.update_content(force_update=force_update)
        self.update_ui()

    def add_filter(self, key, value, typelabel, label, force_overwrite=False):
        index = -1
        new_filter = {"id": value,
                      "type": key,
                      "typelabel": typelabel,
                      "label": label}
        if new_filter in self.filters:
            return False
        for i, item in enumerate(self.filters):
            if item["type"] == key:
                index = i
                break
        if not value:
            return False
        if index == -1:
            self.filters.append(new_filter)
            return None
        if force_overwrite:
            self.filters[index]["id"] = urllib.quote_plus(str(value))
            self.filters[index]["label"] = str(label)
            return None
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno(heading=LANG(587),
                           line1=LANG(32106),
                           nolabel="OR",
                           yeslabel="AND")
        if ret:
            self.filters[index]["id"] = self.filters[index]["id"] + "," + urllib.quote_plus(str(value))
            self.filters[index]["label"] = self.filters[index]["label"] + "," + label
        else:
            self.filters[index]["id"] = self.filters[index]["id"] + "|" + urllib.quote_plus(str(value))
            self.filters[index]["label"] = self.filters[index]["label"] + "|" + label
