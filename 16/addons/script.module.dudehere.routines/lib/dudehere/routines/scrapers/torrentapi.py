import re
import json
import urllib
import xbmcaddon
import xbmcgui
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines.scrapers import CommonScraper, ScraperResult
from dudehere.routines.premiumize import PremiumizeAPI

pm = PremiumizeAPI()

def validate_premiumize():
	return xbmcaddon.Addon('script.module.urlresolver').getSetting('PremiumizeMeResolver_login') == 'true'

class torrentapiScraper(CommonScraper):
	def __init__(self):
		self.service='torrentapi'
		self.name = 'torrentapi.org'
		self.referrer = 'https://torrentapi.org'
		self.base_url = 'https://torrentapi.org'
		self.is_cachable = True
		self.premiumize = True
		self.broken = validate_premiumize() == False
		self.get_debrid_hosts()

	
	def Request(self, uri):
		r = self.request(uri, return_json=True)
		if 'error_code' in r and (r['error_code'] == 1 or r['error_code'] == 4):
			plugin.clear_property('torrent.token')
			self.get_token(force_refresh=True)
			r = self.request(uri, return_json=True)
		return r
			
		
				
	def get_token(self, force_refresh=False):
		token = plugin.get_property('torrent.token')
		if token and force_refresh is False:
			return token
		uri = "/pubapi_v2.php"
		params = {"get_token": "get_token"}
		uri = uri + '?' + urllib.urlencode(params)
		r = self.request(uri, return_json=True)
		if 'token' in r:
			token = r['token']
			plugin.set_property('torrent.token', str(token))
			return token
	
	def search_tvshow(self, args):
		results = []
		uri = "/pubapi_v2.php"
		token = self.get_token()
		query = "%s S%sE%s" % (args['showname'], str(args['season']).zfill(2), str(args['episode']).zfill(2))
		params = {"token": token, "format": "json_extended", "mode": "search", "category":"tv", "search_string": query}
		uri = uri + '?' + urllib.urlencode(params)
		response = self.Request(uri)
		if 'torrent_results' in response:
			results = self.process_results(response)
		return self.get_response(results)	

	
	def search_movie(self, args):
		results = []
		uri = "/pubapi_v2.php"
		token = self.get_token()
		params = {"token": token, "format": "json_extended", "mode": "search", "category":"movies", "search_imdb": args['imdb_id']}
		uri = uri + '?' + urllib.urlencode(params)
		response = self.Request(uri)
		if 'torrent_results' in response:
			results = self.process_results(response)
		return self.get_response(results)
	
	def process_results(self, response):
		results = []
		hashes = []
		hash_regex = re.compile('btih:([^&]+)&')
		for r in response['torrent_results']:
			hash = hash_regex.search(r['download'])
			if hash:
				hashes.append(hash.group(1))
		hashes = pm.check(hashes)
		for r in response['torrent_results']:
			hash = hash_regex.search(r['download'])
			if not hash: continue
			hash = hash.group(1)
			if self.return_cached_torrents and hashes['hashes'][hash]['status'] != 'finished': continue
			if self.return_cached_torrents is False and hashes['hashes'][hash]['status'] == 'finished': continue
			url = "%s://%s" % (self.service, r['download'])
			result = ScraperResult({}, self.service, self.name, url, r['title'])
			result.quality = self.test_quality(r['title'])
			result.size = r['size']
			results += [result]
		return results
	
	
	
	
	def get_resolved_url(self, raw_url):
		resolved_url = ''
		hash = re.search('btih:([^&]+)&', raw_url).group(1)
		self.set_property('Playback.Hash', hash)
		response = pm.queue(raw_url)
		if 'status' in response:
			if response['status'] == 'success':
				if 'id' not in response: return ''
				hash = response['id']
				results = pm.browse(hash)
				resolved_url = pm.get_stream(results)
			else:
				pm.clear(hash)
				response = pm.queue(raw_url)
				if 'id' not in response: return ''
				hash = response['id']
				results = pm.browse(hash)
				resolved_url = pm.get_stream(results)
		return resolved_url
