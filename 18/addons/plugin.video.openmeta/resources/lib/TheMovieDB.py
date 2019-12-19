import os, json, requests, requests_cache
from resources.lib.xswift2 import plugin

ext_key = plugin.get_setting('tmdb_api', str)

if len(ext_key) == 32:
	API_key = ext_key
else:
	API_key = '1248868d7003f60f2386595db98455ef'

requests_cache.install_cache(os.path.join(plugin.storage_path, 'TheMovieDB'), expire_after=21600)

class TMDB(object):
	BASE_PATH = ''
	URLS = {}
	def _get_path(self, key):
		return self.BASE_PATH + self.URLS[key]

	def _get_id_path(self, key):
		return self._get_path(key).format(id=self.id)

	def _get_guest_session_id_path(self, key):
		return self._get_path(key).format(guest_session_id=self.guest_session_id)

	def _get_credit_id_path(self, key):
		return self._get_path(key).format(credit_id=self.credit_id)

	def _get_series_id_season_number_path(self, key):
		return self._get_path(key).format(series_id=self.series_id, season_number=self.season_number)

	def _get_series_id_season_number_episode_number_path(self, key):
		return self._get_path(key).format(series_id=self.series_id, season_number=self.season_number, episode_number=self.episode_number)

	def _get_complete_url(self, path):
		return 'https://api.themoviedb.org/3/%s' % path

	def _get_params(self, params):
		api_dict = {'api_key': API_key}
		if params:
			params.update(api_dict)
		else:
			params = api_dict
		return params

	def _request(self, method, path, params=None, payload=None):
		url = self._get_complete_url(path)
		params = self._get_params(params)
		headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'Connection': 'close'
			}
		try:
			response = requests.request(method, url, params=params, data=json.dumps(payload) if payload else payload, headers=headers)
		except requests.exceptions.SSLError:
			response = requests.request(method, url, params=params, data=json.dumps(payload) if payload else payload, headers=headers, verify=False)
		try:
			response.raise_for_status()
		except requests.exceptions.HTTPError:
			pass
		response.encoding = 'utf-8'
		return response.json()

	def _GET(self, path, params=None):
		return self._request('GET', path, params=params)

	def _POST(self, path, params=None, payload=None):
		return self._request('POST', path, params=params, payload=payload)

	def _DELETE(self, path, params=None, payload=None):
		return self._request('DELETE', path, params=params, payload=payload)

	def _set_attrs_to_values(self, response={}):
		if isinstance(response, dict):
			for key in response.keys():
				if not hasattr(self, key) or not callable(getattr(self, key)):
					setattr(self, key, response[key])

class Account(TMDB):
	BASE_PATH = 'account'
	URLS = {
		'info': '',
		'lists': '/{id}/lists', 
		'favorite_movies': '/{id}/favorite/movies',
		'favorite_tv': '/{id}/favorite/tv',
		'favorite': '/{id}/favorite',
		'rated_movies': '/{id}/rated/movies',
		'rated_tv': '/{id}/rated/tv',
		'watchlist_movies': '/{id}/watchlist/movies',
		'watchlist_tv': '/{id}/watchlist/tv',
		'watchlist': '/{id}/watchlist'
		}

	def __init__(self, session_id):
		super(Account, self).__init__()
		self.session_id = session_id

	def info(self, **kwargs):
		path = self._get_path('info')
		kwargs.update({'session_id': self.session_id})
		response = self._GET(path, kwargs)
		self.id = response['id']
		self._set_attrs_to_values(response)
		return response

	def lists(self, **kwargs):
		path = self._get_id_path('lists')
		kwargs.update({'session_id': self.session_id})
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def favorite_movies(self, **kwargs):
		path = self._get_id_path('favorite_movies')
		kwargs.update({'session_id': self.session_id})
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def favorite_tv(self, **kwargs):
		path = self._get_id_path('favorite_tv')
		kwargs.update({'session_id': self.session_id})
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def favorite(self, **kwargs):
		path = self._get_id_path('favorite')
		kwargs.update({'session_id': self.session_id})
		payload = {
			'media_type': kwargs.pop('media_type', None),
			'media_id': kwargs.pop('media_id', None),
			'favorite': kwargs.pop('favorite', None)
			}
		response = self._POST(path, kwargs, payload)
		self._set_attrs_to_values(response)
		return response

	def rated_movies(self, **kwargs):
		path = self._get_id_path('rated_movies')
		kwargs.update({'session_id': self.session_id})
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def rated_tv(self, **kwargs):
		path = self._get_id_path('rated_tv')
		kwargs.update({'session_id': self.session_id})
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def watchlist_movies(self, **kwargs):
		path = self._get_id_path('watchlist_movies')
		kwargs.update({'session_id': self.session_id})
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def watchlist_tv(self, **kwargs):
		path = self._get_id_path('watchlist_tv')
		kwargs.update({'session_id': self.session_id})
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def watchlist(self, **kwargs):
		path = self._get_id_path('watchlist')
		kwargs.update({'session_id': self.session_id})
		payload = {
			'media_type': kwargs.pop('media_type', None),
			'media_id': kwargs.pop('media_id', None),
			'watchlist': kwargs.pop('watchlist', None)
			}
		response = self._POST(path, kwargs, payload)
		self._set_attrs_to_values(response)
		return response

