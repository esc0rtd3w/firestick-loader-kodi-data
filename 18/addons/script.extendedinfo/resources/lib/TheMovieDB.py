import re
import xbmc, xbmcgui, xbmcaddon
from resources.lib import Utils
from resources.lib import local_db
from resources.lib.WindowManager import wm

ext_key = xbmcaddon.Addon().getSetting('tmdb_api')

if len(ext_key) == 32:
	API_key = ext_key
else:
	API_key = '1248868d7003f60f2386595db98455ef'

def get_certification_list(media_type):
	response = get_tmdb_data('certification/%s/list?' % media_type, 999999)
	if 'certifications' in response:
		return response['certifications']
	else:
		return []

def merge_with_cert_desc(input_list, media_type):
	cert_list = get_certification_list(media_type)
	for item in input_list:
		if item['iso_3166_1'].upper() not in cert_list:
			continue
		hit = Utils.dictfind(lst=cert_list[item['iso_3166_1'].upper()], key='certification', value=item['certification'])
		if hit:
			item['meaning'] = hit['meaning']
	return input_list

def handle_tmdb_multi_search(results=[]):
	listitems = []
	for item in results:
		if item['media_type'] == 'movie':
			listitem = handle_tmdb_movies([item])[0]
		elif item['media_type'] == 'tv':
			listitem = handle_tmdb_tvshows([item])[0]
		else:
			listitem = handle_tmdb_people([item])[0]
		listitems.append(listitem)
	return listitems

def handle_tmdb_movies(results=[], local_first=True, sortkey='year'):
	response = get_tmdb_data('genre/movie/list?language=%s&' % xbmcaddon.Addon().getSetting('LanguageID'), 30)
	id_list = [item['id'] for item in response['genres']]
	label_list = [item['name'] for item in response['genres']]
	movies = []
	for movie in results:
		if 'genre_ids' in movie:
			genre_list = [label_list[id_list.index(genre_id)] for genre_id in movie['genre_ids'] if genre_id in id_list]
			genres = ' / '.join(genre_list)
		else:
			genres = ''
		tmdb_id = str(Utils.fetch(movie, 'id'))
		artwork = get_image_urls(poster=movie.get('poster_path'), fanart=movie.get('backdrop_path'))
		trailer = 'plugin://script.extendedinfo?info=playtrailer&&id=%s' % tmdb_id
		path = 'plugin://script.extendedinfo?info=extendedinfo&&id=%s' % tmdb_id
		listitem = {
			'title': Utils.fetch(movie, 'title'),
			'Label': Utils.fetch(movie, 'title'),
			'OriginalTitle': Utils.fetch(movie, 'original_title'),
			'id': tmdb_id,
			'path': path,
			'media_type': 'movie',
			'mediatype': 'movie',
			'country': Utils.fetch(movie, 'original_language'),
			'plot': Utils.fetch(movie, 'overview'),
			'Trailer': trailer,
			'Popularity': Utils.fetch(movie, 'popularity'),
			'Rating': Utils.fetch(movie, 'vote_average'),
			'credit_id': Utils.fetch(movie, 'credit_id'),
			'character': Utils.fetch(movie, 'character'),
			'job': Utils.fetch(movie, 'job'),
			'department': Utils.fetch(movie, 'department'),
			'Votes': Utils.fetch(movie, 'vote_count'),
			'User_Rating': Utils.fetch(movie, 'rating'),
			'year': Utils.get_year(Utils.fetch(movie, 'release_date')),
			'genre': genres,
			'Premiered': Utils.fetch(movie, 'release_date')
			}
		listitem.update(artwork)
		date = Utils.fetch(movie, 'release_date')
		movies.append(listitem)
	movies = local_db.merge_with_local_movie_info(movies, local_first, sortkey)
	return movies

