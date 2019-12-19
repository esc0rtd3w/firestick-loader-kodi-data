import os
import xbmc, xbmcvfs, xbmcplugin
from resources.lib import text
from resources.lib import Trakt
from resources.lib import tools
from resources.lib import nav_base
from resources.lib import meta_info
from resources.lib import lib_movies
from resources.lib import playrandom
from resources.lib import play_movies
from resources.lib.rpc import RPC
from resources.lib import fanarttv
from resources.lib.xswift2 import plugin


enablefanart = plugin.get_setting('enablefanart', bool)
countenabled = plugin.get_setting('countenabled', bool)
traktenabled = True if plugin.get_setting('trakt_access_token', unicode) != '' else False
SORT = [
	xbmcplugin.SORT_METHOD_UNSORTED,
	xbmcplugin.SORT_METHOD_LABEL,
	xbmcplugin.SORT_METHOD_VIDEO_YEAR,
	xbmcplugin.SORT_METHOD_GENRE,
	xbmcplugin.SORT_METHOD_VIDEO_RATING,
	xbmcplugin.SORT_METHOD_PLAYCOUNT]
SORTRAKT = [
	xbmcplugin.SORT_METHOD_UNSORTED,
	xbmcplugin.SORT_METHOD_LABEL,
	xbmcplugin.SORT_METHOD_VIDEO_YEAR,
	xbmcplugin.SORT_METHOD_GENRE,
	xbmcplugin.SORT_METHOD_VIDEO_RATING,
	xbmcplugin.SORT_METHOD_PLAYCOUNT,
	xbmcplugin.SORT_METHOD_DURATION]

@plugin.route('/movies/tmdb/blockbusters/<page>/')
def tmdb_movies_blockbusters(page, raw=False):
	from resources.lib.TheMovieDB import Discover
	result = Discover().movie(language='en', append_to_response='external_ids,videos', **{'page': page, 'sort_by': 'revenue.desc'})
	if raw:
		return result
	else:
		return list_tmdb_movies(result)

@plugin.route('/movies/tmdb/random_blockbuster')
def tmdb_movies_play_random_blockbuster():
	result = {}
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.update(tmdb_movies_blockbusters(i, raw=True))
	tmdb_movies_play_random(result)

@plugin.route('/movies/tmdb/now_playing/<page>/')
def tmdb_movies_now_playing(page, raw=False):
	from resources.lib.TheMovieDB import Movies
	result = Movies().now_playing(language='en', page=page, append_to_response='external_ids,videos')
	if raw:
		return result
	else:
		return list_tmdb_movies(result)

@plugin.route('/movies/tmdb/random_now_playing')
def tmdb_movies_play_random_now_playing():
	result = {}
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.update(tmdb_movies_now_playing(i, raw=True))
	tmdb_movies_play_random(result)


@plugin.route('/movies/tmdb/popular/<page>/')
def tmdb_movies_popular(page, raw=False):
	from resources.lib.TheMovieDB import Movies
	result = Movies().popular(language='en', page=page)
	if raw:
		return result
	else:
		return list_tmdb_movies(result)

@plugin.route('/movies/tmdb/random_popular')
def tmdb_movies_play_random_popular():
	result = {}
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.update(tmdb_movies_popular(i, raw=True))
	tmdb_movies_play_random(result)


@plugin.route('/movies/tmdb/top_rated/<page>/')
def tmdb_movies_top_rated(page, raw=False):
	from resources.lib.TheMovieDB import Movies
	result = Movies().top_rated(language='en', page=page, append_to_response='external_ids,videos')
	if raw:
		return result
	else:
		return list_tmdb_movies(result)

@plugin.route('/movies/tmdb/random_top_rated')
def tmdb_movies_play_random_top_rated():
	result = {}
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.update(tmdb_movies_top_rated(i, raw=True))
	tmdb_movies_play_random(result)

