import xbmc,os

addon_id   = 'script.cypherstream'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))


def cat():
	addDir('[COLOR white][B]Arconaitv.me[/COLOR][/B]','arconaitv',2,'https://pbs.twimg.com/profile_images/590745210000433152/2u_nu2TM.png',fanart,'')
	addDir('[COLOR white][B]Fluxus TV[/COLOR][/B]','fluxustv',2,'https://pbs.twimg.com/profile_images/858019601820467200/FWi_rtsG.jpg',fanart,'')
	addDir('[COLOR white][B]iBrod.tv[/COLOR][/B]','ibrod',2,'https://www.ibrod.tv/images/logo.png',fanart,'')
	addDir('[COLOR white][B]LiveonlineTv247.to[/COLOR][/B]','liveonlinetv',2,'https://lh3.googleusercontent.com/_QDQuHHm1aj1wyBTRVBoemhvttNZ5fF4RhLG4BWoYpx0z69OKsbvg568hxup5oBqsyrJs7XV-w=s640-h400-e365',fanart,'')
	addDir('[COLOR white][B]Mamahd.com[/COLOR][/B]','mamahd',2,'http://www.topmanzana.com/static/mamahd.jpg',fanart,'')
	addDir('[COLOR white][B]Shadownet.ro[/COLOR][/B]','shadownet',2,'https://s4.postimg.org/iy7lkmw8d/logon.png',fanart,'')
	addDir('[COLOR white][B]Ustreamix.com[/COLOR][/B]','ustreamix',2,'https://cdn6.aptoide.com/imgs/a/7/8/a78c34966c4e443e7235d839b5856c0d_icon.png?w=256',fanart,'')
	addDir('[COLOR white][B]Youtube.com[/COLOR][/B]','youtube',2,'https://pbs.twimg.com/profile_images/877566581135597568/PkjTkC0V_400x400.jpg',fanart,'')
	
	
	
	
def get(url):
	if url == 'shadownet':
		shadownet()
	elif 'shadownetchan:' in url:
		shadownetchannels(url)
	elif url == 'ustreamix':
		ustreamix()
	elif url == 'ibrod':
		ibrod()
	elif url == 'fluxustv':
		fluxustv()
	elif url == 'liveonlinetv':
		liveonlinetv()
	elif url == 'arconaitv':
		arconaitv()
	elif url == 'youtube':
		xbmc.executebuiltin('ActivateWindow(Videos,plugin://plugin.video.youtube/kodion/search/query/?event_type=live&amp;q=live%20tv&amp;search_type=video)')
	elif url == 'mamahd':
		mamahd()
	elif url == 'crichd':
		crichd()
		
def mamahd():
	import re
	open = OPEN_URL('http://mamahd.com')
	part = regex_from_to(open,'<div class="standard row channels">','</div>')
	regex = re.compile('href="(.+?)".+?src="(.+?)".+?span>(.+?)<',re.MULTILINE|re.DOTALL).findall(part)
	for url,icon,name in regex:
		if not 'Stream' in name:
			if not 'Bundesliga' in name:
				if not 'Channel' in name:
					if not 'HD ' in name:
						addDir(name,url,10,icon,fanart,'')
def arconaitv():
	import urllib
	url = 'https://www.arconaitv.me'
	page = OPEN_URL(url)
	part = regex_from_to(page,'id="cable">','id="movies">')
	all_vids=regex_get_all(part,'div class="box-content"','</a>')
	for a in all_vids:
		url = regex_from_to(a,'href="','"')
		name = regex_from_to(a,'title="','"').replace('#038;','')
		if not url=='https://www.arconaitv.me/':
			if not name == 'A-E':
				if not name == 'F-J':
					if not name == 'K-O':
						if not name == 'P-T':
							if not name == 'U-Z':
								addDir('[B][COLOR white]%s[/COLOR][/B]'%name,urllib.quote_plus('https://www.arconaitv.me/'+url),10,icon,fanart,'')
		
def liveonlinetv():
	open = OPEN_URL('http://liveonlinetv247.info/tvchannels.php')
	all  = regex_get_all(open,'<li>','</li>')
	for a in all:
		name = regex_from_to(a,'">','<')
		url  = regex_from_to(a,'href=".*?channel=','"')
		if not 'Live' in name:
			if not 'UEFA' in name:
				if not 'Barclays Premier League' in name:
					if not 'IPL' in name:
						addDir('[B][COLOR white]%s[/COLOR][/B]'%name,'liveonlinetv247:'+url,10,icon,fanart,'')
		
		
def fluxustv():
	import re
	open  = OPEN_URL('https://raw.githubusercontent.com/fluxustv/IPTV/master/list.m3u')
	regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in regex:
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,10,icon,fanart,'')
		
		
def ibrod():
	open = OPEN_URL('https://www.ibrod.tv/tvchans.php')
	all  = regex_get_all(open,'<li> <span>','</a></li>')
	for a in all:
		name = regex_from_to(a,'</span> <span>','</span>')
		url  = regex_from_to(a,'href="','"')
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,'http://www.ibrod.tv/'+url,10,'https://www.ibrod.tv/images/logo.png',fanart,'')
		
		
		
def shadownet():
	open = OPEN_URL('http://www.shadownet.me')
	part = regex_from_to(open,'id="SideCategoryList">','class="afterSideCategoryList">')
	all  = regex_get_all(part,'<li class="">','</a>')
	for a in all:
		name = regex_from_to(a,'/">','<').replace('amp;','')
		url  = regex_from_to(a,'href="','"')
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,'shadownetchan:' + url,2,icon,fanart,'')	
		

def shadownetchannels(url):
	import urllib
	url  = (url).replace('shadownetchan:','')
	open = OPEN_URL(url)
	part = regex_from_to(open,'id="CategoryContent">','<br class="Clear" />')
	all  = regex_get_all(part,'<div class="ProductImage">','</li>')
	for a in all:
		name = regex_from_to(a,'alt="','"')
		url1  = regex_from_to(a,'href="','"')
		icon = regex_from_to(a,'img src="','"')
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url1,10,icon,fanart,name)
	try:
		np = regex_from_to(open,'<div class="FloatRight"><a href="','"')
		addDir('[COLOR red][B]Next Page >[/COLOR][/B]','shadownetchan:'+urllib.quote_plus(np),2,icon,fanart,'')
	except:
		pass
				
def ustreamix():
	import urllib
	open = OPEN_URL('http://v2.ustreamix.com')
	
	t    = OPEN_URL('http://www.newtvworld.com/livetv/india/DiscoveryChannel.html')
	all  = regex_get_all(open,'<p><a','</a>')
	for a in sorted(all):
		name = regex_from_to(a,'target="_blank">','<')
		url  = regex_from_to(a,'href="','"')
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,urllib.quote_plus('http://v2.ustreamix.com'+url),10,icon,fanart,'')
		
logfile    = xbmc.translatePath(os.path.join('special://home/addons/script.cypherstream', 'log.txt'))

def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
				
				
######################################################################################################
		
		
		
def regex_from_to(text, from_string, to_string, excluding=True):
	import re,string
	if excluding:
		try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r


def regex_get_all(text, start_with, end_with):
	import re,string
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r



def OPEN_URL(url):
	import requests
	headers = {}
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
	link = requests.session().get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
	
	

		
		
def addDir(name,url,mode,iconimage,fanart,description):
	import xbmcgui,xbmcplugin,urllib,sys
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==10:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory