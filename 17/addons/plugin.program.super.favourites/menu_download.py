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


def download(silent=False):
    params = menuUtils.getCurrentParams()

    if params == None or ('file' not in params):
        if not silent:
            import utils
            utils.DialogOK(utils.GETTEXT(30261))
        return

    menuUtils.doDownload(params['file'])


try:
    download()
except Exception, e:
    import utils
    utils.log('Error in menu_download : %s' % str(e))