@plugin.route('/movies/trakt/search/<term>/<page>/')
def trakt_movies_search_term(term, page):
	results, pages = Trakt.search_for_movie_paginated(term, page)
	return list_trakt_search_items(results, pages, page)

@plugin.route('/movies/trakt/latest_releases')
def trakt_movies_latest_releases(raw=False):
	results = sorted(Trakt.get_latest_releases_movies(), key=lambda k: k['listed_at'], reverse=True)
	if raw:
		return results
	else:
		return list_trakt_movies(results)

@plugin.route('/movies/trakt/random_latest_releases')
def trakt_movies_play_random_latest_releases():
	results = trakt_movies_latest_releases(raw=True)
	trakt_movies_play_random(results)

@plugin.route('/movies/trakt/imdb_top_rated_movies/<page>/')
def trakt_movies_imdb_top_rated(page, raw=False):
	results, pages = Trakt.get_imdb_top_rated_movies(page)
	if raw:
		return results
	else:
		return list_trakt_movies(results, pages, page)

@plugin.route('/movies/trakt/random_imdb_top_rated')
def trakt_movies_play_random_imdb_top_rated():
	result = []
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.extend(trakt_movies_imdb_top_rated(i, raw=True))
	trakt_movies_play_random(result)

@plugin.route('/movies/trakt/watched/<page>/')
def trakt_movies_watched(page, raw=False):
	results, pages = Trakt.get_watched_movies_paginated(page)
	if raw:
		return results
	else:
		return list_trakt_movies(results, pages, page)

@plugin.route('/movies/trakt/random_watched')
def trakt_movies_play_random_watched():
	result = []
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.extend(trakt_movies_watched(i, raw=True))
	trakt_movies_play_random(result)

@plugin.route('/movies/trakt/collected/<page>/')
def trakt_movies_collected(page, raw=False):
	results, pages = Trakt.get_collected_movies_paginated(page)
	if raw:
		return results
	else:
		return list_trakt_movies(results, pages, page)

@plugin.route('/movies/trakt/random_collected')
def trakt_movies_play_random_collected():
	result = []
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.extend(trakt_movies_collected(i, raw=True))
	trakt_movies_play_random(result)

@plugin.route('/movies/trakt/popular/<page>/')
def trakt_movies_popular(page, raw=False):
	results, pages = Trakt.get_popular_movies_paginated(page)
	if raw:
		return results
	else:
		return list_trakt_movies([{u'movie': m} for m in results], pages, page)

@plugin.route('/movies/trakt/random_popular') 
def trakt_movies_play_random_popular():
	result = []
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.extend(trakt_movies_popular(i, raw=True))
	trakt_movies_play_random(result)


@plugin.route('/movies/trakt/trending/<page>/')
def trakt_movies_trending(page, raw=False):
	results, pages = Trakt.get_trending_movies_paginated(page)
	if raw:
		return results
	else:
		return list_trakt_movies(results, pages, page)

@plugin.route('/movies/trakt/random_trending')
def trakt_movies_play_random_trending():
	result = []
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.extend(trakt_movies_trending(i, raw=True))
	trakt_movies_play_random(result)


@plugin.route('/movies/tmdb/search_term/<term>/<page>/')
def tmdb_movies_search_term(term, page):
	from resources.lib.TheMovieDB import Search
	result = Search().movie(query=term, language='en', page=page, append_to_response='external_ids,videos')
	return list_tmdb_items(result)

@plugin.route('/movies/trakt/person/<person_id>')
def trakt_movies_person(person_id, raw=False):
	result = Trakt.get_person_movies(person_id)['cast']
	if raw:
		return result
	else:
		return list_trakt_persons(result)

@plugin.route('/movies_genres')
def tmdb_movies_genres():
	genres = nav_base.get_base_genres()
	items = sorted([
		{
			'label': name,
			'path': plugin.url_for('tmdb_movies_genre', id=id, page=1),
			'thumbnail': nav_base.get_genre_icon(id),
			'fanart': plugin.get_addon_fanart(),
			'context_menu': [
				('Play (random)', 'RunPlugin(%s)' % plugin.url_for('tmdb_movies_play_random_genre', id = id))]
		} for id, name in genres.items()], key=lambda k: k['label'])
	return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/movies/genre/<id>/<page>/')
