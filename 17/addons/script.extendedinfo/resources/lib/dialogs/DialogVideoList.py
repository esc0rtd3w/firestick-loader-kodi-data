# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcgui
from ..Utils import *
from ..TheMovieDB import *
from DialogBaseList import DialogBaseList
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from ..import VideoPlayer
PLAYER = VideoPlayer.VideoPlayer()

ch = OnClickHandler()

SORTS = {"movie": {"popularity": LANG(32110),
                   "release_date": LANG(172).replace(":",""),
                   "revenue": LANG(32108),
                   # "Release Date": "primary_release_date",
                   "original_title": LANG(20376),
                   "vote_average": LANG(32112),
                   "vote_count": LANG(32111)},
         "tv": {"popularity": LANG(32110),
                "first_air_date": LANG(20416),
                "vote_average": LANG(32112),
                "vote_count": LANG(32111)},
         "favorites": {"created_at": LANG(32157)},
         "list": {"created_at": LANG(32157)},
         "rating": {"created_at": LANG(32157)}}
TRANSLATIONS = {"movie": LANG(20338),
                "tv": LANG(20364),
                "person": LANG(32156)}

include_adult = SETTING("include_adults").lower()


def get_tmdb_window(window_type):

    class DialogVideoList(DialogBaseList, window_type):

        @busy_dialog
        def __init__(self, *args, **kwargs):
            super(DialogVideoList, self).__init__(*args, **kwargs)
            self.type = kwargs.get('type', "movie")
            self.list_id = kwargs.get("list_id", False)
            self.sort = kwargs.get('sort', "popularity")
            self.page = kwargs.get('page', 1)
            self.sort_label = kwargs.get('sort_label', LANG(32110))
            self.order = kwargs.get('order', "desc")
            self.logged_in = check_login()
            if self.listitem_list:
                self.listitems = create_listitems(self.listitem_list)
                self.total_items = len(self.listitem_list)
            else:
                self.update_content(force_update=kwargs.get('force', False))

        def onClick(self, control_id):
            super(DialogVideoList, self).onClick(control_id)
            ch.serve(control_id, self)

        def onAction(self, action):
            super(DialogVideoList, self).onAction(action)
            ch.serve_action(action, self.getFocusId(), self)

        def update_ui(self):
            super(DialogVideoList, self).update_ui()
            self.window.setProperty("Type", TRANSLATIONS[self.type])
            if self.type == "tv":
                self.window.getControl(5006).setVisible(False)
                self.window.getControl(5008).setVisible(False)
                self.window.getControl(5009).setVisible(False)
                self.window.getControl(5010).setVisible(False)
            else:
                self.window.getControl(5006).setVisible(True)
                self.window.getControl(5008).setVisible(True)
                self.window.getControl(5009).setVisible(True)
                self.window.getControl(5010).setVisible(True)

        def go_to_next_page(self):
            self.get_column()
            if self.page < self.total_pages:
                self.page += 1

        def go_to_prev_page(self):
            self.get_column()
            if self.page < 2:
                if self.order == "asc":
                    self.order = "desc"
                else:
                    self.order = "asc"
                self.update()
            elif self.page > 1:
                self.page -= 1

        @ch.action("contextmenu", 500)
        def context_menu(self):
            if self.listitem.getProperty("dbid") and self.listitem.getProperty("dbid") != 0: dbid = self.listitem.getProperty("dbid")
            else: dbid = 0
            busy = False
            item_id = self.listitem.getProperty("id")
            if self.type == "tv":
                imdb_id = fetch(get_tvshow_ids(item_id), "imdb_id")
                tvdb_id = fetch(get_tvshow_ids(item_id), "tvdb_id")
                #notify(header="TMDb-id: "+item_id, message=" IMDb-id: "+str(imdb_id).replace("tt",""), icon=self.listitem.getProperty("poster"))
            elif self.type == "episode":
                tvdb_id = self.listitem.getProperty("tvdb_id")
                imdb_id = self.listitem.getProperty("imdb_id")
            else: imdb_id = get_imdb_id_from_movie_id(item_id)
                #notify(header="TMDb-id: "+item_id, message=" IMDb-id: "+str(imdb_id).replace("tt",""), icon=self.listitem.getProperty("poster"))
            if self.type == "tv" or self.type == "episode":
                if self.listitem.getProperty("dbid"): listitems = [LANG(208)]
                else: listitems = [LANG(32239)]
            else: listitems = [LANG(208)]
            if self.listitem.getProperty("dbid"): listitems += [LANG(32233)]
            else: listitems += [LANG(32232)]
            listitems += [LANG(32051)]
            if self.logged_in:
                if self.type == "tv": listitems += [LANG(32169)]
                elif self.type == "episode": listitems += [LANG(32244)]
                else: listitems += [LANG(32113)]
                listitems += [LANG(14076)]
                if not self.type == "tv" or self.type == "episode": listitems += [LANG(32107)]
                if self.mode == "list": listitems += [LANG(32035)]
            if self.type == "movie" and xbmc.getCondVisibility("system.hasaddon(plugin.video.couchpotato_manager)"): 
                listitems += [LANG(32165)]
                if xbmc.getCondVisibility("system.hasaddon(plugin.video.trakt_list_manager)"): listitems += [LANG(32253)]
            if self.type == "tv" and xbmc.getCondVisibility("system.hasaddon(plugin.video.sickrage)"):
                listitems += [LANG(32166)]
            selection = xbmcgui.Dialog().select(heading=LANG(32151), list=listitems)
            if selection == 0:
                if self.type == "tv" or self.type == "episode":
                    if self.listitem.getProperty("dbid"):
                        show_playlist = xbmc.translatePath("special://profile/playlists/video/%s.xsp" % (tvdb_id, SETTING("player_alt")))
                        if os.path.exists(show_playlist):
                            url = show_playlist
                        else: url = 'plugin://plugin.video.metalliq-forqed/tv/play/%s/1/1/%s' % (tvdb_id, SETTING("player_alt"))
                    else: url = 'plugin://plugin.video.metalliq-forqed/tv/play/%s/1/1/%s' % (tvdb_id, SETTING("player_alt"))
                else:
                    if self.listitem.getProperty("dbid"): url = 'temp'
                    else: url = 'plugin://plugin.video.metalliq-forqed/movies/play/tmdb/%s/%s' % (item_id, SETTING("player_alt"))
                PLAYER.qlickplay(url, listitem=None, dbid=dbid, window=self)
            if selection == 1:
                if self.type == "tv" or self.type == "episode":
                    TVLibrary   = METALLIQ.getSetting("tv_library_folder")
                    TVPlaylists = METALLIQ.getSetting("tv_playlist_folder")
                    if self.listitem.getProperty("dbid"):
                        get_kodi_json(method="VideoLibrary.RemoveTVShow", params='{"tvshowid": %s}' % dbid)
                        if os.path.exists(xbmc.translatePath("%s%s.xsp" % (TVPlaylists, tvdb_id))):
                            os.remove(xbmc.translatePath("%s%s.xsp" % (TVPlaylists, tvdb_id)))
                        if os.path.exists(xbmc.translatePath("%s%s/" % (TVLibrary, tvdb_id))):
                            import shutil
                            shutil.rmtree(xbmc.translatePath("%s%s/" % (TVLibrary, tvdb_id)))
                            notify(header='Removed "%s" from library' % self.listitem.getProperty("TVShowTitle"), message="Refreshing %s list" % self.type, icon=self.listitem.getProperty("poster"), time=5000, sound=False)
                            after_add(type="tvshow")
                            self.update(force_update=True)
                            self.getControl(500).selectItem(self.position)
                        else:
                            notify(header='Item not added by QlickPlay' % self.listitem.getProperty("TVShowTitle"), message="Needs manual deletion", icon=self.listitem.getProperty("poster"), time=5000, sound=False)
                    else:
                        xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/tv/add_to_library/%s)" % tvdb_id)
                        notify(header='Added "%s" to library' % self.listitem.getProperty("TVShowTitle"), message="Starting library scan now", icon=self.listitem.getProperty("poster"), time=5000, sound=False)
                else:
                    MovieLibrary = METALLIQ.getSetting("movies_library_folder")
                    if self.listitem.getProperty("dbid"):
                        get_kodi_json(method="VideoLibrary.RemoveMovie", params='{"movieid": %s}' % dbid)
                        if os.path.exists(xbmc.translatePath("%s%s/" % (MovieLibrary, imdb_id))):
                            import shutil
                            shutil.rmtree(xbmc.translatePath("%s%s/" % (MovieLibrary, imdb_id)))
                            notify(header='Removed "%s" from library' % self.listitem.getProperty("title"), message="Exit &amp; re-enter to refresh", icon=self.listitem.getProperty("poster"), time=5000, sound=False)
                        else:
                            notify(header='Item not added by QlickPlay', message="Needs manual deletion", icon=self.listitem.getProperty("poster"), time=5000, sound=False)
                    else:
                        xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/movies/add_to_library/tmdb/%s)" % item_id)
                        notify(header='Added "%s" to library' % self.listitem.getProperty("title"), message="Starting library scan now", icon=self.listitem.getProperty("poster"), time=5000, sound=False)
                after_add(type=self.type)
                self.update(force_update=True)
                self.getControl(500).selectItem(self.position)
            if selection == 2:
                if self.type == "tv": url = "plugin://script.extendedinfo/?info=playtvtrailer&id=%s" % item_id
                elif self.type == "episode": url = "plugin://script.extendedinfo/?info=playtvtrailer&tvdb_id=%s" % tvdb_id
                elif self.type == "movie": url = "plugin://script.extendedinfo/?info=playtrailer&id=%s" % item_id
                PLAYER.qlickplay(url, listitem=None, dbid=0, window=self)
            if selection == 3:
                if self.logged_in:
                    if self.type == "tv" or self.type == "movie":
                        if set_rating_prompt(self.type, item_id):
                            xbmc.sleep(2000)
                            self.update(force_update=True)
                            self.getControl(500).selectItem(self.position)
                else:
                    if self.type == "episode":
                        path = xbmc.translatePath("special://profile/addon_data/script.extendedinfo/exclusions_tvdb.txt")
                        if xbmcvfs.exists(path): content = read_from_file(path, True).split("\n")
                        else: content = []
                        content.append("year - tvdb-id | TVShowTitle")
                        item = '%04d - %07d | %s' % (int(self.listitem.getProperty("year")), int(self.listitem.getProperty("tvdb_id")), self.listitem.getProperty("TVShowTitle"))
                        if item not in content:
                            content.append(item)
                            exclusions = ""
                            for item in content: exclusions = str(exclusions) + str(item) + "\n"
                            exclusion_file = xbmcvfs.File(path, 'w')
                            exclusion_file.write(exclusions.rstrip("\n"))
                            exclusion_file.close()
                        else: notify(message="TV show",header="allready in exclusion list",sound=False)
                    if self.type == "movie":
                        if xbmc.getCondVisibility("system.hasaddon(plugin.video.couchpotato_manager)"):
                            xbmc.executebuiltin("RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add?imdb_id=%s)" % imdb_id)
                        elif xbmc.getCondVisibility("system.hasaddon(plugin.video.trakt_list_manager)"):
                            xbmc.executebuiltin("RunPlugin(plugin://plugin.video.trakt_list_manager/movies/add?tmdb_id=%s)" % item_id)
                    elif self.type == "tv" or self.type == "episode":
                        xbmc.executebuiltin("RunPlugin(plugin://plugin.video.sickrage?action=addshow&tvdb_id=%s)" % tvdb_id)
                if self.type == "episode":
                    path = xbmc.translatePath("special://profile/addon_data/script.extendedinfo/exclusions_tvdb.txt")
                    if xbmcvfs.exists(path): content = read_from_file(path, True).split("\n")
                    else: content = []
                    content.append("year - tvdb-id | TVShowTitle")
                    item = '%04d - %07d | %s' % (int(self.listitem.getProperty("year")), int(self.listitem.getProperty("tvdb_id")), self.listitem.getProperty("TVShowTitle"))
                    if item not in content:
                        content.append(item)
                        exclusions = ""
                        for item in content: exclusions = str(exclusions) + str(item) + "\n"
                        exclusion_file = xbmcvfs.File(path, 'w')
                        exclusion_file.write(exclusions.rstrip("\n"))
                        exclusion_file.close()
                    else: notify(message="TV show",header="allready in exclusion list",sound=False)
            elif selection == 4:
                if self.logged_in:
                    change_fav_status(media_id=item_id,
                                      media_type=self.type,
                                      status="true")
                elif xbmc.getCondVisibility("system.hasaddon(plugin.video.trakt_list_manager)"):
                    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.trakt_list_manager/movies/add?tmdb_id=%s)" % item_id)
            elif selection == 5:
                if self.logged_in:
                    self.list_dialog(item_id)
                else:
                    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add?imdb_id=%s)" % imdb_id)
            elif selection == 6:
                if self.type == "tv" or self.type == "episode":
                    change_tvlist_status(list_id=self.list_id,
                                       tvshow_id=item_id,
                                       status=False)
                    self.update(force_update=True)
                    self.getControl(500).selectItem(self.position)
                else:
                    change_list_status(list_id=self.list_id,
                                       movie_id=item_id,
                                       status=False)
                    self.update(force_update=True)
                    self.getControl(500).selectItem(self.position)
            elif selection == 7:
                if xbmc.getCondVisibility("system.hasaddon(plugin.video.trakt_list_manager)"):
                    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.trakt_list_manager/movies/add?tmdb_id=%s)" % item_id)
                elif xbmc.getCondVisibility("system.hasaddon(plugin.video.couchpotato_manager)"):
                    xbmc.executebuiltin("RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add?imdb_id=%s)" % imdb_id)
            elif selection == 8:
                xbmc.executebuiltin("RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add?imdb_id=%s)" % imdb_id)

        def list_dialog(self, movie_id):
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            listitems = [LANG(32139)]
            account_lists = get_account_lists()
            for item in account_lists:
                listitems.append("%s (%i)" % (item["name"], item["item_count"]))
            listitems.append(LANG(32138))
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            index = xbmcgui.Dialog().select(heading=LANG(32136),
                                            list=listitems)
            if index == 0:
                listname = xbmcgui.Dialog().input(heading=LANG(32137),
                                                  type=xbmcgui.INPUT_ALPHANUM)
                if listname:
                    list_id = create_list(listname)
                    xbmc.sleep(1000)
                    change_list_status(list_id=list_id,
                                       movie_id=movie_id,
                                       status=True)
            elif index == len(listitems) - 1:
                self.remove_list_dialog(account_lists)
            elif index > 0:
                change_list_status(list_id=account_lists[index - 1]["id"],
                                   movie_id=movie_id,
                                   status=True)

        @ch.click(5001)
        def get_sort_type(self):
            if self.mode in ["favorites", "rating", "list"]:
                sort_key = self.mode
            else:
                sort_key = self.type
            listitems = [key for key in SORTS[sort_key].values()]
            sort_strings = [value for value in SORTS[sort_key].keys()]
            index = xbmcgui.Dialog().select(heading=LANG(32104),
                                            list=listitems)
            if index == -1:
                return None
            if sort_strings[index] == "vote_average":
                self.add_filter(key="vote_count.gte",
                                value="10",
                                typelabel="%s (%s)" % (LANG(32111), LANG(21406)),
                                label="10")
            self.sort = sort_strings[index]
            self.sort_label = listitems[index]
            self.update()

        def add_filter(self, key, value, typelabel, label):
            if ".gte" in key or ".lte" in key:
                super(DialogVideoList, self).add_filter(key=key,
                                                        value=value,
                                                        typelabel=typelabel,
                                                        label=label,
                                                        force_overwrite=True)
            else:
                super(DialogVideoList, self).add_filter(key=key,
                                                        value=value,
                                                        typelabel=typelabel,
                                                        label=label,
                                                        force_overwrite=False)

        @ch.click(5004)
        def toggle_order(self):
            if self.order == "asc":
                self.order = "desc"
            else:
                self.order = "asc"
            self.update()

        @ch.click(5007)
        def toggle_media_type(self):
            self.filters = []
            self.page = 1
            self.mode = "filter"
            if self.type == "tv":
                self.type = "movie"
            else:
                self.type = "tv"
            self.update()

        @ch.click(7000)
        def open_account_menu(self):
            if self.type == "tv":
                listitems = [LANG(32145)]
                if self.logged_in:
                    listitems.append(LANG(32144))
            else:
                listitems = [LANG(32135)]
                if self.logged_in:
                    listitems.append(LANG(32134))
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            if self.logged_in:
                account_lists = get_account_lists()
                for item in account_lists:
                    listitems.append("%s (%i)" % (item["name"], item["item_count"]))
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            index = xbmcgui.Dialog().select(heading=LANG(32136),
                                            list=listitems)
            if index == -1:
                pass
            elif index == 0:
                self.mode = "rating"
                self.sort = "created_at"
                self.sort_label = LANG(32157)
                self.filters = []
                self.page = 1
                self.update()
            elif index == 1:
                self.mode = "favorites"
                self.sort = "created_at"
                self.sort_label = LANG(32157)
                self.filters = []
                self.page = 1
                self.update()
            else:
                self.close()
                dialog = DialogVideoList(u'%s-VideoList.xml' % ADDON_ID, ADDON_PATH,
                                         color=self.color,
                                         filters=[],
                                         mode="list",
                                         list_id=account_lists[index - 2]["id"],
                                         filter_label=account_lists[index - 2]["name"])
                dialog.doModal()

        @ch.click(5002)
        def set_genre_filter(self):
            response = get_tmdb_data("genre/%s/list?language=%s&" % (self.type, SETTING("LanguageID")), 10)
            id_list = [item["id"] for item in response["genres"]]
            label_list = [item["name"] for item in response["genres"]]
            index = xbmcgui.Dialog().select(heading=LANG(32151),
                                            list=label_list)
            if index == -1:
                return None
            self.add_filter("with_genres", str(id_list[index]), LANG(135), label_list[index])
            self.mode = "filter"
            self.page = 1
            self.update()

        @ch.click(5012)
        def set_vote_count_filter(self):
            ret = True
            if not self.type == "tv":
                ret = xbmcgui.Dialog().yesno(heading=LANG(32151),
                                             line1=LANG(32106),
                                             nolabel=LANG(32150),
                                             yeslabel=LANG(32149))
            result = xbmcgui.Dialog().input(heading=LANG(32111),
                                            type=xbmcgui.INPUT_NUMERIC)
            if result:
                if ret:
                    self.add_filter("vote_count.%s" % "lte", result, LANG(32111), " < " + result)
                else:
                    self.add_filter("vote_count.%s" % "gte", result, LANG(32111), " > " + result)
                self.mode = "filter"
                self.page = 1
                self.update()

        @ch.click(5003)
        def set_year_filter(self):
            ret = xbmcgui.Dialog().yesno(heading=LANG(32151),
                                         line1=LANG(32106),
                                         nolabel=LANG(32150),
                                         yeslabel=LANG(32149))
            result = xbmcgui.Dialog().input(heading=LANG(345),
                                            type=xbmcgui.INPUT_NUMERIC)
            if not result:
                return None
            if ret:
                order = "lte"
                value = "%s-12-31" % result
                label = " < " + result
            else:
                order = "gte"
                value = "%s-01-01" % result
                label = " > " + result
            if self.type == "tv":
                self.add_filter("first_air_date.%s" % order, value, LANG(20416), label)
            else:
                self.add_filter("primary_release_date.%s" % order, value, LANG(345), label)
            self.mode = "filter"
            self.page = 1
            self.update()

        @ch.click(5008)
        def set_actor_filter(self):
            result = xbmcgui.Dialog().input(heading=LANG(16017),
                                            type=xbmcgui.INPUT_ALPHANUM)
            if not result or result == -1:
                return None
            response = get_person_info(result)
            if not response:
                return None
            self.add_filter("with_people", str(response["id"]), LANG(32156), response["name"])
            self.mode = "filter"
            self.page = 1
            self.update()

        @ch.click(500)
        def open_media(self):
            self.last_position = self.control.getSelectedPosition()
            media_type = self.listitem.getProperty("media_type")
            if media_type:
                self.type = media_type
            if self.type == "tv":
                wm.open_tvshow_info(prev_window=self,
                                    tvshow_id=self.listitem.getProperty("id"),
                                    dbid=self.listitem.getProperty("dbid"))
            elif self.type == "person":
                wm.open_actor_info(prev_window=self,
                                   actor_id=self.listitem.getProperty("id"))
            else:
                wm.open_movie_info(prev_window=self,
                                   movie_id=self.listitem.getProperty("id"),
                                   dbid=self.listitem.getProperty("dbid"))

        @ch.click(5010)
        def set_company_filter(self):
            result = xbmcgui.Dialog().input(heading=LANG(16017),
                                            type=xbmcgui.INPUT_ALPHANUM)
            if not result or result < 0:
                return None
            response = search_company(result)
            if len(response) > 1:
                selection = xbmcgui.Dialog().select(heading=LANG(32151),
                                                    list=[item["name"] for item in response])
                if selection > -1:
                    response = response[selection]
            elif response:
                response = response[0]
            else:
                notify("No company found")
            self.add_filter(key="with_companies",
                            value=str(response["id"]),
                            typelabel=LANG(20388),
                            label=response["name"])
            self.mode = "filter"
            self.page = 1
            self.update()

        @ch.click(5009)
        def set_keyword_filter(self):
            result = xbmcgui.Dialog().input(heading=LANG(16017),
                                            type=xbmcgui.INPUT_ALPHANUM)
            if not result or result == -1:
                return None
            response = get_keyword_id(result)
            if not response:
                return None
            self.add_filter("with_keywords", str(response["id"]), LANG(32114), response["name"])
            self.mode = "filter"
            self.page = 1
            self.update()

        @ch.click(5006)
        def set_certification_filter(self):
            response = get_certification_list(self.type)
            country_list = [key for key in response.keys()]
            index = xbmcgui.Dialog().select(heading=LANG(21879),
                                            list=country_list)
            if index == -1:
                return None
            country = country_list[index]
            cert_list = ["%s  -  %s" % (i["certification"], i["meaning"]) for i in response[country]]
            index = xbmcgui.Dialog().select(heading=LANG(32151),
                                            list=cert_list)
            if index == -1:
                return None
            cert = cert_list[index].split("  -  ")[0]
            self.add_filter("certification_country", country, LANG(32153), country)
            self.add_filter("certification", cert, LANG(32127), cert)
            self.page = 1
            self.mode = "filter"
            self.update()

        def fetch_data(self, force=False):  # TODO: rewrite
            sort_by = self.sort + "." + self.order
            if self.type == "tv":
                temp = "tv"
                rated = LANG(32145)
                starred = LANG(32144)
            else:
                temp = "movies"
                rated = LANG(32135)
                starred = LANG(32134)
            if self.mode == "search":
                url = "search/multi?query=%s&page=%i&include_adult=%s&" % (urllib.quote_plus(self.search_str), self.page, include_adult)
                if self.search_str:
                    self.filter_label = LANG(32146) % self.search_str
                else:
                    self.filter_label = ""
            elif self.mode == "list":
                url = "list/%s?language=%s&" % (str(self.list_id), SETTING("LanguageID"))
                # self.filter_label = LANG(32036)
            elif self.mode == "favorites":
                url = "account/%s/favorite/%s?language=%s&page=%i&session_id=%s&sort_by=%s&" % (get_account_info(), temp, SETTING("LanguageID"), self.page, get_session_id(), sort_by)
                self.filter_label = starred
            elif self.mode == "rating":
                force = True  # workaround, should be updated after setting rating
                if self.logged_in:
                    session_id = get_session_id()
                    if not session_id:
                        notify("Could not get session id")
                        return {"listitems": [],
                                "results_per_page": 0,
                                "total_results": 0}
                    url = "account/%s/rated/%s?language=%s&page=%i&session_id=%s&sort_by=%s&" % (get_account_info(), temp, SETTING("LanguageID"), self.page, session_id, sort_by)
                else:
                    session_id = get_guest_session_id()
                    if not session_id:
                        notify("Could not get session id")
                        return {"listitems": [],
                                "results_per_page": 0,
                                "total_results": 0}
                    url = "guest_session/%s/rated_movies?language=%s&" % (session_id, SETTING("LanguageID"))
                self.filter_label = rated
            else:
                self.set_filter_url()
                self.set_filter_label()
                url = "discover/%s?sort_by=%s&%slanguage=%s&page=%i&include_adult=%s&" % (self.type, sort_by, self.filter_url, SETTING("LanguageID"), int(self.page), include_adult)
            if force:
                response = get_tmdb_data(url=url,
                                         cache_days=0)
            else:
                response = get_tmdb_data(url=url,
                                         cache_days=2)
            if not response:
                return None
            if self.mode == "list":
                prettyprint(response)
                info = {"listitems": handle_tmdb_movies(results=response["items"],
                                                        local_first=True,
                                                        sortkey=None),
                        "results_per_page": 1,
                        "total_results": len(response["items"])}
                return info
            if "results" not in response:
                # self.close()
                return {"listitems": [],
                        "results_per_page": 0,
                        "total_results": 0}
            if not response["results"]:
                notify(LANG(284))
            if self.mode == "search":
                listitems = handle_tmdb_multi_search(response["results"])
            elif self.type == "movie":
                listitems = handle_tmdb_movies(results=response["results"],
                                               local_first=False,
                                               sortkey=None)
            else:
                listitems = handle_tmdb_tvshows(results=response["results"],
                                                local_first=False,
                                                sortkey=None)
            info = {"listitems": listitems,
                    "results_per_page": response["total_pages"],
                    "total_results": response["total_results"]}
            return info

    return DialogVideoList
