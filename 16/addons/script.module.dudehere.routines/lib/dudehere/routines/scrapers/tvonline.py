'''
tvonline.tw source plugin
@natko1412, 2015

'''

import re
import urllib
import base64
from dudehere.routines import *
from dudehere.routines.plugin import log
from dudehere.routines.scrapers import CommonScraper, ScraperResult



class tvonlineScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='tvonline'
		self.name = 'tvonline.tw'
		self.referrer = 'http://opentuner.is'
		self.base_url = 'http://opentuner.is'
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html)
		return self.get_response(results)
	

	def process_results(self, html):
		results = []
		pattern = 'stream\.php\?([^"]+)"'
		for match in re.finditer(pattern, html, re.DOTALL):
			
			encoded = match.group(1)
			href = base64.b64decode(encoded)
			test = re.search('(http[s]?.*)', href)
			if test:
				href = test.group(1)
			else: continue
			host_name = self.get_domain_from_url(href)
			if self.filter_host(host_name):
				url = "%s://%s" % (self.service, href)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				result.quality = QUALITY.UNKNOWN
				results += [result]

		return results
	
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			showname = self.url_friendly(args[0])
			uri = "/%s-%s/season-%s-episode-%s/" % (showname, args[3], args[1], args[2])
			return uri
		else:
			return False
