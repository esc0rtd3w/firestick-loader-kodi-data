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


BASE_URL = 'http://filmikz.ch'

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
        return 'filmikz.ch'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        pattern = "/w\.php\?q=([^']+)"
        seen_hosts = {}
        for match in re.finditer(pattern, html, re.DOTALL):
            url = match.group(1)
            hoster = {'multi-part': False, 'url': url.decode('base-64'), 'class': self, 'quality': None, 'views': None, 'rating': None, 'direct': False}
            hoster['host'] = urlparse.urlsplit(hoster['url']).hostname
            # top list is HD, bottom list is SD
            if hoster['host'] in seen_hosts:
                quality = QUALITIES.HIGH
            else:
                quality = QUALITIES.HD720
                seen_hosts[hoster['host']] = True
            hoster['quality'] = scraper_utils.get_quality(video, hoster['host'], quality)
            hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/index.php')
        params = {'search': title, 'image.x': 0, 'image.y': 0}
        html = self._http_get(search_url, params=params, cache_limit=1)

        # Are we on a results page?
        if not re.search('window\.location', html):
            pattern = '<td[^>]+class="movieText"[^>]*>(.*?)</p>.*?href="(/watch/[^"]+)'
            for match in re.finditer(pattern, html, re.DOTALL):
                match_title_year, match_url = match.groups('')
                # skip porn
                if '-XXX-' in match_url.upper() or ' XXX:' in match_title_year: continue
                match_title_year = re.sub('</?.*?>', '', match_title_year)
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if not year or not match_year or year == match_year:
                    result = {'url': match_url, 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        else:
            match = re.search('window\.location\s+=\s+"([^"]+)', html)
            if not match: return results
            url = match.group(1)
            if url != 'movies.php':
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(title), 'year': year}
                results.append(result)
        return results
