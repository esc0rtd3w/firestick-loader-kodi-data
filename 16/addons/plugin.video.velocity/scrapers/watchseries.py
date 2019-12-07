"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris
    Altered by Blazetamer for Velocity

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
from libs import kodi
from libs import dom_parser
import scraper_utils
from libs.constants import FORCE_NO_MATCH
from libs.constants import QUALITIES
from libs.constants import VIDEO_TYPES
from libs.constants import XHR
import main_scrape
import scrapeit

def __enum(**enums):
    return type('Enum', (), enums)


FORCE_NO_MATCH = '***FORCE_NO_MATCH***'
QUALITIES = __enum(LOW='Low', MEDIUM='Medium', HIGH='High', HD720='HD720', HD1080='HD1080')
VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')


BASE_URL = 'https://watchseriesfree.to'

class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
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
            url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(url, cache_limit=0)
            stream_url = dom_parser.parse_dom(html, 'a', {'class': 'myButton p2'}, ret='href')
            if stream_url: return stream_url[0]
        else:
            return link
    
    def get_sources(self, video, video_type):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            headers = {'Refer': self.base_url}
            html = self._http_get(page_url, headers=headers, cache_limit=.5)
            table = dom_parser.parse_dom(html, 'div', {'class': 'linktable'})
            if table:
                for row in dom_parser.parse_dom(table[0], 'tr'):
                    spans = dom_parser.parse_dom(row, 'span')
                    stream_url = dom_parser.parse_dom(row, 'a', ret='href')
                    is_sponsored = any([i for i in spans if 'sponsored' in i.lower()])
                    if not is_sponsored and len(spans) > 1 and stream_url:
                        host, rating = spans[0], spans[1]
                        stream_url = stream_url[0]
                        quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                        hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                        if 'rating'.endswith('%') and rating[:-1].isdigit():
                            hoster['rating'] = rating[:-1]
                        hosters.append(hoster)
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]*s%s_e%s(?!\d)[^"]*)' % (video.season, video.episode)
        return self._default_get_episode_url(show_url, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/'+title)
        #search_url = urlparse.urljoin(self.base_url, '/suggest.php')
        headers = {'Referer': self.base_url}
        headers.update(XHR)
        params = {'ajax': 1, 's': title, 'type': 'TVShows'}
        html = self._http_get(search_url, params=params, cache_limit=8)
        kodi.log(html)
        for match in re.finditer('href="([^"]+)[^>]*>(.*?)</a>', html):
            match_url, match_title = match.groups()
            match_title = re.sub('</?span[^>]*>', '', match_title)
            match = re.search('\((\d{4})\)$', match_url)
            if match:
                match_year = match.group(1)
            else:
                match_year = ''

            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)

        return results
