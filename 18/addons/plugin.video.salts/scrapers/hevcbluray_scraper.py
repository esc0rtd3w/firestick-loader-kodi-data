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

BASE_URL = 'http://www.300mbmoviesdl.com'
QUALITY_MAP = {'HD 720P': QUALITIES.HD720, 'HD 1080P': QUALITIES.HD1080, '1080P BLURAY': QUALITIES.HD1080}

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
        return 'HEVCBluRay'

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if not source_url or source_url == FORCE_NO_MATCH: return sources
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        is_3d = False
        page_quality = QUALITIES.HD720
        title = dom_parser2.parse_dom(html, 'title')
        if title:
            title = title[0].content
            match = re.search('(\d{3,})p', title)
            if match:
                page_quality = scraper_utils.height_get_quality(match.group(1))
            
            is_3d = True if re.search('\s+3D\s+', title) else False
        
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'entry'})
        if fragment:
            for _attrs, item in dom_parser2.parse_dom(fragment[0].content, 'h3'):
                for attrs, _content in dom_parser2.parse_dom(item, 'a', req='href'):
                    stream_url = attrs['href']
                    host = urlparse.urlparse(stream_url).hostname
                    source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': page_quality, 'views': None, 'rating': None, 'direct': False}
                    source['format'] = 'x265'
                    source['3D'] = is_3d
                    sources.append(source)
                    
        return sources

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'cover'}):
            match = dom_parser2.parse_dom(item, 'a', req=['href', 'title'])
            if not match: continue
            
            match_url, match_title_year = match[0].attrs['href'], match[0].attrs['title']
            if re.search('S\d+E\d+', match_title_year, re.I): continue
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if not match_year:
                match = re.search('-(\d{4})-', match_url)
                if match:
                    match_year = match.group(1)
                    
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results
