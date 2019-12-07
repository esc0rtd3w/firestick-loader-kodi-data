import base64,hashlib,os,random,re,requests,shutil,string,sys,urllib,urllib2,json,urlresolver,ssl,zipfile,urlparse
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs


addon_id   = 'script.module.sportsvod'

icon       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
putlockerhd  = 'http://putlockerhd.co'
ccurl      = 'http://cartooncrazy.me'
s          = requests.session()
xxxurl     ='http://www.xvideos.com'
kidsurl    = base64.b64decode ('')
docurl     = 'http://documentaryheaven.com'
mov2       = 'http://zmovies.to'
wwe        = 'http://watchwrestling.in'
tv         = base64.b64decode ('')
proxy      = 'http://www.justproxy.co.uk/index.php?q='
music      = 'http://woodmp3.net/mp3.php?q='
movies_url = 'https://torba.se'
logfile    = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'log.txt'))
def log(text):
	file = open(logfile,"w+")
	file.write(str(text))
	
def fullmatchtv(url):
	open = OPEN_URL(url)
	part = regex_from_to(open,'<span>Latest.+?</span>','</div></div></div>')
	all  = re.compile('<div class="td-module-thumb">.+?href="(.+?)".+?title="(.+?)".+?src="(.+?)"',re.DOTALL).findall(part)
	for url,name,icon in all:
		addDir(name.replace('&#8211;','-'),url,117,icon,fanart,'')
		
def rugbyget(url):
	open = OPEN_URL(url)
	url  = regex_from_to(open,'iframe src="','"')
	
	play=urlresolver.HostedMediaFile(url).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
def footballhighlight():
	open = OPEN_URL('http://livefootballvideo.com/highlights')
	all  = regex_get_all(open,'class="date_time','class="play_btn')
	for a in all:
		home = regex_from_to(a,' class="team home.+?>','&nbsp')
		away = regex_from_to(a,'class="team column".+?alt="','"')
		date = regex_from_to(a,'shortdate".+?>','<')
		score= regex_from_to(a,'class="score">','<')
		url  = regex_from_to(a,'href="','"')
		if 'span class' in score:
			score = 'Postponed'
		
		name = '[COLOR ffff0000][B]%s[/COLOR][/B]: %s v %s | %s'%(date,home,away,score)
		addDir(name,'HIGHLIGHT:'+url,113,icon,fanart,'')
		#log(t)

def footballreplays(url):
	if not url.startswith('http'):
		open = OPEN_URL('http://livefootballvideo.com/fullmatch')
	else:
		open = OPEN_URL(url)
		
	all  = regex_get_all(open,'<div class="cover">','</li>')
	for a in all:
		name = regex_from_to(a,'title="','"')
		url  = regex_from_to(a,'href="','"')
		icon = regex_from_to(a,'img src="','"')
		date = regex_from_to(a,'class="postmetadata longdate.+?">','<')
		log(date)
		addDir('[COLOR ffff0000][B]%s[/COLOR][/B]: %s'%(date,name),url,113,icon,fanart,'')
		
	try:
		np = regex_from_to(open,'class="nextpostslink.+?href="','"')
		addDir('[COLOR ffff0000][B]Next Page >[/COLOR][/B]',np,112,icon,fanart,'')
	except:
		pass
		
def footballreplaysget(url):
	if url.startswith('HIGHLIGHT:'):
		url = url.replace('HIGHLIGHT:','')
		open = OPEN_URL(url)
		url  = re.compile('><iframe src="(.+?)"').findall(open)[0]
	else:
		open = OPEN_URL(url)
		all  = re.findall('><iframe src="(.+?)"',open)
		d    = xbmcgui.Dialog().select('Select a Half', ['First Half: 0 - 45min', 'Second Half: 45 - 90min'])
		if d==0:
			url = all[0]
		elif d==1:
			url = all[1]
		else:
			return
	
	play=urlresolver.HostedMediaFile(url).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	

def CAT():
	addDir('EXABYTE','url',85,icon,fanart,'')
	addDir('MOVIES2','url',37,icon,fanart,'')
	addDir('FAMILY SECTION',kidsurl,56,icon,fanart,'')
	addDir('XXX SECTION','URL',31,icon,fanart,'')
	addDir('DOCS',docurl+'/watch-online/',35,icon,fanart,'')
	addDir('24/7 TV',tv,47,icon,fanart,'')
	addDir('MUSIC',tv,64,icon,fanart,'')
	addDir('IPTV','url',84,icon,fanart,'')
	addDir('IPTV2','url',88,icon,fanart,'')
	addDir('Liveonlinetv','url',95,icon,fanart,'')
	addDir('jango','url',106,icon,fanart,'')
	addDir('MLB','http://fullmatchtv.com/mlb',116,icon,fanart,'')
	addDir('NBA','http://fullmatchtv.com/basketball',116,icon,fanart,'')
	addDir('NFL','http://fullmatchtv.com/nfl',116,icon,fanart,'')
	addDir('NHL','http://fullmatchtv.com/nhl',116,icon,fanart,'')
	addDir('Rugby','http://fullmatchtv.com/rugby',116,icon,fanart,'')
	addDir('jango','url',99999,icon,fanart,'')
	
	

def MOV2CAT():
	addDir('[COLOR red]L[/COLOR]atest Releases','NEW:http://novamovie.net',79,icon,fanart,'')
	addDir('[COLOR red]M[/COLOR]ost Popular','http://novamovie.net',79,icon,fanart,'')
	addDir('[COLOR red]M[/COLOR]ost Viewed','http://novamovie.net/?v_sortby=views&v_orderby=desc',79,icon,fanart,'')
	addDir('[COLOR red]R[/COLOR]ecommended','http://novamovie.net/tag/recommended/',79,icon,fanart,'')
	addDir('[COLOR red]G[/COLOR]enres','url',81,icon,fanart,'')
	addDir('[COLOR red]Y[/COLOR]ears','years',81,icon,fanart,'')
	addDir('[COLOR red]S[/COLOR]earch','url',82,icon,fanart,'')
