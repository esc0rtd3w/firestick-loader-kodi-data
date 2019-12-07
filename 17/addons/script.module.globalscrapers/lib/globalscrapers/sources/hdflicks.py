#Jor-EL Addon KoDIY

import re
import urllib
import urlparse
from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['123flix.pw']
		self.base_link = 'http://hd-flicks.xyz'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = self.base_link + '/%s/' % title
			return url
		except:
			return

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
			url = self.base_link + '/episode/%s-season-%s-episode-%s/' % (tvshowtitle,season,episode)
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			scraper = cfscrape.create_scraper()
			r = scraper.get(url).content
			try:
				match = re.compile('<iframe src=".+?//(.+?)/(.+?)"').findall(r)
				for host,url in match: 
					url = 'https://%s/%s' % (host,url)
					host = host.replace('www.','')
					sources.append({'source': host,'quality': 'HD','language': 'en','url': url,'direct': False,'debridonly': False}) 
			except:
				return
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url