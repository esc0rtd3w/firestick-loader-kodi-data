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
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'https://seriesonline.is'
Q_MAP = {'TS': QUALITIES.LOW, 'CAM': QUALITIES.LOW, 'HDTS': QUALITIES.LOW, 'HD-720P': QUALITIES.HD720}

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
        return 'SeriesOnline'

    def get_sources(self, video):
        hosters = []
        sources = {}
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        for match in re.finditer('player-data="([^"]+)[^>]+episode-data="([^"]+)[^>]*>(.*?)</a>', html, re.DOTALL):
            player_url, ep_id, label = match.groups()
            if video.video_type == VIDEO_TYPES.EPISODE and not self.__episode_match(video, ep_id):
                continue
            label = label.strip()
            headers = {'Referer': page_url}
            if re.match('https?://embed', player_url):
                src_html = self._http_get(player_url, headers=headers, cache_limit=.5)
                sources.update(scraper_utils.parse_sources_list(self, src_html))
                sources.update(self.__get_sources(src_html, label))
            else:
                sources[player_url] = {'direct': False, 'quality': Q_MAP.get(label.upper(), QUALITIES.HIGH)}
                    
        for source, value in sources.iteritems():
            direct = value['direct']
            quality = value['quality']
            if direct:
                host = scraper_utils.get_direct_hostname(self, source)
                stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            else:
                host = urlparse.urlparse(source).hostname
                stream_url = source

            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
            hosters.append(hoster)
            
        return hosters
    
    def __get_sources(self, html, label):
        sources = {}
        for attrs, _label in dom_parser2.parse_dom(html, 'source', req='src'):
            if scraper_utils.get_direct_hostname(self, attrs['src']) == 'gvideo':
                quality = scraper_utils.gv_get_quality(attrs['src'])
            else:
                quality = Q_MAP.get(label.upper(), QUALITIES.HIGH)
                
            sources[attrs['src']] = {'direct': True, 'quality': quality}
        return sources
    
    def __episode_match(self, video, label):
        return re.search('(episode)?\s*0*%s' (video.episode), label, re.I) is not None
    
    def _get_episode_url(self, season_url, video):
        season_url = scraper_utils.urljoin(self.base_url, season_url)
        html = self._http_get(season_url, cache_limit=.5)
        for match in re.finditer('episode-data="([^"]+)', html):
            if self.__episode_match(video, match.group(1)):
                return season_url

    def search(self, video_type, title, year, season=''):
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/movie/search/')
        title = re.sub('[^A-Za-z0-9 ]', '', title)
        title = re.sub('\s+', '-', title)
        search_url += title
        html = self._http_get(search_url, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'ml-item'}):
            match_title = dom_parser2.parse_dom(item, 'span', {'class': 'mli-info'})
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_year = ''

            if not match_title or not match_url: continue
            match_url = match_url[0].attrs['href']
            match_title = match_title[0].content
            is_season = re.search('season\s+(\d+)', match_title, re.I)
            if (video_type == VIDEO_TYPES.MOVIE and not is_season) or (video_type == VIDEO_TYPES.SEASON and is_season):
                match_title = re.sub('</?h\d+>', '', match_title)
                if video_type == VIDEO_TYPES.SEASON:
                    if season and int(is_season.group(1)) != int(season): continue
                
                match_url += '/watching.html'
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
