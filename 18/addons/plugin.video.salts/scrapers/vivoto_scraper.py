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

logger = log_utils.Logger.get_logger(__name__)

BASE_URL = 'https://vivo.to'
LINK_URL = '/ip.file/swf/plugins/ipplugins.php'
PLAYER_URL = '/ip.file/swf/ipplayer/ipplayer.php'
XHR = {'X-Requested-With': 'XMLHttpRequest'}
QUALITY_MAP = {'HD': QUALITIES.HD720, 'SD': QUALITIES.HIGH}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        if 'www' in self.base_url: self.base_url = BASE_URL  # hack base url to work

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.SEASON, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'vivo.to'

    def resolve_link(self, link):
        if self.base_url in link:
            html = self._http_get(link, cache_limit=.5)
            match = dom_parser2.parse_dom(html, 'iframe', req='src')
            if match: link = match[0].attrs['src']

        return link
        
    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        page_quality = dom_parser2.parse_dom(html, 'dd', {'class': 'status'})
        if page_quality:
            page_quality = QUALITY_MAP.get(page_quality[0].content, QUALITIES.HIGH)
        else:
            page_quality = QUALITIES.HIGH
        
        if video.video_type == VIDEO_TYPES.EPISODE:
            fragment = dom_parser2.parse_dom(html, 'div', {'id': 'servers-list'})
            gk_html = fragment[0].content if fragment else ''
        else:
            gk_html = html

        link_url = scraper_utils.urljoin(self.base_url, LINK_URL)
        player_url = scraper_utils.urljoin(self.base_url, PLAYER_URL)
        for stream_url, quality in scraper_utils.get_gk_links(self, gk_html, page_url, page_quality, link_url, player_url).iteritems():
            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                direct = True
                quality = quality
            else:
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.get_quality(video, host, quality)
                direct = False

            if host is not None:
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
                hosters.append(hoster)

        return hosters

    def _get_episode_url(self, season_url, video):
        episode_pattern = 'href="([^"]+)[^>]*>\s*%s\s*<' % (video.episode)
        season_url = scraper_utils.urljoin(self.base_url, season_url)
        html = self._http_get(season_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'div_episode'})
        return self._default_get_episode_url(fragment, video, episode_pattern)
    
    def search(self, video_type, title, year, season=''):
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/%s.html')
        search_url = search_url % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=1)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'movie'})
        if not fragment: return results
        
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(fragment[0].content, 'li'):
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_title = dom_parser2.parse_dom(item, 'span', {'class': 'text'})
            match_year = dom_parser2.parse_dom(item, 'span', {'class': 'year'})
            if not match_url or not match_title: continue
            
            match_url = match_url[0].attrs['href']
            match_title = re.sub('</?strong>', '', match_title[0].content)
            is_season = re.search('Season\s+(\d+)$', match_title, re.I)
            if (not is_season and video_type == VIDEO_TYPES.MOVIE) or (is_season and video_type == VIDEO_TYPES.SEASON):
                if video_type == VIDEO_TYPES.MOVIE:
                    if match_year:
                        match_year = match_year[0].content
                    else:
                        match_year = ''
                else:
                    if season and int(is_season.group(1)) != int(season):
                        continue
                    match_year = ''
            
                match_norm_title = scraper_utils.normalize_title(match_title)
                title_match = (norm_title in match_norm_title) or (match_norm_title in norm_title)
                if title_match and (not year or not match_year or year == match_year):
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
                    
        return results
