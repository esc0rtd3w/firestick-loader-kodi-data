import re
import copy
import urllib
import json
from meta import plugin, import_tmdb, LANG
from meta.navigation.base import get_background_path
from meta.utils.text import parse_year, to_utf8
from xbmcswift2 import xbmc

def get_movie_metadata(movie, genres_dict=None):
    info = {}
    info['title'] = movie['title']
    try: info['premiered'] = movie['release_date']
    except: info['premiered'] = "2020-02-02"
    info['year'] = info['premiered'][:4]
    info['name'] = u'%s (%s)' % (info['title'], info['year'])
    info['rating'] = movie['vote_average']
    info['votes'] = movie['vote_count']
    info['plot'] = movie['overview']
    info['originaltitle'] = movie['original_title']
    info['tmdb'] = str(movie['id'])
    if movie['poster_path'] and movie['poster_path'] != None and movie['poster_path'] != "": info['poster'] = u'%s%s' % ('http://image.tmdb.org/t/p/original', movie['poster_path'])
    else: info['poster'] = "https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/default/unavailable.png"
    if movie['backdrop_path'] and movie['backdrop_path'] != None and movie['backdrop_path'] != "": info['fanart'] = u'%s%s' % ('http://image.tmdb.org/t/p/original', movie['backdrop_path'])
    else: info['fanart'] = get_background_path()
    try: info['genre'] = u' / '.join([x['name'] for x in movie['genres']])
    except KeyError:
        if genres_dict: 
            try: info['genre'] = u' / '.join([genres_dict[x] for x in movie['genre_ids']])
            except: info['genre'] = ''
    return info

def get_trakt_movie_metadata(movie, genres_dict=None):
    info = {}
    info['title'] = movie['title']
    info['year'] = movie['year']
    info['name'] = u'%s (%s)' % (info['title'], info['year'])
    info['premiered'] = movie.get('released')
    info['rating'] = movie.get('rating')
    info['votes'] = movie.get('votes')
    info['tagline'] = movie.get('tagline')
    info['plot'] = movie.get('overview')
    if xbmc.getInfoLabel('System.BuildVersion')[:2] == "14": info['duration'] = int(movie.get('runtime') or 0)
    else: info['duration'] = (movie.get('runtime') or 0) * 60
    info['mpaa'] = movie.get('certification')
    info['playcount'] = movie.get('plays')
    if not info['playcount'] and movie.get('watched'): info['playcount'] = 1
    info['tmdb'] = movie['ids'].get('tmdb')
    info['trakt_id'] = movie['ids'].get('trakt_id')
    info['imdb_id'] = movie['ids'].get('imdb')
    if info['tmdb'] == None: info['tmdb'] = ""
    if info['trakt_id'] == None: info['trakt_id'] = ""
    if info['imdb_id'] == None: info['imdb_id'] = ""
    images = item_images("movie", tmdb_id=info['tmdb'], imdb_id=info['imdb_id'], name=info['title'])
    info['poster'] = images[0]
    info['fanart'] = images[1]
    if 'genres' in movie:
        if genres_dict: info['genre'] = u' / '.join([genres_dict[x] for x in movie['genres']])
    else: info['genre'] = ""
    if movie.get('trailer'): info['trailer'] = make_trailer(movie['trailer'])
    if not info['playcount'] and movie.get('watched'): info['playcount'] = 1
    return info

def make_trailer(trailer_url):
    match = re.search('\?v=(.*)', trailer_url)
    if match: return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (match.group(1))

def get_tvshow_metadata_trakt(show, genres_dict=None):
    info = {}
    info['title'] = show['title']
    info['year'] = show['year']
    info['name'] = u'%s (%s)' % (info['title'], info['year'])
    info['tvshowtitle'] = info['title']
    info['premiered'] = show.get('released')
    info['rating'] = show.get('rating')
    info['votes'] = show.get('votes')
    info['tagline'] = show.get('tagline')
    info['plot'] = show.get('overview')
    info['studio'] = show.get('network','')
    info['mpaa'] = show.get('certification')
    info['playcount'] = show.get('plays')
    if not info['playcount'] and show.get('watched'): info['playcount'] = 1
    info['tmdb'] = show['ids'].get('tmdb')
    info['trakt_id'] = show['ids'].get('trakt_id')
    info['imdb_id'] = show['ids'].get('imdb')
    info['tvdb_id'] = show['ids'].get('tvdb')
    if info['tmdb'] == None: info['tmdb'] = ""
    if info['trakt_id'] == None: info['trakt_id'] = ""
    if info['imdb_id'] == None: info['imdb_id'] = ""
    if info['tvdb_id'] == None: info['tvdb_id'] = ""
    images = item_images("tv", tmdb_id=info['tmdb'], imdb_id=info['imdb_id'], tvdb_id=info['tvdb_id'], name=info['title'])
    info['poster'] = images[0]
    info['fanart'] = images[1]
    if genres_dict: info['genre'] = u" / ".join([genres_dict[x] for x in show['genres']])
    if show.get('trailer'): info['trailer'] = make_trailer(show['trailer'])
    return info

