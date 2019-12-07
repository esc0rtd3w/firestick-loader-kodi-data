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
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://movie4k.to'
QUALITY_MAP = {None: None, '0': QUALITIES.LOW, '1': QUALITIES.LOW, '2': QUALITIES.MEDIUM, '3': QUALITIES.MEDIUM, '4': QUALITIES.HIGH, '5': QUALITIES.HIGH}

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
        return 'Movie4K'

    def resolve_link(self, link):
        url = scraper_utils.urljoin(self.base_url, link)
        html = self._http_get(url, cache_limit=0)
        match = re.search('href="([^"]+).*?src="/img/click_link.jpg"', html)
        if match:
            return match.group(1)

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        pattern = '''tablemoviesindex2.*?href\s*=\s*['"]([^'"]+).*?&nbsp;([^<]+)'''
        for match in re.finditer(pattern, html):
            url, host = match.groups()
            if not url.startswith('/'): url = '/' + url
            quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': url, 'direct': False}
            hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/movies.php')
        cookies = {'onlylanguage': 'en', 'lang': 'en'}
        params = {'list': 'search', 'search': title}
        html = self._http_get(search_url, params=params, cookies=cookies, cache_limit=8)
        for _attrs, content in dom_parser2.parse_dom(html, 'TR', {'id': re.compile('coverPreview\d+')}):
            match = dom_parser2.parse_dom(content, 'a', req='href')
            if not match: continue
            
            match_url, match_title = match[0].attrs['href'], match[0].content
            is_show = re.search('\(tvshow\)', match_title, re.I)
            if (video_type == VIDEO_TYPES.MOVIE and is_show) or (video_type == VIDEO_TYPES.TVSHOW and not is_show):
                continue

            match_title = match_title.replace('(TVshow)', '')
            match_title = match_title.strip()
            
            match_year = ''
            for _attrs, div in dom_parser2.parse_dom(content, 'div'):
                match = re.match('\s*(\d{4})\s*', div)
                if match:
                    match_year = match.group(1)

            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        if not scraper_utils.force_title(video):
            url = scraper_utils.urljoin(self.base_url, show_url)
            html = self._http_get(url, cache_limit=2)
            season_div = 'episodediv%s' % (video.season)
            fragment = dom_parser2.parse_dom(html, 'div', {'id': season_div})
            if not fragment: return

            pattern = 'value="([^"]+)[^>]*>Episode %s\s*<' % (video.episode)
            match = re.search(pattern, fragment[0].content, re.I)
            if not match: return
            
            return scraper_utils.pathify_url(match.group(1))
