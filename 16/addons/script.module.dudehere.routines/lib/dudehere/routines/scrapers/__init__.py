#!/usr/bin/python
# -*- coding: utf-8 -*-

'''*
	Copyright (C) 2015 DudeHere

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
*'''

import os
import sys
import re
import urllib
import urllib2
import zlib
import json
import time
import socket
import unicodedata
import xbmc
import xbmcgui
import xbmcaddon
from cgitb import html
try:
	import urlresolver
except:
	pass
import cookielib
import hashlib
import random
import requests
from Queue import Queue
from threading import Thread, Event
from urlparse import urljoin, urlparse
from dudehere.routines import *
from dudehere.routines.threadpool import ThreadPool
from dudehere.routines.network import Net, HttpResponse
from BeautifulSoup import BeautifulSoup
from dudehere.routines import cloudflare
from dudehere.routines import plugin
from dudehere.routines.plugin import ProgressBar

DECAY = 2
SCRAPER_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_PATH = vfs.join(DATA_PATH,'cookies')
CACHE_PATH = vfs.join(DATA_PATH,'cache')
if not vfs.exists(COOKIE_PATH): vfs.mkdir(COOKIE_PATH, recursive=True)
if not vfs.exists(CACHE_PATH): vfs.mkdir(CACHE_PATH, recursive=True)
sys.path.append(SCRAPER_DIR)
RD_HOSTS = []
if plugin.get_setting('database_type')=='1':
	DB_NAME = plugin.get_setting('database_mysql_name')
	DB_USER = plugin.get_setting('database_mysql_user')
	DB_PASS = plugin.get_setting('database_mysql_pass')
	DB_PORT = plugin.get_setting('database_mysql_port')
	DB_ADDRESS = plugin.get_setting('database_mysql_host')
	DB_TYPE = 'mysql'
	from dudehere.routines.database import MySQLDatabase as DatabaseAPI

else:
	DB_TYPE = 'sqlite'
	DB_FILE = xbmc.translatePath(plugin.get_setting('database_sqlite_file'))
	from dudehere.routines.database import SQLiteDatabase as DatabaseAPI

class MyDatabaseAPI(DatabaseAPI):
	def _initialize(self):
		root = xbmcaddon.Addon('script.module.dudehere.routines').getAddonInfo('path')
		schema_file = vfs.join(root, 'resources/database/schema.%s.sql' % self.db_type)
		if self.run_script(schema_file, commit=False):
			self.execute('DELETE FROM version WHERE 1')
			self.execute('INSERT INTO version(db_version) VALUES(?)', [self.db_version])
			self.commit()
	
	def do_init(self):
		do_init = True
		try:
			test = self.query("SELECT 1 FROM version WHERE db_version >= ?", [self.db_version], silent=True)
			if test:
				do_init = False
		except:
			do_init = True
		return do_init

if DB_TYPE == 'mysql':
	DB=MyDatabaseAPI(DB_ADDRESS, DB_NAME, DB_USER, DB_PASS, DB_PORT, version=DB_VERSION, connect=False)
else:
	DB = MyDatabaseAPI(DB_FILE, version=DB_VERSION, connect=False)

class NoRedirection(urllib2.HTTPErrorProcessor):
	def http_response(self, request, response):
		return response
	https_response = http_response

class NetLibError(Exception):
	pass

class NetLib(Net):
	timeout=1
	get_redirect = False
	test_stream = False
	def get(self, url, headers=None, timeout=1):
		self.timeout = timeout
		html = self.http_GET(url, headers=headers)
		return html
	
	def post(self, url, params, headers=None, timeout=1):
		self.timeout = timeout
		html = self.http_POST(url, params, headers=headers)
		return html
		
	def _fetch(self, url, form_data={}, headers={}, compression=True):
		encoding = ''
		req = urllib2.Request(url)
		if form_data:
			form_data = urllib.urlencode(form_data)
			req = urllib2.Request(url, form_data)
		req.add_header('User-Agent', self._user_agent)
		for k, v in headers.items():
			req.add_header(k, v)
		if compression:
			req.add_header('Accept-Encoding', 'gzip')
		try:
			if self.get_redirect:
				opener = urllib2.build_opener(NoRedirection)
				urllib2.install_opener(opener)
				response = urllib2.urlopen(req, timeout=self.timeout)
				if response.info().getheader('Refresh') is not None:
					refresh = response.info().getheader('Refresh')
					return refresh.split(';')[-1].split('url=')[-1]
				else:
					return response.info().getheader('Location')
			elif self.test_stream:
				response = urllib2.urlopen(req, timeout=self.timeout)
				return response.getcode() in [200, 206]
			else:
				response = urllib2.urlopen(req, timeout=self.timeout)
	
		except urllib2.HTTPError as e:
			if e.code == 503 and 'cf-browser-verification' in e.read():
				html = cloudflare.solve(url, self._cjf, self._user_agent)
				return html
			elif e.code == 404:
				plugin.log("Scraper-HTTP Error: %s %s" % (e.code, url))
				return ''
			else:
				plugin.log("Scraper-HTTP Error: %s %s" % (e.code, url))
				raise NetLibError("Scraper-HTTP Error")
				return ''
		except urllib2.URLError as e:
			plugin.log("Scraper-URL Error: %s %s " % (e, url))
			raise NetLibError("Scraper-URL Error")
			return ''
		except socket.timeout as e:
			plugin.log("Scraper-Timeout Error: %s %s" % (e, url))
			raise NetLibError("Scraper-Timeout Error")
			return ''
		except Exception as e:
			plugin.log("Scraper-Other Error: %s" % e)
			raise NetLibError("Scraper-Other Error")
			plugin.log(url)
			return ''
		try:
			html = HttpResponse(response).content
		except urllib2.URLError as e:
			plugin.log("Scraper-URL Error: %s" % e)
			plugin.log(url)
			raise NetLibError("Scraper-URL Error")
			return ''
		except socket.timeout as e:
			plugin.log("Scraper-Timeout Error: %s" % e)
			plugin.log(url)
			raise NetLibError("Scraper-Timeout Error")
			return ''
		except Exception as e:
			plugin.log("Scraper-Other Error: %s" % e)
			plugin.log(url)
			raise NetLibError("Scraper-Other Error")
			return ''
			
		return html

