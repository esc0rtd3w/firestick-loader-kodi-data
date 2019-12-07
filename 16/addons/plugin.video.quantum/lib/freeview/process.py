import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, xbmcaddon, json, time

ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.quantum/')
USERDATA_PATH = xbmc.translatePath('special://home/userdata/addon_data')
ADDON_DATA = USERDATA_PATH + '/quantum/'
if not os.path.exists(ADDON_DATA):
    os.makedirs(ADDON_DATA)
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
Dialog = xbmcgui.Dialog()
addon_id = 'plugin.video.quantum'
ADDON = xbmcaddon.Addon(id=addon_id)
PATH = 'quantum'
VERSION = '0.0.1'
addon_resources = ADDON_PATH + 'scripts/'
favourites = ADDON_DATA + 'favourites'
if os.path.exists(favourites)==True:
    FAV = open(favourites).read()
else: FAV = []
dp = xbmcgui.DialogProgress()
addon_handle = int(sys.argv[1])
List = []
temp_file = ADDON_PATH + 'Temp.txt'
debug = ADDON.getSetting('debug')



def Menu(name,url,mode,iconimage,fanart,description,extra,showcontext=True,allinfo={}):
        if iconimage == '':
            iconimage = ICON
        elif iconimage == ' ':
            iconimage = ICON
        if fanart == '':
            fanart = FANART
        elif fanart == ' ':
            fanart = FANART
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(('Remove from quantum Favorites','XBMC.RunPlugin(%s?mode=12&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to quantum Favorites','XBMC.RunPlugin(%s?mode=11&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))		

		
def Play(name,url,mode,iconimage,fanart,description,extra,showcontext=True,allinfo={}):
        if iconimage == '':
            iconimage = ICON
        if fanart == '':
            fanart = FANART
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(('Remove from quantum Favorites','XBMC.RunPlugin(%s?mode=12&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to quantum Favorites','XBMC.RunPlugin(%s?mode=11&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok		
        xbmcplugin.endOfDirectory(int(sys.argv[1]))		
		
#===============================Favourites-----------Not sure whos code this is but credit due to them-------------------------------

def addon_log(string):
    if debug == 'true':
        xbmc.log("[addon.live.quantum-%s]: %s" %(addon_version, string))

def addFavorite(name,url,iconimage,fanart,mode,playlist=None,regexs=None):
        favList = []
        try:
            # seems that after
            name = name.encode('utf-8', 'ignore')
        except:
            pass
        if os.path.exists(favourites)==False:
            addon_log('Making Favorites File')
            favList.append((name,url,iconimage,fanart,mode,playlist,regexs))
            a = open(favourites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            addon_log('Appending Favorites')
            a = open(favourites).read()
            data = json.loads(a)
            data.append((name,url,iconimage,fanart,mode))
            b = open(favourites, "w")
            b.write(json.dumps(data))
            b.close()
		

def getFavorites():
        if os.path.exists(favourites)==False:
            favList = []
            addon_log('Making Favorites File')
            favList.append(('quantum Favourites Section','','','','','',''))
            a = open(favourites, "w")
            a.write(json.dumps(favList))
            a.close()        
        else:
			items = json.loads(open(favourites).read())
			total = len(items)
			for i in items:
				name = i[0]
				url = i[1]
				iconimage = i[2]
				try:
					fanArt = i[3]
					if fanArt == None:
						raise
				except:
					if ADDON.getSetting('use_thumb') == "true":
						fanArt = iconimage
					else:
						fanArt = fanart
				try: playlist = i[5]
				except: playlist = None
				try: regexs = i[6]
				except: regexs = None

				if i[4] == 0:
					Menu(name,url,'',iconimage,fanart,'','','fav')
					xbmcplugin.endOfDirectory(int(sys.argv[1]))
				else:
					Menu(name,url,i[4],iconimage,fanart,'','','fav')
					xbmcplugin.endOfDirectory(int(sys.argv[1]))
def rmFavorite(name):
        data = json.loads(open(favourites).read())
        for index in range(len(data)):
            if data[index][0]==name:
                del data[index]
                b = open(favourites, "w")
                b.write(json.dumps(data))
                b.close()
                break
        xbmc.executebuiltin("XBMC.Container.Refresh")
		
############################## FAVOURITES END ###############################
		
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
        
params=get_params()
url=None
name=None
iconimage=None
mode=None
description=None
extra=None
fav_mode=None

try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
    extra=urllib.unquote_plus(params["extra"])
except:
    pass
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
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
def Resolve(url): 
    play=xbmc.Player()
    import urlresolver
    try: play.play(url)
    except: pass

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = ''
    link = ''
    try: 
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    except: pass
    if link != '':
        return link
    else:
        link = 'Opened'
        return link

def setView(content, viewType):
	if content:
	    xbmcplugin.setContent(int(sys.argv[1]), content)
		
		

def resolve_playercore(url): 
    play=xbmc.Player(GetPlayerCore())
    import urlresolver
    try: play.play(url)
    except: pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Big_Resolve(url): 
    play=xbmc.Player(GetPlayerCore())
    import urlresolver
    try: play.play(url)
    except: pass
    from urlresolver import common
    dp = xbmcgui.DialogProgress()
    dp.create('LOADING','Opening %s Now'%(name))
    play=xbmc.Player(GetPlayerCore())
    url=urlresolver.HostedMediaFile(url).resolve() 
    if dp.iscanceled(): 
        print "[COLORblue]STREAM CANCELLED[/COLOR]" # need to get this part working    
        dialog = xbmcgui.Dialog()
        if dialog.yesno("[B]CANCELLED[/B]", '[B]Was There A Problem[/B]','', "",'Yes','No'):
            dialog.ok("Message Send", "Your Message Has Been Sent")
        else:
	         return
    else:
        try: play.play(url)
        except: pass
        try: ADDON.resolve_url(url) 
        except: pass 
        dp.close()
	
	
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
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

	
if mode==10:
    addon_log("getFavorites")
    getFavorites()
elif mode==11:
    addon_log("addFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,iconimage,fanart,fav_mode)
elif mode==12:
    addon_log("rmFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)
