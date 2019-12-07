# -*- coding: utf-8 -*-

import xbmc,xbmcgui,json,sys
import re,sys,urllib,urlparse,base64,urllib2
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cloudflare
from resources.lib.modules import cache

mediaPath = control.addonInfo('path') + '/resources/media/vidtoon/'
thisPlugin = int(sys.argv[1])
base_url = sys.argv[0]
args = urlparse.parse_qs(sys.argv[2][1:])

def TEST():
    return

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def VidToon():
    addDirectoryItem('[B]Cartoon Craze[/B]','VCartoonCraze', '0', mediaPath+'VidToonsLogo.png', mediaPath+'VidToons.png')
    addDirectoryItem('[B]Anime[/B]','VAnime', '0', mediaPath+'AnimeLogo.png', mediaPath+'Anime.png')
    endCategory()

def VAnime(image, fanart):
    addDirectoryItem('[B]NEWEST[/B]', 'VAcat', '0', image, fanart,'AnimeList/Newest')
    addDirectoryItem('[B]LATEST UPDATED[/B]', 'VAcat', '0', image, fanart,'AnimeList/LatestUpdate')
    #addDirectoryItem('[B]LIST (A-Z)[/B]', 'VAalpha', '0', image, fanart,'')
    addDirectoryItem('[B]GENRES[/B]', 'VAgenres', '0', image, fanart,'')
    addDirectoryItem('[B]SEARCH[/B]', 'VAsearch', '0', image, fanart, '')
    endDirectory()

def VAalpha(image,fanart):
    try:    
        url = 'http://kissanime.to/AnimeList/'
        result = cloudflare.request(url)
        items = client.parseDOM(result, 'div', attrs={'class' : 'alphabet'})
        title = client.parseDOM(items, 'a')
        addy = client.parseDOM(items, 'a', ret='href')
        list = zip(title,addy)
        for item in list:
            url = 'AnimeList/'+item[1]
            if item[0] == "All":url = item[1]
            url = url.encode('utf-8')
            addDirectoryItem('[B]'+item[0]+'[/B]', 'VAcat', image, image, fanart, url)
        endDirectory()
    except:
        pass
    
def VAgenres(image,fanart):
    try:
        url = 'http://kissanime.to/AnimeList/'

        result = cloudflare.request(url)

        items = client.parseDOM(result, 'div', attrs={'id': 'container'})
        items = client.parseDOM(items, 'div', attrs={'id': 'rightside'})
        items = client.parseDOM(items, 'div', attrs={'class': 'barContent'})[1]       
        items = client.parseDOM(items, 'a', ret='href')
    except:
        return

    for item in items:
        try:
            name = '[B]'+ item[7:] +'[/B]'
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem(name, 'VAcat', image, image, fanart, url)
        except:
            pass

    endDirectory()

