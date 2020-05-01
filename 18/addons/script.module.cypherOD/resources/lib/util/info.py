# -*- coding: utf-8 -*-
"""
    info.py --- Collection of functions to get metadata for items
    Copyright (C) 2017, Jen

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
"""
import copy
import re

import xbmc
import xbmcaddon
import time
import requests
import resources.lib.external.tmdbsimple as tmdbsimple
import resources.lib.external.tvdb_api as tvdb_api
from resources.lib.plugin import run_hook
from koding import route
import koding
import pickle
import __builtin__
from language import get_string as _

ADDON = xbmcaddon.Addon()
TRAKT_API_ENDPOINT = "https://api.trakt.tv"
TRAKT_CLIENT_ID = __builtin__.trakt_client_id
TRAKT_CLIENT_SECRET = __builtin__.trakt_client_secret
TTL = 1440 * 31

if ADDON.getSetting("language_id") == "system":
    LANG = xbmc.getLanguage(
        xbmc.ISO_639_1)
else:
    LANG = ADDON.getSetting("language_id")

tvdb = tvdb_api.Tvdb(
    __builtin__.tvdb_api_key,
    language=LANG,
    cache=xbmc.translatePath(xbmcaddon.Addon().getSetting("cache_folder")))


def get_movie_metadata(movie_id):
    """
    get metadata for a movie

    wrapper function that gets metadata from the provider set in settings
    ARGS:
        movie_id: movie identifier (depends on set metadata provider)
    RETURNS:
        movie metadata as dict
    """
    metadata_provider = ADDON.getSetting("movie_metadata_provider")
    info, created_time = fetch_from_db(movie_id, metadata_provider, LANG)
    if info:
        return info
    elif created_time and float(created_time) <= time.time() + 3600:
        return info
    try:
        if metadata_provider == "Trakt":
            headers = {
                'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': TRAKT_CLIENT_ID
            }
            url = TRAKT_API_ENDPOINT + "/movies/" + movie_id + '?extended=full'
            info = requests.get(url, headers=headers, verify=False).json()
            xbmc.log("info:" + repr(info), xbmc.LOGNOTICE)
            if LANG != "en":
                translation_url = TRAKT_API_ENDPOINT + \
                    "/movies/" + movie_id + "/translations/" + LANG
                translation_info = requests.get(
                    translation_url, headers=headers, verify=False).json()
                if translation_info:
                    translation_info = translation_info[0]
                    for key in translation_info.iterkeys():
                        info[key] = translation_info[key]
            genres_dict = trakt_genres("movies")
            info = __convert_trakt_movie_metadata(info, genres_dict)
        elif metadata_provider == "TMDB":
            genres_dict = tmdb_movie_genres(LANG)
            info = tmdbsimple.Find(movie_id).info(
                external_source="imdb_id", language=LANG)["movie_results"][0]
            if (not info or (info.get("overview", None) is None and info.get('plot', None) is None) and
                    LANG != "en"):
                info, created_time = fetch_from_db(movie_id, metadata_provider, "en")
                if info:
                    return info
                else:
                    info = tmdbsimple.Find(movie_id).info(
                        external_source="imdb_id",
                        language="en")["movie_results"][0]
                    info = _convert_tmdb_movie_metadata(
                        info, movie_id, genres_dict)
                    save_to_db(movie_id, metadata_provider, "en", info)
            info = _convert_tmdb_movie_metadata(info, movie_id, genres_dict)
    except:
        pass
    save_to_db(movie_id, metadata_provider, LANG, info)
    return info


def __convert_trakt_movie_metadata(movie, genres_dict=None):
    """
    converts trakt movie metadata to format suited for kodiswift
    Args:
        movie: dictionary of trakt movie metadata
        genres_dict: dictionary of kodi movie genres
    Returns
        movie metadata
    """
    info = {
        'title': movie['title'],
        'year': movie['year'],
        'premiered': movie.get('released'),
        'rating': movie.get('rating'),
        'votes': movie.get('votes'),
        'tagline': movie.get('tagline'),
        'plot': movie.get('overview'),
        'duration': 60 * (movie.get('runtime') or 0),
        'mpaa': movie.get('certification'),
        'playcount': movie.get('plays'),
        'tmdb': movie['ids'].get('tmdb'),
        'trakt_id': movie['ids'].get('trakt_id'),
        'imdb_id': movie['ids'].get('imdb'),
        'poster': "",
        'fanart': ""
    }
    info['name'] = u'%s (%s)' % (info['title'], info['year'])
    if not info['playcount'] and movie.get('watched'):
        info['playcount'] = 1
    if genres_dict:
        info['genre'] = u" / ".join([genres_dict[x] for x in movie['genres']])
    if movie.get('trailer'):
        info['trailer'] = make_trailer(movie['trailer'])
    return info


