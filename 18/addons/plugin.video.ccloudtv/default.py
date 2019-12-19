# -*- coding: utf-8 -*-

"""
Copyright (C) 2017 rattlehead

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
"""

import urllib, urllib2, sys, re, os, random, unicodedata, cookielib, shutil
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, requests, base64
import datetime
from time import gmtime, strftime
import liveresolver
# import urlresolver
try:
    import json
except:
    import simplejson as json


plugin_handle = int(sys.argv[1])
mysettings = xbmcaddon.Addon(id = 'plugin.video.ccloudtv')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
getSetting = xbmcaddon.Addon().getSetting

enable_adult_section = mysettings.getSetting('enable_adult_section')

fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
iconpath = xbmc.translatePath(os.path.join(home, 'resources/icons/'))
icon = xbmc.translatePath(os.path.join(home, 'resources/icons/icon.png'))
addonDir = mysettings.getAddonInfo('path').decode("utf-8")

xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
m3u_thumb_regex = 'tvg-logo=[\'"](.*?)[\'"]'
group_title_regex = 'group-title=[\'"](.*?)[\'"]'
m3u_regex = '#(.+?),(.+)\s*(.+)\s*'
eng_regex = '#(.+?),English,(.+)\s*(.+)\s*'
adult_regex = '#(.+?)group-title="Adult",(.+)\s*(.+)\s*'
adult_regex2 = '#(.+?)group-title="Public-Adult",(.+)\s*(.+)\s*'
ondemand_regex = '[ON\'](.*?)[\'nd]'
ou812=base64.b64decode
yt = 'http://www.youtube.com'
m3u = 'WVVoU01HTkViM1pNTTBKb1l6TlNiRmx0YkhWTWJVNTJZbE01ZVZsWVkzVmpSMmgzVURKck9WUlViRWxTYXpWNVZGUmpQUT09'.decode('base64')
text = 'http://pastebin.com/raw.php?i=Zr0Hgrbw'
xbmcplugin.setContent(int(sys.argv[1]), 'movies')
skin = xbmc.getSkinDir()
ADDON_NAME = '[COLOR blue][B]cCloud TV[/B][/COLOR]'
addon_id = 'plugin.video.ccloudtv'
ADDON = xbmcaddon.Addon(id=addon_id)
ADDON_PATH = xbmc.translatePath('special://home/addons/'+addon_id)
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
Dialog = xbmcgui.Dialog()
addon_data = xbmc.translatePath('special://home/userdata/addon_data/'+addon_id+'/')
# AddonPY = xbmc.translatePath(('special://home/addons/plugin.video.ccloudtv/resources/tvGuide/addon.py'))
favorites = os.path.join(addon_data, 'favorites.txt')
debug = ADDON.getSetting('debug')
if os.path.exists(addon_data)==False:
    os.makedirs(addon_data)
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else: FAV = []

def set_view_thumbnail():
    if skin == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(500)')
    elif skin == 'skin.aeon.nox':
        xbmc.executebuiltin('Container.SetViewMode(511)')
    if skin == 'skin.estuary':
        xbmc.executebuiltin('Container.SetViewMode(511)')
    else:
        xbmc.executebuiltin('Container.SetViewMode(500)')
        
def read_file(file):
    try:
        f = open(file, 'r')
        content = f.read()
        f.close()
        return content
    except:
        pass
        

def make_request():
    for server in shuffle(CCLOUDTV_SRV_URL):
            conn = GetHttpStatusAndData(server)
            if conn['valid']:
                links = conn['data'].encode('utf-8')
                return links
    return None

            
