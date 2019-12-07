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
import xbmc, xbmcgui
import re, os, time, datetime, traceback
import shutil
import os
from libs2 import *
from settings import *

try: Emulating = xbmcgui.Emulating
except: Emulating = False

IMAGE_RATING = 142
BUTTON_RATE1 = 143
BUTTON_RATE2 = 144
BUTTON_RATE3 = 145
BUTTON_RATE4 = 146
BUTTON_RATE5 = 147
BUTTON_RATE = 148
BUTTON_CANCEL = 149
BUTTON_RATE0 = 150

class CDialogRating(xbmcgui.WindowXMLDialog): 
    def __init__(self, strXMLname, strFallbackPath):#, strDefaultName, forceFallback):
        self.setCoordinateResolution(PAL_4x3)

        #user background image
#        self.bg = xbmcgui.ControlImage(100,100,520,376, imageDir + "background_txt.png")
#        self.addControl(self.bg)

        #read user ID from file
        self.state = 0 #success
        self.rating = 0

    def onInit( self ):   
        control=self.getControl(IMAGE_RATING)     
        control.setImage("rating0.png")   
        control=self.getControl(BUTTON_RATE0)
        self.setFocus(control)   

    def onAction(self, action):
        #select item is handled via other onClick().
        if not action.getId() == ACTION_SELECT_ITEM:
            self.onAction1(action)

    def onAction1(self, action):
        if (action == ACTION_PREVIOUS_MENU) or (action == ACTION_PARENT_DIR) or (action == ACTION_PREVIOUS_MENU2):
            self.state = -1
            self.close()
        
        if action == ACTION_SELECT_ITEM:  
            if self.getFocus() == self.getControl(BUTTON_RATE1):
                self.rating = 1
                control=self.getControl(IMAGE_RATING)  
                control.setImage('rating1.png')
            elif self.getFocus() == self.getControl(BUTTON_RATE2):
                self.rating = 2
                control=self.getControl(IMAGE_RATING)  
                control.setImage('rating2.png')  
            elif self.getFocus() == self.getControl(BUTTON_RATE3):
                self.rating = 3
                control=self.getControl(IMAGE_RATING)  
                control.setImage('rating3.png') 
            elif self.getFocus() == self.getControl(BUTTON_RATE4):
                self.rating = 4
                control=self.getControl(IMAGE_RATING)  
                control.setImage('rating4.png')    
            elif self.getFocus() == self.getControl(BUTTON_RATE5):
                self.rating = 5
                control=self.getControl(IMAGE_RATING)  
                control.setImage('rating5.png')                   
          
            elif self.getFocus() == self.getControl(BUTTON_RATE):
                #success
                self.state = 0
                self.close()
            elif self.getFocus() == self.getControl(BUTTON_CANCEL):
                self.state = -1
                self.close()
                
        elif action == ACTION_MOVE_RIGHT:
            if not self.getFocus() == self.getControl(BUTTON_RATE) and not self.getFocus() == self.getControl(BUTTON_CANCEL):
                if self.rating < 5:
                    self.rating = self.rating + 1
                    control=self.getControl(IMAGE_RATING)  
                    control.setImage('rating' + str(self.rating) + '.png')

        elif action == ACTION_MOVE_LEFT:
            if not self.getFocus() == self.getControl(BUTTON_RATE) and not self.getFocus() == self.getControl(BUTTON_CANCEL):
                if self.rating > 0:
                    self.rating = self.rating - 1
                    control=self.getControl(IMAGE_RATING)  
                    control.setImage('rating' + str(self.rating) + '.png')                 
                

    def onFocus( self, controlId ):
        pass
            
    def onClick( self, controlId ):
        if controlId == BUTTON_CANCEL:          
            self.onAction1(ACTION_PREVIOUS_MENU)
        else:
            self.onAction1(ACTION_SELECT_ITEM)   
        pass
   
    def onControl(self, control):
        #self.setFocus(control)
        pass
          
        
    #end of class    
        