'''
    Ultimate Whitecream
    Copyright (C) 2016 Whitecream, hdgdl

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

import re
import os
import sys
import sqlite3

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils


@utils.url_dispatcher.register('480')
def Main():
	utils.addDir('[COLOR red]Refresh naked.com images[/COLOR]','',483,'',Folder=False)
	List('http://new.naked.com/')
	xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('481', ['url'])
def List(url):
    if utils.addon.getSetting("chaturbate") == "true":
        clean_database(False)
    try:
        data = utils.getHtml(url, '')
    except:
        
        return None
    model_list = re.compile('each-model-img[^?]+title="([^"]+)"[^?]+href="([^"]+)"[^?]+src="([^"]+)"[^?]+each-model-info', re.DOTALL | re.IGNORECASE).findall(data)
    for model, url, img in model_list:
        name = model.replace("'s webcam","").strip()
        videourl = "http://new.naked.com" + url
        utils.addDownLink(name, videourl, 482, img, '', noDownload=True)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('483')
def clean_database(showdialog=True):
    conn = sqlite3.connect(xbmc.translatePath("special://database/Textures13.db"))
    try:
        with conn:
            list = conn.execute("SELECT id, cachedurl FROM texture WHERE url LIKE '%%%s%%';" % ".nk-img.com")
            for row in list:
                conn.execute("DELETE FROM sizes WHERE idtexture LIKE '%s';" % row[0])
                try: os.remove(xbmc.translatePath("special://thumbnails/" + row[1]))
                except: pass
            conn.execute("DELETE FROM texture WHERE url LIKE '%%%s%%';" % ".nk-img.com")
            if showdialog:
                utils.notify('Finished','naked.com images cleared')
    except:
        pass


@utils.url_dispatcher.register('482', ['url', 'name'])
def Playvid(url, name):
    listhtml = utils.getHtml(url, '')
    match = re.compile('(hls_[0-9]+s_[0-9a-z]+)', re.DOTALL | re.IGNORECASE).findall(listhtml)
    if match:
        videourl = "https://static-transcode-k8s-do.camster.com/hls/" + match[0] + "/index.m3u8"
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        listitem.setProperty("IsPlayable","true")
        if int(sys.argv[1]) == -1:
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            pl.clear()
            pl.add(videourl, listitem)
            xbmc.Player().play(pl)
        else:
            listitem.setPath(str(videourl))
            xbmcplugin.setResolvedUrl(utils.addon_handle, True, listitem)
    else:
        utils.notify('Oh oh','Couldn\'t find a playable webcam link')
