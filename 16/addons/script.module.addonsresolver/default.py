# -*- coding: UTF-8 -*-
# Addons resolver
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.
# MafaStudios@gmail.com
import re,xbmcgui,xbmcaddon,xbmc,os,urllib,json,xbmcplugin
from resources.libs import play,basic
from resources.libs.parsers import links

addonId			= xbmcaddon.Addon().getAddonInfo("id")
selfAddon 		= xbmcaddon.Addon(id=addonId)
language		= selfAddon.getLocalizedString

if links.link().getSetting("settings_version") <> '0.1.0':
	if os.path.exists(os.path.join(links.link().dataPath,'settings.xml')): os.remove(os.path.join(links.link().dataPath,'settings.xml'))
	links.link().setSetting('settings_version', '0.1.0')
	
def MAIN():
	addDir('Settings','settings')
	xbmc.executebuiltin('Addon.OpenSettings(%s)' % addonId)

def addDir(name,action):
        u=sys.argv[0]+"?action="+urllib.quote_plus(action)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
        liz.setProperty('fanart_image', '')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param
		
params=get_params()
url=None
name=None
action=None
imdbid=None
year=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: action=urllib.unquote_plus(params["action"])
except: pass
try: imdbid=urllib.unquote_plus(params["imdbid"])
except: pass
try: year=urllib.unquote_plus(params["year"])
except: pass

print "Action: "+str(action)
print "URL: "+str(url)
print "Name: "+str(name)
print "imdbid: "+str(imdbid)
print "year: "+str(year)

if action==None: MAIN()
elif action == 'play': play.play().play_stream(name, url, imdbid, year)
elif action == 'library': basic.library_movie_add(name, url, imdbid, year)
elif action == 'settings': xbmc.executebuiltin('Addon.OpenSettings(%s)' % addonId)
xbmcplugin.endOfDirectory(int(sys.argv[1]))