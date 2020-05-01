#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import sys
import re
import os
import xbmcplugin
import xbmcaddon
import xbmcgui

#addon = xbmcaddon.Addon()
#addonID = addon.getAddonInfo('id')
addonID = "plugin.video.blip_tv"
addon = xbmcaddon.Addon(id=addonID)
socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
forceViewMode = addon.getSetting("forceView") == "true"
useThumbAsFanart = addon.getSetting("useThumbAsFanart") == "true"
showNotConverted = addon.getSetting("showNotConverted") == "true"
showSubtitles = addon.getSetting("showSubtitles") == "true"
viewIDShows = str(addon.getSetting("viewIDShows"))
viewIDEpisodes = str(addon.getSetting("viewIDEpisodes"))
xbox = xbmc.getCondVisibility("System.Platform.xbox")
icon = xbmc.translatePath(os.path.join(addon.getAddonInfo('path') ,'icon.png'))
addonUserDataFolder = xbmc.translatePath(addon.getAddonInfo('profile'))
channelFavsFile = os.path.join(addonUserDataFolder ,'favourites')
maxVideoQuality = addon.getSetting("maxVideoQuality")
maxVideoQuality = ["SD", "720p", "Source"][int(maxVideoQuality)]
baseUrl = "http://www.blip.tv"
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/25.0')]

if not os.path.isdir(addonUserDataFolder):
    os.mkdir(addonUserDataFolder)


def index():
    addDir(translation(30001), "", "listEpisodesMain", icon)
    addDir(translation(30002), "", "listShowsMain", icon)
    addDir(translation(30003), "", "listShowsFavs", icon)
    xbmcplugin.endOfDirectory(pluginhandle)


def listEpisodesMain():
    addDir(translation(30017), "", "listLatestAll", icon)
    addDir(translation(30004), "new episodes", "listEpisodesLatest", icon)
    addDir(translation(30005), "trending now", "listEpisodesLatest", icon)
    addDir(translation(30006), "editors picks", "listEpisodesLatest", icon)
    addDir(translation(30007), "", "listEpisodesFeaturedMain", icon)
    addDir(translation(30008), "episodes", "search", icon)
    xbmcplugin.endOfDirectory(pluginhandle)


def listEpisodesFeaturedMain():
    content = opener.open(baseUrl).read()
    content = content[content.find('<ul class="browse-genres">'):]
    content = content[:content.find('</ul>')]
    match = re.compile('<li><a href="(.+?)" data-link-text=".+?">(.+?)<', re.DOTALL).findall(content)
    for url, title in match:
        addDir(title, baseUrl+url, "listEpisodesFeatured", "")
    xbmcplugin.endOfDirectory(pluginhandle)


def listShowsMain():
    addDir("- "+translation(30008), "shows", "search", icon)
    addDir("- "+translation(30016), "", "listShowsBlipPicks", icon)
    content = opener.open(baseUrl).read()
    content = content[content.find('<ul class="browse-genres">'):]
    content = content[:content.find('</ul>')]
    match = re.compile('<li><a href="(.+?)" data-link-text=".+?">(.+?)<', re.DOTALL).findall(content)
    for url, title in match:
        addDir(title, baseUrl+url, "listShowsMain2", "")
    xbmcplugin.endOfDirectory(pluginhandle)


def listShowsMain2(url):
    addDir(translation(30009), url, "listShowsStaff", icon)
    addDir(translation(30010), url, "listShowsAudience", icon)
    addDir(translation(30011), url, "listShows", icon)
    xbmcplugin.endOfDirectory(pluginhandle)


