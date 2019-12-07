import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import plugintools
import plugintools
import zipfile
import ntpath
import base64
import skinSwitch
import maintenance
import common as Common
from os import listdir
from os.path import isfile, join
from shutil import copyfile

base            =  'firetvguru.net'
dp              =  xbmcgui.DialogProgress()
AddonTitle      =  "StarTec Maintenance"
AddonID         =  'plugin.program.StarTecMaintenance'
selfAddon       =  xbmcaddon.Addon(id=AddonID)
PACKAGES        =  xbmc.translatePath(os.path.join('special://home/addons/' + 'packages'))
dialog          =  xbmcgui.Dialog()  
ICON            =  xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
HOME            =  xbmc.translatePath('special://home/')
USERDATA        =  xbmc.translatePath(os.path.join('special://home/userdata',''))
zip             =  plugintools.get_setting("zip")
USB             =  xbmc.translatePath(os.path.join(zip))
HOME            =  xbmc.translatePath('special://home/')
EXCLUDES_FOLDER =  xbmc.translatePath(os.path.join(USERDATA,'BACKUP'))
ADDON_DATA      =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
GUIDE           =  xbmc.translatePath(os.path.join(ADDON_DATA,'script.ivueguide'))
SUPERFAVS       =  xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.program.super.favourites'))
ADDON_DATA      =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
DATABASES       =  xbmc.translatePath(os.path.join(USERDATA,'Database'))
ADDONS          =  xbmc.translatePath(os.path.join('special://home','addons',''))
EXCLUDES        =  ['cache','temp','tmp_trakt','EXCLUDES','Database','backupdir','plugin.program.fire','script.module.requests','repository.fire']
EXCLUDES_BUILD  =  ['Thumbnails','cache','temp','tmp_trakt','EXCLUDES','Database','backupdir','plugin.program.fire','script.module.requests','repository.fire']
EXCLUDES_FILES  =  ""

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
	
def OPEN_URL(url):#!F!T!G!#
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)##F#T#G##
	link=response.read()
	response.close()
	return link
	
