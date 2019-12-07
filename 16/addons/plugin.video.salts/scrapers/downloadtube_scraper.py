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
import urllib
import scraper
import urlparse
import re
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
from salts_lib.constants import XHR

BASE_URL = 'http://www.mydownloadtube.com'

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
        return 'DownloadTube'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=8)
        movie_id = dom_parser2.parse_dom(html, 'input', {'id': 'movie_id'}, req='value')
        if not movie_id: return hosters
        
        data = {'movie': movie_id[0].attrs['value'], 'starttime': 'undefined', 'pageevent': 0, 'aspectration': ''}
        xhr_url = scraper_utils.urljoin(self.base_url, '/movies/play_online')
        headers = {'Referer': page_url}
        headers.update(XHR)
        html = self._http_get(xhr_url, data=data, headers=headers, cache_limit=.5)
        best_quality, _sources = self.__get_direct(html, page_url)
        for attrs, _content in dom_parser2.parse_dom(html, 'iframe', req='src'):
            stream_url = attrs['src']
            host = urlparse.urlparse(stream_url).hostname
            quality = scraper_utils.get_quality(video, host, best_quality)
            hoster = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
            hosters.append(hoster)

        return hosters

    def __get_direct(self, html, page_url):
        sources = []
        best_quality = QUALITIES.HIGH
        match = re.search('''['"]?sources["']?\s*:\s*\[(.*?)\}\s*,?\s*\]''', html, re.DOTALL)
        if match:
            files = re.findall('''['"]?file['"]?\s*:\s*(.*?)['"]([^'"]+)''', match.group(1), re.DOTALL)
            labels = re.findall('''['"]?label['"]?\s*:\s*['"]([^'"]*)''', match.group(1), re.DOTALL)
            for stream, label in map(None, files, labels):
                func, stream_url = stream
                if 'atob' in func:
                    stream_url = base64.b64decode(stream_url)
                stream_url = stream_url.replace(' ', '%20')
                host = scraper_utils.get_direct_hostname(self, stream_url)
                label = re.sub(re.compile('\s*HD', re.I), '', label)
                quality = scraper_utils.height_get_quality(label)
                if Q_ORDER[quality] > Q_ORDER[best_quality]: best_quality = quality
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})
                source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
                sources.append(source)
        return best_quality, sources
        
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/%s' % (urllib.quote(title)))
        html = self._http_get(search_url, cache_limit=8)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'who-likes'})
        if not fragment: return results
        
        fragment = fragment[0].content
        match_url = dom_parser2.parse_dom(fragment, 'a', req='href')
        match_title_year = dom_parser2.parse_dom(fragment, 'img', req='alt')
        if match_url and match_title_year:
            match_url = match_url[0].attrs['href']
            match_title_year = match_title_year[0].attrs['alt']
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results
