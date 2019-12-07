
import urllib
import re
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import os
import geturllib

ADDON   = xbmcaddon.Addon()
TITLE   = '80s Music Videos'
VERSION = '1.0.2'
DIR     = 'plugin.video.80smusicvideos'


_PLAY   = 100
_LETTER = 200
_YEAR   = 300


def main():   
    checkVersion()
    addDecade('80s', 'http://www.80smusicvids.com/')
    addDecade('90s', 'http://www.90smusicvidz.com/')


def addDecade(year, url):
    thumbnail = 'DefaultPlaylist.png'
    u         = sys.argv[0]
    u        += "?url="  + urllib.quote_plus(url)
    u        += "&mode=" + str(_YEAR)
    liz       = xbmcgui.ListItem(year, iconImage=thumbnail, thumbnailImage=thumbnail)

    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
    

def checkVersion():
    prev = ADDON.getSetting('VERSION')
    curr = VERSION

    if prev == curr:
        return

    #new version, inform user of new features
    ADDON.setSetting('VERSION', curr)

    if prev == '0.0.0':
        d = xbmcgui.Dialog()
        d.ok(TITLE, '', 'Now with 90s Music Videos')



def addLetters(url):
    for i in range(65, 91):
        addLetter(url, chr(i))


def addLetter(url, letter):
    thumbnail = 'DefaultPlaylist.png'
    u         = sys.argv[0]
    u        += "?letter=" + letter
    u        += "&mode="   + str(_LETTER)
    u        += "&url="    + urllib.quote_plus(url)
    liz       = xbmcgui.ListItem(letter, iconImage=thumbnail, thumbnailImage=thumbnail)

    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)


def addItem(url, item):
    items = item.split('&a=a">')
    root  = items[0]
    title = items[1]

    url += 'vid/' + root + '.flv'

    thumbnail = 'DefaultPlaylist.png'
    u         = sys.argv[0]
    u        += "?url="   + urllib.quote_plus(url)
    u        += "&title=" + urllib.quote_plus(title)
    u        += "&mode="   + str(_PLAY)
    liz       = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)   

    liz.setProperty("IsPlayable","true")

    xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = False)


def requestLetter(url, letter):
    response = geturllib.GetURL(url, 60*60*24) # 1 day

    r     = 'vid=(.+?)</a>'
    match = re.compile(r).findall(response)

    for item in match:
        if item[0].upper() == letter:
            addItem(url, item)


def play(url, title):    
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()    

    liz = xbmcgui.ListItem (title)

    liz.setInfo( type="Video", infoLabels={ "Title": title} )
    liz.setPath(url)

    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)

    #pl.add(url, liz)
    #xbmc.Player().play(pl)
    

def get_params():
    param       = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params        = sys.argv[2]
        cleanedparams = params.replace('?','')

        if params[len(params)-1] == '/':
           params = params[0:len(params)-2]

        pairsofparams = cleanedparams.split('&')
        param         = {}

        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')

            if len(splitparams) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


geturllib.SetCacheDir(xbmc.translatePath(os.path.join("special://profile", "addon_data", DIR,'cache')))


params = get_params()
mode   = None
url    = None

try:
    mode=int(params["mode"])
except:
    pass

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass


if mode == None:
    main()

elif mode == _PLAY:  
    try:
        title = urllib.unquote_plus(params["title"])  
        play(url, title)
    except:
        pass

elif mode == _LETTER:
    try:
        letter = urllib.unquote_plus(params["letter"])
        requestLetter(url, letter)
    except:
        pass

elif mode == _YEAR:
    addLetters(url)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
