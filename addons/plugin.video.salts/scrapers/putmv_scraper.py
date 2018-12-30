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
import urllib
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://putmv.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL
    
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'PutMV'

    def resolve_link(self, link):
        html = self._http_get(link, cache_limit=.5)
        iframe_url = dom_parser2.parse_dom(html, 'iframe', req='src')
        if iframe_url:
            return iframe_url[0].attrs['src']
        else:
            match = re.search('href="([^"]+)[^>]*>Click Here To Play<', html, re.I)
            if match:
                return match.group(1)
            else:
                return link
        
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=2)
        for _attrs, tr in dom_parser2.parse_dom(html, 'tr', {'id': re.compile('link_\d+')}):
            match = dom_parser2.parse_dom(tr, 'a', {'class': 'buttonlink'}, req=['href', 'title'])
            if match:
                stream_url = match[0].attrs['href']
                host = match[0].attrs['title']
                host = re.sub(re.compile('Server\s+', re.I), '', host)
                quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                hosters.append(hoster)
            
        return hosters

    def _get_episode_url(self, season_url, video):
        episode_pattern = 'href="([^"]+)[^>]*>%s<' % (video.episode)
        season_url = scraper_utils.urljoin(self.base_url, season_url)
        html = self._http_get(season_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'episode_show'})
        return self._default_get_episode_url(fragment, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search-movies/%s.html' % urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'movie_about'}):
            match = dom_parser2.parse_dom(item, 'a', req='href')
            if match:
                match_url = match[0].attrs['href']
                match_title_year = match[0].content
                is_season = re.search('Season\s+(\d+)\s*', match_title_year, re.I)
                if (not is_season and video_type == VIDEO_TYPES.MOVIE) or (is_season and video_type == VIDEO_TYPES.SEASON):
                    match_title, match_year = scraper_utils.extra_year(match_title_year)
                    if video_type == VIDEO_TYPES.SEASON:
                        match_year = ''
                        if season and int(season) != int(is_season.group(1)):
                            continue
                                
                    if (not year or not match_year or year == match_year):
                        result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)
        
        return results
