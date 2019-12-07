
#
#      Copyright (C) 2014 Sean Poyser
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


import xbmcaddon
import xbmcgui
import sfile
import os


ADDONID = 'plugin.video.supercartoons'
ADDON   = xbmcaddon.Addon(ADDONID)
PROFILE = ADDON.getAddonInfo('profile')
CACHE   = os.path.join(PROFILE, 'cache')



def deleteCache(silent=False):
    try:    sfile.rmtree(CACHE)
    except: pass
    
    if not silent:
        d = xbmcgui.Dialog()
        d.ok('Super Cartoons', '', 'Cache successfully cleared')


if __name__ == '__main__':
    deleteCache()
