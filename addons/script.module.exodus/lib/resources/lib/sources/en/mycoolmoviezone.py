# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 12-10-2018 by JewBMX in Scrubs.

import re,traceback,urllib,urlparse,xbmcgui
from resources.lib.modules import cleantitle,client,proxy,source_utils,log_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['coolmoviezone.online']
		self.base_link = 'https://coolmoviezone.online'


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = self.base_link + '/%s-%s' % (title,year)
			return url
		except:
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			r = client.request(url)
			match = re.compile('<td align="center"><strong><a href="(.+?)"').findall(r)
			for url in match: 
				host = url.split('//')[1].replace('www.','')
				host = host.split('/')[0].split('.')[0].title()
				quality = source_utils.check_sd_url(url)
				sources.append({'source': host, 'quality': quality, 'language': 'en','url': url,'direct': False,'debridonly': False})
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url