def _convert_tmdb_movie_metadata(movie, imdb_id, genres_dict=None):
    """
converts tmdb movie metadata to format suited for kodiswift
    :param movie: dictionary of tmdb movie metadata
    :type movie: dict[str,str or dict]
    :param dict genres_dict: dictionary of kodi movie genres
    :return: movie metadata
    :rtype: dict[str,str]
    """
    info = {
        'title': movie['title'],
        'year': parse_year(movie['release_date']),
        'premiered': movie['release_date'],
        'rating': movie['vote_average'],
        'votes': movie['vote_count'],
        'originaltitle': movie['original_title'],
        'tmdb': str(movie['id']),
        'imdb_id': imdb_id,
        'poster': '%s%s' % ("http://image.tmdb.org/t/p/w500",
                             movie['poster_path']),
        'fanart': '%s%s' % ("http://image.tmdb.org/t/p/original",
                             movie['backdrop_path'])
    }
    if 'overview' in movie:
        info['plot'] = movie['overview']
    elif 'plot' in movie:
        info['plot'] = movie['plot']
    else:
        info['plot'] = ''
    info['name'] = u'%s (%s)' % (info['title'], info['year'])
    try:
        info['genre'] = u" / ".join([x['name'] for x in movie['genres']])
    except KeyError:
        if genres_dict:
            info['genre'] = u" / ".join(
                [genres_dict[x] for x in movie['genre_ids']])
        else:
            info['genre'] = ''
    videos = tmdbsimple.Movies(movie["id"]).videos()
    for video in videos["results"]:
        xbmc.log("video:" + repr(video), xbmc.LOGNOTICE)
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            info["trailer"] = 'plugin://plugin.video.youtube/play/?video_id=%s' % (video["key"])
            break
    return info


def make_trailer(trailer_url):
    """
makes a playable trailer url
    :param str trailer_url: youtube identifier for the trailer
    :return: playable url for the trailer
    :rtype: str
    """
    match = re.search('\?v=(.*)', trailer_url)
    if match:
        return 'plugin://plugin.video.youtube/play/?video_id=%s' % (
            match.group(1))


def get_show_metadata(show_id):
    """
    get metadata for a tv show

    wrapper function that gets metadata from the provider set in settings
    Args:
        show_id: tv show identifier (depends on set metadata provider)
    Returns:
        tv show metadata
    """
    metadata_provider = ADDON.getSetting("tv_metadata_provider")
    info, created_time = fetch_from_db(show_id, metadata_provider, LANG)
    if info:
        return info
    elif created_time and float(created_time) <= time.time() + 3600:
        return info
    try:
        if metadata_provider == "Trakt":
            headers = {
                'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': TRAKT_CLIENT_ID
            }
            url = TRAKT_API_ENDPOINT + "/shows/" + show_id + '?extended=full'
            info = requests.get(url, headers=headers, verify=False).json()
            if LANG != "en":
                translation_url = TRAKT_API_ENDPOINT + \
                    "/shows/" + show_id + "/translations/" + LANG
                translation_info = requests.get(
                    translation_url, headers=headers, verify=False).json()
                if translation_info:
                    translation_info = translation_info[0]
                    for key in translation_info.iterkeys():
                        info[key] = translation_info[key]
            genres_dict = trakt_genres("shows")
            info = _convert_trakt_tvshow_metadata(info, genres_dict)
        elif metadata_provider == "TVDB":
            tvdb_id = tvdb.search_by_imdb(show_id)
            if tvdb_id:
                info = tvdb[tvdb_id]
                info = _convert_tvdb_tvshow_metadata(info, show_id, language=LANG)
    except:
        pass
    save_to_db(show_id, metadata_provider, LANG, info)
    return info


