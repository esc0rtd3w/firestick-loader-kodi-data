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
import re
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://cinemamkv.xyz'
QUALITY_MAP = {'HD 720P': QUALITIES.HD720, 'HD 1080P': QUALITIES.HD1080}

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
        return 'CinemaMKV'

    def get_sources(self, video):
        sources = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return sources
        
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, require_debrid=True, cache_limit=8)
        for div in dom_parser2.parse_dom(html, 'div', {'id': re.compile('stb-container-\d+')}):
            stream_url = dom_parser2.parse_dom(div.content, 'iframe', req='src')
            if not stream_url: continue
            stream_url = stream_url[0].attrs['src']
            host = urlparse.urlparse(stream_url).hostname
            source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': QUALITIES.HIGH, 'views': None, 'rating': None, 'direct': False}
            sources.append(source)
                
        fragment = dom_parser2.parse_dom(html, 'div', {'class': "stb-download-body_box"})
        if not fragment: return sources
        
        labels = dom_parser2.parse_dom(fragment[0].content, 'a', {'href': '#'})
        stream_urls = [result for result in dom_parser2.parse_dom(fragment[0].content, 'a', req='href') if result.content.lower() == 'download now']
        for label, stream_url in zip(labels, stream_urls):
            stream_url = stream_url.attrs['href']
            label = re.sub('</?[^>]*>', '', label.content)
            host = urlparse.urlparse(stream_url).hostname
            quality = scraper_utils.blog_get_quality(video, label, host)
            source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
            sources.append(source)

        return sources

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, require_debrid=True, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'post'}):
            match = dom_parser2.parse_dom(item, 'a', req='href')
            if not match: continue

            match_url, match_title_year = match[0].attrs['href'], match[0].content
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results
