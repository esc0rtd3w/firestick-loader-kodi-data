#!/usr/bin/python
# -*- coding: utf-8 -*-
PYTHONIOENCODING="UTF-8"

'''*
	Copyright (C) 2016 DudeHere

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

import re
import json
import xbmc
import xbmcgui
import xbmcaddon
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines.windows import BaseWindow
from dudehere.routines.constants import WINDOW_ACTIONS
from dudehere.routines.trakt import TraktAPI
trakt = TraktAPI()
CONTROLS = enum(
			CLOSE=82000,
			SET_LIST=82001,
			LISTS=91050,
			CONTEXT=84001,
			CONTEXT_WINDOW=84000
)

class SetListWindow(BaseWindow):
	def __init__(self, *args, **kwargs):
			BaseWindow.__init__(self)
	
	def onInit(self):
		lists = trakt.get_custom_lists()
		items = []
		default_list = plugin.get_setting('default_trakt_list')
		for li in lists:
			icon = 'checked.png' if li['ids']['slug'] == default_list else ''
			liz = xbmcgui.ListItem(li['name'], iconImage=icon)
			liz.setProperty("slug", li['ids']['slug'])
			items.append(liz)
		self.getControl(CONTROLS.LISTS).addItems(items)
	
	def onClick(self, controlID):
		if controlID==CONTROLS.LISTS:
			index = self.getControl(CONTROLS.LISTS).getSelectedPosition()
			liz = self.getControl(CONTROLS.LISTS).getSelectedItem()
			for i in xrange(self.getControl(CONTROLS.LISTS).size()):
				self.getControl(CONTROLS.LISTS).getListItem(i).setIconImage('')
			self.getControl(CONTROLS.LISTS).getListItem(index).setIconImage('checked.png')
			plugin.set_setting('default_trakt_list', liz.getProperty("slug"))
		elif controlID == CONTROLS.CLOSE:
			self.close()	