import re
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult


class vumooScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='vumoo'
		self.name = 'vumoo.ch'
		self.referrer = 'http://vumoo.li'
		self.base_url = 'http://vumoo.li'
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html, args['season'], args['episode'])
		return self.get_response(results)
	
	def search_movie(self, args):
		results = []
		uri = self.prepair_query('movie', args['title'], args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_movie_results(html, args['year'])
		return self.get_response(results)
	
	def process_results(self, html, season, episode):
		results = []
		pattern = '<li\sid=\"season%s-%s[^"]+"\sdata-click="([^"]+)"' % (season, episode)
		for match in re.finditer(pattern, html, re.DOTALL):
			stream_url = self.get_redirect(match.group(1))
			plugin.log(stream_url)
			if stream_url:
				url = "%s://%s" % (self.service, stream_url)
				result = ScraperResult(self.debrid_hosts, self.service, 'gvideo', url)
				result.quality = self.test_gv_quality(stream_url)
				results += [result]
		return results
	
	def process_movie_results(self, html, year):
		results = []
		pattern = '<div class="video"> <iframe src="([^"]+)" scrolling="no" frameborder="0" width="100%" height="450px"'
		match = re.search(pattern, html, re.DOTALL)
		if match:
			href = match.group(1)
			host_name = self.get_domain_from_url(href)
			url = self.get_embeded_url(href)
			result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
			result.quality = QUALITY.HD720
			results += [result]
		return results

	def get_resolved_url(self, raw_url):
		resolved_url = raw_url
		return resolved_url
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			uri = "/videos/search/"
			html = self.request(uri, query={"search": args[0]}, cache=86640)
			pattern = 'href="([^"]+)" data-remote="[^"]+" alt="%s" class="zoom"' % args[0]
			match = re.search(pattern, html, re.IGNORECASE)
			if match:
				uri = match.group(1)
				return uri
			#pattern = 'href="([^"]+)" data-remote="[^"]+" alt="([^"]+)" class="zoom"'
			#for match in re.finditer(pattern, html, re.DOTALL):
			#	uri, title = match.groups()
			#	if title == args[0]:
			#		return uri	
		else:
			uri = "/videos/search/"
			html = self.request(uri, query={"search": args[0]}, cache=86640)
			pattern = 'href="([^"]+)" data-remote="[^"]+" alt="([^"]+)" class="zoom"'
			for match in re.finditer(pattern, html, re.DOTALL):
				uri, title = match.groups()
				if title == args[0]:
					return uri	
		return False
	
