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
import scraper
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://www.spacemov.ag'

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
        return 'SpaceMov'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=8)
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'responsiveVideo'}):
            for attrs, _content in dom_parser2.parse_dom(fragment, 'iframe', req='src') + dom_parser2.parse_dom(fragment, 'script', req='src'):
                source = attrs['src']
                if 'validateemb' in source: continue
                host = urlparse.urlparse(source).hostname
                source = {'multi-part': False, 'url': source, 'host': host, 'class': self, 'quality': QUALITIES.HD720, 'views': None, 'rating': None, 'direct': False}
                hosters.append(source)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'browse-movie-bottom'}):
            match = dom_parser2.parse_dom(item, 'a', req='href')
            if match:
                match_url, match_title_year = match[0].attrs['href'], match[0].content
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if not match_year:
                    div = dom_parser2.parse_dom(item, 'div', {'class': 'browse-movie-year'})
                    if div: match_year = div[0].content.strip()
                        
                match_url += '?watching'
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
