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
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'http://www.pubfilm.to'
MAX_PAGES = 10

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Pubfilm.to'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        iframe_url = dom_parser2.parse_dom(html, 'iframe', {'id': 'myiframe'}, req='src', exclude_comments=True)
        if not iframe_url: return hosters
        iframe_url = iframe_url[0].attrs['src']
        html = self._http_get(iframe_url, headers={'Referer': page_url}, cache_limit=.5)
        
        for source in dom_parser2.parse_dom(html, 'source', {'type': 'video/mp4'}, req=['src', 'data-res']):
            stream_url = source.attrs['src']
            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            else:
                quality = scraper_utils.height_get_quality(source.attrs['data-res'])
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})
                  
            source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
            hosters.append(source)

        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+season-0*%s-episode-0*%s-[^"]*)' % (video.season, video.episode)
        page_url = show_url
        pages = 0
        while page_url and pages < MAX_PAGES:
            page_url = scraper_utils.urljoin(self.base_url, page_url)
            html = self._http_get(page_url, cache_limit=2)
            ep_url = self._default_get_episode_url(html, video, episode_pattern)
            if ep_url: return ep_url
            
            fragment = dom_parser2.parse_dom(html, 'div', {'class': 'pagination'})
            if not fragment: break
            match = re.search('href="([^"]+)[^>]+>\s*&gt;\s*<', fragment[0].content)
            if not match: break
            page_url = scraper_utils.cleanse_title(match.group(1))
            pages += 1
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        params = {'c': 'movie', 'm': 'filter', 'keyword': title}
        html = self._http_get(self.base_url, params=params, cache_limit=8)
        for attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'recent-item'}, req='title'):
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            if not match_url: continue
            
            match_url = match_url[0].attrs['href']
            is_series = re.search('/series/', match_url, re.I)
            if (video_type == VIDEO_TYPES.MOVIE and is_series) or (video_type == VIDEO_TYPES.TVSHOW and not is_series):
                continue
            
            match_title_year = attrs['title']
            match_title, match_year = scraper_utils.extra_year(match_title_year)

            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results
