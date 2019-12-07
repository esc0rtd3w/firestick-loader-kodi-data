import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import re
import time
addon_id   = 'program.StarTecMaintenance'
AddonTitle = "StarTec Maintenance"
HOME         =  xbmc.translatePath('special://home/')
dialog       =  xbmcgui.Dialog()


def addDir(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
	liz.setProperty( "Fanart_Image", fanart )
	if mode==90 :
	    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
	    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addItem(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDirWTW(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addLink(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)\
	+ "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",
			   thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
				     listitem=liz, isFolder=False)
    return ok

def find_single_match(text,pattern):

    result = ""
    try:    
	single = re.findall(pattern,text, flags=re.DOTALL)
	result = single[0]
    except:
	result = ""

    return result

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
	return unicode( keyboard.getText(), "utf-8" )
    return default
		
def TextBoxes(announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel('FTG - View Log Facility') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

def TextBoxesPlain(announce):
	class TextBox():
		WINDOW=10147
		CONTROL_LABEL=1
		CONTROL_TEXTBOX=5
		def __init__(self,*args,**kwargs):
			xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			self.win=xbmcgui.Window(self.WINDOW) # get window
			xbmc.sleep(500) # give window time to initialize
			self.setControls()
		def setControls(self):
			self.win.getControl(self.CONTROL_LABEL).setLabel('[B]FTG[/B]') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

##########################
###DETERMINE PLATFORM#####
##########################
	
def platform():
    if xbmc.getCondVisibility('system.platform.android'):
	return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
	return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
	return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
	return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
	return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
	return 'ios'
		
############################
###REMOVE EMPTY FOLDERS#####
############################

def REMOVE_EMPTY_FOLDERS():
#initialize the counters
    print"########### Start Removing Empty Folders #########"
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
	if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
	    empty_count += 1 #increment empty_count
	    os.rmdir(curdir) #delete the directory
	    print "successfully removed: "+curdir
	elif len(subdirs) > 0 and len(files) > 0: #check for used directories
	    used_count += 1 #increment 
		
###############################################################
###FORCE CLOSE KODI - ANDROID ONLY WORKS IF ROOTED#############
###############################################################

def killkodi1():
	choice = xbmcgui.Dialog().yesno("[B][COLOR yellow]GenTec Maintenance[/COLOR][/B]", '     Do you want to Force Close your Media Center?', 'Highly recommended that you do!', '', yeslabel='[COLOR=red]Yes[/COLOR]',nolabel='[COLOR=green]No[/COLOR]')
	if choice == 0:
		return
	elif choice == 1:
		killkodi()


def killkodi():
	myplatform = platform()
	os._exit(1)
	log("Force close failed!  Trying alternate methods.")
	if myplatform == 'osx': # OSX
		log("############ try osx force close #################")
		try: os.system('killall -9 XBMC')
		except: pass
		try: os.system('killall -9 Kodi')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
	elif myplatform == 'linux': #Linux
		log("############ try linux force close #################")
		try: os.system('killall XBMC')
		except: pass
		try: os.system('killall Kodi')
		except: pass
		try: os.system('killall -9 xbmc.bin')
		except: pass
		try: os.system('killall -9 kodi.bin')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
	elif myplatform == 'android': # Android 
		log("############ try android force close #################")
		try: os.system('adb shell am force-stop org.xbmc.kodi')
		except: pass
		try: os.system('adb shell am force-stop org.kodi')
		except: pass
		try: os.system('adb shell am force-stop org.xbmc.xbmc')
		except: pass
		try: os.system('adb shell am force-stop org.xbmc')
		except: pass		
		try: os.system('adb shell kill org.xbmc.kodi')
		except: pass
		try: os.system('adb shell kill org.kodi')
		except: pass
		try: os.system('adb shell kill org.xbmc.xbmc')
		except: pass
		try: os.system('adb shell kill org.xbmc')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.xbmc,kodi());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.kodi());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.xbmc.xbmc());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.org.xbmc());')
		except: pass
		try: os.system('Process.killProcess(android.os.Process.com.semperpax.spmc16());')
		except: pass
		DIALOG.ok( "[COLOR=red][B]WARNING !!![/COLOR][/B]","Press the HOME button on your remote and [COLOR=red][B]FORCE STOP[/COLOR][/B] KODI via the Manage Installed Applications menu in settings on your Amazon home page then re-launch KODI")
	elif myplatform == 'windows': # Windows
		log("############ try windows force close #################")
		try:
			os.system('@ECHO off')
			os.system('tskill XBMC.exe')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('tskill Kodi.exe')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im Kodi.exe /f')
		except: pass
		try:
			os.system('@ECHO off')
			os.system('TASKKILL /im XBMC.exe /f')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
	else: #ATV
		log("############ try atv force close #################")
		try: os.system('killall AppleTV')
		except: pass
		log("############ try raspbmc force close #################") #OSMC / Raspbmc
		try: os.system('sudo initctl stop kodi')
		except: pass
		try: os.system('sudo initctl stop xbmc')
		except: pass
		DIALOG.ok("[COLOR=red][B]WARNING !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","iOS detected. Press and hold both the Sleep/Wake and Home button for at least 10 seconds, until you see the Apple logo.")