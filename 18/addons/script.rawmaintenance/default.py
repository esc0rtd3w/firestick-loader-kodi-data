#   script.rawmaintenance, Raw Media's XBMC Maintenance Tool
#   Copyright (C) 2014  Adam Parker
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.



import urllib,urllib2,re,uuid, time
import xbmcgui,xbmcplugin
import feedparser
import os

import GATracker

thumbnailPath = xbmc.translatePath('special://thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'script.rawmaintenance')
mediaPath = os.path.join(addonPath, 'media')
databasePath = xbmc.translatePath('special://database')

#######################################################################
#                          CLASSES
#######################################################################

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi
        
#######################################################################
#						Google Analytics
#######################################################################
global analytics

def setupAnalytics():
    global analytics

    if(os.path.isfile(os.path.join(addonPath, "uuid.txt")) != True):
        userID = uuid.uuid1()
        uuidFile = open(os.path.join(addonPath,"uuid.txt"), "w")
        uuidFile.write(str(userID))
        uuidFile.close()

    uuidFile = open(os.path.join(addonPath, "uuid.txt"), "r")
    userID = uuidFile.readline()
    uuidFile.close()

    analytics = GATracker.GAconnection("UA-36482713-5", userID)
    
#######################################################################
#                           NEWS
#######################################################################

def NewsText():
    global analytics
    analytics.sendEvent("MainMenu", "News")
    
    dialog = xbmcgui.Dialog()
    dialog.ok("Raw Maintenance", "News from Raw-Media.ca:", "Happy St. Patricks Day! Don't forget to subscribe to our YouTube channel youtube.com/gombeek ")


#######################################################################
#							RSS
#######################################################################
global rss

def rssStartup():
    print "----####RSS STARTUP####----"
    global rss 

    rss = feedparser.parse('http://notanrss.info/rss.vex')
    if rss.bozo:
        dialog = xbmcgui.Dialog()
        dialog.ok("RSS", "There was a problem with the feed", "Check your internet connection and/or try again later")
        return -1

def rssMenu():
    analytics.sendPageView("RawMaintenenance","RSSmenu","RSS")
    print "----####RSS MENU CONFIG####----"
    global rss
    xbmc.executebuiltin("Container.SetViewMode(50)")
    x = 50
    for entry in rss.entries:
        print entry.title
        addItem(entry.title, 'url', x, os.path.join(mediaPath, "news.png"))
        x=x+1
        
def rssShowStory(mode):
    mode = mode - 50;
    print mode
    
    rss = feedparser.parse('http://www.feedforall.com/sample.xml')
    if rss.bozo:
        dialog = xbmcgui.Dialog()
        dialog.ok("RSS", "There was a problem with the feed", "Check your internet connection and/or try again later")
	
    dialog = xbmcgui.Dialog()
    dialog.ok(rss.entries[mode].title, rss.entries[mode].description)
        
#######################################################################
#						Define Menus
#######################################################################

def mainMenu():
    global analytics
    analytics.sendPageView("RawMaintenenance","mainmenu","main")
    xbmc.executebuiltin("Container.SetViewMode(500)")
    addDir('Maintenance','url', 5,os.path.join(mediaPath, "maintenance.png"))
    addItem('News', 'url', 4,os.path.join(mediaPath, "news.png"))
    addItem('Support', 'url', 6, os.path.join(mediaPath, "support.png"))
    
def maintMenu():
    analytics.sendPageView("RawMaintenenance","maintenance","maint")
    xbmc.executebuiltin("Container.SetViewMode(500)")
    addItem('Clear Cache','url', 1,os.path.join(mediaPath, "cache.png"))
    addItem('Delete Thumbnails', 'url', 2,os.path.join(mediaPath, "thumbs.png"))
    addItem('Purge Packages', 'url', 3,os.path.join(mediaPath, "packages.png"))

#######################################################################
#						Add to menus
#######################################################################

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok


def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	
def addItem(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

#######################################################################
#						Parses Choice
#######################################################################
      
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

#######################################################################
#						Work Functions
#######################################################################
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["WTF", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.video.whatthefurk/cache", "special://profile/addon_data/plugin.video.4od/cache",
					"special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries


def clearCache():
    global analytics
    analytics.sendEvent("Maintenance", "ClearCache")
    
    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            if (f == "xbmc.log" or f == "xbmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Kodi Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f == "xbmc.log" or f == "xbmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    dialog = xbmcgui.Dialog()
                    if dialog.yesno("Raw Manager",str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
                

    dialog = xbmcgui.Dialog()
    dialog.ok("Raw Maintenance", "Done Clearing Cache files")
    
    
def deleteThumbnails():
    global analytics
    analytics.sendEvent("Maintenance", "DeleteThumbnails")
    
    if os.path.exists(thumbnailPath)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete Thumbnails", "This option deletes all thumbnails", "Are you sure you want to do this?"):
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass                
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    os.unlink(text13)
        
    dialog.ok("Restart Kodi", "Please restart Kodi to rebuild thumbnail library")
        
def purgePackages():
    global analytics
    analytics.sendEvent("Maintenance", "PurgePacakges")
    
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    if dialog.yesno("Delete Package Cache Files", "%d packages found."%file_count, "Delete Them?"):  
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                dialog = xbmcgui.Dialog()
                dialog.ok("Raw Maintenance", "Deleting Packages all done")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok("Raw Maintenance", "No Packages to Purge")

#######################################################################
#                       Support
#######################################################################
def SupportText():
    global analytics
    analytics.sendEvent("MainMenu", "Support")
    
    dialog = xbmcgui.Dialog()
    dialog.ok("Raw Maintenance", "Log into http://www.no-issue.ca for support", "Follow No-Issue on Twitter @Gombeek or Youtube youtube.com/gombeek", "Raw Media Instagram @iloveitraw or Twitter @iloveitraw")

#######################################################################
#						START MAIN
#######################################################################              
setupAnalytics()

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

if mode==None or url==None or len(url)<1:
        mainMenu()
       
elif mode==1:
		clearCache()
        
elif mode==2:
        deleteThumbnails()

elif mode==3:
		purgePackages()
        
elif mode==4:
        NewsText()
        
elif mode==5:
        maintMenu()

elif mode==6:
        SupportText()
        
elif mode >= 50:
        rssShowStory(mode)



xbmcplugin.endOfDirectory(int(sys.argv[1]))