class Authentication(TMDB):
	BASE_PATH = 'authentication'
	URLS = {
		'token_new': '/token/new',
		'token_validate_with_login': '/token/validate_with_login',
		'session_new': '/session/new',
		'guest_session_new': '/guest_session/new'
		}

	def token_new(self, **kwargs):
		path = self._get_path('token_new')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def token_validate_with_login(self, **kwargs):
		path = self._get_path('token_validate_with_login')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def session_new(self, **kwargs):
		path = self._get_path('session_new')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def guest_session_new(self, **kwargs):
		path = self._get_path('guest_session_new')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class GuestSessions(TMDB):
	BASE_PATH = 'guest_session'
	URLS = {'rated_movies': '/{guest_session_id}/rated_movies'}

	def __init__(self, guest_session_id=0):
		super(GuestSessions, self).__init__()
		self.guest_session_id = guest_session_id

	def rated_movies(self, **kwargs):
		path = self._get_guest_session_id_path('rated_movies')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Lists(TMDB):
	BASE_PATH = 'list'
	URLS = {
		'info': '/{id}',
		'item_status': '/{id}/item_status',
		'create_list': '',
		'add_item': '/{id}/add_item',
		'remove_item': '/{id}/remove_item',
		'clear': '/{id}/clear'
		}

	def __init__(self, id=0, session_id=0):
		super(Lists, self).__init__()
		self.id = id
		self.session_id = session_id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def item_status(self, **kwargs):
		path = self._get_id_path('item_status')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def create_list(self, **kwargs):
		path = self._get_path('create_list')
		kwargs.update({'session_id': self.session_id})
		payload = {
			'name': kwargs.pop('name', None),
			'description': kwargs.pop('description', None)
			}
		if 'language' in kwargs:
			payload['language'] = kwargs['language']
		response = self._POST(path, kwargs, payload)
		self._set_attrs_to_values(response)
		return response

	def add_item(self, **kwargs):
		path = self._get_id_path('add_item')
		kwargs.update({'session_id': self.session_id})
		payload = {'media_id': kwargs.pop('media_id', None)}
		response = self._POST(path, kwargs, payload)
		self._set_attrs_to_values(response)
		return response

	def remove_item(self, **kwargs):
		path = self._get_id_path('remove_item')
		kwargs.update({'session_id': self.session_id})
		payload = {'media_id': kwargs.pop('media_id', None)}
		response = self._POST(path, kwargs, payload)
		self._set_attrs_to_values(response)
		return response

	def clear_list(self, **kwargs):
		path = self._get_id_path('clear')
		kwargs.update({'session_id': self.session_id})
		payload = {}
		response = self._POST(path, kwargs, payload)
		self._set_attrs_to_values(response)
		return response

