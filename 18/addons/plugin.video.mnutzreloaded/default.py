import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,urlparse,random
from t0mm0.common.addon import Addon
from metahandler import metahandlers

from resources.lib.libraries import client
from resources.lib.resolvers import googleplus

addon_id = 'plugin.video.mnutzreloaded'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

metaset = selfAddon.getSetting('enable_meta')
addon = Addon(addon_id, sys.argv)

def CATEGORIES():
        
        addDir2('[COLOR gold]Latest Movies[/COLOR]','https://afdah.org/recent_movies?page=1',1,icon,fanart)
        addDir2('[COLOR gold]Most Watched[/COLOR]','https://afdah.org/most_viewed?page=1',1,icon,fanart)
        addDir2('[COLOR green]Genres[/COLOR]','https://afdah.org/most_watched_movies?page=1',2,icon,fanart)
        addDir2('[COLOR green]Year[/COLOR] (1998-2015)','https://afdah.org/most_viewed?page=1',4,icon,fanart)

        addDir2('Search','https://afdah.org/most_watched_movies?page=1',3,icon,fanart)
def GENRES():
        
        addDir2('Action','https://afdah.org/action_movies?page=1',1,icon,fanart)
        addDir2('Animation','https://afdah.org/animation_movies?page=1',1,icon,fanart)
        addDir2('Comedy','https://afdah.org/comedy_movies?page=1',1,icon,fanart)
        addDir2('Adventure','https://afdah.org/adventure_movies?page=1',1,icon,fanart)
        addDir2('Sci-Fi','https://afdah.org/sci-fi_movies?page=1',1,icon,fanart)
        addDir2('Thriller','https://afdah.org/thriller_movies?page=1',1,icon,fanart)
        addDir2('Documentary','https://afdah.org/documentary_movies?page=1',1,icon,fanart)
        addDir2('Family','https://afdah.org/family_movies?page=1',1,icon,fanart)
        addDir2('History','https://afdah.org/history_movies?page=1',1,icon,fanart)
        addDir2('Crime','https://afdah.org/crime_movies?page=1',1,icon,fanart)
        addDir2('Drama','https://afdah.org/drama_movies?page=1',1,icon,fanart)
        addDir2('Fantasy','https://afdah.org/fantasy_movies?page=1',1,icon,fanart)
        addDir2('Horror','https://afdah.org/horror_movies?page=1',1,icon,fanart)
        addDir2('Music','https://afdah.org/music_movies?page=1',1,icon,fanart)
        addDir2('Mystery','https://afdah.org/mystery_movies?page=1',1,icon,fanart)
        addDir2('Romance','https://afdah.org/romance_movies?page=1',1,icon,fanart)
        addDir2('War','https://afdah.org/war_movies?page=1',1,icon,fanart)
        addDir2('Western','https://afdah.org/western_movies?page=1',1,icon,fanart)

		

def GETYEAR(url,name):
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'Input Year (1998-2015)')
        keyboard.doModal()
        if keyboard.isConfirmed(): search_entered = keyboard.getText().replace(' ','')
        base_link_2 = 'https://afdah.org'
        url = base_link_2 + "/" + search_entered + "_movies?page=1"
	try:
			
			basepage=url.split('?page=')
			
			curpage = int(basepage[1])
			nextpage = curpage + 1
			nextpageurl = basepage[0]+'?page='+str(nextpage)
	except:pass
        originalpage = open_url(url)
        metaset = selfAddon.getSetting('enable_meta')
        link = open_url(url)
        match=re.compile('<a title="(.+?)" href="(.+?)">.+?</a>').findall(link)
        for name,url in match:
                name=cleanHex(name)
				
                name=re.sub('Full Movie','',name)
                name=re.sub('HD 1080p','',name)
                name=re.sub('HD 720p','',name)
                name=re.sub('BluRay','',name)
                name=re.sub('-','',name)
                url= base_link_2 + url
                if metaset=='false':
                        try:
                                addDir(name,url,105,icon,len(match),isFolder=True)
                        except:pass
                else:
                        try:
                                addDir(name,url,105,icon,len(match),isFolder=True)
                        except:pass
	try:
                    
					
					addLink('NEXT>>',nextpageurl,1,icon,'')
					
	except: pass

