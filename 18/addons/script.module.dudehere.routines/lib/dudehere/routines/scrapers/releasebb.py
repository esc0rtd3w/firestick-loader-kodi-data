#!/usr/bin/python
# -*- coding: utf-8 -*-
PYTHONIOENCODING="UTF-8"

import re
import urllib
from dudehere.routines import *
from dudehere.routines.vfs import VFSClass
from dudehere.routines.scrapers import CommonScraper, ScraperResult



class releasebbScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='releasebb'
		self.name = 'releasebb'
		self.referrer = 'http://rlsbb.com'
		self.base_url = 'http://rlsbb.com'
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		if uri:
			html = self.request(uri)
			pattern = "S%02dE%02d" % (args['season'], args['episode'])

			include = re.compile(pattern, re.IGNORECASE)
			results = self.process_results(html, include)
		return self.get_response(results)
	
	def search_movie(self, args):
		self.base_url = 'http://old.rlsbb.com'
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('movie', args['title'], args['year'])
		if uri:
			html = self.request(uri)
			if html:
				results = self.process_movie_results(html)
		return self.get_response(results)
	
	def process_results(self, html, include):
		results = []
		pattern = 'href="([^"]+)"\s+rel="nofollow"'
		exclude = re.compile("(\.rar$)|(\.part\d+\.|-|_rar)", re.IGNORECASE)
		
		for link in re.finditer(pattern, html, re.DOTALL):
			href = link.group(1)
			if include.search(href):
				if exclude.search(href): continue
				url = "%s://%s" % (self.service, href)
				host = self.get_domain_from_url(href)
				file = self.get_file_from_url(href, clean='\.html$')
				result = ScraperResult(self.debrid_hosts, self.service, host, url, file)
				result.quality = self.test_quality(file)
				results += [result]
		return results
	

	def process_movie_results(self, html):
		results = []
		pattern = 'href="([^"]+)"\s+rel="nofollow"'
		exclude = re.compile("(\.|_|-rar\.html$)(\.|_|-rar$)|(\.part\d+\.|_|-rar)", re.IGNORECASE)
		for link in re.finditer(pattern, html, re.DOTALL):
			href = link.group(1)
			if exclude.search(href): continue
			url = "%s://%s" % (self.service, href)
			host = self.get_domain_from_url(href)
			if host in self.domains:
				file = self.get_file_from_url(href, clean='\.html$')
				result = ScraperResult(self.debrid_hosts, self.service, host, url, file)
				result.quality = self.test_quality(file)
				results += [result]

		return results

		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			uri = '/%s-s%se%s' % (args[0].replace(' ', '-'), str(args[1]).zfill(2), str(args[2]).zfill(2))
		else:
			uri = '/%s-%s' % (args[0].replace(' ', '-'), args[1])
		return uri
	
