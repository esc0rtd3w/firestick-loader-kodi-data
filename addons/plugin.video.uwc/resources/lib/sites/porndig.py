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

import urllib
import re
import json

import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'#resolveurl.lib.net.get_ua()

addon = utils.addon

headers = {'User-Agent': USER_AGENT,
           'X-Requested-With': 'XMLHttpRequest',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.8,nl;q=0.6',
           'Connection': 'keep-alive'}

headers['Cookie'] = addon.getSetting('pd_cookie')

pdreferer = 'https://www.porndig.com/videos/'

class UrlOpenerPD(urllib.FancyURLopener):
    version = USER_AGENT


def set_cookie():
    opener = UrlOpenerPD()
    req = opener.open(pdreferer)
    headers['Cookie'] = [x[12:] for x in req.info().headers if x.startswith('Set-Cookie')][0].split(';')[0]
    addon.setSetting('pd_cookie', headers['Cookie'])


@utils.url_dispatcher.register('290', ['name'])
def Main(name):
    set_cookie()
    if 'Amateurs' in name:
        addon.setSetting('pdsection', '1')
    else:
        addon.setSetting('pdsection', '0')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]', 'https://www.porndig.com/videos/', 293, '', '')
    if addon.getSetting("pdsection") == '0':
        utils.addDir('[COLOR hotpink]Studios[/COLOR]', 'https://www.porndig.com/studios/load_more_studios', 294, '', 0)
        utils.addDir('[COLOR hotpink]Pornstars[/COLOR]', 'https://www.porndig.com/pornstars/load_more_pornstars', 295, '', 0)
    List('', 0, 0)


@utils.url_dispatcher.register('293', ['url'])
def Categories(caturl):
    if addon.getSetting("pdsection") == '1':
        caturl = 'https://www.porndig.com/amateur/videos/'
    urldata = utils.getHtml(caturl, pdreferer, headers, data='')
    urldata = re.compile(
        '<select name="filter_1" class="js_loader_category_select js_category_select filter_select_item custom_select">(.*?)</select>',
        re.DOTALL | re.IGNORECASE).findall(urldata)
    reobj = re.compile(r'value="(\d+)"[^>]*?>([^<]+)<', re.DOTALL | re.IGNORECASE).findall(urldata[0])
    for catchannel, catname in reobj:
        utils.addDir(catname, '', 291, '', 0, catchannel, 3)
    xbmcplugin.endOfDirectory(utils.addon_handle)


def VideoListData(page, channel):
    sort = 'date'
    offset = page * 100
    if addon.getSetting("pdsection") == '1':
        catid = 4
    else:
        catid = 1
    values = {'main_category_id': catid,
              'type': 'post',
              'name': 'category_videos',
              'filters[filter_type]': sort,
              'filters[filter_period]': '',
              'offset': offset}
    return urllib.urlencode(values)
    
def CatListData(page, channel):
    sort = 'date'
    offset = page * 100
    if addon.getSetting("pdsection") == '1':
        catid = 4
    else:
        catid = 1    
    values = {'main_category_id': catid,
              'type': 'post',
              'name': 'category_videos',
              'filters[filter_type]': sort,
              'filters[filter_period]': '',
              'offset': offset,
              'quantity': 100,
              'category_id[]': channel}
    return urllib.urlencode(values)

def VideoListStudio(page, channel):
    sort = 'date'
    offset = page * 65
    values = {'main_category_id': '1',
              'type': 'post',
              'name': 'studio_related_videos',
              'filters[filter_type]': sort,
              'filters[filter_period]': '',
              'offset': offset,
              'content_id': channel}
    return urllib.urlencode(values)

def VideoListPornstar(page, channel):
    sort = 'date'
    offset = page * 65
    values = {'main_category_id': '1',
              'type': 'post',
              'name': 'pornstar_related_videos',
              'filters[filter_type]': sort,
              'filters[filter_period]': '',
              'offset': offset,
              'content_id': channel}
    return urllib.urlencode(values)

def StudioListData(page):
    offset = page * 60
    values = {'main_category_id': '1',
              'type': 'studio',
              'name': 'top_studios',
              'filters[filter_type]': 'likes',
              'starting_letter': '',
              'offset': offset}
    return urllib.urlencode(values)

def PornstarListData(page):
    offset = page * 60
    values = {'main_category_id': '1',
              'type': 'pornstar',
              'name': 'top_pornstars',
              'filters[filter_type]': 'likes',
              'country_code': '',
              'starting_letter': '',
              'offset': offset}
    return urllib.urlencode(values)


@utils.url_dispatcher.register('295', ['url'], ['page'])
def Pornstars(url, page=1):
    data = PornstarListData(page)
    urldata = utils.getHtml(url, pdreferer, headers, data=data)
    urldata = ParseJson(urldata)
    i = 0
    match = re.compile(r'pornstar_([\d]+).*?alt="([^"]+)".*?Videos</div>\s+<div class="value">([\d]+)',
                       re.DOTALL | re.IGNORECASE).findall(urldata)
    for ID, studio, videos in match:
        title = studio + " Videos: [COLOR deeppink]" + videos + "[/COLOR]"
        img = "https://static-push.porndig.com/media/default/pornstars/pornstar_" + ID + ".jpg"
        utils.addDir(title, '', 291, img, 0, ID, 2)
        i += 1
    if i >= 60:
        page += 1
        utils.addDir('Page ' + str(page), url, 295, '', page)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('294', ['url'], ['page'])
