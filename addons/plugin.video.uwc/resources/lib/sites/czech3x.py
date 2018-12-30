'''
    Ultimate Whitecream
    Copyright (C) 2016 Whitecream

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

import xbmcplugin
from resources.lib import utils

    
@utils.url_dispatcher.register('310')
def Main():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://czech3x.net/',313,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://czech3x.net/?s=',314,'','')
    List('http://czech3x.net')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('311', ['url'])
def List(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        return None
    match = re.compile('<div id="main">(.*?)<div id="sidebar', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    match1 = re.compile(r'data-id="\d+" title="([^"]+)" href="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match)
    for name, videopage, img in match1:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 312, img, '')
    try:
        nextp = re.compile('link rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
        utils.addDir('Next Page', nextp[0], 311,'')
    except:
        pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('312', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)


@utils.url_dispatcher.register('313', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<a href="(http://czech3x.net/category/[^"]+)" >([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 311, '')    
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('314', ['url'], ['keyword'])
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 314)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        List(searchUrl)