class ScraperResult():
	bitrate_color = plugin.get_setting('custom_color_bitrate') if plugin.get_setting('custom_color_bitrate') != '' else 'purple'
	hostname_color = plugin.get_setting('custom_color_hostname') if plugin.get_setting('custom_color_hostname') != '' else 'red'
	size_color = plugin.get_setting('custom_color_filesize') if plugin.get_setting('custom_color_filesize') != '' else 'blue'
	extension_color = plugin.get_setting('custom_color_extension') if plugin.get_setting('custom_color_extension') != '' else 'green'
	quality_color = plugin.get_setting('custom_color_quality') if plugin.get_setting('custom_color_quality') != '' else 'yellow'
	service_color = plugin.get_setting('custom_color_service') if plugin.get_setting('custom_color_service') != '' else 'white'
	debrid_color = plugin.get_setting('custom_color_debrid_color') if plugin.get_setting('custom_color_debrid_color') != '' else 'hotpink'
	x265_color = plugin.get_setting('custom_color_x265') if plugin.get_setting('custom_color_x265') != '' else 'chocolate'
	hc_color = plugin.get_setting('custom_color_hc') if plugin.get_setting('custom_color_hc') != '' else 'olive'
	
	host_cleaner = re.compile('[^a-z0-9\.]', re.IGNORECASE)
	
	def __init__(self, debrid_hosts, service, hostname, url, text=None):
		hostname = self.host_cleaner.sub('', str(hostname))
		if hostname.startswith('www.'):
			hostname = hostname.replace('www.', '')
		self.hostname = hostname
		self.service = service
		if text is not None:
			self.text = text.strip(' \t\n\r')
		else:
			self.text = text
		self.url = url
		self.bitrate = None
		self.size = None
		self.extension = None
		self.quality = QUALITY.UNKNOWN
		self.score = 0
		self.PB = False
		self.debrid = 0
		self.x265 = 0
		self.hc = 0
		self.alldebrid = 0
		self.realdebrid = 0
		self.rpnet = 0
		self.premiumize = 0
		self.debrid_flags = []
		if debrid_hosts:
			if 'ad' in debrid_hosts:
				if self.hostname in debrid_hosts['ad']:
					self.alldebrid = 1
					self.debrid_flags.append('AD')
	
			if 'rp' in debrid_hosts:
				if self.hostname in debrid_hosts['rp']:
					self.rpnet = 1
					self.debrid_flags.append('RPN')
	
			if 'rd' in debrid_hosts:
				if self.hostname in debrid_hosts['rd']:
					self.realdebrid = 1
					self.debrid_flags.append('RD')
	
			if 'pm' in debrid_hosts:
				if self.hostname in debrid_hosts['pm']:
					self.premiumize = 1
					self.debrid_flags.append('PM')
					
			if len(self.debrid_flags):
				self.debrid = 1

		if self.text is not None and re.search('([-_\s\.]?(x265)|(hevc)[-_\s\.])', self.text, re.IGNORECASE):
			self.x265 = 'x265'
		
		if self.text is not None and re.search('([-_\s\.]?(HC)[-_\s\.])', self.text, re.IGNORECASE):
			self.hc = 'HC'	
	
	def colorize(self, attrib, value):
		color = getattr(self, attrib+'_color')
		if attrib == 'bitrate':
			return "[COLOR %s]%s kb/s[/COLOR]" % (color, value)
		elif attrib == 'quality':
			quality = QUALITY.r_map[value]
			return "[COLOR %s]%s[/COLOR]" % (color, quality)
		elif attrib == 'size':
			size = self.format_size(value)
			return "[COLOR %s]%s[/COLOR]" % (color, size)
		elif attrib == 'extension':
			if value.lower() in ['avi', 'mkv', 'mp4', 'flv']:
				return "[COLOR %s]%s[/COLOR]" % (color, value)
			else:
				return False
		else:
			return "[COLOR %s]%s[/COLOR]" % (color, value)
	
	def format_size(self, size):
		size = int(size) / (1024 * 1024)
		if size > 2000:
			size = size / 1024
			unit = 'GB'
		else :
			unit = 'MB'
		size = "%s %s" % (size, unit)
		return size
		
	def ck(self, attrib):
		if getattr(self, attrib):
			attrib = self.colorize(attrib, getattr(self, attrib))
			if attrib:
				self.attributes.append(attrib)
		
	def format(self):
		self.attributes = []
		self.attributes.append(self.colorize('hostname', self.hostname))
		self.attributes.append(self.colorize('service', self.service))
		
		if self.debrid:
			self.attributes.append(self.colorize('debrid', ','.join(self.debrid_flags)))
			
		for foo in ['size', 'bitrate', 'extension', 'hc', 'x265', 'quality']:
			self.ck(foo)
		
		format = "[%s]: %s"	
		if self.text is None: self.text = self.hostname
		try:
			format = format % (' | '.join(self.attributes), self.text)
		except UnicodeEncodeError:
			for k in self.attributes:
				if isinstance(self.attributes[k], unicode):
					self.attributes[k] = self.attributes[k].encode('utf-8')
			format = format % (' | '.join(self.attributes), self.text)
		return format

	
	

