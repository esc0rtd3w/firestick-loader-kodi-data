# -*- coding: utf-8 -*-
#
# FTV Guide
# Copyright (C) 2015 Thomas Geppert [bluezed]
# bluezed.apps@gmail.com
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
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmc
import xbmcgui
import xbmcaddon
import os
import json
import ConfigParser
import xml.etree.ElementTree as ET

from fileFetcher import *
from strings import *
from operator import itemgetter

ADDON = xbmcaddon.Addon(id='script.ftvguide')


class GuideTypes(object):
    GUIDE_ID = 0
    GUIDE_SORT = 1
    GUIDE_NAME = 2
    GUIDE_FILE = 3
    GUIDE_DEFAULT = 4

    CUSTOM_FILE_ID = 6

    guideTypes = []
    guideParser = ConfigParser.ConfigParser()
    filePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ftvguide', 'guides.ini'))

    def __init__(self):
        guideTypes = []
        defaultGuideId = 0  # fallback to the first guide in case no default is actually set in the ini file
        try:
            fetcher = FileFetcher('guides.ini', ADDON)
            if fetcher.fetchFile() < 0:
                xbmcgui.Dialog().ok(strings(FETCH_ERROR_TITLE), strings(FETCH_ERROR_LINE1), strings(FETCH_ERROR_LINE2))

            self.guideParser.read(self.filePath)

            for section in self.guideParser.sections():
                sectMap = self.SectionMap(section)
                id = int(sectMap['id'])
                fName = sectMap['file']
                sortOrder = int(sectMap['sort_order'])
                default = False
                if 'default' in sectMap and sectMap['default'] == 'true':
                    default = True
                    defaultGuideId = id
                guideTypes.append((id, sortOrder, section, fName, default))
            self.guideTypes = sorted(guideTypes, key=itemgetter(self.GUIDE_SORT))
            xbmc.log('[script.ftvguide] GuideTypes collected: %s' % str(self.guideTypes), xbmc.LOGDEBUG)

        except:
            xbmc.log('[script.ftvguide] unable to parse guides.ini', xbmc.LOGWARNING)

        if len(guideTypes) == 0:
            self.guideTypes.append((self.CUSTOM_FILE_ID, 9000, "Custom File", "CUSTOM", True))
            defaultGuideId = self.CUSTOM_FILE_ID

        if str(ADDON.getSetting('xmltv.type')) == '':
            ADDON.setSetting('xmltv.type', str(defaultGuideId))

    def SectionMap(self, section):
        dict1 = {}
        options = self.guideParser.options(section)
        for option in options:
            try:
                dict1[option] = self.guideParser.get(section, option)
                if dict1[option] == -1:
                    xbmc.log('[script.ftvguide] skip: %s' % option, xbmc.LOGDEBUG)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1


    def getGuideDataItem(self, id, item):
        value = None
        guide = self.getGuideById(id)
        try:
            value = guide[item]
        except IndexError:
            xbmc.log('[script.ftvguide] DataItem with index %s not found' % item, xbmc.LOGDEBUG)
        return value


    def getGuideById(self, id):
        xbmc.log('[script.ftvguide] Finding Guide with ID: %s' % id, xbmc.LOGDEBUG)
        ret = []
        for guide in self.guideTypes:
            if guide[self.GUIDE_ID] == int(id):
                ret = guide
                xbmc.log('[script.ftvguide] Found Guide with data: %s' % str(guide), xbmc.LOGDEBUG)
        return ret


def getKodiVersion():
    # retrieve current installed version
    jsonQuery = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["version", "name"]}, "id": 1 }')
    jsonQuery = unicode(jsonQuery, 'utf-8', errors='ignore')
    jsonQuery = json.loads(jsonQuery)
    version = []
    if jsonQuery.has_key('result') and jsonQuery['result'].has_key('version'):
        version = jsonQuery['result']['version']
    return version['major']


if __name__ == '__main__':
    guideList = []
    gTypes = GuideTypes()
    for gType in gTypes.guideTypes:
        guideList.append(gType[gTypes.GUIDE_NAME])
    d = xbmcgui.Dialog()
    ret = d.select('Select what type of guide you want to use', guideList)
    if ret >= 0:
        guideId = gTypes.guideTypes[ret][gTypes.GUIDE_ID]
        typeId = str(guideId)
        typeName = gTypes.getGuideDataItem(guideId, gTypes.GUIDE_NAME)
        ver = getKodiVersion()
        if xbmc.getCondVisibility('system.platform.android') and int(ver) < 15:
            # This workaround is needed due to a Bug in the Kodi Android implementation
            # where setSetting() does not have any effect:
            #  #13913 - [android/python] addons can not save settings  [http://trac.kodi.tv/ticket/13913]
            xbmc.log('[script.ftvguide] Running on ANDROID with Kodi v%s --> using workaround!' % str(ver), xbmc.LOGDEBUG)
            filePath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.ftvguide', 'settings.xml'))
            tree = ET.parse(filePath)
            root = tree.getroot()
            updated = False
            for item in root.findall('setting'):
                if item.attrib['id'] == 'xmltv.type':
                    item.attrib['value'] = typeId
                    updated = True
                elif item.attrib['id'] == 'xmltv.type_select':
                    item.attrib['value'] = typeName
                    updated = True
            if updated:
                tree.write(filePath)
                ADDON.openSettings()
        else:  # standard settings handling...
            ADDON.setSetting('xmltv.type', typeId)
            ADDON.setSetting('xmltv.type_select', typeName)
