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
import scraper
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'https://www.mehlizmovieshd.com'
Q_MAP = {'HD': QUALITIES.HD720, 'DVD': QUALITIES.HIGH, 'CAM': QUALITIES.LOW}

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
        return 'Mehliz'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=8)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'playex'})
        if fragment: html = fragment[0].content
        iframe_url = dom_parser2.parse_dom(html, 'iframe', req='src')
        if not iframe_url: return hosters
        iframe_url = iframe_url[0].attrs['src']
        if iframe_url.startswith('/'):
            iframe_url = scraper_utils.urljoin(self.base_url, iframe_url)
        html = self._http_get(iframe_url, headers={'Referer': page_url}, cache_limit=.5)
        obj = dom_parser2.parse_dom(html, 'object', req='data')
        if obj:
            streams = dict((stream_url, {'quality': scraper_utils.gv_get_quality(stream_url), 'direct': True}) for stream_url in
                           scraper_utils.parse_google(self, obj[0].attrs['data']))
        else:
            streams = scraper_utils.parse_sources_list(self, html)
            
        for stream_url, values in streams.iteritems():
            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
            else:
                quality = values['quality']
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})
                 
            source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': True}
            hosters.append(source)

        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+-0*%sx0*%s(?!\d)[^"]*)' % (video.season, video.episode)
        title_pattern = 'class="episodiotitle">\s*<a[^>]+href="(?P<url>[^"]+)[^>]*>(?P<title>.*?)</a>'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        parts = dom_parser2.parse_dom(html, 'ul', {'class': 'episodios'})
        fragment = '\n'.join(part.content for part in parts)
        return self._default_get_episode_url(fragment, video, episode_pattern, title_pattern)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'result-item'}):
            match = dom_parser2.parse_dom(item, 'div', {'class': 'title'})
            is_movie = dom_parser2.parse_dom(item, 'span', {'class': 'movies'})
            is_show = dom_parser2.parse_dom(item, 'span', {'class': 'tvshows'})
            if (video_type == VIDEO_TYPES.TVSHOW and is_movie) or (video_type == VIDEO_TYPES.MOVIE and is_show) or not match:
                continue
            
            match = dom_parser2.parse_dom(match[0].content, 'a', req='href')
            if not match: continue
            
            match_url, match_title_year = match[0].attrs['href'], match[0].content
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if not match_year:
                match_year = dom_parser2.parse_dom(item, 'span', {'class': 'year'})
                match_year = match_year[0].content if match_year else ''
                
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results