def handle_tmdb_tvshows(results, local_first=True, sortkey='year'):
	tvshows = []
	response = get_tmdb_data('genre/tv/list?language=%s&' % xbmcaddon.Addon().getSetting('LanguageID'), 30)
	id_list = [item['id'] for item in response['genres']]
	label_list = [item['name'] for item in response['genres']]
	for tv in results:
		tmdb_id = Utils.fetch(tv, 'id')
		artwork = get_image_urls(poster=tv.get('poster_path'), fanart=tv.get('backdrop_path'))
		if 'genre_ids' in tv:
			genre_list = [label_list[id_list.index(genre_id)] for genre_id in tv['genre_ids'] if genre_id in id_list]
			genres = ' / '.join(genre_list)
		else:
			genres = ''
		duration = ''
		if 'episode_run_time' in tv:
			if len(tv['episode_run_time']) > 1:
				duration = '%i - %i' % (min(tv['episode_run_time']), max(tv['episode_run_time']))
			elif len(tv['episode_run_time']) == 1:
				duration = '%i' % tv['episode_run_time'][0]
		newtv = {
			'title': Utils.fetch(tv, 'name'),
			'TVShowTitle': Utils.fetch(tv, 'name'),
			'OriginalTitle': Utils.fetch(tv, 'original_name'),
			'duration': duration,
			'id': tmdb_id,
			'genre': genres,
			'country': Utils.fetch(tv, 'original_language'),
			'Popularity': Utils.fetch(tv, 'popularity'),
			'credit_id': Utils.fetch(tv, 'credit_id'),
			'Plot': Utils.fetch(tv, 'overview'),
			'Trailer': 'plugin://script.extendedinfo?info=tvtrailer&&id=%s' % tmdb_id,
			'year': Utils.get_year(Utils.fetch(tv, 'first_air_date')),
			'media_type': 'tv',
			'mediatype': 'tvshow',
			'character': Utils.fetch(tv, 'character'),
			'path': 'plugin://script.extendedinfo?info=extendedtvinfo&&id=%s' % tmdb_id,
			'Rating': Utils.fetch(tv, 'vote_average'),
			'User_Rating': str(Utils.fetch(tv, 'rating')),
			'Votes': Utils.fetch(tv, 'vote_count'),
			'TotalEpisodes': Utils.fetch(tv, 'number_of_episodes'),
			'TotalSeasons': Utils.fetch(tv, 'number_of_seasons'),
			'Release_Date': Utils.fetch(tv, 'first_air_date'),
			'Premiered': Utils.fetch(tv, 'first_air_date')
			}
		newtv.update(artwork)
		date = Utils.fetch(tv, 'first_air_date')
		tvshows.append(newtv)
	tvshows = local_db.merge_with_local_tvshow_info(tvshows, local_first, sortkey)
	return tvshows

def handle_tmdb_seasons(results):
	listitems = []
	for season in results:
		season_number = str(Utils.fetch(season, 'season_number'))
		artwork = get_image_urls(poster=season.get('poster_path'))
		title = 'Specials' if season_number == '0' else u'Season %s' % season_number
		listitem = {
			'media_type': 'season',
			'mediatype': 'season',
			'title': title,
			'season': season_number,
			'air_date': Utils.fetch(season, 'air_date'),
			'year': Utils.get_year(Utils.fetch(season, 'air_date')),
			'id': Utils.fetch(season, 'id')
			}
		listitem.update(artwork)
		listitems.append(listitem)
	return listitems

def handle_tmdb_episodes(results):
	listitems = []
	for item in results:
		title = Utils.clean_text(Utils.fetch(item, 'name'))
		if not title:
			title = '%s %s' % ('Episode', Utils.fetch(item, 'episode_number'))
		try:
			artwork = get_image_urls(still=item.get('still_path'))
		except:
			artwork = []
		listitem = {
			'media_type': 'episode',
			'mediatype': 'episode',
			'title': title,
			'release_date': Utils.fetch(item, 'air_date'),
			'episode': Utils.fetch(item, 'episode_number'),
			'production_code': Utils.fetch(item, 'production_code'),
			'season': Utils.fetch(item, 'season_number'),
			'Rating': round(float(Utils.fetch(item, 'vote_average')), 1),
			'Votes': Utils.fetch(item, 'vote_count'),
			'Plot': Utils.fetch(item, 'overview'),
			'id': Utils.fetch(item, 'id'),
			'Description': Utils.clean_text(Utils.fetch(item, 'overview'))
			}
		listitem.update(artwork)
		date = Utils.fetch(item, 'air_date')
		listitems.append(listitem)
	return listitems

def handle_tmdb_misc(results):
	listitems = []
	for item in results:
		artwork = get_image_urls(poster=item.get('poster_path'))
		listitem = {
			'title': Utils.clean_text(Utils.fetch(item, 'name')),
			'certification': Utils.fetch(item, 'certification') + Utils.fetch(item, 'rating'),
			'item_count': Utils.fetch(item, 'item_count'),
			'release_date': Utils.fetch(item, 'release_date'),
			'path': 'plugin://script.extendedinfo?info=listmovies&---id=%s' % Utils.fetch(item, 'id'),
			'year': Utils.get_year(Utils.fetch(item, 'release_date')),
			'iso_3166_1': Utils.fetch(item, 'iso_3166_1').lower(),
			'author': Utils.fetch(item, 'author'),
			'content': Utils.clean_text(Utils.fetch(item, 'content')),
			'id': Utils.fetch(item, 'id'),
			'url': Utils.fetch(item, 'url'),
			'Description': Utils.clean_text(Utils.fetch(item, 'description'))
			}
		listitem.update(artwork)
		listitems.append(listitem)
	return listitems

