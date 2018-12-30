import json
import urllib
import urllib2
import re
import sys
import cookielib
import os
import StringIO
import gzip
import time
import string
from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
import xbmcaddon
import xbmcplugin
import xbmcgui
from xml.dom.minidom import Document
import datetime


addon_id = "plugin.video.NoobRoom"
ADDON = __settings__ = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id)
datapath = addon.get_profile()
home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'noobroom.xml'))
tvfilename = xbmc.translatePath(os.path.join(home, 'resources', 'tvshow.xml'))
noobroomlogo = xbmc.translatePath(os.path.join(home, 'logo.png'))
cookie_path = os.path.join(datapath, 'cookies')
cookiefile = os.path.join(cookie_path, "cookiejar.lwp")
cj = None
authcode = ADDON.getSetting('authcode')
reg_list = ["15", "42", "62", "10", "18", "52", "65","72"]
if len(authcode) > 0 and authcode != "0":
    location = reg_list[int(ADDON.getSetting('region'))]
    isHD = "1"
else:
    isHD = "0"
    location = reg_list[0]
if ADDON.getSetting('use-hd') != 'true':
    isHD = "0"

latest = ADDON.getSetting('latest')
lst_list = [" 25 Added", " 50 Added", " 100 Added", " 500 Added", " All"]
latest = lst_list[int(ADDON.getSetting('latest'))]

strUsername = ADDON.getSetting('Username')
strpwd = ADDON.getSetting('Password').replace("@","%40")

genres = [
    "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family",
    "Fantasy", "Film-Noir", "Game-Show", "History", "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV",
    "Romance", "Sci-Fi", "Sport", "Talk-Show", "Thriller", "War", "Western"]

if os.path.exists(cookiefile):
    cj = cookielib.LWPCookieJar()
    cj.load(cookiefile, ignore_discard=True)
	
def GetContent(url, data, referr, cj):
    if cj is None:
        cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer', referr),
        ('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache')]
    usock = opener.open(url, data)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return (cj, response)


def GetInput(strMessage, headtxt, ishidden):
    keyboard = xbmc.Keyboard("", strMessage, ishidden)
    keyboard.setHeading(headtxt)  # optional
    keyboard.doModal()
    inputText = ""
    if keyboard.isConfirmed():
        inputText = keyboard.getText()
    del keyboard
    return inputText


def GetLoginCookie(cj, cookiefile):
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    if not os.path.exists(cookie_path):
        os.makedirs(cookie_path)
    if cj is None:
        cj = cookielib.LWPCookieJar()
    strUsername = urllib.quote_plus(
        GetInput("Please enter your username", "Username", False))
    respon = ""
    match=[]
    if strUsername is not None and strUsername != "":
        strpwd = urllib.quote_plus(GetInput("Please enter your password", "Password", True))
        (cj, respon) = GetContent(nooblink + "/login2.php", "email=" + strUsername +
                                  "&password=" + strpwd + "&remember=on", nooblink + "/login2.php", cj)
        cj.save(cookiefile, ignore_discard=True)
        link = ''.join(respon.splitlines()).replace('\'', '"')
        matchsrc = re.compile('setup\({(.+?)}\)').findall(link)
        if(len(matchsrc)==0):
              matchsrc = re.compile('"sources":\s*\[(.+?)\]').findall(link)
        match = re.compile('"streamer":\s*"(.+?)"').findall(matchsrc[0])
        if(len(match)==0):
              match = re.compile('"file":\s*"(.+?)"').findall(matchsrc[0])
        if(len(match) ==0):
           cj.load(cookiefile, ignore_discard=True)
           (cj, respon) = GetContent(nooblink + "/login2.php", "email=" + strUsername +
                                  "&password=" + strpwd + "&remember=on", nooblink + "/login2.php", cj)

           cj.save(cookiefile, ignore_discard=True)
           link = ''.join(respon.splitlines()).replace('\'', '"')

           matchsrc = re.compile('setup\({(.+?)}\)').findall(link)
           if(len(matchsrc)==0):
                 matchsrc = re.compile('"sources":\s*\[(.+?)\]').findall(link)
           match = re.compile('"streamer":\s*"(.+?)"').findall(matchsrc[0])
           if(len(match)==0):
                 match = re.compile('"file":\s*"(.+?)"').findall(matchsrc[0])
        loginsuc = match[0].split("&")[1]
        matchauth = loginsuc.replace("auth=", "")
        ADDON.setSetting('authcode', matchauth)

    cj = cookielib.LWPCookieJar()
    cj.load(cookiefile, ignore_discard=True)
    if len(match) == 0:
        ADDON.setSetting('authcode', "")
        d = xbmcgui.Dialog()
        d.ok("Incorrect Login", "Login failed", 'Try logging in again')
        return None
    else:
        ADDON.setSetting('Username', strUsername)
        ADDON.setSetting('Password', strpwd)
    return cj, respon


