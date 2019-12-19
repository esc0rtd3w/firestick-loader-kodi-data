#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    plugin.audio.squeezebox
    Squeezelite Player for Kodi
    plugin_content.py
    plugin entry point t
'''

import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
from utils import log_msg, KODI_VERSION, log_exception, ADDON_ID, parse_duration
import urlparse
from urllib import quote_plus
import sys
import os
from operator import itemgetter
from lmsserver import LMSServer, TAGS_BASIC, TAGS_FULL, TAGS_ALBUM

PLUGIN_BASE = "plugin://%s/" % ADDON_ID
ADDON_HANDLE = int(sys.argv[1])


class PluginContent:
    '''Hidden plugin entry point providing some helper features'''
    params = {}
    lmsserver = None
    addon = None

    def __init__(self):
        win = xbmcgui.Window(10000)
        self.addon = xbmcaddon.Addon(id=ADDON_ID)

        # initialize lmsserver object - grab details from window props set by the service
        lmsplayerid = win.getProperty("lmsplayerid").decode("utf-8")
        lmshost = win.getProperty("lmshost").decode("utf-8")
        lmsport = win.getProperty("lmsport").decode("utf-8")
        
        if "select_output" in sys.argv[2]:
            self.select_output()
        elif not lmsplayerid:
            log_msg("Service not yet ready - try again later!")
            xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)
        else:
            # show plugin listing
            self.lmsserver = LMSServer(lmshost, lmsport, lmsplayerid)

            # initialize plugin listing
            try:
                self.params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '').decode("utf-8")))
                log_msg("plugin called with parameters: %s" % self.params, xbmc.LOGDEBUG)
                self.main()
            except Exception as exc:
                log_exception(__name__, exc)
                xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

        # cleanup when done processing
        del win
        del self.addon

    def main(self):
        '''main action, load correct function'''
        action = self.params.get("action", "")
        if action and hasattr(self.__class__, action):
            # launch module for action provided by this plugin
            getattr(self, action)()
        else:
            # load main listing
            self.menu()

    def albums(self):
        '''get albums from server'''
        params = self.params.get("params")
        xbmcplugin.setContent(ADDON_HANDLE, "albums")
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(132))
        request_str = "albums 0 100000 tags:%s" % TAGS_ALBUM
        if params:
            request_str += " %s" % params
            if "artist_id" in params:  # add All tracks entry
                self.create_generic_listitem("All Tracks", "DefaultMusicSongs.png", "tracks&params=%s" % params)
        result = self.lmsserver.send_request(request_str)
        if result:
            for item in result.get("albums_loop"):
                self.create_album_listitem(item)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def artists(self):
        '''get artists from server'''
        params = self.params.get("params")
        xbmcplugin.setContent(ADDON_HANDLE, "artists")
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(133))
        request_str = "artists 0 100000 tags:%s" % TAGS_FULL
        if params:
            request_str += " %s" % params
        result = self.lmsserver.send_request(request_str)
        if result:
            for item in result.get("artists_loop"):
                self.create_artist_listitem(item)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def tracks(self):
        '''get tracks from server'''
        params = self.params.get("params", "")
        xbmcplugin.setContent(ADDON_HANDLE, "songs")
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(134))
        request_str = "tracks 0 100000 tags:%s" % TAGS_BASIC
        if params:
            request_str += " %s" % params
        result = self.lmsserver.send_request(request_str)
        listitems = []
        if result:
            result = self.lmsserver.process_trackdetails(result["titles_loop"])
            result = [self.create_track_listitem(item) for item in result]
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def playlisttracks(self):
        '''get tracks from server'''
        playlistid = self.params.get("playlistid")
        xbmcplugin.setContent(ADDON_HANDLE, "songs")
        request_str = "playlists tracks 0 100000 tags:%s playlist_id:%s" % (TAGS_BASIC, playlistid)
        result = self.lmsserver.send_request(request_str)
        if result:
            result = self.lmsserver.process_trackdetails(result["playlisttracks_loop"])
            result = [self.create_track_listitem(item) for item in result]
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def currentplaylist(self):
        '''get the current playlist loaded in the player'''
        playlistid = self.params.get("playlistid")
        xbmcplugin.setContent(ADDON_HANDLE, "songs")
        result = self.lmsserver.cur_playlist(True)
        if result:
            result = [self.create_track_listitem(item) for item in result]
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def playlists(self):
        '''get playlists from server'''
        xbmcplugin.setContent(ADDON_HANDLE, "files")
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(136))
        params = self.params.get("params")
        request_str = "playlists 0 100000 tags:%s" % TAGS_FULL
        if params:
            request_str += " %s" % params
        result = self.lmsserver.send_request(request_str)
        if result:
            for item in result.get("playlists_loop"):
                cmd = "playlisttracks&playlistid=%s" % item["id"]
                self.create_generic_listitem(item["playlist"], "DefaultMusicPlaylists.png", cmd)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def genres(self):
        '''get genres from server'''
        xbmcplugin.setContent(ADDON_HANDLE, "files")
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(135))
        params = self.params.get("params")
        request_str = "genres 0 100000 tags:%s" % TAGS_FULL
        if params:
            request_str += " %s" % params
        result = self.lmsserver.send_request(request_str)
        if result:
            for item in result.get("genres_loop"):
                cmd = "tracks&params=genre_id:%s" % item["id"]
                thumb = self.lmsserver.get_thumb(item)
                contextmenu = []
                params = quote_plus("playlist loadalbum %s * *" % item["genre"])
                contextmenu.append((self.addon.getLocalizedString(32203),
                                    "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
                params = quote_plus("playlist insertalbum %s * *" % item["genre"])
                contextmenu.append((self.addon.getLocalizedString(32204),
                                    "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
                params = quote_plus("playlist addalbum %s * *" % item["genre"])
                contextmenu.append((self.addon.getLocalizedString(32205),
                                    "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
                self.create_generic_listitem(item["genre"], thumb, cmd, True, contextmenu)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def years(self):
        '''get years from server'''
        xbmcplugin.setContent(ADDON_HANDLE, "files")
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(652))
        params = self.params.get("params")
        request_str = "years 0 100000 tags:%s" % TAGS_FULL
        if params:
            request_str += " %s" % params
        result = self.lmsserver.send_request(request_str)
        if result:
            for item in result.get("years_loop"):
                cmd = "albums&params=year:%s" % item["year"]
                thumb = self.lmsserver.get_thumb(item)
                self.create_generic_listitem("%s" % item["year"], thumb, cmd)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def musicfolder(self):
        '''explore musicfolder on the server'''
        xbmcplugin.setContent(ADDON_HANDLE, "files")
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(744))
        params = self.params.get("params")
        request_str = "musicfolder 0 100000 tags:%s" % TAGS_FULL
        if params:
            request_str += " %s" % params
        result = self.lmsserver.send_request(request_str)
        if result:
            for item in result.get("folder_loop"):
                thumb = self.lmsserver.get_thumb(item)
                if item["type"] == "track":
                    item = self.get_songinfo(item["url"])
                    self.create_track_listitem(item)
                elif item["type"] == "playlist":
                    cmd = "command&params=playlist play %s" % item["url"]
                    self.create_generic_listitem("%s" % item["filename"], thumb, cmd, False)
                else:
                    cmd = "musicfolder&params=folder_id:%s" % item["id"]
                    self.create_generic_listitem("%s" % item["filename"], thumb, cmd)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def favorites(self):
        '''get favorites from server'''
        xbmcplugin.setContent(ADDON_HANDLE, "files")
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(1036))
        request_str = "favorites items 0 100000 want_url:1 tags:%s" % TAGS_FULL
        params = self.params.get("params")
        if params:
            request_str += " %s" % params
        result = self.lmsserver.send_request(request_str)
        if result:
            for item in result.get("loop_loop"):
                thumb = self.lmsserver.get_thumb(item)
                if item.get("isaudio") and "title" in item:
                    track_details = self.lmsserver.trackdetails(item)
                    self.create_track_listitem(track_details)
                elif item["isaudio"] and "url" in item:
                    result = self.lmsserver.send_request("songinfo 0 100 tags:%s url:%s" % (TAGS_FULL, item["url"]))
                    cmd = "command&params=" + quote_plus("favorites playlist play item_id:%s" % item["id"])
                    self.create_generic_listitem(item["name"], thumb, cmd, False)
                else:
                    cmd = "favorites&params=item_id:%s" % item["id"]
                    self.create_generic_listitem(item["name"], thumb, cmd)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def get_menu(self, node):
        '''grabs the menu for this player'''
        menu_items = []
        root_menu = self.lmsserver.send_request("menu items 0 1000 direct:1")
        for item in root_menu["item_loop"]:
            if item["node"] == node or (node == "apps" and "isApp" in item):
                actionstr = ""
                icon = self.lmsserver.get_thumb(item)
                if "isANode" in item and item["isANode"]:
                    actionstr = "menu&node=%s" % item["id"]
                elif "actions" in item and "go" in item["actions"]:

                    # library nodes
                    if "browselibrary" in item["actions"]["go"]["cmd"]:
                        action = item["actions"]["go"]["params"]["mode"]
                        if "albums" in action.lower():
                            action = "albums"
                        elif "tracks" in action.lower():
                            action = "tracks"
                        elif "artists" in action.lower():
                            action = "artists"
                        elif "bmf" in action:
                            action = "musicfolder"
                        elif "filesystem" in action:
                            continue  # skip filesystem entry
                        for key, value in item["actions"]["go"]["params"].iteritems():
                            if not key in ["mode", "menu"]:
                                actionstr += "%s:%s " % (key, value.replace("%s", "1").replace(" ", "[SP]"))
                        actionstr += " library_id:%s" % item["id"]
                        actionstr = "%s&params=%s" % (action, quote_plus(actionstr))
                    elif "selectVirtualLibrary" in item["actions"]["go"]["cmd"]:
                        continue  # skip virtual library entry
                    elif "radios" in item["actions"]["go"]["cmd"]:
                        actionstr = "radios"
                    elif "globalsearch" in item["actions"]["go"]["cmd"]:
                        actionstr = "globalsearch"
                    elif "myapps" in item["actions"]["go"]["cmd"]:
                        actionstr = "apps"
                    elif "appgallery" in item["actions"]["go"]["cmd"]:
                        continue  # do not show app gallery directly on homescreen
                    elif "favorites" in item["actions"]["go"]["cmd"]:
                        actionstr = "favorites"
                    else:
                        # other nodes
                        for cmd in item["actions"]["go"]["cmd"]:
                            if cmd == "items":
                                actionstr += "items 0 100000 "
                            else:
                                actionstr += "%s " % cmd
                        if "params" in item["actions"]["go"]:
                            for key, value in item["actions"]["go"]["params"].iteritems():
                                if not "menu" in key:
                                    actionstr += "%s:%s " % (key, value)
                        actionstr = "browse&params=%s" % quote_plus(actionstr)
                if actionstr:
                    menu_item = {
                        "label": item["text"],
                        "cmd": actionstr,
                        "icon": icon,
                        "weight": item.get("weight", 0)}
                    menu_items.append(menu_item)
        return sorted(menu_items, key=itemgetter('weight'))

    def menu(self):
        node = self.params.get("node", "home")
        # show current playlist in menu
        if node == "home":
            result = self.lmsserver.send_request("playlist tracks ?")
            if result:
                count = int(result["_tracks"])
                if count > 0:
                    self.create_generic_listitem(xbmc.getLocalizedString(13350), "", "currentplaylist")
        for item in self.get_menu(node):
            thumb = self.lmsserver.get_thumb(item)
            self.create_generic_listitem(item["label"], thumb, item["cmd"])
        # show sync settings in menu
        if node == "home":
            self.create_generic_listitem(self.addon.getLocalizedString(32206), "", "syncsettings")
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def search(self):
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(19140))
        xbmcplugin.setContent(ADDON_HANDLE, "files")
        kb = xbmc.Keyboard('', xbmc.getLocalizedString(16017))
        kb.doModal()
        if kb.isConfirmed():
            searchterm = kb.getText().replace(" ", "[SP]")
            result = self.lmsserver.send_request("search 0 1 term:%s" % searchterm)
            if result:
                if result.get("artists_count"):  # artist items
                    label = "Artists (%s)" % result["artists_count"]
                    cmd = "artists&params=search:%s" % searchterm
                    self.create_generic_listitem(label, "DefaultMusicArtists.png", cmd)
                elif result.get("contributors_count"):  # artist items alt
                    label = "Artists (%s)" % result["contributors_count"]
                    cmd = "artists&params=search:%s" % searchterm
                    self.create_generic_listitem(label, "DefaultMusicArtists.png", cmd)
                if result.get("albums_count"):  # album items
                    label = "Albums (%s)" % result["albums_count"]
                    cmd = "albums&params=search:%s" % searchterm
                    self.create_generic_listitem(label, "DefaultMusicAlbums.png", cmd)
                if result.get("tracks_count"):  # track items
                    label = "Songs (%s)" % result["tracks_count"]
                    cmd = "tracks&params=search:%s" % searchterm
                    self.create_generic_listitem(label, "DefaultMusicSongs.png", cmd)
                if result.get("genres_count"):  # genre items
                    label = "Genres (%s)" % result["genres_count"]
                    cmd = "genres&params=search:%s" % searchterm
                    self.create_generic_listitem(label, "DefaultMusicGenres.png", cmd)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def globalsearch(self):
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(19140))
        xbmcplugin.setContent(ADDON_HANDLE, "files")
        kb = xbmc.Keyboard('', xbmc.getLocalizedString(16017))
        kb.doModal()
        if kb.isConfirmed():
            searchterm = kb.getText().replace(" ", "[SP]")
            result = self.lmsserver.send_request("globalsearch items 0 10 search:%s" % searchterm)
            for item in result["loop_loop"]:
                params = "globalsearch items 0 100 item_id:%s" % item["id"]
                cmd = "browse&params=%s" % quote_plus(params)
                self.create_generic_listitem(item["name"], "DefaultMusicSearch.png", cmd)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def apps(self):
        '''get apps from server'''
        self.params["params"] = "myapps items 0 100000"
        self.browse()

    def get_redirect(self, appname):
        '''workaround to get app command redirects'''
        cmd = ""
        all_apps = self.lmsserver.send_request("apps 0 100000")["appss_loop"]
        for app in all_apps:
            if app["name"] == appname:
                # match found
                cmd = app["cmd"]
        return cmd

    def browse(self):
        '''browse generic (app/radio) listing'''
        request_str = self.params.get("params")
        contenttype = self.params.get("contenttype", "files")
        xbmcplugin.setContent(ADDON_HANDLE, contenttype)
        if "__TAGGEDINPUT__" in request_str:
            kb = xbmc.Keyboard('', xbmc.getLocalizedString(16017))
            kb.doModal()
            if kb.isConfirmed():
                search = kb.getText().replace(" ", "[SP]")
            request_str = request_str.replace("__TAGGEDINPUT__", search)
        if not "tags:" in request_str:
            request_str += " tags:%s wantMetadata:1" % TAGS_FULL
        result = self.lmsserver.send_request(request_str)
        if "item_loop" in result:
            result = result["item_loop"]
        else:
            result = result["loop_loop"]
        for item in result:
            thumb = self.lmsserver.get_thumb(item)
            app = request_str.split(" ")[0]
            itemtype = item.get("type", "")
            if "actions" in item:
                actionstr = ""
                action_key = "go"
                is_folder = True
                if "do" in item["actions"]:
                    action_key = "do"
                    is_folder = False
                if action_key in item["actions"] and "cmd" in item["actions"][action_key]:
                    for cmd in item["actions"][action_key]["cmd"]:
                        if cmd == "items":
                            actionstr += "items 0 100000 "
                        else:
                            actionstr += "%s " % cmd
                if action_key in item["actions"] and "params" in item["actions"][action_key]:
                    for key, value in item["actions"][action_key]["params"].iteritems():
                        if not "menu" in key:
                            actionstr += "%s:%s " % (key, value)
                if actionstr:
                    if is_folder:
                        cmd = "browse&params=%s" % quote_plus(actionstr)
                    else:
                        cmd = "command&params=%s" % quote_plus(actionstr)
                    thumb = self.lmsserver.get_thumb(item)
                    self.create_generic_listitem(item["text"], thumb, cmd, is_folder)
            elif item.get("isaudio"):
                # playable item
                contextmenu = []
                params = quote_plus("%s playlist play item_id:%s" % (app, item["id"]))
                contextmenu.append((self.addon.getLocalizedString(32203),
                                    "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
                params = quote_plus("%s playlist insert item_id:%s" % (app, item["id"]))
                contextmenu.append((self.addon.getLocalizedString(32204),
                                    "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
                params = quote_plus("%s playlist add item_id:%s" % (app, item["id"]))
                contextmenu.append((self.addon.getLocalizedString(32205),
                                    "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
                if itemtype in ["playlist", "link"]:
                    params = quote_plus("%s items 0 100000 item_id:%s" % (app, item["id"]))
                    contextmenu.append(
                        ("Browse", "Container.Update(%s?action=browse&params=%s)" %
                         (PLUGIN_BASE, params)))
                cmd = "%s playlist play item_id:%s" % (app, item["id"])
                cmd = "command&params=%s" % quote_plus(cmd)
                self.create_generic_listitem(item["name"], thumb, cmd, False, contextmenu)
            else:
                # folder item
                contentttype = self.get_app_contenttype(item)
                if itemtype == "redirect":
                    app = self.get_redirect(item["name"])
                    params = "%s items 0 10000" % app
                elif itemtype == "search":
                    params = quote_plus("%s items 0 100000 search:__TAGGEDINPUT__" % app)
                elif "id" in item:
                    # subnode for app/radio
                    params = quote_plus("%s items 0 100000 item_id:%s" % (app, item["id"]))
                elif "text" in item:
                    # text node without any actions ?
                    self.create_generic_listitem(item["text"], thumb, "browse&params=%s" % request_str)
                    continue
                cmd = "browse&params=%s&contentttype=%s" % (params, contentttype)
                self.create_generic_listitem(item["name"], thumb, cmd)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def syncsettings(self):
        '''sync settings (The synchroniser plugin)'''
        xbmcplugin.setContent(ADDON_HANDLE, "files")
        result = self.lmsserver.send_request("syncTop")
        if result and "item_loop" in result and result["item_loop"]:
            # The synchroniser plugin present
            # sync all to this player
            cmd = "command&params=syncSyncToMe&refresh=true"
            self.create_generic_listitem(self.addon.getLocalizedString(32207), "", cmd, False)
            # sync groups
            for item in result["item_loop"]:
                if "syncSyncToSet" in item["actions"]["do"]["params"]["menu"]:
                    cmd = quote_plus("syncSyncToSet set:%s" % item["actions"]["do"]["params"]["set"])
                    cmd = "command&params=%s" % cmd
                    self.create_generic_listitem(item["text"], "", cmd, False)
            # desync all
            cmd = "command&params=syncUnsync&refresh=true"
            self.create_generic_listitem(self.addon.getLocalizedString(32208), "", cmd, False)
        else:
            # fall back to legacy LMS method to set syncing....
            result = self.lmsserver.send_request("syncsettings 0 100")
            for item in result["item_loop"]:
                if "actions" in item:
                    # player entry
                    syncwith = item["actions"]["do"]["params"]["syncWith"]
                    unsyncwith = item["actions"]["do"]["params"]["unsyncWith"]
                    label = item["text"]
                    if unsyncwith != 0 and not syncwith == 0:
                        label += " [SYNC]"
                    actionstr = "jivesync syncWith:%s unsyncWith:%s" % (syncwith, unsyncwith)
                    cmd = "command&params=%s&refresh=true" % quote_plus(actionstr)
                    self.create_generic_listitem(label, "", cmd, False)
                else:
                    # header with no action
                    self.create_generic_listitem(item["text"], "", "syncsettings")
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def radios(self):
        '''get radio items'''
        xbmcplugin.setProperty(ADDON_HANDLE, 'FolderName', xbmc.getLocalizedString(19183))
        xbmcplugin.setContent(ADDON_HANDLE, "files")
        request_str = "radios 0 100000 tags:%s" % TAGS_FULL
        result = self.lmsserver.send_request(request_str)
        if result:
            for item in result.get("radioss_loop"):
                if item["cmd"] == "search":
                    params = "%s items 0 100000 search:__TAGGEDINPUT__" % item["cmd"]
                else:
                    params = params = "%s items 0 100000" % item["cmd"]
                cmd = "browse&params=%s" % quote_plus(params)
                thumb = self.lmsserver.get_thumb(item)
                self.create_generic_listitem(item["name"], thumb, cmd)
        xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(handle=ADDON_HANDLE)

    def get_app_contenttype(self, item):
        '''try to parse the contenttype from the details'''
        contenttype = ""
        if "url" in item:
            url = item["url"]
            if "whatsnew" in url:
                contenttype = "albums"
            elif "spotify:playlist" in url:
                contenttype = "songs"
            elif "categories" in url:
                contenttype = "albums"
            elif "myAlbums" in url:
                contenttype = "albums"
            elif "myArtists" in url:
                contenttype = "artists"
            elif "mySongs" in url:
                contenttype = "songs"
            elif "playlists" in url:
                contenttype = "playlists"
        return contenttype

    def create_artist_listitem(self, lms_item):
        '''Create Kodi listitem from LMS artist details'''
        thumb = self.lmsserver.get_thumb(lms_item)
        listitem = xbmcgui.ListItem(lms_item.get("artist"))
        listitem.setInfo('music',
                         {
                             'title': lms_item.get("artist"),
                             'artist': lms_item.get("artist"),
                             'rating': lms_item.get("rating"),
                             'genre': lms_item.get("genre"),
                             'year': lms_item.get("year"),
                             'mediatype': "artist"
                         })
        listitem.setArt({"thumb": thumb})
        listitem.setIconImage(thumb)
        listitem.setThumbnailImage(thumb)
        listitem.setProperty("DBYPE", "artist")
        # contextmenu
        contextmenu = []
        params = quote_plus("playlist loadalbum * %s *" % lms_item["artist"].encode("utf-8"))
        contextmenu.append((self.addon.getLocalizedString(32203),
                            "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
        params = quote_plus("playlist insertalbum * %s *" % lms_item["artist"].encode("utf-8"))
        contextmenu.append((self.addon.getLocalizedString(32204),
                            "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
        params = quote_plus("playlist addalbum * %s *" % lms_item["artist"].encode("utf-8"))
        contextmenu.append((self.addon.getLocalizedString(32205),
                            "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
        listitem.addContextMenuItems(contextmenu, True)
        url = "plugin://plugin.audio.squeezebox?action=albums&params=artist_id:%s" % lms_item.get("id")
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE,
                                    url=url, listitem=listitem, isFolder=True)

    def get_songinfo(self, url):
        '''get songinfo for given path'''
        result = {}
        track_details = self.lmsserver.send_request("songinfo 0 100 url:%s tags:dguxcyajlKRAG" % url)
        if track_details:
            # songdetails is really weird formatted in the server response
            for item in track_details["songinfo_loop"]:
                if isinstance(item, dict):
                    for key, value in item.iteritems():
                        result[key] = value
        return result

    def create_album_listitem(self, lms_item):
        '''Create Kodi listitem from LMS album details'''
        thumb = self.lmsserver.get_thumb(lms_item)
        listitem = xbmcgui.ListItem(lms_item.get("album"))
        listitem.setInfo('music',
                         {
                             'title': lms_item.get("album"),
                             'artist': lms_item.get("artist"),
                             'album': lms_item.get("album"),
                             'rating': lms_item.get("rating"),
                             'genre': lms_item.get("genre"),
                             'year': lms_item.get("year"),
                             'mediatype': 'album'
                         })
        listitem.setArt({"thumb": thumb})
        listitem.setProperty("DBYPE", "album")
        listitem.setIconImage(thumb)
        listitem.setThumbnailImage(thumb)
        url = "plugin://plugin.audio.squeezebox?action=tracks&params=album_id:%s" % lms_item.get("id")
        # contextmenu
        contextmenu = []
        try:
            special_char = "*".encode("utf-8")
            params = quote_plus(
                u"playlist loadalbum %s %s %s" %
                (special_char, lms_item["artist"].replace(
                    " ", "[SP]"), lms_item["album"].replace(
                    " ", "[SP]")))
            contextmenu.append((self.addon.getLocalizedString(32201),
                                "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
            contextmenu.append((self.addon.getLocalizedString(32202),
                                "Container.Update(%s)" % url))
        except:
            pass
        listitem.addContextMenuItems(contextmenu, True)
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE,
                                    url=url, listitem=listitem, isFolder=True)

    def create_track_listitem(self, lms_item):
        '''Create Kodi listitem from LMS track details'''
        listitem = xbmcgui.ListItem(lms_item["title"])
        listitem.setInfo('music',
                         {
                             'title': lms_item["title"],
                             'artist': lms_item["trackartist"],
                             'album': lms_item.get("album"),
                             'duration': parse_duration(lms_item.get("duration")),
                             'discnumber': lms_item.get("disc"),
                             'rating': lms_item.get("rating"),
                             'genre': lms_item["genres"],
                             'tracknumber': lms_item.get("track_number"),
                             'lyrics': lms_item.get("lyrics"),
                             'year': lms_item.get("year"),
                             'comment': lms_item.get("comment"),
                             "mediatype": "song"
                         })
        listitem.setArt({"thumb": lms_item["thumb"]})
        listitem.setIconImage(lms_item["thumb"])
        listitem.setThumbnailImage(lms_item["thumb"])
        listitem.setProperty("isPlayable", "false")
        listitem.setProperty("DBYPE", "song")
        cmd = quote_plus("playlist play %s" % lms_item.get("url"))

        contextmenu = []
        if "playlist index" in lms_item and lms_item["playlist index"]:
            # contextmenu for now playing list
            pl_index = int(lms_item["playlist index"])
            pl_pos = int(self.lmsserver.cur_index)
            cmd = quote_plus("playlist index %s" % pl_index)
            params = quote_plus("playlist index %s" % pl_index)
            contextmenu.append((self.addon.getLocalizedString(32203),
                                "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
            contextmenu.append((self.addon.getLocalizedString(32204),
                                "RunPlugin(%s?action=playlistplaynext&params=%s)" % (PLUGIN_BASE, pl_index)))
            params = quote_plus("playlist move %s +1" % pl_index)
            contextmenu.append((xbmc.getLocalizedString(13332),
                                "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
            params = quote_plus("playlist move %s -1" % pl_index)
            contextmenu.append((xbmc.getLocalizedString(13333),
                                "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
            params = quote_plus("playlist delete %s" % pl_index)
            contextmenu.append((xbmc.getLocalizedString(117),
                                "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
            params = quote_plus(xbmc.getLocalizedString(192))
            contextmenu.append(("Clear playlist",
                                "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
        else:
            # normal contextmenu
            params = quote_plus("playlist play %s" % lms_item["url"])
            contextmenu.append((self.addon.getLocalizedString(32203),
                                "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
            params = quote_plus("playlist insert %s" % lms_item["url"])
            contextmenu.append((self.addon.getLocalizedString(32204),
                                "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
            params = quote_plus("playlist add %s" % lms_item["url"])
            contextmenu.append((self.addon.getLocalizedString(32205),
                                "RunPlugin(%s?action=command&params=%s)" % (PLUGIN_BASE, params)))
        listitem.addContextMenuItems(contextmenu, True)
        url = "plugin://plugin.audio.squeezebox?action=command&params=%s" % cmd
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE,
                                    url=url, listitem=listitem, isFolder=False)

    def create_generic_listitem(self, label, icon, cmd, is_folder=True, contextmenu=None):
        listitem = xbmcgui.ListItem(label, iconImage=icon)
        url = "plugin://plugin.audio.squeezebox?action=%s" % cmd
        if not contextmenu:
            contextmenu = []
        listitem.addContextMenuItems(contextmenu, True)
        listitem.setProperty("isPlayable", "false")
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE,
                                    url=url, listitem=listitem, isFolder=is_folder)

    def playlistplaynext(self):
        _id = self.params.get("params")
        result = self.lmsserver.send_request("playlist index ?")
        if result:
            pl_pos = int(result["_index"])
            if int(_id) > pl_pos:
                pl_pos += 1
            cmd = "playlist move %s %s" % (_id, pl_pos)
            self.lmsserver.send_request(cmd)

    def command(self):
        '''play item or other command'''
        cmd = self.params.get("params")
        refresh = self.params.get("refresh", "") == "true"
        self.lmsserver.send_request(cmd)
        if refresh:
            xbmc.executebuiltin("Container.Refresh")
            
    def select_output(self):
        '''helper to select the output device for squeezelite'''
        xbmc.executebuiltin("ActivateWindow(busydialog")
        from utils import get_audiodevices
        devices = ["auto"]
        devices += get_audiodevices()
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        dialog = xbmcgui.Dialog()
        ret = dialog.select("Detected audio devices", devices)
        if ret != -1:
            selected_device = devices[ret].split("-")[0].strip()
            self.addon.setSetting("output_device", selected_device)
            dialog.ok("restart required", "a restart is required to make the changes effective")
        del dialog
            