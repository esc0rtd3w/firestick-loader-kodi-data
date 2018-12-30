#
#      Copyright (C) Sean Poyser
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import urllib
import urllib2
import random
import re
import os

import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui


ADDONID = 'plugin.video.funniermoments'
ADDON   = xbmcaddon.Addon(ADDONID)
HOME    = ADDON.getAddonInfo('path')
TITLE   = ADDON.getAddonInfo('name')
VERSION = ADDON.getAddonInfo('version')
ARTWORK = os.path.join(HOME, 'resources', 'artwork')
ICON    = os.path.join(HOME, 'icon.png')
FANART  = os.path.join(HOME, 'fanart.jpg')
URL     = 'http://www.funniermoments.com/'
URL     = 'http://toon.is/'
WWW     = 'http://www.toon.is/'


ALL      = 100
NEW      = 200
TOP      = 300
RANDOM   = 400
PROGRAM  = 500
CARTOON  = 600
KIDSTIME = 700
SEARCH   = 800
LIBRARY  = 900
DOWNLOAD = 1000
MORE     = 1100
RESULTS  = 1200


try:    NMR_KIDSTIME = int(ADDON.getSetting('KIDSTIME'))
except: NMR_KIDSTIME = 10


def CheckVersion():
    prev = ADDON.getSetting('VERSION')
    curr = VERSION

    if prev == curr:
        return

    ADDON.setSetting('VERSION', curr)

    #xbmcgui.Dialog().ok(TITLE + ' - ' + VERSION, 'Funnier Moments acquires distribution rights for all videos', 'This costs money - please consider a small donation', 'via the website - www.funniermoments.com')

    #call showChangeLog like this to workaround bug in openElec
    script = os.path.join(HOME, 'showChangelog.py')
    cmd    = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % ('changelog', script, ADDONID, 0)
    xbmc.executebuiltin(cmd)



def Clean(text):
    text = text.replace('&amp;#39;', '\'')
    text = text.replace('&#8211;',   '-')
    text = text.replace('&#8217;',   '\'')
    text = text.replace('&#8220;',   '"')
    text = text.replace('&#8221;',   '"')
    text = text.replace('&#39;',     '\'')
    text = text.replace('&euml;',    'e')
    text = text.replace('<b>',       '')
    text = text.replace('</b>',      '')
    text = text.replace('&amp;',     '&')
    text = text.replace('\ufeff',    '')
    text = text.replace('&nbsp;',    ' ')
    return text.strip()


def FixURL(url):
    url = url.replace('\\\'', '%27')
    return url



def PostHTML(url, data, maxAge = 86400):
    html = geturllib.PostURL(url, data, maxAge)
    html = html.replace('\n', '')
    html = html.replace('\t', '')
    return html


def GetHTML(url, maxAge = 86400):
    html = geturllib.GetURL(url,maxAge)
    html = html.replace('\n', '')
    html = html.replace('\t', '')
    return html


def Main():
    CheckVersion()

    kidstime = 'Kids Time (%d Random Cartoons)' % NMR_KIDSTIME

    AddSection(kidstime,         'kidstime', KIDSTIME, False)    
    AddSection('All Moments',    'all',      ALL)
    AddSection('New Moments',    'new',      NEW)
    AddSection('Top Moments',    'top',      TOP)
    AddSection('Random Moment',  'random',   RANDOM,   False)
    AddSection('Search Moments', 'search',   SEARCH)


def AddSection(name, image, mode, isFolder=True):
    AddDir(name, mode, image=os.path.join(ARTWORK, image+'.png'), isFolder=isFolder)


def AddMore(mode, url, page, keyword = None):
    AddDir('More Moments...', mode, url, image=os.path.join(ARTWORK, 'more.png'), page=page, keyword=keyword)


def AddDir(name, mode, url='', image=None, isFolder=True, page=1, keyword=None, infoLabels=None, contextMenu=None):
    name = Clean(name)

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


def All():
    html  = GetHTML(URL)

    xbmc.log(html)
   
    #match = re.compile('<li class=""><h4><a href="(.+?)" class="">(.+?)</br></b></a> <p>\((.+?)\)</p></li>').findall(html)
    #match = re.compile('<li class=""><h4><a href="(.+?)" class="">(.+?)</a></h4><h6>\((.+?)\)</h6><br/></li>').findall(html)
    match = re.compile('li class=""><a href="(.+?)" class="">(.+?)</a><p>\((.+?)\)</p></li>').findall(html)  


                      
    list = []

    for url, title, nmr in match:
        if title not in list:
            menu = []
            menu.append(('Add to library', 'XBMC.RunPlugin(%s?mode=%d&title=%s&url=%s)' % (sys.argv[0], LIBRARY, urllib.quote_plus(title), urllib.quote_plus(url))))

            list.append(title)            
            AddProgram(title, nmr.strip(), url, 1, menu)