def listEpisodesLatest(type):
    content = opener.open(baseUrl).read()
    content = content[content.find('data-placement="'+type+'"'):]
    spl = content.split('<div class="episode">')
    for i in range(1, 6, 1):
        entry = spl[i]
        match = re.compile('data-episode-id="(.+?)"', re.DOTALL).findall(entry)
        videoID = match[0]
        match = re.compile('data-episode-title="(.+?)"', re.DOTALL).findall(entry)
        titleEpisode = cleanTitle(match[0])
        match = re.compile('data-series-title="(.+?)"', re.DOTALL).findall(entry)
        titleShow = cleanTitle(match[0])
        title = titleShow+" - "+titleEpisode
        match = re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0].replace("w=270&h=152","w=690&h=380")
        if not thumb.startswith("http:"):
            thumb = "http:"+thumb
        addLink(title, videoID, 'playVideo', thumb)
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewIDEpisodes+')')


def listLatestAll():
    content = opener.open(baseUrl+"/rss").read()
    spl = content.split('<item>')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('<blip:posts_id>(.+?)</blip:posts_id>', re.DOTALL).findall(entry)
        videoID = match[0]
        match = re.compile('<title>(.+?)</title>', re.DOTALL).findall(entry)
        titleEpisode = cleanTitle(match[0])
        match = re.compile('<blip:show>(.+?)</blip:show>', re.DOTALL).findall(entry)
        titleShow = cleanTitle(match[0])
        match = re.compile('<blip:datestamp>.+?T(.+?)Z</blip:datestamp>', re.DOTALL).findall(entry)
        time = match[0]
        time = time[:time.rfind(":")]
        title = time+" - "+titleShow+" - "+titleEpisode
        match = re.compile('<blip:runtime>(.+?)</blip:runtime>', re.DOTALL).findall(entry)
        duration = ""
        if match:
            duration = str(int(match[0])/60)
            if duration=="0":
                duration = "1"
        match = re.compile('<blip:puredescription>(.+?)</blip:puredescription>', re.DOTALL).findall(entry)
        desc = ""
        if match:
            desc = match[0].replace("<![CDATA[","").replace("]]>","")
        match = re.compile('<media:thumbnail url="(.+?)"/>', re.DOTALL).findall(entry)
        thumb = match[0]
        if not thumb.startswith("http:"):
            thumb = "http:"+thumb
        addLink(title, videoID, 'playVideo', thumb, desc, duration)
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewIDEpisodes+')')


def listEpisodes(url):
    content = opener.open(url).read()
    spl = content.split('<a class="ArchiveCard"')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('data-episode-id="(.+?)"', re.DOTALL).findall(entry)
        videoID = match[0]
        match = re.compile('<span class="Title" itemprop="name">(.+?)</span>', re.DOTALL).findall(entry)
        title = cleanTitle(match[0])
        match = re.compile('<span class="ReleaseDate">(.+?)</span>', re.DOTALL).findall(entry)
        date = match[0].strip()
        title = date+" - "+title
        match = re.compile('<span class="Runtime">(.+?)</span>', re.DOTALL).findall(entry)
        duration = match[0].strip()
        if duration.startswith("00:"):
            duration = "1"
        match = re.compile('<span class="Description">(.+?)</span>', re.DOTALL).findall(entry)
        desc = cleanTitle(match[0])
        match = re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0].replace("w=190&h=107","w=690&h=380")
        if not thumb.startswith("http:"):
            thumb = "http:"+thumb
        addLink(title, videoID, 'playVideo', thumb, desc, duration)
    currentPage = url[url.find("page=")+5:]
    if "&" in currentPage:
        currentPage = currentPage[:currentPage.find("&")]
    nextPage = int(currentPage)+1
    match = re.compile('<span class="LastPage">(.+?)</span>', re.DOTALL).findall(content)
    lastPage = int(match[0])
    if nextPage<=lastPage:
        urlNext = url.replace("page="+currentPage, "page="+str(nextPage))
        addDir(translation(30012), urlNext, "listEpisodes", icon)
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewIDEpisodes+')')


def listEpisodesByShowID(showID):
    url = baseUrl+"/pr/show_get_full_episode_list?users_id="+showID+"&lite=0&esi=1&page=1"
    listEpisodes(url)


