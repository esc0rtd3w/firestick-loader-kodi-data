#
#      Copyright (C) 2013 Sean Poyser
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#


import urllib
import urllib2
import re
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import os
import display
import utils
import random

ADDONID  = utils.ADDONID
URL      = utils.URL
ADDON    = xbmcaddon.Addon(ADDONID)
HOME     = ADDON.getAddonInfo('path')
TITLE    = ADDON.getAddonInfo('name')
VERSION  = ADDON.getAddonInfo('version')
ICON     = os.path.join(HOME, 'icon.png')
ARTWORK  = os.path.join(HOME, 'resources', 'artwork')
#FANART  = os.path.join(HOME, 'fanart.jpg')


SECTION   = 100
CHARACTER = 200
SLIDESHOW = 300


def CheckVersion():
    prev = ADDON.getSetting('VERSION')
    curr = VERSION

    if prev == curr:
        return

    ADDON.setSetting('VERSION', curr)

    if curr == '1.0.4':
        import shutil
        try:    shutil.rmtree(utils.CACHE)
        except: pass

    #call showChangeLog like this to workaround bug in openElec
    script = os.path.join(HOME, 'showChangelog.py')
    cmd    = 'AlarmClock(%s,RunScript(%s),%d,True)' % ('changelog', script, 0)
    xbmc.executebuiltin(cmd)


def Clean(text):
    #text = text.replace('&#8211;', '-')
    #text = text.replace('&#8217;', '\'')
    #text = text.replace('&#8220;', '"')
    #text = text.replace('&#8221;', '"')
    #text = text.replace('&#39;',   '\'')
    #text = text.replace('<b>',     '')
    #text = text.replace('</b>',    '')
    text = text.replace('&#x27;', '\'')
    text = text.replace('&amp;',   '&')
    #text = text.replace('\ufeff', '')
    return text


def Main():
    CheckVersion()

    AddSection('Comics',              'comics')    
    AddSection('Political Cartoons',  'editorials')
    AddSection('Sherpa',              'sherpa')
    AddSection('Comics en Espanol',   'espanol')


def Section(url):
    url  = URL + '/explore/' + url
    html = utils.GetHTML(url, timeout=43200) #1/2 a day
    #html = html.replace('a href="/explore', '') 

    match = re.compile('<li>(.+?)</li>').findall(html)

    for item in match:
        items = re.compile('<a href="(.+?)">.+?<img alt=".+?" class="thumb" height="60" src="(.+?)" title="(.+?)"').findall(item)
        url   = items[0][0]
        image = items[0][1].replace('tiny_avatar', 'avatar')
        name  = items[0][2]
        AddCharacter(name, url, image)


def Character(url):
    ShowStrip(url, False)


def Slideshow(url):
    ShowStrip(url, True)


def ShowStrip(url, slideshow):
    app = None

    xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem())

    try:
        app = display.Display(url, slideshow)
        app.doModal()   
    except Exception, e:        
        pass

    if app:
        del app


def AddSection(name, url):
    AddDir(name, SECTION, url, image=os.path.join(ARTWORK, url+'.png'))


def AddCharacter(name, url, image):
    menu = []
    menu.append(('Start Comic Strip Slideshow','XBMC.RunPlugin(%s?mode=%d&url=%s)'% (sys.argv[0], SLIDESHOW, url)))

    AddDir(name, CHARACTER, url, image, isFolder=False, contextMenu=menu)


def AddDir(name, mode, url='', image=None, isFolder=True, page=1, keyword=None, infoLabels=None, contextMenu=None):

    name = Clean(name)

    if not image:
        image = ICON

    u  = sys.argv[0] 
    u += '?mode='  + str(mode)
    u += '&title=' + urllib.quote_plus(name)
    u += '&image=' + urllib.quote_plus(image)
    u += '&page='  + str(page)

    if url != '':     
        u += '&url='   + urllib.quote_plus(url) 

    if keyword:
        u += '&keyword=' + urllib.quote_plus(keyword) 

    liz = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)

    if contextMenu:
        liz.addContextMenuItems(contextMenu)

    if infoLabels:
        liz.setInfo(type="Video", infoLabels=infoLabels)


    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)


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


params = get_params()
mode   = None
url    = None

try:    mode = int(urllib.unquote_plus(params['mode']))
except: pass

try:    url   = urllib.unquote_plus(params['url'])
except: pass


if mode == SECTION:
    Section(url)

elif mode == CHARACTER:
    Character(url)

elif mode == SLIDESHOW:
    Slideshow(url)

else:
    Main()

        
try:
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
except:
    pass


 
