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
import traceback

import requests
import requests_cache
import urllib
import urllib2
import urlparse
import json
from base64 import b64encode
from datetime import timedelta


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

requests_cache.core.install_cache(CACHE_FILE, expire_after=expire_after, old_data_on_error=True)
requests_cache.core.remove_expired_responses()

USER = 'SolidStreamz'
PASS = '@!SolidStreamz!@'
data_url = 'http://solidstreamz.com/api/streamzdata.php'

#USER = 'GeoDATA'
#PASS = '%!GEODATA!%'
#data_url = 'http://www.solidstreamz.com/geopocket/streamzdata.php'

r = requests.post(data_url, headers = {'User-Agent': user_agent}, auth=(USER, PASS))
res_b64 = r.text
res = json.loads((res_b64[:2] + res_b64[3:]).decode('base-64'), strict=False)

api_url = '{0}/panel_api.php?mode=live&username={1}&password={2}'.format(res['DATA'][0]['MainURL'],
                                                                         res['DATA'][0]['Username'],
                                                                         res['DATA'][0]['Password'])

def quote(s):
    return urllib.quote(s.encode('utf-8'), str(''))


def unquote(s):
    return urllib.unquote(s).decode('utf-8')


@plugin.route('/')
def root():
    r = requests.get(api_url, headers = {'User-Agent': user_agent})
    api_res = r.json()
    list_items = []
    categories = []
    for ch in api_res['available_channels'].keys():
        categories.append((api_res['available_channels'][ch]['category_id'],api_res['available_channels'][ch]['category_name']))

    categories = set(categories)
    while categories:
        cat = categories.pop()
        li = ListItem(cat[1])
        url = plugin.url_for(list_channels, cat_id=cat[0])
        list_items.append((url, li, True))


    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/list_channels/<cat_id>')
def list_channels(cat_id=None):
    r = requests.get(api_url, headers = {'User-Agent': user_agent})
    api_res = r.json()
    list_items = []
    for ch in api_res['available_channels'].keys():
        if api_res['available_channels'][ch]['category_id'] == cat_id:
            li = ListItem(api_res['available_channels'][ch]['name'])
            li.setProperty("IsPlayable", "true")
            li.setArt({'thumb': '{0}|User-Agent={1}'.format(api_res['available_channels'][ch]['stream_icon'], quote(user_agent))})
            li.setInfo(type='Video', infoLabels={'Title': api_res['available_channels'][ch]['name'], 'mediatype': 'video'})
            l = 'http://{0}:{1}/live/{2}/{3}/{4}.ts'.format(api_res['server_info']['url'],
                                                            api_res['server_info']['port'],
                                                            api_res['user_info']['username'],
                                                            api_res['user_info']['password'],
                                                            ch)
            url = plugin.url_for(play, link=quote(l),
                                label=quote(api_res['available_channels'][ch]['name']),
                                thumb=quote(api_res['available_channels'][ch]['stream_icon'] or '_'))
            list_items.append((url, li, False))


    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/play/<link>/<label>/<thumb>')
def play(link, label, thumb):
    link = urllib.unquote(link)
    label = unquote(label)
    thumb = "{0}|User-Agent={1}".format(unquote(thumb), quote(user_agent))
    url = '{0}|User-Agent={1}'.format(link, quote(res['DATA'][0]['UserAgent']))

    if addon.getSetting('ts') == 'true':
        media_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url={0}&name={1}&imgurl={2}'.format(quote(url), quote(label), quote(thumb))
    else:
        media_url = url
    li = ListItem(label, path=media_url)
    li.setArt({'thumb': thumb})
    xbmcplugin.setResolvedUrl(plugin.handle, True, li)


if __name__ == '__main__':
    try:
        plugin.run()
    except requests.exceptions.RequestException:
        dialog = xbmcgui.Dialog()
        dialog.notification(plugin.name, "Web Request Exception", xbmcgui.NOTIFICATION_ERROR)
        traceback.print_exc()
