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
import urllib
import urlparse

import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger()
Q_LIST = [item[0] for item in sorted(Q_ORDER.items(), key=lambda x:x[1])]

BASE_URL = 'http://www.alluc.ee'
SEARCH_URL = '/api/search/%s/'
SEARCH_TYPES = ['stream', 'download']
QUALITY_MAP = {
    QUALITIES.LOW: ['DVDSCR', 'CAMRIP', 'HDCAM'],
    QUALITIES.MEDIUM: [],
    QUALITIES.HIGH: ['BDRIP', 'BRRIP', 'HDRIP'],
    QUALITIES.HD720: ['720P'],
    QUALITIES.HD1080: ['1080P']}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'alluc.com'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        
        params = scraper_utils.parse_query(source_url)
        if video.video_type == VIDEO_TYPES.MOVIE:
            query = urllib.quote_plus('%s %s' % (params['title'], params['year']))
        else:
            query = urllib.quote_plus('%s S%02dE%02d' % (params['title'], int(params['season']), int(params['episode'])))
        query_url = '/search?query=%s' % (query)
        hosters = self.__get_links(query_url, video)
        if not hosters and video.video_type == VIDEO_TYPES.EPISODE and params['air_date']:
            query = urllib.quote_plus('%s %s' % (params['title'], params['air_date'].replace('-', '.')))
            query_url = '/search?query=%s' % (query)
            hosters = self.__get_links(query_url, video)

        return hosters

    def __get_links(self, url, video):
        hosters = []
        seen_urls = set()
        for search_type in SEARCH_TYPES:
            search_url, params = self.__translate_search(url, search_type)
            if not search_url: continue
            html = self._http_get(search_url, params=params, cache_limit=.5)
            js_result = scraper_utils.parse_json(html, search_url)
            if js_result.get('status') != 'success':
                logger.log('Alluc API Error: |%s|%s|: %s' % (search_url, params, js_result.get('message', 'Unknown Error')), log_utils.LOGWARNING)
                continue
            
            for result in js_result['result']:
                stream_url = result['hosterurls'][0]['url']
                if len(result['hosterurls']) > 1: continue
                if result['extension'] == 'rar': continue
                if stream_url in seen_urls: continue

                if scraper_utils.release_check(video, result['title']):
                    host = urlparse.urlsplit(stream_url).hostname
                    quality = scraper_utils.get_quality(video, host, self._get_title_quality(result['title']))
                    hoster = {'multi-part': False, 'class': self, 'views': None, 'url': stream_url, 'rating': None, 'host': host, 'quality': quality, 'direct': False}
                    hoster['extra'] = scraper_utils.cleanse_title(result['title'])
                    if video.video_type == VIDEO_TYPES.MOVIE:
                        meta = scraper_utils.parse_movie_link(hoster['extra'])
                    else:
                        meta = scraper_utils.parse_episode_link(hoster['extra'])
                    if 'format' in meta: hoster['format'] = meta['format']
                    
                    hosters.append(hoster)
                    seen_urls.add(stream_url)

        return hosters
        
    def _get_title_quality(self, title):
        post_quality = QUALITIES.HIGH
        title = title.upper()
        for key in Q_LIST:
            if any(q in title for q in QUALITY_MAP[key]):
                post_quality = key

        # logger.log('Setting |%s| to |%s|' % (title, post_quality), log_utils.LOGDEBUG)
        return post_quality
    
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
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-3,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-4,true)"/>' % (name, i18n('password')))
        return settings

    def __translate_search(self, url, search_type):
        query = scraper_utils.parse_query(url)
        query = query['query'] + ' lang:en'
        url = scraper_utils.urljoin(self.base_url, SEARCH_URL % (search_type))
        params = {'query': query, 'count': 100, 'from': 0, 'getmeta': 0}
        if self.username and self.password:
            params.update({'user': self.username, 'password': self.password})
        else:
            url = ''
        return url, params
