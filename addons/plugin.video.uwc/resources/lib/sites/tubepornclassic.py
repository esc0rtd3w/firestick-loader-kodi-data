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

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

progress = utils.progress


@utils.url_dispatcher.register('360')
def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.tubepornclassic.com/categories/', 363, '', '')
    utils.addDir('[COLOR hotpink]Top Rated[/COLOR]','http://www.tubepornclassic.com/top-rated/', 361, '', '')
    utils.addDir('[COLOR hotpink]Most Viewed[/COLOR]','http://www.tubepornclassic.com/most-popular/', 361, '', '')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.tubepornclassic.com/search/', 364, '', '')    
    List('http://www.tubepornclassic.com/latest-updates/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('361', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        return None
    match = re.compile('<a href="([^"]+)" title="([^"]+)".*?src="([^"]+)".*?duration">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, name, img, duration in match:
        name = utils.cleantext(name)
        name = name + " [COLOR deeppink]" + duration + "[/COLOR]"
        utils.addDownLink(name, videopage, 362, img, '')
    try:
        nextp = re.compile('<a href="([^"]+)"[^>]+>Next', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', 'http://www.tubepornclassic.com/' + nextp[0], 361,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('364', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 364)
    else:
        title = keyword.replace(' ','%20')
        searchUrl = searchUrl + title + "/"
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('363', ['url'])
def Cat(url):
    listhtml = utils.getHtml(url, '')
    match = re.compile('<a class="list-item__link" href="([^"]+)" title="([^"]+)".*?class="list-item__info">([^<]+)', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for catpage, name, videos in match:
        name = utils.cleantext(name) + " [COLOR deeppink]" + videos + "[/COLOR]"
        utils.addDir(name, catpage, 361)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('362', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    vp = utils.VideoPlayer(name, download, None, 'video_url="([^"]+)"')
    vp.play_from_site_link(url)
