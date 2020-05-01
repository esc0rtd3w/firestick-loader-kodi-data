
import urllib
import re
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import os
import geturllib
import json

from simpleYT import yt

ADDON   = xbmcaddon.Addon()
URL     = 'http://www.thegreat80s.com/'
TITLE   = "The Great 80's"
VERSION = '1.0.0'
DIR     = 'theplugin.video.great80s'

_POP    = 100
_METAL  = 200
_ARTIST = 300
_VIDEO  = 400


def main():   
    checkVersion()

    addCategory('Pop Music',   _POP)
    addCategory('Metal Music', _METAL)


def atoz(mode):
    addLetter(mode, '0')
    for i in range(65, 91):
        addLetter(mode, chr(i))


def playVideo(id):
    yt.PlayVideo(id)
    #url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % id    

    #liz = xbmcgui.ListItem('title', iconImage='image', thumbnailImage='image')
    #liz.setInfo( type="Video", infoLabels={ "Title": 'title'} )
    #liz.setPath(url)

    #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


def requestArtist(artist):
    if requestArtistWithMode(artist, _POP):
        return
    requestArtistWithMode(artist, _METAL)


def requestArtistWithMode(artist, mode):
    if mode == _POP:
        url = URL + 'Explore-the-80s.html?band=%s' % artist
    elif mode == _METAL:
        url = URL + 'Explore-80s-Metal.html?band=%s' % artist
    else:
        return False

    response = str(geturllib.GetURL(url, 24 * 3600)) # 24 hr
    respone  = response.replace('\r', '').replace('\n', '').replace('\t', '')

    try:
        response = response.split('var videoarray = ')[1]
        response = response.split('var artistarray = ')[0]

        jsn = json.loads(response.strip()[:-1])

        for item in jsn:
            try:
                id   = item['ID']
                song = item['Song']
                addVideo(song, id)
            except:
                pass
    except:
        return False
    
    return True


def requestLetter(mode, letter):
    if mode == _POP:
        url = '80s-Bands-and-Artists.html?bandletter=%s' % letter
    elif mode == _METAL:
        url = '80s-Metal-Bands.html?bandletter=%s' % letter
    else:
        return

    response = geturllib.GetURL(URL + url, 24 * 3600) # 24 hr

    r     = 'var artistarray = (.+?);'
    match = re.compile(r).findall(response)

    jsn = json.loads(match[0])

    artists = []
    match   = []

    if letter == '0':
        for i in range(0, 9):
            match.append(str(i))
    else:
        match.append(letter)       

    for item in jsn:
        if item[0] in match:
            if item not in artists:
                artists.append(item)
    
    for artist in artists:
        addArtist(artist)


def checkVersion():
    prev = ADDON.getSetting('VERSION')
    curr = VERSION

    if prev == curr:
        return

    #new version, inform user of new features
    ADDON.setSetting('VERSION', curr)


def addLetter(mode, letter, thumbnail = None):
    if not thumbnail:
        thumbnail = 'DefaultPlaylist.png'

    u   = sys.argv[0]
    u  += "?letter=" + letter
    u  += "&mode="   + str(mode)

    if letter == '0':
        letter = '0-9'
    liz = xbmcgui.ListItem(letter, iconImage=thumbnail, thumbnailImage=thumbnail)

    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)


def addCategory(title, mode, thumbnail = None):
    if not thumbnail:
        thumbnail = 'DefaultPlaylist.png'

    u    = sys.argv[0]
    u   += "?mode="   + str(mode)
    liz  = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)   

    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)


def addArtist(artist):
    artist    = artist.strip()
    thumbnail = URL + 'images/Artists/%s.jpg' % artist
    thumbnail = thumbnail.replace(' ', '%20')

    u    = sys.argv[0]
    u   += "?mode="   + str(_ARTIST)
    u   += "&artist=" + urllib.quote_plus(artist) 
    
    liz  = xbmcgui.ListItem(artist, iconImage=thumbnail, thumbnailImage=thumbnail)   

    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)


def addVideo(song, id):
    song      = song.strip()
    thumbnail = 'http://img.youtube.com/vi/%s/1.jpg' % id

    u    = sys.argv[0]
    u   += "?mode=" + str(_VIDEO)
    u   += "&id="   + urllib.quote_plus(id) 
    
    liz  = xbmcgui.ListItem(song, iconImage=thumbnail, thumbnailImage=thumbnail) 

    menu = []
    cmd = 'plugin://plugin.video.youtube/?path=root/video&action=download&videoid=%s' % id
    menu.append(('Download', 'XBMC.RunPlugin(%s)' % cmd))           
    liz.addContextMenuItems(menu)      
    liz.setProperty("IsPlayable","true")

    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)

    
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
           params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param


geturllib.SetCacheDir(xbmc.translatePath(os.path.join("special://profile", "addon_data", DIR,'cache')))


params = get_params()
mode   = None
letter = None
artist = None
id     = None

try:
    mode = int(params['mode'])
except:
    pass

try:
    letter = params['letter']
except:
    pass

try:
    artist = params['artist']
except:
    pass

try:
    id = params['id']
except:
    pass


if mode == None:
    main()

elif mode == _POP or mode == _METAL:  
    if not letter:
        atoz(mode)
    else:
        requestLetter(mode, letter)

elif mode == _ARTIST:  
    requestArtist(artist)

elif mode == _VIDEO:
    playVideo(id)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
