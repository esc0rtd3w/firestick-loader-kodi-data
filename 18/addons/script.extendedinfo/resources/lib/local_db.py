import json
import xbmc, xbmcgui
from resources.lib import Utils

id_list = []
title_list = []
otitle_list = []
tvshow_id_list = []
tvshow_otitle_list = []
tvshow_title_list = []
tvshow_imdb_list = []
movie_props = '["title", "originaltitle", "votes", "playcount", "year", "genre",\
				"studio", "country", "tagline", "plot", "runtime", "file", "plotoutline",\
				"lastplayed","trailer", "rating", "resume", "art", "streamdetails",\
				"mpaa", "director", "writer", "cast", "dateadded", "imdbnumber"]'

shows_props = '["title", "genre", "year", "rating", "plot", "studio", "mpaa", "cast",\
				"playcount", "episode", "imdbnumber", "premiered", "votes", "lastplayed",\
				"fanart", "thumbnail", "file", "originaltitle", "sorttitle", "episodeguide",\
				"season", "watchedepisodes", "dateadded", "tag", "art"]'

def get_db_movies(filter_str=''):
	params = '{"properties": %s, %s}' % (movie_props, filter_str)
	json_response = Utils.get_kodi_json(method='VideoLibrary.GetMovies', params=params)
	if 'result' in json_response and 'movies' in json_response['result']:
		return [handle_db_movies(item) for item in json_response['result']['movies']]
	else:
		return []

def get_db_tvshows(filter_str=''):
	params = '{"properties": %s, %s}' % (shows_props, filter_str)
	json_response = Utils.get_kodi_json(method='VideoLibrary.GetTVShows', params=params)
	if 'result' in json_response and 'tvshows' in json_response['result']:
		return [handle_db_tvshows(item) for item in json_response['result']['tvshows']]
	else:
		return []

def handle_db_movies(movie):
	trailer = 'plugin://script.extendedinfo?info=playtrailer&&dbid=%s' % movie['movieid']
	path = 'plugin://script.extendedinfo?info=extendedinfo&&dbid=%s' % movie['movieid']
	if (movie['resume']['position'] and movie['resume']['total']) > 0:
		resume = 'true'
		played = '%s' % int((float(movie['resume']['position']) / float(movie['resume']['total'])) *100)
	else:
		resume = 'false'
		played = '0'
	stream_info = Utils.media_streamdetails(movie['file'].encode('utf-8').lower(), movie['streamdetails'])
	db_movie = {
		'mediatype': 'movie',
		'fanart': movie['art'].get('fanart', ''),
		'fanart_small': movie['art'].get('fanart', ''),
		'thumb': movie['art'].get('poster', ''),
		'poster': movie['art'].get('poster', ''),
		'Banner': movie['art'].get('banner', ''),
		'clearart': movie['art'].get('clearart', ''),
		'DiscArt': movie['art'].get('discart', ''),
		'title': movie.get('label', ''),
		'File': movie.get('file', ''),
		'year': movie.get('year', ''),
		'writer': ' / '.join(movie['writer']),
		'Logo': movie['art'].get('clearlogo', ''),
		'OriginalTitle': movie.get('originaltitle', ''),
		'imdb_id': movie.get('imdbnumber', ''),
		'path': path,
		'plot': movie.get('plot', ''),
		'director': ' / '.join(movie.get('director')),
		'writer': ' / '.join(movie.get('writer')),
		'PercentPlayed': played,
		'Resume': resume,
		'Play': '',
		'trailer': trailer,
		'dbid': movie['movieid'],
		'Rating': round(float(movie['rating']), 1)
		}
	streams = []
	for i, item in enumerate(movie['streamdetails']['audio']):
		language = item['language']
		if language not in streams and language != 'und':
			streams.append(language)
			db_movie['AudioLanguage.%d' % (i + 1)] = language
			db_movie['AudioCodec.%d' % (i + 1)] = item['codec']
			db_movie['AudioChannels.%d' % (i + 1)] = str(item['channels'])
	subs = []
	for i, item in enumerate(movie['streamdetails']['subtitle']):
		language = item['language']
		if language not in subs and language != 'und':
			subs.append(language)
			db_movie['SubtitleLanguage.%d' % (i + 1)] = language
	db_movie.update(stream_info)
	return dict((k, v) for k, v in db_movie.iteritems() if v)

