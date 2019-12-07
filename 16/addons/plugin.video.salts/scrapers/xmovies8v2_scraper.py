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
import time
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import XHR
import scraper

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'https://xmovies8.ru'
PLAYER_URL = '/ajax/movie/load_player_v3'

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
        return 'xmovies8.v2'

    def get_sources(self, video):
        hosters = []
        sources = {}
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        match = re.search("load_player\('([^']+)", html)
        if not match: return hosters
        
        headers = {'Referer': page_url, 'Server': 'cloudflare-nginx', 'Accept': 'text/html, */*; q=0.01',
                   'Accept-Language': 'en-US,en;q=0.5', 'Accept-Formating': 'application/json, text/javascript', 'Accept-Encoding': 'gzip, deflate'}
        headers.update(XHR)
        params = {'id': match.group(1)}
        player_url = scraper_utils.urljoin(self.base_url, PLAYER_URL)
        html = self._http_get(player_url, params=params, headers=headers, cache_limit=1)
        js_data = scraper_utils.parse_json(html, player_url)
        pl_url = js_data.get('value') or js_data.get('download')
        if not pl_url: return hosters
        
        headers = {'Referer': page_url}
        if pl_url.startswith('//'): pl_url = 'https:' + pl_url
        html = self._http_get(pl_url, headers=headers, allow_redirect=False, cache_limit=0)
        if html.startswith('http'):
            streams = [(html, '')]
        else:
            js_data = scraper_utils.parse_json(html, pl_url)
            try: streams = [(source['file'], source.get('label', '')) for source in js_data['playlist'][0]['sources']]
            except: streams = []
            
        for stream in streams:
            stream_url, label = stream
            if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                sources[stream_url] = {'quality': scraper_utils.gv_get_quality(stream_url), 'direct': True}
            else:
                if label:
                    quality = scraper_utils.height_get_quality(label)
                else:
                    quality = QUALITIES.HIGH
                sources[stream_url] = {'quality': quality, 'direct': False}
                    
        for source, value in sources.iteritems():
            direct = value['direct']
            quality = value['quality']
            if direct:
                host = scraper_utils.get_direct_hostname(self, source)
            else:
                host = urlparse.urlparse(source).hostname

            stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
            hosters.append(hoster)
            
        return hosters
    
    def __make_token(self):
        token = int(time.time()) / 60 * 60
        token = token * 1000 + (token % 1000)
        return token
        
    def _get_episode_url(self, season_url, video):
        season_url = scraper_utils.urljoin(self.base_url, season_url)
        html = self._http_get(season_url, cache_limit=0)
        logger.log(html)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'ep_link'})
        if not fragment: return
        logger.log(fragment)
        
        episode_pattern = 'href="([^"]+)[^>]+>(?:Episode)?\s*0*%s<' % (video.episode)
        match = re.search(episode_pattern, fragment[0].content)
        if not match: return
        
        return scraper_utils.pathify_url(match.group(1))

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/movies/search')
        html = self._http_get(search_url, params={'s': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'item_movie'}):
            match = dom_parser2.parse_dom(item, 'a', req=['href', 'title'])
            if not match: continue
            
            match_title_year = match[0].attrs['title']
            match_url = match[0].attrs['href']
            is_season = re.search('S(?:eason\s+)?(\d+)', match_title_year, re.I)
            match_vt = video_type == (VIDEO_TYPES.MOVIE and not is_season) or (video_type == VIDEO_TYPES.SEASON and is_season)
            match_year = ''
            if video_type == VIDEO_TYPES.SEASON:
                if not season and not match_vt: continue
                if match_vt:
                    if season and int(is_season.group(1)) != int(season): continue
                else:
                    if season and int(season) != 1: continue
                    site_title, site_year = scraper_utils.extra_year(match_title_year)
                    if scraper_utils.normalize_title(site_title) not in scraper_utils.normalize_title(title) or year != site_year: continue
                    
                match_title = match_title_year
            else:
                if not match_vt: continue
                match_title, match_year = scraper_utils.extra_year(match_title_year)

            match_url = scraper_utils.urljoin(match_url, 'watching.html')
            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)
        return results
