# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import datetime
from Utils import *
from local_db import *

TRAKT_KEY = '988f3835e5410b3f5e5e90b922a8a0016ef21ec65a2fc63f68e44a6b03041fe7'
BASE_URL = "https://api-v2launch.trakt.tv/"
HEADERS = {
    'Content-Type': 'application/json',
    'trakt-api-key': TRAKT_KEY,
    'trakt-api-version': 2
}


def get_trakt_calendar_shows(content):
    shows = []
    url = ""
    if content == "shows":
        url = 'calendars/shows/%s/14?extended=full,images' % datetime.date.today()
    elif content == "premieres":
        url = 'calendars/shows/premieres/%s/14?extended=full,images' % datetime.date.today()
    try:
        results = get_JSON_response(url=BASE_URL + url,
                                    cache_days=0.5,
                                    folder="Trakt",
                                    headers=HEADERS)
    except:
        log("Error when fetching Trakt data from net")
        log("Json Query: " + url)
        results = None
    count = 1
    if not results:
        return None
    for day in results.iteritems():
        for episode in day[1]:
            banner = episode["show"]["images"]["banner"]["full"]
            fanart = episode["show"]["images"]["fanart"]["full"]
            poster = episode["show"]["images"]["poster"]["full"]
            show = {'title': episode["episode"]["title"],
                    'TVShowTitle': episode["show"]["title"],
                    'tvdb_id': episode["show"]["ids"]["tvdb"],
                    'id': episode["show"]["ids"]["tvdb"],
                    'imdb_id': episode["show"]["ids"]["imdb"],
                    'tmdb_id': episode["show"]["ids"]["tmdb"],
                    'trakt_id': episode["show"]["ids"]["trakt"],
                    'path': 'plugin://script.wraith/?info=extendedtvinfo&tvdb_id=%s' % episode["show"]["ids"]["tvdb"],
                    'Runtime': episode["show"]["runtime"] * 60,
                    'duration': episode["show"]["runtime"] * 60,
                    'duration(h)': format_time(episode["show"]["runtime"], "h"),
                    'duration(m)': format_time(episode["show"]["runtime"], "m"),
                    'year': fetch(episode["show"], "year"),
                    'Certification': episode["show"]["certification"],
                    'Studio': episode["show"]["network"],
                    'Plot': episode["show"]["overview"],
                    'genre': " / ".join(episode["show"]["genres"]),
                    'thumb': episode["episode"]["images"]["screenshot"]["thumb"],
                    'poster': poster,
                    'Banner': banner,
                    'fanart': fanart}
            shows.append(show)
            count += 1
            if count > 20:
                break
    return shows


def handle_trakt_movies(results):
    movies = []
    for movie in results:
        if SETTING("infodialog_onclick") != "false":
            path = 'plugin://script.wraith/?info=wraith&id=%s' % str(fetch(movie["movie"]["ids"], 'tmdb'))
        else:
            path = "plugin://script.wraith/?info=playtrailer&id=" + str(fetch(movie["movie"]["ids"], 'tmdb'))
        movie = {'title': movie["movie"]["title"],
                 'Runtime': movie["movie"]["runtime"] * 60,
                 'duration': movie["movie"]["runtime"] * 60,
                 'duration(h)': format_time(movie["movie"]["runtime"], "h"),
                 'duration(m)': format_time(movie["movie"]["runtime"], "m"),
                 'Tagline': movie["movie"]["tagline"],
                 'Trailer': convert_youtube_url(movie["movie"]["trailer"]),
                 'year': movie["movie"]["year"],
                 'id': movie["movie"]["ids"]["tmdb"],
                 'imdb_id': movie["movie"]["ids"]["imdb"],
                 'trakt_id': movie["movie"]["ids"]["trakt"],
                 'slug': movie["movie"]["ids"]["slug"],
                 'path': path,
                 'mpaa': movie["movie"]["certification"],
                 'Plot': movie["movie"]["overview"],
                 'Premiered': movie["movie"]["released"],
                 'Rating': round(movie["movie"]["rating"], 1),
                 'Votes': movie["movie"]["votes"],
                 'Watchers': movie["watchers"],
                 'genre': " / ".join(movie["movie"]["genres"]),
                 'poster': movie["movie"]["images"]["poster"]["full"],
                 'fanart': movie["movie"]["images"]["fanart"]["full"],
                 'thumb': movie['movie']["images"]["poster"]["thumb"]}
        movies.append(movie)
    movies = merge_with_local_movie_info(online_list=movies,
                                         library_first=False)
    return movies


