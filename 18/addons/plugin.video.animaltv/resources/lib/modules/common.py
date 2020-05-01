"""
    Animal TV Add-on
    Developed by mhancoc7

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

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import m7lib

try:
    # Python 3
    from urllib.parse import parse_qs
except ImportError:
    # Python 2
    from urlparse import parse_qs

dlg = xbmcgui.Dialog()
addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_id = addon.getAddonInfo('id')
plugin_path = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(plugin_path, 'icon.png'))
fanart = xbmc.translatePath(os.path.join(plugin_path, 'icon.png'))

class AnimalTV:
    def __init__(self):
        self.plugin_queries = parse_query(sys.argv[2][1:])


def dlg_oops(heading):
    dlg.ok(heading, "Oops something went wrong.")
    exit()


def stream_list():
    try:
        streams = m7lib.Stream.get_explore_org_streams()
        for stream in sorted(streams, key=lambda k: k['title']):
            if (sys.version_info > (3, 0)):
                # Python 3
                m7lib.Common.add_channel(stream["id"], stream["icon"], stream["fanart"], stream["title"].decode('UTF-8'))
            else:
                # Python 2
                m7lib.Common.add_channel(stream["id"], stream["icon"], stream["fanart"], stream["title"])
    except StandardError:
        dlg_oops(addon_name)


def play_stream(video_id):
    try:
        stream_url = m7lib.Common.get_playable_youtube_url(video_id)
        m7lib.Common.play(stream_url)
    except StandardError:
        dlg_oops(addon_name)


def parse_query(query, clean=True):
    queries = parse_qs(query)

    q = {}
    for key, value in queries.items():
        q[key] = value[0]
    if clean:
        q['mode'] = q.get('mode', 'main')
    return q

