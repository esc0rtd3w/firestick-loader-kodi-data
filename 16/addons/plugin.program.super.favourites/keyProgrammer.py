#
#       Copyright (C) 2014
#       Sean Poyser (seanpoyser@gmail.com)
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
#  KeyListener class based on XBMC Keymap Editor by takoi


import xbmc
import xbmcgui
from threading import Timer

import utils

GETTEXT = utils.GETTEXT
ICON    = utils.ICON


ACTION_MOVE_LEFT          = 1
ACTION_MOVE_RIGHT         = 2
ACTION_MOVE_UP            = 3
ACTION_MOVE_DOWN          = 4
ACTION_SELECT_ITEM        = 7
ACTION_MOUSE_LEFT_CLICK   = 100
ACTION_MOUSE_DOUBLE_CLICK = 103
ACTION_MOUSE_MOVE         = 107

ACTION_PARENT_DIR         = 9
ACTION_PREVIOUS_MENU      = 10
ACTION_NAV_BACK           = 92

TIMEOUT = 10

class KeyListener(xbmcgui.WindowXMLDialog):

    def __new__(cls):
        try: 
            ret = super(KeyListener, cls).__new__(cls, 'DialogProgress.xml', '')
        except:
            ret   = super(KeyListener, cls).__new__(cls, 'DialogConfirm.xml', '')
        return ret 


    def __init__(self):
        self.key     = 0
        self.timeout = TIMEOUT
        self.setTimer()


    def close(self):
        self.timer.cancel()
        xbmcgui.WindowXML.close(self)


    def onInit(self):
        try:
            self.getControl(20).setVisible(False)
            self.getControl(10).setLabel(xbmc.getLocalizedString(222))
            self.setFocus(self.getControl(10))
            self.getControl(11).setVisible(False)
            self.getControl(12).setVisible(False)
        except:
            pass


        self.onUpdate()


    def onUpdate(self):
        text  = GETTEXT(30110) + '[CR]'
        text += GETTEXT(30109) % self.timeout
        self.getControl(9).setText(text)


    def onAction(self, action):
        actionId = action.getId()     

        if actionId in [ACTION_MOVE_LEFT, ACTION_MOVE_RIGHT, ACTION_MOVE_UP, ACTION_MOVE_DOWN, ACTION_SELECT_ITEM, ACTION_MOUSE_LEFT_CLICK, ACTION_MOUSE_DOUBLE_CLICK , ACTION_MOUSE_MOVE         ]:
            return

        if actionId in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_NAV_BACK]:
            return self.close()
       
        self.key = action.getButtonCode()
        self.close()


    def onClick(self, controlId):
        self.close()


    def onTimer(self):
        self.timeout -= 1
        if self.timeout < 0:
            return self.close()

        self.onUpdate()
        self.setTimer()


    def setTimer(self):
        self.timer = Timer(1, self.onTimer)
        self.timer.start()


def recordKey():
    dialog  = KeyListener()

    dialog.doModal()

    key = dialog.key

    del dialog
    return key


def main():
    if utils.isATV():
        utils.DialogOK(GETTEXT(30118), GETTEXT(30119))
        return False

    key = recordKey()
    if key < 1:
        utils.DialogOK(GETTEXT(30269))
        return

    start = 'key id="%d"' % key
    end   = 'key'

    if utils.WriteKeymap(start, end):
        utils.DialogOK(GETTEXT(30270))
        xbmc.executebuiltin('Action(reloadkeymaps)')  

    
if __name__ == '__main__':
    main()