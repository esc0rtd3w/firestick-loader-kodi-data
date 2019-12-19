import re, json, urllib, datetime
import xbmc
from resources.lib import text
from resources.lib import meta_info
from resources.lib import play_base
from resources.lib import meta_players
from resources.lib.xswift2 import plugin

NTH = {1: 'first', 2: 'second', 3: 'third', 5: 'fifth', 8: 'eigth'}
DCS = {2: 'twenty', 3: 'thirty', 4: 'fourty', 5: 'fifty', 6: 'sixty'}

def play_episode(id, season, episode, usedefault):
	from resources.lib.TheTVDB import TVDB
	from resources.lib.TheTVDB import create_tvdb
	id = int(id)
	season = int(season)
	episode = int(episode)
	dbid = xbmc.getInfoLabel('ListItem.DBID')
	try:
		dbid = int(dbid)
	except:
		dbid = None
	show = TVDB[id]
	show_info = meta_info.get_tvshow_metadata_tvdb(show, banners=False)
	play_plugin = meta_players.ADDON_SELECTOR.id
	players = meta_players.get_players('tvshows', filters={'network': show.get('network')})
	players = [p for p in players if p.id == play_plugin] or players
	if not players or len(players) == 0:
		xbmc.executebuiltin('Action(Info)')
		play_base.action_cancel()
		return
	if usedefault == 'True':
		default = plugin.get_setting('tvshowsdefault', unicode)
		for player in players:
			if player.title == default:
			 	players = [player]
	trakt_ids = play_base.get_trakt_ids(id_type='tvdb', id=id, type='show')
	params = {}
	for lang in meta_players.get_needed_langs(players):
		tvdb_data = create_tvdb(lang)[id]
		if tvdb_data['seriesname'] is None:
			continue
		episode_parameters = get_episode_parameters(tvdb_data, season, episode)
		if episode_parameters is not None:
			params[lang] = episode_parameters
		else:
			if trakt_ids['tmdb'] != None and trakt_ids['tmdb'] != '':
				return tmdb_play_episode(trakt_ids['tmdb'], season, episode)
			elif trakt_ids['tvdb'] == None or trakt_ids['tvdb'] == '':
				plugin.ok('Information not found for:', '%s - S%sE%s' % (show_info['name'], season, episode))
			else:
				plugin.ok('Information not found for:', '%s - S%sE%s' % (show_info['name'], season, episode))
		if trakt_ids != None:
			params[lang].update(trakt_ids)
		params[lang]['info'] = show_info
		params[lang] = text.to_unicode(params[lang])
	link = play_base.on_play_video(players, params, trakt_ids)
	if link:
		plugin.setProperty('plugin.video.openmeta.data', json.dumps(
			{
				'dbid': dbid,
				'tvdb': id,
				'season': season,
				'episode': episode
			}))
		season_info = meta_info.get_season_metadata_tvdb(show_info, show[season], banners=False)
		episode_info = meta_info.get_episode_metadata_tvdb(season_info, show[season][episode])
		play_base.action_play(
			{
				'label': episode_info['name'],
				'path': link,
				'info': episode_info,
				'is_playable': True,
				'info_type': 'video',
				'thumbnail': episode_info['poster'],
				'poster': episode_info['poster'],
				'fanart': episode_info['fanart']
			})

