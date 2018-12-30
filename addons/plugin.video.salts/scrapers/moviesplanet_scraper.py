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
import re
import time
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger()
BASE_URL = 'https://www.moviesplanet.tv'
GK_KEY = base64.urlsafe_b64decode('MllVcmlZQmhTM2swYU9BY0lmTzQ=')
QUALITY_MAP = {'HD': QUALITIES.HD720}

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
        return 'MoviesPlanet'

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = {}
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=0)
        for match in re.finditer("embeds\[(\d+)\]\s*=\s*'([^']+)", html):
            match = re.search('src="([^"]+)', match.group(2))
            if match:
                iframe_url = match.group(1)
                if 'play-en.php' in iframe_url:
                    match = re.search('id=([^"&]+)', iframe_url)
                    if match:
                        proxy_link = match.group(1)
                        proxy_link = proxy_link.split('*', 1)[-1]
                        picasa_url = scraper_utils.gk_decrypt(self.get_name(), GK_KEY, proxy_link)
                        for stream_url in scraper_utils.parse_google(self, picasa_url):
                            sources[stream_url] = {'quality': scraper_utils.gv_get_quality(stream_url), 'direct': True}
                else:
                    html = self._http_get(iframe_url, cache_limit=0)
                    temp_sources = scraper_utils.parse_sources_list(self, html)
                    for source in temp_sources:
                        if 'download.php' in source:
                            redir_html = self._http_get(source, allow_redirect=False, method='HEAD', cache_limit=0)
                            if redir_html.startswith('http'):
                                temp_sources[redir_html] = temp_sources[source]
                                del temp_sources[source]
                    sources.update(temp_sources)
                    for source in dom_parser2.parse_dom(html, 'source', {'type': 'video/mp4'}, req='src'):
                        sources[source.attrs['src']] = {'quality': QUALITIES.HD720, 'direct': True, 'referer': iframe_url}
                                
        for source, values in sources.iteritems():
            host = scraper_utils.get_direct_hostname(self, source)
            headers = {'User-Agent': scraper_utils.get_ua()}
            if 'referer' in values: headers['Referer'] = values['referer']
            stream_url = source + scraper_utils.append_headers(headers)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(source)
            else:
                quality = values['quality']
                if quality not in Q_ORDER:
                    quality = QUALITY_MAP.get(values['quality'], QUALITIES.HIGH)
                    
            hoster = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
            hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/ajax/search.php')
        timestamp = int(time.time() * 1000)
        query = {'q': title, 'limit': 100, 'timestamp': timestamp, 'verifiedCheck': ''}
        html = self._http_get(search_url, data=query, headers=XHR, cache_limit=1)
        if video_type in [VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE]:
            media_type = 'TV SHOW'
        else:
            media_type = 'MOVIE'

        js_data = scraper_utils.parse_json(html, search_url)
        for item in js_data:
            if not item['meta'].upper().startswith(media_type): continue
            
            result = {'title': scraper_utils.cleanse_title(item['title']), 'url': scraper_utils.pathify_url(item['permalink']), 'year': ''}
            results.append(result)

        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+/season/0*%s/episode/0*%s/?)"' % (video.season, video.episode)
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        return self._default_get_episode_url(html, video, episode_pattern)

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-3,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-4,true)"/>' % (name, i18n('password')))
        return settings

    def _http_get(self, url, data=None, headers=None, allow_redirect=True, method=None, cache_limit=8):
        # return all uncached blank pages if no user or pass
        if not self.username or not self.password:
            return ''

        html = super(self.__class__, self)._http_get(url, data=data, headers=headers, allow_redirect=allow_redirect, method=method, cache_limit=cache_limit)
        if re.search('Please Register or Login', html, re.I):
            logger.log('Logging in for url (%s)' % (url), log_utils.LOGDEBUG)
            self.__login()
            html = super(self.__class__, self)._http_get(url, data=data, headers=headers, allow_redirect=allow_redirect, method=method, cache_limit=0)
        return html

    def __login(self):
        url = scraper_utils.urljoin(self.base_url, '/login')
        data = {'username': self.username, 'password': self.password, 'returnpath': '/'}
        html = super(self.__class__, self)._http_get(url, data=data, headers=XHR, cache_limit=0)
        if 'incorrect login' in html.lower():
            raise Exception('moviesplanet login failed')
