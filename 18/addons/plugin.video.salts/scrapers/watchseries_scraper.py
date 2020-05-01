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
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
import scraper

BASE_URL = 'https://watchseriesfree.to'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'WatchSeries'

    def resolve_link(self, link):
        if not link.startswith('http'):
            url = scraper_utils.urljoin(self.base_url, link)
            html = self._http_get(url, cache_limit=0)
            for attrs, content in dom_parser2.parse_dom(html, 'a', req='href'):
                if re.search('Click Here To Play', content, re.I):
                    return attrs['href']
        else:
            return link
    
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        headers = {'Refer': self.base_url}
        html = self._http_get(page_url, headers=headers, cache_limit=.5)
        for _attrs, table in dom_parser2.parse_dom(html, 'table', {'class': 'W'}):
            for _attrs, row in dom_parser2.parse_dom(table, 'tr'):
                td = dom_parser2.parse_dom(row, 'td')
                stream_url = dom_parser2.parse_dom(row, 'a', req='href')
                if not td or not stream_url: continue
                
                host = td[0].content
                host = re.sub('<!--.*?-->', '', host)
                host = re.sub('<([^\s]+)[^>]*>.*?</\\1>', '', host)
                host = host.strip()
                stream_url = stream_url[0].attrs['href']
                quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                hosters.append(hoster)
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]*s0*%s_e0*%s(?!\d)[^"]*)' % (video.season, video.episode)
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'seasons-grid'})
        return self._default_get_episode_url(fragment, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/suggest.php')
        headers = {'Referer': self.base_url}
        headers.update(XHR)
        params = {'ajax': 1, 's': title, 'type': 'TVShows'}
        html = self._http_get(search_url, params=params, cache_limit=8)
        for attrs, match_title in dom_parser2.parse_dom(html, 'a', req='href'):
            match_url = attrs['href']
            match_title = re.sub('</?[^>]*>', '', match_title)
            match = re.search('\((\d{4})\)$', match_url)
            if match:
                match_year = match.group(1)
            else:
                match_year = ''

            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)

        return results
