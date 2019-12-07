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
import urlparse
import kodi
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://watchmovies-online.is'

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
        return 'wmo.ch'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        for _attrs, td in dom_parser2.parse_dom(html, 'td', {'class': 'tdhost'}):
            match = dom_parser2.parse_dom(td, 'a', req='href')
            if match:
                stream_url = match[0].attrs['href']
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
                hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title, 'search': ''}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'movie_poster'}):
            match = dom_parser2.parse_dom(item, 'a', req=['href', 'title'])
            if match:
                attrs = match[0].attrs
                match_title, match_year = scraper_utils.extra_year(attrs['title'])
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(attrs['href']), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results
