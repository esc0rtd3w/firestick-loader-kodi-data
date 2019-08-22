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
    YFTList('https://www.yourfreetube.net/newvideos.html')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('191', ['url'])
def YFTList(url):
	try:
		listhtml = utils.getHtml(url)
	except:
		
		return None
	match0= re.compile('<div id="wrapper">(.+?)</div><!-- end wrapper -->', re.DOTALL).findall(listhtml)[0]
#
	match = re.compile('<div class="pm-li-video">.+?<a href="([^"]+)".*?<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(match0)
	for videopage, img, name in match:
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

	match0 = re.compile('<ul class="pm-browse-ul-subcats">(.*?)</ul>', re.DOTALL | re.IGNORECASE).findall(cathtml)[0]
#	match1 = re.compile('-category menu-item.*?<a href="([^"]+)">(.+?)</a>', re.DOTALL | re.IGNORECASE).findall(cathtml)
	match = re.compile('<a href="([^"]+)".*?class="">(.+?)</a>', re.DOTALL | re.IGNORECASE).findall(match0)
	for catpage, name in match:
		utils.addDir(name, catpage, 191, '')
	xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('192', ['url', 'name'], ['download'])
#def YFTPlayvid(url, name, download=None):
#    utils.PLAYVIDEO(url, name, download, '''src=\s*["']([^'"]+)''')

def YFTPlayvid(url, name, download=None):
    links = {}
    vp = utils.VideoPlayer(name, download)
    vp.progress.update(25, "", "Loading video page", "")
    videopage = utils.getHtml(url)
    iframes = re.compile('<iframe.+?src="([^"]+)"[^>]+>.*?</iframe', re.DOTALL | re.IGNORECASE).findall(videopage)
    if iframes:
        for link in iframes:
            if vp.resolveurl.HostedMediaFile(link):
                links[link.split('/')[2]] = link
    srcs = re.compile('label="([^"]+)" src="([^"]+)" type=', re.DOTALL | re.IGNORECASE).findall(videopage)
    if srcs:
        for quality, videourl in srcs:
            links['Direct ' + quality] = videourl + '|Referer=%s&User-Agent=%s' % (url, utils.USER_AGENT)

    videourl = utils.selector('Select link', links, dont_ask_valid=False)
    if '|Referer' in videourl:
        vp.play_from_direct_link(videourl)
    else:
        vp.play_from_link_to_resolve(videourl)

