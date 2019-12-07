#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, urllib, urllib2, re, xbmcplugin, xbmcgui, xbmcaddon

pluginhandle = int(sys.argv[1])
settings = xbmcaddon.Addon(id='plugin.video.recordedgames')
translation = settings.getLocalizedString
forceViewMode = settings.getSetting("forceViewMode") == "true"
viewMode = str(settings.getSetting("viewMode"))

amigalongplaysurl = 'http://www.recordedamigagames.org'
c64longlaysurl = 'http://c64-longplays.de'
wolurl = 'http://www.longplays.org'

def index():
	addDir('World of Longplays', 'http://www.longplays.org/news.php', 'showWOLIndex', '')
	addDir('C64 Longplays new Series', 'http://c64-longplays.de/videos.php', 'showC64VideosNew', '')
	addDir('C64 Longplays original Series', 'http://c64-longplays.de/longplays.php', 'showC64VideosOrig', '')
	addDir('Recorded Amiga Games', 'http://www.recordedamigagames.org/backup.php', 'showAmigaVideos', '')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceViewMode: xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def showWOLIndex(url):
	content = getUrl(url)
	for block in re.compile('<div class=\'submenu2c\'>(.*?)</div>', re.S|re.I|re.DOTALL).findall(content):
		for href, category in re.compile('<a[^>]*href[^>]*=[\'\"]([^\'\"]*)[\'\"]>([^<]*)</a>', re.S|re.I|re.DOTALL).findall(block):
			addDir(category, href, 'showWOLVideos', '')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceViewMode: xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def showWOLVideos(url):
	content = getUrl(url.replace('&amp;','&'))
	block = re.compile('Select a sub category:(.*?)</ul', re.S|re.I|re.DOTALL).findall(content)
	if block:
		for href, subcat in re.compile('<li>[^<]*<a[^>]*href[ ]*=[\'\"]([^\'\"]*)[\'\"]>([^<]*)</a>', re.S|re.I|re.DOTALL).findall(block[0]):
			if wolurl not in href: href = wolurl + '/' + href
			addDir(subcat, href, 'showWOLVideos', '')
	for table in re.compile('<table[^>]*id=\'myTable\'[^>]*>(.*?)</table>', re.S|re.I|re.DOTALL).findall(content):
		for block in re.compile('<tr[^>]*>(.*?)</tr>', re.S|re.I|re.DOTALL).findall(table):
			row = re.compile('<td[^>]*>(.*?)</td>', re.S|re.I|re.DOTALL).findall(block)
			if len(row) == 10:
				a, date, b, link, duration, size, lang, c, player, d = row
				(href, title) = re.compile('<a[^>]*href=[\'\"]([^\'\"]*)[\'\"][^>]*>([^<]*)</a>', re.S|re.I|re.DOTALL).findall(link)[0]
				#name = date + ' - ' + title + ' (' + duration +')'
				name = cleanTitle(title) + ' (' + duration +')'
				if wolurl not in href: href = wolurl + '/' + href
				addLink(name, href, 'playWOLVideo', '')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceViewMode: xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def playWOLVideo(url):
	content = getUrl(url.replace('&amp;','&'))
	ytid = re.compile('<a[^>]*href=[\'\"][^\'\"]*www.youtube.com/watch\?v=([^\'\"]*)&[^\'\"]*[\'\"][^>]*>Homepage</a>', re.S|re.I|re.DOTALL).findall(content)
	if ytid:
		ytpath = "plugin://%s/?path=/root/video&action=play_video&videoid=%s" % ('video/YouTube' if xbmc.getCondVisibility("System.Platform.xbox") else 'plugin.video.youtube', ytid[0])
		listitem = xbmcgui.ListItem(path=ytpath)
		return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

	for vidurl in re.compile('Download \(right click save as\):</strong>[^<]*<br[^>]*>[^<]*<a[^>]*href=[\'\"]([^\'\"]*)[\'\"][^>]*>', re.S|re.I|re.DOTALL).findall(content):
		if wolurl not in vidurl: vidurl = wolurl + '/' + vidurl
		listitem = xbmcgui.ListItem(path=vidurl.replace('&amp;','&'))
		return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	
