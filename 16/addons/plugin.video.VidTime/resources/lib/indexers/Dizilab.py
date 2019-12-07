# -*- coding: utf-8 -*-

import xbmc,json
import re,sys,urllib,urlparse,base64,urllib2
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cloudflare

thisPlugin = int(sys.argv[1])
base_url = sys.argv[0]
args = urlparse.parse_qs(sys.argv[2][1:])

def TEST():
    return

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def CCTV(fanart):
    try:
        url = 'http://dizilab.com/'
        result = cloudflare.request(url)
        items = client.parseDOM(result, 'div', attrs={'class':'tv-series-list'})
        title = client.parseDOM(items, 'li')
        page = client.parseDOM(title, 'a', ret='href')
        image = client.parseDOM(title,'img',ret='src')
        name = client.parseDOM(title, 'span', attrs={'class' : 'title'})
        part = client.parseDOM(title, 'span', attrs={'class' : 'alt-title'})

        season = []
        C = 0
        for item in part:
            item = re.sub('\n|\W{3,}','',item)
            item = item.encode('utf-8')
            result = item.replace('sezon', 'S').replace('bölüm','E').replace('.','').split(' ')
            if len(result) >= 4:
                if len(result[0]) == 1: result[0] = '0'+result[0]
                if len(result[2]) == 1: result[2] = '0'+result[2]
                final = result[1]+result[0]+result[3]+result[2]
                i = name[C].encode('utf-8')
                
                i = re.sub('\n|\W{3,}|amp;','',i)
                
                mate = (i + '- ' +str(final)).upper()
                season.append(mate)
                C = C + 1
            else:pass
        files = zip(page,image,season)
        for items in files:
            image = items[1].replace('_thumb','_cover').split('?')[0]+'?raw=true'.encode('utf-8')
            url = items[0].encode('utf-8')
            title = client.replaceHTMLCodes(items[2])
            
            addDirectoryItem('[B]'+title+'[/B]','CCfind',image, image, fanart,url)
            
        endDirectory()
    except:pass

    
def CCfind(url):
    url = str(url)+'?Altyazısız'
    result = cloudflare.request(str(url))
    if re.search('https://openload',str(result)):
        url = re.findall('"(https://openload.+?)"',str(result))[0]
        import urlresolver
        url = urlresolver.HostedMediaFile(url).resolve() 
    else:   
        url = re.compile('webkit-playsinline="" src="(.+?)"').findall(result)
        url =[]
        
        for item in streams:
            if item.endswith('=m22') or item.endswith('=m18') or item.endswith('=m37'):
                url.append(item)
            elif ('mp4?') in item:
                url.append(item)
            else:
                pass       
        quality = len(url)-1
        url = url[quality].encode('utf-8') 

    player().run(url)  
    

    
def addDirectoryItem(name, action, thumb, image, fanart, url='0'):
    
    thumb = image
    u = build_url({'mode' : str(action),'image': image,'fanart': fanart,'url':url})
    item = control.item(name, iconImage=image, thumbnailImage=thumb)
    item.addContextMenuItems([], replaceItems=False)
    item.setProperty('Fanart_Image', fanart)
    control.addItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)


def endDirectory():
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
       
    