def main():
    #text_online2()
    #checkaddon.do_block_check()
    # Create_INI()
    set_view_thumbnail()
    addDir('[COLOR white][B]*Announcements*[/B][/COLOR]', yt, 3, '%s/announcements.png'% iconpath, fanart)
    addDir('[COLOR white][B]*ReadMe*[/B][/COLOR]', yt, 8, '%s/readme.png'% iconpath, fanart)
    addDir('[COLOR white][B]*Server Status*[/B][/COLOR]', yt, 7, '%s/serverStatus.png'% iconpath, fanart)
    if os.path.exists(favorites) == True:
        addDir('[COLOR white][B]*Favorites*[/B][/COLOR]', yt, 6, '%s/favorites.png'% iconpath, fanart)
    addDir('[COLOR white][B]*Search*[/B][/COLOR]', 'searchlink', 99, '%s/search.png'% iconpath, fanart)
    if len(CCLOUDTV_SRV_URL) > 0:    
        addDir('[COLOR white][B]All Channels[/B][/COLOR]', yt, 2, '%s/allchannels.png'% iconpath, fanart)
    if (len(CCLOUDTV_SRV_URL) < 1 ):        
        mysettings.openSettings()
        xbmc.executebuiltin("Container.Refresh")
    # addDir2('[COLOR white][B]TV Guide[/B][/COLOR]', 'guide', 97, '%s/guide.png'% iconpath, fanart)
    addDir('[COLOR white][B]FilmOn[/B][/COLOR]', 'filmon', 20,'%s/filmon.png'% iconpath, fanart)
    addDir('[COLOR white][B]English[/B][/COLOR]', 'english', 62, '%s/english.png'% iconpath, fanart)
    addDir('[COLOR white][B]Top 10[/B][/COLOR]', 'top10', 51, '%s/top10.png'% iconpath, fanart)
    addDir('[COLOR white]Sports[/COLOR]', 'sports', 52, '%s/sports.png'% iconpath, fanart)
    addDir('[COLOR white]News[/COLOR]', 'news', 53, '%s/news.png'% iconpath, fanart)
    addDir('[COLOR white]Documentary[/COLOR]', 'documentary', 54, '%s/documentary.png'% iconpath, fanart)
    addDir('[COLOR white]Entertainment[/COLOR]', 'entertainment', 55, '%s/entertainment.png'% iconpath, fanart)
    addDir('[COLOR white]Family[/COLOR]', 'family', 56, '%s/family.png'% iconpath, fanart)
    addDir('[COLOR white]Movies[/COLOR]', 'movie', 57, '%s/movies.png'% iconpath, fanart)
    addDir('[COLOR white]Music[/COLOR]', 'music', 58, '%s/music.png'% iconpath, fanart)
    addDir('[COLOR white]Lifestyle[/COLOR]', 'lifestyle', 63, '%s/lifestyle.png'% iconpath, fanart)
    addDir('[COLOR white]On Demand Movies[/COLOR]', 'ondemandmovies', 59, '%s/ondemandmovies.png'% iconpath, fanart)
    addDir('[COLOR white]On Demand Shows[/COLOR]', 'ondemandshows', 65, '%s/ondemandshows.png'% iconpath, fanart)
    addDir('[COLOR white]24/7 Channels[/COLOR]', '24', 60, '%s/twentyfourseven.png'% iconpath, fanart)
    addDir('[COLOR white]Radio[/COLOR]', 'radio', 61, '%s/radio.png'% iconpath, fanart)
    addDir('[COLOR white]Non-English/International[/COLOR]', 'international', 64,'%s/international.png'% iconpath, fanart)
    if getSetting("enable_adult_section") == 'true':    
        addDir('[COLOR white][B]Adult(18+)[/B][/COLOR]', 'adult', 98, '%s/adult.png'% iconpath, fanart)

def removeAccents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s.decode('utf-8')) if unicodedata.category(c) != 'Mn'))
        
