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

import xbmcgui

import os
import urllib

import utils
import favourite
import parameters


FILENAME  = utils.FILENAME
FOLDERCFG = utils.FOLDERCFG
PROFILE   = utils.PROFILE
GETTEXT   = utils.GETTEXT


def reset():
    xbmcgui.Window(10000).clearProperty('SF_FILE')
    xbmcgui.Window(10000).clearProperty('SF_FOLDER')
    xbmcgui.Window(10000).clearProperty('SF_CMD')
    xbmcgui.Window(10000).clearProperty('SF_LABEL')
    xbmcgui.Window(10000).clearProperty('SF_TYPE')
    xbmcgui.Window(10000).clearProperty('SF_THUMB')
    xbmcgui.Window(10000).clearProperty('SF_FANART')
    xbmcgui.Window(10000).clearProperty('SF_DESCRIPTION')
    xbmcgui.Window(10000).clearProperty('SF_META')


def cutCopy(file, cmd, cut=True):
    reset()
    xbmcgui.Window(10000).setProperty('SF_FILE',   file)
    xbmcgui.Window(10000).setProperty('SF_FOLDER', file.rsplit(os.sep, 1)[0])
    xbmcgui.Window(10000).setProperty('SF_CMD',    cmd)
    xbmcgui.Window(10000).setProperty('SF_TYPE',  'cut' if cut else 'copy')

    fave, index, nFaves = favourite.findFave(file, cmd)

    if index < 0:
        return

    thumb  = fave[1]
    fanart = favourite.getFanart(fave[2])
    desc   = favourite.getOption(fave[2], 'desc')
    meta   = favourite.getOption(fave[2], 'meta')
    meta   = utils.convertURLToDict(meta)

    _setPasteProperties(thumb, fanart, desc, meta=meta)

    return True


def cutCopyFolder(folder, cut=True):
    reset()
    xbmcgui.Window(10000).setProperty(  'SF_FILE',   folder)
    xbmcgui.Window(10000).setProperty(  'SF_FOLDER', folder.rsplit(os.sep, 1)[0])
    xbmcgui.Window(10000).clearProperty('SF_CMD')
    xbmcgui.Window(10000).setProperty(  'SF_TYPE',  'cutfolder' if cut else 'copyfolder')

    file = os.path.join(folder, FOLDERCFG)
    cfg  = parameters.getParams(file)

    thumb  = parameters.getParam('ICON',   cfg)
    fanart = parameters.getParam('FANART', cfg)
    desc   = parameters.getParam('DESC',   cfg)

    _setPasteProperties(thumb, fanart, desc)

    return True


def setPasteProperties(thumb='', fanart='', desc='', label=None, cmd=None, meta=None):
    reset()
    _setPasteProperties(thumb, fanart, desc, label, cmd, meta)


def getThumb():
    return xbmcgui.Window(10000).getProperty('SF_THUMB')


def getFanart():
    return xbmcgui.Window(10000).getProperty('SF_FANART')


def getDesc():
    return  urllib.unquote(xbmcgui.Window(10000).getProperty('SF_DESCRIPTION'))


def getMeta():
    return xbmcgui.Window(10000).getProperty('SF_META')


def _setPasteProperties(thumb='', fanart='', desc='', label=None, cmd=None, meta=None):
    if not thumb:  thumb  = ''
    if not fanart: fanart = ''
    if not desc:   desc   = ''
    if not cmd:    cmd    = ''
    if not label:  label  = ''
    if not meta:   meta   = ''

    xbmcgui.Window(10000).setProperty('SF_THUMB',       thumb)
    xbmcgui.Window(10000).setProperty('SF_FANART',      fanart)
    xbmcgui.Window(10000).setProperty('SF_DESCRIPTION', urllib.quote(desc))
    xbmcgui.Window(10000).setProperty('SF_LABEL',       label)
    xbmcgui.Window(10000).setProperty('SF_META',        utils.convertDictToURL(meta))

    if len(xbmcgui.Window(10000).getProperty('SF_TYPE')) > 0:
        return

    xbmcgui.Window(10000).setProperty('SF_TYPE', 'capture')
    xbmcgui.Window(10000).setProperty('SF_CMD',  cmd)


