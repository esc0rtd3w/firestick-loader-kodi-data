import time, requests
import xbmc, xbmcgui
from resources.lib import text
from resources.lib.xswift2 import plugin

title = 'Authenticate Trakt'
msg1  = 'Do you want to authenticate with Trakt now?'
msg2  = 'Please go to  https://trakt.tv/activate  and enter this code: '
limit =  plugin.get_setting('trakt_items_per_page', int)

TCI = plugin.get_setting('trakt_api_client_id', str)
TCS = plugin.get_setting('trakt_api_client_secret', str)
if len(TCI) == 64 and len(TCS) == 64:
	CLIENT_ID = TCI
	CLIENT_SECRET = TCS
else:
	CLIENT_ID     = 'd1feff7915af479f8d14cf9afcc2e5a2fb5534512021d58447985e2fd555b26d'
	CLIENT_SECRET = '68dd208db29a54c56753549a6dbc635e7e3a1e03104b15fc0dd00555f1a549cb'

def call_trakt(path, params={}, data=None, is_delete=False, with_auth=True, pagination=False, page=1):
	params = dict([(k, text.to_utf8(v)) for k, v in params.items() if v])
	headers = {
		'Content-Type': 'application/json',
		'trakt-api-key': CLIENT_ID,
		'trakt-api-version': '2'
		}

	def send_query():
		if with_auth:
			try:
				expires_at = plugin.get_setting('trakt_expires_at', int)
				if time.time() > expires_at:
					trakt_refresh_token()
			except:
				pass
			token = plugin.get_setting('trakt_access_token', unicode)
			if token:
				headers['Authorization'] = 'Bearer ' + token
		if data is not None:
			assert not params
			return requests.post('https://api.trakt.tv/' + path, json=data, headers=headers)
		elif is_delete:
			return requests.delete('https://api.trakt.tv/' + path, headers=headers)
		else:
			return requests.get('https://api.trakt.tv/' + path, params, headers=headers)

	def paginated_query(page):
		lists = []
		params['page'] = page
		results = send_query()
		if with_auth and results.status_code == 401 and plugin.yesno(title, msg1) and trakt_authenticate():
			response = paginated_query(1)
			return response
		results.raise_for_status()
		results.encoding = 'utf-8'
		lists.extend(results.json())
		return lists, results.headers['X-Pagination-Page-Count']

	if pagination == False:
		response = send_query()
		if with_auth and response.status_code == 401 and plugin.yesno(title, msg1) and trakt_authenticate():
			response = send_query()
		response.raise_for_status()
		response.encoding = 'utf-8'
		return response.json()
	else:
		response, numpages = paginated_query(page)
		return response, numpages

def search_trakt(id_type, id, type):
	return call_trakt('search/%s/%s?type=%s' % (id_type, id, type))

def find_trakt_ids(id_type, id, type):
	response = search_trakt(id_type, id, type)
	if response:
		content = response[0]
		return content[content['type']]['ids']
	return {}

def trakt_get_device_code():
	data = {'client_id': CLIENT_ID}
	return call_trakt('oauth/device/code', data=data, with_auth=False)

def trakt_get_device_token(device_codes):
	data = {
		'code': device_codes['device_code'],
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET
		}
	start = time.time()
	expires_in = device_codes['expires_in']
	pDialog = xbmcgui.DialogProgress()
	pDialog.create(title, msg2 + str(device_codes['user_code']))
	try:
		time_passed = 0
		while not xbmc.Monitor().abortRequested() and not pDialog.iscanceled() and time_passed < expires_in:            
			try:
				response = call_trakt('oauth/device/token', data=data, with_auth=False)
			except requests.HTTPError as e:
				if e.response.status_code != 400:
					raise e
				progress = int(100 * time_passed / expires_in)
				pDialog.update(progress)
				xbmc.sleep(max(device_codes['interval'], 1)*1000)
			else:
				return response
			time_passed = time.time() - start
	finally:
		pDialog.close()
		del pDialog
	return None

def trakt_refresh_token():
	data = {
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
		'grant_type': 'refresh_token',
		'refresh_token': plugin.get_setting('trakt_refresh_token', unicode)
		}
	response = call_trakt('oauth/token', data=data, with_auth=False)
	if response:
		plugin.set_setting('trakt_access_token', response['access_token'])
		plugin.set_setting('trakt_refresh_token', response['refresh_token'])

@plugin.route('/authenticate_trakt')
def trakt_authenticate():
	code = trakt_get_device_code()
	token = trakt_get_device_token(code)
	if token:
		expires_at = time.time() + 60*60*24*30
		plugin.set_setting('trakt_expires_at', str(expires_at))
		plugin.set_setting('trakt_access_token', token['access_token'])
		plugin.set_setting('trakt_refresh_token', token['refresh_token'])
		return True
	return False

@plugin.route('/cleartrakt')
def clear_trakt():
	title = 'OpenMeta: Clear Trakt account settings'
	msg = 'Reauthorizing Trakt will be required to access My Trakt.[CR][CR]Are you sure?'
	if plugin.yesno(title, msg):
		plugin.set_setting('trakt_access_token', '')
		plugin.set_setting('trakt_refresh_token', '')
		plugin.set_setting('trakt_expires_at', '')

def add_list(name, privacy_id=None, description=None):
	data = {
		'name': name,
		'description': description or '',
		'privacy': privacy_id or ('private', 'friends', 'public')[0]
		}
	return call_trakt('users/me/lists', data=data)

def del_list(list_slug):
	return call_trakt('users/me/lists/%s' % list_slug, is_delete=True)