def handle_db_tvshows(tvshow):
	path = 'plugin://script.extendedinfo?info=extendedtvinfo&&dbid=%s' % tvshow['tvshowid']
	db_tvshow = {
		'mediatype': 'tvshow',
		'fanart': tvshow['art'].get('fanart', ''),
		'fanart_small': tvshow['art'].get('fanart', ''),
		'thumb': tvshow['art'].get('poster', ''),
		'poster': tvshow['art'].get('poster', ''),
		'Banner': tvshow['art'].get('banner', ''),
		'DiscArt': tvshow['art'].get('discart', ''),
		'title': tvshow.get('label', ''),
		'genre': ' / '.join(tvshow.get('genre', '')),
		'File': tvshow.get('file', ''),
		'year': tvshow.get('year', ''),
		'Logo': tvshow['art'].get('clearlogo', ''),
		'OriginalTitle': tvshow.get('originaltitle', ''),
		'imdb_id': tvshow.get('imdbnumber', ''),
		'path': path,
		'Play': '',
		'dbid': tvshow['tvshowid'],
		'Rating': round(float(tvshow['rating']), 1)
		}
	return dict((k, v) for k, v in db_tvshow.iteritems() if v)

def get_movie_from_db(movie_id):
	params = '{"properties": %s, "movieid": %s}' % (movie_props, movie_id)
	response = Utils.get_kodi_json(method='VideoLibrary.GetMovieDetails', params=params)
	if 'result' in response and 'moviedetails' in response['result']:
		return handle_db_movies(response['result']['moviedetails'])
	return {}

def get_tvshow_from_db(tvshow_id):
	params = '{"properties": %s, "tvshowid": %s}' % (shows_props, tvshow_id)
	response = Utils.get_kodi_json(method='VideoLibrary.GetTVShowDetails', params=params)
	if 'result' in response and 'tvshowdetails' in response['result']:
		return handle_db_tvshows(response['result']['tvshowdetails'])
	return {}

def merge_with_local_movie_info(online_list=[], library_first=True, sortkey=False):
	global id_list
	global otitle_list
	global title_list
	global imdb_list
	if not title_list:
		id_list = xbmc.getInfoLabel('Window(home).Property(id_list.JSON)')
		if id_list and id_list != '[]':
			id_list = json.loads(id_list)
			otitle_list = json.loads(xbmc.getInfoLabel('Window(home).Property(otitle_list.JSON)'))
			title_list = json.loads(xbmc.getInfoLabel('Window(home).Property(title_list.JSON)'))
			imdb_list = json.loads(xbmc.getInfoLabel('Window(home).Property(imdb_list.JSON)'))
		else:
			params = '{"properties": ["originaltitle", "imdbnumber"], "sort": {"method": "none"}}'
			json_response = Utils.get_kodi_json(method='VideoLibrary.GetMovies', params=params)
			id_list = []
			imdb_list = []
			otitle_list = []
			title_list = []
			if 'result' in json_response and 'movies' in json_response['result']:
				for item in json_response['result']['movies']:
					id_list.append(item['movieid'])
					imdb_list.append(item['imdbnumber'])
					otitle_list.append(item['originaltitle'].lower())
					title_list.append(item['label'].lower())
			xbmcgui.Window(10000).setProperty('id_list.JSON', json.dumps(id_list))
			xbmcgui.Window(10000).setProperty('otitle_list.JSON', json.dumps(otitle_list))
			xbmcgui.Window(10000).setProperty('title_list.JSON', json.dumps(title_list))
			xbmcgui.Window(10000).setProperty('imdb_list.JSON', json.dumps(imdb_list))
	local_items = []
	remote_items = []
	for online_item in online_list:
		found = False
		if 'imdb_id' in online_item and online_item['imdb_id'] in imdb_list:
			index = imdb_list.index(online_item['imdb_id'])
			found = True
		elif online_item['title'].lower() in title_list:
			index = title_list.index(online_item['title'].lower())
			found = True
		elif 'OriginalTitle' in online_item and online_item['OriginalTitle'].lower() in otitle_list:
			index = otitle_list.index(online_item['OriginalTitle'].lower())
			found = True
		if found:
			local_item = get_movie_from_db(id_list[index])
			if local_item:
				try:
					diff = abs(int(local_item['year']) - int(online_item['year']))
					if diff > 1:
						remote_items.append(online_item)
						continue
				except:
					pass
				online_item.update(local_item)
				if library_first:
					local_items.append(online_item)
				else:
					remote_items.append(online_item)
			else:
				remote_items.append(online_item)
		else:
			remote_items.append(online_item)
	if sortkey:
		local_items = sorted(local_items, key=lambda k: k[sortkey], reverse=True)
		remote_items = sorted(remote_items, key=lambda k: k[sortkey], reverse=True)
	return local_items + remote_items

