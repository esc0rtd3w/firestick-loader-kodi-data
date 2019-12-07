"""
    tknorris shared module
    Copyright (C) 2016 tknorris

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
import datetime
import _strptime
import time
import re
import json
import urllib2
import urllib
import urlparse
import os
import kodi
import log_utils
import xbmcgui
import xbmcvfs
import xbmc

logger = log_utils.Logger.get_logger(__name__)

def __enum(**enums):
    return type('Enum', (), enums)

PROGRESS = __enum(OFF=0, WINDOW=1, BACKGROUND=2)
CHUNK_SIZE = 512 * 1024
DEFAULT_EXT = 'mpg'
BROWSER_UA = 'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'
INTERVALS = 5
WATCHLIST_SLUG = 'watchlist_slug'

def make_list_item(label, meta, art=None, cast=None):
    if art is None: art = {'thumb': '', 'fanart': ''}
    if cast is None: cast = []
    listitem = xbmcgui.ListItem(label, iconImage=art['thumb'], thumbnailImage=art['thumb'])
    listitem.setProperty('fanart_image', art['fanart'])
    listitem.setProperty('isPlayable', 'false')
    listitem.addStreamInfo('video', {})
    try: listitem.setArt(art)
    except AttributeError: pass
    try: listitem.setCast(cast)
    except AttributeError: pass
    if 'ids' in meta and 'imdb' in meta['ids']: listitem.setProperty('imdb_id', str(meta['ids']['imdb']))
    if 'ids' in meta and 'tvdb' in meta['ids']: listitem.setProperty('tvdb_id', str(meta['ids']['tvdb']))
    return listitem

def iso_2_utc(iso_ts):
    if not iso_ts or iso_ts is None: return 0
    delim = -1
    if not iso_ts.endswith('Z'):
        delim = iso_ts.rfind('+')
        if delim == -1: delim = iso_ts.rfind('-')

    if delim > -1:
        ts = iso_ts[:delim]
        sign = iso_ts[delim]
        tz = iso_ts[delim + 1:]
    else:
        ts = iso_ts
        tz = None

    if ts.find('.') > -1:
        ts = ts[:ts.find('.')]

    try: d = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
    except TypeError: d = datetime.datetime(*(time.strptime(ts, '%Y-%m-%dT%H:%M:%S')[0:6]))

    dif = datetime.timedelta()
    if tz:
        hours, minutes = tz.split(':')
        hours = int(hours)
        minutes = int(minutes)
        if sign == '-':
            hours = -hours
            minutes = -minutes
        dif = datetime.timedelta(minutes=minutes, hours=hours)
    utc_dt = d - dif
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = utc_dt - epoch
    try: seconds = delta.total_seconds()  # works only on 2.7
    except: seconds = delta.seconds + delta.days * 24 * 3600  # close enough
    return seconds

def to_slug(username):
    username = username.strip()
    username = username.lower()
    username = re.sub('[^a-z0-9_]', '-', username)
    username = re.sub('--+', '-', username)
    return username

def json_load_as_str(file_handle):
    return _byteify(json.load(file_handle, object_hook=_byteify), ignore_dicts=True)

def json_loads_as_str(json_text):
    return _byteify(json.loads(json_text, object_hook=_byteify), ignore_dicts=True)

def _byteify(data, ignore_dicts=False):
    if isinstance(data, unicode):
        return data.encode('utf-8')
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]
    if isinstance(data, dict) and not ignore_dicts:
        return dict([(_byteify(key, ignore_dicts=True), _byteify(value, ignore_dicts=True)) for key, value in data.iteritems()])
    return data

def download_media(url, path, file_name, translations, progress=None):
    try:
        if progress is None:
            progress = int(kodi.get_setting('down_progress'))
            
        i18n = translations.i18n
        active = not progress == PROGRESS.OFF
        background = progress == PROGRESS.BACKGROUND
            
        with kodi.ProgressDialog(kodi.get_name(), i18n('downloading') % (file_name), background=background, active=active) as pd:
            try:
                headers = dict([item.split('=') for item in (url.split('|')[1]).split('&')])
                for key in headers: headers[key] = urllib.unquote(headers[key])
            except:
                headers = {}
            if 'User-Agent' not in headers: headers['User-Agent'] = BROWSER_UA
            request = urllib2.Request(url.split('|')[0], headers=headers)
            response = urllib2.urlopen(request)
            if 'Content-Length' in response.info():
                content_length = int(response.info()['Content-Length'])
            else:
                content_length = 0
    
            file_name += '.' + get_extension(url, response)
            full_path = os.path.join(path, file_name)
            logger.log('Downloading: %s -> %s' % (url, full_path), log_utils.LOGDEBUG)
    
            path = kodi.translate_path(xbmc.makeLegalFilename(path))
            try:
                try: xbmcvfs.mkdirs(path)
                except: os.makedirs(path)
            except Exception as e:
                logger.log('Path Create Failed: %s (%s)' % (e, path), log_utils.LOGDEBUG)
    
            if not path.endswith(os.sep): path += os.sep
            if not xbmcvfs.exists(path):
                raise Exception(i18n('failed_create_dir'))
            
            file_desc = xbmcvfs.File(full_path, 'w')
            total_len = 0
            cancel = False
            while True:
                data = response.read(CHUNK_SIZE)
                if not data:
                    break
    
                if pd.is_canceled():
                    cancel = True
                    break
    
                total_len += len(data)
                if not file_desc.write(data):
                    raise Exception(i18n('failed_write_file'))
    
                percent_progress = (total_len) * 100 / content_length if content_length > 0 else 0
                logger.log('Position : %s / %s = %s%%' % (total_len, content_length, percent_progress), log_utils.LOGDEBUG)
                pd.update(percent_progress)
            
            file_desc.close()

        if not cancel:
            kodi.notify(msg=i18n('download_complete') % (file_name), duration=5000)
            logger.log('Download Complete: %s -> %s' % (url, full_path), log_utils.LOGDEBUG)

    except Exception as e:
        logger.log('Error (%s) during download: %s -> %s' % (str(e), url, file_name), log_utils.LOGERROR)
        kodi.notify(msg=i18n('download_error') % (str(e), file_name), duration=5000)

def get_extension(url, response):
    filename = url2name(url)
    if 'Content-Disposition' in response.info():
        cd_list = response.info()['Content-Disposition'].split('filename=')
        if len(cd_list) > 1:
            filename = cd_list[-1]
            if filename[0] == '"' or filename[0] == "'":
                filename = filename[1:-1]
    elif response.url != url:
        filename = url2name(response.url)
    ext = os.path.splitext(filename)[1][1:]
    if not ext: ext = DEFAULT_EXT
    return ext

def create_legal_filename(title, year):
    filename = title
    if year: filename += ' %s' % (year)
    filename = re.sub(r'(?!%s)[^\w\-_\.]', '.', filename)
    filename = re.sub('\.+', '.', filename)
    xbmc.makeLegalFilename(filename)
    return filename

def url2name(url):
    url = url.split('|')[0]
    return os.path.basename(urllib.unquote(urlparse.urlsplit(url)[2]))

def auth_trakt(Trakt_API, translations):
    i18n = translations.i18n
    start = time.time()
    use_https = kodi.get_setting('use_https') == 'true'
    trakt_timeout = int(kodi.get_setting('trakt_timeout'))
    trakt_api = Trakt_API(use_https=use_https, timeout=trakt_timeout)
    result = trakt_api.get_code()
    code, expires, interval = result['device_code'], result['expires_in'], result['interval']
    time_left = expires - int(time.time() - start)
    line1 = i18n('verification_url') % (result['verification_url'])
    line2 = i18n('prompt_code') % (result['user_code'])
    with kodi.CountdownDialog(i18n('trakt_acct_auth'), line1=line1, line2=line2, countdown=time_left, interval=interval) as cd:
        result = cd.start(__auth_trakt, [trakt_api, code, i18n])
    
    try:
        kodi.set_setting('trakt_oauth_token', result['access_token'])
        kodi.set_setting('trakt_refresh_token', result['refresh_token'])
        trakt_api = Trakt_API(result['access_token'], use_https=use_https, timeout=trakt_timeout)
        profile = trakt_api.get_user_profile(cached=False)
        kodi.set_setting('trakt_user', '%s (%s)' % (profile['username'], profile['name']))
        kodi.notify(msg=i18n('trakt_auth_complete'), duration=3000)
    except Exception as e:
        logger.log('Trakt Authorization Failed: %s' % (e), log_utils.LOGDEBUG)
        
        
def __auth_trakt(trakt_api, code, i18n):
    try:
        result = trakt_api.get_device_token(code)
        return result
    except urllib2.URLError as e:
        # authorization is pending; too fast
        if e.code in [400, 429]:
            return
        elif e.code == 418:
            kodi.notify(msg=i18n('user_reject_auth'), duration=3000)
            return True
        elif e.code == 410:
            return
        else:
            raise

def choose_list(Trakt_API, translations, username=None):
    i18n = translations.i18n
    trakt_api = Trakt_API(kodi.get_setting('trakt_oauth_token'), kodi.get_setting('use_https') == 'true', timeout=int(kodi.get_setting('trakt_timeout')))
    lists = trakt_api.get_lists(username)
    if username is None: lists.insert(0, {'name': 'watchlist', 'ids': {'slug': WATCHLIST_SLUG}})
    if lists:
        dialog = xbmcgui.Dialog()
        index = dialog.select(i18n('pick_a_list'), [list_data['name'] for list_data in lists])
        if index > -1:
            return (lists[index]['ids']['slug'], lists[index]['name'])
    else:
        kodi.notify(msg=i18n('no_lists_for_user') % (username), duration=5000)

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes > 60:
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        return "%02d:%02d" % (minutes, seconds)

