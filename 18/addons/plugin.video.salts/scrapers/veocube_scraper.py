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
import scraper
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://veocube.cf'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'VeoCube'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=8)
        hosters += self.__get_sources(html, url)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'parts-middle'})
        if fragment:
            for attrs, _content in dom_parser2.parse_dom(fragment[0].content, 'a', req='href'):
                url = scraper_utils.urljoin(self.base_url, attrs['href'])
                html = self._http_get(url, cache_limit=8)
                hosters += self.__get_sources(html, url)

        return hosters

    def __get_sources(self, html, page_url):
        sources = []
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'video-content'})
        if fragment:
            referer = page_url
            iframes = dom_parser2.parse_dom(fragment[0].content, 'iframe', req='src')
            for attrs, _content in iframes:
                iframe_url = attrs['src']
                if self.base_url in iframe_url:
                    headers = {'Referer': referer}
                    html = self._http_get(iframe_url, headers=headers, cache_limit=.5)
                    referer = iframe_url
                    links = scraper_utils.parse_sources_list(self, html)
                    if links:
                        for link, values in links.iteritems():
                            host = scraper_utils.get_direct_hostname(self, link)
                            if host == 'gvideo':
                                quality = scraper_utils.gv_get_quality(link)
                            else:
                                quality = values['quality']
                            source = {'multi-part': False, 'url': link, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
                            sources.append(source)
                    else:
                        iframes += dom_parser2.parse_dom(html, 'iframe', req='src')
                else:
                    host = urlparse.urlparse(iframe_url).hostname
                    source = {'multi-part': False, 'url': iframe_url, 'host': host, 'class': self, 'quality': QUALITIES.HIGH, 'views': None, 'rating': None, 'direct': False}
                    sources.append(source)
        return sources
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'movie-details'}):
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_title = dom_parser2.parse_dom(item, 'a')
            match_year = dom_parser2.parse_dom(item, 'span', {'class': 'movie-release'})
            if match_url and match_title:
                match_url = match_url[0].attrs['href']
                match_title = match_title[0].content
                if match_year:
                    match_year = match_year[0].content.strip()
                else:
                    match_year = ''
                    
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
