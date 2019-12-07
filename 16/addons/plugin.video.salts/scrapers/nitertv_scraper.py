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
import urlparse
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger()
BASE_URL = 'http://niter.co'
PHP_URL = BASE_URL + '/player/pk/pk/plugins/player_p2.php'
DIR_URL = BASE_URL + '/player/getVideo.php'
MAX_TRIES = 3

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'niter.tv'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        match = re.search('((?:pic|emb|vb|dir|emb2)=[^<]+)', html)
        if match:
            embeds = match.group(1)
            for stream_url in embeds.split('&'):
                if stream_url.startswith('dir='):
                    headers = {'Referer': url}
                    html = self._http_get(DIR_URL, params={'v': stream_url[3:]}, headers=headers, auth=False, allow_redirect=False, cache_limit=.5)
                    if html.startswith('http'):
                        stream_url = html + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': url})
                        host = scraper_utils.get_direct_hostname(self, stream_url)
                        direct = True
                        quality = QUALITIES.HD720
                    else:
                        continue
                elif stream_url.startswith('vb='):
                    stream_url = 'http://www.vidbux.com/%s' % (stream_url[3:])
                    host = 'vidbux.com'
                    direct = False
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HD1080)
                elif stream_url.startswith('pic='):
                    data = {'url': stream_url[4:]}
                    html = self._http_get(PHP_URL, data=data, auth=False, cache_limit=1)
                    js_data = scraper_utils.parse_json(html, PHP_URL)
                    host = scraper_utils.get_direct_hostname(self, stream_url)
                    direct = True
                    for item in js_data:
                        if item.get('medium') == 'video':
                            stream_url = item['url']
                            quality = scraper_utils.width_get_quality(item['width'])
                            break
                    else:
                        continue
                elif stream_url.startswith(('emb=', 'emb2=')):
                    stream_url = re.sub('emb\d*=', '', stream_url)
                    host = urlparse.urlparse(stream_url).hostname
                    direct = False
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HD720)
                else:
                    continue

                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        search_url = scraper_utils.urljoin(self.base_url, '/search')
        html = self._http_get(search_url, params={'q': title}, cache_limit=.25)
        results = []
        pattern = 'data-name="([^"]+).*?href="([^"]+)'
        for match in re.finditer(pattern, html, re.DOTALL):
            match_title, url = match.groups()
            result = {'title': scraper_utils.cleanse_title(match_title), 'year': '', 'url': scraper_utils.pathify_url(url)}
            results.append(result)
        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-3,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-4,true)"/>' % (name, i18n('password')))
        return settings

    def _http_get(self, url, params=None, data=None, headers=None, auth=True, allow_redirect=True, cache_limit=8):
        # return all uncached blank pages if no user or pass
        if not self.username or not self.password:
            return ''

        html = super(self.__class__, self)._http_get(url, params=params, data=data, headers=headers, allow_redirect=allow_redirect, cache_limit=cache_limit)
        if auth and not re.search('href="[^"]+/logout"', html):
            logger.log('Logging in for url (%s)' % (url), log_utils.LOGDEBUG)
            self.__login()
            html = super(self.__class__, self)._http_get(url, params=params, data=data, headers=headers, allow_redirect=allow_redirect, cache_limit=0)

        return html

    def __login(self):
        url = scraper_utils.urljoin(self.base_url, '/sessions')
        data = {'username': self.username, 'password': self.password, 'remember': 1}
        html = super(self.__class__, self)._http_get(url, data=data, allow_redirect=False, cache_limit=0)
        if html != self.base_url:
            raise Exception('niter.tv login failed')