class Changes(TMDB):
	BASE_PATH = ''
	URLS = {
		'movie': 'movie/changes',
		'person': 'person/changes',
		'tv': 'tv/changes'
		}

	def movie(self, **kwargs):
		path = self._get_path('movie')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def person(self, **kwargs):
		path = self._get_path('person')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def tv(self, **kwargs):
		path = self._get_path('tv')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Configuration(TMDB):
	BASE_PATH = 'configuration'
	URLS = {'info': ''}
    
	def info(self, **kwargs):
		path = self._get_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Certifications(TMDB):
	BASE_PATH = 'certification'
	URLS = {'movie_list': '/movie/list'}

	def list(self, **kwargs):
		path = self._get_path('movie_list')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Timezones(TMDB):
	BASE_PATH = 'timezones'
	URLS = {'list': '/list'}

	def list(self, **kwargs):
		path = self._get_path('list')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Discover(TMDB):
	BASE_PATH = 'discover'
	URLS = {
		'movie': '/movie',
		'tv': '/tv'
		}

	def movie(self, **kwargs):
		for param in kwargs:
			if '_lte' in param:
				kwargs[param.replace('_lte', '.lte')] = kwargs.pop(param)
			if '_gte' in param:
				kwargs[param.replace('_gte', '.gte')] = kwargs.pop(param)
		path = self._get_path('movie')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def tv(self, **kwargs):
		for param in kwargs:
			if '_lte' in param:
				kwargs[param.replace('_lte', '.lte')] = kwargs.pop(param)
			if '_gte' in param:
				kwargs[param.replace('_gte', '.gte')] = kwargs.pop(param)
		path = self._get_path('tv')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Find(TMDB):
	BASE_PATH = 'find'
	URLS = {'info': '/{id}'}

	def __init__(self, id=0):
		super(Find, self).__init__()
		self.id = id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Genres(TMDB):
	BASE_PATH = 'genre'
	URLS = {
		'movie_list': '/movie/list',
		'tv_list': '/tv/list',
		'movies': '/{id}/movies'
		}

	def __init__(self, id=0):
		super(Genres, self).__init__()
		self.id = id

	def movie_list(self, **kwargs):
		path = self._get_path('movie_list')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def tv_list(self, **kwargs):
		path = self._get_path('tv_list')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def movies(self, **kwargs):
		path = self._get_id_path('movies')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Search(TMDB):
	BASE_PATH = 'search'
	URLS = {
		'movie': '/movie',
		'collection': '/collection',
		'tv': '/tv',
		'person': '/person',
		'company': '/company',
		'keyword': '/keyword',
		'multi': '/multi'
		}

	def movie(self, **kwargs):
		path = self._get_path('movie')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def collection(self, **kwargs):
		path = self._get_path('collection')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def tv(self, **kwargs):
		path = self._get_path('tv')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def person(self, **kwargs):
		path = self._get_path('person')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def company(self, **kwargs):
		path = self._get_path('company')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def keyword(self, **kwargs):
		path = self._get_path('keyword')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def multi(self, **kwargs):
		path = self._get_path('multi')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class People(TMDB):
	BASE_PATH = 'person'
	URLS = {
		'info': '/{id}',
		'movie_credits': '/{id}/movie_credits',
		'tv_credits': '/{id}/tv_credits',
		'combined_credits': '/{id}/combined_credits',
		'external_ids': '/{id}/external_ids',
		'images': '/{id}/images',
		'changes': '/{id}/changes',
		'popular': '/popular',
		'latest': '/latest'
		}

	def __init__(self, id=0):
		super(People, self).__init__()
		self.id = id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def movie_credits(self, **kwargs):
		path = self._get_id_path('movie_credits')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def tv_credits(self, **kwargs):
		path = self._get_id_path('tv_credits')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def combined_credits(self, **kwargs):
		path = self._get_id_path('combined_credits')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def external_ids(self, **kwargs):
		path = self._get_id_path('external_ids')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def images(self, **kwargs):
		path = self._get_id_path('images')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def changes(self, **kwargs):
		path = self._get_id_path('changes')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def popular(self, **kwargs):
		path = self._get_path('popular')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def latest(self, **kwargs):
		path = self._get_path('latest')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Credits(TMDB):
	BASE_PATH = 'credit'
	URLS = {'info': '/{credit_id}'}

	def __init__(self, credit_id):
		super(Credits, self).__init__()
		self.credit_id = credit_id

	def info(self, **kwargs):
		path = self._get_credit_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Jobs(TMDB):
	BASE_PATH = 'job'
	URLS = {'list': '/list'}

	def list(self, **kwargs):
		path = self._get_path('list')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Movies(TMDB):
	BASE_PATH = 'movie'
	URLS = {
		'info': '/{id}',
		'alternative_titles': '/{id}/alternative_titles',
		'credits': '/{id}/credits',
		'images': '/{id}/images',
		'keywords': '/{id}/keywords',
		'release_dates': '/{id}/release_dates',
		'releases': '/{id}/releases',
		'videos': '/{id}/videos',
		'translations': '/{id}/translations',
		'similar_movies': '/{id}/similar_movies',
		'reviews': '/{id}/reviews',
		'lists': '/{id}/lists',
		'changes': '/{id}/changes',
		'latest': '/latest',
		'upcoming': '/upcoming',
		'now_playing': '/now_playing',
		'popular': '/popular',
		'top_rated': '/top_rated',
		'account_states': '/{id}/account_states',
		'rating': '/{id}/rating',
		'recommendations': '/{id}/recommendations'
		}

	def __init__(self, id=0):
		super(Movies, self).__init__()
		self.id = id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def alternative_titles(self, **kwargs):
		path = self._get_id_path('alternative_titles')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def credits(self, **kwargs):
		path = self._get_id_path('credits')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def images(self, **kwargs):
		path = self._get_id_path('images')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def keywords(self):
		path = self._get_id_path('keywords')
		response = self._GET(path)
		self._set_attrs_to_values(response)
		return response

	def recommendations(self, **kwargs):
		path = self._get_id_path('recommendations')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def release_dates(self, **kwargs):
		path = self._get_id_path('release_dates')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def releases(self, **kwargs):
		path = self._get_id_path('releases')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def videos(self, **kwargs):
		path = self._get_id_path('videos')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def translations(self, **kwargs):
		path = self._get_id_path('translations')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def similar_movies(self, **kwargs):
		path = self._get_id_path('similar_movies')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def reviews(self, **kwargs):
		path = self._get_id_path('reviews')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def lists(self, **kwargs):
		path = self._get_id_path('lists')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def changes(self, **kwargs):
		path = self._get_id_path('changes')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def latest(self, **kwargs):
		path = self._get_path('latest')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def upcoming(self, **kwargs):
		path = self._get_path('upcoming')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def now_playing(self, **kwargs):
		path = self._get_path('now_playing')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def popular(self, **kwargs):
		path = self._get_path('popular')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def top_rated(self, **kwargs):
		path = self._get_path('top_rated')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def account_states(self, **kwargs):
		path = self._get_id_path('account_states')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def rating(self, **kwargs):
		path = self._get_id_path('rating')
		payload = {'value': kwargs.pop('value', None)}
		response = self._POST(path, kwargs, payload)
		self._set_attrs_to_values(response)
		return response

