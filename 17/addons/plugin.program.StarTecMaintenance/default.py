

#######################################################################
#						StarTec Maintenance							  #
#######################################################################
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
from urllib import FancyURLopener
import platform
import urllib2,urllib
import re
import glob
import time
import errno
import socket
import json
import parameters
import maintenance
import plugintools
import common as Common
import backuprestore
import maint
import speedtest
from net import Net
net = Net()


AddonTitle = "StarTec Maintenance"
addon_id   = 'plugin.program.StarTecMaintenance'
AddonData  = xbmc.translatePath('special://userdata/addon_data')
USERDATA   = xbmc.translatePath(os.path.join('special://home/userdata',''))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png')) 
favourites =  os.path.join(USERDATA,'favourites.xml')
ADDON      = xbmcaddon.Addon(id=addon_id)
CHANGELOG  = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id,'changelog.txt'))
skin       = xbmc.getSkinDir()
string     = ""
dialog     = xbmcgui.Dialog()
FANART     = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON       = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
backupdir    =  xbmc.translatePath(os.path.join('special://home/backupdir',''))
backupzip    =  os.path.join(backupdir,'backup_fav.zip')

def INDEX():
	cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
	tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
	WindowsCache = xbmc.translatePath('special://home')
	i = 0

	if os.path.exists(tempPath):
		for root, dirs, files in os.walk(tempPath,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							i = i + 1

	if os.path.exists(WindowsCache):
		for root, dirs, files in os.walk(WindowsCache,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							i = i + 1
	
	if i == 0:
		ERRORS_IN_LOG = "[COLOR blue]0 [COLOR yellow]Errors found in the log[/COLOR]"
	else:
		ERRORS_IN_LOG = "[COLOR red]" + str(i) + " [COLOR yellow]Errors found in the log[/COLOR]"
	HOME       =  xbmc.translatePath('special://home/')
	CACHE      =  xbmc.translatePath(os.path.join('special://home/cache',''))
	PACKAGES   =  xbmc.translatePath(os.path.join('special://home/addons','packages'))
	THUMBS     =  xbmc.translatePath(os.path.join('special://home/userdata','Thumbnails'))

	if not os.path.exists(CACHE):
		CACHE     =  xbmc.translatePath(os.path.join('special://home/temp',''))
	if not os.path.exists(PACKAGES):
		os.makedirs(PACKAGES)

	try:
		CACHE_SIZE_BYTE    = get_size(CACHE)#!f!T!G!#
		PACKAGES_SIZE_BYTE = get_size(PACKAGES)
		THUMB_SIZE_BYTE    = get_size(THUMBS)
	except: pass
	
	try:
		CACHE_SIZE    = convertSize(CACHE_SIZE_BYTE)
		PACKAGES_SIZE = convertSize(PACKAGES_SIZE_BYTE)
		THUMB_SIZE    = convertSize(THUMB_SIZE_BYTE)
	except: pass
	Common.addItem("[COLOR green][B]-------------------------------------------------[/B][/COLOR]",'url',0,ICON,FANART,'')
	Common.addItem("[COLOR yellow]Cache Size = [/COLOR]" + str(CACHE_SIZE),'url',3,ICON,FANART,'')
	Common.addItem("[COLOR yellow]Packages Size = [/COLOR]" + str(PACKAGES_SIZE),'url',6,ICON,FANART,'')
	Common.addItem("[COLOR yellow]Thumbnails Size = [/COLOR]" + str(THUMB_SIZE),'url',5,ICON,FANART,'')
	Common.addItem("[COLOR green][B]-------------------------------------------------[/B][/COLOR]",'url',0,ICON,FANART,'')
	Common.addDir('[COLOR yellow]Back-Up Options[/COLOR]','url',11,ICON,FANART,'')
	Common.addDir('[COLOR yellow]Internet Tools[/COLOR]','url',13,ICON,FANART,'')
	Common.addDir('[COLOR yellow]Open Addon Settings[/COLOR]','url',1,ICON,FANART,'')
	Common.addItem("[COLOR green][B]-------------------------------------------------[/B][/COLOR]",'url',0,ICON,FANART,'')
	Common.addItem('[COLOR yellow]View Current or Old Log File[/COLOR]','url',8,ICON,FANART,'')
	Common.addItem( ERRORS_IN_LOG,'url',17,ICON,FANART,'')
	Common.addItem('[COLOR yellow]Force Close Kodi[/COLOR]','url',10,ICON,FANART,'')
	Common.addItem('[COLOR red]!!Fresh Start!![/COLOR]','url',9,ICON,FANART,'')
	Common.addItem("[COLOR green][B]-------------------------------------------------[/B][/COLOR]",'url',0,ICON,FANART,'')
	Common.addItem('[COLOR yellow]Clear Cache[/COLOR]','url',3,ICON,FANART,'')
	Common.addItem('[COLOR yellow]Delete Crash Logs[/COLOR]','url',4,ICON,FANART,'')
	Common.addItem('[COLOR yellow]Delete Thumbnails[/COLOR]','url',5,ICON,FANART,'')
	Common.addItem('[COLOR yellow]Purge Packages[/COLOR]','url',6,ICON,FANART,'')

	
def IP_TOOLS():
	Common.addItem("[COLOR green][B]-------------------------------------------------[/B][/COLOR]",'url',79,ICON,FANART,'')
	Common.addItem('[COLOR yellow] IP Checker[/COLOR]','fanart', 14, ICON,FANART,'')
	Common.addItem('[COLOR yellow] Speed Test[/COLOR]','fanart', 15, ICON,FANART,'')
	Common.addItem("[COLOR green][B]-------------------------------------------------[/B][/COLOR]",'url',79,ICON,FANART,'')
	
def BackupMenu():
	if not os.path.exists(backupdir):os.makedirs(backupdir)
##needs work and modules added ####
	Common.addItem('[COLOR green][B]-----BACKUP OPTIONS-----[/B][/COLOR]','url',79,ICON,FANART,'')	
	Common.addItem('[COLOR yellow] Full Backup (Everything)[/COLOR]','url',20,ICON,FANART,'')	
	Common.addItem('[COLOR yellow] Backup Build ( No Thumbs or DBs)[/COLOR]','url',21,ICON,FANART,'')
	Common.addItem('[COLOR yellow] Backup Favorites[/COLOR]','url',18,ICON,FANART,'')
	Common.addItem('[COLOR yellow] Backup Super Favorites[/COLOR]','url',32,ICON,FANART,'')
	Common.addItem('[COLOR yellow] Backup Addon Data[/COLOR]','url',22,ICON,FANART,'')
	Common.addItem('[COLOR yellow] Backup RD & Trakt Settings[/COLOR]','url',23,ICON,FANART,'')
	Common.addItem('[COLOR yellow] Backup Ivue TV Guide settings[/COLOR]','url',31,ICON,FANART,'')
	Common.addItem('[COLOR green][B]-----RESTORE OPTIONS-----[/B][/COLOR]','url',79,ICON,FANART,'')	
	Common.addDir('[COLOR yellow] Restore A Full Backup[/COLOR]','url',24,ICON,FANART,'')
	Common.addItem('[COLOR yellow] Restore Favorites[/COLOR]','url',19,ICON,FANART,'')
	Common.addDir('[COLOR yellow] Restore Super Favourites[/COLOR]','url',24,ICON,FANART,'')
	Common.addDir('[COLOR yellow] Restore Addon Data[/COLOR]','url',24,ICON,FANART,'')
	Common.addDir('[COLOR yellow] Restore Ivue TV Guide settings[/COLOR]','url',24,ICON,FANART,'')
	Common.addDir('[COLOR yellow] Restore RD & Trakt Settings[/COLOR]','url',25,ICON,FANART,'')
	Common.addItem('[COLOR green][B]-----OTHER OPTIONS-----[/B][/COLOR]','url',79,ICON,FANART,'')	
	Common.addDir('[COLOR yellow] Delete A Backup[/COLOR]','url',26,ICON,FANART,'')
	Common.addItem('[COLOR yellow] Delete All Backups[/COLOR]','url',27,ICON,FANART,'')
	
def RESTOREFAV():
	dialog = xbmcgui.Dialog()
	if not os.path.isfile(backupzip):
			dialog.ok("[COLOR=red]FAVS BACKUP/RESTORE[/COLOR]", '', ' ', '                    You have no Favourites to Restore.')
			return
	else:
		choice = xbmcgui.Dialog().yesno("[COLOR=red]FAVS BACKUP/RESTORE[/COLOR]", 'Do you want to Restore your Favourites?', '', '', yeslabel='[COLOR=red]Yes[/COLOR]',nolabel='[COLOR=green]No[/COLOR]')
		if choice == 0:
			return
		elif choice == 1:
			import time
			dialog = xbmcgui.Dialog()
			dp =  xbmcgui.DialogProgress()
			lib=xbmc.translatePath(os.path.join(backupdir,'backup_fav.zip'))
			addonfolder = xbmc.translatePath(os.path.join('special://','home/userdata'))
			time.sleep(2)
			dp.create("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]","Restoring",'', 'Please Wait')
#(S)T(B)##(S)T(B)##(S)T(B)##(S)T(B)##(S)T(B)##(S)T(B)##(S)T(B)##(S)T(B)##(S)T(B)##(S)T(B)##(S)T(B)#
			extract.all(lib,addonfolder,dp)
			dp.close()
			dialog.ok("[COLOR=red]COMPLETE[/COLOR]", '', 'Your Favourites are Restored.', '')
			
def BACKUPFAV():
	if not os.path.exists(backupdir):os.makedirs(backupdir)
	if not os.path.isfile(favourites):
			dialog.ok("[COLOR=red]FAVS BACKUP/RESTORE[/COLOR]", '', ' ', '                    You have no Favourites to back-up.')
			return
	else:
		choice = xbmcgui.Dialog().yesno("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'Do you want to Back-up your Favourites?', '', '', yeslabel='[COLOR=red]Yes[/COLOR]',nolabel='[COLOR=green]No[/COLOR]')
		if choice == 0:
			return
		elif choice == 1:
			to_backup = xbmc.translatePath(os.path.join('special://','home/userdata'))	
			rootlen = len(to_backup)
			backup_ui_zip = xbmc.translatePath(os.path.join(backupdir,'backup_fav.zip'))
			zipobj = zipfile.ZipFile(backup_ui_zip , 'w', zipfile.ZIP_DEFLATED)
			fn = os.path.join(USERDATA, 'favourites.xml')
			dp.create("FTG BACKUP","Backing Up Favourites",'', 'Please Wait')
			zipobj.write(fn, fn[rootlen:])
			zipobj.close()
			dp.close()
			dialog.ok("[COLOR=red]COMPLETE[/COLOR]", '', 'Your Favourites are Backed up.', '')

##############################    Open addon settings    #########################################
def OPEN_SETTINGS(params):
	plugintools.open_settings_dialog()

##############################	Maint sizes   #########################################
def get_size(start_path):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	return total_size

def convertSize(size):
   import math
   if (size == 0):
	   return '[COLOR yellow]0 MB[/COLOR]'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")#!f!T!G!#
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if size_name[i] == "B":
		return '[COLOR lime]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if size_name[i] == "KB":##f#T#G##
		return '[COLOR yellow]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if size_name[i] == "GB":
		return '[COLOR lightskyblue]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if size_name[i] == "TB":
		return '[COLOR lightskyblue]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s < 50:
		return '[COLOR yellow]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s >= 50:
		if s < 100:
			return '[COLOR red]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s >= 100:
		return '[COLOR lightskyblue]%s %s' % (s,size_name[i]) + '[/COLOR]'

def convertSizeInstall(size):
   import math
   if (size == 0):
	   return '[COLOR blue]0 MB[/COLOR]'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if size_name[i] == "B":
		return '[COLOR lime]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if size_name[i] == "KB":
		return '[COLOR yellow]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if size_name[i] == "TB":
		return '[COLOR lightskyblue]%s %s' % (s,size_name[i]) + '[/COLOR]'#!f!T!G!#
   if s < 1000:
		return '[COLOR yellow]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s >= 1000:
		if s < 1500:
			return '[COLOR red]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s >= 1500:
		return '[COLOR lightskyblue]%s %s' % (s,size_name[i]) + '[/COLOR]'
##################################################################################

def addFolder(type,name,url,mode,iconimage = '',FanArt = '',video = '',description = ''):
	if type != 'folder2' and type != 'addon':
		if len(iconimage) > 0:
			iconimage = Images + iconimage
		else:##F#T#G##
			iconimage = 'DefaultFolder.png'
	if type == 'addon':
		if len(iconimage) > 0:
			iconimage = iconimage
		else:
			iconimage = 'none'
	if FanArt == '':
		FanArt = FanArt
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&FanArt="+urllib.quote_plus(FanArt)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
	liz.setProperty( "FanArt_Image", FanArt )
	liz.setProperty( "Build.Video", video )
	if (type=='folder') or (type=='folder2') or (type=='tutorial_folder') or (type=='news_folder'):
		ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	else:
		ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok
def Add_Directory_Item(handle, url, listitem, isFolder):
	xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder) 
#######################################################################
def SpeedTest():
	choice = xbmcgui.Dialog().yesno("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'Would you like to perform a speed test?', '', '', yeslabel='[COLOR=red]Yes[/COLOR]',nolabel='[COLOR=green]No[/COLOR]')
	if choice == 0:
		return
	elif choice == 1:
		xbmc.executebuiltin ( 'Runscript("special://home/addons/plugin.program.StarTecMaintenance/speedtest.py")' )
		xbmc.executebuiltin ( 'Runscript("special://home/addons/plugin.program.StarTecMaintenance/speedtest.py")' )
		
def IP_Check(url='http://myipinfo.net/',inc=1):
	mac = xbmc.getInfoLabel('Network.MacAddress')
	inIP = xbmc.getInfoLabel('Network.IPAddress')
	match=re.compile("<h2>(.+?)</h2>").findall(net.http_GET(url).content)
	for ip in match:
		if inc <2: dialog=xbmcgui.Dialog(); dialog.ok('[COLOR blue][B]What is My IP[/B][/COLOR]',"[B][COLOR yellow]Your External IP Address is: [B][COLOR lime]%s [/COLOR][/B] "  % ip, "[COLOR blue][B]Your Internal IP Address is: [COLOR lime]%s[/COLOR][/B]" % inIP, "[COLOR blue][B]Network MAC Address = [COLOR lime] %s [/B][/COLOR]" % mac)
		inc=inc+1
		
params=parameters.get_params()

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

if mode==None or url==None or len(url)<1:
		INDEX()

elif mode==1:OPEN_SETTINGS(params)
elif mode==2:maintenance.autocleanask()
elif mode==3:maintenance.clearCache()
elif mode==4:maintenance.DeleteCrashLogs()
elif mode==5:maintenance.deleteThumbnails()
elif mode==6:maintenance.purgePackages()
elif mode==7:maintenance.deleteAddonDB()
elif mode==8:maintenance.viewLogFile()
elif mode==9:maintenance.freshstart()
elif mode==10:
		print "############   ATTEMPT TO KILL XBMC/KODI   #################"
		Common.KillKodi()
elif mode == 11: BackupMenu()
elif mode == 13: IP_TOOLS()
elif mode == 14: IP_Check()
elif mode == 15: SpeedTest()
elif mode == 17: maintenance.view_LastError()
elif mode == 18: BACKUPFAV() #BackupMenu
elif mode == 19: RESTOREFAV()#RestoreMenu
elif mode == 20: backuprestore.FullBackup()
elif mode == 21: backuprestore.Backup()
elif mode == 22: backuprestore.ADDON_DATA_BACKUP()
elif mode == 23: backuprestore.BACKUP_RD_TRAKT()
elif mode == 24: backuprestore.Restore()
elif mode == 25: backuprestore.RESTORE_RD_TRAKT()
elif mode == 26: backuprestore.ListBackDel()
elif mode == 27: backuprestore.DeleteAllBackups()
elif mode == 28: backuprestore.READ_ZIP(url)
elif mode == 29: backuprestore.DeleteBackup(url)
elif mode == 30: backuprestore.READ_ZIP_TRAKT(url)
elif mode == 31: backuprestore.TV_GUIDE_BACKUP()
elif mode == 32: backuprestore.SUPERFAVS_BACKUP()

xbmcplugin.endOfDirectory(int(sys.argv[1]))