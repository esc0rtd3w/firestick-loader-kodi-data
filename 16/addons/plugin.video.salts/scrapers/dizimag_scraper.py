# -*- coding: utf-8 -*-
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
import urlparse
import re
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
import scraper

logger = log_utils.Logger.get_logger(__name__)

BASE_URL = 'http://dizimag2.co'
XHR = {'X-Requested-With': 'XMLHttpRequest'}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Dizimag'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.5)
        # exit early if trailer
        if re.search('Şu an fragman*', html, re.I):
            return hosters
        
        hosters = self.__get_embed_sources(html, page_url)
        if not hosters:
            match = re.search('''html\('<iframe[^>]+src="(http[^"]+)''', html)
            if match:
                hosters = self.__get_iframe_sources(match.group(1), page_url)
                
        if not hosters:
            hosters = self.__get_ajax_sources(html, page_url)
                
        return hosters

    def __get_embed_sources(self, html, page_url):
        hosters = []
        match = re.search('var\s+kaynaklar\d+\s*=\s*\[(.*?)\]', html, re.DOTALL)
        if match:
            for match in re.finditer('''['"]?file['"]?\s*:\s*['"]([^'"]+)['"][^}]*['"]?label['"]?\s*:\s*['"]([^'"]*)''', match.group(1), re.DOTALL):
                stream_url, label = match.groups()
                stream_url = stream_url.replace('\\x', '').decode('hex')
                hoster = self.__create_source(stream_url, label, page_url)
                hosters.append(hoster)
                    
        return hosters
        
    def __get_ajax_sources(self, html, page_url):
        hosters = []
        match = re.search('''url\s*:\s*"([^"]+)"\s*,\s*data:'id=''', html)
        if match:
            ajax_url = match.group(1)
            for data_id in re.findall("kaynakdegis\('([^']+)", html):
                url = scraper_utils.urljoin(self.base_url, ajax_url)
                data = {'id': data_id}
                headers = {'Referer': page_url}
                headers.update(XHR)
                result = self._http_get(url, data=data, headers=headers, cache_limit=.5)
                js_data = scraper_utils.parse_json(result, url)
                if 'iframe' in js_data:
                    if self.base_url in js_data['iframe']:
                        hosters += self.__get_iframe_sources(js_data['iframe'], page_url)
                    else:
                        hosters.append(self.__create_source(js_data['iframe'], 720, page_url, direct=False))
                else:
                    hosters += self.__get_js_sources(js_data, page_url)
                    pass
                    
        return hosters
        
    def __get_iframe_sources(self, iframe_url, page_url):
        hosters = []
        headers = {'Referer': page_url}
        html = self._http_get(iframe_url, headers=headers, cache_limit=.5)
        sources = dom_parser2.parse_dom(html, 'div', {'class': 'dzst-player'}, req='data-dzst-player')
        if sources:
            sources = scraper_utils.cleanse_title(sources[0].attrs['data-dzst-player'].replace('&#x3D;', '='))
            js_data = scraper_utils.parse_json(scraper_utils.cleanse_title(sources), iframe_url)
            sources = js_data.get('tr', {})
            for key in sources:
                hosters.append(self.__create_source(sources[key], key, page_url, subs=True))
            
        return hosters
    
    def __get_js_sources(self, js_data, page_url):
        hosters = []
        for key in js_data:
            if 'videolink' in key:
                stream_url = js_data[key]
                if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                    hosters.append(self.__create_source(stream_url, 480, page_url))
        return hosters
        
    def __create_source(self, stream_url, height, page_url, subs=False, direct=True):
        if direct:
            stream_url = stream_url.replace('\\/', '/')
            if self.get_name().lower() in stream_url:
                headers = {'Referer': page_url}
                redir_url = self._http_get(stream_url, headers=headers, method='HEAD', allow_redirect=False, cache_limit=.25)
                if redir_url.startswith('http'):
                    stream_url = redir_url
                    stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                else:
                    stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url, 'Cookie': self._get_stream_cookies()})
            else:
                stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})

            host = scraper_utils.get_direct_hostname(self, stream_url)
        else:
            host = urlparse.urlparse(stream_url).hostname

        if host == 'gvideo':
            quality = scraper_utils.gv_get_quality(stream_url)
        else:
            quality = scraper_utils.height_get_quality(height)
            
        hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
        if subs: hoster['subs'] = 'Turkish Subtitles'
        return hoster
        
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+/%s-sezon-%s-bolum[^"]*)"' % (video.season, video.episode)
        title_pattern = 'class="gizle".*?href="(?P<url>[^"]+)">(?P<title>[^<]+)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        episodes = dom_parser2.parse_dom(html, 'tr', {'bgcolor': '444444'})
        episodes = '\n'.join([ep.content for ep in episodes])
        return self._default_get_episode_url(episodes, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, cache_limit=48)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'fil'})
        if not fragment: return results
        
        norm_title = scraper_utils.normalize_title(title)
        for match in re.finditer('href="([^"]+)"\s+title="([^"]+)', fragment[0].content):
            url, match_title = match.groups()
            if norm_title in scraper_utils.normalize_title(match_title):
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                results.append(result)

        return results
