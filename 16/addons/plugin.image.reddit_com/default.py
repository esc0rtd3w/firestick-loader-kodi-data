#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import socket
import sys
import re
import os
import json
import random
import datetime
import xbmcplugin
import xbmcgui
import xbmcaddon
import SimpleDownloader


addon = xbmcaddon.Addon()
pluginhandle = int(sys.argv[1])
addonID = addon.getAddonInfo('id')
xbox = xbmc.getCondVisibility("System.Platform.xbox")
osWin = xbmc.getCondVisibility('system.platform.windows')
osOsx = xbmc.getCondVisibility('system.platform.osx')
osLinux = xbmc.getCondVisibility('system.platform.linux')

socket.setdefaulttimeout(30)
opener = urllib2.build_opener()
userAgent = "XBMC | "+addonID+" | "+addon.getAddonInfo('version')
opener.addheaders = [('User-Agent', userAgent)]
urlMain = "http://www.reddit.com"

cat_new = addon.getSetting("cat_new") == "true"
cat_hot_h = addon.getSetting("cat_hot_h") == "true"
cat_hot_d = addon.getSetting("cat_hot_d") == "true"
cat_hot_w = addon.getSetting("cat_hot_w") == "true"
cat_hot_m = addon.getSetting("cat_hot_m") == "true"
cat_top_d = addon.getSetting("cat_top_d") == "true"
cat_top_w = addon.getSetting("cat_top_w") == "true"
cat_top_m = addon.getSetting("cat_top_m") == "true"
cat_top_y = addon.getSetting("cat_top_y") == "true"
cat_top_a = addon.getSetting("cat_top_a") == "true"
cat_com_h = addon.getSetting("cat_com_h") == "true"
cat_com_d = addon.getSetting("cat_com_d") == "true"
cat_com_w = addon.getSetting("cat_com_w") == "true"
cat_com_m = addon.getSetting("cat_com_m") == "true"
cat_com_y = addon.getSetting("cat_com_y") == "true"
cat_com_a = addon.getSetting("cat_com_a") == "true"

filter = addon.getSetting("filter") == "true"
filterRating = int(addon.getSetting("filterRating"))
filterThreshold = int(addon.getSetting("filterThreshold"))

forceViewMode = addon.getSetting("forceViewMode") == "true"
viewMode = str(addon.getSetting("viewMode"))

itemsPerPage = int(addon.getSetting("itemsPerPage"))
itemsPerPage = ["25", "50", "75", "100"][itemsPerPage]

searchSort = int(addon.getSetting("searchSort"))
searchSort = ["ask", "relevance", "new", "hot", "top", "comments"][searchSort]
searchTime = int(addon.getSetting("searchTime"))
searchTime = ["ask", "hour", "day", "week", "month", "year", "all"][searchTime]

showBrowser = addon.getSetting("showBrowser") == "true"
browser_win = int(addon.getSetting("browser_win"))
browser_wb_zoom = str(addon.getSetting("browser_wb_zoom"))

downDir = str(addon.getSetting("downDir"))

addonUserDataFolder = xbmc.translatePath("special://profile/addon_data/"+addonID)
subredditsFile = xbmc.translatePath("special://profile/addon_data/"+addonID+"/subreddits")
nsfwFile = xbmc.translatePath("special://profile/addon_data/"+addonID+"/nsfw")
if not os.path.isdir(addonUserDataFolder):
    os.mkdir(addonUserDataFolder)

allHosterQuery = urllib.quote_plus("site:imgur.com")
if os.path.exists(nsfwFile):
    nsfw = ""
else:
    nsfw = "nsfw:no+"


def addSubreddit(subreddit):
    alreadyIn = False
    fh = open(subredditsFile, 'r')
    content = fh.readlines()
    fh.close()
    if subreddit:
        for line in content:
            if line.lower()==subreddit.lower():
                alreadyIn = True
        if not alreadyIn:
            fh = open(subredditsFile, 'a')
            fh.write(subreddit+'\n')
            fh.close()
    else:
        keyboard = xbmc.Keyboard('', translation(30001))
        keyboard.doModal()
        if keyboard.isConfirmed() and keyboard.getText():
            subreddit = keyboard.getText()
            for line in content:
                if line.lower()==subreddit.lower()+"\n":
                    alreadyIn = True
            if not alreadyIn:
                fh = open(subredditsFile, 'a')
                fh.write(subreddit+'\n')
                fh.close()