def VAcat(url, image, fanart):
    try:
        url = urlparse.urljoin('http://kissanime.to/', url)

        result = cloudflare.request(url)
        result = re.sub('<tr\s+.+?>', '<tr>', result)

        items = client.parseDOM(result, 'tr')
    except:
        return
        
    for item in items:
        try:
            name = client.parseDOM(item, 'a')[0]
            name = re.sub('\n|\W{3,}','',name)
            
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')
           
            info = client.parseDOM(item, 'p')[0]
            info = client.replaceHTMLCodes(info)
            info = re.sub('\W{2,}','',info)
            info = info.encode('utf-8')
            
            url = client.parseDOM(item, 'a', ret='href')[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            thumb = client.parseDOM(item, 'img', ret='src')[0]
            thumb = client.replaceHTMLCodes(thumb)
            
            thumb = thumb.encode('utf-8')
           
            cookie = cloudflare.justcookie(thumb)
           
            cookie = cookie.split(';ASP')[0]
            image = thumb+cookie
            addDirectoryItem('[B]'+name+'[/B]', 'VApart', image, image, fanart, url)
        except:
            pass

    try:
        next = client.parseDOM(result, 'ul', attrs={'class': 'pager'})[0]
        next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
        next = [i[0] for i in next if 'Next' in i[1]][0]

        addDirectoryItem('[I]NEXT[/I]', 'VAcat', image, image, fanart, next)
    except:
        pass

    movieCategory()

def VApart(url, image, fanart):
    try:
        url = urlparse.urljoin('http://kissanime.to/', url)

        result = cloudflare.request(url)

        items = client.parseDOM(result, 'table', attrs={'class': 'listing'})
        items = client.parseDOM(items, 'td')
        items = zip(client.parseDOM(items, 'a', ret='href'), client.parseDOM(items, 'a'))
        if len(items) == 1: return VAstream(items[0][0])
    except:
        return

    for item in items[::-1]:
        try:
            name = item[1]
            name = re.sub('\n|\W{3,}','',name)
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem('[B]'+name+'[/B]','VAstream',image,image,fanart,url)
        except:
            pass

    episodeCategory()

def VAsearch(image, fanart):
    keyboard = control.keyboard()
    keyboard.setHeading('ANIME SEARCH')
    keyboard.doModal()

    if not keyboard.isConfirmed(): return

    search = keyboard.getText()
    search = re.sub(r'\W+|\s+','-', search)
    if search == '': return

    url = '/Search/Anime/'+search
    url = url.encode('utf-8')

    VAcat(url, image, fanart)

def resolved(url):
    import urlresolver
    u = urlresolver.HostedMediaFile(url).resolve()  
    return u

def VAstream(url):
    try:
        url = urlparse.urljoin('http://kissanime.to', url)

        result = cloudflare.request(url)
        items = client.parseDOM(result,'select', attrs={'id':'selectQuality'}) 
        items = client.parseDOM(items, 'option', ret='value')
  
        if not items:
            url = re.findall('divContentVideo.+?iframe.+?src="(.+?)"',str(result))[0]
            player().run(resolved(url))
       
        try:
            url= base64.b64decode(items[0])
            url= url.encode('utf-8')
            
        except:
            pass   
        if len(url) > 1:player().run(url)
    except:
        return
#CARTOON

def VCartoonCraze(image, fanart):

    addDirectoryItem('[B]NEWEST[/B]', 'VCcat', '0', image, fanart,'CartoonList/Newest')
    addDirectoryItem('[B]LATEST UPDATED[/B]', 'VCcat', '0', image, fanart,'CartoonList/LatestUpdate')
    #addDirectoryItem('[B]LIST (A-Z)[/B]', 'VCalpha', '0', image, fanart,'')
    addDirectoryItem('[B]GENRES[/B]', 'VCgenres', image, image, fanart,'')
    addDirectoryItem('[B]SEARCH[/B]', 'VCsearch', image, image, fanart, '')
    endDirectory()

def VCgenres(image,fanart):
    try:
        url = 'http://kisscartoon.me/CartoonList/'

        result = cloudflare.request(url)

        items = client.parseDOM(result, 'div', attrs={'id': 'container'})
        items = client.parseDOM(items, 'div', attrs={'id': 'rightside'})
        items = client.parseDOM(items, 'div', attrs={'class': 'barContent'})[1]       
        items = client.parseDOM(items, 'a', ret='href')
    except:
        return

    for item in items:
        try:
            name = '[B]'+ item[7:] +'[/B]'
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem(name, 'VCcat', image, image, fanart, url)
        except:
            pass

    endDirectory()

def VCalpha(image,fanart):
    try:    
        url = 'http://kisscartoon.me/CartoonList/'
        result = cloudflare.request(url)
        items = client.parseDOM(result, 'div', attrs={'class' : 'alphabet'})
        title = client.parseDOM(items, 'a')
        addy = client.parseDOM(items, 'a', ret='href')
        list = zip(title,addy)
        for item in list:
            url = 'CartoonList/Newest'+item[1]
            if item[0] == "All":url = item[1]
            url = url.encode('utf-8')        
            addDirectoryItem('[B]'+item[0]+'[/B]', 'VCcat', image, image, fanart, url)
        endDirectory()
    except:
        pass
def VCcat(url, image, fanart):
    try:
        url = urlparse.urljoin('http://kisscartoon.me', url)

        result = cloudflare.request(url)
        result = re.sub('<tr\s+.+?>', '<tr>', result)

        items = client.parseDOM(result, 'tr')
    except:
        return
        
    for item in items:
        try:
            name = client.parseDOM(item, 'a')[0]
            name = name.replace('\n', '')
            name = '[B]'+ name +'[/B]'
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')
            
            info = client.parseDOM(item, 'p')[0]
            info = client.replaceHTMLCodes(info)
            info = re.sub('\W{2,}','',info)
            info = info.encode('utf-8')
            
            url = client.parseDOM(item, 'a', ret='href')[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            thumb = client.parseDOM(item, 'img', ret='src')[0]
            #thumb = thumb.replace('kisscartoon.me','cdn-c.whatbest.net')
            thumb = client.replaceHTMLCodes(thumb)
            thumb = thumb.encode('utf-8')
            image = str(thumb)+cloudflare.justcookie(thumb)
            addDirectoryItem(name, 'VCpart', image, image, fanart, url)
        except:
            pass

    try:
        next = client.parseDOM(result, 'ul', attrs={'class': 'pager'})[0]
        next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
        next = [i[0] for i in next if 'Next' in i[1]][0]

        addDirectoryItem('[I]NEXT[/I]', 'VCcat', image, image, fanart, next)
    except:
        pass

    movieCategory()


def VCsearch(image, fanart):
    keyboard = control.keyboard()
    keyboard.setHeading('CARTOON SEARCH')
    keyboard.doModal()

    if not keyboard.isConfirmed(): return

    search = keyboard.getText()
    search = re.sub(r'\W+|\s+','-', search)
    if search == '': return

    url = '/Search/Cartoon/'+search
    url = url.encode('utf-8')

    VCcat(url, image, fanart)


def VCpart(url, image, fanart):
    try:
        url = urlparse.urljoin('http://kisscartoon.me', url)

        result = cloudflare.request(url)

        items = client.parseDOM(result, 'table', attrs={'class': 'listing'})
        items = client.parseDOM(items, 'td')
        items = zip(client.parseDOM(items, 'a', ret='href'), client.parseDOM(items, 'a'))

        if len(items) == 1: return VCstream(items[0][0])
    except:
        return

    for item in items[::-1]:
        try:
            name = item[1]
            name = name.replace('\n', '')
            name = client.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            url = item[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            addDirectoryItem('[B]'+name+'[/B]','VCstream',image,image,fanart,url)
        except:
            pass

    episodeCategory()


def VCstream(url):
    try:
        url = urlparse.urljoin('http://kisscartoon.me', url)
        result = cloudflare.request(str(url)+'&s=openload')
        items = client.parseDOM(result,'select', attrs={'id':'selectQuality'}) 
        items = client.parseDOM(items, 'option', ret='value')      
       
        if not items:
                try:
                    url = re.findall('"(https://openload\.co/.+?.mp4")',str(result))[0]
                except:
                    url = re.findall('"(https://2.bp.blogspot.com/.+?)"',str(result))[0]
                player().run(resolved(url))
       
        
        
    except:
        return
def addDirectoryItem(name, action, thumb, image, fanart, url='0'):
    thumb=image
    u = build_url({'mode' : str(action),'image': image,'fanart': fanart,'url':url})
    item = control.item(name, iconImage=image, thumbnailImage=thumb)
    item.addContextMenuItems([], replaceItems=False)
    item.setProperty('Fanart_Image', fanart)
    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)


def endDirectory():
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def endCategory():
   
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def movieCategory():
    
    control.directory(int(sys.argv[1]), cacheToDisc=True)


def episodeCategory():
    control.directory(int(sys.argv[1]), cacheToDisc=True)


class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def run(self, url):
        title = control.infoLabel('ListItem.Label')
        image = control.infoLabel('ListItem.Icon')
        item = control.item(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo(type='Video', infoLabels = {'title': title})
        control.player.play(url, item)

        for i in range(0, 240):
            if self.isPlayingVideo(): break
            control.sleep(1000)

    def onPlayBackStarted(self):
        control.sleep(200)
       