def tmdb_play_episode(id, season, episode):
	from resources.lib.TheMovieDB import TV, TV_Seasons, TV_Episodes
	tried = 'tvdb'
	id = int(id)
	season = int(season)
	episode = int(episode)
	dbid = xbmc.getInfoLabel('ListItem.DBID')
	try:
		dbid = int(dbid)
	except:
		dbid = None
	show = TV(id).info(language='en', append_to_response='external_ids,images')
	if 'first_air_date' in show and show['first_air_date'] != None:
		year = show['first_air_date'][:4]
	else:
		year = None
	trakt_ids = play_base.get_trakt_ids(id_type='tmdb', id=id, type='show')
	if 'status_code' in show:
		return trakt_play_episode(trakt_ids['trakt'], season, episode)
	if 'name' in show:
		title = show['name']
	else:
		title = None
	show_info = meta_info.get_tvshow_metadata_tmdb(show)
	title = show_info['name']
	preason = TV_Seasons(id, season).info(language='en', append_to_response='external_ids,images')
	if 'The resource you requested could not be found' in str(preason):
		return trakt_play_episode(trakt_ids['trakt'], season, episode)
	season_info = meta_info.get_season_metadata_tmdb(show_info, preason)
	prepisode = TV_Episodes(id, season, episode).info(language='en', append_to_response='external_ids,images')
	if prepisode == '{u"status_code": 34, u"status_message": u"The resource you requested could not be found."}':
		return trakt_play_episode(trakt_ids['tmdb'], season, episode)
	episode_info = meta_info.get_episode_metadata_tmdb(season_info, prepisode)
	if show_info['poster'] != None and show_info['poster'] != '':
		show_poster = show_info['poster']
	else:
		show_poster = ''
	if show_info['fanart'] != None and show_info['fanart'] != '':
		show_fanart = show_info['fanart']
	else:
		show_fanart = ''
	episodes = preason['episodes']
	items = []
	play_plugin = meta_players.ADDON_SELECTOR.id
	players = meta_players.get_players('tvshows', filters={'network': show.get('network')})
	players = [p for p in players if p.id == play_plugin] or players
	if not players:
		return xbmc.executebuiltin('Action(Info)')
	trakt_ids = play_base.get_trakt_ids(id_type='tmdb', id=id, type='show')
	params = {}
	for lang in meta_players.get_needed_langs(players):
		if show['name'] is None:
			continue
		episode_parameters = get_tmdb_episode_parameters(show, preason, prepisode)
		if episode_parameters is not None:
			params[lang] = episode_parameters
		else:
			if trakt_ids['trakt'] != None and trakt_ids['trakt'] != '':
				return trakt_play_episode(trakt_ids['trakt'], season, episode)
			else:
				msg = 'No TMDb information found for %s - S%sE%s' % (show_info['name'], season, episode)
				plugin.ok('Episode information not found', msg)
		if trakt_ids != None:
			params[lang].update(trakt_ids)
		params[lang]['info'] = show_info
		params[lang] = text.to_unicode(params[lang])
	link = play_base.on_play_video(players, params, trakt_ids)
	if link:
		plugin.setProperty('plugin.video.openmeta.data', json.dumps(
			{
				'dbid': dbid,
				'tmdb': id,
				'season': season,
				'episode': episode
			}))
		episode_metadata = meta_info.get_episode_metadata_tmdb(season_info, prepisode)
		play_base.action_play(
			{
				'label': episode_info['title'],
				'path': link,
				'info': [],
				'is_playable': True,
				'info_type': 'video',
				'thumbnail': episode_info['poster'],
				'poster': episode_info['poster'],
				'fanart': str(show_info['fanart'])
			})