def removeSubreddit(subreddit):
    fh = open(subredditsFile, 'r')
    content = fh.readlines()
    fh.close()
    contentNew = ""
    for line in content:
        if line!=subreddit+'\n':
            contentNew+=line
    fh = open(subredditsFile, 'w')
    fh.write(contentNew)
    fh.close()
    xbmc.executebuiltin("Container.Refresh")


def index():
    content = ""
    if os.path.exists(subredditsFile):
        fh = open(subredditsFile, 'r')
        content = fh.read()
        fh.close()
    if "all\n" not in content:
        fh = open(subredditsFile, 'a')
        fh.write('all\n')
        fh.close()
    if "earthporn\n" not in content:
        fh = open(subredditsFile, 'a')
        fh.write('earthporn\n')
        fh.close()
    entries = []
    if os.path.exists(subredditsFile):
        fh = open(subredditsFile, 'r')
        content = fh.read()
        fh.close()
        spl = content.split('\n')
        for i in range(0, len(spl), 1):
            if spl[i]:
                subreddit = spl[i].strip()
                entries.append(subreddit.title())
    entries.sort()
    for entry in entries:
        if entry.lower() in ["all", "earthporn"]:
            addDir(entry, entry.lower(), 'listSorting', "")
        else:
            addDirR(entry, entry.lower(), 'listSorting', "")
    #addDir("[ Imgur.com ]", "all", 'listSorting', "", "site:imgur.com")
    addDir("[B]- "+translation(30001)+"[/B]", "", 'addSubreddit', "")
    addDir("[B]- "+translation(30019)+"[/B]", "", 'searchReddits', "")
    xbmcplugin.endOfDirectory(pluginhandle)


