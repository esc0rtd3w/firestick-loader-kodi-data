# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcgui
from ..Utils import *
from ..TheMovieDB import *
from ..omdb import *
from ..ImageTools import *
import threading
from DialogBaseInfo import DialogBaseInfo
from ..WindowManager import wm
from ..OnClickHandler import OnClickHandler
from .. import VideoPlayer

PLAYER = VideoPlayer.VideoPlayer()
ch = OnClickHandler()


def get_movie_window(window_type):

    class DialogVideoInfo(DialogBaseInfo, window_type):

        def __init__(self, *args, **kwargs):
            super(DialogVideoInfo, self).__init__(*args, **kwargs)
            self.type = "Movie"
            data = extended_movie_info(movie_id=kwargs.get('id'),
                                       dbid=self.dbid)
            if not data:
                return None
            self.info, self.data, self.account_states = data
            sets_thread = SetItemsThread(self.info["SetId"])
            self.omdb_thread = FunctionThread(get_omdb_movie_info, self.info["imdb_id"])
            lists_thread = FunctionThread(self.sort_lists, self.data["lists"])
            filter_thread = FilterImageThread(self.info.get("thumb", ""), 25)
            for thread in [self.omdb_thread, sets_thread, lists_thread, filter_thread]:
                thread.start()
            if "dbid" not in self.info:
                self.info['poster'] = get_file(self.info.get("poster", ""))
            sets_thread.join()
            self.setinfo = sets_thread.setinfo
            self.data["similar"] = [i for i in self.data["similar"] if i["id"] not in sets_thread.id_list]
            filter_thread.join()
            self.info['ImageFilter'] = filter_thread.image
            self.info['ImageColor'] = filter_thread.imagecolor
            lists_thread.join()
            self.listitems = [(1900, self.data["addons"]),
                              ( 250, sets_thread.listitems),
                              ( 150, self.data["similar"]),
                              ( 450, lists_thread.listitems),
                              (1150, self.data["videos"]),
                              (1000, self.data["actors"]),
                              ( 750, merge_dict_lists(self.data["crew"])),
                              ( 550, self.data["studios"]),
                              ( 650, merge_with_cert_desc(self.data["releases"], "movie")),
                              ( 850, self.data["genres"]),
                              (950, self.data["keywords"]),
                              (1050, self.data["reviews"]),
                              (1250, self.data["images"]),
                              (1350, self.data["backdrops"])]

        def onInit(self):
            super(DialogVideoInfo, self).onInit()
            pass_dict_to_skin(data=self.info,
                              prefix="movie.",
                              window_id=self.window_id)
            super(DialogVideoInfo, self).update_states()
            self.get_youtube_vids("%s %s, movie" % (self.info["Label"], self.info["year"]))
            self.fill_lists()
            pass_dict_to_skin(data=self.setinfo,
                              prefix="movie.set.",
                              window_id=self.window_id)
            self.join_omdb_async()

        def onClick(self, control_id):
            super(DialogVideoInfo, self).onClick(control_id)
            ch.serve(control_id, self)

        def onAction(self, action):
            super(DialogVideoInfo, self).onAction(action)
            ch.serve_action(action, self.getFocusId(), self)



        @ch.action("contextmenu", 450)
        def add_list_to_account(self):
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            movieslist = get_movies_from_list(self.listitem.getProperty("id"))
            movies_list = [["All (" + str(len(movieslist)) + ")", ""]]
            for item in movieslist:
                title = fetch(item, 'title').encode('utf8')
                movie_id = str(fetch(item, 'id'))
                movies_list.append([title, movie_id])
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            selection = xbmcgui.Dialog().select(LANG(32232), list=[i[0] for i in movies_list])
            if selection == -1:
                return
            elif selection == 0:
                xbmc.executebuiltin("ActivateWindow(busydialog)")
                ids = ""
                for item in movies_list:
                    if item != "":
                        ids = ids + str(item[1]) + '\n'
                batch_add_file_path = "special://profile/addon_data/plugin.video.metalliq-forqed/movies_to_add.txt"
                if not xbmcvfs.exists(batch_add_file_path):
                    batch_add_file = xbmcvfs.File(batch_add_file_path, 'w')
                    batch_add_file.write(ids)
                    batch_add_file.close()
                xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/movies/batch_add_to_library)")
                xbmc.executebuiltin("Dialog.Close(busydialog)")
            elif selection > 0:
                xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/movies/add_to_library/tmdb/%s)" % str(movies_list[selection][1]))

        @ch.click(1000)
        @ch.click(750)
        def open_actor_info(self):
            wm.open_actor_info(prev_window=self,
                               actor_id=self.listitem.getProperty("id"))

        @ch.click(150)
        @ch.click(250)
        def open_movie_info(self):
            wm.open_movie_info(prev_window=self,
                               movie_id=self.listitem.getProperty("id"),
                               dbid=self.listitem.getProperty("dbid"))

        @ch.click(10)
        def play_trailer(self):
            PLAYER.playtube(self.getControl(1150).getListItem(0).getProperty("youtube_id"), listitem=self.listitem, window=self)

        @ch.click(350)
        @ch.click(1150)
        def play_youtube_video(self):
            PLAYER.playtube(self.listitem.getProperty("youtube_id"), listitem=self.listitem, window=self)

        @ch.click(550)
        def open_company_list(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_companies",
                        "typelabel": LANG(20388),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(1050)
        def show_review(self):
            author = self.listitem.getProperty("author")
            text = "[B]%s[/B][CR]%s" % (author, clean_text(self.listitem.getProperty("content")))
            wm.open_textviewer(header=LANG(207),
                               text=text,
                               color=self.info['ImageColor'])

        @ch.click(950)
        def open_keyword_list(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_keywords",
                        "typelabel": LANG(32114),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(850)
        def open_genre_list(self):
            filters = [{"id": self.listitem.getProperty("id"),
                        "type": "with_genres",
                        "typelabel": LANG(135),
                        "label": self.listitem.getLabel().decode("utf-8")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(650)
        def open_cert_list(self):
            filters = [{"id": self.listitem.getProperty("iso_3166_1"),
                        "type": "certification_country",
                        "typelabel": LANG(32153),
                        "label": self.listitem.getProperty("iso_3166_1")},
                       {"id": self.listitem.getProperty("certification"),
                        "type": "certification",
                        "typelabel": LANG(32127),
                        "label": self.listitem.getProperty("certification")},
                       {"id": self.listitem.getProperty("year"),
                        "type": "year",
                        "typelabel": LANG(345),
                        "label": self.listitem.getProperty("year")}]
            wm.open_video_list(prev_window=self,
                               filters=filters)

        @ch.click(450)
        def open_lists_list(self):
            wm.open_video_list(prev_window=self,
                               mode="list",
                               list_id=self.listitem.getProperty("id"),
                               filter_label=self.listitem.getLabel())

        @ch.click(6002)
        def show_list_dialog(self):
            listitems = [LANG(32134), LANG(32135)]
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            account_lists = get_account_lists()
            for item in account_lists:
                listitems.append("%s (%i)" % (item["name"], item["item_count"]))
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            index = xbmcgui.Dialog().select(LANG(32136), listitems)
            if index == -1:
                pass
            elif index == 0:
                wm.open_video_list(prev_window=self,
                                   mode="favorites")
            elif index == 1:
                wm.open_video_list(prev_window=self,
                                   mode="rating")
            else:
                wm.open_video_list(prev_window=self,
                                   mode="list",
                                   list_id=account_lists[index - 2]["id"],
                                   filter_label=account_lists[index - 2]["name"],
                                   force=True)

        @ch.click(120)
        def search_in_metalliq_by_title(self):
            url = "plugin://plugin.video.metalliq-forqed/movies/tmdb/search_term/%s/1" % self.info.get("title", "")
            self.close()
            xbmc.executebuiltin("ActivateWindow(videos,%s,return)" % url)

        @ch.click(132)
        def show_plot(self):
            wm.open_textviewer(header=LANG(207),
                               text=self.info["Plot"],
                               color=self.info['ImageColor'])

        @ch.click(6001)
        def set_rating_dialog(self):
            if set_rating_prompt("movie", self.info["id"]):
                self.update_states()

        @ch.click(6005)
        def add_to_list_dialog(self):
            xbmc.executebuiltin("ActivateWindow(busydialog)")
            account_lists = get_account_lists()
            listitems = ["%s (%i)" % (i["name"], i["item_count"]) for i in account_lists]
            listitems.insert(0, LANG(32139))
            listitems.append(LANG(32138))
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            index = xbmcgui.Dialog().select(heading=LANG(32136),
                                            list=listitems)
            if index == 0:
                listname = xbmcgui.Dialog().input(heading=LANG(32137),
                                                  type=xbmcgui.INPUT_ALPHANUM)
                if not listname:
                    return None
                list_id = create_list(listname)
                xbmc.sleep(1000)
                change_list_status(list_id=list_id,
                                   movie_id=self.info["id"],
                                   status=True)
            elif index == len(listitems) - 1:
                self.remove_list_dialog(account_lists)
            elif index > 0:
                change_list_status(account_lists[index - 1]["id"], self.info["id"], True)
                self.update_states()

        @ch.click(6003)
        def change_list_status(self):
            change_fav_status(media_id=self.info["id"],
                              media_type="movie",
                              status=str(not bool(self.account_states["favorite"])).lower())
            self.update_states()

        @ch.click(6006)
        def open_rating_list(self):
            wm.open_video_list(prev_window=self,
                               mode="rating")

        @ch.click(9)
        def play_movie_resume(self):
            self.close()
            get_kodi_json(method="Player.Open",
                          params='{"item": {"movieid": %s}, "options":{"resume": %s}}' % (self.info['dbid'], "true"))

        @ch.click(8)
        def play_movie_no_resume(self):
            if self.dbid:
                dbid = self.dbid
                url = "temp"
            else:
                dbid = 0
                url = "plugin://plugin.video.metalliq-forqed/movies/play/tmdb/%s/%s" % (self.info.get("id", ""), SETTING("player_main_movie"))
            PLAYER.qlickplay(url,
                             listitem=None,
                             window=self,
                             dbid=dbid)

        @ch.click(445)
        def show_manage_dialog(self):
            manage_list = []
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % ADDON_ID) + " " + LANG(10004), 'Addon.OpenSettings(%s)' % ADDON_ID])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % 'plugin.video.metalliq-forqed') + " " + LANG(10004), 'Addon.OpenSettings(%s)' % 'plugin.video.metalliq-forqed'])
            addons = get_addons("movies")
            if len(addons) > 0:
                for addon in addons: manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % addon[0]) + " " + LANG(10004), 'Addon.OpenSettings(%s)' % addon[1]])
            manage_list.append([xbmc.getInfoLabel('System.AddonTitle(%s)' % 'script.module.youtube.dl') + " " + LANG(10004), 'Addon.OpenSettings(%s)' % 'script.module.youtube.dl'])
            selection = xbmcgui.Dialog().select(heading=LANG(10004), list=[i[0] for i in manage_list])
            if selection > -1:
                for item in manage_list[selection][1].split("||"): xbmc.executebuiltin(item)

        @ch.click(19)
        def appintegration_movie(self):
            manage_list = []
            movie_id = str(self.info.get("dbid", ""))
            tmdb_id = str(self.info.get("id", ""))
            imdb_id = str(self.info.get("imdb_id", ""))
            year = str(self.info.get("year", ""))
            premocktitle = self.info.get("title", "")
            mocktitle = premocktitle.replace("&", "%26")
            title = mocktitle.encode('utf-8')
            language = xbmc.getLanguage()
            if movie_id:
                if xbmc.getCondVisibility("system.hasaddon(script.artwork.downloader)"):
                    manage_list.append(["Download Artwork", "RunScript(script.artwork.downloader,mediatype=movie,dbid="+movie_id+")||Notification(Artwork Downloader:,"+title+",5000,special://home/addons/script.artwork.downloader/icon.png)"])
            if not movie_id and xbmc.getCondVisibility("system.hasaddon(plugin.video.couchpotato_manager)"):
                manage_list.append([LANG(32165), "RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add?imdb_id="+imdb_id+")||Notification(Couch Potato,"+title+",5000,special://home/addons/plugin.video.couchpotato_manager/icon.png))"])
            if xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"):
                manage_list.append(["Search Youtube Videos", "RunScript(script.extendedinfo,info=list,type=video,query="+title+")||Notification(YouTube Videos:,"+title+",5000,special://home/addons/script.extendedinfo/resources/skins/Default/media/common/youtube.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)") and ADDON.getSetting("ExtendedYoutubeMovie") == "true":
                manage_list.append(["Search Youtube Channels", "RunScript(script.extendedinfo,info=list,type=channel,query="+title+")||Notification(YouTube Channels:,"+title+",5000,special://home/addons/script.extendedinfo/resources/skins/Default/media/common/youtube.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)") and ADDON.getSetting("ExtendedYoutubeMovie") == "true":
                manage_list.append(["Search Youtube Playlists", "RunScript(script.extendedinfo,info=list,type=playlist,query="+title+")||Notification(YouTube Playlists:,"+title+",5000,special://home/addons/script.extendedinfo/resources/skins/Default/media/common/youtube.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.exodus)"):
                manage_list.append(["Search Exodus", "ActivateWindow(10025,plugin://plugin.video.exodus/?action=movieSearch&query="+title+",return)||Notification(Exodus:,"+title+",5000,special://home/addons/plugin.video.exodus/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.icechannel)"):
                manage_list.append(["Search iSTREAM", "ActivateWindow(10025,plugin://script.icechannel/?indexer=movies&indexer_id&mode=search&search_term="+title+"&section=search&type=movies)||Notification(iSTREAM:,"+title+",5000,special://home/addons/script.icechannel/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.salts)"):
                manage_list.append(["Search SALTS", "ActivateWindow(10025,plugin://plugin.video.salts/?query="+title+"&section=Movies&mode=search_results,return)||Notification(SALTS:,"+title+",5000,special://home/addons/plugin.video.salts/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltshd.lite)"):
                manage_list.append(["Search Salts HD Lite", "ActivateWindow(10025,plugin://plugin.video.saltshd.lite/?query="+title+"&section=Movies&mode=search_results,return)||Notification(Salts HD Lite:,"+title+",5000,special://home/addons/plugin.video.saltshd.lite/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.saltsrd.lite)"):
                manage_list.append(["Search Salts RD Lite", "ActivateWindow(10025,plugin://plugin.video.saltsrd.lite/?query="+title+"&section=Movies&mode=search_results,return)||Notification(Salts RD Lite:,"+title+",5000,special://home/addons/plugin.video.saltsrd.lite/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.specto)"):
                manage_list.append(["Search Specto", "ActivateWindow(10025,plugin://plugin.video.specto/?action=movieSearch&query="+title+",return)||Notification(Specto:,"+title+",5000,special://home/addons/plugin.video.specto/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.1channel)"):
                manage_list.append(["Search 1Channel", "ActivateWindow(10025,&quot;plugin://plugin.video.1channel/?mode=Search&amp;section=movies&amp;query="+title+",return)||Notification(1Channel:,"+title+",5000,special://home/addons/plugin.video.1channel/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.theroyalwe)"):
                manage_list.append(["Search The Royal We", "ActivateWindow(10025,plugin://plugin.video.theroyalwe/?query="+title+"&section=Movies&mode=search_results,return)||Notification(The Royal We:,"+title+",5000,special://home/addons/plugin.video.theroyalwe/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.phstreams)"):
                manage_list.append(["Search Phoenix", "ActivateWindow(10025,plugin://plugin.video.phstreams/?action=addSearch&url="+title+",return)||Notification(Phoenix:,"+title+",5000,special://home/addons/plugin.video.phstreams/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.pulsar)"):
                manage_list.append(["Search Pulsar", "PlayMedia(plugin://plugin.video.pulsar/movie/"+imdb_id+"/links)||Notification(Pulsar:,"+title+",5000,special://home/addons/plugin.video.pulsar/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.quasar)"):
                manage_list.append(["Search Quasar", "PlayMedia(plugin://plugin.video.quasar/movie/"+tmdb_id+"/links)||Notification(Quasar:,"+title+",5000,special://home/addons/plugin.video.quasar/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.search.play2kd)") and language == 'Dutch':
                manage_list.append(["NL [COLOR FFF35C9F]Search+Play[/COLOR]2KD", "RunScript(script.search.play2kd,type=1,query="+title+" gesproken)||Notification([COLOR FFF35C9F]Search+Play[/COLOR]2KD:,"+title+",5000,special://home/addons/script.search.play2kd/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(script.search.play2kd)"):
                manage_list.append(["[COLOR FFF35C9F]Search+Play[/COLOR]2KD", "RunScript(script.search.play2kd,type=1,query="+title+")||Notification([COLOR FFF35C9F]Search+Play[/COLOR]2KD:,"+title+",5000,special://home/addons/script.search.play2kd/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)") and language == 'Dutch':
                manage_list.append(["NL K-Search (KickAss)", "ActivateWindow(10025,plugin://plugin.video.kmediatorrent/kat/browse/usearch/"+title+"%2520gesproken%2520%2520verified%253A1/1/seeders/desc,return)||Notification(K-Search NL:,"+title+",5000,special://home/addons/plugin.video.kmediatorrent/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)"):
                manage_list.append(["K-Search (KickAss)", "ActivateWindow(10025,plugin://plugin.video.kmediatorrent/kat/browse/usearch/"+title+"2520verified%253A1/1/seeders/desc,return)||Notification(K-Search KickAss:,"+title+",5000,special://home/addons/plugin.video.kmediatorrent/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)"):
                manage_list.append(["K-Search Yify", "ActivateWindow(10025,plugin://plugin.video.kmediatorrent/yify/search/"+title+"/1,return)||Notification(K-Search Yify:,"+title+",5000,special://home/addons/plugin.video.kmediatorrent/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.kmediatorrent)"):
                manage_list.append(["K-Search ExtraTorrent", "ActivateWindow(10025,plugin://plugin.video.kmediatorrent/extratorrent/search/?query="+title+",return)||Notification(K-Search ExtraTorrent:,"+title+",5000,special://home/addons/plugin.video.kmediatorrent/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.video.yifymovies.hd)"):
                manage_list.append(["Search Yifymovies HD", "ActivateWindow(10025,plugin://plugin.video.yifymovies.hd/?action=movies_search&query="+title+",return)||Notification(YifyFind:,"+title+",5000,special://home/addons/plugin.video.yifymovies.hd/icon.png)"])
            if xbmc.getCondVisibility("system.hasaddon(plugin.program.super.favourites)"):
                manage_list.append(["iSearch (Super Favourites)", "ActivateWindow(10025,plugin://plugin.program.super.favourites/?mode=0&keyword="+title+",return)||Notification(iSearch:,"+title+",5000,special://home/addons/plugin.program.super.favourites/icon.png)"])
            selection = xbmcgui.Dialog().select(heading=LANG(32188),
                                                list=[i[0] for i in manage_list])
            if movie_id:
                if selection == 0 and xbmc.getCondVisibility("system.hasaddon(script.artwork.downloader)"):
                    artwork_list = []
                    artwork_call = "RunScript(script.artwork.downloader,%s)"
                    artwork_list += [[LANG(413), artwork_call % " mode=gui, mediatype=movie, dbid=%s" % movie_id],
                                    [LANG(14061), artwork_call % " mediatype=movie, dbid=%s" % movie_id],
                                    [LANG(32101), artwork_call % " mode=custom, mediatype=movie, dbid=%s, extrathumbs" % movie_id],
                                    [LANG(32100), artwork_call % " mode=custom, mediatype=movie, dbid=%s, extrafanart" % movie_id]]
                    selection = xbmcgui.Dialog().select(heading=LANG(32191),
                                    list=[i[0] for i in artwork_list])
                    if selection > -1:
                        for item in artwork_list[selection][1].split("||"):
                            xbmc.executebuiltin(item)
                elif selection > -1:
                    for item in manage_list[selection][1].split("||"):
                        self.close()
                        xbmc.executebuiltin(item)
            else:
                if selection > -1:
                    for item in manage_list[selection][1].split("||"):
                        if selection == 0 and xbmc.getCondVisibility("system.hasaddon(plugin.video.couchpotato_manager)"):
                            xbmc.executebuiltin(item)
                        else:
                            self.close()
                            xbmc.executebuiltin(item)

        @ch.click(1900)
        def pick_and_mix(self):
            dbid = 0
            url = "plugin://plugin.video.metalliq-forqed/movies/play/tmdb/%s/%s" % (self.info.get("id", ""), self.listitem.getProperty("qid"))
            PLAYER.qlickplay(url, listitem=None, window=self, dbid=dbid)

        def sort_lists(self, lists):
            if not self.logged_in:
                return lists
            account_list = get_account_lists(10)  # use caching here, forceupdate everywhere else
            id_list = [item["id"] for item in account_list]
            own_lists = [item for item in lists if item["id"] in id_list]
            own_lists = [dict({"account": "True"}, **item) for item in own_lists]
            misc_lists = [item for item in lists if item["id"] not in id_list]
            return own_lists + misc_lists

        def update_states(self):
            xbmc.sleep(2000)  # delay because MovieDB takes some time to update
            _, __, self.account_states = extended_movie_info(self.info["id"], self.dbid, 0)
            super(DialogVideoInfo, self).update_states()

        def remove_list_dialog(self, account_lists):
            listitems = ["%s (%i)" % (d["name"], d["item_count"]) for d in account_lists]
            index = xbmcgui.Dialog().select(LANG(32138), listitems)
            if index >= 0:
                remove_list(account_lists[index]["id"])
                self.update_states()

        @ch.click(18)
        def add_movie_to_library(self):
            MovieLibrary = METALLIQ.getSetting("movies_library_folder")
            imdb_id = self.info["imdb_id"]
            if not os.path.exists(xbmc.translatePath("%s%s/" % (MovieLibrary, imdb_id))):
                xbmc.executebuiltin("RunPlugin(plugin://plugin.video.metalliq-forqed/movies/add_to_library/tmdb/%s)" % self.info.get("id", ""))
                notify(header='Added "%s" to library' % self.info.get("title", ""), message="Starting library scan now", icon=self.info["poster"], time=5000, sound=False)
                after_add(type="movie")
            else:
                notify(header="To refresh all content:", message="Exit %s & re-enter" % ADDON_NAME, icon=self.info["poster"], time=5000, sound=False)

        @ch.click(19)
        def remove_movie_from_library(self):
            MovieLibrary = METALLIQ.getSetting("movies_library_folder")
            imdb_id = self.info["imdb_id"]
            if os.path.exists(xbmc.translatePath("%s%s/" % (MovieLibrary, imdb_id))):
                get_kodi_json(method="VideoLibrary.RemoveMovie", params='{"movieid": %d}' % int(self.info["dbid"]))
                import shutil
                shutil.rmtree(xbmc.translatePath("%s%s/" % (MovieLibrary, imdb_id)))
                notify(header='Removed "%s" from library' % self.info.get("title", ""), message="Exit & re-enter to refresh", icon=self.info["poster"], time=5000, sound=False)
                after_add(type="movie")
            else:
                notify(header="To refresh all content:", message="Exit %s & re-enter" % ADDON_NAME, icon=self.info["poster"], time=5000, sound=False)

        @run_async
        def join_omdb_async(self):
            self.omdb_thread.join()
            pass_dict_to_skin(data=self.omdb_thread.listitems,
                              prefix="movie.omdb.",
                              window_id=self.window_id)

    class SetItemsThread(threading.Thread):

        def __init__(self, set_id=""):
            threading.Thread.__init__(self)
            self.set_id = set_id

        def run(self):
            if self.set_id:
                self.listitems, self.setinfo = get_set_movies(self.set_id)
                self.id_list = [item["id"] for item in self.listitems]
            else:
                self.id_list = []
                self.listitems = []
                self.setinfo = {}

    return DialogVideoInfo
