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

import urllib
import re
import sys

import xbmcplugin
from resources.lib import utils

progress = utils.progress

@utils.url_dispatcher.register('230')
def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','https://k18.co/categories',233,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://k18.co/?s=',234,'','')
    List('https://k18.co/?filter=latest')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('231', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        return None
#    cookieString = getCookiesString()
    match = re.compile('<article id=(.+)<div class="video-archive-ad">', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    match1 = re.compile('<a href="([^"]+)" title="([^"]+)">.+?<img data-src="([^"]+).+?class="duration">([^<]+)</span>', re.DOTALL | re.IGNORECASE).findall(match)
    if match1 == []:
        match1 = re.compile('<a href="([^"]+)" title="([^"]+)">.+?<img data-src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match)	
        for videopage, name, img in match1:
            name = utils.cleantext(name)
            utils.addDownLink(name, videopage, 232, img, '')
    else:
        for videopage, name, img, duration in match1:
            name = utils.cleantext(name) + ' [COLOR deeppink]' + duration + '[/COLOR]'
            utils.addDownLink(name, videopage, 232, img, '')
    try:
        match = re.compile('<div class="pagination">(.+?)</div>', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        match = match.replace("'",'"')
        match1 = re.compile('href="([^"]+)".*?>([^<]+)</a>', re.DOTALL | re.IGNORECASE).findall(match)
        for pageurl, pagenumber in match1:        
            utils.addDir('[COLOR deeppink]Page (' + str(pagenumber) + ')[/COLOR]', pageurl, 231,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


def getCookiesString():
    cookieString=""
    import cookielib
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(utils.cookiePath,ignore_discard=True)
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except:
        import sys,traceback
        traceback.print_exc(file=sys.stdout)
    return cookieString


@utils.url_dispatcher.register('234', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 234)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)

@utils.url_dispatcher.register('233', ['url'])
def Cat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<article.+?href="([^"]+)" title="([^"]+)".+? src="([^"]+)" ', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name, img in match:
        utils.addDir(name, catpage, 231, img)
    try:
        match = re.compile('<div class="pagination">(.+?)</div>', re.DOTALL | re.IGNORECASE).findall(cathtml)[0]
        match = match.replace("'",'"')
        match1 = re.compile('href="([^"]+)".*?>([^<]+)</a>', re.DOTALL | re.IGNORECASE).findall(match)
        for pageurl, pagenumber in match1:        
            utils.addDir('[COLOR deeppink]Page (' + str(pagenumber) + ')[/COLOR]', pageurl, 233,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)   


@utils.url_dispatcher.register('232', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
# needs fixing ...
    utils.PLAYVIDEO(url, name, download, 'td><a href="([^"]+)"><img class')