def TVREQUESTCAT():
	addDir('Everybody Loves Raymond','ELR',50,'http://www.gstatic.com/tv/thumb/tvbanners/184243/p184243_b_v8_ab.jpg','','')
	addDir('How i Met Your Mother','HIMYM',50,'http://www.gstatic.com/tv/thumb/tvbanners/9916255/p9916255_b_v8_aa.jpg','','')
	addDir('Naked And Afraid','NAA',50,'http://www.gstatic.com/tv/thumb/tvbanners/9974211/p9974211_b_v8_ad.jpg','','')
	addDir('The Walking Dead','TWD',50,'http://www.gstatic.com/tv/thumb/tvbanners/13176393/p13176393_b_v8_ab.jpg','','')
	addDir('[COLOR red][B]IF IT FAILS THE FIRST TIME CLICK IT AGAIN[/COLOR][/B]','url','','','','')
	
def FAMILYCAT():
	addDir('Disney Movies','url',58,icon,fanart,'')
	addDir('Family Cartoons',kidsurl,51,icon,fanart,'')
	addDir('Family Movies','http://kisscartoon.so/cartoon-movies/',77,icon,fanart,'')
	
def FAMILYMOVIESCAT():
	addDir('All','http://kisscartoon.so/cartoon-movies/',74,icon,fanart,'')
	addDir('By Year','http://kisscartoon.so/cartoon-movies/',78,icon,fanart,'')
	addDir('By Genre','http://kisscartoon.so/cartoon-movies/',76,icon,fanart,'')

def MUSICCAT():
	addDir('Popular Artists','http://',107,icon,fanart,'')
	addDir('Top Music','http://',68,icon,fanart,'')
	addDir('Collections','url',72,icon,fanart,'')
	addDir('Radio','http://',69,icon,fanart,'')
	addDir('Search','search',63,icon,fanart,'')
	
def TOPMUSICAT():
	addDir('UK | The Offical Top 40 Singles','http://www.bbc.co.uk/radio1/chart/singles',67,icon,fanart,'')
	addDir('UK | The Offical Top 40 Dance Singles','http://www.bbc.co.uk/radio1/chart/dancesingles',67,icon,fanart,'')
	addDir('UK | The Offical Top 40 Rock Singles','http://www.bbc.co.uk/radio1/chart/rocksingles',67,icon,fanart,'')
	addDir('UK | The Offical Top 40 R&B Singles','http://www.bbc.co.uk/radio1/chart/rnbsingles',67,icon,fanart,'')
	addDir('UK | The Offical Top 30 Indie Singles','http://www.bbc.co.uk/radio1/chart/indiesingles',67,icon,fanart,'')
	
def MUSICCOL():
	addDir('BBC Radio 1 Live Lounge Collection','https://www.discogs.com/label/804379-Radio-1s-Live-Lounge',70,icon,fanart,'')
	addDir('Now Thats What I Call Music Collection','NOW',70,icon,fanart,'')

def jango():
	addDir('Popular Artists','url',107,icon,fanart,'')
	addDir('Genres','url',109,icon,fanart,'')
	
def jangopopular():
	open = OPEN_URL('http://www.jango.com')
	
	part = regex_from_to(open,'Popular Choices','class="station_module_bottom" >')
	
	all  = regex_get_all(part,'<a class="station_anchor"','</a>')
	for a in all:
		name = regex_from_to(a,'<span class="sp_tgname">','</span>').strip()
		icon = 'http:' + regex_from_to(a,'data-original="','"').strip()
		url  = 'http://www.jango.com'+regex_from_to(a,'href="','"').strip()
		addDir(name,url,108,icon,fanart,'')
		
		
def jangogenres(url):
	if url == 'url':
		open = OPEN_URL('https://www.jango.com/browse_music')
		
		part = regex_from_to(open,'<ul id="genres">','</ul>')
		all  = regex_get_all(part,'<li id','</li>')
		for a in all:
			name = regex_from_to(a,'title="','"')
			url  = 'https://www.jango.com'+regex_from_to(a,'href="','"')
			addDir(name,url,108,icon,fanart,'')
	else:
		open = OPEN_URL(url)
		all  = regex_get_all(open,'<div class="left left_body">','</div>')
		for a in all:
			name = regex_from_to(a,'</span></span>','</a>')
			url  = regex_from_to(a,'href="','"')
			addDir(name,url,2,icon,fanart,'')
		
def jangosongs(url):
	if not 'gcid=' in url:
		url  = url+'/_more_songs?limit=250&np=all'
		open = OPEN_URL(url)
		
	#open = requests.session().get(url,headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Encoding':'gzip, deflate','Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6','User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'},verify=False).text
	all  = regex_get_all(open,'<li class="song_li artist_song_li','</div>')
	for a in all:
		name = regex_from_to(a,'title="','"').replace('Play','').replace('Now!','')
		url  = regex_from_to(a,'video_id&quot;:&quot;','&')
		icon = regex_from_to(a,'data-original="','"')
		addDir(replaceHTMLCodes(name),url,62,icon,fanart,'')
		
	
	
def replaceHTMLCodes(txt):
    import HTMLParser
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.strip()
    return txt
	
