#!/usr/bin/python
import urllib, sys, os
import xbmcaddon, xbmcplugin, xbmcgui

addonID = "plugin.video.thewiz.kids"
Addon = xbmcaddon.Addon(addonID)
AddonName = Addon.getAddonInfo("name")

def getParams(string):
    parsed = {};
    if string:
        params = string[1:].split("&")
        for param in params:
            pair = param.split("=")
            if len(pair) == 2:
                parsed[pair[0]] = pair[1]
    return parsed

def addFolder(name,url,icon="",description=""):
	li = xbmcgui.ListItem(name)
	li.setThumbnailImage(icon)
	xbmcplugin.setResolvedUrl(pluginhandle, True, li)
	xbmcplugin.addDirectoryItem(pluginhandle,url,li,True) 

pluginhandle = int(sys.argv[1])
params = getParams(sys.argv[2])
addFolder("בייבי אינשטיין","plugin://plugin.video.youtube/playlist/PLwCtRnl6mSkgr4O7igScDk9ULr_yuQzrZ/","http://from-us.cachefly.net/blog/wp-content/uploads/2014/11/Baby-Einstein.jpg")
addFolder("רוץ דייגו רוץ!","plugin://plugin.video.youtube/playlist/PLqx6fN1abed4oHQ2Y5xadY-ILjzFdoMNM/","http://msc.wcdn.co.il/archive/768471-35.jpg")
addFolder("הצגות ילדים","plugin://plugin.video.youtube/playlist/PLuDrdycU7c6hEmDRRz4vCK5loXcRM6Ama/","http://images.mouse.co.il/storage/0/a/ggg--zota.jpg")
addFolder("שירי ילדים אהובים","plugin://plugin.video.youtube/playlist/PLD844E42A04406A34/","http://www.yosmusic.com/images/articles/hayeladim.jpg")
addFolder("יום העצמאות לילדים","plugin://plugin.video.youtube/playlist/PLeL_VG-7obI01X4Y3diyJxD0t3xoyZ4rg/","http://www.galim.org.il/pools/files/GalimGifs/GalimGifPicture/3766.gif")
addFolder("מיקי מאוס קלאב [E]","plugin://plugin.video.youtube/playlist/PLlhWlE60ki0gZVFvC86GgnQvHOmBu8QaI/","http://upload.wikimedia.org/wikipedia/en/d/d4/Mickey_Mouse.png")
addFolder("רשימת שירי ערש לילדים","plugin://plugin.video.youtube/playlist/PLDawkzK5FF6oqPnh5EHxcG9FdDjBR9XVI/","http://media.israel-music.com/images/38712021.jpg")
addFolder("דיסקים לילדים","plugin://plugin.video.youtube/playlist/PLdbM_E489jekYTo06X7zOt-lmgVg-Z1b3/","http://ypk.cs4u.co.il/wbl_vcs31_P_Images/bmx/pic/ZF6250765_3.jpg")