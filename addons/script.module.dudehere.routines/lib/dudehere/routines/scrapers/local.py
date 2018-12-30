import sys
import os
import re
import json
import xbmc

from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult
from dudehere.routines.vfs import VFSClass
vfs = VFSClass()

class localScraper(CommonScraper):
	def __init__(self):
		self.service='local'
		self.name = 'VideoLibrary'
		self.referrer = 'http://localhost'
		self.base_url = 'http://localhost'
		self.is_cachable = False
		self.get_debrid_hosts()
			
	def search_tvshow(self, args):
		results = []
		path = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'], args['year'])
		if path:
			results = self.process_results(path)
		return self.get_response(results)
	
	def search_movie(self, args):
		results = []
		path = self.prepair_query('movie', args['title'], args['year'])
		if path:
			results = self.process_results(path)
		return self.get_response(results)
	
	def process_results(self, path):
		results = []
		url = "%s://%s" % (self.service, path)
		result = ScraperResult(self.debrid_hosts, self.service, self.name, url)
		result.quality = QUALITY.LOCAL
		result.size = vfs.get_size(path)
		result.text = path
		parts = vfs.path_parts(path)
		result.extension = parts['extension']
		results += [result]
		return results
	
	def get_resolved_url(self, raw_url):
		resolved_url = raw_url
		return resolved_url
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			title = args[0]
			season = args[1]
			episode = args[2]
			year = args[3]
			filter_str = '{{"field": "title", "operator": "contains", "value": "{search_title}"}}'
			filter_str = '{{"and": [%s, {{"field": "year", "operator": "is", "value": "%s"}}]}}' % (filter_str, year)
			cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": { "filter": %s, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "year"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libTvShows"}'
			command = cmd % (filter_str.format(search_title=title))
			data = json.loads(xbmc.executeJSONRPC(command))
			if 'result' in data and 'tvshows' in data['result']:
				for r in data['result']['tvshows']:
					if r['year'] != year or r['title'] != title: continue
					tvshowid = r['tvshowid']
					break
				cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"tvshowid": %s, "season": %s, "filter": {"field": "%s", "operator": "is", "value": "%s"}, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "season", "episode", "file", "streamdetails"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true }}, "id": "libTvShows"}'
				command = cmd % (tvshowid, season, 'episode', episode)
				data = json.loads(xbmc.executeJSONRPC(command))
				if 'result' in data and 'episodes' in data['result']:
					for episode in data['result']['episodes']:
						if episode['file'].endswith('.strm'):
							continue
						else:
							return episode['file']
			return False
		else:
			title = args[0]
			year = args[1]
			filter_str = '{{"field": "title", "operator": "contains", "value": "{search_title}"}}'
			filter_str = '{{"and": [%s, {{"field": "year", "operator": "is", "value": "%s"}}]}}' % (filter_str, year)
			cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "filter": %s, "limits": { "start" : 0, "end": 25 }, "properties" : ["title", "year", "file", "streamdetails"], "sort": { "order": "ascending", "method": "label", "ignorearticle": true } }, "id": "libMovies"}'
			command = cmd % (filter_str.format(search_title=title))
			data = json.loads(xbmc.executeJSONRPC(command))
			if 'result' in data and 'movies' in data['result']:
				for r in data['result']['movies']:
					if r['year'] != year or r['title'] != title or r['file'].endswith('.strm'): continue
					return r['file']
			return False
