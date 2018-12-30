'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream
    Copyright (C) 2015 NothingGnome

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

base_url = 'https://spankbang.com'
main_mode = 440
list_mode =  441
play_mode = 442
categories_mode = 443
search_mode = 444


@utils.url_dispatcher.register('440')
def Main():
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://spankbang.com/s/', search_mode, '', '')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','https://spankbang.com/categories', categories_mode, '', '')
    List('https://spankbang.com/new_videos/1/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('441', ['url'])
def List(url):
    print "spankbang::List " + url
    try:
        listhtml = utils.getHtml(url, '')
    except:
        return None
    main_block = re.compile('<main id="container">(.*?)</main>', re.DOTALL).findall(listhtml)[0]
    match = re.compile('<a href="([^"]+)" class="thumb.*?<img src="([^"]+)" alt="([^"]+)" class="cover.*?</span>(.*?)i-len"><i class="fa fa-clock-o"></i>([^<]+)<', re.DOTALL).findall(main_block)
    for videopage, img, name, hd, duration in match:
        if hd.find('HD') > 0:
            hd = " [COLOR orange]HD[/COLOR] "
        else:
            hd = " "
        name = utils.cleantext(name) + hd + "[COLOR deeppink]" + duration + "m[/COLOR]"
        utils.addDownLink(name, base_url + videopage, play_mode, 'https:' + img, '')
    try:
        nextp=re.compile('<li class="active"><a>.+?</a></li><li><a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', base_url + nextp[0], list_mode,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('444', ['url'], ['keyword'])
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, search_mode)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title + '/'
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('443', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<a href="/category/([^"]+)"><img src="([^"]+)"><span>([^>]+)</span>', re.DOTALL).findall(cathtml)
    for catpage, img, name in match:
        utils.addDir(name, base_url + '/category/' + catpage, list_mode, base_url + img, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('442', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    vp = utils.VideoPlayer(name, download)
    vp.progress.update(25, "", "Loading video page", "")
    html = utils.getHtml(url, '')
    sources = {}
    srcs = re.compile("stream_url_(240p|320p|480p|720p|1080p|4k).*?= '([^']+|)'", re.DOTALL | re.IGNORECASE).findall(html)
    for quality, videourl in srcs:
        if videourl:
            sources[quality] = videourl
    videourl = utils.selector('Select quality', sources, dont_ask_valid=True, sort_by=lambda x: 1081 if x == '4k' else int(x[:-1]), reverse=True)
    vp.play_from_direct_link(videourl)
