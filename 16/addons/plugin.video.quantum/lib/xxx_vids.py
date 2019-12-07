# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmcaddon, xbmc, re, sys, os, process
import clean_name
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.quantum')
ICON = ADDON_PATH + '/icon.png'
FANART = 'http://www.artsfon.com/pic/201605/1920x1080/artsfon.com-84741.jpg'
Dialog = xbmcgui.Dialog()
List = []
pornhub = 'http://pornhub.com'
letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def Porn_Menu():
	process.Menu('X Videos','',700,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
	process.Menu('Porn Hub','',708,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png',FANART,'','')
	process.Menu('X Hamster','',714,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
	process.Menu('Chaturbate','',720,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
	process.Menu('You Porn','',723,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Red Tube','',730,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Tube 8','',738,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Thumbzilla','',745,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('XTube','',753,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Eporner','',760,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('YouJizz','',771,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('Spank Wire','',772,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')
	process.Menu('4k','',758,'https://pbs.twimg.com/profile_images/700315084980035588/fZZO6Pf-.jpg',FANART,'','')
	process.Menu('VR','http://www.xvideos.com/?k=vr',701,'https://pbs.twimg.com/profile_images/741907565689217024/DByQczLO.jpg',FANART,'','')

	
##############################Spank Wire#############################

def spank_wire():
	process.Menu('Categories','http://www.spankwire.com/categories/Straight',773,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')
	process.Menu('Tags','http://www.spankwire.com/tags/Straight',774,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')
	process.Menu('Top Rated','http://www.spankwire.com/home1/Straight/Week/Rating',775,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')
	process.Menu('Most Viewed','http://www.spankwire.com/home1/Straight/Week/Views',775,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')
	process.Menu('Talked About','http://www.spankwire.com/home1/Straight/Week/Comments',775,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')
	process.Menu('Search','',776,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')

def spank_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="category-thumb">.+?<a href="(.+?)".+?<img src="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'http://spankwire.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,775,img,FANART,'','')

def spank_tags(url):
	for letter in letters:
		process.Menu(letter,url,778,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')
		
def spank_tags_letter(letter,url):
	html = process.OPEN_URL(url)
	match = re.compile('<span class="tag-value">(.+?)</span>').findall(html)
	for item in match:
		if item[0].lower() == letter.lower():
			url = 'http://www.spankwire.com/search/straight/tag/'+item
			process.Menu(item,url,775,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')

def spank_videos(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="thumb-info-wrapper">.+?<a href="(.+?)".+?data-original="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'http://www.spankwire.com'+url
		process.PLAY(name,url,777,img,FANART,'','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		if not 'http://www.spankwire.com' in item:
			item = 'http://www.spankwire.com'+item
		process.Menu('Next Page',item,775,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')

def spank_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	match = re.compile("playerData.cdnPath(.+?) .+?= '(.+?)';").findall(html)
	for quality,playlink in match:
		sources.insert(0,{'quality': quality+'p', 'playlink': playlink})
		if len(sources) == len(match):
			choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
			if choice != -1:
				playlink = sources[choice]['playlink']
				isFolder=False
				xbmc.Player().play(playlink)
		

def spank_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.spankwire.com/search/straight/keyword/teen'+Search_name.replace(' ','%2B')
	spank_videos(url)

	
##############################youjizz#################################
	
def youjizz():
	process.Menu('Popular','https://www.youjizz.com/most-popular/1.html',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('Test','https://www.youjizz.com/pornstars/Aaliyah-Ca-Pelle-1.html',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('Newest','https://www.youjizz.com/newest-clips/1.html',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('Top Rated','https://www.youjizz.com/top-rated-week/1.html',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('Random','https://www.youjizz.com/random.php',765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('Tags','https://www.youjizz.com/tags/',766,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('Pornstars','https://www.youjizz.com/pornstars',767,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('Search','',768,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')

def youjizz_videos(url):
	next_list = []
	html = process.OPEN_URL(url)
	match = re.compile('<a class="frame".+?href="(.+?)".+?<img.+?data-original="(.+?)".+?<a href=.+?>(.+?)</a>.+?"time">(.+?)</span>',re.DOTALL).findall(html)
	for url,img,name,length in match:
		url = 'http://youjizz.com'+url
		img = 'http:'+img
		name = length+' - '+name
		name = clean_name.clean_name(name)
		process.PLAY(name,url,769,img,FANART,'','')
	next = re.compile("a href='([^']*)'>Next.+?</a>").findall(html)
	for item in next:
		if 'Next' not in next_list:
			process.Menu('Next Page','http://youjizz.com'+item,765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
			next_list.append('Next')
	
def youjizz_playlink(url):
	sources=[]
	xbmc.log(url,xbmc.LOGNOTICE)
	html = process.OPEN_URL(url)
	match = re.compile('"quality":"(.+?)","filename":"(.+?)"').findall(html)
	for quality,playlink in match:
		playlink = 'http:'+playlink.replace('\\','')
		if 'm3u8' in playlink:
			quality = 'm3u8 | '+quality
		elif 'mp4' in playlink:
			quality = 'mp4 | '+quality 
		sources.insert(0,{'quality': quality+'p', 'playlink': playlink})
		if len(sources) == len(match):
			choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
			if choice != -1:
				playlink = sources[choice]['playlink']
				isFolder=False
				xbmc.Player().play(playlink)

		
def youjizz_tags(url):
	for letter in letters:
		process.Menu(letter,url,770,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')

def youjizz_tags_letters(letter,url):
	html = process.OPEN_URL(url)
	match = re.compile('<li class="tag_col_0"><a href="(.+?)"><b>(.+?)</b>').findall(html)
	for url,name in match:
		if letter.lower() == name[0].lower():
			process.Menu(name,url,765,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	
def youjizz_pornstars(url):
	for letter in letters:
		url = 'https://www.youjizz.com/pornstars/name/'+letter
		process.Menu(letter,url,770,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	
	
def youjizz_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.youjizz.com/search/'+Search_name.replace(' ','-')+'-1.html'
	youjizz_videos(url)
	
	
###############################Eporner##########################################

def eporner():
	process.Menu('4k','https://www.eporner.com/category/4k-porn/',761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('1080p','https://www.eporner.com/category/hd-1080p/',761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('60fps','https://www.eporner.com/category/60fps/',761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('HD','https://www.eporner.com/category/hd-sex/',761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('Popular','https://www.eporner.com/popular/',761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('Top Rated','https://www.eporner.com/top-rated/',761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('Amateur','https://www.eporner.com/category/amateur/',761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('Solo Girls','https://www.eporner.com/category/amateur/',761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('Pornstars','https://www.eporner.com/pornstars/',762,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('Categories','https://www.eporner.com/categories/',763,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('Search','',764,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')

def eporner_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.eporner.com/search/'+Search_name.replace(' ','-')
	eporner_video(url)
	
def eporner_pornstar(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="mbprofile">.+?<a href="(.+?)" title="(.+?)">.+?<img src="(.+?)"',re.DOTALL).findall(html)
	for url,name,img in match:
		url = 'http://eporner.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,761,img,FANART,'','')
	next = re.compile("<a href='([^']*)' title='Next page'>").findall(html)
	for item in next:
		url = 'http://eporner.com'+item
		url = clean_name.clean_name(url)
		process.Menu('Next Page',url,762,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	
	
def eporner_cats(url):
	html = process.OPEN_URL(url)
	block = re.compile('<div class="listcat responsivecategories">(.+?)<table id="categories-list-left">',re.DOTALL).findall(html)
	for item in block:
		match = re.compile('<a href="(.+?)".+?title="(.+?)">.+?<img src="(.+?)"').findall(str(item))
		for url,name,img in match:
			url = 'http://eporner.com'+url
			name = clean_name.clean_name(name)
			if 'img src' in name:
				pass
			else:
				process.Menu(name.replace('Porn Videos',''),url,761,img,FANART,'','')
	
def eporner_video(url):
	html = process.OPEN_URL(url)
	match = re.compile('onmouseenter="show_video_prev.+?<span>(.+?)</span>.+?<a href="(.+?)".+?title="(.+?)".+?<img id=.+?src="(.+?)".+?"mbtim">(.+?)</div>',re.DOTALL).findall(html)
	for max_qual,url,name,img,length in match:
		url = 'http://www.eporner.com'+url
		name = clean_name.clean_name(name)
		name = max_qual.replace('4K','[COLOR darkgoldenrod][B]4K[/B][/COLOR]')+'-[COLORred]'+length+'[/COLOR]-'+name
		process.PLAY(name,url,759,img,FANART,'','')
	next = re.compile('<a href="([^"]*)" title="Next page">').findall(html)
	for item in next:
		url = 'http://eporner.com'+item
		url = clean_name.clean_name(url)
		process.Menu('Next Page',url,761,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')

def eporner_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	match = re.compile('href="/dload/(.+?)">.+?\((.+?)p,').findall(html)
	for playlink,quality in match:
		playlink = 'http://www.eporner.com/dload/'+playlink.replace('\\','')
		sources.insert(0,{'quality': quality+'p', 'playlink': playlink})
		if len(sources) == len(match):
			choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
			if choice != -1:
				playlink = sources[choice]['playlink']
				isFolder=False
				xbmc.Player().play(playlink)

################################4k##############################################

def fourK():
	html = process.OPEN_URL('https://www.eporner.com/category/4k-porn/')
	match = re.compile('<span>4K \(2160p\)</span></div> <a href="(.+?)" title="(.+?)".+?src="(.+?)"').findall(html)
	for url,name,img in match:
		url = 'http://eporner.com'+url
		name = clean_name.clean_name(name)
		process.PLAY(name,url,759,img,FANART,'','')

	
###############################X Tube###########################################

def xtube():
	process.Menu('Most Recent','http://www.xtube.com/video',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Most Viewed','http://www.xtube.com/video/mvi',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Top Rated','http://www.xtube.com/video/trt',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Most Discussed','http://www.xtube.com/video/mdi',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Top Length','http://www.xtube.com/video/tln',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Top Favourites','http://www.xtube.com/video/tfv',754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Categories','http://www.xtube.com/categories',755,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Search','',756,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')

def xtube_videos(url):
	next_list = []
	html = process.OPEN_URL(url)
	match = re.compile('<a href="/video-watch(.+?)" title="(.+?)".+?<img src="(.+?)".+?<span class="duration">(.+?)</span>',re.DOTALL).findall(html)
	for url,name,img,length in match:
		name = length + ' - ' + name
		url = 'http://xtube.com/video-watch'+url
		name = clean_name.clean_name(name)
		process.PLAY(name,url,757,img,FANART,'','')
	next = re.compile('<a href="([^"]*)" title="next">').findall(html)
	for item in next:
		if 'Next' not in next_list:
			url = 'http://xtube.com'+item
			process.Menu('Next Page',url,754,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
			next_list.append('Next')
		

	
def xtube_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('data-sort="{alphabetical:.+?<a href="(.+?)".+?<img src=".+?" data-lazySrc="(.+?)" alt="(.+?)">',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'http://www.xtube.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,754,img,FANART,'','')
	match2 = re.compile('data-sort="{alphabetical:.+?<a href="(.+?)".+?<img src="(.+?)" alt="(.+?)">',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'http://www.xtube.com'+url
		name = clean_name.clean_name(name)
		process.Menu(name,url,754,img,FANART,'','')
		
def xtube_search(url):
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.xtube.com/search/video?keywords='+Search_name.replace(' ','+')
	xtube_videos(url)
	
	
	
def xtube_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	block = re.compile('"sources":{(.+?)}',re.DOTALL).findall(html)
	for item in block:
		match = re.compile('"(.+?)":"(.+?)"').findall(str(item))
		for quality,playlink in match:
			playlink = playlink.replace('\\','')
			sources.append({'quality': quality, 'playlink': playlink})
			if len(sources) == len(match):
				choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
				if choice != -1:
					playlink = sources[choice]['playlink']
					isFolder=False
					xbmc.Player().play(playlink)
	
################################Thumb Zilla#####################################

def thumbzilla():
	process.Menu('Hottest','https://www.thumbzilla.com/',746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('Newest','https://www.thumbzilla.com/newest',746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('Trending','https://www.thumbzilla.com/trending',746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('Top','https://www.thumbzilla.com/top',746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('Popular','https://www.thumbzilla.com/popular',746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('HD','https://www.thumbzilla.com/hd',746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('Homemade','https://www.thumbzilla.com/homemade',746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('Tags','https://www.thumbzilla.com/tags',747,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('Pornstars','https://www.thumbzilla.com/pornstars',748,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('Categories','https://www.thumbzilla.com/',749,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('Search','',750,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')

def thumbzilla_videos(url):
	html = process.OPEN_URL(url)
	match = re.compile('<a class="js-thumb" href="(.+?)".+?src="(.+?)".+?<span class="title">(.+?)</span>.+?<span class="duration">(.+?)</span>(.+?)</span>',re.DOTALL).findall(html)
	for url,img,name,length,hd_check in match:
		length+' - '+name
		url = 'http://thumbzilla.com'+url
		if 'hd' in hd_check:
			name = clean_name.clean_name(name)
			name = '[COLORred]HD [/COLOR]'+name
		process.PLAY(name,url,752,img,FANART,'','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		item = clean_name.clean_name(item)
		process.Menu('Next Page',item,746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
		
def thumbzilla_tags(url):
	for letter in letters:
		process.Menu(letter,url,751,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
		
def thumbzilla_tags_letters(letter,url):
	html = process.OPEN_URL(url)
	match = re.compile('<a href="/tags/(.+?)">').findall(html)
	for url in match:
		name = url[0].upper()+url[1:].replace('-',' ')
		if letter.lower() == name[0].lower():
			process.Menu(name,'http://thumbzilla.com/tags/'+url,746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	
def thumbzilla_pornstars(url):
	html = process.OPEN_URL(url)
	match = re.compile(' <a href="/pornstars/(.+?)".+?<img src="(.+?)"',re.DOTALL).findall(html)
	for url,img in match:
		name = url[0].upper()+url[1:].replace('-',' ')
		process.Menu(name,'http://thumbzilla.com/pornstars/'+url,746,img,FANART,'','')
	next = re.compile('<li class="page_next"><a href="(.+?)"').findall(html)
	for item in next:
		url = 'http://thumbzilla.com'+item
		process.Menu('Next Page',url,748,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
		
def thumbzilla_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="checkHomepage">.+?<a href="/categories/(.+?)"',re.DOTALL).findall(html)
	for url in match:
		name = url[0].upper()+url[1:].replace('-',' ')
		process.Menu(name,'http://thumbzilla.com/categories/'+url,746,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	
def thumbzilla_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.thumbzilla.com/video/search?q='+Search_name.replace(' ','+')
	thumbzilla_videos(url)
	
def thumbzilla_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	match = re.compile('"quality_(.+?)":(.+?),').findall(html)
	for quality,playlink in match:
		playlink = playlink.replace('\\','').replace('"','')
		sources.append({'quality': quality, 'playlink': playlink})
		if len(sources) == len(match):
			choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
			if choice != -1:
				playlink = sources[choice]['playlink']
				isFolder=False
				xbmc.Player().play(playlink)
				
################################Tube 8##########################################

def tube8():
	process.Menu('Longest','http://www.tube8.com/longest.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Magic','http://www.tube8.com/magic.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Most Discussed','http://www.tube8.com/mostdiscussed.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Most Favourited','http://www.tube8.com/mostfavorited.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Most Viewed','http://www.tube8.com/mostviewed.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Most Voted','http://www.tube8.com/mostvoted.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Newest','http://www.tube8.com/newest.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Top','http://www.tube8.com/top.html',739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Categories','http://www.tube8.com/categories.html',741,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Tags','http://www.tube8.com/tags.html',742,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Search','',743,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')

def tube8_videos(url):
	html = process.OPEN_URL(url)
	match = re.compile('data-value=.+?src="(.+?)".+?alt="(.+?)".+?"video_duration">(.+?)</div>.+?<a href="(.+?)"',re.DOTALL).findall(html)
	for img,name,length,url in match:
		name = clean_name.clean_name(name)
		length = clean_name.clean_name(length)
		process.PLAY('[COLORred]'+length+'[/COLOR] : '+name,url,740,img,FANART,'','')
	next = re.compile('<link rel="next" href="(.+?)">').findall(html)
	for item in next:
		process.Menu('Next Page',item,739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
		
def tube8_cats(url):
	html = process.OPEN_URL(url)
	block = re.compile('<ul class="categories-menu categoriesFooterFontSize">(.+?)</ul>',re.DOTALL).findall(html)
	for item in block:
		match = re.compile('<a href="(.+?)">(.+?)</a>').findall(str(item))
		for url,name in match:
			process.Menu(name,url,739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')

def tube8_tags(url):
	for letter in letters:
		process.Menu(letter,url,744,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
		
def tube8_letters(letter,url):
	html = process.OPEN_URL(url)
	match = re.compile('<li class="tag" title="(.+?)">.+?<a class="tag" href="(.+?)">',re.DOTALL).findall(html)
	for name,url in match:
		if letter.lower() == name[0].lower():
			process.Menu(name,url,739,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	
def tube8_search():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.tube8.com/searches.html?q='+Search_name.replace(' ','+')
	tube8_videos(url)
	
def tube8_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	match = re.compile('"quality_(.+?)":(.+?),').findall(html)
	for quality,playlink in match:
		playlink = playlink.replace('\\','').replace('"','')
		if playlink == 'false':
			pass
		else:
			sources.append({'quality': quality, 'playlink': playlink})
	choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
	if choice != -1:
		playlink = sources[choice]['playlink']
		xbmc.Player().play(playlink)

	
#################################Red Tube########################################

def redtube():
	process.Menu('Trending Now','http://www.redtube.com/hot',731,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Channels','http://www.redtube.com/channel',733,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Pornstars','http://www.redtube.com/pornstar',734,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Collections','http://www.redtube.com/straight/playlists',735,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Recommended','http://www.redtube.com/recommended',731,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Top Rated','http://www.redtube.com/top',731,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Most Viewed','http://www.redtube.com/mostviewed',731,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Categories','http://www.redtube.com/categories',736,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Most Favourited','http://www.redtube.com/mostfavored',731,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Newest','http://www.redtube.com/',731,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Longest','http://www.redtube.com/longest',731,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Search','',737,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')

def redtube_channels(url):
	html = process.OPEN_URL(url)
	match = re.compile('class="channels-list-img">.+?<img.+?src="(.+?)" alt="(.+?)">',re.DOTALL).findall(html)
	for img,name in match:
		img = 'http:'+img
		url = 'http://www.redtube.com/'+name
		name = clean_name.clean_name(name)
		process.Menu(name,url,731,img,FANART,'','')
	
def redtube_pornstars(url):
	html = process.OPEN_URL(url)
	match = re.compile('<a href="/pornstar/(.+?)".+?title="(.+?)".+?src="(.+?)"',re.DOTALL).findall(html)
	for url,name,img in match:
		url = 'http://redtube.com/pornstar/'+url
		name = clean_name.clean_name(name)
		img = 'http:' + img
		process.Menu(name,url,731,img,FANART,'','')
	
def redtube_collections(url):
	html = process.OPEN_URL(url)
	match = re.compile('<a  href="/playlist/(.+?)".+?<img src="(.+?)".+?<span class="playlist-title">.+?</a>(.+?)</a>',re.DOTALL).findall(html)
	for url,img,name in match:
		url = 'http://redtube.com/playlist/'+url
		img = 'http:'+img
		name = clean_name.clean_name(name)
		process.Menu(name,url,731,img,FANART,'','')
	
def redtube_cats(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="video">.+?<a href="(.+?)" title="(.+?)">.+?data-src="(.+?)"',re.DOTALL).findall(html)
	for url,name,img in match:
		url = 'http://redtube.com'+url
		name = clean_name.clean_name(name)
		img = 'http://'+img
		process.Menu(name,url,731,img,FANART,'','')
	
def redtube_search(url):
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.redtube.com/?search='+Search_name.replace(' ','+')
	redtube_video(url)
	
def redtube_video(url):
	html = process.OPEN_URL(url)
	match = re.compile('<img title="(.+?)".+?id="(.+?)".+?data-src="(.+?)"',re.DOTALL).findall(html)
	for name,url,img in match:
		name = clean_name.clean_name(name)
		url = 'http://www.redtube.com/'+url
		if not img.startswith('https:'):
			img = 'https:'+img
			xbmc.log(url,xbmc.LOGNOTICE)
		process.PLAY(name,url,732,img,FANART,'','')
	next = re.compile('<link rel="next" href="(.+?)">').findall(html)
	for item in next:
		process.Menu('Next Page',item,731,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	
def redtube_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	block = re.compile('"defaultQuality"(.+?)}').findall(html)
	for b in block:
		try:
			qual = re.findall('"quality":"(.+?)"',str(b))[0]
			playlink = re.findall('"videoUrl":"(.+?)"',str(b))[0]
			qual = qual.replace('\)','p\)')
			playlink = playlink.replace('\\','')
			sources.append({'quality': qual, 'url': playlink})
		except:
			pass
	choice = Dialog.select('Select Playlink',["(" + link["quality"] + ")" for link in sources])
	if choice != -1:
		url = sources[choice]['url']
		isFolder=False
		xbmc.Player().play(url)
		
################################You Porn########################################

def YouPorn():
	process.Menu('New Videos','http://www.youporn.com/',724,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Recommended','http://www.youporn.com/recommended/',725,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Top Rated','http://www.youporn.com/top_rated/',725,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Most Viewed','http://www.youporn.com/most_viewed/',725,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Most Favourited','http://www.youporn.com/most_favorited/',725,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Most Discussed','http://www.youporn.com/most_discussed/',725,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Collections','http://www.youporn.com/collections/',726,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Random Video','http://www.youporn.com/random/video/',725,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Categories','http://www.youporn.com/categories/',727,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Search','',729,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')

def search_youporn(url):
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'https://www.youporn.com/search/?query='+Search_name.replace(' ','+')
	youporn_video(url)
	
	
def youporn_collections(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="collection-box-title">.+?<a href="(.+?)">(.+?)</a>.+?<img src=\'(.+?)\'',re.DOTALL).findall(html)
	for url,name,img in match:
		process.Menu(name,'https://youporn.com'+url,725,img,FANART,'','')

def youporn_categories(url):	
	html = process.OPEN_URL(url)
	block = re.compile("<div class='row most_popular' id='categoryList'>(.+?)<div class='row' id=\"countryFlags\">",re.DOTALL).findall(html)
	for item in block:
		match = re.compile('<a href="(.+?)".+?<img src="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(str(item))
		for url,img,name in match:
			process.Menu(name,'https://youporn.com'+url,725,img,FANART,'','')
	
def youporn_video(url):
	html = process.OPEN_URL(url)
	match = re.compile("<div class='video-box.+?<a href=\"(.+?)\".+?<img src=\"(.+?)\".+?alt='(.+?)'",re.DOTALL).findall(html)
	for url,img,name in match:
		name = clean_name.clean_name(name)
		url = 'https://www.youporn.com'+url
		process.PLAY(name,url,728,img,FANART,'','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		process.Menu('Next Page',item,725,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')

def youporn_new_video(url):
	html = process.OPEN_URL(url)
	block = re.compile('"day_by_day_section">(.+?)<div class="title-bar sixteen-column">',re.DOTALL).findall(html)
	for item in block:
		match = re.compile("<div class='video-box four-column'.+?<a href=\"(.+?)\".+?<img src=\"(.+?)\".+?alt='(.+?)'",re.DOTALL).findall(str(item))
		for url,img,name in match:
			name = clean_name.clean_name(name)
			url = 'https://www.youporn.com'+url
			process.PLAY(name,url,728,img,FANART,'','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		process.Menu('Next Page',item,725,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')

def youporn_playlink(url):
	sources = []
	url = url.replace('watch','embed')
	html = process.OPEN_URL(url)
	block = re.compile('"defaultQuality"(.+?)}').findall(html)
	for b in block:
		try:
			qual = re.findall('"quality":"(.+?)"',str(b))[0]
			playlink = re.findall('"videoUrl":"(.+?)"',str(b))[0]
			qual = qual.replace('\)','p\)')
			playlink = playlink.replace('\\','')
			sources.append({'quality': qual, 'url': playlink})
		except:
			pass
	choice = Dialog.select('Select Playlink',["(" + link["quality"] + ")" for link in sources])
	if choice != -1:
		url = sources[choice]['url']
		isFolder=False
		xbmc.Player().play(url)
		
#################################Chaturbate######################################

def chaturbate():
	process.Menu('Featured','https://chaturbate.com/',721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
	process.Menu('Female','https://chaturbate.com/female-cams/',721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
	process.Menu('Male','https://chaturbate.com/male-cams/',721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
	process.Menu('Couple','https://chaturbate.com/couple-cams/',721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
	process.Menu('Tags','https://chaturbate.com/tags/',717,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')

def chaturbate_tags(url):
	html = process.OPEN_URL(url)
	match = re.compile('<span class="tag">.+?<a href="(.+?)" title="(.+?)">.+?</a>.+?</span>',re.DOTALL).findall(html)
	for url, name in match:
		url2 = 'http://chaturbate.com' + url
		process.Menu(name,url2,721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
	
def chaturbate_videos(url):
	html = process.OPEN_URL(url)
	block = re.compile('<ul class="list">(.+?)<div class="c-1 featured_blog_posts">',re.DOTALL).findall(html)
	for item in block:
		match = re.compile('<li>.+?<a href="(.+?)">.+?<img src="(.+?)"',re.DOTALL).findall(str(item))
		for url,img in match:
			url2 = 'http://chaturbate.com' + url
			process.PLAY(url.replace('/',''),url2,722,img,FANART,'','')
	next = re.compile('<li><a href="([^"]*)" class="next endless_page_link">next</a></li>').findall(html)
	for thing in next:
		process.Menu('Next Page','http://chaturbate.com'+thing,721,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
			

def chaturbate_playlink(url):
	sources = []
	html = process.OPEN_URL(url)
	fast = re.compile("Hls.isSupported.+?source src='(.+?)'",re.DOTALL).findall(html)
	for item in fast:
		xbmc.Player().play(item)
			
		
#########################################X HAMSTER#############################################################

def XHamster():
	process.Menu('Categories','https://xhamster.com/channels.php',715,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
	process.Menu('Top Rated','https://xhamster.com/rankings/weekly-top-videos.html',716,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
	process.Menu('HD','https://xhamster.com/channels/new-hd_videos-1.html',716,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
	
def hamster_cats(url):
	for letter in letters:
		process.Menu(letter,url,718,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
		
def hamster_cats_split(letter,url):
	html = process.OPEN_URL(url)
	if letter == 'Y':
		block = re.compile('<h2 class="letter-sign">(.+?)</h2>(.+?)<div id="footer">',re.DOTALL).findall(html)
	else:
		block = re.compile('<h2 class="letter-sign">(.+?)</h2>(.+?)<div class="letter-block"',re.DOTALL).findall(html)
	for check,rest in block:
		if check == letter:
			match = re.compile('<a href="(.+?)"><span >(.+?)</span>').findall(str(rest))
			for url,name in match:
				if '<div' in name:
					name = re.compile('(.+?)<div').findall(str(name))
					for item in name:
						name = item
				process.Menu(name,url,716,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
			
def get_hamster_vid(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="video"><a href="(.+?)".+?<img src=\'(.+?)\'.+?alt="(.+?)"/>.+?><b>(.+?)</b>(.+?)<div class="fr">(.+?)</div><div class="views-value">(.+?)</div></div></div>').findall(html)
	for url,img,name,duration,hd_check,rating,views in match:
		name = clean_name.clean_name(name)
		name = duration+' - '+name
		if 'hSpriteHD' in hd_check:
			name = '[COLORred]HD [/COLOR]'+name
		process.PLAY(name,url,719,img,img,'Views : '+views+'\nRating : '+rating,'')
	next = re.compile('<link rel="next" href="(.+?)">').findall(html)
	for item in next:
		item = clean_name.clean_name(item)
		process.Menu('Next Page',item ,716,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
		
def get_hamster_playlinks(url):
	sources = []
	html = process.OPEN_URL(url)
	block = re.compile('sources:(.+?)},').findall(html)
	for item in block:
		match = re.compile('"(.+?)":"(.+?)"').findall(str(item))
		for quality,playlink in match:
			playlink = playlink.replace('\\','')
			sources.append({'quality': quality, 'playlink': playlink})
			if len(sources)==len(match):
				if len(match)>1:
					choice = Dialog.select('Select Playlink',["(" + link["quality"] + ")" for link in sources])
					if choice != -1:
						playlink = sources[choice]['playlink']
						isFolder=False
						xbmc.Player().play(playlink)
				else:
					isFolder=False
					xbmc.Player().play(playlink)

#########################################PORN HUB###############################################################	
	
def Porn_Hub():
	process.Menu('Videos','http://www.pornhub.com/video',709,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png',FANART,'','')
	process.Menu('Categories','http://www.pornhub.com/categories',710,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png',FANART,'','')
	process.Menu('Pornstars','http://www.pornhub.com/pornstars',712,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png',FANART,'','')
	process.Menu('Search','',713,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png',FANART,'','')
	
def search_pornhub():
	Dialog = xbmcgui.Dialog()
	Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
	Search_name = Search_title.lower()
	url = 'http://www.pornhub.com/video/search?search='+Search_name.replace(' ','+')
	get_video_item(url)
	
def get_pornstar(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="subscribe-to-pornstar-icon display-none">.+?data-mxptext="(.+?)" href="(.+?)">.+?<img src="(.+?)"',re.DOTALL).findall(html)
	for name,url,img in match:
		name = clean_name.clean_name(name)
		url = pornhub + url
		process.Menu(name,url,709,img,FANART,'','')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		item = clean_name.clean_name(item)
		process.Menu('Next Page',item,712,'','','','')
		
def get_video_item(url):
	html = process.OPEN_URL(url)
	match = re.compile('<div class="preloadLine">.+?<a href="(.+?)" title="(.+?)".+?<var class="duration">(.+?)</var>(.+?)</div>.+?data-mediumthumb="(.+?)".+?<span class="views"><var>(.+?)</var> views</span>.+?<div class="value">(.+?)</div>.+?<var class="added">(.+?)</var>',re.DOTALL).findall(html)
	for url,name,duration,hd_check,image,views,rating,uploaded in match:
		fin_url = pornhub+url
		name = duration+' - '+name
		if 'hd-thumbnail' in hd_check:
			name = '[COLORred]HD [/COLOR]'+name
		name = clean_name.clean_name(name)
		process.PLAY(name,fin_url,711,image,FANART,'Views : '+views+'\nRating : '+rating+'\nUploaded : '+uploaded,'')
	next = re.compile('<link rel="next" href="(.+?)" />').findall(html)
	for item in next:
		item = clean_name.clean_name(item)
		process.Menu('Next Page',item,709,'','','','')

			
def get_cat_item(url):
	html = process.OPEN_URL(url)
	match = re.compile('<li class=" ">.+?<a href="(.+?)".+?alt="(.+?)">.+?<img class="js-menuSwap" data-image="(.+?)"',re.DOTALL).findall(html)
	for url,name,image in match:
		url = pornhub + url
		process.Menu(name,url,709,image,FANART,'','')
	match = re.compile('<li class="big video">.+?<a href="(.+?)".+?alt="(.+?)">.+?<img class="js-menuSwap" data-image="(.+?)"',re.DOTALL).findall(html)
	for url,name,image in match:
		url = pornhub + url
		process.Menu(name.encode('utf-8', 'ignore'),url,709,image,image,'','')
	
def get_pornhub_playlinks(url):
	sources = []
	xbmc.log('url:'+url,xbmc.LOGNOTICE)
	html = process.OPEN_URL(url)
	block = re.compile('"defaultQuality"(.+?)}').findall(html)
	for b in block:
		try:
			qual = re.findall('"quality":"(.+?)"',str(b))[0]
			playlink = re.findall('"videoUrl":"(.+?)"',str(b))[0]
			qual = qual.replace('\)','p\)')
			playlink = playlink.replace('\\','')
			sources.append({'quality': qual, 'url': playlink})
		except:
			pass
	choice = Dialog.select('Select Playlink',["(" + link["quality"] + ")" for link in sources])
	if choice != -1:
		url = sources[choice]['url']
		isFolder=False
		xbmc.Player().play(url)


	
##################################################XVIDEOS############################################################################	
	
def X_vid_Menu():
    process.Menu('Best Videos','http://www.xvideos.com/best',701,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
    process.Menu('Genres','http://www.xvideos.com',702,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
    process.Menu('Recently Uploaded','http://xvideos.com',701,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
    process.Menu('Tags','http://www.xvideos.com/tags',705,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
    process.Menu('Search','',704,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

	
def Xtags(url):
    HTML = process.OPEN_URL(url)
    match = re.compile('<li><a href="(.+?)"><b>(.+?)</b><span class="navbadge default"(.+?)</span>').findall(HTML)
    for url,name,no in match:
        if '<span' in name:
            pass
        else:
            process.Menu(name + ' - No of Videos : ' + (no).replace('>',''),'http://www.xvideos.com'+url,701,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
    next_button = re.compile('<li><a class=".+?".+?href="(.+?)">Next</a></li>').findall(HTML)
    for url in next_button:
        if 'Next' not in List:
            process.Menu('Next Page','http://www.xvideos.com'+url,705,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
            List.append('Next')
    
def XPornstars(url):
    HTML = process.OPEN_URL(url)
    match = re.compile(':"([^"]*)".+?;</script></a></div></div><p class="profile-name"><a href="([^"]*)">(.+?)</a></p><p class="profile-counts">\n(.+?)\n',re.DOTALL).findall(HTML)
    for img,url,name,count in match:
        process.Menu(name+'--'+count,'http://www.xvideos.com'+url+'#_tabVideos,videos-best',701,(img).replace('http:\/\/','http://'),FANART,'','')        
    next_button = re.compile('href="([^"]*)">Next</a></li>').findall(HTML)
    for url in next_button:
        if 'Next' not in List:
            process.Menu('Next Page','http://www.xvideos.com'+url,705,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
            List.append('Next')
		
	  
def XNew_Videos(url):
    HTML = process.OPEN_URL(url)
    match = re.compile('<div class="thumb-inside">.+?<img src="(.+?)".+?<a href="(.+?)" title="(.+?)">.+?<strong>(.+?)</strong> - (.+?)%').findall(HTML)
    for img,url,name,length,rating in match:
        process.PLAY((name).replace('&nbsp;','-').replace('---',' - ').replace('&#039;','\'').replace('&amp;','&').replace('&quot;','"').replace('  ','') + ' - Porn Quality : ' + rating.replace('<span class="mobile-hide">','') + '% - ' + length,'http://www.xvideos.com'+url,706,img,FANART,rating.replace('<span class="mobile-hide">','') + '% - ' + length,'')	
    next_button2 = re.compile('<li><a href="([^"]*)" class="no-page">Next</a></li></ul></div>').findall(HTML)
    for url in next_button2:
        if 'Next' not in List:
            url = clean_name.clean_name(url)
            process.Menu('Next Page','http://www.xvideos.com'+url,701,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
            List.append('Next')
    
def XGenres(url):
    HTML = process.OPEN_URL(url)
    block = re.compile('</div>.+?<div class="main-categories">(.+?)</script>',re.DOTALL).findall(HTML)
    match = re.compile('"url":"(.+?)","label":"(.+?)"').findall(str(block))
    for url,name in match:
    	if 'span' in name :
        	name = 'porn'
        else:
        	process.Menu(name,'http://www.xvideos.com'+url.replace('\\',''),701,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
    next_button = re.compile('<li><a class=".+?".+?href="(.+?)">Next</a></li>').findall(HTML)
    for url in next_button:
        if 'Next' not in List:
            process.Menu('Next Page','http://www.xvideos.com'+url,705,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
            List.append('Next')

		
def XSearch_X():
    Search_Name = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    Search_Clean = (Search_Name).replace(' ','+').replace('&','&')
    Search_Title = Search_Clean.lower()
    Search_URL = 'http://www.xvideos.com/?k=' + Search_Title
    XNew_Videos(Search_URL)

def XPlayLink(url):
    import xbmc
    HTML = process.OPEN_URL(url)
    low = re.compile("html5player.setVideoUrlLow\('(.+?)'\);").findall(HTML)
    for item in low:
        low = item
    medium = re.compile("html5player.setVideoUrlHigh\('(.+?)'\);").findall(HTML)
    for item in medium:
        medium = item
    high = re.compile("html5player.setVideoHLS\('(.+?)'\);").findall(HTML)
    for item in high:
        high = item
    choices = ['Low Quality','Medium Quality','High Quality']
    choice = xbmcgui.Dialog().select('Select Playlink', choices)
    if choice==0:
        process.Resolve(low)
    elif choice==1:
        process.Resolve(medium)
    elif choice==2:
        process.Resolve(high)
