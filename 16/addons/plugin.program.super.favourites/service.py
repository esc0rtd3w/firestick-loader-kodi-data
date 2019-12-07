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


import utils
import xbmc
import xbmcgui
import os


utils.safeCall(utils.VerifyZipFiles)
utils.safeCall(utils.VerifyKeymaps)
utils.safeCall(utils.verifyPlugins)
utils.safeCall(utils.verifyLocation)


HOME = 10000


if utils.ADDON.getSetting('AUTOSTART') == 'true':
    utils.LaunchSF()


class MyMonitor(xbmc.Monitor):
    def __init__(self):
        xbmc.Monitor.__init__(self)
        self.hotkey  = utils.ADDON.getSetting('HOTKEY')
        self.context = utils.ADDON.getSetting('CONTEXT') == 'true'
       
        self.updateStdContextMenuItem()


    def onSettingsChanged(self):
        hotkey  = utils.ADDON.getSetting('HOTKEY')
        context = utils.ADDON.getSetting('CONTEXT') == 'true'
        
        self.updateStdContextMenuItem()

        utils.VerifyKeymaps()

        if self.hotkey == hotkey and self.context == context:
            return

        self.hotkey  = hotkey
        self.context = context

        utils.UpdateKeymaps()

    def updateStdContextMenuItem(self):
        self.std_context    = utils.ADDON.getSetting('CONTEXT_STD')       == 'true'
        self.std_addtofaves = utils.ADDON.getSetting('ADDTOFAVES_ON_STD') == 'true'
        self.std_download   = utils.ADDON.getSetting('DOWNLOAD_ON_STD')   == 'true'

        #print "*************************"
        #print "CONTEXT_STD       = %s" % self.std_context
        #print type(self.std_context)
        #print "ADDTOFAVES_ON_STD = %s" % self.std_addtofaves
        #print type(self.std_addtofaves)
        #print "DOWNLOAD_ON_STD   = %s" % self.std_download
        #print type(self.std_download)

        #useage in addon.xml : <visible>!IsEmpty(Window(Home).Property(SF_STD_CONTEXTMENU_ENABLED))</visible>

        #---------- SF on standard context menu ------------------------------------------------
        if self.std_context:
            xbmcgui.Window(HOME).setProperty('SF_STD_CONTEXTMENU_ENABLED', 'True')  
        else:
            xbmcgui.Window(HOME).clearProperty('SF_STD_CONTEXTMENU_ENABLED')


        #---------- Add to Faves on standard context menu --------------------------------------
        if self.std_addtofaves:
            xbmcgui.Window(HOME).setProperty('SF_STD_ADDTOFAVES_ENABLED', 'True')  
        else:
            xbmcgui.Window(HOME).clearProperty('SF_STD_ADDTOFAVES_ENABLED')


        #---------- Download on standard context menu ------------------------------------------
        if self.std_download:         
            xbmcgui.Window(HOME).setProperty('SF_STD_DOWNLOAD_ENABLED', 'True')  
        else:
            xbmcgui.Window(HOME).clearProperty('SF_STD_DOWNLOAD_ENABLED')


monitor = MyMonitor()

while (not xbmc.abortRequested):
    xbmc.sleep(1000)
 

del monitor