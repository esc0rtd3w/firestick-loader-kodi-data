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
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'https://moviesub.is'
LINK_URL2 = '/Htplugins/Loader.php'
LINK_URL = '/ip.file/swf/plugins/ipplugins.php'
PLAYER_URL = '/ip.file/swf/ipplayer/ipplayer.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

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
        return 'MovieSub'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        if video.video_type == VIDEO_TYPES.EPISODE:
            gk_html = ''.join(match.group(0) for match in re.finditer('<a[^>]*>(%s|Server \d+)</a>' % (video.episode), html, re.I))
        else:
            gk_html = html
        link_url = scraper_utils.urljoin(self.base_url, LINK_URL)
        player_url = scraper_utils.urljoin(self.base_url, PLAYER_URL)
        sources = scraper_utils.get_gk_links(self, gk_html, page_url, QUALITIES.HIGH, link_url, player_url)
        sources.update(self.__get_ht_links(html, page_url))
        
        for stream_url, quality in sources.iteritems():
            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                direct = True
            else:
                host = urlparse.urlparse(stream_url).hostname
                direct = False
            
            if host is None: continue
            stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
            hosters.append(hoster)

        return hosters

    def __get_ht_links(self, html, page_url):
        sources = {}
        match = re.search('Htplugins_Make_Player\("([^"]+)', html)
        if match:
            data = {'data': match.group(1)}
            url = scraper_utils.urljoin(self.base_url, LINK_URL2)
            headers = {'Referer': page_url}
            html = self._http_get(url, data=data, headers=headers, cache_limit=.25)
            js_data = scraper_utils.parse_json(html, url)
            if 'l' in js_data:
                for link in js_data['l']:
                    if scraper_utils.get_direct_hostname(self, link) == 'gvideo':
                        quality = scraper_utils.gv_get_quality(link)
                    else:
                        quality = QUALITIES.HIGH
                    sources[link] = quality
        return sources
        
    def _get_episode_url(self, season_url, video):
        episode_pattern = 'href="([^"]+)[^>]*>\s*%s\s*<' % (video.episode)
        season_url = scraper_utils.urljoin(self.base_url, season_url)
        html = self._http_get(season_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'episode_show'})
        return self._default_get_episode_url(fragment, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/%s.html' % (urllib.quote_plus(title)))
        html = self._http_get(search_url, cache_limit=1)
        fragment = dom_parser2.parse_dom(html, 'ul', {'class': 'cfv'})
        if not fragment: return results
        
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(fragment[0].content, 'li'):
            is_season = dom_parser2.parse_dom(item, 'div', {'class': 'status'})
            if (not is_season and video_type == VIDEO_TYPES.MOVIE) or (is_season and video_type == VIDEO_TYPES.SEASON):
                match = dom_parser2.parse_dom(item, 'a', req=['href', 'title'])
                if not match: continue
                
                match_title = match[0].attrs['title']
                match_url = match[0].attrs['href']
                match_year = ''
                if video_type == VIDEO_TYPES.SEASON:
                    if season and not re.search('Season\s+%s$' % (season), match_title, re.I):
                        continue
                else:
                    match = re.search('-(\d{4})[-.]', match_url)
                    if match:
                        match_year = match.group(1)
                
                match_norm_title = scraper_utils.normalize_title(match_title)
                title_match = (norm_title in match_norm_title) or (match_norm_title in norm_title)
                if title_match and (not year or not match_year or year == match_year):
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