def showC64VideosNew(url):
	content = getUrl(url)
	table = re.compile('<table class="sortable" id="anyid">.*?</table>', re.S|re.I|re.DOTALL).findall(content)
	for k, f in enumerate(re.compile('<td[^>]*>([^<]*)</td>[^<]*<td[^>]*>([^<]*)</td>[^<]*<td>[^<]*<a href="([^<]+?)">([^<]+?)</a>', re.S|re.I|re.DOTALL).findall(table[0])):
		num, year, href, name = f
		addLink('(' + num + ') ' + year + ' ' + name, href, 'playC64Video', '')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceViewMode: xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def showC64VideosOrig(url):
	content = getUrl(url)
	table = re.compile('<table class="sortable" id="anyid">.*?</table>', re.S|re.I|re.DOTALL).findall(content)
	for k, f in enumerate(re.compile('<td[^>]*>([^<]*)</td>[^<]*<td>[^<]*<a href="([^<]+?)">([^<]+?)</a>', re.S|re.I|re.DOTALL).findall(table[0])):
		num, href, name = f
		addLink('(' + num + ') ' + name, href, 'playC64Video', '')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceViewMode: xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def showAmigaVideos(url):
	content = getUrl(url)
	for k, f in enumerate(re.compile('<a href="([^<]+?)">([^<]+?)</a>', re.DOTALL).findall(content)):
		href, name = f
		href = amigalongplaysurl + href
		addLink(name, href, 'playAmigaVideo', '')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceViewMode: xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def playAmigaVideo(url):
	print 'Amiga: ' + url
	listitem = xbmcgui.ListItem(path=url.replace(' ', '%20'))
	return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def playC64Video(url):
	response = urllib2.urlopen(urllib2.Request(url), timeout=30)
	url = response.geturl()
	response.close()
	print 'C64: ' + url
	listitem = xbmcgui.ListItem(path=url.replace(' ', '%20'))
	return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def cleanTitle(title):
	title = re.sub('<[^>]*>', ' ', title)
	title = re.sub('&#\d{3};', ' ', title)
	title = title.replace('&lt;','<').replace('&gt;','>').replace('&amp;','&').replace('&quot;','"').replace('&szlig;','ß').replace('&ndash;','-')
	title = title.replace('&Auml;','Ä').replace('&Uuml;','Ü').replace('&Ouml;','Ö').replace('&auml;','ä').replace('&uuml;','ü').replace('&ouml;','ö').replace('&nbsp;', ' ')
	title = title.replace('„','"').replace('“','"')
	title = re.sub('\s+', ' ', title)
	return title.strip()

def getUrl(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
	response = urllib2.urlopen(req, timeout=30)
	link = response.read()
	response.close()
	return link 

def parameters_string_to_dict(parameters):
	''' Convert parameters encoded in a URL to a dict. '''
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split("&")
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

def addLink(name, url, mode, image):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	return xbmcplugin.addDirectoryItem(handle=pluginhandle, url=u, listitem=liz)

def addDir(name, url, mode, iconimage):
	name = '* ' + name
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode)
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	return xbmcplugin.addDirectoryItem(handle=pluginhandle, url=u, listitem=liz, isFolder=True)

params = parameters_string_to_dict(sys.argv[2])
mode = params.get('mode')
url = params.get('url')
if type(url)==type(str()): url = urllib.unquote_plus(url)

if   mode == 'showC64VideosNew': showC64VideosNew(url)
elif mode == 'showC64VideosOrig': showC64VideosOrig(url)
elif mode == 'showAmigaVideos': showAmigaVideos(url)
elif mode == 'playC64Video': playC64Video(url)
elif mode == 'playAmigaVideo': playAmigaVideo(url)
elif mode == 'showWOLIndex' : showWOLIndex(url)
elif mode == 'showWOLVideos' : showWOLVideos(url)
elif mode == 'playWOLVideo' : playWOLVideo(url)
else: index()
