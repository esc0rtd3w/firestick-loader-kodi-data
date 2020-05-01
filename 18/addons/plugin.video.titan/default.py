import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,urlparse,random
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from resources.lib.libraries import cache
from resources.lib.libraries import client
from resources.lib.libraries import cloudflare
from resources.lib.libraries import cartoons
import threading
hosts = ["https://archive.org/download/hifimoviesdocs/main_page.xml", "https://archive.org/download/NaviXPlaylist/playlist_mari.xml", "https://pastebin.com/raw/N43zpcjG"]
try: action = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))['action']
except: action = None
addon_id = 'plugin.video.titan'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
randomico = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/random1.png'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
icon2 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/mm.png'))
icon3 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/hifi.png'))
icon4 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/featured.png'))
icon5 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/jicon.png'))
icon6 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/g10icon.png'))
icon7 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/mari.png'))
icon8 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/featured2.png'))
fanarthifi = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/hifibe.jpg'))
fanartmm = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/mmbb.jpg'))
fanartm = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/dfanart.jpg'))
fanartfeatured2 = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/lo.jpg'))
searchicon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/search1.png'))
metaset = selfAddon.getSetting('enable_meta')
addon = Addon(addon_id, sys.argv)
livetv = ['.m3u8','.ts=','rtmp://','iptvnation']
HOME         =  xbmc.translatePath('special://home/')
EXCLUDE_HATER   = ['spartan','techtimeruu', 'spartanpixel' , 'beast', 'royalist','Spartanpixel','Spartan']
dialog = xbmcgui.Dialog()
def CATEGORIES():
	Check_haters()	
	addDir2('Featured Movies','https://archive.org/download/hifimoviesdocs/HdMovies.xml',21,icon8,fanartfeatured2)
	addDir2('M&Ms World','https://archive.org/download/NaviXPlaylist/playlist_mari.xml',6,icon2,fanartmm)
	addDir2('HiFi2007 World','https://archive.org/download/hifimoviesdocs/main_page.xml',10,icon3,fanarthifi)	
	
    
	addDir2('3D Movies','https://archive.org/download/hifimoviesdocs/3D.xml',6,icon7,fanartm)
	addDir2('Random 3 Picks','http://',102,randomico,fanart)
	addDir2('Search','http://titan',8,searchicon,fanart)
	xbmc.executebuiltin("Container.SetViewMode(500)")