def handle_tmdb_videos(results):
	listitems = []
	for item in results:
		image = 'https://i.ytimg.com/vi/%s/0.jpg' % Utils.fetch(item, 'key')
		listitem = {
			'thumb': image,
			'title': Utils.fetch(item, 'name'),
			'iso_639_1': Utils.fetch(item, 'iso_639_1'),
			'type': Utils.fetch(item, 'type'),
			'key': Utils.fetch(item, 'key'),
			'youtube_id': Utils.fetch(item, 'key'),
			'site': Utils.fetch(item, 'site'),
			'id': Utils.fetch(item, 'id'),
			'size': Utils.fetch(item, 'size')
			}
		listitems.append(listitem)
	return listitems

def handle_tmdb_people(results):
	people = []
	for person in results:
		artwork = get_image_urls(profile=person.get('profile_path'))
		also_known_as = ' / '.join(Utils.fetch(person, 'also_known_as'))
		newperson = {
			'adult': str(Utils.fetch(person, 'adult')),
			'name': person['name'],
			'title': person['name'],
			'also_known_as': also_known_as,
			'alsoknownas': also_known_as,
			'biography': Utils.clean_text(Utils.fetch(person, 'biography')),
			'birthday': Utils.fetch(person, 'birthday'),
			'age': Utils.calculate_age(Utils.fetch(person, 'birthday'), Utils.fetch(person, 'deathday')),
			'character': Utils.fetch(person, 'character'),
			'department': Utils.fetch(person, 'department'),
			'job': Utils.fetch(person, 'job'),
			'media_type': 'person',
			'id': str(person['id']),
			'cast_id': str(Utils.fetch(person, 'cast_id')),
			'credit_id': str(Utils.fetch(person, 'credit_id')),
			'path': 'plugin://script.extendedinfo?info=extendedactorinfo&&id=%s' % str(person['id']),
			'deathday': Utils.fetch(person, 'deathday'),
			'place_of_birth': Utils.fetch(person, 'place_of_birth'),
			'placeofbirth': Utils.fetch(person, 'place_of_birth'),
			'homepage': Utils.fetch(person, 'homepage')
			}
		newperson.update(artwork)
		people.append(newperson)
	return people

def handle_tmdb_images(results):
	images = []
	for item in results:
		artwork = get_image_urls(poster=item.get('file_path'))
		image = {
			'aspectratio': item['aspect_ratio'],
			'vote_average': Utils.fetch(item, 'vote_average'),
			'iso_639_1': Utils.fetch(item, 'iso_639_1')
			}
		image.update(artwork)
		images.append(image)
	return images

def handle_tmdb_tagged_images(results):
	images = []
	for item in results:
		artwork = get_image_urls(poster=item.get('file_path'))
		image = {
			'aspectratio': item['aspect_ratio'],
			'vote_average': Utils.fetch(item, 'vote_average'),
			'iso_639_1': Utils.fetch(item, 'iso_639_1'),
			'title': Utils.fetch(item['media'], 'title'),
			'mediaposter': 'https://image.tmdb.org/t/p/w500%s' % Utils.fetch(item['media'], 'poster_path')
			}
		image.update(artwork)
		images.append(image)
	return images

def search_company(company_name):
	regex = re.compile('\(.+?\)')
	company_name = regex.sub('', company_name)
	response = get_tmdb_data('search/company?query=%s&' % Utils.url_quote(company_name), 10)
	if response and 'results' in response:
		return response['results']
	else:
		return ''

def get_person_info(person_label):
	persons = person_label.split(' / ')
	response = get_tmdb_data('search/person?query=%s&include_adult=%s&' % (Utils.url_quote(persons[0]), xbmcaddon.Addon().getSetting('include_adults')), 30)
	if not response or 'results' not in response:
		return False
	if len(response['results']) > 1:
		listitem, index = wm.open_selectdialog(listitems=handle_tmdb_people(response['results']))
		if index >= 0:
			return response['results'][index]
	elif response['results']:
		return response['results'][0]
	return False

def get_keyword_id(keyword):
	response = get_tmdb_data('search/keyword?query=%s&include_adult=%s&' % (Utils.url_quote(keyword), xbmcaddon.Addon().getSetting('include_adults')), 30)
	if response and 'results' in response and response['results']:
		if len(response['results']) > 1:
			names = [item['name'] for item in response['results']]
			selection = xbmcgui.Dialog().select('Keyword', names)
			if selection > -1:
				return response['results'][selection]
		elif response['results']:
			return response['results'][0]
	else:
		return False

def get_set_id(set_name):
	set_name = set_name.replace('[', '').replace(']', '').replace('Kollektion', 'Collection')
	response = get_tmdb_data('search/collection?query=%s&language=%s&' % (Utils.url_quote(set_name.encode('utf-8')), xbmcaddon.Addon().getSetting('LanguageID')), 14)
	if 'results' in response and response['results']:
		return response['results'][0]['id']
	else:
		return ''

def get_tmdb_data(url='', cache_days=14, folder='TheMovieDB'):
	url = 'https://api.themoviedb.org/3/%sapi_key=%s' % (url, API_key)
	return Utils.get_JSON_response(url, cache_days, folder)

