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
##############################################################################

#############################################################################
#
# CDialogBrowse:
# This class is a non-standard dialog window which is used for downloading 
# and file selection.
# @todo: Use WindowXMLDialog instead of the WindowDialog for better customization
# @todo: fix layout issues for non-XBOX platforms.
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

try:
    Emulating = xbmcgui.Emulating
except:
    Emulating = False

LABEL_TITLE = 141
TEXT_PATH = 142
BUTTON_BROWSE = 143
BUTTON_EDIT = 144
BUTTON_OK = 145
BUTTON_CANCEL = 146


######################################################################
# Description: Browse dialog class
######################################################################
class CDialogBrowse(xbmcgui.WindowXMLDialog):
    def __init__(self, strXMLname, strFallbackPath):
        self.setCoordinateResolution(PAL_4x3)
        self.filename = ''
        self.dir = ''
    
    def onInit(self):
        control = self.getControl(LABEL_TITLE)
        control.setLabel(self.label)
        
        self.SetLabel(self.dir + self.filename)
        
        control = self.getControl(BUTTON_OK)
        self.setFocus(control)
    
    def onAction(self, action):
        # select item is handled via other onClick().
        if not action.getId() == ACTION_SELECT_ITEM:
            self.onAction1(action)
    
    def onAction1(self, action):
        if (action == ACTION_PREVIOUS_MENU) or (action == ACTION_PARENT_DIR) or (action == ACTION_PREVIOUS_MENU2):
            self.state = -1  # success
            self.close()  # exit
        
        if action == ACTION_SELECT_ITEM:
            if self.getFocus() == self.getControl(BUTTON_OK):
                if (self.dir.lower().startswith('http://') == False) and (
                    self.dir.lower().startswith('ftp://') == False):
                    self.state = 0  # success
                    self.close()  # exit
                elif os.path.exists(self.dir) == False:
                    dialog = xbmcgui.Dialog()
                    dialog.ok("Error", "Destination directory does not exist")
                else:
                    self.state = 0  # success
                    self.close()  # exit
            if self.getFocus() == self.getControl(BUTTON_CANCEL):
                self.state = -1  # success
                self.close()  # exit
            if self.getFocus() == self.getControl(BUTTON_EDIT):
                keyboard = xbmc.Keyboard(self.dir + self.filename)
                keyboard.doModal()
                
                if (keyboard.isConfirmed() == True):
                    fn = keyboard.getText()
                    pos = fn.rfind(SEPARATOR)  # find last '\' in the string
                    if fn.lower().startswith('http://') or fn.lower().startswith('ftp://'):
                        filename = fn
                        self.filename = fn
                    elif pos != -1:
                        self.dir = fn[:pos + 1]
                        filename = fn[pos + 1:]
                        if len(filename) > 42:
                            dialog = xbmcgui.Dialog()
                            dialog.ok("Error", "Filename exceeds 42 characters.")
                            self.filename = filename
                        else:
                            self.filename = filename
                    
                    self.SetLabel(self.dir + self.filename)
            
            if self.getFocus() == self.getControl(BUTTON_BROWSE):
                dialog = xbmcgui.Dialog()
                fn = dialog.browse(self.type, 'Xbox Media Center', 'files', '', False, False)
                if fn:
                    if self.type == 3:
                        if fn[-1] != SEPARATOR:
                            fn = fn + SEPARATOR
                        
                        self.dir = fn
                    else:
                        pos = fn.rfind(SEPARATOR)  # find last '\' in the string
                        if pos != -1:
                            self.dir = fn[:pos + 1]
                            filename = fn[pos + 1:]
                            self.filename = filename
                    
                    self.SetLabel(self.dir + self.filename)
    
    def onFocus(self, controlId):
        pass
    
    def onClick(self, controlId):
        if controlId == BUTTON_CANCEL:
            self.onAction1(ACTION_PREVIOUS_MENU)
        else:
            self.onAction1(ACTION_SELECT_ITEM)
    
    def onControl(self, control):
        pass
    
    def SetFile(self, dir, filename, type, heading=""):
        self.dir = dir
        self.filename = filename
        self.type = type
        self.label = heading
    
    def SetLabel(self, filename):
        control = self.getControl(TEXT_PATH)
        # control.setLabel(filename[-60:])
        control.setText(filename)
