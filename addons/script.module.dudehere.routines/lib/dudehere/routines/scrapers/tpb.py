import re
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

class tpbScraper(CommonScraper):
	def __init__(self):
		self.service='tpb'
		self.name = 'thepiratebay.org'
		self.referrer = 'https://thepiratebay.org'
		self.base_url = 'https://thepiratebay.org'
		self.is_cachable = True
		self.premiumize = True
		self.broken = validate_premiumize() == False
		self.get_debrid_hosts()
			
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		pattern = "S%sE%s" % (str(args['season']).zfill(2), str(args['episode']).zfill(2))
		title = urllib.quote_plus(re.sub("[^a-zA-Z0-9 ]", '', args['showname']))
		uri = '/search/%s+%s/0/5/200' % (title, pattern)
		soup = self.request(uri, return_soup=True, cache=3600)
		results = self.process_results(soup)
		return self.get_response(results)

	def search_movie(self, args):
		results = []
		self.domains = args['domains']
		title = re.sub("[^a-zA-Z0-9 ]", '', args['title'])
		uri = '/search/%s %s/0/99/201' % (title, args['year'])
		soup = self.request(uri, return_soup=True, cache=3600)
		results = self.process_results(soup)
		return self.get_response(results)
		
	def process_results(self, soup):
		results = []
		links = soup.findAll('tr')

		hashes = []
		hash_regex = re.compile('btih:([^&]+)&')
		for link in links:
			magnet = link.find('a', {"title": "Download this torrent using magnet"})
			if not magnet: continue
			hash = hash_regex.search(magnet['href'])
			if hash:
				hashes.append(hash.group(1))
		hashes = pm.check(hashes)
		regex = re.compile('\/torrent\/\d+\/')
		size_regex = re.compile('Size\s(\d+\.\d+)&nbsp;(M|G)')
		for link in links:
			magnet = link.find('a', {"title": "Download this torrent using magnet"})
			if not magnet: continue
			hash = hash_regex.search(magnet['href'])
			if not hash: continue
			hash = hash.group(1)
			if hash in hashes['hashes']:
				if self.return_cached_torrents and hashes['hashes'][hash]['status'] != 'finished': continue
				if self.return_cached_torrents is False and hashes['hashes'][hash]['status'] == 'finished': continue
				title = link.find('a', {"class": "detLink"})
				if title:
					title = title['href']
					title = regex.sub('', title)
				url = "%s://%s" % (self.service, magnet['href'])
				result = ScraperResult({}, self.service, self.name, url, title)
				result.quality = self.test_quality(title)
				match = link.find('font', {"class": "detDesc"})
				if match:
					match = size_regex.search(str(match))
					if match:
						size, prefix = match.groups()
						if prefix == 'M':
							result.size = float(size) * 1024 * 1024
						else:
							result.size = float(size) * 1024 * 1024 * 1024
				results += [result]

		return results
	
	
	def get_resolved_url(self, raw_url):
		resolved_url = ''
		hash = re.search('btih:([^&]+)&', raw_url).group(1)
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
				if 'id' not in response: return ''
				hash = response['id']
				results = pm.browse(hash)
				resolved_url = pm.get_stream(results)
		return resolved_url		
