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
import re
import urlparse
import copy
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://stream-tv2.ag'
DEF_EP_URL = 'http://stream-tv-series.net'

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
        return 'stream-tv.co'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        base_ep_url = self.__get_base_ep_url(video)
        url = scraper_utils.urljoin(base_ep_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        for match in re.finditer('postTabs_titles.*?iframe.*?src="([^"]+)', html, re.I | re.DOTALL):
            stream_url = match.group(1)
            host = urlparse.urlparse(stream_url).hostname
            hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': scraper_utils.get_quality(video, host, None), 'views': None, 'rating': None, 'direct': False}
            hosters.append(hoster)

        return hosters

    def __get_base_ep_url(self, video):
        temp_video = copy.copy(video)
        temp_video.video_type = VIDEO_TYPES.TVSHOW
        url = scraper_utils.urljoin(self.base_url, self.get_url(temp_video))
        html = self._http_get(url, cache_limit=8)
        match = re.search('href="([^"]+[sS]\d+-?[eE]\d+[^"]+)', html)
        if match:
            return match.group(1)
        else:
            return DEF_EP_URL
        
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+s0*%s-?e0*%s[^"]+)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+-s\d+-?e\d+-(?P<title>[^/"]*)[^"]*)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'entry'})
        return self._default_get_episode_url(fragment or html, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, cache_limit=8)
        norm_title = scraper_utils.normalize_title(title)
        pattern = 'li><a\s+href="([^"]+)">([^<]+)'
        for match in re.finditer(pattern, html):
            url, match_title = match.groups()
            if norm_title in scraper_utils.normalize_title(match_title):
                match_title = match_title.replace(' – ', '')
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                results.append(result)

        return results
