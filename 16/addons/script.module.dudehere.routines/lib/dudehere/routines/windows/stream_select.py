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
import xbmc
import xbmcgui
from dudehere.routines import *
from dudehere.routines.windows import BaseWindow
from dudehere.routines.scrapers import ScraperPool
from dudehere.routines.scrapers import DB

CONTROLS = enum(
	CLOSE=82000,
	LISTS=91050,
)
table = {9: "local.png", 8: '1080.png', 7:"720.png", 6: "hd.png", 5: "hd.png", 4:"480.png", 3:"unknown.png", 2:"low.png", 1:"low.png"}
def format_size(size):
	if size == 0 or size is None: return False
	size = int(size) / (1024 * 1024)
	if size > 2000:
		size = size / 1024
		unit = 'GB'
	else :
		unit = 'MB'
	size = "%s %s" % (size, unit)
	return size

def test_url(encoded_url):	
	skin_path = plugin.get_addon('script.module.dudehere.routines').getAddonInfo('path')
	test = StreamTest("test_url.xml", skin_path)
	test.encoded_url = encoded_url
	test.doModal()
	test = test.return_val
	return test

class StreamTest(BaseWindow):
	return_val = False
	def onAction(self, action):
		pass
	
	def onInit(self):
		self.test_url()
	
	def test_url(self):
		encoded_url = self.encoded_url
		test = re.search("^(.+?)(://)(.+?)$", encoded_url)
		scraper = test.group(1)
		raw_url = test.group(3)
		Scraper = ScraperPool(load=[scraper])
		if Scraper.get_scraper_by_index(0).skip_pretest:
			self.return_val = True
			self.close()
			return
		resolved_url = Scraper.resolve_url(encoded_url)
		try:
			self.return_val = Scraper.test_stream(scraper, resolved_url)
			self.getControl(84001).setLabel("Success!")
		except:
			self.return_val = False
		plugin.sleep(150)
		self.close()
	
	def onClick(self, controlID):
		if controlID == 84005:
			self.close()	
		

class StreamSelect(BaseWindow):
	choice = -1
	def __init__(self, *args, **kwargs):
		BaseWindow.__init__(self)

	def onInit(self):
		items = []
		for stream in self.streams:
			result = self.results[self.streams.index(stream)]
			raw_url = self.options[self.streams.index(stream)]
			icon = table[result.quality]
			liz = xbmcgui.ListItem(stream, iconImage='definition/' + icon)
			liz.setProperty('raw_url', raw_url)
			items.append(liz)
		self.getControl(CONTROLS.LISTS).addItems(items)
		self.getControl(CONTROLS.LISTS).selectItem(0)

	
	def onClick(self, controlID):
		if controlID==CONTROLS.LISTS:
			index = self.getControl(CONTROLS.LISTS).getSelectedPosition()
			raw_url = self.getControl(CONTROLS.LISTS).getSelectedItem().getProperty("raw_url")
			if plugin.get_setting('test_streams') == "true" and test_url(raw_url) is False:
				plugin.error_message('Streaming Error', "Stream failed, try again")
				index = self.getControl(CONTROLS.LISTS).removeItem(index)
			else:	
				self.choice = index
				self.close()
		elif controlID == CONTROLS.CLOSE:
			self.close()
			
class StreamSelect2(BaseWindow):
	choice = -1
	def __init__(self, *args, **kwargs):
		BaseWindow.__init__(self)

	def onInit(self):
		items = []
		DB.connect()
		results = DB.query("SELECT host, score FROM host_scores", force_double_array=True)
		DB.disconnect()
		scores = {}
		for r in results:
			scores[r[0]] = r[1]

		for stream in self.streams:
			result = self.results[self.streams.index(stream)]
			raw_url = self.options[self.streams.index(stream)]
			icon = table[result.quality]
			liz = xbmcgui.ListItem(result.text, iconImage='definition/' + icon)
			liz.setProperty("host", "%s://%s" % (result.service, result.hostname))
			if result.hostname in scores:
				score = int(round(scores[result.hostname] * 10))
				liz.setProperty("score", "scores/%s.png" % score)
			display = []
			size = format_size(result.size)
			if size:
				display.append('[COLOR blue]Size: ' + size + '[/COLOR]')
				
			if result.bitrate is not None:
				display.append('[COLOR purple]Bitrate: %s kb/s[/COLOR]' % result.bitrate)
			if result.x265:
				display.append('[COLOR darkorange]x265[/COLOR]')
			if result.hc:
				display.append('[COLOR olive]HC[/COLOR]')	
			if len(result.debrid_flags):
				display.append('[COLOR pink]Debrid: ' + ','.join(result.debrid_flags) + '[/COLOR]')
					
			if result.extension is not None and result.extension.lower() in ['avi', 'mkv', 'mp4', 'flv']:
				display.append('[COLOR green]Ext: ' + result.extension + '[/COLOR]')
				
			liz.setLabel2('  '.join(display))
			liz.setProperty('raw_url', raw_url)
			
			items.append(liz)
		self.getControl(CONTROLS.LISTS).addItems(items)
		self.getControl(CONTROLS.LISTS).selectItem(0)

	
	def onClick(self, controlID):
		if controlID==CONTROLS.LISTS:
			index = self.getControl(CONTROLS.LISTS).getSelectedPosition()
			raw_url = self.getControl(CONTROLS.LISTS).getSelectedItem().getProperty("raw_url")
			if plugin.get_setting('test_streams') == "true" and test_url(raw_url) is False:
				plugin.error_message('Streaming Error', "Stream failed, try again")
				index = self.getControl(CONTROLS.LISTS).removeItem(index)
			else:
				self.choice = index
				self.close()
		elif controlID == CONTROLS.CLOSE:
			self.close()				