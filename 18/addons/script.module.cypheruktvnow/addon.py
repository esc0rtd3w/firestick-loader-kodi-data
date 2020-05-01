# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 RACC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from xbmcgui import ListItem
from routing import Plugin

import time
import os
import warnings
import traceback

import requests
import requests_cache
import urllib
from datetime import timedelta
from base64 import b64encode
from pyDes import des, PAD_PKCS5


import urllib2


addon = xbmcaddon.Addon()
plugin = Plugin()
plugin.name = addon.getAddonInfo('name')
user_agent = 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)'
USER_DATA_DIR = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
CACHE_TIME = int(addon.getSetting('cache_time'))
CACHE_FILE = os.path.join(USER_DATA_DIR, 'cache')
expire_after = timedelta(hours=CACHE_TIME)

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

s = requests_cache.CachedSession(CACHE_FILE, allowable_methods='POST', expire_after=expire_after, old_data_on_error=True)
s.headers.update({'User-Agent': 'USER-AGENT-UKTVNOW-APP-V2'})

token_url = 'http://uktvnow.net/uktvnow8/index_new.php?case=get_channel_link_with_token_revision'
list_url = 'http://uktvnow.net/uktvnow8/index_new.php?case=get_all_channels'

def quote(s):
    return urllib.quote(s.encode('utf-8'), str(''))


def unquote(s):
    return urllib.unquote(s).decode('utf-8')


@plugin.route('/')
def root():
    categories = {"01": "UK & USA Channels",
                  "02": "Movies",
                  "03": "Music",
                  "04": "News",
                  "05": "Sport",
                  "06": "Documentary",
                  "07": "Kids",
                  "08": "Food",
                  "09": "Religious"}
    list_items = []
    for cat in categories.keys():
        li = ListItem(categories[cat])
        url = plugin.url_for(list_channels, cat_id=cat.lstrip('0'))
        list_items.append((url, li, True))

    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/list_channels/<cat_id>')
def list_channels(cat_id=None):
    list_items = []
    r = s.post(list_url, headers={'app-token': '9120163167c05aed85f30bf88495bd89'}, data={'username': '603803577'}, timeout=15)
    ch = r.json()

    for c in ch['msg']['channels']:
        if c['cat_id'] == cat_id:
            image = "http://uktvnow.net/uktvnow8/{0}|User-Agent={1}".format(urllib.quote(c['img'].encode('utf-8')), quote(user_agent))
            li = ListItem(c['channel_name'].rstrip('.'))
            li.setProperty("IsPlayable", "true")
            li.setArt({'thumb': image, 'icon': image})
            li.setInfo(type='Video', infoLabels={'Title': c['channel_name'].rstrip('.'),
                                                 'mediatype': 'video',
                                                 'PlayCount': 0})
            try:
                li.setContentLookup(False)
            except:
                pass
            url = plugin.url_for(play, ch_id=c['pk_id'])
            list_items.append((url, li, False))

    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/play/<ch_id>')
def play(ch_id, link=None):
    # 178.132.5.135 193.70.111.192 137.74.200.60 149.202.197.108
    key = b"10912895"


    r = s.post(list_url, headers={'app-token': '9120163167c05aed85f30bf88495bd89'}, data={'username': '603803577'}, timeout=15)
    ch = r.json()
    for c in ch['msg']['channels']:
        if c['pk_id'] == ch_id:
            selected_channel = c
            break

    title = selected_channel.get('channel_name')
    icon = selected_channel.get('img')
    image = "http://uktvnow.net/uktvnow8/{0}|User-Agent={1}".format(urllib.quote(icon.encode('utf-8')), quote(user_agent))

    with s.cache_disabled():
        r = s.post(token_url, headers={'app-token': '9120163167c05aed85f30bf88495bd89'}, data={'channel_id': ch_id, 'username': '603803577'}, timeout=15)

    links = []
    for stream in r.json()['msg']['channel'][0].keys():
        if 'stream' in stream or 'chrome_cast' in stream:
            d = des(key)
            link = d.decrypt(r.json()['msg']['channel'][0][stream].decode('base64'), padmode=PAD_PKCS5)
            if link:
                if not link == 'dummytext':
                    links.append(link)

    if addon.getSetting('autoplay') == 'true':
        link = links[0]
    else:
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Choose Stream', links)
        link = links[ret]

    if 'uktvnow.net' and 'playlist.m3u8' in link:
        media_url = '{0}|User-Agent={1}'.format(link, quote(user_agent))

        if addon.getSetting('inputstream') == 'true':
            li = ListItem(title, path=media_url)
            li.setArt({'thumb': image, 'icon': image})
            li.setMimeType('application/vnd.apple.mpegurl')
            li.setProperty('inputstreamaddon', 'inputstream.adaptive')
            li.setProperty('inputstream.adaptive.manifest_type', 'hls')
            li.setProperty('inputstream.adaptive.stream_headers', media_url.split('|')[-1])

        elif addon.getSetting('livestreamer') == 'true':
            serverPath = os.path.join(xbmc.translatePath(addon.getAddonInfo('path')), 'livestreamerXBMCLocalProxy.py')
            runs = 0
            while not runs > 10:
                try:
                    requests.get('http://127.0.0.1:19001/version')
                    break
                except:
                    xbmc.executebuiltin('RunScript(' + serverPath + ')')
                    runs += 1
                    xbmc.sleep(600)

            livestreamer_url = 'http://127.0.0.1:19001/livestreamer/'+b64encode('hlsvariant://'+media_url)
            li = ListItem(title, path=livestreamer_url)
            li.setArt({'thumb': image, 'icon': image})
            li.setMimeType('video/x-mpegts')
        else:
            li = ListItem(title, path=media_url)
            li.setArt({'thumb': image, 'icon': image})
            li.setMimeType('application/vnd.apple.mpegurl')

    else:
        media_url = link
        li = ListItem(title, path=media_url)
        li.setArt({'thumb': image, 'icon': image})

    try:
        li.setContentLookup(False)
    except:
        pass

    xbmcplugin.setResolvedUrl(plugin.handle, True, li)


if __name__ == '__main__':
    try:
        plugin.run()
    except requests.exceptions.RequestException:
        dialog = xbmcgui.Dialog()
        dialog.notification(plugin.name, "Web Request Exception", xbmcgui.NOTIFICATION_ERROR)
        traceback.print_exc()
