#############################################################################
#
#   Copyright (C) 2013 Navi-X
#
#   This file is part of Navi-X.
#
#   Navi-X is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   Navi-X is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Navi-X.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
user_agent_default = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4';

#############################################################################
import xbmc, sys, os, xbmcaddon, xbmcplugin, urllib2, urllib

Addon = xbmcaddon.Addon()
def SettingG(setting, d=""):
    try:
        return addon.getSetting(setting)
    except:
        return d


def SettingS(setting, value): addon.setSetting(id=setting, value=value)


def gAI(t):
    try:
        return Addon.getAddonInfo(t)
    except:
        return ""


def tfalse(r, d=False):  ## Get True / False
    if (r.lower() == 'true') or (r.lower() == 't') or (r.lower() == 'y') or (r.lower() == '1') or (r.lower() == 'yes'):
        return True
    elif (r.lower() == 'false') or (r.lower() == 'f') or (r.lower() == 'n') or (r.lower() == '0') or (
        r.lower() == 'no'):
        return False
    else:
        return d


def UrlDoGet(url):
    try:
        import urllib2
        req = urllib2.Request(url)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        return link
    except:
        return ''


def UrlDoPost(url, form_data={}):
    try:
        # import urllib2,urllib
        # req=urllib2.Request(url)
        # if len(form_data) > 0:
        # print 'posting information to: '+str(url)
        form_data = urllib.urlencode(form_data)
        req = urllib2.Request(url, form_data)
        
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        return link
    except:
        return ''


def FileDoSave(path, data):
    file = open(path, 'w')
    file.write(data)
    file.close()


def FileDoOpen(path):
    if os.path.isfile(path):  ## File found.
        file = open(path, 'r')
        contents = file.read()
        file.close()
        return contents
    else:
        return ''  ## File not found.


#############################################################################

ACTION_MOVE_LEFT = 1  # Dpad Left
ACTION_MOVE_RIGHT = 2  # Dpad Right
ACTION_MOVE_UP = 3  # Dpad Up
ACTION_MOVE_DOWN = 4  # Dpad Down
ACTION_PAGE_UP = 5  # Left trigger
ACTION_PAGE_DOWN = 6  # Right trigger
ACTION_SELECT_ITEM = 7  # 'A'
ACTION_HIGHLIGHT_ITEM = 8
ACTION_PARENT_DIR = 9  # 'B'
ACTION_PREVIOUS_MENU = 10  # 'Back'
ACTION_SHOW_INFO = 11
ACTION_PAUSE = 12
ACTION_STOP = 13  # 'Start'
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15
ACTION_XBUTTON = 18  # 'X'
ACTION_YBUTTON = 34  # 'Y'
ACTION_MOUSEMOVE = 90  # Mouse has moved
ACTION_MOUSEMOVE2 = 107  # Mouse has moved
ACTION_PREVIOUS_MENU2 = 92  # 'Back'
ACTION_CONTEXT_MENU = 117  # pops up the context menu
ACTION_CONTEXT_MENU2 = 229  # pops up the context menu (remote control "title" button)

#############################################################################
# auto scaling values
#############################################################################

HDTV_1080i = 0  # (1920x1080, 16:9, pixels are 1:1)
HDTV_720p = 1  # (1280x720, 16:9, pixels are 1:1)
HDTV_480p_4x3 = 2  # (720x480, 4:3, pixels are 4320:4739)
HDTV_480p_16x9 = 3  # (720x480, 16:9, pixels are 5760:4739)
NTSC_4x3 = 4  # (720x480, 4:3, pixels are 4320:4739)
NTSC_16x9 = 5  # (720x480, 16:9, pixels are 5760:4739)
PAL_4x3 = 6  # (720x576, 4:3, pixels are 128:117)
PAL_16x9 = 7  # (720x576, 16:9, pixels are 512:351)
PAL60_4x3 = 8  # (720x480, 4:3, pixels are 4320:4739)
PAL60_16x9 = 9  # (720x480, 16:9, pixels are 5760:4739)

