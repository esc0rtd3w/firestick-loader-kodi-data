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
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','http://porn-czech.com/',313,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','http://porn-czech.com/?s=',314,'','') 
    List('http://porn-czech.com/')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('311', ['url'])
def List(url):
	try:
		listhtml = utils.getHtml(url, '')
	except:
		return None

	try:
		match = re.compile('</nav>(.+?)alert alert-info', re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
		match1 = re.compile(r'<a title="(.+?)" href="(.+?)"><img.+?src="(.+?)"', re.DOTALL | re.IGNORECASE).findall(match)
	except:
		match = re.compile(r'<div class="item-img">.+?<a href="(.+?)".+?src="(.+?)".+?<h3><a.+?>(.+?)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
		match1 = []
		for videopage, img, name in match:
			match1.append([name, videopage, img])
	for name, videopage, img in match1:
		name = utils.cleantext(name)
		utils.addDownLink(name, videopage, 312, img, '')
	try:
		nextp = re.compile('class="next page-numbers" href="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(listhtml)
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
    match = re.compile('<a href="(http://porn-czech.com/categories/[^"]+)">([^<]+)<', re.DOTALL | re.IGNORECASE).findall(cathtml)
    for catpage, name in match:
        utils.addDir(name.title(), catpage, 311, '')    
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

