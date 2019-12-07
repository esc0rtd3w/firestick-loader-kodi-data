#!/usr/bin/python
# -*- coding: utf-8 -*-
PYTHONIOENCODING="UTF-8"

'''*
	Copyright (C) 2015 DudeHere

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.

*'''

import os
import sys
import xbmc
import xbmcaddon
from dudehere.routines.vfs import VFSClass
addon = xbmcaddon.Addon()
vfs = VFSClass()
def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	forward = dict((key, value) for key, value in enums.iteritems())
	reverse = dict((value, key) for key, value in enums.iteritems())
	enums['f_map'] = forward
	enums['r_map'] = reverse
	return type('Enum', (), enums)

def has_item(obj, key):
	if key in obj: return True
	for k, v in obj.items():
		if isinstance(v,dict):
			item = has_item(v, key)
			if item is not None:
				return True
	return False

def utf8(string):
	try: 
		string = u'' + string
	except UnicodeEncodeError:
		string = u'' + string.encode('utf-8')
	except UnicodeDecodeError:
		string = u'' + string.decode('utf-8')
	return string
PLATFORM = sys.platform
try:
	HANDLE_ID = int(sys.argv[1])
	ADDON_URL = sys.argv[0]
	PLUGIN_URL = sys.argv[0] + sys.argv[2]
except:
	HANDLE_ID = -1
	ADDON_URL = 'plugin://%s' % addon.getAddonInfo('name')
	PLUGIN_URL = 'plugin://%s' % addon.getAddonInfo('name')




ADDON_ID = addon.getAddonInfo('id')
ADDON_NAME =  addon.getAddonInfo('name')
VERSION = addon.getAddonInfo('version')
ROOT_PATH = addon.getAddonInfo('path').decode('utf-8')
DATA_PATH = addon.getAddonInfo('profile').decode('utf-8')
ARTWORK = ROOT_PATH + '/resources/artwork/'
SHARED_ARTWORK = vfs.join("special://home", "addons/script.module.dudehere.routines/resources/artwork/") 

ALLOWED_CALLERS = ['plugin.video.theroyalwe', 'plugin.video.ugottoo', 'plugin.video.redbeard', 'service.walter.sobchak']

try:
	KODI_LANGUAGE = xbmc.getLanguage().capitalize()
except:
	KODI_LANGUAGE = 'English'
LANGUAGE_PATH = VFSClass().join(ROOT_PATH, 'resources/language/' + KODI_LANGUAGE)

def i18n(id):
	return addon.getLocalizedString(id).encode('utf-8', 'ignore')
QUALITY = enum(LOCAL=9, HD1080=8, HD720=7, HD=6, HIGH=5, SD480=4, UNKNOWN=3, LOW=2, POOR=1)
LOG_LEVEL = enum(STANDARD=0, VERBOSE=1)
VIEWS = enum(DEFAULT=500, LIST=50, BIGLIST=51, THUMBNAIL=500, SMALLTHUMBNAIL=522, FANART=508, POSTERWRAP=501, MEDIAINFO=504, MEDIAINFO2=503, MEDIAINFO3=515, WIDE=505, LIST_DEFAULT=50, TV_DEFAULT=50, MOVIE_DEFAULT=50, SEASON_DEFAULT=50, EPISODE_DEFAULT=50)
DB_VERSION = 15

WINDOWXML = enum(
	ALIGN_LEFT = 0,
	ALIGN_RIGHT = 1,
	ALIGN_CENTER_X = 2,
	ALIGN_CENTER_Y = 4,
	ALIGN_CENTER = 6,
	ALIGN_TRUNCATED = 8,
	ALIGN_JUSTIFY = 10,
	MESSAGE_ACTION_OK = 110,
	MESSAGE_EXIT = 111
)

WINDOW_ACTIONS = enum(
	ACTION_PREVIOUS_MENU = 10,
	ACTION_NAV_BACK = 92,
	ACTION_MOVE_LEFT = 1,
	ACTION_MOVE_RIGHT = 2,
	ACTION_MOVE_UP = 3,
	ACTION_MOVE_DOWN = 4,
	ACTION_MOUSE_WHEEL_UP = 104,
	ACTION_MOUSE_WHEEL_DOWN = 105,
	ACTION_MOUSE_DRAG = 106,
	ACTION_MOUSE_MOVE = 107,
	ACTION_MOUSE_LEFT_CLICK = 100,
	ACTION_ENTER = 13,
	ACTION_SELECT_ITEM = 7,
	ACTION_SPACE = 12,
	ACTION_MOUSE_RIGHT_CLICK = 101,
	ACTION_SHOW_INFO = 11,
	ACTION_CONTEXT_MENU = 117,
)