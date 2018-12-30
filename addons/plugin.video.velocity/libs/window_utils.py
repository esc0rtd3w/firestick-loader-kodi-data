"""
    Velocity XBMC Addon
    Copyright (C) 2016 blazetamer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmcgui,xbmc,sys
import time
import os
import kodi
import random
import json
from libs import log_utils
from libs import trakt
addon_id=kodi.addon_id

ICON_PATH = os.path.join(kodi.get_path(), 'icon.png')


def get_pin():
    AUTH_BUTTON = 200
    LATER_BUTTON = 201
    NEVER_BUTTON = 202
    ACTION_PREVIOUS_MENU = 10
    ACTION_BACK = 92
    CENTER_Y = 6
    CENTER_X = 2
    
    class PinAuthDialog(xbmcgui.WindowXMLDialog):
        auth = False
        
        def onInit(self):
            self.pin_edit_control = self.__add_editcontrol(30, 240, 40, 550)
            self.setFocus(self.pin_edit_control)
            auth = self.getControl(AUTH_BUTTON)
            never = self.getControl(NEVER_BUTTON)
            self.pin_edit_control.controlUp(never)
            self.pin_edit_control.controlLeft(never)
            self.pin_edit_control.controlDown(auth)
            self.pin_edit_control.controlRight(auth)
            auth.controlUp(self.pin_edit_control)
            auth.controlLeft(self.pin_edit_control)
            never.controlDown(self.pin_edit_control)
            never.controlRight(self.pin_edit_control)
            
        def onAction(self, action):
            # print 'Action: %s' % (action.getId())
            if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
                self.close()

        def onControl(self, control):
            # print 'onControl: %s' % (control)
            pass

        def onFocus(self, control):
            # print 'onFocus: %s' % (control)
            pass

        def onClick(self, control):
            # print 'onClick: %s' % (control)
            if control == AUTH_BUTTON:
                print "PIN INPUT"
                if not self.__get_token():
                    kodi.notify(header='Not Authorized',msg='Using Standard Menus',duration=5000,sound=None)
                #self.auth = True

            if control == NEVER_BUTTON:

                kodi.notify(header='Not Authorized',msg='Using Standard Menus',duration=5000,sound=None)



            if control in [AUTH_BUTTON, LATER_BUTTON, NEVER_BUTTON]:
                self.close()
        
        def __get_token(self):
            pin = self.pin_edit_control.getText().strip()
            if pin:
                try:
                    trakt_api=trakt.TraktAPI()
                    trakt_api.authorize(pin=pin)
                    return True
                except Exception as e:
                    log_utils.log('Trakt Authorization Failed: %s' % (e), log_utils.LOGDEBUG)
                    return False
            return False
        
        # have to add edit controls programatically because getControl() (hard) crashes XBMC on them
        def __add_editcontrol(self, x, y, height, width):
            media_path = os.path.join(kodi.get_path(), 'resources', 'skins', 'Default', 'media')
            temp = xbmcgui.ControlEdit(5, 5, 5, 5, '', font='font12', textColor='0xFFFFFFFF', focusTexture=os.path.join(media_path, 'button-focus2.png'),
                                       noFocusTexture=os.path.join(media_path, 'button-nofocus.png'), _alignment=CENTER_Y | CENTER_X)
            temp.setPosition(x, y)
            temp.setHeight(height)
            temp.setWidth(width)
            self.addControl(temp)
            return temp
        
    dialog = PinAuthDialog('TraktPinAuthDialog.xml', kodi.get_path())
    dialog.doModal()
    del dialog

class ProgressDialog(object):
    def __init__(self, heading, line1='', line2='', line3='', active=True):
        if active:
            self.pd = xbmcgui.DialogProgress()
            self.pd.create(heading, line1, line2, line3)
            self.pd.update(0)
        else:
            self.pd = None

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        if self.pd is not None:
            self.pd.close()
            del self.pd
    
    def is_canceled(self):
        if self.pd is not None:
            return self.pd.iscanceled()
        else:
            return False
        
    def update(self, percent, line1='', line2='', line3=''):
        if self.pd is not None:
            self.pd.update(percent, line1, line2, line3)