def tmdb_movies_genre(id, page, raw=False):
	from resources.lib.TheMovieDB import Genres
	result = Genres(id).movies(id=id, language='en', page=page)
	if raw:
		return result
	else:
		return list_tmdb_movies(result)

@plugin.route('/movies/tmdb/random_genre/<id>')
def tmdb_movies_play_random_genre(id):
	result = {}
	pages = plugin.get_setting('random_pages', int) + 1
	for i in range(1, pages):
		result.update(tmdb_movies_genre(id, i, raw=True))
	tmdb_movies_play_random(result)

@plugin.route('/movies/add_to_library/<src>/<id>')
def movies_add_to_library(src, id):
	from resources.lib.TheMovieDB import Movies
	library_folder = lib_movies.setup_library(plugin.get_setting('movies_library_folder', unicode))
	if library_folder == False:
		return
	date = None
	if src == 'tmdb':
		movie = Movies(id).info()
		date = text.date_to_timestamp(movie.get('release_date'))
		imdb_id = movie.get('imdb_id')
		if imdb_id:
			src = 'imdb'
			id = imdb_id
			ids = [str(movie.get('id')), str(movie.get('imdb_id', None))]
			try:
				libmovies = RPC.VideoLibrary.GetMovies(properties=['imdbnumber', 'title', 'year'])['movies']
				libmovies = [i for i in libmovies if str(i['imdbnumber']) in ids or (str(i['year']) == str(movie.get('year', 0)) and equals(movie.get['title'], i['title']))]
				libmovie = libmovies[0]
			except:
				libmovie = []
	else:
		ids = [str(id), 'None']
		try:
			libmovies = RPC.VideoLibrary.GetMovies(properties=['imdbnumber', 'title', 'year'])['movies']
			libmovies = [i for i in libmovies if str(i['imdbnumber']) in ids]
			libmovie = libmovies[0]
		except:
			libmovie = []
	if libmovie != []:
		return
	lib_movies.add_movie_to_library(library_folder, src, id)
	tools.scan_library(path=plugin.get_setting('movies_library_folder', unicode))

@plugin.route('/movies/add_to_library_parsed/<src>/<id>/<player>')
def movies_add_to_library_parsed(src, id, player):
	from resources.lib.TheMovieDB import Movies
	library_folder = lib_movies.setup_library(plugin.get_setting('movies_library_folder', unicode))
	date = None
	if src == 'tmdb':
		movie = Movies(id).info()
		date = text.date_to_timestamp(movie.get('release_date'))
		imdb_id = movie.get('imdb_id')
		if imdb_id:
			if imdb_id != None and imdb_id != '':
				src = 'imdb'
				id = imdb_id
	lib_movies.add_movie_to_library(library_folder, src, id, player)
	tools.scan_library(path=plugin.get_setting('movies_library_folder', unicode))

def movies_add_all_to_library(items, noscan=False):
	library_folder = lib_movies.setup_library(plugin.get_setting('movies_library_folder', unicode))
	if 'results' in items:
		ids = '\n'.join([str(r['id']) for r in items['results']])
	else:
		ids = '\n'.join([i['movie']['ids']['imdb'] if i['movie']['ids']['imdb'] != None and i['movie']['ids']['imdb'] != '' else str(i['movie']['ids']['tmdb']) for i in items])
	movies_batch_add_file = plugin.get_setting('movies_batch_add_file_path', unicode)
	if xbmcvfs.exists(movies_batch_add_file):
		batch_add_file = xbmcvfs.File(movies_batch_add_file)
		pre_ids = batch_add_file.read()
		xids = pre_ids.split('\n')
		for id in xids:
			if id != '' and id != None and id not in ids:
				ids = ids + str(id) + '\n'
		batch_add_file.close()
		xbmcvfs.delete(movies_batch_add_file)
	batch_add_file = xbmcvfs.File(movies_batch_add_file, 'w')
	batch_add_file.write(str(ids))
	batch_add_file.close()
	xbmc.executebuiltin('RunPlugin(plugin://plugin.video.openmeta/movies/batch_add_to_library)')