def NOVAMOVIES(url):
	if url.startswith('NEW:'):
		url  = str(url).replace('NEW:','')
		open = OPEN_URL(url)
		part = regex_from_to(open,'<div id="slider2"','<h1 style="display:none;">')
		all  = regex_get_all(part,'<div class="item"','</div>')
		for a in all:
			name = regex_from_to(a,'alt="','"')
			url  = regex_from_to(a,'href="','"')
			icon = regex_from_to(a,'img src="','"')
			addDir(name,url,80,icon,fanart,'')
	else:
		open = OPEN_URL(url)
		part = regex_from_to(open,'<h1 style="display:none;">','</html>')
		if not part == "":
			all  = regex_get_all(part,'<div class="fixyear">','</a>')
			for a in all:
				name = regex_from_to(a,'alt="','"')
				url  = regex_from_to(a,'href="','"')
				icon = regex_from_to(a,'img src="','"')
				addDir(name,url,80,icon,fanart,'')
		else:
			all  = regex_get_all(open,'<div class="fixyear">','</a>')
			for a in all:
				name = regex_from_to(a,'alt="','"')
				url  = regex_from_to(a,'href="','"')
				icon = regex_from_to(a,'img src="','"')
				addDir(name,url,80,icon,fanart,'')
		
		try:
			np = regex_from_to(open,'<div class="pag_b"><a href="','"')
			addDir('[COLOR red][B]NEXT PAGE >[/B][/COLOR]',np,79,icon,fanart,'')
		except:
			pass
	
def NOVAMOVIESGENRE(url):
	open = OPEN_URL('http://novamovie.net')
	if not url == 'years':
		part = regex_from_to(open,'>GENRE</a>','</ul>')
	else:
		part = regex_from_to(open,'>YEAR</a>','</ul>')
	all  = regex_get_all(part,'<li','</li')
	for a in all:
		name = regex_from_to(a,'/">','<')
		url  = regex_from_to(a,' href="','"')
		addDir(name,url,79,icon,fanart,'')
	
	
def NOVAMOVIESSEARCH():

	kb = xbmc.Keyboard ('', 'Search For a Movie', False)
	kb.doModal()
	if (kb.isConfirmed()):
		query = kb.getText()
		query = str(query).replace(' ','+')

	open = OPEN_URL('http://novamovie.net/?s='+query)
	all  = regex_get_all(open,'<div class="fixyear">','</a>')
	for a in all:
		name = regex_from_to(a,'alt="','"')
		url  = regex_from_to(a,'href="','"')
		icon = regex_from_to(a,'img src="','"')
		if not name=="":
			addDir(name,url,80,icon,fanart,'')

	
def xxxCAT():
	if xbmcaddon.Addon().getSetting('freshstart')=='true':
		setxxxpass()
		xbmcaddon.Addon().setSetting('freshstart','false')
	if xbmcaddon.Addon().getSetting('enablexxxpass')=='true':
		kb = xbmc.Keyboard ('', 'Enter Your Password', False)
		kb.doModal()
		if (kb.isConfirmed()):
			pw = kb.getText()
			if pw == xbmcaddon.Addon().getSetting('xxxpass'):
				addDir("The Best Videos",xxxurl+'/best',24,icon,fanart,'')
				addDir("Latest Videos",xxxurl,24,icon,fanart,'')
				addDir("Real Videos",xxxurl+'/c/Amateur-17',24,icon,fanart,'')
				addDir("All Videos",xxxurl+'/tags',99,icon,fanart,'')
				addDir("Search",'search',24,icon,fanart,'')
			else:
				xbmcgui.Dialog().ok('[COLOR red][B]ProjectCypher[/B][/COLOR]','Incorrect Password, Please Try Again')
				return
	else:
		addDir("The Best Videos",xxxurl+'/best',24,icon,fanart,'')
		addDir("Latest Videos",xxxurl,24,icon,fanart,'')
		addDir("Real Videos",xxxurl+'/c/Amateur-17',24,icon,fanart,'')
		addDir("All Videos",xxxurl+'/tags',99,icon,fanart,'')
		addDir("Search",'search',24,icon,fanart,'')
	

def setxxxpass():
	d = xbmcgui.Dialog().yesno('[COLOR red]ProjectCypher[/COLOR]','Would You Like To Set a Password for the XXX Section?')
	if d:
		kb = xbmc.Keyboard ('', 'Please Enter a Password', False)
		kb.doModal()
		if (kb.isConfirmed()):
			pw = kb.getText()
			if pw =="":
				xbmcgui.Dialog().notification('[COLOR red]Password Cannot Be Blank[/COLOR]','ProjectCypher')
				setxxxpass()
			else:
				xbmcaddon.Addon().setSetting('xxxpass',pw)
				xbmcaddon.Addon().setSetting('enablexxxpass','true')
				xbmcgui.Dialog().ok('[COLOR red]ProjectCypher[/COLOR]','Password has been set')
			

	
	
	
	
def NOVAMOVIERESOLVE(url):
	open = OPEN_URL(url)
	url  = re.compile('<iframe.+?src="(.+?)"').findall(open)[0]
	open = OPEN_URL('http:'+url)
	res_quality = []
	stream_url  = []
	quality     = ''

	match = regex_get_all(open,'file"','type"')
	try:
		for a in match:
			quality = '[B][I][COLOR red]%s[/COLOR][/I][/B]' %regex_from_to(a,'label": "','"')
			url     =  regex_from_to(a,': "','"')
			if not '.srt' in url:
				res_quality.append(quality)
				stream_url.append(url)
		if len(match) >1:
			ret = xbmcgui.Dialog().select('Select Stream Quality',res_quality)
			if ret == -1:
				return
			elif ret > -1:
				url = stream_url[ret]
			else:
				url = regex_from_to(open,'file":"','"')
	except:
		url = regex_from_to(open,'file":"','"')
		
	liz = xbmcgui.ListItem('', iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels='')
	liz.setProperty("IsPlayable","true")
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	

	
	
	
	

