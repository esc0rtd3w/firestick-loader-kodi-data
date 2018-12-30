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
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://www.mintmovies.net'

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
        return 'MintMovies'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters

        sources = []
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        for _attrs, div in dom_parser2.parse_dom(html, 'div', {'class': 'tab-content'}):
            for attrs, _content in dom_parser2.parse_dom(div, 'iframe', req='src'):
                sources.append(attrs['src'])
        
        sources += [match.group(1) for match in re.finditer("window\.open\('([^']+)", html)]
        
        for source in sources:
            host = urlparse.urlparse(source).hostname
            quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': False}
            hosters.append(hoster)
                    
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=1)
        if re.search('Sorry, but nothing matched', html, re.I): return results
        
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(html, 'li', {'class': 'box-shadow'}):
            for attrs, _content in dom_parser2.parse_dom(item, 'a', req=['href', 'title']):
                match_url, match_title_year = attrs['href'], attrs['title']
                if re.search('S\d{2}E\d{2}', match_title_year): continue  # skip episodes
                if re.search('TV\s*SERIES', match_title_year, re.I): continue  # skip shows
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if (not year or not match_year or year == match_year) and norm_title in scraper_utils.normalize_title(match_title):
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
