#Jor-EL Addon KoDIY

import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['watch-series.ru']
		self.base_link = 'https://watch-series.ru'
		self.search_link = '/series/%s-season-%s-episode-%s'

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = cleantitle.geturl(tvshowtitle)
			return url
		except:
			return
 
	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url: return
			tvshowtitle = url
			url = self.base_link + self.search_link % (tvshowtitle, season, episode)
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			r = client.request(url)
			try:
				match = re.compile('data-video="http(.+?)"><div class=".+?">(.+?)</div>').findall(r)
				for url, source in match: 
					url = 'http' + url
					source = source.replace('OpenUpload','Openload')
					sources.append({
						'source': source,
						'quality': 'SD',
						'language': 'en',
						'url': url,
						'direct': False,
						'debridonly': False
					})
			except:
				return
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url