def tvlist(url):
    thumb = ''
    art   = ''
    OPEN = Open_Url(url)
    Regex = re.compile('<title>(.+?)</title>.+?url>(.+?)</url>.+?thumb>(.+?)</thumb>',re.DOTALL).findall(OPEN)
    for name,url,icon in Regex:
		addDir(name,url,46,icon,fanart,'') 
		
		



def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def OPEN_URLputlockerhd(url):
        headers = {}
        headers['User-Agent'] = User_Agent
        link = requests.get(url, headers=headers, allow_redirects=False).text
        link = link.encode('ascii', 'ignore').decode('ascii')
        return link
		
def addDirputlockerhd(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        liz.setProperty('fanart_image', fanart)
        if mode==3 or mode ==15:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
	
def putlockerhdread(url):
        url = url.replace('https','http')
        link = OPEN_URLputlockerhd(url)
        all_videos = regex_get_all(link, 'cell_container', '<div><b>')
        items = len(all_videos)
        for a in all_videos:
                name = regex_from_to(a, 'a title="', '\(')
                name = addon.unescape(name)
                url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
                thumb = regex_from_to(a, 'src="', '"')
                addDirputlockerhd(name,putlockerhd+url,15,'http://'+thumb,fanart,'')
        try:
                match = re.compile('<a href="(.*?)\?page\=(.*?)">').findall(link)
                for url, pn in match:
                        url = putlockerhd+url+'?page='+pn
                        addDir('[I][B][COLOR red]Page %s [/COLOR][/B][/I]' %pn,url,19,icon,fanart,'')
        except: pass
		
def putlockerhdplay(url):
    try:
        url = re.split(r'#', url, re.I)[0]
        request_url = putlockerhd+'/video_info/iframe'
        link = OPEN_URLputlockerhd(url)
        form_data={'v': re.search(r'v\=(.*?)$',url,re.I).group(1)}
        headers = {'origin':'http://putlockerhd.co', 'referer': url,
                   'user-agent':User_Agent,'x-requested-with':'XMLHttpRequest'}
        r = requests.post(request_url, data=form_data, headers=headers, allow_redirects=False)
        try:
                url = re.findall(r'url\=(.*?)"', str(r.text), re.I|re.DOTALL)[-1]
        except:
                url = re.findall(r'url\=(.*?)"', str(r.text), re.I|re.DOTALL)[0]
        url = url.replace("&amp;","&").replace('%3A',':').replace('%3D','=').replace('%2F','/')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
	
def xxx(url):
        if url=='search':
			kb = xbmc.Keyboard ('', 'Enter a Search Query', False)
			kb.doModal()
			if (kb.isConfirmed()):
				query = kb.getText()
				query = str(query).replace(' ','+').lower()
				url   = xxxurl+'/?k='+query
        link = OPEN_URL(url)
        try:
			xxxadd_next_button(link)
        except:pass
        all_videos = regex_get_all(link, 'class="thumb-block ">', '</a></p>')
        for a in all_videos:
			name = regex_from_to(a, 'title="', '"')
			name = str(name).replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#039;',"'")
			url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
			thumb = regex_from_to(a, '<img src="', '"')
			addDir(name,'http://www.xvideos.com'+url,27,thumb,'','')
			

def xxxadd_next_button(link):
			try:
				if '/tags/' in link:
					link = str(link).replace('\n','').replace('\r','').replace('\t','').replace(' ','').replace('  ','')
					nextp=regex_from_to(link,'<aclass="active"href="">.+?</a></li><li><ahref="','"')
					addDir('[B][COLOR red]Next Page>>>[/COLOR][/B]',xxxurl+nextp,24,'','','')
			except: pass
			
			try:
				if '/tags/' not in link:
					link = str(link).replace('\n','').replace('\r','').replace('\t','').replace(' ','').replace('  ','')
					nextp = regex_from_to(link,'<aclass="active"href="">.+?</a></li><li><ahref="','"')
					if not nextp=='':return
					addDir('[B][COLOR red]Next Page[/COLOR][/B]',xxxurl+nextp,24,'','','')
			except: pass
			return
		
def xxxgenre(url):
		if xbmcaddon.Addon().getSetting('enablexxxpass')=='true':
			kb = xbmc.Keyboard ('', 'Please Enter Your XXX Password', False)
			kb.doModal()
			if (kb.isConfirmed()):
				pw = kb.getText()
				if pw == xbmcaddon.Addon().getSetting('xxxpass'):
					url = url
				else:
					xbmcgui.Dialog().ok('Attention','Incorrect Password, Please Try Again')
					return
			else:
				xbmcgui.Dialog().ok('Attention','Blank Password is Not Aloud, Please Try Again')
				return
		link = OPEN_URL(url)
		main = regex_from_to(link,'<strong>All tags</strong>','mobile-hide')
		all_videos = regex_get_all(main, '<li>', '</li>')
		for a in all_videos:
			name = regex_from_to(a, '"><b>', '</b><span').replace("&amp;","&")
			url = regex_from_to(a, 'href="', '"').replace("&amp;","&")
			url = url+'/'
			thumb = regex_from_to(a, 'navbadge default">', '<')
			addDir('%s     [B][COLOR red](%s Videos)[/COLOR][/B]' %(name,thumb),xxxurl+url,24,'','','')
			

def resolvexxx(url):
	base = 'http://www.xvideos.com'
	page  = OPEN_URL(url)
	page=urllib.unquote(page.encode("utf8"))
	page=str(page).replace('\t','').replace('\n','').replace('\r','').replace('                                            	','')
	play = regex_from_to(page,"setVideoUrlHigh.+?'","'")
	url = str(play).replace('[','').replace("'","").replace(']','')
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
        liz.setInfo(type='Video', infoLabels={'Title':description})
        liz.setProperty("IsPlayable","true")
        liz.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	

def passpopup(url):
 kb =xbmc.Keyboard ('', 'heading', True)
 kb.setHeading('Enter 18+ Password') # optional
 kb.setHiddenInput(True) # optional
 kb.doModal()
 if (kb.isConfirmed()):
    text = kb.getText()
    if text == str(xbmcaddon.Addon().getSetting('xxxpass')):
		url = str(url).replace('****','/tags')
		return url
    else:
        xbmcgui.Dialog().ok('Attention', "Incorrect Password, You would of set this on first use of this Addon.")

def documentary(url):
	OPEN = OPEN_URL(url)
	regex = regex_get_all(OPEN,'<h2><a href','alt="')
	for a in regex:
		url = regex_from_to(a,'="','"')
		title = regex_from_to(a,'">','<').replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
		thumb = regex_from_to(a,'img src="','"')
		vids = regex_from_to(a,'</a> (',')</h2>').replace('(','').replace(')','')
		if vids == "":
			addDir(title,url,36,thumb,fanart,'')
		else:
			addDir(title,docurl+url,35,thumb,fanart,'')
	try:
		link = re.compile('<li class="next-btn"><a href="(.+?)"').findall(OPEN)
		link = str(link).replace('[','').replace(']','').replace("'","")
		xbmc.log(str(link))
		if link == "":
			return False
		else:
			addDir('[B][COLOR red]NEXT PAGE[/COLOR][/B]',link,35,thumb,fanart,'')
	except:pass
def resolvedoc(url):
	open = OPEN_URL(url)
	xbmc.log(str(open))
	url = regex_from_to(open,'iframe.+?src="','"')
	url = regex_from_to(url,'/embed/','$')
	url = 'plugin://plugin.video.youtube/play/?video_id='+url
	
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
	liz.setProperty('IsPlayable','true')
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

	
def opentwentyfourseven(url):
	url = 'https://www.arconaitv.me'
	page = OPEN_URL(url)
	part = regex_from_to(page,'id="shows">','id="cable">')
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
								addDir(name,urllib.quote_plus('https://www.arconaitv.me/'+url),46,icon,fanart,'')
								
	part = regex_from_to(page,'id="movies">','id="donate">')
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
								addDir(name,urllib.quote_plus('https://www.arconaitv.me/'+url),46,icon,fanart,'')
		
		
def resolvetwentyfourseven(url,name):
	ref  = url
	open = OPEN_URL(url)
	m3u  = re.compile('source src="(.*?)"',re.DOTALL).findall(open)[0]
	m3u  = (m3u).replace('\/','/')
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
	liz.setProperty('IsPlayable','true')
	liz.setPath(m3u+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36&Referer='+ref)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
def home():
	home = xbmc.executebuiltin('XBMC.RunAddon(plugin://plugin.video.ProjectCypher/?action=)')
	return home
	

#get = OPEN_URL(cartoons)
#xbmc.log(str(get))
		
def toongetlist(url):
	open = OPEN_URL(url)
	all  = regex_get_all(open,'<td>','</td>')
	for a in all:
		url = regex_from_to(a,'href="','"')
		name= regex_from_to(a,'">','<')
		addDir('[COLOR white]%s[/COLOR]'%name,url,52,icon,fanart,'')
		
def toongeteps(url):
		open = OPEN_URL(url)
		all  = regex_get_all(open,'&nbsp;&nbsp;','<span')
		for a in all:
			url = regex_from_to(a,'href="','"')
			name = regex_from_to(a,'">','<')
			addDir('[COLOR white]%s[/COLOR]'%name,url,53,icon,fanart,'')
			
def toongetresolve(name,url):
    OPEN = OPEN_URL(url)
    url1=regex_from_to(OPEN,'Playlist 1</span></div><div><iframe src="','"')
    url2=regex_from_to(OPEN,'Playlist 2</span></div><div><iframe src="','"')
    url3=regex_from_to(OPEN,'Playlist 3</span></div><div><iframe src="','"')
    url4=regex_from_to(OPEN,'Playlist 4</span></div><div><iframe src="','"')
    xbmc.log(str(url1))
    xbmc.log(str(url2))
    xbmc.log(str(url3))
    xbmc.log(str(url4))
    try:
			u   = OPEN_URL(url1)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url2)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url3)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass
    try:

			u   = OPEN_URL(url4)
			play= regex_from_to(u,'link":"','"').replace('\/','/')
			liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
			liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
			liz.setProperty('IsPlayable','true')
			liz.setPath(str(play))
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:
		xbmcgui.Dialog().notification('[COLOR red][B]ProjectCypher[/B][/COLOR]','Oops, This Link Is Down!')
	
