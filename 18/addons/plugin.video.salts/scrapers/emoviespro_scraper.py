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
import scraper


BASE_URL = 'http://emovies.is'

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
        return 'eMovies.Pro'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        q_str = 'HDRIP'
        match = re.search('>Quality(.*?)<br\s*/?>', html, re.I)
        if match:
            q_str = match.group(1)
            q_str = re.sub('(</?strong[^>]*>|:|\s)', '', q_str, re.I | re.U)

        for _attr, content in dom_parser2.parse_dom(html, 'div', {'class': 'tab_content'}):
            for attrs, _content in dom_parser2.parse_dom(content, 'iframe', req='src'):
                source = attrs['src']
                host = urlparse.urlparse(source).hostname
                quality = scraper_utils.blog_get_quality(video, q_str, host)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': False}
                match = re.search('class="views-infos">(\d+).*?class="rating">(\d+)%', html, re.DOTALL)
                if not match: continue
                
                hoster['views'] = int(match.group(1))
                hoster['rating'] = match.group(2)
            
            hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        slug = scraper_utils.to_slug(title)
        test_url = scraper_utils.urljoin(self.base_url, slug)
        test_url += '-%s' % (year)
        html = self._http_get(test_url, cache_limit=8)
        if html:
            result = {'title': scraper_utils.cleanse_title(title), 'year': year, 'url': scraper_utils.pathify_url(test_url)}
            results.append(result)
        return results
