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
import scraper
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib import jsunpack
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://openloadmovies.tv'
Q_MAP = {'HD': QUALITIES.HD720, 'DVD': QUALITIES.HIGH, 'CAM': QUALITIES.LOW}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'OLMovies'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=8)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'playex'})
        if fragment: html = fragment[0].content
        links = scraper_utils.parse_sources_list(self, html)
        for link in links:
            stream_url = link
            if self.base_url in link:
                redir_url = self._http_get(link, headers={'Referer': url}, allow_redirect=False, method='HEAD')
                if redir_url.startswith('http'):
                    stream_url = redir_url
            
            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
            else:
                quality = links[link]['quality']
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': url})
                
            source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
            hosters.append(source)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'result-item'}):
            match = dom_parser2.parse_dom(item, 'div', {'class': 'title'})
            is_movie = dom_parser2.parse_dom(item, 'span', {'class': 'movies'})
            if not is_movie or not match: return results
            
            match = dom_parser2.parse_dom(match[0].content, 'a', req='href')
            if not match: return results
            
            match_url, match_title_year = match[0].attrs['href'], match[0].content
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if not match_year:
                match_year = dom_parser2.parse_dom(item, 'span', {'class': 'year'})
                match_year = match_year[0].content if match_year else ''
                
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results

    def _http_get(self, url, params=None, data=None, multipart_data=None, headers=None, cookies=None, allow_redirect=True, method=None,
                  require_debrid=False, read_error=False, cache_limit=8):
        html = super(self.__class__, self)._http_get(url, params=params, data=data, multipart_data=multipart_data, headers=headers, cookies=cookies,
                                                     allow_redirect=allow_redirect, method=method, require_debrid=require_debrid, read_error=read_error, cache_limit=cache_limit)
        
        if re.search('<body\s+onload=', html, re.I):
            if cookies is None: cookies = {}
            cookies.update(self.__get_cookies(html))
            html = super(self.__class__, self)._http_get(url, params=params, data=data, multipart_data=multipart_data, headers=headers, cookies=cookies,
                                                         allow_redirect=allow_redirect, method=method, require_debrid=require_debrid, read_error=read_error, cache_limit=0)
            
        return html
    
    def __get_cookies(self, html):
        try:
            js_code = ''
            for match in re.finditer('(eval\(function\(.*?)</script>', html, re.DOTALL):
                js_data = jsunpack.unpack(match.group(1))
                js_data = js_data.replace('\\', '')
                js_code += js_data
                
            match = re.search("cookie\s*=\s*'([^;']+)", js_code)
            parts = match.group(1).split('=')
            cookies = {parts[0]: parts[1]}
        except:
            cookies = {}
            
        return cookies
