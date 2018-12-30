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
from dudehere.routines.scrapers import ScraperPool
	
CONTROLS = enum(
			CLOSE=82000,
			CLOSE2=82001,
			ENABLE=82002,
			DISABLE=82003,
			SCRAPERS=91050,
)

class ScraperListWindow(BaseWindow):
	def __init__(self, *args, **kwargs):
			BaseWindow.__init__(self)
	
	def onInit(self):
		Scraper = ScraperPool(load='all')
		scrapers = Scraper.read_scraper_states()
		items = []
		for scraper in scrapers: 
			try:
				broken = Scraper.get_scraper_by_name(scraper['name']).broken	
			except:
				broken = False if 'transmogrifier' in scraper['name'] else True
		
			try:
				premiumize = Scraper.get_scraper_by_name(scraper['name']).premiumize
			except:
				premiumize = False
			
			icon = 'checked.png' if scraper['enabled'] else ''
			name = "[COLOR red]%s[/COLOR]" % scraper['name'] if broken else  scraper['name']
			premiumize = 'premiumize.png' if premiumize else ''
			liz = xbmcgui.ListItem(name, iconImage=icon)
			liz.setProperty("scraper", scraper['name'])
			liz.setProperty("broken", str(broken))
			liz.setProperty("premiumize", premiumize)
			liz.setProperty("enabled", str(scraper['enabled']))
			
			items.append(liz)
				
		self.getControl(CONTROLS.SCRAPERS).addItems(items)
	
	def onClick(self, controlID):
		if controlID==CONTROLS.SCRAPERS:
			index = self.getControl(CONTROLS.SCRAPERS).getSelectedPosition()
			liz = self.getControl(CONTROLS.SCRAPERS).getSelectedItem()
			scraper = liz.getProperty("scraper")
			if liz.getProperty("enabled") == '1':
				self.getControl(CONTROLS.SCRAPERS).getSelectedItem().setProperty("enabled", "0")
				self.getControl(CONTROLS.SCRAPERS).getSelectedItem().setIconImage("")
			else:
				self.getControl(CONTROLS.SCRAPERS).getSelectedItem().setProperty("enabled", "1")
				self.getControl(CONTROLS.SCRAPERS).getSelectedItem().setIconImage("checked.png")
			query = {'mode': 'toggle_scraper', "name": scraper}
			plugin.execute_query(query)

		elif controlID in [CONTROLS.CLOSE, CONTROLS.CLOSE2]:
			self.close()
		elif controlID == CONTROLS.ENABLE:
			for index in xrange(self.getControl(CONTROLS.SCRAPERS).size()):
				liz = self.getControl(CONTROLS.SCRAPERS).getListItem(index)
				liz.setProperty("enabled", "1")
				liz.setIconImage("checked.png")
			query = {'mode': 'enable_all_scrapers', "name": "all"}
			plugin.execute_query(query)
				
		elif controlID == CONTROLS.DISABLE:
			for index in xrange(self.getControl(CONTROLS.SCRAPERS).size()):
				liz = self.getControl(CONTROLS.SCRAPERS).getListItem(index)
				liz.setProperty("enabled", "0")
				liz.setIconImage("")
				name = liz.getProperty("scraper")
			query = {'mode': 'disable_all_scrapers', "name": name}
			plugin.execute_query(query)
			