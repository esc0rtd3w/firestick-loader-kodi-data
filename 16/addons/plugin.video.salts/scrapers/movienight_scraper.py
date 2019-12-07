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
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


BASE_URL = 'http://movienight.ws'
QUALITY_MAP = {'SD': QUALITIES.HIGH, 'HD': QUALITIES.HD720}

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
        return 'MovieNight'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)

        match = re.search('Quality\s*:\s*([^<]+)', html)
        if match:
            page_quality = QUALITY_MAP.get(match.group(1), QUALITIES.HIGH)
        else:
            page_quality = QUALITIES.HD720

        match = re.search("onClick=\"javascript:replaceb64Text.*?,\s*'([^']+)", html)
        if match:
            html = match.group(1).decode('base-64').replace('&quot;', '"')
                
        iframe_url = dom_parser2.parse_dom(html, 'iframe', req='src')
        if iframe_url:
            iframe_url = iframe_url[0].attrs['src']
            host = urlparse.urlsplit(iframe_url).hostname
            hoster = {'multi-part': False, 'host': host, 'url': iframe_url, 'class': self, 'rating': None, 'views': None, 'quality': scraper_utils.get_quality(video, host, page_quality), 'direct': False}
            hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=4)
        for _attrs, movie in dom_parser2.parse_dom(html, 'div', {'class': 'movie'}):
            match_url = dom_parser2.parse_dom(movie, 'a', req='href')
            match_title_year = dom_parser2.parse_dom(movie, 'img', req='alt')
            if match_url and match_title_year:
                match_url = match_url[0].attrs['href']
                if re.search('season-\d+-episode\d+', match_url): continue
                match_title_year = match_title_year[0].attrs['alt']

                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if not match_year:
                    match_year = dom_parser2.parse_dom(movie, 'div', {'class': 'year'})
                    try: match_year = match_year[0].content
                    except: match_year = ''
                    
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results
