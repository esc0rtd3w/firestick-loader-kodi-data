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
import urllib
import re
import scraper
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://www.movieblast.co'
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
        return 'MovieBlast'

    def resolve_link(self, link):
        if self.base_url in link:
            html = self._http_get(link, allow_redirect=False, cache_limit=.25)
            if html.startswith('http'):
                return html
        else:
            return link
    
    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=8)
        for _attrs, row in dom_parser2.parse_dom(html, 'tr', {'class': 'streaming-link'}):
            match = re.search("nowPlaying\(\s*\d+\s*,\s*'([^']+)'\s*,\s*'([^']+)", row)
            if not match: continue
            
            host, stream_url = match.groups()
            if re.search('server\s*\d+', host, re.I):
                for source, value in self.__get_direct_links(stream_url).iteritems():
                    host = scraper_utils.get_direct_hostname(self, source)
                    source = {'multi-part': False, 'url': source, 'host': host, 'class': self, 'quality': value['quality'], 'views': None, 'rating': None, 'direct': True}
                    hosters.append(source)
            else:
                source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': QUALITIES.HIGH, 'views': None, 'rating': None, 'direct': False}
                hosters.append(source)

        return hosters

    def __get_direct_links(self, stream_url):
        return scraper_utils.parse_sources_list(self, self._http_get(stream_url, cache_limit=1))
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/%s/' % (urllib.quote(title)))
        html = self._http_get(search_url, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'item'}):
            match_title = dom_parser2.parse_dom(item, 'span')
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            if match_url and match_title:
                match_url = match_url[0].attrs['href']
                match_title = match_title[0].content
                match_year = re.search('(\d{4})$', match_url)
                match_year = match_year.group(1) if match_year else ''
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
