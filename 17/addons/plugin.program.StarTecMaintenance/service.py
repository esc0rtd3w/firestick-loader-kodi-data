import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
import urllib2,urllib
import re
import time
import common as Common
import plugintools
from random import randint
from datetime import date
import calendar
import maintenance
import maint

my_date = date.today()
today = calendar.day_name[my_date.weekday()]
my_addon = xbmcaddon.Addon()
addon_id   = 'plugin.program.StarTecMaintenance'
AddonTitle = "StarTec Maintenance"

if my_addon.getSetting('clearcache') == 'true':
	maintenance.AutoCache()

xbmc.executebuiltin ( 'Runscript("special://home/addons/plugin.program.StarTecMaintenance/maint.py")' )