def Program(_url, page):
    page  = int(page)

    url = _url.replace('-date.', '-title.')

    html = GetHTML(url)
    html = html.split('<ul class="videolist">', 1)[-1]

    pagination = url.replace('videos-%d' % (page), 'videos-%d' % (page+1))
    parseCartoons(html, PROGRAM, _url, page, pagination)


def New(page):
    page  = int(page)

    _url = URL  + 'new/index.php'
    url  = _url + '?&page=%s' % str(page)

    html = GetHTML(url)

    split = 'Recently added videos'
    html  = html.split(split, 1)[-1]  

    pagination = '<a href="index.html?&page=%d"' % (page+1)
    parseCartoons(html, NEW, _url, page, pagination)



def Top(page):
    page  = int(page)

    _url = URL  + 'top/index.php'
    url  = _url + '?&page=%s' % str(page)

    html = GetHTML(url)

    split = 'Most popular episodes</h1>'
    html  = html.split(split, 1)[-1]

    pagination = '<a href="index.html?&page=%d"' % (page+1)
    parseCartoons(html, TOP, _url, page, pagination)


def GetRandom():
    url  = URL + 'randomizer.php'
    html = GetHTML(url, 0) 

    return GetInfo(html)


def GetInfo(html):
    html = html.split('<section id="video">', 1)[-1]

    try:
        title = re.compile('<h1.+?itemprop="name">(.+?)</h1>').search(html).group(1)
    except:
        title = None

    try:    
        url = re.compile("file: '%svids/(.+?),primary:" % URL).search(html).group(1)
        url = '%svids/' % URL + url[:-1]
    except:
        url = None

    try:
        img = re.compile("image: '%suploads/thumbs/(.+?)-1.jpg'" % WWW).search(html).group(1)
        img = '%suploads/thumbs/%s-1.jpg' % (WWW, img)
    except:
        img = None

    return title, img, url


def Random():
    title, img, url = GetRandom()
    PlayCartoon(title, img, url, True)


def AddCartoon(title, url, image):
    image += '|referer=%s' % URL

    menu = []
    menu.append(('Download', 'XBMC.RunPlugin(%s?mode=%d&title=%s&url=%s)' % (sys.argv[0], DOWNLOAD, urllib.quote_plus(title), urllib.quote_plus(url))))


    AddDir(title, CARTOON, url, image, isFolder=False, contextMenu=menu)


def AddProgram(title, nmr, url, page, menu):
    title += ' (%s)' % nmr
    AddDir(title, PROGRAM, url, page=page, contextMenu=menu)


def Download(title, _url):
    file = DownloadPath(_url)
    if not file:
        return

    url  = GetCartoonURL(_url)
    url  = url.rsplit('|', 1)[0]

    try:
        import download
        download.download(url, file, TITLE, URL)
    except Exception, e:
        print '%s - %s Error during downloading of %s' % (TITLE, VERSION, _url)
        print str(e)


def FileSystemSafe(text):
    text = re.sub('[:\\/*?\<>|"]+', '', text)
    return text.strip()


