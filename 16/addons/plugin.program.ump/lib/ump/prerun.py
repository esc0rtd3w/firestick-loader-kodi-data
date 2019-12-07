import xbmc
import sys

def direct():
	xbmc.executebuiltin('Dialog.Close(all,true)')
	from sys import argv
	query=argv[2][1:]
	#run only on root
	if not "module=" in query and not "page=" in query:
		from dom import check
		from defs import addon_setxml,addon_bsetxml,kodi_setxml,kodi_bsetxml,kodi_favxml,kodi_bfavxml
		check(addon_setxml,addon_bsetxml)
		check(kodi_setxml,kodi_bsetxml)
		check(kodi_favxml,kodi_bfavxml)
	
def run(ump):
	#runs on root page only
	try:
		kodimajor=int(xbmc.getInfoLabel( "System.BuildVersion" ).split(".")[0])
	except:
		konimajor=0
	if kodimajor<13:
		ump.dialog.ok("OLD XBMC/KODI VERSION","This addon requires Minimum XBMC/Kodi version 13,\n your current version is %d.\n You should upgrade your kodi version to use UMP."%kodimajor)
		ump.shut()
		ump._clean()
		sys.exit()
	if ump.module == "ump" and ump.page == "root":
		from ump.providers import update_settings
		# syncronize providers to settings.xml
		update_settings()
	else:
		#runs on each addon run
		pass

	if not ump.handle=="-1":
		#runs on each time addon is browsed
		from webtunnel import check_health
		check_health(ump)