@plugin.route('/movies/batch_add_to_library')
def movies_batch_add_to_library():
	from resources.lib.TheMovieDB import Movies
	movie_batch_file = plugin.get_setting('movies_batch_add_file_path', unicode)
	if xbmcvfs.exists(movie_batch_file):
		try:
			f = open(xbmc.translatePath(movie_batch_file), 'r')
			r = f.read()
			f.close()
			ids = r.split('\n')
		except:
			plugin.notify('Movies', 'not found', plugin.get_addon_icon(), 3000)
		library_folder = lib_movies.setup_library(plugin.get_setting('movies_library_folder', unicode))
		for id in ids:
			if ',' in id:
				csvs = id.split(',')
				for csv in csvs:
					if not str(csv).startswith('tt') and csv != '':
						movie = Movies(csv).info()
						csv = movie.get('imdb_id')
					lib_movies.batch_add_movies_to_library(library_folder, csv)
			else:
				if not str(id).startswith('tt') and id != '':
					movie = Movies(id).info()
					id = movie.get('imdb_id')
				lib_movies.batch_add_movies_to_library(library_folder, id)
		os.remove(xbmc.translatePath(movie_batch_file))
		lib_movies.update_library()
		return True

def list_tmdb_movies(result):
	genres_dict = nav_base.get_base_genres()
	movies = [meta_info.get_movie_metadata(item, genres_dict) for item in result['results']]
	items = [make_movie_item(movie) for movie in movies]
	if 'page' in result:
		page = int(result['page'])
		pages = int(result['total_pages'])
		args = nav_base.caller_args()
		if pages > page:
			args['page'] = page + 1
			args['confirm'] = 'yes'
			items.append(
				{
					'label': '%s/%s  [I]Next page[/I]  >>' % (page, pages + 1),
					'path': plugin.url_for(nav_base.caller_name(), **args),
					'thumbnail': plugin.get_media_icon('item_next'),
					'fanart': plugin.get_addon_fanart()
				})
	return plugin.finish(items=items, sort_methods=SORT)

def list_tmdb_items(result):
	genres_dict = nav_base.get_base_genres()
	movies = [meta_info.get_movie_metadata(item, None) for item in result['results']]
	items = [make_movie_item(movie) for movie in movies]
	if 'page' in result:
		page = int(result['page'])
		pages = int(result['total_pages'])
		args = nav_base.caller_args()
		if pages > page:
			args['page'] = page + 1
			items.append(
				{
					'label': '%s/%s  [I]Next page[/I]  >>' % (page, pages + 1),
					'path': plugin.url_for(nav_base.caller_name(), **args),
					'thumbnail': plugin.get_media_icon('item_next'),
					'fanart': plugin.get_addon_fanart()
				})
	return plugin.finish(items=items, sort_methods=SORT)

def list_trakt_persons(results):
	genres_dict = dict([(x['slug'], x['name']) for x in Trakt.get_genres('movies')])
	movies = [meta_info.get_trakt_movie_metadata(item['movie'], genres_dict) for item in results]
	items = [make_movie_item(movie) for movie in movies]
	return items

def list_trakt_search_items(results, pages, page):
	movies = [meta_info.get_trakt_movie_metadata(item['movie'], None) for item in results]
	items = [make_movie_item(movie) for movie in movies]
	page = int(page)
	pages = int(pages)
	if pages > 1:
		args = nav_base.caller_args()
		args['page'] = page + 1
		items.append(
			{
				'label': '%s/%s  [I]Next page[/I]  >>' % (page, pages + 1),
				'path': plugin.url_for(nav_base.caller_name(), **args),
				'thumbnail': plugin.get_media_icon('item_next'),
				'fanart': plugin.get_addon_fanart()
			})
	return items