def DownloadPath(url):          
    downloadFolder = ADDON.getSetting('DOWNLOAD_FOLDER')

    if ADDON.getSetting('ASK_FOLDER') == 'true':
        d = xbmcgui.Dialog()
        downloadFolder = d.browse(3, 'Download to folder...', 'files', '', False, False, xbmc.translatePath(downloadFolder))
        if downloadFolder == '':
            return None

    if downloadFolder is '':
        d = xbmcgui.Dialog()
        d.ok('Funnier Moments', 'You have not set the default download folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings() 
        downloadFolder = xbmc.translatePath(ADDON.getSetting('DOWNLOAD_FOLDER'))

    if downloadFolder == '' and ADDON.getSetting('ASK_FOLDER') == 'true':
        dialog = xbmcgui.Dialog()
        downloadFolder = dialog.browse(3, 'Download to folder...', 'files', '', False, False, downloadFolder)   

    if downloadFolder == '' :
        return None

    downloadFolder = xbmc.translatePath(downloadFolder)

    html  = GetHTML(url)
    info  = GetInfo(html)
    title = FileSystemSafe(info[0])

    series, season, episode, name, ok = GetSeasonInfo(title)

    if ok:
        filename = '%s - %sx%s' % (name, season, episode)
    else:
        filename = title
   
    if ADDON.getSetting('ASK_FILENAME') == 'true':        
        kb = xbmc.Keyboard(filename, 'Download Cartoon as...' )
        kb.doModal()
        if kb.isConfirmed():
            filename = kb.getText()
        else:
            return None

    ext      = 'mp4'
    filename = FileSystemSafe(filename) + '.' + ext

    if not os.path.exists(downloadFolder):
        os.mkdir(downloadFolder)

    downloadFolder = os.path.join(downloadFolder, series)
    if not os.path.exists(downloadFolder):
        os.mkdir(downloadFolder)

    return os.path.join(downloadFolder, filename)


def AddToLibrary(series, _url, page):
    page  = int(page)

    sortBy = 'title'
    url    = _url + '&page=%s&sortby=%s' % (str(page), sortBy)

    html  = GetHTML(url)

    html = html.split('<ul class="videolist">', 1)[-1]

    match = re.compile('<li><a href="(.+?)">.+?<img src="(.+?)" alt="(.+?)"/></a></li>').findall(html)

    for url, img, title in match:
        if not AddCartoonToLibrary(title, url, img):
            d = xbmcgui.Dialog()
            d.ok(TITLE + ' - ' + VERSION, 'Failed to add to library.', Clean(series))
            return

    html = html.split('<ul class="pagination">')[-1]

    pages = re.compile('<li class=""><a href="show.php\?title=.+?page=(.+?)&sortby=.+?</a></li>').findall(html)

    allPages = []
    for p in pages:
        if not p in allPages:
            allPages.append(int(p))

    if page+1 in allPages:
        AddToLibrary(series, _url, page+1)


def AddCartoonToLibrary(title, url, img):
    try:
        series, season, episode, name, ok = GetSeasonInfo(title)
        if not ok:
            return False

        series = FixNameForLibrary(series)
        series = FileSystemSafe(series)

        library = xbmc.translatePath(ADDON.getSetting('LIBRARY'))
        if not os.path.exists(library):
            os.mkdir(library)

        library = os.path.join(library, series)
        if not os.path.exists(library):
            os.mkdir(library)

        library = os.path.join(library, 'Season %s' % season)
        if not os.path.exists(library):
            os.mkdir(library)

        episode = FixEpisodeForLibrary(series, episode)

        filename = '%sx%s - %s.strm' % (season, episode, name)
        fullname = os.path.join(library, filename)

        strm = '%s?mode=%d&url=%s&title=%s&image=%s&'% (sys.argv[0], CARTOON, urllib.quote_plus(url), urllib.quote_plus(title), urllib.quote_plus(img))
        
        file = open(fullname, 'w')
        file.write(strm)
        file.close()

    except Exception, e:
        print '%s - %s Error in AddCartoonToLibrary : %s' % (TITLE, VERSION, title) 
        print str(e)
        return False

    return True


def GetSeasonInfo(title, index = 0):
    items = title.split(' - ')

    if len(items) < 3:
        return '', '', '', '', False

    series = items[0]
    info   = items[1]
    name   = items[2]

    try:
        if 'x' in info:
            season = int(info.split('x', 1)[0])
        else:
            season = 1

        episode  = info.split('x', 1)[-1]
    except:
        season  = 1
        episode = index

    name = FileSystemSafe(name)

    #Adventures of Sonic - 04 - Slowwww Going
    #(1, 'Adventures of Sonic', '04 - Slowwww Going')

    #Flintstones - 1x08 - At the Races
    #(1, 'Flintstones', '1x08 - At the Races')

    return series, season, episode, Clean(name), True


def FixEpisodeForLibrary(series, episode):
    SERIES = series.upper()
    if SERIES == 'THE IMPOSSIBLES' and episode == '01':
        return '02'
    if SERIES == 'THE IMPOSSIBLES' and episode == '02':
        return '03'
    if SERIES == 'THE IMPOSSIBLES' and episode == '03':
        return '04'
    if SERIES == 'THE IMPOSSIBLES' and episode == '04':
        return '01'

    return episode


def FixNameForLibrary(series):
    SERIES = series.upper()

    if 'THE ADDAMS FAMILY' in SERIES:
        return 'The Addams Family (1973)'

    if 'THE ADVENTURES OF DON COYOTE' in SERIES:
        return 'Don Coyote and Sancho Panda'

    if 'AUGGIE DOGGIE & DOGGIE DADDY' in SERIES:
        return 'Augie Doggie & Doggie Daddy'
    
    if 'PAC-MAN (THE SERIES)' in SERIES:
        return 'Pac-Man'

    if 'SCOOBY\'S ALL-STAR LAFF-A-LYMPICS' in SERIES:
        return 'Scooby\'s All Star Laff-A-Lympics'

    if 'COPS (THE ANIMATED SERIES)' in SERIES:
        return 'C.O.P.S'

    if 'COW & CHICKEN' in SERIES:
        return 'Cow and Chicken'

    if 'THE FUNKY PHANTOM' in SERIES:
        return 'Funky Phantom'

    if 'GOOBER' in SERIES:
        return 'Goober and the Ghost-Chasers'

    if 'HEATHCLIFF & DINGBAT SHOW' in SERIES:
        return 'Heathcliff'

    if 'GRAPE APE' in SERIES:
        return 'Grape Ape'

    return series
   

def GetCartoonURL(url):
    html  = GetHTML(url)
    match = re.compile('%svids/(.+?).mp4' % URL).search(html).group(1)
    url   = '%svids/%s.mp4' % (URL, match)
    url   = FixURL(url)
    url   = urllib.unquote_plus(url)
    url  += '|referer=%s' % URL
    return url


def PlayCartoon(title, image, url, isResolved=False):    
    if not url:
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem('title'))

    if not isResolved:
        url = GetCartoonURL(url)

    if '|referer=' not in image:
        image += '|referer=%s' % URL

    liz = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)

    liz.setInfo(type="Video", infoLabels={ "Title": title} )
    liz.setPath(url)

    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
   

