'''
    Ultimate Whitecream
    Copyright (C) 2018 Whitecream, holisticdioxide

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
from random import randint

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

progress = utils.progress

@utils.url_dispatcher.register('50')    
def PTMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]', 'https://www.porntrex.com/categories/', 53, '', '')
    utils.addDir('[COLOR hotpink]Search[/COLOR]', 'https://www.porntrex.com/search/', 54, '', '')
    PTList('https://www.porntrex.com/latest-updates/1/', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('55')    
def JHMain():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]', 'https://www.javwhores.com/categories/', 53, '', '')
    utils.addDir('[COLOR hotpink]Search[/COLOR]', 'https://www.javwhores.com/search/', 54, '', '')
    PTList('https://www.javwhores.com/latest-updates/1/', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('51', ['url'], ['page'])
def PTList(url, page=1, onelist=None):

	if onelist:
		url = url.replace('/1/', '/' + str(page) + '/')
	try:
		listhtml = utils.getHtml(url, '')
	except:
		return None
#	match = re.compile('class="video-item(.+?)video-preview".*?href="([^"]+)"\s+title="(.+?)".+?<img class="cover lazyload" data-src="(.+?)".+?<span class="quality">(.+?)<.+?<i class="fa fa-clock-o"><.+?>(.+?)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
	match = re.compile('class="video-item(.+?)".*?href="([^"]+)"\s+title="(.+?)".+?<img class=.+?data.+?="(.+?)".+?.+?<span class(.+?)<i class="fa fa-clock-o"><.+?>(.+?)<', re.DOTALL | re.IGNORECASE).findall(listhtml)

	for pryw,videopage, name, img, hd, duration in match:
		name = utils.cleantext(name)
		if 'private' in pryw:
			continue
		if 'HD' in hd:
			hd = " [COLOR orange]HD[/COLOR] "
		elif '2160' in hd:
			hd = " [COLOR orange]4K[/COLOR] "
		elif '1440' in hd:
			hd = " [COLOR orange]HD[/COLOR] "
		elif '1080' in hd:
			hd = " [COLOR orange]HD[/COLOR] "
		elif '720' in hd:
			hd = " [COLOR orange]HD[/COLOR] "
		else:
			hd = " "
		name = name + hd + "[COLOR deeppink]" + duration + "[/COLOR]"
		if img.startswith('//'):
			img = 'https:' + img
		img = re.sub(r"http:", "https:", img)
		imgint = randint(1, 10)
		newimg = str(imgint) + '.jpg'
		img = img.replace('1.jpg', newimg)
		utils.addDownLink(name, videopage, 52, img, '')
	if not onelist:
		if re.search('<li class="next">', listhtml, re.DOTALL | re.IGNORECASE):
			npage = page + 1
			if '/categories/' in url:
				url = url.replace('from=' + str(page), 'from=' + str(npage))
			elif '/search/' in url:
				url = url.replace('from_videos=' + str(page), 'from_videos=' + str(npage)).replace('from_albums=' + str(page), 'from_albums=' + str(npage))
			else:
				url = url.replace('/' + str(page) + '/', '/' + str(npage) + '/')
			utils.addDir('Next Page (' + str(npage) + ')', url, 51, '', npage)
		xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('52', ['url', 'name'], ['download'])
def PTPlayvid(url, name, download=None):
	progress.create('Play video', 'Searching for videofile.')
	progress.update(25, "", "Loading video page", "")
	videopage = utils.getHtml(url, '')
	if 'video_url_text' not in videopage:
		videourl = re.compile("video_url: '([^']+)'", re.DOTALL | re.IGNORECASE).search(videopage).group(1)
	else:
		sources = {}
		srcs = re.compile("video(?:_alt_|_)url(?:[0-9]|): '([^']+)'.*?video(?:_alt_|_)url(?:[0-9]|)_text: '([^']+)'", re.DOTALL | re.IGNORECASE).findall(videopage)
		for src, quality in srcs:
			sources[quality] = src
		videourl = utils.selector('Select quality', sources, dont_ask_valid=True, sort_by=lambda x: int(''.join([y for y in x if y.isdigit()])), reverse=True)
	if not videourl:
		progress.close()
		return
	progress.update(75, "", "Video found", "")
	progress.close()
	if download == 1:
		utils.downloadVideo(videourl, name)
	else:
		iconimage = xbmc.getInfoImage("ListItem.Thumb")
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
		xbmc.Player().play(videourl, listitem)		

@utils.url_dispatcher.register('53', ['url'])
def PTCat(url):
    cathtml = utils.getHtml(url, '')
    cat_block = re.compile('<span class="icon type-video">(.*?)<div class="footer-margin">', re.DOTALL | re.IGNORECASE).search(cathtml).group(1)
    match = re.compile('<a class="item" href="([^"]+)" title="([^"]+)".*?src="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(cat_block)
    for catpage, name, img in sorted(match, key=lambda x: x[1]):
        if img.startswith('//'):
            img = 'https:' + img
        img = re.sub(r"cdn\d?", "www", img)
        catpage = catpage + '?mode=async&function=get_block&block_id=list_videos_common_videos_list&sort_by=post_date&from=1'
        utils.addDir(name, catpage, 51, img, 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('54', ['url'], ['keyword'])  
def PTSearch(url, keyword=None):
	searchUrl = url
	if not keyword:
		utils.searchDir(url, 54)
	else:
		searchUrl += keyword.replace(' ', '+')+'/'
		PTList(searchUrl, 1)
