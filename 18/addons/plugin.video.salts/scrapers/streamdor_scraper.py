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
import urllib
import scraper
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import XHR

BASE_URL = 'https://api.streamdor.com'
Q_MAP = {'hd': QUALITIES.HD720, 'sd': QUALITIES.HIGH}

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
        return 'StreamDor'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, headers=XHR, cache_limit=8)
        js_data = scraper_utils.parse_json(html, url)
        quality = Q_MAP.get(js_data.get('Key', {}).get('MovieDefinition'), QUALITIES.HIGH)
        value = js_data.get('Value', {})
        stream_url = value.get('VideoLink')
        if stream_url and value.get('ProviderSource', '').lower() == 'youtube':
            host = 'youtube.com'
            source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
            hosters.append(source)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/searchBoxSuggestion')
        html = self._http_get(search_url, params={'top': 8, 'query': title}, cache_limit=8)
        js_data = scraper_utils.parse_json(html, search_url)
        for item in js_data:
            entityName = match_title_year = item.get('Value', '')
            if entityName:
                match_title, match_year2 = scraper_utils.extra_year(match_title_year)
                match_year = str(item.get('ReleaseYear', ''))
                if not match_year: match_year = match_year2
                
                match_url = '/ontology/EntityDetails?' + urllib.urlencode({'entityName': entityName, 'ignoreMediaLinkError': 'false'})
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
