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
import json
import re
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'https://sit2play.com'
TITLE_URL = '/api/v1/title/{id}'
SEARCH_BASE = 'https://xxdazcoul3-dsn.algolia.net'
TEMPLATE = 'https://{prefix}{mirror}.{suffix}{path}'
Q_MAP = {'normal': QUALITIES.HD720, 'hd': QUALITIES.HD1080}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Sit2Play'

    def get_sources(self, video):
        sources = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return sources
        object_id = self.__extract_id(source_url)
        if object_id is None: return sources
        source_url = TITLE_URL.format(id=object_id)
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._authed_http_get(page_url, cache_limit=.5)
        js_data = scraper_utils.parse_json(html, page_url)
        if video.video_type == VIDEO_TYPES.MOVIE:
            links = js_data.get('links', {})
        else:
            links = self.__episode_match(js_data, video)

        prefix = js_data.get('domain', {}).get('prefix')
        suffix = js_data.get('domain', {}).get('suffix')
        for key, path in links.get('links', {}).iteritems():
            for mirror in sorted(list(set(links.get('mirrors', [])))):
                stream_url = TEMPLATE.format(prefix=prefix, mirror=mirror, suffix=suffix, path=path)
                host = scraper_utils.get_direct_hostname(self, stream_url)
                quality = Q_MAP.get(key, QUALITIES.HIGH)
                source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
                source['version'] = '(Mirror %d)' % (mirror)
                sources.append(source)

        return sources

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(SEARCH_BASE, '/1/indexes/al_titles_index/query')
        params = {'x-algolia-agent': 'Algolia for vanilla JavaScript (lite) 3.22.1', 'x-algolia-application-id': 'XXDAZCOUL3',
                  'x-algolia-api-key': 'c5c1279f5ad09819ecf2af9d6b5ee06a'}
        data = {'params': urllib.urlencode({'query': title, 'facets': '*', 'hitsPerPage': 30})}
        headers = {'Origin': self.base_url}
        html = self._http_get(search_url, params=params, data=json.dumps(data), headers=headers, cache_limit=8)
        js_data = scraper_utils.parse_json(html, search_url)
        media_type = '/movies/' if video_type == VIDEO_TYPES.MOVIE else '/tv/'
        for item in js_data.get('hits', []):
            if 'permalink' in item and 'title' in item and media_type in item['permalink']:
                match_year = str(item.get('yr', ''))
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(item['title']), 'url': scraper_utils.pathify_url(item['permalink']), 'year': match_year}
                    results.append(result)

        return results

    def _get_episode_url(self, show_url, video):
        object_id = self.__extract_id(show_url)
        if object_id is None: return
        url = scraper_utils.urljoin(self.base_url, TITLE_URL.format(id=object_id))
        html = self._authed_http_get(url, cache_limit=2)
        js_data = scraper_utils.parse_json(html, url)
        if self.__episode_match(js_data, video):
            return show_url

    def __episode_match(self, js_data, video):
        label = 's%se%s' % (video.season, video.episode)
        for key in js_data.get('links', {}).iterkeys():
            if key == label:
                return js_data['links'][key]
        
        return {}
    
    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-3,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-4,true)"/>' % (name, i18n('password')))
        return settings

    def _http_get(self, url, params=None, data=None, multipart_data=None, headers=None, cookies=None,
                  allow_redirect=True, method=None, require_debrid=False, read_error=False, cache_limit=8):
        # return all uncached pages if no user or pass
        if not self.username or not self.password:
            return json.dumps({'msg': 'unauthorized'})
    
        return super(self.__class__, self)._http_get(url, params=params, data=data, multipart_data=multipart_data, headers=headers, cookies=cookies,
                                                     allow_redirect=allow_redirect, method=method, require_debrid=require_debrid, read_error=read_error, cache_limit=cache_limit)
    
    def _authed_http_get(self, url, data=None, headers=None, method=None, cache_limit=8):
        html = self._http_get(url, data=data, headers=headers, method=method, cache_limit=cache_limit)
        if not html:
            logger.log('Logging in for url (%s)' % (url), log_utils.LOGDEBUG)
            self.__login()
            html = self._http_get(url, data=data, headers=headers, method=method, cache_limit=0)

        return html
    
    def __extract_id(self, url):
        try: return re.search('/(tt\d+)', url).group(1)
        except AttributeError: pass
        
    def __login(self):
        url = scraper_utils.urljoin(self.base_url, '/api/v1/user/login')
        data = {'user': self.username, 'password': self.password}
        headers = {'Content-Type': 'application/json'}
        html = self._http_get(url, data=json.dumps(data), headers=headers, cache_limit=0)
        js_data = scraper_utils.parse_json(html, url)
        if 'user' not in js_data: raise Exception('sit2play login failed')