def listEpisodesFeatured(url):
    content = opener.open(url).read()
    spl = content.split('<div class="FeaturedEpisode"')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('data-episode-id="(.*?)"', re.DOTALL).findall(entry)
        if match and match[0]:
            videoID = match[0]
            match = re.compile('<div class="Title">(.+?)</div>', re.DOTALL).findall(entry)
            titleEpisode = cleanTitle(match[0])
            match = re.compile('<div class="ShowName">(.+?)</div>', re.DOTALL).findall(entry)
            titleShow = cleanTitle(match[0])
            title = titleShow+" - "+titleEpisode
            match = re.compile('data-thumbnail="(.+?)"', re.DOTALL).findall(entry)
            thumb = match[0]
            if not thumb.startswith("http:"):
                thumb = "http:"+thumb
            addLink(title, videoID, 'playVideo', thumb)
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewIDEpisodes+')')


def listEpisodesSearch(url):
    content = opener.open(url).read()
    spl = content.split('<div class="MyBlipEpisodeCardWrap"')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('data-episode-id="(.+?)"', re.DOTALL).findall(entry)
        videoID = match[0]
        match = re.compile('data-episode-title="(.+?)"', re.DOTALL).findall(entry)
        titleEpisode = cleanTitle(match[0])
        match = re.compile('data-series-title="(.+?)"', re.DOTALL).findall(entry)
        titleShow = cleanTitle(match[0])
        title = titleShow+" - "+titleEpisode
        match = re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0].replace("w=230&h=128","w=690&h=380")
        if not thumb.startswith("http:"):
            thumb = "http:"+thumb
        addLink(title, videoID, 'playVideo', thumb)
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewIDEpisodes+')')


def listShows(url):
    xbmcplugin.setContent(pluginhandle, "movies")
    content = opener.open(url).read()
    match = re.compile('data-channels-id="(.+?)"', re.DOTALL).findall(content)
    channelID = match[0]
    content = opener.open("http://blip.tv/channel/get_directory_listing?channels_id="+channelID+"&page=1&no_wrap=1").read()
    listShowContent(content)
    
    
def listShowsURL(url):
    xbmcplugin.setContent(pluginhandle, "movies")
    content = opener.open(url).read()
    listShowContent(content)
    
    
def listShowsStaff(url):
    xbmcplugin.setContent(pluginhandle, "movies")
    content = opener.open(url).read()
    content = content[content.find('<h3 class="sectionHeader">Staff Picks'):]
    content = content[:content.find('<div class="cardContainer"')]
    listShowContent(content)


def listShowsAudience(url):
    xbmcplugin.setContent(pluginhandle, "movies")
    content = opener.open(url).read()
    content = content[content.find('<h3 class="sectionHeader">Audience Favorites'):]
    content = content[:content.find('<div class="backgroundStripe">')]
    listShowContent(content)


def listShowsBlipPicks():
    xbmcplugin.setContent(pluginhandle, "movies")
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    content = opener.open(baseUrl).read()
    content = content[content.find('data-placement="blip picks"'):]
    listShowContent(content)


def listShowContent(content):
    spl = content.split('<div class="PosterCardWrap">')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('data-show-id="(.+?)"', re.DOTALL).findall(entry)
        showID = match[0]
        match = re.compile('<div class="ShowTitle">(.+?)</div>', re.DOTALL).findall(entry)
        title = cleanTitle(match[0])
        match = re.compile('<p class="EpisodeCount">(.+?)</p>', re.DOTALL).findall(entry)
        episodes = match[0].strip()
        match = re.compile('<p class="ShowDescription">(.+?)</p>', re.DOTALL).findall(entry)
        desc = episodes+"\n"+cleanTitle(match[0])
        match = re.compile('style="background-image:url\\((.+?)\\);"', re.DOTALL).findall(entry)
        thumb = match[0].replace("w=220&h=325","w=440&h=650")
        if not thumb.startswith("http:"):
            thumb = "http:"+thumb
        addShowDir(title, showID, 'listEpisodesByShowID', thumb, desc)
    match = re.compile('<div class="nextNav arrowNav">.+?data-results_page="(.+?)"', re.DOTALL).findall(content)
    if match:
        addDir(translation(30012), baseUrl+match[0], "listShowsURL", icon)
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewIDShows+')')


