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
# CTextView:
# Text viewer class. Displays a text file in a new window.
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
from settings import *
from CFileLoader import *
from libs2 import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

######################################################################
# Description: Text viewer
######################################################################
class CTextView(xbmcgui.WindowXMLDialog): 
    def __init__(self,strXMLname, strFallbackPath):#, strDefaultName, forceFallback):

        self.setCoordinateResolution(PAL_4x3)
    
        #user background image
        self.bg = xbmcgui.ControlImage(0,0,720,576, imageDir + "background_txt.png")
        self.addControl(self.bg)
        
        #background overlay image (to darken the user background)       
        self.bg1 = xbmcgui.ControlImage(0,0,720,576, imageDir + "background_txt.png")
        self.addControl(self.bg1)
        
        self.offset = 0

    def onInit( self ):
        control=self.getControl(130)
        control.setText(self.text) 
        
        control=self.getControl(132)
        self.setFocus(control)
 
    def onAction(self, action):
        if (action == ACTION_PREVIOUS_MENU) or (action == ACTION_PARENT_DIR) or (action == ACTION_PREVIOUS_MENU2):# or (action == ACTION_MOVE_LEFT):
            self.close()

    def onFocus( self, controlId ):
        pass
            
    def onClick( self, controlId ):
        pass
            
    def onControl(self, control):
        #self.setFocus(control)
        pass

    ######################################################################
    # Description: Reads the document and prepares the display. The
    #              document will not be displayed yet. For this the 
    #              doModal() method needs to be called.
    #              There are two ways to open a document. Using a URL to
    #              the file or to use a CMediaItem object contain all
    #              information (including the background image).
    # Parameters : URL=(optional) URL to the (local) file;
    #              mediaitem=(optional) CMediaItem object containing all 
    #              information.
    #              URL(optional)=link to media file;
    # Return     : -
    ######################################################################
    def OpenDocument(self, URL='', mediaitem=0):
        if mediaitem == 0:
            mediaitem=CMediaItem()
        
        #from here we use the mediaitem object
        loader = CFileLoader2()
        #first load the background image
        if (mediaitem.background != 'default'): #default BG image
            ext = getFileExtension(mediaitem.background)
            loader.load(mediaitem.background, imageCacheDir + "backtextview." + ext, 5, proxy="ENABLED")
            if loader.state == 0: #if this fails we still continue
                self.bg.setImage(loader.localfile)
        
        if URL == '':
            URL = mediaitem.URL
        
        #now load the text file
        loader.load(URL, tempCacheDir + 'document.txt')
        if loader.state == 0:
            #open the local file
            try:            
                f=open(loader.localfile, 'r')
                data = f.read()
                f.close()
                self.text=""
                lines = data.split("\n")
                #we check each line if it exceeds 80 characters and does not contain
                #any space characters (e.g. long URLs). The textbox widget does not
                #split up these strings. In this case we add a space characters ourself.
                for m in lines:
                    if (len(m) > 80) and (m.find(" ") == -1):
                        m = m[:80] + " " + m[80:]
                    self.text = self.text + m + "\n"
                
                self.offset = 0
                return 0 #success
            except IOError:
                return -1 #failure
        else:
            return -1 #failure   
        
