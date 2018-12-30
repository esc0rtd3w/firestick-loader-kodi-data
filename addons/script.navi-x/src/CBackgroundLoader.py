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
# CBackgroundLoader:
# This class loads playlists properties in a separate background task.
# At this moment loading of the thumbnail images are handled by this task.
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui
import re, os, time, datetime, traceback
import shutil
import zipfile
import threading
from settings import *
from CFileLoader import *
from libs2 import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

######################################################################
# Description: Background loader thread
######################################################################
class CBackgroundLoader(threading.Thread):
    def __init__(self, *args, **kwargs):
      try:
        if (kwargs.has_key('window')):
            self.MainWindow = kwargs['window']
        else:
            self.MainWindow = 0

        threading.Thread.__init__(self)

        self.setDaemon(True) #make a deamon thread

        self.killed = False

        self.counter=0
        self.URL = ''
        self.URL2 = ''
        self.page = 0
      except: pass

    def run(self):
        try:
            while self.killed == False:
                time.sleep(0.1) #delay 0,1 second
            
                if self.MainWindow.list == self.MainWindow.list5:
                    self.LoadThumbPanelView()
                else:
                    self.LoadThumbListView()
            
                self.LoadBackGroundImage()
            
                self.UpdateTime()
        except: pass
    def kill(self):
      try:
        self.killed = True
      except: pass

