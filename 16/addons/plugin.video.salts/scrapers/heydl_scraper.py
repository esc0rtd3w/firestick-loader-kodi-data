# -*- coding: utf-8 -*-
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
import kodi
import dom_parser2
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://heydl.com'
MOVIE_URL = 'http://dl2.heydl.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.row_pattern = '<td>\s*<a\s+href="(?P<link>[^"]+)">(?P<title>[^<]+)</a></td>\s*<td>\s*(?P<size>.*?)</td><td>(?P<date>.*?)</td>'

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'HeyDL'

    def resolve_link(self, link):
        if link.startswith('http'):
            return link
        else:
            return MOVIE_URL + link
    
    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=8)
        for attrs, _content in dom_parser2.parse_dom(html, 'a', req='href'):
            stream_url = attrs['href']
            if MOVIE_URL in stream_url:
                meta = scraper_utils.parse_movie_link(stream_url)
                stream_url = scraper_utils.pathify_url(stream_url) + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                quality = scraper_utils.height_get_quality(meta['height'])
                hoster = {'multi-part': False, 'host': scraper_utils.get_direct_hostname(self, stream_url), 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                if 'format' in meta: hoster['format'] = meta['format']
                hosters.append(hoster)
                
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'h2'):
            for attrs, match_title_year in dom_parser2.parse_dom(item, 'a', req=['href']):
                match_url = attrs['href']
                match_title_year = re.sub('[^\x00-\x7F]', '', match_title_year)
                match = re.search('(.*?)\s+(\d{4})$', match_title_year)
                if match:
                    match_title, match_year = match.groups()
                else:
                    match = re.search('-(\d{4})/?$', match_url)
                    if match:
                        match_year = match.groups(1)
                    else:
                        match_title, match_year = match_title_year, ''
                        
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
        
        return results
