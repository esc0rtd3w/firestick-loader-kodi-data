# -*- coding: utf-8 -*-

'''
	Venom Add-on
'''

import json, requests, threading, re, urllib
import datetime

from resources.lib.modules import control
from resources.lib.modules import log_utils
from resources.lib.modules import client
from resources.lib.modules import workers
from resources.lib.modules import trakt
from resources.lib.modules import cleantitle


class TVDBAPI:
	def __init__(self):
		self.apiKey = tools.getSetting('tvdb.apikey')
		if self.apiKey == '':
			self.apiKey = "43VPI0R8323FB7TI"

		self.baseUrl = 'https://api.thetvdb.com/'
		self.jwToken = tools.getSetting('tvdb.jw')
		self.headers = {'Content-Type': 'application/json'}
		self.art = {}
		self.info = {}
		self.episode_summary = {}
		self.cast = []
		self.baseImageUrl = 'https://www.thetvdb.com/banners/'
		self.threads = []