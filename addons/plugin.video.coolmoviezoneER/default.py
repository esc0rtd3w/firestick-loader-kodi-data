import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib, urllib2
import re, string, sys, os
import urlresolver
from TheYid.common.addon import Addon
from TheYid.common.net import Net
from htmlentitydefs import name2codepoint as n2cp
import HTMLParser

addon_id = 'plugin.video.coolmoviezoneER'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'coolmoviezoneER.db')
BASE_URL = 'http://coolmoviezone.net/'
net = Net()
addon = Addon('plugin.video.coolmoviezoneER', sys.argv)

###### PATHS ###########
AddonPath = addon.get_path()
IconPath = AddonPath + "/icons/"
FanartPath = AddonPath + "/icons/"

##### Queries ##########
mode = addon.queries['mode']
url = addon.queries.get('url', None)
content = addon.queries.get('content', None)
query = addon.queries.get('query', None)
listitem = addon.queries.get('listitem', None)
urlList = addon.queries.get('urlList', None)
section = addon.queries.get('section', None)
text = addon.queries.get('text', None)
img = addon.queries.get('img', None)
#\s*?#
################################################################################# Titles #################################################################################

def GetTitles4(url, text): #year
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile("<a href='http://coolmoviezone.net/tag/(.+?)' class='tag-link.+?' title='.+?topics' style='font-size.+?'>(.+?)</a>").findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetTitles3', 'url': 'http://coolmoviezone.net/tag/' + url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#-------------------------------------------------------------------------------#
def GetTitles2(url, text): #gen
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<li class="cat-item cat-item-.+?"><a href="http://coolmoviezone.net/category/(.+?)" title=".+?">(.+?)</a>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetTitles3', 'url': 'http://coolmoviezone.net/category/' + url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles3(url, text, img):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<div style=".+?" class=".+?"><img class=".+?" src="(.+?)" alt="(.+?)" width=".+?" height=".+?" /><p class="wp-caption-text">.+?</p></div>\s*?<p> <a href="http://coolmoviezone.net/(.+?)/.+?" class="more-link">.+?</a></p>').findall(content)
        match1 = re.compile('''rel="next" href="(.+?)">.+?</a>''').findall(content)
        for img, name, url in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://coolmoviezone.net/' + url, 'listitem': listitem, 'text': name.strip(), 'img': img}, {'title': name.strip()}, img= img, fanart=FanartPath + 'fanart.jpg')
        for url in match1:
                addon.add_directory({'mode': 'GetTitles3', 'url': url, 'listitem': listitem, 'text': url}, {'title': 'Next Page...'}, img= 'http://raumatiroadsurgery.co.nz/img/arrow.png', fanart=FanartPath + 'fanart.jpg')
        setView('tvshows', 'tvshows-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

#----------------------------------------------------------------------------------------------------------------------------------------------#
def GetTitles(url, text): #AtoZ
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<span class="azlink"><a href="(.+?)" title=".+?">(.+?)</a></span>').findall(content)
        for url, name in match:
                addon.add_directory({'mode': 'GetTitles1', 'url': url, 'listitem': listitem, 'text': name.strip()}, {'title': name.strip()}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles1(url, text, img):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="http://coolmoviezone.net/(.+?)" class="thumbnail-wrapper"><img src="(.+?)"').findall(content)
        match1 = re.compile('''rel="next" href="(.+?)">.+?</a>''').findall(content)
        for url, img in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://coolmoviezone.net/' + url, 'listitem': listitem, 'text': url, 'img': img}, {'title': url.replace('-', ' ').replace('/', '')}, img= img, fanart=FanartPath + 'fanart.jpg')
        for url in match1:
                addon.add_directory({'mode': 'GetTitles1', 'url': url, 'listitem': listitem, 'text': url}, {'title': 'Next Page...'}, img= 'http://raumatiroadsurgery.co.nz/img/arrow.png', fanart=FanartPath + 'fanart.jpg')
        setView('tvshows', 'tvshows-view')
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))


