# -*- coding: utf-8 -*-
"""
    xml.py --- functions dealing with jen xml list format
    Copyright (C) 2017, Jen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import __builtin__
import datetime
import os
import re
import time
from threading import Thread

import koding
import requests
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import sys
import sqlite3

import base64,pickle,koding

from language import get_string as _
from resources.lib.plugin import run_hook
from resources.lib.util.context import get_context_items
from resources.lib.util.info import get_info
from resources.lib.util.url import replace_url, get_addon_url

CACHE_TIME = 120  # change to wanted cache time in seconds

ADDON = xbmcaddon.Addon()
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_data_folder = xbmc.translatePath('special://home/userdata/addon_data')
addon_data = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(addon_data, 'database.db')
main_cache_time = int(ADDON.getSetting("main_cache_time"))*60

class JenList(object):
    """
wrapper class for jen list functions
    """

    list_pattern = re.compile(
        '((?:<item>.+?</item>|<dir>.+?</dir>|<plugin>.+?</plugin>'
        '|<info>.+?</info>|'
        '<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail>'
        '<mode>[^<]+</mode>|'
        '<name>[^<]+</name><link>[^<]+</link><thumbnail>[^<]+</thumbnail>'
        '<date>[^<]+</date>))', re.MULTILINE | re.DOTALL)

    def __init__(self, url, cached=True):
        if cached:
            xml = run_hook("get_xml", url)
        else:
            xml = run_hook("get_xml_uncached", url)
        if not xml:
            if url.endswith(".xml") or url.startswith("http"):
                try:
                    xml = requests.get(url).content
                except Exception as e:
                    xml = None
                    koding.dolog("error: " + repr(e))
                    koding.dolog("url: " + repr(url))
                    koding.dolog("#####################")
            else:
                xml = url
        if xml:
            self.xml = xml
            self.content = ""
            self.list = JenList.list_pattern.findall(xml)
            info = JenItem(xml.split('<item>')[0].split('<dir>')[0])
            intro = info.get("intro", "")
            if intro:
                import resources.lib.sources as sources
                sources.get_sources(intro)
            self.playlister = info.get('poster', '0')
            self.list_image = replace_url(info.get("animated_thumbnail", ""))
            if not self.list_image:
                self.list_image = replace_url(
                    info.get('thumbnail', ADDON.getAddonInfo('icon')))
            self.list_fanart = replace_url(info.get("animated_fanart", ""))
            if not self.list_fanart:
                self.list_fanart = replace_url(info.get('fanart', "0"))
            if self.list_fanart == "0":
                theme = xbmcaddon.Addon().getSetting('theme')
                if theme and theme != 'DEFAULT' and theme != 'none':
                    self.list_fanart = self.set_theme(theme)
                else:
                    self.list_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
            self.metadata = {}
        else:
            self.list = []

    @staticmethod
    def set_theme(theme):
        """set jen theme"""
        import random
        theme_list = run_hook("get_theme_list")

        if theme.lower() == "user":
            user_theme_folder = os.path.join(
                xbmc.translatePath(
                    xbmcaddon.Addon().getSetting("cache_folder")),
                "theme")
            if os.path.isdir(user_theme_folder):
                user_files = []
                for ufile in os.listdir(user_theme_folder):
                    if os.path.isfile(os.path.join(user_theme_folder, ufile)):
                        user_files.append(
                            os.path.join(user_theme_folder, ufile))
                theme_list["user"] = user_files
            else:
                koding.dolog("huh?: " + repr(theme))
                return xbmcaddon.Addon().getAddonInfo('fanart')
        return replace_url(random.choice(theme_list[theme.lower()]))

    def get_raw_list(self):
        """returns the raw xml list of items"""
        return self.list

    def get_list(self, input_list=None, skip_meta=False, skip_dialog=False):
        """
        returns the list of items in a format suitable for kodiswift
        Returns:
        list of jen items
        """
        items = []
        meta = ADDON.getSetting("metadata") == "true"
        try:
            is_widget = __builtin__.JEN_WIDGET
        except:
            is_widget = False
        if is_widget:
            skip_dialog = True
        if input_list is None:
            input_list = self.list

        xbmc.log("input_list: " + repr(input_list))

        dialog = None
        dialog2 = None

        if not skip_dialog:
            if ADDON.getSetting("disable_metadata_dialog") == "false":
                dialog = xbmcgui.DialogProgress()
                addon_name = ADDON.getAddonInfo("name")
                dialog.create(addon_name, _("Loading items"))

        if meta and not skip_meta:
            info_thread = threadWithReturn(
                target=get_info, args=(input_list, dialog))
            info_thread.start()
        else:
            info_thread = None

        num_items = len(input_list)
        for index, item_xml in enumerate(input_list):
            if dialog2:
                percent = ((index + 1) * 100) / num_items
                dialog2.update(percent, _("processing item"),
                               "%s of %s" % (index + 1, num_items))
            result_item = self.process_item(item_xml)
            if result_item:
                items.append(result_item)
        if dialog2:
            dialog2.close()

        if info_thread:
            info = info_thread.join()  # wait till for thread to finish
            if info:
                skip = 0
                for index, item in enumerate(items):
                    if not item.get("summary", None) and not item.get("imdb", None):
                        continue
                    if index <= len(info) - 1:
                        for info_item in info[index + skip:]:
                            if not info_item:
                                break
                            if info_item.get("manual", ""):
                                item["info"]["plot"] = info_item["plot"]
                                break
                            if "imdb_id" in info_item:
                                if info_item["imdb_id"] == item["imdb"]:
                                    item["info"].update(info_item)
                                    break
                                else:
                                    skip = skip + 1
                            else:
                                break
                    else:
                        break

        for item in items:
            if not item.get("imdb", ""):
                continue
            match = koding.Get_From_Table("watched", {
                "identifier": item["imdb"],
                "season": item["season"],
                "episode": item["episode"]
            })
            if match:
                match = match[0]
                if match["watched"] and match["watched"] == "1":
                    item["info"]["playcount"] = 1
                    item["info"]["watched"] = 1

        if ADDON.getSetting("trailer_context") == "true":
            for item in items:
                if "trailer" in item["info"]:
                    try:
                        item["context"].append((_("Trailer"), "PlayMedia({0})".format(
                            item["info"]["trailer"])))
                    except:
                        pass
        return items

    def process_item(self, item_xml):
        hook_result = run_hook("process_item", item_xml)
        if hook_result:
            if hook_result.get("content", ""):
                self.content = hook_result["content"]
            return hook_result
        try:
            is_widget = __builtin__.JEN_WIDGET
        except:
            is_widget = False
        item = JenItem(item_xml)
        enable_gifs = xbmcaddon.Addon().getSetting('enable_gifs') == "true"
        if item.item_string.startswith("<item>"):
            title = item["title"]
            if title == "":
                title = item["name"]
                koding.dolog("depricated: <name>")
                koding.dolog("name: " + repr(title))
                koding.dolog("Use <title> instead of <name> in your xml")
                koding.dolog("#####################")
            try:
                title = xbmcaddon.Addon().getLocalizedString(int(title))
            except ValueError:
                pass
            is_playable = True
            mode = "get_sources"
            link = item_xml
        elif item.item_string.startswith("<dir>"):
            title = item["name"]
            if title == "":
                title = item["title"]
            try:
                title = xbmcaddon.Addon().getLocalizedString(int(title))
            except ValueError:
                pass
            if item["link"].startswith("message"):
                is_playable = True
                mode = "message"
                link = item["link"].replace("message(", "")[:-1]
                if link.startswith("http"):
                    text = requests.request("GET", replace_url(link), verify=False).content
                    link = text
            else:
                is_playable = False
                mode = "get_list"
                link = item["link"]
        elif item.item_string.startswith("<plugin>"):
            link = item["link"]
            title = item["name"]
            if title == "":
                title = item["title"]
            try:
                title = xbmcaddon.Addon().getLocalizedString(int(title))
            except ValueError:
                pass
            if link.endswith("openSettings"):
                is_playable = True
                link = ""
                mode = "Settings"
            elif link.endswith("developer"):
                import os
                is_playable = False
                link = '{"file_name":"testings.xml"}'
                mode = "Testings"
                path = xbmcaddon.Addon().getAddonInfo('profile')
                profile_path = xbmc.translatePath(path).decode('utf-8')
                test_file = os.path.join(profile_path, "testings.xml")
                if not os.path.exists(test_file):
                    return
            elif link.endswith("search"):
                is_playable = False
                link = ""
                mode = "Search"
            else:
                if "youtube" in link and ("user" in link or "playlist" in link):
                    is_playable = True
                    mode = 'get_sources'
                    link = item_xml
                else:
                    is_playable = True
                    mode = 'get_sources'
                    link = item_xml
        else:
            koding.dolog("other: " + repr(item), xbmc.LOGDEBUG)
            raise Exception()

        # filter out "unreleased"
        if title == "" or " /title" in title or "/ title" in title:
            return

        if is_widget:
            if mode == "message":
                return

        context = get_context_items(item)

        content = item["content"]
        if content == "boxset":
            content = "set"
        if content != '':
            self.content = content
        imdb = item["imdb"]
        season = item["season"] or '0'
        episode = item["episode"] or '0'
        year = item["year"] or '0'
        fanart = None
        if enable_gifs:
            fan_url = item.get("animated_fanart", "")
            if fan_url and fan_url != "0":
                fanart = replace_url(fan_url)
        if not fanart:
            fanart = replace_url(
                item.get("fanart", self.list_fanart), replace_gif=False)
        thumbnail = None
        if enable_gifs:
            thumb_url = item.get("animated_thumbnail", "")
            if thumb_url and thumb_url != "0":
                thumbnail = replace_url(thumb_url)
        if not thumbnail:
            thumbnail = replace_url(
                item.get("thumbnail", self.list_image), replace_gif=False)

        premiered = item.get("premiered", "")
        if premiered:
            try:
                today_tt = datetime.date.today().timetuple()
                premiered_tt = time.strptime(premiered, "%Y-%m-%d")
                if today_tt < premiered_tt:
                    title = "[COLORyellow]" + title + "[/COLOR]"
            except:
                koding.dolog("wrong premiered format")
                pass
        result_item = {
            'label': title,
            'icon': thumbnail,
            'fanart': fanart,
            'mode': mode,
            'url': link,
            'folder': not is_playable,
            'imdb': imdb,
            'content': content,
            'season': season,
            'episode': episode,
            'info': {},
            'year': year,
            'context': context,
            'plot': item.get("summary", None),
            "summary": item.get("summary", None)
        }
        if fanart:
            result_item["properties"] = {'fanart_image': fanart}
            result_item['fanart_small'] = fanart

        if content in ['movie', 'episode']:
            # only add watched data for applicable items
            result_item['info']['watched'] = 0
        return result_item

    def get_content_type(self):
        """return content type of list"""
        try:
            if self.content in ["movie", "set"]:
                return "movies"
            elif self.content == "tvshow":
                return "tvshows"
            elif self.content == "season":
                return "seasons"
            elif self.content == 'episode':
                return "episodes"
            elif self.content == 'artist':
                return "artists"
            elif self.content == 'album':
                return "albums"
            elif self.content == 'song':
                return "songs"
            else:
                return "files"
        except:
            return "files"


class JenItem(object):
    """represents an item in a jen xml list"""
    

    def __init__(self, item_xml):
        self.item_string = item_xml

    def get_tag_content(self, tag):
        """
        parses xml string for the content of a tag
        Args:
            collection: xml to search through
            tag: tag to find the content in
            default: value to return if nothing found
        Returns:
            tag content or default value if content is not found
        """
        return re.findall('<%s>(.+?)</%s>' % (tag, tag), self.item_string,
                          re.MULTILINE | re.DOTALL)

    def keys(self):
        """returns all keys in item"""
        return re.findall("<([^/]+?)>", self.item_string)[1:]

    def get(self, tag, default):
        """proxy for get_tag_content"""
        try:
            return self.get_tag_content(tag)[0]
        except IndexError:
            return default

    def getAll(self, tag):
        "get all tags contents" ""
        return self.get_tag_content(tag)

    def __getitem__(self, item):
        return self.get(item, "")

    def __eq__(self, other):
        return bool(self.item_string == other.item_string)

    def __repr__(self):
        return self.item_string


def display_list(items, content_type, pins):
    "display jen list in kodi"
    if ADDON.getSetting("enable_cache") == "true":
        Items = fetch_from_db(pins)
        if Items:
            import xbmcplugin
            import sys
            display_code(items, content_type)                                                 
        elif not Items:
            import xbmcplugin
            import sys
            hook_result = run_hook("display_list", items, content_type, pins)
            if hook_result:       
                return
            pins = pins.lower()     
            save_to_db(items, pins)
            display_code(items, content_type)           
    else:
        import xbmcplugin
        import sys
        hook_result = run_hook("display_list", items, content_type, pins)
        if hook_result:       
            return
        display_code(items, content_type)    

def display_list2(items, content_type, pins):
        save_to_db(items, pins)
        display_data(Items)              

def display_data(Items):
    for item in Items:           
        context_items = []
        if ADDON.getSetting("settings_context") == "true":
            context_items.append((_("Settings"),
                                 "RunPlugin({0})".format(
                                     get_addon_url("Settings"))))
        context_items.extend(item["context"])
        koding.Add_Dir(
            name=item["label"],
            url=item["url"],
            mode=item["mode"],
            folder=item["folder"],
            icon=item["icon"],
            fanart=item["fanart"],
            context_items=context_items,
            content_type="video",
            info_labels=item["info"],
            set_property=item.get("properties", {}),
            set_art={"poster": item["icon"]})    
    #xbmcplugin.setContent(int(sys.argv[1]), content_type)

def save_to_db(items, url):
    if not items or not url:
        return False
    url2 = clean_url(url)        
    koding.reset_db()
    test_spec = {
    "columns": {
        "value": "TEXT",
        "created": "TEXT"}
        }
    koding.Create_Table(url2, test_spec)
    set_val = base64.b64encode(pickle.dumps(items))        
    koding.Add_To_Table(url2,
                        {
                            "value": set_val,
                            "created": time.time()
                        })    
    table_name_spec = {
    "columns": {
        "name": "TEXT",}
        }
    koding.Create_Table("Table_names", table_name_spec)            
    plugin_table_name_spec = {
    "columns": {
        "name": "TEXT",}
        }
    koding.Create_Table("Plugin_table_names", plugin_table_name_spec)
    if "PLugin" in url:
        koding.Add_To_Table("Plugin_table_names",
                            {
                                "name": url2,
                            })
    else:                                 
        koding.Add_To_Table("Table_names",
                            {
                                "name": url2,
                            })        

def fetch_from_db(url):
    koding.reset_db()
    url2 = clean_url(url)
    match = koding.Get_All_From_Table(url2)
    if match:
        match = match[0]
        if not match["value"]:
            return None
        match_item = match["value"]
        try:
                result = pickle.loads(base64.b64decode(match_item))
        except:
                return None
        created_time = match["created"]
        if float(created_time) + int(main_cache_time) <= time.time():
            koding.Remove_Table(url2)
            db = sqlite3.connect('%s' % (database_loc))        
            cursor = db.cursor()
            db.execute("vacuum")
            db.commit()
            db.close()
            return result
        else:
            return result                
        return result
    else:
        return []


def clean_url(url):
   url = re.sub('\\\|/|\(|\)|\[|\]|\{|\}|-|:|;|\*|\?|"|\'|<|>|\_|\.|\?|%20|_', '', url).replace("|","").replace(" ","")
   return url            

def display_code(Items, content_type):
    for item in Items:           
        context_items = []
        if ADDON.getSetting("settings_context") == "true":
            context_items.append((_("Settings"),
                                 "RunPlugin({0})".format(
                                     get_addon_url("Settings"))))
        context_items.extend(item["context"])
        koding.Add_Dir(
            name=item["label"],
            url=item["url"],
            mode=item["mode"],
            folder=item["folder"],
            icon=item["icon"],
            fanart=item["fanart"],
            context_items=context_items,
            content_type="video",
            info_labels=item["info"],
            set_property=item.get("properties", {}),
            set_art={"poster": item["icon"]})                            
    xbmcplugin.setContent(int(sys.argv[1]), content_type)    

class threadWithReturn(Thread):
    def __init__(self, *args, **kwargs):
        super(threadWithReturn, self).__init__(*args, **kwargs)

        self._return = None

    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)

    def join(self, *args, **kwargs):
        super(threadWithReturn, self).join(*args, **kwargs)

        return self._return


