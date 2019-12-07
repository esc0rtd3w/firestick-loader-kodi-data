import json
import os
import sys
import urllib
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import re

ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.quantum/')
USERDATA_PATH = xbmc.translatePath('special://home/userdata/addon_data')
ADDON_DATA = USERDATA_PATH + '/plugin.video.quantum/'
if not os.path.exists(ADDON_DATA):
    os.makedirs(ADDON_DATA)
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
Dialog = xbmcgui.Dialog()
addon_id = 'plugin.video.quantum'
ADDON = xbmcaddon.Addon(id=addon_id)
PATH = 'Quantum'
VERSION = '0.0.1'
favourites = ADDON_DATA + 'favourites'
if os.path.exists(favourites) == True:
    FAV = open(favourites).read()
else:
    FAV = []
dp = xbmcgui.DialogProgress()
addon_handle = int(sys.argv[1])
List = []
temp_file = ADDON_PATH + 'Temp.txt'
debug = ADDON.getSetting('debug')
watched_list = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.quantum/watched')

def nanMenu(title, show_year, season, episode,mode, allinfo={}):
    u = sys.argv[0] + "?title=" + urllib.quote_plus(title) + "&show_year=" + urllib.quote_plus(
        show_year) + "&season=" + urllib.quote_plus(season) + "&episode=" + urllib.quote_plus(
        episode)+ "&mode=" + str(mode)
    ok = True
    liz = xbmcgui.ListItem(title)
    liz.setInfo(type="Video", infoLabels={"Title": title,})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Menu(name, url, mode, iconimage, fanart, description, extra, showcontext=True, allinfo={}):
    if iconimage == '':
        iconimage = ICON
    elif iconimage == ' ':
        iconimage = ICON
    if fanart == '':
        fanart = FANART
    elif fanart == ' ':
        fanart = FANART
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(
        fanart) + "&description=" + urllib.quote_plus(description) + "&extra=" + urllib.quote_plus(extra)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty("Fanart_Image", fanart)
    if showcontext:
        contextMenu = []
        if showcontext == 'fav':
            contextMenu.append(('Remove from Quantum Favorites', 'XBMC.RunPlugin(%s?mode=12&name=%s)'
                                % (sys.argv[0], urllib.quote_plus(name))))
            contextMenu.append(('Check for episode', 'XBMC.RunPlugin(%s?mode=41&name=%s)'
                                % (sys.argv[0], urllib.quote_plus(name))))								
        if not name in FAV:
            contextMenu.append(('Add to Quantum Favorites',
                                'XBMC.RunPlugin(%s?mode=11&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s&description=%s&extra=%s)'
                                % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url),
                                   urllib.quote_plus(iconimage), urllib.quote_plus(fanart), mode, urllib.quote_plus(description),
								   urllib.quote_plus(extra))))
        liz.addContextMenuItems(contextMenu)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Play(name, url, mode, iconimage, fanart, description, extra, showcontext=True, allinfo={}):
    if iconimage == '':
        iconimage = ICON
    if fanart == '':
        fanart = FANART
    if not 'http' in url:
        PLAY(name, url, mode, iconimage, fanart, description, extra)
    elif 'watchseries' in url:
        PLAY(name, url, mode, iconimage, fanart, description, extra)
    elif 'm3u' in url:
        PLAY(name, url, mode, iconimage, fanart, description, extra)
    else:
        from pyramid import pyramid
        pyramid.addLink(url, name, iconimage, fanart, description, '', '', True, '', '', 1, '')


def PLAY(name, url, mode, iconimage, fanart, description, extra, showcontext=True, allinfo={}):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(
        fanart) + "&description=" + urllib.quote_plus(description)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=" ", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty("Fanart_Image", fanart)
    if showcontext:
        contextMenu = []
        if showcontext == 'fav':
            contextMenu.append(('Remove from Quantum Favorites', 'XBMC.RunPlugin(%s?mode=12&name=%s)'
                                % (sys.argv[0], urllib.quote_plus(name))))
        if not name in FAV:
            contextMenu.append(('Add to Quantum Favorites',
                                'XBMC.RunPlugin(%s?mode=11&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
                                % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url),
                                   urllib.quote_plus(iconimage), urllib.quote_plus(fanart), mode)))
        contextMenu.append(('Queue Item', 'RunPlugin(%s?mode=1)' % sys.argv[0]))
        liz.addContextMenuItems(contextMenu)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def queueItem():
    return xbmc.executebuiltin('Action(Queue)')

# =======================================Credit to Spoyser for this, was in funnier moments and using to implement playlists, will rewrite when i better understand it ======

