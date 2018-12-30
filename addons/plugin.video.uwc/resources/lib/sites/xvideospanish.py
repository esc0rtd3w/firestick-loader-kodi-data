'''
    Ultimate Whitecream
    Copyright (C) 2018 Whitecream, Fr33m1nd, holisticdioxide

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


@utils.url_dispatcher.register('130')
def Main():
    utils.addDir('[COLOR hotpink]Tags[/COLOR]','http://www.xvideospanish.net/tags/',133,'','')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://www.xvideospanish.net/videos-pornos-por-productora-gratis/',135,'','')
    utils.addDir('[COLOR hotpink]Actors[/COLOR]','http://www.xvideospanish.net/actors/',136,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.xvideospanish.net/?s=',134,'','')
    List('http://www.xvideospanish.net/', False)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('131', ['url'], ['next_page_needed'])
def List(url, next_page_needed=True):
    try:
        listhtml = utils.getHtml(url, '')
    except:
        return None
    main = re.compile('<main.*?>(.*?)</main>', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    match = re.compile('<a href="([^"]+)" title="([^"]+)".*?data-src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(main)
    for videopage, name, img in match:
        name = utils.cleantext(name)
        utils.addDownLink(name, videopage, 132, img, '')
    if next_page_needed:
        try:
            nextp=re.compile('<link rel="next" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
            utils.addDir('Next Page', nextp, 131,'')
        except:
            pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('134', ['url'], ['keyword'])    
def Search(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 134)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        List(searchUrl)


@utils.url_dispatcher.register('133', ['url'])
def Tags(url):
    cathtml = utils.getHtml(url, '')
    cathtml = re.compile('<main.*?>(.*?)</main>', re.DOTALL | re.IGNORECASE).findall(cathtml)[0]
    match = re.compile('<a href="([^"]+)" class="tag-cloud-link.*?>([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage, 131)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('135', ['url'])
def Categories(url):
    cathtml = utils.getHtml(url, '')
    cathtml = re.compile('<main.*?>(.*?)</main>', re.DOTALL | re.IGNORECASE).findall(cathtml)[0]
    match = re.compile('<a href="([^"]+)" title="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name, img in match:
        utils.addDir(name, catpage, 131, img)
    xbmcplugin.endOfDirectory(utils.addon_handle) 


@utils.url_dispatcher.register('136', ['url'])
def Actors(url):
    cathtml = utils.getHtml(url, '')
    cathtml = re.compile('<main.*?>(.*?)</main>', re.DOTALL | re.IGNORECASE).findall(cathtml)[0]
    match = re.compile('<a href="([^"]+)".*?</i>([^<]+)', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name, catpage.strip(), 131)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('132', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
    html = utils.getHtml(url, url)
    vp = utils.VideoPlayer(name, download, regex='''(?:SRC|src|"embedURL" content)=\s*["']([^'"]+)''')
    vp.play_from_html(html)
