import sys
import os
import re
import gc
import urllib
import time
from urlparse import urlparse
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult
QUALITY_MAP = {"HD": QUALITY.HD, "DVD": QUALITY.SD480, "CAM": QUALITY.LOW, "TS": QUALITY.LOW}
class losmoviesScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='losmovies'
		self.name = 'losmovies.es'
		self.referrer = 'http://losmovies.cc'
		self.base_url = 'http://losmovies.cc'
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		self.start_time = time.time()
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_tvshow_results(html, args['imdb_id'], args['season'], args['episode'])
		return self.get_response(results)
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('movie', args['title'], args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_movie_results(html, args['imdb_id'])
		return self.get_response(results)
	
	def process_movie_results(self, html, imdb_id):
		results = []
		match = re.search('imdb\.com/title/(tt\d+?)"', html)
		if match:
			if match.group(1) != imdb_id: return results
		gc.disable()
		for link in re.finditer('<tr class="linkTr">(.+?)</tr>', html, re.DOTALL):
			html = link.group(1)
			url = re.search('linkHiddenUrl" data-width="\d+" data-height="\d+">(.+?)</td>', html).group(1)
			obj = urlparse(url)
			host_name =  re.sub('^(www\.|embed\.)*', '', obj.hostname)
			if self.filter_host(host_name):
				url = "%s://%s" % (self.service, url)
				quality = re.search('linkQuality([A-Z]+?)"', html).group(1)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				if quality in QUALITY_MAP.keys():
					result.quality = QUALITY_MAP[quality]
				else:
					result.quality = QUALITY.UNKNOWN
				results += [result]
		gc.enable()
		return results
	
	def process_tvshow_results(self, html, imdb_id, season, episode):
		results = []
		match = re.search('imdb\.com/title/(tt\d+?)"', html)
		if match:
			if match.group(1) != imdb_id: return results
		pattern = '(Season %s Serie %s</h3>.*?</table>)' % (season, episode)
		match = re.search(pattern, html, re.DOTALL)
		if not match: return []
		fragment = match.group(1)
		gc.disable()
		for link in re.finditer('<tr class="linkTr">(.+?)</tr>', fragment, re.DOTALL):
			html = link.group(1)
			url = re.search('linkHiddenUrl" data-width="\d+" data-height="\d+">(.+?)</td>', html).group(1)
			obj = urlparse(url)
			host_name =  re.sub('^(www\.|embed\.)*', '', obj.hostname)
			if self.filter_host(host_name):
				url = "%s://%s" % (self.service, url)
				quality = re.search('linkQuality([A-Z]+?)"', html).group(1)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				if quality in QUALITY_MAP.keys():
					result.quality = QUALITY_MAP[quality]
				else:
					result.quality = QUALITY.UNKNOWN
				results += [result]
	
		gc.enable()
		return results
	

		
	def prepair_query(self, media, *args, **kwards):
		search_title = args[0].lower().replace(" ", "-")
		if media == 'tvshow':
			search_uri = 'search'
			html = self.request(search_uri, query={"type": "movies", "q": args[0]}, cache=86400)
			pattern = 'class="movieQuality[^>]+>\s*(.*?)\s*<div\s+class="movieInfo".*?showRowImage">\s*<a\s+href="([^"]+).*?<h4[^>]+>([^<]+)'
			for match in re.finditer(pattern, html, re.DOTALL):
				match_type, uri, title = match.groups('')
				if 'movieTV' not in match_type:
					continue
				r = re.search('(\d{4})$', uri)
				if r:
					match_year = r.group(1)
				else:
					match_year = ''
				if args[1] == match_year:
					return uri
				pattern = '/watch-online-%s$' % search_title
				match = re.search(pattern, uri)
				if match:
					return uri
			
			return False	
		else:
			search_uri = 'search'
			html = self.request(search_uri, query={"type": "movies", "q": args[0]}, cache=86400)
			pattern = 'class="movieQuality[^>]+>\s*(.*?)\s*<div\s+class="movieInfo".*?showRowImage">\s*<a\s+href="([^"]+).*?<h4[^>]+>([^<]+)'
			for match in re.finditer(pattern, html, re.DOTALL):
				match_type, uri, title = match.groups('')
				if 'movieTV' in match_type:
					continue
				r = re.search('(\d{4})$', uri)
				if r:
					match_year = r.group(1)
				else:
					match_year = ''
				if args[1] == match_year:
					return uri
				pattern = '/watch-online-%s$' % search_title
				match = re.search(pattern, uri)
				if match: 
					return uri
			return False