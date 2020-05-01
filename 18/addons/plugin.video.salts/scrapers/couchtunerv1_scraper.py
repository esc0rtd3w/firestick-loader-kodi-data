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
import log_utils  # @UnusedImport
import kodi
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://www.couch-tuner.ag'
BASE_URL2 = 'http://couchtuner.city'

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
        return 'CouchTunerV1'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        entry = ''
        while True:
            html = self._http_get(url, cache_limit=.5)
            if not html:
                url = scraper_utils.urljoin(BASE_URL2, source_url)
                html = self._http_get(url, cache_limit=.5)
                
            entry = dom_parser2.parse_dom(html, 'div', {'class': 'entry'})
            if entry:
                entry = entry[0].content
                match = re.search('Watch it here\s*:.*?href="([^"]+)', entry, re.I)
                if not match: break
                url = match.group(1)
            else:
                entry = ''
                break

        for _attribs, tab in dom_parser2.parse_dom(entry, 'div', {'class': 'postTabs_divs'}):
            match = dom_parser2.parse_dom(tab, 'iframe', req='src')
            if not match: continue
            link = match[0].attrs['src']
            host = urlparse.urlparse(link).hostname
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'views': None, 'rating': None, 'url': link, 'direct': False}
            hosters.append(hoster)

        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+[sS](?:eason-)?%s-[eE](?:pisode-)?%s-[^"]+)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+).*?</a>:?\s*(?P<title>[^<]+)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'entry'})
        return self._default_get_episode_url(fragment, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        show_list_url = scraper_utils.urljoin(self.base_url, '/tv-lists/')
        html = self._http_get(show_list_url, cache_limit=8)
        results = []
        seen_urls = set()
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(html, 'li'):
            match = dom_parser2.parse_dom(item, 'a', req='href')
            if match:
                match_url = scraper_utils.pathify_url(match[0].attrs['href'])
                match_title = match[0].content
                if match_url in seen_urls: continue
                seen_urls.add(match_url)
                match_title = re.sub('</?strong[^>]*>', '', match_title)
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': match_url, 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results
