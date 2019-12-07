#!/usr/bin/python
# -*- coding: utf-8 -*-

'''*
	Copyright (C) 2016 DudeHere

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
import urllib
import json
import requests

from dudehere.routines import *
from dudehere.routines import plugin

_user_agent = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.99 Safari/535.1'
_accept = 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
_headers = {"User-Agent": _user_agent, "Content-Type": "application/json"}
TMDB_KEY = plugin.get_setting('tmdb_api_key', addon_id="script.module.dudehere.routines")
TVDB_KEY =  plugin.get_setting('tvdb_api_key', addon_id="script.module.dudehere.routines")
FANART_KEY =  plugin.get_setting('fanarttv_api_key', addon_id="script.module.dudehere.routines")
DISABLE_FANART = plugin.get_setting('enable_fanart') == "false"
DISABLE_FANART_SERIES = plugin.get_setting('enable_series_fanart') == "false"
DISABLE_FANART_EPISODES = plugin.get_setting('enable_episode_fanart') == "false"
DISABLE_FANART_MOVIES = plugin.get_setting('enable_movie_fanart') == "false"
DISABLE_FANARTTV = plugin.get_setting('enable_fanarttv') == "false"
DISABLE_TVDB = plugin.get_setting('enable_tvdb') == "false"
DISABLE_TMDB = plugin.get_setting('enable_tmdb') == "false"
DISABLE_TVMAZE = plugin.get_setting('enable_tvmaze') == "false"
DISABLE_OIMDB = plugin.get_setting('enable_oimdbapi') == "false"

def set_art(results, media, url):
	if not results[media]:
		results[media] = url
	return results	

def get_ids(media_type, trakt_id):
	
	if media_type == 'show':
		result = DB.query("SELECT tvdb_id, tmdb_id, imdb_id FROM id_table WHERE media_type='show' AND trakt_id=?", [trakt_id])
		if result:
			return result[0], result[1], result[2]
		else:
			try:
				r = trakt.query_ids(trakt_id, "trakt", media_type)
				ids = r[media_type]
				cache_ids(media_type, ids)
				return ids['tvdb'], ids['tmdb'], ids['imdb']
			except:
				return False, False, False
	elif media_type == 'movie':
		result = DB.query("SELECT tmdb_id, imdb_id FROM id_table WHERE media_type='movie' AND trakt_id=?", [trakt_id])
		if result:
			return result[0], result[1]
		else:
			try:
				r = trakt.query_ids(trakt_id, "trakt", media_type)
				ids = r[media_type]
				cache_ids(media_type, ids)
				return ids['tmdb'], ids['imdb']
			except:
				return False, False
	else:
		result = DB.query("SELECT tvdb_id, tmdb_id, season, episode, show_tvdb_id, tvmaze_id FROM id_table WHERE media_type='episode' AND trakt_id=?", [trakt_id])
		if result:
			return result[0], result[1], result[2], result[3], result[4], result[5]
		else:
			return False, False, False, False, False, False

def cache_ids(media_type, ids):
	if media_type == 'show':
		SQL = "INSERT INTO id_table(media_type, trakt_id, slug, tvdb_id, imdb_id, tmdb_id, tvrage_id) VALUES('show',?,?,?,?,?,?)"
		data = [ids['trakt'],ids['slug'],ids['tvdb'],ids['imdb'],ids['tmdb'],ids['tvrage']]
	elif media_type == 'movie':
		SQL = "INSERT INTO id_table(media_type, trakt_id, slug, imdb_id, tmdb_id) VALUES('movie',?,?,?,?)"
		data = [ids['trakt'],ids['slug'],ids['imdb'],ids['tmdb']]
	else:
		return
		
	DB.execute(SQL, data)
	DB.commit()
				

def get_movie_art(trakt_id):
	result = _get_cached_movie(trakt_id)
	if result:
		return result
	
	result = {"fanart": "", "poster": ""}
	tmdb_id, imdb_id = get_ids('movie', trakt_id)
	
	if DISABLE_FANARTTV is False:
		response = search_fanart('movies', imdb_id)
		result = set_art(result, "poster", response["poster"])
		result = set_art(result, "fanart", response["fanart"])
	
	if DISABLE_TMDB is False:
		if not result['fanart'] or not result['poster']:
			response = search_tmdb("movies", tmdb_id)
			result = set_art(result, "fanart", response["fanart"])
			result = set_art(result, "poster", response["poster"])
	
	if DISABLE_OIMDB is False:
		if not result['poster']:
			response = omdbapi_request().request('/', params={"r": "json", "i": imdb_id})
			if response and 'Poster' in response:
				result = set_art(result, "poster", [response['Poster'].replace('_V1_SX300', '_V1_SX500')])
	_cache_movie_result(trakt_id, result)
	return result

def get_all_movie_art(trakt_id):
	results = {"fanart": [], "poster": []}
	tmdb_id, imdb_id = get_ids('movie', trakt_id)
	
	if DISABLE_FANARTTV is False:
		try:
			uri = '/movies/%s' % imdb_id
			response = fanart_request.request(uri)
			if 'moviebackground' in response:
				results['fanart'] += [art['url'] for art in response['moviebackground']]
			if 'movieposter' in response:
				results['poster'] += [art['url'] for art in response['movieposter']]
		except: pass
	
	if DISABLE_TMDB is False:
		try:
			uri = "/movie/%s/images" % tmdb_id
			response = tmdb_request.request(uri)
			if 'backdrops' in response and response['backdrops']:
				results['fanart'] += ["http://image.tmdb.org/t/p/w1280" + art['file_path'] for art in response['backdrops']]
			if 'posters' in response and response['posters']:
				results['poster'] += ["http://image.tmdb.org/t/p/w500" + art['file_path'] for art in response['posters']]
		except: pass
	
	if DISABLE_OIMDB is False:
		try:
			response = omdbapi_request().request('/', params={"r": "json", "i": imdb_id})
			if response and 'Poster' in response:
				results['poster'] += [response['Poster'].replace('_V1_SX300', '_V1_SX500')]
		except: pass
	
	return results
	
def get_show_art(trakt_id):
	result = _get_cached_tv(trakt_id)
	if result:
		return result
	tvdb_id,tmdb_id,imdb_id = get_ids('show', trakt_id)
	result = {"fanart": "", "poster": ""}
	if DISABLE_TMDB is False:
		if not result['fanart'] or not result['poster']:
			response = search_tmdb("shows", tmdb_id)
			result = set_art(result, "fanart", response["fanart"])
			result = set_art(result, "poster", response["poster"])
	
	if DISABLE_TVDB is False:
		if not result['fanart'] or not result['poster']:
			response = search_tvdb(tvdb_id)
			result['fanart'] = response['fanart']
			result['poster'] = response['poster']
			
	if DISABLE_FANARTTV is False:
		response = search_fanart('shows', tvdb_id)
		result = set_art(result, "poster", response["poster"])
		result = set_art(result, "fanart", response["fanart"])

	if DISABLE_OIMDB is False and imdb_id is not None:
		if not result['poster']:
			response = omdbapi_request().request('/', params={"r": "json", "i": imdb_id})
			if response and 'Poster' in response:
				result = set_art(result, "poster", [response['Poster'].replace('_V1_SX300', '_V1_SX500')])
	_cache_tv_result(trakt_id, result)
	return result

def get_all_show_art(trakt_id):
	results = {"fanart": [], "poster": []}
	tvdb_id,tmdb_id,imdb_id = get_ids('show', trakt_id)
	
	if DISABLE_FANARTTV is False:
		uri = '/tv/%s' % tvdb_id
		try:
			response = fanart_request().request(uri)
			if 'showbackground' in response:
				results['fanart'] += [art['url'] for art in response['showbackground']]
			if 'tvposter' in response:
				results['poster'] += [art['url'] for art in response['tvposter']]
		except: pass
	
	
	if DISABLE_TVDB is False:
		uri = "/series/%s/images/query" % tvdb_id
		try:
			response = tvdb_request().request(uri, params={"keyType": "fanart"})
			results['fanart'] += ["http://thetvdb.com/banners/" + art['fileName'] for art in response['data']]
		except: pass
		try:
			response = tvdb_request().request(uri, params={"keyType": "poster"})
			results['poster'] += ["http://thetvdb.com/banners/" + art['fileName'] for art in response['data']]
		except: pass
	
	if DISABLE_TMDB is False:
		uri = '/tv/%s/images' % tmdb_id
		try:
			response = imdb_request().request(uri, params={"api_key": TMDB_KEY})
			if 'backdrops' in response and response['backdrops']:
				results['fanart'] += ["http://image.tmdb.org/t/p/w1280" + art['file_path'] for art in response['backdrops']]
			if 'posters' in response and response['posters']:
				results['poster'] += ["http://image.tmdb.org/t/p/w500" + art['file_path'] for art in response['posters']]
		except: pass
	
	return results

def search_tvdb(tvdb_id):
	result = {"fanart": "", "poster": ""}
	def sort_art(record):
		return record['ratingsInfo']['average']
	uri = "/series/%s/images/query" % tvdb_id
	try:
		response = tvdb_request().request(uri, params={"keyType": "fanart"})
		data = sorted(response['data'], reverse=True, key=lambda k: sort_art(k))
		result["fanart"] = "http://thetvdb.com/banners/" + data[0]['fileName']
	except: pass
	try:
		response = tvdb_request().request(uri, params={"keyType": "poster"})
		data = sorted(response['data'], reverse=True, key=lambda k: sort_art(k))
		result["poster"] = "http://thetvdb.com/banners/" + data[0]['fileName']
	except: pass

	return result

def search_tmdb(media, tmdb_id):
	result = {"fanart": "", "poster": ""}
	if media == 'shows':
		
		uri = '/tv/%s/images' % tmdb_id
		try:
			response = tmdb_request().request(uri)
			if 'backdrops' in response and response['backdrops']:
				result['fanart'] = "http://image.tmdb.org/t/p/w1280%s" % response['backdrops'][0]['file_path']
			if 'posters' in response and response['posters']:
				result['poster'] = "http://image.tmdb.org/t/p/w500%s" % response['posters'][0]['file_path']
		except: pass
	else:
		try:
			uri = "/movie/%s/images" % tmdb_id
			response = tmdb_request().request(uri)
			if 'backdrops' in response and response['backdrops']:
				result['fanart'] = "http://image.tmdb.org/t/p/w1280%s" % response['backdrops'][0]['file_path']
			if 'posters' in response and response['posters']:
				result['poster'] = "http://image.tmdb.org/t/p/w500%s" % response['posters'][0]['file_path']
		except: pass
	return result

def search_fanart(media, id):
	result = {"fanart": "", "poster": ""}
	if media == 'shows':
		uri = '/tv/%s' % id
		try:
			response = fanart_request().request(uri)
			if 'showbackground' in response:
				result['fanart'] = response['showbackground'][0]['url']
			if 'tvposter' in response:
				result['poster'] = response['tvposter'][0]['url']
		except: pass
		
	else:
		try:
			uri = '/movies/%s' % id
			response = fanart_request().request(uri)
			if 'moviebackground' in response:
				result['fanart'] = response['moviebackground'][0]['url']
			if 'movieposter' in response:
				result['poster'] = response['movieposter'][0]['url']
		except: pass	
	return result

def get_season_art(tvdb_id, imdb_id=None):
	result = {}
	if DISABLE_TVDB: return result
	
	def sort_art(record):
		return record['ratingsInfo']['average']
	try:
		uri = "/series/%s/images/query" % tvdb_id
		response = tvdb_request().request(uri, params={"keyType": "season"})
		data = sorted(response['data'], reverse=False, key=lambda k: sort_art(k))
		for d in data:
			season = int(d["subKey"])
			result[season] = "http://thetvdb.com/banners/" + d["fileName"]
	except: pass
	if DISABLE_TVMAZE is False:
		cache_episode_art(tvdb_id, imdb_id)
	return result

def get_season_poster(tvdb_id, season):
	result = _get_cached_season(tvdb_id, season)
	if result: return result

	results = {}
	if DISABLE_TVDB: return result
	def sort_art(record):
		return record['ratingsInfo']['average']
	try:
		uri = "/series/%s/images/query" % tvdb_id
		response = tvdb_request().request(uri, params={"keyType": "season"})
		data = sorted(response['data'], reverse=False, key=lambda k: sort_art(k))
		for d in data:
			s = int(d["subKey"])
			img = "http://thetvdb.com/banners/" + d["fileName"]
			results[s] = img
			if s == season:
				result = img
		_cache_seasons(tvdb_id, results)
	except:
		return False
	return result

def get_episode_art(trakt_id):
	result = _get_cached_screenshot(trakt_id)
	if result:
		return result['screenshot']
	else:
		screenshot = ''
		
	tvdb_id, tmdb_id, season, episode, show_tvdb_id, tvmaze_id = get_ids('episode', trakt_id)	
	if not screenshot:
		try:
			uri = "/tv/%s/season/%s/episode/%s/images" % (tmdb_id, season, episode)
			response = tmdb_request().request(uri)
			if response and 'stills' in response and response['stills']:
				screenshot = "http://image.tmdb.org/t/p/w500%s" % response['stills'][0]['file_path']
		except: pass
	
	if not screenshot:
		try:
			uri = '/episodes/%s' % tvdb_id
			response = tvdb_request().request(uri)
			if response and 'data' in response and response['data']['filename']:
				screenshot = 'http://thetvdb.com/banners/_cache/' + response['data']['filename']
		except: pass
	
	if not screenshot:
		cached = DB.query("SELECT screenshot FROM tvmaze_episodes WHERE tvdb_id=? AND season=? and episode=?", [show_tvdb_id, season, episode])
		if cached:
			screenshot = cached[0]
		else:
			tvmaze_id = lookup_tvmaze_id(show_tvdb_id)
			if tvmaze_id:
				uri = "/shows/%s/episodes" % tvmaze_id
				response = tvmaze_request().request(uri, params={"specials": 0})
				values = []
				for e in response:
					try:
						if season == int(e['season']) and episode == int(e['number']):
							screenshot = e['image']['original']
						values.append([show_tvdb_id, tvmaze_id, e['season'], e['number'], e['image']['original']])
					except:pass
				if DB.db_type == 'mysql':
					SQL = "INSERT IGNORE INTO tvmaze_episodes(tvdb_id, tvmaze_id, season, episode, screenshot) VALUES(?,?,?,?,?)"
				else:
					SQL = "INSERT INTO tvmaze_episodes(tvdb_id, tvmaze_id, season, episode, screenshot) VALUES(?,?,?,?,?)"
				DB.execute_many(SQL, values)
				DB.commit()
	if screenshot:
		_cache_screenshot(trakt_id, screenshot)
	return screenshot

def get_person_art(tmdb_id):
	person = ''
	try:
		uri = "/person/%s" % tmdb_id
		response = tmdb_request().request(uri)
		if 'profile_path' in response and response['profile_path'] is not None:
			person = "http://image.tmdb.org/t/p/w500%s" % response['profile_path']
			_cache_person(tmdb_id, person)
	except: pass
	
	return person
	
	
def _get_cached_tv(trakt_id):
	result = DB.query("SELECT fanart, poster FROM fanart_shows WHERE trakt_id=?", [trakt_id])
	if result:
		return {"fanart": result[0], "poster": result[1]}
	else:
		return False
	
def _get_cached_movie(trakt_id):
	result = DB.query("SELECT fanart, poster FROM fanart_movies WHERE trakt_id=?", [trakt_id])
	if result:
		return {"fanart": result[0], "poster": result[1]}
	else:
		return False

def _get_cached_screenshot(trakt_id):
	result = DB.query("SELECT screenshot FROM fanart_episodes WHERE trakt_id=?", [trakt_id])
	if result:
		return {"screenshot": result[0]}
	else:
		return False

def _get_cached_person(tmdb_id):
	result = DB.query("SELECT image FROM fanart_people WHERE tmdb_id=?", [tmdb_id])
	if result:
		return {"person": result[0]}
	else:
		return False
		
def _get_cached_season(tvdb_id, season):
	poster = DB.query("SELECT poster FROM fanart_seasons WHERE tvdb_id=? AND season=?", [tvdb_id, season])
	if poster:
		return poster[0]
	else:
		return False

def _cache_tv_result(trakt_id, result):
	if not result['poster'] and not result['fanart']: return
	SQL = "INSERT INTO fanart_shows(trakt_id, fanart, poster) VALUES(?,?,?)"
	DB.execute(SQL, [trakt_id, result['fanart'], result['poster']])
	DB.commit()

def _cache_movie_result(trakt_id, result):
	if not result['poster'] and not result['fanart']: return
	SQL = "INSERT INTO fanart_movies(trakt_id, fanart, poster) VALUES(?,?,?)"
	DB.execute(SQL, [trakt_id, result['fanart'], result['poster']])
	DB.commit()

def _cache_seasons(tvdb_id, seasons):
	for season in seasons:
		DB.execute("INSERT INTO fanart_seasons(tvdb_id, season, poster) VALUES(?,?,?)", [tvdb_id, season, seasons[season]])
	DB.commit()
	
def _cache_screenshot(trakt_id, screenshot):
	DB.execute("INSERT INTO fanart_episodes(trakt_id, screenshot) VALUES(?,?)", [trakt_id, screenshot])
	DB.commit()

def _cache_person(tmdb_id, image):
	DB.execute("INSERT INTO fanart_people(tmdb_id, image) VALUES(?,?)", [tmdb_id, image])
	DB.commit()

def _cache_result(url, result):	
		DB.execute("REPLACE INTO request_cache(url, results) VALUES(?,?)", [url, json.dumps(result)])
		DB.commit()

def _get_cached_result(url, cache_limit=28800):
	result = False
	if DB.db_type == 'mysql':
		SQL = "SELECT results FROM request_cache WHERE unix_timestamp() - unix_timestamp(ts) < ? AND url=?"
		cache = DB.query(SQL, [cache_limit, url])
	else:
		SQL = "SELECT results FROM request_cache WHERE strftime('%s','now') -  strftime('%s',ts) < ? AND url=?"
		cache = DB.query(SQL, [cache_limit, url])
	if cache:
		result = json.loads(cache[0])
	return result		

class base_request():
	require_auth = False
	timeout = 5
	base_url = ''
	name = ''
	api_key = False
	headers = {"User-Agent": _user_agent, "Content-Type": "application/json"}
	
	def login(self): 
		pass
	
	def request(self, uri, params=None, data=None, cache_limit=False, auth=False):
		result = False
		url = '%s%s' % (self.base_url, uri)
		if self.api_key:
			if params is not None: params["api_key"] = self.api_key
			else: params = {"api_key": self.api_key}
			
		if params is not None:
			cache_url = url + '?' + urllib.urlencode(params)
		else:
			cache_url = url	
		result = _get_cached_result(cache_url)
		if result: return result
		if self.require_auth: self.login()
		if data is None:
			if params is not None:
				response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
			else:
				response = requests.get(url, headers=self.headers, timeout=self.timeout)
		else:		
			if params is not None:
				response = requests.post(url, data=json.dumps(data), params=params, headers=self.headers, timeout=self.timeout)
			else:
				response = requests.post(url, data=json.dumps(data), headers=self.headers, timeout=self.timeout)
		if response.status_code == requests.codes.ok:
			result = response.json()
			_cache_result(cache_url, result)
			return result
		else:
			response.raise_for_status()
		

class fanart_request(base_request):
	base_url = "http://webservice.fanart.tv/v3"
	headers = {"User-Agent": _user_agent, "Content-Type": "application/json", "api-key": FANART_KEY}
	
class tvdb_request(base_request):
	require_auth = True
	name = "tvdb"
	base_url = "https://api.thetvdb.com"
	headers = {"User-Agent": _user_agent, "Content-Type": "application/json", "Accept": "application/json"}
	
	def login(self):
		token = plugin.get_property(self.name + "_token")
		if not token:
			url = '%s%s' % (self.base_url, "/login")
			data = {"apikey": TVDB_KEY}
			response = requests.post(url, data=json.dumps(data), headers=self.headers, timeout=self.timeout)
			if response.status_code == requests.codes.ok:
				result = response.json()
				token = result['token']
				plugin.set_property(self.name + "_token", token)
			else:
				response.raise_for_status()
		self.headers["Authorization"] = "Bearer %s" % token	

class tmdb_request(base_request):
	base_url = "http://api.themoviedb.org/3"
	api_key = TMDB_KEY

class omdbapi_request(base_request):
	base_url = "http://www.omdbapi.com"

class tvmaze_request(base_request):
	base_url = "http://api.tvmaze.com"

def lookup_tvmaze_id(tvdb_id):
	test = DB.query("SELECT tvmaze_id FROM id_table WHERE tvdb_id=?", [tvdb_id])
	if test and test[0] is not None:
		return test[0]
	else:
		url = "http://api.tvmaze.com/lookup/shows?thetvdb=%s" % tvdb_id
		response = requests.get(url, allow_redirects=False)
		redirect = response.headers.get('Location')
		tvmaze_id = redirect.split('/')[-1]
		if DB.query("SELECT tvmaze_id FROM id_table WHERE tvdb_id=?", [tvdb_id]):
			DB.execute("UPDATE id_table SET tvmaze_id=? WHERE tvdb_id=?", [tvmaze_id, tvdb_id])
		else:
			DB.execute("INSERT INTO id_table(tvdb_id, tvmaze_id) VALUES(?,?)", [tvdb_id, tvmaze_id])
		DB.commit()
		return tvmaze_id
	return False