class Collections(TMDB):
	BASE_PATH = 'collection'
	URLS = {
		'info': '/{id}',
		'images': '/{id}/images'
		}

	def __init__(self, id):
		super(Collections, self).__init__()
		self.id = id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def images(self, **kwargs):
		path = self._get_id_path('images')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Companies(TMDB):
	BASE_PATH = 'company'
	URLS = {
		'info': '/{id}',
		'movies': '/{id}/movies'
		}

	def __init__(self, id=0):
		super(Companies, self).__init__()
		self.id = id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def movies(self, **kwargs):
		path = self._get_id_path('movies')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Keywords(TMDB):
	BASE_PATH = 'keyword'
	URLS = {
		'info': '/{id}',
		'movies': '/{id}/movies'
		}

	def __init__(self, id):
		super(Keywords, self).__init__()
		self.id = id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def movies(self, **kwargs):
		path = self._get_id_path('movies')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Reviews(TMDB):
	BASE_PATH = 'review'
	URLS = {'info': '/{id}'}

	def __init__(self, id):
		super(Reviews, self).__init__()
		self.id = id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class TV(TMDB):
	BASE_PATH = 'tv'
	URLS = {
		'info': '/{id}',
		'alternative_titles': '/{id}/alternative_titles',
		'content_ratings': '/{id}/content_ratings',
		'credits': '/{id}/credits',
		'external_ids': '/{id}/external_ids',
		'images': '/{id}/images',
		'rating': '/{id}/rating',
		'similar': '/{id}/similar',
		'recommendations': '/{id}/recommendations',
		'translations': '/{id}/translations',
		'videos': '/{id}/videos',
		'latest': '/latest',
		'on_the_air': '/on_the_air',
		'airing_today': '/airing_today',
		'top_rated': '/top_rated',
		'popular': '/popular'
		}

	def __init__(self, id=0):
		super(TV, self).__init__()
		self.id = id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def alternative_titles(self, **kwargs):
		path = self._get_id_path('alternative_titles')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def content_ratings(self, **kwargs):
		path = self._get_id_path('content_ratings')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def credits(self, **kwargs):
		path = self._get_id_path('credits')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def external_ids(self, **kwargs):
		path = self._get_id_path('external_ids')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def images(self, **kwargs):
		path = self._get_id_path('images')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def rating(self, **kwargs):
		path = self._get_id_path('rating')
		payload = {'value': kwargs.pop('value', None)}
		response = self._POST(path, kwargs, payload)
		self._set_attrs_to_values(response)
		return response

	def similar(self, **kwargs):
		path = self._get_id_path('similar')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def recommendations(self, **kwargs):
		path = self._get_id_path('recommendations')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def translations(self, **kwargs):
		path = self._get_id_path('translations')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def videos(self, **kwargs):
		path = self._get_id_path('videos')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def latest(self, **kwargs):
		path = self._get_id_path('latest')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def on_the_air(self, **kwargs):
		path = self._get_path('on_the_air')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def airing_today(self, **kwargs):
		path = self._get_path('airing_today')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def top_rated(self, **kwargs):
		path = self._get_path('top_rated')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def popular(self, **kwargs):
		path = self._get_path('popular')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class TV_Seasons(TMDB):
	BASE_PATH = 'tv/{series_id}/season/{season_number}'
	URLS = {
		'info': '',
		'credits': '/credits',
		'external_ids': '/external_ids',
		'images': '/images',
		'videos': '/videos'
		}

	def __init__(self, series_id, season_number):
		super(TV_Seasons, self).__init__()
		self.series_id = series_id
		self.season_number = season_number

	def info(self, **kwargs):
		path = self._get_series_id_season_number_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def credits(self, **kwargs):
		path = self._get_series_id_season_number_path('credits')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def external_ids(self, **kwargs):
		path = self._get_series_id_season_number_path('external_ids')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def images(self, **kwargs):
		path = self._get_series_id_season_number_path('images')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def videos(self, **kwargs):
		path = self._get_series_id_season_number_path('videos')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class TV_Episodes(TMDB):
	BASE_PATH = 'tv/{series_id}/season/{season_number}/episode/{episode_number}'
	URLS = {
		'info': '',
		'credits': '/credits',
		'external_ids': '/external_ids',
		'images': '/images',
		'rating': '/rating',
		'videos': '/videos'
		}

	def __init__(self, series_id, season_number, episode_number):
		super(TV_Episodes, self).__init__()
		self.series_id = series_id
		self.season_number = season_number
		self.episode_number = episode_number

	def info(self, **kwargs):
		path = self._get_series_id_season_number_episode_number_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def credits(self, **kwargs):
		path = self._get_series_id_season_number_episode_number_path('credits')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def external_ids(self, **kwargs):
		path = self._get_series_id_season_number_episode_number_path('external_ids')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def images(self, **kwargs):
		path = self._get_series_id_season_number_episode_number_path('images')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

	def rating(self, **kwargs):
		path = self._get_series_id_season_number_episode_number_path('rating')
		payload = {'value': kwargs.pop('value', None)}
		response = self._POST(path, kwargs, payload)
		self._set_attrs_to_values(response)
		return response

	def videos(self, **kwargs):
		path = self._get_series_id_season_number_episode_number_path('videos')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response

class Networks(TMDB):
	BASE_PATH = 'network'
	URLS = {'info': '/{id}'}

	def __init__(self, id):
		super(Networks, self).__init__()
		self.id = id

	def info(self, **kwargs):
		path = self._get_id_path('info')
		response = self._GET(path, kwargs)
		self._set_attrs_to_values(response)
		return response