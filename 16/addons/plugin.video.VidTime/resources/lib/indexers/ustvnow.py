import xbmc,requests,json, os,base64
import sys, re, urllib,urllib2,urlparse
from default import english
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

pUrl='https://dl.dropboxusercontent.com/s/gsi57fqqkosg073/247%20shows.xml'
result = OPEN_URL(pUrl)

#variable=re.findall('<uslivetv>([^>]+)</uslivetv>',result)[0]
variable=base64.b64encode('ogwpjllcxnnzqa4chwcdydcz6hwq')
xbmc.log('chekit1 '+str(base64.b64decode(variable)))
def CHList(fanart):
    link=OPEN_URL(english('Vm10V2IyTnJOVmhWYTFwc1UwWJsV20aN1mFXRmx0TlVOamJGVjNWMjVrVGxadGVIaFdSekYzWVRGYWRHUkVWbFZOVjJoVVZrWlZlR1JHVmxsYVIwWlRUVzVOZDFkc1ZsZE5NbFpZVm10c1VtSllVbkJXYlhoYVpWWmtWVkZ0ZEU5U01GcEpWbTE0YjJGV1RrZFhiV2hWVmpOQ1dGUlhlSGRUVjBvMlZtczFVMDFIZHpGWGExWnJUa2RHV0ZKdVJsSldSM001L1ZtMHdkMlZIVVhoVFdHaHBVbTFTV1ZZd1pEUldWbGwzV2tjNVdGSnNiRE5YYTFwUFZsVXhWMk5JY0ZoaE1rMHhWbXBLUzFOSFZrZFhiRnBwVmtWYVNWZFdaRFJUTWxKWFVtNU9hVkp1UWs5VmJYaDNWRlphYzFadFJsZE5WbkJYVkZaV1YyRkhWbkZSVkdzOQ=='+base64.b64decode(variable)))
    data=json.loads(link)
    data=data["results"]
    for var in data:
        url=english('VmtWb2NrNVhVa1psU0ZaJsV16aN1WFltNUNjbFV3V25kTlZteHhWRzF3YTFadGREVlVNV2hUVkZVeGRHVkVUbHBXVjAweFdrWmFkMVpGT1VsaFJURk9ZbTFvTTFkclkzaFdiVkowVlc1U2FWSXphSEpVVnpWdlpERndTRTFXV2sxTmF6RTJWbGMxYzFsV1dYZFhha0phWWxSR1NGcEZXbmRXVlRGRlRVUXdQUT09L1ZtMHhkMUl4YkZkWFdHeFVWMGRvV0ZZd1pGTlVNVnB6V2tjNVYySkhlRlpWYlRGSFlXeEtkVkZzYkZwTlJscE1WbFZhVjFaVk1VVmhlakE5')+var['stream']+'&stream_origin='+var['stream_origin']+'&app_name='+var['app_name']+'&token='+base64.b64decode(variable)+'&passkey=tbd&extrato=tbd'
        thumb='http://m.ustvnow.com/'+var['img'].replace('\/','/')
        plot=var['description']
        xbmc.log('chekit1 '+str(url))
        addDirectoryItem('[B][COLOR yellow]'+var['stream_code']+'[/COLOR][/B] :[COLOR red]'+var['title']+'[/COLOR]','CHPLAY',thumb, plot, fanart,url)
    endDirectory()
def CLEAR():
    xbmc.executebuiltin('XBMC.Container.Update(path,replace)')

       
def CHPlay(url):
    link = OPEN_URL(url)
    stream  = re.findall('src="([^"]+)"',link)[0]
    if '4.4.4.4' in stream:
        #xbmc.executebuiltin("XBMC.Notification(Server Offline!,Try Again Later,3000,"+icon+")")
        #return
        stream=stream.split('?')[0]
        stream=stream+'?hdnea=ip=73.200.150.164~st=1479686400~exp=1479715200~acl=/*~hmac=b06a0d9c7c59bda9401293b68e02e92efc0c89a5d0041f25ec451954253d8736'
    player().run(stream) 
        
            
def addDirectoryItem(name, action, thumb, plot, fanart, url='0'):   
    u = build_url({'mode' : str(action),'image': thumb,'fanart': fanart,'url':url})
    item = control.item(name, iconImage=thumb, thumbnailImage=thumb)
    item.addContextMenuItems([], replaceItems=False)
    item.setProperty('Fanart_Image', fanart)
    item.setInfo( type="Video", infoLabels={'plot': plot})
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