def Studios(url, page=1):
    data = StudioListData(page)
    urldata = utils.getHtml(url, pdreferer, headers, data=data)
    urldata = ParseJson(urldata)
    i = 0
    match = re.compile(r'studio_([\d]+).*?alt="([^"]+)".*?Videos</div>\s+<div class="value">([\d]+)',
                       re.DOTALL | re.IGNORECASE).findall(urldata)
    for ID, studio, videos in match:
        title = studio + " Videos: [COLOR deeppink]" + videos + "[/COLOR]"
        img = "https://static-push.porndig.com/media/default/studios/studio_" + ID + ".jpg"
        utils.addDir(title, '', 291, img, 0, ID, 1)
        i += 1
    if i >= 60:
        page += 1
        utils.addDir('Page ' + str(page), url, 294, '', page)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('291', ['channel', 'section'], ['page'])
def List(channel, section, page=0):
	if section == 0:
		data = VideoListData(page, channel)
		maxresult = 100
	elif section == 1:
		data = VideoListStudio(page, channel)
		maxresult = 65
	elif section == 2:
		data = VideoListPornstar(page, channel)
		maxresult = 65
	elif section == 3:
		data = CatListData(page, channel)
		maxresult = 100
	try:
		urldata = utils.getHtml("https://www.porndig.com/posts/load_more_posts", pdreferer, headers, data=data)
	except:
		return None
	urldata = ParseJson(urldata)
	
	i = 0
	match = re.compile(
		r'<a.*?href="([^"]+)" title="([^"]+)">.+?img\s+src="(.+?)".+?<span class="pull-left">(.+?)<',
		re.DOTALL | re.IGNORECASE).findall(urldata)
	for url, name,img, duration in match:
		#if len(hd) > 2:
		#	if hd.find('full') > 0:
		#		hd = " [COLOR yellow]FULLHD[/COLOR] "
		#	elif hd.find('4k') > 0:
		#		hd = " [COLOR red]4K[/COLOR] "                
		#	else:
		#		hd = " [COLOR orange]HD[/COLOR] "
		#else:
		hd = " "
		url = "https://www.porndig.com" + url
		name = name + hd + "[COLOR deeppink]" + duration + "[/COLOR]"
		utils.addDownLink(name, url, 292, img, '')
		i += 1
	if i >= maxresult and channel:
		page += 1
		name = 'Page ' + str(page)
		utils.addDir(name, '', 291, page=page, channel=channel, section=section)
	xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('292', ['url', 'name'], ['download'])
def Playvid(url, name, download=None):
	#vp = utils.VideoPlayer(name, download)
	#vp.progress.update(25, "", "Loading video page", "")
	videopage = utils.getHtml(url, pdreferer, headers, data='')
	links = re.compile('<a href="([^"]+)" class="post_download_link clearfix">[^>]+>([^<]+)<',
					re.DOTALL | re.IGNORECASE).findall(videopage)
	videourl = getVideoUrl(links)
	videourl = utils.getVideoLink(videourl, url)
	
	#vp.play_from_direct_link(videourl)
	iconimage = xbmc.getInfoImage("ListItem.Thumb")
	listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
	xbmc.Player().play(videourl, listitem)	

def getVideoUrl(testquality):
    print testquality
    p240 = findx('240p', testquality)
    p360 = findx('360p', testquality)
    p270 = findx('270p', testquality)
    p480 = findx('480p', testquality)
    p540 = findx('540p', testquality)
    p720 = findx('720p', testquality)
    p1080 = findx('1080p', testquality)
    p4k = findx('UHD 4K', testquality)

    if p240 is not None:
        try: testurl = testquality[p240[0]][0]
        except: pass
    if p270 is not None:
        try: testurl = testquality[p270[0]][0]
        except: pass
    if p360 is not None:
        try: testurl = testquality[p360[0]][0]
        except: pass
    if p480 is not None:
        try: testurl = testquality[p480[0]][0]
        except: pass
    if p540 is not None:
        try: testurl = testquality[p540[0]][0]
        except: pass
    if p720 is not None:
        try: testurl = testquality[p720[0]][0]
        except: pass
    if p1080 is not None:
        try: testurl = testquality[p1080[0]][0]
        except: pass
    if p4k is not None:
        try: testurl = testquality[p4k[0]][0]
        except: pass        
    return testurl


def findx(needle, haystack):
    if needle == haystack: return []
    # Strings are iterable, too
    if isinstance(haystack, str) and len(haystack) <= 1:
        return None
    try:
        for i, e in enumerate(haystack):
            r = findx(needle, e)
            if r is not None:
                r.insert(0, i)
                return r
    except TypeError:
        pass
    return None


def ParseJson(urldata):
    urldata = json.loads(urldata)
    return urldata['data']['content']
