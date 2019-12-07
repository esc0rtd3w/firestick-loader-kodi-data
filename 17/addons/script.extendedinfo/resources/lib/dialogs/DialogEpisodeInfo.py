# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
from ..Utils import *
from ..TheMovieDB import *
from ..ImageTools import *
from DialogBaseInfo import DialogBaseInfo
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer

PLAYER = VideoPlayer.VideoPlayer()
ch = OnClickHandler()


def get_episode_window(window_type):

    class DialogEpisodeInfo(DialogBaseInfo, window_type):

        @busy_dialog
        def __init__(self, *args, **kwargs):
            super(DialogEpisodeInfo, self).__init__(*args, **kwargs)
            self.type = "Episode"
            self.tvshow_id = kwargs.get('show_id')
            data = extended_episode_info(tvshow_id=self.tvshow_id,
                                         season=kwargs.get('season'),
                                         episode=kwargs.get('episode'))
            if not data:
                return None
            self.info, self.data, self.account_states = data
            self.info['ImageFilter'], self.info['ImageColor'] = filter_image(input_img=self.info.get("thumb", ""),
                                                                             radius=25)
            self.listitems = [(1900, self.data["addons"]),
                              (1150, self.data["videos"]),
                              (1000, self.data["actors"] + self.data["guest_stars"]),
                              (750, self.data["crew"]),
                              (1350, self.data["images"])]
        def onInit(self):
            super(DialogEpisodeInfo, self).onInit()
            pass_dict_to_skin(self.info, "movie.", False, False, self.window_id)
            super(DialogEpisodeInfo, self).update_states()
            self.get_youtube_vids("%s tv" % (self.info['title']))
            self.fill_lists()

        def onClick(self, control_id):
            super(DialogEpisodeInfo, self).onClick(control_id)
            ch.serve(control_id, self)

        @ch.click(750)
        @ch.click(1000)
        def open_actor_info(self):
            wm.open_actor_info(prev_window=self,
                               actor_id=self.listitem.getProperty("id"))

        @ch.click(132)
        def open_text(self):
            wm.open_textviewer(header=LANG(32037),
                               text=self.info["Plot"],
                               color=self.info['ImageColor'])

        @ch.click(6001)
        def set_rating_dialog(self):
            if set_rating_prompt(media_type="episode",
                                 media_id=[self.tvshow_id, self.info["season"], self.info["episode"]]):
                self.update_states()

        @ch.click(6006)
        def open_rating_list(self):
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            listitems = get_rated_media_items("tv/episodes")
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            wm.open_video_list(prev_window=self,
                               listitems=listitems)

        @ch.click(350)
        @ch.click(1150)
        def play_youtube_video(self):
            PLAYER.playtube(self.listitem.getProperty("youtube_id"), listitem=self.listitem, window=self)

        @ch.click(11)
        def play_episode_no_resume(self):
            if self.dbid:
                dbid = self.dbid
                url = "special://profile/playlists/mixed/MetalliQ/TVShows/%s.xsp" % self.info.get("tvdb_id", "")
                if not os.path.exists(url):
                    url = "plugin://plugin.video.metalliq-forqed/tv/play/%s/%s/%s/%s" % (self.info.get("tvdb_id", ""), self.info.get("season", ""), self.info["episode"], SETTING("player_main_tv"))
            else:
                dbid = 0
                tvdb_id = fetch(get_tvshow_ids(self.tvshow_id), "tvdb_id")
                url = "plugin://plugin.video.metalliq-forqed/tv/play/%s/%s/%s/%s" % (tvdb_id, self.info["season"], self.info["episode"], SETTING("player_main_tv"))
            PLAYER.qlickplay(url,
                             listitem=None,
                             window=self,
                             dbid=dbid)

        @ch.click(445)
        def show_manage_dialog(self):
            manage_list = []
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % 'script.extendedinfo') + " " + LANG(32133), 'Addon.OpenSettings(%s)' % 'script.extendedinfo'])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % 'plugin.video.metalliq-forqed') + " " + LANG(32133), 'Addon.OpenSettings(%s)' % 'plugin.video.metalliq-forqed'])
            addons = get_addons("tvshows")
            if len(addons) > 0:
                for addon in addons:  manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % addon[0]) + " " + LANG(32133), 'Addon.OpenSettings(%s)' % addon[1]])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % 'script.module.youtube.dl') + " " + LANG(32133), 'Addon.OpenSettings(%s)' % 'script.module.youtube.dl'])
            selection = xbmcgui.Dialog().select(heading=LANG(10004), list=[i[0] for i in manage_list])
            if selection > -1:
                for item in manage_list[selection][1].split("||"): xbmc.executebuiltin(item)

        @ch.click(1900)
        def pick_and_mix(self):
            url = 'plugin://plugin.video.metalliq-forqed/tv/play/%s/%s/%s/%s' % (self.data.get("tvdb_id", ""), self.info.get("season", ""), self.info.get("episode", ""), self.listitem.getProperty("qid"))
            PLAYER.qlickplay(url, listitem=None, window=self, dbid=0)

        def update_states(self):
            xbmc.sleep(2000)  # delay because MovieDB takes some time to update
            _, __, self.account_states = extended_episode_info(tvshow_id=self.tvshow_id,
                                                               season=self.info["season"],
                                                               episode=self.info["episode"],
                                                               cache_time=0)
            super(DialogEpisodeInfo, self).update_states()

        @ch.click(23)
        def change_episode_fav_status(self):
            message = ""
            fav_name = self.data.get("TVShowTitle", "") + " - S%02dE%02d - %s" % (int(self.info["season"]), int(self.info["episode"]), self.info['title'])
            faves = get_kodi_json(method="Favourites.GetFavourites", params='{"type":"window"}')
            status = ""
            if faves["result"]["favourites"]:
                for item in faves["result"]["favourites"]:
                    if item["title"] == fav_name: status = "present"
            if status == "present": message = LANG(32237)
            else: message = LANG(32236)
            get_kodi_json(method="Favourites.AddFavourite", params='{"title":"%s", "type":"window", "window":"Videos", "windowparameter":"%s", "thumbnail":"%s"}' % (fav_name, 'plugin://script.extendedinfo/?info=extendedepisodeinfo&tvshow_id=%s&tvshow=%s&season=%s&episode=%s' % (self.data.get("show_id", ""), self.data.get("TVShowTitle", ""), self.info["season"], self.info["episode"]), self.info["still_original"]))
            notify(header=fav_name, message=message, icon=self.info["still_original"], time=1500, sound=False)

    return DialogEpisodeInfo
