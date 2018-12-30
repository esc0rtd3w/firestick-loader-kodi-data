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
import scraper

BASE_URL = 'http://watchonline.pro'

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
        return 'WatchOnline'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)

        sources = {}
        for _attrs, fragment in dom_parser2.parse_dom(html, 'ul', {'class': 'enlaces'}):
            for attrs, _content in dom_parser2.parse_dom(fragment, 'a', req='href'):
                stream_url = attrs['href']
                if video.video_type == VIDEO_TYPES.MOVIE:
                    meta = scraper_utils.parse_movie_link(stream_url)
                else:
                    meta = scraper_utils.parse_episode_link(stream_url)
                sources.update({stream_url: {'quality': scraper_utils.height_get_quality(meta['height']), 'direct': False}})
                
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'movieplay'}) + dom_parser2.parse_dom(html, 'div', {'id': re.compile('player\d+')}):
            for attrs, _content in dom_parser2.parse_dom(fragment, 'iframe', req='src') + dom_parser2.parse_dom(fragment, 'iframe', req='data-lazy-src'):
                iframe_url = attrs.get('src', '')
                if not iframe_url.startswith('http'):
                    iframe_url = attrs.get('data-lazy-src', '')
                    if not iframe_url.startswith('http'): continue
                
                if '//player' in iframe_url:
                    html = self._http_get(iframe_url, headers={'Referer': page_url}, cache_limit=.5)
                    sources.update(scraper_utils.parse_sources_list(self, html))
                else:
                    if video.video_type == VIDEO_TYPES.MOVIE:
                        meta = scraper_utils.parse_movie_link(iframe_url)
                    else:
                        meta = scraper_utils.parse_episode_link(iframe_url)
                    sources.update({iframe_url: {'quality': scraper_utils.height_get_quality(meta['height']), 'direct': False}})
                    
        for stream_url, values in sources.iteritems():
            direct = values['direct']
            quality = values['quality']
            if direct:
                host = scraper_utils.get_direct_hostname(self, stream_url)
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            else:
                stream_url = stream_url
                host = urlparse.urlparse(stream_url).hostname

            hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': host, 'rating': None, 'views': None, 'direct': direct}
            hosters.append(hoster)
        
        return hosters
            
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+s0*%se0*%s(?!\d)[^"]*)' % (video.season, video.episode)
        title_pattern = 'class="episodiotitle">\s*<a[^>]+href="(?P<url>[^"]+)[^>]*>(?P<title>.*?)</a>'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        parts = dom_parser2.parse_dom(html, 'ul', {'class': 'episodios'})
        fragment = '\n'.join(part.content for part in parts)
        return self._default_get_episode_url(fragment, video, episode_pattern, title_pattern)
                
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/advanced-search/')
        headers = {'Referer': self.base_url}
        params = {'search_query': title, 'orderby': '', 'order': '', 'wpas': 1}
        html = self._http_get(search_url, params=params, headers=headers, cache_limit=8)
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'datos'}):
            match = dom_parser2.parse_dom(item, 'a', req='href')
            if not match: continue
            
            match_url = match[0].attrs['href']
            is_tvshow = '/tvshows/' in match_url
            if is_tvshow and video_type == VIDEO_TYPES.MOVIE or not is_tvshow and video_type == VIDEO_TYPES.TVSHOW:
                continue
            
            match_title = match[0].content
            match_title, match_year = scraper_utils.extra_year(match_title)
            if scraper_utils.normalize_title(match_title) in norm_title and (not year or not match_year or year == match_year):
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)
            
        return results