def HIFI(name,url):
        Check_haters()
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('name=(.+?)\s*URL=(.+?)\n+player').findall(link)
        match2=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+player').findall(link)
        match3=re.compile('name=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match4=re.compile('name=(.+?)\s*thumb=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match5=re.compile('name=(.+?)\s*URL=(.+?)\s*thumb=(.+?)\n+player').findall(link)

        for name,url,thumb in match5:
			if "archive" in str(url):
				addDir2(name,url,10,thumb,fanarthifi)
			else:
				addLink(name,url,101,thumb,thumb)

        for name,thumb,url in match2:
			if "archive" in str(url):
				addDir2(name,url,10,thumb,fanarthifi)
			else:
				addLink(name,url,101,thumb,thumb)
        for name,thumb,date,url in match4:
			if "archive" in str(url):
				addDir2(name,url,10,thumb,fanarthifi)
			else:
				addLink(name,url,101,thumb,fanarthifi)
        for name,url in match:
			if "archive" in str(url):
				addDir2(name,url,10,icon3,fanarthifi)
			else:
				addLink(name,url,101,icon3,fanarthifi)
        for name,date,url in match3:
			if "archive" in str(url):
				addDir2(name,url,10,icon3,fanarthifi)
			else:
				addLink(name,url,101,icon3,fanarthifi)
def GETLINKSNEW(url,name,iconimage):
		numTries = 7
		host = 0
		urlorig = url
		originalname = name
		try:link = open_url(url)
		except:link = cloudflare.request(url, mobile=True)
		matchlink=re.compile('data-link="(.+?)">').findall(link)
		matchlink2=re.compile("<a style='.+?' href='(.+?)' target='_blank'").findall(link)
		for url in matchlink:
						host=url.split('/')[2].replace('www.','').capitalize()
						addLink(url,url,101,icon,'')
def GETLIVE(url,name):
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
       
        match=re.compile('name=(.+?)\s*thumb=(.+?)\s*date=(.+?)\s*URL=(.+?)\s*player=').findall(link)
        match2=re.compile('name=(.+?)\s*URL=(.+?)\s*player=').findall(link)
        for name,url in match2:
				addDir2(name,url,101,icon,'')
def GETSHOWS(url,name):
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('name=(.+?)\s*thumb=(.+?)\s*date=(.+?)\s*URL=(.+?)\s*player=').findall(link)
        match2=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\s*player=').findall(link)
        for name,thumb,date,url in match:
				addDir2(name,url,5,thumb,fanart)
        for name,thumb,url in match2:
				addDir2(name,url,5,thumb,fanart)
def GET_SEARCH_FOLDERS(url,name):
        Check_haters()
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match2=re.compile('name=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match3=re.compile('name=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match4=re.compile('name=(.+?)\s*thumb=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
        for name,thumb,url in match:
			if "archive" in str(url):
				addDir2(name,url,9,thumb,fanart)
			else:
				addLink(name,url,101,thumb,thumb)
        for name,url in match2:
			if "archive" in str(url):
				addDir2(name,url,9,icon,fanart)
			else:
				addLink(name,url,101,icon,fanart)
        for name,date,url in match3:
			if "archive" in str(url):
				addDir2(name,url,9,icon,fanart)
			else:
				addLink(name,url,101,icon,fanart)
        for name,thumb,date,url in match4:
			if "archive" in str(url):
				addDir2(name,url,9,thumb,fanart)
			else:
				addLink(name,url,101,thumb,fanart)
def GETEPISODES(url,name):
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match2=re.compile('name=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match3=re.compile('name=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match4=re.compile('name=(.+?)\s*thumb=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
        for name,thumb,url in match:
                name=re.sub(r'\.',r' ', name)
                addLink(name,url,101,thumb,thumb)
        for name,url in match2:
				addLink(name,url,101,icon,fanart)
        for name,date,url in match3:
				addLink(name,url,101,icon,fanart)
        for name,thumb,date,url in match4:
				addLink(name,url,101,thumb,fanart)		
def GETMM(url,name):
        Check_haters()
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match_random=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+random').findall(link)
        match=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match2=re.compile('name=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match3=re.compile('name=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match4=re.compile('name=(.+?)\s*thumb=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
        match5=re.compile('name=(.+?)\s*URL=(.+?)\s*thumb=(.+?)\s*player').findall(link)
        for name,thumb,url in match_random:
			addDir2(name,url,998,thumb,fanart)
        for name,thumb,url in match:
			if "archive" in str(url):
				addDir2(name,url,6,thumb,fanartmm)
			else:
				addLink(name,url,101,thumb,fanartmm)	
        for name,thumb,date,url in match4:
			if "archive" in str(url):
				addDir2(name,url,6,thumb,fanartmm)
			else:
				addLink(name,url,101,thumb,fanartmm)
        for name,url in match2:
			if "archive" in str(url):
				addDir2(name,url,6,icon2,fanartmm)
			else:
				addLink(name,url,101,icon2,fanartmm)	
        for name,date,url in match3:
			if "archive" in str(url):
				addDir2(name,url,6,icon2,fanartmm)
			else:
				addLink(name,url,101,icon2,fanartmm)
        for name,url,thumb in match5:
			if "archive" in str(url):
				addDir2(name,url,6,icon2,fanartmm)
			else:
				addLink(name,url,101,thumb,fanartmm)				
def PLAYMOVIE(name,url):
	if".m3u8" in url:
		addon.resolve_url(url)
	elif "iptvnation" in url:
		# try:link = open_url(url)
		# except:link = cloudflare.request(url, mobile=True)
		addon.resolve_url(url)
	elif ".ts=" in url:
		addon.resolve_url(url)
	elif "rtmp://" in url:
		addon.resolve_url(url)		
	elif "pompa1.nosvideo" in url:
		addon.resolve_url(url)	
	else:
		try:
			resolved=urlresolver.resolve(url)
			addon.resolve_url(resolved)
		except: 
			try:
				stream_url = urlresolver.HostedMediaFile(url).resolve()
				liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
				xbmc.Player ().play(stream_url,liz,False)
			except:
				try:
					from resources.lib import resolvers
					url = resolvers.request(url)
					addon.resolve_url(url)
				except: pass		
		addLink('Press back to exit','',1,icon,fanart)
    
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

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
def GETFEATURED(url,name):
        Check_haters()
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match2=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+player').findall(link)
        for name,thumb,url in match2: addLink(name,url,101,thumb,fanart)
        url2 = "https://archive.org/download/NaviXPlaylist/HD.xml"
        try:link2 = open_url(url2)
        except:link2 = cloudflare.request(url2, mobile=True)
        matchm=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+p').findall(link2)
        matchm2=re.compile('name=(.+?)\s*URL=(.+?)\n+p').findall(link2)
        matchm3=re.compile('name=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link2)
        matchm4=re.compile('name=(.+?)\s*thumb=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link2)
        for name,thumb,url in matchm:
                name=re.sub(r'\.',r' ', name)
                addLink(name,url,101,thumb,thumb)
        for name,url in matchm2:
				addLink(name,url,101,icon,fanart)
        for name,date,url in matchm3:
				addLink(name,url,101,icon,fanart)
        for name,thumb,date,url in matchm4:
				addLink(name,url,101,thumb,fanart)		
def fetch_random(url):
		link = open_url(url)
		try:
			matchm=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+p').findall(link)
			matchm4=re.compile('name=(.+?)\s*thumb=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
			for name,thumb,url in matchm: randomitem.append([name,thumb,url])
			for name,thumb,date,url in matchm4: randomitem.append([name,thumb,url])
		except: pass

def GETRANDOM(url,name):
		Check_haters()
		global randomitem ; randomitem = []
		randomurl = ["https://archive.org/download/hifimoviesdocs/HdMovies.xml", "https://archive.org/download/NaviXPlaylist/HD.xml"] 
		threads = [threading.Thread(target=fetch_random, args=(url,)) for url in randomurl]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()
		index = random.randrange(1, len(randomitem))
		index2 = random.randrange(1, len(randomitem))
		index3 = random.randrange(1, len(randomitem))
		name = randomitem[index][0]
		image = randomitem[index][1]
		url   = randomitem[index][2]
		name2 = randomitem[index2][0]
		image2 = randomitem[index2][1]
		url2   = randomitem[index2][2]
		name3 = randomitem[index3][0]
		image3 = randomitem[index3][1]
		url3  = randomitem[index3][2]
		addLink(name,url,101,image,fanart)
		addLink(name2,url2,101,image2,fanart)
		addLink(name3,url3,101,image3,fanart)
					
###### JOHNNY LISTS ##### NAMES SET TO URL FOR RESOLVERS CHECK
def GETJLIST(url,name):
	Check_haters()

	try:link = open_url(url)
	except:link = cloudflare.request(url, mobile=True)
	all_links = regex_get_all(link, '<channel>', '</channel>')
	for list in all_links:
		dir = regex_from_to(list, '<externallink>', '</externallink>')
		name = regex_from_to(list, '<name>', '</name>')
		url = regex_from_to(list, '<link>', '</link>')
		thumb = regex_from_to(list, '<thumbnail>', '</thumbnail>')
		if "ignore" in url:
			addDir2(name,dir,30,thumb,fanart)
		
	item_links = regex_get_all(link, '<item>', '</item>')
	for list in item_links:
		name = regex_from_to(list, '<title>', '</title>')
		url = regex_from_to(list, '<link>', '</link>')
		thumb = regex_from_to(list, '<thumbnail>', '</thumbnail>')
		if url:
			if "sublink" in url:
				addDir2(name,url,31,thumb,fanart)
			else:
				addLink(name,url,101,thumb,fanart)
	youtube_links = regex_get_all(link, '<item>', '</item>')
	for list in youtube_links:
		name = regex_from_to(list, '<title>', '</title>')
		url = regex_from_to(list, '<utube>', '</utube>')
		url = "https://www.youtube.com/watch?v=" + url
		thumb = regex_from_to(list, '<thumbnail>', '</thumbnail>')
		if url:
			if "sublink" in url:
				addDir2(name,url,31,thumb,fanart)
			else:
				addLink(name,url,101,thumb,fanart)


def fetch_url(url,global_search):
		link = open_url(url)
		try:
			match5=re.compile('name=(.+?)\s*URL=(.+?)\s*thumb=(.+?)\s*player').findall(link)
			match=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+p').findall(link)
			match2=re.compile('name=(.+?)\s*URL=(.+?)\n+p').findall(link)
			match3=re.compile('name=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
			match4=re.compile('name=(.+?)\s*thumb=(.+?)\s*date=(.+?)\s*URL=(.+?)\n+p').findall(link)
			for name,thumb,url in match:
					if str(global_search).title() in name.title():
						if "archive" in str(url):
							addDir2(name,url,9,thumb,fanart)
						else:
							addLink(name + " [COLOR blue]Hifi[/COLOR] - [COLOR purple]M&M[/COLOR]",url,101,thumb,fanart)
			for name,url in match2:
					if str(global_search).title() in name.title():
						if "archive" in str(url):
							addDir2(name,url,9,icon,fanart)
						else:
							addLink(name + " [COLOR blue]Hifi[/COLOR] - [COLOR purple]M&M[/COLOR]",url,101,icon,fanart)
			for name,date,url in match3:
					if str(global_search).title() in name.title():
						if "archive" in str(url):
							addDir2(name,url,9,icon,fanart)
						else:
							addLink(name + " [COLOR blue]Hifi[/COLOR] - [COLOR purple]M&M[/COLOR]",url,101,icon,fanart)
			for name,thumb,date,url in match4:
					if str(global_search).title() in name.title():
						if "archive" in str(url):
							addDir2(name,url,9,thumb,fanart)
						else:
							addLink(name + " [COLOR blue]Hifi[/COLOR] - [COLOR purple]M&M[/COLOR]",url,101,thumb,fanart)
			for name,thumb,date,url in match5:
					if str(global_search).title() in name.title():
						if "archive" in str(url):
							addDir2(name,url,9,thumb,fanart)
						else:
							addLink(name + " [COLOR blue]Hifi[/COLOR] - [COLOR purple]M&M[/COLOR]",url,101,thumb,fanart)
		except: pass
		try:
			item_links = regex_get_all(link, '<item>', '</item>')
			for list in item_links:
				name = regex_from_to(list, '<title>', '</title>')
				playurl = regex_from_to(list, '<link>', '</link>')
				thumb = regex_from_to(list, '<thumbnail>', '</thumbnail>')
				if playurl:
					if "sublink" in playurl:
						if str(global_search).title() in name.title():addDir2(name+"  [COLOR yellow]Midnight Society[/COLOR]",playurl,31,thumb,fanart)
					else:
						if str(global_search).title() in name.title():addLink(name+"  [COLOR yellow]Midnight Society[/COLOR]",playurl,101,thumb,fanart)				
		except: pass


def fetch_hosts(host):
	link = open_url(host)
	all_links = regex_get_all(link, '<channel>', '</channel>')
	for list in all_links:
		dir = regex_from_to(list, '<externallink>', '</externallink>')
		name = regex_from_to(list, '<name>', '</name>')
		url = regex_from_to(list, '<link>', '</link>')
		thumb = regex_from_to(list, '<thumbnail>', '</thumbnail>')
		if "pastebin" in url:
			global_fetch.append(url)
		elif "pastebin" in dir:
			global_fetch.append(dir)

	match=re.compile('name=(.+?)\s*URL=(.+?)\n+player').findall(link)
	match2=re.compile('name=(.+?)\s*thumb=(.+?)\s*URL=(.+?)\n+player').findall(link)
	for name,thumb,url in match2:
			if "archive.org" in url:
				global_fetch.append(url)
	for name,url in match:
			if "archive.org" in url:
				global_fetch.append(url)
def SEARCH(url,name):
	Check_haters()

	search_entered =''
	keyboard = xbmc.Keyboard(search_entered, 'Search Movie')
	keyboard.doModal()
	if keyboard.isConfirmed(): search_entered = keyboard.getText()
	if len(search_entered)>1:
		global global_search ; global_search = search_entered
		global global_fetch ; global_fetch = []
		threads_hosts = [threading.Thread(target=fetch_hosts, args=(host,)) for host in hosts]
		for thread in threads_hosts:
			thread.start()
		for thread in threads_hosts:
			thread.join()
		threads = [threading.Thread(target=fetch_url, args=(url,global_search)) for url in global_fetch]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()
		threads = [threading.Thread(target=fetch_url, args=(url,global_search)) for url in global_fetch]
		for thread in threads:
			thread.start()
		for thread in threads:
			thread.join()

def GetSublinks(name,url,iconimage,fanart):
    sources = []
    sname = []
    n = 0
    all_videos = regex_get_all(url, 'sublink:', '#')
    for a in all_videos:
		n = n+1
		vurl = a.replace('sublink:','').replace('#','')
		sources.append(vurl)
		sname.append(name+ ' Source ['+str(n)+']')
	
    dialog = xbmcgui.Dialog()
    index = dialog.select('Select a source:', sname)
    if index>-1:
			url=sources[index]
			try:
				from resources.lib import resolvers
				url = resolvers.request(url)
				xbmc.Player().play(url)
			except:
				try:
					resolved=urlresolver.resolve(url)
					addon.resolve_url(resolved)
				except:
					 stream_url = urlresolver.HostedMediaFile(url).resolve()
					 liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
					 xbmc.Player ().play(stream_url,liz,False)
		
			addLink('Press back to exit','',1,icon,fanart)
def PLAYGVIDEO(url,name,mode,iconimage):
	sources = []
	sname = []
	n = 0
	originalname = name
	fanart_image = iconimage
	if "sublink" in url:
		match = re.compile('<sublink>(.+?)</sublink>').findall(url)
		for list in match:
			n=n+1
			sources.append(list)
			sname.append(name+ ' Source ['+str(n)+']')
		dialog = xbmcgui.Dialog()
		index = dialog.select('Select a source:', sources)
		if index>-1:
			link=sources[index]
			stream_url = urlresolver.HostedMediaFile(link).resolve()
			liz=xbmcgui.ListItem(name, iconImage=fanart_image, thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": originalname } )
			xbmc.Player ().play(stream_url,liz,False)
	else:		
		try:
			name=selfAddon.getSetting('namestore')
			resp = urllib2.urlopen(url)
			url2 = resp.geturl()
			stream_url = urlresolver.HostedMediaFile(url2).resolve()
			liz=xbmcgui.ListItem(name, iconImage=fanart_image, thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": originalname } )
			xbmc.Player ().play(stream_url,liz)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
		except:
			liz=xbmcgui.ListItem(name, iconImage=fanart_image, thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": originalname } )
			xbmc.Player ().play(url)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	addLink("Press Back to exit",url,'',icon,fanart)		
def addDir2(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addLink(name,url,mode,iconimage,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def addDir(name,url,mode,iconimage,itemcount,isFolder=False):
        try:
          if not 'COLOR' in name:
            splitName=name.partition('(')
            simplename=""
            simpleyear=""
            if len(splitName)>0:
                simplename=splitName[0]
                simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
            mg = metahandlers.MetaData()
            meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
            liz.setInfo( type="Video", infoLabels= meta )
            liz.setProperty("IsPlayable","true")
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=False)
            if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
            else: liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
            return ok
        except:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
            return ok
def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r				

def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
	   try: r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
	   except: r = ''
    else:
       try: r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
       except: r = ''
    return r        
def open_url(url):
        # url=url.replace(' ','%20')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
print params
def Check_haters():
		safe_to_go = 0
		name = "plugin.video.titan"
		import shutil
		for root, dirs, files in os.walk(HOME,topdown=True):
				if "spartan" in str(dirs):
					dialog.ok('[COLOR lime][B]Titan[/B][/COLOR][COLOR white] Autodetect[/COLOR] ','Titan addon doesnt support scammers and dishonest reviewers... If you have installed anything related to spartanpixel this addon will not work for you, and you should use a different build, plenty of free build out there','','')
					for dir in dirs:
						shutil.rmtree(os.path.join(root,name))
				if "techtimeruu" in str(dirs):
					dialog.ok('[COLOR lime][B]Titan[/B][/COLOR][COLOR white] Autodetect[/COLOR] ','Titan addon doesnt support scammers and dishonest reviewers... If you have installed anything related to spartanpixel this addon will not work for you, and you should use a different build, plenty of free build out there','','')
					for dir in dirs:
						shutil.rmtree(os.path.join(root,name))
				if "techtimeru" in str(dirs):
					dialog.ok('[COLOR lime][B]Titan[/B][/COLOR][COLOR white] Autodetect[/COLOR] ','Titan addon doesnt support scammers and dishonest reviewers... If you have installed anything related to spartanpixel this addon will not work for you, and you should use a different build, plenty of free build out there','','')
					for dir in dirs:
						shutil.rmtree(os.path.join(root,name))
				if "techtimeruuu" in str(dirs):
					dialog.ok('[COLOR lime][B]Titan[/B][/COLOR][COLOR white] Autodetect[/COLOR] ','Titan addon doesnt support scammers and dishonest reviewers... If you have installed anything related to spartanpixel this addon will not work for you, and you should use a different build, plenty of free build out there','','')
					for dir in dirs:
						shutil.rmtree(os.path.join(root,name))					
				if "spartanpixel" in str(dirs):
					dialog.ok('[COLOR lime][B]Titan[/B][/COLOR][COLOR white] Autodetect[/COLOR] ','Titan addon doesnt support scammers and dishonest reviewers... If you have installed anything related to spartanpixel this addon will not work for you, and you should use a different build, plenty of free build out there','','')
					for dir in dirs:
						shutil.rmtree(os.path.join(root,name))		

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==3: GETSHOWS(url,name)
elif mode==4: GETLIVE(url,name)
elif mode==5: GETEPISODES(url,name)
elif mode==6: GETMM(url,name)

elif mode==8: SEARCH(url,name)
elif mode==9: GET_SEARCH_FOLDERS(url,name)
elif mode==10: HIFI(name,url)

elif mode==101: PLAYMOVIE(name,url)
elif mode==102: GETRANDOM(url,name)
elif mode==21: GETFEATURED(url,name)
elif mode==30: GETJLIST(url,name)
elif mode==31: GetSublinks(name,url,iconimage,fanart)
elif mode == 999: cartoons.CartoonDirectory()
elif mode == 998: 
	from resources.lib.libraries import titanlive
	titanlive.randomtv(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

