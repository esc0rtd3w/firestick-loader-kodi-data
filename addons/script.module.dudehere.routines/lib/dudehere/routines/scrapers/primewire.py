import re
import urllib
from dudehere.routines import *
from dudehere.routines.scrapers import CommonScraper, ScraperResult



class primewireScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='primewire'
		self.name = 'primewire'
		self.referrer = 'http://primewire.ag'
		self.base_url = 'http://primewire.ag'
		self.get_debrid_hosts()

	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('tvshow', args['showname'], args['season'], args['episode'],args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html)
		return self.get_response(results)
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = self.prepair_query('movie', args['title'], args['year'])
		if uri:
			html = self.request(uri)
			results = self.process_results(html)
		return self.get_response(results)
	
	def process_results(self, html):
		results = []
		container_pattern = r'<table[^>]+class="movie_version[ "][^>]*>(.*?)</table>'
		item_pattern = (
			r'quality_(?!sponsored|unknown)([^>]*)></span>.*?'
			r'url=([^&]+)&(?:amp;)?domain=([^&]+)&(?:amp;)?(.*?)'
			r'"version_veiws"> ([\d]+) views</'
		)
		for container in re.finditer(container_pattern, html, re.DOTALL | re.IGNORECASE):
			for i, source in enumerate(re.finditer(item_pattern, container.group(1), re.DOTALL)):
				qual, url, host, parts, views = source.groups()
				if host == 'ZnJhbWVndGZv': continue
				host_name = host.decode('base-64')
				if self.filter_host(host_name):
					url = "%s://%s" % (self.service, url.decode('base-64'))
					result = ScraperResult(self.debrid_hosts, self.service, host_name, url)
					if qual == 'dvd':
						result.quality = QUALITY.SD480
					else:
						result.quality = QUALITY.LOW
					results += [result]
		return results
	
		
	def prepair_query(self, media, *args, **kwards):
		if media == 'tvshow':
			uri = '/index.php?'
			query = {"search_keywords": args[0], "year": args[3], "search_section": 2}
			uri += urllib.urlencode(query)
			html = self.request(uri, timeout=4)
			match = re.search('input type="hidden" name="key" value="([0-9a-f]*)"', html)
			if match:
				key = match.group(1)
				uri += '&key=' + key
				html = self.request(uri, timeout=3)
				pattern = r'class="index_item.+?href="(.+?)" title="Watch (.+?)"?\(?([0-9]{4})?\)?"?>'
				for match in re.finditer(pattern, html):
					uri, title, year = match.groups('')
					title = title.strip()
					if title.lower() == args[0].lower() and int(year) == int(args[3]):
						match = re.search('watch-(\d+?)-', uri)
						if match:
							uri = '/tv-%s-%s/season-%s-episode-%s' % (match.group(1), title.replace(' ', '-'), args[1], args[2])
							return uri
			return False
		else:
			uri = '/index.php?'
			query = {"search_keywords": args[0], "year": args[1], "search_section": 1}
			uri += urllib.urlencode(query)
			html = self.request(uri, timeout=4)
			match = re.search('input type="hidden" name="key" value="([0-9a-f]*)"', html)
			if match:
				key = match.group(1)
				uri += '&key=' + key
				html = self.request(uri, timeout=3)
				pattern = r'class="index_item.+?href="(.+?)" title="Watch (.+?)"?\(?([0-9]{4})?\)?"?>'
				for match in re.finditer(pattern, html):
					uri, title, year = match.groups('')
					title = title.strip()
					if title.lower() == args[0].lower() and int(year) == int(args[1]):
						return uri
			return False