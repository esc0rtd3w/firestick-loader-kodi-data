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

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'http://geektv.ma'

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
        return 'Watch8Now'

    def resolve_link(self, link):
        html = self._http_get(link, cache_limit=.5)
        match = dom_parser2.parse_dom(html, 'iframe', req='src')
        if match:
            return match[0].attrs['src']
        else:
            match = re.search('Nothing in HERE<br>([^<]+)', html, re.I)
            if match:
                return match.group(1).strip()
        
        return link

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        fragment = dom_parser2.parse_dom(html, 'tbody')
        if fragment:
            fragment = fragment[0].content
            for attrs, content in dom_parser2.parse_dom(fragment, 'a', req='href'):
                stream_url = attrs['href']
                match = dom_parser2.parse_dom(content, 'img')
                if not match: continue
                host = match[0].content.strip()
                quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                hosters.append(hoster)

        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+[sS]%s-?[eE]%s(?!\d)[^"]*)"' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+)(?:[^>]*>){3}\s*S\d+\s+Episode\s+\d+\s*:\s*(?P<title>[^<]+)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'accordion'})
        return self._default_get_episode_url(fragment, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        search_url = scraper_utils.urljoin(self.base_url, '/search')
        html = self._http_get(search_url, params={'q': title}, cache_limit=8)
        results = []
        for _attrs, item in dom_parser2.parse_dom(html, 'td', {'class': 'col-md-10'}):
            match = dom_parser2.parse_dom(item, 'a', req='href')
            if match:
                match_url, match_title = match[0].attrs['href'], match[0].content
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                results.append(result)

        return results