def get_company_data(company_id):
	response = get_tmdb_data('company/%s/movies?' % company_id, 30)
	if response and 'results' in response:
		return handle_tmdb_movies(response['results'])
	else:
		return []

def get_credit_info(credit_id):
	return get_tmdb_data('credit/%s?language=%s&' % (credit_id, xbmcaddon.Addon().getSetting('LanguageID')), 30)

def get_image_urls(poster=None, still=None, fanart=None, profile=None):
	images = {}
	if poster:
		images['poster'] = 'https://image.tmdb.org/t/p/w500' + poster
		images['poster_original'] = 'https://image.tmdb.org/t/p/original' + poster
		images['original'] = 'https://image.tmdb.org/t/p/original' + poster
		images['poster_small'] = 'https://image.tmdb.org/t/p/w342' + poster
		images['thumb'] = 'https://image.tmdb.org/t/p/w342' + poster
	if still:
		images['thumb'] = 'https://image.tmdb.org/t/p/w300' + still
		images['still'] = 'https://image.tmdb.org/t/p/w300' + still
		images['still_original'] = 'https://image.tmdb.org/t/p/original' + still
		images['still_small'] = 'https://image.tmdb.org/t/p/w185' + still
	if fanart:
		images['fanart'] = 'https://image.tmdb.org/t/p/w1280' + fanart
		images['fanart_original'] = 'https://image.tmdb.org/t/p/original' + fanart
		images['original'] = 'https://image.tmdb.org/t/p/original' + fanart
		images['fanart_small'] = 'https://image.tmdb.org/t/p/w780' + fanart
	if profile:
		images['poster'] = 'https://image.tmdb.org/t/p/w500' + profile
		images['poster_original'] = 'https://image.tmdb.org/t/p/original' + profile
		images['poster_small'] = 'https://image.tmdb.org/t/p/w342' + profile
		images['thumb'] = 'https://image.tmdb.org/t/p/w342' + profile
	return images

def get_movie_tmdb_id(imdb_id=None, name=None, dbid=None):
	if dbid and (int(dbid) > 0):
		movie_id = local_db.get_imdb_id_from_db('movie', dbid)
		Utils.log('IMDB Id from local DB: %s' % movie_id)
		response = get_tmdb_data('find/%s?external_source=imdb_id&language=%s&' % (movie_id, xbmcaddon.Addon().getSetting('LanguageID')), 30)
		if response['movie_results']:
			return response['movie_results'][0]['id']
		else:
			Utils.notify('Could not find TMDb-id 1')
			return None
	elif imdb_id:
		response = get_tmdb_data('find/%s?external_source=imdb_id&language=%s&' % (imdb_id, xbmcaddon.Addon().getSetting('LanguageID')), 30)
		if 'movie_results' in response:
			if response['movie_results'] != None and len(response['movie_results']) > 0:
				try:
					return response['movie_results'][0]['id']
				except: 
					Utils.notify('Could not find TMDb-id 2')
					return None
			else: 
				Utils.notify('Could not find TMDb-id 3')
				return None
	elif name:
		return search_media(name)
	else:
		Utils.notify('Could not find TMDb-id 4')
		return None

def get_show_tmdb_id(tvdb_id=None, db=None, imdb_id=None):
	if tvdb_id:
		id = tvdb_id
		db = 'tvdb_id'
	elif imdb_id:
		id = 'tt%s' % imdb_id
		db = 'imdb_id'
	response = get_tmdb_data('find/%s?external_source=%s&language=%s&' % (id, db, xbmcaddon.Addon().getSetting('LanguageID')), 30)
	if response:
		return response['tv_results'][0]['id']
	else:
		Utils.notify('TV Show info not found', time=5000, sound=False)
		return None

def get_trailer(movie_id):
	response = get_tmdb_data('movie/%s?append_to_response=videos,null,%s&language=%s&' % (movie_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID')), 30)
	if response and 'videos' in response and response['videos']['results']:
		return response['videos']['results'][0]['key']
	Utils.notify('Movie trailer not found', sound=False)
	return ''

def get_tvtrailer(tvshow_id):
	response = get_tmdb_data('tv/%s?append_to_response=videos,null,%s&language=%s&' % (tvshow_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID')), 30)
	if response and 'videos' in response and response['videos']['results']:
		return response['videos']['results'][0]['key']
	Utils.notify('TV Show trailer not found', sound=False)
	return ''

def play_movie_trailer(id):
	trailer = get_trailer(id)
	xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=%s,1)' % trailer)
	xbmc.executebuiltin('Dialog.Close(busydialog)')

def play_movie_trailer_fullscreen(id):
	trailer = get_trailer(id)
	xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=%s)' % trailer)

def play_tv_trailer(id):
	trailer = get_tvtrailer(id)
	xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=%s,1)' % trailer)
	xbmc.executebuiltin('Dialog.Close(busydialog)')

def play_tv_trailer_fullscreen(id):
	trailer = get_tvtrailer(id)
	xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=%s)' % trailer)

