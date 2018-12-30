'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream

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
import sys
import json

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

# from youtube-dl
from resources.lib.compat import (
    compat_chr,
    compat_ord,
    compat_urllib_parse_unquote,
)

dialog = utils.dialog
addon = utils.addon


def BGVersion():
    bgpage = utils.getHtml('https://beeg.com','')
    bgversion = re.compile(r"cpl/(\d+)\.js", re.DOTALL | re.IGNORECASE).findall(bgpage)[0]
    bgsavedversion = addon.getSetting('bgversion')
    if bgversion != bgsavedversion or not addon.getSetting('bgsalt'):
        addon.setSetting('bgversion',bgversion)
        bgjspage = utils.getHtml('https://beeg.com/static/cpl/'+bgversion+'.js','https://beeg.com')
        bgsalt = re.compile('beeg_salt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(bgjspage)[0]
        addon.setSetting('bgsalt',bgsalt)


@utils.url_dispatcher.register('80')
def BGMain():
    BGVersion()
    bgversion = addon.getSetting('bgversion')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','https://beeg.com/api/v6/'+bgversion+'/index/main/0/pc',83,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://beeg.com/api/v6/'+bgversion+'/index/main/0/pc?query=',84,'','')
    BGList('https://beeg.com/api/v6/'+bgversion+'/index/main/0/pc')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('81', ['url'])
def BGList(url):
    bgversion = addon.getSetting('bgversion')
    try:
        listjson = utils.getHtml(url,'')
    except:
        return None
    match = re.compile(r'\{"title":"([^"]+)","id":"([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listjson)
    for title, videoid in match:
        img = "https://img.beeg.com/236x177/" + videoid +  ".jpg"
        videopage = "https://beeg.com/api/v6/" + bgversion + "/video/" + videoid
        name = title.encode("utf8")
        utils.addDownLink(name, videopage, 82, img, '')
    try:
        page=re.compile('https://beeg.com/api/v6/' + bgversion + '/index/[^/]+/([0-9]+)/pc', re.DOTALL | re.IGNORECASE).findall(url)[0]
        page = int(page)
        npage = page + 1
        jsonpage = re.compile(r'pages":(\d+)', re.DOTALL | re.IGNORECASE).findall(listjson)[0]
        if int(jsonpage) > page:
            nextp = url.replace("/"+str(page)+"/", "/"+str(npage)+"/")
            utils.addDir('Next Page ('+str(npage)+')', nextp,81,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)

# from youtube-dl   
def split(o, e):
    def cut(s, x):
        n.append(s[:x])
        return s[x:]
    n = []
    r = len(o) % e
    if r > 0:
        o = cut(o, r)
    while len(o) > e:
        o = cut(o, e)
    n.append(o)
    return n

def decrypt_key(key):
    bgsalt = addon.getSetting('bgsalt')
    # Reverse engineered from http://static.beeg.com/cpl/1738.js
    a = bgsalt
    e = compat_urllib_parse_unquote(key)
    o = ''.join([
        compat_chr(compat_ord(e[n]) - compat_ord(a[n % len(a)]) % 21)
        for n in range(len(e))])
    return ''.join(split(o, 3)[::-1])   


@utils.url_dispatcher.register('82', ['url', 'name'], ['download'])
def BGPlayvid(url, name, download=None):
    videopage = utils.getHtml(url,'http://beeg.com')
    videopage = json.loads(videopage)
   
    if not videopage["240p"] == None:
        url = videopage["240p"].encode("utf8")
    if not videopage["480p"] == None:
        url = videopage["480p"].encode("utf8")
    if not videopage["720p"] == None:
        url = videopage["720p"].encode("utf8")

    url = url.replace("{DATA_MARKERS}","data=pc_XX")
    if not url.startswith("http:"): url = "https:" + url
    
    key = re.compile("/key=(.*?)%2Cend", re.DOTALL | re.IGNORECASE).findall(url)[0]
    decryptedkey = decrypt_key(key)
    
    videourl = url.replace(key, decryptedkey)

    if download == 1:
        utils.downloadVideo(videourl, name)
    else:
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


@utils.url_dispatcher.register('83', ['url'])
def BGCat(url):
    bgversion = addon.getSetting('bgversion')
    caturl = utils.getHtml2(url)
    tags = re.compile(r'"nonpopular":\[(.*?)\]', re.DOTALL | re.IGNORECASE).findall(caturl)[0]
    tags = re.compile('"([^"]+)"', re.DOTALL | re.IGNORECASE).findall(tags)
    for tag in tags:
        videolist = "https://beeg.com/api/v6/"+bgversion+"/index/tag/0/mobile?tag=" + tag.encode("utf8")
        name = tag.encode("utf8")
        name = name[:1].upper() + name[1:]
        utils.addDir(name, videolist, 81, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('84', ['url'], ['keyword'])
def BGSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 84)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        BGList(searchUrl)
