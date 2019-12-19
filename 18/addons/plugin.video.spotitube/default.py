#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import urlparse
import json
import xbmcvfs
import random
import socket
import datetime
import time
from operator import itemgetter
from StringIO import StringIO
import gzip
import ssl

try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	# Legacy Python that doesn't verify HTTPS certificates by default
	pass
else:
	# Handle target environment that doesn't support HTTPS verification
	ssl._create_default_https_context = _create_unverified_https_context

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()
socket.setdefaulttimeout(40)
translation = addon.getLocalizedString
addonPath = xbmc.translatePath(addon.getAddonInfo('path')).decode('utf-8')
dataPath = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
region = xbmc.getLanguage(xbmc.ISO_639_1, region=True).split("-")[1]
icon = os.path.join(addonPath, 'icon.png').decode('utf-8')
defaultFanart = os.path.join(addonPath, 'fanart.jpg').decode('utf-8')
pic = os.path.join(addonPath, 'resources/media/')
blacklist = addon.getSetting("blacklist").split(',')
infoEnabled = addon.getSetting("showInfo") == "true"
infoType = addon.getSetting("infoType")
infoDelay = int(addon.getSetting("infoDelay"))
infoDuration = int(addon.getSetting("infoDuration"))
useThumbAsFanart = addon.getSetting("useThumbAsFanart") == 'true'
cachePath = xbmc.translatePath(os.path.join(addon.getSetting("cacheDir")))
cacheDays = int(addon.getSetting("cacheLong"))
deezerSearchDisplay = str(addon.getSetting("deezerSearch_count"))
deezerVideosDisplay = str(addon.getSetting("deezerVideos_count"))
itunesShowSubGenres = addon.getSetting("itunesShowSubGenres") == 'true'
itunesForceCountry = addon.getSetting("itunesForceCountry") == 'true'
itunesCountry = addon.getSetting("itunesCountry")
spotifyForceCountry = addon.getSetting("spotifyForceCountry") == 'true'
spotifyCountry = addon.getSetting("spotifyCountry")
forceView = addon.getSetting("forceView") == 'true'
viewIDGenres = str(addon.getSetting("viewIDGenres"))
viewIDPlaylists = str(addon.getSetting("viewIDPlaylists"))
viewIDVideos = str(addon.getSetting("viewIDVideos"))
urlBaseBP = "https://www.beatport.com"
urlBaseBB = "https://www.billboard.com"
urlBaseDDP = "http://www.dj-playlist.de/"
urlBaseHypem = "https://hypem.com"
urlBaseOC = "http://www.officialcharts.com"
urlBaseSCC = "https://spotifycharts.com/"
urlBaseSTUN = "https://api.tunigo.com/v3/space/"
#REtoken2 = "AIzaSyBT8_HQW02I1hNSeQdfnapsReDda9Mz0N4"
token = "AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo"
xbmcplugin.setContent(int(sys.argv[1]), 'musicvideos')
	
if itunesForceCountry and itunesCountry:
	iTunesRegion = itunesCountry
else:
	iTunesRegion = region
	
if spotifyForceCountry and spotifyCountry:
	spotifyRegion = spotifyCountry
else:
	spotifyRegion = region
	
if not os.path.isdir(dataPath):
	os.makedirs(dataPath)
	
if cachePath == "":
	addon.setSetting(id='cacheDir', value='special://profile/addon_data/'+addon.getAddonInfo('id')+'/cache')
elif cachePath != "" and not os.path.isdir(cachePath) and not cachePath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')):
	os.mkdir(cachePath)
elif cachePath != "" and not os.path.isdir(cachePath) and cachePath.startswith(('smb://', 'nfs://', 'upnp://', 'ftp://')):
	addon.setSetting(id='cacheDir', value='special://profile/addon_data/'+addon.getAddonInfo('id')+'/cache') and os.mkdir(cachePath)
elif cachePath != "" and os.path.isdir(cachePath):
		xDays = cacheDays # Days after which Files would be deleted
		now = time.time() # Date and time now
		for root, dirs, files in os.walk(cachePath):
			for name in files:
				filename = os.path.join(root, name).decode('utf-8')
				try:
					if os.path.exists(filename):
						if os.path.getmtime(filename) < now - (60*60*24*xDays): # Check if CACHE-File exists and remove CACHE-File after defined xDays
							os.unlink(filename)
				except: pass
	