def merge_with_local_tvshow_info(online_list=[], library_first=True, sortkey=False):
	global tvshow_id_list
	global tvshow_otitle_list
	global tvshow_title_list
	global tvshow_imdb_list
	if not tvshow_title_list:
		tvshow_id_list = xbmc.getInfoLabel('Window(home).Property(tvshow_id_list.JSON)')
		if tvshow_id_list and tvshow_id_list != '[]':
			tvshow_id_list = json.loads(tvshow_id_list)
			tvshow_otitle_list = json.loads(xbmc.getInfoLabel('Window(home).Property(tvshow_otitle_list.JSON)'))
			tvshow_title_list = json.loads(xbmc.getInfoLabel('Window(home).Property(tvshow_title_list.JSON)'))
			tvshow_imdb_list = json.loads(xbmc.getInfoLabel('Window(home).Property(tvshow_imdb_list.JSON)'))
		else:
			params = '{"properties": ["originaltitle", "imdbnumber"], "sort": {"method": "none"}}'
			json_response = Utils.get_kodi_json(method='VideoLibrary.GetTVShows', params=params)
			tvshow_id_list = []
			tvshow_imdb_list = []
			tvshow_otitle_list = []
			tvshow_title_list = []
			if 'result' in json_response and 'tvshows' in json_response['result']:
				for item in json_response['result']['tvshows']:
					tvshow_id_list.append(item['tvshowid'])
					tvshow_imdb_list.append(item['imdbnumber'])
					tvshow_otitle_list.append(item['originaltitle'].lower())
					tvshow_title_list.append(item['label'].lower())
			xbmcgui.Window(10000).setProperty('tvshow_id_list.JSON', json.dumps(tvshow_id_list))
			xbmcgui.Window(10000).setProperty('tvshow_otitle_list.JSON', json.dumps(tvshow_otitle_list))
			xbmcgui.Window(10000).setProperty('tvshow_title_list.JSON', json.dumps(tvshow_title_list))
			xbmcgui.Window(10000).setProperty('tvshow_imdb_list.JSON', json.dumps(tvshow_imdb_list))
	local_items = []
	remote_items = []
	for online_item in online_list:
		found = False
		if 'imdb_id' in online_item and online_item['imdb_id'] in tvshow_imdb_list:
			index = tvshow_imdb_list.index(online_item['imdb_id'])
			found = True
		elif online_item['title'].lower() in tvshow_title_list:
			index = tvshow_title_list.index(online_item['title'].lower())
			found = True
		elif 'OriginalTitle' in online_item and online_item['OriginalTitle'].lower() in tvshow_otitle_list:
			index = tvshow_otitle_list.index(online_item['OriginalTitle'].lower())
			found = True
		if found:
			local_item = get_tvshow_from_db(tvshow_id_list[index])
			if local_item:
				try:
					diff = abs(int(local_item['year']) - int(online_item['year']))
					if diff > 1:
						remote_items.append(online_item)
						continue
				except:
					pass
				online_item.update(local_item)
				if library_first:
					local_items.append(online_item)
				else:
					remote_items.append(online_item)
			else:
				remote_items.append(online_item)
		else:
			remote_items.append(online_item)
	if sortkey:
		local_items = sorted(local_items, key=lambda k: k[sortkey], reverse=True)
		remote_items = sorted(remote_items, key=lambda k: k[sortkey], reverse=True)
	return local_items + remote_items

def get_set_name_from_db(dbid):
	params = '{"properties": ["setid"], "movieid": %s}' % dbid
	json_response = Utils.get_kodi_json(method='VideoLibrary.GetMovieDetails', params=params)
	if 'result' in json_response and 'moviedetails' in json_response['result']:
		set_dbid = json_response['result']['moviedetails'].get('setid', '')
		if set_dbid:
			params = '{"setid": %s}' % set_dbid
			json_response = Utils.get_kodi_json(method='VideoLibrary.GetMovieSetDetails', params=params)
			return json_response['result']['setdetails'].get('label', '')
	return ''

def get_imdb_id_from_db(media_type, dbid):
	if not dbid:
		return None
	if media_type == 'movie':
		params = '{"properties": ["imdbnumber", "title", "year"], "movieid": %s}' % dbid
		json_response = Utils.get_kodi_json(method='VideoLibrary.GetMovieDetails', params=params)
		if 'result' in json_response and 'moviedetails' in json_response['result']:
			return json_response['result']['moviedetails']['imdbnumber']
	elif media_type == 'tvshow':
		params = '{"properties": ["imdbnumber", "title", "year"], "tvshowid": %s}' % dbid
		json_response = Utils.get_kodi_json(method='VideoLibrary.GetTVShowDetails', params=params)
		if 'result' in json_response and 'tvshowdetails' in json_response['result']:
			return json_response['result']['tvshowdetails']['imdbnumber']
	return None