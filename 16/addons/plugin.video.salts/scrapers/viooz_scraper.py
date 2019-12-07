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
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://viooz.ac'

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
        return 'viooz.ac'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        iframes = []
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'boxed'}):
            iframes += dom_parser2.parse_dom(fragment, 'iframe', req='src')
            
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'contenu'}):
            for attrs, _content in dom_parser2.parse_dom(fragment, 'a', req='href') + iframes:
                stream_url = attrs.get('href') or attrs.get('src')
                if '/go/' not in stream_url: continue
                
                stream_url = stream_url.split('/')[-1]
                if stream_url.startswith('aHR0c'):
                    stream_url = base64.b64decode(stream_url)
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': host, 'rating': None, 'views': None, 'direct': False}
                hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search')
        params = {'q': title, 's': 't'}
        html = self._http_get(search_url, params=params, cache_limit=1)
        for _attrs, content in dom_parser2.parse_dom(html, 'span', {'class': 'title_list'}):
            match = dom_parser2.parse_dom(content, 'a', req=['href', 'title'])
            if match:
                attrs = match[0].attrs
                match_url, match_title_year = attrs['href'], attrs['title']
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
                    
        return results
