# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

from ..Utils import *
from ..TheMovieDB import *
from ..ImageTools import *
from DialogBaseInfo import DialogBaseInfo
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer

ch = OnClickHandler()
PLAYER = VideoPlayer.VideoPlayer()


def get_season_window(window_type):

    class DialogSeasonInfo(DialogBaseInfo, window_type):

        def __init__(self, *args, **kwargs):
            super(DialogSeasonInfo, self).__init__(*args, **kwargs)
            self.type = "Season"
            self.tvshow_id = kwargs.get('id')
            data = extended_season_info(tvshow_id=self.tvshow_id,
                                        season_number=kwargs.get('season'))
            if not data:
                return None
            self.info, self.data = data
            if "dbid" not in self.info:  # need to add comparing for seasons
                self.info['poster'] = get_file(url=self.info.get("poster", ""))
            self.info['ImageFilter'], self.info['ImageColor'] = filter_image(input_img=self.info.get("poster", ""),
                                                                             radius=25)
            self.listitems = [(1900, self.data["addons"]),
                              (2000, self.data["episodes"]),
                              (1150, self.data["videos"]),
                              (1000, self.data["actors"]),
                              (750, self.data["crew"]),
                              (1250, self.data["images"]),
                              (1350, self.data["backdrops"])]

        def onInit(self):
            self.get_youtube_vids("%s %s tv" % (self.info["TVShowTitle"], self.info['title']))
            super(DialogSeasonInfo, self).onInit()
            pass_dict_to_skin(data=self.info,
                              prefix="movie.",
                              window_id=self.window_id)
            self.fill_lists()

        def onClick(self, control_id):
            super(DialogSeasonInfo, self).onClick(control_id)
            ch.serve(control_id, self)

        @ch.click(121)
        def browse_season(self):
            if self.dbid:
                url = "videodb://tvshows/titles/%s/%s/" % ((self.dbid), self.info.get("season", ""))
            else:
                tvdb_id = fetch(get_tvshow_ids(self.tvshow_id), "tvdb_id")
                url = "plugin://plugin.video.metalliq-forqed/tv/tvdb/%s/%s/" % (tvdb_id, self.info.get("season", ""))
            self.close()
            xbmc.executebuiltin("ActivateWindow(videos,%s,return)" % url)

        @ch.click(750)
        @ch.click(1000)
        def open_actor_info(self):
            wm.open_actor_info(prev_window=self,
                               actor_id=self.listitem.getProperty("id"))

        @ch.click(2000)
        def open_episode_info(self):
            wm.open_episode_info(prev_window=self,
                                 tvshow=self.info["TVShowTitle"],
                                 tvshow_id=self.tvshow_id,
                                 season=self.listitem.getProperty("season"),
                                 episode=self.listitem.getProperty("episode"))

        @ch.click(10)
        def play_season_no_resume(self):
            if self.dbid:
                url = "special://profile/playlists/video/%s.xsp" % self.info.get("tvdb_id", "")
                if not os.path.exists(url):
                    url = "plugin://plugin.video.metalliq-forqed/tv/play/%s/%s/1/%s" % (self.info.get("tvdb_id", ""), self.info.get("season", ""), SETTING("player_main_tv"))
            else:
                url = "plugin://plugin.video.metalliq-forqed/tv/play/%s/%s/1/%s" % (self.info.get("tvdb_id", ""), self.info.get("season", ""), SETTING("player_main_tv"))
            PLAYER.qlickplay(url,
                             listitem=None,
                             window=self,
                             dbid=0)

        @ch.click(445)
        def show_manage_dialog(self):
            manage_list = []
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % ADDON_ID) + " " + LANG(32133), 'Addon.OpenSettings(%s)' % ADDON_ID])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % 'plugin.video.metalliq-forqed') + " " + LANG(32133), 'Addon.OpenSettings(%s)' % 'plugin.video.metalliq-forqed'])
            addons = get_addons("tvshows")
            if len(addons) > 0:
                for addon in addons:  manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % addon[0]) + " " + LANG(32133), 'Addon.OpenSettings(%s)' % addon[1]])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % 'script.module.youtube.dl') + " " + LANG(32133), 'Addon.OpenSettings(%s)' % 'script.module.youtube.dl'])
            selection = xbmcgui.Dialog().select(heading=LANG(10004), list=[i[0] for i in manage_list])
            if selection > -1:
                for item in manage_list[selection][1].split("||"): xbmc.executebuiltin(item)

        @ch.click(132)
        def open_text(self):
            wm.open_textviewer(header=LANG(32037),
                               text=self.info["Plot"],
                               color=self.info['ImageColor'])

        @ch.click(1900)
        def pick_and_mix(self):
            url = 'plugin://plugin.video.metalliq-forqed/tv/play/%s/%s/1/%s' % (self.info.get("tvdb_id", ""), self.info.get("season", ""), self.listitem.getProperty("qid"))
            PLAYER.qlickplay(url, listitem=None, window=self, dbid=0)

        @ch.click(350)
        @ch.click(1150)
        def play_youtube_video(self):
            PLAYER.playtube(self.listitem.getProperty("youtube_id"), listitem=self.listitem, window=self)

        @ch.click(22)
        def change_kodi_fav_status(self):
            message = ""
            fav_name = self.info["TVShowTitle"] + " - Season %s" % self.info["season"]
            faves = get_kodi_json(method="Favourites.GetFavourites", params='{"type":"window"}')
            status = ""
            if faves["result"]["favourites"]:
                for item in faves["result"]["favourites"]:
                    if item["title"] == fav_name: status = "present"
            if status == "present": message = LANG(32237)
            else: message = LANG(32236)
            get_kodi_json(method="Favourites.AddFavourite", params='{"title":"%s", "type":"window", "window":"Videos", "windowparameter":"%s", "thumbnail":"%s"}' % (fav_name, 'plugin://script.extendedinfo/?info=seasoninfo&id=%s&tvshow=%s&season=%s' % (self.tvshow_id, self.info["TVShowTitle"], self.info["season"]), self.info["poster"]))
            notify(header=fav_name, message=message, icon=self.info["poster"], time=1500, sound=False)

    return DialogSeasonInfo
