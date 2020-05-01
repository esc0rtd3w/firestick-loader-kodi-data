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

class extratorrentScraper(CommonScraper):
	def __init__(self):
		self.service='extratorrent'
		self.name = 'extratorrent.cc'
		self.referrer = 'https://extratorrent.cc'
		self.base_url = 'https://extratorrent.cc'
		self.is_cachable = True
		self.premiumize = True
		self.broken = validate_premiumize() == False
		self.get_debrid_hosts()
			
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = '/rss.xml'
		query = {"search": "%s S%sE%s" % (args['showname'], str(args['season']).zfill(2), str(args['episode']).zfill(2)), "type": "search"}
		xml = self.request(uri, query=query, return_xml=True, cache=3600)
		results = self.process_results(xml)
		return self.get_response(results)

	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = '/rss.xml'
		query = {"search": "%s %s" % (args['title'], args['year']), "type": "search"}
		xml = self.request(uri, query=query, return_xml=True, cache=3600)
		results = self.process_results(xml)
		return self.get_response(results)
		
	def process_results(self, xml):
		results = []
		hashes = [item.find("info_hash").text for item in xml.iter('item')]
		hashes = pm.check(hashes)
		for item in xml.iter('item'):
			hash = item.find("info_hash").text
			if self.return_cached_torrents and hashes['hashes'][hash]['status'] != 'finished': continue
			if self.return_cached_torrents is False and hashes['hashes'][hash]['status'] == 'finished': continue
			title = os.path.basename(vfs.path_parts(urllib.unquote_plus(item.find('link').text))['path'])
			magnet = item.find('magnetURI').text
			url = "%s://%s" % (self.service, magnet)
			result = ScraperResult({}, self.service, self.name, url, title)
			result.quality = self.test_quality(title)
			result.size = item.find('size').text
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
