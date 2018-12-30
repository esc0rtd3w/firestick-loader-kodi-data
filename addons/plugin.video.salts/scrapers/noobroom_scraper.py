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
import urllib2
import kodi
import dom_parser2
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger()
BASE_URL = 'http://superchillin.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))
        self.include_paid = kodi.get_setting('%s-include_premium' % (self.get_name())) == 'true'

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'NoobRoom'

    def resolve_link(self, link):
        url = scraper_utils.urljoin(self.base_url, link)
        html = self._http_get(url, cache_limit=.5)
        match = re.search('"file"\s*:\s*"([^"]+)', html)
        if match:
            file_link = match.group(1)
            stream_url = scraper_utils.urljoin(self.base_url, file_link)
            cj = self._set_cookies(self.base_url, {})
            request = urllib2.Request(stream_url)
            request.add_header('User-Agent', scraper_utils.get_ua())
            request.add_unredirected_header('Host', request.get_host())
            request.add_unredirected_header('Referer', url)
            cj.add_cookie_header(request)
            response = urllib2.urlopen(request)
            return response.geturl()

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        has_1080p = True if 'Watch in 1080p' in html else False
        if video.video_type == VIDEO_TYPES.MOVIE:
            quality = QUALITIES.HD720
            paid_quality = QUALITIES.HD1080
        else:
            quality = QUALITIES.HIGH
            paid_quality = QUALITIES.HD720
            
        loads = re.findall('<span[^>]*>(\d+)%</span>', html)
        for match, load in map(None, dom_parser2.parse_dom(html, 'a', {'class': 'hoverz'}, req='href'), loads):
            stream_url = match.attrs['href']
            label = match.content
            if load is None: load = 0

            match = re.search('([^<]+)\s+\(([^)]+)', label)
            if not match: continue
            host, status = match.groups()
            if not self.include_paid and status.upper() == 'PREMIUM':
                continue

            url = url.replace('&amp;', '&')
            host = '%s (%s)' % (host, status)
            hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': quality, 'views': None, 'rating': 100 - int(load), 'direct': True}
            hosters.append(hoster)

            if self.include_paid and has_1080p:
                url += '&hd=1'
                hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': paid_quality, 'views': None, 'rating': 100 - int(load), 'direct': True}
                hosters.append(hoster)
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = "%sx%02d\s*-\s*.*?href='([^']+)" % (video.season, int(video.episode))
        title_pattern = "\d+x\d+\s*-\s*.*?href='(?P<url>[^']+)'>(?P<title>[^<]+)"
        airdate_pattern = "href='([^']+)(?:[^>]+>){3}\s*-\s*\(Original Air Date:\s+{day}-{month}-{year}"
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        return self._default_get_episode_url(html, video, episode_pattern, title_pattern, airdate_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        if not self.include_paid and video_type != VIDEO_TYPES.MOVIE: return []
        search_url = scraper_utils.urljoin(self.base_url, '/search.php')
        html = self._http_get(search_url, params={'q': title}, cache_limit=.25)
        results = []
        if video_type == VIDEO_TYPES.MOVIE:
            pattern = '<i>\s*Movies\s*</i>(.*)'
        else:
            pattern = '<i>\s*TV Series\s*</i>(.*)'

        match = re.search(pattern, html)
        if not match: return results
        
        container = match.group(1)
        pattern = "href='([^']+)'>([^<]+)\s*</a>\s*(?:\((\d{4})\))?"
        for match in re.finditer(pattern, container):
            url, match_title, match_year = match.groups('')
            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)

        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-3,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-4,true)"/>' % (name, i18n('password')))
        settings.append('         <setting id="%s-include_premium" type="bool" label="     %s" default="false" visible="eq(-5,true)"/>' % (name, i18n('include_premium')))
        return settings

    def _http_get(self, url, params=None, data=None, headers=None, method=None, cache_limit=8):
        # return all uncached blank pages if no user or pass
        if not self.username or not self.password:
            return ''

        html = super(self.__class__, self)._http_get(url, params=params, data=data, headers=headers, method=method, cache_limit=cache_limit)
        if 'href="logout.php"' not in html:
            logger.log('Logging in for url (%s)' % (url), log_utils.LOGDEBUG)
            self.__login(html)
            html = super(self.__class__, self)._http_get(url, params=params, data=data, headers=headers, method=method, cache_limit=0)

        return html

    def __login(self, html):
        url = scraper_utils.urljoin(self.base_url, '/login2.php')
        data = {'email': self.username, 'password': self.password, 'echo': 'echo'}
        match = re.search('challenge\?k=([^"]+)', html)
        if match:
            data.update(scraper_utils.do_recaptcha(self, match.group(1)))
            
        html = super(self.__class__, self)._http_get(url, data=data, allow_redirect=False, cache_limit=0)
        if 'index.php' not in html:
            raise Exception('noobroom login failed')