def _convert_trakt_tvshow_metadata(show, genres_dict=None):
    """
    converts trakt tv show metadata to format suited for kodiswift
    Args:
        show: dictionary of trakt tv show metadata
        dictionary of kodi tv genres
    Returns:
        tv show metadata
    """
    info = {
        'title': show['title'],
        'year': show['year'],
        'premiered': show.get('released'),
        'rating': show.get('rating'),
        'votes': show.get('votes'),
        'tagline': show.get('tagline'),
        'plot': show.get('overview'),
        'duration': 60 * (show.get('runtime') or 0),
        'studio': show.get('network', ''),
        'mpaa': show.get('certification'),
        'playcount': show.get('plays'),
        'tmdb': show['ids'].get('tmdb'),
        'trakt_id': show['ids'].get('trakt_id'),
        'imdb_id': show['ids'].get('imdb'),
        'tvdb_id': show['ids'].get('tvdb'),
        'poster': "",
        'fanart': ""
    }
    info['tvshowtitle'] = info['title']
    info['name'] = u'%s (%s)' % (info['title'], info['year'])
    if not info['playcount'] and show.get('watched'):
        info['playcount'] = 1
    if genres_dict:
        info['genre'] = u" / ".join([genres_dict[x] for x in show['genres']])
    if show.get('trailer'):
        info['trailer'] = make_trailer(show['trailer'])
    return info


def _convert_tvdb_tvshow_metadata(tvdb_show, imdb_id, banners=True,
                                  language="en"):
    """
    converts tvdb tv show metadata to format suited for kodiswift
    Args:
        tvdb_show: dictionary of tvdb tv show metadata
        banners: whether to get the poster image from tvdb
        language: the language to get the poster image in
    Returns:
        tv show metadata
    """
    info = {}
    if tvdb_show is None:
        return info
    info['tvdb_id'] = str(tvdb_show['id'])
    info['name'] = tvdb_show['seriesname']
    info['title'] = tvdb_show['seriesname']
    info['tvshowtitle'] = tvdb_show['seriesname']
    info['originaltitle'] = tvdb_show['seriesname']
    # info['genre'] =
    info['plot'] = tvdb_show.get('overview', '')
    info['fanart'] = tvdb_show.get('fanart', '')
    info['rating'] = tvdb_show.get('rating')
    info['votes'] = tvdb_show.get('ratingcount')
    info['year'] = tvdb_show.get('year', 0)
    info['studio'] = tvdb_show.get('network', '')
    info['imdb_id'] = tvdb_show.get('imdb_id', '')
    info['genre'] = u" / ".join(tvdb_show.get('genre', '').split("|")[1:-1])
    info["imdb_id"] = imdb_id
    if banners:
        info['poster'] = tvdb_show.get_poster(language=language)
    return info


def get_episode_metadata(show_id, season_num, episode_num):
    """
    get metadata for a tv show episode

    wrapper function that gets metadata from the provider set in settings
    Args:
        show_id: tv show identifier (depends on set metadata provider)
        season_num: season number of the episode
        episode_num: episode number in the season
    Returns:
        tv episode metadata
    """
    metadata_provider = ADDON.getSetting("tv_metadata_provider")
    info, created_time = fetch_episode_from_db(show_id,
                                               str(season_num),
                                               str(episode_num),
                                               metadata_provider, LANG)
    if info:
        return info
    elif created_time and float(created_time) <= time.time() + 3600:
        return info
    if info:
        return info
    try:
        if metadata_provider == "Trakt":
            headers = {
                'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': TRAKT_CLIENT_ID
            }
            url = '{0}/shows/{1}/seasons/{2}/episodes/{3}?extended=full'.format(
                TRAKT_API_ENDPOINT, show_id, season_num, episode_num)
            show_metadata = get_show_metadata(show_id)
            info = requests.get(url, headers=headers, verify=False).json()
            if LANG != "en":
                translation_url = TRAKT_API_ENDPOINT + \
                    "/shows/{1}/seasons/{2}/episodes/{3}/translations/{4}".format(
                        TRAKT_API_ENDPOINT, show_id, season_num,
                        episode_num, LANG)
                translation_info = requests.get(
                    translation_url, headers=headers, verify=False).json()
                if translation_info:
                    translation_info = translation_info[0]
                    for key in translation_info.iterkeys():
                        info[key] = translation_info[key]
            info = _convert_trakt_episode_metadata(show_metadata, info)
        elif metadata_provider == "TVDB":
            tvdb_id = tvdb.search_by_imdb(show_id)
            if tvdb_id:
                show = tvdb[tvdb_id]
                show_metadata = get_show_metadata(show_id)
                season = show[int(season_num)]
                season_metadata = _convert_tvdb_season_metadata(
                    show_metadata, season, language=LANG)
                episode_metadata = _convert_tvdb_episode_metadata(
                    show_id, season_metadata, season[int(episode_num)])
                info = episode_metadata
    except:
        pass
    save_episode_to_db(show_id, season_num, episode_num, metadata_provider,
                       LANG, info)
    return info