def get_tvshow_metadata_tvdb(tvdb_show, banners=True):
    info = {}
    if tvdb_show is None: return info
    if tvdb_show['genre']:
        if '|' in tvdb_show['genre']: genres = tvdb_show['genre'].replace('|',' / ')
        info['genre'] = genres[3:-3]
    info['tvdb_id'] = str(tvdb_show['id'])
    info['name'] = tvdb_show['seriesname']
    info['title'] = tvdb_show['seriesname']
    info['tvshowtitle'] = tvdb_show['seriesname']
    info['originaltitle'] = tvdb_show['seriesname']
    info['plot'] = tvdb_show.get('overview', '')
    if banners: info['poster'] = tvdb_show.get_poster(language=LANG)
    info['fanart'] = tvdb_show.get('fanart', '')
    info['rating'] = tvdb_show.get('rating')
    info['votes'] = tvdb_show.get('ratingcount')
    info['year'] = tvdb_show.get('year', 0)
    info['studio'] = tvdb_show.get('network','')
    info['imdb_id'] = tvdb_show.get('imdb_id', '')
    if xbmc.getInfoLabel('System.BuildVersion')[:2] == "14": info['duration'] = int(tvdb_show.get('runtime') or 0)
    else: info['duration'] = int(tvdb_show.get('runtime') or 0) * 60
    return info

def get_tvshow_metadata_tmdb(show, genres_dict=None):
    info = {}
    if show is None: return info
    if 'id' in show: info['tmdb'] = str(show['id'])
    info['name'] = show['name']
    info['title'] = show['name']
    info['tvshowtitle'] = show['original_name']
    info['originaltitle'] = show['original_name']
    info['plot'] = show['overview']
    info['rating'] = str(show['vote_average'])
    info['votes'] = str(show['vote_count'])
    try: info['genre'] = u' / '.join([x['name'] for x in show['genres']])
    except KeyError:
        if genres_dict:
            try: info['genre'] = u' / '.join([genres_dict[x] for x in show['genre_ids']])
            except: info['genre'] = ''
    if show['poster_path']: info['poster'] = u'%s%s' % ('http://image.tmdb.org/t/p/original', show['poster_path'])
    else: info['poster'] = "https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/default/unavailable.png"
    if show['backdrop_path']: info['fanart'] = u'%s%s' % ('http://image.tmdb.org/t/p/original', show['backdrop_path'])
    else: info['fanart'] = get_background_path()
    return info

def get_tvshow_metadata_tvmaze(show):
    info = {}
    if show is None: return info
    if show['externals']['thetvdb'] is not None: info['id'] = show['externals']['thetvdb']
    if show['externals']['imdb'] is not None: info['imdb'] = show['externals']['imdb']
    info['name'] = show['name']
    info['title'] = show['name']
    info['tvshowtitle'] = show['name']
    info['originaltitle'] = show['name']
    info['plot'] = re.sub(r'\<[^)].*?\>', '', show['summary']).replace("&amp;","&").replace("\t","")
    info['rating'] = str(show['rating']['average'])
    info['votes'] = str(show['weight'])
    info['genre'] = show['type']
    if show['image']['original']: info['poster'] = show['image']['original']
    info['fanart'] = get_background_path()
    return info

def get_season_metadata_tvdb(show_metadata, season, banners=True):
    info = copy.deepcopy(show_metadata)
    del info['title']
    info['season'] = season.num
    if banners: info['poster'] = season.get_poster(language=LANG)
    return info

def get_season_metadata_tmdb(show_metadata, season):
    info = copy.deepcopy(show_metadata)
    del info['name']
    info['season'] = season['season_number']
    if season['images']['posters']: info['poster'] = season['images']['posters'][0]
    if show_metadata['fanart']: info['fanart'] = show_metadata['fanart']
    else: info['fanart'] = ""
    return info

def get_season_metadata_trakt(show_metadata, season, banners=True):
    info = copy.deepcopy(show_metadata)
    del info['title']
    info['season'] = season['number']
    if not info['playcount'] and season.get('watched'): info['playcount'] = 1
    return info

def get_season_metadata_tvmaze(show_metadata, season):
    info = copy.deepcopy(show_metadata)
    del info['name']
    info['season'] = season['number']
    info['fanart'] = get_background_path()
    return info

