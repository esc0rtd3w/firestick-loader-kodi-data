import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib, urllib2
import re, string, sys, os
import urlresolver
from TheYid.common.addon import Addon
from TheYid.common.net import Net
from htmlentitydefs import name2codepoint as n2cp
import HTMLParser

addon_id = 'plugin.video.ts80k'
plugin = xbmcaddon.Addon(id=addon_id)
DB = os.path.join(xbmc.translatePath("special://database"), 'ts80k.db')
BASE_URL = 'http://www.santaseries.com/'
net = Net()
addon = Addon('plugin.video.ts80k', sys.argv)

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
def GetTitles(url, text, img):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        #match1 = re.compile("<br/>\s*?Synopsis: (.+?)\s*?</div>").findall(content)
        match = re.compile('<div class="episodiotitle">\s*?<a href="(.+?)">\s*?(.+?)\s*?</a>').findall(content)
        #for name in match1:
                #addon.add_directory({'mode': 'GetLinks', 'url': name, 'listitem': listitem, 'text': name.strip(), 'img' : img}, {'title': '[COLOR blue][B]' + name.strip() + '[/COLOR][/B]'}, img= img, fanart=FanartPath + 'fanart.jpg')
        for url, name in match:
                addon.add_directory({'mode': 'GetLinks', 'url': url, 'listitem': listitem, 'text': name.strip(), 'img' : img}, {'title': name.strip()}, img= img, fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetTitles1(url, text, img):
    try:
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match1 = re.compile("<br/>\s*?Synopsis: (.+?)\s*?</div>").findall(content)
        match = re.compile("<li><a href='http://tvonline.tw/(.+?)' title='Wtach.+?online'><strong>(.+?)</strong>(.+?)</a></li>").findall(content)
        for name in match1:
                addon.add_directory({'mode': 'GetLinks', 'url': name, 'listitem': listitem, 'text': name.strip(), 'img' : img}, {'title': '[COLOR blue][B]' + name.strip() + '[/COLOR][/B]'}, img= img, fanart=FanartPath + 'fanart.jpg')
        for url, name, name1 in match:
                addon.add_directory({'mode': 'GetLinks', 'url': 'http://tvonline.tw/' + url, 'listitem': listitem, 'text': name.strip(), 'img' : img}, {'title': name.strip() + ' ' + name1}, img= img, fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    except:
       	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetLinks(section, url, text, img):
        html = net.http_GET(url).content
        listitem = GetMediaInfo(html)
        content = html
        match = re.compile('<a href="(.+?)" target="_blank">').findall(content)
        listitem = GetMediaInfo(content)
        for url in match:
                host = GetDomain(url)
                if urlresolver.HostedMediaFile(url= url):
                        addon.add_directory({'mode': 'PlayVideo', 'url': url, 'listitem': listitem, 'img' : img}, {'title':  host }, img= img, fanart=FanartPath + 'fanart.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))


def PlayVideo(url, listitem, img):
    try:
        print 'in PlayVideo %s' % text
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player().play(stream_url)
        addon.add_directory({'mode': 'help'}, {'title':  '[COLOR slategray][B]^^^ Press back ^^^[/B] [/COLOR]'}, img=img, fanart=FanartPath + 'fanart.jpg')
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

###################################################################### menus ####################################################################################################

def MainMenu(url, img, text):    #homescreenserie
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/the-a-team/', 'img' : 'http://travelblog.portfoliocollection.com/images/A-Team-Movie-Poster.jpg'}, {'title':  '[COLOR blue][B]The A-Team (1983)[/B] [/COLOR]>>'}, img= 'http://travelblog.portfoliocollection.com/images/A-Team-Movie-Poster.jpg', fanart= 'https://adameastondotcom.files.wordpress.com/2014/05/a-team.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/airwolf/', 'img' : 'http://ecx.images-amazon.com/images/I/910i7M-sOgL._SL1500_.jpg'}, {'title':  '[COLOR blue][B]Airwolf (1984)[/B] [/COLOR]>>'}, img= 'http://ecx.images-amazon.com/images/I/910i7M-sOgL._SL1500_.jpg', fanart= 'https://mindreels.files.wordpress.com/2015/03/airwolf2.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/knight-rider/', 'img' : 'https://upload.wikimedia.org/wikipedia/en/b/b5/Knight_Rider_season_1_DVD.png'}, {'title':  '[COLOR blue][B]Knight Rider (1982)[/B] [/COLOR]>>'}, img= 'https://upload.wikimedia.org/wikipedia/en/b/b5/Knight_Rider_season_1_DVD.png', fanart= 'https://lh3.ggpht.com/iQltD9YoehRbIbFdleRN1TE9Se7EZihXSH_Y36NVcB74tvyOIuT59hRMbXB7MDZhwr-sGQ=w1264')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/blue-thunder/', 'img' : 'http://ecx.images-amazon.com/images/I/51MTG3B61CL.jpg'}, {'title':  '[COLOR blue][B]Blue Thunder (1984)[/B] [/COLOR]>>'}, img= 'http://ecx.images-amazon.com/images/I/51MTG3B61CL.jpg', fanart= 'http://spinoff.comicbookresources.com/wp-content/uploads/2015/03/blue-thunder.jpg')
        #addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/street-hawk-1985/', 'img' : 'http://www.scifi-movies.com/images/contenu/data/0003380/affiche-tonnerre-mecanique-street-hawk-1985-1.jpg'}, {'title':  '[COLOR blue][B]Street Hawk (1985)[/B] [/COLOR]>>'}, img= 'http://www.scifi-movies.com/images/contenu/data/0003380/affiche-tonnerre-mecanique-street-hawk-1985-1.jpg', fanart= 'http://www.streethawkonline.com/Wallpapers/StreetHawk_02_800x600.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + 'watch-tvshows/red-dwarf/', 'img' : 'http://ecx.images-amazon.com/images/I/41-8sKNcXnL.jpg'}, {'title':  '[COLOR blue][B]Red Dwarf (1988)[/B] [/COLOR]>>'}, img= 'http://ecx.images-amazon.com/images/I/41-8sKNcXnL.jpg', fanart= 'http://static.comicvine.com/uploads/original/11/113883/4012095-7578756264-biRLb.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/galactica-1980/', 'img' : 'https://i.jeded.com/i/galactica-1980-first-season.26199.jpg'}, {'title':  '[COLOR blue][B]Galactica (1980)[/B] [/COLOR]>>'}, img= 'https://i.jeded.com/i/galactica-1980-first-season.26199.jpg', fanart= 'https://lh4.ggpht.com/YE0os7_aPCh_wkelRHNTHDecsEB8bC4qtqoObkAi_a_TeQpkC1Y2VNl4o4Lz5pMLT6k=w1264')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/the-hitchhiker/', 'img' : 'http://ecx.images-amazon.com/images/I/51pZriFzfhL._AC_UL320_SR224,320_.jpg'}, {'title':  '[COLOR blue][B]The Hitchhiker (1983)[/B] [/COLOR]>>'}, img= 'http://ecx.images-amazon.com/images/I/51pZriFzfhL._AC_UL320_SR224,320_.jpg', fanart= 'https://i.ytimg.com/vi/diZ1SLDLKww/maxresdefault.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/spitting-image/', 'img' : 'https://upload.wikimedia.org/wikipedia/en/a/a2/Spitting_Image_Cover.jpg'}, {'title':  '[COLOR blue][B]Spitting Image (1984)[/B] [/COLOR]>>'}, img= 'https://upload.wikimedia.org/wikipedia/en/a/a2/Spitting_Image_Cover.jpg', fanart= 'http://home.bt.com/images/royal-family-spitting-image-characters-136387946136702601-140226142836.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/quantum-leap/', 'img' : 'http://ecx.images-amazon.com/images/I/91ZKsyE2LXL._SL1500_.jpg'}, {'title':  '[COLOR blue][B]Quantum Leap (1989)[/B] [/COLOR]>>'}, img= 'http://ecx.images-amazon.com/images/I/91ZKsyE2LXL._SL1500_.jpg', fanart= 'http://blogs-images.forbes.com/curtissilver/files/2015/10/quantumleap.jpg')

        #addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/the-hitch-hikers-guide-to-the-galaxy-1981/', 'img' : 'https://nettikmovie.files.wordpress.com/2007/05/hitchhikers-guide-galaxy-03.jpg'}, {'title':  '[COLOR blue][B]The hitch hikers guide to the galaxy (1981)[/B] [/COLOR]>>'}, img= 'https://nettikmovie.files.wordpress.com/2007/05/hitchhikers-guide-galaxy-03.jpg', fanart= 'http://33.media.tumblr.com/tumblr_lety6yOKz31qzr8nao1_500.gif')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/only-fools-and-horses/', 'img' : 'http://www.listsworld.com/wp-content/uploads/2013/02/only-fools-and-horses.jpg'}, {'title':  '[COLOR blue][B]Only Fools and Horses (1981)[/B] [/COLOR]>>'}, img= 'http://www.listsworld.com/wp-content/uploads/2013/02/only-fools-and-horses.jpg', fanart= 'http://i.huffpost.com/gen/1544078/images/o-ONLY-FOOLS-AND-HORSES-facebook.jpg')
        #addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/v-1984-1984/', 'img' : 'http://thumbs2.ebaystatic.com/d/l225/m/meuKILw5SZ9uwRyciaWwZ1w.jpg'}, {'title':  '[COLOR blue][B]V (1984)[/B] [/COLOR]>>'}, img= 'http://thumbs2.ebaystatic.com/d/l225/m/meuKILw5SZ9uwRyciaWwZ1w.jpg', fanart= 'http://www.coronacomingattractions.com/sites/default/files/news/V-2009_TV_series_logo.jpg')
        #addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/v-the-final-battle-1984/', 'img' : 'http://4.bp.blogspot.com/-XJJng6hTzKE/Uuvw39J-y6I/AAAAAAAAImA/0H2zeAsnOgc/s1600/a+V+2.jpg'}, {'title':  '[COLOR blue][B]V the Final Battle (1984)[/B] [/COLOR]>>'}, img= 'http://4.bp.blogspot.com/-XJJng6hTzKE/Uuvw39J-y6I/AAAAAAAAImA/0H2zeAsnOgc/s1600/a+V+2.jpg', fanart= 'http://vignette3.wikia.nocookie.net/vwikia/images/4/40/V_tv_series_400.jpg/revision/latest?cb=20091128014648')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/magnum-pi/', 'img' : 'http://static2.opensubtitles.org/gfx/thumbs/0/4/6/9/0639640.jpg'}, {'title':  '[COLOR blue][B]Magnum Pi (1980)[/B] [/COLOR]>>'}, img= 'http://static2.opensubtitles.org/gfx/thumbs/0/4/6/9/0639640.jpg', fanart= 'http://www.gadgetshowprizes.co.uk/wp-content/uploads/2014/06/Magnum-PI-3.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/miami-vice/', 'img' : 'http://cache.coverbrowser.com/image/bestselling-movies-2006/3730-1.jpg'}, {'title':  '[COLOR blue][B]Miami Vice (1984)[/B] [/COLOR]>>'}, img= 'http://cache.coverbrowser.com/image/bestselling-movies-2006/3730-1.jpg', fanart= 'http://www.oldskooldepartment.com/attachments/miami-vice-13-jpg.177/')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/21-jump-street/', 'img' : 'http://1.fwcdn.pl/po/62/33/106233/7439895.3.jpg'}, {'title':  '[COLOR blue][B]21 Jump Street (1987)[/B] [/COLOR]>>'}, img= 'http://1.fwcdn.pl/po/62/33/106233/7439895.3.jpg', fanart= 'http://images.starpulse.com/news/bloggers/6/blog_images/21-jump-street-cast.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/macgyver/', 'img' : 'http://www.iceposter.com/thumbs/MOV_34d8a6b3_b.jpg'}, {'title':  '[COLOR blue][B]MacGyver (1985)[/B] [/COLOR]>>'}, img= 'http://www.iceposter.com/thumbs/MOV_34d8a6b3_b.jpg', fanart= 'http://www.the-medium-is-not-enough.com/images/Macgyver-031609.jpg')

        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/thundercats/', 'img' : 'http://img.soundtrackcollector.com/movie/large/Thundercats_(1985).jpg'}, {'title':  '[COLOR gold][B]Thundercats (1985)[/B] [/COLOR]>>'}, img= 'http://img.soundtrackcollector.com/movie/large/Thundercats_(1985).jpg', fanart= 'http://mygenerationtoys.com/images/Thundercats%20Poster%2003.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/he-man-and-the-masters-of-the-universe/', 'img' : 'http://3.bp.blogspot.com/-H5xQKNYJryc/UTdtgk-s4OI/AAAAAAAAFuE/f3pHLmpverU/s1600/He-Man.jpg'}, {'title':  '[COLOR gold][B]He man and the masters of the universe (1984)[/B] [/COLOR]>>'}, img= 'http://3.bp.blogspot.com/-H5xQKNYJryc/UTdtgk-s4OI/AAAAAAAAFuE/f3pHLmpverU/s1600/He-Man.jpg', fanart= 'http://www.posters57.com/images/He_Man.jpg=600.jpeg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/dungeons-dragons/', 'img' : 'http://ia.media-imdb.com/images/M/MV5BMTYxMzY4OTY0OV5BMl5BanBnXkFtZTcwMTgxODkzMQ@@._V1_SY317_CR10,0,214,317_AL_.jpg'}, {'title':  '[COLOR gold][B]Dungeons and Dragons (1983)[/B] [/COLOR]>>'}, img= 'http://ia.media-imdb.com/images/M/MV5BMTYxMzY4OTY0OV5BMl5BanBnXkFtZTcwMTgxODkzMQ@@._V1_SY317_CR10,0,214,317_AL_.jpg', fanart= 'http://www.lifedaily.com/wp-content/uploads/2013/05/Dungeons-Dragons-1983.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/the-transformers/', 'img' : 'http://ia.media-imdb.com/images/M/MV5BMTg0NTc4NzA2MF5BMl5BanBnXkFtZTcwMDc0NTQyMQ@@._V1._CR19,2,308,430_SY317_CR6,0,214,317_AL_.jpg'}, {'title':  '[COLOR gold][B]Transformers (1984)[/B] [/COLOR]>>'}, img= 'http://ia.media-imdb.com/images/M/MV5BMTg0NTc4NzA2MF5BMl5BanBnXkFtZTcwMDc0NTQyMQ@@._V1._CR19,2,308,430_SY317_CR6,0,214,317_AL_.jpg', fanart= 'http://www.geekworldordersite.com/blog/wp-content/uploads/2013/07/G1_Logo-1024x689.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/mister-t/', 'img' : 'http://ecx.images-amazon.com/images/I/51ilh4OzLAL.jpg'}, {'title':  '[COLOR gold][B]Mr. T (1983)[/B] [/COLOR]>>'}, img= 'http://ecx.images-amazon.com/images/I/51ilh4OzLAL.jpg', fanart= 'http://sp4.fotolog.com/photo/4/33/41/losochentas_com/1173293358_f.jpg')
        addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '/watch-tvshows/top-cat/', 'img' : 'http://www.newkadia.com/Covers/L/T/Top%20Cat%201961%20series/topcat1961series21.jpg'}, {'title':  '[COLOR gold][B]Top Cat (1961)[/B] [/COLOR]>>'}, img= 'http://www.newkadia.com/Covers/L/T/Top%20Cat%201961%20series/topcat1961series21.jpg', fanart= 'http://atbishopsgate.com/wp-content/uploads/2014/07/Top-Cat-17.jpg')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

        #addon.add_directory({'mode': 'GetTitles', 'section': 'ALL', 'url': BASE_URL + '', 'img' : ''}, {'title':  '[COLOR blue][B]()[/B] [/COLOR]>>'}, img= '', fanart= '')
#################################################################################################################################################################################

if mode == 'main': 
	MainMenu(url, img, text)
elif mode == 'GetTitles': 
	GetTitles(url, text, img)
elif mode == 'GetTitles1': 
	GetTitles1(url, text, img)
elif mode == 'GetLinks':
	GetLinks(section, url, text, img)
elif mode == 'PlayVideo':
	PlayVideo(url, listitem, img)
xbmcplugin.endOfDirectory(int(sys.argv[1]))