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
import kodi
import log_utils  # @UnusedImport
import dom_parser2
import json
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger()

BASE_URL = 'http://www.snagfilms.com'
SOURCE_BASE_URL = 'http://mp4.snagfilms.com'
SEARCH_URL = '/apis/search.json'
SEARCH_TYPES = {VIDEO_TYPES.MOVIE: 'film', VIDEO_TYPES.TVSHOW: 'show'}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'SnagFilms'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'film-container'})
        if fragment:
            iframe_url = dom_parser2.parse_dom(fragment[0].content, 'iframe', req='src')
            if iframe_url:
                iframe_url = scraper_utils.urljoin(self.base_url, iframe_url[0].attrs['src'])
                headers = {'Referer': page_url}
                html = self._http_get(iframe_url, headers=headers, cache_limit=.5)
                sources = scraper_utils.parse_sources_list(self, html)
                for source in sources:
                    quality = sources[source]['quality']
                    host = scraper_utils.get_direct_hostname(self, source)
                    stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': iframe_url})
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    match = re.search('(\d+[a-z]bps)', source)
                    if match:
                        hoster['extra'] = match.group(1)
                    hosters.append(hoster)
                        
        hosters.sort(key=lambda x: x.get('extra', ''), reverse=True)
        return hosters

    def _get_episode_url(self, season_url, video):
        episode_pattern = 'data-title\s*=\s*"Season\s+0*%s\s+Episode\s+0*%s[^>]*data-permalink\s*=\s*"([^"]+)' % (video.season, video.episode)
        title_pattern = 'data-title\s*=\s*"Season\s+\d+\s+Episode\s+\d+\s*(?P<title>[^"]+)[^>]+data-permalink\s*=\s*"(?P<url>[^"]+)'
        season_url = scraper_utils.urljoin(self.base_url, season_url)
        html = self._http_get(season_url, cache_limit=2)
        return self._default_get_episode_url(html, video, episode_pattern, title_pattern)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, SEARCH_URL)
        referer = scraper_utils.urljoin(self.base_url, '/search/?q=%s')
        referer = referer % (urllib.quote_plus(title))
        headers = {'Referer': referer}
        headers.update(XHR)
        params = {'searchTerm': title, 'type': SEARCH_TYPES[video_type], 'limit': 500}
        html = self._http_get(search_url, params=params, headers=headers, auth=False, cache_limit=2)
        js_data = scraper_utils.parse_json(html, search_url)
        if 'results' in js_data:
            for result in js_data['results']:
                match_year = str(result.get('year', ''))
                match_url = result.get('permalink', '')
                match_title = result.get('title', '')
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-3,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-4,true)"/>' % (name, i18n('password')))
        return settings

    def _http_get(self, url, params=None, data=None, headers=None, auth=True, method=None, cache_limit=8):
        # return all uncached blank pages if no user or pass
        if not self.username or not self.password:
            return ''

        html = super(self.__class__, self)._http_get(url, params=params, data=data, headers=headers, method=method, cache_limit=cache_limit)
        if auth and not dom_parser2.parse_dom(html, 'span', {'class': 'user-name'}):
            logger.log('Logging in for url (%s)' % (url), log_utils.LOGDEBUG)
            self.__login()
            html = super(self.__class__, self)._http_get(url, params=params, data=data, headers=headers, method=method, cache_limit=0)

        return html

    def __login(self):
        url = scraper_utils.urljoin(self.base_url, '/apis/v2/user/login.json')
        data = {'email': self.username, 'password': self.password, 'rememberMe': True}
        referer = scraper_utils.urljoin(self.base_url, '/login')
        headers = {'Content-Type': 'application/json', 'Referer': referer}
        headers.update(XHR)
        html = super(self.__class__, self)._http_get(url, data=json.dumps(data), headers=headers, cache_limit=0)
        js_data = scraper_utils.parse_json(html, url)
        return js_data.get('status') == 'success'
