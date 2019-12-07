import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import re, string, sys, os
import urlresolver
from TheYid.common.addon import Addon
from TheYid.common.net import Net
from htmlentitydefs import name2codepoint as n2cp
import HTMLParser

addon_id = 'plugin.video.allinone'
plugin = xbmcaddon.Addon(id=addon_id)
net = Net()
addon = Addon('plugin.video.allinone', sys.argv)
DB = os.path.join(xbmc.translatePath("special://database"), 'allinone.db')
BASE_URL86 = 'http://free-on-line.net/'
BASE_URL2 = 'http://tvdl.xyz/'
BASE_URL1 = 'http://awesomedl.ru/'
BASE_URL3 = 'http://moviz4u.in/'
BASE_URL4 = 'http://tvshows-hdtv.org/'
BASE_URL12 = 'http://www.allcinemamovies.com/'
BASE_URL14 = 'http://rlsseries.com/'
BASE_URL20 = 'http://world4ufree.cc'
#BASE_URL21 = 'http://movies2k.eu/'
BASE_URL21 = 'http://onlinemoviegazes.com/'
BASE_URL22 = 'http://themovie4u.co/'
BASE_URL23 = 'http://300mbmovies4u.com/'
BASE_URL25 = 'http://www.rapgrid.com/'
BASE_URL30 = 'http://www.allcinemamovies.com/'#12#
BASE_URL32 = 'http://www.tvhq.info/'
BASE_URL35 = 'https://raw.githubusercontent.com/TheYid/yidpics/master'
BASE_URL38 = 'http://www.kidsmovies.tv/'
BASE_URL39 = 'http://www.onlinemoviesgold.in'
BASE_URL40 = 'http://www.uwatchfree.net/'
BASE_URL40a = 'http://www.uwatchfree.net/genres/'
BASE_URL42 = 'http://watchwrestling.to/'
BASE_URL43 = 'http://www.princessmovies.tv/'
BASE_URL44 = 'http://pullvideos.tv/'
BASE_URL45 = 'http://watchfullepisode.com/'
BASE_URL46 = 'http://www.mhighonline.com/'
BASE_URL47 = 'http://watchkidsmoviesonline.blogspot.co.uk/'
BASE_URL49 = 'http://www.moviefone.com/'
BASE_URL50 = 'http://movie900.com/'
BASE_URL52 = 'http://asdl.us/'
BASE_URL55 = 'http://documentarystorm.com/'
BASE_URL57 = 'http://latestdude.com'
BASE_URL60 = 'http://watchdtvonline.com/'
BASE_URL62 = 'http://www.tvguide.com/'
BASE_URL64 = 'http://m.liveonlinetv247.info/'
BASE_URL65 = 'http://rlseries.com/'
BASE_URL66 = 'http://watchitvideos.com/'
BASE_URL68 = 'http://tvonline.tw/'
BASE_URL69 = 'http://schoenheitsoperationen.biz'
BASE_URL70 = 'http://www.movies-300mb.com/'
BASE_URL71 = 'http://watchtvshow.org/'
BASE_URL73 = 'http://www.pogdesign.co.uk/'
BASE_URL74 = 'http://watchseries-onlines.ch/'
BASE_URL76 = 'http://oneclickwatch.ws/'
BASE_URL81 = 'http://livematch.org.uk/'
BASE_URL83 = 'http://www.watchfreetvlinks.com/'
BASE_URL84 = 'http://superseriale.com/'
BASE_URL85 = 'http://www.watchfreetvlinks.com/'
BASE_URL87 = 'http://www.bluraymovieswatchonline.com/'
BASE_URL88 = 'http://onlineseries.ucoz.com/'
BASE_URL89 = 'http://upbuzz.net'
BASE_URL90 = 'http://moviewatcher.to/'
BASE_URL91 = 'http://www.freemoviesu.to'

#### PATHS ##########
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/"
FanartPath = AddonPath + "/icons/"

##### Queries ##########
mode = addon.queries['mode']
url = addon.queries.get('url', None)
content = addon.queries.get('content', None)
query = addon.queries.get('query', None)
startPage = addon.queries.get('startPage', None)
numOfPages = addon.queries.get('numOfPages', None)
listitem = addon.queries.get('listitem', None)
urlList = addon.queries.get('urlList', None)
section = addon.queries.get('section', None)
text = addon.queries.get('text', None)
urlurl = addon.queries.get('urlurl', None)
img = addon.queries.get('img', None)

##################################### GetTitles ################################ GetTitles ############################################### GetTitles ######################################
#------------------------------------------------------------------------------- freemoviesu ------------------------------------------------------------------------------#

