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
import scraper
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib import jsunpack
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://vebup.com'
Q_MAP = {'HD': QUALITIES.HD720, 'DVD': QUALITIES.HIGH, 'CAM': QUALITIES.LOW}

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
        return 'Vebup'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=8)
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'movieplay'}):
            iframe_src = dom_parser2.parse_dom(fragment, 'iframe', req='src')
            if iframe_src:
                iframe_src = iframe_src[0].attrs['src']
                if re.search('o(pen)?load', iframe_src, re.I):
                    meta = scraper_utils.parse_movie_link(iframe_src)
                    quality = scraper_utils.height_get_quality(meta['height'])
                    links = {iframe_src: {'quality': quality, 'direct': False}}
                else:
                    links = self.__get_links(iframe_src, url)

                for link in links:
                    direct = links[link]['direct']
                    quality = links[link]['quality']
                    if direct:
                        host = scraper_utils.get_direct_hostname(self, link)
                        if host == 'gvideo':
                            quality = scraper_utils.gv_get_quality(link)
                        stream_url = link + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': url})
                    else:
                        host = urlparse.urlparse(link).hostname
                        stream_url = link
                        
                    source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                    hosters.append(source)

        return hosters

    def __get_links(self, iframe_src, page_url):
        sources = {}
        headers = {'Referer': page_url}
        html = self._http_get(iframe_src, headers=headers, cache_limit=1)
        for match in re.finditer('(eval\(function\(.*?)</script>', html, re.DOTALL):
            js_data = jsunpack.unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            sources = scraper_utils.parse_sources_list(self, js_data)
        return sources
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'item'}):
            match_title = dom_parser2.parse_dom(item, 'span', {'class': 'tt'})
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_year = dom_parser2.parse_dom(item, 'span', {'class': 'year'})
            if match_url and match_title:
                match_url = match_url[0].attrs['href']
                match_title = match_title[0].content
                match_year = match_year[0].content if match_year else ''
                    
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