def search(type):
    keyboard = xbmc.Keyboard('', translation(30008))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        search_string = keyboard.getText().replace(" ", "+")
        if type=="shows":
            xbmcplugin.setContent(pluginhandle, "movies")
            content = opener.open(baseUrl+"/search?search="+search_string+"&type="+type+"&sort_by=relevant").read()
            listShowContent(content)
        elif type=="episodes":
            listEpisodesSearch(baseUrl+"/search/get_episode_results?search="+search_string+"&page_length=30&first_page_length=30&sort_by=relevant&page=1&no_wrap=1")


def playVideo(videoID):
    content = opener.open(baseUrl+"/rss/flash/"+videoID).read()
    match = re.compile('<media:content url="(.+?)" blip:role="(.+?)"', re.DOTALL).findall(content)
    streamURL = ""
    subURL = ""
    for url, title in match:
        if title=="Blip SD":
            streamURL = url
        elif title=="Closed Captioning - English":
            subURL = url
    for url, title in match:
        if title=="Blip HD 720" and (maxVideoQuality=="720p" or maxVideoQuality=="Source"):
            streamURL = url
    for url, title in match:
        if title=="Source" and maxVideoQuality=="Source":
            streamURL = url
    for url, title in match:
        if title=="Source" and not streamURL:
            streamURL = url
            if showNotConverted:
                xbmc.executebuiltin('XBMC.Notification(Blip.tv:,'+str(translation(30018))+',10000)')
    match = re.compile('<item>.+?<title>(.+?)</title>', re.DOTALL).findall(content)
    title = match[0]
    match = re.compile('<media:thumbnail url="(.+?)"/>', re.DOTALL).findall(content)
    thumb = match[0]
    listitem = xbmcgui.ListItem(path=streamURL, thumbnailImage=thumb)
    listitem.setInfo(type='Video', infoLabels={'Title': title})
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
    if showSubtitles and subURL:
        xbmc.sleep(1000)
        xbmc.Player().setSubtitles(subURL)


def queueVideo(url, name, thumb):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    listitem = xbmcgui.ListItem(name, thumbnailImage=thumb)
    playlist.add(url, listitem)


def listShowsFavs():
    xbmcplugin.setContent(pluginhandle, "movies")
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    if os.path.exists(channelFavsFile):
        fh = open(channelFavsFile, 'r')
        all_lines = fh.readlines()
        for line in all_lines:
            title = line[line.find("###TITLE###=")+12:]
            title = title[:title.find("#")]
            url = line[line.find("###URL###=")+10:]
            url = url[:url.find("#")]
            thumb = line[line.find("###THUMB###=")+12:]
            thumb = thumb[:thumb.find("#")]
            addShowFavDir(title, urllib.unquote_plus(url), "listEpisodesByShowID", thumb)
        fh.close()
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewIDShows+')')


def favs(param):
    mode = param[param.find("###MODE###=")+11:]
    mode = mode[:mode.find("###")]
    channelEntry = param[param.find("###TITLE###="):]
    if mode == "ADD":
        if os.path.exists(channelFavsFile):
            fh = open(channelFavsFile, 'r')
            content = fh.read()
            fh.close()
            if content.find(channelEntry) == -1:
                fh = open(channelFavsFile, 'a')
                fh.write(channelEntry+"\n")
                fh.close()
        else:
            fh = open(channelFavsFile, 'a')
            fh.write(channelEntry+"\n")
            fh.close()
    elif mode == "REMOVE":
        refresh = param[param.find("###REFRESH###=")+14:]
        refresh = refresh[:refresh.find("#")]
        fh = open(channelFavsFile, 'r')
        content = fh.read()
        fh.close()
        entry = content[content.find(channelEntry):]
        fh = open(channelFavsFile, 'w')
        fh.write(content.replace(channelEntry+"\n", ""))
        fh.close()
        if refresh == "TRUE":
            xbmc.executebuiltin("Container.Refresh")


