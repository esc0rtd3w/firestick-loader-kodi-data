'''
    Animal TV Add-on

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
'''

from resources.lib import Addon, animaltv
import sys, os, urllib, urllib2
import json, base64
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

import re,urllib
from modules import client

def play(id):
    url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
    return url

addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_id = addon.getAddonInfo('id')
plugin_path = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')

Addon.plugin_url = sys.argv[0]
Addon.plugin_handle = int(sys.argv[1])
Addon.plugin_queries = Addon.parse_query(sys.argv[2][1:])

dlg = xbmcgui.Dialog()

Addon.log('plugin url: ' + Addon.plugin_url)
Addon.log('plugin queries: ' + str(Addon.plugin_queries))
Addon.log('plugin handle: ' + str(Addon.plugin_handle)) 

addon_logo = xbmc.translatePath(os.path.join(plugin_path,'tvaddons_logo.png'))

mode = Addon.plugin_queries['mode']

if mode == 'main':
    try:
        channels = animaltv.AnimalTV().get_channels()
        if channels:
            for c in channels:
                channel = c['channel'];
                id = c['id'];
                img = c['img']
                rURL = "plugin://plugin.video.animaltv/?id=" + id + "&channel=" + channel + "&mode=play&rand=" + Addon.random_generator()
                cm_refresh = ('Refresh', 'XBMC.RunPlugin(%s/?mode=refresh)' % (Addon.plugin_url))
                cm_menu = [cm_refresh]
           
                Addon.add_video_item(rURL,{'title': channel}, img=img, playable=True, cm=cm_menu, cm_replace=True)
        if len(Addon.get_setting('notify')) > 0:
            Addon.set_setting('notify', str(int(Addon.get_setting('notify')) + 1))  
        else:
            Addon.set_setting('notify', "1")        
        if int(Addon.get_setting('notify')) == 1:
            xbmcgui.Dialog().notification(addon_name + ' is provided by:','www.tvaddons.co',addon_logo,5000,False)
        elif int(Addon.get_setting('notify')) == 9:
            Addon.set_setting('notify', "0")
    except:
        dlg.ok(addon_name, 'Unable to connect to service. Please try again later.')
        exit()

elif mode == 'refresh':
    xbmc.executebuiltin('Container.Refresh')

elif mode == 'play':
    yt_addon = xbmcaddon.Addon('plugin.video.youtube')
    if yt_addon.getSetting('kodion.video.quality.mpd') != 'true':
        dlg.ok(addon_name, "This addon requires MPEG-DASH to be enabled in the YouTube addon. Once enabled try again.")
        yt_settings = xbmcaddon.Addon('plugin.video.youtube').openSettings()
        xbmc.executebuiltin('yt_settings')
    else:
        id = Addon.plugin_queries['id']
        channel = Addon.plugin_queries['channel']
        stream_status = animaltv.AnimalTV()._get_json('/status_json' + base64.b64decode('LnBocA=='), {'id': id})['status']
        if stream_status == 'live':
            stream_url = play(id)
            item = xbmcgui.ListItem(path=stream_url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            dlg.ok(addon_name, channel + " Offline")
            exit()

Addon.end_of_directory()
