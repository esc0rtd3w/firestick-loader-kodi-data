'''
    Ultimate Whitecream
    Copyright (C) 2018 holisticdioxide

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
import xbmc
import xbmcplugin
import xbmcgui
from resources.lib import utils

BASE_URL = 'https://yourporn.sexy'


def make_url(link):
    return link if link.startswith('http') else 'https:' + link if link.startswith('//') else BASE_URL + link


@utils.url_dispatcher.register('650')
def yourporn_main():
    utils.addDir('[COLOR hotpink]Watch live stream[/COLOR]','https://yourporn.sexy/live/', 652, '', '')
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','https://yourporn.sexy/', 653, '', '')
    utils.addDir('[COLOR hotpink]Top networks[/COLOR]','https://yourporn.sexy/', 654, '', '', section='networks')
    utils.addDir('[COLOR hotpink]Top pornstars[/COLOR]','https://yourporn.sexy/', 654, '', '', section='pornstars')
    utils.addDir('[COLOR hotpink]Top rated last week[/COLOR]','https://yourporn.sexy/popular/top-rated.html', 651, '', section='rating')
    utils.addDir('[COLOR hotpink]Top viewed last week[/COLOR]','https://yourporn.sexy/popular/top-viewed.html', 651, '', section='views')
    utils.addDir('[COLOR hotpink]Orgasmic[/COLOR]','https://yourporn.sexy/orgasm/', 651, '', section='orgasmic')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://yourporn.sexy/', 655, '', '')
    yourporn_list('https://yourporn.sexy/blog/all/0.html?fl=all')


@utils.url_dispatcher.register('651', ['url', 'page'], ['section'])
def yourporn_list(url, page=None, section=None):

	popular_mode = section if section else None
	try:
		if popular_mode and page:
			listhtml = utils.postHtml(url, compression=False, form_data={'period': 'week', 'popular_source': 'blogs', 'popular_mode': popular_mode, 'popular_off': page})
			page += 6
			listhtml += utils.postHtml(url, compression=False, form_data={'period': 'week', 'popular_source': 'blogs', 'popular_mode': popular_mode, 'popular_off': page})
		else:
			listhtml = utils.getHtml(url)
	except Exception as e:
		return None
	if popular_mode and page:
		content = listhtml
	else:
		content = listhtml.replace("\'",'"')
	match_big = re.compile('''data-title="([^"]+)".+?<a href="([^"]+)">.+?<img class=.+?;" src="([^"]+)".+?<span class="duration_small".+?" ; title=".+?">(.+?)<''', re.DOTALL | re.IGNORECASE).findall(content)
	for name,video,img, duration in match_big:
		duration = duration.strip()
		if duration == '??':
			continue
		try:
			name=name.split('\n')[0]
			name=name.split('#')[0]
		except:
			pass
		name = utils.cleantext(name) + " [COLOR deeppink]" + duration + "[/COLOR]"
		utils.addDownLink(name, make_url(video), 652, make_url(img), '')
	match_small = re.compile('''<div class='blog_post_small'>.*?<div class='blog_post_small_title'>(.*?)</div>.*?href.*?href='([^']+)'.*? src='([^']+)'[^>]''', re.DOTALL | re.IGNORECASE).findall(content)
	for name, video, img in match_small:
		name = utils.cleantext(re.sub("<.*?>", '', name))
		utils.addDownLink(name, make_url(video), 652, make_url(img), '')
	if popular_mode:
		page = page + 6 if page else 12
		utils.addDir('Next Page', 'https://yourporn.sexy/php/popular_append.php', 651, '', page, section=popular_mode)
	else:
		try:
			next_page = re.compile('''<a href='([^']+)' class='tdn'><div class='next''', re.DOTALL | re.IGNORECASE).search(content).group(1)
			next_page = make_url(next_page)
			utils.addDir('Next Page' , next_page, 651, '')
		except:
			pass
	xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('653', ['url']) 
def yourporn_cat(url):
	listhtml = utils.getHtml(url)
	listhtml=listhtml.replace("\'",'"')
	match = re.compile('<a href="([^"]+)".+?"top_sub_el_key_sc">(.+?)<.+?"top_sub_el_count">(.+?)<', re.DOTALL | re.IGNORECASE).findall(listhtml)
	for catpage, name, count in match: #sorted(match, key=lambda x: x[2]):
		#count = count.strip()
		name = name.strip() + " [COLOR deeppink]" + count + "[/COLOR]"
		utils.addDir(name, make_url(catpage), 651, '', 1)
	xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('654', ['url'], ['section']) 
def yourporn_channels(url, section):
    listhtml = utils.getHtml(url)
    if section == 'networks':
        handle = 'sc'
        categories = re.compile('''<span>Top SubCat Subs</span>(.*?)<div class='now_watching_div'>''', re.DOTALL | re.IGNORECASE).search(listhtml).group(1)
    else:
        handle = 'ps'
        categories = re.compile('''<span>Top Porn Stars Subs</span>(.*?)<span>Top SubCat Subs</span>''', re.DOTALL | re.IGNORECASE).search(listhtml).group(1)
    match = re.compile("<a href='([^']+)'.*?<span class='top_sub_el_key_" + handle + "'>([^<]+)<.*?<span class='top_sub_el_count'>([^<]+)<", re.DOTALL | re.IGNORECASE).findall(categories)
    for catpage, name, count in sorted(match, key=lambda x: x[1]):
        name = name  + " [COLOR deeppink]" + count + "[/COLOR]"
        utils.addDir(name, make_url(catpage), 651, '', 1)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('655', ['url'], ['keyword'])
def yourporn_search(url, keyword=None):
    if not keyword:
        utils.searchDir(url, 655)
    else:
        title = keyword.replace(' ','_')
        url = url + title + '.html'
        yourporn_list(url)

@utils.url_dispatcher.register('652', ['url', 'name'], ['download'])
def yourporn_play(url, name, download=None):
	html = utils.getHtml(url, '')
	videourl = re.compile('''data-vnfo='{".+?":"(.+?)"''', re.DOTALL | re.IGNORECASE).findall(html)[0].replace('\/','/').replace('/cdn/','/cdn2/')
	videourl='https://yourporn.sexy'+videourl
	if download == 1:
		utils.downloadVideo(videourl, name)
	else:
		iconimage = xbmc.getInfoImage("ListItem.Thumb")
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
		listitem.setInfo('video', {'Title': name, 'Genre': 'Porn'})
		xbmc.Player().play(videourl, listitem)		
		
		
		
def yourporn_multiple_videos(html):
    videos = re.compile('''class="pl_vid_el transition".*?data-hash="([^"]+)".*?title="([^"]+)"''', re.DOTALL | re.IGNORECASE).findall(html)
    vids = {}
    for vid_hash, title in videos:
        vids[title] = vid_hash
    sel_vid_hash = utils.selector('Multiple videos found', vids, dont_ask_valid=False, sort_by=lambda x: x)
    if sel_vid_hash:
        vid_url = BASE_URL + "/post/" + sel_vid_hash + '.html'
        return utils.getHtml(vid_url)
    return None
