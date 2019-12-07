import re, os
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

class torrentprojectScraper(CommonScraper):
	def __init__(self):
		self.service='torrentproject'
		self.name = 'torrentproject.se'
		self.referrer = 'https://torrentproject.se'
		self.base_url = 'https://torrentproject.se'
		self.is_cachable = True
		self.premiumize = True
		self.broken = validate_premiumize() == False
		self.get_debrid_hosts()
			
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = '/rss/%s/' % self.format_tv_search(args['showname'], args['season'], args['episode'])
		xml = self.request(uri, return_xml=True, cache=3600)
		results = self.process_results(xml)
		return self.get_response(results)

	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = '/rss/%s/' % self.format_movie_search(args['title'], args['year'])
		xml = self.request(uri, query=query, return_xml=True, cache=3600)
		results = self.process_results(xml)
		return self.get_response(results)
		
	def process_results(self, xml):
		results = []
		regex_hash = re.compile("<hash>([^<]+)<\/hash>")
		regex_title = re.compile("<br\/>([^<]+) <br\/>")
		 
		hashes = []
		for item in xml.iter('item'):
			desc = item.find("description").text
			hashes.append(str(regex_hash.search(desc).group(1)).upper())
		hashes = pm.check(hashes)
		for item in xml.iter('item'):
			desc = item.find("description").text
			hash = str(regex_hash.search(desc).group(1)).upper()
			if self.return_cached_torrents and hashes['hashes'][hash]['status'] != 'finished': continue
			if self.return_cached_torrents is False and hashes['hashes'][hash]['status'] == 'finished': continue
			atributes = item.find("enclosure").attrib
			url = "%s://%s" % (self.service, hash)
			title = hash = regex_title.search(desc).group(1)
			result = ScraperResult({}, self.service, self.name, url, title)
			result.size = atributes['length']
			result.quality = self.test_quality(title)
			results += [result]
		return results
	
	
	def get_resolved_url(self, raw_url):
		resolved_url = ''
		hash = raw_url
		raw_url = "%s/torrent/%s.torrent'" % (self.base_url, hash)
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
