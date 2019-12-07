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
from libs import kodi

from libs import dom_parser
import scraper_utils
from libs.constants import FORCE_NO_MATCH
from libs.constants import VIDEO_TYPES
from libs.constants import QUALITIES
import scrapeit
import main_scrape


XHR = {'X-Requested-With': 'XMLHttpRequest'}
BASE_URL = 'http://www.watchepisodes.com'

class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('watchepi_base_url')

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'WatchEpisodes'

    def get_sources(self, video, video_type):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            for link in dom_parser.parse_dom(html, 'div', {'class': '[^"]*ldr-item[^"]*'}):
                stream_url = dom_parser.parse_dom(link, 'a', ret='data-actuallink')
                
                views = None
                watched = dom_parser.parse_dom(link, 'div', {'class': 'click-count'})
                if watched:
                    match = re.search(' (\d+) ', watched[0])
                    if match:
                        views = match.group(1)
                        
                score = dom_parser.parse_dom(link, 'div', {'class': '\s*point\s*'})
                if score:
                    score = int(score[0])
                    rating = score * 10 if score else None
                
                if stream_url:
                    stream_url = stream_url[0].strip()
                    host = urlparse.urlparse(stream_url).hostname
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    #source = {'hostname': 'IceFilms', 'multi-part': False, 'quality': quality, 'class': '','version': label,'rating': None, 'views': None, 'direct': False}
                    hoster = {'hostname': 'WatchEpisodes','multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': views, 'rating': rating, 'url': stream_url, 'direct': False}
                    hosters.append(hoster)
        main_scrape.apply_urlresolver(hosters)
        return hosters

    def _get_episode_url(self, show_url, video):
    #def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=2)
        if html:
            episodes = dom_parser.parse_dom(html, 'div', {'class': '\s*el-item\s*'})
            episode_pattern = 'href="([^"]*-[sS]%02d[eE]%02d(?!\d)[^"]*)' % (int(video.season), int(video.episode))
            match = re.search(episode_pattern, html)
            if match:
                return scraper_utils.pathify_url(match.group(1))

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search/ajax_search')
        html = self._http_get(search_url, params={'q': title}, headers=XHR, cache_limit=1)
        js_result = scraper_utils.parse_json(html, search_url)
        match_year = ''
        if 'series' in js_result:
            for series in js_result['series']:
                if 'seo' in series and 'label' in series:
                    if not year or not match_year or year == match_year:
                        result = {'url': scraper_utils.pathify_url('/' + series['seo']), 'title': scraper_utils.cleanse_title(series['label']), 'year': match_year}
                        results.append(result)

        return results
