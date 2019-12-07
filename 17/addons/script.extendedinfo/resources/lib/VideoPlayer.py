# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcgui
import yt
from WindowManager import wm
from Utils import *


class VideoPlayer(xbmc.Player):

    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self)
        self.stopped = False

    def onPlayBackEnded(self):
        self.stopped = True

    def onPlayBackStopped(self):
        self.stopped = True

    def onPlayBackStarted(self):
        self.stopped = False

    def play(self, url, listitem, window=False):
        if window and window.window_type == "dialog":
            wm.add_to_stack(window)
            window.close()
        super(VideoPlayer, self).play(item=url,
                                      listitem=listitem,
                                      windowed=False,
                                      startpos=-1)
        if window and window.window_type == "dialog":
            self.wait_for_video_end()
            wm.pop_stack()

    def qlickplay(self, url, listitem, window=False, dbid=0):
        if dbid != 0 : item = '{"movieid": %s}' % dbid
        else: item = '{"file":"%s"}' % url
        get_kodi_json(method="Player.Open", params='{"item": %s, "options":{"resume": true}}' % item )
        if ADDON.getSetting("window_mode") == "false":
            if xbmc.getCondVisibility("player.hasvideo"):
                if window is not False and window is not True:
                    wm.add_to_stack(window)
                    window.close()
                    self.wait_for_video_end()
                    return wm.pop_stack()
            else:
                for i in range(10):
                    xbmc.sleep(750)
                    while xbmc.getCondVisibility('Window.IsActive(progressdialog)') or xbmc.getCondVisibility('Window.IsActive(extendedprogressdialog)') or xbmc.getCondVisibility('Window.IsActive(selectdialog)') or xbmc.getCondVisibility('Window.IsActive(notification)') or xbmc.getCondVisibility('Window.IsActive(busydialog)'):
                        for i in range(100):
                            xbmc.sleep(100)
                            if xbmc.getCondVisibility("player.hasvideo"):
                                xbmc.sleep(500)
                                if xbmc.getCondVisibility("player.hasvideo"):
                                    wm.add_to_stack(window)
                                    window.close()
                                    self.wait_for_video_end()
                                    return wm.pop_stack()
                            xbmc.sleep(100)
                    xbmc.sleep(750)

    def playtube(self, youtube_id=False, listitem=None, window=False):
        url = "plugin://plugin.video.youtube/play/?video_id=%s" % youtube_id
        self.qlickplay(url=url, listitem=listitem, window=window)

    def play_youtube_video(self, youtube_id="", listitem=None, window=False):
        url = "plugin://plugin.video.youtube/play/?video_id=%s" % youtube_id
        self.qlickplay(url=url, listitem=listitem, window=window)

    def play_youtube_playlist(self, youtube_id="", listitem=None, window=False):
        xbmc.executebuiltin("PlayMedia(plugin://plugin.video.youtube/playlist/%s/)" % youtube_id)
        window.close()


    @busy_dialog
    def youtube_info_by_id(self, youtube_id):
        import YDStreamExtractor
        vid = YDStreamExtractor.getVideoInfo(youtube_id,
                                             quality=1)
        if not vid:
            return None, None
        listitem = xbmcgui.ListItem(label=vid.title,
                                    thumbnailImage=vid.thumbnail)
        listitem.setInfo(type='video',
                         infoLabels={"genre": vid.sourceName,
                                     "plot": vid.description})
        return vid.streamURL(), listitem

    def wait_for_video_end(self):
        xbmc.sleep(500)
        while not self.stopped:
            xbmc.sleep(200)
        self.stopped = False
