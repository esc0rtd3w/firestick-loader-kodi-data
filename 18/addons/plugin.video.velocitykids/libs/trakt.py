# -*- coding: utf-8 -*-
#

import urllib2, urllib
from urllib2 import URLError, HTTPError
from datetime import datetime
import re, time
import json
import traceback
import kodi
from tm_libs import cache_stat

use_https = kodi.get_setting('use_https')
list_size = int(kodi.get_setting('list_size'))
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
if use_https =='true':
	BASE_URL = "https://api-v2launch.trakt.tv"
else:
	BASE_URL = "http://api-v2launch.trakt.tv"


CLIENT_ID = 'a19aa7f7cf7fa27437254cc27fcba454664360086949e80029f83874fa455e8f'
SECRET_ID = '5872236e7c198363867d89014ee334281648a7f433f9e4c362e5519e334693d1'


PIN_URL = 'http://trakt.tv/pin/7558'
DAYS_TO_GET = 21
DECAY = 2
ADDON_NAME = 'Velocity'


class TraktError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		try:
			s = self.value
		except Exception,e:
			print "-----",type(e),e
		return s
	

class TraktAPI():
	def __init__(self):
		self.token = None
		self.timeout = int(kodi.get_setting('timeout'))
		self.limit = int(kodi.get_setting('list_size'))
		self.cache_limit = int(kodi.get_setting('cache_limit'))
		self.cacheset = kodi.get_setting('cache_set')
	def authorize(self, pin):
		response = self._authorize(pin)
		if response:
			kodi.notify(header='Trakt', msg='You are now authorized' , duration=5000, sound=None)
			the_username=self.my_username()
			kodi.set_setting('trakt_username',the_username['username'])
		else:
			kodi.notify(header='Trakt', msg='Authorization Failed try again' , duration=5000, sound=None)
		return response

	def my_username(self):
		uri = '/users/me/'
		results = self._call(uri, auth=True)
		return results



	def get_object_id(self, trakt_id = None, imdb_id=None, tmdb_id=None, id_type='trakt'):
		if trakt_id is not None: return trakt_id
		if imdb_id is not None: return imdb_id
		uri = '/search'
		result = self._call(uri, params={"id_type": 'tmdb_id', "id": tmdb_id})
		type = result[0]['type']
		return result[0][type]['ids']['id_type']
	
	def query_id(self, id_type, id):
		uri = '/search'
		result = self._call(uri, params={"id_type": id_type, "id": id})
		type = result[0]['type']
		return result[0][type]['ids']['imdb']
	
	def query_slug(self, id_type, id):
		uri = '/search'
		result = self._call(uri, params={"id_type": id_type, "id": id})
		type = result[0]['type']
		return result[0][type]['ids']['slug']
	
	def lookup(self, media, id, id_type='imdb'):
		uri = '/search'
		record = self._call(uri, params={"id_type": id_type, "id": id, 'extended': 'full,images'})
		metadata = self.process_record(record, media)
		return metadata
	
	def get_episode_details(self, id, season, episode, params={'extended': 'full,images'}):
		uri = '/shows/%s/seasons/%s/episodes/%s' % (id, season, episode)
		episode = self._call(uri, params=params, auth=False)
		show = self.get_show_details(id)
		record = {"episode": episode, "show": show}
		return self.process_record(record, media='episode')
	
	def get_show_details(self, id):
		uri = '/shows/%s' % id
		record = self._call(uri, params={'extended': 'full,images'}, auth=False)
		return record
	
	def get_movie_details(self, id):
		uri = '/movies/%s' % (id)	
		record = self._call(uri, params={'extended': 'full,images'}, auth=False)
		return self.process_record(record, media='movie')
		
	def search_tv(self, query, media='show'):
		uri = '/search'
		return self._call(uri, params={'query': query, 'type': media, 'extended': 'full,images'})

	def search_movies(self, query, media='movie'):
		uri = '/search'
		return self._call(uri, params={'query': query, 'type': media, 'extended': 'full,images'})
		
	def get_calendar_shows(self):
		from datetime import date, timedelta
		d = date.today() - timedelta(days=(DAYS_TO_GET - 1)) 
		today = d.strftime("%Y-%m-%d")
		uri = '/calendars/my/shows/%s/%s' % (today, DAYS_TO_GET)
		media='episode'
		return self._call(uri, params={'extended': 'full,images'}, cache=False, auth=True)
	
	def get_calendar_daily_shows(self, delta=0, number=1):
		from datetime import date, timedelta
		d = date.today() - timedelta(days=delta)
		start_date = d.strftime("%Y-%m-%d")
		uri = '/calendars/my/shows/%s/%s' % (start_date, number)
		media='episode'
		return self._call(uri, params={'extended': 'full,images'}, cache=False, auth=True)
	
	def get_calendar_episodes(self, delta=0, number=1):
		from datetime import date, timedelta
		d = date.today() - timedelta(days=delta)
		start_date = d.strftime("%Y-%m-%d")
		uri = '/calendars/all/shows/%s/%s' % (start_date, number)
		media='episode'
		return self._call(uri, params={'extended': 'full,images'}, cache=False, auth=False)
	
	def get_calendar(self, calendar, delta=0, number=1):
		from datetime import date, timedelta
		d = date.today() - timedelta(days=delta)
		start_date = d.strftime("%Y-%m-%d")
		uri = '/calendars/%s/%s/%s' % (calendar, start_date, number)
		media='episode'
		auth = calendar.startswith("my")
		return self._call(uri, params={'extended': 'full,images'}, cache=False, auth=auth)
		
	def get_similar_tvshows(self, id):
		uri = '/shows/%s/related' % id
		media = 'show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)

	def get_most_collected_tvshows(self):
		uri = '/shows/collected'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)


	def get_most_played_tvshows(self):
		uri = '/shows/played/weekly'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)

	def get_most_watched_tvshows(self):
		uri = '/shows/watched/'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)




	def get_trending_tvshows(self):
		uri = '/shows/trending'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)
	
	def get_anticipated_tvshows(self):
		uri = '/shows/anticipated'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)

	def get_my_collected_tvshows(self):
		uri = '/sync/collection/shows'
		media = 'show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=True)

	def collection_progress(self,trakt_id):
		uri = '/shows/'+trakt_id+'/progress/collection?hidden=true&specials=true'
		media = 'show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=True)


	def get_popular_tvshows(self):
		uri = '/shows/popular'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)
	
	def get_recommended_tvshows(self):
		uri = '/recommendations/shows'
		media='show'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=True)
	
	def get_show_seasons(self, id):
		uri = '/shows/%s/seasons' % id
		return self._call(uri, params={'extended': 'images'})
	
	def get_show_episodes(self, id, season):
		uri = '/shows/%s/seasons/%s' % (id, season)
		media='episode'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset)
	
	def get_watchlist_tvshows(self, extended='full,images', simple=False, id_type='imdb'):
		uri = '/users/me/watchlist/shows'
		media = 'tvshow'
		if simple:
			records = self._call(uri, cache=False, auth=True)
			return [record['show']['ids'][id_type] for record in records]
		else:
			return self._call(uri, params={'extended': extended}, cache=False, auth=True)
	
	def get_watchlist_movies(self, extended='full,images', simple=False, id_type='imdb'):
		uri = '/users/me/watchlist/movies'
		if simple:
			records = self._call(uri, auth=True)
			return [record['movie']['ids'][id_type] for record in records]
		else:
			return self._call(uri, params={'extended': extended}, auth=True)
	
	def get_trending_movies(self):
		uri = '/movies/trending'
		media='movie'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)

	def get_popular_movies(self):
		uri = '/movies/popular'
		media = 'movie'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)

	def get_most_watched_movies(self):
		uri = '/movies/watched/'
		media='movie'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)

	def get_most_played_movies(self):
		uri = '/movies/played/weekly'
		media='movie'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)

	def get_most_collected_movies(self):
		uri = '/movies/collected'
		media='movie'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)

	def get_boxoffice_movies(self):
		uri = '/movies/boxoffice'
		media='movie'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)


	
	def get_recommended_movies(self):
		uri = '/recommendations/movies'
		media = 'movie'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=True)

	def get_my_collected(self):
		uri = '/sync/collection/movies'
		media = 'movie'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=True)
	
	def get_similar_movies(self, id):
		uri = '/movies/%s/related' % id
		media = 'movie'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=False)
	
	def get_show_info(self, id, episodes=False):
		if episodes:
			uri = '/shows/%s/seasons' % id
			return self._call(uri, params={'extended': 'episodes,full'})
		else:
			uri = '/shows/%s' % id
			return self._call(uri)
	
	def get_custom_lists(self):
		uri = '/users/me/lists'
		return sorted(self._call(uri, params={}, auth=True))
	
	def get_liked_lists(self):
		uri = '/users/likes/lists'
		return sorted(self._call(uri, params={}, auth=True))
	
	def get_custom_list(self, slug, media, username=None, params={'extended': 'full,images'}):
		if media=='tvshows': media = 'show'
		if media=='tv': media = 'show'
		if username is None:	
			uri = '/users/me/lists/%s/items' % slug 
			auth = True
		else:
			uri = '/users/%s/lists/%s/items' % (username.replace('.', '-'), slug)
			auth = False
		temp = self._call(uri, params=params, auth=auth)
		results = []
		for r in temp:
			if r['type'] == media:
				results.append(r)
		return results		
	
	def create_custom_list(self, title):
		uri = '/users/me/lists'
		post_dict = {
			"name": title,
			"description": "Created by %s" % ADDON_NAME,
			"privacy": "public",
			"display_numbers": True,
			"allow_comments": True
		}
		return self._call(uri, data=post_dict, auth=True)
	
	def add_to_watchlist(self, media, id, id_type='trakt'):
		if kodi.get_setting('debug') == "true":
			print "Adding Trakt Id: "+id+" to Watchlist"
		uri = '/sync/watchlist'
		data = {media:  [{'ids': {id_type: id}}]}
		return self._call(uri, data, auth=True)

	def delete_from_watchlist(self, media, id, id_type='trakt'):
		if kodi.get_setting('debug') == "true":
			print"Deleting Trakt Id: "+id+" from Watchlist"
		uri = '/sync/watchlist/remove'
		data = {media:  [{'ids': {id_type: id}}]}
		return self._call(uri, data, auth=True)
		
	def add_to_custom_list(self, media, slug, id, id_type='trakt'):
		if media=='movies':
			post_dict = {'movies': [{'ids': {id_type: id}}]}
		else:
			post_dict = {'shows': [{'ids': {id_type: id}}]}
		uri = '/users/me/lists/%s/items' % slug
		return self._call(uri, data=post_dict, auth=True)
	
	def delete_from_custom_list(self, media, slug, id, id_type='trakt'):
		if media=='movies':
			post_dict = {'movies': [{'ids': {id_type: id}}]}
		else:
			post_dict = {'shows': [{'ids': {id_type: id}}]}
		uri = '/users/me/lists/%s/items/remove' % slug
		return self._call(uri, post_dict, auth=True)
	
	def delete_custom_list(self, slug):
		uri = '/users/me/lists/%s' % slug
		return self._delete(uri)
	
	def set_watched_state(self, media, id, watched, season=None):
		uri = '/sync/history' if watched else '/sync/history/remove'
		if media == 'episode':
			post_dict = {'episodes': [{"ids": {"trakt": id}}]}
		elif media == 'movies':
			post_dict = {'movies': [{"ids": {"trakt": id}}]}
		elif media == 'season':
			post_dict = {'shows': [{'seasons': [{'number': int(season)}], 'ids': {'trakt': id}}]}
		return self._call(uri, post_dict, auth=True)
	
	def get_watched_history(self, media):
		uri = '/sync/watched/%s' % media
		if media == 'shows':
			results = {}
			response = self._call(uri, auth=True, cache=False)
			for r in response:
				imdb_id =  r['show']['ids']['imdb']
				results[imdb_id] = {}
				seasons = r['seasons']
				for season in seasons:
					results[imdb_id][season['number']] = []
					for episode in season['episodes']: results[imdb_id][season['number']].append(episode['number'])
			return results
		else:
			results = {"imdb": [], "tmdb": [], "trakt": []}
			response = self._call(uri, auth=True, cache=False)
			for r in response:
				results['trakt'].append(r['movie']['ids']['trakt'])
				results['imdb'].append(r['movie']['ids']['imdb'])
				results['tmdb'].append(r['movie']['ids']['tmdb'])
			return results	
	
	def get_next_episodes(self):
		uri = '/sync/history/episodes'
		response = self._call(uri, auth=True)
		for r in response:
			ADDON.log(r)
		#ADDON.log(response)

	
	def get_bookmark(self, media, id, id_type = 'imdb', season=None, episode=None):
		bookmarks = self.get_bookmarks(media)
		for bookmark in bookmarks:
			if media == 'episodes':
				if id== bookmark['show']['ids'][id_type] and bookmark['episode']['season'] == int(season) and bookmark['episode']['number'] == int(episode):
					return bookmark['progress']
			else:
				if id == bookmark['movie']['ids'][id_type]:
					return bookmark['progress']
		return None
	def get_bookmarks(self, media):
		uri = '/sync/playback/%s' % media
		return self._call(uri, auth=True)
		
	
	def process_record(self, record, media=None, watched=None):
		if media=='movie':
			meta = self.process_movie(record)
			return meta
		elif media=='episode':
			meta = self.process_episode(record, watched=watched)
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
				object = object if object is not None else default
			return object
		except:
			return default
		
	
	def process_show(self, record):
		try:
			show = record['show']
		except:
			show = record
		meta = {}

		meta['imdb_id'] = self.meta_map(['ids', 'imdb'], show)
		meta['tvdb_id'] = self.meta_map(['ids', 'tvdb'], show)
		meta['tmdb_id'] = self.meta_map(['ids', 'tmdb'], show)
		meta['trakt_id'] = self.meta_map(['ids', 'trakt'], show)
		meta['title'] = self.meta_map('title', show)
		meta['TVShowTitle'] = self.meta_map('title', show)
		meta['rating'] = self.meta_map('rating', show)
		meta['number'] = self.meta_map('number', show)
		meta['duration'] = self.meta_map('runtime', show)
		meta['plot'] = self.meta_map('overview', show)
		meta['mpaa'] = self.meta_map('certification', show)
		meta['premiered'] = self.meta_map('first_aired', show)
		meta['year'] = int(self.meta_map('year', show, default=0))
		meta['trailer_url'] = self.meta_map('trailer', show)
		meta['genre'] = self.meta_map('genres', show)
		meta['studio'] = self.meta_map('network', show)
		meta['status'] = self.meta_map('status', show)     
		meta['cast'] = []
		meta['banner_url'] = self.meta_map(['images', 'thumb', 'full'], show)
		meta['cover_url'] = self.meta_map(['images', 'poster', 'full'], show)
		meta['backdrop_url'] = self.meta_map(['images', 'fanart', 'full'], show)
		meta['overlay'] = 6
		meta['playcount'] = 0
		return meta
		
	def process_movie(self, record):
		try:
			movie = record['movie']
		except:
			movie = record
		meta = {}
		meta['imdb_id'] = self.meta_map(['ids', 'imdb'], movie)
		meta['tmdb_id'] = self.meta_map(['ids', 'tmdb'], movie)
		meta['trakt_id'] = self.meta_map(['ids', 'trakt'], movie)
		meta['title'] = self.meta_map('title', movie)
		meta['year'] = int(self.meta_map('year', movie, default=0))
		meta['writer'] = ''
		meta['director'] = ''
		meta['tagline'] = self.meta_map('tagline', movie)
		meta['cast'] = []
		meta['rating'] = self.meta_map('rating', movie)
		meta['votes'] = self.meta_map('votes', movie)
		meta['duration'] = self.meta_map('runtime', movie)
		meta['plot'] = self.meta_map('overview', movie)
		meta['mpaa'] = self.meta_map('certification', movie)
		meta['premiered'] = self.meta_map('released', movie)
		meta['trailer_url'] = self.meta_map('trailer', movie)
		meta['genre'] = self.meta_map('genres', movie)
		meta['studio'] = ''
		meta['thumb_url'] = self.meta_map(['images', 'thumb', 'full'], movie)
		meta['cover_url'] = self.meta_map(['images', 'poster', 'full'], movie)
		meta['backdrop_url'] = self.meta_map(['images', 'fanart', 'full'], movie)
		meta['overlay'] = 6
		meta['playcount'] = 0
		return meta
	
	def process_episode(self, record, watched=None):
		if 'show' in record.keys():
			show = record['show']
			episode = record['episode']
			meta = {}
			meta['imdb_id']= self.meta_map(['ids', 'imdb'], show) 				# show['ids']['imdb']
			meta['tvdb_id']= self.meta_map(['ids', 'tvdb'], show) 				# show['ids']['tvdb']
			meta['tmdb_id']= self.meta_map(['ids', 'tmdb'], show) 				# show['ids']['tmdb']
			meta['trakt_id']= self.meta_map(['ids', 'trakt'], episode) 			# episode['ids']['trakt']
			meta['year'] = int(self.meta_map('year', show, default=0)) 			# int(show['year'])
			meta['episode_id'] = ''                
			meta['season']= int(self.meta_map('season', episode, default=0)) 	# int(episode['season'])
			meta['episode']= int(self.meta_map('number', episode, default=0)) 	# int(episode['number'])
			meta['title']= self.meta_map('title', episode) 						# episode['title']
			meta['showtitle'] = self.meta_map('title', show) 					# #show['title']
			meta['director'] = ''
			meta['writer'] = ''
			meta['plot'] = self.meta_map('overview', episode) 					# episode['overview']
			meta['rating'] = self.meta_map('rating', episode) 					# episode['rating']
			meta['premiered'] = self.meta_map('first_aired', episode) 			# episode['first_aired']
			meta['poster'] = self.meta_map(['images', 'poster', 'full'], show) 	# show['images']['poster']['full']
			meta['cover_url']= self.meta_map(['images', 'screenshot', 'full'], episode) 	# episode['images']['screenshot']['full']
			meta['trailer_url']=''
			meta['backdrop_url'] = self.meta_map(['images', 'fanart', 'full'], show) 	# show['images']['fanart']['full']
			meta['overlay'] = 6
			meta['playcount'] = 0
			if watched:
				for w in watched:
					if w['episode']['number'] == meta['episode']:
						meta['overlay'] = 7
						meta['playcount'] = 1
						break
			return meta
		else:
			meta = {}
			episode = record
			meta['premiered'] = self.meta_map('first_aired', episode)
			tmp = re.match('^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.000Z', meta['premiered'])
			if tmp:
				aired = datetime(int(tmp.group(1)), int(tmp.group(2)),int(tmp.group(3)),int(tmp.group(4)),int(tmp.group(5)),int(tmp.group(6)))
				aired = time.mktime(aired.timetuple())
				now = time.mktime(datetime.now().timetuple())
			else:
				return False
			if aired < now:
				meta['imdb_id']= self.meta_map(['ids', 'imdb'], episode) 			# episode['ids']['imdb']
				meta['tvdb_id']= self.meta_map(['ids', 'tvdb'], episode) 			# episode['ids']['tvdb']
				meta['tmdb_id']= self.meta_map(['ids', 'tmdb'], episode) 			# episode['ids']['tmdb']
				meta['trakt_id']= self.meta_map(['ids', 'trakt'], episode) 			# episode['ids']['trakt']
				meta['year'] = 0
				meta['episode_id'] = ''
				meta['season']= int(self.meta_map('season', episode, default=0))		# int(episode['season'])
				meta['episode']= int(self.meta_map('number', episode, default=0))	#int(episode['number'])
				meta['title']= self.meta_map('title', episode)						# episode['title']
				meta['showtitle'] = ''
				meta['director'] = ''
				meta['writer'] = ''
				meta['plot'] = self.meta_map('overview', episode) 					#episode['overview']
				meta['rating'] = self.meta_map('rating', episode) 					#episode['rating']
				meta['premiered'] = self.meta_map('first_aired', episode) 			#episode['first_aired']
				meta['poster'] = ''
				meta['cover_url']= self.meta_map(['images', 'screenshot', 'full'], episode)
				meta['trailer_url']=''
				meta['backdrop_url'] = ''
				meta['overlay'] = 6
				meta['playcount'] = 0
				if watched:
					for w in watched:
						if w['episode']['number'] == meta['episode']:
							meta['overlay'] = 7
							meta['playcount'] = 1
							break
				return meta
			return False

	def _authorize(self, pin=None):
		if kodi.get_setting('debug') == "true":
			print "Attempting to login/refresh Trakt Account"
		uri = '/oauth/token'
		data = {'client_id': CLIENT_ID, 'client_secret': SECRET_ID, 'redirect_uri': REDIRECT_URI}
		if pin:
			data['code'] = pin
			data['grant_type'] = 'authorization_code'
		else:
			refresh_token = kodi.get_setting('trakt_refresh_token')
			if refresh_token:
				data['refresh_token'] = refresh_token
				data['grant_type'] = 'refresh_token'
			else:
				kodi.set_setting('trakt_oauth_token', '')
				kodi.set_setting('trakt_refresh_token', '')
				kodi.set_setting('trakt_authorized', 'false')
				return False
		if self.token is None: self.token = False
		response = self._call(uri, data, auth=False)
		if response is False or response is None:
			return False
		if 'access_token' in response.keys() and 'refresh_token' in response.keys():
			kodi.set_setting('trakt_oauth_token', response['access_token'])
			kodi.set_setting('trakt_refresh_token', response['refresh_token'])
			kodi.set_setting('trakt_authorized', "true")
			self.token = response['access_token']
			if kodi.get_setting('debug') == "true":
				print "YOU JUST AUTHORIZED TRAKT"
				#kodi.notify('TRAKT ','Account Authorized You may continue','5000','')
			return True
	
	def _call(self, uri, data=None, params=None, auth=False, cache=False, timeout=None):
		url = '%s%s' % (BASE_URL, uri)
		if timeout is not None: self.timetout = timeout
		json_data = json.dumps(data) if data else None
		headers = {'Content-Type': 'application/json', 'trakt-api-key': CLIENT_ID, 'trakt-api-version': 2}
		if auth:
			self._authorize()
			if self.token is None:
				raise TraktError('Trakt Authorization Required: 400')
			headers.update({'Authorization': 'Bearer %s' % (self.token)})
		#url = '%s%s' % (BASE_URL, uri)
		#print "URL IS = "+url
		if params and not uri.endswith('/token'):
			params['limit'] = self.limit
		else:
			params = {'limit': self.limit}
		url = url + '?' + urllib.urlencode(params)
		#START CACHE STUFF
		created, cached_result = cache_stat.get_cached_url(url)
		now = time.time()
		#print "API NOW TIME IS :"+str(now)
		limit = 60 * 60 * int(kodi.get_setting('cache_limit'))
		#print "API LIMIT IS : "+str(limit)
		age = now - created
		#print "API AGE IS :"+str(age)
		if cached_result and  age < limit:
			result = cached_result
			#print 'Using cached result for: %s' % (url)
			response = json.loads(result)
			return response
		#END CACHE STUFF
		else:
			try:
				request = urllib2.Request(url, data=json_data, headers=headers)
				f = urllib2.urlopen(request, timeout=self.timeout)
				result = f.read()
				response = json.loads(result)
			except HTTPError as e:
				print "ERROR IS  = "+str(e)
				#ADDON.log(url, LOG_LEVEL.VERBOSE)
				if not uri.endswith('/token'):
					print "ERROR IS  = "+str(e)
					#ADDON.show_error_dialog(['Trakt Error', 'HTTP ERROR', str(e)])
					#raise TraktError('Trakt-HTTP-Error: %s' % e)
				return False
			except URLError as e:
				print "URLERROR IS  = "+str(e)
				#ADDON.log(url, LOG_LEVEL.VERBOSE)
				if not uri.endswith('/token'):
					#ADDON.show_error_dialog(['Trakt Error', 'URLLib ERROR', str(e)])
					raise TraktError('Trakt-URL-Error: %s' % e)
				return False
			else:
				if cache =='true':
					cache_stat.set_cache_url(url,result)
					return response
				else:
					return response
	
	def _delete(self, uri, data=None, params=None, auth=True):
		json_data = json.dumps(data) if data else None
		url = '%s%s' % (BASE_URL, uri)
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		headers = {'Content-Type': 'application/json', 'trakt-api-key': CLIENT_ID, 'trakt-api-version': 2}
		if auth: headers.update({'Authorization': 'Bearer %s' % (self.token)})
		request = urllib2.Request(url, data=json_data, headers=headers)
		request.get_method = lambda: 'DELETE'
		response = opener.open(request)
		return response

	def add_my_watchlist(self, media, id, year):
		uri = '/sync/watchlist'
		data = {media:  [{'title': id,'year':year}]}
		return self._call(uri, data, auth=True)


	def delete_my_watchlist(self, media, id, year):
		uri = '/sync/watchlist/remove'
		data = {media:  [{'title': id,'year':year}]}
		return self._call(uri, data, auth=True)

	def get_show_progress(self, show_id):
		uri = '/shows/%s/progress/watched' % (show_id)
		media = 'show'
		#if hidden: params['hidden'] = 'true'
		#if specials: params['specials'] = 'true'
		return self._call(uri, params={'extended': 'full,images'}, cache=self.cacheset, auth=True)


	def add_to_collection(self, media, id, id_type='trakt'):
		if kodi.get_setting('debug') == "true":
			print "Adding Trakt Id: "+id+" from Collection"
		uri = '/sync/collection'
		data = {media:  [{'ids': {id_type: id}}]}
		return self._call(uri, data, auth=True)

	def remove_from_collection(self, media, id, id_type='trakt'):
		if kodi.get_setting('debug') == "true":
			print"Deleting Trakt Id: "+id+" from Collection"
		uri = '/sync/collection/remove'
		data = {media:  [{'ids': {id_type: id}}]}
		return self._call(uri, data, auth=True)

	def get_user_lists(self,name,media):
		uri = '/users/'+name+'/lists'
		return sorted(self._call(uri, params={}))

	def get_users_list(self, slug, media, username=None, params={'extended': 'full,images'}):
		if media=='tvshows': media = 'show'
		if media=='tv': media = 'show'
		if username is None:
			uri = '/users/me/lists/%s/items' % slug
			auth = True
		else:
			uri = '/users/%s/lists/%s/items' % (username.replace('.', '-'), slug)
			auth = False
		temp = self._call(uri, params=params, auth=auth)
		results = []
		for r in temp:
			if r['type'] == media:
				results.append(r)
		return results

	def get_special_list(self, slug, media, username=None, params={'extended': 'full,images'}):
		if media=='tvshows': media = 'show'
		if media=='tv': media = 'show'
		if media=='shows': media='show'
		if media =='movies': media = 'movie'
		if username is None:
			uri = '/users/me/lists/%s/items' % slug
			auth = True
		else:
			uri = '/users/%s/lists/%s/items' % (username.replace('.', '-'), slug)
			auth = False
		temp = self._call(uri, params=params, auth=auth)
		results = []
		for r in temp:
			if r['type'] == media:
				results.append(r)
		return results

	def get_watched_movies(self, id):
		uri = '/sync/history/movies/%s' % id
		results = self._call(uri, auth=True)
		return results


	def get_watched_shows(self, id):
		uri = '/sync/history/shows/%s' % id
		results = self._call(uri, auth=True)
		return results

	def get_watched_seasons(self, id):
		uri = '/sync/history/seasons/%s' % id
		results = self._call(uri, auth=True)
		return results

	def get_watched_episodes(self, id):
		uri = '/sync/history/episodes/%s' % id
		results = self._call(uri, auth=True)
		return results


	def get_watched(self,media):
		uri = '/sync/watched/%s' % (media)
		#uri = '/sync/history/shows/tt0364845'
		response = self._call(uri, auth=True)
		return response
'''
movies = TraktAPI()
#response =movies.get_movie_details("iron+man")
response = movies.get_trending_movies()
print response'''