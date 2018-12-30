import re
import json
import urllib,urllib2
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines.scrapers import CommonScraper, ScraperResult
class furkScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='furk'
		self.name = 'furk.net'
		self.referrer = 'http://furk.net'
		self.base_url = 'https://www.furk.net/api'
		self.api_key = ""
		self.username = plugin.get_setting(self.service + '_username')
		self.password = plugin.get_setting(self.service + '_password')
		self.require_auth = True
		self.skip_pretest = True
		self.get_debrid_hosts()
		
	def _login(self):
		params = {"login": self.username, "pwd": self.password}
		uri = '/login/login'
		response = self.request(uri, params=params)
		if 'status' in response.keys():
			if response['status'] == 'ok':
				self.api_key = response['api_key']
			else:
				plugin.log(response)
				return False
		else:
			plugin.log(response)
		return self.api_key
	
	def check_authentication(self, username, password):
		valid = True
		self.username = username
		self.password = password
		key = self._login()
		if key is False: valid = False
		return valid
	
	def _clean_query(self, query):
		cleaned = re.sub("[^A-Za-z0-9. ]", "", query)
		return cleaned
	
	def search_tvshow(self, args):
		results = []
		uri, params = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'])
		data = self.request(uri, params=params)
		results = self.process_results(data)
		return self.get_response(results)

	def search_movie(self, args):
		results = []
		uri, params = self.prepair_query('movie', args['title'], args['year'])
		data = self.request(uri, params=params)
		results = self.process_results(data)
		return self.get_response(results)
	
	def get_resolved_url(self, id):
		self.search_results = []
		resolved_url = ''
		api_key = self._login()
		params = {"type": "video", "id": id, "api_key": api_key, 't_files': 1}
		results = self.request("/file/get", params)
		if results=='':
			return False
		files = results['files'][0]['t_files']
		regex = re.compile('^video/')
		for f in files:
			if regex.search(f['ct']):
				title = f['name']
				result = ScraperResult(self.debrid_hosts, self.service, 'furk.net', f['url_dl'], title)
				if 'size' in f.keys(): result.size = int(f['size'])
				if 'bitrate' in f.keys(): result.bitrate = f['bitrate']
				result.quality = self.test_quality(title)
				self.search_results += [result]
		if len(self.search_results) == 1:
			return self.search_results[0].url
		resolved_url, autoplay =  self.select_stream(sort=False)
		return resolved_url
	
	def process_results(self, data):
		results = []
		if 'files' not in data.keys() : return results
		files = data['files']
		extension = re.compile('(\.MKV)|(\.AVI)|(\.MP4)', re.IGNORECASE)
		for f in files:
			if f['type'] == 'video':
				url = "furk://%s" % f['id']
				title = f['name']
				result = ScraperResult(self.debrid_hosts, self.service, 'furk.net', url, title)
				result.quality = self.test_quality(title)
				result.size = int(f['size'])
				bitrate = re.search('bitrate: (.+?) kb/s', f['video_info'])
				if bitrate: result.bitrate = bitrate.group(1)
				ext = extension.search(title)
				if ext:
					if ext.group(1): result.extension = 'MKV'
					if ext.group(2): result.extension = 'AVI'
					if ext.group(3): result.extension = 'MP4'
				results.append(result)
			
		return results
	
	def prepair_query(self, media, *args, **kwards):
		uri = "/plugins/metasearch"
		api_key = self._login()
		params = {"pretty": 1, "type": "video", "filter": "cached", "api_key": api_key}

		if media == 'tvshow':
			title = self._clean_query(args[0])
			params['q'] = '@name "%s" @name S%02dE%02d | %sx%s' % (title, args[1], args[2], args[1], args[2])

		else:
			title = self._clean_query(args[0])
			params['q'] = '@name "%s" @name %s' % (title, args[1])
		return uri, params
	
	def request(self, uri, params=None):
		url = '%s%s' % (self.base_url, uri)
		if params:
			params['pretty'] = 1
		else:
			params = {'pretty': 1}

		paramsenc = urllib.urlencode(params)
		req = urllib2.Request(url, paramsenc)
		opener = urllib2.build_opener()
		response = opener.open(req)
		data = json.loads(response.read())
		return data
	