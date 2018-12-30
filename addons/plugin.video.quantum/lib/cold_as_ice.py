import process, re, urlresolver, xbmcgui, xbmcplugin, sys, xbmcaddon

addon_id = 'plugin.video.quantum'
ADDON = xbmcaddon.Addon(id=addon_id)
Adult_Pass = ADDON.getSetting('Adult')
Adult_Default = ADDON.getSetting('Porn_Pass')

def Cold_Menu():
	link=process.OPEN_URL('http://g10.x10host.com/coldasice/Index.txt')
	match= re.compile('<link>(.+?)</link><thumbnail>(.+?)</thumbnail><title>(.+?)</title>').findall(link)
	for url,iconimage,name in match:
		if 'Movie' in name:
			pass
		elif 'N A K E D' in name:
			if Adult_Pass == Adult_Default:
				process.Menu(name,url,1801,iconimage,'','','')
		elif not 'http' in iconimage:
			iconimage=''
		else:
			process.Menu(name,url,1801,iconimage,'','','')
		
def GetContent(url,iconimage):
        link=process.OPEN_URL(url)
        match= re.compile('<link>(.+?)</link><thumbnail>(.+?)</thumbnail><title>(.+?)</title>').findall(link)
        for url,iconimage,name in match:
                if not 'http' in iconimage:iconimage=''
                if '/coldasice/' in url:
                    process.Menu(name,url,1801,iconimage,'','','')
                elif 'letwatch' in url:
                    name = '[COLORred]*[/COLOR]'+name
                    from freeview.freeview import addLink
                    addLink(name,url,1802,iconimage)
                else:
                    from freeview.freeview import addLink
                    addLink(name,url,1802,iconimage)

def PLAYLINK(name,url,iconimage):
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
        liz.setPath(stream_url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)