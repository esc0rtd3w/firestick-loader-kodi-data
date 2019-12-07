import re
import xbmcaddon
import xbmcgui
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult
from dudehere.routines.premiumize import PremiumizeAPI

pm = PremiumizeAPI()

def validate_premiumize():
	return xbmcaddon.Addon('script.module.urlresolver').getSetting('PremiumizeMeResolver_login') == 'true'

class ytsScraper(CommonScraper):
	def __init__(self):
		self.service='yts'
		self.name = 'yts.ag'
		self.referrer = 'https://yts.ag'
		self.base_url = 'https://yts.ag'
		self.is_cachable = True
		self.premiumize = True
		self.broken = validate_premiumize() == False
		self.get_debrid_hosts()
	
	def search_movie(self, args):
		if 'year' in args:
			self.return_cached = args['year']
		else:
			self.return_cached = True
		self.domains = args['domains']
		results = []
		query = {"query_term": args['imdb_id']}
		uri = '/api/v2/list_movies.json'
		data = self.request(uri, query=query, return_json=True)
		if 'status' in data and data['status'] == 'ok':
			for movie in data['data']['movies']:
				results += self.process_results(movie)
		return self.get_response(results)
	
	def process_results(self, movie):
		results = []
		hashes = [r['hash'] for r in movie['torrents']]
		hashes = PremiumizeAPI().check(hashes)

		for link in movie['torrents']:
			if self.return_cached and hashes['hashes'][link['hash']]['status'] != 'finished': continue
			if self.return_cached is False and hashes['hashes'][link['hash']]['status'] == 'finished': continue
			url = "%s://%s" % (self.service, link['hash'])
			result = ScraperResult({}, self.service, self.name, url, self.name)
			result.size = link['size_bytes']
			result.quality = self.test_quality(str(link['quality']))
			results += [result]
		return results
	
	def get_resolved_url(self, raw_url):
		resolved_url = ''
		hash = raw_url
		raw_url = "https://yts.ag/torrent/download/%s.torrent" % hash
		self.set_property('Playback.Hash', hash)
		response = pm.queue(raw_url)
		if 'status' in response:
			if response['status'] == 'success':
				hash = response['id']
				if 'id' not in response: return ''
				results = pm.browse(hash)
				resolved_url = pm.get_stream(results)
			else:
				pm.clear(hash)
				response = pm.queue(raw_url)
				hash = response['id']
				if 'id' not in response: return ''
				results = pm.browse(hash)
				resolved_url = pm.get_stream(results)
		return resolved_url
