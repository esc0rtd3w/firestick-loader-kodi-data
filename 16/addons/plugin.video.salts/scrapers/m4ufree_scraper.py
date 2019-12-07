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
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
import scraper

BASE_URL = 'http://m4ufree.info'
AJAX_URL = '/ajax.php'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'm4ufree'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        
        views = None
        fragment = dom_parser2.parse_dom(html, 'img', {'src': re.compile('[^"]*view_icon.png')})
        if fragment:
            match = re.search('(\d+)', fragment[0].content)
            if match:
                views = match.group(1)
            
        match = re.search('href="([^"]+-full-movie-[^"]+)', html)
        if match:
            url = match.group(1)
            html = self._http_get(url, cache_limit=.5)
        
        sources = self.__get_embedded(html)
        for link in dom_parser2.parse_dom(html, 'span', {'class': 'btn-eps'}, req='link'):
            link = link.attrs['link']
            ajax_url = scraper_utils.urljoin(self.base_url, AJAX_URL)
            headers = {'Referer': url}
            headers.update(XHR)
            html = self._http_get(ajax_url, params={'v': link}, headers=headers, cache_limit=.5)
            sources.update(self.__get_sources(html))
        
        for source in sources:
            if sources[source]['direct']:
                host = scraper_utils.get_direct_hostname(self, source)
            else:
                host = urlparse.urlparse(source).hostname
            stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            direct = sources[source]['direct']
            quality = sources[source]['quality']
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': views, 'rating': None, 'url': stream_url, 'direct': direct}
            hosters.append(hoster)

        return hosters
    
    def __get_embedded(self, html):
        return self.__proc_sources(scraper_utils.parse_sources_list(self, html))
    
    def __get_sources(self, html):
        sources = scraper_utils.parse_sources_list(self, html)
        for source in dom_parser2.parse_dom(html, 'source', {'type': 'video/mp4'}, req='src') + dom_parser2.parse_dom(html, 'iframe', req='src'):
            source = source.attrs['src']
            if scraper_utils.get_direct_hostname(self, source) == 'gvideo':
                quality = scraper_utils.gv_get_quality(source)
                direct = True
            else:
                quality = QUALITIES.HD720
                direct = False
            
            sources[source] = {'quality': quality, 'direct': direct}
        return self.__proc_sources(sources)
    
    def __proc_sources(self, sources):
        sources2 = {}
        for source in sources:
            if not source.startswith('http'):
                stream_url = scraper_utils.urljoin(self.base_url, source)
            else:
                stream_url = source
                
            if self.base_url in stream_url:
                redir_url = self._http_get(stream_url, allow_redirect=False, method='HEAD')
                if redir_url.startswith('http'):
                    sources2[redir_url] = sources[source]
                    if scraper_utils.get_direct_hostname(self, redir_url) == 'gvideo':
                        sources2[redir_url]['direct'] = True
            else:
                sources2[stream_url] = sources[source]
            
        return sources2
        
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        title = re.sub('[^A-Za-z0-9 ]', '', title)
        title = re.sub('\s+', '-', title)
        search_url = scraper_utils.urljoin(self.base_url, '/tag/%s' % (title))
        html = self._http_get(search_url, cache_limit=1)
        for attrs, match_title_year in dom_parser2.parse_dom(html, 'a', {'class': 'top-item'}, req='href'):
            match_url = attrs['href']
            if '-tvshow-' in match_url: continue
            match_title_year = re.sub('</?[^>]*>', '', match_title_year)
            match_title_year = re.sub('^Watch\s*', '', match_title_year)
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results
