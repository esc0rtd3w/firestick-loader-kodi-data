import sys
import os
import re
import urllib
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult
'''*	Example Scraper Plugin
	Class Name
		The class must follow the format [service]Scraper where service is a unique identifier for the scraper class
		the example below uses the identifier `example`. This should must also be the name of the scraper file example.py
	
	Required Properties
		service: the unique identifier of the scraper
		name: The formated name for the scraper. A string that will be used as the visible name associated with the results
		base_url: Fairly obvious.
		referrer: default referrer url
	
	Optional Properties
		broken: A boolean flag to marke the scraper as broken. It will not be loaded if set to True
		timeout: Scraper specific request timeout limit in seconds
		require_auth: If set to true, the worker pool will check for the parent addon settings for `service`_username and `service`_username
			if either are null, the scraper will not be loaded 
		
		 
*'''


class exampleScraper(CommonScraper):
	def __init__(self):
		self.service='example'
		self.name = 'example.com'
		self.referrer = 'http://www.example.com'
		self.base_url = 'http://www.example.com'
		self.timeout = 2
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'])
		soup = self.request(uri, return_soup=True)
		results = self.process_results(soup)
		return self.get_response(results)
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('movie', args['title'])
		soup = self.request(uri, return_soup=True)
		results = self.process_results(soup)
		return self.get_response(results)
	
	def process_results(self, soup):
		results = []
		links = soup.findAll('a', {"rel": "nofollow", "target": "_blank"})
		for link in links:
			host_name = link.string.lower()
			if host_name in self.domains:
				url = "%s://%s" % (self.service, link['href'])
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				result.quality = QUALITY.UNKNOWN
				results.append(result)	
		return results
	
	def get_resolved_url(self, raw_url):
		import urlresolver
		resolved_url = ''
		raw_url = self.get_redirect(raw_url)
		source = urlresolver.HostedMediaFile(url=raw_url)
		resolved_url = source.resolve() if source else None
		return resolved_url
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			showname = args[0].lower().replace(" ", "_")
			season = args[1]
			episode = args[2]
			uri = "/Serie/%s-Season-%s-Episode-%s" % (showname, season, episode)
		else:
			import string
			title = string.capwords(args[0]).replace(" ", "_")		
			uri = "/Film/%s" % title
		return uri
