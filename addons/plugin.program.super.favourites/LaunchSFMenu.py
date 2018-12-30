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
  

def main():
    try:
        import xbmc

        if xbmc.getCondVisibility('System.HasAddon(%s)' % 'plugin.program.super.favourites') == 1:        
            cmd = 'runscript(special://home/addons/plugin.program.super.favourites/capture.py,LaunchSFMenu)'
            xbmc.executebuiltin(cmd)

    except Exception, e:        
        xbmc.log('Super Favourites : Error in LaunchSFMenu.py')
        xbmc.log(str(e))

main()