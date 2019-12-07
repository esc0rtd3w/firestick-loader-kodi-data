# -*- coding: utf-8 -*-

class Settings:
	def __init__(self, addon):
		self.addon = addon

	def language(self):
		languages = ['en', 'de']
		return languages[int(self.addon.getSetting('language'))]

	def location(self):
		locations = ['int', 'de', 'at']
		return locations[int(self.addon.getSetting('location'))]

	def debug(self):
		return self.addon.getSetting('debug') == 'true'

	def livefilter(self):
		livefilters = ['all', 'icehockey', 'tabletennis', 'basketball', 'volleyball', 'beachvolley', 'handball', 'football']
		return livefilters[int(self.addon.getSetting('livefilter'))]

	def livelimit(self):
		livelimits = [None, 3, 7, 14]
		return livelimits[int(self.addon.getSetting('livelimit'))]

	def htmlstripping(self):
		return self.addon.getSetting('htmlstripping') == 'true'