def PLAYLINKAFDAH(name,url):
        moviename = name

        link = open_url(url)
        base_link_1 = 'https://afdah.org'
        
        search_link = '/results?q=%s'
        info_link = '/video_info'
        base_link = random.choice([base_link_1])
        url = urlparse.urljoin(base_link, url)

        result = client.source(url)

        video_id = re.compile('video_id *= *[\'|\"](.+?)[\'|\"]').findall(result)[0]
        post = urllib.urlencode({'video_id': video_id})

        result = client.source(urlparse.urljoin(base_link, info_link), post=post)

        u = [i for i in result.split('&') if 'google' in i][0]
        u = urllib.unquote_plus(u)
        u = [urllib.unquote_plus(i.split('|')[-1]) for i in u.split(',')]
        u = [googleplus.tag(i)[0] for i in u]
        u = [i for i in u if i['quality'] in ['1080p', 'HD']]
        for i in u:
		i['quality']=re.sub('HD','720p',i['quality'])
		
		 
		addLink(moviename + " - " + i['quality'],i['url'],101,icon,fanart)

def GETMOVIESAFDAH(url,name):
        base_link_2 = 'https://afdah.org'
	try:
			
			basepage=url.split('?page=')
			
			curpage = int(basepage[1])
			nextpage = curpage + 1
			nextpageurl = basepage[0]+'?page='+str(nextpage)
	except:pass
        originalpage = open_url(url)
        metaset = selfAddon.getSetting('enable_meta')
        link = open_url(url)
        match=re.compile('<a title="(.+?)" href="(.+?)">.+?</a>').findall(link)
        for name,url in match:
                name=cleanHex(name)
				
                name=re.sub('Full Movie','',name)
                name=re.sub('HD 1080p','',name)
                name=re.sub('HD 720p','',name)
                name=re.sub('BluRay','',name)
                name=re.sub('-','',name)
                url= base_link_2 + url
                if metaset=='false':
                        try:
                                addDir(name,url,105,icon,len(match),isFolder=True)
                        except:pass
                else:
                        try:
                                addDir(name,url,105,icon,len(match),isFolder=True)
                        except:pass
	try:
                    
					
					addLink('NEXT>>',nextpageurl,1,icon,'')
					
	except: pass						
	

	
	# ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH --------------------------------------------------------
 # ------------------------------------------------------- MEGA SEARCH -------------------------------------------------------- 
def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Movies')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
     try:
    	url = 'https://afdah.org/results?q=' + search_entered
        link = open_url(url)
        match=re.compile('<a title="(.+?)" href="(.+?)">.+?</a>').findall(link)
        for name,url in match:
                name=cleanHex(name)
                name=re.sub('Full Movie','',name)
                name=re.sub('HD 1080p','',name)
                name=re.sub('HD 720p','',name)
                name=re.sub('BluRay','',name)
                name=re.sub('-','',name)

                url= 'https://afdah.org/' + url
                addDir(name,url,105,icon,len(match),isFolder=True)
     except: pass


		
def PLAYMOVIE(name,url):
        # liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": name } )
     
        xbmc.Player().play(url)      # ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
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

def addDir2(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        liz.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
            liz.addContextMenuItems(contextMenuItems, replaceItems=True)
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
        
def open_url(url):
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

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==4: GETYEAR(url,name)
elif mode==3: SEARCH()
elif mode==2: GENRES()
elif mode==1: GETMOVIESAFDAH(url,name)
elif mode==101: PLAYMOVIE(name,url)
elif mode==105: PLAYLINKAFDAH(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