def list_trakt_movies(results, pages=1, page=1):
	genres_dict = dict([(x['slug'], x['name']) for x in Trakt.get_genres('movies')])
	try:
		movies = [meta_info.get_trakt_movie_metadata(item['movie'], genres_dict) for item in results]
	except KeyError:
		movies = [meta_info.get_trakt_movie_metadata(item, genres_dict) for item in results]
	items = [make_movie_item(movie) for movie in movies]
	page = int(page)
	pages = int(pages)
	if pages > 1:
		args = nav_base.caller_args()
		args['page'] = page + 1
		args['confirm'] = 'yes'
		items.append(
			{
				'label': '%s/%s  [I]Next page[/I]  >>' % (page, pages + 1),
				'path': plugin.url_for(nav_base.caller_name(), **args),
				'thumbnail': plugin.get_media_icon('item_next'),
				'fanart': plugin.get_addon_fanart()
			})
	return plugin.finish(items=items, sort_methods=SORTRAKT)

@plugin.route('/movies/play_choose_player/<src>/<id>/<usedefault>')
def movies_play_choose_player(src, id, usedefault):
	from resources.lib.TheMovieDB import Find
	tmdb_id = None
	if src == 'tmdb':
		tmdb_id = id
	elif src == 'imdb':
		info = Find(id).info(external_source='imdb_id')
		tmdb_id = info['movie_results'][0]['id']
	if not tmdb_id:
		plugin.notify('tmdb id', 'not found', plugin.get_addon_icon(), 3000)
	play_movies.play_movie(tmdb_id, usedefault)	

@plugin.route('/movies/play/<src>/<id>')
def movies_play(src, id, usedefault='True'):
	playaction = plugin.get_setting('movies_default_action', int)
	if playaction == 1 and xbmc.getCondVisibility('system.hasaddon(script.extendedinfo)') and not plugin.getProperty('infodialogs.active'):
		from resources.lib.play_base import action_cancel
		action_cancel()
		src = 'id' if src == 'tmdb' else 'imdb_id'
		xbmc.executebuiltin('RunScript(script.extendedinfo,info=extendedinfo,%s=%s)' % (src, id))
	else:
		movies_play_choose_player(src, id, usedefault)

@plugin.route('/movies/play_by_name/<name>/<lang>')
def movies_play_by_name(name, lang='en', usedefault='True'):
	tools.show_busy()
	from resources.lib.TheMovieDB import Search
	items = Search().movie(query=name, language=lang, page=1)['results']
	if not items:
		tools.hide_busy()
		plugin.ok('Movie not found', 'No information found for ' + name)
	if len(items) > 1:
		selection = plugin.select('Movie', ['%s (%s)' % ((s['title']), text.parse_year(s['release_date'])) for s in items])
	else:
		selection = 0
	tools.hide_busy()
	if selection != -1:
		id = items[selection]['id']
		movies_play_choose_player('tmdb', id, usedefault)

@plugin.route('/movies/play_by_name_choose_player/<name>/<lang>/<usedefault>')
def movies_play_by_name_choose_player(name, lang='en', usedefault='False'):
	movies_play_by_name(name, lang, usedefault)

def trakt_movies_play_random(movies, convert_list=False):
	for movie in movies:
		movie['type'] = 'movie'
		if convert_list:
			movie['movie'] = movie
	playrandom.trakt_play_random(movies)

def tmdb_movies_play_random(list):
	movies = list['results']
	for movie in movies:
		movie['type'] = 'movie'
	playrandom.tmdb_play_random(movies)