def Random_play(name, mode, url='', image=None, isFolder=True, page=1, keyword=None, infoLabels=None, contextMenu=None):
    if not image:
        image = ICON
    u  = sys.argv[0] 
    u += '?mode='  + str(mode)
    u += '&title=' + urllib.quote_plus(name)
    u += '&image=' + urllib.quote_plus(image)
    u += '&page='  + str(page)
    if url != '':     
        u += '&url='   + urllib.quote_plus(url) 
    if keyword:
        u += '&keyword=' + urllib.quote_plus(keyword) 
    liz = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
    if contextMenu:
        liz.addContextMenuItems(contextMenu)
    if infoLabels:
        liz.setInfo(type="Video", infoLabels=infoLabels)
    if not isFolder:
        liz.setProperty("IsPlayable","true")
    liz.setProperty('Fanart_Image', FANART)     
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)


# ===============================Favourites-----------Not sure whos code this is but credit due to them-------------------------------

def addon_log(string):
    if debug == 'true':
        xbmc.log("[addon.live.Quantum-%s]: %s" % (addon_version, string))


def addFavorite(name, url, mode, iconimage, fanart, description, extra):
    favList = []
    xbmc.log(extra)
    try:
        name = name.encode('utf-8', 'ignore')
    except:
        pass
    if os.path.exists(favourites) == False:
        favList.append((name, url, mode, iconimage, fanart, description, extra))
        a = open(favourites, "w")
        a.write(json.dumps(favList))
        a.close()
    else:
        a = open(favourites).read()
        data = json.loads(a)
        data.append((name, url, mode, iconimage, fanart, description, extra))
        b = open(favourites, "w")
        b.write(json.dumps(data))
        b.close()


def getFavourites():
    if not os.path.exists(favourites):
        favList = []
        addon_log('Making Favorites File')
        favList.append(('Quantum Favourites Section', '', '', '', '', '', ''))
        a = open(favourites, "w")
        a.write(json.dumps(favList))
        a.close()
    else:
        items = json.loads(open(favourites).read())
        for i in items:
            name = i[0]
            url = i[1]
            try:
			    iconimage = i[3]
            except:
                iconimage = ''
            try:
                fanart = i[4]
            except:
                fanart = ''
            try:
                description = i[5]
            except:
                description = ''
            try:
                extra = i[6]
            except:
                extra = ''

            if i[2] == 906:
                Play(name, url, i[2], iconimage, fanart, description, extra, 'fav')
            else:
                Menu(name, url, i[2], iconimage, fanart, description, extra, 'fav')


def rmFavorite(name):
    data = json.loads(open(favourites).read())
    for index in range(len(data)):
        if data[index][0] == name:
            del data[index]
            b = open(favourites, "w")
            b.write(json.dumps(data))
            b.close()
            break
    xbmc.executebuiltin("XBMC.Container.Refresh")
	
def rmWatched(name):
    try:
        data = json.loads(open(watched_list).read())
        for index in range(len(data)):
            if data[index][0] == name:
                del data[index]
                b = open(watched_list, "w")
                b.write(json.dumps(data))
                b.close()
    except:
        pass

def Addwatched(title,season,episode):
    watchedlist = []
    try:
        name = name.encode('utf-8', 'ignore')
    except:
        pass
    if os.path.exists(watched_list) == False:
        watchedlist.append((title,season,episode))
        a = open(watched_list, "w")
        a.write(json.dumps(watchedlist))
        a.close()
    else:
        a = open(watched_list).read()
        data = json.loads(a)
        data.append((title,season,episode))
        b = open(watched_list, "w")
        b.write(json.dumps(data))
        b.close()

