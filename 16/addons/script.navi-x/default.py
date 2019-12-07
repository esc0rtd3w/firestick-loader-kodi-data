#############################################################################
#
#   Copyright (C) 2013-2015 Navi-X
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

#############################################################################
#
# Navi-X bootloader + auto update installer.
#############################################################################
import xbmc, xbmcgui, xbmcaddon, sys, re, os, time, datetime, traceback, urllib2, shutil, zipfile, downloader, extract

# Script constants
Addon = xbmcaddon.Addon()
addon = Addon.getAddonInfo('id')
__scriptname__ = Addon.getAddonInfo('name')
__version__ = Addon.getAddonInfo('version')
__author__ = "Navi-X team"
__url__ = "http://code.google.com/p/navi-x/"
__credits__ = "Navi-X team"

RootDir = Addon.getAddonInfo('path')
sys.path.append(os.path.join(RootDir.replace(";", ""), 'src'))

if RootDir[-1] == ';': RootDir = RootDir[0:-1]
if RootDir[0] == '/':
    if RootDir[-1] != '/': RootDir = RootDir + '/'
    SEPARATOR = '/'
else:
    if RootDir[-1] != '\\': RootDir = RootDir + '\\'
    SEPARATOR = '\\'

version_default = '0.0.0'
version_URL = ''
update_URL = ''


