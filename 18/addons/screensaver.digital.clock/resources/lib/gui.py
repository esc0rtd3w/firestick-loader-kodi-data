#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015 DudeHere
#	 Modified from the work of Philip Schmiegelt
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import random
import datetime
import time
import os
import math
import xbmcaddon
import xbmcgui
import xbmc
import xml.etree.ElementTree as ET
import controller


addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path')
SKIN = addon.getSetting('skin')
MILITARY = addon.getSetting('military_time') == 'true'
BURININ = addon.getSetting('anti_burn_in') == 'true'
SHOW_SECONDS = addon.getSetting('enable_seconds') == 'true'

image_dir = xbmc.translatePath( os.path.join( addon_path, 'resources', 'skins', SKIN, 'media' ,'').encode("utf-8") ).decode("utf-8")
settings_file = xbmc.translatePath( os.path.join( addon_path, 'resources', 'skins', SKIN ,'settings.xml').encode("utf-8") ).decode("utf-8")
scriptId   = 'screensaver.digital.clock'



class Screensaver(xbmcgui.WindowXMLDialog):

	class ExitMonitor(xbmc.Monitor):
		def __init__(self, exit_callback, log_callback):
			self.exit_callback = exit_callback
			self.log_callback = log_callback

		def onScreensaverDeactivated(self):
			self.exit_callback()
		def onAbortRequested(self):
			self.exit_callback()


	def showClock(self):
		now = datetime.datetime.today()
		hour = str(now.hour).zfill(2)
		minute = str(now.minute).zfill(2)
		second = str(now.second).zfill(2)
		if MILITARY or self.settings['military_only']=="true":
			hour_1 = str(hour[0])
			hour_2 = str(hour[1])
		else:
			if now.hour > 12:
				PM = True
				hour = str(now.hour % 12).zfill(2)
			else:
				PM = False		
	
			hour_1 = str(hour[0])
			hour_2 = str(hour[1])
	
		minute_1 = str(minute[0])
		minute_2 = str(minute[1])
	
		if SHOW_SECONDS and self.settings['enable_seconds'] == "true":
			second_1 = str(second[0])
			second_2 = str(second[1])
			self.getControl(5).setImage("%s.png" % second_1)
			self.getControl(6).setImage("%s.png" % second_2)
		else:
			self.getControl(7).setVisible(now.second % 2 == 0)
				
		
		self.getControl(1).setImage("%s.png" % hour_1)
		self.getControl(2).setImage("%s.png" % hour_2)
		self.getControl(3).setImage("%s.png" % minute_1)
		self.getControl(4).setImage("%s.png" % minute_2)

		if MILITARY is False and self.settings['military_only']=="false":
			if PM:
				self.getControl(9).setImage("%s.png" % 'pm')
			else :
				self.getControl(9).setImage("%s.png" % 'am')
			self.getControl(9).setVisible(True)
		else:
			self.getControl(9).setVisible(False)
		
		if BURININ and (now.second % 30==0 and self.settings['enable_burn_in']=='true'):
			seed = random.random() * 150
			offsetY = int(seed - 75)
			seed = random.random() * 150
			offsetX = int(seed-75)
			for i in range(1,9):
				x = self.Positions['x'][i-1]
				y = self.Positions['y'][i-1]
				self.getControl(i).setPosition(x+offsetX, y+offsetY)
			seed = random.random() * 30
			offsetY = int(seed - 15)
			seed = random.random() * 30
			offsetX = int(seed-15)
			x = self.Positions['x'][8]
			y = self.Positions['y'][8]
			self.getControl(9).setPosition(x+offsetX, y+offsetY)
			
	def onInit(self):
		self.settings = {}
		doc = ET.parse(settings_file)
		for s in doc.findall('.//setting'): 
			v = str([s.attrib['value']])
			v = v[2:len(v)-2]
			self.settings[s.attrib['id']] = v
			
		self.log("Screensaver starting")
		self.addon      = xbmcaddon.Addon(scriptId)
		
		self.getControl(7).setImage("sep.png")
		if SHOW_SECONDS and self.settings['enable_seconds'] == "true":
			self.getControl(8).setImage("sep.png")
		else:
			offsetX = int( self.settings['military_offset_x'] )
			offsetY = int( self.settings['military_offset_y'] )
			for i in range(1,8):
				x,y = self.getControl(i).getPosition()
				self.getControl(i).setPosition(x+offsetX, y+offsetY)

		self.monitor = self.ExitMonitor(self.exit, self.log)
		self.allImages = list()
		self.Positions = {'x': [], 'y': []}
		
		for i in range(1,10):
			x,y = self.getControl(i).getPosition()
			self.Positions['x'].append(x)
			self.Positions['y'].append(y)

		self.showClock()
		self.cont = controller.Controller(self.log, self.showClock, True)
		self.cont.start() 


	def exit(self):
		self.log('Exit requested')
		self.cont.stop()
		for b in self.allImages[:]:
			b.setVisible(False)
		del self.monitor
		del self.cont
		for b in self.allImages[:]:
			self.removeControl(b)
		del self.allImages[:]
		self.close()

	def log(self, msg):
		xbmc.log(u'Digital Clock Screensaver: %s' % msg)
		

