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
import log_utils  # @UnusedImport
import kodi
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://netflix-putlocker.com'
QUALITY_MAP = {'DVD': QUALITIES.HIGH, 'TS': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}

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
        return 'MovieHut'

    def format_source_label(self, item):
        label = super(self.__class__, self).format_source_label(item)
        if 'part_label' in item:
            label += ' (%s)' % (item['part_label'])
        return label

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        pattern = 'href="([^"]+)">Watch (Link \d+)(.*?)</td>\s*<td[^>]*>(.*?)</td>.*?<td[^>]*id="lv_\d+"[^>]*>([^<]+)'
        for match in re.finditer(pattern, html, re.DOTALL):
            stream_url, label, part_str, q_str, views = match.groups()
            q_str = q_str.strip().upper()
            parts = re.findall('href="([^"]+)">(Part\s+\d+)<', part_str, re.DOTALL)
            if parts:
                multipart = True
            else:
                multipart = False
            host = urlparse.urlparse(stream_url).hostname
            if host is None: continue
            
            quality = scraper_utils.get_quality(video, host, QUALITY_MAP.get(q_str, QUALITIES.HIGH))
            hoster = {'multi-part': multipart, 'host': host, 'class': self, 'quality': quality, 'views': views, 'rating': None, 'url': stream_url, 'direct': False}
            hoster['extra'] = label
            hosters.append(hoster)
            for part in parts:
                stream_url, part_label = part
                part_hoster = hoster.copy()
                part_hoster['part_label'] = part_label
                part_hoster['url'] = stream_url
                hosters.append(part_hoster)
            
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/bestmatch-fund-movies-%s.html')
        search_title = title.replace(' ', '-')
        search_title = re.sub('[^A-Za-z0-9-]', '', search_title).lower()
        search_url = search_url % (search_title)
        html = self._http_get(search_url, cache_limit=1)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'thumbsTitle'}):
            match = dom_parser2.parse_dom(item, 'a', req='href')
            if not match: continue

            match_url, match_title_year = match[0].attrs['href'], match[0].content
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if (not year or not match_year or year == match_year):
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)
        
        return results
