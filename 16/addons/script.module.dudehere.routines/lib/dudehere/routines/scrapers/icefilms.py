import re
import urllib
import random
import urlparse
import hashlib
import zlib
import time
from urlparse import urljoin
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines.scrapers import CommonScraper, ScraperResult, NetLib

COOKIE_PATH = vfs.join(DATA_PATH,'cookies')
CACHE_PATH = vfs.join(DATA_PATH,'cache')

class icefilmsScraper(CommonScraper):
	def __init__(self):
		self._settings = {}
		self.service='icefilms'
		self.name = 'icefilms.info'
		self.base_url = 'http://www.icefilms.info'
		self.referrer = 'http://www.icefilms.info'
		self.referer  = '/membersonly/components/com_iceplayer/video.php?h=374&w=631&vid=%s&img='
		self.ajax_url = '/membersonly/components/com_iceplayer/video.phpAjaxResp.php?id=%s&s=%s&iqs=&url=&m=%s&cap=+&sec=%s&t=%s'
		self.get_debrid_hosts()
	
	def search_tvshow(self, args):
		self.domains = args['domains']
		results = []
		uri = "/tv/a-z/%s" % re.sub('^(A )|(An )|(The )', '', args['showname'], re.IGNORECASE)[0:1]
		html = self.request(uri)
		pattern = "<a href=/tv/series/(\d+?)/(\d+?)>%s \(%s\)</a>" % (args['showname'], args['year'])
		show = re.search(pattern, html)
		if show:
			uri = "/tv/series/%s/%s" % (show.group(1), show.group(2))
			html = self.request(uri, cache=86600)
			pattern = 'ip\.php\?v=(\d+?)&>%sx%s'  % (args['season'], str(args['episode']).zfill(2))
			match = re.search(pattern, html, re.DOTALL)
			if match:
				vid = match.group(1)
				results = self._get_sources(vid)
		return self.get_response(results)
	
	def search_movie(self, args):
		self.domains = args['domains']
		results = []
		uri = "/movies/a-z/%s" % re.sub('^(A )|(An )|(The )', '', args['title'], re.IGNORECASE)[0:1]
		html = self.request(uri)
		pattern = "<a href=/ip.php\?v=(\d+?)&>%s \(%s\)</a>" % (args['title'], args['year'])
		match = re.search(pattern, html)
		if match:
			vid = match.group(1)
			results = self._get_sources(vid)
		return self.get_response(results)
	
	def get_resolved_url(self, raw_url):
		uri, query = raw_url.split('?', 1)
		data = urlparse.parse_qs(query, True)
		uri += '?s=%s&t=%s&app_id=DHCR' % (data['id'][0], data['t'][0])
		referer = self.referer % (data['t'][0])
		try:
			ad_url = urllib.unquote(data['ad_url'][0])
			del data['ad_url']
		except:
			pass
		headers = {"Referer": referer}
		params = {}
		for key in data.keys():
			params[key] = data[key][0]
		html = self.request(uri, params, headers=headers)
		match = re.search('url=(.*)', html)
		if match:
			raw_url = urllib.unquote_plus(match.group(1))
			return self.do_urlresolver(raw_url)
		return ''
	
	def _get_sources(self, vid):
		uri = self.referer % vid
		results = []
		html = self.request(uri)
		
		match = re.search('lastChild\.value="([^"]+)"(?:\s*\+\s*"([^"]+))?', html)
		secret = ''.join(match.groups(''))

		match = re.search('"&t=([^"]+)', html)
		t = match.group(1)

		match = re.search('(?:\s+|,)s\s*=(\d+)', html)
		s_start = int(match.group(1))

		match = re.search('(?:\s+|,)m\s*=(\d+)', html)
		m_start = int(match.group(1))
		
		match = re.search('<iframe[^>]*src="([^"]+)', html)
		if match:
			ad_url = urllib.quote(match.group(1))
		else:
			ad_url = ''
		
		pattern = '<div class=ripdiv>(.*?)<\/div>'
		for block in re.findall(pattern, html, re.DOTALL):
			if 'HD 720p' in block:
				quality = QUALITY.HD720
			else: 
				quality = QUALITY.SD480
			pattern = "go\((\d+)\)'>([^:]+):\s+(.+?)<\/a>"
			for match in re.finditer(pattern, block, re.DOTALL):
				mirror_id, title, link = match.groups()
				host_name = self.get_provider(link)
				if self.filter_host(host_name):
					s = s_start + random.randint(3, 1000)
					m = m_start + random.randint(21, 1000)
					uri = self.ajax_url % (mirror_id, s, m, secret, t)
					url = "%s://%s" % (self.service, uri)
					result = ScraperResult(self.debrid_hosts, self.service, host_name, url, title)
					result.quality = quality
					results += [result]

		return results
		
	def get_provider(self, link):
		skey = self.strip_tags(link).lower()
		table = {
				'180upload': 		'180upload.com',
				'hugefiles':		'hugefiles.net',
				'clicknupload':		'clicknupload.com',
				'tusfiles':			'tusfiles.net',
				'xfileload':		'xfileload.com',
				'mightyupload':		'mightyupload.com',
				'movreel':			'movreel.com',
				'donevideo':		'donevideo.com',
				'vidplay':			'vidplay.net',
				'24uploading':		'24uploading.com',
				'xvidstage':		'xvidstage.com',
				'2shared':			'2shared.com',
				'upload':			'upload.af',
				'uploadx':			'uploadx.org',
				'kingfiles':		'kingfiles.net',
				'openload':			'openload.co',
				'uploadz':			'uploadz.co',
				'fileweed':			'fileweed.net',
				'filehoot':			'filehoot.com'
		}
		if skey in table.keys():
			return table[skey]
		else: 
			plugin.log("Icefilms unmatched host: %s" % skey)
		return None

	def strip_tags(self, html):
		import htmlentitydefs
		from HTMLParser import HTMLParser
		class HTMLTextExtractor(HTMLParser):
			def __init__(self):
				HTMLParser.__init__(self)
				self.result = [ ]
		
			def handle_data(self, d):
				self.result.append(d)
		
			def handle_charref(self, number):
				codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
				self.result.append(unichr(codepoint))
		
			def handle_entityref(self, name):
				codepoint = htmlentitydefs.name2codepoint[name]
				self.result.append(unichr(codepoint))
				
			def get_text(self):
				return u''.join(self.result)	
				
		s = HTMLTextExtractor()
		s.feed(html)
		return s.get_text()
	
	def request(self, uri, params=None, query=None, headers=None, timeout=None, cache=False, append_base=True, get_redirect=False, test_stream=False):
		if plugin.get_setting("overide_scraper_%s" % self.service) == 'true':
			self.base_url = plugin.get_setting("base_url_scraper_%s" % self.service)
			self.name = plugin.get_setting("name_scraper_%s" % self.service)
			self.timeout = plugin.get_setting("timeout_scraper_%s" % self.service)
		
		COOKIE_JAR = vfs.join(COOKIE_PATH,self.service + '.lwp')
		net = NetLib(cookie_file=COOKIE_JAR)
		net._cjf = COOKIE_JAR
		net.get_redirect = get_redirect
		net.test_stream = test_stream
		if headers:
			if 'Referer' not in headers.keys(): 
				headers['Referer'] = self.referrer
			if 'Accept' not in headers.keys():	
				headers['Accept'] = self.accept
			if 'User-Agent' not in headers.keys():
				headers['User-Agent'] = self.get_user_agent()
		else:
			headers = {
			'Referer': self.referrer,
			'Accept': self.accept,
			'User-Agent': self.user_agent
			}
		if query:
			uri += "?" + urllib.urlencode(query)
		if append_base:
			base_url = self.base_url
			url = urljoin(base_url, uri)
		else:
			url = uri
		if url is None: return ''	
		
		if timeout is None:
			timeout = self.timeout

		if cache:
			cache_hash = hashlib.md5(str(url) + str(params) if params else str(url)).hexdigest()
			cache_file = vfs.join(CACHE_PATH, cache_hash)
			if vfs.exists(cache_file):
				temp = vfs.read_file(cache_file + '.ts')
				
				if (time.time() - vfs.get_stat(cache_file).st_ctime()) / 60 > int(temp):
					vfs.rm(cache_file, quiet=True)
					vfs.rm(cache_file + '.ts', quiet=True)
				else:
					html = zlib.decompress(vfs.read_file(cache_file))
					return html
		if params:
			html = net.post(url, params, headers=headers, timeout=timeout)
		else:
			html = net.get(url, headers=headers, timeout=timeout)
		if cache:
			output = html.encode('utf-8') if type(html) == unicode else html
			vfs.write_file(cache_file, zlib.compress(output))
			vfs.write_file(cache_file+'.ts', str(cache))
		net.save_cookies(COOKIE_JAR)
		return html
		