class CommonScraper():
	USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
	ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	accept = ACCEPT
	user_agent = USER_AGENT
	HOST_COLOR = 'red'
	SIZE_COLOR = 'blue'
	EXTENSION_COLOR = 'green'
	QUALITY_COLOR = 'yellow'
	BITRATE_COLOR = 'purple'
	X265_COLOR = 'chocolate'
	HC_COLOR = 'olive'
	timeout = 5
	broken = False
	require_auth = False
	is_cachable = True
	host_cleaner = re.compile('[^a-z0-9\.]', re.IGNORECASE)
	debrid_hosts = False
	return_cached_torrents = True
	premiumize = False
	use_ssl = False
	skip_pretest = False
	session = False
	
	def __init__(self):
		pass
	
	def get_debrid_hosts(self):
		if self.debrid_hosts is False:
			try:
				self.debrid_hosts = plugin.load_data(vfs.join(DATA_PATH, 'debrid_hosts.cache'))
			except:
				self.debrid_hosts = {"pm": [], "rd": [], "ad": [], "rp": []}

	def get_user_agent(self):
		user_agent = plugin.get_setting('user_agent')
		try: agent_refresh_time = int(plugin.get_setting('agent_refresh_time'))
		except: agent_refresh_time = 0
		if not user_agent or agent_refresh_time < (time.time() - (7 * 24 * 60 * 60)):
			user_agent = self.generate_user_agent()
			plugin.set_setting('user_agent', user_agent)
			plugin.set_setting('agent_refresh_time', str(int(time.time())))
		return user_agent

	def generate_user_agent(self):
		BR_VERS = [
			['%s.0' % i for i in xrange(18, 43)],
			['41.0.2228.0', '41.0.2227.1', '41.0.2227.0', '41.0.2226.0', '40.0.2214.93', '37.0.2062.124'],
			['11.0'],
			['11.0']
		]
		WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
		FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
		RAND_UAS = [
			'Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
			'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
			'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko'
		]
		index = random.randrange(len(RAND_UAS))
		user_agent = RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES), br_ver=random.choice(BR_VERS[index]))
		
		return user_agent

	def get_property(self, k):
		p = xbmcgui.Window(10000).getProperty('GenericPlaybackService.' + k)
		if p == 'false': return False
		if p == 'true': return True
		return p
	
	def set_property(self, k, v):
		xbmcgui.Window(10000).setProperty('GenericPlaybackService.' + k, v)
	
	def clear_property(self, k):
		xbmcgui.Window(10000).clearProperty('GenericPlaybackService.' + k)

	def clean_hostname(self, hostname):
		return self.host_cleaner.sub('', hostname)
	
	def filter_host(self, host_name):
		if self.domains is None:
			return True
		if host_name in self.domains:
			return True
		return False
	
	def normalize(self, string):
		return unicodedata.normalize('NFKD', unicode(string)).encode('utf-8','ignore')
	
	def url_friendly(self, string, s='-'):
		if string.endswith('(US)'):
			string = string[0:len(string)-4]
		string = re.sub('([^\s\w]|_)+', '', string.lower())
		return string.replace(" ", s)
	
	def get_response(self, results):
		return {"service": self.service, "name": self.name, "count": len(results), "results": results}
	
	
	def do_urlresolver(self, raw_url):
		try:
			source = urlresolver.HostedMediaFile(url=raw_url)
			resolved_url = source.resolve() if source else None
			return resolved_url
		except Exception, e:
			plugin.log(e)
			plugin.raise_notify('UrlResolver Error.', str(e).replace(",", ''))
			return None

	def test_quality(self, string, default=QUALITY.UNKNOWN):
		if re.search('1080p', string, re.IGNORECASE): return QUALITY.HD1080
		if re.search('720p', string, re.IGNORECASE): return QUALITY.HD720
		if re.search('480p', string, re.IGNORECASE): return QUALITY.SD480
		if re.search('(320p)|(240p)', string, re.IGNORECASE): return QUALITY.LOW
		return default
	
	def test_gv_quality(self, stream_url, default=QUALITY.HIGH):
		if 'itag=18' in stream_url or '=m18' in stream_url or stream_url.endswith('m18'):
			return QUALITY.LOW
		elif 'itag=22' in stream_url or '=m22' in stream_url or stream_url.endswith('m22'):
			return QUALITY.HD720
		elif 'itag=34' in stream_url or '=m34' in stream_url or stream_url.endswith('m34'):
			return QUALITY.HIGH
		elif 'itag=35' in stream_url or '=m35' in stream_url or stream_url.endswith('m35'):
			return QUALITY.HIGH
		elif 'itag=37' in stream_url or '=m37' in stream_url or stream_url.endswith('m37'):
			return QUALITY.HD1080
		else:
			return default
	
	def test_width_quality(self, width):
		width = int(width)
		if width > 1280:
			return QUALITY.HD1080
		elif width > 800:
			return QUALITY.HD720
		elif width > 640:
			return QUALITY.HIGH
		elif width > 320:
			return QUALITY.SD480
		
		return QUALITY.LOW
	
	def test_height_quality(self, height):
		height = int(height)
		if height > 900:
			return QUALITY.HD1080
		if height > 700:
			return QUALITY.HD720
		if height > 500:
			return QUALITY.HIGH
		elif height > 320:
			return QUALITY.SD480
		return QUALITY.LOW
	
	def set_color(self, text, color):
		return "[COLOR %s]%s[/COLOR]" % (color, text)
	
	def format_tv_search(self, title, season, episode):
		return "%s S%02dE%02d" % (title, season, episode)
	
	def format_movie_search(self, title, year):
		return "%s %s" % (title, year)
	
	def format_size(self, size):
		size = int(size) / (1024 * 1024)
		if size > 2000:
			size = size / 1024
			unit = 'GB'
		else :
			unit = 'MB'
		size = "%s %s" % (size, unit)
		return size
		
	def get_embeded_url(self, url, user_agent=False, referer=False, cookies=False):
		encoded = "%s://%s" % (self.service, url)
		if user_agent or referer or cookies:
			encoded += '|'
			addons = []
			if user_agent:
				addons.append("User-Agent=%s" % user_agent)
			if referer:
				addons.append("Referer=%s" % urllib.quote(referer))
			if cookies:
				addons.append("Cookie=%s" % self.get_cookies())
			encoded += '&'.join(addons)
		return encoded
		
	def get_cookies(self):
		parsed_uri = urlparse( self.base_url )
		domain = '{uri.netloc}'.format(uri=parsed_uri)
		if domain.startswith('www'):
			domain=domain[3:]
		cj = cookielib.LWPCookieJar()  
		COOKIE_JAR = vfs.join(COOKIE_PATH,self.service + '.lwp')
		cj.load(COOKIE_JAR)
		cookies = []
		for cookie in cj:
			if domain == cookie.domain:
				cookies.append('%s=%s' % (cookie.name, cookie.value))
		return urllib.quote(';'.join(cookies))
		
	def get_domain_from_url(self, url):
		parsed_uri = urlparse( url )
		domain = '{uri.netloc}'.format(uri=parsed_uri)
		if domain.startswith('www'):
			domain=domain[4:]
		return domain	
	
	def get_file_from_url(self, url, clean=None):
		file = url.split('/')[-1]
		if clean is not None:
			file = re.sub(clean, '', file)
		return file

	def get_cached_response(self, url):
		cache_hash = hashlib.md5(str(url)).hexdigest()
		cache_file = vfs.join(CACHE_PATH, cache_hash)
		if vfs.exists(cache_file):
			temp = vfs.read_file(cache_file + '.ts')
			if (time.time() - vfs.get_stat(cache_file).st_ctime()) / 60 > int(temp):
				vfs.rm(cache_file, quiet=True)
				vfs.rm(cache_file + '.ts', quiet=True)
				return False
			else:
				html = zlib.decompress(vfs.read_file(cache_file))
				return html
		return False	
			

	def cache_response(self, url, html, cache):
		if html and cache:
			cache_hash = hashlib.md5(str(url)).hexdigest()
			cache_file = vfs.join(CACHE_PATH, cache_hash)
			output = html.encode('utf-8') if type(html) == unicode else html
			vfs.write_file(cache_file, zlib.compress(output))
			vfs.write_file(cache_file+'.ts', str(cache))
	
	def request(self, uri, params=None, query=None, headers=None, timeout=None, cache=False, return_soup=False, return_json=False, return_xml=False, append_base=True, get_redirect=False, test_stream=False):
		
		if plugin.get_setting("overide_scraper_%s" % self.service) == 'true':
			self.base_url = plugin.get_setting("base_url_scraper_%s" % self.service)
			self.name = plugin.get_setting("name_scraper_%s" % self.service)
			self.timeout = plugin.get_setting("timeout_scraper_%s" % self.service)
		
		SESSION_FILE = vfs.join(COOKIE_PATH,self.service + '.ssf')
		if self.session is False:
			#if vfs.exists(SESSION_FILE):
			#	self.session = plugin.load_data(SESSION_FILE, compress=True)
			#else:
			self.session = requests.Session()
			
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
		if test_stream:
			response = self.session.head(url, headers=headers, timeout=timeout)
			return response.status_code == requests.codes.ok
		
		if cache:
			cached_response = self.get_cached_response(url)
			if cached_response:
				if return_soup:
					return BeautifulSoup(cached_response)
				elif return_xml:
					import xml.etree.ElementTree as ET
					return ET.fromstring(cached_response)
				elif return_json:
					return json.loads(cached_response)
				else: 
					return cached_response
		
		if params:
			response = self.session.post(url, data=json.dumps(params), headers=headers, timeout=timeout)
		else:
			response = self.session.get(url, headers=headers, timeout=timeout)	
		#plugin.save_data(SESSION_FILE, self.session, compress=True)
		response.encoding = 'utf-8'
		#plugin.log(response.url)
		
		if response.status_code == requests.codes.ok:
			html = response.text
		elif response.status_code == 403 and '<title>Attention Required! | Cloudflare</title>' in response.text:
			plugin.log('protected by cloudflare')
			response.raise_for_status()
		elif response.status_code == 503 and 'cf-browser-verification' in response.text:
			COOKIE_FILE = vfs.join(COOKIE_PATH,self.service + '.lpw')
			html, cj = cloudflare.solve(url, COOKIE_FILE, self.user_agent)
			cookie_dict =  requests.utils.dict_from_cookiejar(cj)
			requests.utils.add_dict_to_cookiejar(self.session.cookies, cookie_dict)
			#plugin.save_data(SESSION_FILE, self.session, compress=True)
			
		else:
			plugin.log(response)
			plugin.log(response.headers)
			response.raise_for_status()	

		if cache:
			self.cache_response(url, html, cache)
			
		if return_soup:
			return BeautifulSoup(html)
		elif return_xml:
			import xml.etree.ElementTree as ET
			return ET.fromstring(html)
		elif return_json:
			return response.json()
		else: 
			return html
				
	def get_redirect(self, uri, append_base=True):

		headers = {
			'Referer': self.referrer,
			'Accept': self.accept,
			'User-Agent': self.get_user_agent()
		}
		if self.session is False:
			#SESSION_FILE = vfs.join(COOKIE_PATH,self.service + '.ssf')
			#if vfs.exists(SESSION_FILE):
			#	self.session = plugin.load_data(SESSION_FILE, compress=True)
			#else:
			self.session = requests.Session()
		if append_base:
			base_url = self.base_url
			url = urljoin(base_url, uri)
		else:
			url = uri
		response = self.session.head(url, timeout=self.timeout)
		if response.status_code == 302:
			for k in response.headers:
				if k.lower() == 'location' or k.lower() == 'content-location':
					return response.headers[k]
		else:	
			return False