def get_episode_metadata_tvdb(season_metadata, episode, banners=True):
    info = copy.deepcopy(season_metadata)
    info['episode'] = episode.get('episodenumber')
    info['title'] = episode.get('episodename','')
    info['aired'] = episode.get('firstaired','')
    info['premiered'] = episode.get('firstaired','')
    info['rating'] = episode.get('rating', '')
    info['plot'] = episode.get('overview','')
    info['plotoutline'] = episode.get('overview','')
    info['votes'] = episode.get('ratingcount','')
    if banners: info['poster'] = episode['filename']
    return info

def get_episode_metadata_tmdb(season_metadata, episode):
    info = copy.deepcopy(season_metadata)
    if episode == None or episode == "" or "status_code" in str(episode): return info
    info['episode'] = episode['episode_number']
    info['title'] = episode['name']
    info['aired'] = episode['air_date']
    info['premiered'] = episode['air_date']
    info['rating'] = episode['vote_average']
    info['plot'] = episode['overview']
    info['plotoutline'] = episode['overview']
    info['votes'] = episode['vote_count']
    if episode['still_path']: info['poster'] = u'%s%s' % ('http://image.tmdb.org/t/p/original', episode['still_path'])
    elif season_metadata['poster']: info['poster'] = u'%s%s' % ('http://image.tmdb.org/t/p/original', season_metadata['poster'])
    else: info['poster'] = ''
    if season_metadata['fanart']: info['fanart'] = season_metadata['fanart']
    else: info['fanart'] = ''
    return info

def get_episode_metadata_trakt(season_metadata, episode):
    info = copy.deepcopy(season_metadata)
    info['episode'] = episode.get('number')
    info['title'] = episode.get('title','')
    info['aired'] = episode.get('first_aired','')
    info['premiered'] = episode.get('first_aired','')
    info['rating'] = episode.get('rating', '')
    info['plot'] = episode.get('overview','')
    info['plotoutline'] = episode.get('overview','')
    info['votes'] = episode.get('votes','')
    if not info['playcount'] and episode.get('watched'): info['playcount'] = 1
    return info

def get_episode_metadata_tvmaze(season_metadata, episode):
    info = copy.deepcopy(season_metadata)
    if episode == None or episode == "": return info
    info['episode'] = episode['number']
    info['season'] = episode['season']
    info['title'] = episode['name']
    info['aired'] = episode['airdate']
    info['premiered'] = episode['airdate']
    info['plot'] = re.sub(r'\<[^)].*?\>', '', str(episode['summary'])).replace("&amp;","&").replace("\t","")
    info['plotoutline'] = re.sub(r'\<[^)].*?\>', '', str(episode['summary'])).replace("&amp;","&").replace("\t","")
    if episode['image']: info['poster'] = episode['image']['original']
    info['fanart'] = get_background_path()
    return info

def item_images(type, tmdb_id=None, imdb_id=None, tvdb_id=None, name=None):
    poster = ""
    fanart = ""
    response = ""
    if not tmdb_id and not imdb_id and not tvdb_id and not tvrage_id and not name: return None
    if type == "movie" and tmdb_id != None and tmdb_id != "": response = tmdb.Movies(tmdb_id).info()
    elif type == "tv"  and tmdb_id != None and tmdb_id != "": response = tmdb.TV(tmdb_id).info()
    elif type == "tv"  and tvdb_id != None and tvdb_id != "": response = tmdb.Find(tvdb_id).info(external_source="tvdb_id")
    elif                   imdb_id != None and imdb_id != "": response = tmdb.Find(imdb_id).info(external_source="imdb_id")
    if response == "": return False
    if tmdb_id == None:
        if   type == "movie"  : response = response.get("movie_results")
        elif type == "tv"     : response = response.get("tv_results")
        elif type == "season" : response = response.get("season_results")
        elif type == "episode": response = response.get("episode_results")
    if isinstance(response, dict):
        if response.get("backdrop_path"): fanart = "http://image.tmdb.org/t/p/original/%s" % response.get("backdrop_path")
        else                            : fanart = get_background_path()
        if response.get("poster_path")  : poster = "http://image.tmdb.org/t/p/original/%s" % response.get("poster_path")
        else                            : poster = "https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/default/unavailable.png"
    elif isinstance(response, list):
        if response["backdrop_path"]: fanart = "http://image.tmdb.org/t/p/original/%s" % response["backdrop_path"]
        else                        : fanart = get_background_path()
        if response["poster_path"]  : poster = "http://image.tmdb.org/t/p/original/%s" % response["poster_path"]
        else                        : poster = "https://raw.githubusercontent.com/OpenELEQ/Style/master/MetalliQ/default/unavailable.png"
    images = [poster, fanart]
    return images 