def GetTitles91(section, url, startPage= '1', numOfPages= '1'):
    try:
        print 'buzz get Movie Titles Menu %s' % url
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content
                match = re.compile('<li class="post box row fixed-hight">\s*?<div class="thumbnail">\s*?<a href="(.+?)" class="zoom" rel="bookmark" title="(.+?)">\s*?<img alt=".+?" src="(.+?)"/>', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles91', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- moviewatcher ------------------------------------------------------------------------------#

def GetTitles90(section, url, startPage= '1', numOfPages= '1'):
    try:
        print 'buzz get Movie Titles Menu %s' % url
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content
                match = re.compile('<div class="video_item">\s*?<a href="(.+?)" class="video_inner">\s*?<span class="rait_nfo" data-toggle="tooltip" title="IMDb rating" data-placement="bottom" data-container="body">\s*?.+?</span>\s*?<div class="img_holder">\s*?<img src="(.+?)" width="160" height="225" alt="(.+?)">', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': 'http://moviewatcher.to/' + movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles90', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- buzz ------------------------------------------------------------------------------#

def GetTitles89(section, url, startPage= '1', numOfPages= '1'):
    try:
        print 'buzz get Movie Titles Menu %s' % url
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content
                match = re.compile('<h2 class="title"><a href="(.+?)" title="Permalink.+?">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles89', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- bluraymovieswatchonline ------------------------------------------------------------------------------#

def GetTitles87(section, url):  
    try:
        pageUrl = url
        print pageUrl
        html = net.http_GET(pageUrl).content
        match = re.compile("<h2 class='article_heading'>\s*?<a href='(.+?)' rel='bookmark' title='(.+?)free.+?'>.+?</a></h2>\s*?<div class='post_meta'>", re.DOTALL).findall(html)
        match1 = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link' title='Older Posts'>Older Posts</a>", re.DOTALL).findall(html)
        for movieUrl, name in match:
                addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= 'http://icons.iconarchive.com/icons/iconleak/atrous/256/movie-icon.png', fanart=FanartPath + 'fanart.png')
        for movieUrl in match1:
                addon.add_directory({'mode': 'GetTitles87', 'section': section, 'url': movieUrl}, {'title':  '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')  
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#------------------------------------------------------------------------------- onlineseries ------------------------------------------------------------------------------#

def GetTitles88(section, url):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a class="threadLink" href="(.+?)">(.+?)</a>', re.DOTALL).findall(html)
        match1 = re.compile('<a class="switchNext" href="(.+?)" title="Next">.+?</a></td>', re.DOTALL).findall(html)
        for movieUrl, name in match:
                addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= 'http://icons.iconarchive.com/icons/designbolts/free-multimedia/1024/Film-icon.png', fanart=FanartPath + 'fanart.png') 
        for movieUrl in match1:
                addon.add_directory({'mode': 'GetTitles88', 'section': section, 'url': movieUrl}, {'title':  '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')   

    except:

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#------------------------------------------------------------------------------- tvm ------------------------------------------------------------------------------#

def GetTitles85(section, url, startPage= '1', numOfPages= '1'):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("<h3 class='post-title entry-title' itemprop='name'>\s*?<a href='(.+?)'>(.+?)</a>.+? src='(.+?)'", re.DOTALL).findall(html)
        match1 = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link' title='Older Posts'>Older Posts</a>", re.DOTALL).findall(html)
        for movieUrl, name, img in match:
                addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
        for movieUrl in match1:
                addon.add_directory({'mode': 'GetTitles85', 'section': section, 'url': movieUrl}, {'title':  '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')   

    except:

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#------------------------------------------------------------------------------- superseriale ------------------------------------------------------------------------------#

def GetTitles84(section, url, startPage= '1', numOfPages= '1'): #
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content
                match = re.compile('<h1 class="entry-title">\s*?<a href="(.+?)" title=".+?">(.+?)</a>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        addon.add_directory({'mode': 'GetLinks1', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= 'http://simpleicon.com/wp-content/uploads/film-3.png', fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles84', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- tvmuseum ------------------------------------------------------------------------------#

def GetTitles83(section, url, startPage= '1', numOfPages= '1'): #tv
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<header class="entry-header">\s*?<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('.', ' ')}, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles83', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")

def GetTitles83a(section, url, startPage= '1', numOfPages= '1'): #movie
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<h1 class="entry-title"><a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a></h1>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('.', ' ')}, img= 'http://www.thecreativefoundry.com.au/wp-content/uploads/2014/02/Film-Icon.png', fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles83a', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")


#------------------------------------------------------------------------------- themovie4u ------------------------------------------------------------------------------#

def GetTitles22(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<li class="border-radius-5 box-shadow">\s*?<img src="(.+?)" alt=".+?" title="(.+?)" />\s*?<a href="(.+?)" title=".+?">.+?</a>', re.DOTALL).findall(html)
                for img, name, movieUrl in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles22', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")

#------------------------------------------------------------------------------- tvdl ------------------------------------------------------------------------------#

def GetTitles2(section, url, startPage= '1', numOfPages= '1'):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<h2 class="post-box-title"> <a href="(.+?)">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        match1 = re.compile('<link rel="next" href="(.+?)"', re.DOTALL).findall(html)
        for movieUrl, name, img in match:
                addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
        for movieUrl in match1:
                addon.add_directory({'mode': 'GetTitles2', 'section': section, 'url': movieUrl}, {'title':  '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')   

    except:

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- watchonlinefreeseries ------------------------------------------------------------------------------#

def GetTitles71(section, url, startPage= '1', numOfPages= '1'):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<h2 class="title"><a href="(.+?)" title=".+?">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        match1 = re.compile("<link rel='next' href='(.+?)' />", re.DOTALL).findall(html)
        for movieUrl, name, img in match:
                addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
        for movieUrl in match1:
                addon.add_directory({'mode': 'GetTitles71', 'section': section, 'url': movieUrl}, {'title':  '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')   

    except:

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#------------------------------------------------------------------------------- movies-300mb ------------------------------------------------------------------------------#

def GetTitles70(section, url, startPage= '1', numOfPages= '1'):
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
                match = re.compile('<div class="entry-thumb">\s*?<a href="(.+?)" title="(.+?)"><img width="240" height="344" src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles70', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#------------------------------------------------------------------------------- schoenheitsoperationen ------------------------------------------------------------------------------#

def GetTitles69(section, url, startPage= '1', numOfPages= '1'):
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
                match = re.compile('<h1 class="entry-title">\s*?<a href="(.+?)" rel="bookmark">(.+?)</a>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks5', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles69', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#------------------------------------------------------------------------------- watchitvideos ------------------------------------------------------------------------------#

def GetTitles66(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('class="post-thumbnail"> <a\s*?href="(.+?)" rel="bookmark"> <img\s*?width="310" height="165" src="(.+?)" class="attachment-tie-medium size-tie-medium wp-post-image" alt="(.+?)" />', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks66', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles66', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks66(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('rel="nofollow" target="_blank" href="(.+?)">').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles66a(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('class="item-list"><h2 class="post-box-title"> <a\s*?href="(.+?)">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks66', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles66a', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#.replace('//', 'http://')#\s*?#
#------------------------------------------------------------------------------- ADL -----------------------------------------------------------------------------------------#

def GetTitles1(section, url, startPage= '1', numOfPages= '1'): 
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/?paged=' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/?paged=' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                      
                match = re.compile('<h2 class="title"><a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a></h2>\s*?<div class="postmeta-primary">\s*?<span class="meta_date">.+?</span> <span class="meta_categories">.+?<a href=".+?" rel="tag">.+?</a></span>\s*?</div>\s*?<img width="280" src="(.+?)" class="alignleft" alt="" />', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles1', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')      
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- moviz4u ------------------------------------------------------------------------------#

def GetTitles3(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<h2 class="post-box-title"><a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles3', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------- episodes-tv ---------------------------------------------------------------------------------#

def GetTitles41(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<div class="movieposter" title="Watch Video (.+?)" >\s*?<a href="(.+?)"><img class="bannersIMG" src="(.+?)" alt=".+?" title=".+?" /></a>', re.DOTALL).findall(html)
                for name, movieUrl, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search12&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks18', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= 'http://episodes-tv.com' + img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles41', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------- pullvideos ---------------------------------------------------------------------------------#

def GetTitles44(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<h3><li><a href="(.+?)" rel="bookmark">(.+?)</a></li></h3>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= 'http://pullvideos.tv/wp-content/uploads/2014/10/logo104x100.png', fanart=FanartPath + 'fanart.png')        
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------- world4ufree -----------------------------------------------------------------------------------------#

def GetTitles20(section, url, startPage= '1', numOfPages= '1'): 
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                    
                match = re.compile('class="cover"><a href="http://world4ufree.cc/(.+?)" title="(.+?)"><img src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': 'http://world4ufree.cc/' + movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles20', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('tvshows', 'tvshows-view')        
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- movies2k.eu ------------------------------------------------------------------------------------------#

def GetTitles21(section, url, startPage= '1', numOfPages= '1'): 
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content
                match = re.compile('<a href="(http://onlinemoviegazes.com/20\S+/)" rel="bookmark"><img width="\d+" height="\d+" src="(http://\S+)" class="[A-Za-z0-9 \-]+" alt="(\S+)" /></a>', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        cm  = []
                        #print 'Name: '+name+'   URL: '+movieUrl+'   Thumb:'+img+'\n\n'
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks21B', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles21', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('tvshows', 'tvshows-view')  
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def GetLinks21B(section, url):
    try: 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<p><iframe src="(.+?)&amp;width=\d+&amp;height=\d+" width="\d+" height="\d+" frameborder="\d+?" scrolling="\w+" allowfullscreen="\w+"></iframe></p>').findall(content)
        match1 = re.compile('href="(http://uptobox.com/.+?)"').findall(content)
        match2 = re.compile('<IFRAME SRC="(.+?)"').findall(content)
        match3 = re.compile('<a href="(http://.+)" target="_blank">.+</a><[br|/p]').findall(content)
        listitem = GetMediaInfo(content)
        for url in match1:
                addon.add_directory({'mode': 'GetLinks99', 'url':  url, 'listitem': listitem}, {'title':  'UpToStream : direct link'}, img= 'https://uptostream.com/images/logo.png', fanart=FanartPath + 'fanart.png')
        for url in match + match3:
                host = GetDomain(url)
                print 'We got: '+url+'    with: '+host
                if host=='watchvideo.us':
                        print 'We have a WatchVid host. URL is: '+url+'  host is: '+host
                        #addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
				
                if urlresolver.HostedMediaFile(url= url):
                        url = url.replace('https://openload.co/embed/', 'https://openload.co/f/')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

		
		
		
		#---------------------------------------------------------------------- 300mbmovies4u ------------------------------------------------------------------------------------------#

def GetTitles23(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content
                match = re.compile('<li>\s*?<h2><a href="(.+?)" title="(.+?)">.+?</a></h2>\s*?<div class="cover"><a href=".+?" title=".+?"><img src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles23', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'tvshows-view') 
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#------------------------------------------------------------------ TVHQ Categories movies -----------------------------------------------------------------------------------------------------#

def GetTitles32(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/' + startPage + ''
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/' + startPage + ''
                        html = net.http_GET(pageUrl).content                   
                match = re.compile('<figure class=".+?">\s*?<a href="(.+?)">\s*?<img class=".+?" src="(.+?)" alt="(.+?)">', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles32', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------- hqtv tv --------------------------------------------------------------------------------------------#

def GetTitles32a(section, url, startPage= '1', numOfPages= '1'): #2nd
        pageUrl = url
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<a class="list-group-item" href="(.+?)" title="(.+?)">.+?</a>',re.DOTALL).findall(html)
        for movieUrl, name in match:
                addon.add_directory({'mode': 'GetLinks1', 'section': section, 'url': movieUrl}, {'title':  name.strip()},img= 'http://tvhq.info/tvhqMAINLogo1.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def GetTitles32b(section, url, startPage= '1', numOfPages= '1'): #1st
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/' + startPage + ''
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/' + startPage + ''
                        html = net.http_GET(pageUrl).content
                match = re.compile('<figure class=".+?">\s*?<a href="(.+?)">\s*?<img class=".+?" src="(.+?)" alt="(.+?)">', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        addon.add_directory({'mode': 'GetTitles32a', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles32b', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')  
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- github iptv -------------------------------------------------------------------------------------#

def GetTitles35a(url):                                           
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<>title="(.+?)" href="(.+?)" />< src="(.+?)"').findall(content)
        for name, url, img in match:
                addon.add_directory({'mode': 'PlayVideo5', 'url': url, 'listitem': listitem}, {'title':  name.strip()}, img=img, fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------------- github help -----------------------------------------------------------------------------------#

def GetTitles37(url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<>title="(.+?)" href="(.+?)" />< src="(.+?)"').findall(content)
        for name, url, img in match:
                addon.add_directory({'mode': 'PlayVideo4', 'url': url, 'listitem': listitem}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo4(url, listitem):
    try:
        print 'in PlayVideo %s' % url
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^^^ Press back ^^^[/B] [/COLOR]'},'','')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Link may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")

#---------------------------------------------------------------------------------- watchwrestling -----------------------------------------------------------------------------------#

def GetTitles42(section, url, startPage= '1', numOfPages= '1'):
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
                match = re.compile('<a class="clip-link" data-id=".+?" title="Watch (.+?)" href="(.+?)">\s*?<span class="clip">\s*?<img src="(.+?)" alt=".+?"', re.DOTALL).findall(html)
                for name, movieUrl, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip().replace('/', ' '))
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks13', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img.replace('//', 'http://'), fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles42', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- uwatchfree category -----------------------------------------------------------------------------------#

def Categoriesuwf(url):
        url = BASE_URL40a + '/category/'
        html = net.http_GET(BASE_URL40a).content
        match = re.compile('<li><a href="http://www.uwatchfree.net/category/(.+?)/">(.+?)</a></li>').findall(html)
        #match = re.compile('<li class="cat-item cat-item-.+?"><a href="http://www.uwatchfree.net/category/(.+?)/" >(.+?)</a>').findall(html)
        for cat, title in match:
                addon.add_directory({'mode': 'GetTitles40', 'url': 'http://www.uwatchfree.net/category/' + cat + '/', 'startPage': '1', 'numOfPages': '1'}, {'title':  title }, img=IconPath + 'uw3.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles40(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<h2 class="entry-title"><a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a></h2>\s*?</header>.+?\s*?<figure class="visual-thumbnail"><a href=".+?"><img src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles40', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------------- movie900 -----------------------------------------------------------------------------------#

def GetTitles50(section, url, startPage= '1', numOfPages= '1'):
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
                match = re.compile('<span class="clip">\s*?<img src="(.+?)" alt=".+?" /><span class="vertical-align"></span>\s*?</span>\s*?<span class="overlay"></span>\s*?</a>\s*?</div>\s*?<div class="data">\s*?<h2 class="entry-title"><a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
                for img, movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip().replace('/', ' '))
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles50', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- asdl.us ------------------------------------------------------------------------------#

def GetTitles52(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<div class="moviefilm">\s*?<a href="(.+?)">\s*?<img src="(.+?)" alt="(.+?)" height="150px" width="115px" />', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= 'http://asdl.us/' + img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles52', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#------------------------------------------------------------------------------- onlinemoviesgold OMG------------------------------------------------------------------------------#

def GetTitles39(section, url, startPage= '1', numOfPages= '1'):
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
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                      
                match = re.compile('<img width="165" height="220" src="(.+?)" class="attachment-thumb_site wp-post-image" alt=".+?" title="(.+?) Online.+?" />\s*?<a href="(.+?)" title=".+?"><span>.+?</span></a>', re.DOTALL).findall(html)
                for img, name, movieUrl in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
                        cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks130', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles39', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:

        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- documentarystorm ------------------------------------------------------------------------------#

def GetTitles55(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content 
                match = re.compile('<div class="item">\s*?<a href="(.+?)" .+?=".+?" .+?=".+?" .+?=".+?" .+?=".+?" .+?="<h1>(.+?)</h1>">\s*?<div .+?=".+?">\s*?<img src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks55', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles55', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'tvshows-view') 
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks55(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('src="(http://embed.snagfilms.com/embed/.+?)"').findall(content)
        match1 = re.compile("src='(http://embed.snagfilms.com/embed/.+?)'").findall(content)
        match2 = re.compile('src="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1:
                addon.add_directory({'mode': 'GetLinks55a', 'url': url, 'listitem': listitem}, {'title':  'Load Stream >>'}, img= 'https://pbs.twimg.com/profile_images/476849424732131328/A2a1Z8Qc.jpeg', fanart=FanartPath + 'fanart.png')
        for url in match2 :
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks55a(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('file: "(.+?)",\s*?label: "(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo1', 'url': url, 'listitem': listitem}, {'title': 'play stream' + ' - ' + name}, img= 'https://pbs.twimg.com/profile_images/476849424732131328/A2a1Z8Qc.jpeg', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


#------------------------------------------------------------------------------- latestdude ------------------------------------------------------------------------------#

def GetTitles57(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page' + startPage
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page' + str(page)
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<div class="item">\s*?<a href="(.+?)">\s*?<div class="image">\s*?<img src="(.+?)" alt="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        addon.add_directory({'mode': 'GetLinks22', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles57', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')    
        setView('tvshows', 'tvshows-view') 
    except:

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- watchdtvonline ------------------------------------------------------------------------------#

def GetTitles60(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('class="entry-header"><h2><a href="(.+?)" title="(.+?)" >.+?</a></h2><div class="entry-meta">.+?<a href=".+?" rel=".+?">.+?</a>.+?<a href=".+?">.+?</a></div></div></div><div class="entry-content"><p><p><img class=" aligncenter" src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allinone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles60', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- live tv ------------------------------------------------------------------------------#

def GetTitles64(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<li><a target="_top" href="(.+?)">(.+?)</a></li>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        addon.add_directory({'mode': 'PlayVideo1', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= '', fanart=FanartPath + 'fanart.png')    
                #addon.add_directory({'mode': 'GetTitles64', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles64a(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<li><a href="(.+?)">(.+?)</a></li>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= '', fanart=FanartPath + 'fanart.png')    
                #addon.add_directory({'mode': 'GetTitles64', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################### index ################################ index ############################################### index ############################################
#---------------------------------------------------------------------------- TV Calendar index ----------------------------------------------------------------------------------------------------#

def GetTitles143(section, url):
    try:
        pageUrl = url
        html = net.http_GET(pageUrl).content
        match = re.compile('<strong><a href="./day/(.+?)" title="(.+?)">', re.DOTALL).findall(html)
        match1 = re.compile('<div class="month_name"><div class="prev-month"><a href="/cat/(.+?)"><span>.+?</span> <strong>(.+?)</strong></a></div> <h1><a href=".+?">.+?</a></h1> <div class=".+?"><a href=".+?"><span>.+?</span> <strong>.+?</strong></a></div></div><div id="loginbox"', re.DOTALL).findall(html)
        match2 = re.compile('<div class="next-month"><a href="/cat/(.+?)"><span>.+?</span> <strong>(.+?)</strong></a></div></div>\s*?<div class="box728 atop">', re.DOTALL).findall(html)
        for movieUrl, name in match1:
                addon.add_directory({'mode': 'GetTitles143', 'section': section, 'url': 'http://www.pogdesign.co.uk/cat/' + movieUrl }, {'title': '<< ' + name}, img= 'https://www.globalbrigades.org/media_gallery/thumb/320/0/VRS_Calendar2_512x512x32_2.png',  fanart=FanartPath + 'fanart.png') 
        for movieUrl, name in match:
                addon.add_directory({'mode': 'GetTitles143a', 'section': section, 'url': 'http://www.pogdesign.co.uk/cat/day/' + movieUrl }, {'title': '[B]' + name.replace('Thursday 1st October 2015', 'Choose a day') + '[/B]'}, img= 'https://www.globalbrigades.org/media_gallery/thumb/320/0/VRS_Calendar2_512x512x32_2.png',  fanart=FanartPath + 'fanart.png') 
        for movieUrl, name in match2:
                addon.add_directory({'mode': 'GetTitles143', 'section': section, 'url': 'http://www.pogdesign.co.uk/cat/' + movieUrl }, {'title': name + ' >>'}, img= 'https://www.globalbrigades.org/media_gallery/thumb/320/0/VRS_Calendar2_512x512x32_2.png',  fanart=FanartPath + 'fanart.png') 
        setView('tvshows', 'calendar-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles143a(query, section): 
    try:
        pageUrl = url
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<div class="contbox ovbox" style=" background-image: url(.+?);">\s*?<h4><a href=".+?">(.+?)<span>.+?</span></a></h4>\s*?<h5><a href=".+?">(.+?)<span>(.+?)/span></a></h5>\s*?<div class=".+?">(.+?)<a href=".+?">.+?</a></div> \s*?<ul class=".+?">\s*?<li><strong>.+?</strong>(.+?)</li>',re.DOTALL).findall(html)
        for img, name1, query1, name, sum, time in match:
                img = 'http://www.pogdesign.co.uk/' + img.replace('(', '').replace(')', '')
                query = name1.replace('[', '').replace(']', '') + name.replace("'", "").replace(' 1,', '01').replace(' 2,', '02').replace(' 3,', '03').replace(' 4,', '04').replace(' 5,', '05').replace(' 6,', '06').replace(' 7,', '07').replace(' 8,', '08').replace(' 9,', '09').replace(' 1<', '01').replace(' 2<', '02').replace(' 3<', '03').replace(' 4<', '04').replace(' 5<', '05').replace(' 6<', '06').replace(' 7<', '07').replace(' 8<', '08').replace(' 9<', '09').replace('Season', 's').replace('Episode', 'e').replace(',', '').replace('<', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
                title = '[COLOR blue][B]' + name1 +'[/B][/COLOR]' + ' - ' + '[COLOR lime]' + query1 + '[/COLOR]' + ' - ' + '[COLOR pink][I]' + name.replace('<', ' ') + '[/I][/COLOR]' + ' - ' + '[COLOR khaki]' + sum + '[/COLOR]' + ' - ' + time
                query = query.replace('This Is England ', 'this is england 90 ')
                query = query.replace('Doctor Who ', 'Doctor Who 2005 ')
                query = query.replace('The Late Late Show Corden ', 'James Corden 2015')
                query = query.replace('Blood and Oil ', 'blood and oil 2015')
                query = query.replace('Public Morals ', 'public morals 2015')
                query = query.replace('The Voice (US) ', 'the voice')
                query = query.replace('Empire ', 'empire 2015')
                query = query.replace('&', 'and')
                query = query.replace("You're the Worst ", 'youre the worst')
                query = query.replace("DC's Legends of Tomorrow", 'DCs Legends of Tomorrow')
                addon.add_directory({'mode': 'Search12', 'section': section, 'query': query}, {'title': title}, img= img,  fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------- watchseries-onlines a/z index ----------------------------------------------------------------------------------------------------#

def GetTitles144(section, query):
    try:
        pageUrl = url
        html = net.http_GET(pageUrl).content
        match = re.compile('<option class="level-0" value=".+?">(.+?)</option>', re.DOTALL).findall(html)
        for movieUrl in match:
                addon.add_directory({'mode': 'Search12', 'section': section, 'query': movieUrl}, {'title': movieUrl}, img= 'https://briantudor.files.wordpress.com/2010/12/tv-icon1.png', fanart=FanartPath + 'fanart.png') 
        setView('tvshows', 'calendar-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#---------------------------------------------------------------------------- moviefone movie index ---------------------------------------------------------------------------------#

def GetTitles49(query):
    try:
        pageUrl = url
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<img name="replace-image" rel=".+?" id=".+?" class=".+?" src=".+?" data-src="(.+?)" alt="(.+?)"/>',re.DOTALL).findall(html)
        for img, query in match:
                addon.add_directory({'mode': 'Search11', 'query': query}, {'title':  query}, img= img, fanart=FanartPath + 'fanart3.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles49a(query):
    try:
        pageUrl = url
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<img name="replace-image" rel=".+?" id="movie-poster.+?" class="movie-poster" src=".+?" data-src="(.+?)" alt="">\s*?</div>\s*?<div class="hover-cover">\s*?<div class="wrapper details">\s*?<h3>(.+?)</h3>',re.DOTALL).findall(html)
        for img, query in match:
                addon.add_directory({'mode': 'Search11', 'query': query}, {'title':  query}, img= img, fanart=FanartPath + 'fanart3.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------------- TvHQ TV index -----------------------------------------------------------------------------------#

def GetTitles2a(query):
    try:
        pageUrl = url
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<img class="img-responsive hoverZoomLink" src="(.+?)" alt="(.+?)">',re.DOTALL).findall(html)
        for img, query in match:
                addon.add_directory({'mode': 'Search12', 'query': query.replace('-', ' ').replace('[', ' ').replace(']', ' ') + ' s'}, {'title':  query.replace('-', ' ').replace('[', ' ').replace(']', ' ')}, img= img, fanart=FanartPath + 'fanart4.png')
        setView('tvshows', 'tvshows-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------------- allcinemamovies index TV -----------------------------------------------------------------------------------#

def GetTitles2b(query):
    try:
        pageUrl = url
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<img class="img-preview spec-border show-thumbnail"  src=".+?src=(.+?)&amp;w=130&amp;h=190&amp;zc=1" alt="Watch (.+?)Online" />',re.DOTALL).findall(html)
        for img, query in match:
                addon.add_directory({'mode': 'Search12', 'query': query.replace('-', ' ').replace('[', ' ').replace(']', ' ') + ' s'}, {'title':  query.replace('-', ' ').replace('[', ' ').replace(']', ' ')}, img= img, fanart=FanartPath + 'fanart4.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

##.replace('/', ' ')## \s*? ##

#----------------------------------------------------------------------------- episodes-tv index ---------------------------------------------------------------------------------#

def GetTitles41a(query, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<div class="moviefilm">\s*?<a href=".+?">\s*?<img src="(.+?)" alt="(.+?)" height="150px" width="115px" />', re.DOTALL).findall(html)
                for img, query in match:
                        img = img.replace('http://asdl.us/', '')
                        addon.add_directory({'mode': 'Search12', 'section': section, 'query': query.replace('[720p]', '').replace('(', '').replace(')', '').replace("'", "")}, {'title':  query}, img= 'http://asdl.us/' + img, fanart=FanartPath + 'fanart4.png')
                addon.add_directory({'mode': 'GetTitles41a', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart4.png') 
        setView('tvshows', 'tvshows-view')       
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site mite be down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------- tvguide index ---------------------------------------------------------------------------------#

def GetTitles62(query):
    try:
        pageUrl = url
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<span class="show-card show-card-small">\s*?<img src="(.+?)" class=".+?" alt=".+?" title="(.+?)" srcset=".+?" width=".+?" height=".+?" />',re.DOTALL).findall(html)
        for img, query in match:
                addon.add_directory({'mode': 'Search12', 'query': query}, {'title':  query}, img= img.replace('100x133.png', '1000x339.png').replace('100x133.jpg', '1000x339.jpg'), fanart=FanartPath + 'fanart4.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles62a(query):
    try:
        pageUrl = url
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<span class="show-card show-card-small">\s*?<img src="(.+?)" class=".+?" alt=".+?" title="(.+?)" srcset=".+?" width=".+?" height=".+?" />',re.DOTALL).findall(html)
        for img, query in match:
                addon.add_directory({'mode': 'Search11', 'query': query}, {'title':  query}, img= img.replace('100x133.png', '1000x339.png').replace('100x133.jpg', '1000x339.jpg'), fanart=FanartPath + 'fanart4.png')
        setView('tvshows', 'tvshows-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------tvshows-hdtv----------------------------------------------------------------------------------------------#
 
def GetLinks17(section, url):
    try: 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<b>(.+?)</b></center>.<br></span></td></tr><tr> \s*?<tr><td><center><a href="(http://hugefiles.net/.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for name, url in match:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url , 'listitem': listitem}, {'title': name.strip().replace('.', ' ')  + ' =  ' + host }, img= 'http://www.anbient.net/sites/all/imagens/servers/hugefiles.png' , fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################### Getlinks ################################ Getlinks ############################################### Getlinks ######################################

#--------------------------------------------------------- ocw - wtt - binf - 300mbmovies4u - movies2k.eu --------------------------------------------------------------------------------#
def GetLinks(section, url):
    try: 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="(.+?)"').findall(content)
        match1 = re.compile('href="(http://uptobox.com/.+?)"').findall(content)
        match2 = re.compile('<IFRAME SRC="(.+?)"').findall(content)
        match3 = re.compile('<iframe src="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match1:
                addon.add_directory({'mode': 'GetLinks99', 'url':  url, 'listitem': listitem}, {'title':  'UpToStream : direct link'}, img= 'https://uptostream.com/images/logo.png', fanart=FanartPath + 'fanart.png')
        for url in match + match2:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        url = url.replace('https://openload.co/embed/', 'https://openload.co/f/')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks99(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('Streaming link: <a href="(.+?)" class="blue_link">.+?</a>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                addon.add_directory({'mode': 'GetLinks99a', 'url': url, 'listitem': listitem}, {'title':  'load stream' + ' : ' + url}, img= 'https://uptostream.com/images/logo.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks99a(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("<source src='(.+?)' type='.+?' data-res='(.+?)'").findall(content)
        listitem = GetMediaInfo(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo1', 'url': url, 'listitem': listitem}, {'title': name }, img= 'https://uptostream.com/images/logo.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks99b(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<p style="text-align: center;"><a href=".+?http:/(.+?)">.+?</a></p>').findall(content)
        match1 = re.compile('http:/uptobox.com/(.+?)">Uptobox</a></p>').findall(content)
        match2 = re.compile('<p style="text-align: center;"><a href="http:/(.+?)">.+?</a></p>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match1:
                url = 'http://uptobox.com/' + url
                addon.add_directory({'mode': 'GetLinks99', 'url':  url, 'listitem': listitem}, {'title':  'UpToStream : direct link'}, img= 'https://uptostream.com/images/logo.png', fanart=FanartPath + 'fanart.png')
        for url in match + match2:
                url = 'http://' + url
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ primeflicks - hqtv ---------------------------------------------------------------------------------#

def GetLinks1(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('src="(.+?)"').findall(content)
        match2 = re.compile('href="(.+?)"').findall(content)
        match1 = re.compile('SRC="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1 + match2 :
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------- watchfullepisode --------------------------------------------------------------------------------------------#

def GetLinks1a(section, url): 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<td><a href="(.+?)">.+?</td>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ bluray ------------------------------------------------------------------------------------#

def GetLinks5(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" target="_blank">').findall(content)
        match1 = re.compile('<span style="color: black;">.+?</span> <a href="(.+?)" target="_blank">.+?</a></span></span></span><br />').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------------- mvl.eu --------------------------------------------------------------------------------------------#

def GetLinks7(section, url): 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<li><a href="(.+?)">.+?</a></li>').findall(content)
        match1 = re.compile('<li><a href="(.+?)">V-Vids</a></li>').findall(content)
        match2 = re.compile("Watch=window.+?'(.+?)'").findall(content)
        listitem = GetMediaInfo(content)
        for url in match1:
                addon.add_directory({'mode': 'GetLinks9', 'url': url, 'listitem': listitem}, {'title':  'V-vids.com'}, img=IconPath + 'vids.png', fanart=FanartPath + 'fanart.png')
        for url in match + match2:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('youtube.com','[COLOR lime]Movie Trailer[/COLOR]')
                        host = host.replace('youtu.be','[COLOR lime]Movie Trailer[/COLOR]')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks9(url):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<IFRAME SRC="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                addon.add_directory({'mode': 'GetLinks9a', 'url': url, 'listitem': listitem}, {'title':  'Get stream'}, img=IconPath + 'watch.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks9a(url):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match1 = re.compile('<a id="downloadbutton" onclick=".+?" href="(.+?)" title=".+?"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match1:
                addon.add_directory({'mode': 'PlayVideo1', 'url': url, 'listitem': listitem}, {'title':  'load stream'}, img=IconPath + 'watch.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- shows4u -------------------------------------------------------------------------------------------#

def GetLinks8(section, url):   
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<IFRAME SRC="(.+?)"').findall(content)
        match1 = re.compile('<iframe src="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1 :
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------------rlssource--------------------------------------------------------------------------------------#

def GetLinks10(section, url): 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href=(.+?) target=').findall(content)
        match1 = re.compile('<iframe src="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        title = title.replace('480p','[COLOR coral][B][I]480p[/B][/I][/COLOR]')
                        title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                        title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                        title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                        title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                        title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#--------------------------------------------------------------------------------moviezstream------------------------------------------------------------------------------------------------#

def GetLinks11(section, url): 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<td><a href="(.+?)">Sockshare</a></td>').findall(content)
        match1 = re.compile('<td><a href="(.+?)">Billion</a></td>').findall(content)
        match2 = re.compile('<td><a href="(.+?)">1fichier</a></td>').findall(content)
        match3 = re.compile('<td><a href="(.+?)">Uploaded</a></td>').findall(content)
        match4 = re.compile('<td><a href="(.+?)">FileCloud</a></td>').findall(content)
        match5 = re.compile('<td><a href="(.+?)">Up</a></td>').findall(content)
        match6 = re.compile('<td><a href="(.+?)">MU</a></td>').findall(content)
        match7 = re.compile('<td><a href="(.+?)">Turbo</a></td>').findall(content)
        match8 = re.compile('<td><a href="(.+?)">Putlocker</a></td>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1 + match2 + match3 + match4 + match5 + match6 + match7 + match8:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ watch wrestling2 ------------------------------------------------------------------------------------#

def GetLinks12(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<iframe frameborder=".+?" width=".+?" height=".+?" src="(.+?)"></iframe><br />').findall(content)
        match1 = re.compile('<iframe width=".+?" height=".+?" src="(.+?)" frameborder=".+?" allowfullscreen></iframe><br />').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ watch wrestling ------------------------------------------------------------------------------------#

def GetLinks13(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="(.+?)" target="_blank">(.+?)</a>').findall(content)
        #match1 = re.compile('href="(http://pwtalk.net/cgi-bin/protect.cgi.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        #for url in match1:
                #addon.add_directory({'mode': 'GetLinks12', 'url': url, 'listitem': listitem}, {'title':  url }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        for url, name in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' - ' + name }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


#---------------------------------------------------------------------- dlmovies ------------------------------------------------------------------------------------------#

def GetLinks14(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="http://dlmoviegames.com/download/(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ episodes-tv ---------------------------------------------------------------------------------#

def GetLinks18(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('name=".+?" href="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ bear-movies ---------------------------------------------------------------------------------#

def GetLinks18a(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('target="_blank">(.+?)</a><br />').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ fdl ---------------------------------------------------------------------------------#

def GetLinks19(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a target="_blank" href="(.+?)" class="play_link " id="">Play</a>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ 20 ---------------------------------------------------------------------------------#

def GetLinks20(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a target="_blank" rel="nofollow" href="(.+?)">Play</a>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ onlinehdmovies ---------------------------------------------------------------------------------#

def GetLinks21(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<div id=".+?"><IFRAME SRC="(.+?)" FRAMEBORDER=.+? MARGINWIDTH=.+? MARGINHEIGHT=.+? SCROLLING=.+? WIDTH=.+? HEIGHT=.+?></IFRAME></div>').findall(content)
        match1 = re.compile('<center><a href="(.+?)" target="_blank"><strong><span style=".+?">.+?</span></strong></a></center>').findall(content)
        match2 = re.compile('<center><a href="(https://openload.io.+?)" target="_blank"><strong><span style=".+?">.+?</span></strong></a></center>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        for url in match2:
                addon.add_directory({'mode': 'GetLinks21a', 'url':  url, 'listitem': listitem}, {'title':  'direct link - ' + url}, img= 'https://openload.io/assets/img/logo-alpha.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks21a(section, url):                                            
        print 'GETLINKS FROM URL: '+url
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match1 = re.compile('<span style="display:none;" id="realdownload"><a href="(.+?)" class=".+?"><strong>.+?</strong>.+?</a>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match1:
                addon.add_directory({'mode': 'PlayVideo1', 'url': url, 'listitem': listitem}, {'title':  'load stream'}, img=IconPath + 'watch.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ perfecthdmovies ---------------------------------------------------------------------------------#

def GetLinks22(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" target="_blank">').findall(content)
        match1 = re.compile('<a href="(http://uptobox.com/.+?)" target="_blank">').findall(content)
        listitem = GetMediaInfo(content)
        for url in match1:
                addon.add_directory({'mode': 'GetLinks99', 'url':  url, 'listitem': listitem}, {'title':  'UpToStream : direct link'}, img= 'https://uptostream.com/images/logo.png', fanart=FanartPath + 'fanart.png')
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ watchcartoononline ---------------------------------------------------------------------------------#

def GetLinks23(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<option value="(.+?)">(.+?)</option>').findall(content)
        listitem = GetMediaInfo(content)
        for url, name in match:
                addon.add_directory({'mode': 'PlayVideo1', 'url':  url, 'listitem': listitem}, {'title':  'direct link : ' + name}, img= 'http://watchcartoononline.eu/themes/default/img/icon/logo.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ moviz4u ---------------------------------------------------------------------------------#

def GetLinks129(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<form action="https?:\/\/www\.ezfilehost\.[a-z\.]{2,6}\/.+?" method="post".+?name="filename" type="hidden" value="(.+?)".*\s*?.*\s*?<input name="id" type="hidden" value="(.+?)"').findall(content)
        for movieLink, addr  in match:
                url = 'http://' + addr + '/HDMoviesPoint.com/' + movieLink
                print 'Found HDMP' + str(url)
                addon.add_directory({'mode': 'PlayVideo1', 'url': url, 'listitem': listitem}, {'title':  'HDMP: direct link'}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        match1 = re.compile('<p><a href="(http:\/\/.+?)">.+?b>([A-Z].+?) Link</b>.+?</p>').findall(content)
        listitem = GetMediaInfo(content)
        for url, locker in match1:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  locker }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ OMG ---------------------------------------------------------------------------------#

def GetLinks130(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<h2><strong><span style="font-size.+?"><a href="(.+?)" target="_blank" rel="nofollow">.+?<u>(PLAY MOVIE)</u>.+?</a></span></strong></h2>').findall(content)
        listitem = GetMediaInfo(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks130a', 'url': url, 'listitem': listitem}, {'title':  name}, img= 'http://www.onlinemoviesgold.com/wp-content/uploads/logo.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks130a(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('src="(.+?)"').findall(content)
        match1 = re.compile('SRC="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- desimovies ------------------------------------------------------------------------------#

def GetTitles81(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        pageUrl = 'http://inditvmov.asia/movees/donloadmovies.php'
        headprop = {'X-Requested-With': 'com.Milan.IPL2812', 'Referer':'http://www.inditvmov.asia/MovieeshhHome0708.php'};
        html = net.http_GET(pageUrl,headprop).content
        #html = net.http_GET(pageUrl).content
        content = html
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<li><a href="(http://.+?.[zee18info|inditvmov].asia/.+?|http://zee18.com/newapp/source/Movies/.+?)">(.+?)</a></li>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks81', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= '', fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles71', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks81(section, url):
	headprop = {'X-Requested-With': 'com.Milan.IPL2812', 'Referer':'http://inditvmov.asia/movees/donloadmovies.php'};
	html = net.http_GET(url,headprop).content
	listitem = GetMediaInfo(html)
	content = html
	match = re.compile('<a id="lbtnBrowser" class="button-error pure-button" href="httphost://.http-raw=(http://.+?).http-refferer=http://.+?">Single Link</a>').findall(content)
	match1 = re.compile('<a id="lbtnBrowser" class="button-error pure-button" href="(http://.+?)">Single Link</a>').findall(content)
	#match2 = re.compile('<a id="lbtnBrowser" class="button-secondary pure-button" href="(?!.+/65506d8589f72|.+/9debbf4ca3752|.+/5a7de6fd042e4|.+/20d320d73c73e)(http.+?)">(.+?)</a>').findall(content)	
	for url in match:
			linkpage = net.http_GET(url).content
			match2 = re.compile('sources: \[{file:"(http://.+?\.m3u8)"},{file:"(http://.+?\.mp4)",label:".+"}\]').findall(linkpage)
			for dl1, dl2 in match2:
				addon.add_directory({'mode': 'PlayVideo2', 'url': dl2, 'listitem': listitem}, {'title':  'Direct 1'}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
				addon.add_directory({'mode': 'PlayVideo2', 'url': dl1, 'listitem': listitem}, {'title':  'Direct 2'}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')   			
	#match1 = re.compile('<a id="lbtnBrowser" class="button-secondary pure-button" href="(?!.+/65506d8589f72|.+/9debbf4ca3752|.+/5a7de6fd042e4|.+/20d320d73c73e)(http.+?)">(.+?)</a>').findall(content)
	listitem = GetMediaInfo(content)
	for url in match1:
			addon.add_directory({'mode': 'PlayVideo2', 'url': url, 'listitem': listitem}, {'title':  'Direct 3'}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

	#------------------------------------------------------------------------------- desimovies 2------------------------------------------------------------------------------#

def GetTitles811(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + 'page/' + startPage + '/'
        print pageUrl
        headprop = {'X-Requested-With': 'com.Milan.IPL2812', 'Referer':'http://www.inditvmov.asia/MovieeshhHome0708.php'};
        html = net.http_GET(pageUrl,headprop).content
        #html = net.http_GET(pageUrl).content
        content = html
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + 'page/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                       
                match = re.compile('<a href="(http://.+?php)"><div class="\S+"><table><tr><td><img src="(http://.+?)" /></td><td>([\S -]+ \(\d+\)[\S -]+?)</td></tr></table></div></a>').findall(html)
                for movieUrl, img, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.allone/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR green]Search[/COLOR]', runstring))
                        addon.add_directory({'mode': 'GetLinks811', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img=img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles811', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks811(section, url):
	headprop = {'X-Requested-With': 'com.Milan.IPL2812', 'Referer':'http://inditvmov.asia/movees/donloadmovies.php'};
	html = net.http_GET(url,headprop).content
	listitem = GetMediaInfo(html)
	content = html
	match = re.compile('<a id="lbtnBrowser" class="button-secondary pure-button" href="httphost://.http-raw=(http://.+?).http-refferer=http://.+?">Single Link</a>').findall(content)
	match1 = re.compile('<a id="lbtnBrowser" class="button-secondary pure-button" href="(http://.+?[mkv|mp4|m3u8])">Single Link</a>').findall(content)
	#match2 = re.compile('<a id="lbtnBrowser" class="button-secondary pure-button" href="(?!.+/65506d8589f72|.+/9debbf4ca3752|.+/5a7de6fd042e4|.+/20d320d73c73e)(http.+?)">(.+?)</a>').findall(content)	
	for url in match:
			linkpage = net.http_GET(url).content
			match2 = re.compile('sources: \[{file:"(http://.+?\.m3u8)"},{file:"(http://.+?\.mp4)",label:".+"}\]').findall(linkpage)
			for dl1, dl2 in match2:
				addon.add_directory({'mode': 'PlayVideo2', 'url': dl2, 'listitem': listitem}, {'title':  'Direct 1'}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
				addon.add_directory({'mode': 'PlayVideo2', 'url': dl1, 'listitem': listitem}, {'title':  'Direct 2'}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')   			
	#match1 = re.compile('<a id="lbtnBrowser" class="button-secondary pure-button" href="(?!.+/65506d8589f72|.+/9debbf4ca3752|.+/5a7de6fd042e4|.+/20d320d73c73e)(http.+?)">(.+?)</a>').findall(content)
	listitem = GetMediaInfo(content)
	for url in match1:
			addon.add_directory({'mode': 'PlayVideo2', 'url': url, 'listitem': listitem}, {'title':  'Direct Link'}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#------------------------------------------------------------------------------ tvonline ---------------------------------------------------------------------------------#

def GetLinks131(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("'(.+?)'").findall(content)
        match1 = re.compile('<h1><a href="http://tvonline.tw/(.+?)">.+?</a>.+?<a href=".+?">.+?</a>.+?</h1>', re.DOTALL).findall(html)
        listitem = GetMediaInfo(content)
        for url in match1:
                addon.add_directory({'mode': 'GetTitles68a', 'url': 'http://tvonline.tw/' + url}, {'title':  '[COLOR lime]All Seasons[/COLOR] >> '},img= 'http://images.tvonline.tw/logo.gif', fanart=FanartPath + 'fanart.png') 
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ WM ---------------------------------------------------------------------------------#

def GetLinks132(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)"').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if 'Unknown' in host:
                                continue
                r = re.search('\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
                        continue
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------ rb ---------------------------------------------------------------------------------#

def GetLinks133(section, url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)"').findall(content)
        match2 = re.compile('<a href="http://sh.st/st/.+?/(.+?)">.+?</a><br />').findall(content)
        match1 = re.compile('<meta name="description" content="Download and (.+?)"/>').findall(content)
        match3 = re.compile('width=".+?" height=".+?" /></p>\s*?<p>(.+?)</p>').findall(content)
        listitem = GetMediaInfo(content)
        for name in match1:
                addon.add_directory({'listitem': listitem}, {'title': '[COLOR pink][B](' + name + ')[/B][/COLOR]' }, img= '', fanart=FanartPath + 'fanart.png')
        for name in match3:
                addon.add_directory({'listitem': listitem}, {'title': '[COLOR blue][B](' + name + ')[/B][/COLOR]' }, img= '', fanart=FanartPath + 'fanart.png')
        for url in match:
                host = GetDomain(url)
                if 'Unknown' in host:
                                continue
                r = re.search('\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
                        continue
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img= '', fanart=FanartPath + 'fanart.png')
        for url in match2:
                url = 'http://' + url
                host = GetDomain(url)
                if 'Unknown' in host:
                                continue
                r = re.search('\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
                        continue
                if urlresolver.HostedMediaFile(url= url):
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img= '', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

############################### PlayVideo ######################################## PlayVideo ############################################# PlayVideo ###########################

def PlayVideo(url, listitem):
    try:
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^ Press back ^[/B] [/COLOR]'},'','')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Link may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")

#-------livestreams------------#

def PlayVideo2(url, listitem):
    try:
	xbmc.Player().play(url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^ Press back ^[/B] [/COLOR]'},'','')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Stream may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")

#-------myvideolinks------------#

def PlayVideo1(url, listitem):
        addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(addon_handle, 'video')
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]PLAY STREAM[/B][/COLOR]  >> ', iconImage='https://lh5.googleusercontent.com/-p2h0tx7Trgs/Uzu-3kxzKuI/AAAAAAAAOsU/sVJKqxSMY-4/s319/watch2.jpg', thumbnailImage= 'http://s29.postimg.org/8z8jd5x5j/logo1.png')
        li.setProperty('fanart_image', 'http://littletechboy.com/downloads/sins/modding/LoadingSplash.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)

#-------m3u playlists------------#

def PlayVideo5(url, listitem):
        addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(addon_handle, 'video')
        li = xbmcgui.ListItem('[COLOR dodgerblue][B]LOAD STREAM PLAYLIST[/B][/COLOR]  >> ', iconImage='http://www.creation-spip.fr/IMG/arton37.png?1357155686', thumbnailImage= 'http://www.creation-spip.fr/IMG/arton37.png?1357155686')
        li.setProperty('fanart_image', 'http://littletechboy.com/downloads/sins/modding/LoadingSplash.jpg') 
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)

#--------------------------------------------------------------------------------------------------#

def GetDomain(url):
        tmp = re.compile('//(.+?)/').findall(url)
        domain = 'Unknown'
        if len(tmp) > 0 :
            domain = tmp[0].replace('www.', '')
        return domain

#--------------------------------------------------------------------------------------------------#

def GetMediaInfo(html):
        listitem = xbmcgui.ListItem()
        match = re.search('og:title" content="(.+?) \((.+?)\)', html)
        if match:
                print match.group(1) + ' : '  + match.group(2)
                listitem.setInfo('video', {'Title': match.group(1), 'Year': int(match.group(2)) } )
        return listitem

############################# menus ################################## menus ########################################################### menus ################################

def MainMenu():    #homescreen
        addon.add_directory({'mode': 'MovieMenu'}, {'title':  '[COLOR cornflowerblue][B]Movies >[/B][/COLOR] >'}, img=IconPath + 'films.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'TvMenu'}, {'title':  '[COLOR darkorange][B]Tv Shows >[/B][/COLOR] >'}, img=IconPath + 'tv2.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'SportMenu'}, {'title':  '[COLOR lemonchiffon][B]Sports >[/B][/COLOR] >'}, img=IconPath + 'sport1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'DocMenu'}, {'title':  '[COLOR peachpuff][B]Documentaries >[/B][/COLOR] >'}, img=IconPath + 'doc.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'LiveMenu'}, {'title':  '[COLOR peachpuff][COLOR mediumorchid][B]Streams >[/COLOR][/B] >'}, img=IconPath + 'stream.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'MusicMenu'}, {'title':  '[COLOR cadetblue][B]Music >[/B][/COLOR] >'}, img=IconPath + 'music.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'RadioMenu'}, {'title':  '[COLOR lightsteelblue][B]Radio >[/B][/COLOR]>'}, img=IconPath + 'radio.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'SearchMenu'}, {'title':  '[COLOR green][B]Searches >[/B] [/COLOR] >'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR red]Resolver Settings >[/COLOR] >'}, img=IconPath + 'resolver.png', fanart=FanartPath + 'fanart.png') 
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[B][COLOR yellow]www.entertainmentrepo.com  [/B][/COLOR]'}, img=IconPath + 'newart.jpg', fanart=FanartPath + 'newart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#--------------------------------MusicVideos-----------------------------MusicVideos-------------------------------------MusicVideos---------------------------MusicVideos-----------#

def MusicMenu():   #MusicVideos
        addon.add_directory({'mode': 'GetTitles25', 'section': 'ALL', 'url': BASE_URL25 + '/battles',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cadetblue][B]Rap Battle videos[/B][/COLOR] [COLOR springgreen](Rap Grid) [/COLOR]>>'}, img=IconPath + 'rg.png', fanart=FanartPath + 'fanart.png')

        addon_handle = int(sys.argv[1]) 
        xbmcplugin.setContent(addon_handle, 'audio')

        url = 'rtmp://live.drumandbasslines.com/DnBTV/ch1'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Drum and Bass tv[/B][/COLOR] >>  [COLOR lime](live)[/COLOR]', thumbnailImage= 'http://cdn.desktopwallpapers4.me/wallpapers/music/1366x768/1/6742-drum-and-bass-1366x768-music-wallpaper.jpg')
        li.setProperty('fanart_image', 'https://raw.githubusercontent.com/TheYid/My-Repo/master/plugin.video.allinone/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)


        xbmcplugin.endOfDirectory(addon_handle)

#----------------------------------radio----------------------------radio------------------------------radio-----------------------------radio------------------------------#

def RadioMenu():   #radio
        #setView('radio', 'radio-view')

        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  '[COLOR lime]~~~~~~~[/COLOR][COLOR yellow][B].....WE ARE.....[/B][/COLOR] [COLOR red][I][B](((LIVE)))[/B][/I][/COLOR] [COLOR yellow][B].....TheYids RADIO.....[/B][/COLOR][COLOR lime]~~~~~~~[/COLOR]'}, img=IconPath + 'radioty.png', fanart='http://geewall.com/mmc_uploads/6119-music-notes-wallpaper-37082.jpg')

        addon_handle = int(sys.argv[1])   # thanks to Android TV Boxes a member of xbmchub for this code thanks mate #
        xbmcplugin.setContent(addon_handle, 'audio')

        url = 'http://80.85.84.114:8118/;'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]MEATtransMISSION[/B][/COLOR] >>          [COLOR lime](Old skool, Groove, jazz funk, boogie, new music)[/COLOR]  [COLOR red]NEW[/COLOR]', iconImage='http://meatliquor.com/images/logo-meat-trans-mission-hover.png', thumbnailImage= 'http://meatliquor.com/images/logo-meat-trans-mission-hover.png')
        li.setProperty('fanart_image', 'http://mad-learn.com/wp-content/uploads/2015/07/music.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://sh.fl-us.audio-stream.com/tunein.php/freshrad.asx'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]FreshRadioUK[/B][/COLOR] >>          [COLOR lime](Electronic, Dance Music)[/COLOR]  [COLOR red]NEW[/COLOR]', iconImage='http://www.freshradiouk.com/wp/wp-content/uploads/2012/08/Logo.jpeg', thumbnailImage= 'http://www.freshradiouk.com/wp/wp-content/uploads/2012/08/Logo.jpeg')
        li.setProperty('fanart_image', 'http://mad-learn.com/wp-content/uploads/2015/07/music.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)


        url = 'http://stream.x1hosting.net:8016/stream?type=.mp3'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]viberadioonline.com[/B][/COLOR] >>          [COLOR lime](Old skool Groove, jazz funk, boogie & soulful house)[/COLOR] ', iconImage='https://static-media.streema.com/media/object-images/84973b11c9b9ada7552847f31f49091f.png', thumbnailImage= 'https://static-media.streema.com/media/object-images/84973b11c9b9ada7552847f31f49091f.png')
        li.setProperty('fanart_image', 'https://static-media.streema.com/media/object-images/84973b11c9b9ada7552847f31f49091f.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://78.129.245.8:8018/;'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]OnTopRadio[/B][/COLOR] >>          [COLOR lime](Dancehall, Hip Hop, RnB)[/COLOR]', iconImage='http://jerrardwayne3.wpengine.netdna-cdn.com/wp-content/themes/ontop/images/logo.png', thumbnailImage= 'http://jerrardwayne3.wpengine.netdna-cdn.com/wp-content/themes/ontop/images/logo.png')
        li.setProperty('fanart_image', 'https://pbs.twimg.com/profile_images/528703244122746881/Y9nGAwfB_400x400.jpeg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://uk1-pn.webcast-server.net:8698'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Kool London[/B][/COLOR] >>          [COLOR lime](Drum n bass, jungle, oldskool hardcore)[/COLOR]', iconImage='http://s1.postimg.org/fko2kyu9b/icon.png', thumbnailImage= 'http://s1.postimg.org/fko2kyu9b/icon.png')
        li.setProperty('fanart_image', 'http://koollondon.com/images/stories/kool-timetable-september-2014.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://webstreamer.co.uk:41940/;'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Pure Music 247[/B][/COLOR] >>          [COLOR lime](House + much more)[/COLOR]', iconImage='http://puremusic247.com/images/dj-Copyedittest.gif', thumbnailImage= 'http://puremusic247.com/images/dj-Copyedittest.gif')
        li.setProperty('fanart_image', 'http://djautograph.com/wp-content/uploads/2013/10/House_Music_by_Labelrx.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://50.7.184.106:8631/listen.pls'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Central Radio UK[/B][/COLOR] >>          [COLOR lime](Dance + much more)[/COLOR]', iconImage='http://s13.postimg.org/jcdhx5pqf/image.png', thumbnailImage= 'http://s13.postimg.org/jcdhx5pqf/image.png')
        li.setProperty('fanart_image', 'http://www.mrwallpaper.com/wallpapers/Music-equipment.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://213.229.108.96/RTB'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Rough Tempo[/B][/COLOR] >>          [COLOR lime](Drum n bass, jungle, oldskool hardcore)[/COLOR]', iconImage='http://www.roughtempo.com/fbimage.jpg', thumbnailImage= 'http://www.roughtempo.com/fbimage.jpg')
        li.setProperty('fanart_image', 'http://i1.ytimg.com/vi/UwCoz9kGJAs/maxresdefault.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://176.31.239.83:9136/'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Deja Classic [/B][/COLOR] >>         [COLOR lime](oldskool, UK Garage, RnB, HipHop)[/COLOR]', iconImage='http://s2.postimg.org/eg7k51z3t/icon.png', thumbnailImage= 'http://s2.postimg.org/eg7k51z3t/icon.png')
        li.setProperty('fanart_image', 'http://s18.postimg.org/fnbfwgw3d/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://176.31.239.83:9041/'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]DejaVu Live [/B][/COLOR] >>          [COLOR lime](Urban, RnB, HipHop)[/COLOR]', iconImage='http://s2.postimg.org/eg7k51z3t/icon.png', thumbnailImage= 'http://s2.postimg.org/eg7k51z3t/icon.png')
        li.setProperty('fanart_image', 'http://s18.postimg.org/fnbfwgw3d/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://78.129.228.187:8008/;stream/1'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]House fm [/B][/COLOR] >>          [COLOR lime](House)[/COLOR]', iconImage='http://i1.sndcdn.com/artworks-000049756393-x4gokq-crop.jpg?435a760', thumbnailImage= 'http://i1.sndcdn.com/artworks-000049756393-x4gokq-crop.jpg?435a760')
        li.setProperty('fanart_image', 'http://www.strictlyhousefm.co.uk/wp-content/uploads/2012/10/strictly-house-6.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://shine879.internetdomainservices.com:8204/'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Shine879 [/B][/COLOR] >>          [COLOR lime](Drum n Bass, House, UK Garage)[/COLOR]', iconImage='https://lh4.ggpht.com/0rdHZ2GOZYeiDfo1jyuWzbiFa9VIHNulX8qvTgXG3bHWMxO28mrxxUrT2VYWeQgaU4k=w300', thumbnailImage= 'https://lh4.ggpht.com/0rdHZ2GOZYeiDfo1jyuWzbiFa9VIHNulX8qvTgXG3bHWMxO28mrxxUrT2VYWeQgaU4k=w300')
        li.setProperty('fanart_image', 'http://dnbvideo.ru/wp-content/uploads/2013/09/antinox-liquid-drum-n-bass-4-1080p-hq.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://178.32.222.61:8080/'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Flames radio [/B][/COLOR] >>          [COLOR lime](Funk, Reggae, RnB, Soul)[/COLOR]', iconImage='http://i1.sndcdn.com/artworks-000069969699-cvl43d-original.jpg?a0633e8', thumbnailImage= 'http://i1.sndcdn.com/artworks-000069969699-cvl43d-original.jpg?a0633e8')
        li.setProperty('fanart_image', 'http://www.disclosurenewsonline.com/wp-content/uploads/2014/01/burning-flames-yellow-fire1.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://typhoon.exequo.org:8000/rinseradio'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Rinse fm [/B][/COLOR] >>             [COLOR lime](Urban, RnB, HipHop)[/COLOR]', iconImage='http://s16.postimg.org/kdlyi29j9/icon.png', thumbnailImage= 'http://s16.postimg.org/kdlyi29j9/icon.png')
        li.setProperty('fanart_image', 'http://s7.postimg.org/u3877stpn/fanart.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://bbc.co.uk/radio/listen/live/r1x.asx'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]bbc 1xtra[/B][/COLOR] >>             [COLOR lime](Urban, RnB, HipHop)[/COLOR]', iconImage='http://www.madtechrecords.com/wp-content/uploads/2013/08/artworks-000014947132-lbebhn-original.jpg', thumbnailImage= 'http://www.madtechrecords.com/wp-content/uploads/2013/08/artworks-000014947132-lbebhn-original.jpg')
        li.setProperty('fanart_image', 'http://s23.postimg.org/5jq12phff/fanart.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://tx.whatson.com/icecast.php?i=kissnationallow.mp3'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Kiss 100[/B][/COLOR] >>           [COLOR lime](Dance, RnB, HipHop)[/COLOR]', iconImage='http://3.bp.blogspot.com/-x1AWbyHFGug/UGMUaprrDuI/AAAAAAAAAi8/fJrShXB1SrI/s1600/kissfm.gif', thumbnailImage= 'http://3.bp.blogspot.com/-x1AWbyHFGug/UGMUaprrDuI/AAAAAAAAAi8/fJrShXB1SrI/s1600/kissfm.gif')
        li.setProperty('fanart_image', 'http://336fcc281d9fb3480f2a-0af712088f38ef5910226b2ecb408482.r82.cf2.rackcdn.com/img-230-3-1366642376.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://media-ice.musicradio.com/CapitalXTRALondonMP3.m3u'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Capital Xtra[/B][/COLOR] >>           [COLOR lime](Dance, RnB, Urban)[/COLOR]', iconImage='http://www.musicweek.com/cimages/7ec1c3e8cda116edcba97d259933f288.jpg', thumbnailImage= 'http://www.musicweek.com/cimages/7ec1c3e8cda116edcba97d259933f288.jpg')
        li.setProperty('fanart_image', 'http://londonist.com/wp-content/uploads/2013/11/Capital-XTRA.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://193.27.42.226:8192/mosdir.mp3'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Ministry of Sound Radio[/B][/COLOR] >>           [COLOR lime](Dance, House, Drum n Bass)[/COLOR]', iconImage='http://i1.sndcdn.com/artworks-000070064884-tec6ir-original.jpg?f775e59', thumbnailImage= 'http://i1.sndcdn.com/artworks-000070064884-tec6ir-original.jpg?f775e59')
        li.setProperty('fanart_image', 'http://1.bp.blogspot.com/-pXdClkxvZu8/TleccVYC3EI/AAAAAAAAAic/A7aV-CrKcaU/s1600/Ministry-of-Sound.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://50.117.26.26:5448/'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Upper Echelon Radio[/B][/COLOR] >>        [COLOR yellow](US)[/COLOR] [COLOR lime](HipHop)[/COLOR]', iconImage='https://lh4.ggpht.com/TQuDn_5thkjgYupY294UbkBiri4lf8InlIa7_MRj8OVwWhZcVcTxiX0CZV6eF00u9lP1=w300', thumbnailImage= 'https://lh4.ggpht.com/TQuDn_5thkjgYupY294UbkBiri4lf8InlIa7_MRj8OVwWhZcVcTxiX0CZV6eF00u9lP1=w300')
        li.setProperty('fanart_image', 'http://i1.ytimg.com/vi/L8IU9C3xZCk/maxresdefault.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://powerhitz.powerhitz.com:5030'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Power Hitz[/B][/COLOR] >>        [COLOR yellow](US)[/COLOR] [COLOR lime](RnB, HipHop)[/COLOR]', iconImage='http://sfweb3.radioline.fr/covers/39322/logo196.png', thumbnailImage= 'http://sfweb3.radioline.fr/covers/39322/logo196.png')
        li.setProperty('fanart_image', 'http://w8themes.com/wp-content/uploads/2013/08/Musical-Wallpapers.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://209.105.250.73:8206'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Zmix 97[/B][/COLOR] >>        [COLOR yellow](US)[/COLOR] [COLOR lime](old school, HipHop, funk)[/COLOR]', iconImage='http://media-cache-ec0.pinimg.com/236x/d8/be/0b/d8be0ba53a350149e97eb0e643f5fd1f.jpg', thumbnailImage= 'http://media-cache-ec0.pinimg.com/236x/d8/be/0b/d8be0ba53a350149e97eb0e643f5fd1f.jpg')
        li.setProperty('fanart_image', 'http://prettyriveracademy.com/wp-content/uploads/2013/08/hiphop6.jpg.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://s9.myradiostream.com:4418'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Urban hitz radio[/B][/COLOR] >>        [COLOR yellow](US)[/COLOR] [COLOR lime](RnB, HipHop)[/COLOR]', iconImage='https://pbs.twimg.com/profile_images/3424721247/d1111dabf5fd05d86d7fadde2be2e956.png', thumbnailImage= 'https://pbs.twimg.com/profile_images/3424721247/d1111dabf5fd05d86d7fadde2be2e956.png')
        li.setProperty('fanart_image', 'http://upload.wikimedia.org/wikipedia/commons/8/87/The_official_Urban_Hitz_Radio_Logo_for_2013!.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://hot108jamz.hot108.com:4020'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Hot 108 jamz[/B][/COLOR] >>        [COLOR yellow](US)[/COLOR] [COLOR lime](HipHop)[/COLOR]', iconImage='http://i1.ytimg.com/i/DvfgG9q0DPIrVCfy6C-sFA/mq1.jpg?v=dbb2c7', thumbnailImage= 'http://i1.ytimg.com/i/DvfgG9q0DPIrVCfy6C-sFA/mq1.jpg?v=dbb2c7')
        li.setProperty('fanart_image', 'http://i1.sndcdn.com/artworks-000006705654-aw46p2-original.jpg?435a760')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://tuner.defjay.com:80/'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Def jay[/B][/COLOR] >>        [COLOR yellow](US)[/COLOR] [COLOR lime](RnB)[/COLOR]', iconImage='http://www.defjay.com/_img/_layout/boomboom.gif', thumbnailImage= 'http://www.defjay.com/_img/_layout/boomboom.gif')
        li.setProperty('fanart_image', 'http://www.defjay.de/_data/promo/logo_hg_schwarz.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://war.str3am.com:7550/'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Power 106 FM[/B][/COLOR] >>        [COLOR yellow](Jam)[/COLOR] [COLOR lime](Reggae)[/COLOR]', iconImage='http://i.img.co/radio/62/27/2762_290.png', thumbnailImage= 'http://i.img.co/radio/62/27/2762_290.png')
        li.setProperty('fanart_image', 'http://th03.deviantart.net/fs70/PRE/f/2010/344/3/6/rasta_wallpaper_by_ipwnpt-d34luim.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://war.str3am.com:7970'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Ragga Kings[/B][/COLOR] >>        [COLOR yellow](Jam)[/COLOR] [COLOR lime](Reggae, Dancehall)[/COLOR]', iconImage='http://static.rad.io/images/broadcasts/33/32/1922/w175.png', thumbnailImage= 'http://static.rad.io/images/broadcasts/33/32/1922/w175.png')
        li.setProperty('fanart_image', 'http://dubmarine.org/wp-content/uploads/2011/11/RaggakingsPodcast1111-INFRA.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://radio.bigupradio.com:8000/;.mp3'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Big up radio[/B][/COLOR] >>        [COLOR yellow](Jam)[/COLOR] [COLOR lime](Dancehall)[/COLOR]', iconImage='http://static.radio.fr/images/broadcasts/64/3d/3420/w175.png', thumbnailImage= 'http://static.radio.fr/images/broadcasts/64/3d/3420/w175.png')
        li.setProperty('fanart_image', 'http://2.bp.blogspot.com/-G59C17P6Rqo/UHDcmBFcucI/AAAAAAAAAFg/HOtnL0fiaJs/s1600/Jah1.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://radio.bigupradio.com:8013/;.mp3'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Big up radio[/B][/COLOR] >>        [COLOR yellow](Jam)[/COLOR] [COLOR lime](Dub)[/COLOR]', iconImage='http://www.pcwelt.de/images/1/0/7/6/5/3/1/f4735b397dcba707.jpeg', thumbnailImage= 'http://www.pcwelt.de/images/1/0/7/6/5/3/1/f4735b397dcba707.jpeg')
        li.setProperty('fanart_image', 'http://bigupradio.com/reggae/wp-content/uploads/2009/10/Reggae-Flag.jpg')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        url = 'http://radio.bigupradio.com:8029/;.mp3'
        li = xbmcgui.ListItem('[COLOR lightsteelblue][B]Big up radio[/B][/COLOR] >>        [COLOR yellow](Jam)[/COLOR] [COLOR lime](Reggaeton)[/COLOR]', iconImage='http://zvlastnistyl.cz/wp-content/uploads/2009/01/BUR_radio_tag.gif', thumbnailImage= 'http://zvlastnistyl.cz/wp-content/uploads/2009/01/BUR_radio_tag.gif')
        li.setProperty('fanart_image', 'http://0.static.wix.com/media/5013e42b6aea16dfd8af90d21b9e4ebb.wix_mp_512')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        addon.add_directory({'mode': 'HelpMenu'}, {'title':  '[B][COLOR gold]if you like rave music install Rave player from TheYids REPO[/COLOR][/B]'}, img= 'https://raw.githubusercontent.com/TheYid/My-Repo/master/plugin.audio.raveplayer/icon.png', fanart= 'https://raw.githubusercontent.com/TheYid/My-Repo/master/plugin.audio.raveplayer/fanart.jpg')
        addon.add_directory({'mode': 'RadioMenu', '': '', '': '',
                             '': '', '': ''}, {'title':  '[COLOR mediumvioletred]~~~~~~~[/COLOR][COLOR aqua][B]Please report any broken links to @TheYid009 on twitter[/B][/COLOR][COLOR mediumvioletred]~~~~~~~[/COLOR]'}, img=IconPath + 'radioty.png', fanart='http://geewall.com/mmc_uploads/6119-music-notes-wallpaper-37082.jpg')

        xbmcplugin.endOfDirectory(addon_handle)

#-----------------------live---------------------------------------live-----------------------------live--------------------------live-------------------------------live-------#


def LiveMenu():    #streams
        addon.add_directory({'mode': 'GetTitles64', 'section': 'ALL', 'url': BASE_URL64 + '/skysports.php',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR red](TEST) [/COLOR][COLOR cornflowerblue][B]live stream Sky Sports[/B][/COLOR] [COLOR cadetblue](SS) [/COLOR]>>'}, img= 'https://lh5.ggpht.com/z8Rj0gcoQa-XIwRaxRNBbiCX5SV1gfnEXtJx5AqQitxRY0Y1-3zwNk7RONmRschckXqn=w300', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles64', 'section': 'ALL', 'url': BASE_URL64 + '/btsport.php',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR red](TEST) [/COLOR][COLOR cornflowerblue][B]live stream BT Sports[/B][/COLOR] [COLOR cadetblue](SS) [/COLOR]>>'}, img= 'https://lh5.ggpht.com/z8Rj0gcoQa-XIwRaxRNBbiCX5SV1gfnEXtJx5AqQitxRY0Y1-3zwNk7RONmRschckXqn=w300', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles64', 'section': 'ALL', 'url': BASE_URL64 + '/espn.php',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR red](TEST) [/COLOR][COLOR cornflowerblue][B]live stream ESPN Sports[/B][/COLOR] [COLOR cadetblue](SS) [/COLOR]>>'}, img= 'https://lh5.ggpht.com/z8Rj0gcoQa-XIwRaxRNBbiCX5SV1gfnEXtJx5AqQitxRY0Y1-3zwNk7RONmRschckXqn=w300', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles64', 'section': 'ALL', 'url': BASE_URL64 + '/wwenetwork.php',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR red](TEST) [/COLOR][COLOR cornflowerblue][B]live stream WWE Network[/B][/COLOR] [COLOR cadetblue](SS) [/COLOR]>>'}, img= 'https://lh5.ggpht.com/z8Rj0gcoQa-XIwRaxRNBbiCX5SV1gfnEXtJx5AqQitxRY0Y1-3zwNk7RONmRschckXqn=w300', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles35a', 'url': BASE_URL35 + '/yellow2.txt'}, {'title':  '[COLOR mediumorchid][B]Streams >[/COLOR][/B] >'}, img=IconPath + 'stream.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-----------------------documentarys---------------------------------------documentarys-----------------------------documentarys--------------------------documentarys-------------------------------help-------#


def DocMenu():    #documentarys
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/culture/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Culture [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/drugs/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Drugs [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/environment/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Environment [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/mystery/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Mystery [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/nature/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Nature [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/psychology/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Psychology [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/science/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Science [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/sexuality/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Sexuality [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/society/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Society [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles55', 'section': 'ALL', 'url': BASE_URL55 + '/category/sports/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Sports [/B][/COLOR] [COLOR powderblue](DocumentaryStorm) [/COLOR]>>'}, img=IconPath + 'ds.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/movie-tags/documentary/date',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Latest Documentaries[/B][/COLOR] [COLOR royalblue](TV HQ) [/COLOR]>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles40', 'section': 'ALL', 'url': BASE_URL40 + '/category/documentaries/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR peachpuff][B]Latest Documentaries[/B][/COLOR] [COLOR seagreen](uwatchfree) [/COLOR]>>'}, img=IconPath + 'uw3.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------sport------------------------------sport----------------------sport---------------------------sport------------------------------sport--------#

def SportMenu():   #sport
        addon.add_directory({'mode': 'GetTitles42', 'section': 'ALL', 'url': BASE_URL42 + '/category/wwe/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest WWE[/B][/COLOR]  [COLOR gold](watchwrestling) [/COLOR] >>'}, img=IconPath + 'ww.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles42', 'section': 'ALL', 'url': BASE_URL42 + '/category/wwenetwork/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest WWE Network[/B][/COLOR]  [COLOR gold](watchwrestling) [/COLOR] >>'}, img=IconPath + 'ww.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles42', 'section': 'ALL', 'url': BASE_URL42 + '/category/tna/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest TNA[/B][/COLOR]  [COLOR gold](watchwrestling) [/COLOR] >>'}, img=IconPath + 'ww.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles42', 'section': 'ALL', 'url': BASE_URL42 + '/category/weekly-indys/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest Weekly Indys[/B][/COLOR]  [COLOR gold](watchwrestling) [/COLOR] >>'}, img=IconPath + 'ww.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles42', 'section': 'ALL', 'url': BASE_URL42 + '/category/other-sports/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest MMA & Boxing[/B][/COLOR]  [COLOR gold](watchwrestling) [/COLOR] >>'}, img=IconPath + 'ww.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles42', 'section': 'ALL', 'url': BASE_URL42 + '/category/njpw/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest NJPW[/B][/COLOR]  [COLOR gold](watchwrestling) [/COLOR] >>'}, img=IconPath + 'ww.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles42', 'section': 'ALL', 'url': BASE_URL42 + '/category/archives/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Archives & More[/B][/COLOR]  [COLOR gold](watchwrestling.ch) [/COLOR] >>'}, img=IconPath + 'ww.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[COLOR lemonchiffon][B]Watch Wrestling[/B][/COLOR] : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery12'},  {'title':  '[COLOR khaki][B]M[/COLOR][COLOR blue]E[/COLOR][COLOR salmon]G[/COLOR][COLOR darkseagreen]A[/COLOR][/B] [COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR blue][B]HUB[/B][/COLOR] : [COLOR green]Search[/COLOR] (Sport)'}, img=IconPath + 'mes.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------movies ------------------------movies ---------------------------movies --------------------------movies -------------------------------movies -------#

def MovieMenu():   #movies
        addon.add_directory({'mode': 'GetTitles49', 'url': BASE_URL49 + '/new-movie-releases'}, {'title':  '[COLOR cornflowerblue][B]Box office[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (moviefone)'}, img=IconPath + 'isbo.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles49', 'url': BASE_URL49 + '/dvd'}, {'title':  '[COLOR cornflowerblue][B]Featured[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (moviefone)'}, img=IconPath + 'inf.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles49a', 'url': BASE_URL49 + '/dvd/coming-soon/'}, {'title':  '[COLOR cornflowerblue][B]Featured now[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (moviefone)'}, img=IconPath + 'inf.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles62a', 'url': BASE_URL62 + '/movies/'}, {'title':  '[COLOR blue][B]Top Movies[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR]'}, img=IconPath + 'reto.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles89', 'section': 'ALL', 'url': BASE_URL89 + '/tag/movies/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR  cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR blue](UpBuzz) [/COLOR]>>'}, img=IconPath + 'ub.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles91', 'section': 'ALL', 'url': BASE_URL91 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR pink](freemoviesu.to) [/COLOR]>>'}, img=IconPath + 'fmu1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles20', 'section': 'ALL', 'url': BASE_URL20 + '/category/hollywood/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR][COLOR darkorchid](World4UFree) [/COLOR]>>'}, img=IconPath + 'w4u.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles23', 'section': 'ALL', 'url': BASE_URL23 + '/category/hollywood-movie/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR crimson](300mb movies4u) [/COLOR] >>'}, img=IconPath + 'm4u1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles57', 'section': 'ALL', 'url': BASE_URL57 + '/category/english/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR yellow](latestdude) [/COLOR]>>'}, img=IconPath + 'ld.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles87', 'section': 'ALL', 'url': BASE_URL87 + '/'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR yellow](bluraymovies) [/COLOR]>>'}, img=IconPath + 'bmf.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles88', 'section': 'ALL', 'url': BASE_URL88 + 'forum/2'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR gold](onlineseries) [/COLOR]>>'}, img=IconPath + '1010.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles90', 'section': 'ALL', 'url': BASE_URL90 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR green](moviewatcher) [/COLOR]>>'}, img=IconPath + 'tvmu.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles22', 'section': 'ALL', 'url': BASE_URL22 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR pink](themovie4u) [/COLOR]>>'}, img=IconPath + 'm4uco.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles66', 'section': 'ALL', 'url': BASE_URL66 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR brown](watchitvideos) [/COLOR]>>'}, img=IconPath + 'wm.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles70', 'section': 'ALL', 'url': BASE_URL70 + '/category/hollywood/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR darkorange](filmxy) [/COLOR]>>'}, img=IconPath + 'fil.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles69', 'section': 'ALL', 'url': BASE_URL69 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR orange](moviesland4u) [/COLOR]>>'}, img=IconPath + 'jland.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles40', 'section': 'ALL', 'url': BASE_URL40 + '/category/hollywood/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR seagreen](uwatchfree) [/COLOR]>>'}, img=IconPath + 'uw3.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles21', 'section': 'ALL', 'url': BASE_URL21 + '/category/hollywood-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR lawngreen](movies2k.eu) [/COLOR]>>'}, img=IconPath + '2k.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles84', 'section': 'ALL', 'url': BASE_URL84 + '/index.php/category/movies-online/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR blue](superseriale) [/COLOR]>>'}, img=IconPath + 'ss1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles39', 'section': 'ALL', 'url': BASE_URL39 + '/movies/category/hollywood-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR cadetblue](OMG) [/COLOR]>>'}, img=IconPath + 'omg.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'HqMenu'}, {'title':  '[COLOR deepskyblue][B]Movie Genre[/B][/COLOR] [COLOR royalblue](TV HQ) [/COLOR]>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'WtMenu'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR lightsteelblue][B]International Movies Zone[/B][/COLOR] >>'}, img=IconPath + 'iz.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'RgMenu'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR mediumturquoise][B]Full HD Zone[/B][/COLOR] >>'}, img=IconPath + 'fhz1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery11'},  {'title':  '[COLOR khaki][B]M[/COLOR][COLOR blue]E[/COLOR][COLOR salmon]G[/COLOR][COLOR darkseagreen]A[/COLOR][/B] [COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR blue][B]HUB[/B][/COLOR] : [COLOR green]Search[/COLOR] (movies)'}, img=IconPath + 'mes.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- tvhq movies ------------------------------------------------------------------------------------------------#

def HqMenu():   #tvhq
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/movies/date/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]Latest Movies[/B][/COLOR] [COLOR royalblue](TV HQ) [/COLOR]>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/movies/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]movies[/B] [/COLOR][COLOR teal](imdb)[/COLOR] >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/movies/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]movies[/B] [/COLOR][COLOR teal](abc)[/COLOR] >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/movie-tags/action',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Action >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=adventure',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Adventure>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=/category/movies/animation',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Animation >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + 'index.php?menu=movie-tag&tag=biography',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Biography>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=comedy',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Comedy >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=crime',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Crime >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=documentary',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Documentary >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=drama',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Drama>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=family',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Family >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=fantasy',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Fantasy >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=horror',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Horror >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=history',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'History >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=musical',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Musical >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=mystery',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Mystery >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=reality-tv',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Reality-tv >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=romance',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Romance >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=sci-fi',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Sci-fi >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=sport',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Sport >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=talk-show',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Talk-show >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=thriller',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Thriller >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=war',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'War >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=western',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Western >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32', 'section': 'ALL', 'url': BASE_URL32 + '/index.php?menu=movie-tag&tag=zombie',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Zombie >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')


        addon.add_directory({'mode': 'GetSearchQuery5'},  {'title':  '[COLOR green][B]Search[/B][/COLOR] [COLOR royalblue](TV HQ) [/COLOR] >> '}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------- HD zone movies -------------------------------------------------------------------------------------------------#

def RgMenu():  #HD zone
        addon.add_directory({'mode': 'GetTitles66', 'section': 'ALL', 'url': BASE_URL66 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest 1080p[/B][/COLOR] [COLOR brown](watchitvideos) [/COLOR]>>'}, img=IconPath + 'wm.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles23', 'section': 'ALL', 'url': BASE_URL23 + '/category/hollywood-movie/english-yify-movie/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Movies by Yify[/B][/COLOR] [COLOR crimson](300mb movies4u) [/COLOR] >>'}, img=IconPath + 'm4u1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles23', 'section': 'ALL', 'url': BASE_URL23 + '/category/hevc-movie/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Movies by HEVC[/B][/COLOR] [COLOR crimson](300mb movies4u) [/COLOR] >>'}, img=IconPath + 'm4u1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles23', 'section': 'ALL', 'url': BASE_URL23 + '/category/hollywood-movie/english-3d-movie/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]3D Movies[/B][/COLOR] [COLOR crimson](300mb movies4u) [/COLOR] >>'}, img=IconPath + 'm4u1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles57', 'section': 'ALL', 'url': BASE_URL57 + '/category/1080p/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest 1080p Movies[/B][/COLOR] [COLOR yellow](latestdude) [/COLOR]>>'}, img=IconPath + 'ld.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles57', 'section': 'ALL', 'url': BASE_URL57 + '/category/brrip/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest 720p Movies[/B][/COLOR] [COLOR yellow](latestdude) [/COLOR]>>'}, img=IconPath + 'ld.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles57', 'section': 'ALL', 'url': BASE_URL57 + '/category/3d/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest 3D Movies[/B][/COLOR] [COLOR yellow](latestdude) [/COLOR]>>'}, img=IconPath + 'ld.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- inter zone movies -------------------------------------------------------------------------------------------------#

def WtMenu():   #world4ufree #m2k
        #addon.add_directory({'mode': 'Categoriesuwf' },  {'title':  '[COLOR cornflowerblue][B]Movie Genre[/B][/COLOR] [COLOR seagreen](uwatchfree) [/COLOR]>>'}, img=IconPath + 'uw3.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles3', 'section': 'ALL', 'url': BASE_URL3 + '/category/bollywood-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Bollywood Movies[/B][/COLOR] [COLOR yellow](moviz4u) [/COLOR] >>'}, img=IconPath + 'mo4u.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles3', 'section': 'ALL', 'url': BASE_URL3 + '/category/hollywood-movies-in-hindi/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Hollywood Movies (In Hindi)[/B][/COLOR] [COLOR yellow](moviz4u) [/COLOR] >>'}, img=IconPath + 'mo4u.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles3', 'section': 'ALL', 'url': BASE_URL3 + '/category/hindi-dubbed-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Hindi Dubbed [/B][/COLOR] [COLOR yellow](moviz4u) [/COLOR] >>'}, img=IconPath + 'mo4u.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles3', 'section': 'ALL', 'url': BASE_URL3 + '/category/animation-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Latest Animation Movies [/B][/COLOR] [COLOR yellow](moviz4u) [/COLOR] >>'}, img=IconPath + 'mo4u.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles23', 'section': 'ALL', 'url': BASE_URL23 + '/category/hollywood-movie/english-movie-dual-audio/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Dual Audio[/B][/COLOR] [COLOR crimson](300mb movies4u) [/COLOR] >>'}, img=IconPath + 'm4u1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles23', 'section': 'ALL', 'url': BASE_URL23 + '/category/tamil-movie/tamil-hindi-dubbed-movie/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Tamil hindi Dubbed[/B][/COLOR] [COLOR crimson](300mb movies4u) [/COLOR] >>'}, img=IconPath + 'm4u1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles23', 'section': 'ALL', 'url': BASE_URL23 + '/category/bollywood-movie/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Bollywood[/B][/COLOR] [COLOR crimson](300mb movies4u) [/COLOR] >>'}, img=IconPath + 'm4u1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles23', 'section': 'ALL', 'url': BASE_URL23 + '/category/tamil-movie/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Tamil[/B][/COLOR] [COLOR crimson](300mb movies4u) [/COLOR] >>'}, img=IconPath + 'm4u1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles20', 'section': 'ALL', 'url': BASE_URL20 + '/category/bollywood/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Bollywood [/B][/COLOR] [COLOR darkorchid](World4UFree) [/COLOR]>>'}, img=IconPath + 'w4u.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles20', 'section': 'ALL', 'url': BASE_URL20 + '/category/hindi-dubbed-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Hindi Dubbed [/B][/COLOR] [COLOR darkorchid](World4UFree) [/COLOR]>>'}, img=IconPath + 'w4u.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles20', 'section': 'ALL', 'url': BASE_URL20 + '/category/songs/indian-videos/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Indian Music Videos [/B][/COLOR] [COLOR darkorchid](World4UFree) [/COLOR]>>'}, img=IconPath + 'w4u.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles21', 'section': 'ALL', 'url': BASE_URL21 + '/category/hindi-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]Hindi [/B][/COLOR] [COLOR lawngreen](movies2k.eu) [/COLOR]>>'}, img=IconPath + '2k.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles21', 'section': 'ALL', 'url': BASE_URL21 + '/category/hindi-dubbed/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]Hindi Dubbed [/B][/COLOR] [COLOR lawngreen](movies2k.eu) [/COLOR]>>'}, img=IconPath + '2k.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles21', 'section': 'ALL', 'url': BASE_URL21 + '/category/malayalam-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]Malayalam [/B][/COLOR] [COLOR lawngreen](movies2k.eu) [/COLOR]>>'}, img=IconPath + '2k.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles21', 'section': 'ALL', 'url': BASE_URL21 + '/category/tamil-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]Tamil [/B][/COLOR] [COLOR lawngreen](movies2k.eu) [/COLOR]>>'}, img=IconPath + '2k.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles21', 'section': 'ALL', 'url': BASE_URL21 + '/category/telugu-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]Telugu [/B][/COLOR] [COLOR lawngreen](movies2k.eu) [/COLOR]>>'}, img=IconPath + '2k.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles57', 'section': 'ALL', 'url': BASE_URL57 + '/category/hindi-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Hindi Movies[/B][/COLOR] [COLOR yellow](latestdude) [/COLOR]>>'}, img=IconPath + 'ld.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles39', 'section': 'ALL', 'url': BASE_URL39 + '/movies/category/bollywood-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Hindi Movies[/B][/COLOR] [COLOR cadetblue](OMG) [/COLOR]>>'}, img=IconPath + 'omg.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles39', 'section': 'ALL', 'url': BASE_URL39 + '/movies/category/others/punjabi/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Punjabi Movies[/B][/COLOR] [COLOR cadetblue](OMG) [/COLOR]>>'}, img=IconPath + 'omg.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles39', 'section': 'ALL', 'url': BASE_URL39 + '/movies/category/tamil/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Tamil Movies[/B][/COLOR] [COLOR cadetblue](OMG) [/COLOR]>>'}, img=IconPath + 'omg.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles39', 'section': 'ALL', 'url': BASE_URL39 + '/movies/category/telugu/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Telugu Movies[/B][/COLOR] [COLOR cadetblue](OMG) [/COLOR]>>'}, img=IconPath + 'omg.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles39', 'section': 'ALL', 'url': BASE_URL39 + '/movies/category/malayalam/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Malayalam Movies[/B][/COLOR] [COLOR cadetblue](OMG) [/COLOR]>>'}, img=IconPath + 'omg.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles39', 'section': 'ALL', 'url': BASE_URL39 + '/movies/category/bengali/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Bengali Movies[/B][/COLOR] [COLOR cadetblue](OMG) [/COLOR]>>'}, img=IconPath + 'omg.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles39', 'section': 'ALL', 'url': BASE_URL39 + '/movies/category/dubbed/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Dubbed Movies[/B][/COLOR] [COLOR cadetblue](OMG) [/COLOR]>>'}, img=IconPath + 'omg.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles39', 'section': 'ALL', 'url': BASE_URL39 + '/movies/category/others/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR cornflowerblue][B]Others Movies[/B][/COLOR] [COLOR cadetblue](OMG) [/COLOR]>>'}, img=IconPath + 'omg.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles81', 'section': 'ALL', 'url': BASE_URL81 + 'newapp/part/MAIN.php',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]New Releases[/B][/COLOR] [COLOR cadetblue](DesiMovies) [/COLOR]>>'}, img=IconPath + 'links1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles811', 'section': 'ALL', 'url': BASE_URL81 + 'newapp/part/MAIN.php',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]New Releases[/B][/COLOR] [COLOR cadetblue](DesiMovies 2) [/COLOR]>>'}, img=IconPath + 'links1.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

####################################---tv---####################---tv---####################---tv---###########################---tv---##########################---tv---#####################################################

def TvMenu():       #tv
        addon.add_directory({'mode': 'GetTitles143', 'section': 'ALL', 'url': BASE_URL73 + '/cat/'}, {'title':  '[COLOR orchid][B]*TV Calendar Search*[/B][/COLOR]'}, img=IconPath + 'tcs.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles144', 'section': 'ALL', 'url': BASE_URL74 + '/'}, {'title':  '[COLOR greenyellow][B]*TV Index Search[/B] (A-Z)*[/COLOR]'}, img=IconPath + 'tas.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles62', 'url': BASE_URL62 + '/tvshows/'}, {'title':  '[COLOR darkorange][B]Top Shows[/B] [/COLOR]: [COLOR green]Index Search[/COLOR]'}, img=IconPath + 'rt.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles2b', 'url': BASE_URL12 + '/tv-shows'}, {'title':  '[COLOR darkorange][B]Latest Episodes[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (allcinemamovies)'}, img=IconPath + 'intvs.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles89', 'section': 'ALL', 'url': BASE_URL89 + '/tag/tv/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Latest Episodes[/B][/COLOR] [COLOR blue](UpBuzz) [/COLOR]>>'}, img=IconPath + 'ub.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles2', 'section': 'ALL', 'url': BASE_URL2 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Latest Episodes[/B][/COLOR] [COLOR green](TVDL) [/COLOR]>>'}, img=IconPath + 'tvdl.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles71', 'section': 'ALL', 'url': BASE_URL71 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Latest Episodes[/B][/COLOR] [COLOR blue](CNW) [/COLOR]>>'}, img=IconPath + 'cnw.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles83', 'section': 'ALL', 'url': BASE_URL83 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Latest Episodes[/B][/COLOR] [COLOR green](tvmuseum) [/COLOR]>>'}, img=IconPath + 'tvmu.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles88', 'section': 'ALL', 'url': BASE_URL88 + 'forum/3'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Latest Episodes[/B][/COLOR] [COLOR gold](onlineseries) [/COLOR]>>'}, img=IconPath + '1010.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles23', 'section': 'ALL', 'url': BASE_URL23 + '/category/tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Latest Episodes[/B][/COLOR] [COLOR crimson](300mb movies4u) [/COLOR] >>'}, img=IconPath + 'm4u1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles66a', 'section': 'ALL', 'url': BASE_URL66 + '/movies-genre/tv-shows-episodes/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Latest Episodes[/B][/COLOR] [COLOR brown](watchitvideos) [/COLOR]>>'}, img=IconPath + 'wm.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles1', 'section': 'ALL', 'url': BASE_URL1 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Latest Episodes[/B][/COLOR] [COLOR salmon](ADL) [/COLOR]>>'}, img=IconPath + 'adl.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles44', 'section': 'ALL', 'url': BASE_URL44 + 'shows-movies-releases/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Latest Episodes[/B][/COLOR] [COLOR green](pullvideos) [/COLOR]>>'}, img=IconPath + 'ptv.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetLinks17', 'section': 'ALL', 'url': BASE_URL4 + '/'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Todays Hugefiles links[/B][/COLOR] [COLOR chartreuse](tvshows-hdtv) [/COLOR]>>'}, img=IconPath + 'hf.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'Hq4Menu'}, {'title':  '[COLOR orange][B]Full Seasons[/B][/COLOR] [COLOR royalblue](TV HQ) [/COLOR]>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles2a', 'url': BASE_URL32 + '/tv-shows'}, {'title':  '[COLOR darkorange][B]Latest Episodes[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (TVHQ)'}, img=IconPath + 'intvs.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery12'},  {'title':  '[COLOR khaki][B]M[/COLOR][COLOR blue]E[/COLOR][COLOR salmon]G[/COLOR][COLOR darkseagreen]A[/COLOR][/B] [COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR blue][B]HUB[/B][/COLOR] : [COLOR green]Search[/COLOR] (tv episodes)'}, img=IconPath + 'mes.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------TVHQ---------------------------------------------------------------------------------------#

def Hq4Menu():          # tvhq tv
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-shows/date',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]Latest Added [/B][/COLOR] >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-shows/abc/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]ABC [/B][/COLOR] >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-shows/imdb_rating/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR cornflowerblue][B]Top IMDB [/B][/COLOR] >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'Hq5Menu'}, {'title':  '[COLOR deepskyblue][B]TV Shows Genre[/B][/COLOR] [COLOR teal](Latest added) [/COLOR]>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png') 
        addon.add_directory({'mode': 'Hq6Menu'}, {'title':  '[COLOR deepskyblue][B]TV Shows Genre[/B][/COLOR] [COLOR teal](IMDB rating) [/COLOR]>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png') 
        addon.add_directory({'mode': 'Hq7Menu'}, {'title':  '[COLOR deepskyblue][B]TV Shows Genre[/B][/COLOR] [COLOR teal](A/Z) [/COLOR]>>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Hq5Menu():          # hqtv tv
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/documentary',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Documentary >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/action',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Action >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/adventure',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Adventure >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/animation',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Animation >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/comedy',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Comedy >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/cooking-food',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Cooking - Food >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/crime',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Crime >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/drama',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Drama >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/family',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Family >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/fantasy',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Fantasy >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/horror',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Horror >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/mystery',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Mystery >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/news',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'News >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/reality-tv',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Reality-tv >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/romance',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Romance >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/thriller',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Thriller >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Hq6Menu():          # tvhq tv imdb
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/-documentary/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Documentary >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/action/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Action >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/adventure/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Adventure >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/animation/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Animation >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/comedy/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Comedy >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/cooking-food/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Cooking - Food >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/crime/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Crime >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/drama/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Drama >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/family/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Family >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/fantasy/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Fantasy >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/horror/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Horror >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/mystery/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Mystery >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/news/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'News >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/reality-tv/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Reality-tv >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/romance/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Romance >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/thriller/imdb_rating',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Thriller >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Hq7Menu():          # tvhq tv abc
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/-documentary/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Documentary >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/action/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Action >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/adventure/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Adventure >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/animation/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Animation >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/comedy/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Comedy >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/cooking-food/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Cooking - Food >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/crime/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Crime >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/drama/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Drama >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/family/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Family >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/fantasy/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Fantasy >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/horror/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Horror >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/mystery/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Mystery >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/news/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'News >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/reality-tv/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Reality-tv >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/romance/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Romance >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles32b', 'section': 'ALL', 'url': BASE_URL32 + '/tv-tags/thriller/abc',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  'Thriller >>'}, img=IconPath + 'tvhq.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

################################################################################searchmenu###############################################################################################

def SearchMenu():
        addon.add_directory({'mode': 'GetSearchQuery11'},  {'title':  '[COLOR khaki][B]M[/COLOR][COLOR blue]E[/COLOR][COLOR salmon]G[/COLOR][COLOR darkseagreen]A[/COLOR][/B] [COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR blue][B]HUB[/B][/COLOR] : [COLOR green]Search[/COLOR] (movies)'}, img=IconPath + 'mes.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery12'},  {'title':  '[COLOR khaki][B]M[/COLOR][COLOR blue]E[/COLOR][COLOR salmon]G[/COLOR][COLOR darkseagreen]A[/COLOR][/B] [COLOR blue][B]E[/B][/COLOR]ntertainment [COLOR blue][B]HUB[/B][/COLOR] : [COLOR green]Search[/COLOR] (tv episodes & sport)'}, img=IconPath + 'mes.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles49', 'url': BASE_URL49 + '/new-movie-releases'}, {'title':  '[COLOR cornflowerblue][B]Box office[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (moviefone)'}, img=IconPath + 'isbo.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles49', 'url': BASE_URL49 + '/dvd'}, {'title':  '[COLOR cornflowerblue][B]Featured[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (moviefone)'}, img=IconPath + 'inf.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles49', 'url': BASE_URL49 + '/dvd/coming-soon'}, {'title':  '[COLOR cornflowerblue][B]Featured now[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (moviefone)'}, img=IconPath + 'inf.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles41a', 'section': 'ALL', 'url': BASE_URL41 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Episodes[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (latest episodes)'}, img=IconPath + 'nintvs.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles2b', 'url': BASE_URL12 + '/tv-shows/date'}, {'title':  '[COLOR darkorange][B]Latest Episodes[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (allcinemamovies)'}, img=IconPath + 'intvs.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles2a', 'url': BASE_URL32 + '/tv-shows'}, {'title':  '[COLOR darkorange][B]Latest Episodes[/B] [/COLOR]: [COLOR greenyellow]Index Search[/COLOR] (TVHQ)'}, img=IconPath + 'intvs.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery5'},  {'title':  '[COLOR royalblue][B]TV HQ[/B][/COLOR] : (movie) [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery9'},  {'title':  '[COLOR royalblue][B]PrimeFlicks[/B][/COLOR] : (movie) [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[COLOR lemonchiffon][B]Watch Wrestling[/B][/COLOR] : (mma, boxing & wrestling [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

########################################################################search#################################################################################################

##------------------------------------------------ tvhq ----------------------------------------------------------------------------------------------------------------##

def GetSearchQuery5():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]Search[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search5(query)
	else:
                return
def Search5(query):
        url = 'http://www.tvhq.info/index.php?menu=search&query='+query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<figure class=".+?">\s*?<a href="(.+?)">\s*?<img class=".+?" src="(.+?)" alt="(.+?)">', re.DOTALL).findall(html)
        for url, img, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title}, img=img, fanart=FanartPath + 'fanart.png')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

##----------------------------------------------------------- primeflicks ------------------------------------------------------------------------------------------##

def GetSearchQuery9():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]Search [/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search9(query)
	else:
                return
def Search9(query):
        url = 'http://primeflicks.me/index.php?menu=search&query='+query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('img-preview spec-border.+?src=".+?src=(.+?)&amp;.+?".+?href="(.+?)".+?>(.+?)<.+?', re.DOTALL).findall(html)
        for img, url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title}, img= img, fanart=FanartPath + 'fanart.png')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

##----------------------------------------------------------- watchwrestling ------------------------------------------------------------------------------------------##

def GetSearchQuery():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]Search [/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search(query)
	else:
                return
def Search(query):
        url = 'http://watchwrestling.ch/index.php?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<a class="clip-link" data-id=".+?" title="Watch (.+?)" href="(.+?)">\s*?<span class="clip">\s*?<img src="(.+?)" alt=".+?"', re.DOTALL).findall(html)
        for title, url, img in match:
                addon.add_directory({'mode': 'GetLinks13', 'url': url}, {'title':  title}, img= img.replace('//', 'http://'), fanart=FanartPath + 'fanart.png')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))


##------------------------------------------------------------- mega movie search-------------------------------------------------------------------------------------------##

def GetSearchQuery11():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]Search[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search11(query)
	else:
                return
def Search11(query):
    try:
        url = 'http://upbuzz.net/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="title"><a href="(.+?)" title="Permalink.+?">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR blue]...(upbuzz)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry upbuzz search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://www.bluraymovieswatchonline.com/search?q=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile("<h2 class='article_heading'>\s*?<a href='(.+?)' rel='bookmark' title='(.+?)free.+?'>.+?</a></h2>\s*?<div class='post_meta'>", re.DOTALL).findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR yellow]...(bluraymovies)[/COLOR]'}, img= 'http://komtv.org/wp-content/uploads/2015/08/lenta.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry bluraymovies search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://www.lotsmovies.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="featured-image">\s*?<a href="(.+?)" title="(.+?)"><img width=".+?" height=".+?" src="(.+?)" class="attachment-colormag-featured-image wp-post-image" alt=".+?" /></a>', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks99b', 'url': url}, {'title':  title + ' [COLOR aqua]...(lotsmovies)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry areaddl search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://www.solarmovie.ac/search/' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="afis">\s*?<a href="(.+?)" title="(.+?)"><img src="(.+?)" width=".+?" height=".+?" alt=".+?"/> </a><div class=".+?"></div>', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR darkorange]...(solarmovie)[/COLOR]'}, img=img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry solarmovie search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://300mbmovies4u.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="cover"><a href="(.+?)" title="(.+?)"><img src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR crimson]...(300mb movies4u)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry 300mbmovies4u search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://latestdude.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="item">\s*?<a href="(.+?)">\s*?<div class="image">\s*?<img src="(.+?)" alt="(.+?)"', re.DOTALL).findall(html)
        for url, img, title in match:
                addon.add_directory({'mode': 'GetLinks22', 'url': url}, {'title':  title + ' [COLOR yellow]...(latestdude)[/COLOR]'}, img=img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry perfecthdmovies is search down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://superseriale.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h1 class="entry-title">\s*?<a href="(.+?)" title=".+?">(.+?)</a>', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR powderblue]...(superseriale)[/COLOR]'}, img= 'http://komtv.org/wp-content/uploads/2015/08/lenta.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry superseriale search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://bear-movies.biz/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>', re.DOTALL).findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks18a', 'url': url}, {'title':  title + ' [COLOR sienna]...(bear-movies)[/COLOR]'}, img= 'http://komtv.org/wp-content/uploads/2015/08/lenta.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry bear-movies search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://world4ufree.com/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="cover"><a href="(.+?)" title="(.+?)"><img src="(.+?)" alt=.+? class=.+? width=.+? height=.+? /></a></div>', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR blue]...(world4ufree)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry world4ufree search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://www.vonlinemovies.com/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<a class="tc-grid-bg-link" href="(.+?)" title="(.+?)"></a><span', re.DOTALL).findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR lime]...(vonlinemovies)[/COLOR]'}, img= 'https://raw.githubusercontent.com/TheYid/yidpics/8333f2912d71cc7ddd71a7cee9714dfe263ee543/icons/nopic.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry vonlinemovies search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://cyberreel.com/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div id=".+?" class="item">\s*?<a href="(.+?)">\s*?<div class="image">\s*?<img src="(.+?)" alt="(.+?)" width=".+?" height=".+?" />\s*?<span class="player"></span>\s*?<span class="imdb"><b><b class="icon-star"></b></b>.+?</span>', re.DOTALL).findall(html)
        for url, img, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR lime]...(cyberreel)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry cyberreel search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))



##------------------------------------------------------------- mega tv search-------------------------------------------------------------------------------------------##

def GetSearchQuery12():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]Search[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search1',query)
                Search11(query)
	else:
                return
def Search12(query):
    try:
        url = 'http://tvdl.xyz/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="post-box-title">\s*?<a href="(.+?)">(.+?)</a>\s*?</h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR gold]...(tvdl)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry tvdl search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://upbuzz.net/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="title"><a href="(.+?)" title="Permalink.+?">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR pink]...(upbuzz)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry upbuzz search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://tvserieslog.in/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2><a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks132', 'url': url}, {'title':  title + ' [COLOR blue]...(tvserieslog)[/COLOR]'}, img= 'http://androidability.com/wp-content/uploads/2015/01/How-to-watch-movies-and-TV-shows-for-free-on-Android-androidability.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry tvserieslog is search down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://www.watchfreetvlinks.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<header class="entry-header">\s*?<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR aqua]...(wofs)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry watchonlinefreeseries search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://watchtvshow.org/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="title"><a href="(.+?)" title="Permalink to.+?">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR red]...(WTS)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry watchonlinefreeseries search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://watchitvideos.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('class="item-list"><h2 class="post-box-title"> <a\s*?href="(.+?)">(.+?)</a></h2><p.+?width="310" height="205" src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR brown]...(watchitvideos)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry watchitvideos search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://watchseriesus.tv/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="moviefilm">\s*?<a href="(.+?)">v<img src=".+?" alt="(.+?)" height=".+?" width=".+?" /></a>', re.DOTALL).findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR green]...(watchseriesus)[/COLOR]'}, img='', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry watchseriesus is search down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://free-download.link/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<a href="(.+?)" title="Permalink to .+?" rel="bookmark">(.+?)</a></h1>', re.DOTALL).findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title.replace('.', ' ') + ' [COLOR cornflowerblue]...(FDL)[/COLOR]'}, img= 'http://androidability.com/wp-content/uploads/2015/01/How-to-watch-movies-and-TV-shows-for-free-on-Android-androidability.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry FDL search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://superseriale.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h1 class="entry-title">\s*?<a href="(.+?)" title=".+?">(.+?)</a>', re.DOTALL).findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR powderblue]...(superseriale)[/COLOR]'}, img= 'http://komtv.org/wp-content/uploads/2015/08/lenta.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry superseriale search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://watchseries-onlines.ch/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<figure class="post-thumbnail">\s*?<a href="(.+?)">\s*?<img width="500" height="70" src="(.+?)" class="img-featured img-responsive wp-post-image" alt="(.+?)" />', re.DOTALL).findall(html)
        for url, img, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR red]...(watchseries-onlines)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry watchseries-onlines search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://300mbmovies4u.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="cover"><a href="(.+?)" title="(.+?)"><img src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR crimson]...(300mb movies4u)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry 300mbmovies4u search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://tvmuseum.freexblogs.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<header class="entry-header">\s*?<h1 class="entry-title"><a href="(.+?)" title="Permalink.+?" rel="bookmark">(.+?)</a></h1>', re.DOTALL).findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR green]...(tvmuseum)[/COLOR]'}, img= 'http://androidability.com/wp-content/uploads/2015/01/How-to-watch-movies-and-TV-shows-for-free-on-Android-androidability.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry tvmuseum search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://onlineseries.ucoz.com/search/?q=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="eTitle" style="text-align:left;font-weight:normal"><a href="(.+?)">(.+?)<b>(.+?)</b>(.+?)</a></div>', re.DOTALL).findall(html)
        for url, title, name, name1 in match:
                title= title.replace('<b>', '').replace('</b>', '')
                name= name.replace('<b>', '').replace('</b>', '')
                name1= name1.replace('<b>', '').replace('</b>', '')
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' ' + name + ' ' + name1 + ' [COLOR gold]...(onlineseries)[/COLOR]'}, img= 'http://androidability.com/wp-content/uploads/2015/01/How-to-watch-movies-and-TV-shows-for-free-on-Android-androidability.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry onlineseries search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


##.replace('/', ' ')## \s*? ##
###################################################################################### setViews ##########################################################################

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

##############################################################################################################################################################################

if mode == 'main': 
	MainMenu()
elif mode == 'HelpMenu':
        HelpMenu()
elif mode == 'GetTitles': 
	GetTitles(section, url, startPage, numOfPages)
elif mode == 'GetTitles1': 
	GetTitles1(section, url, startPage, numOfPages)
elif mode == 'GetTitles2': 
	GetTitles2(section, url, startPage, numOfPages)
elif mode == 'GetTitles2a': 
	GetTitles2a(query)
elif mode == 'GetTitles2b': 
	GetTitles2b(query)
elif mode == 'GetTitles3': 
	GetTitles3(section, url, startPage, numOfPages)
elif mode == 'GetTitles14': 
	GetTitles14(section, url, startPage, numOfPages)
elif mode == 'GetTitles16': 
	GetTitles16(section, url, startPage, numOfPages)
elif mode == 'GetTitles20': 
	GetTitles20(section, url, startPage, numOfPages)
elif mode == 'GetTitles21': 
	GetTitles21(section, url, startPage, numOfPages)
elif mode == 'GetTitles22': 
	GetTitles22(section, url, startPage, numOfPages)
elif mode == 'GetTitles23': 
	GetTitles23(section, url, startPage, numOfPages)
elif mode == 'GetTitles27': 
	GetTitles27(section, url, startPage, numOfPages)
elif mode == 'GetTitles27a': 
	GetTitles27a(section, url, startPage, numOfPages)
elif mode == 'GetTitles31': 
	GetTitles31(section, url, startPage, numOfPages)
elif mode == 'GetTitles31a': 
	GetTitles31a(section, url, startPage, numOfPages)
elif mode == 'GetTitles32': 
	GetTitles32(section, url, startPage, numOfPages)
elif mode == 'GetTitles32a': 
	GetTitles32a(section, url, startPage, numOfPages)
elif mode == 'GetTitles32b': 
	GetTitles32b(section, url, startPage, numOfPages)
elif mode == 'GetTitles34': 
	GetTitles34(section, url, startPage, numOfPages)
elif mode == 'GetTitles35': 
	GetTitles35(url)
elif mode == 'GetTitles35a': 
	GetTitles35a(url)
elif mode == 'GetTitles37': 
	GetTitles37(url)
elif mode == 'GetTitles39': 
	GetTitles39(section, url, startPage, numOfPages)
elif mode == 'GetTitles40': 
	GetTitles40(section, url, startPage, numOfPages)
elif mode == 'GetTitles42': 
	GetTitles42(section, url, startPage, numOfPages)
elif mode == 'GetTitles44': 
	GetTitles44(section, url, startPage, numOfPages)
elif mode == 'GetTitles48': 
	GetTitles48(section, url, startPage, numOfPages)
elif mode == 'GetTitles48a': 
	GetTitles48a(url)
elif mode == 'GetTitles49': 
	GetTitles49(query)
elif mode == 'GetTitles49a': 
	GetTitles49a(query)
elif mode == 'GetTitles50': 
	GetTitles50(section, url, startPage, numOfPages)
elif mode == 'GetTitles51': 
	GetTitles51(section, url, startPage, numOfPages)
elif mode == 'GetTitles52': 
	GetTitles52(section, url, startPage, numOfPages)
elif mode == 'GetTitles55': 
	GetTitles55(section, url, startPage, numOfPages)
elif mode == 'GetTitles57': 
	GetTitles57(section, url, startPage, numOfPages)
elif mode == 'GetTitles60': 
	GetTitles60(section, url, startPage, numOfPages)
elif mode == 'GetTitles62': 
	GetTitles62(query)
elif mode == 'GetTitles62a': 
	GetTitles62a(query)
elif mode == 'GetTitles64': 
	GetTitles64(section, url, startPage, numOfPages)
elif mode == 'GetTitles64a': 
	GetTitles64a(section, url, startPage, numOfPages)
elif mode == 'GetTitles64b': 
	GetTitles64b(section, url, startPage, numOfPages)
elif mode == 'GetTitles65': 
	GetTitles65(section, url, startPage, numOfPages)
elif mode == 'GetTitles66': 
	GetTitles66(section, url, startPage, numOfPages)
elif mode == 'GetTitles66a': 
	GetTitles66a(section, url, startPage, numOfPages)
elif mode == 'GetTitles65b': 
	GetTitles65b(url)
elif mode == 'GetTitles69': 
	GetTitles69(section, url, startPage, numOfPages)
elif mode == 'GetTitles70': 
	GetTitles70(section, url, startPage, numOfPages)
elif mode == 'GetTitles71': 
	GetTitles71(section, url, startPage, numOfPages)
elif mode == 'GetTitles76': 
	GetTitles76(section, url, startPage, numOfPages)
elif mode == 'GetTitles81': 
	GetTitles81(section, url, startPage, numOfPages)
elif mode == 'GetTitles811': 
	GetTitles811(section, url, startPage, numOfPages)
elif mode == 'GetTitles83': 
	GetTitles83(section, url, startPage, numOfPages)
elif mode == 'GetTitles83a': 
	GetTitles83a(section, url, startPage, numOfPages)
elif mode == 'GetTitles84': 
	GetTitles84(section, url, startPage, numOfPages)
elif mode == 'GetTitles85': 
	GetTitles85(section, url, startPage, numOfPages)
elif mode == 'GetTitles86': 
	GetTitles86(section, url, startPage, numOfPages)
elif mode == 'GetTitles87': 
	GetTitles87(section, url)
elif mode == 'GetTitles88': 
	GetTitles88(section, url)
elif mode == 'GetTitles89': 
	GetTitles89(section, url, startPage, numOfPages)
elif mode == 'GetTitles90': 
	GetTitles90(section, url, startPage, numOfPages)
elif mode == 'GetTitles91': 
	GetTitles91(section, url, startPage, numOfPages)
elif mode == 'GetTitles143': 
	GetTitles143(section, url)
elif mode == 'GetTitles143a': 
	GetTitles143a(query, section)
elif mode == 'GetTitles144': 
	GetTitles144(query, section)
elif mode == 'Categorieswco':
        Categorieswco(url)
elif mode == 'Categorieswoc':
        Categorieswoc(url)
elif mode == 'Categories':
        Categories(url)
elif mode == 'Categories1':
        Categories1(url)
elif mode == 'Categories2':
        Categories2(url)
elif mode == 'Categoriesuwf':
        Categoriesuwf(url)
elif mode == 'GetLinks':
	GetLinks(section, url)
elif mode == 'GetLinks1':
	GetLinks1(section, url)
elif mode == 'GetLinks1a':
	GetLinks1a(section, url)
elif mode == 'GetLinks1b':
	GetLinks1b(section, url)
elif mode == 'GetLinks1c':
	GetLinks1c(section, url)
elif mode == 'GetLinks1d':
	GetLinks1d(section, url)
elif mode == 'GetLinks1e':
	GetLinks1e(section, url)
elif mode == 'GetLinks5':
	GetLinks5(section, url)
elif mode == 'GetLinks7':
	GetLinks7(section, url)
elif mode == 'GetLinks8':
	GetLinks8(section, url)
elif mode == 'GetLinks9':
	GetLinks9(url)
elif mode == 'GetLinks9a':
	GetLinks9a(url)
elif mode == 'GetLinks10':
	GetLinks10(section, url)
elif mode == 'GetLinks11':
	GetLinks11(section, url)
elif mode == 'GetLinks12':
	GetLinks12(section, url)
elif mode == 'GetLinks12a':
	GetLinks12a(section, url)
elif mode == 'GetLinks13':
	GetLinks13(section, url)
elif mode == 'GetLinks14':
	GetLinks14(section, url)
elif mode == 'GetLinks16':
	GetLinks16(section, url)
elif mode == 'GetLinks17':
	GetLinks17(section, url)
elif mode == 'GetLinks18':
	GetLinks18(section, url)
elif mode == 'GetLinks18a':
	GetLinks18a(section, url)
elif mode == 'GetLinks19':
	GetLinks19(section, url)
elif mode == 'GetLinks20':
	GetLinks20(section, url)
elif mode == 'GetLinks21':
	GetLinks21(section, url)
elif mode == 'GetLinks21a':
	GetLinks21a(section, url)
elif mode == 'GetLinks21B':
	GetLinks21B(section, url)
elif mode == 'GetLinks22':
	GetLinks22(section, url)
elif mode == 'GetLinks23':
	GetLinks23(section, url)
elif mode == 'GetLinks66':
	GetLinks66(section, url)
elif mode == 'GetLinks99':
	GetLinks99(section, url)
elif mode == 'GetLinks99a':
	GetLinks99a(section, url)
elif mode == 'GetLinks55':
	GetLinks55(section, url)
elif mode == 'GetLinks55a':
	GetLinks55a(section, url)
elif mode == 'GetLinks81':
	GetLinks81(section, url)
elif mode == 'GetLinks811':
	GetLinks811(section, url)
elif mode == 'GetLinks129':
        GetLinks129(section, url)
elif mode == 'GetLinks130':
        GetLinks130(section, url)
elif mode == 'GetLinks130a':
        GetLinks130a(section, url)
elif mode == 'GetLinks131':
        GetLinks131(section, url)
elif mode == 'GetLinks132':
        GetLinks132(section, url)
elif mode == 'GetLinks133':
        GetLinks133(section, url)
elif mode == 'GetLinks99b':
	GetLinks99b(section, url)
elif mode == 'GetLinks75':
	GetLinks75(section, url)
elif mode == 'GetLinks145':
	GetLinks145(section, url, text)
elif mode == 'GetSearchQuery9':
	GetSearchQuery9()
elif mode == 'Search9':
	Search9(query)
elif mode == 'GetSearchQuery5':
	GetSearchQuery5()
elif mode == 'Search5':
	Search5(query)
elif mode == 'GetSearchQuery11':
	GetSearchQuery11()
elif mode == 'Search11':
	Search11(query)
elif mode == 'GetSearchQuery12':
	GetSearchQuery12()
elif mode == 'Search12':
	Search12(query)
elif mode == 'GetSearchQuery14':
	GetSearchQuery14()
elif mode == 'Search14':
	Search14(query)
elif mode == 'GetSearchQuery':
	GetSearchQuery()
elif mode == 'Search':
	Search(query)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)
elif mode == 'PlayVideo1':
	PlayVideo1(url, listitem)	
elif mode == 'PlayVideo2':
	PlayVideo2(url, listitem)
elif mode == 'PlayVideo4':
	PlayVideo4(url, listitem)	
elif mode == 'PlayVideo5':
	PlayVideo5(url, listitem)
elif mode == 'ResolverSettings':
        urlresolver.display_settings()
elif mode == 'SearchMenu':
        SearchMenu()
elif mode == 'ShowMenu':
        ShowMenu(urlurl)
elif mode == 'MovieMenu':
        MovieMenu()
elif mode == 'DocMenu':
        DocMenu()
elif mode == 'KidsMenu':
        KidsMenu()
elif mode == 'TvMenu':
        TvMenu()
elif mode == 'MusicMenu':
        MusicMenu()
elif mode == 'WtMenu':
        WtMenu()
elif mode == 'RgMenu':
        RgMenu()
elif mode == 'OmpMenu':
        OmpMenu()
elif mode == 'SportMenu':
        SportMenu()
elif mode == 'OmpazMenu':
        OmpazMenu()
elif mode == 'RadioMenu':
        RadioMenu()
elif mode == 'TvsMenu':
        TvsMenu()
elif mode == 'Tvs1Menu':
        Tvs1Menu()
elif mode == 'HqMenu':
        HqMenu()
elif mode == 'Hq4Menu':
        Hq4Menu()
elif mode == 'Hq5Menu':
        Hq5Menu()
elif mode == 'Hq6Menu':
        Hq6Menu()
elif mode == 'Hq7Menu':
        Hq7Menu()
elif mode == 'LiveMenu':
        LiveMenu()
elif mode == 'Help':
    import helpbox
    helpbox.HelpBox()


xbmcplugin.endOfDirectory(int(sys.argv[1]))