def GetNoobLink(cj):
    #(cj, link) = GetContent("http://www.noobroom.com", "", "", cj)
    #match = re.compile('value="(.+?)">').findall(link)
    return "http://superchillin.com/"


nooblink = GetNoobLink(cj)

def AutoLogin(url, cj):
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    if not os.path.exists(cookie_path):
        os.makedirs(cookie_path)
    if cj is None:
        cj = cookielib.LWPCookieJar()
    if strUsername is not None and strUsername != "" and strpwd is not None and strpwd != "":
      try:
        (cj, respon) = GetContent(nooblink + "/login2.php", "email=" + strUsername +
                                  "&password=" + strpwd + "&remember=on", nooblink + "/login2.php", cj)
        cj.save(cookiefile, ignore_discard=True)
        link = ''.join(respon.splitlines()).replace('\'', '"')
        matchsrc = re.compile('setup\({(.+?)}\)').findall(link)
        if(len(matchsrc)==0):
              matchsrc = re.compile('"sources":\s*\[(.+?)\]').findall(link)
        match = re.compile('"streamer":\s*"(.+?)"').findall(matchsrc[0])
        if(len(match)==0):
              match = re.compile('"file":\s*"(.+?)"').findall(matchsrc[0])
        loginsuc = match[0].split("&")[1]
      except:
        (cj, respon) = GetContent(nooblink + "/login2.php", "email=" + strUsername +
                                  "&password=" + strpwd + "&remember=on", nooblink + "/login2.php", cj)
        cj.save(cookiefile, ignore_discard=True)
        link = ''.join(respon.splitlines()).replace('\'', '"')
        matchsrc = re.compile('setup\({(.+?)}\)').findall(link)
        if(len(matchsrc)==0):
              matchsrc = re.compile('"sources":\s*\[(.+?)\]').findall(link)
        match = re.compile('"streamer":\s*"(.+?)"').findall(matchsrc[0])
        if(len(match)==0):
              match = re.compile('"file":\s*"(.+?)"').findall(matchsrc[0])
        loginsuc = match[0].split("&")[1]
      matchauth = loginsuc.replace("auth=", "")
      ADDON.setSetting('authcode', matchauth)
    cj.load(cookiefile, ignore_discard=True)
    return cj, respon

def SEARCHTC(name):
    searchText = urllib.quote_plus(name)
    SearchXml(searchText)
	
def GetVideoLink(url, isHD, cj):
    if len(strUsername) == 0 or len(strpwd) == 0:
        (cj, link) = GetLoginCookie(cj, cookiefile)
    else:
        (cj, link) = AutoLogin(url, cj)
    authstring = ""
    if len(authcode) > 0:
        authstring = "&auth=" + authcode
    else:
        isHD = "0"
    link = ''.join(link.splitlines()).replace('\'', '"')
    matchsrc = re.compile('setup\({(.+?)}\)').findall(link)
    if(len(matchsrc)==0):
              matchsrc = re.compile('"sources":\s*\[(.+?)\]').findall(link)
    match = re.compile('"streamer":\s*"(.+?)"').findall(matchsrc[0])
    if(len(match)==0):
              match = re.compile('"file":\s*"(.+?)"').findall(matchsrc[0])
    match=match[0].split("&")[0] + authstring + "&loc=" + location + "&hd=" + isHD
    return cj, match




