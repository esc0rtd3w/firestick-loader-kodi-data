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
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper


BASE_URL = 'http://www.movie-tube.co'
QUALITY_MAP = {'CAMRIP': QUALITIES.MEDIUM, 'HD': QUALITIES.HD720, '720 BLURAY': QUALITIES.HD720}

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
        return 'MovieTube'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        for _attrs, item in dom_parser2.parse_dom(html, 'li'):
            label = dom_parser2.parse_dom(item, 'span', {'class': 'type'})
            value = dom_parser2.parse_dom(item, 'p', {'class': 'text'})
            if label and value and 'quality' in label[0].content.lower():
                q_str = value[0].content.upper()
                break
        else:
            q_str = ''
        
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'fstory-video'})
        if not fragment: return hosters
        
        for match in re.finditer('<iframe[^>]*src="([^"]+)', fragment[0].content, re.I):
            stream_url = match.group(1)
            host = urlparse.urlparse(stream_url).hostname
            quality = scraper_utils.get_quality(video, host, QUALITY_MAP.get(q_str, QUALITIES.HIGH))
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
            hosters.append(hoster)
            
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/index.php')
        data = {'subaction': 'search', 'story': title, 'do': 'search'}
        headers = {'Referer': search_url}
        html = self._http_get(search_url, params={'do': 'search'}, data=data, headers=headers, cache_limit=1)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'dle-content'})
        if not fragment: return results
        
        for _attrs, item in dom_parser2.parse_dom(fragment[0].content, 'div', {'class': 'short-film'}):
            match = re.search('<h5><a\s+href="([^"]+)[^>]+title="([^"]+)', item)
            if not match: continue
            
            url, match_title = match.groups('')
            result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
            results.append(result)
        
        return results
