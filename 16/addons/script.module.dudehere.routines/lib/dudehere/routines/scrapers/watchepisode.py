'''
watchepisode.tv source plugin
@natko1412, 2015

'''

import re
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult

class watchepisodeScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='watchepisode'
		self.name = 'watchepisode.tv'
		self.referrer = 'http://www.watchepisodeseries.com'
		self.base_url = 'http://www.watchepisodeseries.com'
		self.get_debrid_hosts()

	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		url = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		html = self.request(url, append_base=False, cache=86440)
		if html:
			results = self.process_results(html, args['showname'], args['season'], args['episode'])
		return self.get_response(results)
	

	def process_results(self, html, show, season, episode):
		results = []
		showname = self.url_friendly(show)
		pattern = 'href="(http:\/\/www\.watchepisodeseries\.com\/%s-season-%s-episode-%s-[^"]+)">([^<]+)<\/a>'  % (showname, season, episode)
		for match in re.finditer(pattern, html, re.DOTALL):
			url, host_name = match.groups()
			if self.filter_host(host_name):
				url = "%s://%s" % (self.service, url)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				results += [result]
		return results
		
		
	def prepair_query(self, media, *args, **kwards):
		uri = False
		if media == 'tvshow':
			showname = self.url_friendly(args[0])
			uri = "/%s" % showname
			html = self.request(uri, cache=86440)
			pattern = 'href="(http:\/\/www\.watchepisodeseries\.com\/%s-season-%s-episode-%s-[^"]+)"' % (showname, args[1], args[2])
			match = re.search(pattern, html, re.DOTALL)
			if match:
				href = match.group(1)
				return href

	def get_resolved_url(self, raw_url):
		html = self.request(raw_url, append_base=False)
		pattern = 'href="([^"]+)"\s+data-episodeid'
		match = re.search(pattern, html, re.DOTALL)
		if match:
			href = match.group(1)
			return self.do_urlresolver(href)