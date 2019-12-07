# -*- coding: utf-8 -*-
#
# USTVnow Guide
# Developed by mhancoc7
# Forked from FTV Guide:
# Copyright (C) 2015 Thomas Geppert [bluezed]
# bluezed.apps@gmail.com
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmc
import xbmcaddon
import xbmcvfs
import os
import urllib2
import datetime
import zlib
import base64
if xbmc.getCondVisibility('System.HasAddon(plugin.video.ustvnow.tva)'):
    ustvnow_type = xbmcaddon.Addon('plugin.video.ustvnow.tva')

if xbmc.getCondVisibility('System.HasAddon(plugin.video.ustvnow.tva)'):
    if ustvnow_type.getSetting('free_package') == 'true':
        if ustvnow_type.getSetting('secure') == 'true':
            MAIN_URL = base64.b64decode('aHR0cHM6Ly9taGFuY29jNy5zb3VyY2Vjb2RlLmFnL3VzdHZub3cvZnJlZS8=')
        else:
            MAIN_URL = base64.b64decode('aHR0cDovL21oYW5jb2M3LnNvdXJjZWNvZGUuYWcvdXN0dm5vdy9mcmVlLw==')
    else:
        if ustvnow_type.getSetting('secure') == 'true':
            MAIN_URL = base64.b64decode('aHR0cHM6Ly9taGFuY29jNy5zb3VyY2Vjb2RlLmFnL3VzdHZub3cvcHJlbWl1bS8=')
        else:
            MAIN_URL = base64.b64decode('aHR0cDovL21oYW5jb2M3LnNvdXJjZWNvZGUuYWcvdXN0dm5vdy9wcmVtaXVtLw==')
else:
    if ustvnow_type.getSetting('secure') == 'true':
        MAIN_URL = base64.b64decode('aHR0cHM6Ly9taGFuY29jNy5zb3VyY2Vjb2RlLmFnL3VzdHZub3cvZnJlZS8=')
    else:
        MAIN_URL = base64.b64decode('aHR0cDovL21oYW5jb2M3LnNvdXJjZWNvZGUuYWcvdXN0dm5vdy9mcmVlLw==')

class FileFetcher(object):
    INTERVAL_ALWAYS = 0
    INTERVAL_12 = 1
    INTERVAL_24 = 2
    INTERVAL_48 = 3

    FETCH_ERROR = -1
    FETCH_NOT_NEEDED = 0
    FETCH_OK = 1

    TYPE_DEFAULT = 1
    TYPE_REMOTE = 2

    basePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ustvnow.plus.guide'))
    filePath = ''
    fileUrl = ''
    addon = None
    fileType = TYPE_DEFAULT

    def __init__(self, fileName, addon):
        self.addon = addon

        if fileName.startswith("http://") or fileName.startswith("sftp://") or fileName.startswith("ftp://") or \
                fileName.startswith("https://") or fileName.startswith("ftps://") or fileName.startswith("smb://") or \
                fileName.startswith("nfs://"):
            self.fileType = self.TYPE_REMOTE
            self.fileUrl = fileName
            self.filePath = os.path.join(self.basePath, fileName.split('/')[-1])
        else:
            self.fileType = self.TYPE_DEFAULT
            self.fileUrl = MAIN_URL + fileName
            self.filePath = os.path.join(self.basePath, fileName)

        # make sure the folder is actually there already!
        if not os.path.exists(self.basePath):
            os.makedirs(self.basePath)

    def fetchFile(self):
        retVal = self.FETCH_NOT_NEEDED
        fetch = False
        if not os.path.exists(self.filePath):  # always fetch if file doesn't exist!
            fetch = True
        else:
            interval = int(self.addon.getSetting('xmltv.interval'))
            if interval != self.INTERVAL_ALWAYS:
                modTime = datetime.datetime.fromtimestamp(os.path.getmtime(self.filePath))
                td = datetime.datetime.now() - modTime
                # need to do it this way cause Android doesn't support .total_seconds() :(
                diff = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6
                if ((interval == self.INTERVAL_12 and diff >= 43200) or
                        (interval == self.INTERVAL_24 and diff >= 43200) or
                        (interval == self.INTERVAL_48 and diff >= 43200)):
                    fetch = True
            else:
                fetch = True

        if fetch:
            tmpFile = os.path.join(self.basePath, 'tmp')
            if self.fileType == self.TYPE_REMOTE:
                xbmc.log('[script.ustvnow.plus.guide] file is in remote location: %s' % self.fileUrl, xbmc.LOGDEBUG)
                if not xbmcvfs.copy(self.fileUrl, tmpFile):
                    xbmc.log('[script.ustvnow.plus.guide] Remote file couldn\'t be copied: %s' % self.fileUrl, xbmc.LOGERROR)
            else:
                f = open(tmpFile, 'wb')
                xbmc.log('[script.ustvnow.plus.guide] file is on the internet: %s' % self.fileUrl, xbmc.LOGDEBUG)
                tmpData = urllib2.urlopen(self.fileUrl)
                data = tmpData.read()
                if tmpData.info().get('content-encoding') == 'gzip':
                    data = zlib.decompress(data, zlib.MAX_WBITS + 16)
                f.write(data)
                f.close()
            if os.path.getsize(tmpFile) > 256:
                if os.path.exists(self.filePath):
                    os.remove(self.filePath)
                os.rename(tmpFile, self.filePath)
                retVal = self.FETCH_OK
                xbmc.log('[script.ustvnow.plus.guide] file %s was downloaded' % self.filePath, xbmc.LOGDEBUG)
            else:
                retVal = self.FETCH_ERROR
        return retVal
