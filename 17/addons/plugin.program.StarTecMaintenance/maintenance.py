import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import shutil
import urllib2,urllib
import re
import glob
import common as Common
import time


EXCLUDES     = ['plugin.program.StarTecMaintenance','plugin.program.StarTecMaintenance','repository.startectec','backupdir','script.module.requests','temp','kodi.log','kodi.log.old','spmc.log','spmc.log.old','dbmc.log','dbmc.log.old']

thumbnailPath = xbmc.translatePath('special://userdata/Thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
HOME           =  xbmc.translatePath('special://home/')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.program.ftgmaint')
mediaPath = os.path.join(addonPath, 'resources/art')
databasePath = xbmc.translatePath('special://userdata/Database')
USERDATA = xbmc.translatePath('special://userdata/')
AddonData = xbmc.translatePath('special://userdata/addon_data')
MaintTitle="StarTec Maintenance"
dp = xbmcgui.DialogProgress()
Windows = xbmc.translatePath('special://home')
WindowsCache = xbmc.translatePath('special://home')
OtherCache = xbmc.translatePath('special://home/temp')
dialog = xbmcgui.Dialog()
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
SKIN           =  xbmc.getSkinDir()

def skincheck():
	if SKIN not in ['skin.confluence', 'skin.estuary']:
		skin = 'skin.estuary' if KODIV >= 17 else 'skin.confluence'
		choice = xbmcgui.Dialog().yesno("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", "The skin needs to be set back to [COLOR lime]%s[/COLOR]" % skin[5:], "Before doing a fresh install", "Would you like us to do that for you?", nolabel="No, Thanks", yeslabel="Yes, Swap Skin");
		if choice == 1:	
			skinSwitch.swapSkins(skin)
			while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
				xbmc.sleep(200)
			xbmc.executebuiltin("Action(Left)")
			xbmc.executebuiltin("Action(Select)")
		
	skin         =  xbmc.getSkinDir()

	####Check if the skin is not Confluence####
	if skin not in ['skin.confluence','skin.estuary']:
		choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR red][B]ERROR: Autoswitch was not succesfull[/B][/COLOR]','[COLOR blue][B]Click YES to manually switch to confluence now[/B][/COLOR]','[COLOR blue][B]YOU CAN PRESS NO AND ATTEMPT THE AUTO SWITCH AGAIN IF YOU WISH[/B][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
		if choice == 1:
			xbmc.executebuiltin("ActivateWindow(appearancesettings)")
			return
		else:
			sys.exit(1)
def freshstart():
    skincheck()
    choice = xbmcgui.Dialog().yesno("[COLOR=red]ABSOLUTELY CERTAIN?!!![/COLOR]", 'Are you absolutely certain you want to wipe this install?', '', 'All addons EXCLUDING The Addon and Backups', yeslabel='[COLOR=red]Yes[/COLOR]',nolabel='[COLOR=green]No[/COLOR]')
    if choice == 0:
        return
    elif choice == 1:
        dp.create("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]","Wiping Install",'', 'Please Wait')
        try:
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass
                        
                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    Remove_AddonsDB()
    Remove_Textures()
    dp.close()
    Common.killkodi()
	
def Remove_Textures():
	textures   =  xbmc.translatePath('special://home/userdata/Database/Textures13.db')
	try:
		dbcon = database.connect(textures)
		dbcur = dbcon.cursor()
		dbcur.execute("DROP TABLE IF EXISTS path")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS sizes")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS texture")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
		dbcon.commit()
	except:
		pass
		