def paste(folder):
    if len(folder) < 1:
        return False

    file = xbmcgui.Window(10000).getProperty('SF_FILE')
    cmd  = xbmcgui.Window(10000).getProperty('SF_CMD')
    type = xbmcgui.Window(10000).getProperty('SF_TYPE').lower()

    dst = os.path.join(folder, FILENAME)

    if type == 'cut':
        return pasteCut(file, cmd, folder)
    elif type == 'copy':
        return pasteCopy(file, cmd, folder)
    elif type == 'capture':
        return pasteCapture(cmd, folder)

    return False


def pasteCapture(cmd, folder):
    thumb = xbmcgui.Window(10000).getProperty('SF_THUMB')
    name  = xbmcgui.Window(10000).getProperty('SF_LABEL')

    file = os.path.join(folder, FILENAME)

    copy = [name, thumb, cmd]
    return favourite.addFave(file, copy)


def pasteFolder(dst, addonid):
    if len(dst) == 0:
        return False

    src = xbmcgui.Window(10000).getProperty('SF_FILE')
    cut = xbmcgui.Window(10000).getProperty('SF_TYPE').lower() == 'cutfolder'

    root       = src.rsplit(os.sep, 1)[0]
    folderName = src.rsplit(os.sep, 1)[-1]

    same = (root == dst)

    link = True

    if dst == 'special://profile': #i.e. Kodi favourites
        if cut:
            cut   = False
            line1 = GETTEXT(30187) % DISPLAYNAME
            line2 = GETTEXT(30188) % folderName
            line3 = GETTEXT(30189)
            link  = utils.DialogYesNo(line1, line2, line3, noLabel=GETTEXT(30190), yesLabel=GETTEXT(30186))
            if not link:
                return
    else:
        if cut:
            link = False
        else:  
            line1 = GETTEXT(30183) % folderName
            link  = True if same else utils.DialogYesNo(line1, GETTEXT(30184), noLabel=GETTEXT(30185), yesLabel=GETTEXT(30186))

    if link:
        success = pasteFolderLink(src, dst, folderName, addonid)
    else:
        success = pasteFolderCopy(src, dst, folderName)

    if not success:
        line1 = GETTEXT(30191) % folderName
        utils.DialogOK(line1)
        return False

    if cut:
        import sfile
        sfile.rmtree(src)

    return success


def pasteFolderLink(src, dst, folderName, addonid):
    import urllib
    thumbnail, fanart = utils.getFolderThumb(src)

    folderConfig = os.path.join(src, FOLDERCFG)
    colour       = parameters.getParam('COLOUR', folderConfig)

    if colour:
        folderName = '[COLOR %s]%s[/COLOR]' % (colour, folderName)

    path = utils.convertToHome(src)
    path = path.replace(PROFILE, '')
    path = path.replace('\\', '/')
    if path.startswith('/'):
        path = path[1:]

    cmd = '%s?label=%s&mode=%d&folder=%s' % (addonid, folderName, utils._FOLDER, urllib.quote_plus(path))
    cmd = '"%s"' % cmd  
    cmd = cmd.replace('+', '%20')
    cmd = 'ActivateWindow(%d,%s)' % (utils.getCurrentWindowId(), cmd) 
    cmd = favourite.addFanart(cmd, fanart)

    file = os.path.join(dst, FILENAME)

    if favourite.findFave(file, cmd)[0]:
        return True

    faves = favourite.getFavourites(file, validate=False)
    fave  = [folderName, thumbnail, cmd]

    faves.append(fave)

    favourite.writeFavourites(file, faves)

    return True


def pasteFolderCopy(src, _dst, folderName):
    import sfile

    dst = os.path.join(_dst, folderName)

    index = 0
    while sfile.exists(dst):
        index += 1
        dst    = os.path.join(_dst, GETTEXT(30192) % (folderName, index))

    try:
        sfile.copytree(src, dst)
    except Exception, e: 
        utils.log('Error in pasteFolderCopy: %s' % str(e))
        return False

    return True


def pasteCopy(file, cmd, folder):
    copy, index, nFaves = favourite.findFave(file, cmd)
    if not copy:
        return False

    file = os.path.join(folder, FILENAME)

    return favourite.copyFave(file, copy)


def pasteCut(file, cmd, folder):
    if not pasteCopy(file, cmd, folder):
        return False

    return favourite.removeFave(file, cmd)