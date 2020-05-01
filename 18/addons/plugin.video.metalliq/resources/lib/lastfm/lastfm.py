# -*- coding: utf-8 -*-
import requests
from meta.utils.text import to_utf8
from meta.gui import dialogs
from meta import plugin, LANG
from settings import *
from language import get_string as _

LAK = plugin.get_setting(SETTING_LASTFM_API_KEY, str)
LASS = plugin.get_setting(SETTING_LASTFM_API_SHARED_SECRET, str)

if len(LAK) == 32 and len(LASS) == 32:
    API_KEY = LAK
    SHARED_SECRET = LASS
else:
    API_KEY = ""
    SHARED_SECRET = ""

API_ENDPOINT = "http://ws.audioscrobbler.com/2.0/"


def call_last_fm(params={}, data=None, result_format = "json"):
    params = dict([(k, to_utf8(v)) for k, v in params.items() if v])
    params["api_key"] = API_KEY
    params["format"] = result_format

    def send_query():
        if data is not None:
            assert not params
            return requests.post("{0}".format(API_ENDPOINT), json=data)
        else:
            return requests.get("{0}".format(API_ENDPOINT), params)

    response = send_query()
    response.raise_for_status()
    response.encoding = 'utf-8'
    if result_format == "json":
        return response.json()
    else:
        return response.text

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def search_artist(artist_name, page=1):
    parameters = {}
    parameters['method'] = 'artist.search'
    parameters['artist'] = artist_name
    parameters["limit"] = 25
    parameters["page"] = page

    results = call_last_fm(parameters)["results"]
    return results

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def search_album(album_name, page=1):
    parameters = {}
    parameters['method'] = 'album.search'
    parameters['album'] = album_name
    parameters["limit"] = 25
    parameters["page"] = page

    results = call_last_fm(parameters)["results"]
    return results

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def search_track(track_name, page=1):
    parameters = {}
    parameters['method'] = 'track.search'
    parameters['track'] = track_name
    parameters["limit"] = 25
    parameters["page"] = page

    results = call_last_fm(parameters)["results"]
    return results


@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def get_artist_top_tracks(artist_name, page):
    parameters = {}
    parameters['method'] = 'artist.gettoptracks'
    parameters["artist"] = artist_name
    parameters["page"] = page
    results = call_last_fm(parameters)
    return results["toptracks"]

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def get_artist_top_albums(artist_name, page=1):
    parameters = {}
    parameters['method'] = 'artist.gettopalbums'
    parameters["artist"] = artist_name
    parameters["page"] = page
    results = call_last_fm(parameters)
    return results["topalbums"]

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def get_track_info(artist_name, track_name):
    parameters = {}
    parameters['method'] = 'track.getinfo'
    parameters["artist"] = artist_name
    parameters["track"] = track_name
    results = call_last_fm(parameters)
    if "track" in results: return results["track"]

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def get_album_info(artist_name, album_name):
    parameters = {}
    parameters['method'] = 'album.getinfo'
    parameters["artist"] = artist_name
    parameters["album"] = album_name
    results = call_last_fm(parameters)
    if "album" in results: return results["album"]
    else: return []

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def get_artist_info(artist_name):
    parameters = {}
    parameters['method'] = 'artist.getinfo'
    parameters["artist"] = artist_name
    results = call_last_fm(parameters)
    if "artist" in results: return results["artist"]
    else: return []

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def get_top_artists(page):
    parameters = {}
    parameters['method'] = 'chart.gettopartists'
    parameters["limit"] = 100
    parameters["page"] = page
    results = call_last_fm(parameters)
    return results

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def get_top_tracks(page):
    parameters = {}
    parameters['method'] = 'tag.gettoptracks'
    parameters["limit"] = 100
    parameters["page"] = page
    results = call_last_fm(parameters)
    return results

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def get_top_artists_by_country(country, page):
    parameters = {}
    parameters['method'] = 'geo.gettopartists'
    parameters["country"] = country
    parameters["limit"] = 100
    parameters["page"] = page
    results = call_last_fm(parameters)
    return results

@plugin.cached(TTL=CACHE_TTL, cache="lastfm")
def get_top_tracks_by_country(country, page):
    parameters = {}
    parameters['method'] = 'geo.gettoptracks'
    parameters["country"] = country
    parameters["limit"] = 100
    parameters["page"] = page
    results = call_last_fm(parameters)
    return results