def trakt_play_episode(id, season, episode):
	from resources.lib.Trakt import get_show, get_season, get_seasons, get_episode
	id = int(id)
	season = int(season)
	episode = int(episode)
	show = None
	preason = None
	prepisode = None
	dbid = xbmc.getInfoLabel('ListItem.DBID')
	try:
		dbid = int(dbid)
	except:
		dbid = None
	show = get_show(id)
	if 'name' in show:
		show_title = show['name']
	elif 'title' in show:
		show_title = show['title']
	if show:
		if show.get('first_aired', None):
			year = show['first_aired'][:4]
		else:
			year = None
		trakt_ids = play_base.get_trakt_ids(id_type='trakt', id=id, type='show')
		preason = get_season(id, season)
		if preason:
			prepisode = get_episode(id, season, episode)
		elif not preason and season > 1900: 
			seasons = get_seasons(id)
			for item in seasons:
				if item['first_aired'] != None:
					if int(item['first_aired'][:4]) == season: 
						season_number = item['number']
						preason = get_season(id, season_number)
	if not prepisode or not preason or not show:
		return tvmaze_play_episode(show_title, season, episode)
	show_info = meta_info.get_tvshow_metadata_trakt(show)
	season_info = meta_info.get_season_metadata_trakt(show_info, preason)
	episode_info = meta_info.get_episode_metadata_trakt(season_info, prepisode)
	title = show_info['name']
	if show_info['poster'] != None and show_info['poster'] != '':
		show_poster = show_info['poster']
	else:
		show_poster = ''
	if show_info['fanart'] != None and show_info['fanart'] != '':
		show_fanart = show_info['fanart']
	else:
		show_fanart = ''
	items = []
	play_plugin = meta_players.ADDON_SELECTOR.id
	players = meta_players.get_players('tvshows', filters={'network': show.get('network')})
	players = [p for p in players if p.id == play_plugin] or players
	if not players:
		return xbmc.executebuiltin('Action(Info)')
	params = {}
	for lang in meta_players.get_needed_langs(players):
		if show['name'] is None:
			continue
		episode_parameters = get_trakt_episode_parameters(show, preason, prepisode)
		if episode_parameters is not None:
			params[lang] = episode_parameters
		else:
			if trakt_ids['tmdb'] != None and trakt_ids['tmdb'] != '' and tried != 'tmdb': 
				tried = 'tmdb'
				return tvdb_play_episode(trakt_ids['tvdb'], season, episode)
			elif tried == 'tmdb':
				msg = 'No TVDb or TMDb information found for %s - S%sE%s' % (show_info['name'], season, episode)
				plugin.ok('Episode information not found', msg)
			else:
				msg = 'No TMDb information found for %s - S%sE%s' % (show_info['name'], season, episode)
				plugin.ok('Episode information not found', msg)
		if trakt_ids != None:
			params[lang].update(trakt_ids)
		params[lang]['info'] = show_info
		params[lang] = text.to_unicode(params[lang])
	link = play_base.on_play_video(players, params, trakt_ids)
	if link:
		plugin.setProperty('plugin.video.openmeta.data', json.dumps(
			{
				'dbid': dbid,
				'trakt': id,
				'season': season,
				'episode': episode
			}))
		episode_metadata = meta_info.get_episode_metadata_trakt(season_info, prepisode)
		play_base.action_play(
			{
				'label': episode_info['title'],
				'path': link,
				'info': episode_info,
				'is_playable': True,
				'info_type': 'video',
				'thumbnail': episode_info['poster'],
				'poster': episode_info['poster'],
				'fanart': str(show_info['fanart'])
			})