class ScraperPool():
	filters = False
	skip_autoplay = False
	fallback = False
	PB = False
	return_cached_torrents = True
	settings_id = ADDON_ID
	
	def __init__(self, load = None, disable = None, cache_results=False, is_stream=False, return_cached_torrents=True, skip_states=False):
		self.threadpool_size = 5
		self.threadpool_timeout = 20
		self.cache_results = cache_results
		self._load_list = load
		self._disable_list = disable
		self.enabled_scrapers = 0
		self.active_scrapers = []
		self.supported_scrapers = []
		self._active_scrapers = []
		self.search_results = []
		self.__abort_event = Event()
		self.skip_states=skip_states
		self._caller = xbmc.getInfoLabel('Container.PluginName')
		
		self.return_cached_torrents = return_cached_torrents
		if is_stream:
			self.show_scraper_progress = False
		else:
			self.show_scraper_progress = plugin.get_setting('enable_scraper_progress') == 'true'
		
		self.is_stream = plugin.get_arg('media_type') == 'stream'
			
		self.skip_second_search = True
		expired = True
		self.filters = False
		self.cache_queue = Queue()
		if plugin.get_setting('enable_result_filters') == 'true':
			cache_file = vfs.join(DATA_PATH, 'filters.cache')
			if vfs.exists(cache_file):
				self.filters = plugin.load_data(cache_file)
		cache_file = vfs.join(DATA_PATH, 'debrid_hosts.cache')
		
		if vfs.exists(cache_file):
			timestamp = int(time.time())
			m_time = vfs.get_stat(cache_file).st_mtime()
			if (timestamp - m_time) < 86400: expired = False
		
		if expired:
			hosts = {"pm": [], "rd": [], "ad": [], "rp": []}
			net = Net()
			try:
				customer_id = xbmcaddon.Addon('script.module.urlresolver').getSetting('PremiumizeMeResolver_username')
				pin = xbmcaddon.Addon('script.module.urlresolver').getSetting('PremiumizeMeResolver_password')
				query = {"method": "hosterlist", "params[login]": customer_id, "params[pass]": pin}
				api_url = "http://api.premiumize.me/pm-api/v1.php?" + urllib.urlencode(query)
				response = net.http_GET(api_url).content
				data = json.loads(response)
				if 'result' in data:
					hosts['pm'] = data['result']['hosterlist']
			except: pass

			try:
				response = Net().http_GET('https://api.real-debrid.com/rest/1.0/hosts').content
				data = json.loads(response)
				hosts['rd'] = [r.strip() for r in data]
			except: pass
			
			try:
				response = Net().http_GET('http://alldebrid.com/api.php?action=get_host').content
				hosts['ad'] = [x.strip('"') for x in response.split(',\n')]
			except: pass
				
			try:
				response = Net().http_GET('http://premium.rpnet.biz/hoster2.json').content
				hosts['rp'] = json.loads(response)['supported']
			except: pass
			plugin.save_data(cache_file, hosts)
			self.debrid_hosts = hosts
		else:
			self.debrid_hosts = plugin.load_data(cache_file)
			plugin.set_property('debrid_hosts', str(plugin.pickle(self.debrid_hosts)))

		self._load_scrapers()
		self._enable_scrapers()
	
	def is_canceled(self):
		if self.show_scraper_progress and self.PB:
			test = self.PB.iscanceled()
			if test:
				self.__abort_event.set()
				plugin.log('Abort Event')
			return test
		else:
			return False
	
	def reinitialize_cache(self):
		vfs.rm(DB_FILE)
		DB=MyDatabaseAPI(DB_FILE, init_flag='database_sqlite_init.cache')
		DB._initialize()
		
	def get_host_list(self):
		DB.connect()
		hosts = DB.query_assoc("SELECT host, weight, disabled FROM host_weights ORDER BY weight, host ASC", force_double_array=True)
		DB.disconnect()
		return hosts
	
	def toggle_host(self, host):
		DB.connect()
		DB.execute("UPDATE host_weights SET disabled = (disabled * -1 + 1) WHERE host=?",  [host])
		DB.commit()
		DB.disconnect()
	
	def change_host_weight(self, host, weight):
		DB.connect()
		DB.execute("UPDATE host_weights SET weight=? WHERE host=?",  [weight, host])
		DB.commit()
		DB.disconnect()
	
	def read_scraper_states(self):
		DB.connect()
		results = DB.query_assoc("SELECT name, enabled FROM scraper_states ORDER BY name ASC")
		DB.disconnect()
		return results
	
	def toggle_scraper_state(self, name):
		DB.connect()
		DB.execute("UPDATE scraper_states SET enabled = (enabled * -1 + 1) WHERE name=?",  [name])
		DB.commit()
		DB.disconnect()
		
	def enable_scraper_state(self, name):
		DB.connect()
		DB.execute("UPDATE scraper_states SET enabled = 1 WHERE name=?",  [name])
		DB.commit()
		DB.disconnect()
	
	def disable_scraper_state(self, name):
		DB.connect()
		DB.execute("UPDATE scraper_states SET enabled = 0 WHERE name=?",  [name])
		DB.commit()
		DB.disconnect()		
		
	def set_scraper_state(self, name, state):
		DB.connect()
		state = 1 if state else 0
		DB.execute("UPDATE scraper_states SET enabled = ? WHERE name=?",  [state, name])
		DB.commit()
		DB.disconnect()
		
	def disable_all_scrapers(self):
		DB.connect()
		DB.execute("UPDATE scraper_states SET enabled=0")
		DB.commit()
		DB.disconnect()		
		
	def enable_all_scrapers(self):
		DB.connect()
		DB.execute("UPDATE scraper_states SET enabled=1")
		DB.commit()
		DB.disconnect()	
		
	def _load_scrapers(self):
		DB.connect()
		names = []
		count = 0
		for filename in sorted(os.listdir(SCRAPER_DIR)):
			if not re.search('(__)|(common\.py)|(example\.py)|(all\.py)', filename) and re.search('py$', filename):
				name = filename[0:len(filename)-3]
				self.supported_scrapers.append(name)
				names.append([name])
				if self._load_list is False: continue 	#should I even load anything?
				skip = False
				if self._load_list == 'all':
					pass 					#load all except explicitly disabled
				elif isinstance(self._load_list, list):
					skip = True				#load all in the supplied load list except explicitly disabled
					if name in self._load_list: skip = False
				else:
					skip = True				#load all enabled from db except explicitly disabled
					if DB.query("SELECT 1 FROM scraper_states WHERE enabled AND name=?", [name]): skip = False
						
				if self._disable_list is not None:
					if name in self._disable_list:
						skip = True			#now disable any scrapers in the disable list
				if skip is False:	
					classname = name+'Scraper'
					scraper = __import__(name, globals(), locals(), [classname], -1)
					klass = getattr(scraper, classname)
					scraper = klass()
					scraper.return_cached_torrents = self.return_cached_torrents
					self.put_scraper(scraper.service, scraper)
				count +=1
		if self.skip_states is False:
			if count > DB.query("SELECT count(1) FROM scraper_states")[0]:
				for name in names: DB.execute("INSERT INTO scraper_states(name) VALUES (?)", name)
				DB.commit()
		DB.disconnect()
				
	def get_scraper_by_name(self, name):
		try:
			index = self.active_scrapers.index(name)
			return self.get_scraper_by_index(index)
		except:
			return None
		
	def get_scraper_by_index(self, index):
		try:
			return self._active_scrapers[index]
		except:
			return None
	
	def _enable_scrapers(self):
		for index in range(0, len(self.active_scrapers)):
			self.enabled_scrapers += 1
		
	def put_scraper(self, service, scraper):
		if not scraper.broken:
			if plugin.get_setting('overide_scraper_' + service, addon_id="script.module.dudehere.routines") == "true":
				plugin.log(service)
				scraper.name = plugin.get_setting('name_scraper_' + service, addon_id="script.module.dudehere.routines")
				scraper.base_url = plugin.get_setting('base_url_scraper_' + service, addon_id="script.module.dudehere.routines")
				scraper.referrer = plugin.get_setting('base_url_scraper_' + service, addon_id="script.module.dudehere.routines")
				scraper.timeout = plugin.get_setting('timeout_scraper_' + service, addon_id="script.module.dudehere.routines")
				
			self.active_scrapers.append(service)
			self._active_scrapers.append(scraper)
			
	def queue_SQL(self, SQL, values=None):
		self.cache_queue.put((SQL, values))
		return True
	
	def _get_active_resolvers(self):
		self.domains = ['oboom.com']
		try:
			for universal in self.debrid_hosts:
				self.domains += filter(None, self.debrid_hosts[universal])
			for r in urlresolver.relevant_resolvers(include_universal=False):
				self.domains += r.domains
			
			self.domains = list(set(self.domains))
		except:
			self.domains = None
			
	def process_queue(self):
		if self.cache_results:	
			if DB_TYPE == 'mysql':
				TDB = MyDatabaseAPI(DB_ADDRESS, DB_NAME, DB_USER, DB_PASS, DB_PORT, version=DB_VERSION, connect=True)
			else:
				TDB = MyDatabaseAPI(DB_FILE, version=DB_VERSION, connect=True)
			TDB.execute("DELETE FROM search_results WHERE search_results.cache_id in (select cache_id FROM stale_cache)")
		while True:
			if self.is_canceled() or self.__abort_event.is_set():
				break
			SQL, values = self.cache_queue.get()
			if SQL == 'EOL':
				self.__abort_event.set()
				break
			if self.cache_results:
				TDB.execute_many(SQL, values)

			plugin.sleep(50)
			
		if self.cache_results:	
			TDB.commit()
			TDB.disconnect()
			del TDB
	
	def process_results(self, response):
		if 'count' in response and 'results' in response:
			results = response['results']
		else:
			return
		if self.show_scraper_progress and self.PB:
			self.PB.results += len(results)
			self.PB.next('Found [COLOR yellow]%s[/COLOR] sources from [B][COLOR lightgreen]%s[/COLOR][/B], %s total' % (response['count'], response['name'], self.PB.results))
		delta = time.time() - self._start_time
		plugin.log("Search returned %s links from %s in %s (s)" % (response['count'], response['name'], delta))
		if self.cache_results:
			values =[]
			for r in results:
				try:
					values += [(self.hashid, r.service, plugin.pickle(r))]
				except: pass
			SQL = "INSERT INTO search_results(hash, service, result) VALUES(?,?,?)"
			self.queue_SQL(SQL, values)
		self.search_results += results		

	def search_tvshows(self, showname, season, episode, year=None, imdb_id=None, tmdb_id=None, tvdb_id=None, return_sources=False):
		self._start_time = time.time()
		DB.connect()
		self.hashid = hashlib.md5(showname+str(season)+str(episode)).hexdigest()
		last_hash_id = plugin.get_property('last_hash_id')
		if self.hashid == last_hash_id or self.skip_autoplay:
			self.skip_autoplay = True
		else:
			self.skip_autoplay = False
			plugin.set_property('last_hash_id', self.hashid)
	
			
		self._get_active_resolvers()
		args = {"showname": showname, "season": season, "episode": episode, "year": year, "domains": self.domains, "imdb_id": imdb_id, "tmdb_id": tmdb_id, "tvdb_id": tvdb_id}
		workers = ThreadPool(self.threadpool_size)
		if self.show_scraper_progress:
			self.PB = ProgressBar()
			self.PB.new('Searching for TV Sources', self.enabled_scrapers)
			self.PB.results = 0
		#if self.cache_results:	
		self.processor = Thread(target=self.process_queue)
		self.processor.start()	
		self.threadpool_size = self.enabled_scrapers if self.threadpool_size == 0 else self.threadpool_size	
		for index in range(0, self.enabled_scrapers):
			if self.show_scraper_progress and self.PB:
				if self.PB.is_canceled(): break
				
			service = self.get_scraper_by_index(index).service
			if self.cache_results and self.get_scraper_by_index(index).is_cachable:
				SQL = "SELECT result FROM fresh_cache WHERE hash=? AND service=?"
				results = DB.query(SQL, [self.hashid, service], force_double_array=True)
				cached = [plugin.unpickle(str(r[0])) for r in results]
			else:
				cached = False
			if cached:
				number = len(cached)
				plugin.log("Search returned %s cached links from %s" % (number, service))
				if self.show_scraper_progress and self.PB:
					self.PB.results += number
					self.PB.next('Found [COLOR yellow]%s[/COLOR] cached sources (%s total)' % (number, self.PB.results))
				self.search_results += cached
			else:
				if 'search_tvshow' in dir(self.get_scraper_by_index(index)):
					if self.cache_results and self.get_scraper_by_index(index).is_cachable and self.hashid == last_hash_id and self.skip_second_search:
						continue
					if self.get_scraper_by_index(index).require_auth and (plugin.get_setting(service + '_username', self.settings_id ) == '' or plugin.get_setting(service + '_password', self.settings_id ) == ''): 
						continue
					self.get_scraper_by_index(index)._PB = self.PB
					self.get_scraper_by_index(index).is_canceled = self.is_canceled
					workers.queueTask(self.get_scraper_by_index(index).search_tvshow, args=args, taskCallback=self.process_results)
		workers.joinAll()
		time.time() - self._start_time
		resolved_url = None
		#if self.cache_results:
		self.queue_SQL('EOL')
		DB.disconnect()
		
		if return_sources:
			return self.process_sources(self)
		else:
			raw_url, autoplay =  self.select_stream()
			if raw_url is False and self.fallback:
				plugin.log('No sources found, attempting full scraper set', 1)
				self._load_list = 'all'
				self._disable_list = None
				self.enabled_scrapers = 0
				self.active_scrapers = []
				self.supported_scrapers = []
				self._active_scrapers = []
				self._load_scrapers()
				self._enable_scrapers()
				self.search_results = []
				self.fallback = False
				self.skip_autoplay = True
				plugin.clear_property('last_hash_id')
				self.settings_id = 'plugin.video.theroyalwe'
				self.get_scraper_by_name('furk').username = plugin.get_setting('furk_username', self.settings_id )
				self.get_scraper_by_name('furk').password = plugin.get_setting('furk_password', self.settings_id )
				
				self.get_scraper_by_name('alluc_api').username = plugin.get_setting('alluc_api_username', self.settings_id )
				self.get_scraper_by_name('alluc_api').password = plugin.get_setting('alluc_api_password', self.settings_id )
				
				self.search_tvshows(showname, season, episode, year=year, imdb_id=imdb_id, tmdb_id=tmdb_id, tvdb_id=tvdb_id)
			if raw_url:
				resolved_url = self.resolve_url(raw_url,autoplay)
			return resolved_url	
	
	def search_movies(self, title, year, imdb_id=None, tmdb_id=None, return_sources=False):
		self._start_time = time.time()
		DB.connect()
		self.hashid = hashlib.md5(title+str(year)).hexdigest()
		last_hash_id = plugin.get_property('last_hash_id')
		if self.hashid == last_hash_id:
			self.skip_autoplay = True
		else:
			self.skip_autoplay = False
			plugin.set_property('last_hash_id', self.hashid)
		
		self._get_active_resolvers()
		args = {"title": title, "year": year, "domains": self.domains, "imdb_id": imdb_id, "tmdb_id": tmdb_id}
		workers = ThreadPool(self.threadpool_size)
		if self.show_scraper_progress:
			self.PB = ProgressBar()
			self.PB.new('Searching for Movie Sources', self.enabled_scrapers)
			self.PB.results = 0
		if self.cache_results:
			self.processor = Thread(target=self.process_queue)
			self.processor.start()	
		self.threadpool_size = self.enabled_scrapers if self.threadpool_size == 0 else self.threadpool_size	
		for index in range(0, self.enabled_scrapers):
			if self.show_scraper_progress and self.PB:
				if self.PB.is_canceled(): break
			service = self.get_scraper_by_index(index).service
			if self.cache_results:
				SQL = "SELECT result FROM fresh_cache WHERE hash=? AND service=?"
				results = DB.query(SQL, [self.hashid, service], force_double_array=True)
				cached = [plugin.unpickle(str(r[0])) for r in results]
			else:
				cached = False	
			if cached:
				number = len(cached)
				plugin.log("Search returned %s cached links from %s" % (number, service))
				if self.show_scraper_progress and self.PB:
					self.PB.results += number
					self.PB.next('Found [COLOR yellow]%s[/COLOR] cached sources (%s total)' % (number, self.PB.results))
				self.search_results += cached
			else:
				if 'search_movie' in dir(self.get_scraper_by_index(index)):
					if self.get_scraper_by_index(index).require_auth and (plugin.get_setting(service + '_username', self.settings_id ) == '' or plugin.get_setting(service + '_password', self.settings_id ) == ''): 
						continue
					if self.get_scraper_by_index(index).require_auth and (plugin.get_setting(service + '_username', self.settings_id ) == '' or plugin.get_setting(service + '_password', self.settings_id ) == ''): 
						continue
					self.get_scraper_by_index(index)._PB = self.PB
					self.get_scraper_by_index(index).is_canceled = self.is_canceled
					workers.queueTask(self.get_scraper_by_index(index).search_movie, args=args, taskCallback=self.process_results)

		workers.joinAll()
		resolved_url = None
		if self.cache_results:
			self.queue_SQL('EOL')
		DB.disconnect()
		if return_sources:
			return self.process_sources(self)
		else:
			raw_url, autoplay =  self.select_stream()
			if raw_url is False and self.fallback:
				plugin.log('No sources found, attempting full scraper set', 1)
				self._load_list = 'all'
				self._disable_list = None
				self.enabled_scrapers = 0
				self.active_scrapers = []
				self.supported_scrapers = []
				self._active_scrapers = []
				self._load_scrapers()
				self._enable_scrapers()
				self.search_results = []
				self.fallback = False
				self.skip_autoplay = True
				plugin.clear_property('last_hash_id')
				self.settings_id = 'plugin.video.theroyalwe'
				self.get_scraper_by_name('furk').username = plugin.get_setting('furk_username', self.settings_id )
				self.get_scraper_by_name('furk').password = plugin.get_setting('furk_password', self.settings_id )
				
				self.get_scraper_by_name('alluc_api').username = plugin.get_setting('alluc_api_username', self.settings_id )
				self.get_scraper_by_name('alluc_api').password = plugin.get_setting('alluc_api_password', self.settings_id )
				self.search_movies(title, year, imdb_id=imdb_id, tmdb_id=tmdb_id)
			if raw_url:
				resolved_url = self.resolve_url(raw_url,autoplay)
			return resolved_url
		
	def process_sources(self, sort=True):
		DB.connect()
		streams = []
		options = []
		disabled = []
		rankings = {}
		if self.show_scraper_progress and self.PB:
			self.PB.update_subheading('Processing results...', percent=100)
			
		
		
		def get_rank(hostname):
			try:
				return rankings[hostname]
			except:
				return 0

		if plugin.get_setting('enable_result_sorting') == 'true' and plugin.get_setting('custom_result_sorting') == '1':
			def sort_streams(record):
				if isinstance(record, dict):
					debrid = record['debrid']
					rank = get_rank(record['host'])
					hostname = record['host']
					quality = record['quality']
				elif isinstance(record, int) or isinstance(record, str):
					return (0,1000, 0,'')
				else:
					debrid = record.debrid
					rank = get_rank(record.hostname)
					hostname = record.hostname
					quality = record.quality
				return (quality, rank, debrid, hostname)
				
		elif plugin.get_setting('enable_result_sorting') == 'true' and plugin.get_setting('custom_result_sorting') == '2':
			def sort_streams(record):
				if isinstance(record, dict):
					debrid = record['debrid']
					rank = get_rank(record['host'])
					hostname = record['host']
					quality = record['quality']
				elif isinstance(record, int) or isinstance(record, str):
					return (0,1000, 0,'')
				else:
					debrid = record.debrid
					rank = get_rank(record.hostname)
					hostname = record.hostname
					quality = record.quality
				return (debrid, rank, quality, hostname)
		elif plugin.get_setting('enable_result_sorting') == 'true' and plugin.get_setting('custom_result_sorting') == '0':
			def sort_streams(record):
				if isinstance(record, dict):
					rank = get_rank(record['host'])
					hostname = record['host']
					quality = record['quality']
				elif isinstance(record, int) or isinstance(record, str):
					return (0,0,'')
				else:
					rank = get_rank(record.hostname)
					hostname = record.hostname
					quality = record.quality
				return (quality, rank, hostname)
		
		if plugin.get_setting('enable_result_sorting') == 'true':
			rows = DB.query("SELECT host, rank FROM host_ranks", force_double_array=True)
			for r in rows: rankings[r[0]] = r[1]
			rows = DB.query("SELECT host FROM host_weights WHERE disabled=1", force_double_array=True)
			disabled = [r[0] for r in rows]
			self.search_results.sort(reverse=True, key=lambda k: sort_streams(k))
		hosts = []
		for result in self.search_results:
			if isinstance(result, int) or isinstance(result, str): continue
			elif isinstance(result, dict):
				display = result['title']
				url = result['url']
				hostname = result['host']
				service = result['service']
				quality = result['quality']
				alldebrid = result['alldebrid']
				realdebrid = result['realdebrid']
				rpnet = result['rpnet']
				premiumize = result['premiumize']
				x265 = result['x265']
			else:
				try:
					display = result.format()
					url = result.url
					hostname = result.hostname
					service = result.service
					quality = result.quality
					alldebrid = result.alldebrid
					realdebrid = result.realdebrid
					rpnet = result.rpnet
					premiumize = result.premiumize
					x265 = result.x265
				except Exception, e:
					plugin.log("Sort Error: %s" % str(e))
					continue

			if hostname in disabled:
				continue
			
			if self.filters:
				if QUALITY.r_map[quality] not in self.filters: continue
				
				if x265:
					if 'x265' not in self.filters: continue
				
				if realdebrid:
					if 'RealDebrid' not in self.filters:
						if not alldebrid and not rpnet and not premiumize: continue
				
				if alldebrid:
					if 'AllDebrid' not in self.filters:
						if not realdebrid and not rpnet and not premiumize: continue
						
				if rpnet:
					if 'Premiumize.ME' not in self.filters:
						if not realdebrid and not alldebrid and not premiumize: continue
				
				if premiumize:
					if 'RPNET' not in self.filters:
						if not realdebrid and not alldebrid and not rpnet: continue		
			
			hosts += [[hostname]]
			streams += [display]
			options += [url]
		if DB_TYPE == 'mysql':
			SQL = "INSERT IGNORE INTO host_weights(host) VALUES(?)"
		else:
			SQL = "INSERT INTO host_weights(host) VALUES(?)"	
		DB.execute_many(SQL, hosts)
		DB.commit()
		DB.disconnect()
		return streams, options, self.search_results
	
	def select_stream(self, sort=True):
		if 'transmogrify' in plugin.mode: self.skip_autoplay = True
		streams, options, results = self.process_sources(sort)
		if plugin.get_setting('enable_autoplay') == 'true' and self.skip_autoplay is False:
			resolved_url = self.attempt_autoplay(options, results)
			if resolved_url:
				plugin.log("Autoplay: %s" % resolved_url)
				return resolved_url, True
			
		if self.PB: self.PB.close()
		if len(streams) == 0:
			if self.fallback is False:
				plugin.raise_notify('No results found.', 'No results, try changing your scraper set.')
			return False, False

		if 'Custom Dialog' in plugin.get_setting('source_selection_mode') and self.is_stream is False:
			skin_path = plugin.get_addon('script.module.dudehere.routines').getAddonInfo('path')
			if plugin.get_setting('source_selection_mode') == 'Custom Dialog 2':
				from dudehere.routines.windows.stream_select import StreamSelect2 as StreamSelect
				LI = StreamSelect("stream_select2.xml", skin_path)
			else:
				from dudehere.routines.windows.stream_select import StreamSelect
				LI = StreamSelect("stream_select.xml", skin_path)
			LI.streams = streams
			LI.results = results
			LI.options = options
			LI.doModal()
			select = LI.choice
			del LI
		elif plugin.get_setting('source_selection_mode') == 'Redbeard Dialog' and self.is_stream is False:
			from dudehere.routines.windows.stream_select import StreamSelect2 as StreamSelect
			LI = StreamSelect("redbeard_stream_select.xml", ROOT_PATH)
			LI.streams = streams
			LI.results = results
			LI.options = options
			LI.doModal()
			select = LI.choice
			del LI	
		else:	
			dialog = xbmcgui.Dialog()
			select = dialog.select("Select a stream", streams)
		if select < 0:
			return False, False
		if isinstance(results[select], dict):
			self.hostname = results[select]['host']
		else:
			self.hostname = results[select].hostname
			service = results[select].service
		self.log_attempt(service, self.hostname)
		return options[select], False
	
	def log_attempt(self, service, hostname):
		plugin.log("Attempting: %s %s" % (service, hostname))
		DB.connect()
		DB.execute("INSERT INTO host_stats(service, host) VALUES(?,?)", [service, hostname])
		DB.commit()
		attempt_id = DB.lastrowid
		DB.disconnect()
		plugin.set_property("attempt.id", attempt_id)
	
	def attempt_autoplay(self, options, results):
		if len(options) == 0: return False
		attempts = int(plugin.get_setting('autoplay_attempts'))
		for attempt in xrange(attempts):
			raw_url = options[attempt]
			result = results[attempt]
			if isinstance(result, dict):
				hostname = result['host']
			else:
				hostname = result.hostname
			self.hostname=hostname
			
			if self.show_scraper_progress and self.PB:
				self.PB.update_subheading('AutoPlay [COLOR yellow]%s[/COLOR]: [B][COLOR lightgreen]%s[/COLOR][/B]' % (attempt+1, hostname), percent=100)
			test = re.search("^(.+?)(://)(.+?)$", raw_url)
			service = test.group(1)
			self.log_attempt(service, hostname)
			resolved_url = self.resolve_url(raw_url)
			if resolved_url is None: continue
			if 'urlresolver.plugnplay.interfaces.unresolvable' not in str(resolved_url):
				if hostname in ['furk.net', 'transmogrified', 'VideoLibrary', 'local']:
					if self.PB: self.PB.close()
					return resolved_url
				test = self.test_stream(service, resolved_url)
				if test:
					if self.PB: self.PB.close()
					return resolved_url
	
		return False
	
	
	def test_stream(self, service, resolved_url):
		timeout = float(plugin.get_setting('test_stream_timeout')) if plugin.get_setting('test_stream_timeout') else 5
		test = self.get_scraper_by_name(service).request(resolved_url, append_base=False, test_stream=True, timeout=timeout)
		if test:
			return True
		return False
	
	def resolve_url(self, encoded_url, autoplay=False):
		if isinstance(encoded_url, tuple):
			(encoded_url, autoplay) = encoded_url

		test = re.search("^(.+?)(://)(.+?)$", encoded_url)
		scraper = test.group(1)
		raw_url = test.group(3)
		if scraper.startswith('http') or autoplay: return encoded_url

		if 'get_resolved_url' in dir(self.get_scraper_by_name(scraper)):
			resolved_url = self.get_scraper_by_name(scraper).get_resolved_url(raw_url)
			return resolved_url
		else:
			return self.do_urlresolver(raw_url)
		
	def do_urlresolver(self, raw_url):
		try:
			source = urlresolver.HostedMediaFile(url=raw_url)
			resolved_url = source.resolve() if source else None
			return resolved_url
		except Exception, e:
			plugin.log(e)
			plugin.raise_notify('UrlResolver Error.', str(e).replace(",", ''))
			return None	

