import requests
from meta.utils.text import to_utf8
from meta import plugin, LANG
from settings import *

API_KEY = "195003"
API_ENDPOINT = "http://www.theaudiodb.com/api/v1/json/{0}".format(API_KEY)

def call_audiodb(path, params={}):
    params = dict([(k, to_utf8(v)) for k, v in params.items() if v])
    response = requests.get("{0}/{1}.php".format(API_ENDPOINT, path), params)
    response.raise_for_status()
    response.encoding = 'utf-8'
    return response.json()

# general search
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def search(mode, artist, album="", track=""):
    if mode not in ["search", "searchalbum", "searchtrack", "searchmdvd", "discography", "discography-mb"]: plugin.log.info("NO\nm={0}\ns={1}\na={2}\nt={3}".format(mode, artist, album, track))
    plugin.log.info("YES\nm={0}\ns={1}\na={2}\nt={3}".format(mode, artist, album, track))
    return call_audiodb(mode, params={'s': artist, 'a': album, 't': track})

# search audiodb
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def search_details_from_artist(artist_name):
    return call_audiodb("search", params={'s': artist_name})
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def search_albums_from_artist(artist_name):
    return call_audiodb("searchalbum", params={'s': artist_name})
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def search_album_from_artist_and_title(artist_name, album_name):
    return call_audiodb("searchalbum", params={'s': artist_name, 'a': album_name})
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def search_album_from_title(album_name):
    return call_audiodb("searchalbum", params={'a': album_name})
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def search_track_from_artist_or_title(artist_name, track_name):
    return call_audiodb("searchtrack", params={'s': artist_name, 't': track_name})
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def search_dvd_from_artist_or_title(artist_name, dvd_name):
    return call_audiodb("searchmdvd", params={'s': artist_name, 'a': dvd_name})
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def search_disco_from_artist(artist_name):
    return call_audiodb("discography", params={'s': artist_name})
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def search_disco_from_mbid(mb_id):
    # md_id = Music_Brainz_Artist_ID
    return call_audiodb("discography-mb", params={'s': mb_id})
# get artist info
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def details_from_artist_id(artist_id):
    return call_audiodb("artist", params={'i': artist_id})

@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def details_from_md_id(md_id):
    # mb_id = mb_artist_id
    return call_audiodb("artist-mb", params={'i': md_id})

# get album info
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def all_albums_from_artist_id(artist_id):
    return call_audiodb("album", params={'i': artist_id})

@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def one_album_from_album_id(album_id):
    return call_audiodb("album", params={'i': album_id})

@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def one_album_from_mdid(mb_id):
    # md_id = Music_Brainz_Artist_ID
    return call_audiodb("album-mb", params={'i': mb_id})

# get track info
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def all_tracks_from_album_id(album_id):
    return call_audiodb("track", params={'i': album_id})

@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def track_from_track_id(track_id):
    return call_audiodb("track", params={'i': track_id})

@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def track_from_track_id(mb_id):
    # mb_id = mb_recording_id
    return call_audiodb("track-mb", params={'i': mb_id})

# get musicvideo info
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def all_musicvideos_from_album_id(artist_id):
    return call_audiodb("mvid", params={'i': artist_id})

@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def all_musicvideos_from_mb_id(mb_id):
    return call_audiodb("mvid-mb", params={'i': mb_id})

# get top 10 tracks
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def top_tracks_from_artist(artist_name):
    return call_audiodb("track-top10", params={'s': artist_name})

def top_tracks_from_mb_id(mb_id):
    return call_audiodb("track-top10-mb", params={'s': mb_id})

# get current trending
@plugin.cached(TTL=CACHE_TTL, cache="audiodb")
def top_tracks_from_artist(country, format):
    return call_audiodb("trending", params={'country': country, 'type': "itunes", 'format': format})
