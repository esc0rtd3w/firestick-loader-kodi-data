import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys
from resources.libs.common_addon import Addon

addon_id        = 'plugin.video.NJMSOCCER'
addon           = Addon(addon_id, sys.argv)
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def Index():
        GetLinks('https://dl.dropboxusercontent.com/s/9n106bmhlbc56ct/soccerpublic.plx')

def GetLinks(url):
        link = open_url(url)
        link = link.replace('\n','').replace('#','##')
        try:
                fanart=re.compile('background=(.+?)logo').findall(link)[0]
        except:
                fanart=re.compile('background=(.+?)thumb').findall(link)[0]
        match=re.compile('#.+?#',re.DOTALL).findall(link)
        for item in match:
                match=re.compile('type=playlistthumb=(.+?)name=(.+?)URL=(.+?)#').findall(item) 
                for thumb,name,url in match:
                        addDir(name,url,1,thumb,fanart)
                match=re.compile('type=videoname=(.+?)thumb=(.+?)URL=(.+?)#').findall(item) 
                for name,thumb,url in match:
                        addLink(name,url,3,thumb,fanart)

def PLAYLINK(url,iconimage):
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
            try:
                xbmc.Player ().play(url, liz, False)
                return ok
            except:
                pass
            
def TWITTER():
        text = ''
        twit = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?588677963413065728'
        link = open_url(twit)
        link = link.replace('/n','')
        link = link.decode('utf-8').encode('utf-8').replace('&#39;','\'').replace('&#10;',' - ').replace('&#x2026;','')
        match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
        for status, dte in match:
            try:
                            status = status.decode('ascii', 'ignore')
            except:
                            status = status.decode('utf-8','ignore')
            dte = dte[:-15]
            status = status.replace('&amp;','')
            dte = '[COLOR blue][B]'+dte+'[/B][/COLOR]'
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('[COLOR blue][B]@uk_turk[/B][/COLOR]', text)

def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass
                                     
def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link = link.replace('\r','').replace('\t','').replace('&nbsp;','').replace('\'','')
        response.close()
        return link

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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

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
 
if mode==None or url==None or len(url)<1: Index()
elif mode==1:GetLinks(url)
elif mode==3:PLAYLINK(url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