def make_movie_item(movie_info):
	try:
		tmdb_id = movie_info.get('tmdb')
	except:
		tmdb_id = ''
	if tmdb_id == '': 
		try:
			tmdb_id = info['tmdb']
		except:
			tmdb_id = False
	try:
		imdb_id = movie_info.get('imdbnumber')
	except:
		imdb_id = ''
	if imdb_id == '':
		try:
			imdb_id = info['imdb_id']
		except:
			imdb_id = False
	if tmdb_id:
		id = tmdb_id 
		src = 'tmdb'
	elif imdb_id:
		id = imdb_id 
		src = 'imdb'
	else:
		plugin.notify('tmdb or imdb id', 'not found', plugin.get_addon_icon(), 3000)
	if xbmc.getCondVisibility('system.hasaddon(script.extendedinfo)'):
		context_menu = [
			('Movie trailer', 'RunScript(script.extendedinfo,info=playtrailer,id=%s)' % id),
			('Add to library','RunPlugin(%s)' % plugin.url_for('movies_add_to_library', src=src, id=id))]
	else:
		context_menu = [
			('Add to library','RunPlugin(%s)' % plugin.url_for('movies_add_to_library', src=src, id=id))]
	try:
		if traktenabled and countenabled:
			if 'trakt_id' in movie_info.keys() and movie_info['trakt_id'] != '':
				movie_id = movie_info['trakt_id']
			elif tmdb_id != '':
				movie_id = Trakt.find_trakt_ids('tmdb', tmdb_id, 'movie')['trakt']
			else:
				movie_id = Trakt.find_trakt_ids('imdb', imdb_id, 'movie')['trakt']
			playdata = Trakt.get_movie_history(movie_id)
			movie_info.update({'playcount': len([k for d in playdata for k in d.keys() if k == 'watched_at'])})
	except:
		pass
	movieitem = {
		'label': movie_info['title'],
		'path': plugin.url_for('movies_play', src=src, id=id, usedefault=True),
		'context_menu': context_menu,
		'thumbnail': movie_info['poster'],
		'banner': movie_info['fanart'],
		'poster': movie_info['poster'],
		'fanart': movie_info['fanart'],
		'is_playable': True,
		'info_type': 'video',
		'stream_info': {'video': {}},
		'info': movie_info
		}
	if enablefanart:
		try:
			art = get_fanarttv_art(id)
			art = checkart(art)
			movieitem.update(art)
		except:
			pass
	return movieitem

def checkart(item):
	art = {}
	for key, val in item.items():
		if val != '':
			art.update({key: val})
	return art

def get_fanarttv_art(id, query='movies', season=False):
	return fanarttv.get(id, query, season)

@plugin.route('/my_trakt/movie_lists/movies/recommendations')
def trakt_movies_recommendations(raw=False):
	result = Trakt.get_recommendations('movies')
	if raw:
		return result
	else:
		return list_trakt_movies(result, '1', '1')

@plugin.route('/my_trakt/movie_lists/movies/watchlist')
def trakt_movies_watchlist(raw=False):
	result = Trakt.get_watchlist('movies')
	if raw:
		return result
	else:
		return list_trakt_movies(result, '1', '1')

@plugin.route('/my_trakt/movie_lists/movies/watchlist/movies_play_random')
def trakt_movies_play_random_watchlist():
	trakt_movies_play_random(trakt_movies_watchlist(raw=True))

@plugin.route('/my_trakt/movie_list/trakt_my_movie_lists')
def lists_trakt_my_movie_lists():
	lists = Trakt.get_lists()
	items = []
	for list in lists:
		name = list['name']
		user = list['user']['username']
		slug = list['ids']['slug']
		items.append(
			{
				'label': name,
				'path': plugin.url_for('lists_trakt_show_movie_list', user=user, slug=slug),
				'thumbnail': plugin.get_media_icon('traktmylists'),
				'fanart': plugin.get_addon_fanart()
			})
	return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/my_trakt/movie_list/trakt_liked_movie_list/<page>/')