@plugin.cached(TTL=60, cache='Trakt')
def get_hidden_items(type):
	return call_trakt('users/hidden/%s' % type)

def get_collection(type):
	return call_trakt('sync/collection/%s?extended=full' % type)

def get_movie_history(id):
	return call_trakt('users/me/history/movies/%s' % id)

def get_lists():
	return call_trakt('users/me/lists')

@plugin.cached(TTL=60, cache='Trakt')
def get_list(user, slug):
	return call_trakt('users/%s/lists/%s/items?extended=full' % (user, slug))

def get_liked_lists(page):
	result, pages = call_trakt('users/likes/lists?limit=%s' % limit, pagination=True, page=page)
	return result, pages

def get_watchlist(type):
	return call_trakt('sync/watchlist/%s?extended=full' % type)

def get_recommendations(type):
	return call_trakt('recommendations/%s?extended=full&ignore_collected=true&limit=%s' % (type, limit))

@plugin.cached(TTL=60, cache='Trakt')
def get_calendar():
	return call_trakt('calendars/my/shows?extended=full')
    
@plugin.cached(TTL=60*24, cache='Trakt')
def get_genres(type):
	return call_trakt('genres/%s' % type)

@plugin.cached(TTL=60, cache='Trakt')
def get_show(id):
	return call_trakt('shows/%s' % id)

@plugin.cached(TTL=60, cache='Trakt')
def get_show_play_count(id):
	return call_trakt('shows/%s/progress/watched' % id)

@plugin.cached(TTL=60, cache='Trakt')
def get_show_play_count_specials(id):
	return call_trakt('shows/%s/progress/watched?specials=true' % id)

def get_latest_episode(id):
	return call_trakt('shows/%s/last_episode' % id)

@plugin.cached(TTL=60, cache='Trakt')
def get_season(id,season_number):
	seasons = call_trakt('shows/%s/seasons' % id)
	for season in seasons:
		if season['number'] == season_number:
			return season

@plugin.cached(TTL=60, cache='Trakt')
def get_seasons(id):
	seasons = call_trakt('shows/%s/seasons' % id)
	return seasons

@plugin.cached(TTL=60, cache='Trakt')
def get_episode(id, season, episode):
	return call_trakt('shows/%s/seasons/%s/episodes/%s?extended=full' % (id, season, episode))

@plugin.cached(TTL=60, cache='Trakt')
def get_movie(id):
	return call_trakt('movies/%s' % id)

@plugin.cached(TTL=60, cache='Trakt')
def search_for_list(list_name, page):
	results, pages = call_trakt('search?type=list&query=%s&limit=%s' % (list_name, limit), pagination=True, page=page)
	return results, pages

@plugin.cached(TTL=60, cache='Trakt')
def search_for_movie(movie_title, page):
	results = call_trakt('search?type=movie&query=%s' % movie_title)
	return results

@plugin.cached(TTL=60, cache='Trakt')
def search_for_movie_paginated(movie_title, page):
	results, pages = call_trakt('search?type=movie&query=%s&limit=%s' % (movie_title, limit), pagination=True, page=page)
	return results, pages

@plugin.cached(TTL=60, cache='Trakt')
def search_for_tvshow_paginated(show_name, page):
	results, pages = call_trakt('search?type=show&query=%s&limit=%s' % (show_name, limit), pagination=True, page=page)
	return results, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_next_episodes():
	shows = call_trakt('sync/watched/shows?extended=noseasons&extended=full')
	hidden_shows = [item['show']['ids']['trakt'] for item in get_hidden_items('progress_watched') if item['type'] == 'show']
	items = []
	for item in shows:
		show = item['show']
		id = show['ids']['trakt']
		if id in hidden_shows:
			continue
		response = call_trakt('shows/%s/progress/watched?extended=full' % id)    
		if response['next_episode']:
			next_episode = response['next_episode']
			next_episode['show'] = show
			items.append(next_episode)
	return items

@plugin.cached(TTL=60, cache='Trakt')
def get_netflix_collected_shows(page):
	result, pages = call_trakt('shows/collected/weekly?networks=Netflix&extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_latest_releases_movies():
	return call_trakt('users/giladg/lists/latest-releases/items?extended=full', with_auth=False)

@plugin.cached(TTL=60, cache='Trakt')
def get_imdb_top_rated_movies(page):
	result, pages = call_trakt('users/justin/lists/imdb-top-rated-movies/items?extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_trending_shows_paginated(page):
	result, pages = call_trakt('shows/trending?extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_popular_shows_paginated(page):
	result, pages = call_trakt('shows/popular?extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_watched_shows_paginated(page):
	result, pages = call_trakt('shows/watched/weekly?extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_collected_shows_paginated(page):
	result, pages = call_trakt('shows/collected/weekly?extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_trending_movies_paginated(page):
	result, pages = call_trakt('movies/trending?extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_popular_movies_paginated(page):
	result, pages = call_trakt('movies/popular?extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_watched_movies_paginated(page):
	result, pages = call_trakt('movies/watched/weekly?extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_collected_movies_paginated(page):
	result, pages = call_trakt('movies/collected/weekly?extended=full&limit=%s' % limit, pagination=True, page=page, with_auth=False)
	return  result, pages

@plugin.cached(TTL=60, cache='Trakt')
def get_related_movies_paginated(imdb_id, page):
	return call_trakt('movies/%s/related?extended=full&limit=%s' % (imdb_id, limit), pagination=True, page=page, with_auth=False)