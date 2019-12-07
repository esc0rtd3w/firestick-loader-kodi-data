# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import sys
import xbmc
import xbmcplugin
import xbmcgui
from resources.lib.process import start_info_actions
from resources.lib.Utils import *
from resources.lib.TheMovieDB import check_login

class Main:

    def __init__(self):
        xbmc.log("version %s started" % ADDON_VERSION)
        xbmc.executebuiltin('SetProperty(extendedinfo_running,True,home)')
        if xbmc.getCondVisibility('Skin.String(WindowColorMain,'+COLORMAIN+')') == False: xbmc.executebuiltin('Skin.SetString(WindowColorMain,'+COLORMAIN+')')
        elif xbmc.getCondVisibility('Skin.String(WindowColorThemed,'+COLORTHEMED+')') == False: xbmc.executebuiltin('Skin.SetString(WindowColorThemed,'+COLORTHEMED+')')
        self._parse_argv()
        logged_in = check_login()
        if self.infos:
            start_info_actions(self.infos, self.params)
        else:
            videos = {"ytvideos": "yt - %s [I](Youtube)[/I]" % LANG(32231),
                      "ytchannels": "yt - %s [I](Youtube)[/I]" % LANG(32229),
                      "ytplaylists": "yt - %s [I](Youtube)[/I]" % LANG(32230),}
            movies = {"trendingmovies": "tr - %s [I](Trakt.tv)[/I]" % LANG(32047),
                      "incinemas": "tm - %s [I](TheMovieDB)[/I]" % LANG(32042),
                      "upcoming": "tm - %s [I](TheMovieDB)[/I]" % LANG(32043),
                      "topratedmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32046),
                      "popularmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32044),
                      "allmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32248),}
            tvshows = {"airingshows": "tr - %s [I](Trakt.tv)[/I]" % LANG(32028),
                       "premiered": "tr - %s [I](Trakt.tv)[/I]" % LANG(32029),
                       "trendingshows": "tr - %s [I](Trakt.tv)[/I]" % LANG(32032),
                       "airingtodaytvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32038),
                       "onairtvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32039),
                       "topratedtvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32040),
                       "populartvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32041),
                       "alltvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32249),}
            if logged_in:
                personal_movies = {"accountlists": "tm - %s [I](TheMovieDB)[/I]" % LANG(32045),
                                   "starredmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32134),
                                   "ratedmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32135),}
                personal_tvshows = {"starredtvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32144),
                                    "ratedtvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32145),}
            else:
                personal_movies = {}
                personal_tvshows = {}
            if xbmc.getCondVisibility("Library.HasContent(Movies)"):
                library_movies = {"libraryinprogressmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32241),
                                  "librarylatestmovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32242),
                                  "libraryrandommovies": "tm - %s [I](TheMovieDB)[/I]" % LANG(32243),}
            else: library_movies = {}
            if xbmc.getCondVisibility("Library.HasContent(TVShows)"):
                library_tvshows = {"libraryinprogresstvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32245),
                                   "librarylatesttvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32246),
                                   "libraryrandomtvshows": "tm - %s [I](TheMovieDB)[/I]" % LANG(32247),}
            else: library_tvshows = {}
            xbmcplugin.setContent(self.handle, 'videos')
            movie_items = merge_dicts(movies, personal_movies, library_movies)
            tvshow_items = merge_dicts(tvshows, personal_tvshows, library_tvshows)
            youtube_items = videos
            for key, value in iter(sorted(movie_items.iteritems())):
                temp = {}
                temp['value'] = value
                image_code = temp['value'][:2]
                label = temp['value'][5:]
                li = xbmcgui.ListItem(label, iconImage="%s/resources/skins/Default/media/%s.png" % (ADDON_PATH, image_code), thumbnailImage="%s/resources/skins/Default/media/%s.png" % (ADDON_PATH, image_code))
                li.setProperty('fanart_image', "special://home/addons/script.extendedinfo/resources/skins/Default/media/%s-fanart.jpg" % image_code)
                if SCRIPT == "true" and "yt" not in value: url = 'plugin://script.extendedinfo?info=%s&type=script' % key
                else: url = 'plugin://script.extendedinfo?info=%s' % key
                xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=True)
            for key, value in iter(sorted(tvshow_items.iteritems())):
                temp = {}
                temp['value'] = value
                image_code = temp['value'][:2]
                label = temp['value'][5:]
                li = xbmcgui.ListItem(label, iconImage="%s/resources/skins/Default/media/%s.png" % (ADDON_PATH, image_code), thumbnailImage="%s/resources/skins/Default/media/%s.png" % (ADDON_PATH, image_code))
                li.setProperty('fanart_image', "special://home/addons/script.extendedinfo/resources/skins/Default/media/%s-fanart.jpg" % image_code)
                if SCRIPT == "true" and "yt" not in value: url = 'plugin://script.extendedinfo?info=%s&type=script' % key
                else: url = 'plugin://script.extendedinfo?info=%s' % key
                xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=True)
            for key, value in iter(sorted(youtube_items.iteritems())):
                temp = {}
                temp['value'] = value
                image_code = temp['value'][:2]
                label = temp['value'][5:]
                li = xbmcgui.ListItem(label, iconImage="%s/resources/skins/Default/media/%s.png" % (ADDON_PATH, image_code), thumbnailImage="%s/resources/skins/Default/media/%s.png" % (ADDON_PATH, image_code))
                li.setProperty('fanart_image', "special://home/addons/script.extendedinfo/resources/skins/Default/media/%s-fanart.jpg" % image_code)
                if SCRIPT == "true" and "yt" not in value: url = 'plugin://script.extendedinfo?info=%s&type=script' % key
                else: url = 'plugin://script.extendedinfo?info=%s' % key
                xbmcplugin.addDirectoryItem(handle=self.handle, url=url, listitem=li, isFolder=True)
            xbmcplugin.endOfDirectory(self.handle)
        xbmc.executebuiltin('ClearProperty(extendedinfo_running,home)')

    def _parse_argv(self):
        args = sys.argv[2][1:]
        self.handle = int(sys.argv[1])
        self.control = "plugin"
        self.infos = []
        self.params = {"handle": self.handle,
                       "control": self.control}
        if args.startswith("---"):
            delimiter = "&"
            args = args[3:]
        else:
            delimiter = "&"
        for arg in args.split(delimiter):
            param = arg.replace('"', '').replace("'", " ")
            if param.startswith('info='):
                self.infos.append(param[5:])
            else:
                try:
                    self.params[param.split("=")[0].lower()] = "=".join(param.split("=")[1:]).strip()
                except:
                    pass

if (__name__ == "__main__"):
    Main()
xbmc.log('finished')