#    def notify(self):
#        self.event.set()

    ######################################################################
    # Description: Displays the logo or media item thumb on left side of
    #              the screen.
    # Parameters : -
    # Return     : -
    ######################################################################
    def LoadThumbPanelView(self):
        try:
            if (self.URL != self.MainWindow.URL) or (self.page != self.MainWindow.page):
                self.URL = self.MainWindow.URL
                self.counter = 0
            self.MainWindow.user_thumb.setVisible(0)
            self.MainWindow.rating.setVisible(0)
            
            position = self.MainWindow.getPlaylistPosition()
            if position == position + (self.MainWindow.page * self.MainWindow.page_size) - 1:
                self.DisplayMediaSource("")
            else:
                self.DisplayMediaSource(position)
            
            # search for entry that is not in the cache
            while (self.MainWindow.state_busy == 0) \
                    and (self.URL == self.MainWindow.URL) \
                    and (self.counter <= self.MainWindow.page_size + 1):
                try:
                    if (self.MainWindow.page > 0):
                        index = self.counter + (self.MainWindow.page * self.MainWindow.page_size) - 1
                    else: index = self.counter
                    
                    m = self.MainWindow.pl_focus.list[index].thumb
                    # For future use of list thumb if a thumbnail is not provided in the list entry
                    # if (m == 'default') or (m == ""):  # no thumb image
                    #     m = self.MainWindow.pl_focus.logo  # use the logo instead
                    listentry = self.MainWindow.list5.getListItem(self.counter)
                    # Setup non-user defined button art
                    if ((self.counter <= 0 and (self.MainWindow.page >= 0)) \
                                or ((self.counter == self.MainWindow.list.size() - 1) \
                                            and (self.MainWindow.page_size <= self.MainWindow.list.size()) \
                                            and (self.counter >= self.MainWindow.page_size))) \
                            or 'sorted' in self.MainWindow.pl_focus.list[index].name.lower() \
                            or '<<<' in self.MainWindow.pl_focus.list[index].name \
                            or '>>>' in self.MainWindow.pl_focus.list[index].name:
                        
                        if (self.counter <= 0 and self.MainWindow.page <= 0) \
                                and 'sorted by' in self.MainWindow.pl_focus.list[index].name.lower():
                            listentry.setThumbnailImage(imageDir + 'icon_sort.png')
                        elif (self.counter <= 0 and self.MainWindow.page > 0) \
                                or '<<<' in self.MainWindow.pl_focus.list[index].name:
                            listentry.setThumbnailImage(imageDir + 'icon_left4.png')
                        elif (self.counter == self.MainWindow.list.size() - 1 \
                                      and self.MainWindow.page_size <= self.MainWindow.list.size()) \
                                or '>>>' in self.MainWindow.pl_focus.list[index].name:
                            listentry.setThumbnailImage(imageDir + 'icon_right.png')
                    # User defined buttons
                    elif (m != 'default'):  # no thumb image
                        ext = getFileExtension(m)
                        loader = CFileLoader2()  # file loader
                        for prox in "INCACHE", "ENABLED", "":
                            if prox == "":
                                loader.load(m, imageCacheDir + "thumb." + ext)
                            else:
                                loader.load(m, imageCacheDir + "thumb." + ext, timeout=20, \
                                            proxy=prox, content_type='image')
                                # if loader.state == 0:
                                #     break
                        listentry = self.MainWindow.list5.getListItem(self.counter)
                        listentry.setThumbnailImage(loader.localfile)
                    self.counter += 1
                except Exception as e:
                    # print "LoadThumbPanelView() failed." , '\t\t\te= '+str(e), '\t\t\tself.URL= '+str(self.URL), '\t\t\tm= '+str(m)
                    self.counter += 1
        except:
            pass
    
    ######################################################################
    # Description: Displays the logo or media item thumb on left side of
    #              the screen.
    # Parameters : -
    # Return     : -
    ######################################################################
    def LoadThumbListView(self):
        try:
            index = self.MainWindow.getPlaylistPosition()
            index2 = -2  # this value never will be reached
            thumb_update = False
            
            try:
                while (self.MainWindow.state_busy == 0) and (index != index2):
                    index = self.MainWindow.getPlaylistPosition()
                    if (index != -1) and (self.MainWindow.pl_focus.size() > 0):
                        self.UpdateRateingImage(index)
                        self.DisplayMediaSource(index)
                        
                        # now update the thumb
                        m = self.MainWindow.pl_focus.list[index].thumb
                        
                        if (m == 'default') or (m == ""):  # no thumb image
                            m = self.MainWindow.pl_focus.logo  # use the logo instead
                            if m != self.MainWindow.userthumb:
                                self.MainWindow.user_thumb.setVisible(0)
                        
                        if m != self.MainWindow.userthumb:
                            # diffent thumb image
                            if (m == 'default') or (m == ""):  # no image
                                self.MainWindow.thumb_visible = False
                            elif m != 'previous':  # URL to image located elsewhere
                                ext = getFileExtension(m)
                                if (ext != 'jpg') and (ext != 'png') and (ext != 'gif'):
                                    ext = ''
                                loader = CFileLoader2()  # file loader
                                loader.load(m, imageCacheDir + "thumb." + ext, timeout=20, \
                                            proxy="ENABLED", content_type='image')
                                if loader.state == 0:  # success
                                    self.MainWindow.thumb_visible = True
                                    thumb_update = True
                                else:
                                    self.MainWindow.thumb_visible = False
                            self.MainWindow.userthumb = m
                    else:  # the list is empty
                        self.MainWindow.thumb_visible = False
                    
                    index2 = self.MainWindow.getPlaylistPosition()
                
                if (self.MainWindow.state_busy == 0) and (self.MainWindow.thumb_visible == True):
                    if thumb_update == True:
                        self.MainWindow.user_thumb.setVisible(0)
                        self.MainWindow.user_thumb.setImage("")
                        self.MainWindow.user_thumb.setImage(loader.localfile)

                    self.MainWindow.user_thumb.setVisible(1)
                else:
                    self.MainWindow.user_thumb.setVisible(0)
            except Exception, e:
                print "LoadThumbListView() failed.", str(e)
        except:
            pass
    
    ######################################################################
    # Description: Displays the logo or media item thumb on left side of
    #              the screen.
    # Parameters : -
    # Return     : -
    ######################################################################
    def LoadBackGroundImage(self):
        try:
            if (self.URL2 != self.MainWindow.URL) and (self.MainWindow.state_busy == 0):
                self.URL2 = self.MainWindow.URL
                
                # set the background image
                if self.MainWindow.disable_background == 'false':
                    m = self.MainWindow.playlist.background
                else:
                    m = 'default'
                
                if m == 'default':
                    m = self.MainWindow.default_background
                
                if m == 'default':  # default BG image
                    self.MainWindow.bg.setImage(imageDir + background_image1)
                    self.MainWindow.bg1.setImage(imageDir + background_image2)
                    self.MainWindow.background = m
                elif m != 'previous':  # URL to image located elsewhere
                    ext = getFileExtension(m)
                    loader = CFileLoader2()  # file loader
                    loader.load(m, imageCacheDir + "background." + ext, timeout=20, \
                                proxy="ENABLED", content_type='image')
                    if loader.state == 0:
                        self.MainWindow.bg.setImage(loader.localfile)
                        self.MainWindow.bg1.setImage(imageDir + background_image2)
                    else:
                        self.MainWindow.bg.setImage(imageDir + background_image1)
                        self.MainWindow.bg1.setImage(imageDir + background_image2)
                        self.MainWindow.background = m
        except: pass
    
    ######################################################################
    # Description: Update the time
    # Parameters : -
    # Return     : -
    ######################################################################
    def UpdateTime(self):
        try:
            today = datetime.date.today()
            self.MainWindow.dt.setLabel(time.strftime("%A, %d %B | %I:%M %p"))
        except: pass
    
    ######################################################################
    # Description: Sets the rating image.
    # Parameters : -
    # Return     : -
    ######################################################################
    def UpdateRateingImage(self, pos):
        try:
            rating = self.MainWindow.pl_focus.list[pos].rating
            if rating != '':
                self.MainWindow.rating.setImage('rating' + rating + '.png')
                self.MainWindow.rating.setVisible(1)
            else:
                self.MainWindow.rating.setVisible(0)
        except: pass
    
    ######################################################################
    # Description: Display the media source for processor based entries.
    # Parameters : -
    # Return     : -
    ######################################################################
    def DisplayMediaSource(self, pos):
        try:
            try: str_url = self.MainWindow.pl_focus.list[pos].URL
            except: str_url = ""
            # try:
            #  if "://" in str_url: ProtocolMarker=str_url.split("://")[0]
            #  else: ProtocolMarker="Local"
            # except: ProtocolMarker=""
            ##TestBug("ProtocolMarker (navix.py): "+ProtocolMarker)
            # if hasattr(self,'labProtocol'):
            #    try: self.MainWindow.labProtocol.setLabel(ProtocolMarker.upper());
            #    except:
            #        try: self.MainWindow.labProtocol.setLabel("");
            #        except: pass
            str_server_report = ""
            if str_url != "" and self.MainWindow.pl_focus.list[pos].type != "playlist":
                match = re_server.search(str_url)
                if match:
                    str_server_report = match.group(1)
                    if self.MainWindow.pl_focus.list[pos].processor != "":
                        str_server_report = str_server_report + "+"
            SetInfoText(str_server_report)
        except: pass
