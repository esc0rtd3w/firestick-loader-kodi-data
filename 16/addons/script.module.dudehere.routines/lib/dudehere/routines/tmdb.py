import re
import json
import urllib
import unicodedata
from dudehere.routines import *
from dudehere.routines.omdbapi import OMDBapi
from dudehere.routines.vfs import VFSClass
from dudehere.routines.database import SQLiteDatabase as DatabaseAPI
from metahandler.TMDB import TMDB
MOVIE_GENRES =  enum(
		ACTION = 28,
		ADVENTURE = 12,
		ANIMATION = 16,
		COMEDY = 35,
		CRIME = 80,
		DOCUMENTARY = 99,
		DRAMA = 18,
		FAMILY = 10751,
		FANTASY = 14,
		HISTORY = 36,
		HORROR = 27,
		MUSIC = 10402,
		MYSTERY = 9648,
		ROMANCE = 10749,
		SCIFI = 878,
		THRILLER = 53,
		WAR = 10752,
		WESTERN = 37
)

TV_GENRES =  enum(
		ACTION = 10759,
		ADVENTURE = 10759,
		ANIMATION = 16,
		COMEDY = 35,
		DOCUMENTARY = 99,
		DRAMA = 18,
		EDUCATION = 10761,
		FAMILY = 10751,
		FANTASY = 10765,
		KIDS = 10762,
		HISTORY = 36,
		MYSTERY = 9648,
		NEWS = 10763,
		POLITICS = 10768,
		REALITY = 10764,
		SCIFI = 10765,
		WAR = 10768,
		WESTERN = 37
)

TV_NETWORK_TABLE = {
	'A&E': '129|567|891',
	'ABC': '2|167|279|396',
	'AMC': '174',
	'Animal Planet': '91',
	'BBC': '3|4|7|271|126|100|27|459',
	'BET': '24',
	'Bravo': '312|485',
	'CBS': '16',
	'CMT': '85|377',
	'Comedy Central': '102|278',
	'Discovery Channel': '10|22|106',
	'Disney Channel': '281',
	'DIY Network': '625',
	'ESPN': '29',
	'FX': '88',
	'Fox': '303|961',
	'Game Show Network': '280',
	'HBO': '49',
	'HGTV': '210|482',
	'Hallmark Channel': '384',
	'IFC': '124',
	'ION Television': '293',
	'Lifetime Television': '34',
	'MSNBC': '37',
	'MTV': '17|33|295|488',
	'NBC': '6|582',
	'Netflix': '213',
	'Nick Jr.': '35|208|889',
	'Nickelodeon': '13|474|794|978',
	'Oxygen': '132',
	'PBS': '14|122|305',
	'Starz': '318',
	'Syfy': '77',
	'TBS': '49',
	'TV Land': '397',
	'The WB': '21|292',
	'TLC': '84',
	'TNT': '613',
	'Travel Channel': '209',
	'The History Channel': '238|560|893|894',
	'USA Network': '30',
	'VH1': '158',
}

vfs = VFSClass()
omdb = OMDBapi()

class MyDatabaseAPI(DatabaseAPI):
	def _initialize(self):
		do_init = True
		try:
			test = self.query("SELECT 1 FROM version WHERE db_version >= ?", [self.db_version])
			if test:
				do_init = False
		except:
			do_init = True
		if do_init:
			import xbmcaddon
			root = xbmcaddon.Addon('script.module.dudehere.routines').getAddonInfo('path')
			schema = vfs.join(root, 'resources/database/trakt.schema.sql')
			if vfs.exists(schema):
				full_sql = vfs.read_file(schema)
				sql_stmts = full_sql.split(';')
				for SQL in sql_stmts:
					if SQL is not None and len(SQL.strip()) > 0:
						self.execute(SQL)
						print SQL
				self.commit()
				self.execute('INSERT OR REPLACE INTO version(db_version) VALUES(?)', [self.db_version])
				self.commit()
DB_LOCATION = vfs.join('special://userdata', 'addon_data/script.module.dudehere.routines')
if not vfs.exists(DB_LOCATION):
	vfs.mkdir(DB_LOCATION)
DB_FILE = vfs.join('special://userdata', 'addon_data/script.module.dudehere.routines/trakt.db')
DB = MyDatabaseAPI(DB_FILE, init_flag='database_sqlite_init.trakt', version_flag='database_sqlite_version.trakt', version=4, connect=True)

backdrop_sizes = ["w300","w780","w1280","original"]
logo_sizes = ["w45","w92","w154","w185","w300","w500","original"]
poster_sizes = ["w92","w154","w185","w342","w500","w780","original"]
profile_sizes = ["w45","w185","h632","original"]
still_sizes = ["w92","w185","w300","original"
			]
