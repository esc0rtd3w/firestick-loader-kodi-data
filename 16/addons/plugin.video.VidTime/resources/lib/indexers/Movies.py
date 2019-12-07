import xbmc,requests,json, os
import sys, re, urllib,urllib2,urlparse
from resources.lib.modules import control

path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.VidTime/'))
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
thisPlugin = int(sys.argv[1])
base_url = sys.argv[0]
args = urlparse.parse_qs(sys.argv[2][1:])
icon = path+'icon.png'

def TEST():
    return
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
           
def OPEN_URL(url):
    headers = {}
    headers['User-Agent'] = User_Agent
    link = requests.get(url, headers=headers, allow_redirects=False).text
    link = link.encode('ascii', 'ignore').decode('ascii')
    return link
def MOVIECAT(image,fanart):
    url = 'http://m4ufree.info/'
    addDirectoryItem('[B]ALL[/B]','NEWMOVE',image, image, fanart,str(url))
    addDirectoryItem('[B]TOP VIEWED[/B]','NEWMOVE',image, image, fanart,str(url)+'top-view')
    #addDirectoryItem('[B]LATEST ADDED - Not all recent[/B]','NEWMOVE',image, image, fanart,str(url)+'newupdate')
    addDirectoryItem('[B]GENRE[/B]','GENRE',image, image, fanart,'Genre')
    addDirectoryItem('[B]YEAR[/B]','GENRE',image, image, fanart,'Year')
    addDirectoryItem('[B]SEARCH[/B]','SEARCH',image, image, fanart,'http://m4ufree.info/tag/')
    endDirectory()
def CLEAR():
    xbmc.executebuiltin('XBMC.Container.Update(path,replace)')
def GENRE(url,image,fanart):
    print 
    a = OPEN_URL('http://m4ufree.info/')
    if url == 'Genre':list = re.findall('<a href="(http://m4ufree\.info/movie-.+?)" title=".+?">(.+?)</a>',str(a))
    if url == 'Year':list = re.findall('<a href="(http://m4ufree\.info/year-.+?)" title=".+?">(.+?)</a>',str(a))
    for i in list:
        addDirectoryItem('[B]'+i[1]+'[/B]','NEWMOVE',image,image,fanart,i[0])
    endDirectory()
def SEARCH(url,fanart):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('VIDTIME MOVIES SEARCH')
    keyboard.doModal()
    if keyboard.isConfirmed(): 
        search = keyboard.getText()
        search = re.sub(r'\W+|\s+','-', search)
        NEWMOVE(str(url)+str(search),fanart)
def NEWMOVE(url,fanart):
    curl = url
    a= OPEN_URL(str(url))
    a = str(a).replace('\n','').replace('\r','')
    dclass = re.findall('<div class="item">(.+?)</div>',str(a))
    if ('tvshow') in url:dclass = re.findall('<div class="item">(.+?)"clear:both;"',str(a))
    for i in dclass:
            
            image = re.findall('src= (.+?) ',i)[0]
            
            url = re.findall('href="(.+?)"',i)[0]
            try:
                title = re.findall('alt="(.+?)"',i)[0].replace('Watch free full Movie Online ','').replace('amp;','').upper()
            except:
                title = re.findall('alt=(.+?)>',i)[0].replace('Watch free full Movie Online ','').replace('amp;','').upper()
            
            try:b = OPEN_URL(url)
            except:pass
            try:url = re.findall('<h3 class="h3-detail"> <a  href="(.+?)"',str(b))[0]
            except:pass
         
            addDirectoryItem('[B]'+title+'[/B]','NMP',image, image, fanart,url)
    next = re.findall('waves-button waves-effect" href="(.+?)">(.+?)</a>',str(a))
    image=icon
    for i in next:
        url = i[0]  
        title = 'PAGE '+i[1]
        if not '...' in title and not url == curl: addDirectoryItem('[COLOR red][I]'+title+'[/COLOR][/I]','NEWMOVE',image,image,fanart,str(url))
    addDirectoryItem('[B]EXIT VIDTIME...[/B]','CLEAR',image,image,fanart,'')
    endDirectory()
       
def NMP(url):
    c = OPEN_URL(url)
    
    d = re.findall('href="(.+?\.html)"',str(c))[0]
    c = OPEN_URL(d)
    
    
    
    try:      
        f = re.findall('".(/view\.php\?v=.+?)"',str(c))[0]
        url = 'http://m4ufree.info'+str(f)
        player().run(url)       
    except: 
        pass
        
        
            
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
