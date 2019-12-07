import xbmc,os

addon_id   = 'script.cypherstream'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

def cat():
	addDir('[COLOR white][B]Freetvip.com[/COLOR][/B]','freetvvip',3,'https://cdn6.aptoide.com/imgs/a/7/8/a78c34966c4e443e7235d839b5856c0d_icon.png?w=256',fanart,'')
	addDir('[COLOR white][B]Iptv4sat.com[/COLOR][/B]','iptv4sat',3,'https://cdn6.aptoide.com/imgs/a/7/8/a78c34966c4e443e7235d839b5856c0d_icon.png?w=256',fanart,'')
	addDir('[COLOR white][B]Iptvfilmover.com[/COLOR][/B]','iptvfilmmover',3,'https://cdn6.aptoide.com/imgs/a/7/8/a78c34966c4e443e7235d839b5856c0d_icon.png?w=256',fanart,'')
	addDir('[COLOR white][B]Iptvsatlinks.com[/COLOR][/B]','iptvsattlinks',3,'https://cdn6.aptoide.com/imgs/a/7/8/a78c34966c4e443e7235d839b5856c0d_icon.png?w=256',fanart,'')
	addDir('[COLOR white][B]Panda TV[/COLOR][/B]','panda',3,'https://cdn6.aptoide.com/imgs/a/7/8/a78c34966c4e443e7235d839b5856c0d_icon.png?w=256',fanart,'')
	addDir('[COLOR white][B]Sourcetv.info[/COLOR][/B]','sourceetv',3,'https://cdn6.aptoide.com/imgs/a/7/8/a78c34966c4e443e7235d839b5856c0d_icon.png?w=256',fanart,'')
	
def get(url):
	if url == 'sourceetv':
		sourcetv()
	elif 'sourcetv' in url:
		sourcetvm3u(url)
	elif url == 'iptvsattlinks' or url.startswith('iptvsattlinks:'):
		iptvsatlinks(url)
	elif 'iptvsatlinks' in url:
		iptvsatlinksm3u(url)
	elif 'iptvfilmmover' in url:
		iptvfilmover('url')
	elif 'iptv.filmover.com/page' in url:
		iptvfilmover(url)
	elif 'iptv.filmover' in url:
		iptvfilmoverm3u(url)
	elif url == 'iptv4sat':
		iptv4sat()
	elif url == 'freetvvip':
		freetvip()
	elif url == 'panda':
		panda()
	else:
		listm3u(url)
		
		
		
def panda():
	import re
	open = OPEN_URL('http://pandasat.info/iptv/kodi')
	regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in regex:
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,10,icon,fanart,'')
		
def freetvip():
	import re,urllib
	open = OPEN_URL('http://freetvip.com/1876-2/')
	all  = re.compile('<strong><a.+?href="(.+?)">(.+?)<',re.DOTALL).findall(open)
	for url,name in all:
		url = (url).replace('amp;','').replace('#038;','')
		addDir(name,urllib.quote_plus(url),3,fanart,'','')
	
		
		
def iptv4sat():
	from resources.modules import downloader
	import os,re
	open = OPEN_URL('https://www.iptv4sat.com/download-iptv-sport/')
	part = regex_from_to(open,'<tr class="zip">','</td>')
	zip  = regex_from_to(part,'href="','"')
	
	udata= xbmc.translatePath('special://home/userdata/addon_data/script.cypherstream/downloads/')
	dest = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.cypherstream/downloads/', 'iptv4sat.zip'))
	if not os.path.exists(udata):
		os.makedirs(udata)
	downloader.download(zip,dest)
	downloader.unzip(dest,udata)
	os.remove(dest)
	dir = os.listdir(udata)
	for a in dir:
		if a.endswith('.m3u'):
			m3u = readfile(udata,a)
			os.remove(xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.cypherstream/downloads/',a)))
			regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(m3u)
			for name,url in regex:
				addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,10,icon,fanart,'')
				
def iptvfilmover(url):
	if url == 'url':
		open = OPEN_URL('http://iptv.filmover.com/')
	else:
		open = OPEN_URL(url)
	all  = regex_get_all(open,'<article id="','</article>')
	for a in all:
		name = regex_from_to(a,'rel="bookmark">','</a>').strip()
		url  = regex_from_to(a,'href="','"')
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,3,icon,fanart,'')
	try:
		np = regex_from_to(open,'<a class="next page-numbers" href="','"')
		addDir('[COLOR red][B]Next Page >[/B][/COLOR]',np,3,icon,fanart,'')
	except:
		pass
def iptvfilmoverm3u(url):
	import re
	open = OPEN_URL(url)
	m3u  = regex_from_to(open,'</strong></p>','</script>')
	regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(m3u)
	for name,url in regex:
		name = (name).replace('<br />','')
		url  = (url).replace('<br />','')
		log(url)
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,10,icon,fanart,'')
		
		
def iptvsatlinks(url):
	if not url == 'iptvsattlinks':
		url  = (url).replace('iptvsattlinks:','')
		open = OPEN_URL(url)
	else:
		open = OPEN_URL('http://iptvsatlinks.com')
	all  = regex_get_all(open,'<header class="mh-loop-header">','</a>')
	for a in all:
		name = regex_from_to(a,'rel="bookmark">','</a>').strip()
		url  = regex_from_to(a,'href="','"')
		if not '{New m3u}' in name:
			addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,3,icon,fanart,'')
	try:
		np = regex_from_to(open,'<a class="next page-numbers" href="','"')
		addDir('[COLOR red][B]Next Page >[/COLOR][/B]','iptvsattlinks:'+np,3,icon,fanart,'')
	except:
		pass
		
def iptvsatlinksm3u(url):
	import re
	open = OPEN_URL(url)
	m3u  = regex_from_to(open,'<pre><code>','</code></pre>')
	if '.ts' in m3u:
		regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(m3u)
		for name,url in regex:
			addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,10,icon,fanart,'')
		
def sourcetv():
	open = OPEN_URL('https://sourcetv.info/')
	all  = regex_get_all(open,'<div class="article-image-wrapper">','<div class="panel">')
	for a in all:
		name = regex_from_to(a,'title="','"')
		url  = regex_from_to(a,'href="','"')
		icon = regex_from_to(a,'src="','"')
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,3,icon,fanart,'')
def sourcetvm3u(url):
	import re
	open = OPEN_URL(url)
	url  = regex_from_to(open,'<p><a href="','"')
	open = OPEN_URL(url)
	regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in regex:
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,10,icon,fanart,'')
		
		
		
def listm3u(url):
	import re
	open = OPEN_URL(url)
	regex = re.compile('#EXTINF:.+?\,(.+?)\n(.+?)\n', re.MULTILINE|re.DOTALL).findall(open)
	for name,url in regex:
		if name.endswith('.ts') or name.endswith('.m3u'):
			url = name
		addDir('[B][COLOR white]%s[/COLOR][/B]'%name,url,10,icon,fanart,'')
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
	
logfile    = xbmc.translatePath(os.path.join('special://home/addons/script.cypherstream', 'log.txt'))

def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
	
	
def readfile(url,file):
            file = open(os.path.join(url, file))
            data = file.read()
            file.close()
            return data

		
		
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