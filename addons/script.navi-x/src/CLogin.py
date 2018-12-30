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
# CDownloader:
# This class handles user login to the Navi-Xtreme website.
#############################################################################

from string import *
import sys, os.path
import urllib
import urllib2
import re, random, string
import xbmc, xbmcgui, xbmcaddon
import re, os, time, datetime, traceback
import shutil
import os
from libs2 import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

LABEL_USRNAME = 141
LABEL_PASSWORD = 142
BUTTON_USRNAME = 143
BUTTON_PASSWORD = 1144
BUTTON_LOGIN = 145
BUTTON_CANCEL = 146

class CDialogLogin(xbmcgui.WindowXMLDialog): 
    def __init__(self,strXMLname, strFallbackPath):#, strDefaultName, forceFallback):
#        self.setCoordinateResolution(PAL_4x3)

        #user background image
#        self.bg = xbmcgui.ControlImage(100,100,520,376, imageDir + "background_txt.png")
#        self.addControl(self.bg)

        self.userloggedin = False
        #read user ID from file
        self.user_id=''
        pass

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
          
    def login(self):
        #display GUI window
        self.doModal()
        #perform login to the Navi-Xtreme server
        
        #if success
        self.save_user_id()
        
    def logout(self):
        self.user_id=''
        self.write_user_id() #There is no such function.
            
    def is_user_logged_in(self):
        if self.user_id != '':
            return True  
        return False
     
    def rate_item(self, mediaitem):
        pass
    
    def read_user_id(self):
        pass
    
    def save_user_id(self):
        pass
        
    #end of class    
        
#use singleton
#login = CDialogLogin("CLoginskin.xml", os.getcwd())
login = CDialogLogin("CLoginskin2.xml", addon.getAddonInfo('path'))
