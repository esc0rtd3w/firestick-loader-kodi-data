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

import xbmcplugin
from resources.lib import utils

progress = utils.progress


@utils.url_dispatcher.register('260')
def EROMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','https://www.ero-tik.com',263,'','')
    utils.addDir('[COLOR hotpink]Top Rated[/COLOR]','https://www.ero-tik.com/topvideos.html?page=1',261,'','')
    utils.addDir('[COLOR hotpink]Most Liked[/COLOR]','https://www.ero-tik.com/topvideos.html?do=rating&page=1',261,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://www.ero-tik.com/search.php?keywords=',264,'','')
    EROList('https://www.ero-tik.com/newvideos.html?page=1')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('261', ['url'])
def EROList(url):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        
        return None
    match = re.compile('pm-li-video.*?href="([^"]+)".*?src="([^"]+)".*?alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
    for videopage, img, name in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 262, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)">&raquo;', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        if re.search('http', nextp, re.DOTALL | re.IGNORECASE):
            next = nextp
        else:
            next = "https://www.ero-tik.com/" + nextp
        utils.addDir('Next Page', next, 261,'')
    except: pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('264', ['url'], ['keyword'])    
def EROSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 264)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        EROList(searchUrl)


@utils.url_dispatcher.register('263', ['url'])
def EROCat(url):
    cathtml = utils.getHtml(url, '')
    match = re.compile('<ul class="dropdown-menu">(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)[0]
    match1 = re.compile('href="(https://www.ero-tik.com/browse-[^"]+)"[^>]+>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(match)
    for catpage, name in match1:
        utils.addDir(name, catpage, 261, '')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('262', ['url', 'name'], ['download'])
def EROPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download)