def _convert_trakt_episode_metadata(show_metadata, episode, banners=True):
    """
    converts trakt episode metadata to format suited for kodiswift
    Args:
        show_metadata: dictionary of trakt tv show metadata
        episode: dictionary of trakt episode metadata
        banners: whether to get the poster image from metadata (not functional yet)
    Returns:
        episode metadata
    """
    info = copy.deepcopy(show_metadata)
    info['episode'] = episode.get('number')
    info['title'] = episode.get('title', '')
    info['aired'] = episode.get('first_aired', '')
    info['premiered'] = episode.get('first_aired', '')
    info['rating'] = episode.get('rating', '')
    info['plot'] = episode.get('overview', '')
    info['plotoutline'] = episode.get('overview', '')
    info['votes'] = episode.get('votes', '')
    if banners:
        info['poster'] = ""
    return info


def _convert_tvdb_season_metadata(show_metadata,
                                  season,
                                  banners=True,
                                  language="en"):
    """
    helper function to get season metadata from tvdb
    Args:
        show_metadata: dictionary of tvdb tv show metadata
        season: dictionary of season metadata
        banners: whether to get the poster image from metadata
        language: the language to get the poster image in
    Returns:
    season metadata
    """
    info = copy.deepcopy(show_metadata)
    del info['title']
    info['season'] = season.num
    if banners:
        info['poster'] = season.get_poster(language=language)
    return info


def _convert_tvdb_episode_metadata(imdb_id , season_metadata, episode,
                                   banners=True):
    """
    converts tvdb episode metadata to format suited for kodiswift
    Args:
        season_metadata: dictionary of tvdb season metadata
        episode: dictionary of tvdb episode metadata
        banners: whether to get the poster image from metadata
    Returns:
        episode metadata
    """
    info = copy.deepcopy(season_metadata)
    info['episode'] = episode.get('episodenumber')
    info['title'] = episode.get('episodename', '')
    info['aired'] = episode.get('firstaired', '')
    info['premiered'] = episode.get('firstaired', '')
    info['rating'] = episode.get('rating', '')
    info['plot'] = episode.get('overview', '')
    info['plotoutline'] = episode.get('overview', '')
    info['votes'] = episode.get('ratingcount', '')
    info['imdb_id'] = imdb_id
    if banners:
        info['poster'] = episode['filename']
    return info


def fetch_from_db(identifier, provider, lang):
    """
    get item's meta info from database
    Args:
        identifier: identifier of the item
        provider: metadata provider to fetch info for
        lang: language to fetch info for
    Returns
        item's metadata
    """
    import koding

    versionspec = {"columns": {"version": "TEXT"}}
    koding.Create_Table("version", versionspec)
    if not koding.Get_All_From_Table("version"):
        koding.Add_To_Table("version", {"version": "0.0.1"})

    meta_spec = {
        "columns": {
            "identifier": "TEXT",
            "provider": "TEXT",
            "lang": "TEXT",
            "meta": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "identifier, provider, lang"
        }
    }
    koding.Create_Table("meta", meta_spec)
    match = koding.Get_From_Table(
        "meta", {"identifier": identifier,
                 "provider": provider,
                 "lang": lang})
    if match:
        match = match[0]
        if not match["meta"]:
            return None, match["created"]
        match_meta = match["meta"].replace("'", "\"")
        try:
            match_meta = match_meta.encode('ascii', 'ignore')
        except:
            match_meta = match_meta.decode('utf-8').encode('ascii', 'ignore')
        return pickle.loads(match_meta), match["created"]
    else:
        return [], None


