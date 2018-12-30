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
import re
import urllib
import base64
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger()
BASE_URL = 'https://members.easynews.com'
SEARCH_URL = '/2.0/search/solr-search/advanced'
SORT = {'s1': 'relevance', 's1d': '-', 's2': 'dsize', 's2d': '-', 's3': 'dtime', 's3d': '-'}
SEARCH_PARAMS = {'st': 'adv', 'safeO': 0, 'sb': 1, 'fex': 'mkv, mp4, avi', 'fty[]': 'VIDEO', 'spamf': 1, 'u': '1', 'gx': 1, 'pno': 1, 'sS': 3}
SEARCH_PARAMS.update(SORT)

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
        self.auth = 'Basic ' + base64.b64encode('%s:%s' % (self.username, self.password))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'EasyNews'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        params = scraper_utils.parse_query(source_url)
        if 'title' in params:
            query = params['title'].replace("'", "")
            if video.video_type == VIDEO_TYPES.MOVIE:
                if 'year' in params: query += ' %s' % (params['year'])
            else:
                sxe = ''
                if 'season' in params:
                    sxe = 'S%02d' % (int(params['season']))
                if 'episode' in params:
                    sxe += 'E%02d' % (int(params['episode']))
                if sxe: query = '%s %s' % (query, sxe)
            query = urllib.quote_plus(query)
            query_url = '/search?query=%s' % (query)
            hosters = self.__get_links(query_url, video)
            if not hosters and video.video_type == VIDEO_TYPES.EPISODE and params['air_date']:
                query = urllib.quote_plus('%s %s' % (params['title'], params['air_date'].replace('-', '.')))
                query_url = '/search?query=%s' % (query)
                hosters = self.__get_links(query_url, video)

        return hosters
    
    def __get_links(self, url, video):
        hosters = []
        search_url, params = self.__translate_search(url)
        html = self._http_get(search_url, params=params, cache_limit=.5)
        js_result = scraper_utils.parse_json(html, search_url)
        down_url = js_result.get('downURL')
        dl_farm = js_result.get('dlFarm')
        dl_port = js_result.get('dlPort')
        for item in js_result.get('data', []):
            post_hash, size, post_title, ext, duration = item['0'], item['4'], item['10'], item['11'], item['14']
            checks = [False] * 6
            if not scraper_utils.release_check(video, post_title): checks[0] = True
            if 'alangs' in item and item['alangs'] and 'eng' not in item['alangs']: checks[1] = True
            if re.match('^\d+s', duration) or re.match('^[0-5]m', duration): checks[2] = True
            if 'passwd' in item and item['passwd']: checks[3] = True
            if 'virus' in item and item['virus']: checks[4] = True
            if 'type' in item and item['type'].upper() != 'VIDEO': checks[5] = True
            if any(checks):
                logger.log('EasyNews Post excluded: %s - |%s|' % (checks, item), log_utils.LOGDEBUG)
                continue
            
            stream_url = down_url + urllib.quote('/%s/%s/%s%s/%s%s' % (dl_farm, dl_port, post_hash, ext, post_title, ext))
            stream_url = stream_url + '|Authorization=%s' % (urllib.quote(self.auth))
            host = scraper_utils.get_direct_hostname(self, stream_url)
            quality = None
            if 'width' in item:
                try: width = int(item['width'])
                except: width = 0
                if width:
                    quality = scraper_utils.width_get_quality(width)
            
            if quality is None:
                if video.video_type == VIDEO_TYPES.MOVIE:
                    meta = scraper_utils.parse_movie_link(post_title)
                else:
                    meta = scraper_utils.parse_episode_link(post_title)
                quality = scraper_utils.height_get_quality(meta['height'])
                
            if self.max_bytes:
                match = re.search('([\d.]+)\s+(.*)', size)
                if match:
                    size_bytes = scraper_utils.to_bytes(*match.groups())
                    if size_bytes > self.max_bytes:
                        logger.log('Result skipped, Too big: |%s| - %s (%s) > %s (%s GB)' % (post_title, size_bytes, size, self.max_bytes, self.max_gb))
                        continue

            hoster = {'multi-part': False, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'host': host, 'quality': quality, 'direct': True}
            if any(i for i in ['X265', 'HEVC'] if i in post_title.upper()): hoster['format'] = 'x265'
            if size: hoster['size'] = size
            if post_title: hoster['extra'] = post_title
            hosters.append(hoster)
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

    def _http_get(self, url, params=None, cache_limit=8):
        if not self.username or not self.password:
            return ''
        
        headers = {'Authorization': self.auth}
        return super(self.__class__, self)._http_get(url, params=params, headers=headers, cache_limit=cache_limit)

    def __translate_search(self, url):
        params = SEARCH_PARAMS
        params['pby'] = self.max_results
        params['gps'] = params['sbj'] = scraper_utils.parse_query(url)['query']
        url = scraper_utils.urljoin(self.base_url, SEARCH_URL)
        return url, params
