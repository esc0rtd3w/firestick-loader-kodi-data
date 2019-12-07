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
import scraper

BASE_URL = 'http://project-free-tv.li'

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
        return 'pftv'

    def resolve_link(self, link):
        if not link.startswith('http'):
            url = scraper_utils.urljoin(self.base_url, link)
            html = self._http_get(url, cache_limit=.5)
            match = re.search('href="([^"]+).*?value="Continue to video"', html)
            if match:
                url = scraper_utils.urljoin(self.base_url, match.group(1))
                html = self._http_get(url, cache_limit=.5)
                redirect = dom_parser2.parse_dom(html, 'meta', {'http-equiv': 'refresh'}, req='content')
                if redirect:
                    match = re.search('url=([^"]+)', redirect[0].attrs['content'])
                    if match: return match.group(1)

        return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        for match in re.finditer('<td>\s*<a\s+href="([^"]+)(?:[^>]+>){2}\s*(?:&nbsp;)*\s*([^<]+)', html):
            stream_url, host = match.groups()
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
            hosters.append(hoster)

        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+season-%s-episode-%s/)' % (video.season, video.episode)
        airdate_pattern = '{day} {short_month} {year}\s*<a\s+href="([^"]+)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'table', {'class': 'alternate_color'})
        return self._default_get_episode_url(fragment or html, video, episode_pattern, airdate_pattern=airdate_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        norm_title = scraper_utils.normalize_title(title)
        url = scraper_utils.urljoin(self.base_url, '/watch-series/')
        headers = {'Referer': self.base_url}
        html = self._http_get(url, headers=headers, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'li'):
            for attrs, _content in dom_parser2.parse_dom(item, 'a', req=['title', 'href']):
                match_title, match_url = attrs['title'], attrs['href']
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results