def WIPE_BACKUPRESTORE():

	dp.create(AddonTitle,"Restoring Your Media Center.",'In Progress #+#+#+#+#+#+#+#+#', 'Please Wait')
	try:
		for root, dirs, files in os.walk(HOME,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in files:
				try:
					os.remove(os.path.join(root,name))
					os.rmdir(os.path.join(root,name))
				except: pass
			else:
				continue
                        
			for name in dirs:
				try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
				except: pass
	except: pass

	dp.create(AddonTitle,"Wiping Install",'Removing empty folders.', 'Please Wait')
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()

	if os.path.exists(DATABASES):
		try:
			for root, dirs, files in os.walk(DATABASES,topdown=True):
				dirs[:] = [d for d in dirs]
				for name in files:
					try:
						os.remove(os.path.join(root,name))
						os.rmdir(os.path.join(root,name))
					except: pass
                        
				for name in dirs:
					try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
					except: pass
		except: pass
		
	if os.path.exists(ADDON_DATA):
		try:
			for root, dirs, files in os.walk(ADDON_DATA,topdown=True):
				dirs[:] = [d for d in dirs]
				for name in files:
					try:
						os.remove(os.path.join(root,name))
						os.rmdir(os.path.join(root,name))
					except: pass
                        
				for name in dirs:
					try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
					except: pass
		except: pass

def check_path():

	if not "backupdir" in USB:
		if HOME in USB:
			dialog = xbmcgui.Dialog()
			dialog.ok(AddonTitle, "Invalid path selected for your backups. The path you have selected will be removed during backup and cause an error. Please pick another path that is not in the Kodi directory")
			plugintools.open_settings_dialog()
			sys.exit(0)
	if not os.path.exists(USB):
		os.makedirs(USB)
		
def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default

def Backup():
    guisuccess=1
    check_path()
    if os.path.exists(PACKAGES):
        shutil.rmtree(PACKAGES)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'.zip'))
    exclude_dirs =  ['backupdir','cache', 'Thumbnails','temp','Databases']
    exclude_files = ["spmc.log","spmc.old.log","xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","Textures13.db"]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(USERDATA)
    ARCHIVE_CB(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def FullBackup():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'.zip'))
    exclude_dirs =  ['backupdir','cache','temp']
    exclude_files = ["spmc.log","spmc.old.log","xbmc.log","xbmc.old.log","kodi.log","kodi.old.log"]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(USERDATA)
    ARCHIVE_CB(HOME, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def TV_GUIDE_BACKUP():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'_tv_guide.zip'))
    exclude_dirs =  ['']
    exclude_files = [""]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    ARCHIVE_CB(GUIDE, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')
	
def SUPERFAVS_BACKUP():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'super_favs.zip'))
    exclude_dirs =  ['']
    exclude_files = [""]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    ARCHIVE_CB(SUPERFAVS, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def ADDON_DATA_BACKUP():
    guisuccess=1
    if not os.path.exists(USB):
        os.makedirs(USB)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(USB,title+'_addon_data.zip'))
    exclude_dirs =  ['']
    exclude_files = [""]
    message_header = "Creating full backup..."
    message_header2 = "Creating full backup..."
    message1 = "Archiving..."
    message2 = ""
    message3 = ""
    FIX_SPECIAL(ADDON_DATA)
    ARCHIVE_CB(ADDON_DATA, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
    time.sleep(1)
    dialog.ok("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')

def BACKUP_RD_TRAKT():

	if not os.path.exists(USB):
		os.makedirs(USB)
	vq = _get_keyboard( heading="Enter a name for this backup" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	backup_zip = xbmc.translatePath(os.path.join(USB,title+'RD_Trakt_Settings.zip'))

	if not os.path.exists(EXCLUDES_FOLDER):
		os.makedirs(EXCLUDES_FOLDER)

	link=OPEN_URL('http://tinyurl.com/zehrf84')
	plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
	for match in plugins:
		ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
		ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
		EXCLUDEMOVE = xbmc.translatePath(os.path.join(EXCLUDES_FOLDER,match+'_settings.xml'))
		dialog = xbmcgui.Dialog()

		if os.path.exists(ADDONSETTINGS):
			copyfile(ADDONSETTINGS, EXCLUDEMOVE)

	exclude_dirs =  [' ']
	exclude_files = [" "]
	message_header = "Creating full backup..."
	message_header2 = "Creating full backup..."
	message1 = "Archiving..."
	message2 = ""
	message3 = ""
	ARCHIVE_CB(EXCLUDES_FOLDER, backup_zip, message_header2, message1, message2, message3, exclude_dirs, exclude_files)  
	time.sleep(1)
	try:
		shutil.rmtree(EXCLUDEMOVE)
		shutil.rmdir(EXCLUDEMOVE)
	except: pass
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	maintenance.REMOVE_EMPTY_FOLDERS()
	dialog.ok("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'The backup was completed successfully!.',"Backup Location: ",'[COLOR=yellow]'+backup_zip+'[/COLOR]')


def RESTORE_RD_TRAKT():

	for file in os.listdir(USB):
		if file.endswith("RD_Trakt_Settings.zip"):
			url =  xbmc.translatePath(os.path.join(USB,file))
			addItem(file,url,30,ICON,ICON,'')

def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            try:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR lime]%s[/COLOR]'%file, '')
                fn = os.path.join(base, file)
                zipobj.write(fn, fn[rootlen:]) 
            except: pass			
    zipobj.close()
    dp.close()

def FIX_SPECIAL(url):

    HOME =  xbmc.translatePath('special://home')
    dialog = xbmcgui.Dialog()
    dp.create(AddonTitle,"[COLOR blue]Renaming paths[/COLOR]...",'', '')
    url = xbmc.translatePath('special://userdata')
    for root, dirs, files in os.walk(url):
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0,"Fixing","[COLOR dodgerblue]" + file + "[/COLOR]", "Please wait #+#+#+#+#+#+#")
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(HOME, 'special://home/')
                 f= open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()

def Restore():

	for file in os.listdir(USB):
		if file.endswith(".zip"):
			url =  xbmc.translatePath(os.path.join(USB,file))
			addItem(file,url,28,ICON,ICON,'')
			

def READ_ZIP(url):

	if not "_addon_data" in url:
		if not "tv_guide" in url:
			if not "super_favs" in url:
				if dialog.yesno(AddonTitle,"[COLOR yellow]" + url + "[/COLOR]","Do you want to restore this backup?"):
					skinswap()
					WIPE_BACKUPRESTORE()
					_out = xbmc.translatePath(os.path.join('special://','home'))
				else:
					sys.exit(1)
			else:
				if dialog.yesno(AddonTitle,"[COLOR yellow]" + url + "[/COLOR]","Do you want to restore this backup?"):
					_out = SUPERFAVS
				else:
					sys.exit(1)
		else:
			if dialog.yesno(AddonTitle,"[COLOR yellow]" + url + "[/COLOR]","Do you want to restore this backup?"):
				_out = GUIDE
			else:
				sys.exit(1)
	else:
		if dialog.yesno(AddonTitle,"[COLOR yellow]" + url + "[/COLOR]","Do you want to restore this backup?"):
			_out = ADDON_DATA
		else:
			sys.exit(1)

	_in = url
	dp.create(AddonTitle,"Restoring File:",_in,'')
	unzip(_in, _out, dp)
	
	if not "addon_data" in url:
		if not "tv_guide" in url:
			if not "super_favs" in url:
				dialog.ok(AddonTitle,'Restore Successful, please restart your Media Center for changes to take effect.','','')
				Common.killkodi()
			else:
				dialog.ok(AddonTitle,'Your Super Favourites have been restored.','','')
		else:
			dialog.ok(AddonTitle,'Your TV Guide settings have been restored.','','')
	else:
		dialog.ok(AddonTitle,'Your Addon Data settings have been restored.','','')
		


def READ_ZIP_TRAKT(url):

	dialog = xbmcgui.Dialog()
	if dialog.yesno(AddonTitle,"[COLOR smokewhite]" + url + "[/COLOR]","Do you want to restore this backup?"):
		_out = xbmc.translatePath(os.path.join('special://','home/tmp'))
		_in = url
		dp.create(AddonTitle,"Restoring File:",_in,'')
		unzip(_in, _out, dp)
		name = "[COLOR lime][B]RESTORE[/B][/COLOR]"
		link=OPEN_URL('http://tinyurl.com/zehrf84')
		plugins=re.compile('<plugin>(.+?)</plugin>').findall(link)
		for match in plugins:
			ADDONPATH = xbmc.translatePath(os.path.join(ADDON_DATA,match))
			ADDONSETTINGS = xbmc.translatePath(os.path.join(ADDONPATH,'settings.xml'))
			EXCLUDEMOVE = xbmc.translatePath(os.path.join(_out,match+'_settings.xml'))
			if os.path.exists(EXCLUDEMOVE):
				if not os.path.exists(ADDONPATH):
					os.makedirs(ADDONPATH)
				if os.path.isfile(ADDONSETTINGS):
					os.remove(ADDONSETTINGS)
				os.rename(EXCLUDEMOVE, ADDONSETTINGS)
				try:
					os.remove(EXCLUDEMOVE)
				except: pass
		dialog = xbmcgui.Dialog()
		dialog.ok(AddonTitle,'RD and Trakt Settings Successfully Restored','','')
	else:
		sys.exit(1)


		
def ListBackDel():
	addonfolder = xbmc.translatePath(os.path.join('special://','home'))
	for file in os.listdir(USB):
		if file.endswith(".zip"):
			url =  xbmc.translatePath(os.path.join(USB,file))
			addDir(file,url,29,ICON,ICON,'')
			
def DeleteBackup(url):
	if dialog.yesno(AddonTitle,"[COLOR yellow]" + url + "[/COLOR]","      [COLOR red]Do you want to delete this backup?[/COLOR]"):
		os.remove(url)
		dialog.ok(AddonTitle,"[COLOR yellow]" + url + "[/COLOR]","[COLOR green]Successfully deleted.[/COLOR]")
		
def DeleteAllBackups():
	if dialog.yesno(AddonTitle,"[COLOR red]Do you want to delete all backups?[/COLOR]"):
		shutil.rmtree(USB)
		os.makedirs(USB)
		dialog.ok(AddonTitle,"[COLOR green]All backups successfully deleted.[/COLOR]")

def skinswap():

	SKIN         =  xbmc.getSkinDir()
	KODIV        =  float(xbmc.getInfoLabel("System.BuildVersion")[:4])

	if SKIN not in ['skin.confluence', 'skin.estuary']:
		skin = 'skin.estuary' if KODIV >= 17 else 'skin.confluence'
		choice1 = xbmcgui.Dialog().yesno("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", "The skin needs to be set back to [COLOR lime]%s[/COLOR]" % skin[5:], "Before doing a fresh install", "Would you like us to do that for you?", nolabel="No, Thanks", yeslabel="Yes, Swap Skin");
		if choice1 == 1:	
			skinSwitch.swapSkins(skin)
			while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
				xbmc.sleep(200)
			xbmc.executebuiltin("Action(Left)")
			xbmc.executebuiltin("Action(Select)")
	
	skin         =  xbmc.getSkinDir()

	#CHECK IF THE SKIN IS NOT CONFLUENCE
	if skin not in ['skin.confluence','skin.estuary']:
		choice = xbmcgui.Dialog().yesno(AddonTitle, '[COLOR red][B]ERROR: AUTOSWITCH WAS NOT SUCCESFULL[/B][/COLOR]','[COLOR blue][B]CLICK YES TO MANUALLY SWITCH TO CONFLUENCE NOW[/B][/COLOR]','[COLOR blue][B]YOU CAN PRESS NO AND ATTEMPT THE AUTO SWITCH AGAIN IF YOU WISH[/B][/COLOR]', yeslabel='[B][COLOR green]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
		if choice == 1:
			xbmc.executebuiltin("ActivateWindow(appearancesettings)")
			return
		else:
			sys.exit(1)