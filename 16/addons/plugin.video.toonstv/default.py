import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os
addon_id        = 'plugin.video.toonstv'
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'fanart.jpg'))

def GETCHANNELS():
        link=open_url('https://www.toons.tv/')
        match=re.compile('style="background-image\:url\(\&quot\;(.+?)\&quot\;\)\;"><a href="(.+?)"').findall(link)[9:]
        match.sort()
        for iconimage,url in match:
                url='https://www.toons.tv'+url
                name=url.split('/')[4].replace('_',' ')
                if 'channels' in url:
                        addDir(name,url,1,iconimage,fanart,isFolder=True)
        xbmc.executebuiltin('Container.SetViewMode(500)') 


def GETEPISODES(name,url,iconimage):
        link=open_url(url)
        link=link.replace('&quot;','')
        match=re.compile('background-image\:url\((.+?)\)\;font-size\:24px\;"><div class="video-panel__overlay"><a href="(.+?)"').findall(link)
        for iconimage,url in match:
                if 'url(' in iconimage:
                        iconimage=iconimage.split('url(')[1]
                url='https://www.toons.tv'+url
                if 'channels' in url:
                        addDir(name,url,2,iconimage,fanart,isFolder=False)
        xbmc.executebuiltin('Container.SetViewMode(500)') 

                            
def PLAYLINK(url,name,iconimage):
        link=open_url(url)
        match=re.compile('"url":"(.+?)"').findall(link)
        links=[]
        for url in match:
                if '.mp4' in url:
                        links.append(url)
        url=links[-1]
        liz=xbmcgui.ListItem(str(name), iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo( type="Video", infoLabels={ "Title": str(name) } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	xbmc.Player().play(url, liz, False)

def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
                
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
 
def addDir(name,url,mode,iconimage,fanart,isFolder=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
        return ok
 
params=get_params(); url=None; name=None; mode=None; site=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: mode=int(params["mode"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
 
print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
 
if mode==None or url==None or len(url)<1: GETCHANNELS()
elif mode==1: GETEPISODES(name,url,iconimage)
elif mode==2: PLAYLINK(url,name,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