def fetch_episode_from_db(identifier, season, episode, provider, lang):
    """
    get episode's meta info from database
    Args:
        identifier: identifier of the item
        season: season number of the episode
        episode: episode number of the episode
        provider: metadata provider to fetch info for
        lang: language to fetch info for
    Returns:
        item's metadata
    """
    import koding

    versionspec = {"columns": {"version": "TEXT"}}
    koding.Create_Table("version", versionspec)
    if not koding.Get_All_From_Table("version"):
        koding.Add_To_Table("version", {"version": "0.0.1"})

    episode_meta_spec = {
        "columns": {
            "identifier": "TEXT",
            "season": "TEXT",
            "episode": "TEXT",
            "provider": "TEXT",
            "lang": "TEXT",
            "meta": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "identifier, provider, lang",
        }
    }
    koding.Create_Table("episode_meta", episode_meta_spec)
    match = koding.Get_From_Table("episode_meta", {
        "identifier": identifier,
        "provider": provider,
        "season": season,
        "episode": episode,
        "lang": lang
    })
    if match:
        match = match[0]
        if not match["meta"]:
            return None, match["created"]
        match_meta = match["meta"].replace("'", "\"")
        try:
            match_meta = match_meta.encode('ascii', 'ignore')
        except:
            match_meta = match_meta.decode('utf-8').encode('ascii', 'ignore')
        return pickle.loads(match_meta), match["created"]
    else:
        return [], None


def save_to_db(identifier, provider, lang, meta):
    """
    save item's meta info tp database
    Args:
        identifier: identifier of the item
        provider: metadata provider to sabe info for
        lang: language to save info for
        meta: metadata
    """
    import time
    import koding

    koding.Remove_From_Table(
        "meta", {"identifier": identifier,
                 "provider": provider,
                 "lang": lang})
    koding.Add_To_Table("meta", {
        "identifier": identifier,
        "provider": provider,
        "lang": lang,
        "meta": pickle.dumps(meta).replace("\"", "'"),
        "created": time.time()
    })


def save_episode_to_db(identifier, season, episode, provider, lang, meta):
    """
    save episode's meta info tp database
    Args:
        identifier: identifier of the item
        season: season number of the episode
        episode: episode number of the episode
        provider: metadata provider to sabe info for
        lang: language to save info for
        meta: metadata
    """
    import time
    import koding

    koding.Remove_From_Table("episode_meta", {
        "identifier": identifier,
        "provider": provider,
        "season": season,
        "episode": episode,
        "lang": lang
    })

    koding.Add_To_Table("episode_meta", {
        "identifier": identifier,
        "provider": provider,
        "season": season,
        "episode": episode,
        "lang": lang,
        "meta": pickle.dumps(meta).replace("\"", "'"),
        "created": time.time()
    })


def tmdb_movie_genres(lang):
    """
retrieve movie genre information from tmdb
    :return dict: genre information
    """
    genres = None
    try:
        result = tmdbsimple.Genres().list(language=lang)
        genres = dict([(i['id'], i['name']) for i in result['genres']
                       if i['name'] is not None])
    except:
        pass
    if genres:
        return genres
    else:
        mock = [{
            "id": 28,
            "name": "Action"
        }, {
            "id": 12,
            "name": "Adventure"
        }, {
            "id": 16,
            "name": "Animation"
        }, {
            "id": 35,
            "name": "Comedy"
        }, {
            "id": 80,
            "name": "Crime"
        }, {
            "id": 99,
            "name": "Documentary"
        }, {
            "id": 18,
            "name": "Drama"
        }, {
            "id": 10751,
            "name": "Family"
        }, {
            "id": 14,
            "name": "Fantasy"
        }, {
            "id": 10769,
            "name": "Foreign"
        }, {
            "id": 36,
            "name": "History"
        }, {
            "id": 27,
            "name": "Horror"
        }, {
            "id": 10402,
            "name": "Music"
        }, {
            "id": 9648,
            "name": "Mystery"
        }, {
            "id": 10749,
            "name": "Romance"
        }, {
            "id": 878,
            "name": "Science Fiction"
        }, {
            "id": 10770,
            "name": "TV Movie"
        }, {
            "id": 53,
            "name": "Thriller"
        }, {
            "id": 10752,
            "name": "War"
        }, {
            "id": 37,
            "name": "Western"
        }]
        return dict([(i['id'], i['name'], i['properties']) for i in mock])


def trakt_genres(genre_type):
    """
retrieve genre information from trakt
    :param str genre_type: content type to retrieve info for (movie, show)
    :return dict: genre information
    """
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_CLIENT_ID
    }
    url = TRAKT_API_ENDPOINT + '/genres/' + genre_type
    info = requests.get(url, headers=headers, verify=False).json()
    genres_dict = dict([(x['slug'], x['name']) for x in info])
    return genres_dict


