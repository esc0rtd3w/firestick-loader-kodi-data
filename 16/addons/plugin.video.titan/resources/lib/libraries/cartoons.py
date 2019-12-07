import xbmc
import re,sys,urllib,urllib2,urlparse,base64,urlresolver,random,xbmcgui,xbmcplugin,os
import threading
addon_id = 'plugin.video.titan'

fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'art/animefan.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'art/anime.png'))

def CartoonDirectory():
    addDir2('Most Popular','http://animecrazy.eu/most-popular/',901,icon,fanart)
    addDir2('Most Recent','http://animecrazy.eu/most-recent/',901,icon,fanart)
    addDir2('Search >>','http://animecrazy.eu/most-recent/',903,icon,fanart)
    addDir2('[COLOR yellow]Section is under construction. some links may be unavailable[/COLOR]','http://animecrazy.eu/most-recent/','',icon,fanart)
def Animemovies(url, name):
    try:
        

        result = open_url(url)
		
        items = re.compile('<a title="(.+?)" href="(.+?)"><img src="(.+?)"').findall(result)
        item_next = re.compile('<td class="current">.+?</td><td><a href="(.+?)">').findall(result)
    except:
        return

    for name,url,image in items:
            url = "http://animecrazy.eu" + url
			
            addDir2(name,url,902,image,fanart)
    for url in item_next:
            url = "http://animecrazy.eu" + url
            addDir2('NEXT >>>',url,901,icon,fanart)


def GETLINKS_AnimeMovies(url,name,iconimage):
    original_name = name
    img = iconimage
    link = open_url(url)
			
    match = re.compile('<li class="host-title">(.+?)</li><li class="nembed-link">\s*<a  title=".+?" target="_blank" href="(.+?)">').findall(link)
    match_iframe = re.compile('<a title="click here to watch" href="(.+?)">').findall(link)
    matchseries = re.compile('<a class="floatLeft"  href="(.+?)" title="(.+?)"').findall(link)
    for name,url in match:
		url = "http://animecrazy.eu" + url
		addDir2(name + " - " + original_name,url,904,img,fanart)
    for url,name in matchseries:
		url = "http://animecrazy.eu" + url
		addDir2(name,url,902,img,fanart)
    for url in match_iframe:
		addDir2('(Play) ' + original_name,url,904,img,fanart)
		
def Redirect_link(url,name,iconimage):
	original_name = name
	img = iconimage
	
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.geturl()
	stream_url = urlresolver.HostedMediaFile(link).resolve()
	liz=xbmcgui.ListItem(name, iconImage=img, thumbnailImage=img); liz.setInfo( type="Video", infoLabels={ "Title": original_name } )
	xbmc.Player ().play(stream_url,liz,False)
	addDir2('Press Back to Exit','',901,img,fanart)

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
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage='')
        
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
def open_url(url):
        # url=url.replace(' ','%20')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Anime')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','%20')
    if len(search_entered)>1:
     try:
    	url = 'http://animecrazy.eu/search/' + search_entered + "-page-1"
        Animemovies(url,name)
		
     except: pass
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


if mode==901: Animemovies(url,name)
elif mode==902: GETLINKS_AnimeMovies(url,name,iconimage)
elif mode==903: SEARCH()
elif mode==904: Redirect_link(url,name,iconimage)