############################## FAVOURITES END ###############################
##############################CHECK FOR UPCOMING EPISODES###########################
def check_for_episode():
	Type = ''
	favourite_names = [];Watched_List = []
	Choices = ['Watch now','Upcoming Episodes']
	decide = Dialog.select('Select Choice',Choices)
	if decide == 0:
		Choice = 'Watch now'
	elif decide == 1:
		Choice = 'Upcoming'		
	from datetime import datetime
	today = datetime.now().strftime("%d")
	this_month = datetime.now().strftime("%m")
	this_year = datetime.now().strftime("%y")
	todays_number = (int(this_year)*100)+(int(this_month)*31)+(int(today))
	if not os.path.exists(favourites):
		favList = []
		addon_log('Making Favorites File')
		favList.append(('Quantum Favourites Section', '', '', '', '', '', ''))
		a = open(favourites, "w")
		a.write(json.dumps(favList))
		a.close()
	else:
		items = json.loads(open(favourites).read())
		for i in items:
			name = i[0]
			if '(' in name:
				name = re.compile('(.+?)\(').findall(str(name))
				for name in name:
					name = name
			favourite_names.append(name.lower().replace(' ',''))
	if not os.path.exists(watched_list):
		favList = []
		addon_log('Making Favorites File')
		favList.append(('Quantum Watched Section', '', '', '', '', '', ''))
		a = open(watched_list, "w")
		a.write(json.dumps(favList))
		a.close()
	else:
		items = json.loads(open(watched_list).read())
		for i in items:
			name2 = i[0]
			watched_season = i[1]
			watched_episode = i[2]
			if '(' in name2:
				name2 = re.compile('(.+?)\(').findall(str(name2))
				for name2 in name2:
					name2 = name2
			Watched_List.append([name2,watched_season,watched_episode])
	HTML = OPEN_URL('http://www.tvmaze.com/calendar')
	match = re.compile('<span class="dayofmonth">.+?<span class=".+?">(.+?)</span>(.+?)</span>(.+?)</div>',re.DOTALL).findall(HTML)
	for Day_Month,Date,Block in match:
		Date = Date.replace('\n','').replace('  ','').replace('	','')
		Day_Month = Day_Month.replace('\n','').replace('  ','').replace('	','')
		Final_Name = Day_Month.replace(',',' '+Date+' ')
		split_month = Day_Month+'>'
		Month_split = re.compile(', (.+?)>').findall(str(split_month))
		for item in Month_split:
			month_one = item.replace('January','1').replace('February','2').replace('March','3').replace('April','4').replace('May','5').replace('June','6')
			month = month_one.replace('July','7').replace('August','8').replace('September','9').replace('October','10').replace('November','11').replace('December','12')
		show_day = Date.replace('st','').replace('th','').replace('nd','').replace('rd','')
		shows_number = (int(this_year)*100)+(int(month)*31)+(int(show_day))
		if shows_number< todays_number:
			Aired = 'Watch now'
		else:
			Aired = 'Airs:'
		prog = re.compile('<span class="show">.+?<a href=".+?">(.+?)</a>:.+?</span>.+?<a href=".+?" title=".+?">(.+?)</a>',re.DOTALL).findall(str(Block))
		for prog, ep in prog:
			prog_check = prog.lower().replace(' ','')
			Split = 'season '+ep.replace('x',' episode ')+'>'
			season_check = re.compile('season (.+?) episode (.+?)>').findall(str(Split))
			for season, episode in season_check:
				season = season
				episode = episode
			if prog_check in favourite_names:
				if str(prog_check) in str(Watched_List):
					for check_name, check_season, check_ep in Watched_List:
						if prog_check == check_name:
							if check_name == prog_check and int(season) <= int(check_season) and int(episode) > int(check_ep):
								if Choice == 'Watch now':
									if Aired == 'Watch now':
										Menu(prog+' - Season '+ep.replace('x',' Episode '),'',8,'','','',prog)
								elif Choice == 'Upcoming':
									if Aired == 'Airs:':
										Menu('[COLORwhite]'+Aired+Date+' '+item+'[/COLOR] '+prog+' - Season '+ep.replace('x',' Episode '),'',8,'','','',prog)
								else:
									pass
				else:
					if Choice == 'Watch now':
						if Aired == 'Watch now':
							Menu(prog+' - Season '+ep.replace('x',' Episode '),'',8,'','','',prog)
					elif Choice == 'Upcoming':
						if Aired == 'Airs:':
							Menu('[COLORwhite]'+Aired+Date+' '+item+'[/COLOR] '+prog+' - Season '+ep.replace('x',' Episode '),'',8,'','','',prog)

					
###########################CHECK FOR UPCOMING EPISODES END#############################################

def Straight_Resolve(name,url):
	xbmc.Player().play(url, xbmcgui.ListItem(name))

def Resolve(url):
    Big_Resolve('',url)


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = ''
    link = ''
    try:
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
    except:
        pass
    if link != '':
        return link
    else:
        link = 'Opened'
        return link


def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType))


def resolve_playercore(url):
	Big_Resolve('',url)

def Big_Resolve(name,url):
	import urlresolver
	try:
		resolved_url = urlresolver.resolve(url)
		xbmc.Player().play(resolved_url, xbmcgui.ListItem(name))
	except:
		xbmc.Player().play(url, xbmcgui.ListItem(name))
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Big_resolve2(name,url):
    import liveresolver
    resolved_url = liveresolver.resolve(url)
    xbmc.Player().play(resolved_url, xbmcgui.ListItem(name))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

