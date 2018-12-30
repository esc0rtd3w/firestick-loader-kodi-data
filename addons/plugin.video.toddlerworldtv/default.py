import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os,urlresolver,json

addon_id = 'plugin.video.toddlerworldtv'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
base = 'https://www.googleapis.com/youtube/v3/search?key=AIzaSyAd-YEOqZz9nXVzGtn3KWzYLbLaajhqIDA&channelId=UCSWRu9m-HZANpMBBQuEf14g&part=snippet,id&order=date&maxResults=50'

def CATEGORIES():
        link = open_url(base)
        link=link.replace('\\','')
        match=re.compile('"videoId": "(.+?)".+?"title": "(.+?)"',re.DOTALL).findall(link)
        for vidid,title in match:
                img = 'https://i.ytimg.com/vi/'+vidid+'/default.jpg'
                addLink(title,vidid,2,img,fanart)
        xbmc.executebuiltin('Container.SetViewMode(500)')


def PLAY(name,url,iconimage):
        playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url     
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setPath(playback_url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
       
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

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

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
elif mode==2: PLAY(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

