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
import xbmcgui
import os

import utils
import sfile


ADDON     = utils.ADDON
ADDONID   = utils.ADDONID
GETTEXT   = utils.GETTEXT


SEPARATOR = '%SF%'

WHITELIST = ADDON.getSetting('WHITELIST')

 
def main(toAdd):
    if toAdd:
        doAdd()
        utils.openSettings(ADDONID, 2.7)
    else:
        doRemove()
        utils.openSettings(ADDONID, 2.8)


def doAdd():
    root, folders, files = utils.GetAddons()

    list = []

    for folder in folders:
        file = os.path.join(root, folder, 'addon.xml')
        if sfile.exists(file):
            if not folder in WHITELIST:
                list.append(folder)   

    option = xbmcgui.Dialog().select(GETTEXT(35041), list)
    if option < 0:
        return

    folder = list[option]
    
    whitelist = WHITELIST + SEPARATOR + folder

    ADDON.setSetting('WHITELIST', tidy(whitelist))


def doRemove():
    list = tidy(WHITELIST).split(SEPARATOR)

    if len(list) == 1 and len(list[0]) == 0:
        return

    option = xbmcgui.Dialog().select(GETTEXT(35042), list)
    if option < 0:
        return

    folder = list[option]

    whitelist = WHITELIST.replace(folder, '')

    ADDON.setSetting('WHITELIST', tidy(whitelist))


def tidy(text):
    DOUBLE = SEPARATOR + SEPARATOR
    while DOUBLE in text:
        text = text.replace(DOUBLE, SEPARATOR)

    if text.startswith(SEPARATOR):
        text = text.split(SEPARATOR, 1)[-1]

    if text.endswith(SEPARATOR):
        text = text.rsplit(SEPARATOR, 1)[0]

    return text

    
if __name__ == '__main__':
    try:
        toAdd = True

        if len(sys.argv) > 1:
            toAdd = sys.argv[1].lower() != 'false'

        main(toAdd)

    except:
        pass