def lists_trakt_liked_movie_lists(page):
	lists, pages = Trakt.get_liked_lists(page)
	items = []
	for list in lists:
		info = list['list']
		name = info['name']
		user = info['user']['username']
		slug = info['ids']['slug']
		items.append(
			{
				'label': name,
				'path': plugin.url_for('lists_trakt_show_movie_list', user=user, slug=slug),
				'thumbnail': plugin.get_media_icon('traktlikedlists'),
				'fanart': plugin.get_addon_fanart()
			})
	nextpage = int(page) + 1
	if pages > page:
		items.append(
			{
				'label': '%s/%s  [I]Next page[/I]  >>' % (nextpage, pages),
				'path': plugin.url_for('lists_trakt_liked_movie_lists', page=int(page) + 1),
				'thumbnail': plugin.get_media_icon('item_next'),
				'fanart': plugin.get_addon_fanart()
			})
	return plugin.finish(items=items, sort_methods=SORT)

@plugin.route('/my_trakt/movie_lists/movies/collection')
def lists_trakt_movies_collection(raw=False):
	results = sorted(Trakt.get_collection('movies'), key=lambda k: k['collected_at'], reverse=True)
	if raw:
		return results
	movies = [meta_info.get_trakt_movie_metadata(item['movie']) for item in results]
	items = [make_movie_item(movie) for movie in movies]
	return items

@plugin.route('/my_trakt/movie_lists/movies/collection/movies_to_library')
def lists_trakt_movies_collection_to_library():
	movies_add_all_to_library(Trakt.get_collection('movies'))

@plugin.route('/my_trakt/movie_lists/movies/collection/movies_play_random')
def lists_trakt_movies_play_random_collection():
	movies = lists_trakt_movies_collection(raw=True)
	for movie in movies:
		movie['type'] = 'movie'
	playrandom.trakt_play_random(movies)

@plugin.route('/my_trakt/movie_list/movies/show_list/<user>/<slug>')
def lists_trakt_show_movie_list(user, slug, raw=False):
	list_items = Trakt.get_list(user, slug)
	if raw:
		return list_items
	return _lists_trakt_show_movie_list(list_items)

@plugin.route('/my_trakt/movie_list/play_random/<user>/<slug>')
def lists_trakt_movies_play_random(user, slug):
	items = lists_trakt_show_movie_list(user, slug, raw=True)
	playrandom.trakt_play_random(items)

@plugin.route('/my_trakt/movie_list/movies/_show_list/<list_items>')
def _lists_trakt_show_movie_list(list_items):
	from resources.lib.TheMovieDB import People
	items = []
	for list_item in list_items:
		item = None
		item_type = list_item['type']
		if item_type == 'movie':
			movie = list_item['movie']
			movie_info = meta_info.get_trakt_movie_metadata(movie)
			try:
				tmdb_id = movie_info['tmdb']
			except:
				tmdb_id = ''
			try:
				imdb_id = movie_info['imdb']
			except:
				imdb_id = ''
			if tmdb_id != None and tmdb_id != '':
				src = 'tmdb'
				id = tmdb_id
			elif imdb_id != None and mdb_id != '':
				src = 'imdb'
				id = imdb_id
			else:
				src = ''
				id = ''
			if src == '':
				item = None
			item = make_movie_item(movie_info)
		elif item_type == 'person':
			person_id = list_item['person']['ids']['trakt']
			person_tmdb_id = list_item['person']['ids']['tmdb']
			try:
				person_images = People(person_tmdb_id).images()['profiles']
				person_image = 'https://image.tmdb.org/t/p/w640' + person_images[0]['file_path']
			except:
				person_image = ''
			person_name = text.to_utf8(list_item['person']['name'])
			item = (
				{
					'label': person_name,
					'path': plugin.url_for('trakt_movies_person', person_id=person_id),
					'thumbnail': person_image,
					'poster': person_image,
					'fanart': plugin.get_addon_fanart()
				})
		if item is not None:
			items.append(item)
	return items