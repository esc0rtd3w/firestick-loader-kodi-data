from urllib2 import Request, urlopen
import re
import urllib
import json
import ssl
import socket
import urllib2
import kodi
from libs import watched_cache
from libs import log_utils
import time
import trakt





MY_TOKEN = kodi.get_setting('trakt_oauth_token')  # GET WITH PIN CODE
REFRESH_TOKEN = kodi.get_setting('trakt_refresh_token') #CHANGES # MONTH
V2_API_KEY='a19aa7f7cf7fa27437254cc27fcba454664360086949e80029f83874fa455e8f'
CLIENT_SECRET='5872236e7c198363867d89014ee334281648a7f433f9e4c362e5519e334693d1'
REDIRECT_URL='urn:ietf:wg:oauth:2.0:oob'
BASE_URL='api-v2launch.trakt.tv/'

TEMP_ERRORS = [500, 502, 503, 504, 520, 521, 522, 524]
COMPONENT = __name__

class TraktError(Exception):
    pass

class TraktAuthError(Exception):
    pass

class TraktNotFoundError(Exception):
    pass

class TransientTraktError(Exception):
    pass


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
            log_utils.log(response_body)
            # for e in response_body:
            #     print e
        #return


def stop_tv_watch(name,media):
    # log_utils.log(name)
    print name
    seasons=re.compile('S(.+?)E(.+?) ').findall(media)
    for sea,epi in seasons:
        # log_utils.log(sea,epi)
        print sea + epi
        stop_values = """{"show": {"title": """+name+"""},"episode": {"season": """+sea+""","number": """+epi+"""},"progress": 99.9,"app_version": "1.0","app_date": "2014-09-22"}"""
        #print stop_values
        request = Request('https://api-v2launch.trakt.tv/scrobble/stop', data=stop_values, headers=auth_headers)
        response_body = urlopen(request).read()
        trakt_id=re.compile('"trakt":(.+?),').findall(response_body)
        print trakt_id[0]
        watched_cache.set_watch_cache(trakt_id[0],"shows")
        if kodi.get_setting('debug') == "true":
            print response_body
            log_utils.log(response_body)
        #return


####################

def auth_trakt():
    trakt_api = trakt.TraktAPI()
    start = time.time()
    use_https = kodi.get_setting('use_https') == 'true'
    trakt_timeout = int(kodi.get_setting('timeout'))
    trakt_api = trakt.TraktAPI(use_https=use_https, timeout=trakt_timeout)
    result = trakt_api.get_code()
    kodi.log(result)
    code, expires, interval = result['device_code'], result['expires_in'], result['interval']
    time_left = expires - int(time.time() - start)
    line1 = 'On ANY Device visit: ' +result['verification_url']
    line2 = 'When promted , enter code: '+ result['user_code']
    with kodi.CountdownDialog('Authorizer your account', line1=line1, line2=line2, countdown=time_left,
                              interval=interval) as cd:
        result = cd.start(__auth_trakt, [trakt_api, code,'TEST'])

    try:
        trakt_api = trakt.TraktAPI()
        kodi.set_setting('trakt_oauth_token', result['access_token'])
        kodi.set_setting('trakt_refresh_token', result['refresh_token'])
        kodi.set_setting('trakt_authorized', "true")
        # trakt_api = trakt.Trakt_API(result['access_token'], use_https=True, timeout=trakt_timeout)
        kodi.log(result['access_token'])
        profile = trakt_api.my_username()
        #kodi.log("PROFILE RESULT " + profile['username'])
        kodi.set_setting('trakt_username', profile['username']+'/'+ profile['name'])
        kodi.notify(header='Trakt', msg='You are now authorized', duration=5000, sound=None)
        #kodi.notify(msg='trakt_auth_complete', duration=3000)
    except Exception as e:
        log_utils.log('Trakt Authorization Failed: %s' % (e), log_utils.LOGDEBUG)


def __auth_trakt(trakt_api, code, i18n):
    try:
        result = trakt_api.get_device_token(code)
        return result
    except urllib2.URLError as e:
        # authorization is pending; too fast
        if e.code in [400, 429]:
            return
        elif e.code == 418:
            kodi.notify('Denied - user explicitly denied this code', duration=3000)
            return True
        elif e.code == 410:
            return
        else:
            raise


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes > 60:
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        return "%02d:%02d" % (minutes, seconds)

