import urllib2, urllib
import socket
import json
from urllib2 import URLError, HTTPError
import re
import base64
import hashlib
import traceback
from dudehere.routines import *
from dudehere.routines import plugin
from BeautifulSoup import BeautifulSoup
try:
	from HTMLParser import HTMLParser
except ImportError:
	from html.parser import HTMLParser

_base_url = "http://www.imdb.com"
_user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
_accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
_headers = {"Host": "www.imdb.com", "User-Agent": _user_agent, "Accept": _accept}


DB_TYPE = 'sqlite'
DB_LOCATION = vfs.join('special://userdata', 'addon_data/script.module.dudehere.routines')
if not vfs.exists(DB_LOCATION): vfs.mkdir(DB_LOCATION)
DB_FILE = vfs.join(DB_LOCATION, 'imdb.db')
from dudehere.routines.database import SQLiteDatabase as DatabaseAPI

class MyDatabaseAPI(DatabaseAPI):
	def _initialize(self):
		import xbmcaddon
		root = xbmcaddon.Addon('script.module.dudehere.routines').getAddonInfo('path')
		schema_file = vfs.join(root, 'resources/database/imdb.schema.%s.sql' % self.db_type)

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


DB = MyDatabaseAPI(DB_FILE, version=DB_VERSION, connect=True, quiet=False)


def search_movie_genre(genre, page=None):
	genre = genre.lower()
	uri = '/search/title'
	if genre == 'documentary':
		params = {"title_type":"documentary", "sort": "moviemeter,asc"}
	else:
		params = {"genres": genre, "title_type":"feature", "sort": "moviemeter,asc"}
		
	if page is not None:
		params['start'] = (int(page) * 50) + 1
		
	return process_results(_call(uri, params, cache_limit=3600), 'movie')

def search_tv_genre(genre, page=None):
	genre = genre.lower().replace("-", "_")
	uri = '/search/title'
	params = {"genres": genre, "title_type":"tv_series,mini_series", "sort": "moviemeter,asc", "count": 50}
	if page is not None:
		params['start'] = (int(page) * 50) + 1
		
	return process_results(_call(uri, params, cache_limit=3600), 'tvshow')


def to_slug(title):
	title = title.strip()
	title = title.lower()
	title = re.sub('[^a-z0-9_]', '-', title)
	title = re.sub('--+', '-', title)
	return title




def process_results(html, media):
	results = []
	if html is False: return results
	
	from dudehere.routines.trakt import TraktAPI
	trakt = TraktAPI()
	soup = BeautifulSoup(html)
	movies = soup.findAll('div', {"class": "lister-item mode-advanced"})
	for movie in movies:
		imdb_id = movie.find('div', {"class": "ribbonize"})['data-tconst']
		record = trakt.get_metadata(media, imdb_id, None, None, None)
		if not record: continue
		meta = process_record(imdb_id, record, media)
		if not meta['title']: continue
		results.append(meta)
	return results	

def meta_map(path, object, default='', alt=''):
	try:
		if isinstance(path, list):
			for k in path:
				object = object[k]
		else:
			object = object[path]
			object = object if object is not None else default
		return object
	except:
		return default
def format_trailer(trailer_url):
	if not trailer_url: return trailer_url
	match = re.search('\?v=(.*)', trailer_url)
	if match:
		return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (match.group(1))	
		
def process_record(imdb_id, record, media):
	if media == 'movie':
		return record
	else:
		if 'trakt_id' in record: return record
		meta = {}
		meta['imdb_id'] = imdb_id
		meta['tvdb_id'] = meta_map(['ids', 'tvdb'], record)
		meta['tmdb_id'] = meta_map(['ids', 'tmdb'], record)
		meta['trakt_id'] = meta_map(['ids', 'trakt'], record)
		meta['slug'] = meta_map(['ids', 'slug'], record)
		meta['title'] = meta_map('title', record)
		meta['TVShowTitle'] = meta_map('title', record)
		meta['tvshowtitle'] = meta_map('title', record)
		meta['rating'] = meta_map('rating', record)
		meta['duration'] = meta_map('runtime', record)
		meta['plot'] = meta_map('overview', record)
		meta['mpaa'] = meta_map('certification', record)
		meta['premiered'] = meta_map('first_aired', record)
		meta['year'] = int(meta_map('year', record, default=0))
		meta['trailer'] = format_trailer(meta_map('trailer', record))
		meta['genre'] = meta_map('genres', record)
		meta['studio'] = meta_map('network', record)
		meta['status'] = meta_map('status', record)
		meta['cast'] = []
		meta['banner_url'] = meta_map(['images', 'thumb', 'full'], record)
		meta['cover_url'] = meta_map(['images', 'poster', 'full'], record)
		meta['backdrop_url'] = meta_map(['images', 'fanart', 'full'], record)
		meta['overlay'] = 6
		meta['playcount'] = 0
	return meta

def _cache_result(html, url, cache_limit=15):
	hash_id = hashlib.md5(url).hexdigest()
	if cache_limit > 0:
		if DB.db_type == 'mysql':
			SQL = "DELETE FROM cache WHERE unix_timestamp() - unix_timestamp(ts) > (60 * ?)"
		else:
			SQL = "DELETE FROM cache WHERE strftime('%s','now') -  strftime('%s',ts) > (60 * ?)"
		DB.execute(SQL, [cache_limit])
	SQL = "INSERT INTO cache(hash_id, url, results) VALUES(?,?,?)"
	DB.execute(SQL, [hash_id, url, base64.b64encode(html)])
	DB.commit()

def _get_cached_result(url, cache_limit=15):
		html = False
		if cache_limit > 0:
			if DB.db_type == 'mysql':
				SQL = "DELETE FROM cache WHERE unix_timestamp() - unix_timestamp(ts) > (60 * ?)"
			else:
				SQL = "DELETE FROM cache WHERE strftime('%s','now') -  strftime('%s',ts) > (60 * ?)"
			DB.execute(SQL, [cache_limit])
			DB.commit()
		hash_id = hashlib.md5(url).hexdigest()
		cache = DB.query("SELECT results FROM cache WHERE hash_id=?", [hash_id])
		if cache:
			html = base64.b64decode(cache[0])
		return html

def _call(uri, params=None, data=None, cache_limit=False, timeout=None, method=None):
		timeout = timeout if timeout is not None else 5
		json_data = json.dumps(data) if data else None

		url = '%s%s' % (_base_url, uri)
		if params is not None:
			url += '?' + urllib.urlencode(params)

		plugin.log(url)
		if cache_limit is not False:
			result = _get_cached_result(url, cache_limit)
			if result:
				response = result
				plugin.log("Returning cached results")
				return response
		
		while True:	
			try:
				request = urllib2.Request(url, data=json_data, headers=_headers)
				if method is not None:
					request.get_method = lambda: method.upper()
				f = urllib2.urlopen(request, timeout=timeout)
				result = f.read()
				response = result
				break
			except HTTPError as e:
				plugin.log(e, url)
				return False
			except URLError as e:
				plugin.log("%s: %s" % (e,url), LOG_LEVEL.VERBOSE)
				return False
			except socket.timeout as e:
				plugin.log("%s %s" % (e,url), LOG_LEVEL.VERBOSE)
				return False
		if cache_limit is not False:
			_cache_result(result, url, cache_limit)
		return response