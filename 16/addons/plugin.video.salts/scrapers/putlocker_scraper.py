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
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
import dom_parser2
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'http://putlocker9.is'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Putlocker'

    def resolve_link(self, link):
        if not link.startswith('http'):
            stream_url = scraper_utils.urljoin(self.base_url, link)
            html = self._http_get(stream_url, cache_limit=0)
            iframe_url = dom_parser2.parse_dom(html, 'iframe', req='src')
            if iframe_url:
                return iframe_url[0].attrs['src']
        else:
            return link
        
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'videoPlayer'}):
            for attrs, _content in dom_parser2.parse_dom(fragment, 'iframe', req='src'):
                html = self._http_get(attrs['src'], headers={'Referer': page_url}, cache_limit=.5)
                match = re.search('downloadUrl\s*=\s*"([^"]+)', html)
                if match:
                    stream_url = match.group(1)
                    host = scraper_utils.get_direct_hostname(self, stream_url)
                    if host == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    else:
                        quality = QUALITIES.HIGH
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        headers = {'Referer': self.base_url}
        params = {'search': title}
        html = self._http_get(self.base_url, params=params, headers=headers, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'listCard'}):
            match_title = dom_parser2.parse_dom(item, 'p', {'class': 'extraTitle'})
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_year = dom_parser2.parse_dom(item, 'p', {'class': 'cardYear'})
            if match_url and match_title:
                match_url = match_url[0].attrs['href']
                match_title = match_title[0].content
                match_year = match_year[0].content if match_year else ''
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, headers={'Referer': self.base_url}, cache_limit=24 * 7)
        match = re.search('href="([^"]*season=0*%s(?!\d))[^"]*' % (video.season), html)
        if not match: return

        episode_pattern = 'href="([^"]*/0*%s-0*%s/[^"]*)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+)[^>]*>\s*(?P<title>.*?)\s*</a>'
        season_url = scraper_utils.urljoin(show_url, match.group(1))
        html = self._http_get(season_url, headers={'Referer': show_url}, cache_limit=2)
        episodes = dom_parser2.parse_dom(html, 'div', {'class': 'episodeDetail'})
        fragment = '\n'.join(ep.content for ep in episodes)
        return self._default_get_episode_url(fragment, video, episode_pattern, title_pattern)
