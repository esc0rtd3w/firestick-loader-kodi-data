#/*
# *
# * TuneIn Radio for Kodi.
# *
# * Copyright (C) 2015 Brian Hornsby
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# */

import xbmc
import xbmcgui
import xbmcplugin
import sys
import kodisettings as settings
import kodiutils as utils


class Stream:

    def __init__(self, addonid):
        # Initialise settings.
        self.settings = settings.Settings(addonid, sys.argv)
        self.addonname = self.settings.get_name()
        self.prompt = self.settings.get('prompt') == "true"

    def __add_stream_to_playlist(self, playlist, stream, name=None, logo=None):
        if name:
            liz = xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=logo)
            liz.setInfo('music', {'Title': name})
            playlist.add(url=stream, listitem=liz)
        else:
            playlist.add(url=stream)

    def __add_streams(self, streams, name=None, logo=None):
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(self.addonname, 'Creating playlist')
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
        for count, stream in enumerate(streams):
            pDialog.update(
                50, 'Adding stream %d of %d to playlist' % (count + 1, len(streams)), stream)
            self.__add_stream_to_playlist(playlist, stream, name, logo)
        pDialog.close()
        if len(playlist) > 0:
            xbmcplugin.setResolvedUrl(
                handle=int(self.settings.get_argv(1)), succeeded=True, listitem=playlist[0])
        else:
            xbmcplugin.setResolvedUrl(
                handle=int(self.settings.get_argv(1)), succeeded=False, listitem=None)

    def play_streams(self, streams, name=None, logo=None):
        if (self.prompt and xbmc.Player().isPlayingAudio()):
            if (utils.yesno(self.addonname, self.settings.get_string(3005))):
                self.__add_streams(streams, name, logo)
        else:
            self.__add_streams(streams, name, logo)
