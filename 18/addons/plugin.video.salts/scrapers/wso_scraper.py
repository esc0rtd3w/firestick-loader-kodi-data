# -*- coding: utf-8 -*-
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
import urlparse
import log_utils  # @UnusedImport
import kodi
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'http://watchseries-online.pl'

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
        return 'wso.ch'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        for _attrs, td in dom_parser2.parse_dom(html, 'td', {'class': 'tdhost'}):
            match = dom_parser2.parse_dom(td, 'a', req='href')
            if match:
                stream_url = match[0].attrs['href']
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
                hosters.append(hoster)
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = '''href=['"]([^"']*([Ss]0*{season}[Ee]0*{episode}|-{season}x{episode}-|-season-{season}-episode-{episode}(?!\d))[^"']*)''' .format(
            season=video.season, episode=video.episode)
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'ul', {'class': 'listEpisodes'})
        return self._default_get_episode_url(fragment or html, video, episode_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        url = scraper_utils.urljoin(self.base_url, '/index')
        html = self._http_get(url, cache_limit=24)
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'ddmcc'}):
            norm_title = scraper_utils.normalize_title(title)
            for attrs, match_title in dom_parser2.parse_dom(fragment, 'a', req='href'):
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(attrs['href']), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results
