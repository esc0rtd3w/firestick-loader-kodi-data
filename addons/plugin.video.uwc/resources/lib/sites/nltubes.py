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

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

sitelist = ['https://www.poldertube.nl', 'https://porno.milf.nl/', 'https://www.sextube.nl']


@utils.url_dispatcher.register('100', ['url'], ['page'])
def NLTUBES(url, page=1):
    siteurl = sitelist[page]
    utils.addDir('[COLOR hotpink]Categories[/COLOR]', siteurl + '/categorieen',103,'', page)
    if page == 0:
        utils.addDir('[COLOR hotpink]Search[/COLOR]', siteurl + '/pornofilms/zoeken/',104,'', page)
    else:
        utils.addDir('[COLOR hotpink]Search[/COLOR]', siteurl + '/videos/zoeken/',104,'', page)
    NLVIDEOLIST(url, page)


@utils.url_dispatcher.register('101', ['url'], ['page'])
def NLVIDEOLIST(url, page=1):
    siteurl = sitelist[page]
    try:
        link = utils.getHtml(url, '')
    except:
        
        return None
    match = re.compile(r'<article([^>]*)>.*?href="([^"]+)".*?src="([^"]+)".*?alt="([^"]+).*?duration">[^\d]+([^\s<]+)(?:\s|<)', re.DOTALL | re.IGNORECASE).findall(link)
    for hd, url, img, name, duration in match:
        if len(hd) > 2:
            hd = " [COLOR orange]HD[/COLOR] "
        else:
            hd = " "
        videourl = url if url.startswith('http') else siteurl + url
        duration2 = "[COLOR deeppink]" +  duration + "[/COLOR]"
        utils.addDownLink(name + hd + duration2, videourl, 102, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)" title="volg', re.DOTALL | re.IGNORECASE).findall(link)
        nextp = siteurl + nextp[0]
        utils.addDir('Next Page', nextp,101,'',page)
    except: pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


@utils.url_dispatcher.register('102', ['url', 'name'], ['download'])
def NLPLAYVID(url,name, download=None):
    videopage = utils.getHtml(url, '')
    videourl = re.compile('<source src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videourl[0]
    if download == 1:
        utils.downloadVideo(videourl, name)
    else:    
        iconimage = xbmc.getInfoImage("ListItem.Thumb")
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
        xbmc.Player().play(videourl, listitem)


@utils.url_dispatcher.register('104', ['url'], ['page', 'keyword'])  
def NLSEARCH(url, page=1, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 104, page)
    else:
        title = keyword.replace(' ','%20')
        searchUrl = searchUrl + title
        NLVIDEOLIST(searchUrl, page)


@utils.url_dispatcher.register('103', ['url'], ['page'])
def NLCAT(url, page=1):
    siteurl = sitelist[page]
    link = utils.getHtml(url, '')
    tags = re.compile('<div class="category".*?href="([^"]+)".*?<h2>([^<]+)<.*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for caturl, catname, catimg in tags:
        catimg = siteurl + catimg
        utils.addDir(catname,caturl,101,catimg,page)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