#############################################################################
# directory settings
#############################################################################
addon = Addon.getAddonInfo('id')
#addon = xbmcaddon.Addon(id='script.navi-x')
RootDir = Addon.getAddonInfo('path')
datapaths = xbmc.translatePath(Addon.getAddonInfo('profile'))
RootFwdCmd = 'root\\'  # used @ line 138-ish & 161-ish in CPlayList.py
RootFwdCmd2 = 'root/'  # used @ line 141-ish & 164-ish in CPlayList.py
imageBrowse = {}
imageBrowse['Remote'] = 'connection.png'
imageBrowse['HTTP'] = 'icon_html.png'
imageBrowse['FTP'] = 'browser_ftp.png'
imageBrowse['Local'] = 'files.png'
imageBrowse['Cache'] = 'browser_fan.png'
imageBrowse['Image'] = 'icon_image.png'
imageBrowse['Blank'] = 'blank1.png'
imageBrowse['Rewrite'] = 'browser_write.gif'

if RootDir[-1] == ';': RootDir = RootDir[0:-1]
if RootDir[0] == '/':
    if RootDir[-1] != '/': RootDir = RootDir + '/'
    myDownloadsDir = RootDir + "My Downloads/"
    myDownloadsDir = xbmc.translatePath(os.path.join(datapaths, 'My Downloads')) + "/"
    if os.path.exists(myDownloadsDir) == False:
        try:
            os.makedirs(myDownloadsDir)
        except:
            myDownloadsDir = RootDir + "My Downloads/"
            # pass
    initDir = RootDir + "init/"
    myPlaylistsDir = RootDir + "My Playlists/"
    myPlaylistsDirB = RootDir + "My Playlists/"
    myPlaylistsDir = xbmc.translatePath(os.path.join(datapaths, 'My Playlists'))
    if os.path.exists(myPlaylistsDir) == False:
        try:
            os.makedirs(myPlaylistsDir)
        except:
            myPlaylistsDir = RootDir + "My Playlists/"
            # pass
    srcDir = RootDir + "src/"
    imageDir = RootDir + "images/"
    imageDir = RootDir + "resources/skins/Default/media/"
    
    # cacheDir=RootDir+"cache/"
    # imageViewCacheDir=RootDir+"cache/mageview/"
    # imageCacheDir=RootDir+"cache/images/"
    # tempCacheDir=RootDir+"cache/temp/"
    # nookieCacheDir=RootDir+"cache/nookies/"
    # procCacheDir=RootDir+"cache/proc/"
    
    cacheDir = datapaths + "cache/"
    imageViewCacheDir = datapaths + "cache/mageview/"
    imageCacheDir = datapaths + "cache/images/"
    tempCacheDir = datapaths + "cache/temp/"
    nookieCacheDir = datapaths + "cache/nookies/"
    procCacheDir = datapaths + "cache/proc/"
    
    favoritesDir = RootDir + "favorites/"
    favoritesDir = xbmc.translatePath(os.path.join(datapaths, 'favorites'))
    imageBrowse['Remote'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Remote']))
    imageBrowse['HTTP'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['HTTP']))
    imageBrowse['FTP'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['FTP']))
    imageBrowse['Local'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Local']))
    imageBrowse['Cache'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Cache']))
    imageBrowse['Blank'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Blank']))
    imageBrowse['Rewrite'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Rewrite']))
    if os.path.exists(favoritesDir) == False:
        try:
            os.makedirs(favoritesDir)
        except:
            favoritesDir = RootDir + "favorites/"
            # pass
    SEPARATOR = '/'
else:
    if RootDir[-1] != '\\': RootDir = RootDir + '\\'
    myDownloadsDir = RootDir + "My Downloads\\"
    myDownloadsDir = xbmc.translatePath(os.path.join(datapaths, 'My Downloads')) + "\\"
    if os.path.exists(myDownloadsDir) == False:
        try:
            os.makedirs(myDownloadsDir)
        except:
            myDownloadsDir = RootDir + "My Downloads\\"
            # pass
    initDir = RootDir + "init\\"
    myPlaylistsDir = RootDir + "My Playlists\\"
    myPlaylistsDirB = RootDir + "My Playlists\\"
    myPlaylistsDir = xbmc.translatePath(os.path.join(datapaths, 'My Playlists'))
    if os.path.exists(myPlaylistsDir) == False:
        try:
            os.makedirs(myPlaylistsDir)
        except:
            myPlaylistsDir = RootDir + "My Playlists\\"
            # pass
    srcDir = RootDir + "src\\"
    # imageDir=RootDir+"images\\"
    
    imageDir = RootDir + "resources\\skins\\Default\\media\\"
    # cacheDir=RootDir+"cache\\"
    # imageViewCacheDir=RootDir+"cache\\imageview\\"
    # imageCacheDir=RootDir+"cache\\images\\"
    # tempCacheDir=RootDir+"cache\\temp\\"
    # nookieCacheDir=RootDir+"cache\\nookies\\"
    # procCacheDir=RootDir+"cache\\proc\\"
    
    cacheDir = datapaths + "cache\\"
    imageViewCacheDir = datapaths + "cache\\imageview\\"
    imageCacheDir = datapaths + "cache\\images\\"
    tempCacheDir = datapaths + "cache\\temp\\"
    nookieCacheDir = datapaths + "cache\\nookies\\"
    procCacheDir = datapaths + "cache\\proc\\"
    
    favoritesDir = RootDir + "favorites\\"
    favoritesDir = xbmc.translatePath(os.path.join(datapaths, 'favorites'))
    imageBrowse['Remote'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Remote']))
    imageBrowse['HTTP'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['HTTP']))
    imageBrowse['FTP'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['FTP']))
    imageBrowse['Local'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Local']))
    imageBrowse['Cache'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Cache']))
    imageBrowse['Blank'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Blank']))
    imageBrowse['Rewrite'] = xbmc.translatePath(os.path.join(imageDir, imageBrowse['Rewrite']))
    if os.path.exists(favoritesDir) == False:
        try:
            os.makedirs(favoritesDir)
        except:
            favoritesDir = RootDir + "favorites\\"
            # pass
    SEPARATOR = '\\'

import xbmc

# version = xbmc.getInfoLabel("System.BuildVersion")[:1]
try:
    The1stTwo = xbmc.getInfoLabel("System.BuildVersion")[:2]
    # if xbmc.getInfoLabel("System.BuildVersion")[:2]=='10':
    if The1stTwo == '10':
        scriptDir = "special://home/addons/"
        pluginDir = "special://home/addons/"
        skinDir = "special://home/skin/"
    elif xbmc.getInfoLabel("System.BuildVersion")[:1] == '9':
        scriptDir = "special://home/scripts/"
        pluginDir = "special://home/plugins/"
        skinDir = "special://home/skin/"
    elif int(The1stTwo) > 10:
        scriptDir = "special://home/addons/"
        pluginDir = "special://home/addons/"
        skinDir = "special://home/skin/"
    else:
        scriptDir = "Q:\\scripts\\"
        pluginDir = "Q:\\plugins\\"
        skinDir = "Q:\\skin\\"
except:
    scriptDir = "Q:\\scripts\\"
    pluginDir = "Q:\\plugins\\"
    skinDir = "Q:\\skin\\"

useLibrtmp = os.path.exists(xbmc.translatePath('special://xbmc/system/players/dvdplayer/librtmp.dll'))

######################################################################
# program version: Combination of version and subversion
Version = '4'
SubVersion = '0'
try:
    Version = Addon.getAddonInfo('version').split('.')[0]
    SubVersion = Addon.getAddonInfo('version')[len(Version) + 1:]
    if ' ' in SubVersion: SubVersion = SubVersion.split(' ')[0]
except:
    pass
nxserver_URL = 'http://www.navixtreme.com'
TVACoreURL = 'http://havana.navixtreme.com/'
background_image1 = 'background1.jpg'
background_image2 = 'background2e.png'
TstRplcStrng = '00110011001100'
favorite_file = 'favorites.plx'  # the favorite list is also a playlist
downloads_file = 'downlmenu.plx'  # the downloads list is also a playlist
downloads_queue = 'downlqueue.plx'
incomplete_downloads = 'incdloads.plx'
downloads_complete = 'downloads.plx'
searchhistory_file = 'search.dat'
MyPlaylists_folder = 'My Playlists'
MyPlaylists_list = 'My Playlists.plx'
startup_list = 'startup.plx'
history_list = 'history.plx'
parent_list = 'blacklist.plx'
MyXBMC_list = 'myxbmc.plx'
source_list = 'source.plx'
plxVersion = '9'

# home_URL_old='http://navi-x.googlecode.com/svn/trunk/Playlists/home.plx'
# home_URL_old='http://navi-x.googlecode.com/svn/trunk/Playlists/home2.plx'
# home_URL='http://navi-x.googlecode.com/svn/trunk/Playlists/home2.plx'
# home_URL='http://raw.github.com/HIGHWAY99/navi-x-storage-unit/master/Playlists/home2.plx'
home_URL_offshore = 'http://offshoregit.com/navixtreme/navi-x-support-files/raw/master/Playlists/home2.plx'
home_URL_havana_old = 'http://havana.navixtreme.com/Playlists/home2.plx'
home_URL_havana = 'http://havana.navixtreme.com/Playlists/home2.plx'

home_URL = home_URL_havana
home_URL_old = home_URL_offshore
home_URL_oldD = [home_URL, home_URL_havana, home_URL_old, home_URL_havana_old, home_URL_offshore]

core_homepage = SettingG("core-homepage").lower()
if core_homepage == "default":
    home_URL = home_URL_havana  # pass
elif core_homepage == "havana":
    home_URL = home_URL_havana
elif core_homepage == "havana2":
    home_URL = home_URL_havana_old
elif core_homepage == "offshore":
    home_URL = home_URL_offshore; home_URL_old = home_URL_havana
home_URL_mirror = home_URL_offshore

home_path_HOME2 = 'Home/'
if 'Playlists/' in home_URL:
    home_path_HOME = home_URL.split('Playlists/')[0]
    home_path_PLAYLIST2 = 'HomePlaylist/'
    home_path_PLAYLIST = home_URL.split('Playlists/')[0] + 'Playlists/'
elif 'playlists/' in home_URL:
    home_path_HOME = home_URL.split('playlists/')[0]
    home_path_PLAYLIST2 = 'HomePlaylist/'
    home_path_PLAYLIST = home_URL.split('playlists/')[0] + 'playlists/'
else:
    home_path_HOME = home_URL.split(home_URL.split('/')[-2] + '/')
    home_path_PLAYLIST2 = 'HomePlaylist/'
# home_path_PLAYLIST=home_URL.split(home_URL.split('/')[-2]+'/')+home_URL.split('/')[-2]+'/'

try:
    url_open_timeout = int(SettingG("urltimeout", "20"))
except:
    url_open_timeout = 20  # 60 seconds
try:
    page_size = int(SettingG("pagesize", "200"))
except:
    page_size = 200  # display maximum 200 entries on one page
try:
    history_size = int(SettingG("historysize", "50"))
except:
    history_size = 50  # maximum of entries in the history list

#############################################################################

mediaFolder = os.path.join(RootDir, 'resources', 'skins', 'Default', 'media')
SplashBH = os.path.join(mediaFolder, 'default-panel1.png')
ExitBH = os.path.join(mediaFolder, 'navi-x3.png')

#############################################################################
skinsFolder = os.path.join(RootDir, 'resources', 'skins', 'Default', '720p')
skinsColor = SettingG('core-color')
skinsColor2 = 'ff00ff00'  #
skinsColorDefault = 'ff00ff00'  # Green
skinsColor2Default = 'ff00ff00'  # 'FF000000' #side-menu text color when selected
DefaultOutputColor = 'ff00ff00'  # '[COLOR ff00ff00]Green[/COLOR]'
if skinsColor == 'Default':
    skinsColor = DefaultOutputColor  # skinsColorDefault
elif skinsColor == '[COLOR ff00ff00]Green[/COLOR]':
    skinsColor = 'ff00ff00';
elif skinsColor == '[COLOR ff0000ff]Blue[/COLOR]':
    skinsColor = 'ff0000ff';
elif skinsColor == '[COLOR ffff0000]Red[/COLOR]':
    skinsColor = 'ffff0000';
elif skinsColor == '[COLOR ff800080]Purple[/COLOR]':
    skinsColor = 'ff800080';
elif skinsColor == '[COLOR ffffa500]Orange[/COLOR]':
    skinsColor = 'ffffa500';
elif skinsColor == '[COLOR ffd2b48c]Tan[/COLOR]':
    skinsColor = 'ffd2b48c';
elif skinsColor == '[COLOR ff9370d8]Medium Purple[/COLOR]':
    skinsColor = 'ff9370d8';
elif skinsColor == '[COLOR ffffc0cb]Pink[/COLOR]':
    skinsColor = 'ffffc0cb';
elif skinsColor == '[COLOR ffff1493]Deep Pink[/COLOR]':
    skinsColor = 'ffff1493';
elif skinsColor == '[COLOR ffdeb887]Burly Wood[/COLOR]':
    skinsColor = 'ffdeb887'; skinsColor2 = 'FF000000'
elif skinsColor == '[COLOR ffff7f50]Coral[/COLOR]':
    skinsColor = 'ffff7f50';
elif skinsColor == '[COLOR ff6495ed]Corn Flower Blue[/COLOR]':
    skinsColor = 'ff6495ed';
elif skinsColor == '[COLOR ffdc143c]Crimson[/COLOR]':
    skinsColor = 'ffdc143c';
elif skinsColor == '[COLOR ff8a2be2]Blue Violet[/COLOR]':
    skinsColor = 'ff8a2be2';
elif skinsColor == '[COLOR fffaebd7]Antique White[/COLOR]':
    skinsColor = 'fffaebd7';
elif skinsColor == '[COLOR ff696969]Dim Gray[/COLOR]':
    skinsColor = 'ff696969'; skinsColor2 = 'FFFFFFFF'
elif skinsColor == '[COLOR ffb22222]Fire Brick[/COLOR]':
    skinsColor = 'ffb22222';
elif skinsColor == '[COLOR ff800000]Maroon[/COLOR]':
    skinsColor = 'ff800000'; skinsColor2 = 'FFFFFFFF'
elif skinsColor == '[COLOR ffe6e6fa]Lavender[/COLOR]':
    skinsColor = 'ffe6e6fa';
elif skinsColor == '[COLOR ffffd700]Gold[/COLOR]':
    skinsColor = 'ffffd700';
elif skinsColor == '[COLOR ffffff00]yellow[/COLOR]':
    skinsColor = 'ffffff00';
elif skinsColor == '[COLOR fff5deb3]Wheat[/COLOR]':
    skinsColor = 'fff5deb3';

elif skinsColor == '[COLOR ff228b22]Forest Green[/COLOR]':
    skinsColor = 'ff228b22';
elif skinsColor == '[COLOR ffff00ff]Fuchsia[/COLOR]':
    skinsColor = 'ffff00ff';
elif skinsColor == '[COLOR ffadff2f]Green Yellow[/COLOR]':
    skinsColor = 'ffadff2f';
elif skinsColor == '[COLOR fff0fff0]Honey Dew[/COLOR]':
    skinsColor = 'fff0fff0';
elif skinsColor == '[COLOR ffff69b4]Hot Pink[/COLOR]':
    skinsColor = 'ffff69b4';
elif skinsColor == '[COLOR ffcd5c5c]Indian Red[/COLOR]':
    skinsColor = 'ffcd5c5c';
elif skinsColor == '[COLOR ff4b0082]Indigo[/COLOR]':
    skinsColor = 'ff4b0082';
elif skinsColor == '[COLOR fffff0f5]Lavender Blush[/COLOR]':
    skinsColor = 'fffff0f5';
elif skinsColor == '[COLOR ff7cfc00]Lawn Green[/COLOR]':
    skinsColor = 'ff7cfc00';
elif skinsColor == '[COLOR fffffacd]Lemon Chiffon[/COLOR]':
    skinsColor = 'fffffacd';
elif skinsColor == '[COLOR fff08080]Light Coral[/COLOR]':
    skinsColor = 'fff08080';
elif skinsColor == '[COLOR ffe0ffff]Light Cyan[/COLOR]':
    skinsColor = 'ffe0ffff';
elif skinsColor == '[COLOR fffafad2]Light Golden Rod Yellow[/COLOR]':
    skinsColor = 'fffafad2';
elif skinsColor == '[COLOR ff87cefa]Light Sky Blue[/COLOR]':
    skinsColor = 'ff87cefa';
elif skinsColor == '[COLOR fffaf0e6]Linen[/COLOR]':
    skinsColor = 'fffaf0e6';
elif skinsColor == '[COLOR ff32cd32]Lime Green[/COLOR]':
    skinsColor = 'ff32cd32';
elif skinsColor == '[COLOR ff00fa9a]Medium Spring Green[/COLOR]':
    skinsColor = 'ff00fa9a';
elif skinsColor == '[COLOR ffda70d6]Orchid[/COLOR]':
    skinsColor = 'ffda70d6';
elif skinsColor == '[COLOR ffd87093]Pale Violet Red[/COLOR]':
    skinsColor = 'ffd87093';
elif skinsColor == '[COLOR ffffefd5]Papaya Whip[/COLOR]':
    skinsColor = 'ffffefd5';
elif skinsColor == '[COLOR ffb0e0e6]Powder Blue[/COLOR]':
    skinsColor = 'ffb0e0e6';
elif skinsColor == '[COLOR ffdda0dd]Plum[/COLOR]':
    skinsColor = 'ffdda0dd';
elif skinsColor == '[COLOR ffcd853f]Peru[/COLOR]':
    skinsColor = 'ffcd853f';
elif skinsColor == '[COLOR ffffdab9]Peach Puff[/COLOR]':
    skinsColor = 'ffffdab9';
elif skinsColor == '[COLOR ffbc8f8f]Rosy Brown[/COLOR]':
    skinsColor = 'ffbc8f8f';
elif skinsColor == '[COLOR ff4169e1]Royal Blue[/COLOR]':
    skinsColor = 'ff4169e1';
elif skinsColor == '[COLOR ff8b4513]Saddle Brown[/COLOR]':
    skinsColor = 'ff8b4513';
elif skinsColor == '[COLOR fffa8072]Salmon[/COLOR]':
    skinsColor = 'fffa8072';
elif skinsColor == '[COLOR fff4a460]Sandy Brown[/COLOR]':
    skinsColor = 'fff4a460';
elif skinsColor == '[COLOR fffff5ee]Sea Shell[/COLOR]':
    skinsColor = 'fffff5ee';
elif skinsColor == '[COLOR ffa0522d]Sienna[/COLOR]':
    skinsColor = 'ffa0522d';
elif skinsColor == '[COLOR ff87ceeb]Sky Blue[/COLOR]':
    skinsColor = 'ff87ceeb';
elif skinsColor == '[COLOR ff6a5acd]Slate Blue[/COLOR]':
    skinsColor = 'ff6a5acd';
elif skinsColor == '[COLOR ff708090]Slate Gray[/COLOR]':
    skinsColor = 'ff708090';
elif skinsColor == '[COLOR fffffafa]Snow[/COLOR]':
    skinsColor = 'fffffafa';
elif skinsColor == '[COLOR ff00ff7f]Spring Green[/COLOR]':
    skinsColor = 'ff00ff7f';
elif skinsColor == '[COLOR ff4682b4]Steel Blue[/COLOR]':
    skinsColor = 'ff4682b4';
elif skinsColor == '[COLOR ff008080]Teal[/COLOR]':
    skinsColor = 'ff008080';
elif skinsColor == '[COLOR ffd8bfd8]Thistle[/COLOR]':
    skinsColor = 'ffd8bfd8';
elif skinsColor == '[COLOR ffff6347]Tomato[/COLOR]':
    skinsColor = 'ffff6347';
elif skinsColor == '[COLOR ff40e0d0]Turquoise[/COLOR]':
    skinsColor = 'ff40e0d0';
elif skinsColor == '[COLOR ffee82ee]Violet[/COLOR]':
    skinsColor = 'ffee82ee';
elif skinsColor == '[COLOR ffffffff]White[/COLOR]':
    skinsColor = 'ffffffff'; skinsColor2 = 'FF000000'
elif skinsColor == '[COLOR fff5f5f5]White Smoke[/COLOR]':
    skinsColor = 'fff5f5f5'; skinsColor2 = 'FF000000'
elif skinsColor == '[COLOR ff9acd32]Yellow Green[/COLOR]':
    skinsColor = 'ff9acd32';
# elif skinsColor=='[COLOR ][/COLOR]': skinsColor='';
# elif skinsColor=='[COLOR ][/COLOR]': skinsColor='';
# elif skinsColor=='[COLOR ][/COLOR]': skinsColor='';
else:
    skinsColor = DefaultOutputColor  # skinsColorDefault

sknsClr = "[COLOR " + skinsColor + "]%s[/COLOR]"
sknsClr2 = "[COLOR " + skinsColor2 + "]%s[/COLOR]"
## <colordiffuse>0xff00ff00</colordiffuse>
#############################################################################



#############################################################################
## \/ This isn't used yet. \/ ##
ExtDict = []
ExtDict.append(['text', ['.txt']])
ExtDict.append(['video', ['.flv', '.mp4', '.mpg', '.mpeg', '.avi']])
ExtDict.append(['audio', ['.mp3', '.wav', '.snd', '.mid', '.midi']])
ExtDict.append(['image', ['.png', '.gif', '.bmp', '.jpg', '.jpeg']])
ExtDict.append(['playlist', ['.plx']])
ExtDict.append(['script', ['Navi-X-3.7.', 'Navi-X-3.8.', 'Navi-X-3.9.', 'Navi-X-4.', 'Navi-X-5.']])
ExtDict.append(['plugin', ['.zip']])
ExtDict.append(['rss', ['.atom']])
# ExtDict.append(['addon',[]])
# ExtDict.append(['text',[]])
#############################################################################
cachedFlag = False
cachedFlag = ''
try:
    DefaultCachedExpires = (int(SettingG('cachedexpires', '2')) * 60) * 60
except:
    DefaultCachedExpires = 7200
CachedPagesAndTimes = []
CachedPagesAndTimes.append([72, nxserver_URL.lower() + '/playlist/week.plx'])  # 7 days
CachedPagesAndTimes.append([6, nxserver_URL.lower() + '/playlist/day.plx'])  # 24 hours
CachedPagesAndTimes.append([72, nxserver_URL.lower() + '/plx/search.plx'])  # Search
CachedPagesAndTimes.append(
    [72, nxserver_URL.lower() + '/playlist/50242/navi-xtreme_nxportal_home.plx'])  # Navi-X Portal
CachedPagesAndTimes.append([72, nxserver_URL.lower() + '/playlist/50274/user_lists.plx'])  # User Lists
CachedPagesAndTimes.append([72, nxserver_URL.lower() + '/playlist/2229/realtime_scrapers.plx'])  # Site Scrapers

TSTRMSG = urllib.quote_plus(SettingG("scripts-testers2"))
#############################################################################
# PheonixHome='http://mecca.watchkodi.com/phstreams.xml'
# PheonixBG='http://i.imgur.com/PQEaQ1j.jpg' #'http://s18.postimg.org/v8uu1dj49/phoenix_1080.jpg'
XMLPlaylistIdentifiers = ['<link>', '<LINK>', '<sublink>', '<SUBLINK>', '<name>', '<NAME>', '<title>', '<TITLE>']
# CachedPagesAndTimes.append([72,PheonixHome])   # Pheonix Home Playlist
#############################################################################
DebugForTesting = tfalse(SettingG('debug-enable', 'false'))


# DebugForTesting=True; #DebugForTesting=False;
def TestBug(m):
    if DebugForTesting == True:
        try:
            print m
        except:
            pass


#############################################################################
testing = tfalse(SettingG("GUI-testing-enable", 'false'))
#############################################################################
