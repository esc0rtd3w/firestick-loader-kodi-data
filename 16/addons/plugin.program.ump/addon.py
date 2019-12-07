try:
	import sys
	import os
	import xbmcgui
	import xbmcplugin
	import xbmcaddon
	import xbmc

	addon = xbmcaddon.Addon('plugin.program.ump')
	addon_ldir = xbmc.translatePath( os.path.join(addon.getAddonInfo('path'),"lib") )
	sys.path.append(addon_ldir)
	from ump import prerun
	prerun.direct()
	from ump.defs import addon_ldir
	from ump.defs import arturi

	from ump import api
	from ump import postrun
	from ump import providers
	from ump import ui
	#bookmark.resolve()
	ump=api.ump()
	prerun.run(ump)
	from ump import cloud
	ump.add_log("HANDLE       : %s"%str(ump.handle))
	ump.add_log("MODULE       : %s"%str(ump.module))
	ump.add_log("PAGE         : %s"%str(ump.page))
	#ump.add_log("ARGS         : " + str(ump.args))
	ump.add_log("CONTENT_TYPE : %s"%str(ump.content_type))
	#print "INFO         : " + str(ump.info)
	#print "ART          : " + str(ump.art)
	indexers=providers.find(ump.content_type,"index")
	url_providers=providers.find(ump.content_type,"url")
	link_providers=providers.find(ump.content_type,"link")
	if ump.module == "ump":
		if ump.page == "root":
			for provider in indexers:
				provider_type,provider_cat,provider_name=provider
				if ump.content_type == "ump":content_type=provider_type
				else: content_type = ump.content_type
				img=arturi+provider_name+".png"
				ump.index_item(provider_name.title(),module=provider_name,icon=img,thumb=img,content_type=content_type)
			ump._do_container()
	elif ump.page== "urlselect":
		if not addon.getSetting("tn_chk_url_en").lower()=="false":
			from ump import webtunnel
			webtunnel.check_health(ump,True)
		if len(link_providers)==0:
			ump.dialog.notification("ERROR","There is no available providers for %s"%ump.content_type)
		else:
			for provider in link_providers:
				try:
					provider=providers.load(ump.content_type,"link",provider[2])
				except Exception, e:
					ump.notify_error(e)
					continue
				ump.tm.add_queue(provider.run, (ump,),pri=10)
			ump.window.doModal()
	elif providers.is_loadable(ump.content_type,"index",ump.module,indexers)==1:
		try:
			providers.load(ump.content_type,"index",ump.module).run(ump)
			ump._do_container()
		except Exception,e:
			ump.notify_error(e)
	elif providers.is_loadable(ump.content_type,"index",ump.module,indexers)==2:
		try:
			providers.load("ump","index",ump.module).run(ump)
			ump._do_container()
		except Exception,e:
			ump.notify_error(e)
	postrun.run(ump)		
	ump.shut()
	ump.add_log("PUBLISH      : %s"%str(ump.pub))
	if int(ump.handle)==-1:
		ump.add_log("INFO MEDIA_TYPE: %s"%ump.info.get("mediatype","other"))
	else:
		ump.add_log("CONTAINER MEDIA_TYPE: %s"%ump.container_mediatype)
	ump._clean()
	ump.add_log("UMP:EOF")
except Exception,e:
	import xbmcaddon,xbmc,sys,os
	addon = xbmcaddon.Addon('plugin.program.ump')
	addon_ldir = xbmc.translatePath( os.path.join(addon.getAddonInfo('path'),"lib") )
	sys.path.append(addon_ldir)
	from ump import cloud
	if "ump" in globals():
		umplog=ump.log
		ump.shut()
		ump._clean()
	else:
		umplog="UMP has not initialized yet"
	
	newer=cloud.get_latest()
	if newer:
		import xbmcgui
		dialog = xbmcgui.Dialog()
		dialog.ok("UMPCRASH","You are currently running an OLD version of UMP (%s), latest is %s, please update UMP!"%(addon.getAddonInfo('version'),newer))
	else:
		cloud.collect_log("UMPCRASH","OOPS!","It looks like UMP has crashed, do you want to send logs to developer?",umplog,e)