## STARTUP SERVICE

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import uservar
from datetime import date, datetime, timedelta
from resources.libs import maintenance as clean

AUTOCLEANUP    = clean.getS('autoclean')
AUTOCACHE      = clean.getS('clearcache')
AUTOPACKAGES   = clean.getS('clearpackages')

if AUTOCLEANUP == 'true':
	if AUTOCACHE == 'true': clean.log('[AUTO CLEAN UP][Cache: on]'); clean.clearCache()
	else: clean.log('[AUTO CLEAN UP][Cache: off]')
	if AUTOPACKAGES == 'true': clean.log('[AUTO CLEAN UP][Packages: on]'); clean.clearPackages('startup')
	else: clean.log('[AUTO CLEAN UP][Packages: off]')
else: clean.log('[AUTO CLEAN UP: off]')