def index():
	addDir(translation(40203), "", "SearchDeezer", pic+'deepsearch.gif')
	addDir(translation(40101), "", "beatportMain", pic+'beatport.png')
	addDir(translation(40102), "", "billboardMain", pic+'billboard.png')
	addDir(translation(40103), "", "ddpMain", pic+'ddp-international.png')
	addDir(translation(40104), "", "hypemMain", pic+'hypem.png')
	addDir(translation(40105), "", "itunesMain", pic+'itunes.png')
	addDir(translation(40106), "", "ocMain", pic+'official.png')
	addDir(translation(40107), "", "spotifyMain", pic+'spotify.png')
	addDir(translation(40202), "", "Settings", pic+'settings.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	
def beatportMain():
	content = cache('https://pro.beatport.com', 30)
	content = content[content.find('<div class="mobile-menu-body">')+1:]
	content = content[:content.find('<!-- End Mobile Touch Menu -->')]
	match = re.compile('<a href="(.*?)" class="(.*?)" data-name=".+?">(.*?)</a>', re.DOTALL).findall(content)
	allTitle = translation(40135)
	addAutoPlayDir(allTitle, urlBaseBP+"/top-100", "listBeatportVideos", pic+'beatport.png', "", "browse")
	for genreURL, genreTYPE, genreTITLE in match:
		topUrl = urlBaseBP+genreURL+'/top-100'
		title = cleanTitle(genreTITLE)
		addAutoPlayDir(title, topUrl, "listBeatportVideos", pic+'beatport.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listBeatportVideos(type, url, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	spl = content.split('bucket-item ec-item track')
	count = 0
	pos = 1
	for i in range(1,len(spl),1):
		count += 1
		entry = spl[i]
		artist = re.compile('data-artist=".+?">(.*?)</a>', re.DOTALL).findall(entry)[0]
		song = re.compile('<span class="buk-track-primary-title" title=".+?">(.*?)</span>', re.DOTALL).findall(entry)[0]
		remix = re.compile('<span class="buk-track-remixed">(.*?)</span>', re.DOTALL).findall(entry)
		if "(original mix)" in song.lower():
			song = song.lower().split('(original mix)')[0]
		song = cleanTitle(song)
		if "(feat." in song.lower() and " feat." in song.lower():
			song = song.split(')')[0]+')'
		elif not "(feat." in song.lower() and " feat." in song.lower():
			firstTitle = song.lower().split(' feat.')[0]
			secondTitle = song.lower().split(' feat.')[1]
			song = firstTitle+' (feat.'+secondTitle+')'
		if remix and not "original" in remix[0].lower():
			newRemix = remix[0].replace('[', '').replace(']', '')
			song += ' ['+newRemix.strip()+']'
		title = cleanTitle(artist.strip()+" - "+song.strip())
		newName = title
		try:
			oldDate = re.compile('<p class="buk-track-released">(.*?)</p>', re.DOTALL).findall(entry)[0]
			convert = time.strptime(oldDate,'%Y-%m-%d')
			newDate = time.strftime('%d.%m.%Y',convert)
			newName += '   [COLOR deepskyblue]['+str(newDate)+'][/COLOR]'
		except: pass
		try:
			thumb = re.compile('data-src="(http.*?.jpg)"', re.DOTALL).findall(entry)[0]
			thumb = thumb.split('image_size')[0]+'image/'+thumb.split('/')[-1]
			#thumb = thumb.replace("/30x30/","/500x500/").replace("/60x60/","/500x500/").replace("/95x95/","/500x500/").replace("/250x250/","/500x500/")
		except: thumb = pic+'noimage.png'
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "browse":
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+newName
			addLink(name, title.replace(" - ", " "), "playYTByTitle", thumb)
		else:
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
			musicVideos.append([title, url, thumb])
			if limit and int(limit)==pos:
				break
			pos += 1
	if type == "browse":
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def billboardMain():
	addAutoPlayDir(translation(40108), urlBaseBB+"/charts/hot-100", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	addAutoPlayDir(translation(40109), urlBaseBB+"/charts/billboard-200", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	addDir(translation(40110), "", "listBillboardArchiveYears", pic+'billboard.png')
	addDir(translation(40111), "genre", "listBillboardCharts", pic+'billboard.png')
	addDir(translation(40112), "country", "listBillboardCharts", pic+'billboard.png')
	addDir(translation(40113), "other", "listBillboardCharts", pic+'billboard.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listBillboardArchiveYears():
	for i in range(datetime.date.today().year,1957,-1):
		addDir(str(i), urlBaseBB+"/archive/charts/"+str(i), "listBillboardAR_Genres", pic+'billboard.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listBillboardAR_Genres(url):
	xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
	UN_Supported = ['album', 'artist 100', 'billboard 200', 'greatest of all time', 'next big', 'social 50', 'tastemaker', 'uncharted'] # if Artist and Song are the same or if Album
	content = cache(url, 30)
	content = content[content.find('<li class="year-list__decade last">')+1:]
	content = content[:content.find('<aside class="simple-page__body-supplementary">')]
	match = re.compile('<a href="/archive/charts/(.*?)">(.*?)</a>', re.DOTALL).findall(content)
	for url2, title in match:
		if any(x in title.strip().lower() for x in UN_Supported):
			continue
		addAutoPlayDir(cleanTitle(title), urlBaseBB+'/archive/charts/'+url2, "listBillboardAR_Videos", pic+'billboard.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listBillboardAR_Videos(type, url, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	musicIsolated = set()
	content = cache(url, 30)
	content = content[content.find('<tbody>')+1:]
	content = content[:content.find('</tbody>')]
	spl = content.split('<tr>')
	pos = 1
	for i in range(1,len(spl),1):
		entry = spl[i]
		try:
			song = re.findall('<t.+?>(.*?)</td>',entry,re.S)[1]
			artist = re.findall('<t.+?>(.*?)</td>',entry,re.S)[2]
		except: pass
		if song == "" or artist == "":
			continue
		if song.strip().lower() != artist.strip().lower():
			title = cleanTitle(artist.strip()+" - "+song.strip())
			newTitle = song.strip().lower()
			if newTitle in musicIsolated:
				continue
			musicIsolated.add(newTitle)
			if title.isupper():
				title = title.title()
			filtered = False
			for entry2 in blacklist:
				if entry2.strip().lower() and entry2.strip().lower() in title.lower():
					filtered = True
			if filtered:
				continue
			if type == "browse":
				addLink(title, title.replace(" - ", " "), "playYTByTitle", "")
			else:
				url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
				musicVideos.append([title, url])
				if limit and int(limit) == pos:
					break
				pos += 1
	if type == "browse":
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		random.shuffle(musicVideos)
		for title, url in musicVideos:
			listitem = xbmcgui.ListItem(title)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def listBillboardCharts(type):
	if type == "genre":
		addAutoPlayDir("Pop", urlBaseBB+"/charts/pop-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Rock", urlBaseBB+"/charts/rock-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Alternative", urlBaseBB+"/charts/alternative-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("R&B/Hip-Hop", urlBaseBB+"/charts/r-b-hip-hop-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("R&B", urlBaseBB+"/charts/r-and-b-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Rap", urlBaseBB+"/charts/rap-song", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Gospel", urlBaseBB+"/charts/gospel-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Country", urlBaseBB+"/charts/country-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40114), urlBaseBB+"/charts/latin-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40115), urlBaseBB+"/charts/jazz-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40116), urlBaseBB+"/charts/tropical-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40117), urlBaseBB+"/charts/soundtracks", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Rhythmic", urlBaseBB+"/charts/rhythmic-40", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Dance/Club", urlBaseBB+"/charts/dance-club-play-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Dance/Electronic", urlBaseBB+"/charts/dance-electronic-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	elif type == "country":
		addAutoPlayDir(translation(40118), urlBaseBB+"/charts/canadian-hot-100", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40119), urlBaseBB+"/charts/japan-hot-100", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40120), urlBaseBB+"/charts/germany-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40121), urlBaseBB+"/charts/france-digital-song-sales", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40122), urlBaseBB+"/charts/official-uk-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	elif type == "other":
		addAutoPlayDir(translation(40123), urlBaseBB+"/charts/radio-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("Digital", urlBaseBB+"/charts/digital-song-sales", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40124), urlBaseBB+"/charts/streaming-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir(translation(40125), urlBaseBB+"/charts/on-demand-songs", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
		addAutoPlayDir("TOP on Youtube", urlBaseBB+"/charts/youtube", "listBillboardCH_Videos", pic+'billboard.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listBillboardCH_Videos(type, url, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	content = content[content.find('<div class="chart-data js-chart-data" data-trackaction="Chart List"')+1:]
	content = content[:content.find('<audio class="chart__audio-element js-audio-element"></audio>')]
	spl = content.split('<div class="chart-row__main-display">')
	pos = 1
	for i in range(1,len(spl),1):
		entry = spl[i]
		rank = re.compile('<span class="chart-row__current-week">(.*?)</span>', re.DOTALL).findall(entry)[0]
		try:
			thumb = re.compile('data-imagesrc="(http.*?.jpg)"', re.DOTALL).findall(entry)[0]
		except:
			try:
				thumb = re.compile('style="background-image.+?(http.*?.jpg)', re.DOTALL).findall(entry)[0]
			except: thumb = pic+'noimage.png'
		song = re.compile('<h2 class="chart-row__song">(.*?)</h2>', re.DOTALL).findall(entry)[0]
		try:
			artist = re.compile('data-tracklabel="Artist Name">(.*?)</a>', re.DOTALL).findall(entry)[0]
		except:
			artist = re.compile('<span class="chart-row__artist">(.*?)</span>', re.DOTALL).findall(entry)[0]
		title = cleanTitle(artist.strip()+" - "+song.strip())
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "browse":
			name = '[COLOR chartreuse]'+str(rank)+' •  [/COLOR]'+title
			addLink(name, title.replace(" - ", " "), "playYTByTitle", thumb)
		else:
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
			musicVideos.append([title, url, thumb])
			if limit and int(limit) == pos:
				break
			pos += 1
	if type == "browse":
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def ddpMain():
	content = cache(urlBaseDDP+"DDP-Charts/", 30)
	content = content[content.find('<div class="ddp_subnavigation_top ddp">')+1:]
	content = content[:content.find('<div class="contentbox">')]
	match = re.compile('<li><a href="(.*?)">(.*?)</a></li>', re.DOTALL).findall(content)
	addDir("[COLOR deepskyblue]"+translation(40126)+"[/COLOR]", "", "ddpMain", pic+'ddp-international.png')
	addAutoPlayDir("     AKTUELLE VIDEOS TOP 30", urlBaseDDP+"DDP-Videochart/", "listDdpVideos", pic+'ddp-international.png', "", "browse")
	for url2, title in match:
		title = cleanTitle(title)
		if not 'ddp' in title.lower() and not 'archiv' in title.lower() and not 'highscores' in title.lower():
			if not 'schlager' in url2.lower():
				if 'top 100' in title.lower() or 'hot 50' in title.lower() or 'einsteiger' in title.lower():
					addAutoPlayDir('     '+title, url2, "listDdpVideos", pic+'ddp-international.png', "", "browse")
				elif 'jahrescharts' in title.lower():
					addDir('     '+title, url2, "listDdpYearCharts", pic+'ddp-international.png')
	addDir("[COLOR deepskyblue]"+translation(40127)+"[/COLOR]", "", "ddpMain", pic+'ddp-schlager.png')
	for url2, title in match:
		title = cleanTitle(title)
		if not 'ddp' in title.lower() and not 'archiv' in title.lower() and not 'highscores' in title.lower():
			if 'schlager' in url2.lower():
				if 'top 100' in title.lower() or 'hot 50' in title.lower() or 'einsteiger' in title.lower():
					addAutoPlayDir('     '+title, url2, "listDdpVideos", pic+'ddp-schlager.png', "", "browse")
				elif 'jahrescharts' in title.lower():
					addDir('     '+title, url2, "listDdpYearCharts", pic+'ddp-schlager.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listDdpYearCharts(url):
	musicVideos = []
	content = cache(url, 1)
	content = content[content.find('<div class="contentbox">')+1:]
	content = content[:content.find('</p>')]
	match = re.compile('<a href="(.*?)" alt="(.*?)">', re.DOTALL).findall(content)
	for url2, title in match:
		if 'schlager' in url.lower():
			endURL = urlBaseDDP+'DDP-Schlager-Jahrescharts/?'+url2.split('/?')[1]
			thumb = pic+'ddp-schlager.png'
		elif not 'schlager' in url.lower():
			endURL = urlBaseDDP+'DDP-Jahrescharts/?'+url2.split('/?')[1]
			thumb = pic+'ddp-international.png'
		musicVideos.append([title, endURL, thumb])
	musicVideos = sorted(musicVideos, key=itemgetter(0), reverse=True)
	for title, endURL, thumb in musicVideos:
		addAutoPlayDir(cleanTitle(title), endURL, "listDdpVideos", thumb, "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDdpVideos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	if type == "play":
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	content = content[content.find('<div class="eintrag" id="charthead">')+1:]
	content = content[:content.find('<div id="banner_fuss">')]
	spl = content.split('<div class="eintrag">')
	for i in range(1,len(spl),1):
		entry = spl[i]
		rank = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[0]
		artist = re.compile('<div class="interpret">(.*?)</div>', re.DOTALL).findall(entry)[0]
		song = re.compile('<div class="titel">(.*?)</div>', re.DOTALL).findall(entry)[0]
		if song == "" or artist == "":
			continue
		if artist.isupper():
			artist = unicode(artist).title().encode('utf-8')
		if song.isupper():
			song = unicode(song).title().encode('utf-8')
		firstTitle = cleanTitle(artist.strip()+" - "+song.strip())
		if firstTitle in musicIsolated:
			continue
		musicIsolated.add(firstTitle)
		try:
			newRE = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[1]
			LW = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[2]
			twoW = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[3]
			threeW = re.compile('<div class="platz">(.*?)</div>', re.DOTALL).findall(entry)[4]
			if ('RE' in newRE or 'NEU' in newRE) and not 'images' in newRE:
				completeTitle = firstTitle+'   [COLOR deepskyblue]['+str(newRE)+'][/COLOR]'
			else:
				completeTitle = firstTitle+'   [COLOR deepskyblue][AW: '+str(LW)+'|2W: '+str(twoW)+'|3W: '+str(threeW)+'][/COLOR]'
		except: completeTitle = firstTitle
		try:
			thumb = re.findall('style="background.+?//poolposition.mp3(.*?);"',entry,re.S)[0]
			if thumb:
				thumb = "https://poolposition.mp3"+thumb.split('&amp;width')[0]
		except: thumb = pic+'noimage.png'
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in firstTitle.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(firstTitle.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = firstTitle
		musicVideos.append([int(rank), firstTitle, completeTitle, url, thumb])
	musicVideos = sorted(musicVideos, key=itemgetter(0))
	if type == "browse":
		for rank, firstTitle, completeTitle, url, thumb in musicVideos:
			name = '[COLOR chartreuse]'+str(rank)+' •  [/COLOR]'+completeTitle
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for rank, firstTitle, completeTitle, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(firstTitle, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def hypemMain():
	addAutoPlayDir(translation(40136), urlBaseHypem+"/popular?ax=1&sortby=shuffle", 'listHypemVideos', pic+'hypem.png', "", "browse")
	addAutoPlayDir(translation(40137), urlBaseHypem+"/popular/lastweek?ax=1&sortby=shuffle", 'listHypemVideos', pic+'hypem.png', "", "browse")
	addDir(translation(40138), "", 'listHypemMachine', pic+'hypem.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listHypemMachine():
	for i in range(1, 210, 1):
		dt = datetime.date.today()
		while dt.weekday() != 0:
			dt -= datetime.timedelta(days=1)
		dt -= datetime.timedelta(weeks=i)
		months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		month = months[int(dt.strftime("%m")) - 1]
		addAutoPlayDir(dt.strftime("%d. %b - %Y").replace("Mar", translation(40160)).replace("May", translation(40161)).replace("Oct", translation(40162)).replace("Dec", translation(40163)), urlBaseHypem+"/popular/week:"+month+"-"+dt.strftime("%d-%Y")+"?ax=1&sortby=shuffle", 'listHypemVideos', pic+'hypem.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listHypemVideos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	jsonObject = json.loads(re.compile('id="displayList-data">(.*?)</', re.DOTALL).findall(content)[0])
	for track in jsonObject['tracks']:
		artist = track['artist'].encode('utf-8')
		song = track['song'].encode('utf-8')
		title = cleanTitle(artist.strip()+" - "+song.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		thumb = ""
		match = re.compile('href="/track/'+track['id']+'/.+?background:url\\((.+?)\\)', re.DOTALL).findall(content)
		if match:
			thumb = match[0] #.replace('_320.jpg)', '_500.jpg')
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([title, url, thumb])
	if type == "browse":
		for title, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def itunesMain():
	content = cache("https://itunes.apple.com/"+iTunesRegion+"/genre/music/id34", 30)
	content = content[content.find('id="genre-nav"'):]
	content = content[:content.find('</div>')]
	match = re.compile('<li><a href="https://itunes.apple.com/.+?/genre/.+?/id(.*?)"(.*?)title=".+?">(.*?)</a>', re.DOTALL).findall(content)
	allTitle = translation(40135)
	addAutoPlayDir(allTitle, "0", "listItunesVideos", pic+'itunes.png', "", "browse")
	for genreID, genreTYPE, genreTITLE in match:
		title = cleanTitle(genreTITLE)
		if 'class="top-level-genre"' in genreTYPE:
			if itunesShowSubGenres:
				title = '[COLOR FF1E90FF]'+title+'[/COLOR]'
			addAutoPlayDir(title, genreID, "listItunesVideos", pic+'itunes.png', "", "browse")
		elif itunesShowSubGenres:
			title = '     '+title
			addAutoPlayDir(title, genreID, "listItunesVideos", pic+'itunes.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listItunesVideos(type, genreID, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	url = "https://itunes.apple.com/"+iTunesRegion+"/rss/topsongs/limit=100"
	if genreID != "0":
		url += "/genre="+genreID
	url += "/explicit=true/json"
	content = cache(url, 1)
	response = json.loads(content)
	musicIsolated = set()
	pos = 1
	try:
		for item in response['feed']['entry']:
			artist = item['im:artist']['label'].encode('utf-8')
			song = item['im:name']['label'].encode('utf-8')
			#if " (" in song:
				#song = song[:song.rfind(' (')]
			title = cleanTitle(artist.strip()+" - "+song.strip())
			newTitle = song.strip().lower()
			if newTitle in musicIsolated:
				continue
			musicIsolated.add(newTitle)
			if len(artist) > 30:
				artist = artist[:30]
			if len(song) > 30:
				song = song[:30]
			shortenTitle = cleanTitle(artist.strip()+" - "+song.strip())
			try:
				thumb = item['im:image'][2]['label']
				#thumb = thumb.split('/170x170')[0]+"/320x320bb-85.jpg"
			except:
				thumb = pic+'noimage.png'
			aired = item['im:releaseDate']['attributes']['label']
			filtered = False
			for entry2 in blacklist:
				if entry2.strip().lower() and entry2.strip().lower() in title.lower():
					filtered = True
			if filtered:
				continue
			if type == "browse":
				name = title+"   [COLOR deepskyblue]["+str(aired)+"][/COLOR]"
				addLink(name, shortenTitle.replace(" - ", " "), "playYTByTitle", thumb)
			else:
				url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(shortenTitle.replace(" - ", " "))+"&mode=playYTByTitle"
				musicVideos.append([title, url, thumb])
				if limit and int(limit)==pos:
					break
				pos += 1
		if type == "browse":
			xbmcplugin.endOfDirectory(pluginhandle)
			if forceView:
				xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
		else:
			random.shuffle(musicVideos)
			for title, url, thumb in musicVideos:
				listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
				playlist.add(url, listitem)
			xbmc.Player().play(playlist)
	except: pass
	
def ocMain():
	addAutoPlayDir(translation(40139), urlBaseOC+"/charts/singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40140), urlBaseOC+"/charts/uk-top-40-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40141), urlBaseOC+"/charts/asian-download-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40142), urlBaseOC+"/charts/singles-chart-update/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40143), urlBaseOC+"/charts/singles-downloads-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40144), urlBaseOC+"/charts/singles-sales-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40145), urlBaseOC+"/charts/audio-streaming-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40146), urlBaseOC+"/charts/vinyl-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40147), urlBaseOC+"/charts/scottish-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40148), urlBaseOC+"/charts/physical-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40149), urlBaseOC+"/charts/end-of-year-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40150), urlBaseOC+"/charts/classical-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40151), urlBaseOC+"/charts/dance-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir("R&B", urlBaseOC+"/charts/r-and-b-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	addAutoPlayDir(translation(40152), urlBaseOC+"/charts/rock-and-metal-singles-chart/", "listOcVideos", pic+'official.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listOcVideos(type, url, limit):
	if type == "play":
		musicVideos = []
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	spl = content.split('<div class="track">')
	count = 0
	pos = 1
	for i in range(1,len(spl),1):
		count += 1
		entry=spl[i]
		photo = re.findall('<img src="(.*?)"',entry,re.S)[0]
		if "images-amazon" in photo or "coverartarchive.org" in photo:
			thumb = photo.split('img/small?url=')[1]
		elif "/img/small?url=/images/artwork/" in photo:
			thumb = photo.replace("/img/small?url=", "")
		else:
			thumb = pic+'noimage.png'
		song = re.findall('<a href=".+?">(.*?)</a>',entry,re.S)[0]
		artist = re.findall('<a href=".+?">(.*?)</a>',entry,re.S)[1]
		if "/" in artist:
			artist = artist.split('/')[0]
		song = unicode(song).title().encode('utf-8')
		artist = unicode(artist).title().encode('utf-8')
		title = cleanTitle(artist.strip()+" - "+song.strip())
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "browse":
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, title.replace(" - ", " "), "playYTByTitle", thumb)
		else:
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
			musicVideos.append([title, url, thumb])
			if limit and int(limit)==pos:
				break
			pos += 1
	if type == "browse":
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def spotifyMain():
	addDir("[COLOR deepskyblue]SPOTIFY - International[/COLOR]", "", "spotifyMain", pic+'spotify.png')
	addDir(translation(40153), "viraldaily", "listSpotifyCC_Countries", pic+'spotify.png')
	addDir(translation(40154), "viralweekly", "listSpotifyCC_Countries", pic+'spotify.png')
	addDir(translation(40155), "topdaily", "listSpotifyCC_Countries", pic+'spotify.png')
	addDir(translation(40156), "topweekly", "listSpotifyCC_Countries", pic+'spotify.png')
	addDir("[COLOR deepskyblue]SPOTIFY - Regional[/COLOR]", "", "spotifyMain", pic+'spotify.png')
	addDir(translation(40157), urlBaseSTUN+"toplists?region="+spotifyRegion+"&page=0&per_page=50&platform=web", "listSpotifyTUN_Playlists", pic+'spotify.png')
	addDir(translation(40158), urlBaseSTUN+"featured-playlists?region="+spotifyRegion+"&page=0&per_page=50&dt="+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M").replace(":","%3A")+"%3A00&platform=web", "listSpotifyTUN_Playlists", pic+'spotify.png')
	addDir(translation(40159), urlBaseSTUN+"genres?region="+spotifyRegion+"&per_page=1000&platform=web", "listSpotifyTUN_Genres", pic+'spotify.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listSpotifyCC_Countries(type):
	xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
	UN_Supported = ['andorra', 'bulgaria', 'cyprus', 'hong kong', 'luxembourg', 'monaco', 'malta', 'nicaragua', 'singapore', 'thailand', 'taiwan'] # these lists are empty or signs are not readable
	content = cache(urlBaseSCC+'regional', 1)
	content = content[content.find('<div class="responsive-select" data-type="country">')+1:]
	content = content[:content.find('<div class="responsive-select" data-type="recurrence">')]
	match = re.compile('<li data-value="(.*?)" class=.+?>(.*?)</li>', re.DOTALL).findall(content)
	for url2, toptitle in match:
		if any(x in toptitle.strip().lower() for x in UN_Supported):
			continue
		if type == "viraldaily":
			addAutoPlayDir(cleanTitle(toptitle), urlBaseSCC+'viral/'+url2+'/daily/latest', "listSpotifyCC_Videos", pic+'spotify.png', "", "browse")
		elif type == "viralweekly":
			addAutoPlayDir(cleanTitle(toptitle), urlBaseSCC+'viral/'+url2+'/weekly/latest', "listSpotifyCC_Videos", pic+'spotify.png', "", "browse")
		elif type == "topdaily":
			addAutoPlayDir(cleanTitle(toptitle), urlBaseSCC+'regional/'+url2+'/daily/latest', "listSpotifyCC_Videos", pic+'spotify.png', "", "browse")
		elif type == "topweekly":
			addAutoPlayDir(cleanTitle(toptitle), urlBaseSCC+'regional/'+url2+'/weekly/latest', "listSpotifyCC_Videos", pic+'spotify.png', "", "browse")
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listSpotifyCC_Videos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	content = cache(url, 1)
	content = content[content.find('<tbody>')+1:]
	content = content[:content.find('</tbody>')]
	spl = content.split('<tr>')
	for i in range(1,len(spl),1):
		entry = spl[i]
		song = re.compile('<strong>(.*?)</strong>', re.DOTALL).findall(entry)[0]
		artist = re.compile('<span>(.*?)</span>', re.DOTALL).findall(entry)[0]
		if "(remix)" in song.lower():
			song = song.lower().replace('(remix)', '')
		if " - " in song:
			firstTitle = song[:song.rfind(' - ')]
			secondTitle = song[song.rfind(' - ')+3:]
			song = firstTitle+' ['+secondTitle+']'
		if artist.lower().startswith('by', 0, 2):
			artist = artist.lower().split('by ')[1]
		if artist.islower():
			artist = artist.title()
		title = cleanTitle(artist.strip()+" - "+song.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		try:
			thumb = re.compile('<img src="(.*?)">', re.DOTALL).findall(entry)[0]
			if thumb[:4] != "http":
				#thumb = "https://u.scdn.co/images/pl/default/"+thumb
				thumb = "https://i.scdn.co/image/"+thumb
		except: thumb = pic+'noimage.png'
		rank = re.compile('<td class="chart-table-position">(.*?)</td>', re.DOTALL).findall(entry)[0]
		try:
			streams = re.compile('<td class="chart-table-streams">(.*?)</td>', re.DOTALL).findall(entry)[0]
		except: streams = ""
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([int(rank), title, streams, url, thumb])
	musicVideos = sorted(musicVideos, key=itemgetter(0))
	if type == "browse":
		for rank, title, streams, url, thumb in musicVideos:
			count += 1
			if streams != "":
				name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title+'   [COLOR deepskyblue][DL: '+str(streams).replace(',', '.')+'][/COLOR]'
			else:
				name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for rank, title, streams, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def listSpotifyTUN_Genres(url):
	content = cache(url, 30)
	response = json.loads(content)
	for item in response['items']:
		title = item['genre']['name'].encode('utf-8')
		if title.isupper():
			title = title.title()
		genreID = item['genre']['templateName'].encode('utf-8')
		try:
			thumb = item['genre']['iconUrl']
		except: thumb = pic+'noimage.png'
		if not "top lists" in title.strip().lower():
			addDir(title, urlBaseSTUN+genreID+"?region="+spotifyRegion+"&page=0&per_page=50&platform=web", "listSpotifyTUN_Playlists", thumb)
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDGenres+')')
	
def listSpotifyTUN_Playlists(url):
	content = cache(url, 1)
	response = json.loads(content)
	for item in response['items']:
		title = item['playlist']['title'].encode('utf-8')
		if title.isupper():
			title = title.title()
		plot = item['playlist']['description'].encode('utf-8')
		uriUrl = item['playlist']['uri']
		try:
			thumb = item['playlist']['image']
			if thumb[:4] != "http" and thumb[-11:].lower() != "default.jpg":
				#thumb = "https://u.scdn.co/images/pl/default/"+thumb
				thumb = "https://i.scdn.co/image/"+thumb
			elif thumb[:4] != "http" and thumb[-11:].lower() == "default.jpg":
				thumb = "https://charts-images.scdn.co/"+thumb
		except: thumb = pic+'noimage.png'
		addAutoPlayDir(title, uriUrl, "listSpotifyTUN_Videos", thumb, plot, "browse")
	match = re.compile('&page=(.+?)&per_page=(.+?)&', re.DOTALL).findall(url)
	currentPage = int(match[0][0])
	perPage = int(match[0][1])
	goNextPage = currentPage+1
	if goNextPage*perPage < response['totalItems']:
		addDir(translation(40206), url.replace("&page="+str(currentPage),"&page="+str(goNextPage)), "listSpotifyTUN_Playlists", pic+'nextpage.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listSpotifyTUN_Videos(type, url, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	#content = cache("https://open.spotify.com/embed?uri="+url, 1)
	content = cache("https://embed.spotify.com/?uri="+url, 1)
	jsonObject = json.loads(re.compile('type="application/json">(.*?)</script>', re.DOTALL).findall(content)[-1].strip())
	for item in jsonObject['tracks']['items']:
		artist = item['track']['artists'][0]['name'].encode('utf-8')
		song = item['track']['name'].encode('utf-8')
		album = item['track']['album']['name'].encode('utf-8')
		if "(original mix)" in song.lower():
			song = song.lower().split('(original mix)')[0]
		if " - " in song:
			firstTitle = song[:song.rfind(' - ')]
			secondTitle = song[song.rfind(' - ')+3:]
			song = firstTitle+' ['+secondTitle+']'
		if "," in artist:
			artist = artist.split(',')[0]
		title = cleanTitle(artist.strip()+" - "+song.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		try:
			thumb = item['track']['album']['images'][0]['url']
			if thumb[:4] != "http":
				#thumb = "https://u.scdn.co/images/pl/default/"+thumb
				thumb = "https://i.scdn.co/image/"+thumb
		except: thumb = pic+'noimage.png'
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([title, album, url, thumb])
	if type == "browse":
		for title, album, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title+'   [COLOR deepskyblue][Album: '+album+'][/COLOR]'
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, album, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def SearchDeezer():
	someReceived = False
	dialog = xbmcgui.Dialog()
	word = dialog.input(translation(40204), type=xbmcgui.INPUT_ALPHANUM)
	word = urllib.quote(word, safe='')
	if word == "": return
	artistSEARCH = cache("https://api.deezer.com/search/artist?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	trackSEARCH = cache("https://api.deezer.com/search/track?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	albumSEARCH = cache("https://api.deezer.com/search/album?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	playlistSEARCH = cache("https://api.deezer.com/search/playlist?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	userlistSEARCH = cache("https://api.deezer.com/search/user?q="+word+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
	strukturARTIST = json.loads(artistSEARCH)
	if strukturARTIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]ARTIST[COLOR orangered]  •  •  •[/COLOR][/B]', word, "listDeezerArtists", pic+'searchartists.png')
		someReceived = True
	strukturTRACK = json.loads(trackSEARCH)
	if strukturTRACK['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]SONG[COLOR orangered]     •  •  •[/COLOR][/B]', word, "listDeezerTracks", pic+'searchsongs.png')
		someReceived = True
	strukturALBUM = json.loads(albumSEARCH)
	if strukturALBUM['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]ALBUM[COLOR orangered]  •  •  •[/COLOR][/B]', word, "listDeezerAlbums", pic+'searchalbums.png')
		someReceived = True
	strukturPLAYLIST = json.loads(playlistSEARCH)
	if strukturPLAYLIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]PLAYLIST[COLOR orangered]  •  •  •[/COLOR][/B]', word, "listDeezerPlaylists", pic+'searchplaylists.png')
		someReceived = True
	strukturUSERLIST = json.loads(userlistSEARCH)
	if strukturUSERLIST['total'] != 0:
		addDir('[B][COLOR orangered] •  •  •  [/COLOR]USER[COLOR orangered]     •  •  •[/COLOR][/B]', word, "listDeezerUserlists", pic+'searchuserlists.png')
		someReceived = True
	if not someReceived:
		addDir(translation(40205), word, "", pic+'noresults.png')
	xbmcplugin.endOfDirectory(pluginhandle)
	
def listDeezerArtists(url):
	musicVideos = []
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/artist?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = cleanTitle(item["name"].encode('utf-8'))
		if artist.strip().lower() in musicIsolated or artist == "":
			continue
		musicIsolated.add(artist)
		try:
			thumb = item["picture_big"].encode('utf-8')
			if thumb.endswith('artist//500x500-000000-80-0-0.jpg'):
				thumb = pic+'noavatar.gif'
		except: thumb = pic+'noavatar.gif'
		liked = item['nb_fan']
		tracksUrl = item['tracklist'].encode('utf-8').split('top?limit=')[0]+"top?limit="+deezerVideosDisplay+"&index=0"
		musicVideos.append([int(liked), artist, tracksUrl, thumb])
	musicVideos = sorted(musicVideos, key=itemgetter(0), reverse=True)
	for liked, artist, tracksUrl, thumb in musicVideos:
		name = artist+"   [COLOR FFFFA500][Fans: "+str(liked).strip()+"][/COLOR]"
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerArtists", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerTracks(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/track?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = item['artist']['name'].encode('utf-8')
		song = item['title'].encode('utf-8')
		title = cleanTitle(artist.strip()+" - "+song.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		album = cleanTitle(item['album']['title'].encode('utf-8'))
		try:
			thumb = item['album']['cover_big'].encode('utf-8')
		except: thumb = pic+'noimage.png'
		#rank = item['rank']
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		name = title+"   [COLOR deepskyblue][Album: "+album+"][/COLOR]"
		addLink(name, title.replace(" - ", " "), "playYTByTitle", thumb)
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerTracks", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerAlbums(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/album?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = item['artist']['name'].encode('utf-8')
		album = item['title'].encode('utf-8')
		title = cleanTitle(artist.strip()+" - "+album.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		try:
			thumb = item['cover_big'].encode('utf-8')
		except: thumb = pic+'noimage.png'
		numbers = item['nb_tracks']
		tracksUrl = item['tracklist'].encode('utf-8')+"?limit="+deezerVideosDisplay+"&index=0"
		version = item['record_type'].encode('utf-8')
		name = title+"   [COLOR deepskyblue]["+version.title().strip()+"[/COLOR] - [COLOR FFFFA500]Tracks: "+str(numbers).strip()+"][/COLOR]"
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerAlbums", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerPlaylists(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/playlist?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		artist = cleanTitle(item['title'].encode('utf-8'))
		try:
			thumb = item['picture_big'].encode('utf-8')
		except: thumb = pic+'noimage.png'
		numbers = item['nb_tracks']
		tracksUrl = item['tracklist'].encode('utf-8')+"?limit="+deezerVideosDisplay+"&index=0"
		user = cleanTitle(item['user']['name'].encode('utf-8'))
		name = artist.title()+"   [COLOR deepskyblue][User: "+user.title()+"[/COLOR] - [COLOR FFFFA500]Tracks: "+str(numbers).strip()+"][/COLOR]"
		special = artist+" - "+user.title()
		if special in musicIsolated or artist == "":
			continue
		musicIsolated.add(special)
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerPlaylists", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerUserlists(url):
	musicIsolated = set()
	if url.startswith('https://api.deezer.com/search/'):
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache("https://api.deezer.com/search/user?q="+url+"&limit="+deezerSearchDisplay+"&strict=on&output=json&index=0", 1)
		response = json.loads(Original)
	for item in response['data']:
		user = cleanTitle(item['name'].encode('utf-8'))
		try:
			thumb = item['picture_big'].encode('utf-8')
			if thumb.endswith('user//500x500-000000-80-0-0.jpg'):
				thumb = pic+'noavatar.gif'
		except: thumb = pic+'noavatar.gif'
		tracksUrl = item['tracklist'].encode('utf-8')+"?limit="+deezerVideosDisplay+"&index=0"
		name = user.title()
		if name in musicIsolated or user == "":
			continue
		musicIsolated.add(name)
		addAutoPlayDir(name, tracksUrl, "listDeezerVideos", thumb, "", "browse")
	try:
		nextPage = response['next']
		if 'https://api.deezer.com/search/' in nextPage:
			addDir(translation(40206), nextPage, "listDeezerUserlists", pic+'nextpage.png')
	except: pass
	xbmcplugin.endOfDirectory(pluginhandle)
	if forceView:
		xbmc.executebuiltin('Container.SetViewMode('+viewIDPlaylists+')')
	
def listDeezerVideos(type, url, thumb, limit):
	musicVideos = []
	musicIsolated = set()
	count = 0
	if type == "play":
		playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
		playlist.clear()
	if not "&index=0" in url:
		Forward = cache(url, 1)
		response = json.loads(Forward)
	else:
		Original = cache(url, 1)
		response = json.loads(Original)
	for item in response['data']:
		song = item['title'].encode('utf-8')
		if song.isupper():
			song = song.title()
		artist = item['artist']['name'].encode('utf-8')
		#rank = item['rank']
		title = cleanTitle(artist.strip()+" - "+song.strip())
		if title in musicIsolated or artist == "":
			continue
		musicIsolated.add(title)
		filtered = False
		for entry2 in blacklist:
			if entry2.strip().lower() and entry2.strip().lower() in title.lower():
				filtered = True
		if filtered:
			continue
		if type == "play":
			url = "plugin://"+addon.getAddonInfo('id')+"/?url="+urllib.quote_plus(title.replace(" - ", " "))+"&mode=playYTByTitle"
		else:
			url = title
		musicVideos.append([title, url, thumb])
	if type == "browse":
		for title, url, thumb in musicVideos:
			count += 1
			name = '[COLOR chartreuse]'+str(count)+' •  [/COLOR]'+title
			addLink(name, url.replace(" - ", " "), "playYTByTitle", thumb)
		try:
			nextPage = response['next']
			if 'https://api.deezer.com/' in nextPage:
				addAutoPlayDir(translation(40206), nextPage, "listDeezerVideos", thumb, "", "browse")
		except: pass
		xbmcplugin.endOfDirectory(pluginhandle)
		if forceView:
			xbmc.executebuiltin('Container.SetViewMode('+viewIDVideos+')')
	else:
		if limit:
			musicVideos = musicVideos[:int(limit)]
		random.shuffle(musicVideos)
		for title, url, thumb in musicVideos:
			listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
			playlist.add(url, listitem)
		xbmc.Player().play(playlist)
	
def playYTByTitle(title):
	try:
		youtubeID = getYoutubeId(title)
		finalURL = 'plugin://plugin.video.youtube/play/?video_id='+youtubeID
		xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=finalURL))
		xbmc.sleep(1000)
		if infoEnabled and not xbmc.abortRequested:
			showInfo()
	except: pass
	
def getYoutubeId(title):
	title = urllib.quote_plus(title.lower()).replace('%5B', '').replace('%5D', '').replace('%28', '').replace('%29', '')
	videoBest = False
	movieID = []
	content = cache("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&order=relevance&q=%s&key=%s" %(title,token), 1)
	response = json.loads(content)
	for videoTrack in response.get('items', []):
		if videoTrack['id']['kind'] == "youtube#video":
			movieID.append('%s @@@ %s' %(videoTrack['snippet']['title'], videoTrack['id']['videoId']))
	if len(movieID) > 0:
		for videoTrack in movieID:
			best = movieID[:]
			if not 'audio' in best[0].strip().lower():
				VIDEOexAUDIO = best[0].split('@@@ ')[1].strip()
			elif not 'audio' in best[1].strip().lower():
				VIDEOexAUDIO = best[1].split('@@@ ')[1].strip()
			elif not 'audio' in best[2].strip().lower():
				VIDEOexAUDIO = best[2].split('@@@ ')[1].strip()
			else:
				VIDEOexAUDIO = best[0].split('@@@ ')[1].strip()
		videoBest = VIDEOexAUDIO
	else:
		xbmc.executebuiltin('Notification(Youtube Music : [COLOR red]!!! URL - ERROR !!![/COLOR], ERROR = [COLOR red]No *SingleEntry* found on YOUTUBE ![/COLOR],6000,'+icon+')')
	return videoBest
	
def queueVideo(url, name, image):
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	listitem = xbmcgui.ListItem(name, thumbnailImage=image)
	if useThumbAsFanart:
		listitem.setArt({'fanart': defaultFanart})
	playlist.add(url, listitem)
	
def makeRequest(url, headers=False):
	req = urllib2.Request(url)
	if headers:
		for key in headers:
			req.add_header(key, headers[key])
	else:
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
		req.add_header('Accept-Encoding','gzip, deflate')
	response = urllib2.urlopen(req, timeout=30)
	if response.info().get('Content-Encoding') == 'gzip':
		link = gzip.GzipFile(fileobj=StringIO(response.read())).read()
	else:
		link = response.read()
	response.close()
	return link
	
def cache(url, duration=0):
	cacheFile = os.path.join(cachePath, (''.join(c for c in unicode(url, 'utf-8') if c not in '/\\:?"*|<>')).strip())
	if len(cacheFile) > 255:
		cacheFile = cacheFile.replace("part=snippet&type=video&maxResults=5&order=relevance&q", "")
		cacheFile = cacheFile[:255]
	if os.path.exists(cacheFile) and duration!=0 and (time.time()-os.path.getmtime(cacheFile) < 60*60*24*duration):
		fh = xbmcvfs.File(cacheFile, 'r')
		content = fh.read()
		fh.close()
	else:
		content = makeRequest(url)
		fh = xbmcvfs.File(cacheFile, 'w')
		fh.write(content)
		fh.close()
	return content
	
def showInfo():
	count = 0
	while not xbmc.Player().isPlaying():
		xbmc.sleep(200)
		if count == 50:
			break
		count += 1
	xbmc.sleep(infoDelay*1000)
	if xbmc.Player().isPlaying() and infoType == "0":
		xbmc.sleep(1500)
		xbmc.executebuiltin('ActivateWindow(12901)')
		xbmc.sleep(infoDuration*1000)
		xbmc.executebuiltin('ActivateWindow(12005)')
		xbmc.sleep(500)
		xbmc.executebuiltin('Action(Back)')
	elif xbmc.Player().isPlaying() and infoType == "1":
		TOP = translation(40207)
		xbmc.getInfoLabel('Player.Title')
		xbmc.getInfoLabel('Player.Duration')
		xbmc.getInfoLabel('Player.Art(thumb)')
		xbmc.sleep(500)
		title = xbmc.getInfoLabel('Player.Title')
		relTitle = cleanTitle(title)
		relTitle = relTitle.encode('utf-8').replace(",", " ")
		if relTitle.isupper() or relTitle.islower():
			relTitle = relTitle.title()
		runTime = xbmc.getInfoLabel('Player.Duration')
		photo = xbmc.getInfoLabel('Player.Art(thumb)')
		xbmc.sleep(1000)
		xbmc.executebuiltin('Notification(%s,%s,%d,%s)' %(TOP, relTitle+"[COLOR blue]  * "+runTime+" *[/COLOR]", infoDuration*1000, photo))
	else: pass
	
def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&Amp;", "&").replace("&#34;", "”").replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", "\"").replace("&Quot;", "\"").replace("&reg;", "").replace("&szlig;", "ß").replace("&mdash;", "-").replace("&ndash;", "-").replace('–', '-')
	title = title.replace("&#x00c4", "Ä").replace("&#x00e4", "ä").replace("&#x00d6", "Ö").replace("&#x00f6", "ö").replace("&#x00dc", "Ü").replace("&#x00fc", "ü").replace("&#x00df", "ß")
	title = title.replace("&Auml;", "Ä").replace("&auml;", "ä").replace("&Euml;", "Ë").replace("&euml;", "ë").replace("&Iuml;", "Ï").replace("&iuml;", "ï").replace("&Ouml;", "Ö").replace("&ouml;", "ö").replace("&Uuml;", "Ü").replace("&uuml;", "ü").replace("&#376;", "Ÿ").replace("&yuml;", "ÿ")
	title = title.replace("&agrave;", "à").replace("&Agrave;", "À").replace("&aacute;", "á").replace("&Aacute;", "Á").replace("&egrave;", "è").replace("&Egrave;", "È").replace("&eacute;", "é").replace("&Eacute;", "É").replace("&igrave;", "ì").replace("&Igrave;", "Ì").replace("&iacute;", "í").replace("&Iacute;", "Í")
	title = title.replace("&ograve;", "ò").replace("&Ograve;", "Ò").replace("&oacute;", "ó").replace("&Oacute;", "ó").replace("&ugrave;", "ù").replace("&Ugrave;", "Ù").replace("&uacute;", "ú").replace("&Uacute;", "Ú").replace("&yacute;", "ý").replace("&Yacute;", "Ý")
	title = title.replace("&atilde;", "ã").replace("&Atilde;", "Ã").replace("&ntilde;", "ñ").replace("&Ntilde;", "Ñ").replace("&otilde;", "õ").replace("&Otilde;", "Õ").replace("&Scaron;", "Š").replace("&scaron;", "š")
	title = title.replace("&acirc;", "â").replace("&Acirc;", "Â").replace("&ccedil;", "ç").replace("&Ccedil;", "Ç").replace("&ecirc;", "ê").replace("&Ecirc;", "Ê").replace("&icirc;", "î").replace("&Icirc;", "Î").replace("&ocirc;", "ô").replace("&Ocirc;", "Ô").replace("&ucirc;", "û").replace("&Ucirc;", "Û")
	title = title.replace("&alpha;", "a").replace("&Alpha;", "A").replace("&aring;", "å").replace("&Aring;", "Å").replace("&aelig;", "æ").replace("&AElig;", "Æ").replace("&epsilon;", "e").replace("&Epsilon;", "Ε").replace("&eth;", "ð").replace("&ETH;", "Ð").replace("&gamma;", "g").replace("&Gamma;", "G")
	title = title.replace("&oslash;", "ø").replace("&Oslash;", "Ø").replace("&theta;", "θ").replace("&thorn;", "þ").replace("&THORN;", "Þ")
	title = title.replace("\\'", "'").replace("&x27;", "'").replace("&iexcl;", "¡").replace("&iquest;", "¿").replace("&rsquo;", "’").replace("&lsquo;", "‘").replace("&sbquo;", "’").replace("&rdquo;", "”").replace("&ldquo;", "“").replace("&bdquo;", "”").replace("&rsaquo;", "›").replace("lsaquo;", "‹").replace("&raquo;", "»").replace("&laquo;", "«")
	title = title.replace(" ft ", " feat. ").replace(" FT ", " feat. ").replace(" Ft ", " feat. ").replace("Ft.", "feat.").replace("ft.", "feat.").replace(" FEAT ", " feat. ").replace(" Feat ", " feat. ").replace("Feat.", "feat.").replace("Featuring", "feat.").replace("™", "")
	title = title.strip()
	return title
	
def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split("&")
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if (len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict
	
def addLink(name, url, mode, image, plot=""):
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
	liz = xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=image)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot, 'mediatype':'video'})
	if useThumbAsFanart:
		liz.setArt({'fanart': defaultFanart})
	liz.setProperty('IsPlayable', 'true')
	liz.addContextMenuItems([(translation(40208), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode=queueVideo&url='+urllib.quote_plus(u)+'&name='+urllib.quote_plus(name)+'&image='+urllib.quote_plus(image)+')',)])
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	
def addDir(name, url, mode, image, plot=""):
	u = u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
	liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=image)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
	if useThumbAsFanart:
		liz.setArt({'fanart': defaultFanart})
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	
def addAutoPlayDir(name, url, mode, image, plot="", type="", limit=""):
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&limit="+str(limit)
	liz = xbmcgui.ListItem(name, iconImage="DefaultMusicVideos.png", thumbnailImage=image)
	liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot, 'mediatype':'video'})
	if useThumbAsFanart:
		liz.setArt({'fanart': defaultFanart})
	entries = []
	entries.append((translation(40231), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=)',))
	entries.append((translation(40232), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=10)',))
	entries.append((translation(40233), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=20)',))
	entries.append((translation(40234), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=30)',))
	entries.append((translation(40235), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=40)',))
	entries.append((translation(40236), 'RunPlugin(plugin://'+addon.getAddonInfo('id')+'/?mode='+str(mode)+'&url='+urllib.quote_plus(url)+'&type=play&limit=50)',))
	liz.addContextMenuItems(entries)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	
params = parameters_string_to_dict(sys.argv[2])
name = urllib.unquote_plus(params.get('name', ''))
url = urllib.unquote_plus(params.get('url', ''))
mode = urllib.unquote_plus(params.get('mode', ''))
image = urllib.unquote_plus(params.get('image', ''))
type = urllib.unquote_plus(params.get('type', ''))
limit = urllib.unquote_plus(params.get('limit', ''))
	
if mode == 'beatportMain':
	beatportMain()
elif mode == 'listBeatportVideos':
	listBeatportVideos(type, url, limit)
elif mode == 'billboardMain':
	billboardMain()
elif mode == 'listBillboardArchiveYears':
	listBillboardArchiveYears()
elif mode == 'listBillboardAR_Genres':
	listBillboardAR_Genres(url)
elif mode == 'listBillboardAR_Videos':
	listBillboardAR_Videos(type, url, limit)
elif mode == 'listBillboardCharts':
	listBillboardCharts(url)
elif mode == 'listBillboardCH_Videos':
	listBillboardCH_Videos(type, url, limit)
elif mode == 'ddpMain':
	ddpMain()
elif mode == 'listDdpYearCharts':
	listDdpYearCharts(url)
elif mode == 'listDdpVideos':
	listDdpVideos(type, url, limit)
elif mode == 'hypemMain':
	hypemMain()
elif mode == 'listHypemMachine':
	listHypemMachine()
elif mode == 'listHypemVideos':
	listHypemVideos(type, url, limit)
elif mode == 'itunesMain':
	itunesMain()
elif mode == 'listItunesVideos':
	listItunesVideos(type, url, limit)
elif mode == 'ocMain':
	ocMain()
elif mode == 'listOcVideos':
	listOcVideos(type, url, limit)
elif mode == 'spotifyMain':
	spotifyMain()
elif mode == 'listSpotifyCC_Countries':
	listSpotifyCC_Countries(url)
elif mode == 'listSpotifyCC_Videos':
	listSpotifyCC_Videos(type, url, limit)
elif mode == 'listSpotifyTUN_Genres':
	listSpotifyTUN_Genres(url)
elif mode == 'listSpotifyTUN_Playlists':
	listSpotifyTUN_Playlists(url)
elif mode == 'listSpotifyTUN_Videos':
	listSpotifyTUN_Videos(type, url, limit)
elif mode == 'SearchDeezer':
	SearchDeezer()
elif mode == 'listDeezerArtists':
	listDeezerArtists(url) 
elif mode == 'listDeezerTracks':
	listDeezerTracks(url) 
elif mode == 'listDeezerAlbums':
	listDeezerAlbums(url)
elif mode == 'listDeezerPlaylists':
	listDeezerPlaylists(url)
elif mode == 'listDeezerUserlists':
	listDeezerUserlists(url)
elif mode == 'listDeezerVideos':
	listDeezerVideos(type, url, thumb, limit)
elif mode == 'playYTByTitle':
	playYTByTitle(url)
elif mode == 'queueVideo':
	queueVideo(url, name, image)
elif mode == 'Settings':
	addon.openSettings()
else:
	index()