def search():     
    try:
        keyb = xbmc.Keyboard('', 'Enter Channel Name')
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText(), safe="%/:=&?~#+!$,;'@()*[]").replace('+', ' ')
        HTML = OPEN_URL('http://www.filmon.com/tv')
        match = re.compile('{"id":(.+?),"logo":"(.+?)","big_logo":"(.+?).png","title":"(.+?)","alias":"(.+?)","description":"(.+?)".+?true,"group":"(.+?)"').findall(HTML)
        for id,logo,thumb,name,alias,description,group in match:
            url = 'https://www.filmon.com/tv/' + alias.replace(' ','-')
            thumb = thumb.replace("\/", "/")+'.png'
            icon = thumb
            name = name + ' (FilmOn)'
            if re.search(searchText, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                m3u_playlist(name, url, thumb)
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchText, removeAccents(name.replace('Đ', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)
    except:
        pass


#########CATEGORIES###########
def cats(category):     
    try:
        searchText = category
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchText, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)
					
    except:
        pass


def adult():     
    try:
        searchText = ('(Adult)') or ('(Public-Adult)')
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(adult_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchText, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    adult_playlist(name, url, thumb)    
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(adult_regex2).findall(content)
            for thumb, name, url in match:
                if re.search(searchText, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    adult_playlist(name, url, thumb)    

    except:
        pass
    
    
def international():     
    try:
        searchGerman = '(German)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchGerman, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchSpanish = '(Spanish)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchSpanish, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchFrench = '(French)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchFrench, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchHindi = '(Hindi)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchHindi, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchArabic = '(Arabic)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchArabic, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchUrdu = '(Urdu)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchUrdu, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchFarsi = '(Farsi)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchFarsi, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchPortuguese = '(Portuguese)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchPortuguese, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchKurdish = '(Kurdish)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchKurdish, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchChinese = '(Chinese)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchChinese, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchSomali = '(Somali)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchSomali, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchRussian = '(Russian)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchRussian, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchAfrikaans = '(Afrikaans)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchAfrikaans, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchRomanian = '(Romanian)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchRomanian, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchItalian = '(Italian)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchItalian, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchIsraeli = '(Israeli)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchIsraeli, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchGreek = '(Greek)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchGreek, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchhungarian = '(Hungarian)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchHungarian, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchTamil = '(Tamil)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchTamil, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchMacedonian = '(Macedonian)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchMacedonian, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchIndian = '(Indian)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchIndian, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchCatalan = '(Catalan)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchCatalan, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchJamaica = '(Jamaica)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchJamaica, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchUkrainian = '(Ukrainian)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchUkrainian, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchVietamese = '(Vietamese)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchVietamese, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchMaltese = '(Maltese)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchMaltese, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchLithuanian = '(Lithuanian)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchLithuanian, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchPolish = '(Polish)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchPolish, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchSlovenian = '(Slovenian)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchSlovenian, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchDeutsch = '(Deutsch)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchDeutsch, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchDutch = '(Dutch)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchDutch, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchFilipino = '(Filipino)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchFilipino, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass
    try:
        searchMandarin = '(Mandarin)'
        if len(CCLOUDTV_SRV_URL) > 0:        
            content = make_request()
            match = re.compile(m3u_regex).findall(content)
            for thumb, name, url in match:
                if re.search(searchMandarin, removeAccents(name.replace('Ð', 'D')), re.IGNORECASE):
                    m3u_playlist(name, url, thumb)    
    except:
        pass

def FilmOnAll():
    # addDir('[B]ALL CHANNELS & SCHEDULES[/B] (if available)', '', 21,'%s/filmon.png'% iconpath, fanart)
    HTML = OPEN_URL('http://www.filmon.com/tv')
    match = re.compile('{"id":(.+?),"logo":"(.+?)","big_logo":"(.+?).png","title":"(.+?)","alias":"(.+?)","description":"(.+?)".+?true,"group":"(.+?)"').findall(HTML)
    for id,logo,thumb,name,alias,description,group in match:
        url = 'https://www.filmon.com/tv/' + alias.replace(' ','-')
        thumb = thumb.replace("\/", "/")+'.png'
        icon = thumb
        icon = icon.replace('big_logo','extra_big_logo')
        addDir(name.replace('&amp;','&'), url, 23, icon, fanart)

def FilmOnCAT():
	addDir('[COLOR white]ALL CHANNELS[/COLOR]', 'filmon', 21,'%s/filmon2.png'% iconpath, fanart)
	HTML = OPEN_URL('http://www.filmon.com/tv/groups')
	match = re.compile('<li class="group-item">.*\n.*<a href="\/group\/(.+?)">.*\n.*<img class="logo" src="(.+?)" title="(.+?)"').findall(HTML)
	for group,thumb,name in match:
		url = 'http://www.filmon.com/group/' + group.replace(' ','-')
		thumb = thumb.replace("\/", "/")
		icon = thumb
		exception = "PAY TV - CHANNELS"
		if exception not in name:
			addDir(name.replace('&amp;','&'), url, 22, icon, fanart)

def FilmOn(name,url):
    HTML = OPEN_URL(url)
    match = re.compile('channel_id="(.+?)">.*\n.*<a href="\/channel\/(.+?)" class="clearfix" onclick="return false;">.*\n.*<img class="channel_logo" src="(.+?)" title="(.+?)"').findall(HTML)
    for id,alias,thumb,name in match:
        url = 'https://www.filmon.com/tv/' + alias.replace(' ','-')
        thumb = thumb.replace("\/", "/")
        icon = thumb
        icon = icon.replace('big_logo','extra_big_logo')
        thumb = thumb.replace("\/", "/")+'.png'
        addDir(name.replace('&amp;','&'), url, 23,icon, fanart)
		
def FilmOnSched(name,url,icon):
    if getSetting("filmon_view") == '0':    
			name = re.sub('\s+', ' ', name).strip()            
			url = url.replace('"', ' ').replace('&amp;', '&').strip()
			resolved = liveresolver.resolve(url)
			xbmc.Player().play(resolved)
			sys.exit()
    if getSetting("filmon_view") == '1':    
			url2=url
			url = url.replace('/tv/','/tvguide/rss/')
			HTML = OPEN_URL(url)
			match = re.compile('<item><title>(.+?)<\/title><link>(.+?)<\/link><description>(.+?)<\/description><pubDate>(.+?):(.+?):.*?<\/pubDate><\/item>').findall(HTML)
			match2 = re.compile('<image url="(.+?)" title="(.+?)"\/><atom:link xmlns:atom="atom" href=".+?\/rss\/(.+?)" rel').findall(HTML)
			for logo,title,alias in match2:
				url = 'https://www.filmon.com/tv/' + alias.replace(' ','-')
				title = '[COLOR blue][B]'+alias.replace('-',' ').upper()+'[/B][/COLOR]'
				m3u_playlist(title +' <<<--- CLICK TO PLAY', url, logo)
				m3u_playlist('[B]-----------------------------------------------------[/B]', url, logo)
				m3u_playlist('Your time now is '+datetime.datetime.now().strftime("[B]%H:%M %p - %x[/B]"), url, logo)
				m3u_playlist('Schedule below is [B]GMT (UTC +0)[/B]', url, logo)
				m3u_playlist('[B]-----------------------------------------------------[/B]', url, logo)
			for title,link,desc,hh,mm in match:
				date_string=(hh+':'+mm)
				url = 'https://www.filmon.com/tv/' + alias.replace(' ','-')
				m3u_playlist('[B]'+date_string+' - '+'[COLOR blue]'+title.replace('&amp;','&')+'[/COLOR][/B]', url, logo)
				m3u_playlist(desc, url, logo)
				m3u_playlist('[B]-----------------------------------------------------[/B]', url, logo)
    if getSetting("filmon_view") == '2':    
        thumb=icon
        dialog = xbmcgui.Dialog()
        ret = dialog.select('What Do You Want To Do?', ['Play Channel', 'View Channel Schedule First'])
        if ret == 0:
			name = re.sub('\s+', ' ', name).strip()            
			url = url.replace('"', ' ').replace('&amp;', '&').strip()
			resolved = liveresolver.resolve(url)
			xbmc.Player().play(resolved)
			sys.exit()
        if ret == 1:
			url2=url
			url = url.replace('/tv/','/tvguide/rss/')
			HTML = OPEN_URL(url)
			match = re.compile('<item><title>(.+?)<\/title><link>(.+?)<\/link><description>(.+?)<\/description><pubDate>(.+?):(.+?):.*?<\/pubDate><\/item>').findall(HTML)
			match2 = re.compile('<image url="(.+?)" title="(.+?)"\/><atom:link xmlns:atom="atom" href=".+?\/rss\/(.+?)" rel').findall(HTML)
			for logo,title,alias in match2:
				url = 'https://www.filmon.com/tv/' + alias.replace(' ','-')
				title = '[COLOR blue][B]'+alias.replace('-',' ').upper()+'[/B][/COLOR]'
				m3u_playlist(title +' <<<--- CLICK TO PLAY', url, logo)
				m3u_playlist('[B]-----------------------------------------------------[/B]', url, logo)
				m3u_playlist('Your time now is '+datetime.datetime.now().strftime("[B]%H:%M %p - %x[/B]"), url, logo)
				m3u_playlist('Schedule below is [B]GMT (UTC +0)[/B]', url, logo)
				m3u_playlist('[B]-----------------------------------------------------[/B]', url, logo)
			for title,link,desc,hh,mm in match:
				date_string=(hh+':'+mm)
				url = 'https://www.filmon.com/tv/' + alias.replace(' ','-')
				m3u_playlist('[B]'+date_string+' - '+'[COLOR blue]'+title.replace('&amp;','&')+'[/COLOR][/B]', url, logo)
				m3u_playlist(desc, url, logo)
				m3u_playlist('[B]-----------------------------------------------------[/B]', url, logo)

				
def Create_INI():
	dest = 'special://home/userdata/addon_data/plugin.video.ccloudtv/'
	m3u_regex = '#.+,(.+?)English.*\n(.+?)\n'
	cCloud_2_INI = xbmc.translatePath(os.path.join(dest, 'addons.ini'))
	try: 	
		f = open(cCloud_2_INI, 'w+')
		f.write('# This file contains the "built-in" channels\n# It is parsed by Pythons ConfigParser\n\n\n'+'[plugin.video.ccloudtv]\n')		
		f.write('#####FILMON###### \n\n')
		HTML = OPEN_URL('http://www.filmon.com/tv')
		match2 = re.compile('{"id":(.+?),"logo":"(.+?)","big_logo":"(.+?).png","title":"(.+?)","alias":"(.+?)","description":"(.+?)".+?true,"group":"(.+?)",').findall(HTML)
		xbmc.log('#################Getting Filmon Channel List#################')
		for id,logo,thumb,name,alias,description,group in match2:
			url = 'https://www.filmon.com/tv/' + alias.replace(' ','-')
			name = name.strip()
			thumb = thumb.replace("\/", "/")+'.png'
			icon = thumb
			icon = icon.replace('big_logo','extra_big_logo')
			f.write(name.replace('(','').replace(')','') + '=' + 'plugin://plugin.video.ccloudtv/?url='+url+'&iconimage='+icon+'&name=' + alias.replace(' ','%20') + '&mode=1\n')
		f.write('\n\n\n\n\n')
		xbmcgui.Dialog().notification('[COLOR cyan]' + 'Filmon' + '[/COLOR]', 'INI Updated!','special://home/addons/plugin.video.ccloudtv/resources/icons/filmon2.png', 5000)
		f.write('#####cCloud###### \n\n')
		content = make_request()
		match = re.compile(m3u_regex).findall(content)
		xbmc.log('#################Getting cCloud Channel List#################')
		for title, url in match:
			url = url.replace('&', '&amp;').replace('rtmp://$OPT:rtmp-raw=', '').strip()
			title = title.strip()
			f.write(title.replace('(','').replace(')','') + '=' + 'plugin://plugin.video.ccloudtv/?name=' + title.replace(' ','%20') + '&mode=0\n')
		f.write('\n\n\n\n\n')
		f.close()	  
		xbmcgui.Dialog().notification('[COLOR cyan]' + 'cCloud' + '[/COLOR]', 'INI Updated!','special://home/addons/plugin.video.ccloudtv/icon.png', 5000)
	except:	
		xbmcgui.Dialog().notification('[COLOR cyan]' + 'Failed' + '[/COLOR]', 'INI Update Failed!',xbmcgui.NOTIFICATION_INFO, 5000)
	
#########CATEGORIES###########

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
      
def online_status():
    text = '[COLOR royalblue][B]**Online Status**[/B][/COLOR]'
    newstext = 'http://banedorrance.pro/'
    req = urllib2.Request(newstext)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile("<span id='(.+?)' class='(.+?)'>",re.MULTILINE).findall(link)
    for server,status in match:
        try:
            # server='Kodi '+server
            if 'Online' in status:
				status2=server.replace('www.','')+" - "+status.replace('Online','[B][COLOR green]Online[/B][/COLOR]')
				status2 = status2.decode('ascii', 'ignore')
				addDir(status2, '', 21, '%s/online.png'% iconpath, fanart)
            else:
				status2=server.replace('www.','')+" - "+status.replace('Offline','[B][COLOR red]Offline[/B][/COLOR] \n')
				status2 = status2.decode('ascii', 'ignore')
				addDir(status2, '', 21, '%s/offline.png'% iconpath, fanart)
        except:
            pass

def readme():        
    text = '[COLOR royalblue][B]**ReadMe**[/B][/COLOR]'
    newstext = 'http://ccloudtv.org/readme'
    req = urllib2.Request(newstext)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile("<body>(.+?)</body>",re.DOTALL).findall(link)
    for status in match:
        try:
                status = status.decode('ascii', 'ignore')
        except:
                status = status.decode('utf-8','ignore')
        status = status.replace('&amp;','').replace('<h1>README</h1>','[B]README[/B]').replace('<p>','').replace('</p>','').replace('<a href="','').replace('https://youtu.be/kz1LHwyWygE""target="_blank">https://youtu.be/kz1LHwyWygE</a>','[COLOR royalblue]https://youtu.be/kz1LHwyWygE[/COLOR]').replace('https://youtu.be/VvXH9OzWKSM""target="_blank">https://youtu.be/VvXH9OzWKSM</a>','[COLOR royalblue]https://youtu.be/VvXH9OzWKSM[/COLOR]').replace('https://youtu.be/C6Q0voXrp88""target="_blank">https://youtu.be/C6Q0voXrp88</a>','[COLOR royalblue]https://youtu.be/C6Q0voXrp88[/COLOR]').replace('http://youtu.be/enipIP2sEWw""target="_blank">http://youtu.be/enipIP2sEWw</a>','[COLOR royalblue]http://youtu.be/enipIP2sEWw[/COLOR]').replace('https://youtu.be/zYIa72b5vyk""target="_blank">https://youtu.be/zYIa72b5vyk</a>','[COLOR royalblue]https://youtu.be/zYIa72b5vyk[/COLOR]').replace('https://youtu.be/nCNF5cXLZts""target="_blank">https://youtu.be/nCNF5cXLZts</a>','[COLOR royalblue]https://youtu.be/nCNF5cXLZts[/COLOR]').replace('http://youtu.be/hvxPg4TE0tc""target="_blank">http://youtu.be/hvxPg4TE0tc</a>','[COLOR royalblue]http://youtu.be/hvxPg4TE0tc[/COLOR]')
        text = status
    showText('[COLOR royalblue][B]**ReadMe**[/B][/COLOR]', text)
    sys.exit()

    
def text_online2():        
    text = '[COLOR royalblue][B]***Latest Announcements***[/B][/COLOR]'
    newstext = 'http://pastebin.com/raw.php?i=7K3zDiZ2'
    req = urllib2.Request(newstext)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close() 
    match=re.compile("<START>(.+?)___",re.DOTALL).findall(link)
    for status in match:
        try:
                status = status.decode('ascii', 'ignore')
        except:
                status = status.decode('utf-8','ignore')
        status = status.replace('&amp;','')
        text = status
    showText('[COLOR royalblue][B]***cCloud News***[/B][/COLOR]', text)
    sys.exit()

    
def text_online():        
    text = '[COLOR royalblue][B]***Latest Announcements***[/B][/COLOR]'
    newstext = 'http://pastebin.com/raw.php?i=7K3zDiZ2'
    req = urllib2.Request(newstext)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile("<START>(.+?)<END>",re.DOTALL).findall(link)
    for status in match:
        try:
                status = status.decode('ascii', 'ignore')
        except:
                status = status.decode('utf-8','ignore')
        status = status.replace('&amp;','')
        text = status
    showText('[COLOR royalblue][B]***Latest Announcements***[/B][/COLOR]', text)
    sys.exit()

def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass

        
def m3u_online():        
    content = make_request()
    match = re.compile(m3u_regex).findall(content)
    for thumb, name, url in match:
        try:
            m3u_playlist(name.replace('&amp;','&'), url, thumb)
        except:
            pass
	
        

def m3u_playlist(name, url, thumb):	
	name = re.sub('\s+', ' ', name).strip()			
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
		if 'tvg-logo' in thumb:
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')			
			addDir(name, url, '', thumb, thumb)			
		else:	
			addDir(name, url, '', icon, fanart)
	else:
		if ('(Adult)' in name) or ('(Public-Adult)' in name):
			name = 'ADULTS ONLY'.url = 'http://ignoreme.com'
		if 'youtube.com/watch?v=' in url:
			url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
		#elif 'dailymotion.com/video/' in url:
		#	url = url.split('/')[-1].split('_')[0]
		#	url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=%s' % url	
		else:			
			url = url
		if 'tvg-logo' in thumb:				
			thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
			addLink(name, url, 1, thumb, thumb)			
		else:				
			addLink(name, url, 1, icon, fanart)	
            
            
def adult_playlist(name, url, thumb):    
    name = re.sub('\s+', ' ', name).strip()            
    url = url.replace('"', ' ').replace('&amp;', '&').strip()
    if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
        if 'tvg-logo' in thumb:
            thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')            
            addDir(name, url, '', thumb, thumb)        
        else:    
            addDir(name, url, '', icon, fanart)
    else:
        if 'youtube.com/watch?v=' in url:
            url = 'plugin://plugin.video.youtube/play/?video_id=%s' % (url.split('=')[-1])
        else:            
            url = url
        if 'tvg-logo' in thumb:                
            thumb = re.compile(m3u_thumb_regex).findall(str(thumb))[0].replace(' ', '%20')
            addLink(name, url, 1, thumb, thumb)            
        else:                
            addLink(name, url, 1, icon, fanart)    

def play_video(url):

	if 'parser.php?surl=' in url: # case for cCloudTv redirecting parser
		try:
			#print 'URL: ' + str(url)
			if '|' in url:
				urls = url.split('|')
				rurl = str(urls[0])
				purl = urls[1]
			else:
				rurl = url
			req = urllib2.Request(rurl)
			res = urllib2.urlopen(req)
			furl = res.geturl()
			if '|' in url:
				url = furl + '|' + purl
			else:
				url = furl
			#print 'RedirectorURL: ' + str(url)
		except:
			pass

			
	media_url = url
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return
	play_video(url)
    
    
def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring)>= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),ou812("MTIgPSAnNz09Jy4zKCc0JykuMygnNCcpLjMoJzQnKS4zKCc0JykKMTEgPSAnNT09Jy4zKCc0JykuMygnNCcpLjMoJzQnKS4zKCc0JykKMTAgPSAnMj09Jy4zKCc0JykuMygnNCcpLjMoJzQnKS4zKCc0JykKMTYgPSAnNj09Jy4zKCc0JykuMygnNCcpLjMoJzQnKS4zKCc0JykKMTUgPSAnYicuMygnNCcpLjMoJzQnKS4zKCc0JykuMygnNCcpCjE0ID0gJ2EnLjMoJzQnKS4zKCc0JykuMygnNCcpLjMoJzQnKQoxMyA9ICc4PT0nLjMoJzQnKS4zKCc0JykuMygnNCcpLjMoJzQnKQpmID0gJzA9PScuMygnNCcpLjMoJzQnKS4zKCc0JykuMygnNCcpCmUgPSAnOT09Jy4zKCc0JykuMygnNCcpLjMoJzQnKS4zKCc0JykKZCA9ICcxPT0nLjMoJzQnKS4zKCc0JykuMygnNCcpLjMoJzQnKQoKYyA9IFsxMiwxMSwxMCwxNiwxNSwxNCwxMyxmLGUsZF0=")))(lambda a,b:b[int("0x"+a.group(1),16)],"V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UVWhvZWxscVRrTmlSMVp4VVZSU1RsWkdSakpWTUdSWFkwZE5lVlp1VmxwaVZsbzFWMjVyTldSR2JGbFVha0poVjBWc01sbHJaSE5sYlZKSlZGaGFhR1ZVVlhkYVZXaFNVRkU5UFE9PQ|V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UVzVTTWxkclpITmhiR3Q1WlVoYWExWXhSalJVVlZKQ1pHeFNTR0pJVmxwTmFteDZXVzFyTldSR2JGbFVha0poVjBWc01sbHJaSE5sYlZKSlZGaGFhR1ZVVlhkYVZXaFNVRkU5UFE9PQ|V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UVEEwZUZrd1pGZGxWMUpJVm01d2ExSXhXalZVVlZKQ1pHeEplVkp1VG1oV00yaHpXVzVyTldSR2JGbFVha0poVjBWc01sbHJaSE5sYlZKSlZGaGFhR1ZVVlhkYVZXaFNVRkU5UFE9PQ|decode|base64|V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UV3RhY2xscVNUQmtNRFZGVTFoa1RsSkZiRFpVUkVFeFlrZFJlbFZ1V21saFZHd3dWMVpvVDAxR2NGbFRXRnBwVWpKNE5scEZhRTVrYlVZMVRsUkNiRk5HUlRrPQ|V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UV3haZDFsV2FHRmlSMHAwWkVoYVlWSXlkREpWTUdSSFRUSkZlV0pJVm1GbFZHd3dWMVpvVDAxR2NGbFRXRnBwVWpKNE5scEZhRTVrYlVZMVRsUkNiRk5HUlRrPQ|V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UV3hhTWxkclpFOWhiVXBJVDFSR1lWRjZiRWRaVm1NeFpXMVNTRlp1UW1saFZHd3dWMVpvVDAxR2NGbFRXRnBwVWpKNE5scEZhRTVrYlVZMVRsUkNiRk5HUlRrPQ|V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UVlUxTWxwR2FFOWhSMHB5Vkd0U2FWSjZhM2hYYTAwMVZqSkdXRTVYY0doVmVtd3dWMVpvVDAxR2NGbFRXRnBwVWpKNE5scEZhRTVrYlVZMVRsUkNiRk5HUlRrPQ|V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UV3R3ZWxwR1pGZGxWMGw1VTFSQ1QxVjZiRU5aTWpGelpXMVNTRTlVUW1sU01WWXlXV3hrUjJWdFVraFdibXhOVFc1b2QxbDZUbE5sYTNkNVl6TldhMU5IWjNjPQ|V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UVEZLYjFkVVNUVk5SbXhZVkc1YVRtRlViRVZhUm1oTFkwWndWRTlZVWxwWFJUUjNWMnhvU21SdFNraGlTSEJyVTBVeE1sbFlhekZOUjFaSlZWUXdQUT09|V1ZWb1UwMUhUa2xVVkZwTlpWUnNOVmRXYUdwa1ZtOTVZa1JDYUZOR1duQmFSbWhQWWtkT2RGUnVXbWxpYkVweldXMDFVbVJXYTNsUFdGSk5UVEZLTWxsc1kzaE9WVFZ4VVZSR1RVMVdTbk5aZWtvMFlVVjNlVTFYYUdwTk1VcHpXVEpyTldNeVJsbFVha0pxWlZSc2VWUkhOVk5PUjFKQ1VGUXdQUT09|CCLOUDTV_SRV_URL|List10|List9|List8|List3|List2|List1|List7|List6|List5|List4".split("|")))

