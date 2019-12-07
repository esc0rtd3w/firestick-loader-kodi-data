import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

PLUGIN='plugin.video.freeppv'
ADDON = xbmcaddon.Addon(id=PLUGIN)
ICON = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.freeppv', 'icon.png'))
streamUrl = 'http://zag.gs/free.xml'
    


def CATEGORIES():
    try:
        match =re.compile('<name>(.+?)</name.+?<link>(.+?)</link.+?<img>(.+?)</img.+?<desc>(.+?)</desc>',re.DOTALL).findall(get_html(streamUrl))
        if not match:
            EXIT()
        for name, link,icon,description  in match:
            if icon==' ':
                icon= ICON
            Fuck_YA_Granny(name,link+' timeout=15',icon,description)
    except:
        EXIT()

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')   
    xbmc.executebuiltin("Container.SetViewMode(503)")         
        
def get_html(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

    
        
def EXIT():
        dialog = xbmcgui.Dialog()
        dialog.ok("Free PPV", "Sorry The Plugin Will Only Work When There",'Is an Event On Please Come Again', "Courtesy of[COLOR yellow] www.offsidestreams.com[/COLOR]")
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    

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

def Fuck_YA_Granny(name,url,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels={'Title':name ,'Plot':description})
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok
        
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

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
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        CATEGORIES()
               
        
elif mode==200:
        PLAY_STREAM(name,url,iconimage,play,description)
        

else:
        #just in case mode is invalid 
        CATEGORIES()

               
xbmcplugin.endOfDirectory(int(sys.argv[1]))

