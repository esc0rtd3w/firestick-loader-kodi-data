import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import plugintools
import maintenance
packagesdir    =  xbmc.translatePath(os.path.join('special://home/addons/packages',''))
thumbnails    =  xbmc.translatePath('special://home/userdata/Thumbnails')
dialog = xbmcgui.Dialog()
setting = plugintools.get_setting
filesize = int(setting('filesize_alert'))
filesize_thumb = int(setting('filesizethumb_alert'))
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
print("MAINTENANCE SETTINGS", filesize, filesize_thumb)
total_size2 = 0
total_size = 0
count = 0


for dirpath, dirnames, filenames in os.walk(packagesdir):
	count = 0
	for f in filenames:
		count += 1
		fp = os.path.join(dirpath, f)
		total_size += os.path.getsize(fp)
total_sizetext = "%.0f" % (total_size/1024000.0)
	
if int(total_sizetext) > filesize:
	choice2 = xbmcgui.Dialog().yesno("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'The packages folder is [COLOR lime]' + str(total_sizetext) +' MB [/COLOR] - [COLOR lime]' + str(count) + '[/COLOR] zip files', 'The folder can be cleaned to save space...', 'Do you want to clean it now?', yeslabel='Yes',nolabel='No')
	if choice2 == 1:
		maintenance.AutoPackages()
			
for dirpath2, dirnames2, filenames2 in os.walk(thumbnails):
	for f2 in filenames2:
		fp2 = os.path.join(dirpath2, f2)
		total_size2 += os.path.getsize(fp2)
total_sizetext2 = "%.0f" % (total_size2/1024000.0)

if int(total_sizetext2) > filesize_thumb:
	choice2 = xbmcgui.Dialog().yesno("[B][COLOR yellow]StarTec Maintenance[/COLOR][/B]", 'The thumbnail folder is [COLOR lime]' + str(total_sizetext2) + ' MB   [/COLOR]', 'The folder can be cleaned to save space...', 'Do you want to clean it now?', yeslabel='Yes',nolabel='No')
	if choice2 == 1:
		maintenance.AutoThumbs()

