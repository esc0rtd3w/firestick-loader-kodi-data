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
from string import capwords
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.utils2 import i18n
import scraper

logger = log_utils.Logger.get_logger()

BASE_URL = 'http://www.streamlord.com'
LOGIN_URL = '/login.html'

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
        return 'StreamLord'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=1)
        match = re.search('''["']sources['"]\s*:\s*\[(.*?)\]''', html, re.DOTALL)
        if match:
            for match in re.finditer('''['"]*file['"]*\s*:\s*([^\(]+)''', match.group(1), re.DOTALL):
                stream_url = self.__decode(match.group(1), html)
                if stream_url:
                    if video.video_type == VIDEO_TYPES.MOVIE:
                        quality = QUALITIES.HD720
                    else:
                        quality = QUALITIES.HIGH
                    stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': url, 'Cookie': self._get_stream_cookies()})
                    hoster = {'multi-part': False, 'host': scraper_utils.get_direct_hostname(self, stream_url), 'class': self, 'url': stream_url, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
                    hosters.append(hoster)

        return hosters

    def __decode(self, func, html):
        pattern = 'function\s+%s[^{]+{\s*([^}]+)' % (func)
        match = re.search(pattern, html, re.DOTALL)
        if match:
            match = re.search('\[([^\]]+)[^+]+\+\s*([^.]+).*?getElementById\("([^"]+)', match.group(1), re.DOTALL)
            if match:
                url, array, span = match.groups()
                url = self.__do_join(url)
                array = self.__get_array(array, html)
                span = self.__get_fragment(span, html)
                if url and array and span:
                    return url + array + span
                
    def __do_join(self, array):
        array = re.sub('[" ]', '', array)
        array = array.replace('\/', '/')
        return ''.join(array.split(','))
        
    def __get_array(self, array, html):
        pattern = 'var\s+%s\s*=\s*\[([^\]]+)' % (array)
        match = re.search(pattern, html)
        if match:
            return self.__do_join(match.group(1))
    
    def __get_fragment(self, span, html):
        fragment = dom_parser2.parse_dom(html, 'span', {'id': span})
        if fragment:
            return fragment[0].content
    
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]*-[Ss]0*%s[Ee]0*%s-[^"]+)' % (video.season, video.episode)
        title_pattern = 'class="head".*?</span>(?P<title>.*?)</a>.*?href="(?P<url>[^"]+)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'season-wrapper'})
        return self._default_get_episode_url(fragment, video, episode_pattern, title_pattern)
        
    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-3,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-4,true)"/>' % (name, i18n('password')))
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        url = scraper_utils.urljoin(self.base_url, '/search2.php')
        data = {'searchapi': title}
        headers = {'Referer': self.base_url}
        html = self._http_get(url, data=data, headers=headers, cache_limit=2)
        if video_type == VIDEO_TYPES.MOVIE:
            query_type = 'watch-movie-'
        else:
            query_type = 'watch-tvshow-'

        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(html, 'a', {'href': '#'}):
            match = re.search('href="(%s[^"]+)' % (query_type), item)
            if match:
                link = match.group(1)
                match_title = self.__make_title(link, query_type)
                match_year = ''
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or int(year) == int(match_year)):
                    result = {'url': scraper_utils.pathify_url(link), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results

    def __make_title(self, link, query_type):
        link = link.replace(query_type, '')
        link = re.sub('-\d+\.html', '', link)
        link = link.replace('-', ' ')
        link = capwords(link)
        return link

    def _http_get(self, url, auth=True, data=None, headers=None, allow_redirect=True, method=None, cache_limit=8):
        # return all uncached blank pages if no user or pass
        if not self.username or not self.password:
            return ''

        html = super(self.__class__, self)._http_get(url, data=data, headers=headers, allow_redirect=allow_redirect, method=method, cache_limit=cache_limit)
        if auth and LOGIN_URL in html:
            logger.log('Logging in for url (%s)' % (url), log_utils.LOGDEBUG)
            self.__login()
            html = super(self.__class__, self)._http_get(url, data=data, headers=headers, method=method, cache_limit=0)

        return html

    def __login(self):
        data = {'username': self.username, 'password': self.password, 'submit': 'Login'}
        url = scraper_utils.urljoin(self.base_url, LOGIN_URL)
        html = self._http_get(url, auth=False, data=data, allow_redirect=False, cache_limit=0)
        if html != 'index.html':
            raise Exception('StreamLord login failed: %s' % (html))
