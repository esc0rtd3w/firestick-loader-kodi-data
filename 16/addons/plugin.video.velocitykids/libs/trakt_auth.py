from urllib2 import Request, urlopen
import re
import json
import ssl
import socket
import urllib2
import kodi
from tm_libs import watched_cache

MY_TOKEN = kodi.get_setting('trakt_oauth_token')  # GET WITH PIN CODE
REFRESH_TOKEN = kodi.get_setting('trakt_refresh_token') #CHANGES # MONTH
V2_API_KEY='a19aa7f7cf7fa27437254cc27fcba454664360086949e80029f83874fa455e8f'
CLIENT_SECRET='5872236e7c198363867d89014ee334281648a7f433f9e4c362e5519e334693d1'
REDIRECT_URL='urn:ietf:wg:oauth:2.0:oob'
BASE_URL='api-v2launch.trakt.tv/'


auth_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+MY_TOKEN+'',
    'trakt-api-version': '2',
    'trakt-api-key': ''+V2_API_KEY+''}


def start_movie_watch(name,year):
    start_values = """{"movie": {"title": """+name+""","year": """+year+""","ids": {}},"progress": 1.25,"app_version": "1.0","app_date": "2014-09-22"}"""
    #print start_values
    request = Request('https://api-v2launch.trakt.tv/scrobble/start', data=start_values, headers=auth_headers)
    response_body = urlopen(request).read()
    if kodi.get_setting('debug') == "true":
        print response_body
    #return


def stop_movie_watch(name,year):
    stop_values =  """{"movie": {"title": """+name+""","year": """+year+""","ids": {}},"progress": 99.9,"app_version": "1.0","app_date": "2014-09-22"}"""
    #print stop_values
    request = Request('https://api-v2launch.trakt.tv/scrobble/stop', data=stop_values, headers=auth_headers)
    response_body = urlopen(request).read()
    trakt_id=re.compile('"trakt":(.+?),').findall(response_body)
    print trakt_id[0]
    watched_cache.set_watch_cache(trakt_id[0],"movies")
    if kodi.get_setting('debug') == "true":
        print response_body
    #return


def start_tv_watch(name,media):

    seasons=re.compile('S(.+?)E(.+?) ').findall(media)
    for sea,epi in seasons:

        start_values = """{"show": {"title": """+name+"""},"episode": {"season": """+sea+""","number": """+epi+"""},"progress": 10,"app_version": "1.0","app_date": "2014-09-22"}"""
        #print start_values
        request = Request('https://api-v2launch.trakt.tv/scrobble/start', data=start_values, headers=auth_headers)
        response_body = urlopen(request).read()
        if kodi.get_setting('debug') == "true":
            print response_body
        #return


def stop_tv_watch(name,media):
    seasons=re.compile('S(.+?)E(.+?) ').findall(media)
    for sea,epi in seasons:
        stop_values = """{"show": {"title": """+name+"""},"episode": {"season": """+sea+""","number": """+epi+"""},"progress": 99.9,"app_version": "1.0","app_date": "2014-09-22"}"""
        #print stop_values
        request = Request('https://api-v2launch.trakt.tv/scrobble/stop', data=stop_values, headers=auth_headers)
        response_body = urlopen(request).read()
        trakt_id=re.compile('"trakt":(.+?),').findall(response_body)
        print trakt_id[0]
        watched_cache.set_watch_cache(trakt_id[0],"shows")
        if kodi.get_setting('debug') == "true":
            print response_body
        #return





# STANDARD MEDIA OBJECTS
# movie
#
# {
#   "title":"Batman Begins",
#   "year":2005,
#   "ids":{
#     "trakt":1,
#     "slug":"batman-begins-2005",
#     "imdb":"tt0372784",
#     "tmdb":272
#   }
# }
#
# show
#
# {
#   "title":"Breaking Bad",
#   "year":2008,
#   "ids":{
#     "trakt":1,
#     "slug":"breaking-bad",
#     "tvdb":81189,
#     "imdb":"tt0903747",
#     "tmdb":1396,
#     "tvrage":18164
#   }
# }
#
# season
#
# {
#   "number":0,
#   "ids":{
#     "trakt":1,
#     "tvdb":439371,
#     "tmdb":3577,
#     "tvrage":null
#   }
# }
#
# episode
#
# {
#   "season":1,
#   "number":1,
#   "title":"Pilot",
#   "ids":{
#     "trakt":16,
#     "tvdb":349232,
#     "imdb":"tt0959621",
#     "tmdb":62085,
#     "tvrage":637041
#   }
# }
#
# person
#
# {
#   "name":"Bryan Cranston",
#   "ids":{
#     "trakt":142,
#     "slug":"bryan-cranston",
#     "imdb":"nm0186505",
#     "tmdb":17419,
#     "tvrage":1797
#   }
# }
