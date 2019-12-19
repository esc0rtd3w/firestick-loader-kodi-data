################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
import time
from datetime import date, datetime, timedelta
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from string import digits

######################################################################################################################################################
##
## GLOBAL
##
######################################################################################################################################################

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = xbmcaddon.Addon(ADDON_ID)
DIALOG         = xbmcgui.Dialog()
HOME           = xbmc.translatePath('special://home/')
LOG            = xbmc.translatePath('special://logpath/')
PROFILE        = xbmc.translatePath('special://profile/')
ADDONS         = os.path.join(HOME, 'addons')
USERDATA       = os.path.join(HOME, 'userdata')
PLUGIN         = os.path.join(ADDONS, ADDON_ID)
PACKAGES       = os.path.join(ADDONS, 'packages')
ADDONDATA      = os.path.join(USERDATA, 'addon_data', ADDON_ID)
ADVANCED       = os.path.join(USERDATA, 'advancedsettings.xml')
SOURCES        = os.path.join(USERDATA, 'sources.xml')
FAVOURITES     = os.path.join(USERDATA, 'favourites.xml')
PROFILES       = os.path.join(USERDATA, 'profiles.xml')
THUMBS         = os.path.join(USERDATA, 'Thumbnails')
DATABASE       = os.path.join(USERDATA, 'Database')
FANART         = os.path.join(PLUGIN, 'fanart.jpg')
ICON           = os.path.join(PLUGIN, 'icon.png')
WIZLOG         = os.path.join(ADDONDATA, 'wizard.log')

######################################################################################################################################################
##
## FUNCTIONS X 15
##
######################################################################################################################################################

def getS(name):
	try: return ADDON.getSetting(name)
	except: return False

def setS(name, value):
	try: ADDON.setSetting(name, value)
	except: return False

def openS():
	ADDON.openSettings();


def LogNotify(title, message, times=2000, icon=ICON,sound=False):
	DIALOG.notification(title, message, icon, int(times), sound)

def log(log):
	xbmc.log("[%s]: %s" % (ADDONTITLE, log))
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(WIZLOG): f = open(WIZLOG, 'w'); f.close()
	with open(WIZLOG, 'r+') as f:
		line = "[%s %s] %s" % (datetime.now().date(), str(datetime.now().time())[:8], log)
		content = f.read()
		f.seek(0, 0)
		f.write(line.rstrip('\r\n') + '\n' + content)

def addonId(add):
	return xbmcaddon.Addon(id=add)

def addonInfo(add, info):
	addon = addonId(add)
	return addon.getAddonInfo(info)

def clearPackages(over=None):
	if os.path.exists(PACKAGES):
		try:	
			for root, dirs, files in os.walk(PACKAGES):
				file_count = 0
				file_count += len(files)
				# Count files and give option to delete
				if file_count > 0:
					if over: yes=1
					else: yes=DIALOG.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?", nolabel='No, Cancel',yeslabel='Yes, Remove')
					if yes:
						for f in files:	os.unlink(os.path.join(root, f))
						for d in dirs: shutil.rmtree(os.path.join(root, d))
						LogNotify(ADDONTITLE,'[COLOR yellow]Packages And Thumbnails Purged:[/COLOR] [COLOR red]Success[/COLOR]!')
				else: LogNotify(ADDONTITLE,'[COLOR yellow]Packages:[/COLOR] [COLOR red]None Found![/COLOR]')
		except: LogNotify(ADDONTITLE,'[COLOR yellow]Packages:[/COLOR] [COLOR red]Error[/COLOR]!')
	else: LogNotify(ADDONTITLE,'[COLOR yellow]Packages:[/COLOR] [COLOR red]None Found![/COLOR]')

def clearCache():
	PROFILEADDONDATA = os.path.join(PROFILE,'addon_data')
	cachelist = [
		(PROFILEADDONDATA),
		(ADDONDATA),
		(os.path.join(HOME,'cache')),
		(os.path.join(HOME,'temp')),
		(os.path.join(USERDATA, 'Thumbnails')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
		(os.path.join(ADDONDATA,'script.module.simple.downloader')),
		(os.path.join(ADDONDATA,'plugin.video.itv','Images')),
		(os.path.join(PROFILEADDONDATA,'script.module.simple.downloader')),
		(os.path.join(PROFILEADDONDATA,'plugin.video.itv','Images')),
		(os.path.join(ADDONDATA, 'plugin.video.phstreams', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.bob', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.specto', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.genesis', 'cache.db')),
		(os.path.join(ADDONDATA, 'plugin.video.exodus', 'cache.db')),
		(os.path.join(DATABASE,  'onechannelcache.db')),
		(os.path.join(DATABASE,  'saltscache.db')),
		(os.path.join(DATABASE,  'saltshd.lite.db'))]
		
	delfiles = 0

	for item in cachelist:
		if os.path.exists(item) and not item in [ADDONDATA, PROFILEADDONDATA]:
			for root, dirs, files in os.walk(item):
				file_count = 0
				file_count += len(files)
				if file_count > 0:
					for f in files:
						if not f in ['kodi.log', 'tvmc.log', 'spmc.log', 'xbmc.log']:
							try:
								os.unlink(os.path.join(root, f))
							except:
								pass
						else: log('Ignore Log File: %s' % f)
					for d in dirs:
						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
							log("[COLOR red][Success]  %s Files Removed From %s [/COLOR]" % (str(file_count), os.path.join(item,d)))
						except:
							log("[COLOR red][Failed] To Wipe Cache In: %s [/COLOR]" % os.path.join(item,d))
		else:
			for root, dirs, files in os.walk(item):
				for d in dirs:
					if 'cache' in d.lower():
						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
							log("[COLOR red][Success] Wiped %s [/COLOR]" % os.path.join(item,d))
						except:
							log("[COLOR red][Failed] To Wipe Cache In: %s [/COLOR]" % os.path.join(item,d))

	LogNotify(ADDONTITLE,'[COLOR lime]Cache:[/COLOR] [COLOR red] %s Items Removed[/COLOR]' % delfiles)

