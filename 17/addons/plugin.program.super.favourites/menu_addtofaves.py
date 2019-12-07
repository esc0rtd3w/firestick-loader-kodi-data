#
#       Copyright (C) 2016-
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

import menuUtils


def add(silent=False):
    params = menuUtils.getCurrentParams()
    meta   = menuUtils.getCurrentMeta()

    import utils
    utils.outputDict(params, 'menu_addtofaves - params')
    utils.outputDict(meta,   'menu_addtofaves - meta')

    if params == None:
        if not silent:
            import utils
            utils.DialogOK(utils.GETTEXT(30260))
        return

    menuUtils.addToFaves(params, meta)

try:
    add()     
except Exception, e:
    import utils
    utils.log('Error in menu_addtofaves : %s' % str(e))