def disneymovies(url):
	open = OPEN_URL(url)
	a    = regex_from_to(open,'<br /></div>','<center>')
	all  = regex_get_all(a,'<a href','</div>')
	for a in all:
		url = regex_from_to(a,'="','"')
		name= regex_from_to(a,'<b>','</b>').replace('#038;','').replace('&#8217;',"'")
		addDir('[COLOR white]%s[/COLOR]'%name,url,57,icon,fanart,'')
		
def disneymoviesresolve(url):
	open = OPEN_URL(url)
	try:
		url1 = re.compile('scrolling="no" src="(.*?)"').findall(open)[0]
	except:
		url1 = re.compile('<iframe.+?src="(.*?)"').findall(open)[0]
	if url1.startswith('https://href.li/?'):
		url1 = str(url1).replace('https://href.li/?','')
	play=urlresolver.HostedMediaFile(url1).resolve()
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(play))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def musicsearch(url):
		if url == 'search':
			kb = xbmc.Keyboard ('', 'Enter Your Favourite Song or Artist', False)
			kb.doModal()
			if (kb.isConfirmed()):
				query = kb.getText()
				query = (query.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
				open  = OPEN_URL('http://woodmp3.net/mp3.php?q='+query)
				all   = regex_get_all(open,'<form action="" method="post">','</form>')
				for a in all:
					name = regex_from_to(a,'title.+?value="','"').replace('Free','').replace('mp3','')
					icon = regex_from_to(a,'image.+?value="','"')
					url  = regex_from_to(a,'link.+?value="','"')
					addDir(name,url,62,icon,fanart,'')
		else:
				xbmc.log(str(url))
				open  = OPEN_URL(url)
				all   = regex_get_all(open,'<form action="" method="post">','</form>')
				for a in all:
					name = regex_from_to(a,'title.+?value="','"').replace('Free','').replace('mp3','')
					icon = regex_from_to(a,'image.+?value="','"')
					url  = regex_from_to(a,'link.+?value="','"')
					addDir(name,url,62,icon,fanart,'')
			
def musicindex(url):
	open  = OPEN_URL(url)
	all   = regex_get_all(open,'<div class="song-list"','<i class="fa fa-download">')
	for a in all:
		name = regex_from_to(a,'title="','"').replace('Free','').replace('mp3','')
		icon = regex_from_to(a,' src="','"')
		url  = regex_from_to(a,'none;"><a href="','"')
		addDir(name,url,63,icon,fanart,'')			
def musicresolve(url):
	url  = 'http://www.youtubeinmp3.com/widget/button/?video=https://www.youtube.com/watch?v=%s&color=008000'%url
	open = OPEN_URL(url)
	mp3  = regex_from_to(open,'downloadButton" href="','"')
	xbmc.log(str(mp3))
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Music', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str('http://www.youtubeinmp3.com'+mp3))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
			
def bbcmusicindex(url):
	open = OPEN_URL(url)
	all = regex_get_all(open,'<div class="cht-entry-wrapper">','<div class="cht-entry-status">')
	if 'singles' in url:
		for a in all:
			num  = regex_from_to(a,'<div class="cht-entry-position">','<').strip()
			name = regex_from_to(a,'data-title="','"').replace('||','-').replace('&amp;','')
			name = '[COLOR red]%s[/COLOR] | %s'%(num,name)
			icon = regex_from_to(a,'         src="','"')
			url  = 'http://woodmp3.net/mp3.php?q='+(name.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
			url  = regex_from_to(url,']-','$').replace('(','ABCD')
			url  = re.sub(r'ABCD(.*?)$','',url)
			addDir(name,'http://woodmp3.net/mp3.php?q='+re.sub('-$','',url),63,icon,fanart,'')
			
			
def top40(url):
	open = OPEN_URL(url)
	part  = regex_from_to(open,'<table align=center','<BR><BR>')
	all   = regex_get_all(part,'big>&nbsp;&nbsp;&nbsp;','font class=small>')
	for a in all:
		name = regex_from_to(a,'hspace=5 border=0>','<')
		addDir(name,'url',4,icon,fanart,'')
		
def radio():
	open =OPEN_URL('https://raw.githubusercontent.com/sClarkeIsBack/ProjectCypher/master/Links/RADIO.xml')
	all = regex_get_all(open,'<item>','</item>')
	for a in all:
		name = regex_from_to(a,'<title>','</title>')
		url  = regex_from_to(a,'<link>','</link>')
		icon = regex_from_to(a,'<thumbnail>','</thumbnail>')
		addDir(name,url,999,icon,fanart,'')

def UKNowMusic(url):
	if 'Live-Lounge' in url:
		desc = 'BBCL'
	else:
		desc = 'url'
	if url == 'NOW':
		d    = xbmcgui.Dialog().select('Choose a Country', ['UK Version', 'US Version'])
		if d==0:
			url = 'https://www.discogs.com/label/266040-Now-Thats-What-I-Call-Music!-UK'
		elif d==1:
			url = 'https://www.discogs.com/label/266110-Now-Thats-What-I-Call-Music!-US'
		else:
			return
	
	
	if '-US' in url:
		country = 'USA'
	else:
		country = 'UK'
	open = OPEN_URL(url)
	all  = regex_get_all(open,'td class="artist">','<td class="actions">')
	for a in all:
		url   = regex_from_to(a,' <a href="','"')
		title = regex_from_to(a,'[0-9]">','<').replace('&#39;',"'")
		year  = regex_from_to(a,'Year: ">','<')
		if not 'DVD' in title:
			xbmc.log(str(url))
			addDir('[COLOR red]%s[/COLOR] | [COLOR red]%s[/COLOR]'%(country,year)+' | '+title,url,71,icon,fanart,desc)
			
def UKNowMusic2(url,description):
	open = OPEN_URL('https://www.discogs.com'+url)
	all = regex_get_all(open,'<td class="tracklist_track_artists">','<tr class=" tracklist_track track"')
	for a in all:
		artist = re.compile('a href=".*?">(.*?)<',re.DOTALL).findall(a)
		artist = str(artist).replace("['","").replace("']","").replace('&#39;',"'").replace("'","").replace('"','')
		
		track  = regex_from_to(a,'itemprop="name">','<')
		track  = str(track).replace("['","").replace("']","").replace('&#39;',"'").replace("'","").replace('"','')
		if 'BBCL' in description:
			url = 'bbc+radio+1+live+lounge %s %s'%(artist,track)
		else:
			url    = '%s %s'%(artist,track)
		url    = str(url).replace(' ','-').replace(':','').lower()
		addDir('%s - %s'%(artist,track),'http://woodmp3.net/mp3.php?q='+url,63,icon,fanart,'')
		

   
def discogindex(url):
	open = OPEN_URL(url)
	log(open)
	all  = re.compile('"description".+?title".+?"(.+?)".+?thumbnail".+?"(.+?)".+?file.+?id".+?"(.+?)"',re.DOTALL|re.MULTILINE).findall(open)
	for name,icon,url in all:
		addDir(name,url,63,icon,fanart,'')

	
	
	

		
def regex_from_to(text, from_string, to_string, excluding=True):
	if excluding:
		try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r


def regex_get_all(text, start_with, end_with):
	r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
	return r


def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+url+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
	liz.setProperty('fanart_image', fanart)
	if mode==3 or mode==7 or mode==117 or mode==17 or mode==15 or mode==113 or mode==23 or mode==30 or mode==27 or mode ==36 or mode==39 or mode==97 or mode==46 or mode==50 or mode==53 or mode==55 or mode==57 or mode==60 or mode==104 or mode==62 or mode ==75 or mode==80 or mode==90 or mode==94 or mode==105 or mode==999:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==73 or mode==1000 or mode==118:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory


def OPEN_URL(url):
	headers = {}
	headers['User-Agent'] = User_Agent
	link = s.get(url, headers=headers, verify=False).text
	link = link.encode('ascii', 'ignore')
	return link
	
def sysinfo():
	import socket
	KODIV        = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
	RAM          = xbmc.getInfoLabel("System.Memory(total)")
	
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	IP = s.getsockname()[0]
			
	open  = requests.get('http://canyouseeme.org/').text
	ip    = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',open)
	EXTIP = str(ip.group())

	addDir('Kodi Version: %s'%KODIV,'url',200,icon,fanart,'')
	addDir('System Ram: %s'%RAM,'url',200,icon,fanart,'')
	addDir('Local IP Address: %s'%IP,'url',200,icon,fanart,'')
	addDir('External IP Address: %s'%EXTIP,'url',200,icon,fanart,'')

	
def playf4m(url, name):
                if not any(i in url for i in ['.f4m', '.ts', '.m3u8']): raise Exception()
                ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
                if not ext: ext = url
                if not ext in ['f4m', 'ts', 'm3u8']: raise Exception()

                params = urlparse.parse_qs(url)

                try: proxy = params['proxy'][0]
                except: proxy = None

                try: proxy_use_chunks = json.loads(params['proxy_for_chunks'][0])
                except: proxy_use_chunks = True

                try: maxbitrate = int(params['maxbitrate'][0])
                except: maxbitrate = 0

                try: simpleDownloader = json.loads(params['simpledownloader'][0])
                except: simpleDownloader = False

                try: auth_string = params['auth'][0]
                except: auth_string = ''


                try:
                   streamtype = params['streamtype'][0]
                except:
                   if ext =='ts': streamtype = 'TSDOWNLOADER'
                   elif ext =='m3u8': streamtype = 'HLS'
                   else: streamtype = 'HDS'

                try: swf = params['swf'][0]
                except: swf = None

                from F4mProxy import f4mProxyHelper
                f4mProxyHelper().playF4mLink(url, name, proxy, proxy_use_chunks, maxbitrate, simpleDownloader, auth_string, streamtype, False, swf)
				
def showpremiumimage():
	premium_jpg = xbmc.translatePath(os.path.join('special://home/addons/script.module.sportsvod/resources/premium', 'premium_image.jpg'))
	xbmc.executebuiltin('ShowPicture('+premium_jpg+')')
	return False
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None
# OpenELEQ: query & type-parameter (added 2 lines above)

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass
try:
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass
# OpenELEQ: query & type-parameter (added 8 lines above)

if mode==None or url==None or len(url)<1:
	CAT()

elif mode==2:
	INDEX2(url)

elif mode==3:
	LINKS(url)

elif mode==6:
	EPIS(url)

elif mode==7:
	LINKS2(url,description)

elif mode==8:
	SEARCH(query,type)
# OpenELEQ: query & type-parameter (added to line above)

elif mode==9:
	GENRE(url)

elif mode==10:
	COUNTRY(url)

elif mode==11:
	YEAR(url)
	
elif mode==12:
	INDEX3(url)
	
elif mode==13:
	resolve(name,url,iconimage,description)
	
elif mode==19:
	putlockerhdread(url)
	
elif mode==15:
	putlockerhdplay(url)
	
elif mode==24:
	xxx(url)
	
elif mode==25:
	LiveTV()
	
elif mode==26:
	opencartooncrazy(url)
	
elif mode==27:
	resolvexxx(url)
	
elif mode==99:
	xxxgenre(url)
	
elif mode==30:
	resolvecartooncrazy(url,icon)
	
elif mode==31:
	xxxCAT()
	
elif mode==32:
	CartooncrazyList()
	
elif mode==33:
	listgenre(url)
	
elif mode==34:
	CartooncrazysubList(url)
	
elif mode==35:
	documentary(url)
	
elif mode==36:
	resolvedoc(url)
	
elif mode==37:
	MOV2CAT()
	
elif mode==43:
	wweopen(url)
	
elif mode==44:
	playwwe(url,description)
	
elif mode==45:
	wwepages(url)
	
elif mode==46:
	resolvetwentyfourseven(url,name)
	
elif mode==47:
	opentwentyfourseven(url)

elif mode==48:
	tvlist(url)

elif mode==49:
	TVREQUESTCAT()
	
elif mode==50:
	TVREQUESTCATPLAY(name,url,icon)

elif mode==51:
	toongetlist(url)
	
elif mode==52:
	toongeteps(url)
	
elif mode==53:
	toongetresolve(name,url)

elif mode==56:
	FAMILYCAT()

elif mode==57:
	disneymoviesresolve(url)
	
elif mode==58:
	disneymovies(url)
	
elif mode==59:
	playresolved(url)
	
elif mode==60:
	tvguidepick(name)

elif mode==61:
	setxxxpass()
	
elif mode==62:
	musicresolve(url)
	
elif mode==63:
	musicsearch(url)
	
elif mode==64:
	MUSICCAT()
	
elif mode==65:
	musicindex(url)
	
elif mode==66:
	bbcmusicresolve(name)
	
elif mode==67:
	bbcmusicindex(url)
	
elif mode==68:
	TOPMUSICAT()
	
elif mode==69:
	radio()
	
elif mode==70:
	UKNowMusic(url)
	
elif mode==71:
	UKNowMusic2(url,description)
	
elif mode==72:
	MUSICCOL()
	
elif mode==73:
	xbmc.executebuiltin('XBMC.RunScript(script.module.sportsvod)')
	
elif mode==74:
	kisscartoonindex(url)
	
elif mode==75:
	kisscartoonresolve(url)

elif mode==76:
	kisscartoongenre(url)
	
elif mode==77:
	FAMILYMOVIESCAT()
	
elif mode==78:
	kisscartoonyear(url)
	
elif mode==79:
	NOVAMOVIES(url)
	
elif mode==80:
	NOVAMOVIERESOLVE(url)

elif mode==81:
	NOVAMOVIESGENRE(url)
	
elif mode==82:
	NOVAMOVIESSEARCH()
	
elif mode==83:
	WORLDIPTVM3U(url)
	
elif mode==84:
	WORLDIPTV()
	
elif mode==85:
	EXABYTE()
	
elif mode==86:
	listEXABYTE(url)
	
elif mode==87:
	WORLDIPTVM3U2(url)
	
elif mode==88:
	WORLDIPTV2()

elif mode==89:
	listLIVEONLINETV247()
	
elif mode==90:
	playLIVEONLINETV247(url)
	
elif mode==91:
	 mobdro()
	 
elif mode==93:
	mobdrolist(url)
	
elif mode==94:
	mobdroplay(url)
	
elif mode==95:
	shadownet()
	
elif mode==96:
	shadownetchans(url)
	
elif mode==97:
	shadownetplay(url,description)

elif mode==98:
	xxxstars(url)
	
elif mode==99:
	setxxxpass()
	
elif mode==100:
	MovieCAT()
	
elif mode==101:
	ustreamixchans()
	
elif mode==102:
	ustreamixplay(url)
	
elif mode==103:
	arconaitv()
	
elif mode==105:
	sysinfo()
	
elif mode==106:
	jango()
	
elif mode==107:
	jangopopular()
	
elif mode==108:
	jangosongs(url)
	
elif mode==109:
	jangogenres(url)
	
elif mode==111:
	discogindex(url)
	
elif mode==112:
	footballreplays(url)
	
elif mode==113:
	footballreplaysget(url)
	
elif mode==114:
	footballhighlight()
	
elif mode==115:
	footballhighlight()
	
elif mode==116:
	fullmatchtv(url)
	
elif mode==117:
	rugbyget(url)
	
elif mode==118:
	xbmc.executebuiltin('Addon.OpenSettings(plugin.video.ProjectCypher)')
	sys.exit()
	xbmc.executebuiltin('Container.Refresh')
	
elif mode==200:
	xbmc.log('hello')
	
elif mode==999:
	liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Music', infoLabels={'Title': name, 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


elif mode==1000:
	url = str(url).replace('\t','').replace('\r','').replace('\n','').replace(' ','%20')
	try:
		playf4m(url,name)
	except:
		pass
		
elif mode==99999:
	if xbmcaddon.Addon('plugin.video.ProjectCypher').getSetting('Username') == "":
		d = xbmcgui.Dialog().yesno('[COLOR ffff0000][B]ProjectCypher Premium[/B][/COLOR]','Have You Donated And Would Like To Log-In?')
		if not d:
			showpremiumimage()
			sys.exit()
		else:
			from resources.premium import premium
			d = xbmcgui.Dialog().yesno('[COLOR ffff0000][B]ProjectCypher Premium[/B][/COLOR]','Great! You will need to enter your Login details in the Addons Settings','Would you like us to open the settings for you now?')
			if d:
				xbmcaddon.Addon('plugin.video.ProjectCypher').openSettings()
				premium.start('NEW')
			else:
				sys.exit()
	else:
		from resources.premium import premium
		try:premium.startupd()
		except:pass
		premium.start('NONE')
	
elif mode==999991:
	from resources.premium import premium
	premium.livecategory(url)
	
elif mode==999992:
	from resources.premium import premium
	premium.Livelist(url)
	
elif mode==999993:
	from resources.premium import premium
	premium.vod(url)
	
elif mode==999994:
	from resources.premium import premium
	premium.stream_video(url)
	
elif mode==999995:
	from resources.premium import premium
	premium.search()
	
elif mode==999996:
	from resources.premium import premium
	premium.accountinfo()
	
elif mode==999997:
	xbmc.executebuiltin('ActivateWindow(TVGuide)')
	
elif mode==9999910:
	from resources.premium import premium
	premium.addonsettings(url,description)
	
elif mode==9999912:
	from resources.premium import premium
	premium.catchup()
	
elif mode==9999913:
	from resources.premium import premium
	premium.tvarchive(name,description)
	
elif mode==9999914:
	from resources.premium import premium
	premium.footballguide()
	
elif mode==9999915:
	from resources.premium import premium
	premium.footballguidesearch(description)
	
elif mode==9999916:
	from resources.premium import premium
	premium.extras()

elif mode==9999917:
	from resources.premium import premium
	premium.tvguidesetup()
	
elif mode==9999918:
	from resources.premium import premium
	premium.editas()
	
elif mode==9999919:
	from resources.premium import premium
	premium.apkdownloads()
xbmcplugin.endOfDirectory(int(sys.argv[1]))