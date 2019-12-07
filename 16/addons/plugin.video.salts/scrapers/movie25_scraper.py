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
import re
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


QUALITY_MAP = {'DVD': QUALITIES.HIGH, 'TS': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}
BASE_URL = 'http://www.movie25.me'

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
        return 'movie25'

    def resolve_link(self, link):
        if self.base_url in link:
            html = self._http_get(link, cache_limit=0)
            for attrs, _content in dom_parser2.parse_dom(html, 'a', req='href'):
                if '/external/' in attrs['href']:
                    return base64.b64decode(attrs['href'].split('/')[-1])
        else:
                return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        quality = None
        match = re.search('Links\s+-\s+Quality\s*([^<]*)</h1>', html, re.DOTALL | re.I)
        if match:
            quality = QUALITY_MAP.get(match.group(1).strip().upper())

        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'links'})
        if not fragment: return hosters
        
        for _attrs, item in dom_parser2.parse_dom(fragment[0].content, 'ul'):
            stream_url = dom_parser2.parse_dom(item, 'a', req='href')
            host = dom_parser2.parse_dom(item, 'li', {'id': 'download'})
            if not stream_url or not host: continue
            
            stream_url = stream_url[0].attrs['href']
            host = host[-1].content
            hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': scraper_utils.get_quality(video, host, quality), 'rating': None, 'views': None, 'direct': False}
            hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/keywords/%s/' % (title))
        html = self._http_get(search_url, cache_limit=4)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'movie_about'}):
            match = dom_parser2.parse_dom(item, 'a', req=['href', 'title'])
            if not match: continue

            match_url, match_title, extra = match[0].attrs['href'], match[0].attrs['title'], match[0].content
            _match_title, match_year = scraper_utils.extra_year(extra)
            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)
        return results