def GetLinks(section, url, text, img):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<strong><a href="(.+?)">.+?</a></strong>').findall(content)
        #match1 = re.compile('<h2><strong>Plot Outline.+?</strong></h2>\s*?<p>(.+?)<strong>.+?<a').findall(content)
        listitem = GetMediaInfo(content)
        #for name in match1:
         #       addon.add_directory({'mode': 'GetLinks', 'url': name, 'listitem': listitem, 'text': name, 'img': img}, {'title':' [COLOR lime][B]' + name + '[/B] [/COLOR]'}, img= img, fanart=FanartPath + 'fanart.jpg')
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem}, {'title': host }, img= img, fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def PlayVideo(url, listitem):
    try:
        print 'in PlayVideo %s' % text
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^^^ Press back ^^^[/B] [/COLOR]'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
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


def GetSearchQuery():
	last_search = addon.load_data('search')
	if not last_search: last_search = ''
	keyboard = xbmc.Keyboard()
        keyboard.setHeading('[COLOR green][B]Search tv shows[/B][/COLOR]')
	keyboard.setDefault(last_search)
	keyboard.doModal()
	if (keyboard.isConfirmed()):
                query = keyboard.getText()
                addon.save_data('search',query)
                Search(query)
	else:
                return

        
def Search(query):
        url = 'http://coolmoviezone.net/index.php?s=' + query
        print url
        html = net.http_GET(url).content
        match = re.compile('''<div style=".+?" class="wp-caption alignnone"><img class="" src="(.+?)" alt="(.+?)" width=".+?" height=".+?" /><p class="wp-caption-text">.+?</p></div>\s*?<p> <a href="(.+?)#.+?"''').findall(html)
        for img, title, url in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url}, {'title':  title}, img= img, fanart=FanartPath + 'fanart.jpg')
        setView('tvshows', 'tvshows-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

###################################################################### menus ####################################################################################################

def MainMenu(url, text):    #homescreenserie
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/'}, {'title':  '[COLOR blue][B]A to Z[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles2', 'section': 'ALL', 'url': BASE_URL + '/'}, {'title':  '[COLOR blue][B]Genres[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles4', 'section': 'ALL', 'url': BASE_URL + '/'}, {'title':  '[COLOR blue][B]Year[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles1', 'section': 'ALL', 'url': BASE_URL + '/movies/'}, {'title':  '[COLOR blue][B]All Movies[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles3', 'section': 'ALL', 'url': BASE_URL + '/tag/featured-movies-online/'}, {'title':  '[COLOR blue][B]Featured [/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'GetTitles3', 'section': 'ALL', 'url': BASE_URL + '/tag/browse-year-2015/'}, {'title':  '[COLOR blue][B]Latest[/B] [/COLOR]>>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')

        addon.add_directory({'mode': 'GetSearchQuery'},  {'title':  '[B][COLOR green]Search[/B][/COLOR] >>'}, img=IconPath + 'icon.png', fanart=FanartPath + 'fanart.jpg')
        addon.add_directory({'mode': 'ResolverSettings'}, {'title':  '[COLOR lemonchiffon][B]For more info on this addon please go to :[COLOR yellow] www.entertainmentrepo.com  [/B][/COLOR]'}, img=IconPath + 'er3.png', fanart=FanartPath + 'fanart.jpg') 
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

#################################################################################################################################################################################

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

#################################################################################################################################################################################


if mode == 'main': 
	MainMenu(url, text)
elif mode == 'GetTitles': 
	GetTitles(url, text)
elif mode == 'GetTitles1': 
	GetTitles1(url, text, img)
elif mode == 'GetTitles2': 
	GetTitles2(url, text)
elif mode == 'GetTitles3': 
	GetTitles3(url, text, img)
elif mode == 'GetTitles4': 
	GetTitles4(url, text)
elif mode == 'GetLinks':
	GetLinks(section, url, text, img)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem)
elif mode == 'GetSearchQuery':
	GetSearchQuery()
elif mode == 'Search':
	Search(query)
elif mode == 'ResolverSettings':
        urlresolver.display_settings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))