def extended_movie_info(movie_id=None, dbid=None, cache_time=14):
	if not movie_id:
		return None
	session_str = ''
	response = get_tmdb_data('movie/%s?append_to_response=alternative_titles,credits,images,keywords,releases,videos,translations,similar,reviews,rating&include_image_language=en,null,%s&language=%s&%s' % (movie_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID'), session_str), cache_time)
	if not response:
		Utils.notify('Could not get movie information', sound=False)
		return {}
	mpaa = ''
	set_name = ''
	set_id = ''
	genres = [i['name'] for i in response['genres']]
	Studio = [i['name'] for i in response['production_companies']]
	authors = [i['name'] for i in response['credits']['crew'] if i['department'] == 'Writing']
	directors = [i['name'] for i in response['credits']['crew'] if i['department'] == 'Directing']
	us_cert = Utils.dictfind(response['releases']['countries'], 'iso_3166_1', 'US')
	if us_cert:
		mpaa = us_cert['certification']
	elif response['releases']['countries']:
		mpaa = response['releases']['countries'][0]['certification']
	movie_set = Utils.fetch(response, 'belongs_to_collection')
	if movie_set:
		set_name = Utils.fetch(movie_set, 'name')
		set_id = Utils.fetch(movie_set, 'id')
	artwork = get_image_urls(poster=response.get('poster_path'), fanart=response.get('backdrop_path'))
	movie = {
		'media_type': 'movie',
		'mediatype': 'movie',
		'title': Utils.fetch(response, 'title'),
		'Label': Utils.fetch(response, 'title'),
		'Tagline': Utils.fetch(response, 'tagline'),
		'duration': Utils.fetch(response, 'runtime'),
		'duration(h)': Utils.format_time(Utils.fetch(response, 'runtime'), 'h'),
		'duration(m)': Utils.format_time(Utils.fetch(response, 'runtime'), 'm'),
		'duration(hm)': Utils.format_time(Utils.fetch(response, 'runtime')),
		'mpaa': mpaa,
		'Director': ' / '.join(directors),
		'writer': ' / '.join(authors),
		'Budget': Utils.millify(Utils.fetch(response, 'budget')),
		'Revenue': Utils.millify(Utils.fetch(response, 'revenue')),
		'Homepage': Utils.fetch(response, 'homepage'),
		'Set': set_name, 'SetId': set_id,
		'id': Utils.fetch(response, 'id'),
		'tmdb_id': Utils.fetch(response, 'id'),
		'imdb_id': Utils.fetch(response, 'imdb_id'),
		'Plot': Utils.clean_text(Utils.fetch(response, 'overview')),
		'OriginalTitle': Utils.fetch(response, 'original_title'),
		'Country': Utils.fetch(response, 'original_language'),
		'genre': ' / '.join(genres),
		'Rating': Utils.fetch(response, 'vote_average'),
		'Votes': Utils.fetch(response, 'vote_count'),
		'Adult': str(Utils.fetch(response, 'adult')),
		'Popularity': Utils.fetch(response, 'popularity'),
		'Status': translate_status(Utils.fetch(response, 'status')),
		'release_date': Utils.fetch(response, 'release_date'),
		'Premiered': Utils.fetch(response, 'release_date'),
		'Studio': ' / '.join(Studio),
		'year': Utils.get_year(Utils.fetch(response, 'release_date')),
		'path': 'plugin://script.extendedinfo?info=extendedinfo&&id=%s' % movie_id,
		'trailer': 'plugin://script.extendedinfo?info=playtrailer&&id=%s' % movie_id
		}
	movie.update(artwork)
	videos = handle_tmdb_videos(response['videos']['results']) if 'videos' in response else []
	if dbid:
		local_item = local_db.get_movie_from_db(dbid)
		movie.update(local_item)
	else:
		movie = local_db.merge_with_local_movie_info([movie])[0]
	movie['Rating'] = Utils.fetch(response, 'vote_average')
	listitems = {
		'actors': handle_tmdb_people(response['credits']['cast']),
		'similar': handle_tmdb_movies(response['similar']['results']),
		'studios': handle_tmdb_misc(response['production_companies']),
		'releases': handle_tmdb_misc(response['releases']['countries']),
		'crew': handle_tmdb_people(response['credits']['crew']),
		'genres': handle_tmdb_misc(response['genres']),
		'keywords': handle_tmdb_misc(response['keywords']['keywords']),
		'reviews': handle_tmdb_misc(response['reviews']['results']),
		'videos': videos,
		'images': handle_tmdb_images(response['images']['posters']),
		'backdrops': handle_tmdb_images(response['images']['backdrops'])
		}
	return (movie, listitems)

def extended_tvshow_info(tvshow_id=None, cache_time=7, dbid=None):
	if not tvshow_id:
		return None
	session_str = ''
	response = get_tmdb_data('tv/%s?append_to_response=alternative_titles,content_ratings,credits,external_ids,images,keywords,rating,similar,translations,videos&language=%s&include_image_language=en,null,%s&%s' % (tvshow_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID'), session_str), cache_time)
	if not response:
		return False
	videos = handle_tmdb_videos(response['videos']['results']) if 'videos' in response else []
	tmdb_id = Utils.fetch(response, 'id')
	external_ids = Utils.fetch(response, 'external_ids')
	if external_ids:
		imdb_id = Utils.fetch(external_ids, 'imdb_id')
		freebase_id = Utils.fetch(external_ids, 'freebase_id')
		tvdb_id = Utils.fetch(external_ids, 'tvdb_id')
		tvrage_id = Utils.fetch(external_ids, 'tvrage_id')
	artwork = get_image_urls(poster=response.get('poster_path'), fanart=response.get('backdrop_path'))
	if len(response.get('episode_run_time', -1)) > 1:
		duration = '%i - %i' % (min(response['episode_run_time']), max(response['episode_run_time']))
	elif len(response.get('episode_run_time', -1)) == 1:
		duration = '%i' % response['episode_run_time'][0]
	else:
		duration = ''
	us_cert = Utils.dictfind(response['content_ratings']['results'], 'iso_3166_1', 'US')
	if us_cert:
		mpaa = us_cert['rating']
	elif response['content_ratings']['results']:
		mpaa = response['content_ratings']['results'][0]['rating']
	else:
		mpaa = ''
	genres = [item['name'] for item in response['genres']]
	tvshow = {
		'title': Utils.fetch(response, 'name'),
		'TVShowTitle': Utils.fetch(response, 'name'),
		'OriginalTitle': Utils.fetch(response, 'original_name'),
		'duration': duration,
		'duration(h)': Utils.format_time(duration, 'h'),
		'duration(m)': Utils.format_time(duration, 'm'),
		'id': tmdb_id,
		'tmdb_id': tmdb_id,
		'imdb_id': imdb_id,
		'freebase_id': freebase_id,
		'tvdb_id': tvdb_id,
		'tvrage_id': tvrage_id,
		'mpaa': mpaa,
		'genre': ' / '.join(genres),
		'credit_id': Utils.fetch(response, 'credit_id'),
		'Plot': Utils.clean_text(Utils.fetch(response, 'overview')),
		'year': Utils.get_year(Utils.fetch(response, 'first_air_date')),
		'media_type': 'tv',
		'mediatype': 'tvshow',
		'Popularity': Utils.fetch(response, 'popularity'),
		'Rating': Utils.fetch(response, 'vote_average'),
		'country': Utils.fetch(response, 'original_language'),
		'User_Rating': str(Utils.fetch(response, 'rating')),
		'Votes': Utils.fetch(response, 'vote_count'),
		'Status': translate_status(Utils.fetch(response, 'status')),
		'path': 'plugin://script.extendedinfo?info=extendedtvinfo&&id=%s' % tvshow_id,
		'trailer': 'plugin://script.extendedinfo?info=playtvtrailer&&id=%s' % tvshow_id,
		'ShowType': Utils.fetch(response, 'type'),
		'homepage': Utils.fetch(response, 'homepage'),
		'last_air_date': Utils.fetch(response, 'last_air_date'),
		'first_air_date': Utils.fetch(response, 'first_air_date'),
		'TotalEpisodes': Utils.fetch(response, 'number_of_episodes'),
		'TotalSeasons': Utils.fetch(response, 'number_of_seasons'),
		'in_production': Utils.fetch(response, 'in_production'),
		'Release_Date': Utils.fetch(response, 'first_air_date'),
		'Premiered': Utils.fetch(response, 'first_air_date')
		}
	tvshow.update(artwork)
	if dbid:
		local_item = local_db.get_tvshow_from_db(dbid)
		tvshow.update(local_item)
	else:
		tvshow = local_db.merge_with_local_tvshow_info([tvshow])[0]
	tvshow['Rating'] = Utils.fetch(response, 'vote_average')
	listitems = {
		'actors': handle_tmdb_people(response['credits']['cast']),
		'similar': handle_tmdb_tvshows(response['similar']['results']),
		'studios': handle_tmdb_misc(response['production_companies']),
		'networks': handle_tmdb_misc(response['networks']),
		'certifications': handle_tmdb_misc(response['content_ratings']['results']),
		'crew': handle_tmdb_people(response['credits']['crew']),
		'genres': handle_tmdb_misc(response['genres']),
		'keywords': handle_tmdb_misc(response['keywords']['results']),
		'videos': videos,
		'seasons': handle_tmdb_seasons(response['seasons']),
		'images': handle_tmdb_images(response['images']['posters']),
		'backdrops': handle_tmdb_images(response['images']['backdrops'])
		}
	return (tvshow, listitems)

def extended_season_info(tvshow_id, season_number):
	if not tvshow_id or not season_number:
		return None
	session_str = ''
	tvshow = get_tmdb_data('tv/%s?append_to_response=alternative_titles,content_ratings,credits,external_ids,images,keywords,rating,similar,translations,videos&language=%s&include_image_language=en,null,%s&%s' % (tvshow_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID'), session_str), 99999)
	response = get_tmdb_data('tv/%s/season/%s?append_to_response=videos,images,external_ids,credits&language=%s&include_image_language=en,null,%s&' % (tvshow_id, season_number, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID')), 7)
	dbid = Utils.fetch(tvshow, 'dbid')
	tmdb_id = Utils.fetch(tvshow, 'id')
	external_ids = Utils.fetch(tvshow, 'external_ids')
	year = Utils.get_year(Utils.fetch(tvshow, 'first_air_date'))
	if external_ids:
		imdb_id = Utils.fetch(external_ids, 'imdb_id')
		freebase_id = Utils.fetch(external_ids, 'freebase_id')
		tvdb_id = Utils.fetch(external_ids, 'tvdb_id')
		tvrage_id = Utils.fetch(external_ids, 'tvrage_id')
	if not response:
		Utils.notify('Could not find season info')
		return None
	if response.get('name', False):
		title = response['name']
	else:
		title = 'Specials' if season_number == '0' else u'Season %s' % season_number
	season = {
		'SeasonDescription': Utils.clean_text(response['overview']),
		'Plot': Utils.clean_text(response['overview']),
		'TVShowTitle': Utils.fetch(tvshow, 'name'),
		'title': title,
		'dbid': dbid,
		'imdb_id': imdb_id,
		'tmdb_id': tmdb_id,
		'tvdb_id': tvdb_id,
		'tvrage_id': tvrage_id,
		'year': year,
		'season': season_number,
		'path': 'plugin://script.extendedinfo?info=seasoninfo&tvshow=%s&season=%s' % (Utils.fetch(tvshow, 'name'), season_number),
		'release_date': response['air_date'],
		'AirDate': response['air_date']
		}
	artwork = get_image_urls(poster=response.get('poster_path'))
	season.update(artwork)
	videos = handle_tmdb_videos(response['videos']['results']) if 'videos' in response else []
	listitems = {
		'actors': handle_tmdb_people(response['credits']['cast']),
		'crew': handle_tmdb_people(response['credits']['crew']),
		'videos': videos,
		'episodes': handle_tmdb_episodes(response['episodes']),
		'images': handle_tmdb_images(response['images']['posters'])
		}
	return (season, listitems)

def extended_episode_info(tvshow_id, season, episode, cache_time=7):
	if not tvshow_id or not episode:
		return None
	if not season:
		season = 0
	session_str = ''
	tvshow = get_tmdb_data('tv/%s?append_to_response=alternative_titles,content_ratings,credits,external_ids,images,keywords,rating,similar,translations,videos&language=%s&include_image_language=en,null,%s&%s' % (tvshow_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID'), session_str), 99999)
	response = get_tmdb_data('tv/%s/season/%s/episode/%s?append_to_response=credits,external_ids,images,rating,videos&language=%s&include_image_language=en,null,%s&%s&' % (tvshow_id, season, episode, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID'), session_str), cache_time)
	tmdb_id = Utils.fetch(tvshow, 'id')
	TVShowTitle = Utils.fetch(tvshow, 'name')
	external_ids = Utils.fetch(tvshow, 'external_ids')
	year = Utils.get_year(Utils.fetch(tvshow, 'first_air_date')),
	if external_ids:
		imdb_id = Utils.fetch(external_ids, 'imdb_id')
		freebase_id = Utils.fetch(external_ids, 'freebase_id')
		tvdb_id = Utils.fetch(external_ids, 'tvdb_id')
		tvrage_id = Utils.fetch(external_ids, 'tvrage_id')
	videos = handle_tmdb_videos(response['videos']['results']) if 'videos' in response else []
	try:
		actors = handle_tmdb_people(response['credits']['cast'])
	except:
		actors = []
	try:
		crew = handle_tmdb_people(response['credits']['crew'])
	except:
		crew = []
	try:
		guest_stars = handle_tmdb_people(response['credits']['guest_stars'])
	except:
		guest_stars = []
	try:
		images = handle_tmdb_images(response['images']['stills'])
	except:
		images = []
	answer = {
		'SeasonDescription': Utils.clean_text(response['overview']),
		'Plot': Utils.clean_text(response['overview']),
		'TVShowTitle': TVShowTitle,
		'tvshow_id': tmdb_id,
		'tvdb_id': tvdb_id,
		'actors': actors,
		'path': 'plugin://script.extendedinfo?info=extendedepisodeinfo&tvshow_id=%s&season=%s&episode=%s' % (tvshow_id, season, episode),
		'crew': crew,
		'guest_stars': guest_stars,
		'videos': videos,
		'images': images
		}
	return (handle_tmdb_episodes([response])[0], answer)

def extended_actor_info(actor_id):
	if not actor_id:
		return None
	response = get_tmdb_data('person/%s?append_to_response=tv_credits,movie_credits,combined_credits,images,tagged_images&' % actor_id, 1)
	tagged_images = []
	if 'tagged_images' in response:
		tagged_images = handle_tmdb_tagged_images(response['tagged_images']['results'])
	listitems = {
		'movie_roles': handle_tmdb_movies(response['movie_credits']['cast']),
		'tvshow_roles': handle_tmdb_tvshows(response['tv_credits']['cast']),
		'movie_crew_roles': handle_tmdb_movies(response['movie_credits']['crew']),
		'tvshow_crew_roles': handle_tmdb_tvshows(response['tv_credits']['crew']),
		'tagged_images': tagged_images,
		'images': handle_tmdb_images(response['images']['profiles'])
		}
	info = handle_tmdb_people([response])[0]
	info['DBMovies'] = str(len([d for d in listitems['movie_roles'] if 'dbid' in d]))
	return (info, listitems)

def translate_status(status_string):
	translations = {
		'released': 'Released',
		'post production': 'Post production',
		'in production': 'In production',
		'ended': 'Ended',
		'returning series': 'Continuing',
		'planned': 'Planned'
		}
	if status_string.lower() in translations:
		return translations[status_string.lower()]
	else:
		return status_string

def get_keywords(movie_id):
	response = get_tmdb_data('movie/%s?append_to_response=alternative_titles,credits,images,keywords,releases,videos,translations,similar,reviews,rating&include_image_language=en,null,%s&language=%s&' % (movie_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID')), 30)
	keywords = []
	if 'keywords' in response:
		for keyword in response['keywords']['keywords']:
			keyword_dict = {
				'id': Utils.fetch(keyword, 'id'),
				'name': keyword['name']
				}
			keywords.append(keyword_dict)
	return keywords

def get_tmdb_shows(tvshow_type):
	response = get_tmdb_data('tv/%s?language=%s&' % (tvshow_type, xbmcaddon.Addon().getSetting('LanguageID')), 0.3)
	if 'results' in response:
		return handle_tmdb_tvshows(response['results'], False, None)
	else:
		return []

def get_tmdb_movies(movie_type):
	response = get_tmdb_data('movie/%s?language=%s&' % (movie_type, xbmcaddon.Addon().getSetting('LanguageID')), 0.3)
	if 'results' in response:
		return handle_tmdb_movies(response['results'], False, None)
	else:
		return []

def get_set_movies(set_id):
	response = get_tmdb_data('collection/%s?language=%s&append_to_response=images&include_image_language=en,null,%s&' % (set_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID')), 14)
	if response:
		artwork = get_image_urls(poster=response.get('poster_path'), fanart=response.get('backdrop_path'))
		info = {
			'label': response['name'],
			'overview': response['overview'],
			'id': response['id']
			}
		info.update(artwork)
		return handle_tmdb_movies(response.get('parts', [])), info
	else:
		return [], {}

def get_person_movies(person_id):
	response = get_tmdb_data('person/%s/credits?language=%s&' % (person_id, xbmcaddon.Addon().getSetting('LanguageID')), 14)
	if 'crew' in response:
		return handle_tmdb_movies(response['crew'])
	else:
		return []

def search_media(media_name=None, year='', media_type='movie'):
	search_query = Utils.url_quote('%s %s' % (media_name, year))
	if not search_query:
		return None
	response = get_tmdb_data('search/%s?query=%s&language=%s&include_adult=%s&' % (media_type, search_query, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('include_adults')), 1)
	if not response == 'Empty':
		for item in response['results']:
			if item['id']:
				return item['id']
	return None

def get_imdb_id_from_movie_id(movie_id=None, cache_time=14):
	if not movie_id:
		return None
	session_str = ''
	response = get_tmdb_data('movie/%s?&language=%s,null,%s&%s' % (movie_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID'), session_str), cache_time)
	if not response:
		return False
	imdb_id = Utils.fetch(response, 'imdb_id')
	return imdb_id

def get_tvshow_ids(tvshow_id=None, cache_time=14):
	if not tvshow_id:
		return None
	session_str = ''
	response = get_tmdb_data('tv/%s?append_to_response=external_ids&language=%s&include_image_language=en,null,%s&%s' % (tvshow_id, xbmcaddon.Addon().getSetting('LanguageID'), xbmcaddon.Addon().getSetting('LanguageID'), session_str), cache_time)
	if not response:
		return False
	external_ids = Utils.fetch(response, 'external_ids')
	return external_ids