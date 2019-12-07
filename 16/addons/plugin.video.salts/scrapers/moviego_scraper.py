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
import urlparse
import re
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import jsunpack
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://moviego.cc'
XHR = {'X-Requested-With': 'XMLHttpRequest'}
Q_MAP = {'HD1080': QUALITIES.HD1080, 'HD720': QUALITIES.HD720, 'SD480': QUALITIES.HIGH, 'CAMRIP': QUALITIES.LOW}

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
        return 'MovieGo'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=8)
        q_str = dom_parser2.parse_dom(html, 'div', {'class': 'poster-qulabel'})
        if q_str:
            q_str = q_str[0].content.replace(' ', '').upper()
            page_quality = Q_MAP.get(q_str, QUALITIES.HIGH)
        else:
            page_quality = QUALITIES.HIGH
            
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'tab_box'}):
            iframe_url = dom_parser2.parse_dom(fragment, 'iframe', req='src')
            if iframe_url:
                iframe_url = iframe_url[0].attrs['src']
                if 'youtube' in iframe_url: continue
                
                html = self._http_get(iframe_url, headers={'Referer': page_url}, cache_limit=.5)
                for match in re.finditer('(eval\(function\(.*?)</script>', html, re.DOTALL):
                    js_data = jsunpack.unpack(match.group(1))
                    js_data = js_data.replace('\\', '')
                    html += js_data
                
                sources = scraper_utils.parse_sources_list(self, html)
                if not sources:
                    sources = {iframe_url: {'quality': page_quality, 'direct': False}}
                
                for source, values in sources.iteritems():
                    direct = values['direct']
                    if direct:
                        host = scraper_utils.get_direct_hostname(self, source)
                        if host == 'gvideo':
                            quality = scraper_utils.gv_get_quality(source)
                        else:
                            quality = values['quality']
                        source += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})
                    else:
                        host = urlparse.urlparse(source).hostname
                        quality = scraper_utils.get_quality(video, host, values['quality'])
                    
                    hoster = {'multi-part': False, 'url': source, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                    hosters.append(hoster)

        return hosters

    def __get_ajax_sources(self, html, page_url):
        stream_url = ''
        match = re.search('''\$\.getJSON\('([^']+)'\s*,\s*(\{.*?\})''', html)
        if match:
            ajax_url, params = match.groups()
            params = scraper_utils.parse_params(params)
            ajax_url = scraper_utils.urljoin(self.base_url, ajax_url)
            headers = {'Referer': page_url}
            headers.update(XHR)
            html = self._http_get(ajax_url, params=params, headers=headers, cache_limit=.5)
            js_data = scraper_utils.parse_json(html, ajax_url)
            stream_url = js_data.get('file', '')
        return stream_url
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        data = {'hash': 'indexert', 'do': 'search', 'subaction': 'search', 'search_start': 0, 'full_search': 0, 'result_from': 1, 'story': title}
        search_url = scraper_utils.urljoin(self.base_url, 'index.php')
        html = self._http_get(search_url, params={'do': 'search'}, data=data, cache_limit=8)
        if dom_parser2.parse_dom(html, 'div', {'class': 'sresult'}):
            for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'short_content'}):
                match_url = dom_parser2.parse_dom(item, 'a', req='href')
                match_title_year = dom_parser2.parse_dom(item, 'div', {'class': 'short_header'})
                if match_url and match_title_year:
                    match_url = match_url[0].attrs['href']
                    match_title, match_year = scraper_utils.extra_year(match_title_year[0].content)
                    if not year or not match_year or year == match_year:
                        result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                        results.append(result)

        return results
