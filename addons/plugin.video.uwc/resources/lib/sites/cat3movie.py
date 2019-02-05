'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream
    Copyright (C) 2015 anton40

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
import base64
import urllib

import xbmcplugin
from resources.lib import utils

progress = utils.progress

    
@utils.url_dispatcher.register('350')
def Main():
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://cat3movie.us/?s=', 353, '', '')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://cat3movie.us', 354, '', '')
    List('https://www.pubmovie.com/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('351', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    match = re.compile("<main(.*?)</main", re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    match1 = re.compile('<article id=.+?<a href="([^"]+)" title="([^"]+)">.+?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match)
    cookieString = getCookiesString()
    for videopage, name, img in match1:
        name = utils.cleantext(name)
        img = img + "|Cookie=" + urllib.quote(cookieString) + "&User-Agent=" + urllib.quote(utils.USER_AGENT)
        utils.addDownLink(name, videopage, 352, img, '')
    try:
        nextp=re.compile(r'<span class="active">\d+</span></li><li><a href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 351,'')
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


@utils.url_dispatcher.register('353', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 353)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('354', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<li class="cat-item cat-item.+?<a href="([^"]+)" title=.+?>(.+?)<').findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 351, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('352', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
	utils.PLAYVIDEO(url, name, download, 'iframe src="([^"]+)"')