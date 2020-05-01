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

class torrentdownloadsScraper(CommonScraper):
	def __init__(self):
		self.service='torrentdownloads'
		self.name = 'torrentdownloads.me'
		self.referrer = 'https://torrentdownloads.me'
		self.base_url = 'https://torrentdownloads.me'
		self.is_cachable = True
		self.premiumize = True
		self.broken = validate_premiumize() == False
		self.get_debrid_hosts()
			
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		search = "%s S%sE%s" % (args['showname'], str(args['season']).zfill(2), str(args['episode']).zfill(2))
		query = {"type": "search", "cid": 8, "search": search}
		uri = '/rss.xml'
		xml = self.request(uri, query=query, return_xml=True, cache=3600)
		pattern = "(S%sE%s)|(Part %s)" % (str(args['season']).zfill(2), str(args['episode']).zfill(2), args['episode'])
		regex = re.compile(pattern, re.IGNORECASE)
		results = self.process_results(xml, regex=regex)
		return self.get_response(results)

	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		search = "%s %s" % (args['title'], args['year'])
		query = {"type": "search", "cid": 4, "search": search}
		uri = '/rss.xml'
		xml = self.request(uri, query=query, return_xml=True, cache=3600)
		results = self.process_results(xml)
		return self.get_response(results)
		
	def process_results(self, xml, regex=""):
		results = []
		hashes = [item.find('info_hash').text for item in xml.iter('item')]
		hashes = pm.check(hashes)
		for item in xml.iter('item'):
			
			hash = item.find('info_hash').text
			if self.return_cached_torrents and hashes['hashes'][hash]['status'] != 'finished': continue
			if self.return_cached_torrents is False and hashes['hashes'][hash]['status'] == 'finished': continue
			title = item.find('title').text
			test = True
			if regex:
				test = regex.search(title)
			if test:	
				url = "http://itorrents.org/torrent/%s.torrent?%s" % (hash.upper(), urllib.urlencode({"title": title}))
				url = "%s://%s" % (self.service, url)
				result = ScraperResult({}, self.service, self.name, url, title)
				result.quality = self.test_quality(title)
				result.size = item.find('size').text
				results += [result]

		return results
	
	
	def get_resolved_url(self, raw_url):
		resolved_url = ''
		hash = re.search('torrent/([^\.]+)\.torrent', raw_url).group(1)
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
