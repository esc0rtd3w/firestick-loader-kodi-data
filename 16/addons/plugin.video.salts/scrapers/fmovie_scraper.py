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
import urllib
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
import scraper


BASE_URL = 'https://fmovie.co'
INFO_URL = BASE_URL + '/video_info/iframe'

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
        return 'fmovie.co'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        match = re.search('var\s*video_id="([^"]+)', html)
        if not match: return hosters
        
        video_id = match.group(1)
        data = {'v': video_id}
        headers = {'Referer': page_url}
        headers.update(XHR)
        html = self._http_get(INFO_URL, data=data, headers=headers, cache_limit=.5)
        sources = scraper_utils.parse_json(html, INFO_URL)
        for source in sources:
            match = re.search('url=(.*)', sources[source])
            if not match: continue
            
            stream_url = urllib.unquote(match.group(1))
            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
            else:
                quality = scraper_utils.height_get_quality(source)
            stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
            hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/results')
        html = self._http_get(search_url, params={'q': title}, cache_limit=1)
        pattern = 'class="video_title".*?href="([^"]+)">([^<]+).*?Year</b>:\s*(\d*)'
        for match in re.finditer(pattern, html, re.DOTALL):
            url, match_title, match_year = match.groups()
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                results.append(result)
        return results
