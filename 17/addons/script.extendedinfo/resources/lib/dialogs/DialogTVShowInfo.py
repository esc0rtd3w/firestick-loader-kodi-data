# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcgui
from ..Utils import *
from ..ImageTools import *
from ..TheMovieDB import *
from DialogBaseInfo import DialogBaseInfo
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer

PLAYER = VideoPlayer.VideoPlayer()
ch = OnClickHandler()


def get_tvshow_window(window_type):

    class DialogTVShowInfo(DialogBaseInfo, window_type):

        def __init__(self, *args, **kwargs):
            super(DialogTVShowInfo, self).__init__(*args, **kwargs)
            self.type = "TVShow"
            data = extended_tvshow_info(tvshow_id=kwargs.get('tmdb_id', False),
                                        dbid=self.dbid)
            if not data:
                return None
            self.info, self.data, self.account_states = data
            if "dbid" not in self.info:
                self.info['poster'] = get_file(self.info.get("poster", ""))
            self.info['ImageFilter'], self.info['ImageColor'] = filter_image(input_img=self.info.get("poster", ""),
                                                                             radius=25)
            self.listitems = [(1900, self.data["addons"]),
                              ( 250, self.data["seasons"]),
                              ( 150, self.data["similar"]),
                              (1150, self.data["videos"]),
                              (1000, self.data["actors"]),
                              ( 750, self.data["crew"]),
                              ( 550, self.data["studios"]),
                              (1450, self.data["networks"]),
                              ( 650, merge_with_cert_desc(self.data["certifications"], "tv")),
                              ( 850, self.data["genres"]),
                              ( 950, self.data["keywords"]),
                              (1250, self.data["images"]),
                              (1350, self.data["backdrops"])]

        def onInit(self):
            self.get_youtube_vids("%s tv" % (self.info['title']))
            super(DialogTVShowInfo, self).onInit()
            pass_dict_to_skin(data=self.info,
                              prefix="movie.",
                              window_id=self.window_id)
            super(DialogTVShowInfo, self).update_states()
            self.fill_lists()

        def onClick(self, control_id):
            super(DialogTVShowInfo, self).onClick(control_id)
            ch.serve(control_id, self)

        @ch.click(120)
        def browse_tvshow(self):
            self.close()
            xbmc.executebuiltin("ActivateWindow(videos,videodb://tvshows/titles/%s/)" % (self.dbid))

        @ch.action("contextmenu", 150)
        def right_click_similar(self):
            item_id = self.listitem.getProperty("id")
            listitems = [LANG(208)]
            if self.listitem.getProperty("dbid"):
                listitems += [LANG(32233)]
            else:
                listitems += [LANG(32232)]
            if self.logged_in:
                listitems += [LANG(14076)]
                listitems += [LANG(32107)]
            selection = xbmcgui.Dialog().select(heading=LANG(32151), list=listitems)


        @ch.click(750)
        @ch.click(1000)
        def credit_dialog(self):
            selection = xbmcgui.Dialog().select(heading=LANG(32151),
                                                list=[LANG(32009), LANG(32147)])
            if selection == 0:
                wm.open_actor_info(prev_window=self,
                                   actor_id=self.listitem.getProperty("id"))
            if selection == 1:
                self.open_credit_dialog(self.listitem.getProperty("credit_id"))

        @ch.click(150)
        def open_tvshow_dialog(self):
            wm.open_tvshow_info(prev_window=self,
                                tvshow_id=self.listitem.getProperty("id"),
                                dbid=self.listitem.getProperty("dbid"))

        @ch.click(250)
        def open_season_dialog(self):
            wm.open_season_info(prev_window=self,
                                tvshow_id=self.info["id"],
                                season=self.listitem.getProperty("season"),
                                tvshow=self.info['title'])

        @ch.click(550)
        def open_company_info(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_companies",
                        "typelabel": LANG(20388),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(950)
        def open_keyword_info(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_keywords",
                        "typelabel": LANG(32114),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(850)
        def open_genre_info(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_genres",
                        "typelabel": LANG(135),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters,
                               media_type="tv")

        @ch.click(1450)
        def open_network_info(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_networks",
                        "typelabel": LANG(32152),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters,
                               media_type="tv")

        @ch.click(445)
        def show_manage_dialog(self):
            manage_list = []
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % ADDON_ID) + " " + LANG(10004), 'Addon.OpenSettings(%s)' % ADDON_ID])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % 'plugin.video.metalliq-forqed') + " " + LANG(10004), 'Addon.OpenSettings(%s)' % 'plugin.video.metalliq-forqed'])
            addons = get_addons("tvshows")
            if len(addons) > 0:
                for addon in addons:  manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % addon[0]) + " " + LANG(10004), 'Addon.OpenSettings(%s)' % addon[1]])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % 'script.module.youtube.dl') + " " + LANG(10004), 'Addon.OpenSettings(%s)' % 'script.module.youtube.dl'])
            selection = xbmcgui.Dialog().select(heading=LANG(10004), list=[i[0] for i in manage_list])
            if selection > -1:
                for item in manage_list[selection][1].split("||"): xbmc.executebuiltin(item)

        @ch.click(1900)
        def pick_and_mix(self):
            url = 'plugin://plugin.video.metalliq-forqed/tv/play/%s/1/1/%s' % (self.info.get("tvdb_id", ""), self.listitem.getProperty("qid"))
            PLAYER.qlickplay(url, listitem=None, window=self, dbid=0)

        @ch.click(6001)
        def set_rating(self):
            if set_rating_prompt(media_type="tv",
                                 media_id=self.info["id"]):
                self.update_states()

        @ch.click(6002)
        def open_list(self):
            index = xbmcgui.Dialog().select(heading=LANG(32136),
                                            list=[LANG(32144), LANG(32145)])
            if index == 0:
                wm.open_video_list(prev_window=self,
                                   media_type="tv",
                                   mode="favorites")
            elif index == 1:
                wm.open_video_list(prev_window=self,
                                   mode="rating",
                                   media_type="tv")

        @ch.click(6003)
        def toggle_fav_status(self):
            change_fav_status(media_id=self.info["id"],
                              media_type="tv",
                              status=str(not bool(self.account_states["favorite"])).lower())
            self.update_states()

        @ch.click(6006)
        def open_rated_items(self):
            wm.open_video_list(prev_window=self,
                               mode="rating",
                               media_type="tv")

        @ch.click(9)
        def play_tvshow_no_resume(self):
            #playlist = "special://profile/playlists/video/%s.xsp" % self.info.get("tvdb_id", "")
            if self.dbid:
                url = "special://profile/playlists/video/%s.xsp" % self.info.get("tvdb_id", "")
                if not os.path.exists(url):
                    url = "plugin://plugin.video.metalliq-forqed/tv/play/%s/1/1/%s" % (self.info.get("tvdb_id", ""), SETTING("player_main_tv"))
            else:
                url = "plugin://plugin.video.metalliq-forqed/tv/play/%s/1/1/%s" % (self.info.get("tvdb_id", ""), SETTING("player_main_tv"))
            PLAYER.qlickplay(url,
                             listitem=None,
                             window=self,
                             dbid=0)

        @ch.click(20)
        def add_tvshow_to_library(self):
            TVLibrary = METALLIQ.getSetting("tv_library_folder")
            tvdb_id = self.info["tvdb_id"]
            if not os.path.exists(xbmc.translatePath("%s%s/" % (TVLibrary, tvdb_id))):
                xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/tv/add_to_library/%s)" % self.info.get("tvdb_id", ""))
                notify(header='Added "%s" to library' % self.info.get("TVShowTitle", ""), message="Starting library scan now", icon=self.info["poster"], time=5000, sound=False)
                after_add(type="tv")
            else:
                notify(header="To refresh all content:", message="Exit %s & re-enter" % ADDON_NAME, icon=self.info["poster"], time=5000, sound=False)

        @ch.click(21)
        def remove_tvshow_from_library(self):
            TVLibrary = METALLIQ.getSetting("tv_library_folder")
            TVPlaylists = METALLIQ.getSetting("tv_playlist_folder")
            tvdb_id = self.info["tvdb_id"]
            if os.path.exists(xbmc.translatePath("%s%s.xsp" % (TVPlaylists, tvdb_id))):
                os.remove(xbmc.translatePath("%s%s.xsp" % (TVPlaylists, tvdb_id)))
            if os.path.exists(xbmc.translatePath("%s%s/" % (TVLibrary, tvdb_id))):
                get_kodi_json(method="VideoLibrary.RemoveTVShow", params='{"tvshowid": %s}' % int(self.info["dbid"]))
                import shutil
                shutil.rmtree(xbmc.translatePath("%s%s/" % (TVLibrary, tvdb_id)))
                notify(header='Removed "%s" from library' % self.info.get("TVShowTitle", ""), message="Exit & re-enter to refresh", icon=self.info["poster"], time=5000, sound=False)
                after_add(type="tv")
            else:
                notify(header="To refresh all content:", message="Exit %s & re-enter" % ADDON_NAME, icon=self.info["poster"], time=5000, sound=False)

        @ch.click(120)
        def browse_tvshow(self):
            url = "plugin://plugin.video.metalliq-forqed/tv/tvdb/%s" % self.info.get("tvdb_id", "")
            self.close()
            xbmc.executebuiltin("ActivateWindow(videos,%s,return)" % url)

        @ch.click(132)
        def open_text(self):
            wm.open_textviewer(header=LANG(32037),
                               text=self.info["Plot"],
                               color=self.info['ImageColor'])

        @ch.click(350)
        @ch.click(1150)
        def play_youtube_video(self):
            PLAYER.playtube(self.listitem.getProperty("youtube_id"), listitem=self.listitem, window=self)

        def update_states(self):
            xbmc.sleep(2000)  # delay because MovieDB takes some time to update
            _, __, self.account_states = extended_tvshow_info(tvshow_id=self.info["id"],
                                                              cache_time=0,
                                                              dbid=self.dbid)
            super(DialogTVShowInfo, self).update_states()

    return DialogTVShowInfo