def tvmaze_play_episode(id, season, episode, title=None):
	title = ''
	try:
		id = int(id)
	except:
		title = id
	if title and title != '':
		url = 'https://api.tvmaze.com/search/shows?q=%s' % id
		response = urllib.urlopen(url)
		shows = json.loads(response.read())
		if len(shows) > 0:
			show = shows[0]
			id = show['show']['id']
	url = 'https://api.tvmaze.com/shows/%d?embed[]=seasons&embed[]=episodes' % int(id)
	response = urllib.urlopen(url)
	show = json.loads(response.read())
	season = int(season)
	episode = int(episode)
	dbid = xbmc.getInfoLabel('ListItem.DBID')
	try:
		dbid = int(dbid)
	except:
		dbid = None
	if show['externals']:
		if show['externals']['thetvdb']:
			trakt_ids = play_base.get_trakt_ids(id_type='tvdb', id=show['externals']['thetvdb'], type='show')
		elif show['externals']['imdb']:
			trakt_ids = play_base.get_trakt_ids(id_type='imdb', id=show['externals']['imdb'], type='show')
	else:
		trakt_ids = None
	show_info = meta_info.get_tvshow_metadata_tvmaze(show)
	preasons = show['_embedded']['seasons']
	for item in preasons:
		if item['number'] == season: 
			preason = item
			season = preasons.index(item) + 1
		elif item['premiereDate'] and item['endDate']:
			if int(item['premiereDate'][:4]) <= season and int(item['endDate'][:4]) >= season: 
				preason = item
				season = preasons.index(item) + 1
	prepisodes = show['_embedded']['episodes']
	for item in prepisodes:
		if item['number'] == episode:
			prepisode = item
	season_info = meta_info.get_season_metadata_tvmaze(show_info, preason)
	episode_info = meta_info.get_episode_metadata_tvmaze(season_info, prepisode)
	if show_info['poster'] != None and show_info['poster'] != '':
		show_poster = show_info['poster']
	else:
		show_poster = ''
	if show_info['fanart'] != None and show_info['fanart'] != '':
		show_fanart = show_info['fanart']
	else:
		show_fanart = ''
	items = []
	play_plugin = meta_players.ADDON_SELECTOR.id
	players = meta_players.get_players('tvshows', filters={'network': show.get('network')})
	players = [p for p in players if p.id == play_plugin] or players
	if not players:
		return xbmc.executebuiltin('Action(Info)')
	params = {}
	for lang in meta_players.get_needed_langs(players):
		if show['name'] is None:
			continue
		episode_parameters = get_tvmaze_episode_parameters(show, preason, prepisode)
		if episode_parameters is not None:
			params[lang] = episode_parameters
		else:
			if trakt_ids['tmdb'] != None and trakt_ids['tmdb'] != '' and tried != 'tmdb': 
				tried = 'tmdb'
				return tvdb_play_episode(trakt_ids['tvdb'], season, episode)
			elif tried == 'tmdb':
				msg = 'No TVDb or TMDb information found for %s - S%sE%s' % (show_info['name'], season, episode)
				plugin.ok('Episode information not found', msg)
			else:
				msg = 'No TMDb information found for %s - S%sE%s' % (show_info['name'], season, episode)
				plugin.ok('Episode information not found', msg)
		if trakt_ids != None:
			params[lang].update(trakt_ids)
		params[lang]['info'] = show_info
		params[lang] = text.to_unicode(params[lang])
	link = play_base.on_play_video(players, params, trakt_ids)
	if link:
		plugin.setProperty('plugin.video.openmeta.data', json.dumps(
			{
				'dbid': dbid,
				'tvdb': trakt_ids['tvdb'],
				'season': season,
				'episode': episode
			}))
		episode_metadata = meta_info.get_episode_metadata_tvmaze(season_info, prepisode)
		play_base.action_play(
			{
				'label': episode_info['title'],
				'path': link,
				'info': [],
				'is_playable': True,
				'info_type': 'video',
				'thumbnail': episode_info['poster'],
				'poster': episode_info['poster'],
				'fanart': str(show_info['fanart'])
			})

