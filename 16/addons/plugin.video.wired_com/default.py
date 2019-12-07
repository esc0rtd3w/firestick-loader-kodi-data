#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import sys
import re
import xbmcplugin
import xbmcgui
import xbmcaddon

addon = xbmcaddon.Addon()
socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
translation = addon.getLocalizedString
forceViewMode = addon.getSetting("forceViewMode") == "true"
useThumbAsFanart = addon.getSetting("useThumbAsFanart") == "true"
viewMode = str(addon.getSetting("viewMode"))
quality = addon.getSetting("quality")
urlMain = "http://video.wired.com"


def index():
    addDir(translation(30001), urlMain+"/new", 'listVideos', "")
    addDir("Popular", urlMain+"/popular", 'listVideos', "")
    addDir("Shows", "", 'listShows', "")
    addDir(translation(30002), "", 'listCats', "")
    #addDir(translation(30004), "", 'search', "")
    xbmcplugin.endOfDirectory(pluginhandle)


def listCats():
    content = getUrl(urlMain+"/genres")
    spl = content.split('class="cne-nav--drawer__item--categories"')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('class="cne-nav--drawer__title--categories">(.+?)<', re.DOTALL).findall(entry)
        title = match[0]
        title = cleanTitle(title)
        match = re.compile('href="(.+?)"', re.DOTALL).findall(entry)
        url = urlMain+match[0]
        match = re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0].replace("/c_fill,d_placeholder_cne.jpg,g_face,h_270,q_90,w_480", "")
        addDir(title, url, 'listVideos', thumb, "")
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')


def listShows():
    content = getUrl(urlMain+"/series")
    spl = content.split('<div class="cne-thumb-image cne-rollover">')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('<p class="cne-series-title">(.+?)</p>', re.DOTALL).findall(entry)
        title = match[0]
        title = cleanTitle(title)
        match = re.compile('<span class="cne-thumb-description">(.+?)</span>', re.DOTALL).findall(entry)
        desc = match[0]
        desc = cleanTitle(desc)
        match = re.compile('href="(.+?)"', re.DOTALL).findall(entry)
        url = urlMain+match[0]
        match = re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0].replace("/c_fill,d_placeholder_cne.jpg,g_face,h_270,q_90,w_480", "")
        addDir(title, url, 'listVideos', thumb, desc)
    
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')


def listVideos(url):
    urlTemp = url
    content = getUrl(url).replace("\\n", "").replace("\\", "")
    spl = content.split('<div class="cne-thumb cne-episode-block')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('<span class="cne-rollover-name">(.+?)</span>', re.DOTALL).findall(entry)
        title = match[0]
        title = cleanTitle(title)
        match = re.compile('<span class="cne-rollover-description">(.+?)</span>', re.DOTALL).findall(entry)
        desc = match[0]
        desc = cleanTitle(desc)
        match = re.compile('href="(.+?)"', re.DOTALL).findall(entry)
        url = urlMain+match[0]
        match = re.compile('src="(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0].replace("/c_fill,d_placeholder_cne.jpg,g_face,h_151,q_90,w_270", "")
        addLink(title, url, 'playVideo', thumb, desc)
    match = re.compile('cne-more-videos.+?data-ajaxurl="(.+?)"', re.DOTALL).findall(content)
    # match2=re.compile("'ajaxurl', '(.+?)'", re.DOTALL).findall(content)
    if match and "?category=" not in urlTemp:
        addDir(translation(30003), urlMain+match[0].replace("&amp;", "&"), 'listVideos', "")
    # elif match2:
    #    addDir(translation(30003), urlMain+match2[0].replace("&amp;","&"), 'listVideos', "")
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')


def search():
    keyboard = xbmc.Keyboard('', translation(30004))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        search_string = keyboard.getText().replace(" ", "%20")
        listVideos("http://video.wired.com/videos/search/"+search_string)


def playVideo(url):
    content = getUrl(url)
    match = re.compile('<link itemprop="contentURL" href="(.+?)">', re.DOTALL).findall(content)
    finalUrl = match[0]
    if quality == "1":
        finalUrl = finalUrl.replace("low.mp4", "high.webm")
    else:
        finalUrl = finalUrl.replace("low.mp4", "low.webm")
    listItem = xbmcgui.ListItem(path=finalUrl)
    xbmcplugin.setResolvedUrl(pluginhandle, True, listItem)


def cleanTitle(title):
    title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#x27;", "'").replace("&#39;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
    title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö")
    title = title.replace("n				", "").replace("n			", "").strip()
    return title


def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
    response = urllib2.urlopen(req)
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


def addLink(name, url, mode, iconimage, desc):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    liz.setProperty('IsPlayable', 'true')
    if useThumbAsFanart:
        liz.setProperty("fanart_image", iconimage)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


def addDir(name, url, mode, iconimage, desc=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))

if mode == 'listVideos':
    listVideos(url)
elif mode == 'listCats':
    listCats()
elif mode == 'listShows':
    listShows()
elif mode == 'playVideo':
    playVideo(url)
elif mode == 'search':
    search()
else:
    index()
