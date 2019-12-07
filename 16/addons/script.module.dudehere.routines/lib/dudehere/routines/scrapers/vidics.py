import re
from dudehere.routines import *
from dudehere.routines.plugin import log
from dudehere.routines.scrapers import CommonScraper, ScraperResult
class vidicsScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='vidics'
		self.name = 'vidics.ch'
		self.referrer = 'http://www.vidics.ch'
		self.base_url = 'http://www.vidics.ch'
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html)
		return results
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('movie', args['title'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html)
		return self.get_response(results)
	
	def process_results(self, html):
		results = []
		pattern = 'href="([^"]+)" target="_blank" rel="nofollow">([^>]+)<'
		for match in re.finditer(pattern, html, re.DOTALL):
			href, host_name = match.groups()
			host_name = host_name.lower()
			if self.filter_host(host_name):
				url = "%s://%s" % (self.service, href)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				results += [result]
		return self.get_response(results)
	
	def get_resolved_url(self, raw_url):
		raw_url = self.get_redirect(raw_url)
		if raw_url.startswith('http'):
			return self.do_urlresolver(raw_url)
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			showname = args[0].lower().replace(" ", "-")
			season = args[1]
			episode = args[2]
			uri = "/Serie/%s--Season-%s-Episode-%s" % (showname, season, episode)
		else:
			import string
			title = string.capwords(args[0]).replace(" ", "_")
			uri = "/Film/%s" % title
		return uri