def HOME():
    addDir('Search', 'search', 5, '')
    addDir('TV Shows', 'TV', 9, '')
    addDir('Movies A-Z', 'Movies', 2, '')
    addDir('Latest' + latest, 'Latest', 8, '')
    addDir('by Genre', 'GenreList', 14, '')
    addDir('by Release date', 'Released', 12, '')
    addDir('by IMDB Rating', 'ImdbRating', 13, '')
    addDir('Kids Zone', 'KidsZone', 16, '')
    addLink('Refresh Movie list', 'Refresh', 7, '')
    addLink('Login', 'Login', 11, '')


def INDEXAZ():
    addDir('*', '+', 4, '')
    addDir('?', '-1', 4, '')
    for one in string.ascii_uppercase:
        addDir(one, one, 4, '')


def SEARCH():
    keyb = xbmc.Keyboard('', 'Enter search text')
    keyb.doModal()
    searchText = ''
    if keyb.isConfirmed():
        searchText = urllib.quote_plus(keyb.getText())
    SearchSite(searchText)


def renderListingPage(resourceName, url):
    localfile = xbmc.translatePath(
        os.path.join(home, 'resources', resourceName + '.xml'))
    if os.path.isfile(localfile) is False:
        BuildXMl(cj, localfile, url)
    f = open(localfile, "r")
    text = f.read()
    match = re.compile(
        '<movie name="(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    if latest == " All":
        len_latest = len(match)
    else:
        len_latest = int(latest.replace(" ", "").replace("Added", ""))
        if len_latest > len(match):
           len_latest = len(match)
    for i in range(len_latest):
        (mName, mNumber, vyear) = match[i]
        addLink(urllib.unquote_plus(mName).replace("&amp;","&") + " (" + vyear + ")", mNumber, 6, nooblink + "/2img" + mNumber + ".jpg")


def Released():
    renderListingPage("released", "year.php")


def ImdbRating():
    renderListingPage("rating", "rating.php")


def GenreList(genre=''):
    if genre == '':
        for one in genres:
            addLink(one, string.lower(one), 15, '', True)

    else:
        genreHash = ""
        for one in genres:
            genreHash += "1" if string.lower(one) == genre else "0"

        (jc, link) = GetContent(nooblink + "/genre.php?b=" + genreHash, "", nooblink, cj)
        match = re.compile(
            '<br>(.+?)- <a class=\'tippable\' [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>'
        ).findall(link)

        if len(match) > 0:
            for one in match:
                (movieYear, moviehref, movieName) = one
                href = moviehref.replace("?", "")
                movieYear = movieYear.replace(" ", "")
                addLink('%s (%s)' % (urllib.unquote_plus(movieName), movieYear), href, 6, nooblink + "/2img" + href + ".jpg", False)
        else:
            xbmcplugin.endOfDirectory(handle=int(sysarg), updateListing=False, succeeded=True)
            xbmc.executebuiltin("XBMC.Notification(No movies found!,You have selected %s genre,3000)" % genre)


def Last25():
    renderListingPage("noobroom", "latest.php")


def KidsZone():
    (jc, link) = GetContent(nooblink + "/kids.php", "", nooblink, cj)
    matchname = re.compile(
        '<b><a style=\'color:#fff\' href=\'(.+?)\'>(.+?)</a>[^<]*</div>').findall(link)

    for i in range(len(matchname)):
        (href, movieName) = matchname[i]
        href = href.replace("?", "")
        addLink(urllib.unquote_plus(movieName), href, 6, nooblink + "/2img" + href + ".jpg", False)

def SearchXml(SearchText):
    if os.path.isfile(filename)==False:
        BuildXMl()
    f = open(filename, "r")
    text = f.read()

    matchAll=re.compile('<movie name="(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    matchAll.sort(key=lambda tup: tup[0]) # sort by mName normal for Movie [A-Z]

    if SearchText=='-1':
        matchSearch=re.compile('<movie name="[^A-Za-z](.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    else:
        matchSearch=re.compile('<movie name="' + SearchText + '(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)

    for j in range(len(matchAll)):
        (mName,mNumber,vyear)=matchAll[j]
        for i in range(len(matchSearch)):
            (smName,smNumber,svyear)=matchSearch[i]
            if smNumber == mNumber:
                addLink(urllib.unquote_plus(mName).replace("&amp;","&") + " (" + vyear + ")", mNumber, 6, nooblink + "/2img" + mNumber + ".jpg")

def SearchSite(SearchText):
    (jc, link) = GetContent(nooblink + "/search.php?q=" + SearchText, "", nooblink, cj)
    match = re.compile(
        '<a class=\'tippable\' [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>(.+?)<br>'
    ).findall(link.replace("\n",""))
    for i in range(len(match)):
        ( moviehref, movieName,movieYear) = match[i]
        href = moviehref.replace("?", "")
        addLink('%s %s' % (urllib.unquote_plus(movieName), movieYear), href, 6, nooblink + "/2img" + href + ".jpg")

def ParseXML(year, url, name, doc, mlist):
    movie = doc.createElement("movie")
    mlist.appendChild(movie)
    movie.setAttribute("year", year)
    movie.setAttribute("name", name)
    movie.setAttribute("url", url)

def RefreshAll():
    localfile = xbmc.translatePath(os.path.join(home, 'resources', 'noobroom.xml'))
    BuildXMl(cj, localfile, "latest.php")
    localfile = xbmc.translatePath(os.path.join(home, 'resources', 'rating.xml'))
    BuildXMl(cj, localfile, "rating.php")
    localfile = xbmc.translatePath(os.path.join(home, 'resources', 'released.xml'))
    BuildXMl(cj, localfile, "year.php")

def BuildXMl(cj, filename, url):
    xbmc.executebuiltin(
        "XBMC.Notification(Please Wait!,Refreshing Movie List,5000)")
    (cj, link) = GetContent(nooblink + "/" + url, "", nooblink, cj)
    mydoc = Document()
    mlist = mydoc.createElement("movielist")
    mydoc.appendChild(mlist)
    match = re.compile(
        '<br>(.+?)- <a class=\'tippable\' [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(link)
    for i in range(len(match)):
        (vyear, mNumber, mName) = match[i]
        ParseXML(vyear, mNumber.replace('?', ''),
                 urllib.quote_plus(mName).replace('+', ' '), mydoc, mlist)

    f = open(filename, 'w')
    f.write(mydoc.toprettyxml())
    f.close()


def GetDirVideoUrl(url, cj):
    if cj is None:
        cj = cookielib.LWPCookieJar()

    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):

        def http_error_302(self, req, fp, code, msg, headers):
            self.video_url = headers['Location']
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302

    redirhndler = MyHTTPRedirectHandler()

    opener = urllib2.build_opener(redirhndler, urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer', url),
        ('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache')]
    # urllib2.install_opener(opener)
    usock = opener.open(url)
    return redirhndler.video_url

def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok

def TryMP4(noobvideolink,videoId,cj,location):
    vidlink=GetDirVideoUrl(nooblink + "/"+location+"/"+authcode+"/"+videoId+".mp4", cj)
    if(vidlink.find(authcode) == -1):
         vidlink = GetDirVideoUrl(noobvideolink + "&tv=0" + "&start=0&file=" + videoId, cj) + "&loc=" + location
    vidlink=vidlink.replace("&hd=0","&hd=" + isHD)
    #print "exist nor not:" + str(exists(vidlink))
    return vidlink
	
def Episodes(name, videoId,cj):
    # try:
    xbmc.executebuiltin("XBMC.Notification(PLease Wait!, Loading video link into XBMC Media Player,5000)")
    (cj, noobvideolink) = GetVideoLink(nooblink + "/login2.php", isHD, cj)
    if(noobvideolink.find(nooblink) == -1):
          noobvideolink=nooblink+noobvideolink
    match = re.compile("/(.+?)&sp").findall(videoId + "&sp")
    if len(match) >= 0:
        videoId = match[0]
    try:
        vidlink=TryMP4(noobvideolink,videoId,cj,location)
    except:
        vidlink = GetDirVideoUrl(noobvideolink.replace("&hd=" + isHD, "&hd=0") + "&tv=0" + "&start=0&file=" + videoId, cj) + "&loc=" + location
    cookiestr = ""

    for cookie in cj:
        cookiestr += '%s=%s;' % (cookie.name, cookie.value)
    fullvid = ('%s|Cookie="%s"' % (vidlink, cookiestr + "save=1"))
    fullvid = ('%s|User-Agent="%s"' %
               (fullvid, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'))

    meta = {
        'Title': name,
        'Thumb': nooblink + "/2img" + videoId + ".jpg"
    }
    playVideo("noobroom", fullvid, meta)



def ListTVSeries(cj):
    (cj, link) = GetContent(nooblink + "/series.php", "", nooblink, cj)
    link = ''.join(link.splitlines()).replace('\'', '"')
    match = re.compile(
        '<table><tr><td><a href="(.+?)"><img style="border:0" src="(.+?)" width="(\d+)" height="(\d+)"></a>').findall(link)
    matchname = re.compile(
        '<b><a style="color:#fff" href="(.+?)">(.+?)</a></b>').findall(link)
    for i in range(len(match)):
        addDir(matchname[i][1], nooblink + match[i][0], 10, match[i][1])


def ListEpisodes(name,url, cj):
    (cj, noobvideolink) = GetVideoLink(nooblink + "/login2.php", isHD, cj)
    if(noobvideolink.find(nooblink) == -1):
          noobvideolink=nooblink+noobvideolink
    (cj, link) = GetContent(url, "", nooblink, cj)
    link = ''.join(link.splitlines()).replace('\'', '"')
    match = re.compile(
        '<br><b>(.+?)<a[^>]*color:#(\w+);[^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(link)
    cookiestr = ""
    for cookie in cj:
        cookiestr += '%s=%s;' % (cookie.name, cookie.value)
    for i in range(len(match)):
        vidlink = noobvideolink.replace("&hd=1", "&hd=0") + match[i][2].replace("/?", "&file=")

        fullvid = ('%s|Cookie="%s"' % (vidlink, cookiestr + "save=1"))
        fullvid = ('%s|User-Agent="%s"' %
                   (fullvid, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'))
        movieFree = ""
        if match[i][1] == "ffffcc":
            movieFree = " [COLOR yellow](free)[/COLOR]"
        addTVLink(match[i][0] + match[i][3] + movieFree, fullvid, 3, name)

		
def PlayAgain(url):
        win = xbmcgui.Window(10000)
        meta = {
                 'Title': win.getProperty('1ch.playing.title'),
                 'Thumb': ''
        }
        listitem = xbmcgui.ListItem(meta.get("Title"))
        listitem.setInfo('video', meta)
        listitem.setProperty('IsPlayable', 'true')
        xbmcPlayer  = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
        link=url.replace("&hd=" + isHD, "&hd=0")
        xbmcPlayer.play(link, listitem)
		
class MyPlayer(xbmc.Player):

    def __init__(self):
        xbmc.Player.__init__(self)
        self._totalTime = 999999
        self._lastPos = 0
        self.currentfile=""
    def setfile(self,url):
         self.currentfile=url
    def onPlayBackStarted(self):
        self._totalTime = self.getTotalTime()
        while not xbmc.abortRequested and self.isPlaying():
            self._lastPos = self.getTime()
            xbmc.sleep(500)

    def onPlayBackStopped(self):
        playedTime = int(self._lastPos)
        if playedTime == 0 and self._totalTime == 999999:
            PlayAgain(self.currentfile)


def playVideo(videoType, link, meta=None):
    if(meta==None):
             meta = {
                 'Title': '',
                 'Thumb': ''
    }
    win = xbmcgui.Window(10000)
    win.setProperty('1ch.playing.title', meta.get("Title"))
    win.setProperty('1ch.playing.season', str(3))
    win.setProperty('1ch.playing.episode', str(4))
    if(link.find(nooblink) > -1):
        tmplink= link.split("|")[0]
        tmplink2=GetDirVideoUrl(tmplink, cj)
        link=link.replace(tmplink,tmplink2) + "&loc=" + location + "&hd=0"
    print videoType + '=' + link
    if videoType == "youtube":
        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + link.replace('?', '')
        xbmc.executebuiltin("xbmc.PlayMedia(" + url + ")")
    else:

        listitem = xbmcgui.ListItem(meta.get("Title"))
        listitem.setInfo('video', meta)
        listitem.setProperty('IsPlayable', 'true')
        xbmcPlayer  = MyPlayer() #xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
        xbmcPlayer.setfile(link)
        xbmcPlayer.play(link, listitem)
        ctr=0
        while(not xbmc.abortRequested):
             ctr=ctr+1
             if(ctr==10):
				break
             xbmc.sleep(1000)

def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(
            time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S"))
        )
    except:
        #force update
        return datetime.datetime.today() - datetime.timedelta(days=1)


def addLink(name, url, mode, thumbImage, folder=False, iconImage="DefaultVideo.png"):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(
        url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    meta = {'title': name}
    liz = xbmcgui.ListItem(name, iconImage=iconImage, thumbnailImage=thumbImage)
    liz.setInfo('Video', meta)
    contextMenuItems = getContextMenuItems()
    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=folder)
    return ok

def addTVLink(name, url, mode, showname=""):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(
        url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)+ "&showname=" + urllib.quote_plus(showname)
    meta = {'title': name}
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage="")
    liz.setInfo('Video', meta)
    contextMenuItems = getContextMenuItems()
    liz.addContextMenuItems(contextMenuItems, replaceItems=True)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok
	
def addNext(formvar, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&formvar=" + str(
        formvar) + "&name=" + urllib.quote_plus('Next >')
    liz = xbmcgui.ListItem(
        'Next >', iconImage=noobroomlogo, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": 'Next >'})
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)


def addDir(name, url, mode, iconimage):
    addLink(name, url, mode, iconimage, True, noobroomlogo)


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def getContextMenuItems():
    menu_items = []
    menu_items.append(('Show Information', 'XBMC.Action(Info)'), )
    return menu_items


def getMovieInfo(movieName):
    jsonUrl = 'http://mymovieapi.com/?title=' + movieName + '&type=json&plot=simple&episode=1&limit=1&yg=0&mt=none&lang=en-US&offset=&aka=simple&release=simple&business=0&tech=0&year=2013'
    data = json.load(urllib2.urlopen(jsonUrl))
    return data

params = get_params()
url = None
name = None
mode = None
formvar = None
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
    formvar = int(params["formvar"])
except:
    pass
try:
    showname = urllib.unquote_plus(params["showname"])
except:
    showname=name
	
sysarg = str(sys.argv[1])

if mode is None or url is None or len(url) < 1:
    HOME()

elif mode == 2:
    INDEXAZ()
elif mode == 3:
    meta = {'Title': showname,'Thumb': ''}
    playVideo("noobroom", url,meta)
elif mode == 4:
    SearchXml(url)
elif mode == 5:
    SEARCH()
elif mode == 6:
    Episodes(name, str(url),cj)
elif mode == 7:
    RefreshAll()
elif mode == 8:
    Last25()
elif mode == 9:
    ListTVSeries(cj)
elif mode == 10:
    ListEpisodes(name,url, cj)
elif mode == 11:
    GetLoginCookie(cj, cookiefile)
elif mode == 12:
    Released()
elif mode == 13:
    ImdbRating()
elif mode == 14:
    GenreList()
elif mode == 15:
    GenreList(url)
elif mode == 16:
    KidsZone()
elif mode == 17:
    SEARCHTC(name)
xbmcplugin.endOfDirectory(int(sysarg))