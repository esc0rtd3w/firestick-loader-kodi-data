import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import re, string, sys, os
import urlresolver
from TheYid.common.addon import Addon
from TheYid.common.net import Net
import HTMLParser
addon_id = 'plugin.video.theyidrh'
plugin = xbmcaddon.Addon(id=addon_id)
net = Net()
addon = Addon('plugin.video.theyidrh', sys.argv)
DB = os.path.join(xbmc.translatePath("special://database"), 'theyidrh.db')

########### url's ##########

BASE_URL2 = 'https://ganool.se/'
BASE_URL3 = 'http://crazyhdsource.com/'
BASE_URL5 = 'http://www.300mbcounter.com/'
BASE_URL6 = 'http://www.rlsarchive.com/'
BASE_URL7 = 'http://tddl.tv/'
BASE_URL8 = 'http://sceper.ws/'
BASE_URL9 = 'http://rlsscn.in/'
BASE_URL10 = 'http://www.ddlvalley.cool/'
BASE_URL11 = 'http://rlsbb.ru/'
BASE_URL15 = 'http://www.fullmatches.net/'
BASE_URL22 = 'https://rapidmoviez.unblocked.vc/'
BASE_URL46 = 'http://www.warezmovies.info'#
BASE_URL21 = 'http://www.moviefone.com/'#
BASE_URL24 = 'http://dx-tv.com/'
BASE_URL27 = 'https://raw.githubusercontent.com/TheYid/yidpics/master'
BASE_URL28 = 'http://www.movie.huborama.com/'#
BASE_URL29 = 'http://www.israbox.net/'#
BASE_URL30 = 'https://scnlog.me/'
BASE_URL42 = 'http://www.rls-dl.com/'#
BASE_URL44 = 'http://fanstash.la/'#
BASE_URL45 = 'http://scene-rls.net'
BASE_URL47 = 'http://rlslog.fr/'#
BASE_URL48 = 'http://www.coolxvid.net/'#
BASE_URL50 = 'http://www.rlshd.net'#
BASE_URL52 = 'http://www.movieinsider.com/'#
BASE_URL45 = 'http://scene-rls.net'
BASE_URL48 = 'http://ciceksoyle.net/'
BASE_URL54 = 'http://uksoapshare.blogspot.co.uk/'
BASE_URL56 = 'http://back2back2back.weebly.com'
BASE_URL57 = 'http://veverel.net/'
BASE_URL58 = 'http://scenesource.unblockmy.link/'
BASE_URL60 = 'http://iconvid.co/'#
BASE_URL61 = 'http://to.newmyvideolink.xyz/'
BASE_URL61a = 'http://www.ganool.li/'#
BASE_URL62 = 'http://scenetorrents.download/'#
BASE_URL66 = 'http://www.seriescoco.me'#
BASE_URL67 = 'http://tvshows-hdtv.org'#
BASE_URL72 = 'http://watchseries-online.pw/'#
BASE_URL78 = 'https://watchseries-online.be/'
BASE_URL79 = 'http://ganoolmovies.club/'
BASE_URL80 = 'http://www.gamesmovies.download/'
BASE_URL81 = 'http://to.newmyvideolink.xyz/'
BASE_URL82 = 'http://www.moviedb.cf/'#
BASE_URL84 = 'http://www.rlshd.net'#
BASE_URL85 = 'http://increasefree.com/'#
BASE_URL86 = 'http://www.scnsrc.me/'
BASE_URL87 = 'https://onlineseries.ucoz.com'
BASE_URL88 = 'http://tv-release.pw/'#
BASE_URL89 = 'http://born2dld.com/'#
#BASE_URL90 = 'http://rapidmoviez.eu/'#
BASE_URL90 = 'http://rmz.cr/'
BASE_URL91 = 'https://watchtv-online.pw/'
BASE_URL59 = 'http://sircogestion.com/'#
BASE_URL92 = 'http://wrelease.nl/'#
BASE_URL93 = 'https://seriescr.com/'#
BASE_URL94 = 'http://www.vidzio.net/'
BASE_URL95 = 'http://tvhoster.net/'#
BASE_URL73 = 'http://warez-cc.forumegypt.net/'#
BASE_URL75 = 'http://oneclickwatch.ws/'#
BASE_URL76 = 'http://wrzcraft.net/'
BASE_URL77 = 'http://www.bluray4.me/'#
BASE_URL96 = 'http://300mb.cc/'
BASE_URL97 = 'http://warez-cc.forumegypt.net/'
BASE_URL98 = 'http://allwrestling.in/'
BASE_URL99 = 'https://www.zippymoviez.bid'
BASE_URL100 = 'http://motdtv.blogspot.co.uk/'
BASE_URL101 = 'http://www.matchhighlight.com/'
BASE_URL102 = ''

BASE_URL1 = addon.get_setting('custurl')
if not BASE_URL1.endswith("/"):
    BASE_URL1 = BASE_URL1 + "/"

###### PATHS #########
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
section = addon.queries.get('section', None)
img = addon.queries.get('img', None)
text = addon.queries.get('text', None)
name = addon.queries.get('name', None)

#---------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------#


