import sys
import os
import re
import gc
import urllib
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines.scrapers import CommonScraper, ScraperResult
class alluc_apiScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='alluc_api'
		self.name = 'alluc.ee'
		self.referrer = 'http://www.alluc.ee'
		self.base_url = 'http://www.alluc.ee'
		self.username = plugin.get_setting(self.service + '_username')
		self.password = plugin.get_setting(self.service + '_password')
		self.language = plugin.get_setting(self.service + '_language')
		self.max_results = 50
		self.require_auth = True
		self.domains = None
		self.get_debrid_hosts()
	
	def check_authentication(self, username, password):
		valid = False
		self.max_results = 1
		self.username = username
		self.password = password
		self.language = ''
		query = self.prepair_query('movie', 'big buck bunny', '')
		uri = '/api/search/download/%s' %  query
		results = self.request(uri, return_json=True)
		valid = results['status']=='success'
		return valid
	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		query = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'])
		s=args['season']
		ss=str(args['season']).zfill(2)
		e=str(args['episode']).zfill(2)
		patern = "(S%sE%s)|(%s%s)|(%s.%s)|(%s.%s)" % (ss,e,s,e,ss,e,s,e)
		re_test = re.compile(patern, re.IGNORECASE)
		for endpoint in ['stream', 'download']:
			uri = '/api/search/%s/%s' % (endpoint, query)
			data = self.request(uri, return_json=True)
			results = results + self.process_results(data, re_test)
		return self.get_response(results)
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		query = self.prepair_query('movie', args['title'], args['year'])
		for endpoint in ['stream', 'download']:
			uri = '/api/search/%s/%s' % (endpoint, query)
			data = self.request(uri, return_json=True)
			results = results + self.process_results(data)
		return self.get_response(results)
	
	def quick_search(self, query):
		results = []
		query = self.prepair_query('quick', query)
		for endpoint in ['stream', 'download']:
			uri = '/api/search/%s/%s' % (endpoint, query)
			data = self.request(uri, return_json=True)
			results = results + self.process_results(data)
		return self.get_response(results)
	
	def process_results(self, data, re_test=None):
		results = []
		if data['status'] != 'success':
			plugin.log(data)
			return []
		gc.disable()
		for result in data['result']:
			title = self.normalize(result['title'])
			if re_test:
				if re_test.search(title) is None: continue
			sourcetitle = self.normalize(result['sourcetitle'])
			hoster = result['hosterurls']
			extension = result['extension']
			size = result['sizeinternal']
			extension = result['extension']
			host_name = result['hostername']
			hosts = result['hosterurls']
			if extension == 'rar': continue
			for host in hosts:
				if self.filter_host(host_name):
					url = "%s://%s" % (self.service, host['url'])
					quality = self.test_quality(title+sourcetitle+self.normalize(url))
					result = ScraperResult(self.debrid_hosts, self.service, host_name, url, title)
					result.quality = quality
					result.size = int(size)
					result.extension = extension
					results += [result]
		gc.enable()
		return results
		
	def prepair_query(self, media, *args, **kwards):
		self.max_results = int(plugin.get_setting('max_results')) if plugin.get_setting('max_results') != '' else 100
		uri = "?%s"
		params = {"from": 0, "count": self.max_results, "getmeta":0}
		params['user'] = self.username
		params['password'] = self.password
		if media == 'tvshow':
			params['query'] = "%s S%sE%s" % args
		elif media == 'quick':
			params['query'] = args[0]
		else:
			params['query'] = "%s %s" % args
		if self.language: params['query'] = params['query'] + ' lang:' + self.language
		return uri % urllib.urlencode(params)