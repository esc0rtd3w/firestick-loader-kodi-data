
import re
import urllib
from dudehere.routines import *
from dudehere.routines.plugin import log
from dudehere.routines.scrapers import CommonScraper, ScraperResult
QUALITY_MAP = {"HD": QUALITY.HD, "DVD": QUALITY.SD480, "LQ DVD": QUALITY.LOW}
class solarmovieScraper(CommonScraper):
	broken = False
	def __init__(self):
		self._settings = {}
		self.broken = 1
		self.service='solarmovie'
		self.name = 'solarmovie.is'
		self.referrer = 'http://www.solarmovie.fm'
		self.base_url = 'http://www.solarmovie.fm'
		self.ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
		self.USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
		self.headers = {'Accept-Language': 'en-US,en;q=0.8', 'Upgrade-Insecure-Requests': 1}
		self.get_debrid_hosts()
		
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'], args['year'])
		if uri:
			soup = self.request(uri, headers=self.headers, return_soup=True)
			results = self.process_results(soup)
		return self.get_response(results)
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('movie', args['title'], args['year'])
		if uri:
			html = self.request(uri, headers=self.headers)
			results = self.process_results(html)
		return self.get_response(results)
	
	def process_results(self, soup):
		results = []
		tables = soup.findAll('table', {"class": "movie_version"})
		for table in tables:
			host = table.find("span", {"class": "version_host"})
			if host:
				host = host.string
				if self.filter_host(host) is False: continue
				href = table.find('a')['href']
				quality = QUALITY.HD if 'quality_dvd' in str(table.find('td')) else QUALITY.SD480
				
				plugin.log(href)
			
		'''pattern = '<tr id="link_(\d+?)"(.+?)</tr>'
		for link in re.finditer(pattern, html, re.DOTALL):
			id, html = link.groups()
			host_name = re.search('<a href="/link/show/%s/">\s+(.+?)\s+</a>' % id, html, re.DOTALL)
			host_name = host_name.group(1)
			if self.filter_host(host_name):
				url = "%s:///link/play/%s/" % (self.service, id)
				result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
				
				quality = re.search('<td class="qualityCell js-format" style="text-transform: uppercase;">\s+(.+?)\s+</td>', html, re.DOTALL)
				if quality:
					quality = quality.group(1).upper()
					if quality in QUALITY_MAP.keys():
						result.quality = QUALITY_MAP[quality]

				results += [result]'''
		return results
	
	def get_resolved_url(self, uri):
		html = self.request(uri, headers=self.headers)
		iframe = re.search('<iframe (.+?)</iframe>', html, re.IGNORECASE|re.DOTALL)
		if iframe:
			html = iframe.group(1)
			match = re.search('src="(.+?)"', html, re.DOTALL|re.IGNORECASE)
			if match:
				raw_url = match.group(1)
				return self.do_urlresolver(raw_url)
		return None

		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			showname = self.url_friendly(args[0])
			season = args[1]
			episode = args[2]
			year = args[3]
			uri = "/tvshows/%s-season-%s-episode-%s-online.html" % (showname, season, episode)	
			return uri
		else:
			title = self.url_friendly(args[0])
			year = args[1]
			uri = "/watch-%s-%s.html" % (title, year)
			return uri