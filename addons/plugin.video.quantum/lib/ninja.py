'''
These addons are only possible because websites are open and allow us to view them for free.

These addons are also only possible due to the numerous hours the kodi developers and addon developers put in to ensure that
you, the user can have as much content as you need.

However, it is incredibly clear that numerous cunts exist in the community and like nothing than to rip of the code of us,
the hard working developers. You are known, we are watching.

This section was kindly donated by the dev of the addon - oneil, give him a follow on twitter to say thanks for this amazing section - @oneilxm_uk'''



import sys, os, xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib, urllib2, cookielib, re

settings = xbmcaddon.Addon(id='plugin.video.quantum')
cookiejar = cookielib.LWPCookieJar()
cookie_handler = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_handler)
addon_id = 'plugin.video.quantum'
selfAddon = xbmcaddon.Addon(id=addon_id)
Adult_Pass = selfAddon.getSetting('Adult')
Adult_Default = selfAddon.getSetting('Porn_Pass')
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
Dialog = xbmcgui.Dialog()


def CATEGORIES():
	if Adult_Pass == Adult_Default:
		link = openURL('http://www.perfectgirls.net/')
		match = re.compile('<a href="/category/([0-9][0-9])/(.*)">(.*)</a>').findall(link)
		addDir('[COLOR red]Latest[/COLOR]', 'http://www.perfectgirls.net/',1, icon, 1)
		addDir('---', '',1, '', 1)
		for page_id, channame, name in match:
			addDir(name,
				('http://www.perfectgirls.net/category/' + page_id + '/' + channame),
				1401, icon, 1)
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
	else:
		addDir('[COLORred][B]Password will now be changed monthly to keep it fresh !!![/B][/COLOR]','','','','')
		addDir('[COLORred]Unfortunately you need to enter a password for this section,[/COLOR]','','','','')
		addDir('[COLORwhite]as it contains adult content. You can obtain this[/COLOR]','','','','')
		addDir('[COLORblue]from Our facebook group[/COLOR]','','','','')
		xbmcplugin.endOfDirectory(int(sys.argv[1]))

def VIDEOLIST(url):
    pg = 'http://www.perfectgirls.net/'
    link = openURL(url)
    match = re.compile('<div class="list__item_link"><a href="(.+?)".+?title="(.+?)".+?data-original="(.+?)".+?<time>(.+?)</time>',re.DOTALL).findall(link)
    for url2,name,img,length in match:
        import clean_name
        name = clean_name.clean_name(name)
        addLink('[COLORred]'+length+'[/COLOR] - '+name,pg+url2,1402,icon)
    next = re.compile('<a class="btn_wrapper__btn" href="([^"]*)">Next</a>').findall(link)
    for item in next:
        if url[-1] in '0123456789':
            url3 = url[:-1]+item
        else:
            url3 = url+'/'+item
        addDir('Next Page',url3,1401,icon,'')


def PLAYVIDEO(url):
	sources = []
	link = openURL(url)
	match = re.compile('<source src="(.+?)".+?res="(.+?)"').findall(link)
	for playlink,quality in match:
		sources.append({'quality': quality, 'playlink': playlink})
		if len(sources) == len(match):
			choice = Dialog.select('Select Playlink',[link["quality"] for link in sources])
			if choice != -1:
				playlink = sources[choice]['playlink']
				isFolder=False
				xbmc.Player().play(playlink)


def addLink(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)\
        + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="icon.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=False)
    return ok


def addDir(name, url, mode, iconimage, page):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) +\
        "&name=" + urllib.quote_plus(name) + "&page=" + str(page)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="icon.png",
                           thumbnailImage=iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=True)
    return ok


def openURL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link
