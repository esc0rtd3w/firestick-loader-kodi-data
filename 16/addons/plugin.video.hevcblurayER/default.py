import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import re, string, sys, os
import urlresolver
import HTMLParser
from TheYid.common.addon import Addon
from TheYid.common.net import Net

addon_id = 'plugin.video.hevcblurayER'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'hevcblurayER.db')
net = Net()
addon = Addon('plugin.video.hevcblurayER', sys.argv)
BASE_URL = 'http://hevcbluray.com'
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/"
FanartPath = AddonPath + "/icons/"
mode = addon.queries['mode']
url = addon.queries.get('url', None)
content = addon.queries.get('content', None)
query = addon.queries.get('query', None)
startPage = addon.queries.get('startPage', None)
numOfPages = addon.queries.get('numOfPages', None)
listitem = addon.queries.get('listitem', None)
urlList = addon.queries.get('urlList', None)
section = addon.queries.get('section', None)
img = addon.queries.get('img', None)
text = addon.queries.get('text', None)

def GetTitles(section, url, startPage= '1', numOfPages= '1'): 
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                      
                match = re.compile('<div id="mt-.+?" class="item">\s*?<a href="http://hevcbluray.com/(.+?)\s*?<div class="image">\s*?<img src="(.+?)" alt="(.+?)" width="100%" height="100%" />', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': 'http://www.hevcbluray.com/' + movieUrl , 'img': img , 'text': movieUrl.replace('-', ' ').replace('/', '')}, {'title': movieUrl.replace('-', ' ').replace('/', '')}, img= img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
                addon.add_directory({'mode': 'GetTitles', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
        setView('tvshows', 'tvshows-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles1(section, url, startPage= '1', numOfPages= '1'): 
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                      
                match = re.compile('<div id="mt-.+?" class="item">\s*?<a href="http://hevcbluray.com/(.+?)">\s*?<div class="image">\s*?<img src="(.+?)" alt="(.+?)" width="100%" height="100%" />', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': 'http://www.hevcbluray.com/' + movieUrl , 'img': img , 'text': movieUrl.replace('-', ' ').replace('/', '')}, {'title': movieUrl.replace('-', ' ').replace('/', '')}, img= img, fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
                addon.add_directory({'mode': 'GetTitles', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart= 'http://images.forwallpaper.com/files/thumbs/preview/64/646017__cinema_p.jpg')      
        setView('tvshows', 'tvshows-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(section, url, img, text):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" target="_blank">').findall(content)
        match1 = re.compile('<h1>(.+?)</h1>').findall(content)
        match3 = re.compile('<span class="calidad2">(.+?)</span>').findall(content)
        match4 = re.compile('<a href="(http://kumpulbagi.id/.+?)" target="_blank"').findall(content)
        match5 = re.compile('<a href="http://www.multiup.org/download/(.+?)" target="_blank"').findall(content)
        match2 = re.compile('<span class="dato"><a href="http://www.imdb.com/title/.+?" rel="nofollow" target="_blank">(.+?)</a> <b>(.+?)</b> <b>.+?</b></span>').findall(content)
        listitem = GetMediaInfo(content)
        for name in match1:
                addon.add_directory({'img': img}, {'title':  '[COLOR darkturquoise][B]' + name.strip() + '[/B] [/COLOR]'}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        for name in match3:
                addon.add_directory({'img': img}, {'title':  '[COLOR lime][B]' + name.strip() + '[/B] [/COLOR]'}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        for name, name1 in match2:
                addon.add_directory({'img': img}, {'title':  '[COLOR pink][B]' + name.strip() + ' ' + name1 +'[/B] [/COLOR]'}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        for url in match5:
                addon.add_directory({'mode': 'GetLinks3', 'url': 'http://www.multiup.org/en/mirror/' + url, 'listitem': listitem, 'img': img, 'text': text}, {'title':  'Multiup.org  : ' + text}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        for url in match4:
                addon.add_directory({'mode': 'GetLinks1', 'url': url, 'listitem': listitem, 'img': img, 'text': text}, {'title':  'kumpulbagi.id : Direct Link to = SD  ' + text}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks2(section, url, img, text):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="/en/mirror/(.+?)">').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                addon.add_directory({'mode': 'GetLinks3', 'url': 'http://www.multiup.org/en/mirror/' + url, 'listitem': listitem, 'img': img, 'text': text}, {'title': text + ' : ' + url}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks3(section, url, img, text):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('style="width:97%;text-align:left"\s*?href="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks1(section, url, img, text):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('''data-player="video" data-player-file="(.+?)"''').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo1', 'url': url, 'listitem': listitem, 'img': img, 'text': text}, {'title': text + ' : ' + url}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo1(text, img, url, listitem):
        addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(addon_handle, 'video')
        li = xbmcgui.ListItem(text, iconImage=img, thumbnailImage=img)
        li.setProperty('fanart_image', 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)


def PlayVideo(url, listitem):
    try:
        print 'in PlayVideo %s' % url
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^ Press back ^[/B] [/COLOR]'},'','')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Link may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")

def GetDomain(url):
        tmp = re.compile('//(.+?)/').findall(url)
        domain = 'Unknown'
        if len(tmp) > 0 :
            domain = tmp[0].replace('www.', '')
        return domain

def GetMediaInfo(html):
        listitem = xbmcgui.ListItem()
        match = re.search('og:title" content="(.+?) \((.+?)\)', html)
        if match:
                print match.group(1) + ' : '  + match.group(2)
                listitem.setInfo('video', {'Title': match.group(1), 'Year': int(match.group(2)) } )
        return listitem

def MainMenu():   
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest Added[/B]'}, img=IconPath + 'lat.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles1', 'section': 'ALL', 'url': BASE_URL + '/quality/720p/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest 720p[/B]'}, img=IconPath + '720.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles1', 'section': 'ALL', 'url': BASE_URL + '/quality/1080p/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest 1080p[/B]'}, img=IconPath + '1080.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles1', 'section': 'ALL', 'url': BASE_URL + '/quality/3d/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]Latest 3D[/B]'}, img=IconPath + '3d.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles1', 'section': 'ALL', 'url': BASE_URL + '/category/imdb',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]IMDB Top Movie[/B]'}, img=IconPath + 'imdb.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetTitles1', 'section': 'ALL', 'url': BASE_URL + '/tvshows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[B]TV Shows[/B]'}, img=IconPath + 'tv.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GenreMenu'}, {'title':  '[B]Movies by genre[/B]'}, img=IconPath + 'gen.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'YearMenu'}, {'title':  '[B]Movies by year[/B]'}, img=IconPath + 'year.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[COLOR green]Search[/COLOR]'}, img=IconPath + 'search.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR red]Resolver Settings[/COLOR]'}, img=IconPath + 'url1.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[B][COLOR yellow] www.entertainmentrepo.com  [/B][/COLOR]'}, img=IconPath + 'newart.jpg', fanart=IconPath +  'newart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GenreMenu(): 
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/action/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]action [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/adventure/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]adventure [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/animation/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]animation [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/biography/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]biography [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/comedy/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]comedy [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/crime/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]crime [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/documentary/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]documentary [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/drama/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]drama [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/family/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]family [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/fantasy/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]fantasy [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/foreign/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]foreign [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/history/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]history [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/horror/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]horror [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/music/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]music [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/musical/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]musical [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/mystery/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]mystery [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/romance/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]romance [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/science-fiction/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]science fiction [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/sport/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]sport [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/thriller/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]thriller [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/tv-movie/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]tv movie [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/war/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]war [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/category/western/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]western [/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def YearMenu(): 
        #addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2017/',
                             #'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2017 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2016/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2016[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2015/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2015 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2014/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2014[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2013/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2013 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2012/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2012[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2011/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2011 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2010/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2010[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2009/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2009 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2008/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2008[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2007/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2007 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2006/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2006[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2005/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2005 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2004/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2004[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2003/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2003 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2002/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2002[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2001/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2001 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/2000/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]2000[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1999/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1999 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1998/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1998[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1997/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1997 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1996/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1996[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1995/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1995 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1994/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1994[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1993/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1993 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1992/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1992[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1991/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1991 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1990/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1990[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1989/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1989 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1988/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1988[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1987/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1987 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1986/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1986[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1985/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1985 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1984/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1984[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1983/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1983 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1982/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1982[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1981/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1981 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1980/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1980[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1979/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1979 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1978/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1978[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1977/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1977 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1976/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1976[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1975/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1975 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1974/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1974[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1973/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1973 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1972/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1972[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1971/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1971 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1970/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1970[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1969/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1969 [/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/release-year/1968/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lime]1968[/COLOR] >>'}, img=IconPath + 'icon.png', fanart= 'http://www.hdesktops.com/wp-content/uploads/2013/12/purple-3d-abstract-wallpaper-desktop-background-171.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))



def GetSearchQuery():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('Search')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search(query)
	else:
                return

def Search(query):
        url = 'http://hevcbluray.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div id="mt-.+?" class="item">\s*?<a href="http://hevcbluray.com/(.+?)">\s*?<div class="image">\s*?<img src="(.+?)" alt="(.+?)" width="100%" height="100%" />').findall(html)
        for url, img, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://hevcbluray.com/' + url, 'img': img , 'text': title }, {'title':  title}, img= img, fanart=FanartPath + 'fanart.jpg')
        setView('tvshows', 'tvshows-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if addon.get_setting('auto-view') == 'true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )

if mode == 'main': 
	MainMenu()
elif mode == 'GenreMenu':
        GenreMenu()
elif mode == 'YearMenu':
        YearMenu()
elif mode == 'GetTitles': 
	GetTitles(section, url, startPage, numOfPages)
elif mode == 'GetTitles1': 
	GetTitles1(section, url)
elif mode == 'GetLinks':
	GetLinks(section, url, img, text)
elif mode == 'GetLinks1':
	GetLinks1(section, url, img, text)
elif mode == 'GetLinks2':
	GetLinks2(section, url, img, text)
elif mode == 'GetLinks3':
	GetLinks3(section, url, img, text)
elif mode == 'GetSearchQuery':
	GetSearchQuery()
elif mode == 'Search':
	Search(query)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)
elif mode == 'PlayVideo1':
	PlayVideo1(text, img, url, listitem)	
elif mode == 'ResolverSettings':
        urlresolver.display_settings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))