class TMDB_API():
	api_key = ADDON.get_setting('tmdb_key')
	def __init__(self):
		if self.api_key == 'dude':
			temp = vfs.read_file("special://home/addons/metadata.themoviedb.org/tmdb.xml")
			match = re.search('api_key=([^&]+)', temp)
			if match:
				self.api_key = match.group(1)
				ADDON.set_setting('tmdb_key', self.api_key)
				
	
	def normalize(self, string):
		if isinstance(string, (str, unicode)):
			return string.encode('utf-8','replace')
		else:
			return string
	
	def get_today(self):
		from datetime import date
		d = date.today()
		return str(d.strftime("%Y-%m-%d"))
		
	def resolve_imdb_id(self, title, year, media, tmdb_id='', trakt_id=''):
		imdb_id = None
		try:
			id = DB.query("SELECT imdb_id FROM id_cache WHERE title=? AND media=? AND year=?", [title, media, year])
			if id:
				imdb_id = id[0]
			else:
				imdb_id = omdb.query_id(title, year, media)
				if imdb_id is not None:
					DB.execute("INSERT INTO id_cache(title, year, media, imdb_id, tmdb_id, trakt_id) VALUES(?,?,?,?,?,?)", [title, year, media, imdb_id, tmdb_id, trakt_id])
					DB.commit()
		except Exception, e:
			ADDON.log(e)
		return imdb_id
	
	def lookup(self, media, id):
		if media=='movie':
			base_uri = 'movie/%s' % id
			record = self.request(base_uri)
		metadata = self.process_record(record, media)	
		return metadata
	
	def get_popular_shows(self, page=1):
		base_uri = "tv/popular"
		query = {"page": page}
		return self.request(base_uri, urllib.urlencode(query))
	
	def get_latest_shows(self, page=1):
		base_uri = "discover/tv"
		query = {"page": page, "sort_by": "first_air_date.desc", "first_air_date.lte": self.get_today()}
		return self.request(base_uri, urllib.urlencode(query))
	
	def get_top_rated_shows(self, page=1):
		base_uri = "tv/top_rated"
		query = {"page": page}
		return self.request(base_uri, urllib.urlencode(query))
	
	def shows_airing_soon(self, page=1):
		base_uri = "tv/on_the_air"
		query = {"page": page}
		return self.request(base_uri, urllib.urlencode(query))
	
	def shows_airing_today(self, page=1):
		base_uri = "tv/airing_today"
		query = {"page": page, "primary_release_date.lte": self.get_today()}
		return self.request(base_uri, urllib.urlencode(query))
	
	def get_latest_movies(self, page=1):
		base_uri = "discover/movie"
		query = {"page": page, "sort_by": "primary_release_date.desc", "primary_release_date.lte": self.get_today()}
		return self.request(base_uri, urllib.urlencode(query))
	
	def get_top_rated_movies(self, page=1):
		base_uri = "movie/top_rated"
		query = {"page": page}
		return self.request(base_uri, urllib.urlencode(query))
	
	def get_in_theaters_movies(self, page=1):
		base_uri = "movie/now_playing"
		query = {"page": page}
		return self.request(base_uri, urllib.urlencode(query))
	
	def movie_tmdb_coming_soon(self, page=1):
		base_uri = "movie/upcoming"
		query = {"page": page}
		return self.request(base_uri, urllib.urlencode(query))
		
	def get_network_by_id(self, id):
		base_uri = "network/%s" % id
		return self.request(base_uri)
		
	def discover_movies(self, query):
		base_uri = "discover/movie"
		return self.request(base_uri, urllib.urlencode(query))
	
	def movie_trailers(self, id):
		base_uri = "movie/%s/videos" % id
		results = self.request(base_uri)
		trailers = []
		for result in results['results']:
			if result['site'] == 'YouTube':
				record = {"name": result['name'], "key": result['key']}
				trailers.append(record)
		return trailers
		
	def list_movie_genre(self, id, page=1):
		base_uri = "genre/%s/movies?page=%s" % (id, page)
		results = self.request(base_uri, '')
		return results
	
	def list_tv_genre(self, id, page=1):
		base_uri = "discover/tv"
		query = 'with_genres=%s&sort_by=popularity.desc&page=%s' % (id, page)
		results = self.request(base_uri, query)
		return results
	
	def list_tv_network(self, id, page=1):
		base_uri = "discover/tv"
		query = 'with_networks=%s&sort_by=popularity.desc&page=%s' % (id, page)
		results = self.request(base_uri, query)
		return results
	
	def query_person_id(self, person):
		ids = []
		base_uri = "search/person"
		query = {"query": person}
		results = self.request(base_uri, urllib.urlencode(query))
		for r in results['results']:
			if r['name'].lower() == person.lower():
				ids.append(str(r['id']))
		return ids
	
	def get_popular_people(self, page=1):
		query = {"page": page}
		base_uri = "person/popular"
		return self.request(base_uri, urllib.urlencode(query))
	
	def query_keyword_id(self, keyword, strict=False):
		ids = []
		base_uri = "search/keyword"
		query = {"query": keyword}
		results = self.request(base_uri, urllib.urlencode(query))
		for r in results['results']:
			if strict and r['name'].lower() != keyword.lower(): 
				continue
			ids.append(str(r['id']))
		return ids
	
	def process_record(self, record, media=None):
		if media=='movie':
			meta = self.process_movie(record)
			return meta
		elif media=='episode':
			meta = self.process_episode(record)
			return meta
		elif media=='tvshow':
			meta = self.process_show(record)
			return meta
	
	def meta_map(self, path, object, default=''):
		try:
			if isinstance(path, list):
				for k in path:
					object = object[k]
			else:
				object = object[path]
				object = self.normalize(object) if object is not None else default
			return object
		except Exception, e:
			ADDON.log('TMDB error: %s' % str(e))
			return default
		
	def process_movie(self, record):
		meta = {}
		meta['imdb_id'] = None
		meta['tmdb_id'] = self.meta_map('id', record)
		meta['trakt_id'] = ''
		meta['slug'] = ''
		meta['title'] = self.meta_map('title', record)
		meta['year'] = record['release_date'][0:4] if self.meta_map('release_date', record) else 0
		meta['writer'] = ''
		meta['director'] = ''
		meta['tagline'] = ''
		meta['cast'] = []
		meta['rating'] = self.meta_map('vote_average', record)
		meta['votes'] =self.meta_map('vote_count', record)
		meta['duration'] = ''
		meta['plot'] = self.meta_map('overview', record)
		meta['mpaa'] = ''
		meta['premiered'] = self.meta_map('release_date', record)
		meta['trailer_url'] = ''
		meta['genre'] = ''
		meta['studio'] = ''
		meta['thumb_url'] = 'http://image.tmdb.org/t/p/w780%s' % record['poster_path']
		meta['cover_url'] = 'http://image.tmdb.org/t/p/w780%s' % record['poster_path']
		meta['backdrop_url'] = 'http://image.tmdb.org/t/p/original%s' % record['backdrop_path']
		meta['overlay'] = 6
		meta['playcount'] = 0
		if meta['imdb_id'] is None or meta['imdb_id'] =='None':
			imdb_id = self.resolve_imdb_id(meta['title'], meta['year'], 'movie', meta['tmdb_id'])
			meta['imdb_id'] = imdb_id
		
		
		SQL = """INSERT OR REPLACE INTO movies (
				imdb_id,
				tmdb_id,
				trakt_id,
				title,
				year,
				tagline,
				duration,
				rating,
				votes,
				plot,
				mpaa,
				premiered,
				cover_url,
				thumb_url,
				backdrop_url,
				trailer_url,
				overlay,
				playcount
				) VALUES(?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?)
				"""
		values = [meta[k] for k in ["imdb_id","tmdb_id","trakt_id","title","year","tagline","duration","rating","votes","plot","mpaa","premiered","cover_url","thumb_url","backdrop_url","trailer_url","overlay","playcount"]]
		DB.execute(SQL, values)
		DB.commit()
		return meta	
	
	def process_show(self, record):
		meta = {}
		meta['imdb_id'] = None
		meta['tmdb_id'] = record['id']
		meta['tvdb_id'] = ''
		meta['trakt_id'] = ''
		meta['slug'] = ''
		meta['title'] = self.meta_map('name', record)
		meta['TVShowTitle'] = self.meta_map('name', record)
		meta['rating'] = self.meta_map('popularity', record)
		meta['duration'] = ''
		meta['plot'] = self.meta_map('overview', record)
		meta['mpaa'] = ''
		meta['premiered'] = self.meta_map('first_air_date', record)
		meta['year'] = record['first_air_date'][0:4] if self.meta_map('first_air_date', record) else 0
		meta['trailer_url'] = ''
		meta['genre'] = ''
		meta['studio'] = ''
		meta['status'] = ''
		meta['cast'] = []
		meta['banner_url'] = ''	
		meta['cover_url'] = 'http://image.tmdb.org/t/p/w780%s' % record['poster_path']
		meta['backdrop_url'] = 'http://image.tmdb.org/t/p/original%s' % record['backdrop_path']
		meta['overlay'] = 6
		meta['episode'] = 0
		meta['playcount'] = 0
		if meta['imdb_id'] is None:
			imdb_id = self.resolve_imdb_id(meta['TVShowTitle'], meta['year'], 'series', meta['tmdb_id'])
			meta['imdb_id'] = imdb_id
		SQL = """INSERT OR REPLACE INTO tvshows (
				imdb_id,
				tmdb_id,
				tvdb_id,
				trakt_id,
				title,
				year,
				TVShowTitle,
				duration,
				rating,
				plot,
				mpaa,
				cover_url,
				banner_url,
				backdrop_url,
				trailer_url,
				overlay,
				playcount
				) VALUES(?,?,?,?,? ,?,?,?,?,?, ?,?,?,?,?, ?,?)
				"""
				
		values = [meta[k] for k in ["imdb_id","tmdb_id","tvdb_id","trakt_id","title","year","TVShowTitle","duration","rating","plot","mpaa","cover_url","banner_url","backdrop_url","trailer_url","overlay","playcount"]]
		DB.execute(SQL, values)
		DB.commit()
		return meta
	
	def request(self, base_uri, query=''):
		
		tmdb = TMDB(api_key = self.api_key)
		results = tmdb._do_request(base_uri, query)
		return results
		