def Remove_AddonsDB():
	textures   =  xbmc.translatePath('special://home/userdata/Database/Textures13.db')
	try:
		dbcon = database.connect(textures)
		dbcur = dbcon.cursor()
		dbcur.execute("DROP TABLE IF EXISTS addon")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS addonextra")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS addonlinkrepo")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS blacklist")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS broken")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS dependecies")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS disabled")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS package")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS repo")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS system")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("DROP TABLE IF EXISTS version")
		dbcur.execute("VACUUM")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE addon (id integer primary key, type text,name text, summary text, description text, stars integer,path text, addonID text, icon text, version text, changelog text, fanart text, author text, disclaimer text,minversion text) """)
		dbcon.commit()
		dbcur.execute("""CREATE TABLE addonextra (id integer, key text, value text)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE addonlinkrepo (idRepo integer, idAddon integer)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE blacklist (id integer primary key, addonID text)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE broken (id integer primary key, addonID text, reason text)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE dependencies (id integer, addon text, version text, optional boolean)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE disabled (id integer primary key, addonID text)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE package (id integer primary key, addonID text, filename text, hash text) """)
		dbcon.commit()
		dbcur.execute("""CREATE TABLE repo (id integer primary key, addonID text,checksum text, lastcheck text, version text)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE system (id integer primary key, addonID text)""")
		dbcon.commit()
		dbcur.execute("""CREATE TABLE version (idVersion integer, iCompressCount integer)""")
		dbcon.commit()
	except:
		pass
	
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
            used_count += 1 #increment used_count
			
class Gui(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.header = kwargs.get("header")
        self.content = kwargs.get("content")

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.content)

#path   = xbmcaddon.Addon().getAddonInfo('path').decode("utf-8")

class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi	

#######################################################################
#						Maintenance Functions
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

#######################################################################
#						Clear Cache
#######################################################################

def clearCache():
    
    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Media Center Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
							if (f.endswith(".log")): continue
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
                if dialog.yesno("Delete Media Center Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
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
                    if dialog.yesno(MaintTitle,str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
                

    dialog = xbmcgui.Dialog()
    dialog.ok(MaintTitle, "Done Clearing Cache files")

#######################################################################
#						Delete Thumbnails
#######################################################################
    
def deleteAddonDB():

	dialog = xbmcgui.Dialog()
	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])

	if version >= 17.0 and version <= 17.9:
		codename = 'Krypton'
	else:
		codename = 'Pass'
	
	if codename == "Pass":
		try:
			for root, dirs, files in os.walk(databasePath,topdown=True):
				dirs[:] = [d for d in dirs]
				for name in files:
					if "addons" in name.lower():
						try:
							os.remove(os.path.join(root,name))
						except: 
							dialog.ok(MaintTitle,'Error Removing ' + str(name),'','[COLOR yellow]Thank you for using FTG Maintenance[/COLOR]')
							pass
					else:
						continue
		except:
			pass
	else:
		dialog.ok(MaintTitle,'This feature is not available in Kodi 17 Krypton','','[COLOR yellow]Thank you for using FTG Maintenance[/COLOR]')


#######################################################################
#						Delete Thumbnails
#######################################################################
    
def deleteThumbnails(): 
    if os.path.exists(thumbnailPath)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", "This option deletes all Media Center thumbnails", "Are you sure you want to do this?"):
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
								pass
		Remove_Textures()
		dialog.ok("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", '                [COLOR=lime]All Thumbnails have been deleted.[/COLOR]','     [COLOR=red] Press OK to Attempt to Force Close your Media center[/COLOR]')
		Common.killkodi1()

#######################################################################
#						Delete Packages
#######################################################################

def purgePackages():
    
    purgePath = xbmc.translatePath('special://home/addons/packages')
    dialog = xbmcgui.Dialog()
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    if dialog.yesno("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]","This option deletes all Media Center Packages?", "%d packages found."%file_count, "Delete Them?"):  
        for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
                dialog = xbmcgui.Dialog()
                dialog.ok(MaintTitle, "     Deleting Packages all done")
            else:
                dialog = xbmcgui.Dialog()
                dialog.ok(MaintTitle, "      No Packages to Purge")
				


	
#######################################################################
#						Autoclean Function
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

#######################################################################
#						Delete Crash Log Function
#######################################################################

def DeleteCrashLogs():  

	HomeDir = xbmc.translatePath('special://home')
	WindowsCache = os.path.join(xbmc.translatePath('special://home'), 'cache')
	OtherCache = xbmc.translatePath('special://temp')
	
	if os.path.exists(HomeDir)==True:   
		dialog = xbmcgui.Dialog()
		if dialog.yesno(MaintTitle, '', "Do you want to delete old crash logs?"):
			path=Windows
			import glob
			for infile in glob.glob(os.path.join(path, '*.dmp')):
				File=infile
				print infile
				os.remove(infile)
				
			for infile in glob.glob(os.path.join(path, '*.txt')):
				File=infile
				print infile
				os.remove(infile)
				
		if os.path.exists(WindowsCache)==True:   
			path=WindowsCache
			import glob
			for infile in glob.glob(os.path.join(path, '*.dmp')):
				File=infile
				print infile
				os.remove(infile)
				
			for infile in glob.glob(os.path.join(path, '*.txt')):
				File=infile
				print infile
				os.remove(infile)

		if os.path.exists(OtherCache)==True:   
			path=OtherCache
			import glob
			for infile in glob.glob(os.path.join(path, '*.dmp')):
				File=infile
				print infile
				os.remove(infile)
				
			for infile in glob.glob(os.path.join(path, '*.txt')):
				File=infile
				print infile
				os.remove(infile)
		
		dialog = xbmcgui.Dialog()
		dialog.ok(MaintTitle, "Crash logs deleted", "[COLOR yellow]Thank you for using FTG Maintenance[/COLOR]")
            
	else:
	
		dialog = xbmcgui.Dialog()
		dialog.ok(MaintTitle, "An error occured", "[COLOR yellow]Please report this to FTG Maintenance[/COLOR]")


def viewLogFile():
	kodilog = xbmc.translatePath('special://logpath/kodi.log')
	spmclog = xbmc.translatePath('special://logpath/spmc.log')
	dbmclog = xbmc.translatePath('special://logpath/spmc.log')
	kodiold = xbmc.translatePath('special://logpath/kodi.old.log')
	spmcold = xbmc.translatePath('special://logpath/spmc.old.log')
	dbmcold = xbmc.translatePath('special://logpath/kodi.old.log')
				
	if os.path.exists(spmclog):
		if os.path.exists(spmclog) and os.path.exists(spmcold):
			choice = xbmcgui.Dialog().yesno(MaintTitle,"Curretn & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
			if choice == 0:
				f = open(spmclog,mode='r'); msg = f.read(); f.close()
				TextBoxes("%s - spmc.log" % "[COLOR white]" + msg + "[/COLOR]")
			else:
				f = open(spmcold,mode='r'); msg = f.read(); f.close()
				TextBoxes("%s - spmc.old.log" % "[COLOR white]" + msg + "[/COLOR]")
		else:
			f = open(spmclog,mode='r'); msg = f.read(); f.close()
			TextBoxes("%s - spmc.log" % "[COLOR white]" + msg + "[/COLOR]")
			
	if os.path.exists(kodilog):
		if os.path.exists(kodilog) and os.path.exists(kodiold):
			choice = xbmcgui.Dialog().yesno(MaintTitle,"Curretn & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
			if choice == 0:
				f = open(kodilog,mode='r'); msg = f.read(); f.close()
				TextBoxes("%s - kodi.log" % "[COLOR white]" + msg + "[/COLOR]")
			else:
				f = open(kodiold,mode='r'); msg = f.read(); f.close()
				TextBoxes("%s - kodi.old.log" % "[COLOR white]" + msg + "[/COLOR]")
		else:
			f = open(kodilog,mode='r'); msg = f.read(); f.close()
			TextBoxes("%s - kodi.log" % "[COLOR white]" + msg + "[/COLOR]")
			
	if os.path.exists(dbmclog):
		if os.path.exists(dbmclog) and os.path.exists(dbmcold):
			choice = xbmcgui.Dialog().yesno(MaintTitle,"Curretn & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
			if choice == 0:
				f = open(dbmclog,mode='r'); msg = f.read(); f.close()
				TextBoxes("%s - dbmc.log" % "[COLOR white]" + msg + "[/COLOR]")
			else:
				f = open(dbmcold,mode='r'); msg = f.read(); f.close()
				TextBoxes("%s - dbmc.old.log" % "[COLOR white]" + msg + "[/COLOR]")
		else:
			f = open(dbmclog,mode='r'); msg = f.read(); f.close()
			TextBoxes("%s - dbmc.log" % "[COLOR white]" + msg + "[/COLOR]")
			
	if os.path.isfile(kodilog) or os.path.isfile(spmclog) or os.path.isfile(dbmclog):
		return True
	else:
		dialog.ok(MaintTitle,'Sorry, No log file was found.','','[COLOR yellow]Thank you for using FTG Maintenance[/COLOR]')
		
def view_LastError():

	cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
	tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
	WindowsCache = xbmc.translatePath('special://home')
	found = 0
	get_log = 0

	if os.path.exists(tempPath):
		for root, dirs, files in os.walk(tempPath,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							THE_ERROR = "[B][COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/B][/COLOR]\n\n" + checker + '\n'
						if found == 0:
							dialog.ok(MaintTitle,'Great news! We did not find any errors in your log.')
						else:
							c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
							TextBoxesPlain("%s" % c)
							sys.exit(0)

	if os.path.exists(WindowsCache):
		for root, dirs, files in os.walk(WindowsCache,topdown=True):
			dirs[:] = [d for d in dirs]
			for name in files:
				if ".old.log" not in name.lower():
					if ".log" in name.lower():
						got_log = 1
						a=open((os.path.join(root, name))).read()	
						b=a.replace('\n','NEW_L').replace('\r','NEW_R')
						match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
						for checker in match:
							found = 1
							THE_ERROR = "[B][COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/B][/COLOR]\n\n" + checker + '\n'
						if found == 0:
							dialog.ok(MaintTitle,'Great news! We did not find any errors in your log.')
						else:
							c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
							TextBoxesPlain("%s" % c)
							sys.exit(0)
	if got_log == 0:
		dialog.ok(MaintTitle,'Sorry we could not find a log file on your system')
		
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
			self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR red]StarTec[COLOR snow] -[COLOR blue] Log Viewer[/COLOR]') # set heading
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
			self.win.getControl(self.CONTROL_LABEL).setLabel('[COLOR red]StarTec[COLOR snow] -[COLOR blue] Log Viewer[/COLOR]') # set heading
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			return
	TextBox()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

	
def AutoCache():

    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
							if (f.endswith(".log")): continue
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
                    for f in files:
                        try:
                            if (f.endswith(".log")): continue
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
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass

def AutoThumbs():

    if os.path.exists(thumbnailPath)==True:  
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
								pass
		Remove_Textures()
		dialog.ok("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", '                [COLOR=lime]All Thumbnails have been deleted.[/COLOR]','     [COLOR=red] Press OK to Attempt to Force Close your Media center[/COLOR]')
		Common.killkodi1()


def AutoPackages():

    purgePath = xbmc.translatePath('special://home/addons/packages')
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
    for root, dirs, files in os.walk(purgePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:            
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    dialog.ok("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", "               [COLOR=lime]All Packages have been deleted.[/COLOR]")

