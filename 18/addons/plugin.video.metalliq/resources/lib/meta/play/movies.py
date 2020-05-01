import json
from xbmcswift2 import xbmc
import urllib
import datetime
import re
import string
from meta import plugin, import_tmdb, LANG
from meta.utils.text import to_unicode, parse_year, to_utf8
from meta.utils.properties import set_property
from meta.library.movies import get_movie_player_plugin_from_library
from meta.info import get_movie_metadata
from meta.play.players import get_needed_langs, get_players, ADDON_SELECTOR
from meta.play.channelers import get_needed_langs, ADDON_PICKER
from meta.play.base import get_trakt_ids, active_players, active_channelers, action_cancel, action_play, on_play_video
from settings import SETTING_USE_SIMPLE_SELECTOR, SETTING_MOVIES_DEFAULT_PLAYER, SETTING_MOVIES_DEFAULT_PLAYER_FROM_LIBRARY, SETTING_MOVIES_DEFAULT_PLAYER_FROM_CONTEXT, SETTING_MOVIES_DEFAULT_CHANNELER
from language import get_string as _

def play_movie(tmdb_id, mode):
    import_tmdb()
    # Get players to use
    if mode == 'select':
        play_plugin = ADDON_SELECTOR.id
    elif mode == 'context':
        play_plugin = plugin.get_setting(SETTING_MOVIES_DEFAULT_PLAYER_FROM_CONTEXT, unicode)
    elif mode == 'library':
        play_plugin = get_movie_player_plugin_from_library(tmdb_id)
        if not play_plugin or play_plugin == "default":
            play_plugin = plugin.get_setting(SETTING_MOVIES_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    elif mode == 'default':
        play_plugin = plugin.get_setting(SETTING_MOVIES_DEFAULT_PLAYER, unicode)
    else:
        play_plugin = mode
    if mode != 'context': players = active_players("movies")
    else: players = get_players("movies")
    players = [p for p in players if p.id == play_plugin] or players
    if not players or len(players) == 0:
        xbmc.executebuiltin( "Action(Info)")
        action_cancel()
        return
    # Get movie data from TMDB
    movie = tmdb.Movies(tmdb_id).info(language=LANG, append_to_response="external_ids,alternative_titles,credits,images,keywords,releases,videos,translations,similar,reviews,lists,rating")
    movie_info = get_movie_metadata(movie)
    # Get movie ids from Trakt
    trakt_ids = get_trakt_ids("tmdb", tmdb_id, movie['original_title'],
                    "movie", parse_year(movie['release_date']))
    # Get parameters
    params = {}
    for lang in get_needed_langs(players):
        if lang == LANG:
            tmdb_data = movie
        else:
                        tmdb_data = tmdb.Movies(tmdb_id).info(language=lang, append_to_response="external_ids,alternative_titles,credits,images,keywords,releases,videos,translations,similar,reviews,lists,rating")
        params[lang] = get_movie_parameters(tmdb_data)
        if trakt_ids != None:
            params[lang].update(trakt_ids)
        params[lang]['info'] = movie_info
        params[lang] = to_unicode(params[lang])
    # Go for it
    link = on_play_video(mode, players, params, trakt_ids)
    if link:
        movie = tmdb.Movies(tmdb_id).info(language=LANG)
        action_play({
            'label': movie_info['title'],
            'path': link,
            'info': movie_info,
            'is_playable': True,
            'info_type': 'video',
            'thumbnail': movie_info['poster'],
            'poster': movie_info['poster'],
            'properties' : {'fanart_image' : movie_info['fanart']},
        })

def play_movie_from_guide(tmdb_id, mode):  
    import_tmdb()
    if mode == 'select':
        play_plugin = ADDON_PICKER.id
    elif mode == 'default':
        play_plugin = plugin.get_setting(SETTING_MOVIES_DEFAULT_CHANNELER, unicode)
    else:
        play_plugin = mode
    channelers = active_channelers("movies")
    channelers = [p for p in channelers if p.id == play_plugin] or channelers
    if not channelers:
        xbmc.executebuiltin( "Action(Info)")
        action_cancel()
        return
    movie = tmdb.Movies(tmdb_id).info(language=LANG, append_to_response="external_ids,videos")
    movie_info = get_movie_metadata(movie)
    trakt_ids = get_trakt_ids("tmdb", tmdb_id, movie['original_title'],
                    "movie", parse_year(movie['release_date']))
    params = {}
    for lang in get_needed_langs(channelers):
        if lang == LANG:
            tmdb_data = movie
        else:
            tmdb_data = tmdb.Movies(tmdb_id).info(language=lang)
        params[lang] = get_movie_parameters(tmdb_data)
        if trakt_ids != None:
            params[lang].update(trakt_ids)
        params[lang]['info'] = movie_info
        params[lang] = to_unicode(params[lang])
    link = on_play_video(mode, channelers, params, trakt_ids)
    if link:
        movie = tmdb.Movies(tmdb_id).info(language=LANG)
        action_play({
            'label': movie_info['title'],
            'path': link,
            'info': movie_info,
            'is_playable': True,
            'info_type': 'video',
            'thumbnail': movie_info['poster'],
            'poster': movie_info['poster'],
            'properties' : {'fanart_image' : movie_info['fanart']},
        })

def get_movie_parameters(movie):
    parameters = {}
    parameters['date'] = movie['release_date']
    parameters['premiered'] = movie['release_date']
    parameters['year'] = parse_year(movie['release_date'])
    parameters['released'] = movie['release_date']
    parameters['id'] = movie['id']
    parameters['imdb'] = movie['imdb_id']
    parameters['title'] = movie['title'].replace("&", "%26")
    parameters['striptitle'] = ' '.join(re.compile('[\W_]+').sub(' ', movie['title']).split())
    parameters['urltitle'] = urllib.quote(to_utf8(parameters['title']))
    parameters['sorttitle'] = to_utf8(parameters['title'])
    articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
    for article in articles:
        if to_utf8(parameters['title']).startswith(article): parameters['sorttitle'] = to_utf8(parameters['title']).replace(article,'')
    parameters['shorttitle'] = to_utf8(parameters['title'][1:-1])
    if "movie" in str(parameters['sorttitle']).lower(): parameters['sortesttitle'] = str(parameters['sorttitle']).lower().replace(' movie','')
    elif "movi" in str(parameters['sorttitle']).lower(): parameters['sortesttitle'] = str(parameters['sorttitle']).lower().replace(' movi','')
    else: parameters['sortesttitle'] = parameters['sorttitle']
    parameters['original_title'] = movie['original_title'].replace("&", "%26")
    parameters['name'] = u'%s (%s)' % (parameters['title'], parameters['year'])
    parameters['urlname'] = urllib.quote(to_utf8(parameters['name']))
    parameters['released'] = movie['release_date']
    parameters['rating'] = movie['vote_average']
    genre = [x['name'] for x in movie['genres'] if not x == '']
    studios = [x['name'] for x in movie['production_companies'] if not x == '']
    parameters['studios'] = " / ".join(studios)
    parameters['genres'] = " / ".join(genre)
    if movie['runtime'] and movie['runtime'] != "" and movie['runtime'] != None: parameters['runtime'] = movie['runtime']
    else: parameters['runtime'] = "0"
    if movie['vote_count'] and movie['vote_count'] != "" and movie['vote_count'] != None and movie['vote_count'] != 0: parameters['votes'] = movie['vote_count']
    else: parameters['votes'] = "0"
    if movie['vote_average'] and movie['vote_average'] != "" and movie['vote_average'] != None and movie['vote_average'] != 0: parameters['rating'] = movie['vote_average']
    else: parameters['rating'] = "0"
    if movie['credits']['crew']:
        prewriters = [i["name"] for i in movie['credits']['crew'] if i["department"] == "Writing"]
        writers = []
        for item in prewriters:
            if item not in writers: writers.append(item)
        parameters['writers'] = ", ".join(writers)
    else: parameters['writers'] = ""
    if movie['credits']['crew']:
        predirectors = [i["name"] for i in movie['credits']['crew'] if i["department"] == "Directing"]
        directors = []
        for item in predirectors:
            if item not in directors: directors.append(item)
        parameters['directors'] = ", ".join(directors)
    else: parameters['directors'] = ""
    if movie['credits']['cast']:
        preactors = [i["name"] for i in movie['credits']['cast']]
        actors = []
        for item in preactors:
            if item not in actors: actors.append(item)
        parameters['actors'] = actors
    else: parameters['actors'] = []
    if movie['releases']['countries'][0]['certification']: parameters['mpaa'] = movie['releases']['countries'][0]['certification']
    else: parameters['mpaa'] = ""
    parameters['duration'] = int(parameters['runtime']) * 60
    parameters['plot'] = movie['overview']
    parameters['tagline'] = movie['tagline']
    parameters['poster'] = "http://image.tmdb.org/t/p/original" + str(movie['poster_path'])
    parameters['fanart'] = "http://image.tmdb.org/t/p/original" + str(movie['backdrop_path'])
    parameters['now'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    trakt_ids = get_trakt_ids("tmdb", movie['id'], parameters['title'], "movie", parameters['year'])
    if "slug" in trakt_ids:
        if trakt_ids["slug"] != "" and trakt_ids["slug"] != None:
            parameters['slug'] = trakt_ids["slug"]
        else:
            parameters['slug'] = parameters['title'].lower().replace('~','').replace('#','').replace('%','').replace('&','').replace('*','').replace('{','').replace('}','').replace('\\','').replace(':','').replace('<','').replace('>','').replace('?','').replace('/','').replace('+','').replace('|','').replace('"','').replace(" ","-").replace("--","-")
    return parameters