def KidsTime():
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()  

    titles = []

    for i in range(0, NMR_KIDSTIME):
        title, image, url = GetRandom()  
        if title not in titles:
            titles.append(title)

            liz = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image)

            liz.setInfo( type="Video", infoLabels={"Title": title})

            pl.add(url, liz)

            if i == 0:
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    

def GetSearchKeyword():
    kb = xbmc.Keyboard('', TITLE, False)
    kb.doModal()
    if not kb.isConfirmed():
        return None

    text = kb.getText()

    if text == '':
        return None

    return text


def Search(page, keyword):
    if not keyword or keyword == '':
        keyword = GetSearchKeyword()
    if not keyword or keyword == '':
        return

    url = URL + 'search.php?keywords=%s&page=' % urllib.quote_plus(keyword)

    SearchResults(url, page)


def SearchResults(url, page):
    page = int(page)
    _url = url
    url  = _url + str(page)

    html = GetHTML(url)
    html = html.split('Search Results')[-1]

    pagination = 'search.php' + url.split('search.php', 1)[-1].split('&page=')[0] + '&page=%d' % (page+1)
    parseCartoons(html, RESULTS, _url, page, pagination) 


def parseCartoons(html, mode, _url, page, pagination):
    items = html.split('<li>')
    for item in items:
        match = re.compile('<a href="(.+?)">.+?<img.+?src="(.+?)" alt="(.+?)"').findall(item.split('</li>', 1)[0])
        for url, img, title in match:
            url = url.split('"', 1)[0]

            AddCartoon(title, url, img)

    if pagination in html:
        AddMore(mode, pagination, page+1) 
        return

    pagination = pagination.replace('index.html', 'index.php')
    if pagination in html:
        AddMore(mode, pagination, page+1) 
 

    
def get_params(path):
    params = {}
    path   = path.split('?', 1)[-1]
    pairs  = path.split('&')

    for pair in pairs:
        split = pair.split('=')
        if len(split) > 1:
            params[split[0]] = urllib.unquote_plus(split[1])

    return params



import geturllib
geturllib.SetCacheDir(xbmc.translatePath(os.path.join('special://profile', 'addon_data', ADDONID ,'cache')))


params = get_params(sys.argv[2])
mode   = None

try:    mode = int(params['mode'])
except: pass

doEnd = True

if mode == ALL:
    All()

elif mode == NEW:
    page = params['page']
    New(page)

elif mode == TOP:
    page = params['page']
    Top(page)

elif mode == PROGRAM:
    url  = params['url']
    page = params['page']
    Program(url, page)


elif mode == MORE:
    url = params['url']
    More(url)


elif mode == CARTOON:
    url   = params['url']
    title = params['title']
    image = params['image']
    doEnd = False
    PlayCartoon(title, image, url)


elif mode == LIBRARY:
    url   = params['url']
    title = params['title']
    AddToLibrary(title, url, 1)


elif mode == DOWNLOAD:
    url   = params['url']
    title = params['title']
    doEnd = False
    Download(title, url)


elif mode == RANDOM:
    doEnd = False
    Random()


elif mode == KIDSTIME:
    doEnd = False
    KidsTime()


elif mode == SEARCH:
    page    = 1
    keyword = ''
    try:
        page    = params['page']
        keyword = params['keyword']
    except:
        pass
    Search(page, keyword)


elif mode == RESULTS:
    url  = params['url']
    page = params['page']
    url  = url.rsplit('=', 1)[0] + '=' 
    SearchResults(URL+url, page)

else:
    Main()
        

if doEnd:
    #xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)