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
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://www.watchseries-online.me'

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
        return 'SeriesCoco'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        for _attrs, comment in dom_parser2.parse_dom(html, 'div', {'class': 'commentmetadata'}):
            for attrs, _content in dom_parser2.parse_dom(comment, 'a', req='href'):
                stream_url = attrs['href']
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                hosters.append(hoster)
    
        return hosters

    def _get_episode_url(self, show_url, video):
        pages = [show_url] + self.__get_pages(show_url)
        for page in pages:
            ep_url = self.__find_episode(page, video)
            if ep_url: return ep_url
                        
    def __get_pages(self, url):
        url = scraper_utils.urljoin(self.base_url, url)
        html = self._http_get(url, cache_limit=2)
        pages = [scraper_utils.pathify_url(attrs['href']) for attrs, _content in dom_parser2.parse_dom(html, 'a', {'class': 'page-numbers'}, req='href')]
        return pages
    
    def __find_episode(self, page, video):
        url = scraper_utils.urljoin(self.base_url, page)
        html = self._http_get(url, cache_limit=2)
        for _attrs, article in dom_parser2.parse_dom(html, 'article', {'id': re.compile('post-\d+')}):
            match = re.search('href="([^"]+-s%02d-e%02d[/-][^"]*)' % (int(video.season), int(video.episode)), article, re.I)
            if match:
                return scraper_utils.pathify_url(match.group(1))
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        fragment = dom_parser2.parse_dom(html, 'select', {'id': 'cat'})
        if fragment:
            for attrs, label in dom_parser2.parse_dom(fragment[0].content, 'option', {'class': 'level-0'}, req='value'):
                label = scraper_utils.cleanse_title(label)
                label = re.sub('\s+\(\d+\)$', '', label)
                if norm_title in scraper_utils.normalize_title(label):
                    cat_url = scraper_utils.urljoin(self.base_url, '/?cat=%s' % (attrs['value']))
                    html = self._http_get(cat_url, allow_redirect=False, cache_limit=8)
                    if html.startswith('http'):
                        cat_url = html
                    result = {'url': scraper_utils.pathify_url(cat_url), 'title': label, 'year': ''}
                    results.append(result)

        return results