def handle_trakt_tvshows(results):
    shows = []
    for tvshow in results:
        airs = fetch(tvshow['show'], "airs")
        path = 'plugin://script.wraith/?info=extendedtvinfo&tvdb_id=%s' % tvshow['show']['ids']["tvdb"]
        show = {'title': tvshow['show']["title"],
                'Label': tvshow['show']["title"],
                'TVShowTitle': tvshow['show']["title"],
                'Runtime': tvshow['show']["runtime"] * 60,
                'duration': tvshow['show']["runtime"] * 60,
                'duration(h)': format_time(tvshow['show']["runtime"], "h"),
                'duration(m)': format_time(tvshow['show']["runtime"], "m"),
                'year': tvshow['show']["year"],
                'Status': fetch(tvshow['show'], "status"),
                'mpaa': tvshow['show']["certification"],
                'Studio': tvshow['show']["network"],
                'Plot': tvshow['show']["overview"],
                'id': tvshow['show']['ids']["tmdb"],
                'tvdb_id': tvshow['show']['ids']["tvdb"],
                'imdb_id': tvshow['show']['ids']["imdb"],
                'tmdb_id': tvshow['show']['ids']["tmdb"],
                'trakt_id': tvshow['show']['ids']["trakt"],
                'slug': tvshow['show']['ids']["slug"],
                'path': path,
                'AirDay': fetch(airs, "day"),
                'AirShortTime': fetch(airs, "time"),
                'Premiered': tvshow['show']["first_aired"][:10],
                'Country': tvshow['show']["country"],
                'Rating': round(tvshow['show']["rating"], 1),
                'Votes': tvshow['show']["votes"],
                'Watchers': fetch(tvshow, "watchers"),
                'genre': " / ".join(tvshow['show']["genres"]),
                'poster': tvshow['show']["images"]["poster"]["full"],
                'Banner': tvshow['show']["images"]["banner"]["full"],
                'fanart': tvshow['show']["images"]["fanart"]["full"],
                'thumb': tvshow['show']["images"]["poster"]["thumb"]}
        shows.append(show)
    shows = merge_with_local_tvshow_info(online_list=shows,
                                         library_first=False)
    return shows


def get_trending_shows():
    url = 'shows/trending?extended=full,images'
    results = get_JSON_response(url=BASE_URL + url,
                                folder="Trakt",
                                headers=HEADERS)
    if results is not None:
        return handle_trakt_tvshows(results)
    else:
        return []


def get_tshow_info(imdb_id):
    url = 'show/%s?extended=full,images' % imdb_id
    results = get_JSON_response(url=BASE_URL + url,
                                folder="Trakt",
                                headers=HEADERS)
    if results is not None:
        return handle_trakt_tvshows([results])
    else:
        return []

def get_tshow_info_min(imdb_id):
    url = 'shows/%s?min' % imdb_id
    results = get_JSON_response(url=BASE_URL + url,
                                folder="Trakt",
                                headers=HEADERS)
    if results is not None:
        return results
    else:
        return []


def get_movie_info_min(imdb_id):
    url = 'movies/%s?min' % imdb_id
    results = get_JSON_response(url=BASE_URL + url,
                                folder="Trakt",
                                headers=HEADERS)
    if results is not None:
        return results
    else:
        return []


def get_movie_images(imdb_id):
    url = 'movies/%s?extended=full,images' % imdb_id
    results = get_JSON_response(url=BASE_URL + url,
                                folder="Trakt",
                                headers=HEADERS)
    if results is not None:
        return results
    else:
        return []

def get_movie_info(imdb_id):
    url = 'movies/%s?extended=full,images' % imdb_id
    results = get_JSON_response(url=BASE_URL + url,
                                folder="Trakt",
                                headers=HEADERS)
    if results is not None:
        return results
    else:
        return []


def get_trakt_ids(type=None,db=None,id=None):
    if type == None:
        return
    url = 'movie/%s?min' % (id)
    results = get_JSON_response(url=BASE_URL + url,
                                folder="Trakt",
                                headers=HEADERS)
    if results is not None:
        return results
    else:
        return []


def get_trending_movies():
    url = 'movies/trending?extended=full,images'
    results = get_JSON_response(url=BASE_URL + url,
                                folder="Trakt",
                                headers=HEADERS)
    if results is not None:
        return handle_trakt_movies(results)
    else:
        return []


def get_trakt_similar(media_type, imdb_id):
    if imdb_id is not None:
        url = '%s/%s/related?extended=full,images' % (media_type, imdb_id)
        results = get_JSON_response(url=BASE_URL + url,
                                    folder="Trakt",
                                    headers=HEADERS)
        if results is not None:
            if media_type == "show":
                return handle_trakt_tvshows(results)
            elif media_type == "movie":
                return handle_trakt_movies(results)
    else:
        notify("Error when fetching info from Trakt.TV")
        return[]