@route("tvshow_extended_info", ["url"])
def tv_get_extended_info(imdb):
    import xbmc

    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_CLIENT_ID
    }
    url = TRAKT_API_ENDPOINT + "/search/imdb/" + imdb + '?type=show'
    info = requests.get(url, headers=headers, verify=False).json()[0]
    tvdb = info["show"]["ids"]["tvdb"]

    if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"):
        xbmc.executebuiltin(
            "RunScript(script.qlickplay,info=tvinfo,tvdb_id={0})".format(tvdb))
    elif xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"):
        xbmc.executebuiltin(
            "RunScript(script.extendedinfo,info=extendedtvinfo,tvdb_id={0})".
            format(tvdb))
    return


@route("season_extended_info", ["url"])
def season_get_extended_info(item):
    import xbmc
    item = eval(item)
    imdb = item["imdb"]
    season = item["season"]

    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_CLIENT_ID
    }
    url = TRAKT_API_ENDPOINT + "/search/imdb/" + imdb + '?type=show'
    info = requests.get(url, headers=headers, verify=False).json()[0]
    title = info["show"]["title"]

    if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"):
        xbmc.executebuiltin(
            "RunScript(script.qlickplay,info=seasoninfo,tvshow={0},season={1})".
            format(title, season))
    elif xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"):
        xbmc.executebuiltin(
            "RunScript(script.extendedinfo,info=seasoninfo,tvshow={0},season={1})".
            format(title, season))
    return


@route("episode_extended_info", ["url"])
def episode_get_extended_info(item):
    import xbmc
    item = eval(item)
    imdb = item["imdb"]
    season = item["season"]
    episode = item["episode"]
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_CLIENT_ID
    }
    url = TRAKT_API_ENDPOINT + "/search/imdb/" + imdb + '?type=show'
    info = requests.get(url, headers=headers, verify=False).json()[0]
    title = str(info["show"]["title"])

    if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"):
        xbmc.executebuiltin("RunScript(script.qlickplay,info=episodeinfo,\
            tvshow={0}, season={1}, episode={2})"
                            .format(title, season, episode))
    elif xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"):
        xbmc.executebuiltin(
            "RunScript(script.extendedinfo,info=extendedepisodeinfo,\
            tvshow={0},season={1},episode={2})".format(title, season, episode))


@route("movie_extended_info", ["url"])
def movie_get_extended_info(imdb):
    import xbmc
    if xbmc.getCondVisibility("system.hasaddon(script.qlickplay)"):
        xbmc.executebuiltin(
            "RunScript(script.qlickplay,info=movieinfo,id={0})".format(imdb))
    elif xbmc.getCondVisibility("system.hasaddon(script.extendedinfo)"):
        xbmc.executebuiltin(
            "RunScript(script.extendedinfo,info=extendedinfo,id={0})".format(
                imdb))


def parse_year(text):
    """parse year from a date string of the format yyyy-mm-dd"""
    try:
        return text.split("-")[0].strip()
    except:
        return '0'


def get_info(items, dialog=None):
    from resources.lib.util.xml import JenItem
    result = run_hook("get_info", items, dialog)
    if result:
        return result
    koding.reset_db()
    info = []
    num_items = len(items)
    for index, item_xml in enumerate(items):
        if dialog:
            if dialog.iscanceled():
                dialog.close()
                break
            percent = ((index + 1) * 100) / num_items
            dialog.update(percent, _("processing metadata"),
                          "%s of %s" % (index + 1, num_items))
        if type(item_xml) == dict:
            item = item_xml
        else:
            item = JenItem(item_xml)
        item_info = {}
        content = item.get("content", "")
        try:
            if content == "movie":
                item_info = get_movie_metadata(item["imdb"])
            elif content in ["tvshow", "season"]:
                item_info = get_show_metadata(item["imdb"])
            elif content == "episode":
                item_info = get_episode_metadata(item["imdb"], item["season"],
                                                 item["episode"])
            if type(item_info) == list:
                item_info = {}
            if not item_info.get("plotoutline", None):
                item_info["plotoutline"] = item_info.get("plot", "")
        except Exception as e:
            koding.dolog("info error: " + repr(e))
        summary = item.get("summary", False)
        if summary:
            if not item_info or type(item_info) != dict:
                item_info = {}
            item_info["plot"] = summary
            item_info["manual"] = True

        info.append(item_info)
    if dialog:
        dialog.close()
    tvdb.clear_cache()
    return info
