'''
projectfreetv.so source plugin
@natko1412, 2015
'''

import re
from dudehere.routines import *
from dudehere.routines.plugin import log
from dudehere.routines.scrapers import CommonScraper, ScraperResult



class projectfreetvScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='projectfreetv'
		self.name = 'projectfreetv.so'
		self.referrer = 'http://projectfreetv.im'
		self.base_url = 'http://projectfreetv.im'
		self.get_debrid_hosts()

	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html)
		return self.get_response(results)
	
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('movie', args['title'], args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html)
		return self.get_response(results)

	def process_results(self, html):
		results = []
		pattern='aff_id=(\d+)"\s[^\?]+\?domain=([^"]+)'
		for match in re.finditer(pattern, html, re.DOTALL):
			id, host_name = match.groups()
			if self.filter_host(host_name):
				url = "%s://http://projectfreetv.im/watch/?aff_id=%s" % (self.service, id)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				result.quality = QUALITY.UNKNOWN
				results += [result]
		return results

	def get_resolved_url(self, raw_url):
		html = self.request(raw_url)
		pattern = '<a rel="nofollow" href="([^"]+)"><input type="button" class="myButton"'
		match = re.search(pattern, html)
		if match:
			raw_url = match.group(1)
			return self.do_urlresolver(raw_url)
		return None
	
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			showname = self.url_friendly(args[0])
			season = str(args[1])
			episode = str(args[2])
			uri='/episode/%s-season-%s-episode-%s/' % (showname,season,episode)
			return uri
		elif media=='movie':
			title=self.url_friendly(args[0])
			year=args[1]
			uri='/movies/%s-%s/'%(title,year)
			return uri