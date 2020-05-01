import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='http://mega-tron.tv/fistsofury/'
addon=xbmcaddon.Addon(id='plugin.video.fistsofury')
    
VERSION = "1.6"
PATH = "Fists-O-Fury"

#########################################################################################################################################################
skinspath  =  xbmc.translatePath(os.path.join('special://home','addons','plugin.video.fistsofury','resources','skins'))
furypath  =  xbmc.translatePath(os.path.join('special://home','addons','plugin.video.fistsofury'))
dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()

fanart_background = xbmc.translatePath(os.path.join(furypath,'fanart.jpg'))
install_icon = xbmc.translatePath(os.path.join(skinspath,'install.png'))
wipe_icon = xbmc.translatePath(os.path.join(skinspath,'wipe.png'))
help_icon = xbmc.translatePath(os.path.join(skinspath,'help.png'))
#########################################################################################################################################################

if addon.getSetting('ask')=='false':
    if not dialog.yesno("[COLOR red]WARNING: Explicit adult material[/COLOR]","[COLOR white]You may enter only if you are [COLOR yellow]at least 18 years of age or [CR]at least the legal age [/COLOR][COLOR white]in the jurisdiction you reside or [CR]from which you access this content.[/COLOR]","","","Exit","Enter"):
        addon.setSetting('ask','false')
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(home)")
addon.setSetting('ask','true')

def CATEGORIES():
    addDir('Install','http://mega-tron.tv/fistsofury/tissuebox.zip',1,install_icon,fanart_background,'Install addons and repos.')
    if addon.getSetting('wipe')=='true':
        addDir('Wipe','http://mega-tron.tv/fistsofury/',2,wipe_icon,fanart_background,'Completely wipe Fists-O-Fury addons/repos.')
    if not addon.getSetting('wipe')=='true':
        addDir('Wipe','http://mega-tron.tv/fistsofury/',3,wipe_icon,fanart_background,'Completely wipe Fists-O-Fury addons/repos.')
    addDir('Help','http://mega-tron.tv/fistsofury/',4,help_icon,fanart_background,'Help make Fists-O-Fury better.')
    setView('movies', 'MAIN')
    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def wizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp.create("[COLOR red]Attention[/COLOR]","[COLOR yellow]Downloading... [/COLOR]",'', 'Please wait...')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "[COLOR blue]Installing...[/COLOR]")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    xbmc.sleep(200)
    xbmc.executebuiltin('UpdateLocalAddons()')
    stringslink=OPEN_URL('http://mega-tron.tv/fistsofury/strings.txt')
    strings=re.compile('string="(.+?)"').findall(stringslink)
    for stringname in strings:
        query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true},"id":1}' % (stringname)
        xbmc.executeJSONRPC(query)
        xbmc.sleep(200);
    addon.setSetting('wipe','true')
    xbmc.executebuiltin('UpdateAddonRepos()')
    dp.close()
    dialog.ok("[COLOR red]Attention [/COLOR]","[CR][COLOR yellow]Install complete. Grab a box of [COLOR blue]Kleenex[/COLOR] and enjoy![/COLOR]")

def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def setSetting(setting, value):
    setting = '"%s"' % setting

    if isinstance(value, list):
        text = ''
        for item in value:
            text += '"%s",' % str(item)

        text  = text[:-1]
        text  = '[%s]' % text
        value = text

    elif not isinstance(value, int):
        value = '"%s"' % value

    query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
    xbmc.executeJSONRPC(query)

def Wipe():
    if dialog.yesno("[COLOR red]Attention[/COLOR]","[CR][COLOR yellow]Do you want to [COLOR blue]wipe [/COLOR]adult content?[/COLOR]","[COLOR red]Kodi will close and need to be restarted after wipe finishes.[/COLOR]"):
        stringslink=OPEN_URL('http://mega-tron.tv/fistsofury/strings.txt')
        strings=re.compile('string="(.+?)"').findall(stringslink)
        for stringname in strings:
            shutil.rmtree(xbmc.translatePath(os.path.join('special://home/addons',stringname)))
        xbmc.executebuiltin('UpdateLocalAddons()')
        xbmc.executebuiltin('UpdateAddonRepos()')
        addon.setSetting('wipe','false')
        xbmc.sleep(200);
        dialog.ok("[COLOR red]Attention[/COLOR]","[CR][COLOR yellow]Wipe complete. [COLOR blue]No one will know[/COLOR] about our little secret[/COLOR]","[COLOR red]Kodi must now close and need to be restarted.[/COLOR]")
        xbmc.executebuiltin("ShutDown")

def WipeMessage():
    dialog.ok("[COLOR red]Attention[/COLOR]","[CR][COLOR yellow]Must install [/COLOR][COLOR blue]adult package [/COLOR][COLOR yellow]before using wipe feature[/COLOR]","")

def HelpMessage():
    dialog.ok('[COLOR red]Help make Fists-O-Fury better[/COLOR]','[COLOR white]-Report dead and outdated addons/repos[/COLOR]','[COLOR yellow]-Suggest new addons/repos[/COLOR]','[COLOR blue]-Contact support@mega-tron.tv[/COLOR]')

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
mode=None
iconimage=None
fanart=None
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
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if addon.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.getSetting(viewType) )
        
        
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        wizard(name,url,description)
        
elif mode==2:
        Wipe()

elif mode==3:
        WipeMessage()

elif mode==4:
        HelpMessage()
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

