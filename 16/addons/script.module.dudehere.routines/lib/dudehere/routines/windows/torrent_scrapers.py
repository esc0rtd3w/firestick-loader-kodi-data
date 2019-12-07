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
import xbmcgui
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines.windows import BaseWindow
from dudehere.routines.constants import WINDOW_ACTIONS
from dudehere.routines.scrapers import ScraperPool
	
CONTROLS = enum(
			CLOSE=82000,
			LISTS=91050,
)
MOVIE_SCRAPERS = ['extratorrent', 'tpb', 'yts', 'torrentapi', 'torrentdownloads', 'zooqle']
TV_SCRAPERS = ['extratorrent','eztv', 'tpb', 'torrentapi', 'torrentdownloads', 'zooqle']

class TorrentScrapersWindow(BaseWindow):
	def __init__(self, *args, **kwargs):
			BaseWindow.__init__(self)
			state_file = vfs.join(DATA_PATH, 'scrapers.cache')
			try:
				self.order = plugin.load_data(state_file)
			except:
				self.order = []

	def onInit(self):
		
		items = []
		Scraper = ScraperPool(load='all')
		scrapers = Scraper.read_scraper_states()
		for scraper in scrapers: 
			try:
				if Scraper.get_scraper_by_name(scraper['name']).premiumize:
					icon = 'checked.png' if scraper['enabled'] else ''
		
					liz = xbmcgui.ListItem(scraper['name'], iconImage=icon)
					liz.setProperty("enabled", str(scraper['enabled']))
					icon = 'movie.png' if scraper['name'] in MOVIE_SCRAPERS else ''
					liz.setProperty("movie", icon)
					icon = 'tvshow.png' if scraper['name'] in TV_SCRAPERS else ''
					liz.setProperty("tv", icon)
					items.append(liz)
			except:
				pass
		def sort_scraper(scraper):
			try:
				index = self.order.index(scraper.getLabel())
			except:
				index = 0
			return index	
		items.sort(key=lambda k: sort_scraper(k))
		self.getControl(CONTROLS.LISTS).reset()
		self.getControl(CONTROLS.LISTS).addItems(items)
		#for i in xrange(self.getControl(CONTROLS.LISTS).size()):
		#	label = self.getControl(CONTROLS.LISTS).getListItem(i).getLabel()
		#	self.getControl(CONTROLS.LISTS).getListItem(i).setLabel("%s. %s" % (i+1, label))
		
	
	def onAction(self, action):
		action = action.getId()
		if action in [WINDOW_ACTIONS.ACTION_PREVIOUS_MENU, WINDOW_ACTIONS.ACTION_NAV_BACK]:
			self._close()
		
		try:
			if action == WINDOW_ACTIONS.ACTION_MOVE_LEFT:
				controlID = self.getFocus().getId()
				index = self.getControl(CONTROLS.LISTS).getSelectedPosition()
				if index == 0: return
				to = index - 1
				liz = self.getControl(CONTROLS.LISTS).getListItem(index)
				plugin.log("move_up")
				items = []
				for i in xrange(self.getControl(CONTROLS.LISTS).size()):
					service = self.getControl(CONTROLS.LISTS).getListItem(i).getLabel()
					items.append(service)
				items.insert(to, items.pop(index))
				self.order = items
				state_file = vfs.join(DATA_PATH, 'scrapers.cache')
				plugin.save_data(state_file, items)
				Scraper = ScraperPool(load='all')
				for scraper in items:
					weight = 1 + items.index(scraper)
					host = Scraper.get_scraper_by_name(scraper).name
					Scraper.change_host_weight(host, weight)
				
				self.onInit()
				self.getControl(CONTROLS.LISTS).selectItem(to)


			elif action == 	WINDOW_ACTIONS.ACTION_MOVE_RIGHT:
				controlID = self.getFocus().getId()
				index = self.getControl(CONTROLS.LISTS).getSelectedPosition()
				if index == self.getControl(CONTROLS.LISTS).size()-1: return
				liz = self.getControl(CONTROLS.LISTS).getListItem(index)
				to = index + 1
				plugin.log("move_down")
				items = []
				for i in xrange(self.getControl(CONTROLS.LISTS).size()):
					service = self.getControl(CONTROLS.LISTS).getListItem(i).getLabel()
					items.append(service)
				items.insert(to, items.pop(index))
				self.order = items
				state_file = vfs.join(DATA_PATH, 'scrapers.cache')
				plugin.save_data(state_file, items)
				Scraper = ScraperPool(load='all')
				for scraper in items:
					weight = 1 + items.index(scraper)
					host = Scraper.get_scraper_by_name(scraper).name
					Scraper.change_host_weight(host, weight)
	
				self.onInit()
				self.getControl(CONTROLS.LISTS).selectItem(to)	
				
		except:
			pass
	
	def onClick(self, controlID):
		if controlID==CONTROLS.LISTS:
			index = self.getControl(CONTROLS.LISTS).getSelectedPosition()
			liz = self.getControl(CONTROLS.LISTS).getSelectedItem()
			enabled = liz.getProperty("enabled")== "1"
			if enabled:
				self.getControl(CONTROLS.LISTS).getListItem(index).setIconImage('')
				self.getControl(CONTROLS.LISTS).getListItem(index).setProperty("enabled", "")
			else:
				self.getControl(CONTROLS.LISTS).getListItem(index).setIconImage('checked.png')
				self.getControl(CONTROLS.LISTS).getListItem(index).setProperty("enabled", "1")
			query = {'mode': 'toggle_scraper', "scraper": liz.getLabel()}
			plugin.execute_query(query)
		elif controlID==CONTROLS.CLOSE:
			self.close()	