##########Install Hub Repo#############################################################
def HUBINSTALL(name, url, description, filetype, repourl):
    try:
        path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
        dp = xbmcgui.DialogProgress()
        dp.create("Checking Structure:", "Installing Proper Repo ", '', 'Only Shown on First Launch')
        lib = os.path.join(path, name + '.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib, dp)
        if filetype == 'addon':
            addonfolder = xbmc.translatePath(os.path.join('special://home', 'addons'))
        time.sleep(2)
        # dp.update(0,"","Installing selections.....")
        print '======================================='
        print addonfolder
        print '======================================='
        extract.all(lib, addonfolder, '')
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
    except:
        pass


hubpath = xbmc.translatePath(os.path.join('special://home', 'addons', 'repository.xbmchub'))
if not os.path.exists(hubpath): HUBINSTALL('xbmchubrepo',
                                           'https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/repository.xbmchub/repository.xbmchub-1.0.5.zip',
                                           '', 'addon', 'none')


#############################################################################
def onReadVersion():
    version = version_default
    try:
        f = open(RootDir + 'version.dat', 'r')
        data = f.read()
        data = data.splitlines()
        version = data[0]
        f.close()
    except IOError:
        pass
    return version


#############################################################################
def onReadNewVersion(URL):
    version = version_default
    try:
        # oldtimeout=socket_getdefaulttimeout()
        # socket_setdefaulttimeout(timeout)
        f = urllib2.urlopen(URL)
        data = f.read()
        data = data.splitlines()
        version = data[0]
    except IOError:
        pass
    # socket_setdefaulttimeout(oldtimeout)
    return version


#############################################################################
def onSaveVersion(version):
    try:
        f = open(RootDir + 'version.dat', 'w')
        f.write(version + '\n')
        f.close()
    except IOError:
        pass


######################################################################
def installUpdate(URL):
    try:
        # oldtimeout=socket_getdefaulttimeout()
        # socket_setdefaulttimeout(timeout)
        f = urllib2.urlopen(URL)
        file = open(RootDir + "update.zip", "wb")
        file.write(f.read())
        file.close()
    except IOError:
        # socket_setdefaulttimeout(oldtimeout)
        return -1
    # socket_setdefaulttimeout(oldtimeout)
    zfobj = zipfile.ZipFile(RootDir + "update.zip")
    for name in zfobj.namelist():
        index = name.rfind('/')
        if index != -1:
            # entry contains path
            if not os.path.exists(RootDir + name[:index + 1]):
                try:
                    # create the directory structure
                    os.makedirs(os.path.join(RootDir, name[:index + 1]))
                except IOError:
                    return -1  # failure
        if not name.endswith('/'):
            # entry contains a filename
            try:
                outfile = open(os.path.join(RootDir, name), 'wb')
                outfile.write(zfobj.read(name))
                outfile.close()
            except IOError:
                pass  # There was a problem. Continue...
    zfobj.close()
    try:
        os.remove(RootDir + "update.zip")
    except IOError:
        pass
    return 0  # succesful


######################################################################
def socket_getdefaulttimeout(): return socket.getdefaulttimeout()


######################################################################
def socket_setdefaulttimeout(url_open_timeout):
    if platform == "xbox":
        socket.setdefaulttimeout(url_open_timeout)


#############################################################################
def Trace(string):
    f = open(RootDir + "trace.txt", "a")
    f.write(string + '\n')
    f.close()


######################################################################
def get_system_platform():
    platform = "unknown"
    if xbmc.getCondVisibility("system.platform.linux"):
        platform = "linux"
    elif xbmc.getCondVisibility("system.platform.xbox"):
        platform = "xbox"
    elif xbmc.getCondVisibility("system.platform.windows"):
        platform = "windows"
    elif xbmc.getCondVisibility("system.platform.osx"):
        platform = "osx"
    # Trace("Platform: %s"%platform)
    return platform


#############################################################################
#############################################################################
##check for updates from the Navi-X website
##retrieve the platform.
platform = get_system_platform();
print {'platform': platform};


##read the current version installed
# version=onReadVersion()
# newversion=onReadNewVersion(version_URL)
# if (version != version_default) and (newversion != version_default) and \
#    (version != newversion):
#    installUpdate(update_URL)
#    #save updated version.
#    onSaveVersion(newversion)
#    dialog=xbmcgui.Dialog()
#    dialog.ok("Message","Navi-X has been updated.")
#############################################################################
# Splash Screen
#############################################################################
def SettingG(setting, d=""):
    try:
        return addon.getSetting(setting)
    except:
        return d


def SettingS(setting, value): addon.setSetting(id=setting, value=value)


def tfalse(r, d=False):  ## Get True / False
    if (r.lower() == 'true') or (r.lower() == 't') or (r.lower() == 'y') or (r.lower() == '1') or (r.lower() == 'yes'):
        return True
    elif (r.lower() == 'false') or (r.lower() == 'f') or (r.lower() == 'n') or (r.lower() == '0') or (
        r.lower() == 'no'):
        return False
    else:
        return d


def gAI(t):
    try:
        return Addon.getAddonInfo(t)
    except:
        return ""


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
skinsColor = SettingG('core-color')
skinsColor2 = 'FF000000'  #
skinsColorDefault = 'ff00ff00'  # Green
skinsColor2Default = 'FF000000'  # side-menu text color when selected
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
else:
    skinsColor = DefaultOutputColor  # skinsColorDefault

xbmc_version = xbmc.getInfoLabel('System.BuildVersion');
print {'xbmc version': xbmc_version};
xbmc_v = xbmc_version.split(' ');
try:
    xbmc_major_ver = int(xbmc_version[0] + xbmc_version[1]); print {'XBMC Major Version': xbmc_major_ver}
except:
    xbmc_major_ver = 0
if xbmc_major_ver < 14:
    MainSkinFile = 'skin2.xml'  ##if xbmc_v[0] < '14.0': MainSkinFile='skin2.xml'
else:
    MainSkinFile = 'skin2h.xml'
# SkinCollection=[MainSkinFile,'CBrowseskin2.xml','CLoginskin2.xml','CRatingskin2.xml'] #,'CTextViewskin2.xml']:
SkinCollection = ['skin2.xml', 'skin2h.xml', 'CBrowseskin2.xml', 'CLoginskin2.xml',
                  'CRatingskin2.xml']  # ,'CTextViewskin2.xml']:
skinsFolder720 = os.path.join(RootDir, 'resources', 'skins', 'Default', '720p')
skinsFolder1080 = os.path.join(RootDir, 'resources', 'skins', 'Default', '1080i')
for skinsFolder in [skinsFolder720, skinsFolder1080]:
    for FF1 in SkinCollection:
        FF2 = os.path.join(skinsFolder, FF1)
        FF3 = FileDoOpen(FF2 + '.xml')
        for (FF5, FF6) in [[skinsColorDefault, skinsColor], [skinsColor2Default, skinsColor2]]:
            if not FF5 == FF6:
                FF4b = "<"
                for FF4 in [">", ">0x"]:
                    FF3 = FF3.replace(FF4 + FF5 + FF4b, FF4 + FF6 + FF4b)
                    FF3 = FF3.replace(FF4 + FF5.lower() + FF4b, FF4 + FF6.lower() + FF4b)
                    FF3 = FF3.replace(FF4 + FF5.upper() + FF4b, FF4 + FF6.upper() + FF4b)
        FileDoSave(FF2, FF3)
if SettingG('core-skin') == 'Default':
    pass
elif SettingG('core-skin') == 'skin2':
    MainSkinFile = 'skin2'
elif SettingG('core-skin') == 'skin2h':
    MainSkinFile = 'skin2h'

## <colordiffuse>0xff00ff00</colordiffuse>
#############################################################################

#############################################################################
ProfFolder = xbmc.translatePath(Addon.getAddonInfo('profile'))
if os.path.exists(ProfFolder) == False:
    try:
        os.makedirs(ProfFolder)
    except:
        pass
#############################################################################
# Start Navi-X
#############################################################################
import navix

print ['Main Skin File', MainSkinFile]
win = navix.MainWindow(MainSkinFile, Addon.getAddonInfo('path'))  # ,'Default','720p')
#  win.setCoordinateResolution(5)
win.doModal()
del win

# xbmc.executescript(RootDir + 'default_.py')
