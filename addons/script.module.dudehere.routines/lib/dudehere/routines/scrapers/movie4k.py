import sys
import os
import re
import urllib
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult
QUALITY_MAP = {None: QUALITY.UNKNOWN, '0': QUALITY.POOR, '1': QUALITY.LOW, '2': QUALITY.LOW, '3': QUALITY.HIGH, '4': QUALITY.HIGH, '5': QUALITY.HIGH}
class movie4kScraper(CommonScraper):
	broken = True
	def __init__(self):
		self._settings = {}
		self.service='movie4k'
		self.name = 'movie4k.to'
		self.referrer = 'http://www.movie4k.to'
		self.base_url = 'http://www.movie4k.to'
		self.headers = {"Cookie": 'onlylanguage=en; lang=en'}
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'], args['imdb_id'])
		uri = False	
		if uri:
			html = self.request(uri, headers=self.headers)
			results = self.process_results(html)
		return self.get_response(results)
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('movie', args['title'], args['imdb_id'])

		if uri:
			html = self.request(uri, headers=self.headers)
			results = self.process_results(html)
		return self.get_response(results)
	
	def process_results(self, html):
		results = []
		pattern = r'id="tablemoviesindex2".*?href="([^"]+).*?&nbsp;([^<]+)(.*)'
		for match in re.finditer(pattern, html):
			url, host_name, extra = match.groups()
			if not url.startswith('/'): url = '/' + url
			r = re.search('/smileys/(\d+)\.gif', extra)
			if r:
				smiley = r.group(1)
			else:
				smiley = None
			url = "%s://%s" % (self.service, url)
			result = ScraperResult(self.debrid_hosts, self.service, host_name.lower(), url)
			result.quality = QUALITY_MAP[smiley]
			results += [result]
		return results
	
	def get_resolved_url(self, raw_url):
		resolved_url = None
		soup = self.request(raw_url, return_soup=True, timeout=4)
		result = soup.find('iframe', {"width": "730", "height": "460"})
		if result:
			raw_url = result['src']	
		else:
			img = soup.find('img', {"src": '/img/click_link.jpg'})
			if img: 
				a = img.parent
				raw_url = a['href']

		return self.do_urlresolver(raw_url)
		
	def prepair_query(self, media, *args, **kwards):
		uri = False
		if media == 'tvshow':
			showname = args[0].lower()
			season = args[1]
			episode = args[2]
			imdb_id = args[3]
			uri = '/movies.php?list=search&search=%s' % imdb_id
			html = self.request(uri, headers=self.headers, cache=86400)
			pattern= '<TD\s+width="550"\s+id="tdmovies">\s+<a\s+href="([^"]+)">([^<]+)\s+<'
			def clean_title(title):
				title = title.replace('(TVshow)', '')
				title = title.strip()
				title = title.lower()
				return title
			ADDON.log(pattern)
			ADDON.log(html)
			for match in re.finditer(pattern, html, re.DOTALL):
				uri, title, extra = match.groups('')
				ADDON.log(title)
				if '(TVshow)' in title:
					title = clean_title(title)
					if title == showname:
						break
			if uri is None: 
				return False
			html = self.request(uri, headers=self.headers, cache=86400)
			pattern = '<FORM name="episodeform%s">(.+?)</FORM>' % season
			result = re.search(pattern, html, re.DOTALL)
			if result:
				pattern = 'value="(.+?)">Episode %s<' % episode
				result = re.search(pattern, result.group(1), re.DOTALL)
				if result:
					uri = result.group(1).strip()
					result = uri.split('value="')
					if len(result)>1:
						uri = result[-1]
			
		else:
			uri = None
			movie = args[0].lower()
			imdb_id = args[1]
			uri = '/movies.php?list=search&search=%s' % imdb_id
			html = self.request(uri, headers=self.headers, cache=86400)
			pattern = 'id="tdmovies">\s*<a\s+href="([^"]+)">([^<]+).*?id="f7">(.*?)</TD>'
			def clean_title(title):
				title = title.strip()
				title = title.lower()
				return title
			for match in re.finditer(pattern, html, re.DOTALL):
				uri, title, extra = match.groups('')
				title = clean_title(title)
				if title == movie:
					break
			if uri is None: 
				return False
		return uri