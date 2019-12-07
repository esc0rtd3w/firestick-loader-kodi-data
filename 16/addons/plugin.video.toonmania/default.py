import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os,net,json,urlparse
from common_addon import Addon

addon_id = 'plugin.video.toonmania'
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
art = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/', ''))

net = net.Net()
header={'User-Agent':'okhttp/2.3.0',
         'App-LandingPage':'http://www.mobi24.net/toon.html',
         'App-Name':'#Toonmania',
         'Connection':'Keep-Alive',
         'Host':'api.animetoon.tv',
         'App-Version':'7.7'}

def CATEGORIES():
        addDir('New Movies','http://api.animetoon.tv/GetNewMovies',1,icon,fanart)
        addDir('All Movies','http://api.animetoon.tv/GetAllMovies',1,icon,fanart)
        addDir('Popular Movies','http://api.animetoon.tv/GetPopularMovies',1,icon,fanart)
        addDir('New Cartoons','http://api.animetoon.tv/GetNewCartoon',1,icon,fanart)
        addDir('All Cartoons','http://api.animetoon.tv/GetAllCartoon',1,icon,fanart)
        addDir('Popular Cartoons','http://api.animetoon.tv/GetPopularCartoon',1,icon,fanart)
        addDir('New Dubbed','http://api.animetoon.tv/GetNewDubbed',1,icon,fanart)
        addDir('All Dubbed','http://api.animetoon.tv/GetAllDubbed',1,icon,fanart)
        addDir('Popular Dubbed','http://api.animetoon.tv/GetPopularDubbed',1,icon,fanart)
               
def EPISODES1(name,url,iconimage):
        link=net.http_GET(url,headers=header).content
        data=json.loads(link)
        for item in data:
                name=cleanHex(item['name'])
                id=cleanHex(item['id'])
                description=cleanHex(item['description'])
                iconimage = 'http://www.animetoon.tv/images/series/big/'+item['id']+'.jpg'
                addDir(name,id,3,iconimage,fanart,description)

def EPISODES2(name,url,iconimage):
        imgid=url
        link = net.http_GET('http://api.animetoon.tv/GetDetails/'+url,headers=header).content
        id2 = re.compile('"id":"(.+?)"').findall(link)#THERE IS MORE THAN 1 ID
        i=0
        for num in id2:      
                link = net.http_GET('http://api.animetoon.tv/GetVideos/'+num,headers=header).content
                links = re.compile('"(.+?)"').findall(link.replace('\/','/'))
                for link in links:
                        if 'videozoo.me' in link:
                                i=i+1
                                addLink(name+ ' - Part '+str(i),link,2,iconimage,fanart)
        
def PLAYDOCS(name,url,iconimage):
        link = net.http_GET(url).content
        try: url=re.compile('file: "(.+?)"').findall(link)[-1]
        except: url=re.compile('src: "(.+?)"').findall(link)[-1]
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        liz.setPath(url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))
       
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

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&iconimage="+str(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&iconimage="+str(iconimage)
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

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON2.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON2.getSetting(viewType) )

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
try: description=str(params["description"])
except: pass

print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name); print "IconImage: "+str(iconimage)
print params

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: EPISODES1(name,url,iconimage)
elif mode==2: PLAYDOCS(name,url,iconimage)
elif mode==3: EPISODES2(name,url,iconimage)
elif mode==4: QUEUE(name,url,iconimage)


xbmcplugin.endOfDirectory(int(sys.argv[1]))

