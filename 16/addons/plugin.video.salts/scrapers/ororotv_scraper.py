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
import base64
import datetime
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger()
BASE_URL = 'https://ororo.tv'

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
        return 'ororo.tv'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        query = scraper_utils.parse_query(source_url)
        if 'id' in query:
            vid_type = 'movies' if video.video_type == VIDEO_TYPES.MOVIE else 'episodes'
            url = scraper_utils.urljoin(self.base_url, '/api/v2/%s/%s' % (vid_type, query['id']))
            js_data = self._http_get(url, cache_limit=.5)
            if 'url' in js_data:
                stream_url = js_data['url']
                quality = QUALITIES.HD720
                hoster = {'multi-part': False, 'host': scraper_utils.get_direct_hostname(self, stream_url), 'class': self, 'url': stream_url, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
                hosters.append(hoster)
        return hosters

    def _get_episode_url(self, show_url, video):
        query = scraper_utils.parse_query(show_url)
        if 'id' in query:
            url = scraper_utils.urljoin(self.base_url, '/api/v2/shows/%s' % (query['id']))
            js_data = self._http_get(url, cache_limit=.5)
            if 'episodes' in js_data:
                force_title = scraper_utils.force_title(video)
                if not force_title:
                    for episode in js_data['episodes']:
                        if int(video.season) == int(episode['season']) and int(video.episode) == int(episode['number']):
                            return scraper_utils.pathify_url('?id=%s' % (episode['id']))
                    
                    if kodi.get_setting('airdate-fallback') == 'true' and video.ep_airdate:
                        for episode in js_data['episodes']:
                            if 'airdate' in episode:
                                ep_airdate = scraper_utils.to_datetime(episode['airdate'], "%Y-%m-%d").date()
                                if video.ep_airdate == (ep_airdate - datetime.timedelta(days=1)):
                                    return scraper_utils.pathify_url('?id=%s' % (episode['id']))
                else:
                    logger.log('Skipping S&E matching as title search is forced on: %s' % (video.trakt_id), log_utils.LOGDEBUG)
                
                if (force_title or kodi.get_setting('title-fallback') == 'true') and video.ep_title:
                    norm_title = scraper_utils.normalize_title(video.ep_title)
                    for episode in js_data['episodes']:
                        if 'name' in episode and norm_title in scraper_utils.normalize_title(episode['name']):
                            return scraper_utils.pathify_url('?id=%s' % (episode['id']))

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        if video_type == VIDEO_TYPES.MOVIE:
            url = '/api/v2/movies'
            key = 'movies'
        else:
            url = '/api/v2/shows'
            key = 'shows'
        url = scraper_utils.urljoin(self.base_url, url)
        js_data = self._http_get(url, cache_limit=8)
        norm_title = scraper_utils.normalize_title(title)
        if key in js_data:
            for item in js_data[key]:
                match_title = item['name']
                match_year = item.get('year', '')
                match_url = '?id=%s' % (item['id'])
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-3,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-4,true)"/>' % (name, i18n('password')))
        return settings

    def _http_get(self, url, data=None, headers=None, cookies=None, cache_limit=8):
        # return all uncached blank pages if no user or pass
        if not self.username or not self.password:
            return ''
        
        if headers is None: headers = {}
        auth_header = base64.b64encode('%s:%s' % (self.username, self.password))
        headers['Authorization'] = 'Basic %s' % (auth_header)
        html = super(self.__class__, self)._http_get(url, data=data, headers=headers, cookies=cookies, cache_limit=cache_limit)
        return scraper_utils.parse_json(html, url)