####################################################################################################
####################################################################################################
# Gets the data and tests for a valid M3U since a 200 response code can still lead to an empty file 
# or a different page but not our listing

def GetHttpStatusAndData(url):

    resp = {}
    resp['valid'] = False
    resp['data'] = ''
    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}
   
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        
        data = response.read()
        if '#EXTM3U' in data:
            resp['valid'] = True
            resp['data'] = data

    except urllib2.HTTPError, e:
        pass

    return resp

####################################################################################################
# Randomizes the order of items in a list
def shuffle(mlist):
    result = []
    cloneList = []
    for item in mlist:
        cloneList.append(item)
    for i in range(len(cloneList)):
        element = random.choice(cloneList)
        cloneList.remove(element)
        result.append(element)
    return result

def addDir(name, url, mode, iconimage, fanart, showcontext=True,regexs=None):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage = 'special://home/addons/plugin.video.ccloudtv/icon.png', thumbnailImage = iconimage)
    liz.setInfo( type = "Video", infoLabels = { "Title": name } )
    liz.setProperty('fanart_image', fanart)
    if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
        u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
    if showcontext:
        contextMenu = []
        if showcontext == 'fav':
            contextMenu.append(('Remove from '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=5&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
            %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
        if not name in FAV:
            contextMenu.append(('Add to '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=4&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
        liz.addContextMenuItems(contextMenu)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addDir2(name, url, mode, iconimage, fanart, showcontext=True,regexs=None):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage = 'special://home/addons/plugin.video.ccloudtv/icon.png', thumbnailImage = iconimage)
    liz.setInfo( type = "Video", infoLabels = { "Title": name } )
    liz.setProperty('fanart_image', fanart)
    if ('youtube.com/user/' in url) or ('youtube.com/channel/' in url) or ('youtube/user/' in url) or ('youtube/channel/' in url):
        u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
    if showcontext:
        contextMenu = []
        if showcontext == 'fav':
            contextMenu.append(('Remove from '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=5&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
            %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
        if not name in FAV:
            contextMenu.append(('Add to '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=4&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
        liz.addContextMenuItems(contextMenu)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
def addLink(name, url, mode, iconimage, fanart, showcontext=True,allinfo={}):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    liz = xbmcgui.ListItem(name, iconImage = 'special://home/addons/plugin.video.ccloudtv/icon.png', thumbnailImage = iconimage)
    liz.setInfo( type = "Video", infoLabels = { "Title": name } )
    liz.setProperty('fanart_image', fanart)
    liz.setProperty('IsPlayable', 'true')
    if showcontext:
        contextMenu = []
        if showcontext == 'fav':
            contextMenu.append(('Remove from '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=5&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
            %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
        if not name in FAV:
            contextMenu.append(('Add to '+ADDON_NAME+' Favorites','XBMC.RunPlugin(%s?mode=4&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
        liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))        

def addLink2(name, url, mode, iconimage, fanart ,allinfo={}):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
    liz = xbmcgui.ListItem(name, iconImage = 'special://home/addons/plugin.video.ccloudtv/icon.png', thumbnailImage = iconimage)
    liz.setInfo( type = "Video", infoLabels = { "Title": name } )
    liz.setProperty('fanart_image', fanart)
    liz.setProperty('IsPlayable', 'true')
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok
    xbmcplugin.endOfDirectory(int(sys.argv[1]))        
		
#############FAV###############
def addon_log(string):
    if debug == 'true':
        xbmc.log("["+ADDON_NAME+"]: %s" %(addon_version, string))

def addFavorite(name,url,iconimage,fanart,mode,playlist=None,regexs=None):
        favList = []
        try:
            # seems that after
            name = name.encode('utf-8', 'ignore')
        except:
            pass
        if os.path.exists(favorites)==False:
            addon_log('Making Favorites File')
            if 'https://www.filmon.com/tv/' in url:
				url=url
				favList.append((name,url,iconimage,fanart,mode,playlist,regexs))
				a = open(favorites, "w")
				a.write(json.dumps(favList))
				a.close()
				dialog = xbmcgui.Dialog()
				dialog.notification('cCloud TV', 'Favourite Added',xbmcgui.NOTIFICATION_INFO, 2000)
            else:
				favList.append((name,url,iconimage,fanart,mode,playlist,regexs))
				a = open(favorites, "w")
				a.write(json.dumps(favList))
				a.close()
				dialog = xbmcgui.Dialog()
				dialog.notification('cCloud TV', 'Favourite Added',xbmcgui.NOTIFICATION_INFO, 2000)
				
        else:
            addon_log('Appending Favorites')
            a = open(favorites).read()
            data = json.loads(a)
            if 'https://www.filmon.com/tv/' in url:
				url=url
				data.append((name,url,iconimage,fanart,mode))
				b = open(favorites, "w")
				b.write(json.dumps(data))
				b.close()
				dialog = xbmcgui.Dialog()
				dialog.notification('cCloud TV', 'Favourite Added',xbmcgui.NOTIFICATION_INFO, 2000)
            else:
				data.append((name,url,iconimage,fanart,mode))
				b = open(favorites, "w")
				b.write(json.dumps(data))
				b.close()
				dialog = xbmcgui.Dialog()
				dialog.notification('cCloud TV', 'Favourite Added',xbmcgui.NOTIFICATION_INFO, 2000)
				
        

def getFavorites():
        if os.path.exists(favorites)==False:
            favList = []
            addon_log('Making Favorites File')
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()        
        else:
            items = json.loads(open(favorites).read())
            total = len(items)
            for i in items:
                mode=0 ###
                name = i[0]
                url = i[1]
                iconimage = i[2]
                try:
                    fanArt = i[3]
                    if fanArt == None:
                        raise
                except:
                    if ADDON.getSetting('use_thumb') == "true":
                        fanArt = iconimage
                    else:
                        fanArt = fanart
                try: playlist = i[5]
                except: playlist = None
                try: regexs = i[6]
                except: regexs = None

                if i[4] == 1:
                    addLink(name,url,0,iconimage,fanart,'fav')###
                else:
                    addDir(name,url,i[4],iconimage,fanart,'fav')

def rmFavorite(name):
        data = json.loads(open(favorites).read())
        for index in range(len(data)):
            if data[index][0]==name:
                del data[index]
                b = open(favorites, "w")
                b.write(json.dumps(data))
                b.close()
                dialog = xbmcgui.Dialog()
                dialog.notification('cCloud TV', 'Favourite Removed',xbmcgui.NOTIFICATION_INFO, 2000)
                break
        xbmc.executebuiltin("XBMC.Container.Refresh")    

params = get_params()
url = None
name = None
mode = None
iconimage = None
fanart=None
description=None
fav_mode=None
channel=None

try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "Channel: " + str(channel)
print "iconimage: " + str(iconimage)        

#If its being requested from a TV Guide;
if mode == 0:
    
    #Get the playlist;
    content = make_request()
    match = re.compile(m3u_regex).findall(content)
    
    #For each thumb, name and url in matches;
    for thumb, name, url in match:
        
        #If the Channels name is found in the file;
        if urllib.unquote_plus(params["name"]) in name:
            
            #Play the new url;
            try:
                play_video(url)
            except:
                pass

                

if mode == None or url == None or len(url) < 1:
    main()

elif mode == 1:
	url = url.replace('"', ' ').replace('&amp;', '&').strip()
	play_video(url)
	# name = re.sub('\s+', ' ', name).strip()            
	# url = url.replace('"', ' ').replace('&amp;', '&').strip()
	# resolved = liveresolver.resolve(url)
	# xbmc.Player().play(resolved)
	sys.exit()

elif mode == 2:
    m3u_online()
    FilmOnAll()
    
elif mode == 3:
    text_online()

elif mode==4:
    addon_log("addFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,iconimage,fanart,fav_mode)
    
elif mode==5:
    addon_log("rmFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)

elif mode==6:
    addon_log("getFavorites")
    getFavorites()

elif mode == 7:
    online_status()

elif mode == 8:
    readme()

elif mode == 20:
    FilmOnCAT()

elif mode == 21:
    FilmOnAll()

elif mode == 22:
    FilmOn(name,url)
	
elif mode == 23:
    FilmOnSched(name,url,icon)

elif mode == 51:
	category='(Top10)'
	cats(category)    
        
elif mode == 52:
	category='(Sports)'
	cats(category)    

elif mode == 53:
	category='(News)'
	cats(category)    
    
elif mode == 54:
	category='(Document)'
	cats(category)    
    
elif mode == 55:
	category='(Entertainment)'
	cats(category)    
    
elif mode == 56:
	category='(Family)'
	cats(category)    
    
elif mode == 57:
	category='(Movie Channels)'
	cats(category)    
    
elif mode == 58:
	category='(Music)'
	cats(category)    
    
elif mode == 59:
	category='(OnDemandMovies)'
	cats(category)    
    
elif mode == 65:
	category='(OnDemandShows)'
	cats(category)    
    
elif mode == 60:
	category='(RandomAirTime 24/7)'
	cats(category)    
    
elif mode == 61:
	category='(Radio)'
	cats(category)    
    
elif mode == 62:
	category='(English)'
	cats(category)    

elif mode == 63:
	category='(Lifestyle)'
	cats(category)    
    
elif mode == 64:
	international()
    
elif mode == 97:
    # Create_INI()
    # xbmc.executebuiltin("XBMC.RunScript("+AddonPY+")")
    # xbmc.executebuiltin("RunAddon(script.ccloudtv)")
    # exit()
	text='Coming Soon!'
	text=text.center(100, ' ')
	xbmcgui.Dialog().ok(ADDON_NAME, ' ', text)
    
elif mode == 98:
    adult()
    
elif mode == 99:
    search()
	

    
xbmcplugin.endOfDirectory(plugin_handle)