def listSorting(subreddit, hosterQuery):
    hosterQuery = urllib.quote_plus(hosterQuery)
    if not hosterQuery:
        hosterQuery = allHosterQuery
    if cat_new:
        addDir(translation(30003), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=new&restrict_sr=on&limit="+itemsPerPage, 'listImages', "", subreddit)
    if cat_hot_h:
        addDir(translation(30002)+": "+translation(30006), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=hot&restrict_sr=on&limit="+itemsPerPage+"&t=hour", 'listImages', "", subreddit)
    if cat_hot_d:
        addDir(translation(30002)+": "+translation(30007), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=hot&restrict_sr=on&limit="+itemsPerPage+"&t=day", 'listImages', "", subreddit)
    if cat_hot_w:
        addDir(translation(30002)+": "+translation(30008), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=hot&restrict_sr=on&limit="+itemsPerPage+"&t=week", 'listImages', "", subreddit)
    if cat_hot_m:
        addDir(translation(30002)+": "+translation(30009), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=hot&restrict_sr=on&limit="+itemsPerPage+"&t=month", 'listImages', "", subreddit)
    if cat_top_d:
        addDir(translation(30004)+": "+translation(30007), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=top&restrict_sr=on&limit="+itemsPerPage+"&t=day", 'listImages', "", subreddit)
    if cat_top_w:
        addDir(translation(30004)+": "+translation(30008), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=top&restrict_sr=on&limit="+itemsPerPage+"&t=week", 'listImages', "", subreddit)
    if cat_top_m:
        addDir(translation(30004)+": "+translation(30009), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=top&restrict_sr=on&limit="+itemsPerPage+"&t=month", 'listImages', "", subreddit)
    if cat_top_y:
        addDir(translation(30004)+": "+translation(30010), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=top&restrict_sr=on&limit="+itemsPerPage+"&t=year", 'listImages', "", subreddit)
    if cat_top_a:
        addDir(translation(30004)+": "+translation(30011), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=top&restrict_sr=on&limit="+itemsPerPage+"&t=all", 'listImages', "", subreddit)
    if cat_com_h:
        addDir(translation(30005)+": "+translation(30006), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=comments&restrict_sr=on&limit="+itemsPerPage+"&t=hour", 'listImages', "", subreddit)
    if cat_com_d:
        addDir(translation(30005)+": "+translation(30007), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=comments&restrict_sr=on&limit="+itemsPerPage+"&t=day", 'listImages', "", subreddit)
    if cat_com_w:
        addDir(translation(30005)+": "+translation(30008), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=comments&restrict_sr=on&limit="+itemsPerPage+"&t=week", 'listImages', "", subreddit)
    if cat_com_m:
        addDir(translation(30005)+": "+translation(30009), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=comments&restrict_sr=on&limit="+itemsPerPage+"&t=month", 'listImages', "", subreddit)
    if cat_com_y:
        addDir(translation(30005)+": "+translation(30010), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=comments&restrict_sr=on&limit="+itemsPerPage+"&t=year", 'listImages', "", subreddit)
    if cat_com_a:
        addDir(translation(30005)+": "+translation(30011), urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"&sort=comments&restrict_sr=on&limit="+itemsPerPage+"&t=all", 'listImages', "", subreddit)
    addDir("[B]- "+translation(30023)+"[/B]", subreddit, "listFavourites", "")
    addDir("[B]- "+translation(30017)+"[/B]", subreddit, "searchImages", "")
    xbmcplugin.endOfDirectory(pluginhandle)


def listImages(url, subreddit):
    currentUrl = url
    xbmcplugin.setContent(pluginhandle, "episodes")
    content = opener.open(url).read()
    content = json.loads(content.replace('\\"', '\''))
    count = 1
    for entry in content['data']['children']:
        try:
            title = cleanTitle(entry['data']['title'].encode('utf-8'))
            commentsUrl = urlMain+entry['data']['permalink'].encode('utf-8')
            try:
                date = str(entry['data']['created_utc'])
                date = date.split(".")[0]
                dateTime = str(datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M'))
                date = dateTime.split(" ")[0]
            except:
                date = ""
                dateTime = ""
            ups = entry['data']['ups']
            downs = entry['data']['downs']
            rating = 100
            if ups+downs>0:
                rating = int(ups*100/(ups+downs))
            if filter and (ups+downs) > filterThreshold and rating < filterRating:
                continue
            comments = entry['data']['num_comments']
            try:
                thumb = entry['data']['thumbnail'].encode('utf-8')
            except:
                thumb = ""
            url = entry['data']['url']+'"'
            matchImgur = re.compile('imgur.com/(.+?)"', re.DOTALL).findall(url)
            if matchImgur:
                url = matchImgur[0]
            if url:
                if url.startswith("a/"):
                    addDir("Album: "+title, url.split("/")[1], "listImgurAlbum", thumb)
                elif not url.lower().endswith(".gif"):
                    if "." not in url:
                        url = url+".jpg"
                    url = ("http://i.imgur.com/"+url).replace("/gallery/","/")
                    addLink(title, url, subreddit, commentsUrl)
        except:
            pass
    try:
        after = content['data']['after']
        if "&after=" in currentUrl:
            nextUrl = currentUrl[:currentUrl.find("&after=")]+"&after="+after
        else:
            nextUrl = currentUrl+"&after="+after
        addDir(translation(30016), nextUrl, 'listImages', "", subreddit)
    except:
        pass
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')


def listImgurAlbum(album, title):
    content = opener.open("http://imgur.com/a/"+album).read()
    match1 = re.compile('<img class="unloaded" data-src="(.+?)"', re.DOTALL).findall(content)
    match2 = re.compile('class="unloaded thumb-title" title=".*?" alt=".*?" data-src="(.+?)"', re.DOTALL).findall(content)
    if match1:
        match = match1
    elif match2:
        match = match2
    count = 1
    for url in match:
        if not url.lower().endswith(".gif"):
            addLink2(str(count)+". "+title.replace("Album: ", ""), url)
            count+=1
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')


def listFavourites(subreddit):
    xbmcplugin.setContent(pluginhandle, "episodes")
    file = os.path.join(addonUserDataFolder, subreddit+".fav")
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    if os.path.exists(file):
        fh = open(file, 'r')
        content = fh.read()
        fh.close()
        match = re.compile('<favourite name="(.+?)" url="(.+?)" site="(.+?)" />', re.DOTALL).findall(content)
        for name, url, site in match:
            addFavLink(name, url, site, subreddit)
    xbmcplugin.endOfDirectory(pluginhandle)
    if forceViewMode:
        xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')


def getDownloadPluginUrl(url, title):
    if xbox:
        url = "plugin://image/Reddit.com/?mode=downloadImage&url=" + urllib.quote_plus(url)+"&name=" + urllib.quote_plus(title)
    else:
        url = "plugin://plugin.image.reddit_com/?mode=downloadImage&url=" + urllib.quote_plus(url)+"&name=" + urllib.quote_plus(title)
    return url


def downloadImage(url, title):
    downloader = SimpleDownloader.SimpleDownloader()
    global downDir
    while not downDir:
        xbmc.executebuiltin('XBMC.Notification(Download:,'+translation(30186)+'!,5000)')
        addon.openSettings()
        downDir = addon.getSetting("downDir")
    try:
        filename = (''.join(c for c in unicode(title, 'utf-8') if c not in '/\\:?"*|<>')).strip()+"."+url.split(".")[-1]
    except:
        filename = url.split("/")[-1]
    if not os.path.exists(os.path.join(downDir, filename)):
        params = { "url": url, "download_path": downDir }
        downloader.download(filename, params)
    else:
        xbmc.executebuiltin('XBMC.Notification(Download:,'+translation(30185)+'!,5000)')


def addToFavs(url, subreddit):
    file = os.path.join(addonUserDataFolder, subreddit+".fav")
    if os.path.exists(file):
        fh = open(file, 'r')
        content = fh.read()
        fh.close()
        if url not in content:
            fh = open(file, 'w')
            fh.write(content.replace("</favourites>", "    "+urllib.unquote_plus(urllib.unquote_plus(url)).replace("\n","<br>")+"\n</favourites>"))
            fh.close()
    else:
        fh = open(file, 'a')
        fh.write("<favourites>\n    "+urllib.unquote_plus(urllib.unquote_plus(url)).replace("\n","<br>")+"\n</favourites>")
        fh.close()


def removeFromFavs(url, subreddit):
    file = os.path.join(addonUserDataFolder, subreddit+".fav")
    fh = open(file, 'r')
    content = fh.read()
    fh.close()
    fh = open(file, 'w')
    fh.write(content.replace("    "+url.replace("\n","<br>")+"\n", ""))
    fh.close()
    xbmc.executebuiltin("Container.Refresh")


def searchImages(subreddit, hosterQuery):
    hosterQuery = urllib.quote_plus(hosterQuery)
    if not hosterQuery:
        hosterQuery = allHosterQuery
    keyboard = xbmc.Keyboard('', translation(30017))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        search_string = urllib.quote_plus(keyboard.getText().replace(" ", "+"))
        if searchSort == "ask":
            searchAskOne(urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"%20"+search_string+"&restrict_sr=on&limit="+itemsPerPage+"&sort=", subreddit)
        else:
            if searchTime == "ask":
                searchAskTwo(urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"%20"+search_string+"&restrict_sr=on&limit="+itemsPerPage+"&sort="+searchSort+"&t=", subreddit)
            else:
                listImages(urlMain+"/r/"+subreddit+"/search.json?q="+nsfw+hosterQuery+"%20"+search_string+"&restrict_sr=on&limit="+itemsPerPage+"&sort="+searchSort+"&t="+searchTime, subreddit)


def searchReddits():
    keyboard = xbmc.Keyboard('', translation(30017))
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        search_string = urllib.quote_plus(keyboard.getText().replace(" ", "+"))
        content = opener.open(urlMain+'/r/all/search?q='+search_string+'+'+nsfw+allHosterQuery+'&restrict_sr=on&sort=new&t=all').read()
        match = re.compile('<li class="searchfacet reddit"><a class="facet title word" href=".+?">/r/(.+?)</a>&nbsp;<span class="facet count number">\\((.+?)\\)</span></li>', re.DOTALL).findall(content)
        for subreddit, count in match:
            addDirA(subreddit.title(), subreddit, "listSorting", "")
        xbmcplugin.endOfDirectory(pluginhandle)


def searchAskOne(url, subreddit):
    addDir(translation(30114), url+"relevance", 'searchAskTwo', "", subreddit)
    addDir(translation(30115), url+"new", 'searchAskTwo', "", subreddit)
    addDir(translation(30116), url+"hot", 'searchAskTwo', "", subreddit)
    addDir(translation(30117), url+"top", 'searchAskTwo', "", subreddit)
    addDir(translation(30118), url+"comments", 'searchAskTwo', "", subreddit)
    xbmcplugin.endOfDirectory(pluginhandle)


def searchAskTwo(url, subreddit):
    if searchTime == "ask":
        addDir(translation(30119), url+"&t=hour", 'listImages', "", subreddit)
        addDir(translation(30120), url+"&t=day", 'listImages', "", subreddit)
        addDir(translation(30121), url+"&t=week", 'listImages', "", subreddit)
        addDir(translation(30122), url+"&t=month", 'listImages', "", subreddit)
        addDir(translation(30123), url+"&t=year", 'listImages', "", subreddit)
        addDir(translation(30124), url+"&t=all", 'listImages', "", subreddit)
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        listImages(url+"&t="+searchTime, subreddit)


def translation(id):
    return addon.getLocalizedString(id).encode('utf-8')


def cleanTitle(title):
        title = title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("&#039;","'").replace("&quot;","\"")
        return title.strip()


def toggleNSFW():
    if os.path.exists(nsfwFile):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(translation(30187), translation(30189)):
            os.remove(nsfwFile)
    else:
        dialog = xbmcgui.Dialog()
        if dialog.yesno(translation(30188), translation(30190)+"\n"+translation(30191)):
            fh = open(nsfwFile, 'w')
            fh.write("")
            fh.close()


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


def addLink(name, url, subreddit, site):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=url)
    liz.setInfo( type="Image", infoLabels={ "Title": name } )
    entries = []
    entries.append((translation(30025), 'RunPlugin('+getDownloadPluginUrl(url, name)+')',))
    favEntry = '<favourite name="'+urllib.quote_plus(name)+'" url="'+urllib.quote_plus(url)+'" site="'+urllib.quote_plus(site)+'" />'
    entries.append((translation(30022), 'RunPlugin(plugin://'+addonID+'/?mode=addToFavs&url='+urllib.quote_plus(favEntry)+'&type='+urllib.quote_plus(subreddit)+')',))
    if showBrowser and (osWin or osOsx or osLinux):
        if osWin and browser_win==0:
            entries.append((translation(30021), 'RunPlugin(plugin://plugin.program.webbrowser/?url='+urllib.quote_plus(site)+'&mode=showSite&zoom='+browser_wb_zoom+'&stopPlayback=no&showPopups=no&showScrollbar=no)',))
        else:
            entries.append((translation(30021), 'RunPlugin(plugin://plugin.program.chrome.launcher/?url='+urllib.quote_plus(site)+'&mode=showSite)',))
    liz.addContextMenuItems(entries)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok
    

def addLink2(name, url):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=url)
    liz.setInfo( type="Image", infoLabels={ "Title": name } )
    entries = []
    entries.append((translation(30025), 'RunPlugin('+getDownloadPluginUrl(url, name)+')',))
    liz.addContextMenuItems(entries)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok
    

def addFavLink(name, url, site, subreddit):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=url)
    liz.setInfo(type="Image", infoLabels={"Title": name})
    entries = []
    favEntry = '<favourite name="'+name+'" url="'+url+'" site="'+site+'" />'
    entries.append((translation(30024), 'RunPlugin(plugin://'+addonID+'/?mode=removeFromFavs&url='+urllib.quote_plus(favEntry)+'&type='+urllib.quote_plus(subreddit)+')',))
    if showBrowser and (osWin or osOsx or osLinux):
        if osWin and browser_win==0:
            entries.append((translation(30021), 'RunPlugin(plugin://plugin.program.webbrowser/?url='+urllib.quote_plus(site)+'&mode=showSite&zoom='+browser_wb_zoom+'&stopPlayback=no&showPopups=no&showScrollbar=no)',))
        else:
            entries.append((translation(30021), 'RunPlugin(plugin://plugin.program.chrome.launcher/?url='+urllib.quote_plus(site)+'&mode=showSite)',))
    liz.addContextMenuItems(entries)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


def addDir(name, url, mode, iconimage, type=""):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&type="+str(type)+"&name="+str(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addDirA(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.addContextMenuItems([(translation(30001), 'RunPlugin(plugin://'+addonID+'/?mode=addSubreddit&url='+urllib.quote_plus(url)+')',)])
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addDirR(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.addContextMenuItems([(translation(30013), 'RunPlugin(plugin://'+addonID+'/?mode=removeSubreddit&url='+urllib.quote_plus(url)+')',)])
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))
type = urllib.unquote_plus(params.get('type', ''))
name = urllib.unquote_plus(params.get('name', ''))

if mode == 'listImages':
    listImages(url, type)
elif mode == 'listImgurAlbum':
    listImgurAlbum(url, name)
elif mode == 'listSorting':
    listSorting(url, type)
elif mode == 'listFavourites':
    listFavourites(url)
elif mode == 'downloadImage':
    downloadImage(url, name)
elif mode == 'addSubreddit':
    addSubreddit(url)
elif mode == 'removeSubreddit':
    removeSubreddit(url)
elif mode == 'addToFavs':
    addToFavs(url, type)
elif mode == 'removeFromFavs':
    removeFromFavs(url, type)
elif mode == 'searchAskOne':
    searchAskOne(url, type)
elif mode == 'searchAskTwo':
    searchAskTwo(url, type)
elif mode == 'searchImages':
    searchImages(url, type)
elif mode == 'searchReddits':
    searchReddits()
elif mode == 'openSettings':
    openSettings(url)
elif mode == 'toggleNSFW':
    toggleNSFW()
else:
    index()
