import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time


PLUGIN='plugin.video.disneyjunior'
ADDON = xbmcaddon.Addon(id=PLUGIN)


VIDEO='http://www.disney.co.uk:80/cms_res/disney-junior/video/'

def CATEGORIES():
            url='http://disneyjunior.disney.co.uk/watch?b=mch'
            link=OPEN_URL(url)
            match=re.compile('details_visibility":"show.+?"title":"(.+?)","photo":"(.+?)".+?"href":"(.+?)"').findall(link)
            for name,iconimage ,url in match:
                addDir(name,url,1,iconimage,'')
            setView('movies', 'default') 
       
       
                                                                      
def second_catergory(name,url):
    print  url
    link=OPEN_URL(url)
    link=link.split('"title":"')
    for p in link:
        try:
            title=p.split('"')[0]            
            url=re.compile('"embedURL":"(.+?)"').findall(p)[0]            
            iconimage=re.compile('"thumb":"(.+?)"').findall(p)[0]            
            description=re.compile('"description":"(.+?)"').findall(p)[0]
            SHOWME=re.compile('"ptitle":"(.+?)"').findall(p)[0]
            if name in SHOWME:
                addDir(title,url,2,iconimage,description)
        except:pass     
    setView('movies', 'default') 
    
    
def playvideo(name,url,iconimage,description):
    r='"mp4".+?".+?"url":"(.+?)"}'
    link=OPEN_URL(url)
    match=re.compile(r).findall(link)
    amount = len(match)-1
    URL=match[amount]
    print URL
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
    liz.setProperty("IsPlayable","true")
    liz.setPath(URL)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
    
    
    
def playall(name,url):
    dp = xbmcgui.DialogProgress()
    dp.create("Disney Junior",'Creating Your Playlist')
    dp.update(0)
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()

    response=OPEN_URL(url)
    link=response.split('"title":"')
    test=re.compile('"embedURL":"(.+?)"').findall(response)

    playlist = []
    nItem    = len(test)
    try:
        for p in link:
          try:
            title=p.split('"')[0]            
            newurl=re.compile('"embedURL":"(.+?)"').findall(p)[0]            
            iconimage=re.compile('"thumb":"(.+?)"').findall(p)[0]            
            description=re.compile('"description":"(.+?)"').findall(p)[0]
            SHOWME=re.compile('"ptitle":"(.+?)"').findall(p)[0]       
            if name in SHOWME:        
                liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
                liz.setInfo( type="Video", infoLabels={ "Title": title} )
                liz.setProperty("IsPlayable","true")

                r='"mp4".+?".+?"url":"(.+?)"}'
                html=OPEN_URL(newurl)
                match = re.compile(r).findall(html)
                amount = len(match)-1
                URL=match[amount]
                playlist.append((URL ,liz))
        
                progress = len(playlist) / float(nItem) * 100  
                dp.update(int(progress), 'Adding to Your Playlist',title)

                if dp.iscanceled():
                    return
          except:pass
        dp.close()
    
        print 'THIS IS PLAYLIST====   '+str(playlist)
                
        for blob ,liz in playlist:
            try:
                if blob:
                    print blob
                    pl.add(blob,liz)
            except:
                pass

        if not xbmc.Player().isPlayingVideo():
	    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
    except:
        raise
        dialog = xbmcgui.Dialog()
        dialog.ok("Disney Junior", "Sorry Get All Valid Urls", "Why Not Try A Singular Video") 
        


         
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
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

def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description} )
        menu = []
        if not mode==2 and not mode==2000:
            forurl=urllib.quote(url)
            menu.append(('Play All Videos','XBMC.RunPlugin(%s?name=%s&mode=200&iconimage=None&description=None&url=%s)'% (sys.argv[0],name,forurl)))
            liz.addContextMenuItems(items=menu, replaceItems=True)
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            liz.setProperty("IsPlayable","true")
            xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
 
        
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
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
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        second_catergory(name,url)
        
elif mode==2:
        playvideo(name,url,iconimage,description)
        
elif mode==200:
        playall(name,url)
        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
