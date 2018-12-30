import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,datetime,os
def CATEGORIES():
        url = 'http://www.failarmy.com'
        link = OPEN_URL(url)
        match=re.compile('<li data-tag="(.+?)"><figure><a href="(.+?)"><div class="img"><img src="(.+?)"').findall(link)
        for name,url,image in match:
            addDir('[UPPERCASE]%s[/UPPERCASE]'%name,'http://www.failarmy.com%s'%url,1,image)

def failarmy(url):
        link = OPEN_URL(url)
        match=re.compile('<a href="/video/(.+?)/.+?"><div class="img"><img src="(.+?)" alt="(.+?)"><span class="time">(.+?)</span>').findall(link)
        for url,image,name,time in match:
            addDir2('%s - %s'%(name,time),'http://makerplayer.com/embed/failarmy/%s?maker=1&autoplay=true&no_postroll=true&embed_params=brandlink=http://www.failarmy.com&brandname=Fail'%url,2,image)
def failarmy2(url):
        link = OPEN_URL(url)
        match=re.compile('file":"(.+?)"').findall(link)
        for url in match:
            dp = xbmcgui.DialogProgress()
            dp.create('Featching Your Video','Opening')
            play=xbmc.Player(GetPlayerCore())
            play.play(url)
def OPEN_URL(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent' , "Magic Browser")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def GetPlayerCore(): 
    try: 
        PlayerMethod=getSet("core-player") 
        if   (PlayerMethod=='DVDPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_DVDPLAYER 
        elif (PlayerMethod=='MPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_MPLAYER 
        elif (PlayerMethod=='PAPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_PAPLAYER 
        else: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    except: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    return PlayerMeth 
    return True 

def Search(name):
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter '+str(name))
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_entered = keyboard.getText().replace(' ','%20')
            if search_entered == 0:
                return False          
        return search_entered
        if search_entered == None:
            return False   

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

def addSearch():
	searchStr = ''
	keyboard = xbmc.Keyboard(searchStr, 'Search')
	keyboard.doModal()
	if (keyboard.isConfirmed()==False):
	  return
	searchStr=keyboard.getText()
	if len(searchStr) == 0:
	  return
	else:
	  return searchStr
	  
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addDir2(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
      
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
    failarmy(url)
elif mode==2:
    failarmy2(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