def cleanTitle(title):
    title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#39;", "'").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
    title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö")
    title = title.replace('\\"', '"').strip()
    return title


def translation(id):
    return addon.getLocalizedString(id).encode('utf-8')


def getPluginUrl():
    if xbox:
        return "plugin://video/"+addon.getAddonInfo('name')+"/"
    else:
        return "plugin://"+addonID+"/"


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


def addLink(name, url, mode, iconimage, desc="", duration=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc, "Duration": duration})
    liz.setProperty('IsPlayable', 'true')
    if useThumbAsFanart and iconimage!=icon:
        liz.setProperty("fanart_image", iconimage)
    liz.addContextMenuItems([(translation(30013), 'RunPlugin('+getPluginUrl()+'/?mode=queueVideo&url='+urllib.quote_plus(u)+'&name='+urllib.quote_plus(name)+'&thumb='+urllib.quote_plus(iconimage)+')',)])
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


def addDir(name, url, mode, iconimage, desc=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    if useThumbAsFanart and iconimage!=icon:
        liz.setProperty("fanart_image", iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addShowDir(name, url, mode, iconimage, desc=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    if useThumbAsFanart and iconimage!=icon:
        liz.setProperty("fanart_image", iconimage)
    playListInfos = "###MODE###=ADD###TITLE###="+name+"###URL###="+urllib.quote_plus(url)+"###THUMB###="+iconimage+"###END###"
    liz.addContextMenuItems([(translation(30014), 'RunPlugin('+getPluginUrl()+'/?mode=favs&url='+urllib.quote_plus(playListInfos)+')',)])
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addShowFavDir(name, url, mode, iconimage, desc=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    if useThumbAsFanart and iconimage!=icon:
        liz.setProperty("fanart_image", iconimage)
    playListInfos = "###MODE###=REMOVE###REFRESH###=TRUE###TITLE###="+name+"###URL###="+urllib.quote_plus(url)+"###THUMB###="+iconimage+"###END###"
    liz.addContextMenuItems([(translation(30015), 'RunPlugin('+getPluginUrl()+'/?mode=favs&url='+urllib.quote_plus(playListInfos)+')',)])
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
name = urllib.unquote_plus(params.get('name', ''))
thumb = urllib.unquote_plus(params.get('thumb', ''))

if mode == 'listVideos':
    listVideos(url)
elif mode == 'listEpisodesMain':
    listEpisodesMain()
elif mode == 'listEpisodes':
    listEpisodes(url)
elif mode == 'listEpisodesByShowID':
    listEpisodesByShowID(url)
elif mode == 'listEpisodesLatest':
    listEpisodesLatest(url)
elif mode == 'listLatestAll':
    listLatestAll()
elif mode == 'listEpisodesFeaturedMain':
    listEpisodesFeaturedMain()
elif mode == 'listEpisodesFeatured':
    listEpisodesFeatured(url)
elif mode == 'listEpisodesSearch':
    listEpisodesSearch(url)
elif mode == 'listShowsMain':
    listShowsMain()
elif mode == 'listShowsMain2':
    listShowsMain2(url)
elif mode == 'listShows':
    listShows(url)
elif mode == 'listShowsURL':
    listShowsURL(url)
elif mode == 'listShowsStaff':
    listShowsStaff(url)
elif mode == 'listShowsAudience':
    listShowsAudience(url)
elif mode == 'listShowsBlipPicks':
    listShowsBlipPicks()
elif mode == 'listShowsFavs':
    listShowsFavs()
elif mode == 'queueVideo':
    queueVideo(url, name, thumb)
elif mode == 'playVideo':
    playVideo(url)
elif mode == 'search':
    search(url)
elif mode == 'favs':
    favs(url)
else:
    index()
