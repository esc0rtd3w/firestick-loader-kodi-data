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
from salts_lib.constants import XHR
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://vumoo.li'

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
        return 'Vumoo'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        if video.video_type == VIDEO_TYPES.EPISODE:
            html = self.__episode_match(video, source_url)
            sources = [r.attrs['data-click'] for r in dom_parser2.parse_dom(html, 'div', req='data-click') + dom_parser2.parse_dom(html, 'li', req='data-click')]
        else:
            sources = self.__get_movie_sources(page_url)
        sources = [source.strip() for source in sources if source]

        headers = {'Referer': page_url}
        for source in sources:
            if source.startswith('http'):
                direct = False
                quality = QUALITIES.HD720
                host = urlparse.urlparse(source).hostname
            else:
                source = self.__get_linked_source(source, headers)
                if source is None: continue
                direct = True
                host = scraper_utils.get_direct_hostname(self, source)
                if host == 'gvideo':
                    quality = scraper_utils.gv_get_quality(source)
                else:
                    pass
            
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': direct}
            hosters.append(hoster)
            
        return hosters

    def __get_movie_sources(self, page_url):
        sources = []
        headers = {'Referer': ''}
        html = self._http_get(page_url, headers=headers, cache_limit=.5)
        match = re.search('APP_PATH\+"([^"]+)"\+([^"]+)\+"([^"]+)"', html)
        if match:
            url1, var, url2 = match.groups()
            match = re.search("%s\s*=\s*'([^']+)" % (var), html)
            if match:
                headers = {'Referer': page_url}
                headers.update(XHR)
                contents_url = '/' + url1 + match.group(1) + url2
                contents_url = scraper_utils.urljoin(self.base_url, contents_url)
                js_data = scraper_utils.parse_json(self._http_get(contents_url, headers=headers, cache_limit=2), contents_url)
                if js_data:
                    sources = [item['src'] for item in js_data if 'src' in item]

        match = re.search("openloadLink\s*=\s*'([^']+)", html, re.I)
        if match:
            sources.append(match.group(1))
            
        return sources
    
    def __get_linked_source(self, link_url, headers):
        link_url = scraper_utils.urljoin(self.base_url, link_url)
        html = self._http_get(link_url, headers=headers, allow_redirect=False)
        if html.startswith('http'):
            return html
    
    def _get_episode_url(self, show_url, video):
        if self.__episode_match(video, show_url):
            return show_url

    def __episode_match(self, video, show_url):
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        headers = {'Referer': ''}
        html = self._http_get(show_url, headers=headers, cache_limit=2)
        force_title = scraper_utils.force_title(video)

        if not force_title:
            match = dom_parser2.parse_dom(html, 'li', {'id': 'season%s-%s' % (video.season, video.episode)})
            if match:
                return match[0].content
            
        if (force_title or kodi.get_setting('title-fallback') == 'true') and video.ep_title:
            norm_title = scraper_utils.normalize_title(video.ep_title)
            for episode in re.finditer('''<li\s+id=['"]?season\d+-\d+['"]?>.*?</ul>''', html, re.DOTALL):
                ep_title = dom_parser2.parse_dom(episode.group(0), 'h2')
                if ep_title and norm_title == scraper_utils.normalize_title(ep_title[0].content):
                    return episode
                
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/videos/search/')
        headers = {'Referer': ''}
        html = self._http_get(search_url, params={'search': title, 've': 1}, headers=headers, cache_limit=8)
        for _attrs, article in dom_parser2.parse_dom(html, 'article', {'class': 'movie_item'}):
            match = dom_parser2.parse_dom(article, 'a', req=['href', 'data-title'])
            if match:
                match_url = match[0].attrs['href']
                match_title = match[0].attrs['data-title']
                match_year = ''
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
            
        return results
