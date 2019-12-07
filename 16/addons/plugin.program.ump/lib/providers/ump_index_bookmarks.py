import json
import os

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

from ump import bookmark


addon = xbmcaddon.Addon('plugin.program.ump')
addon_dir = xbmc.translatePath( addon.getAddonInfo('path') )

def run(ump):
	favs=bookmark.load()[1]
	ccat=ump.content_type
	if ump.page=="old":
		ump.dialog.ok("OLD VERSION BOOKMARKS","This bookmark has been created with an old version of UMP and needs to be recreated. Right click the bookmark and select 'Remove from Bookmarks'. And then go to you favorite indexer and create bookmark again.\nSorry for any inconvenience")
		return
	for fav in favs:
		wid,name,thumb,data,cat,module,page,args,info,art=fav
		if cat==ccat or ccat=="ump":
			ump.content_type=cat
			ump.info=info
			ump.art=art
			commands=[
			('Detailed Info', 'Action(Info)'),
			('Rename Bookmark',"RunScript(%s,renfav,%s,%s,%s)"%(os.path.join(addon_dir,"lib","ump","script.py"),json.dumps(name),json.dumps(thumb),json.dumps(data))),
			('Remove From Bookmarks',"RunScript(%s,delfav,%s,%s,%s)"%(os.path.join(addon_dir,"lib","ump","script.py"),json.dumps(name),json.dumps(thumb),json.dumps(data))),
			("Addon Settings","Addon.OpenSettings(plugin.program.ump)")
			]
			if not "index" in info:
				name="[COLOR red]OLD![/COLOR] %s"%name
				page="old"
				module="bookmarks"
			ump.index_item(name,page,args,module,thumb,thumb,info,art,commands,True,True,not wid is None)