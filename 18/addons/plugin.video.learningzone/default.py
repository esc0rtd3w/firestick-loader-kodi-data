import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os

addon_id        = 'plugin.video.learningzone'
baseurl         = 'https://www.thenewboston.com'
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def CATEGORIES():
        req = urllib2.Request(baseurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)
        for url,name in match:
                if not 'class' in name:
                        addDir(name,url,3,icon,isFolder=True)

def GETSUBJECT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\n','').replace('\t','').replace('  ','')
        print link
        response.close()
        match=re.compile('<i class="panel.+?"></i>(.+?)</h2>').findall(link)
        for name in match:
                if not 'Most Popular' in name:
                        addDir(name,url,1,icon,isFolder=True)
       
def GETCATS(name,url):
        name2=name
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\n','').replace('\t','').replace('  ','')
        response.close()
        data=re.compile('<div class="panel video-category-panel">(.+?)</div></div></div>').findall(link)
        for cats in data:
                if name2 in cats:
                        data=re.compile('<a href="(.+?)" class="list-group-item">(.+?)</a>').findall(cats)
                        for url,name in data:
                                try:name=name.split('<span class')[0]
                                except:pass
                                addDir(name,url,4,icon,isFolder=True)

def GETVIDS(name,url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\n','').replace('\t','').replace('  ','')
        response.close()
        data=re.compile('<a href="(.+?)" class="video-item"><span class="mm-text">(.+?)</span>').findall(link)
        for url,name in data:
                addDir(name,url,2,icon,isFolder=False)

def PLAYLINK(url,name):
        if 'a href=' in url:
                url=url+'"'
                url=re.compile('<a href="(.+?)"').findall(url)[-1]
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        ytid=re.compile('data-code="(.+?)"').findall(link)[0]
        playback_url = 'plugin://plugin.video.youtube/play/?video_id=%s' % ytid
        liz=xbmcgui.ListItem(str(name), iconImage="DefaultFolder.png", thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": str(name) } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	xbmc.Player().play(playback_url, liz, False)
                
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
 
def addDir(name,url,mode,iconimage,isFolder=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
        return ok
 
params=get_params(); url=None; name=None; mode=None; site=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
 
print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
 
if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETCATS(name,url)
elif mode==2: PLAYLINK(url,name)
elif mode==3: GETSUBJECT(url)
elif mode==4: GETVIDS(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
