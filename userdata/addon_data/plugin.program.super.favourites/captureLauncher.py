#
#       Copyright (C) 2014-
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

import xbmc
import os


def deleteFile(path):
    import xbmcvfs

    tries = 5
    while xbmcvfs.exists(path) and tries > 0:
        tries -= 1 
        try:    xbmcvfs.delete(path)
        except: xbmc.sleep(500)


def cleanup():
    try:
        #import inspect
        #script = inspect.getfile(inspect.currentframe())
        #deleteFile(script)

        KEYMAP_HOT  = 'super_favourites_hot.xml'
        KEYMAP_MENU = 'super_favourites_menu.xml'

        deleteFile(os.path.join('special://profile/keymaps', KEYMAP_HOT))
        deleteFile(os.path.join('special://profile/keymaps', KEYMAP_MENU))

        xbmc.sleep(1000)
        xbmc.executebuiltin('Action(reloadkeymaps)')  

    except:
        pass

    xbmc.executebuiltin('Action(ContextMenu)')
    

def main():
    try:
        import xbmc

        if xbmc.getCondVisibility('System.HasAddon(%s)' % 'plugin.program.super.favourites') == 1:        
            cmd = 'runscript(special://home/addons/plugin.program.super.favourites/capture.py)'
            xbmc.executebuiltin(cmd)

            return

    except Exception, e:        
        xbmc.log('Super Favourites : Error in captureLauncher.py')
        xbmc.log(str(e))

    cleanup()

main()