def GetTitles102(section, url, name, img, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'name': name, 'img': img, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles102', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#---------------------------------------------------------------------- newmyvideolin ----------------------------------------------------------------------------------------------#

def GetTitles81(section, url, startPage= '1', numOfPages= '1'):  
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
                match = re.compile('''<h2 class="post-title"><a href="(.+?)" rel="bookmark" title="(.+?)">.+?</a></h2>.+? class='alignleft nobottom' src='(.+?)' alt''', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl + '2'}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles81', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#----------------------------------------------------------------------------------onlineseries XLtv----------------------------------------------------------------------------------------------#

def GetTitles87(section, url, name, startPage= '1', numOfPages= '1'): #tv
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
                match = re.compile('<div class="eTitle" style="text-align:left;"><a href="(.+?)">(.+?)</a></div>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinksd', 'section': section, 'name': name.replace('.', ' '), 'img': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/No_image_available_600_x_450.svg/600px-No_image_available_600_x_450.svg.png', 'url': 'https://onlineseries.ucoz.com' + movieUrl}, {'title':  name.strip().replace('.', ' ')}, contextmenu_items= cm, img= 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/No_image_available_600_x_450.svg/600px-No_image_available_600_x_450.svg.png', fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles87', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles87a(section, url, name, img, startPage= '1', numOfPages= '1'): #movies
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
                match = re.compile('<div class="eTitle" style="text-align:left;"><a href="(.+?)">(.+?)</a></div>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinksd', 'section': section, 'name': name.replace('.', ' '), 'img': img, 'url': 'https://onlineseries.ucoz.com' + movieUrl}, {'title':  name.strip().replace('.', ' ')}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles87a', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks87b(section, url, name, img):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('''<source src="(.+?)" type='.+?'>''').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                addon.add_directory({'mode': 'PlayVideo2', 'url': url, 'name': name, 'img': img, 'listitem': listitem}, {'title': '[COLOR blue][B]GetLink : [/B][/COLOR]' + name}, img= img, fanart= 'http://hatterkep.eu/wallpapers/16/img-4606.jpg')
        setView('tvshows', 'calendar-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#-------------------------------------------------------------------------------- motdtv.blogspot ------------------------------------------------------------------------------------------------#

def GetTitles100(section, url):
    try:
        pageUrl = url    
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html                
        match = re.compile('''<h3 class='post-title entry-title' itemprop='name'>\s*?<a href='(.+?)'>(.+?)</a>\s*?</h3>.+? src="(.+?)"''', re.DOTALL).findall(html)
        match1 = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link' title='Older Posts'>Older Posts</a>", re.DOTALL).findall(html)
        for movieUrl, name, img in match:
                addon.add_directory({'mode': 'GetLinks100', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')
        for movieUrl in match1:
                addon.add_directory({'mode': 'GetTitles100', 'section': section, 'url': movieUrl}, {'title':  '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')      
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks100(section, url): 
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="(.+?)"').findall(content)
        match2 = re.compile("href='(.+?)'").findall(content)
        match3 = re.compile('''<span style=".+?"><b>(.+?)</b></span></div>\s*?<div style=".+?">\s*?<div style=".+?">\s*?<div style=".+?">\s*?<div style=".+?">\s*?<span style=".+?"><b><br /></b></span></div>\s*?</div>\s*?</div>\s*?</div>\s*?<div>\s*?<div style=".+?">\s*?<span style=".+?"><iframe allowfullscreen="" frameborder="0" height="360" src="(.+?)"''').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match2:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('\.rar[(?:\.html|\.htm)]*|mega.nz', url, re.IGNORECASE)
                if r:
                        continue

                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        #url = url.replace('/embed', '/f')
                        title = title.replace('1st','[COLOR coral][B]1st HALF[/B][/COLOR]')
                        title = title.replace('2nd','[COLOR coral][B]2nd HALF[/B][/COLOR]')
                        title = title.replace('fullmatches net','')
                        title = title.replace('.',' ')
                        title = title.replace('480p','[COLOR coral][B][I]480p[/B][/I][/COLOR]')
                        title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                        title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                        title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                        title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                        title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        for name, url in match3:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('\.rar[(?:\.html|\.htm)]*|mega.nz', url, re.IGNORECASE)
                if r:
                        continue

                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        #url = url.replace('/embed', '/f')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + name }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- matchhighlight ----------------------------------------------------------------------------------------------#

def GetTitles101(section, url, startPage= '1', numOfPages= '1'):  
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/page/' + startPage
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/page/' + str(page)
                        html = net.http_GET(pageUrl).content
                match = re.compile('<div class="entry-thumbnail thumbnail-landscape">\s*?<a href="(.+?)" title="(.+?)" >.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks101', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles101', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks101(section, url): 
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('''<span class='postTabs_titles'><b>(.+?)</b></span></p>\s*?<p><iframe src="(.+?)" scrolling="no" frameborder="0" width="640" height="360" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe></p>\s*?<p>(.+?)</p>''').findall(content)
        match1 = re.compile('''<span class='postTabs_titles'><b>(.+?)</b></span></p>\s*?<p><iframe width="640" height="360" src="(.+?)" frameborder="0" allowfullscreen></iframe></p>\s*?<p>(.+?)</p>''').findall(content)
        listitem = GetMediaInfo(content)
        for name, url, name1 in match + match1:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
                        continue

                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        url = url.replace('//', 'https://')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + name + ' [COLOR blue]:[/COLOR] ' + name1 }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------zippymoviez----------------------------------------------------------------------------------------------#

def GetTitles99(section, url, startPage= '1', numOfPages= '1'):
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
                match = re.compile("<span class='ipsType_break ipsContained'>\s*?<a href='(.+?)' class='' title='(.+?)'  data-ipsHover data-ipsHover-target='.+?' data-ipsHover-timeout='.+?'>", re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks99', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= 'https://www.zippymoviez.bid/uploads/monthly_2017_12/2017-happy-new-year-wishes-cover-photo.png.f920fac8769fecbf8ca37a6d23b8c01c.png', fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles99', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks99(section, url): 
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('>(.+?)<br').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
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
        setView('tvshows', 'calendar-view')
    except:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------allwrestling----------------------------------------------------------------------------------------------------#

def GetTitles98(section, url, startPage= '1', numOfPages= '1'):
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
                match = re.compile('data-medium-file=".+?" data-large-file="(.+?)" /></a>\s*?<h4 class="pt-cv-title"><a href="(.+?)" class="_self" target="_self" >(.+?)</a></h4>', re.DOTALL).findall(html)
                for img, movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('Watch', '')}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetSearchQuery22'},  {'title':  '[COLOR green]Search...[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')  
                #addon.add_directory({'mode': 'GetTitles98', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')  
   
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#----------------------------------------------------------------------------warez-cc----------------------------------------------------------------------------------------------------#

def GetTitles97(section, url, startPage= '1', numOfPages= '1'):
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
                match = re.compile('<h2 class="topic-title hierarchy"><a class="topictitle" href="(.+?)">(.+?)</a></h2>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks70', 'section': section, 'url': 'http://warez-cc.forumegypt.net/' + movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= 'http://i35.servimg.com/u/f35/11/49/63/09/logos10.png', fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles97', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')       
        setView('tvshows', 'calendar-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks70(section, url): 
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<dd><code>(.+?)</code></dd></dl><br').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        title = title.replace('.rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('sample', '[COLOR lime]Movie Trailer[/COLOR]')
                        title = title.replace('www.', '')
                        title = title.replace ('-',' ')
                        title = title.replace('_',' ')
                        title = title.replace('.',' ')
                        title = title.replace('480p','[COLOR coral][B][I]480p[/B][/I][/COLOR]')
                        title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                        title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                        title = title.replace('1080i','[COLOR orange][B][I]1080i[/B][/I][/COLOR]')
                        title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                        title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                        title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------300mb----------------------------------------------------------------------------------------------------#

def GetTitles96(section, url, startPage= '1', numOfPages= '1'):
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
                match = re.compile('<div class="home_post_box">\s*?<a href="(.+?)"> <img src="(.+?)" title="Direct (.+?)" width="225" height="200" />', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('Download', '').replace('Free ', ' ').replace('Watch Online', '').replace('Watch Online Free', '').replace('Free Download', ' ')}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                if 'next' not in html:
                        break

        if 'next' in html:
                addon.add_directory({'mode': 'GetTitles96', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')  
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------ganool----------------------------------------------------------------------------------------------------#

def GetTitles2(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<div class="movimgbox.+?">\s*?<a href="(.+?)" class="ml-mask"><img src="(.+?)" class="img-responsive homethumb" />\s*?<span class="mli-info"><h2>(.+?)</h2></span>', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles2', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetSearchQuery19'},  {'title':  '[COLOR green]Search...[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')    
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#----------------------------------------------------------------------------rlsscn----------------------------------------------------------------------------------------------------#

def GetTitles6(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<h2 class="title">\s*?<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>.+?src=".+?" data-lazy-type="image" data-lazy-src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles6', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------- scnlog ----------------------------------------------------------------------------------------------------#

def GetTitles30(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('alt="" src=".+?" title="" /><a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h1>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip().replace('.', ' '))
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('.', ' ')}, contextmenu_items= cm, img= 'https://scnlog.me/wp-content/themes/scnlog/images/favicon/apple-touch-icon.png', fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles30', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------300mbcounter----------------------------------------------------------------------------------------------#

def GetTitles5(section, url, startPage= '1', numOfPages= '1'): #tv
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
                match = re.compile('<h2 class="title"><a href=".+?" title=".+?">(.+?)</a></h2>\s*?<div class="post-info-top">\s*?<span class="post-info-date">\s*?.+?<a href=".+?" title=".+?" rel="author">.+?</a>\s*?.+?<a href=".+?" title=".+?" rel="bookmark">.+?</a>\s*?</span>\s*?<span class="gotocomments"><a href="(.+?)">.+?</a></span>\s*?</div>\s*?<div class="clear"></div>\s*?<div class="entry">\s*?<p><img class="aligncenter" src="(.+?)" alt=".+?" width=".+?"', re.DOTALL).findall(html)
                for name, movieUrl, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace ('Movie Free Download',' ').replace ('Movie Download',' ').replace ('Free Download',' ').replace ('Full English Movie Download',' ')}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                if 'next' not in html:
                        break

        if 'next' in html:
                addon.add_directory({'mode': 'GetTitles96', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')  
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-----------------------------------------------------------------------------------ciceksoyle---------------------------------------------------------------------------------------------#

def GetTitles48(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<h2.+?href="(.+?)">(.+?)<.+?src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks69', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                if 'next' not in html:
                        break

        if 'next' in html:
                addon.add_directory({'mode': 'GetTitles48', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')         
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks69(section, url): 
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('rel="nofollow">(.+?)</a>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('facebook.com|plus.google.com|\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
                        continue

                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        title = title.replace('.rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('sample', '[COLOR lime]Movie Trailer[/COLOR]')
                        title = title.replace('www.', '')
                        title = title.replace ('-',' ')
                        title = title.replace('_',' ')
                        title = title.replace('.',' ')
                        title = title.replace('480p','[COLOR coral][B][I]480p[/B][/I][/COLOR]')
                        title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                        title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                        title = title.replace('1080i','[COLOR orange][B][I]1080i[/B][/I][/COLOR]')
                        title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                        title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                        title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------- rapidmoviez.unblocked ----------------------------------------------------------------------------------------------------#

def GetTitles22(section, url, startPage= '1', numOfPages= '1'): 
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content                    
                match = re.compile('<h3><a style="text-decoration:none;" href="(.+?)">(.+?)</a><br /><span', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip().replace('.', ' '))
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks68', 'section': section, 'url': 'https://rapidmoviez.unblocked.vc/' + movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= 'http://rmz.cr/files/img/rmzlogo_christmas.jpg', fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles22', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('tvshows', 'calendar-view') 
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks68(section, url): 
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<pre class="links" id=".+?">(.+?)</pre>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        title = title.replace('.rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('sample', '[COLOR lime]Movie Trailer[/COLOR]')
                        title = title.replace('www.', '')
                        title = title.replace ('-',' ')
                        title = title.replace('_',' ')
                        title = title.replace('.',' ')
                        title = title.replace('480p','[COLOR coral][B][I]480p[/B][/I][/COLOR]')
                        title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                        title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                        title = title.replace('1080i','[COLOR orange][B][I]1080i[/B][/I][/COLOR]')
                        title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                        title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                        title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#---------------------------------------------------------------------- rlsbb back up ----------------------------------------------------------------------------------------------#

def GetTitles80(section, url, startPage= '1', numOfPages= '1'):  
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
                match = re.compile('<h2 class="entry-title" itemprop="headline"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>.+?src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles80', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#---------------------------------------------------------------------- watchseries-online ----------------------------------------------------------------------------------------------#

def GetTitles78(section, url, startPage= '1', numOfPages= '1'):  
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/page/' + startPage
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/page/' + str(page)
                        html = net.http_GET(pageUrl).content
                match = re.compile('<h3><a class="single_title" href="(.+?)" title=".+?">(.+?)</a></h3>.+?src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= 'https://watchseries-online.be/' + img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles78', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- watchtv ----------------------------------------------------------------------------------------------#

def GetTitles91(section, url, startPage= '1', numOfPages= '1'):  
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/page/' + startPage
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/page/' + str(page)
                        html = net.http_GET(pageUrl).content
                match = re.compile('<div class="boxentry">\s*?<a href="(.+?)" title="(.+?)">\s*?<div class="harvendra">\s*?<img src="(.+?)" alt=".+?" />', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= 'https://watchtv-online.pw' + img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles91', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- Watch TV Series 4U ----------------------------------------------------------------------------------------------#

def GetTitles59(section, url, startPage= '1', numOfPages= '1'):  
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
                match = re.compile('<div class="moviefilm">\s*?<a href="(.+?)">\s*?<img src="(.+?)" alt="(.+?)" height="150px" width="115px" /></a>', re.DOTALL).findall(html)
                for movieUrl, img, name in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('.', ' ')}, img= img.replace('/wp-content/themes/Tuan123456/images/no-thumbnail.png', 'http://www.rajnathsingh.in/wp-content/uploads/2016/09/noImg.png'), fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles59', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------rlshd/scenehdtv----------------------------------------------------------------------------------------------#

def GetTitles84(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<h1 class="entry-title">\s*?<a href="(.+?)" rel="bookmark">(.+?)</a>\s*?</h1>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': 'https://www.rlshd.net' + movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles84', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------vidzio----------------------------------------------------------------------------------------------#

def GetTitles94(section, url, startPage= '1', numOfPages= '1'): #tv
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
                match = re.compile('class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= 'http://vidzio.com/wp-content/uploads/2016/06/vidzio-square-300x300.png', fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles94', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- increasefree ----------------------------------------------------------------------------------------------#

def GetTitles85a(section, url, startPage= '1', numOfPages= '1'):  
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
                match = re.compile('<h3 class="stitle"><a href="(.+?)">(.+?)</a></h3>.+?src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles85a', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#-------------------------------------------------------------------------------- rlsarchive ------------------------------------------------------------------------------------------------#

def GetTitles4(section, url, startPage= '1', numOfPages= '1'):
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
                match = re.compile('<h2 class="post-box-title">\s*?<a href="(.+?)">(.+?)</a>\s*?</h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles4', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')       
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def GetTitles56(img, section, url): #primelinks
    try:
        pageUrl = url
        print pageUrl
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<h2 class="blog-title">\s*?<a class="blog-title-link blog-link" href="//(.+?)">(.+?)</a>.+? src="/uploads/(.+?)"', re.DOTALL).findall(html)
        match1 = re.compile('<div class="blog-page-nav-previous">\s*?<a href="/layout(.+?)" class="blog-link">&lt;&lt;Previous</a>', re.DOTALL).findall(html)
        for movieUrl, name, img in match:
                addon.add_directory({'mode': 'GetLinks14', 'section': section, 'url': 'http://' + movieUrl, 'img': 'http://back2back2back.weebly.com/uploads/' + img}, {'title':  name.strip()}, img= 'http://back2back2back.weebly.com/uploads/' + img, fanart=FanartPath + 'fanart.png') 
        for movieUrl in match1:
                addon.add_directory({'mode': 'GetTitles56', 'section': section, 'url': 'http://back2back2back.weebly.com/layout' + movieUrl}, {'title':  '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')     
        setView('tvshows', 'tvshows-view')        
    except:  

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles56a(img, section, url): #spoteone
    try:
        pageUrl = url
        print pageUrl
        html = net.http_GET(pageUrl).content                     
        match = re.compile('<h2 class="blog-title">\s*?<a class="blog-title-link blog-link" href="//(.+?)">(.+?)</a>.+? src="/uploads/(.+?)"', re.DOTALL).findall(html)
        match1 = re.compile('<div class="blog-page-nav-previous">\s*?<a href="/layout(.+?)" class="blog-link">&lt;&lt;Previous</a>', re.DOTALL).findall(html)
        for movieUrl, name, img in match:
                addon.add_directory({'mode': 'GetLinks14', 'section': section, 'url': 'http://' + movieUrl, 'img': 'http://back2back2back.weebly.com/uploads/' + img}, {'title':  name.strip()}, img= 'http://back2back2back.weebly.com/uploads/' + img, fanart=FanartPath + 'fanart.png') 
        for movieUrl in match1:
                addon.add_directory({'mode': 'GetTitles56a', 'section': section, 'url': 'http://back2back2back.weebly.com/layout' + movieUrl}, {'title':  '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')           
        setView('Default', 'default-view')
    except:  

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks14(section, url): 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" target="_blank">.+?</a><br').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if 'Unknown' in host:
                                continue
                r = re.search('facebook.com|plus.google.com|\part1|\part2|\part3|\part4|\part5|\.rar|.html|\.file[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
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
        setView('tvshows', 'calendar-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))



#---------------------------------------------------------------------------------- dx-tv --------------------------------------------------------------------------------------#

def GetTitles24(section, url, startPage= '1', numOfPages= '1'): 
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '?paged=' + startPage + ''
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '?paged=' + startPage + ''
                        html = net.http_GET(pageUrl).content                         
                match = re.compile('<article class="latestPost excerpt ">\s*?<a href="(.+?)" title="(.+?)" rel="nofollow" id="featured-thumbnail">\s*?<div class="featured-thumbnail"><img width="280" height="172" src="(.+?)?resize=.+?"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search11&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks5', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('.', ' ').replace('Watch online', '').replace('Watch Online', '').replace('Download ', '').replace('/', '').replace('Watch', '')}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')    
                addon.add_directory({'mode': 'GetTitles24', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery23'},  {'title':  '[COLOR green]Search...[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- wrzcraft ----------------------------------------------------------------------------------------------#

def GetTitles76(section, url, startPage= '1', numOfPages= '1'):  #tv
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
                match = re.compile('<h2><a href="(.+?)" title=".+?">(.+?)</a></h2>.+? src="(.+?)\s*?"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles76', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles76a(section, url, startPage= '1', numOfPages= '1'):  #movies
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
                match = re.compile('<h2><a href="(.+?)" title=".+?">(.+?)</a></h2>.+? src="(.+?)\s*?"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles76a', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#----------------------------------------------------------------------2ddl----------------------------------------------------------------------------------------------#

def GetTitles33(section, url, startPage= '1', numOfPages= '1'):  
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
                match = re.compile('<h2><a href="(.+?)" title=".+?">(.+?)</a></h2>.+?<div align="center"><img src="(.+?)\s*?"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip().replace('.', ' '))
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('.', ' ')}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles33', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('Default', 'default-view')
    except:

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#---------------------------------------------------------------------- rmz ----------------------------------------------------------------------------------------------#

def GetTitles90(section, url, startPage= '1', numOfPages= '1'):  
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = url + '/' + startPage + '/'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = url + '/' + str(page) + '/'
                        html = net.http_GET(pageUrl).content
                match = re.compile('<h3><a style="text-decoration:none;" href="(.+?)">(.+?)<.+?.+? <img src="/releases/image/(.+?)"', re.DOTALL).findall(html)
                #match = re.compile('<div class="blog-img">\s*?<a href="(.+?)" target="_blank" class="poster" title="(.+?)">\s*?<img src="/releases/image/(.+?)" width="197" height="280" alt="The Block" longdesc="/i/0418372" />', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinksc', 'section': section, 'url': 'http://rmz.cr/' + movieUrl}, {'title':  name.strip()}, img= 'http://rmz.cr/releases/image/' + img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles90', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#---------------------------------------------------------------------------------ddlv-----------------------------------------------------------------------------------------------#

def GetTitles11(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<h2>.+?href="(.+?)".+?>(.+?)<.+?src="(.+?)".+?', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip().replace('.', ' '))
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks12', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('.', ' ')}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles11', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------tvshows-hdtv----------------------------------------------------------------------------------------------#
 
def GetLinks67(section, url):
    try: 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<b>(.+?)</b></center>.<br></span></td></tr><tr> \s*?<tr><td><center><a href="(https://openload.co/f/.+?)"').findall(content)
        match1 = re.compile('<b>(.+?)</b></center>.<br></span></td></tr><tr> \s*?<tr><td><center><a href=".+?" target="_blank"><img src=".+?" /></a> . <a href="(http://rg.to/.+?)"').findall(content)
        #match2 = re.compile('<b>(.+?)</b></center>.<br></span></td></tr><tr> \s*?<tr><td><center><a href=".+?" target="_blank"><img src="i/OP.png" /></a> . <a href=".+?" target="_blank"><img src="i/RG.png" \s*?/></a> . <a href="(http://uploading.site/.+?)" target="_blank"><img').findall(content)
        #match3 = re.compile('<b>(.+?)</b></center>.<br></span></td></tr><tr> \s*?<tr><td><center><a href=".+?" target="_blank"><img src="i/OP.png" /></a> . <a href=".+?" target="_blank"><img src="i/RG.png" \s*?/></a> . <a href=".+?" target="_blank"><img target="_blank"><img src="i/USITE.jpg" /></a> . <a href=".+?" target="_blank"><img src="i/UR.png" /></a> . <a \s*?href="(http://uploaded.net/file/.+?)" target="_blank"><img src="i/UL.jpg"/></a>').findall(content)
        listitem = GetMediaInfo(content)
        for name, url in match + match1:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url , 'listitem': listitem}, {'title': name.strip().replace('.', ' ')  + ' =  ' + host }, img=IconPath + 'th2.png' , fanart=FanartPath + 'fanart.png')
        for url in match2:
                addon.add_directory({'mode': 'GetLinks67', 'url': 'http://tvshows-hdtv.org/' + url, 'listitem': listitem}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('tvshows', 'calendar-view')
    except:

       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------scnsrc----------------------------------------------------------------------------------------------#

def GetTitles86(section, url, startPage= '1', numOfPages= '1'): #movies
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
                match = re.compile('<h2> <a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles86', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def GetTitles86a(section, url, startPage= '1', numOfPages= '1'): #tv
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
                match = re.compile('<h2> <a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img=IconPath + 'scenstv.png', fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles86a', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- mvl ----------------------------------------------------------------------------------------------#

def GetTitles61(section, url, startPage= '1', numOfPages= '1'):  
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
                match = re.compile('<div class="post_content">\s*?<a href="http://newmyvideolink.xyz/(.+?)/" rel="bookmark" title=".+?"> <img src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': 'http://newmyvideolink.xyz/' + movieUrl + '/'}, {'title':  movieUrl.replace('-', ' ')}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles61', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- veverel ----------------------------------------------------------------------------------------------#

def GetTitles57(section, url, startPage= '1', numOfPages= '1'):  
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
                match = re.compile('<h2 class="title"><a href="(.+?)">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles57', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------- soaps ----------------------------------------------------------------------------------------------#

def GetTitles54(section, url):  
    try:
        pageUrl = url
        print pageUrl
        html = net.http_GET(pageUrl).content
        match = re.compile("<a href='http://uksoapshare.blogspot.co.uk/search/label/(.+?)' rel='tag'>(.+?)</a>", re.DOTALL).findall(html)
        for movieUrl, name in match:
                addon.add_directory({'mode': 'GetTitles54a', 'section': section, 'url': 'http://uksoapshare.blogspot.co.uk/search/' + movieUrl}, {'title':  name.strip()}, img= '', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles54a(section, url):  
    try:
        pageUrl = url
        print pageUrl
        html = net.http_GET(pageUrl).content
        match = re.compile("<h3 class='post-title entry-title' itemprop='name'>\s*?<a href='(.+?)'>(.+?)</a>", re.DOTALL).findall(html)
        match1 = re.compile("<a class='blog-pager-older-link' href='(.+?)' id='Blog1_blog-pager-older-link' title='Older Posts'>(.+?)</a>", re.DOTALL).findall(html)
        for movieUrl, name in match:
                addon.add_directory({'mode': 'GetLinks54', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img= 'http://primetime.unrealitytv.co.uk/wp-content/uploads/2012/12/coronation-street-emmerdale-logos-460x459.jpg', fanart=FanartPath + 'fanart.png')
        for movieUrl, name in match1:
                addon.add_directory({'mode': 'GetTitles54a', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks54(section, url): 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" target=_blank>(.+?)</a><br />').findall(content)
        listitem = GetMediaInfo(content)
        for url, name in match:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' [COLOR gold]:[/COLOR] ' + title.replace('_',' ').replace('-',' ') + ' - ' + '[B][COLOR yellow]' + name.replace('_',' ').replace('-',' ') + '[/B][/COLOR]' }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-----------------------------------------------------------------------------------crazyhdsource---------------------------------------------------------------------------------------------#

def GetTitles3(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<h4><span>.+?href="(.+?)".+?>(.+?)<.+?src=.+? .+?="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles3', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue]Next...[/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-----------------------------------------------------------------------------------Sceper---------------------------------------------------------------------------------------------#

def GetTitles7(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<h2.+?href="(.+?)">(.+?)<.+?src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                if 'next' not in html:
                        break

        if 'next' in html:
                addon.add_directory({'mode': 'GetTitles7', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png') 
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#--------------------------------------------------------------------------------rlsbb------------------------------------------------------------------------------------------------#

def GetTitles12(section, url, startPage= '1', numOfPages= '1'): 
    try:
        print 'releaseBB get Movie Titles Menu %s' % url
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
                match = re.compile('postHeader.+?href="(.+?)".+?>(.+?)<.+?src=.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip())
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip()}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                if 'Older Entries' not in html:
                        break

        if 'Older Entries' in html:
                addon.add_directory({'mode': 'GetTitles12', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#--------------------------------------------------------------------------------fullmatch------------------------------------------------------------------------------------------------#

def GetTitles16(section, url, startPage= '1', numOfPages= '1'): 
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
                match = re.compile('<h2><a.+?href="(.+?)".+?>(.+?)<.+?src=.+?.+?', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search12&query=%s)' %(name.strip().replace('Download', '').replace('Full', '').replace('Match', ''))
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('Download', '')}, contextmenu_items= cm, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles16', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------------- github -----------------------------------------------------------------------------------#

def GetTitles27(url):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<>title="(.+?)" href="(.+?)" />< src="(.+?)"').findall(content)
        for name, url, img in match:
                addon.add_directory({'mode': 'PlayVideo3', 'url': url, 'listitem': listitem}, {'title':  name.strip()}, img= img, fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo3(url, listitem):
    try:
        print 'in PlayVideo %s' % url
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^^^ Press back ^^^[/B] [/COLOR]'},'','')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Link may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")


#--------------------------------------------------------------------- scene-rls ----------------------------------------------------------------------------------------------#

def GetTitles45(section, url, startPage= '1', numOfPages= '1'):  
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
                match = re.compile('<h2 class="postTitle"><span></span><a href="(.+?)" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip().replace('.', ' '))
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks9', 'section': section, 'url': movieUrl.replace('(', '').replace(')', '')}, {'title':  name.strip().replace('.', ' ').replace('(', '').replace(')', '')}, contextmenu_items= cm, img= 'http://vignette3.wikia.nocookie.net/shokugekinosoma/images/6/60/No_Image_Available.png/revision/latest?cb=20150708082716', fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles45', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def GetTitles45a(section, url, startPage= '1', numOfPages= '1'):  #4k
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
                match = re.compile('<h2 class="postTitle"><span></span><a href="(.+?)" title=".+?">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip().replace('.', ' '))
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks9', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('.', ' ')}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles45a', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles45b(section, url, startPage= '1', numOfPages= '1'):  
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
                match = re.compile('<h2 class="postTitle"><span></span><a href="(.+?)" title=".+?">(.+?)</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, name, img in match:
                        cm  = []
                        runstring = 'XBMC.Container.Update(plugin://plugin.video.theyidrh/?mode=Search10&query=%s)' %(name.strip().replace('.', ' '))
        		cm.append(('[COLOR blue]R[/COLOR]elease Search', runstring))
                        addon.add_directory({'mode': 'GetLinks9', 'section': section, 'url': movieUrl}, {'title':  name.strip().replace('.', ' ')}, contextmenu_items= cm, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles45b', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")

def GetTitles45c(section, url, startPage= '1', numOfPages= '1'):  #4k
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
                match = re.compile('<h2 class="postTitle"><span></span><a href="http://scene-rls.net/(.+?)/" title=".+?">.+?</a></h2>.+? src="(.+?)"', re.DOTALL).findall(html)
                for movieUrl, img in match:
                        addon.add_directory({'mode': 'GetLinks9', 'section': section, 'url': 'http://scene-rls.net/' + movieUrl + '/'}, {'title':  movieUrl.replace('-', ' ')}, img= img, fanart=FanartPath + 'fanart.png')
                addon.add_directory({'mode': 'GetTitles45a', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('Default', 'default-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles45d(section, url, startPage= '1', numOfPages= '1'):  #tvpacksAZ
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
                match = re.compile('<li><a href="(.+?)"><span class="head">(.+?)</span></a></li>', re.DOTALL).findall(html)
                for movieUrl, name in match:
                        addon.add_directory({'mode': 'GetLinks9', 'section': section, 'url': movieUrl}, {'title':  name}, img= 'http://www.worktopfactoryy.co.uk/portals/22/images/fluff/Alphabet/A-Z%20icon%20grey%202.png', fanart=FanartPath + 'fanart.png')
                #addon.add_directory({'mode': 'GetTitles45d', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')        
        setView('tvshows', 'calendar-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#

def GetTitles45e(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = 'http://scene-rls.com/releases/index.php?p=' + startPage + '&cat=TV%20Shows'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = 'http://scene-rls.net/releases/index.php?p=' + str(page) + '&cat=TV%20Shows'
                        html = net.http_GET(pageUrl).content
                match = re.compile('<div class="p-c p-c-title"><h2><a target="_blank" class="p-title" href="(.+?)">(.+?)</a>(.+?)</h2>', re.DOTALL).findall(html)
                for movieUrl, name, name1 in match:
                        addon.add_directory({'mode': 'GetLinks9', 'section': section, 'url': movieUrl}, {'title':  name + ' ' + name1}, img=IconPath + 'srls22.png', fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles45e', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')   
        addon.add_directory({'mode': 'GetSearchQuery4'},  {'title':  '[COLOR green]Search...[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')     
        setView('tvshows', 'calendar-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles45f(section, url, startPage= '1', numOfPages= '1'):
    try:
        pageUrl = url
        if int(startPage)> 1:
                pageUrl = 'http://scene-rls.net/releases/index.php?p=' + startPage + '&cat=Movies'
        print pageUrl
        html = net.http_GET(pageUrl).content
        start = int(startPage)
        end = start + int(numOfPages)
        for page in range( start, end):
                if ( page != start):
                        pageUrl = 'http://scene-rls.net/releases/index.php?p=' + str(page) + '&cat=Movies'
                        html = net.http_GET(pageUrl).content
                match = re.compile('<div class="p-c p-c-title"><h2><a target="_blank" class="p-title" href="(.+?)">(.+?)</a>(.+?)</h2>', re.DOTALL).findall(html)
                for movieUrl, name, name1 in match:
                        addon.add_directory({'mode': 'GetLinks9', 'section': section, 'url': movieUrl}, {'title':  name + ' ' + name1}, img=IconPath + 'srls22.png', fanart=FanartPath + 'fanart.png') 
                addon.add_directory({'mode': 'GetTitles45f', 'url': url, 'startPage': str(end), 'numOfPages': numOfPages}, {'title': '[COLOR blue][B][I]Next page...[/B][/I][/COLOR]'}, img=IconPath + 'nextpage1.png', fanart=FanartPath + 'fanart.png')   
        setView('tvshows', 'calendar-view')     
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry site is down [/B][/COLOR],[COLOR blue][B]Please try a different site[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


##.replace('/', ' ')## \s*? ## 
#################################################################################getlinks###############################################################################################

def GetLinks(section, url): # Get Links
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        r = re.search('<strong>Links.*</strong>', html)
        if r:
                content = html[r.end():]

        r = re.search('commentblock', content)
        if r:
                content = content[:r.start()]
                
        match = re.compile('href="(.+?)"').findall(content)
        match1 = re.compile('target="_blank">(.+?)</a>').findall(content)
        match2 = re.compile("href='(.+?)'").findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1 + match2:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('facebook.com|plus.google.com|fonts.googleapis.com|nbc.com|tv.com|\.rar[(?:\.html|\.htm|\.file|\.srt)]*', url, re.IGNORECASE)
                if r:
                        continue

                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        title = title.replace('.rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('sample', '[COLOR lime]Movie Trailer[/COLOR]')
                        title = title.replace('www.', '')
                        title = title.replace ('-',' ')
                        title = title.replace('_',' ')
                        title = title.replace('.',' ')
                        title = title.replace('gaz','')
                        title = title.replace('NTb','')
                        title = title.replace('1st','[COLOR coral][B]1st HALF[/B][/COLOR]')
                        title = title.replace('2nd','[COLOR coral][B]2nd HALF[/B][/COLOR]')
                        title = title.replace('fullmatches net','')
                        title = title.replace('.',' ')
                        title = title.replace('480p','[COLOR coral][B][I]480p[/B][/I][/COLOR]')
                        title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                        title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                        title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                        title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                        title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                        title = title.replace('%20',' ')
                        host = host.replace('youtube.com','[COLOR lime]Movie Trailer[/COLOR]')
                        host = host.replace('k2s.cc','[COLOR red]Unsupported Link[/COLOR]')
                        host = host.replace('ryushare.com','[COLOR red]Unsupported Link[/COLOR]')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')

        find = re.search('commentblock', html)
        if find:
                print 'in comments if'
                html = html[find.end():]
                match = re.compile('<a href="(.+?)" rel="nofollow"', re.DOTALL).findall(html)
                print len(match)
                for url in match:
                        host = GetDomain(url)
                        if 'Unknown' in host:
                                continue
                        
                        # ignore .rar files
                        r = re.search('facebook.com|plus.google.com|\.rar[(?:\.html|\.htm|\.file|\.srt)]*', url, re.IGNORECASE)
                        if r:
                                continue
                        try:
                                if urlresolver.HostedMediaFile(url= url):
                                        print 'in GetLinks if loop'
                                        title = url.rpartition('/')
                                        title = title[2].replace('.html', '')
                                        title = title.replace('.htm', '')
                                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' : ' + title}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')

                        except:

                                continue

        setView('tvshows', 'calendar-view')
    except:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
#################################################################################getlinksD###############################################################################################

def GetLinksd(section, url, name, img): # Get Links
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        r = re.search('<strong>Links.*</strong>', html)
        if r:
                content = html[r.end():]

        r = re.search('commentblock', content)
        if r:
                content = content[:r.start()]
                
        match = re.compile('href="(.+?)"').findall(content)
        match1 = re.compile('target="_blank">(.+?)</a>').findall(content)
        match2 = re.compile("href='(.+?)'").findall(content)
        match3 = re.compile('<iframe src="(.+?)" scrolling="no" frameborder="0" width="700" height="430" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true"></iframe> <br /><br /> <a class="link" href=".+?"').findall(content)
        match4 = re.compile('rel="nofollow">(https://filebebo.com/d/.+?)</a>').findall(content)
        match5 = re.compile('<a href="(https://filebebo.com/d/.+?)">(.+?)</a>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match3 + match4:
                url = url.replace('/d/', '/e/')
                addon.add_directory({'mode': 'GetLinks87b', 'url': url, 'name': name, 'img': img, 'listitem': listitem}, {'title': 'filebebo.com [COLOR gold]: [/COLOR]' + name}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        for url, name in match5:
                url = url.replace('/d/', '/e/')
                addon.add_directory({'mode': 'GetLinks87b', 'url': url, 'name': name.replace('.', ' '), 'img': img, 'listitem': listitem}, {'title': 'filebebo.com [COLOR gold]: [/COLOR]' + name.replace('.', ' ')}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        for url in match + match1 + match2:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('facebook.com|plus.google.com|fonts.googleapis.com|nbc.com|tv.com|\.rar[(?:\.html|\.htm|\.file|\.srt)]*', url, re.IGNORECASE)
                if r:
                        continue

                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        title = title.replace('.rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('sample', '[COLOR lime]Movie Trailer[/COLOR]')
                        title = title.replace('www.', '')
                        title = title.replace ('-',' ')
                        title = title.replace('_',' ')
                        title = title.replace('.',' ')
                        title = title.replace('gaz','')
                        title = title.replace('NTb','')
                        title = title.replace('1st','[COLOR coral][B]1st HALF[/B][/COLOR]')
                        title = title.replace('2nd','[COLOR coral][B]2nd HALF[/B][/COLOR]')
                        title = title.replace('fullmatches net','')
                        title = title.replace('.',' ')
                        title = title.replace('480p','[COLOR coral][B][I]480p[/B][/I][/COLOR]')
                        title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                        title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                        title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                        title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                        title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                        title = title.replace('%20',' ')
                        host = host.replace('youtube.com','[COLOR lime]Movie Trailer[/COLOR]')
                        host = host.replace('k2s.cc','[COLOR red]Unsupported Link[/COLOR]')
                        host = host.replace('ryushare.com','[COLOR red]Unsupported Link[/COLOR]')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')

        find = re.search('commentblock', html)
        if find:
                print 'in comments if'
                html = html[find.end():]
                match = re.compile('<a href="(.+?)" rel="nofollow"', re.DOTALL).findall(html)
                print len(match)
                for url in match:
                        host = GetDomain(url)
                        if 'Unknown' in host:
                                continue
                        
                        # ignore .rar files
                        r = re.search('facebook.com|plus.google.com|\.rar[(?:\.html|\.htm|\.file|\.srt)]*', url, re.IGNORECASE)
                        if r:
                                continue
                        try:
                                if urlresolver.HostedMediaFile(url= url):
                                        print 'in GetLinks if loop'
                                        title = url.rpartition('/')
                                        title = title[2].replace('.html', '')
                                        title = title.replace('.htm', '')
                                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' : ' + title}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')

                        except:

                                continue

        setView('tvshows', 'calendar-view')
    except:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#################################################################################getlinksB###############################################################################################

def GetLinksb(section, url): # Get Links
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        r = re.search('<strong>Links.*</strong>', html)
        if r:
                content = html[r.end():]

        r = re.search('commentblock', content)
        if r:
                content = content[:r.start()]
                
        match = re.compile('rel="nofollow">(.+?)</a></p><p><a').findall(content)
        match1 = re.compile('class="external">(.+?)</a>', re.DOTALL).findall(html)
        match2 = re.compile('<br />(.+?)</p>', re.DOTALL).findall(html)
        listitem = GetMediaInfo(content)
        for url in match + match1 + match2:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('facebook.com|plus.google.com|\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
                        continue

                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        title = title.replace('.rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('sample', '[COLOR lime]Movie Trailer[/COLOR]')
                        title = title.replace('www.', '')
                        title = title.replace ('-',' ')
                        title = title.replace('_',' ')
                        title = title.replace('.',' ')
                        title = title.replace('gaz','')
                        title = title.replace('NTb','')
                        title = title.replace('1st','[COLOR coral][B]1st HALF[/B][/COLOR]')
                        title = title.replace('2nd','[COLOR coral][B]2nd HALF[/B][/COLOR]')
                        title = title.replace('fullmatches net','')
                        title = title.replace('.',' ')
                        title = title.replace('480p','[COLOR coral][B][I]480p[/B][/I][/COLOR]')
                        title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                        title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                        title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                        title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                        title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                        title = title.replace('%20',' ')
                        host = host.replace('youtube.com','[COLOR lime]Movie Trailer[/COLOR]')
                        host = host.replace('k2s.cc','[COLOR red]Unsupported Link[/COLOR]')
                        host = host.replace('ryushare.com','[COLOR red]Unsupported Link[/COLOR]')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')

        find = re.search('commentblock', html)
        if find:
                print 'in comments if'
                html = html[find.end():]
                match = re.compile('class="external">(.+?)</a>', re.DOTALL).findall(html)
                print len(match)
                for url in match:
                        host = GetDomain(url)
                        if 'Unknown' in host:
                                continue
                        
                        # ignore .rar files
                        r = re.search('facebook.com|plus.google.com|\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                        if r:
                                continue
                        try:
                                if urlresolver.HostedMediaFile(url= url):
                                        print 'in GetLinks if loop'
                                        title = url.rpartition('/')
                                        title = title[2].replace('.html', '')
                                        title = title.replace('.htm', '')
                                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' : ' + title}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')

                        except:

                                continue

        setView('tvshows', 'calendar-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------------ddlvalley-------------------------------------------------------------------------------------------------#

def GetLinks3(section, url): 
    try:
        html = net.http_GET(str(url)).content
        sources = []
        listitem = GetMediaInfo(html)
        print 'LISTITEM: '+str(listitem)
        content = html
        print'CONTENT: '+str(listitem)
        match = re.compile('href="(.+?)"').findall(content)
        #match2 = re.compile('target="_blank">https://www.multiup.org/download/(.+?)</a></p>').findall(content)
        listitem = GetMediaInfo(content)
        #for url in match2:
                #addon.add_directory({'mode': 'GetLinks12a', 'url': 'http://www.multiup.org/en/mirror/' + url, 'listitem': listitem}, {'title':  'Multiup.org  : Multi links'}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png') 
        for url in match:
                host = GetDomain(url)
                if 'Unknown' in host:
                                continue
                r = re.search('facebook.com|plus.google.com|\part1|\part2|\part3|\part4|\part5|\.rar|.html|\.file[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
                        continue
                print '*****************************' + host + ' : ' + url
                title = url.rpartition('/')
                title = title[2].replace('.html', '')
                title = title.replace('.htm', '')
                title = title.replace('.rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                title = title.replace('DDLValley.net_', ' ')
                title = title.replace('www.', '')
                title = title.replace ('-','')
                title = title.replace('_',' ')
                title = title.replace('gaz','')
                title = title.replace('NTb','')
                title = title.replace('part1','')
                title = title.replace('part2','')
                title = title.replace('part3','')
                title = title.replace('part4','')
                title = title.replace('part5','')
                title = title.replace('.',' ')
                title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                name = host+'-'+title
                hosted_media = urlresolver.HostedMediaFile(url=url, title=name)
                sources.append(hosted_media)
        source = urlresolver.choose_source(sources)
        if source: stream_url = source.resolve()
        else: stream_url = ''
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^^^ Press back ^^^[/B] [/COLOR]'},'','')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Link may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")

#################################################################################getlinksC###############################################################################################

def GetLinksc(section, url): # Get Links
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        r = re.search('<strong>Links.*</strong>', html)
        if r:
                content = html[r.end():]

        r = re.search('commentblock', content)
        if r:
                content = content[:r.start()]
                
        match = re.compile('style="display:none">(.+?)</div>').findall(content)
        match1 = re.compile('<pre class="links" id=".+?">(.+?)</pre>', re.DOTALL).findall(html)
        listitem = GetMediaInfo(content)
        for url in match + match1:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('facebook.com|plus.google.com|\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
                        continue

                if urlresolver.HostedMediaFile(url= url):
                        print 'in GetLinks if loop'
                        title = url.rpartition('/')
                        title = title[2].replace('.html', '')
                        title = title.replace('.htm', '')
                        title = title.replace('.rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('rar', '[COLOR red][B][I]RAR no streaming[/B][/I][/COLOR]')
                        title = title.replace('sample', '[COLOR lime]Movie Trailer[/COLOR]')
                        title = title.replace('www.', '')
                        title = title.replace ('-',' ')
                        title = title.replace('_',' ')
                        title = title.replace('.',' ')
                        title = title.replace('gaz','')
                        title = title.replace('NTb','')
                        title = title.replace('1st','[COLOR coral][B]1st HALF[/B][/COLOR]')
                        title = title.replace('2nd','[COLOR coral][B]2nd HALF[/B][/COLOR]')
                        title = title.replace('fullmatches net','')
                        title = title.replace('.',' ')
                        title = title.replace('480p','[COLOR coral][B][I]480p[/B][/I][/COLOR]')
                        title = title.replace('720p','[COLOR gold][B][I]720p[/B][/I][/COLOR]')
                        title = title.replace('1080p','[COLOR orange][B][I]1080p[/B][/I][/COLOR]')
                        title = title.replace('mkv','[COLOR gold][B][I]MKV[/B][/I][/COLOR] ')
                        title = title.replace('avi','[COLOR pink][B][I]AVI[/B][/I][/COLOR] ')
                        title = title.replace('mp4','[COLOR purple][B][I]MP4[/B][/I][/COLOR] ')
                        title = title.replace('%20',' ')
                        host = host.replace('youtube.com','[COLOR lime]Movie Trailer[/COLOR]')
                        host = host.replace('k2s.cc','[COLOR red]Unsupported Link[/COLOR]')
                        host = host.replace('ryushare.com','[COLOR red]Unsupported Link[/COLOR]')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')

        find = re.search('commentblock', html)
        if find:
                print 'in comments if'
                html = html[find.end():]
                match = re.compile('class="external">(.+?)</a>', re.DOTALL).findall(html)
                print len(match)
                for url in match:
                        host = GetDomain(url)
                        if 'Unknown' in host:
                                continue
                        
                        # ignore .rar files
                        r = re.search('facebook.com|plus.google.com|\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                        if r:
                                continue
                        try:
                                if urlresolver.HostedMediaFile(url= url):
                                        print 'in GetLinks if loop'
                                        title = url.rpartition('/')
                                        title = title[2].replace('.html', '')
                                        title = title.replace('.htm', '')
                                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' : ' + title}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')

                        except:

                                continue

        setView('tvshows', 'calendar-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------------dxtv--------------------------------------------------------------------------------------#

def GetLinks5(section, url): 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('src="(.+?)"').findall(content)
        match1 = re.compile('<p>DL: <a href="(.+?)" target="_blank">.+?</a></p>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match + match1:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
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
                        url = url.replace('https://openload.co/embed/', 'https://openload.co/f/')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host + ' [COLOR gold]:[/COLOR] ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------------9--------------------------------------------------------------------------------------#

def GetLinks9(section, url): 
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('href="(.+?)"').findall(content)
        match1 = re.compile('href="http://nfo.scene-rls.net/view/(.+?)\s*?">(.+?)</a>').findall(content)
        listitem = GetMediaInfo(content)
        for url, name in match1:
                addon.add_directory({'mode': 'GetLinks9', 'url': 'http://nfo.scene-rls.net/view/' + url, 'listitem': listitem}, {'title':  name}, img=IconPath + 'test1.png', fanart=FanartPath + 'fanart.png')
        for url in match:
                host = GetDomain(url)

                if 'Unknown' in host:
                                continue
                        
                # ignore .rar files
                r = re.search('\.rar[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
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
        setView('tvshows', 'calendar-view')
    except:
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------10------------------------------------------------------------------------------------------#

def GetLinks10(section, url, img):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match6 = re.compile('<a href="(.+?)" target="_blank">\s*?<span class=".+?"><b class="icon-download"></b> Option.+?</span>\s*?<span class=".+?">\s*?<img src=".+?" alt="(Userscloud.com)">').findall(content)
        match7 = re.compile('<a href="(.+?)" target="_blank">\s*?<span class=".+?"><b class="icon-download"></b> Option.+?</span>\s*?<span class=".+?">\s*?<img src=".+?" alt="(Openload.co)">').findall(content)
        match = re.compile('SRC="(.+?)"').findall(content)
        match1 = re.compile('src="(.+?)"').findall(content)
        match5 = re.compile('<a href="(.+?)" target="_blank">').findall(content)
        listitem = GetMediaInfo(content)
        for url, name in match6 + match7:
                addon.add_directory({'mode': 'GetLinks10a', 'url':  url, 'listitem': listitem, 'img': img}, {'title': name}, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        for url in match + match1 + match5:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','f')
                        host = host.replace('youtube.com','[COLOR lime]Movie Trailer[/COLOR]')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks10a(section, url, img):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<link rel="prefetch" href="(.+?)" />').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        host = host.replace('embed.','f')
                        host = host.replace('youtube.com','[COLOR lime]Movie Trailer[/COLOR]')
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title':  host }, img= img, fanart= 'http://imgprix.com/web/wallpapers/private-cinema-room/2560x1600.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------------12--------------------------------------------------------------------------------------#

def GetLinks12(section, url): 
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<strong>.+?</strong><br />\s*?<a href="(.+?)"').findall(content)
        match2 = re.compile('target="_blank">https://www.multiup.org/download/(.+?)</a></p>').findall(content)
        listitem = GetMediaInfo(content)
        for url in match2:
                addon.add_directory({'mode': 'GetLinks12a', 'url': 'http://www.multiup.org/en/mirror/' + url, 'listitem': listitem}, {'title':  'Multiup.org  : Multi links' + ' : ' + url}, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png') 
        for url in match:
                host = GetDomain(url)
                if 'Unknown' in host:
                                continue
                r = re.search('facebook.com|plus.google.com|\part1|\part2|\part3|\part4|\part5|\.rar|.html|\.file[(?:\.html|\.htm)]*', url, re.IGNORECASE)
                if r:
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
        setView('tvshows', 'calendar-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks12a(section, url):
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
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host + ' : ' + title }, img=IconPath + 'play.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


############################################################################# PlayVideo #################################################################################

def PlayVideo(url, listitem):
    try:
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^^^ Press back ^^^[/B] [/COLOR]'},'','')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry Link may have been removed ![/B][/COLOR],[COLOR lime][B]Please try a different link/host !![/B][/COLOR],7000,"")")
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo2(url, listitem, name, img):
        addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(addon_handle, 'video')
        li = xbmcgui.ListItem(name, iconImage=img, thumbnailImage=img)
        li.setProperty('fanart_image', '')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(addon_handle)

#---------------------------------------------------------------------------------------------------------------#

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
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

############################################################################# homescreen ################################################################################################

def MainMenu():        
        addon.add_directory({'mode': 'menu2'}, {'title': '[COLOR blue][B]Movies >>[/B] [/COLOR]>>'}, img=IconPath + 'films.png', fanart=FanartPath + 'fanart.png') 
        addon.add_directory({'mode': 'menu4'}, {'title': '[COLOR darkorange][B]Tv Shows >>[/B] [/COLOR]>>'}, img=IconPath + 'tv2.png', fanart=FanartPath + 'fanart.png') 
        addon.add_directory({'mode': 'menu6'}, {'title': '[COLOR lemonchiffon][B]Sport >>[/B] [/COLOR]>>'}, img=IconPath + 'sport1.png', fanart=FanartPath + 'fanart.png') 
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR red]Resolver Settings[/COLOR]'}, img=IconPath + 'resolver.png', fanart=FanartPath + 'fanart.png')
        setView('Main View', 'main-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- movies -------------------------------------------------------------------------------------------------#

def Menu2(): 
        addon.add_directory({'mode': 'GetTitles12', 'section': 'ALL', 'url': BASE_URL11 + '/category/movies/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR gold](ReleaseBB)[/COLOR] >>'}, img=IconPath + 'moviebb.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles87a', 'section': 'ALL', 'url': BASE_URL87 + '/blog/movie/1-0-1',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR darkmagenta](XL Release)[/COLOR] >>'}, img=IconPath + 'xlmovies.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles81', 'section': 'ALL', 'url': BASE_URL81 + '/post/category/movies-download/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR]  [COLOR gold](newmyvideolink)[/COLOR] >>'}, img=IconPath + 'mnvl2.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles90', 'section': 'ALL', 'url': BASE_URL90 + '/l/m',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Moviess[/B] [/COLOR] [COLOR peachpuff](RapidMovies)[/COLOR] >>'}, img=IconPath + 'rmm.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles45b', 'section': 'ALL', 'url': BASE_URL45 + '/category/movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR brown](scene-rls)[/COLOR] >>'}, img=IconPath + 'srls2.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles45f', 'section': 'ALL', 'url': BASE_URL45 + '/releases/index.php?cat=Movies',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Movies Release List[/B] [/COLOR] [COLOR brown](scene-rls)[/COLOR] >>'}, img=IconPath + 'srls22.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles2', 'section': 'ALL', 'url': BASE_URL2 + 'allmovies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR mediumpurple](ganool)[/COLOR] >>'}, img=IconPath + 'gan1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles33', 'section': 'ALL', 'url': BASE_URL7 + '/category/movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR yellow](2DDL)[/COLOR] >>'}, img=IconPath + '2d2.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles86', 'section': 'ALL', 'url': BASE_URL86 + '/category/films/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR orange](ScnSrc)[/COLOR] >>'}, img=IconPath + 'scensmovie.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles11', 'section': 'ALL', 'url': BASE_URL10 + '/category/movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR powderblue](DDLvalley)[/COLOR] >>'}, img=IconPath + 'ddlmo.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles7', 'section': 'ALL', 'url': BASE_URL8 + '/category/movies',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR mediumspringgreen](Sceper)[/COLOR] >>'}, img=IconPath + 'scmovie.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles57', 'section': 'ALL', 'url': BASE_URL57 + 'movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR lime](veverel)[/COLOR] >>'}, img=IconPath + 'vemov.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL6 + '/category/movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR cyan](rlsarchive)[/COLOR] >>'}, img=IconPath + 'rlsa1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles85a', 'section': 'ALL', 'url': BASE_URL85 + 'movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR orangered](Shaanig)[/COLOR] >>'}, img=IconPath + 'shaamovie.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL9 + '/category/movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR plum](Release Scene)[/COLOR] >>'}, img=IconPath + 'rstmovie1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles5', 'section': 'ALL', 'url': BASE_URL5 + '/category/hollywood-movies/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR indianred](300mbcounter)[/COLOR] >>'}, img=IconPath + '300con.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles96', 'section': 'ALL', 'url': BASE_URL96 + '/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR pink](300mb)[/COLOR] >>'}, img=IconPath + '300m1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles97', 'section': 'ALL', 'url': BASE_URL97 + 'f5-montada',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR darkorange](warez-cc)[/COLOR] >>'}, img=IconPath + 'warezcc.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles76a', 'section': 'ALL', 'url': BASE_URL76 + '/movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR khaki](wrzcraft)[/COLOR] >>'}, img=IconPath + 'w21.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles80', 'section': 'ALL', 'url': BASE_URL80 + '/movies/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR gold](rlsbb backup)[/COLOR] >>'}, img=IconPath + 'bbmbu.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles22', 'section': 'ALL', 'url': BASE_URL22 + '/l/m',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest Moviess[/B] [/COLOR] [COLOR peachpuff](RM backup)[/COLOR] >>'}, img=IconPath + 'rmm.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles48', 'section': 'ALL', 'url': BASE_URL48 + '/category/movies',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR mediumspringgreen](Sceper backup)[/COLOR] >>'}, img=IconPath + 'cimovie.png', fanart=FanartPath + 'fanart.png')

        #addon.add_directory({'mode': 'menu3'}, {'title': '[COLOR blue][B]Latest Movies[/B] [/COLOR] [COLOR powderblue](1080p Zone)[/COLOR] >>'}, img=IconPath + '10z.png', fanart=FanartPath + 'fanart.png') 
        addon.add_directory({'mode': 'menu17'}, {'title': '[COLOR blue][B]Latest DVDScr[/B] [/COLOR] [COLOR orangered](DVDScr Zone)[/COLOR] >>'}, img=IconPath + 'dvdz.png', fanart=FanartPath + 'fanart.png') 
        #addon.add_directory({'mode': 'GetSearchQuery10'},  {'title':  '[COLOR khaki][B]M[/COLOR][COLOR blue]E[/COLOR][COLOR salmon]G[/COLOR][COLOR darkseagreen]A[/COLOR][/B] [COLOR blue][B]R[/B][/COLOR]elease [COLOR blue][B]HUB[/B][/COLOR] (Movies) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'rhs.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'menu5'}, {'title': '[COLOR green][B]Searches[/B] [/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png') 
        setView('Main View', 'main-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1])) 

#------------------------------------------------------------------------------- DVDScr -------------------------------------------------------------------------------------------------#

def Menu17(): 
        addon.add_directory({'mode': 'GetTitles12', 'section': 'ALL', 'url': BASE_URL11 + '/category/movies/dvdscr/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR blue][B]Latest DVDScr[/B] [/COLOR] [COLOR gold](ReleaseBB)[/COLOR] >>'}, img=IconPath + 'moviebb.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles33', 'section': 'ALL', 'url': BASE_URL7 + '/category/movies/dvdscr/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest DVDScr[/B] [/COLOR] [COLOR yellow](2DDL)[/COLOR] >>'}, img=IconPath + '2d2.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles99', 'section': 'ALL', 'url': BASE_URL99 + '/forum/-7-hollywood-camtctsvcdpredvdscrwebrip/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR blue][B]Latest CAM/TC/TS/VCD/Pre/DVDScr/WebRip[/B] [/COLOR] [COLOR gold](zippymoviez)[/COLOR] >>'}, img=IconPath + 'irmovie.png', fanart=FanartPath + 'fanart.png')
        setView('Main View', 'main-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#--------------------------------------------------------------------------------- HD Zone movies ----------------------------------------------------------------------------------------------------------#

def Menu3():
        addon.add_directory({'mode': 'GetTitles81', 'section': 'ALL', 'url': BASE_URL81 + '/category/movies-download/3dmovies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR slateblue][B]Latest 3D[/B] [/COLOR]  [COLOR gold](newmyvideolink)[/COLOR] >>'}, img=IconPath + 'mnvl2.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles12', 'section': 'ALL', 'url': BASE_URL11 + '/category/movies/webrip/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR slateblue][B]Latest HDRips[/B] [/COLOR] [COLOR gold](ReleaseBB)[/COLOR] >>'}, img=IconPath + 'moviebb.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles11', 'section': 'ALL', 'url': BASE_URL10 + '/category/movies/web-dl-movies/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR slateblue][B]Latest HDRips[/B] [/COLOR] [COLOR powderblue](DDLvalley)[/COLOR] >>'}, img=IconPath + 'ddlmo.png', fanart=FanartPath + 'fanart.png')
        setView('Main View', 'main-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------- tv -------------------------------------------------------------------------------------------------#

def Menu4():
        addon.add_directory({'mode': 'GetTitles12', 'section': 'ALL', 'url': BASE_URL11 + '/category/tv-shows/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR gold](ReleaseBB)[/COLOR] >>'}, img=IconPath + 'tvbb.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles33', 'section': 'ALL', 'url': BASE_URL7 + '/category/tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR yellow](2DDL)[/COLOR] >>'}, img=IconPath + '2d.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles90', 'section': 'ALL', 'url': BASE_URL90 + 'l/s',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR peachpuff](RapidMovies)[/COLOR] >>'}, img=IconPath + 'rmtv.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles87', 'section': 'ALL', 'url': BASE_URL87 + '/blog/tvshow/1-0-2',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR darkmagenta](XL Release)[/COLOR] >>'}, img=IconPath + 'xltv.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles45', 'section': 'ALL', 'url': BASE_URL45 + '/category/tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR brown](scene-rls)[/COLOR] >>'}, img=IconPath + 'srls1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles45e', 'section': 'ALL', 'url': BASE_URL45 + '/releases/index.php?cat=TV%20Shows',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Episodes Release List[/B] [/COLOR] [COLOR brown](scene-rls)[/COLOR] >>'}, img=IconPath + 'srls22.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles85a', 'section': 'ALL', 'url': BASE_URL85 + 'tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR orangered](Shaanig)[/COLOR] >>'}, img=IconPath + 'shaatv.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles76', 'section': 'ALL', 'url': BASE_URL76 + '/tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR khaki](wrzcraft)[/COLOR] >>'}, img=IconPath + 'w22.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles7', 'section': 'ALL', 'url': BASE_URL8 + '/category/tv-shows',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR mediumspringgreen](Sceper)[/COLOR] >>'}, img=IconPath + 'setv.png', fanart=FanartPath + 'fanart.png')
        #addon.add_directory({'mode': 'GetTitles56', 'section': 'ALL', 'url': BASE_URL56 + '/layout2'}, {'title':  '[COLOR darkorange][B]TV Show Specials & 4K[/B] [/COLOR] [COLOR brown](Prime Links)[/COLOR] >>'}, img=IconPath + 'pl22.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles86a', 'section': 'ALL', 'url': BASE_URL86 + '/category/tv/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR orange](ScnSrc)[/COLOR] >>'}, img=IconPath + 'scenstv.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles11', 'section': 'ALL', 'url': BASE_URL10 + '/category/tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR powderblue](DDLvalley)[/COLOR] >>'}, img=IconPath + 'ddltv.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles6', 'section': 'ALL', 'url': BASE_URL9 + '/category/tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR plum](Release Scene)[/COLOR] >>'}, img=IconPath + 'rstv1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles30', 'section': 'ALL', 'url': BASE_URL30 + '/tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR green](scnlog)[/COLOR] >>'}, img=IconPath + 'slogtv1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles54a', 'section': 'ALL', 'url': BASE_URL54 + '/'}, {'title':  '[COLOR darkorange][B]UK HD Soaps[/B] [/COLOR] [COLOR brown](uksoapshare)[/COLOR] >>'}, img=IconPath + 'soap.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles81', 'section': 'ALL', 'url': BASE_URL81 + '/post/category/tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR gold](newmyvideolink)[/COLOR] >>'}, img=IconPath + 'mnvl1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles78', 'section': 'ALL', 'url': BASE_URL78 + '/wsotv',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR red](watchseries-online)[/COLOR] >>'}, img=IconPath + 'wso99.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles91', 'section': 'ALL', 'url': BASE_URL91 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR blue](watchtv)[/COLOR] >>'}, img=IconPath + 'erwto.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles59', 'section': 'ALL', 'url': BASE_URL59 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR paleturquoise](Watch TV Series 4U)[/COLOR] >>'}, img=IconPath + 'wso.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles94', 'section': 'ALL', 'url': BASE_URL94 + '/category/tv-show',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR coral](vidzio)[/COLOR] >>'}, img=IconPath + 'vidzio.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles80', 'section': 'ALL', 'url': BASE_URL80 + '/tv-shows/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR gold](rlsbb backup)[/COLOR] >>'}, img=IconPath + 'bbtvbu.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles22', 'section': 'ALL', 'url': BASE_URL22 + 'l/s',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR peachpuff](RM backup)[/COLOR] >>'}, img=IconPath + 'rmtv.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles48', 'section': 'ALL', 'url': BASE_URL48 + '/category/tv-shows',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows[/B] [/COLOR] [COLOR mediumspringgreen](Sceper backup)[/COLOR] >>'}, img=IconPath + 'citv.png', fanart=FanartPath + 'fanart.png')
        #addon.add_directory({'mode': 'GetLinks67', 'section': 'ALL', 'url': BASE_URL67 + '/'}, {'title':  '[COLOR goldenrod](HD) [/COLOR][COLOR darkorange][B]Todays links[/B][/COLOR] [COLOR chartreuse](tvshows-hdtv) [/COLOR]>>'}, img=IconPath + 'th2.png', fanart=FanartPath + 'fanart.png')
        #addon.add_directory({'mode': 'menu11'}, {'title': '[COLOR darkorange][B]Latest Added[/B] [/COLOR] [COLOR blue](1080p zone)[/COLOR] >>'}, img=IconPath + '1080.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'menu18'}, {'title': '[COLOR darkorange][B]Latest Added[/B] [/COLOR] [COLOR blue](Tv Packs zone)[/COLOR] >>'}, img=IconPath + 'tvpack.png', fanart=FanartPath + 'fanart.png')
        #addon.add_directory({'mode': 'menu16'}, {'title': '[COLOR darkorange][B]Latest Added[/B] [/COLOR] [COLOR blue](TEST zone)[/COLOR] >>'}, img=IconPath + 'testz.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'menu5'}, {'title': '[COLOR green][B]Searches >>[/B] [/COLOR]>>'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png') 
        setView('Main View', 'main-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------------ tv packs --------------------------------------------------------------------------------------------#

def Menu18():
        #addon.add_directory({'mode': 'GetTitles45a', 'section': 'ALL', 'url': BASE_URL45 + '/category/tv-packs/',
        #                     'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Packs[/B] [/COLOR] [COLOR brown](scene-rls)[/COLOR] >>'}, img=IconPath + 'srls1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles45e', 'section': 'ALL', 'url': BASE_URL45 + '/releases/index.php?cat=TV%20Packs',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Tv Packs Release List[/B] [/COLOR] [COLOR brown](scene-rls)[/COLOR] >>'}, img=IconPath + 'srls22.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'GetTitles76a', 'section': 'ALL', 'url': BASE_URL76 + '/tv-shows/tv-packs/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows Packs[/B] [/COLOR] [COLOR khaki](wrzcraft)[/COLOR] >>'}, img=IconPath + 'w22.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles57', 'section': 'ALL', 'url': BASE_URL57 + 'tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Shows & Packs[/B] [/COLOR] [COLOR lime](veverel)[/COLOR] >>'}, img=IconPath + 'vetv.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles12', 'section': 'ALL', 'url': BASE_URL11 + '/category/tv-shows/tv-packs/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR darkorange][B]Latest Tv Packs[/B] [/COLOR] [COLOR gold](ReleaseBB)[/COLOR] >>'}, img=IconPath + 'tvbb.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles87', 'section': 'ALL', 'url': BASE_URL87 + '/blog/tvpack/1-0-3',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest Tv Pack[/B] [/COLOR] [COLOR darkmagenta](XL Release)[/COLOR] >>'}, img=IconPath + 'xltv.png', fanart=FanartPath + 'fanart.png')
        setView('Main View', 'main-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------------ test zone tv --------------------------------------------------------------------------------------------#

def Menu16():
        addon.add_directory({'mode': 'GetTitles45c', 'section': 'ALL', 'url': BASE_URL45 + '/tag/2160p/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest 4K[/B] [/COLOR] [COLOR brown](scene-rls)[/COLOR] >>'}, img=IconPath + 'srls1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles33', 'section': 'ALL', 'url': BASE_URL7 + '/category/tv-shows/tv-2160p/',
                             'startPage': '1', 'numOfPages': '2'}, {'title':  '[COLOR darkorange][B]Latest 4K[/B] [/COLOR] [COLOR yellow](2DDL)[/COLOR] >>'}, img=IconPath + '2d.png', fanart=FanartPath + 'fanart.png')
        setView('Main View', 'main-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------------ hd zone tv --------------------------------------------------------------------------------------------#

def Menu11():
        addon.add_directory({'mode': 'GetTitles33', 'section': 'ALL', 'url': BASE_URL7 + '/category/tv-shows/tv-1080p/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest 1080p / 720p[/B] [/COLOR] [COLOR yellow](2DDL)[/COLOR] >>'}, img=IconPath + '2d.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles76', 'section': 'ALL', 'url': BASE_URL76 + '/tv-shows/1080p-tv-shows/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest 1080p / 720p[/B] [/COLOR] [COLOR khaki](wrzcraft)[/COLOR] >>'}, img=IconPath + 'w22.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles3', 'section': 'ALL', 'url': BASE_URL3 + '/tv-show',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR darkorange][B]Latest 1080p / 720p[/B] [/COLOR] [COLOR lightcyan](Crazy hd Source)[/COLOR] >>'}, img=IconPath + 'chd.png', fanart=FanartPath + 'fanart.png')
        setView('Main View', 'main-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#------------------------------------------------------------------------------------- sport -------------------------------------------------------------------------------------------#

def Menu6():
        addon.add_directory({'mode': 'GetTitles33', 'section': 'ALL', 'url': BASE_URL7 + '/category/tv-shows/sport/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest Sport[/B] [/COLOR] [COLOR yellow](2DDL)[/COLOR] >>'}, img=IconPath + '2d3.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'menu9'}, {'title': '[COLOR lemonchiffon][B]Combat Sports[/B] [/COLOR] [COLOR blue](SportsOne)[/COLOR] >>'}, img=IconPath + 'sone3.png', fanart=FanartPath + 'fanart.png') 
        addon.add_directory({'mode': 'menu10'}, {'title': '[COLOR lemonchiffon][B]Motorsport[/B] [/COLOR] [COLOR blue](SportsOne)[/COLOR] >>'}, img=IconPath + 'sone4.png', fanart=FanartPath + 'fanart.png') 

        addon.add_directory({'mode': 'GetTitles24', 'section': 'ALL', 'url': BASE_URL24 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest Wrestling/MMA/Boxing[/B] [COLOR chartreuse](DX-TV)[/COLOR] >>'}, img=IconPath + 'dx.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles98', 'section': 'ALL', 'url': BASE_URL98 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest Wrestling/MMA[/B] [/COLOR] [COLOR blue](allwrestling)[/COLOR] >>'}, img=IconPath + 'allw1.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'GetTitles76', 'section': 'ALL', 'url': BASE_URL76 + '/tv-shows/sports/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest Sport[/B] [/COLOR] [COLOR khaki](wrzcraft)[/COLOR] >>'}, img=IconPath + 'w20.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles76', 'section': 'ALL', 'url': BASE_URL76 + '/mma/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest MMA[/B] [/COLOR] [COLOR khaki](wrzcraft)[/COLOR] >>'}, img=IconPath + 'w20.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'menu8'}, {'title': '[COLOR lightyellow][B]Football Full Matches[/B] [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'GetTitles100', 'section': 'ALL', 'url': BASE_URL100 + '/'}, {'title':  '[COLOR lemonchiffon][B]Latest Highlights[/B] [/COLOR] [COLOR khaki](motdtv)[/COLOR] >>'}, img=IconPath + 'motdtv1.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'GetTitles101', 'section': 'ALL', 'url': BASE_URL101 + '/category/soccer/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lemonchiffon][B]Latest Football[/B] [/COLOR] [COLOR khaki](matchhighlight)[/COLOR] >>'}, img=IconPath + 'match1.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'menu5'}, {'title': '[COLOR green][B]Searches >>[/B] [/COLOR]>>'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png') 

        setView('Main View', 'main-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#---------------------------------------------------------------------------------- sport1 ----------------------------------------------------------------------------------------------#

def Menu9():   #sport1
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout1'}, {'title':  '[COLOR lemonchiffon][B]Latest Added[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout1/category/mma'}, {'title':  '[COLOR lemonchiffon][B]MMA[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout1/category/boxing'}, {'title':  '[COLOR lemonchiffon][B]Boxing[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout1/category/wrestling-ppv'}, {'title':  '[COLOR lemonchiffon][B]Wrestling PPV[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout1/category/tv-show'}, {'title':  '[COLOR lemonchiffon][B]Tv Shows & more[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout1/category/documentary'}, {'title':  '[COLOR lemonchiffon][B]Documentarys[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout1/category/classic-ufc'}, {'title':  '[COLOR lemonchiffon][B]Classic UFC[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout1/category/classics'}, {'title':  '[COLOR lemonchiffon][B]Boxing Classics[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone1.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout1/category/street-fights'}, {'title':  '[COLOR lemonchiffon][B]Street Fights[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone1.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Menu10():   #sport1
        addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout3/category/f1'}, {'title':  '[COLOR lemonchiffon][B]Latest Formula 1[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone4.png', fanart=FanartPath + 'fanart.png')
        #addon.add_directory({'mode': 'GetTitles56a', 'section': 'ALL', 'url': BASE_URL56 + '/layout3/category/moto-gp'}, {'title':  '[COLOR lemonchiffon][B]Latest MOTO GP[/B] [/COLOR] [COLOR blue](Sports One)[/COLOR] >>'}, img=IconPath + 'sone4.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------- fullmatch ---------------------------------------------------------------------------------------------#

def Menu8():
        addon.add_directory({'mode': 'GetTitles16', 'section': 'ALL', 'url': BASE_URL15 + '/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lightyellow]Full Matches [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles16', 'section': 'ALL', 'url': BASE_URL15 + '/category/england-20172018/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lightyellow]England Premier League [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles16', 'section': 'ALL', 'url': BASE_URL15 + '/category/spain-20172018/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lightyellow]Spain [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles16', 'section': 'ALL', 'url': BASE_URL15 + '/category/italy-20172018/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lightyellow]Italy [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles16', 'section': 'ALL', 'url': BASE_URL15 + '/category/germany/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lightyellow]Germany [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
        #addon.add_directory({'mode': 'GetTitles16', 'section': 'ALL', 'url': BASE_URL15 + '/category/full-matches/ligue-1/',
        #                     'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lightyellow]Ligue 1 [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
        #addon.add_directory({'mode': 'GetTitles16', 'section': 'ALL', 'url': BASE_URL15 + '/category/full-matches/matches-other/',
        #                     'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lightyellow]Matches Other [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles16', 'section': 'ALL', 'url': BASE_URL15 + '/category/ucl-20172018/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lightyellow]Uefa Champions League [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetTitles16', 'section': 'ALL', 'url': BASE_URL15 + '/category/uel-20172018/',
                             'startPage': '1', 'numOfPages': '1'}, {'title':  '[COLOR lightyellow]Uefa Europa League [/COLOR]>>'}, img=IconPath + 'fullsport.png', fanart=FanartPath + 'fanart.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------------- search ------------------------------------------------------------------------------------------------#

def Menu5():
        addon.add_directory({'mode': 'GetSearchQuery10'},  {'title':  '[COLOR khaki][B]M[/COLOR][COLOR blue]E[/COLOR][COLOR salmon]G[/COLOR][COLOR darkseagreen]A[/COLOR][/B] [COLOR blue][B]R[/B][/COLOR]elease [COLOR blue][B]HUB[/B][/COLOR] (Movies) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery12'},  {'title':  '[COLOR khaki][B]M[/COLOR][COLOR blue]E[/COLOR][COLOR salmon]G[/COLOR][COLOR darkseagreen]A[/COLOR][/B] [COLOR blue][B]R[/B][/COLOR]elease [COLOR blue][B]HUB[/B][/COLOR] (Tv Episodes) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery11'},  {'title':  '[COLOR khaki][B]M[/COLOR][COLOR blue]E[/COLOR][COLOR salmon]G[/COLOR][COLOR darkseagreen]A[/COLOR][/B] [COLOR blue][B]R[/B][/COLOR]elease [COLOR blue][B]HUB[/B][/COLOR] (Sport) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'GetSearchQuery1'},  {'title':  '[COLOR gold][B]ReleaseBB[/COLOR][/B] (movies, tv shows, sport) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery16'},  {'title':  '[COLOR gold][B]2DDL[/COLOR][/B] (movies, tv shows, sport) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery20'},  {'title':  '[COLOR gold][B]Release Scene[/COLOR][/B] (movies, tv shows, sport) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery3'},  {'title':  '[COLOR gold][B]Scene-Rls[/COLOR][/B] (movies, tv shows, sport) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery4'},  {'title':  '[COLOR gold][B]Scene-Rls Release[/COLOR][/B] (movies, tv shows, sport) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery8'},  {'title':  '[COLOR gold][B]RapidMovies[/COLOR][/B] (movies, tv shows, sport) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery21'},  {'title':  '[COLOR gold][B]NewMyVideoLink[/COLOR][/B] (movies, tv shows) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery6'},  {'title':  '[COLOR gold][B]XL Release[/COLOR][/B] (movies, tv shows) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery5'},  {'title':  '[COLOR gold][B]Watchtv-Online[/COLOR][/B] (tv shows, sport) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery9'},  {'title':  '[COLOR gold][B]vidzio[/COLOR][/B] (tv shows, sport) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery7'},  {'title':  '[COLOR gold][B]300mbcounter[/COLOR][/B] (movies) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery19'},  {'title':  '[COLOR gold][B]Ganool[/COLOR][/B] (movies) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')

        addon.add_directory({'mode': 'GetSearchQuery22'},  {'title':  '[COLOR gold][B]All wrestling[/COLOR][/B] (wrestling/mma) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        addon.add_directory({'mode': 'GetSearchQuery23'},  {'title':  '[COLOR gold][B]Dx-Tv[/COLOR][/B] (wrestling/mma/boxing) : [COLOR green]Search[/COLOR]'}, img=IconPath + 'searches.png', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

############################################################################## searches movies #############################################################################################

def GetSearchQuery10():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]MEGA ADDON SEARCH[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search10(query)
	else:
                return
def Search10(query):
    try:
        url = 'http://4dlblog.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="post-box-title">\s*?<a href="http://4dlblog.com/(.+?)">(.+?)</a>\s*?</h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://rlsbb.ru/' + url}, {'title':  title + ' [COLOR lightcyan]...(BB Backup)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry BB Backup search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://tddl.tv/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2><a href="(.+?)" title=".+?">(.+?)</a></h2>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR yellow]...(2ddl)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry 2ddl search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://scene-rls.net/releases/index.php?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="p-c p-c-title"><h2><a target="_blank" class="p-title" href="(.+?)">(.+?)</a>(.+?)</h2>', re.DOTALL).findall(html)
        for movieUrl, title, name in match:
                addon.add_directory({'mode': 'GetLinks9', 'url': movieUrl}, {'title':  title + ' : ' + name + ' [COLOR brown](scene-rls)(R)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry scene-rls (R) search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://rmz.cr/search/' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<a class="title" href="/release/(.+?)"><b>(.+?)</b></a>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks68', 'url': 'http://rmz.cr/release/' + url}, {'title':  title + ' [COLOR green]...(rapidmoviez)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry rapidmoviez search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://www.rlsarchive.com/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="post-box-title">\s*?<a href="(.+?)">(.+?)</a>\s*?</h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR slateblue]...(rlsarchive)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry rlsarchive search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://wrzcraft.net/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2><a href="(.+?)" title=".+?>(.+?)</a></h2>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR khaki]...(wrzcraft)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry wrzcraft search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://to.newmyvideolink.xyz/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="post-title"><a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
        for movieUrl, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl + '2'}, {'title':  title + ' [COLOR aqua](MVL)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry MVL search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://www.300mbcounter.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="title"><a href="(.+?)" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title.replace ('Movie Free Download',' ').replace ('Movie Download',' ').replace ('Free Download',' ').replace ('Full English Movie Download',' ') + ' [COLOR red]...(300mbcounter)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry 300mbcounter search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


############################################################################## searches tv #############################################################################################


def GetSearchQuery12():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]MEGA ADDON SEARCH[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search12(query)
	else:
                return
def Search12(query):
    try:
        url = 'http://4dlblog.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="post-box-title">\s*?<a href="http://4dlblog.com/(.+?)">(.+?)</a>\s*?</h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://rlsbb.ru/' + url}, {'title':  title + ' [COLOR lightcyan]...(BB Backup)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry BB Backup search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://tddl.tv/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2><a href="(.+?)" title=".+?">(.+?)</a></h2>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR yellow]...(2ddl)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry 2ddl search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://www.vidzio.net/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)e</a></h2>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR blue]...(vidzio)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry vidzio search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://scene-rls.net/search/' + query + '/'
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="postTitle"><span></span><a href="(.+?)" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
        for movieUrl, title in match:
                addon.add_directory({'mode': 'GetLinks9', 'url': movieUrl}, {'title':  title.replace('<u>', '').replace('</u>', '') + ' [COLOR brown](scene-rls)(S)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry scene-rls (S) search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://rlsscn.in/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="title">\s*?<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>\s*?</h2>.+? <p><img class="lazy lazy-hidden" src=".+?" data-lazy-type="image" data-lazy-src="(.+?)"').findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title.replace('.', ' ') + ' [COLOR red]...(rlsscn)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry rlsscn search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://wrzcraft.net/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2><a href="(.+?)" title=".+?>(.+?)</a></h2>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR khaki]...(wrzcraft)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry wrzcraft search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://rmz.cr/search/' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<a class="title" href="/release/(.+?)"><b>(.+?)</b></a>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks68', 'url': 'http://rmz.cr/release/' + url}, {'title':  title + ' [COLOR green]...(rapidmoviez)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry rapidmoviez search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://hareemtv.com/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h1 class="entry-title">\s*?<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>\s*?</h1>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR mediumturquoise]...(hareemtv)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry hareemtv search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://shazzmin-estore.com/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="moviefilm">\s*?<a href="(.+?)">\s*?<img src="(.+?)" alt="(.+?)" height="150px" width="115px" /></a>').findall(html)
        for url, img, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR palevioletred]...(WSO)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry WSO search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'https://scnlog.me/tv-shows/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('''<h1><img class='caticonslite_bm' alt="" src="/wp-content/uploads/tv-shows.png" title="" /><a href="(.+?)" rel="bookmark" title="(.+?)">.+?</a></h1>''').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title.replace('.',' ') + ' [COLOR blue]...(scnlog)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry scnlog search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#------------------------------------------------------------------------------ sport search ----------------------------------------------------------------------------------#

def GetSearchQuery11():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]MEGA ADDON SEARCH[/COLOR]')
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
        url = 'http://4dlblog.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="post-box-title">\s*?<a href="http://4dlblog.com/(.+?)">(.+?)</a>\s*?</h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://rlsbb.ru/' + url}, {'title':  title + ' [COLOR lightcyan]...(BB Backup)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry BB Backup search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://scene-rls.net/releases/index.php?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="p-c p-c-title"><h2><a target="_blank" class="p-title" href="(.+?)">(.+?)</a>(.+?)</h2>', re.DOTALL).findall(html)
        for movieUrl, title, name in match:
                addon.add_directory({'mode': 'GetLinks9', 'url': movieUrl}, {'title':  title + ' : ' + name + ' [COLOR brown](scene-rls)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry scene-rls search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://wrzcraft.net/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2><a href="(.+?)" title=".+?>(.+?)</a></h2>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR khaki]...(wrzcraft)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry wrzcraft search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://rmz.cr/search/' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<a class="title" href="/release/(.+?)"><b>(.+?)</b></a>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks68', 'url': 'http://rmz.cr/release/' + url}, {'title':  title + ' [COLOR green]...(rapidmoviez)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry rapidmoviez search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://allwrestling.in/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>').findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title.replace('Watch','') + ' [COLOR pink]...(allwrestling)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry allwrestling search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'https://watchtv-online.pw/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2><a href="(.+?)" rel="bookmark" title="(.+?)</a></h2>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR red]...(watchtv-online)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry watchtv-online search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://hareemtv.com/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h1 class="entry-title">\s*?<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>\s*?</h1>').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR mediumturquoise]...(hareemtv)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry hareemtv search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'http://shazzmin-estore.com/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="moviefilm">\s*?<a href="(.+?)">\s*?<img src="(.+?)" alt="(.+?)" height="150px" width="115px" /></a>').findall(html)
        for url, img, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title + ' [COLOR palevioletred]...(WSO)[/COLOR]'}, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry WSO search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
    try:
        url = 'https://scnlog.me/tv-shows/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('''<h1><img class='caticonslite_bm' alt="" src="/wp-content/uploads/tv-shows.png" title="" /><a href="(.+?)" rel="bookmark" title="(.+?)">.+?</a></h1>''').findall(html)
        for url, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title.replace('.',' ') + ' [COLOR blue]...(scnlog)[/COLOR]'}, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry scnlog search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

##.replace('/', ' ')## \s*? ## 
#-------------------------------------------------------------------------- vidzio ----------------------------------------------------------------------------------------------#

def GetSearchQuery9():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]wrelease[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search9(query)
	else:
                return
def Search9(query):
    try:
        url = 'http://www.vidzio.net/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>', re.DOTALL).findall(html)
        for movieUrl, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl}, {'title':  title }, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry wrelease search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- rmz.cr ----------------------------------------------------------------------------------------------#

def GetSearchQuery8():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]rmz[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search8(query)
	else:
                return
def Search8(query):
    try:
        url = 'http://rmz.cr/search/' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<a class="title" href="/release/(.+?)"><b>(.+?)</b></a>', re.DOTALL).findall(html)
        for movieUrl, title in match:
                addon.add_directory({'mode': 'GetLinksc', 'url': 'http://rmz.cr/release/' + movieUrl}, {'title':  title }, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry rapidmovies search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))
#-------------------------------------------------------------------------- rlsbb ----------------------------------------------------------------------------------------------#

def GetSearchQuery1():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]SEARCH[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search1(query)
	else:
                return
def Search1(query):
    try:
        url = 'http://4dlblog.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="post-box-title">\s*?<a href="http://4dlblog.com/(.+?)">(.+?)</a>\s*?</h2>.+? src="(.+?)"', re.DOTALL).findall(html)
        for url, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://rlsbb.ru/' + url}, {'title':  title }, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry BB Backup search search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- scene-rls ----------------------------------------------------------------------------------------------#

def GetSearchQuery3():   #search
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]SEARCH[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search3(query)
	else:
                return
def Search3(query):
    try:
        url = 'http://scene-rls.net/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="postTitle"><span></span><a href="(.+?)" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
        for movieUrl, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl}, {'title':  title.replace('<u>', '').replace('</u>', '') }, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry scene-rls search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetSearchQuery4():   #releasetv
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]SEARCH[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search4(query)
	else:
                return
def Search4(query):
    try:
        url = 'http://scene-rls.net/releases/index.php?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="p-c p-c-title"><h2><a target="_blank" class="p-title" href="(.+?)">(.+?)</a>(.+?)</h2>', re.DOTALL).findall(html)
        for movieUrl, title, name in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl}, {'title':  title + ' : ' + name }, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
        setView('tvshows', 'calendar-view')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry scene-rls search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- 2ddl ----------------------------------------------------------------------------------------------#

def GetSearchQuery16():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]2DDL SEARCH[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search16(query)
	else:
                return
def Search16(query):
    try:
        url = 'http://ddl2.org/?s=' + query 
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2><a href="(.+?)" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
        for movieUrl, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl}, {'title':  title }, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry rlsbb search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- ganool ----------------------------------------------------------------------------------------------#

def GetSearchQuery19():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]sceper[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search19(query)
	else:
                return
def Search19(query):
    try:
        url = 'https://ganool.se/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="movimgbox.+?">\s*?<a href="(.+?)" class="ml-mask "><img src="(.+?)" class="img-responsive homethumb" />\s*?<span class="mli-info"><h2>(.+?)</h2></span>', re.DOTALL).findall(html)
        for movieUrl, img, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl}, {'title':  title }, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry ganool search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- release scene ----------------------------------------------------------------------------------------------#

def GetSearchQuery20():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]rls-movies[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search20(query)
	else:
                return
def Search20(query):
    try:
        url = 'http://rlsscn.in/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="title">\s*?<a href="(.+?)" title=".+?" rel="bookmark">(.+?)</a>\s*?</h2>.+? <p><img class="lazy lazy-hidden" src=".+?" data-lazy-type="image" data-lazy-src="(.+?)"', re.DOTALL).findall(html)
        for movieUrl, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl}, {'title':  title }, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


#-------------------------------------------------------------------------- newmyvideolink ----------------------------------------------------------------------------------------------#

def GetSearchQuery21():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]NMVL[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search21(query)
	else:
                return
def Search21(query):
    try:
        url = 'http://to.newmyvideolink.xyz/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="post-title"><a href="(.+?)" rel="bookmark" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
        for movieUrl, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl + '2'}, {'title':  title }, img= 'http://to.newmyvideolink.xyz/wp-content/uploads/tn_newszeplin_header_logo.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry NMVL search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- watchtv-online ----------------------------------------------------------------------------------------------#

def GetSearchQuery5():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]watchtv-online[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search5(query)
	else:
                return
def Search5(query):
    try:
        url = 'https://watchtv-online.pw/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="boxentry">\s*?<a href="(.+?)" title="(.+?)">\s*?<div class="harvendra">\s*?<img src="(.+?)" alt=".+?" />', re.DOTALL).findall(html)
        for movieUrl, title, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl}, {'title':  title.replace('.', ' ') }, img= 'https://watchtv-online.pw/' + img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry watchtv-online search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- XL Release ----------------------------------------------------------------------------------------------#

def GetSearchQuery6():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]XL Release[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search6(query)
	else:
                return
def Search6(query):
    try:
        url = 'https://onlineseries.ucoz.com/search/?q=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<div class="eTitle" style="text-align:left;font-weight:normal"><a href="(.+?)"> <b>(.+?)</b>(.+?)</a></div>', re.DOTALL).findall(html)
        for movieUrl, title, name in match:
                addon.add_directory({'mode': 'GetLinksd', 'url': movieUrl}, {'title':  title.replace('.', ' ').replace('<b>', '').replace('</b>', '') + name.replace('.', ' ').replace('<b>', '').replace('</b>', '')  }, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry msearch is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
        setView('tvshows', 'calendar-view')
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- 300mbcounter ----------------------------------------------------------------------------------------------#

def GetSearchQuery7():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]ganoolmovies[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search7(query)
	else:
                return
def Search7(query):
    try:
        url = 'http://www.300mbcounter.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="title"><a href="(.+?)" title=".+?">(.+?)</a></h2>', re.DOTALL).findall(html)
        for movieUrl, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl}, {'title':  title.replace ('Movie Free Download',' ').replace ('Movie Download',' ').replace ('Free Download',' ').replace ('Full English Movie Download',' ') }, img= 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
        setView('tvshows', 'calendar-view')
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- allwrestling ----------------------------------------------------------------------------------------------#

def GetSearchQuery22():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]allwrestling[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search22(query)
	else:
                return
def Search22(query):
    try:
        url = 'http://allwrestling.in/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>', re.DOTALL).findall(html)
        for movieUrl, title in match:
                addon.add_directory({'mode': 'GetLinks', 'url': movieUrl}, {'title':  title.replace ('Watch','') }, img= 'https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg', fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
        setView('tvshows', 'calendar-view')
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------- dx-tv ----------------------------------------------------------------------------------------------#

def GetSearchQuery23():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green]dx-tv[/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search23(query)
	else:
                return
def Search23(query):
    try:
        url = 'http://dx-tv.com/?s=' + query
        url = url.replace(' ', '+')
        print url
        html = net.http_GET(url).content
        match = re.compile('<article class="latestPost excerpt  ">\s*?<a href="(.+?)" title="(.+?)" rel="nofollow" id="featured-thumbnail">\s*?<div class="featured-thumbnail"><img width="280" height="172" src="(.+?)"', re.DOTALL).findall(html)
        for movieUrl, title, img in match:
                addon.add_directory({'mode': 'GetLinks5', 'url': movieUrl}, {'title':  title.replace ('Watch','') }, img= img, fanart=FanartPath + 'fanart.png')
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR red][B]Sorry search is down [/B][/COLOR],[COLOR blue][B]Please try later[/B][/COLOR],7000,"")")
        setView('tvshows', 'calendar-view')
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#https://raw.githubusercontent.com/MrEntertainment/backupREPO/master/plugin.video.theyidrh/icons/newart.jpg#\s*?#
####################################################################### setViews #######################################################################################

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

#######################################################################################################################################################################

if mode == 'main': 
	MainMenu()
elif mode == 'HelpMenu':
        HelpMenu()
elif mode == 'MusicMenu':
        MusicMenu()
elif mode == 'GetTitles': 
	GetTitles(section, url, startPage, numOfPages)
elif mode == 'GetTitles1': 
	GetTitles1(section, url, startPage, numOfPages)
elif mode == 'GetTitles2': 
	GetTitles2(section, url, startPage, numOfPages)
elif mode == 'GetTitles2a': 
	GetTitles2a(section, url, startPage, numOfPages)
elif mode == 'GetTitles3': 
	GetTitles3(section, url, startPage, numOfPages)
elif mode == 'GetTitles4': 
	GetTitles4(section, url, startPage, numOfPages)
elif mode == 'GetTitles5': 
	GetTitles5(section, url, startPage, numOfPages)
elif mode == 'GetTitles6': 
	GetTitles6(section, url, startPage, numOfPages)
elif mode == 'GetTitles7': 
	GetTitles7(section, url, startPage, numOfPages)
elif mode == 'GetTitles8': 
	GetTitles8(section, url, startPage, numOfPages)
elif mode == 'GetTitles9': 
	GetTitles9(section, url, startPage, numOfPages)
elif mode == 'GetTitles1': 
	GetTitles1(section, url, startPage, numOfPages)
elif mode == 'GetTitles11': 
	GetTitles11(section, url, startPage, numOfPages)
elif mode == 'GetTitles12': 
	GetTitles12(section, url, startPage, numOfPages)
elif mode == 'GetTitles12c': 
	GetTitles12c(section, url, startPage, numOfPages)
elif mode == 'GetTitles13': 
	GetTitles13(section, url, startPage, numOfPages)
elif mode == 'GetTitles16': 
	GetTitles16(section, url, startPage, numOfPages)
elif mode == 'GetTitles17': 
	GetTitles17(section, url, startPage, numOfPages)
elif mode == 'GetTitles18': 
	GetTitles18(section, url, startPage, numOfPages)
elif mode == 'GetTitles19': 
	GetTitles19(section, url, startPage, numOfPages)
elif mode == 'GetTitles20': 
	GetTitles20(section, url, startPage, numOfPages)
elif mode == 'GetTitles21': 
	GetTitles21(section, url, startPage, numOfPages)
elif mode == 'GetTitles22': 
	GetTitles22(section, url, startPage, numOfPages)
elif mode == 'GetTitles24': 
	GetTitles24(section, url, startPage, numOfPages)
elif mode == 'GetTitles25': 
	GetTitles25(query)
elif mode == 'GetTitles25a': 
	GetTitles25a(query)
elif mode == 'GetTitles25b': 
	GetTitles25b(query)
elif mode == 'GetTitles26': 
	GetTitles26(query)
elif mode == 'GetTitles27': 
	GetTitles27(url)
elif mode == 'GetTitles28': 
	GetTitles28(query)
elif mode == 'GetTitles29': 
	GetTitles29(section, url, startPage, numOfPages)
elif mode == 'GetTitles30': 
	GetTitles30(section, url, startPage, numOfPages)
elif mode == 'GetTitles32': 
	GetTitles32(query)
elif mode == 'GetTitles32a': 
	GetTitles32a(query)
elif mode == 'GetTitles33': 
	GetTitles33(section, url, startPage, numOfPages)
elif mode == 'GetTitles34': 
	GetTitles34(query)
elif mode == 'GetTitles41': 
	GetTitles41(query, startPage, numOfPages)
elif mode == 'GetTitles42': 
	GetTitles42(section, url, startPage, numOfPages)
elif mode == 'GetTitles42a': 
	GetTitles42a(img, section, url, startPage, numOfPages)
elif mode == 'GetTitles42b': 
	GetTitles42b(img, query)
elif mode == 'GetTitles45': 
	GetTitles45(section, url, startPage, numOfPages)
elif mode == 'GetTitles45a': 
	GetTitles45a(section, url, startPage, numOfPages)
elif mode == 'GetTitles45b': 
	GetTitles45b(section, url, startPage, numOfPages)
elif mode == 'GetTitles45c': 
	GetTitles45c(section, url, startPage, numOfPages)
elif mode == 'GetTitles45d': 
	GetTitles45d(section, url, startPage, numOfPages)
elif mode == 'GetTitles45e': 
	GetTitles45e(section, url, startPage, numOfPages)
elif mode == 'GetTitles45f': 
	GetTitles45f(section, url, startPage, numOfPages)
elif mode == 'GetTitles46': 
	GetTitles46(section, url, startPage, numOfPages)
elif mode == 'GetTitles47': 
	GetTitles47(section, url, startPage, numOfPages)
elif mode == 'GetTitles48': 
	GetTitles48(section, url, startPage, numOfPages)
elif mode == 'GetTitles50': 
	GetTitles50(section, url, startPage, numOfPages)
elif mode == 'GetTitles51': 
	GetTitles51(section, url, startPage, numOfPages)
elif mode == 'GetTitles54': 
	GetTitles54(section, url)
elif mode == 'GetTitles54a': 
	GetTitles54a(section, url)
elif mode == 'GetTitles56': 
	GetTitles56(img, section, url)
elif mode == 'GetTitles56a': 
	GetTitles56a(img, section, url)
elif mode == 'GetTitles57': 
	GetTitles57(section, url, startPage, numOfPages)
elif mode == 'GetTitles59': 
	GetTitles59(section, url, startPage, numOfPages)
elif mode == 'GetTitles60': 
	GetTitles60(section, url, startPage, numOfPages)
elif mode == 'GetTitles60a': 
	GetTitles60a(section, url, startPage, numOfPages)
elif mode == 'GetTitles61': 
	GetTitles61(section, url, startPage, numOfPages)
elif mode == 'GetTitles61a': 
	GetTitles61a(section, url, startPage, numOfPages)
elif mode == 'GetTitles62': 
	GetTitles62(section, url, startPage, numOfPages)
elif mode == 'GetTitles62a': 
	GetTitles62a(section, url, startPage, numOfPages)
elif mode == 'GetTitles65': 
	GetTitles65(section, url, startPage, numOfPages)
elif mode == 'GetTitles66': 
	GetTitles66(section, url, startPage, numOfPages)
elif mode == 'GetTitles72': 
	GetTitles72(section, url, startPage, numOfPages)
elif mode == 'GetTitles73': 
	GetTitles73(section, url, startPage, numOfPages)
elif mode == 'GetTitles74': 
	GetTitles74(section, url, startPage, numOfPages)
elif mode == 'GetTitles76': 
	GetTitles76(section, url, startPage, numOfPages)
elif mode == 'GetTitles76a': 
	GetTitles76a(section, url, startPage, numOfPages)
elif mode == 'GetTitles77': 
	GetTitles77(section, url, startPage, numOfPages)
elif mode == 'GetTitles78': 
	GetTitles78(section, url, startPage, numOfPages)
elif mode == 'GetTitles79': 
	GetTitles79(section, url, startPage, numOfPages)
elif mode == 'GetTitles80': 
	GetTitles80(section, url, startPage, numOfPages)
elif mode == 'GetTitles81': 
	GetTitles81(section, url, startPage, numOfPages)
elif mode == 'GetTitles82': 
	GetTitles82(section, url, startPage, numOfPages)
elif mode == 'GetTitles83': 
	GetTitles83(section, url, startPage, numOfPages)
elif mode == 'GetTitles84': 
	GetTitles84(section, url, startPage, numOfPages)
elif mode == 'GetTitles85a': 
	GetTitles85a(section, url, startPage, numOfPages)
elif mode == 'GetTitles86': 
	GetTitles86(section, url, startPage, numOfPages)
elif mode == 'GetTitles86a': 
	GetTitles86a(section, url, startPage, numOfPages)
elif mode == 'GetTitles87': 
	GetTitles87(section, url, name, startPage, numOfPages)
elif mode == 'GetTitles87a': 
	GetTitles87a(section, url, name, img, startPage, numOfPages)
elif mode == 'GetLinks87b':
	GetLinks87b(section, url, name, img)
elif mode == 'GetTitles88': 
	GetTitles88(section, url, startPage, numOfPages)
elif mode == 'GetTitles89': 
	GetTitles89(section, url, startPage, numOfPages)
elif mode == 'GetTitles90': 
	GetTitles90(section, url, startPage, numOfPages)
elif mode == 'GetTitles91': 
	GetTitles91(section, url, startPage, numOfPages)
elif mode == 'GetTitles92': 
	GetTitles92(section, url, startPage, numOfPages)
elif mode == 'GetTitles93': 
	GetTitles93(section, url, startPage, numOfPages)
elif mode == 'GetTitles94': 
	GetTitles94(section, url, startPage, numOfPages)
elif mode == 'GetTitles94a': 
	GetTitles94a(section, url, startPage, numOfPages)
elif mode == 'GetTitles95': 
	GetTitles95(section, url, startPage, numOfPages)
elif mode == 'GetTitles96': 
	GetTitles96(section, url, startPage, numOfPages)
elif mode == 'GetTitles97': 
	GetTitles97(section, url, startPage, numOfPages)
elif mode == 'GetTitles98': 
	GetTitles98(section, url, startPage, numOfPages)
elif mode == 'GetTitles99': 
	GetTitles99(section, url, startPage, numOfPages)
elif mode == 'GetTitles100': 
	GetTitles100(section, url)
elif mode == 'GetTitles101': 
	GetTitles101(section, url, startPage, numOfPages)
elif mode == 'GetTitles102': 
	GetTitles102(section, url, name, img, startPage, numOfPages)
elif mode == 'GetTitles52': 
	GetTitles52(query, url)
elif mode == 'GetLinks':
	GetLinks(section, url)
elif mode == 'GetLinksd':
	GetLinksd(section, url, name, img)
elif mode == 'GetLinksb':
	GetLinksb(section, url)
elif mode == 'GetLinksc':
	GetLinksc(section, url)
elif mode == 'GetLinks1':
	GetLinks1(section, url)
elif mode == 'GetLinks3':
	GetLinks3(section, url)
elif mode == 'GetLinks5':
	GetLinks5(section, url)
elif mode == 'GetLinks6':
	GetLinks6(section, url)
elif mode == 'GetLinks7':
	GetLinks7(section, url)
elif mode == 'GetLinks8':
	GetLinks8(section, url)
elif mode == 'GetLinks9':
	GetLinks9(section, url)
elif mode == 'GetLinks10':
	GetLinks10(section, url, img)
elif mode == 'GetLinks10a':
	GetLinks10a(section, url, img)
elif mode == 'GetLinks11':
	GetLinks11(section, url)
elif mode == 'GetLinks12':
	GetLinks12(section, url)
elif mode == 'GetLinks12a':
	GetLinks12a(section, url)
elif mode == 'GetLinks14':
	GetLinks14(section, url)
elif mode == 'GetLinks15':
	GetLinks15(section, url)
elif mode == 'GetLinks16':
	GetLinks16(section, url)
elif mode == 'GetLinks17':
	GetLinks17(section, url)
elif mode == 'GetLinks20':
	GetLinks20(section, url)
elif mode == 'GetLinks28':
	GetLinks28(section, url)
elif mode == 'GetLinks54':
	GetLinks54(section, url)
elif mode == 'GetLinks67':
	GetLinks67(section, url)
elif mode == 'GetLinks68':
	GetLinks68(section, url)
elif mode == 'GetLinks69':
	GetLinks69(section, url)
elif mode == 'GetLinks70':
	GetLinks70(section, url)
elif mode == 'GetLinks88':
	GetLinks88(section, url)
elif mode == 'GetLinks89':
	GetLinks89(section, url)
elif mode == 'GetLinks99':
	GetLinks99(section, url)
elif mode == 'GetLinks100':
	GetLinks100(section, url)
elif mode == 'GetLinks101':
	GetLinks101(section, url)
elif mode == 'Categories':
        Categories(url)
elif mode == 'GetSearchQuery1':
	GetSearchQuery1()
elif mode == 'Search1':
	Search1(query)
elif mode == 'GetSearchQuery2':
	GetSearchQuery2()
elif mode == 'Search2':
	Search2(query)
elif mode == 'GetSearchQuery3':
	GetSearchQuery3()
elif mode == 'Search3':
	Search3(query)
elif mode == 'GetSearchQuery4':
	GetSearchQuery4()
elif mode == 'Search4':
	Search4(query)
elif mode == 'GetSearchQuery5':
	GetSearchQuery5()
elif mode == 'Search5':
	Search5(query)
elif mode == 'GetSearchQuery6':
	GetSearchQuery6()
elif mode == 'Search6':
	Search6(query)
elif mode == 'GetSearchQuery7':
	GetSearchQuery7()
elif mode == 'Search7':
	Search7(query)
elif mode == 'GetSearchQuery8':
	GetSearchQuery8()
elif mode == 'Search8':
	Search8(query)
elif mode == 'GetSearchQuery9':
	GetSearchQuery9()
elif mode == 'Search9':
	Search9(query)
elif mode == 'GetSearchQuery10':
	GetSearchQuery10()
elif mode == 'Search10':
	Search10(query)
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
elif mode == 'GetSearchQuery15':
	GetSearchQuery15()
elif mode == 'Search15':
	Search15(query)
elif mode == 'GetSearchQuery16':
	GetSearchQuery16()
elif mode == 'Search16':
	Search16(query)
elif mode == 'GetSearchQuery17':
	GetSearchQuery17()
elif mode == 'Search17':
	Search17(query)
elif mode == 'GetSearchQuery18':
	GetSearchQuery18()
elif mode == 'Search18':
	Search18(query)
elif mode == 'GetSearchQuery19':
	GetSearchQuery19()
elif mode == 'Search19':
	Search19(query)
elif mode == 'GetSearchQuery20':
	GetSearchQuery20()
elif mode == 'Search20':
	Search20(query)
elif mode == 'GetSearchQuery21':
	GetSearchQuery21()
elif mode == 'Search21':
	Search21(query)
elif mode == 'GetSearchQuery22':
	GetSearchQuery22()
elif mode == 'Search22':
	Search22(query)
elif mode == 'GetSearchQuery23':
	GetSearchQuery23()
elif mode == 'Search23':
	Search23(query)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)
elif mode == 'PlayVideo2':
	PlayVideo2(url, listitem, name, img)
elif mode == 'PlayVideo3':
	PlayVideo3(url, listitem)	
elif mode == 'ResolverSettings':
        urlresolver.display_settings()
elif mode == 'Categories':
        Categories()
elif mode == 'GetTitles43': 
	GetTitles43(section, url)
elif mode == 'GetTitles43a': 
	GetTitles43a(query, section)
elif mode == 'GetTitles44': 
	GetTitles44(section, query)
if mode == 'menu2':
       Menu2()
if mode == 'menu3':
       Menu3()
if mode == 'menu4':
       Menu4()
if mode == 'menu5':
       Menu5()
if mode == 'menu6':
       Menu6()
if mode == 'menu7':
       Menu7()
if mode == 'menu8':
       Menu8()
if mode == 'menu9':
       Menu9()
if mode == 'menu10':
       Menu10()
if mode == 'menu11':
       Menu11()
if mode == 'menu12':
       Menu12()
if mode == 'menu13':
       Menu13()
if mode == 'menu14':
       Menu14()
if mode == 'menu15':
       Menu15()
if mode == 'menu16':
       Menu16()
if mode == 'menu17':
       Menu17()
if mode == 'menu18':
       Menu18()
if mode == 'menu19':
       Menu19()
if mode == 'menu20':
       Menu20()
elif mode == 'Help':
    import helpbox
    helpbox.HelpBox()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
