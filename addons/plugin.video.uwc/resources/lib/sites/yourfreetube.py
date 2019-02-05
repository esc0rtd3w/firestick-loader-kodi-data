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


@utils.url_dispatcher.register('190')
def YFTMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','https://www.yourfreetube.net/',193,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://www.yourfreetube.net/search.php?keywords=',194,'','')
    YFTList('https://www.yourfreetube.net/new-videos/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('191', ['url'])
def YFTList(url):
	try:
		listhtml = utils.getHtml(url)
	except:
		
		return None
	match0= re.compile('blog-items blog-items-control site__row grid(.+?)site__col main-sidebar main-sidebar-control', re.DOTALL).findall(listhtml)[0]
#
	match = re.compile('data-post-id=.+?href="(.+?)" title="(.+?)".+?src="(.+?)"', re.DOTALL | re.IGNORECASE).findall(match0)
	for videopage, name, img in match:
		name = utils.cleantext(name)
		utils.addDownLink(name, videopage, 192, img, '')
	try:
		nextp=re.compile('\s+href="([^"]+)">&raquo;', re.DOTALL | re.IGNORECASE).findall(match0)[0]
		if not 'http' in nextp:
			nextp = "http://www.yourfreetube.net/" + nextp
		utils.addDir('Next Page', nextp, 191,'')
	except: pass
	xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('194', ['url'], ['keyword'])
def YFTSearch(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 194)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        YFTList(searchUrl)


@utils.url_dispatcher.register('193', ['url'])
def YFTCat(url):
	cathtml = utils.getHtml(url, '')

	#match = re.compile('<ul class="pm-browse-ul-subcats">(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)
	match1 = re.compile('-category menu-item.*?<a href="([^"]+)">(.+?)</a>', re.DOTALL | re.IGNORECASE).findall(cathtml)
	for catpage, name in match1:
		utils.addDir(name, catpage, 191, '')
	xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('192', ['url', 'name'], ['download'])
def YFTPlayvid(url, name, download=None):
    utils.PLAYVIDEO(url, name, download, '''src=\s*["']([^'"]+)''')