def get_episode_parameters(show, season, episode):
	from resources.lib.TheMovieDB import Find
	if season in show and episode in show[season]:
		season_obj = show[season]
		episode_obj = show[season][episode]
	else:
		return
	episodes = 0
	count = 0
	for i in show.items():
		episodes += len(i[1].items())
		if i[0] != 0 and i[0] < (season -1):
			count += len(i[1].items())
	parameters = {'id': show['id'], 'season': season, 'episode': episode}
	if season in NTH:
		parameters['season_ordinal'] = NTH[season]
	else:
		try:
			if text.number_to_text(season) in (season, ''):
				if int(str(season)[-1]) in NTH:
					parameters['season_ordinal'] = '%s%s' % (DCS[int(str(season)[-2])], NTH[int(str(season)[-1])])
				else:
					parameters['season_ordinal'] = '%s%sth' % (DCS[int(str(season)[-2])], text.number_to_text(int(str(season)[-1])))
			else:
				parameters['season_ordinal'] = '%sth' % text.number_to_text(season)
		except:
			pass
	parameters['episodes'] = episodes
	parameters['seasons'] = len(show.items())
	parameters['seasons_no_specials'] = len([season_num for (season_num, season) in show.items() if season_num != 0])
	show_info = meta_info.get_tvshow_metadata_tvdb(show, banners=True)
	network = show.get('network', '')
	parameters['network'] = network
	if network:
		parameters['network_clean'] = re.sub('(\(.*?\))', '', network).strip()
	else:
		parameters['network_clean'] = network
	try:
		parameters['absolute_number'] = int(episode_obj.get('absolute_number'))
	except:
		parameters['absolute_number'] = count + episode
	parameters['realname'] = re.sub('\(\d{4}\)', '', show['seriesname']).strip()
	parameters['showname'] = text.escape(show['seriesname'])
	parameters['clearname'] = text.escape(show['seriesname'])
	parameters['stripname'] = ' '.join(re.compile('[\W_]+').sub(' ', show['seriesname']).split())
	parameters['sortname'] = text.to_utf8(parameters['clearname'])
	parameters['urlname'] = urllib.quote(text.to_utf8(parameters['clearname']))
	parameters['shortname'] = text.to_utf8(parameters['clearname'][1:-1])
	parameters['title'] = text.escape(episode_obj.get('episodename', str(episode)))
	parameters['urltitle'] = urllib.quote(text.to_utf8(parameters['title']))
	parameters['sorttitle'] = text.to_utf8(parameters['title'])
	parameters['shorttitle'] = text.to_utf8(parameters['title'][1:-1])
	articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
	for article in articles:
		if text.to_utf8(parameters['clearname']).startswith(article):
			parameters['sortname'] = text.to_utf8(parameters['clearname']).replace(article,'')
		if text.to_utf8(parameters['title']).startswith(article):
			parameters['sorttitle'] = text.to_utf8(parameters['title']).replace(article,'')
	parameters['firstaired'] = episode_obj.get('firstaired')
	parameters['series_firstaired'] = show.get('firstaired')
	parameters['year'] = show.get('year', 0)
	if parameters['firstaired']:
		parameters['epyear'] = int(parameters['firstaired'].split('-')[0].strip())
		parameters['epmonth'] = int(parameters['firstaired'].split('-')[1].strip())
		parameters['epday'] = int(parameters['firstaired'].split('-')[2].strip())
	else:
		parameters['epyear'] = 1980
		parameters['epmonth'] = 0
		parameters['epday'] = 0
	parameters['imdb'] = show.get('imdb_id', '')
	parameters['tvrage'] = 0
	parameters['epimdb'] = episode_obj.get('imdb_id', '')
	parameters['eptmdb'] = 0
	parameters['eptrakt'] = 0
	parameters['eptvrage'] = 0
	parameters['epid'] = episode_obj.get('id')
	if episode_obj.get('id') != '':
		parameters['plot'] = text.escape(episode_obj.get('overview'))
	else:
		parameters['plot'] = text.escape(show['overview'])
	parameters['series_plot'] = text.escape(show['overview'])
	if episode_obj.get('rating') not in (None, ''):
		parameters['rating'] = episode_obj.get('rating')
	elif show.get('rating') not in (None, ''):
		parameters['rating'] = show.get('rating')
	else:
		parameters['rating'] = 0.0
	if show.get('rating') not in (None, ''):
		parameters['series_rating'] = show.get('rating')
	else:
		parameters['series_rating'] = 0
	if episode_obj.get('ratingcount') != '':
		parameters['votes'] = episode_obj.get('ratingcount')
	else:
		parameters['votes'] = show['ratingcount']
	parameters['mpaa'] = show.get('contentrating')
	parameters['writers'] = episode_obj.get('writer')
	parameters['directors'] = episode_obj.get('director')
	parameters['status'] = show.get('status')
	if show.get('actors') != None and show.get('actors') != '':
		parameters['actors'] = re.sub(r'\<[^)].*?\>', '', show.get('actors'))
	if show.get('genre') != None and '|' in show.get('genre'):
		parameters['genres'] = show.get('genre').replace('|',' / ')[3:-3]
	else:
		parameters['genres'] = show.get('genre')
	parameters['runtime'] = show['runtime']
	parameters['duration'] = int(show['runtime']) * 60
	tvdb_base = 'https://thetvdb.com/banners/'
	if episode_obj.get('filename') != '':
		parameters['thumbnail'] = tvdb_base + str(episode_obj.get('filename'))
	elif show.get('poster') != '':
		parameters['thumbnail'] = show.get('poster')
	if show.get('poster') != '' and show.get('poster') is not None:
		parameters['poster'] = show.get('poster')
	parameters['thumbnail'] = '%sepisodes/%s/%s.jpg' % (tvdb_base, str(show['id']), str(parameters['epid']))
	parameters['banner'] = show.get('banner')
	if show.get('fanart') != None and show.get('fanart') != '':
		parameters['fanart'] = show.get('fanart')
	else:
		parameters['fanart'] = ''
	is_anime = False
	if parameters['genres'] != None and parameters['absolute_number'] and parameters['absolute_number'] != '0' and 'animation' in parameters['genres'].lower():
		tmdb_results = Find(show['id']).info(external_source='tvdb_id')
		for tmdb_show in tmdb_results.get('tv_results', []):
			if 'JP' in tmdb_show['origin_country']:
				is_anime = True
	if is_anime:
		parameters['name'] = u'%s %s' % (parameters['showname'], parameters['absolute_number'])
	else:
		parameters['name'] = u'%s S%02dE%02d' % (parameters['showname'], parameters['season'], parameters['episode'])
	parameters['now'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
	trakt_ids = play_base.get_trakt_ids(id_type='tvdb', id=show['id'], type='show')
	if 'slug' in trakt_ids:
		if trakt_ids['slug'] != '' and trakt_ids['slug'] != None:
			parameters['slug'] = trakt_ids['slug']
		else:
			parameters['slug'] = text.clean_title(parameters['clearname'].lower())
	return parameters

def get_tmdb_episode_parameters(show, preason, prepisode):
	if 'status_code' in str(prepisode):
		return None
	parameters = {'id': show['external_ids']['tvdb_id'], 'season': preason['season_number'], 'episode': prepisode['episode_number']}
	network = show['networks'][0]['name']
	parameters['network'] = network
	if network:
		parameters['network_clean'] = re.sub('(\(.*?\))', '', network).strip()
	else:
		parameters['network_clean'] = network
	parameters['imdb'] = show['external_ids']['imdb_id']
	parameters['tmdb'] = show['id']
	parameters['showname'] = text.escape(show['seriesname'])
	parameters['clearname'] = text.escape(show['seriesname'])
	parameters['urlname'] = urllib.quote(text.to_utf8(parameters['clearname']))
	articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
	parameters['sortname'] = text.to_utf8(parameters['clearname'])
	for article in articles:
		if text.to_utf8(parameters['clearname']).startswith(article):
			parameters['sortname'] = text.to_utf8(parameters['clearname']).replace(article,'')
	parameters['shortname'] = text.to_utf8(parameters['clearname'][1:-1])
	parameters['absolute_number'] = 'na'
	parameters['title'] = prepisode['name']
	parameters['urltitle'] = urllib.quote(text.to_utf8(parameters['title']))
	parameters['sorttitle'] = text.to_utf8(parameters['title'])
	articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
	for article in articles:
		if text.to_utf8(parameters['title']).startswith(article):
			parameters['sorttitle'] = text.to_utf8(parameters['title']).replace(article,'')
	parameters['shorttitle'] = text.to_utf8(parameters['title'][1:-1])
	parameters['firstaired'] = prepisode['air_date']
	parameters['year'] = int(show['first_air_date'].split('-')[0].strip())
	if parameters['firstaired']:
		parameters['epyear'] = int(parameters['firstaired'].split('-')[0].strip())
		parameters['epmonth'] = int(parameters['firstaired'].split('-')[1].strip())
		parameters['epday'] = int(parameters['firstaired'].split('-')[2].strip())
	else:
		parameters['epyear'] = 1900
		parameters['epmonth'] = 0
		parameters['epday'] = 0
	parameters['epid'] = prepisode['id']
	if preason['episodes'][0] != None and preason['episodes'][0] != '' and preason['episodes'][0] != []:
		parameters['poster'] = u'https://image.tmdb.org/t/p/w500%s' % preason['episodes'][0]['still_path']
	elif show['poster_path'] != None and show['poster_path'] != '' and show['poster_path'] != []:
		parameters['poster'] = u'https://image.tmdb.org/t/p/w500%s' % show['poster_path']
	if show['backdrop_path'] != None and show['backdrop_path'] != '' and show['backdrop_path'] != []:
		parameters['fanart'] = u'https://image.tmdb.org/t/p/original%s' % show['backdrop_path']
	else:
		parameters['fanart'] = ''
	parameters['thumbnail'] = parameters['poster']
	try:
		genre = [x for x in show['genre'].split('|') if not x == '']
	except:
		genre = ''
	parameters['genre'] = ' / '.join(genre)
	if 'JP' in show['origin_country']:
		is_anime = True
	else:
		is_anime = False
	if is_anime:
		parameters['name'] = u'%s %s' % (parameters['showname'], parameters['absolute_number'])
	else:
		parameters['name'] = u'%s S%02dE%02d' % (parameters['showname'], parameters['season'], parameters['episode'])
	parameters['now'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
	return parameters

def get_trakt_episode_parameters(show, preason, prepisode):
	if 'status_code' in str(prepisode):
		return None
	parameters = {'id': show['external_ids']['tvdb_id'], 'season': preason['season_number'], 'episode': prepisode['episode_number']}
	network = show['networks'][0]['name']
	parameters['network'] = network
	if network:
		parameters['network_clean'] = re.sub('(\(.*?\))', '', network).strip()
	else:
		parameters['network_clean'] = network
	parameters['imdb'] = show['external_ids']['imdb_id']
	parameters['tmdb'] = show['id']
	parameters['showname'] = text.escape(show['seriesname'])
	parameters['clearname'] = text.escape(show['seriesname'])
	parameters['urlname'] = urllib.quote(text.to_utf8(parameters['clearname']))
	articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
	parameters['sortname'] = text.to_utf8(parameters['clearname'])
	for article in articles:
		if text.to_utf8(parameters['clearname']).startswith(article):
			parameters['sortname'] = text.to_utf8(parameters['clearname']).replace(article,'')
	parameters['shortname'] = text.to_utf8(parameters['clearname'][1:-1])
	parameters['absolute_number'] = 'na'
	parameters['title'] = prepisode['name']
	parameters['urltitle'] = urllib.quote(text.to_utf8(parameters['title']))
	parameters['sorttitle'] = text.to_utf8(parameters['title'])
	articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
	for article in articles:
		if text.to_utf8(parameters['title']).startswith(article):
			parameters['sorttitle'] = text.to_utf8(parameters['title']).replace(article,'')
	parameters['shorttitle'] = text.to_utf8(parameters['title'][1:-1])
	parameters['firstaired'] = prepisode['air_date']
	parameters['year'] = int(show['first_air_date'].split('-')[0].strip())
	if parameters['firstaired']:
		parameters['epyear'] = int(parameters['firstaired'].split('-')[0].strip())
		parameters['epmonth'] = int(parameters['firstaired'].split('-')[1].strip())
		parameters['epday'] = int(parameters['firstaired'].split('-')[2].strip())
	else:
		parameters['epyear'] = 1900
		parameters['epmonth'] = 0
		parameters['epday'] = 0
	parameters['epid'] = prepisode['id']
	if preason['episodes'][0] != None and preason['episodes'][0] != '' and preason['episodes'][0] != []:
		parameters['poster'] = u'https://image.tmdb.org/t/p/w500%s' % preason['episodes'][0]['still_path']
	elif show['poster_path'] != None and show['poster_path'] != '' and show['poster_path'] != []:
		parameters['poster'] = u'https://image.tmdb.org/t/p/w500%s' % show['poster_path']
	if show['backdrop_path'] != None and show['backdrop_path'] != '' and show['backdrop_path'] != []:
		parameters['fanart'] = u'https://image.tmdb.org/t/p/original%s' % show['backdrop_path']
	else:
		parameters['fanart'] = ''
	parameters['thumbnail'] = parameters['poster']
	try:
		genre = [x for x in show['genre'].split('|') if not x == '']
	except:
		genre = ''
	parameters['genre'] = ' / '.join(genre)
	if 'JP' in show['origin_country']:
		is_anime = True
	else:
		is_anime = False
	if is_anime:
		parameters['name'] = u'%s %s' % (parameters['showname'], parameters['absolute_number'])
	else:
		parameters['name'] = u'%s S%02dE%02d' % (parameters['showname'], parameters['season'], parameters['episode'])
	parameters['now'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
	return parameters

def get_tvmaze_episode_parameters(show, preason, prepisode):
	if 'status_code' in str(prepisode):
		return None
	parameters = {'id': show['externals']['thetvdb'], 'season': preason['number'], 'episode': prepisode['number']}
	network = show['network']['name']
	parameters['network'] = network
	if network:
		parameters['network_clean'] = re.sub('(\(.*?\))', '', network).strip()
	else:
		parameters['network_clean'] = network
	parameters['imdb'] = show['externals']['imdb']
	parameters['tvrage'] = show['externals']['tvrage']
	parameters['showname'] = text.escape(show['seriesname'])
	parameters['clearname'] = text.escape(show['seriesname'])
	parameters['urlname'] = urllib.quote(text.to_utf8(parameters['clearname']))
	articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
	parameters['sortname'] = text.to_utf8(parameters['clearname'])
	for article in articles:
		if text.to_utf8(parameters['clearname']).startswith(article):
			parameters['sortname'] = text.to_utf8(parameters['clearname']).replace(article,'')
	parameters['shortname'] = text.to_utf8(parameters['clearname'][1:-1])
	parameters['absolute_number'] = 'na'
	parameters['title'] = prepisode['name']
	parameters['urltitle'] = urllib.quote(text.to_utf8(parameters['title']))
	parameters['sorttitle'] = text.to_utf8(parameters['title'])
	articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
	for article in articles:
		if text.to_utf8(parameters['title']).startswith(article):
			parameters['sorttitle'] = text.to_utf8(parameters['title']).replace(article,'')
	parameters['shorttitle'] = text.to_utf8(parameters['title'][1:-1])
	parameters['firstaired'] = prepisode['airdate']
	parameters['year'] = int(show['premiered'].split('-')[0].strip())
	if parameters['firstaired']:
		parameters['epyear'] = int(parameters['firstaired'].split('-')[0].strip())
		parameters['epmonth'] = int(parameters['firstaired'].split('-')[1].strip())
		parameters['epday'] = int(parameters['firstaired'].split('-')[2].strip())
	else:
		parameters['epyear'] = 1900
		parameters['epmonth'] = 0
		parameters['epday'] = 0
	parameters['epid'] = prepisode['id']
	if prepisode['image'] != None:
		parameters['poster'] = prepisode['image']['original']
	elif preason['image'] != None:
		parameters['poster'] = preason['image']['original']
	elif show['image'] != None:
		parameters['poster'] = show['image']['original']
	parameters['fanart'] = ''
	parameters['thumbnail'] = parameters['poster']
	parameters['genre'] = show['type']
	parameters['now'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
	return parameters