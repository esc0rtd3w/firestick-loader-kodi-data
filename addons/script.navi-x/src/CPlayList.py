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

#############################################################################
#
# CPlaylist:
# Playlist class. Supports loading of Navi-X PLX files, RSS2.0 files,
# Youtube, shoutcast and flick feed files.
#############################################################################

from string import *
import sys, os.path, urllib, ftplib, os, socket, re, random, string, xbmc, xbmcgui, re, os, time, datetime, traceback, \
    shutil, zipfile
from libs2 import *
from settings import *
from CFileLoader import *

try:
    Emulating = xbmcgui.Emulating
except:
    Emulating = False


######################################################################
# Description: Playlist class. Contains CMediaItem objects
######################################################################
class CPlayList:
    def __init__(self, *args, **kwargs):
        if (kwargs.has_key('window')):
            self.MainWindow = kwargs['window']
        if (kwargs.has_key('whatlist')):
            self.WhatList = kwargs['whatlist']
        self.version = '0'
        self.background = 'default'
        self.logo = 'none'
        #
        self.icon_playlist = 'default'
        self.icon_rss = 'default'
        self.icon_script = 'default'
        self.icon_plugin = 'default'
        self.icon_video = 'default'
        self.icon_audio = 'default'
        self.icon_image = 'default'
        self.icon_text = 'default'
        self.icon_search = 'default'
        self.icon_download = 'default'
        #
        self.title = ''
        self.type = ''
        self.description = ''
        self.URL = ''
        self.player = 'default'
        self.playmode = 'default'
        self.view = 'default'
        self.start_index = 0
        self.expires = ''
        self.list = []
        self.data = {}
    
    ######################################################################
    # Description: Adds a item to playlist.
    # Parameters : item = CMediaItem obect
    # Return     : -
    ######################################################################
    def add(self, item):
        try:
            self.list.append(item)
        except:
            pass
    
    ######################################################################
    # Description: Insert a item to playlist.
    # Parameters : item = CMediaItem obect
    #              index=index of entry to remove
    # Return     : -
    ######################################################################
    def insert(self, item, index):
        try:
            self.list.insert(index, item)
        except:
            pass
    
    ######################################################################
    # Description: clears the complete playlist.
    # Parameters : -
    # Return     : -
    ######################################################################
    def clear(self):
        try:
            del self.list[:]
        except:
            pass
    
    ######################################################################
    # Description: removes a single entry from the playlist.
    # Parameters : index=index of entry to remove
    # Return     : -
    ######################################################################
    def remove(self, index):
        try:
            del self.list[index]
        except:
            pass
    
    ######################################################################
    # Description: Returns the number of playlist entries.
    # Parameters : -
    # Return     : number of playlist entries.
    ######################################################################
    def size(self):
        try:
            return len(self.list)
        except:
            return 0
    
    ######################################################################
    # Description: Loads a playlist .plx file. File source is indicated by
    #              the 'filename' parameter or the 'mediaitem' parameter.
    # Parameters : filename=URL or local file
    #              mediaitem=CMediaItem object to load
    # Return     : 0=succes,
    #              -1=invalid playlist version,
    #              -2=could not open playlist
    ######################################################################
    def load_plx(self, filename='', mediaitem=CMediaItem(), proxy="CACHING"):
        try:
            # try: import urlresolver
            # except: print ['Error','CPlayList.py - load_plx','faild to import urlresolver','possibly missing t0mm0 module or currupt host plugins.']
            # print 'loadplx proxy =   '+ proxy
            if filename != '':
                self.URL = filename
                if self.URL == favorite_file:      self.URL = xbmc.translatePath(os.path.join(datapaths, favorite_file))
                if self.URL == MyPlaylists_folder: self.URL = xbmc.translatePath(
                    os.path.join(datapaths, MyPlaylists_list))
                if self.URL == MyPlaylists_list:   self.URL = xbmc.translatePath(
                    os.path.join(datapaths, MyPlaylists_list))
                if self.URL == myPlaylistsDirB:    self.URL = xbmc.translatePath(myPlaylistsDir)
                # if self.URL==xbmc.translatePath(os.path.join(myPlaylistsDirB,MyPlaylists_folder)): self.URL = xbmc.translatePath(os.path.join(myPlaylistsDir,MyPlaylists_list))
                if RootFwdCmd in self.URL:
                    if RootFwdCmd in self.URL[0:len(RootFwdCmd)]:
                        self.URL = self.URL.replace(RootFwdCmd, RootDir)
                if RootFwdCmd2 in self.URL:
                    if RootFwdCmd2 in self.URL[0:len(RootFwdCmd2)]:
                        self.URL = self.URL.replace(RootFwdCmd2, RootDir)
                if home_path_HOME2 in self.URL:
                    if home_path_HOME2 in self.URL[0:len(home_path_HOME2)]:
                        self.URL = self.URL.replace(home_path_HOME2, home_path_HOME)
                if home_path_PLAYLIST2 in self.URL:
                    if home_path_PLAYLIST2 in self.URL[0:len(home_path_PLAYLIST2)]:
                        self.URL = self.URL.replace(home_path_PLAYLIST2, home_path_PLAYLIST)
            
            else:
                self.URL = mediaitem.URL
                try:
                    if ('/Playlists/scripts.plx' in self.URL) or ('/playlists/scripts.plx' in self.URL):
                        if ('github.com/HIGHWAY99/navi-x-storage-unit/' in self.URL) or (
                                    'sahara.navixtreme.com/' in self.URL) or ('sahara.tvaddons.ag/' in self.URL):
                            if tfalse(SettingG("scripts-testers")) == True:
                                if SettingG("scripts-testers2").lower() == ("In love with XBMCHUB").lower():
                                    self.URL = self.URL.replace('/Playlists/scripts.plx',
                                                                '/Playlists/scripts-testers.plx').replace(
                                        '/playlists/scripts.plx', '/playlists/scripts-testers.plx')
                            # print ['proxy',proxy,self.URL]
                            proxy = "NEVER"  # proxy="DISABLED"
                except:
                    pass
                if self.URL == favorite_file:      self.URL = xbmc.translatePath(os.path.join(datapaths, favorite_file))
                if self.URL == MyPlaylists_folder: self.URL = xbmc.translatePath(
                    os.path.join(datapaths, MyPlaylists_list))
                if self.URL == MyPlaylists_list:   self.URL = xbmc.translatePath(
                    os.path.join(datapaths, MyPlaylists_list))
                if self.URL == myPlaylistsDirB:    self.URL = xbmc.translatePath(myPlaylistsDir)
                # if self.URL==xbmc.translatePath(os.path.join(myPlaylistsDirB,MyPlaylists_folder)): self.URL=xbmc.translatePath(os.path.join(myPlaylistsDir,MyPlaylists_list))
                if RootFwdCmd in self.URL:
                    if RootFwdCmd in self.URL[0:len(RootFwdCmd)]:
                        self.URL = self.URL.replace(RootFwdCmd, RootDir)
                if RootFwdCmd2 in self.URL:
                    if RootFwdCmd2 in self.URL[0:len(RootFwdCmd2)]:
                        self.URL = self.URL.replace(RootFwdCmd2, RootDir)
                if home_path_HOME2 in self.URL:
                    if home_path_HOME2 in self.URL[0:len(home_path_HOME2)]:
                        self.URL = self.URL.replace(home_path_HOME2, home_path_HOME)
                if home_path_PLAYLIST2 in self.URL:
                    if home_path_PLAYLIST2 in self.URL[0:len(home_path_PLAYLIST2)]:
                        self.URL = self.URL.replace(home_path_PLAYLIST2, home_path_PLAYLIST)
            
            if (self.URL.lower().startswith(TVACoreURL.lower())) and (self.URL != home_URL) and (
                        self.URL != home_URL_old):
                if (tfalse(SettingG("scripts-testers")) == True) and (len(SettingG("scripts-testers2")) > 0):
                    TSTRMSG = urllib.quote_plus(SettingG("scripts-testers2"))
                    if (TstRplcStrng in self.URL):  # and (('.htm' in self.URL) or ('.html' in self.URL)):
                        self.URL = self.URL.replace(TstRplcStrng, TSTRMSG)
                    if ('.php' in self.URL):
                        if '?' in self.URL:
                            self.URL += '&tstrmsg=' + TSTRMSG
                        else:
                            self.URL += '?tstrmsg=' + TSTRMSG
                        TestBug(['NEW URL', self.URL])
                elif (TstRplcStrng in self.URL) and (
                            (tfalse(SettingG("scripts-testers")) == False) or (len(SettingG("scripts-testers2")) == 0)):
                    self.URL = self.URL.replace(TstRplcStrng, '')
            
            if hasattr(self, 'WhatList'):
                TestBug({"WhatList": self.WhatList})
            if hasattr(self, 'MainWindow'):
                TestBug("* Fetching with    window URL=" + str(self.URL))
                try:
                    self.MainWindow.state_busy = 1
                except:
                    pass
                loader = CFileLoader2(window=self.MainWindow)
            else:
                TestBug("* Fetching without window URL=" + str(self.URL))
                loader = CFileLoader2()
            try:
                loader.load(self.URL, proxy=proxy)
            except Exception as e:
                print 'ERROR CPL 236' + str(e)
                traceback.print_exc(file=sys.stdout)
            
            if loader.state == -1:
                return -2
            elif loader.state == -3:
                return -3
            
            data = loader.data.splitlines()

            # defaults
            self.version = '-1'
            self.background = mediaitem.background
            self.logo = 'none'
            if mediaitem.thumb != 'default':
                self.logo = mediaitem.thumb
            KindOfPlaylist = 'navi'
            for LLLL in XMLPlaylistIdentifiers:
                if LLLL in str(loader.data):
                    KindOfPlaylist = 'xml'
                    # if self.URL.lower()==PheonixHome.lower(): self.background=PheonixBG
            if (KindOfPlaylist == 'xml') and ('<sublink>' in str(loader.data)):
                try:
                    import urlresolver
                except:
                    print ['Error', 'CPlayList.py - load_plx', 'faild to import urlresolver',
                           'possibly missing t0mm0 module or currupt host plugins.']
            #
            self.icon_playlist = 'default'
            self.icon_rss = 'default'
            self.icon_script = 'default'
            self.icon_video = 'default'
            self.icon_audio = 'default'
            self.icon_image = 'default'
            self.icon_text = 'default'
            self.icon_search = 'default'
            self.icon_download = 'default'
            #
            self.title = ''
            self.type = 'playlist'
            self.description = ''
            self.player = mediaitem.player
            self.view = mediaitem.view
            self.processor = mediaitem.processor
            self.playmode = 'default'
            self.start_index = 0
            self.expires = ''
            
            # parse playlist entries
            counter = 0
            state = 0
            tmp = ''
            previous_state = 0
            # TestBug(data)
            try:
                # if len(data) > 0:
                for m in data:
                    try:
                        if state == 2:  # parsing description field
                            index = m.find('/description')
                            if index != -1:
                                self.description = self.description + "\n" + m[:index]
                                state = 0
                            else:
                                self.description = self.description + "\n" + m
                        elif state == 3:  # parsing description field
                            index = m.find('/description')
                            if index != -1:
                                tmp.description = tmp.description + "\n" + m[:index]
                                state = 1
                            else:
                                tmp.description = tmp.description + "\n" + m
                        elif state == 4:  # multiline comment
                            if m[:3] == '"""':
                                state = previous_state
                        elif m and m[0] != '#':
                            if m[:3] == '"""':
                                previous_state = state
                                state = 4  # muliline comment state
                                continue  # continue with next line
                            index = m.find('=')
                            
                            if (KindOfPlaylist == 'navi') and (index != -1):
                                key = m[:index]
                                value = m[index + 1:]
                                if key == 'version' and state == 0:
                                    self.version = value
                                    # check the playlist version
                                    if int(self.version) > int(plxVersion):
                                        return -1  # invalid
                                    else:
                                        del self.list[:]
                                elif key == 'background' and state == 0:
                                    self.background = value
                                elif key == 'player' and state == 0:
                                    self.player = value
                                elif key == 'logo' and state == 0:
                                    self.logo = value
                                #
                                elif key == 'icon_playlist' and state == 0:
                                    self.icon_playlist = value
                                elif key == 'icon_rss' and state == 0:
                                    self.icon_rss = value
                                elif key == 'icon_script' and state == 0:
                                    self.icon_script = value
                                elif key == 'icon_video' and state == 0:
                                    self.icon_video = value
                                elif key == 'icon_audio' and state == 0:
                                    self.icon_audio = value
                                elif key == 'icon_image' and state == 0:
                                    self.icon_image = value
                                elif key == 'icon_text' and state == 0:
                                    self.icon_text = value
                                elif key == 'icon_search' and state == 0:
                                    self.icon_search = value
                                elif key == 'icon_download' and state == 0:
                                    self.icon_download = value
                                #
                                elif key == 'title' and state == 0:
                                    self.title = value
                                elif key == 'description' and state == 0:
                                    index = value.find('/description')
                                    if index != -1:
                                        self.description = value[:index]
                                    else:
                                        self.description = value
                                        state = 2  # description on more lines
                                elif key == 'playmode' and state == 0:
                                    self.playmode = value
                                elif key == 'view' and state == 0:
                                    self.view = value
                                elif key == 'data' and state == 0:
                                    self.data = literal_eval(value)
                                elif key == 'type':
                                    if state == 1:
                                        self.list.append(tmp)
                                    else:  # state=0
                                        del self.list[:]
                                    # @todo
                                    tmp = CMediaItem()  # create new item
                                    tmp.type = value
                                    if tmp.type == 'video' or tmp.type == 'audio':
                                        tmp.player = self.player
                                        tmp.processor = self.processor
                                    
                                    counter = counter + 1
                                    state = 1
                                elif key == 'version' and state == 1:
                                    tmp.version = value
                                elif key == 'name':
                                    tmp.name = value
                                elif key == 'date':
                                    tmp.date = value
                                elif key == 'thumb':
                                    tmp.thumb = value
                                elif key == 'icon':
                                    tmp.icon = value
                                elif key == 'URL':
                                    tmp.URL = value
                                    if 'addons://' in value:
                                        tmp.URL = xbmc.translatePath(
                                            value.replace('addons://', 'special://home/addons/'))
                                elif key == 'DLloc':
                                    tmp.DLloc = value
                                elif key == 'player':
                                    tmp.player = value
                                elif key == 'background':
                                    tmp.background = value
                                elif key == 'rating':
                                    tmp.rating = value
                                elif key == 'infotag':
                                    tmp.infotag = value
                                elif key == 'view':
                                    tmp.view = value
                                elif key == 'processor':
                                    tmp.processor = value
                                elif key == 'playpath':
                                    tmp.playpath = value
                                elif key == 'swfplayer':
                                    tmp.swfplayer = value
                                elif key == 'pageurl':
                                    tmp.pageurl = value
                                elif key == 'data':
                                    tmp.data = literal_eval(value)
                                elif key == 'description':
                                    # self.description=' ' #this will make the description field visible
                                    index = value.find('/description')
                                    if index != -1:
                                        tmp.description = value[:index]
                                    else:
                                        tmp.description = value
                                        state = 3  # description on more lines
                            if '>' in m and '</' in m:
                                try:
                                    TestBug({'m': m})
                                    if '"text/javascript"' in m: m = ''
                                    for aa1 in ['item', 'items', 'channel', 'channels', 'dir']:
                                        m = m.replace('<%s>' % aa1, '').replace('</%s>' % aa1, '')
                                    ##used -1,0 and -2,-1 so to deal with multiple <>'s in the same line.
                                    key = m.split('</')[-1].split('>')[0]
                                    value = m.split('</')[-2].split('>')[-1]
                                    TestBug({'key': key, 'value': value})
                                except:
                                    key = '';
                                    value = ''
                                #
                                if key == 'item' and state == 0:
                                    pass
                                elif key == 'background' and state == 0:
                                    self.background = value
                                elif key == 'fanart' and state == 0:  # Pheonix
                                    self.background = value
                                # elif key=='player' and state==0:
                                #        self.player=value
                                elif key == 'logo' and state == 0:
                                    self.logo = value
                                elif key == 'poster' and state == 0:  # Pheonix
                                    self.logo = value
                                #
                                # elif key=='icon_playlist' and state==0:
                                #        self.icon_playlist=value
                                # elif key=='icon_rss' and state==0:
                                #        self.icon_rss=value
                                # elif key=='icon_script' and state==0:
                                #        self.icon_script=value
                                # elif key=='icon_video' and state==0:
                                #        self.icon_video=value
                                # elif key=='icon_audio' and state==0:
                                #        self.icon_audio=value
                                # elif key=='icon_image' and state==0:
                                #        self.icon_image=value
                                # elif key=='icon_text' and state==0:
                                #        self.icon_text=value
                                # elif key=='icon_search' and state==0:
                                #        self.icon_search=value
                                # elif key=='icon_download' and state==0:
                                #        self.icon_download=value
                                #
                                # elif key=='title' and state==0:
                                #                self.title=value
                                # elif key=='description' and state==0:
                                #                index=value.find('/description')
                                #                if index != -1:
                                #                        self.description=value[:index]
                                #                else:
                                #                        self.description=value
                                #                        state=2 #description on more lines
                                # elif key=='playmode' and state==0:
                                #                self.playmode=value
                                elif key == 'view' and state == 0:
                                    self.view = value
                                # elif key=='data' and state==0:
                                #        self.data=literal_eval(value)
                                elif key == 'type':
                                    # if state==1:
                                    #        self.list.append(tmp)
                                    # else: #state=0
                                    #        del self.list[:]
                                    ##@todo
                                    # tmp=CMediaItem() #create new item
                                    tmp.type = value
                                    # if tmp.type=='video' or tmp.type=='audio':
                                    #        tmp.player=self.player
                                    #        tmp.processor=self.processor
                                    #
                                    # counter=counter+1
                                    # state=1
                                elif key == 'version' and state == 1:
                                    tmp.version = value
                                elif (key == 'name') or (key == 'title') or (key == 'message'):  # Cliq & Pheonix
                                    if state == 1:
                                        if (len(tmp.URL) == 0):
                                            tmp.name = '[COLOR red]*[/COLOR] ' + tmp.name + ''
                                        if (tmp.type == 'unknown') and (tmp.URL == ''):
                                            pass
                                        else:
                                            self.list.append(tmp)
                                        TestBug({'1 type': tmp.type, '2 name': tmp.name, '3 URL': tmp.URL,
                                                 '4 thumb': tmp.thumb})
                                    else:  # state=0
                                        del self.list[:]
                                    #
                                    tmp = CMediaItem()  # create new item
                                    # tmp.type=value
                                    # if tmp.type=='video' or tmp.type=='audio':
                                    #        tmp.player=self.player
                                    #        tmp.processor=self.processor
                                    
                                    counter = counter + 1
                                    state = 1
                                    tmp.name = value
                                    
                                    if key == 'message':
                                        tmp.type = 'text'
                                elif key == 'date':  # Pheonix
                                    tmp.date = value
                                elif key == 'thumb':
                                    tmp.thumb = value
                                elif key == 'icon':
                                    tmp.icon = value
                                elif key == 'thumbnail':  # Cliq & Pheonix
                                    if value.lower() == 'none':
                                        pass
                                        # self.view='thumbnails'
                                    else:
                                        tmp.thumb = value
                                        # tmp.icon=value
                                        # self.view='thumbnails'
                                elif (key == 'sublink') or (key == 'SUBLINK'):  # Pheonix
                                    # import urlresolver
                                    try:
                                        value = value.strip()
                                        if (tmp.URL == '') or (tmp.URL.lower().startswith('http') == False):
                                            try:
                                                if (tmp.URL == '') and (value.lower().startswith('rtmp')):
                                                    tmp.type = 'video'
                                                    if '.mp3' in tmp.URL: tmp.type = 'audio'
                                                    tmp.URL = value
                                                elif (urlresolver.HostedMediaFile(
                                                        value).valid_url() and value.lower().startswith('http')):
                                                    tmp.URL = value
                                                    if tmp.URL.lower().startswith('plugin://'):
                                                        tmp.type = 'addon'
                                                        tmp.URL = tmp.URL.replace('plugin://', 'addon://')[1]
                                                    elif tmp.URL.lower().endswith('.xml'):
                                                        tmp.type = 'playlist'
                                                    elif tmp.URL.lower().startswith('http://pastebin.com/'):
                                                        tmp.type = 'playlist'
                                                    else:
                                                        tmp.type = 'video'
                                                    if tmp.type == 'video' or tmp.type == 'audio':
                                                        tmp.player = self.player
                                                        tmp.processor = self.processor
                                                    if tmp.URL.startswith('addons://'):
                                                        tmp.URL = xbmc.translatePath(
                                                            tmp.URL.replace('addons://', 'special://home/addons/'))
                                            except:
                                                pass
                                    except:
                                        pass
                                elif (key == 'URL') or (key == 'url') or (key == 'link') or (
                                            key == 'LINK'):  # Cliq & Pheonix
                                    value = value.strip()
                                    if len(value) > 0:
                                        tmp.URL = value
                                        if tmp.URL.lower().startswith('plugin://'):
                                            tmp.type = 'addon'
                                            tmp.URL = tmp.URL.replace('plugin://', 'addon://')[1]
                                        elif tmp.URL.lower().endswith('.xml'):
                                            tmp.type = 'playlist'
                                        elif tmp.URL.lower().startswith('http://pastebin.com/'):
                                            tmp.type = 'playlist'
                                        else:
                                            tmp.type = 'video'
                                        if tmp.type == 'video' or tmp.type == 'audio':
                                            tmp.player = self.player
                                            tmp.processor = self.processor
                                        if tmp.URL.startswith('addons://'):
                                            tmp.URL = xbmc.translatePath(
                                                tmp.URL.replace('addons://', 'special://home/addons/'))
                                elif key == 'popImage':  # Pheonix
                                    tmp.URL = value
                                    tmp.type = 'image'
                                elif key == 'sound':  # Pheonix
                                    if hasattr(tmp, 'URL') == False:
                                        tmp.URL = value
                                        tmp.type = 'audio'
                                    elif len(tmp.URL) == 0:
                                        tmp.URL = value
                                        tmp.type = 'audio'
                                elif key == 'DLloc':
                                    tmp.DLloc = value
                                elif key == 'player':
                                    tmp.player = value
                                elif key == 'background':
                                    tmp.background = value
                                elif key == 'rating':
                                    tmp.rating = value
                                elif key == 'infotag':
                                    tmp.infotag = value
                                elif key == 'view':
                                    tmp.view = value
                                elif key == 'processor':
                                    tmp.processor = value
                                elif key == 'playpath':
                                    tmp.playpath = value
                                elif key == 'swfplayer':
                                    tmp.swfplayer = value
                                elif key == 'pageurl':
                                    tmp.pageurl = value
                                elif key == 'data':
                                    tmp.data = literal_eval(value)
                                elif key == 'description':
                                    # self.description=' ' #this will make the description field visible
                                    index = value.find('/description')
                                    if index != -1:
                                        tmp.description = value[:index]
                                    else:
                                        tmp.description = value
                                        state = 3  # description on more lines
                    except Exception, e:
                        print ['error on m-line of data', self.URL, m]
                        print'CPL 638 ' + str(e)
            except Exception, e:
                print'CPL 640 ' + str(e)
            if (state == 1) or (previous_state == 1):
                if len(tmp.URL) == 0:
                    tmp.name = '[COLOR red]*[/COLOR] ' + tmp.name + ''
                # if len(self.list)==0 and (len(tmp.name)==0): tmp.name="empty"
                if (tmp.type == 'unknown') and (tmp.URL == ''):
                    pass
                else:
                    self.list.append(tmp)
                try:
                    TestBug({'1 type': tmp.type, '2 name': tmp.name, '3 URL': tmp.URL, '4 thumb': tmp.thumb})
                except:
                    pass
            # if no version ID is found then this is not a valid playlist.
            # the next lines to not work because they current playlist is already lost.
            #        if self.version=='-1':
            #            return -2
            try:
                if len(self.list) == 0 and not data:
                    return -2
            except:
                pass
            return 0  # successful
        
        
        except Exception, e:
            print '* Error during CPlayList.py - load_plx.', str(e);
            return -2
    
    ######################################################################
    # Description: Loads a RSS webfeed.
    # Parameters : filename=URL or local file
    #              mediaitem=CMediaItem object to load
    # Return     : 0=succes,
    #              -1=invalid playlist version,
    #              -2=could not open playlist
    ######################################################################
    def load_rss_20(self, filename='', mediaitem=CMediaItem(), proxy="CACHING"):
        try:
            if filename != '':
                self.URL = filename
            else:
                self.URL = mediaitem.URL
            
            if self.URL[:6] == 'rss://':
                self.URL = self.URL.replace('rss:', 'http:')
            
            loader = CFileLoader2()
            
            loader.load(self.URL, proxy=proxy)
            if loader.state != 0:
                return -2
            data = loader.data.split('<item')
            # data=loader.data.split('<entry')
            
            # defaults
            self.version = plxVersion
            self.background = mediaitem.background
            self.logo = 'none'
            if mediaitem.thumb != 'default':
                self.logo = mediaitem.thumb
            self.title = ''
            self.type = 'rss'
            self.description = ''
            self.player = mediaitem.player
            self.processor = mediaitem.processor
            self.playmode = 'default'
            self.view = 'default'
            self.start_index = 0
            # clear the list
            del self.list[:]
            
            # set the default type
            index = mediaitem.type.find(":")
            if index != -1:
                type_default = mediaitem.type[index + 1:]
            else:
                type_default = ''
            
            counter = 0
            # parse playlist entries
            for m in data:
                if counter == 0:
                    # fill the title
                    index = m.find('<title>')
                    if index != -1:
                        index2 = m.find('</title>')
                        if index != -1:
                            value = m[index + 7:index2]
                            self.title = value
                    
                    index = m.find('<description>')
                    if index != -1:
                        index2 = m.find('</description>')
                        if index2 != -1:
                            value = m[index + 13:index2]
                            self.description = value
                            index3 = self.description.find('<![CDATA[')
                            if index3 != -1:
                                self.description = self.description[9:-3]
                    
                    # fill the logo
                    index = m.find('<image>')
                    if index != -1:
                        index2 = m.find('</image>')
                        if index != -1:
                            index3 = m.find('<url>', index, index2)
                            if index != -1:
                                index4 = m.find('</url>', index, index2)
                                if index != -1:
                                    value = m[index3 + 5:index4]
                                    self.logo = value
                    else:  # try if itunes image
                        index = m.find('<itunes:image href="')
                        if index != -1:
                            index2 = m.find('"', index + 20)
                            if index != -1:
                                value = m[index + 20:index2]
                                self.logo = value
                    
                    counter = counter + 1
                else:
                    tmp = CMediaItem()  # create new item
                    tmp.player = self.player
                    tmp.processor = self.processor
                    
                    # get the publication date.
                    index = m.find('<pubDate')
                    if index != -1:
                        index2 = m.find('>', index)
                        if index2 != -1:
                            index3 = m.find('</pubDate')
                            if index3 != -1:
                                index4 = m.find(':', index2, index3)
                                if index4 != -1:
                                    # value=m[index2+1:index4-2]
                                    value = m[index2 + 1:index3]
                                    value = value.replace('\n', "")
                                    # tmp.name=value
                                    tmp.date = self.parsedate(value)
                    
                    # get the title.
                    index = m.find('<title')
                    if index != -1:
                        index2 = m.find('>', index)
                        if index2 != -1:
                            index3 = m.find('</title>')
                            if index3 != -1:
                                index4 = m.find('![CDATA[', index2, index3)
                                if index4 != -1:
                                    value = m[index2 + 10:index3 - 3]
                                else:
                                    value = m[index2 + 1:index3]
                                value = value.replace('\n', " '")
                                # tmp.name=tmp.name+value
                                tmp.name = value
                    
                    # get the description.
                    index1 = m.find('<content:encoded>')
                    index = m.find('<description>')
                    if index1 != -1:
                        index2 = m.find('</content:encoded>')
                        if index2 != -1:
                            value = m[index1 + 17:index2]
                            # value=value.replace('&#39;',"\'")
                            tmp.description = value
                            index3 = tmp.description.find('<![CDATA[')
                            if index3 != -1:
                                tmp.description = tmp.description[9:-3]
                    elif index != -1:
                        index2 = m.find('</description>')
                        if index2 != -1:
                            value = m[index + 13:index2]
                            # value=value.replace('&#39;',"\'")
                            tmp.description = value
                            index3 = tmp.description.find('<![CDATA[')
                            if index3 != -1:
                                tmp.description = tmp.description[9:-3]
                    
                    # get the thumb
                    index = m.find('<media:thumbnail')
                    if index != -1:
                        tmp.thumb = self.findRSSattribute(m, index + 16, 'url', tmp.thumb)
                        #                    index2=m.find('url=',index+16)
                        #                    if index2 != -1:
                        #                        index3=m.find('"',index2+5)
                        #                        if index3 != -1:
                        #                            value=m[index2+5:index3]
                        #                            tmp.thumb=value
                    
                    if tmp.thumb == 'default':
                        # no thumb image found, therefore grab any jpg image in the item
                        index = m.find('.jpg')
                        if index != -1:
                            index2 = m.rfind('http', 0, index)
                            if index2 != -1:
                                value = m[index2:index + 4]
                                tmp.thumb = value
                    
                    # get the enclosed content.
                    index = m.find('enclosure')
                    index1 = m.find('<media:content')
                    if ((index != -1) or (index1 != -1)):  # and (tmp.processor==''):
                        # enclosure is first choice. If no enclosure then use media:content
                        if (index == -1) and (index1 != -1):
                            index = index1
                        index2 = m.find('url="', index)  # get the URL attribute
                        if index2 != -1:
                            index3 = m.find('"', index2 + 5)
                        else:
                            index2 = m.find("url='", index)
                            if index2 != -1:
                                index3 = m.find("'", index2 + 5)
                        if (index2 != -1) and (index3 != -1):
                            value = m[index2 + 5:index3]
                            tmp.URL = value
                        
                        # get the media type
                        if type_default != '':
                            tmp.type = type_default
                        
                        if tmp.type == 'unknown':
                            index2 = m.find('type="', index)  # get the type attribute
                            if index2 != -1:
                                index3 = m.find('"', index2 + 6)
                                if index3 != -1:
                                    type = m[index2 + 6:index3]
                                    if type[0:11] == 'application':
                                        tmp.type = 'download'
                                    elif type[0:5] == 'video':
                                        tmp.type = 'video'
                        
                        if (tmp.type == 'unknown') and (tmp.URL != ''):  # valid URL found
                            # validate the type based on file extension
                            ext_pos = tmp.URL.rfind('.')  # find last '.' in the string
                            if ext_pos != -1:
                                ext = tmp.URL[ext_pos + 1:]
                                ext = ext.lower()
                                if ext == 'jpg' or ext == 'gif' or ext == 'png':
                                    tmp.type = 'image'
                                elif ext == 'mp3':
                                    tmp.type = 'audio'
                                else:
                                    tmp.type = 'video'
                    if (tmp.type == 'unknown') or (tmp.processor != ''):
                        # else: #no enclosed URL and media content or the processor tag has been set, use the link
                        index = m.find('<link>')
                        if index != -1:
                            index2 = m.find('</link>', index + 6)
                            if index2 != -1:
                                value = m[index + 6:index2]
                                tmp.URL = value
                                
                                # get the media type
                                if type_default != '':
                                    tmp.type = type_default
                                elif value[:6] == 'rss://':
                                    tmp.type = 'rss'
                                else:
                                    tmp.type = 'html'
                    
                    if tmp.URL != '':
                        self.list.append(tmp)
                        counter = counter + 1
            
            # Post rocessing in case of Youtube playlist URL.
            self.load_youtube_postprocessor(filename, mediaitem, proxy)
            
            return 0
        
        except:
            return -2
    
    ######################################################################
    # Description: Loads a atom webfeed.
    # Parameters : filename=URL or local file
    #              mediaitem=CMediaItem object to load
    # Return     : 0=succes,
    #              -1=invalid playlist version,
    #              -2=could not open playlist
    ######################################################################
    def load_atom_10(self, filename='', mediaitem=CMediaItem(), proxy="CACHING"):
        try:
            if filename != '':
                self.URL = filename
            else:
                self.URL = mediaitem.URL
            
            loader = CFileLoader2()
            
            loader.load(self.URL, proxy=proxy)
            if loader.state != 0:
                return -2
            data = loader.data.split('<entry')
            
            # defaults
            self.version = plxVersion
            self.background = mediaitem.background
            self.logo = 'none'
            if mediaitem.thumb != 'default':
                self.logo = mediaitem.thumb
            self.title = ''
            self.type = 'atom'
            self.description = ''
            self.player = mediaitem.player
            self.processor = mediaitem.processor
            self.playmode = 'default'
            self.view = 'default'
            self.start_index = 0
            # clear the list
            del self.list[:]
            
            # set the default type
            index = mediaitem.type.find(":")
            if index != -1:
                type_default = mediaitem.type[index + 1:]
            else:
                type_default = ''
            
            counter = 0
            # parse playlist entries
            for m in data:
                if counter == 0:
                    # fill the title
                    index = m.find('<title>')
                    if index != -1:
                        index2 = m.find('</title>')
                        if index != -1:
                            value = m[index + 7:index2]
                            self.title = value
                    
                    index = m.find('<subtitle')
                    if index != -1:
                        index2 = m.find('</subtitle>')
                        if index2 != -1:
                            value = m[index + 13:index2]
                            self.description = value
                            index3 = self.description.find('<![CDATA[')
                            if index3 != -1:
                                self.description = self.description[9:-3]
                    
                    # fill the logo
                    index = m.find('<logo>')
                    if index != -1:
                        index2 = m.find('</logo>')
                        if index2 != -1:
                            index3 = m.find('http', index, index2)
                            if index3 != -1:
                                index4 = m.find('</', index3, index2 + 2)
                                if index4 != -1:
                                    value = m[index3:index4]
                                    self.logo = value
                    
                    # fill the logo
                    index = m.find('<icon>')
                    if index != -1:
                        index2 = m.find('</icon>')
                        if index2 != -1:
                            index3 = m.find('http', index, index2)
                            if index3 != -1:
                                index4 = m.find('</', index3, index2 + 2)
                                if index4 != -1:
                                    value = m[index3:index4]
                                    self.logo = value
                    
                    counter = counter + 1
                else:
                    tmp = CMediaItem()  # create new item
                    tmp.player = self.player
                    tmp.processor = self.processor
                    
                    # get the publication date.
                    index = m.find('<published')
                    if index != -1:
                        index2 = m.find('>', index)
                        if index2 != -1:
                            index3 = m.find('</published')
                            if index3 != -1:
                                index4 = m.find(':', index2, index3)
                                if index4 != -1:
                                    # value=m[index2+1:index4-3]
                                    value = m[index2 + 1:index3]
                                    value = value.replace('\n', "")
                                    # tmp.name=value
                                    tmp.date = self.parsedate(value)
                    
                    # get the publication date.
                    index = m.find('<updated')
                    if index != -1:
                        index2 = m.find('>', index)
                        if index2 != -1:
                            index3 = m.find('</updated')
                            if index3 != -1:
                                index4 = m.find(':', index2, index3)
                                if index4 != -1:
                                    # value=m[index2+1:index4-3]
                                    value = m[index2 + 1:index3]
                                    value = value.replace('\n', "")
                                    tmp.name = value
                    
                    # get the title.
                    index = m.find('<title')
                    if index != -1:
                        index2 = m.find('>', index)
                        if index2 != -1:
                            index3 = m.find('</title>')
                            if index3 != -1:
                                index4 = m.find('![CDATA[', index2, index3)
                                if index4 != -1:
                                    value = m[index2 + 10:index3 - 3]
                                else:
                                    value = m[index2 + 1:index3]
                                value = value.replace('\n', " '")
                                # tmp.name=tmp.name+' '+value
                                tmp.name = value
                    
                    # get the description.
                    index = m.find('<summary')
                    if index != -1:
                        index2 = m.find('>', index)
                        if index2 != -1:
                            index3 = m.find('</summary')
                            if index3 != -1:
                                value = m[index2 + 1:index3]
                                value = value.replace('\n', "")
                                tmp.description = value
                    
                    if tmp.description == '' and tmp.name != '':
                        tmp.description = tmp.name
                    
                    # get the thumb
                    index = m.find('<link type="image')
                    if index != -1:
                        index2 = m.find('href=', index + 16)
                        if index2 != -1:
                            index3 = m.find('"', index2 + 6)
                            if index3 != -1:
                                value = m[index2 + 6:index3]
                                tmp.thumb = value
                    
                    if tmp.thumb == 'default':
                        # no thumb image found, therefore grab any jpg image in the item
                        index = m.find('.jpg')
                        if index != -1:
                            index2 = m.rfind('http', 0, index)
                            if index2 != -1:
                                value = m[index2:index + 4]
                                tmp.thumb = value
                    
                    # get the enclosed content.
                    index = m.find('<link rel="enclosure')
                    if index == -1:
                        index = m.find('<link')
                    if index != -1:
                        index2 = m.find('href=', index)  # get the URL attribute
                        if index2 != -1:
                            index3 = m.find(m[index2 + 5], index2 + 6)
                            if index3 != -1:
                                value = m[index2 + 6:index3]
                                tmp.URL = value
                        
                        # get the media type
                        if type_default != '':
                            tmp.type = type_default
                        
                        if tmp.type == 'unknown':
                            index2 = m.find('type="', index)  # get the type attribute
                            if index2 != -1:
                                index3 = m.find('"', index2 + 6)
                                if index3 != -1:
                                    type = m[index2 + 6:index3]
                                    if type[0:11] == 'application':
                                        tmp.type = 'download'
                                    elif type[0:5] == 'video':
                                        tmp.type = 'video'
                        
                        if (tmp.type == 'unknown') and (tmp.URL != ''):  # valid URL found
                            # validate the type based on file extension
                            ext_pos = tmp.URL.rfind('.')  # find last '.' in the string
                            if ext_pos != -1:
                                ext = tmp.URL[ext_pos + 1:]
                                ext = ext.lower()
                                if ext == 'jpg' or ext == 'gif' or ext == 'png':
                                    tmp.type = 'image'
                                elif ext == 'mp3':
                                    tmp.type = 'audio'
                                else:
                                    tmp.type = 'html'
                    
                    if tmp.URL != '':
                        self.list.append(tmp)
                        counter = counter + 1
            
            # Post rocessing in case of Youtube playlist URL.
            self.load_youtube_postprocessor(filename, mediaitem, proxy)
            
            return 0
        
        except:
            return -2
    
    ######################################################################
    # Description: Loads a OPML file.
    # Parameters : filename=URL or local file
    #              mediaitem=CMediaItem object to load
    # Return     : 0=succes,
    #              -1=invalid playlist version,
    #              -2=could not open playlist
    ######################################################################
    def load_opml_10(self, filename='', mediaitem=CMediaItem(), proxy="CACHING"):
        try:
            if filename != '':
                self.URL = filename
            else:
                self.URL = mediaitem.URL
            
            loader = CFileLoader2()
            loader.load(self.URL, tempCacheDir + 'feed.xml', proxy=proxy)
            if loader.state != 0:
                return -2
            filename = loader.localfile
            
            try:
                f = open(filename, 'r')
                data = f.read()
                # data=data.split('<outline')
                f.close()
            except IOError:
                return -2
            
            # defaults
            self.version = plxVersion
            self.background = mediaitem.background
            self.logo = 'none'
            if mediaitem.thumb != 'default':
                self.logo = mediaitem.thumb
            self.title = ''
            self.type = 'opml'
            self.description = ''
            self.player = mediaitem.player
            self.playmode = 'default'
            self.view = 'default'
            self.start_index = 0
            # clear the list
            del self.list[:]
            
            # first process the header
            index = data.find('<title>')
            if index != -1:
                index2 = data.find('</title>')
                if index2 != -1:
                    value = data[index + 7:index2]
                    self.title = value
            
            # now process the elements
            data = data.split('<outline')
            
            counter = 0
            # parse playlist entries
            for m in data:
                tmp = CMediaItem()  # create new item
                # fill the title
                index = m.find('text=')
                if index != -1:
                    index2 = m.find('"', index + 6)
                    if index2 != -1:
                        value = m[index + 6:index2]
                        
                        tmp.name = value
                
                index = m.find('image=')
                if index != -1:
                    index2 = m.find('"', index + 7)
                    if index2 != -1:
                        value = m[index + 7:index2]
                        
                        tmp.thumb = value
                
                index = m.find('bitrate=')
                if index != -1:
                    index2 = m.find('"', index + 9)
                    if index2 != -1:
                        value = m[index + 9:index2]
                        
                        tmp.infotag = value
                
                index = m.find('URL=')
                if index != -1:
                    index2 = m.find('"', index + 5)
                    if index2 != -1:
                        value = m[index + 5:index2]
                        
                        tmp.URL = value
                
                index = m.find('type=')
                if index != -1:
                    index2 = m.find('"', index + 6)
                    if index2 != -1:
                        value = m[index + 6:index2]
                        
                        if value == "link":
                            tmp.type = 'opml'
                            if (tmp.thumb == 'default') and (self.logo != 'none'):
                                tmp.thumb = self.logo
                        elif value == 'audio':
                            tmp.type = 'audio'
                        else:
                            tmp.type = 'video'
                
                if tmp.name != "":
                    self.list.append(tmp)
            
            return 0
        
        except:
            return -2
    
    ######################################################################
    # Description: Loads a Flickr Daily feed xml file.
    # Parameters : filename=URL or local file
    #              mediaitem=CMediaItem object to load
    # Return     : 0=succes,
    #              -1=invalid playlist version,
    #              -2=could not open playlist
    ######################################################################
    def load_rss_flickr_daily(self, filename='', mediaitem=CMediaItem(), proxy="CACHING"):
        try:
            if filename != '':
                self.URL = filename
            else:
                self.URL = mediaitem.URL
            
            loader = CFileLoader2()
            loader.load(self.URL, tempCacheDir + 'feed.xml', proxy=proxy)
            if loader.state != 0:
                return -2
            filename = loader.localfile
            
            try:
                f = open(filename, 'r')
                data = f.read()
                data = data.split('<item ')
                f.close()
            except IOError:
                return -2
            
            # defaults
            self.version = plxVersion
            self.background = mediaitem.background
            self.logo = 'none'
            self.title = ''
            self.type = 'rss'
            self.description = ''
            self.player = mediaitem.player
            self.playmode = 'default'
            self.view = 'default'
            self.start_index = 0
            # clear the list
            del self.list[:]
            
            counter = 0
            # parse playlist entries
            for m in data:
                if counter == 0:
                    # fill the title
                    index = m.find('<title>')
                    if index != -1:
                        index2 = m.find('</title>')
                        if index != -1:
                            value = m[index + 7:index2]
                            self.title = value
                    
                    counter = counter + 1
                else:
                    # get the title.
                    index = m.find('<title>')
                    if index != -1:
                        index2 = m.find('</title>', index)
                        if index2 != -1:
                            value = m[index + 7:index2]
                            name = value
                    
                    # get the enclosed content.
                    items = 0
                    index = m.find('<description>')
                    if index != -1:
                        index2 = m.find('</description>', index)
                        if index2 != -1:
                            index3 = m.find('src=', index)
                            while index3 != -1:
                                index4 = m.find('"', index3 + 5)
                                if index4 != -1:
                                    tmp = CMediaItem()  # create new item
                                    tmp.type = 'image'
                                    if items > 0:
                                        tmp.name = name + " " + str(items + 1)
                                    else:
                                        tmp.name = name
                                    
                                    value = m[index3 + 5:index4 - 4]
                                    if value[-6] == '_':
                                        value = value[:-6] + ".jpg"
                                    tmp.URL = value
                                    tmp.thumb = tmp.URL[:-4] + "_m" + ".jpg"
                                    
                                    self.list.append(tmp)
                                    counter = counter + 1
                                    
                                    items = items + 1
                                    index3 = m.find('src=', index4)
            
            return 0
        
        except:
            return -2
    
    ######################################################################
    # Description: Youtube post processor.
    # Parameters : filename=URL or local file
    #              mediaitem=CMediaItem object to load
    # Return     : 0=succes,
    #              -1=invalid playlist version,
    #              -2=could not open playlist
    ######################################################################
    def load_youtube_postprocessor(self, filename='', mediaitem=CMediaItem(), proxy="CACHING"):
        # is this the Youtube API?
        if mediaitem.URL.find("http://gdata.youtube.com") != -1:
            maxresults = 0
            index = mediaitem.URL.find("max-results")
            if index != -1:
                index2 = mediaitem.URL.find("&", index)
                if index2 != -1:
                    maxresults = int(mediaitem.URL[index + 12:index2])
                else:
                    maxresults = int(mediaitem.URL[index + 12:])
            
            if len(self.list) < maxresults:
                # no next page
                return
            
            startindex = 1
            URL = mediaitem.URL
            index = mediaitem.URL.find("start-index")
            if index != -1:
                index2 = mediaitem.URL.find("&", index + 1)
                if index2 != -1:
                    startindex = int(mediaitem.URL[index + 12:index2])
                    URL = mediaitem.URL[:index - 1] + mediaitem.URL[index2:]
                else:
                    startindex = int(mediaitem.URL[index + 12:])
                    URL = mediaitem.URL[:index - 1]
            
            if self.list[len(self.list) - 1].name == 'Next Page':
                startindex = startindex + len(self.list) - 1
            else:
                startindex = startindex + len(self.list)
            
            tmp = CMediaItem()  # create new item
            tmp.type = mediaitem.type
            tmp.name = 'Next Page'
            tmp.icon = imageDir + 'icon_right.png'
            tmp.player = mediaitem.player
            tmp.background = mediaitem.background
            tmp.processor = mediaitem.processor
            
            tmp.URL = URL + "&start-index=%d" % startindex
            
            self.list.append(tmp)
        return
    
    ######################################################################
    # Description: Loads shoutcast XML file.
    # Parameters : filename=URL or local file
    #              mediaitem=CMediaItem object to load
    # Return     : 0=succes,
    #              -1=invalid playlist version,
    #              -2=could not open playlist
    ######################################################################
    def load_xml_shoutcast(self, filename='', mediaitem=CMediaItem(), proxy="CACHING"):
        try:
            if filename != '':
                self.URL = filename
            else:
                self.URL = mediaitem.URL
            
            loader = CFileLoader2()
            
            loader.load(self.URL, tempCacheDir + 'shoutcast.xml', proxy=proxy, retries=2)
            if loader.state == 0:
                filename = loader.localfile
                
                try:
                    f = open(filename, 'r')
                    data = f.read()
                    f.close()
                
                except IOError:
                    return -2  # failed
            else:
                return -2  # failed
            
            # Message(str(counter))
            
            
            # defaults
            self.version = plxVersion
            self.background = mediaitem.background
            #        self.logo='none'
            self.logo = imageDir + "shoutcast.png"
            self.title = 'Shoutcast' + ' - ' + mediaitem.name
            self.type = 'xml_shoutcast'
            self.description = ''
            self.player = mediaitem.player
            self.playmode = 'default'
            self.view = 'default'
            self.start_index = 0
            # clear the list
            del self.list[:]
            
            if True:
                # parse playlist entries
                # entries=data.split('<station name')
                entries = data.split('"genre"')
                for m in entries:
                    tmp = CMediaItem()  # create new item
                    tmp.type = 'audio'
                    tmp.player = self.player
                    
                    index1 = m.find('"name"')
                    if index1 != -1:  # valid entry
                        index2 = m.find('"', index1 + 8)
                        tmp.name = m[index1 + 8:index2]
                    
                    index1 = m.find('"br"')
                    if index1 != -1:
                        index2 = m.find(',', index1 + 5)
                        bitrate = m[index1 + 5:index2]
                        tmp.name = tmp.name + " (" + bitrate + "kbps) "
                        tmp.URL = ''
                    
                    index1 = m.find('"ct"')
                    if index1 != -1:
                        index2 = m.find('"', index1 + 6)
                        np = m[index1 + 6:index2]
                        tmp.name = tmp.name + "- Now Playing: " + np
                    
                    tmp.URL = ''
                    
                    index1 = m.find('"id"')
                    if index1 != -1:
                        index2 = m.find('"', index1 + 6)
                        id = m[index1 + 6:index2]
                        tmp.URL = "http://www.shoutcast.com/sbin/shoutcast-playlist.pls?rn=" + id + "&file=filename.pls"
                        tmp.URL = "http://yp.shoutcast.com/sbin/tunein-station.pls?id=" + id + "&file=filename.pls"
                        
                        self.list.append(tmp)
            
            return 0
        
        except:
            return -2
    
    ######################################################################
    # Description: Loads Quicksilverscreen HTML.
    # Parameters : filename=URL or local file
    #              mediaitem=CMediaItem object to load
    # Return     : 0=succes,
    #              -1=invalid playlist version,
    #              -2=could not open playlist
    ######################################################################
    def load_xml_applemovie(self, filename='', mediaitem=CMediaItem(), proxy="CACHING"):
        try:
            if filename != '':
                self.URL = filename
            else:
                self.URL = mediaitem.URL
            
            loader = CFileLoader2()
            loader.load(self.URL, tempCacheDir + 'page.xml', proxy=proxy)
            if loader.state != 0:
                return -2
            filename = loader.localfile
            
            try:
                f = open(filename, 'r')
                data = f.read()
                entries = data.split('</movieinfo>')
                f.close()
            except IOError:
                return -2
            
            # defaults
            self.version = plxVersion
            self.background = mediaitem.background
            self.logo = 'none'
            self.title = 'Apple Movie Trailers'
            self.type = 'xml_applemovie'
            self.description = ''
            self.player = mediaitem.player
            self.processor = mediaitem.processor
            self.playmode = 'default'
            self.view = 'default'
            self.start_index = 0
            # clear the list
            del self.list[:]
            dates = []  # contains the dates
            
            sortstring = mediaitem.GetType(field=1)
            if sortstring != '':
                sortorder = 'descending'
            else:
                sortorder = 'ascending'
                sortstring = 'releasedate'
            
            # get the publication date and add it to the title.
            index = data.find('<records date')
            if index != -1:
                index2 = data.find(':', index)
                if index2 != -1:
                    value = data[index + 15:index2 - 2]
                    self.title = self.title + " (" + value + ")"
            
            # parse playlist entries
            for m in entries:
                # fill the title
                index = m.find('<title>')
                if index != -1:
                    # create a new entry
                    tmp = CMediaItem()  # create new item
                    tmp.type = 'video'
                    tmp.player = self.player
                    tmp.processor = self.processor
                    
                    index2 = m.find('</title>')
                    if index2 != -1:
                        value = m[index + 7:index2]
                        tmp.name = value
                    
                    # fill the release date
                    date = 0
                    index = m.find('<' + sortstring + '>')
                    if index != -1:
                        index2 = m.find('</' + sortstring + '>')
                        if index2 != -1:
                            value = m[index + len(sortstring) + 2:index2]
                            if value != '':
                                date = int(value[2:4]) * 365
                                date = date + int(value[5:7]) * 31
                                date = date + int(value[8:])
                            tmp.name = value + " - " + tmp.name
                    dates.append(date)
                    
                    # fill the thumb
                    index = m.find('<location>')
                    if index != -1:
                        index2 = m.find('</location>')
                        if index2 != -1:
                            value = m[index + 10:index2]
                            tmp.thumb = value
                    
                    # fill the URL
                    index = m.find('<preview>')
                    if index != -1:
                        index2 = m.find('</large>')
                        if index2 != -1:
                            index3 = m.find('http', index, index2)
                            if index3 != -1:
                                value = m[index3:index2]
                                tmp.URL = value
                    
                    # fill the date
                    index = m.find('<postdate>')
                    if index != -1:
                        index2 = m.find('</postdate>')
                        if index2 != -1:
                            value = m[index + 10:index2]
                            tmp.date = value
                    
                    # fill the description
                    index = m.find('<description>')
                    if index != -1:
                        index2 = m.find('</description>')
                        if index2 != -1:
                            value = m[index + 13:index2]
                            tmp.description = value
                    
                    self.list.append(tmp)
            
            # sort the list according release date
            for i in range(len(dates) - 1):
                oldest = i
                for n in range(i, len(dates)):
                    if sortorder == 'ascending':
                        if dates[n] < dates[oldest]:
                            oldest = n
                    else:
                        if dates[n] > dates[oldest]:
                            oldest = n
                if oldest != i:
                    temp = dates[i]
                    dates[i] = dates[oldest]
                    dates[oldest] = temp
                    
                    temp = self.list[i]
                    self.list[i] = self.list[oldest]
                    self.list[oldest] = temp
            return 0
        
        except:
            return -2
    
    ######################################################################
    # Description: Loads the PLX files from a directory on the local disk.
    #              Filename indicates the root directory to scan. Also the
    #              subdirectorys will be scanned for PLX files.
    # Parameters : filename=URL or local file (dir name)
    #              mediaitem=CMediaItem object to load
    # Return     : 0=succes,
    #              -1=invalid playlist version,
    #              -2=could not open playlist
    ######################################################################
    def load_dir(self, filename='', mediaitem=CMediaItem(), proxy="CACHING"):
        try:
            if filename != '':
                self.URL = filename
            else:
                self.URL = mediaitem.URL
            
            # defaults
            self.version = plxVersion
            self.background = mediaitem.background
            self.logo = 'none'
            #
            self.icon_playlist = 'default'
            self.icon_rss = 'default'
            self.icon_script = 'default'
            self.icon_video = 'default'
            self.icon_audio = 'default'
            self.icon_image = 'default'
            self.icon_text = 'default'
            self.icon_search = 'default'
            self.icon_download = 'default'
            #
            self.title = mediaitem.name
            self.type = 'directory'
            self.description = ''
            self.player = mediaitem.player
            self.playmode = 'default'
            self.view = 'default'
            self.start_index = 0
            # clear the list
            del self.list[:]
            
            # set the default type
            index = mediaitem.type.find(":")
            if index != -1:
                type_default = mediaitem.type[index + 1:]
            else:
                type_default = ''
            
            if self.URL[:3] != 'ftp':
                # local directory
                
                if self.URL[1] != ':':
                    # self.URL=RootDir+self.URL
                    self.URL = xbmc.translatePath(os.path.join(datapaths, self.URL))
                    if self.URL == MyXBMC_list: self.URL = RootDir + self.URL
                    # if self.URL==history_list: self.URL=RootDir+self.URL
                    # if self.URL==parent_list: self.URL=RootDir+self.URL
                    if self.URL == downloads_file: self.URL = RootDir + self.URL
                    # if self.URL==downloads_complete: self.URL=RootDir+self.URL
                    # if self.URL==downloads_queue: self.URL=RootDir+self.URL
                    # if self.URL==favorite_file: self.URL=xbmc.translatePath(os.path.join(datapaths,self.URL))
                    # if self.URL=='favorites': self.URL=xbmc.translatePath(os.path.join(datapaths,self.URL))
                    # if self.URL==MyPlaylists_folder: self.URL=xbmc.translatePath(os.path.join(datapaths,self.URL))
                    # if self.URL==MyPlaylists_list: self.URL=xbmc.translatePath(os.path.join(datapaths,self.URL))
                
                if not os.path.exists(self.URL):
                    return -2
                
                # parse directory (including subdirectory) entries
                try:
                    for root, dirs, files in os.walk(self.URL, topdown=False):
                        for name in files:
                            ext = getFileExtension(name)
                            ext = ext.lower()
                            tmp = CMediaItem()  # create new item
                            if ext == 'jpg' or ext == 'gif' or ext == 'png':
                                tmp.type = 'image'
                            elif ext == 'mp3' or ext == 'wav':
                                tmp.type = 'audio'
                            elif ext == 'plx' or ext == 'php' or ext == 'html' or ext == 'htm' or ext == 'xml':
                                tmp.type = 'playlist'
                            elif ext == 'txt':
                                tmp.type = 'text'
                            elif ext == 'avi' or ext == 'mp4' or ext == 'm4v' or ext == 'mkv' or \
                                            ext == 'flv' or ext == 'mov' or ext == '3gp':
                                tmp.type = 'video'
                            else:
                                tmp.type = ''
                            tmp.name = name
                            tmp.URL = os.path.join(root, name)
                            self.list.append(tmp)
                            
                            '''if name[-4:]=='.plx':
                                        tmp=CMediaItem() #create new item
                                        tmp.type='playlist'
                                        tmp.name=name[:-4]
                                        tmp.URL=os.path.join(root,name)
                                        self.list.append(tmp)
                                '''
                except IOError:
                    return -2
            else:
                # FTP directory
                if self.URL[-1] != '/':
                    self.URL = self.URL + '/'
                urlparse = CURLParseFTP(self.URL)
                
                try:
                    self.f = ftplib.FTP()
                    self.f.connect(urlparse.host, urlparse.port)
                except (socket.error, socket.gaierror), e:
                    print 'ERROR: cannot reach "%s"' % urlparse.host
                    return -2
                
                print '*** Connected to host "%s"' % urlparse.host
                
                try:
                    if urlparse.username != '':
                        self.f.login(urlparse.username, urlparse.password)
                    else:
                        self.f.login()
                except ftplib.error_perm:
                    print 'ERROR: cannot login'
                    self.f.quit()
                    return -2
                
                print '*** Logged in ***'
                
                try:
                    if urlparse.path != '':
                        self.f.cwd(urlparse.path)
                except ftplib.error_perm:
                    print 'ERROR: cannot CD to "%s"' % urlparse.path
                    self.f.quit()
                    return -2
                
                print '*** Changed to "%s" folder' % urlparse.path
                
                dir_LIST = []
                try:
                    self.f.retrlines('LIST', dir_LIST.append)
                except ftplib.error_perm:
                    print 'ERROR: cannot read directory'
                    
                    #            print dir_LIST
                    
                    #            dir_NLST = []
                    #            try:
                    #                self.f.retrlines('NLST',dir_NLST.append)
                    #            except ftplib.error_perm:
                    #                print 'ERROR: cannot read directory'
                    
                    #            print dir_NLST
                
                for i in range(len(dir_LIST)):
                    tmp = CMediaItem()  # create new item
                    # tmp.name=dir_NLST[i]
                    tmp.name = dir_LIST[i][49:]
                    
                    if dir_LIST[i][0] == 'd':
                        tmp.type = 'directory'
                        if type_default != '':
                            tmp.type = tmp.type + ":" + type_default
                    elif type_default != '':
                        tmp.type = type_default
                    else:
                        # ext=getFileExtension(dir_NLST[i])
                        ext = getFileExtension(dir_LIST[i])
                        ext = ext.lower()
                        if ext == 'jpg' or ext == 'gif' or ext == 'png':
                            tmp.type = 'image'
                        elif ext == 'mp3' or ext == 'wav':
                            tmp.type = 'audio'
                        elif ext == 'plx' or ext == 'php' or ext == 'html' or ext == 'htm' or ext == 'xml':
                            tmp.type = 'playlist'
                        elif ext == 'txt':
                            tmp.type = 'text'
                        elif ext == 'avi' or ext == 'mp4' or ext == 'm4v' or ext == 'mkv' or \
                                        ext == 'flv' or ext == 'mov' or ext == '3gp':
                            tmp.type = 'video'
                        else:
                            tmp.type = 'download'
                    
                    # tmp.URL=self.URL+dir_NLST[i]
                    tmp.URL = self.URL + dir_LIST[i][49:]
                    self.list.append(tmp)
            
            return 0
            
            #    def load_dir_callback1(self,string):
            #        tmp=CMediaItem() #create new item
            #        if string[0]=='d':
            #            tmp.type='playlist'
            #        self.list.append(tmp)
            
            #    def load_dir_callback2(self,string):
            #        self.list[
        
        except Exception, e:
            print '* Error during CPlayList.py - load_dir.', str(e);
            return -2
    
    ######################################################################
    # Description: Saves a playlist .plx file to disk.
    # Parameters : filename=local path+file name
    # Return     : -
    ######################################################################
    def save(self, filename, start=0, end=-1):
        try:
            if end == -1:
                end = len(self.list)
            
            f = open(filename, 'w')
            f.write('version=' + self.version + '\n')
            if self.background != 'default':
                f.write('background=' + self.background + '\n')
            if self.logo != 'none':
                f.write('logo=' + self.logo + '\n')
            f.write('title=' + self.title + '\n')
            if self.description != '':
                f.write('description=' + self.description + '/description' + '\n')
            if self.player != 'default':
                f.write('player=' + self.player + '\n')
            if self.playmode != 'default':
                f.write('playmode=' + self.playmode + '\n')
            if self.view != 'default':
                f.write('view=' + self.view + '\n')
            if self.expires != '':
                f.write('expires=' + self.expires + '\n')
            f.write('#\n')
            
            for i in range(start, end):
                f.write('type=' + self.list[i].type + '\n')
                f.write('name=' + self.list[i].name + '\n')
                if self.list[i].description != '':
                    f.write('description=' + self.list[i].description + '/description' + '\n')
                if self.list[i].thumb != 'default':
                    f.write('thumb=' + self.list[i].thumb + '\n')
                if self.list[i].icon != 'default':
                    f.write('icon=' + self.list[i].icon + '\n')
                if self.list[i].background != 'default':
                    f.write('background=' + self.list[i].background + '\n')
                f.write('URL=' + self.list[i].URL + '\n')
                if self.list[i].player != 'default':
                    f.write('player=' + self.list[i].player + '\n')
                if self.list[i].processor != '':
                    f.write('processor=' + self.list[i].processor + '\n')
                if self.list[i].date != '':
                    f.write('date=' + self.list[i].date + '\n')
                if len(self.list[i].DLloc) > 0:
                    f.write('DLloc=' + self.list[i].DLloc + '\n')
                f.write('#\n')
            f.close()
        
        except:
            pass
    
    ######################################################################
    def parsedate(self, datestring):
        short_weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # TestBug(datestring)
        
        try:
            s = datestring.split()
            
            if len(s) > 1:
                # RFC822
                day = s[1]
                month = str(months.index(s[2]) + 1)
                year = s[3]
                tim = s[4]  # time
            else:
                # ISO8601
                dt = datestring.split('T')
                d = dt[0].split('-')
                day = d[2]
                month = d[1]
                year = d[0]
                tim = dt[1][:-1]
        except ValueError:
            # no match
            return ""
        
        return year + '-' + month + '-' + day + ' ' + tim
    
    ######################################################################
    def findRSSattribute(self, datastring, startpos, attribute, defaultstring):
        try:
            index = datastring.find(attribute, startpos)
            if index != -1:
                index1 = datastring.find('"', index + len(attribute))
                index2 = datastring.find("'", index + len(attribute))
                
                if (index1 != -1) and ((index2 == -1) or (index1 < index2)):
                    index3 = datastring.find('"', index1 + 1)
                    if index3 != -1:
                        return datastring[index1 + 1:index3]
                
                if (index2 != -1) and ((index1 == -1) or (index2 < index1)):
                    index3 = datastring.find("'", index2 + 1)
                    if index3 != -1:
                        return datastring[index2 + 1:index3]
            
            return defaultstring
        except:
            pass
