"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
import json
import re
import urllib
import kodi
import log_utils  # @UnusedImport
import utils
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper
import xml.etree.ElementTree as ET
import xbmcgui

logger = log_utils.Logger.get_logger()
BASE_URL = 'https://www.furk.net'
SEARCH_URL = '/api/plugins/metasearch'
LOGIN_URL = '/api/login/login'
MIN_DURATION = 10 * 60 * 1000  # 10 minutes in milliseconds

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))
        self.max_results = int(kodi.get_setting('%s-result_limit' % (self.get_name())))
        self.max_gb = kodi.get_setting('%s-size_limit' % (self.get_name()))
        self.max_bytes = int(self.max_gb) * 1024 * 1024 * 1024

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Furk.net'

    def resolve_link(self, link):
        playlist = super(self.__class__, self)._http_get(link, cache_limit=.5)
        try:
            ns = '{http://xspf.org/ns/0/}'
            root = ET.fromstring(playlist)
            tracks = root.findall('.//%strack' % (ns))
            locations = []
            for track in tracks:
                duration = track.find('%sduration' % (ns)).text
                try: duration = int(duration)
                except: duration = 0
                if duration >= MIN_DURATION:
                    location = track.find('%slocation' % (ns)).text
                    locations.append({'duration': duration / 1000, 'url': location})

            if len(locations) > 1:
                result = xbmcgui.Dialog().select(i18n('choose_stream'), [utils.format_time(location['duration']) for location in locations])
                if result > -1:
                    return locations[result]['url']
            elif locations:
                return locations[0]['url']
        except Exception as e:
            logger.log('Failure during furk playlist parse: %s' % (e), log_utils.LOGWARNING)
        
    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        params = scraper_utils.parse_query(source_url)
        if 'title' in params:
            search_title = re.sub("[^A-Za-z0-9. ]", "", urllib.unquote_plus(params['title']))
            query = search_title
            if video.video_type == VIDEO_TYPES.MOVIE:
                if 'year' in params: query += ' %s' % (params['year'])
            else:
                sxe = ''
                if 'season' in params:
                    sxe = 'S%02d' % (int(params['season']))
                if 'episode' in params:
                    sxe += 'E%02d' % (int(params['episode']))
                if sxe: query = '%s %s' % (query, sxe)
            query_url = '/search?query=%s' % (query)
            hosters = self.__get_links(query_url, video)
            if not hosters and video.video_type == VIDEO_TYPES.EPISODE and params['air_date']:
                query = urllib.quote_plus('%s %s' % (search_title, params['air_date'].replace('-', '.')))
                query_url = '/search?query=%s' % (query)
                hosters = self.__get_links(query_url, video)

        return hosters
    
    def __get_links(self, url, video):
        hosters = []
        search_url = scraper_utils.urljoin(self.base_url, SEARCH_URL)
        query = self.__translate_search(url)
        result = self._http_get(search_url, data=query, allow_redirect=False, cache_limit=.5)
        for item in result.get('files', []):
            checks = [False] * 6
            if item.get('type', '').upper() != 'VIDEO': checks[0] = True
            if item.get('is_ready') != '1': checks[1] = True
            if item.get('av_result') in ['warning', 'infected']: checks[2] = True
            if 'video_info' not in item: checks[3] = True
            if item.get('video_info') and not re.search('#0:(0|1)(\((eng|und)\))?:\s*Audio:', item['video_info'], re.I): checks[4] = True
            if not scraper_utils.release_check(video, item['name']): checks[5] = True
            if any(checks):
                logger.log('Furk.net result excluded: %s - |%s|' % (checks, item['name']), log_utils.LOGDEBUG)
                continue
            
            match = re.search('(\d{3,})\s*x\s*(\d{3,})', item['video_info'])
            if match:
                width, _height = match.groups()
                quality = scraper_utils.width_get_quality(width)
            else:
                if video.video_type == VIDEO_TYPES.MOVIE:
                    meta = scraper_utils.parse_movie_link(item['name'])
                else:
                    meta = scraper_utils.parse_episode_link(item['name'])
                quality = scraper_utils.height_get_quality(meta['height'])
                
            if 'url_pls' in item:
                size_gb = scraper_utils.format_size(int(item['size']), 'B')
                if self.max_bytes and int(item['size']) > self.max_bytes:
                    logger.log('Result skipped, Too big: |%s| - %s (%s) > %s (%sGB)' % (item['name'], item['size'], size_gb, self.max_bytes, self.max_gb))
                    continue

                stream_url = item['url_pls']
                host = scraper_utils.get_direct_hostname(self, stream_url)
                hoster = {'multi-part': False, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'host': host, 'quality': quality, 'direct': True}
                hoster['size'] = size_gb
                hoster['extra'] = item['name']
                hosters.append(hoster)
            else:
                logger.log('Furk.net result skipped - no playlist: |%s|' % (json.dumps(item)), log_utils.LOGDEBUG)
                    
        return hosters
    
    def get_url(self, video):
        url = None
        result = self.db_connection().get_related_url(video.video_type, video.title, video.year, self.get_name(), video.season, video.episode)
        if result:
            url = result[0][0]
            logger.log('Got local related url: |%s|%s|%s|%s|%s|' % (video.video_type, video.title, video.year, self.get_name(), url), log_utils.LOGDEBUG)
        else:
            if video.video_type == VIDEO_TYPES.MOVIE:
                query = 'title=%s&year=%s' % (urllib.quote_plus(video.title), video.year)
            else:
                query = 'title=%s&season=%s&episode=%s&air_date=%s' % (urllib.quote_plus(video.title), video.season, video.episode, video.ep_airdate)
            url = '/search?%s' % (query)
            self.db_connection().set_related_url(video.video_type, video.title, video.year, self.get_name(), url, video.season, video.episode)
        return url

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        return []

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-3,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-4,true)"/>' % (name, i18n('password')))
        settings.append('         <setting id="%s-result_limit" label="     %s" type="slider" default="10" range="10,100" option="int" visible="eq(-5,true)"/>' % (name, i18n('result_limit')))
        settings.append('         <setting id="%s-size_limit" label="     %s" type="slider" default="0" range="0,50" option="int" visible="eq(-6,true)"/>' % (name, i18n('size_limit')))
        return settings

    def _http_get(self, url, data=None, retry=True, allow_redirect=True, cache_limit=8):
        if not self.username or not self.password:
            return {}
        
        js_result = {}
        result = super(self.__class__, self)._http_get(url, data=data, allow_redirect=allow_redirect, cache_limit=cache_limit)
        if result:
            try:
                js_result = json.loads(result)
            except (ValueError, TypeError):
                if 'msg_key=session_invalid' in result:
                    logger.log('Logging in for url (%s) (Session Expired)' % (url), log_utils.LOGDEBUG)
                    self.__login()
                    js_result = self._http_get(url, data=data, retry=False, allow_redirect=allow_redirect, cache_limit=0)
                else:
                    logger.log('Invalid JSON returned: %s: %s' % (url, result), log_utils.LOGWARNING)
                    js_result = {}
            else:
                if js_result.get('status') == 'error':
                    error = js_result.get('error', 'Unknown Error')
                    if retry and any(e for e in ['access denied', 'session has expired', 'clear cookies'] if e in error):
                        logger.log('Logging in for url (%s) - (%s)' % (url, error), log_utils.LOGDEBUG)
                        self.__login()
                        js_result = self._http_get(url, data=data, retry=False, allow_redirect=allow_redirect, cache_limit=0)
                    else:
                        logger.log('Error received from furk.net (%s)' % (error), log_utils.LOGWARNING)
                        js_result = {}
            
        return js_result
        
    def __login(self):
        url = scraper_utils.urljoin(self.base_url, LOGIN_URL)
        data = {'login': self.username, 'pwd': self.password}
        result = self._http_get(url, data=data, cache_limit=0)
        if result.get('status') != 'ok':
            raise Exception('furk.net login failed: %s' % (result.get('error', 'Unknown Error')))
    
    def __translate_search(self, url):
        query = {'moderated': 'yes', 'offset': 0, 'limit': self.max_results, 'match': 'all', 'cached': 'yes', 'attrs': 'name'}
        query['q'] = scraper_utils.parse_query(url)['query']
        return query
