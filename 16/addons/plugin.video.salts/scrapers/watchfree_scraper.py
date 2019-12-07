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
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

QUALITY_MAP = {'HD': QUALITIES.HIGH, 'LOW': QUALITIES.LOW}
BASE_URL = 'http://www.watchfree.to'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'WatchFree.to'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        pattern = 'href="[^"]+gtfo=([^&"]+)[^>]+>([^<]+)'
        for match in re.finditer(pattern, html, re.DOTALL | re.I):
            url, link_name = match.groups()
            url = url.decode('base-64')
            host = urlparse.urlsplit(url).hostname
            match = re.search('Part\s+(\d+)', link_name)
            if match:
                if match.group(1) == '2':
                    del hosters[-1]  # remove Part 1 previous link added
                continue
            
            source = {'multi-part': False, 'url': url, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'views': None, 'rating': None, 'direct': False}
            hosters.append(source)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        if video_type == VIDEO_TYPES.MOVIE:
            section = '1'
            url_marker = '-movie-online-'
        else:
            section = '2'
            url_marker = '-tv-show-online-'
        params = {'keyword': title, 'search_section': section}
        html = self._http_get(self.base_url, params=params, cache_limit=1)

        for match in re.finditer('class="item".*?href="([^"]+)"\s*title="Watch (.*?)(?:\s+\((\d{4})\))?"', html):
            url, res_title, res_year = match.groups('')
            if url_marker in url and (not year or not res_year or year == res_year):
                result = {'title': scraper_utils.cleanse_title(res_title), 'url': scraper_utils.pathify_url(url), 'year': res_year}
                results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = '"href="([^"]+/season-%s-episode-%s(?!\d))' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+).*?class="tv_episode_name">\s+-\s+(?P<title>[^<]+)'
        airdate_pattern = 'href="([^"]+)(?:[^<]+<){5}span\s+class="tv_num_versions">{month_name} {day} {year}'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'data-id': video.season, 'class': 'show_season'})
        return self._default_get_episode_url(fragment, video, episode_pattern, title_pattern, airdate_pattern)
