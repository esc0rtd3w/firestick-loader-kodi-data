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

import utils
import favourite
import parameters
import cache

FOLDERCFG = utils.FOLDERCFG
GETTEXT   = utils.GETTEXT

def add(path, name):
    title    = GETTEXT(30079)
    password = utils.GetText(title, text='', hidden=True)

    if not password:
        return False

    md5 = utils.generateMD5(password)

    cfg  = os.path.join(path, FOLDERCFG)
    parameters.setParam('LOCK', md5, cfg)

    return True


def remove(path,name):
    title    = GETTEXT(30078)
    password = utils.GetText(title, text='', hidden=True)

    if not password:
        return False

    md5 = utils.generateMD5(password)

    cfg  = os.path.join(path, FOLDERCFG)
    lock = parameters.getParam('LOCK', cfg)

    if lock != md5:
        utils.DialogOK(GETTEXT(30080))
        return False

    parameters.clearParam('LOCK', cfg)
    utils.DialogOK(GETTEXT(30081))

    return True


def unlocked(path, lock=None):
    if not lock:
        folderConfig = os.path.join(path, FOLDERCFG)
        lock = parameters.getParam('LOCK', folderConfig)

    if not lock:
        return True

    if cache.exists(path):
        return True

    return False


def unlock(path):
    folderConfig = os.path.join(path, FOLDERCFG)
    lock = parameters.getParam('LOCK', folderConfig)

    if unlocked(path, lock):
        return True
    
    md5 = checkPassword(path, lock)

    if len(md5) == 0:
        return False

    if md5 == 'ERROR':
        utils.DialogOK(GETTEXT(30080))
        return False

    periods = [0, 1, 5, 15]
    setting = int(utils.ADDON.getSetting('CACHE'))
    period  = periods[setting]

    cache.add(path, period)

    return True


def checkPassword(path, lock=None):
    if not lock:
        folderConfig = os.path.join(path, FOLDERCFG)
        lock = parameters.getParam('LOCK', folderConfig)

    title = GETTEXT(30069)
    
    unlock = utils.GetText(title, hidden=True)

    if not unlock:
        return ''

    md5   = utils.generateMD5(unlock)
    match = md5 == lock

    if not match:
        return 'ERROR'

    return md5
