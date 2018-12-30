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
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
import scraper

BASE_URL = 'http://watchitvideos.info'
Q_MAP = {'1080P HD': QUALITIES.HD1080, '720P HD': QUALITIES.HD720, 'HD': QUALITIES.HD720, 'DVD': QUALITIES.HIGH}

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
        return 'WatchItVideos'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        
        best_quality = QUALITIES.HIGH
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'entry'})
        if fragment:
            for match in re.finditer('href="[^"]*/movies-quality/[^"]*[^>]*>([^<]+)', fragment[0].content, re.I):
                quality = Q_MAP.get(match.group(1).upper(), QUALITIES.HIGH)
                if Q_ORDER[quality] > Q_ORDER[best_quality]:
                    best_quality = quality
                    
        sources = []
        for attrs, _content in dom_parser2.parse_dom(html, 'a', req='data-vid'):
            try:
                vid_url = dom_parser2.parse_dom(scraper_utils.cleanse_title(attrs['data-vid']), 'iframe', req='src')
                sources.append(vid_url[0])
            except:
                pass
            
        fragment = dom_parser2.parse_dom(html, 'table', {'class': 'additional-links'})
        if fragment:
            sources += dom_parser2.parse_dom(fragment[0].content, 'a', req='href')
                
        for stream_url in sources:
            stream_url = stream_url.attrs.get('href') or stream_url.attrs.get('src')
            host = urlparse.urlparse(stream_url).hostname
            quality = scraper_utils.get_quality(video, host, best_quality)
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
            hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'article', {'class': 'item-list'}):
            match = dom_parser2.parse_dom(item, 'a', req='href')
            if not match: continue
            match_title_year = match[0].content
            match_url = match[0].attrs['href']
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)
        return results
