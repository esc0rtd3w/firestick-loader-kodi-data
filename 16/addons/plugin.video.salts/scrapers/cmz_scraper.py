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
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://coolmoviezone.net'

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
        return 'cmz'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        
        match = re.search('Views?\s*:\s*(\d+)', html, re.I)
        if match:
            views = match.group(1)
        else:
            views = None

        pattern = 'href="[^"]+/rd\.html\?url=([^"]+)'
        for match in re.finditer(pattern, html):
            url = match.group(1)
            host = urlparse.urlsplit(url).hostname
            hoster = {'multi-part': False, 'host': host, 'url': url, 'class': self, 'rating': None, 'views': views, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'direct': False}
            hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/index.php')
        html = self._http_get(search_url, params={'s': title}, cache_limit=1)
        pattern = 'href="([^"]+)"\s+rel="bookmark">([^<]+)\s+\((\d{4})\)'
        for match in re.finditer(pattern, html, re.DOTALL):
            url, match_title, match_year = match.groups()
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                results.append(result)
        
        return results
