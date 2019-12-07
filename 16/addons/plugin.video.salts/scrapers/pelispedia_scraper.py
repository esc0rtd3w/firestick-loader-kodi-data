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
import scraper
import urllib
import base64
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib import jsunpack
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import XHR

logger = log_utils.Logger.get_logger()
BASE_URL = 'http://www.pelispedia.tv'
PK_URL = 'http://player.pelispedia.tv/template/protected.php'
GK_URL = '/gkphp_flv/plugins/gkpluginsphp.php'
DEL_LIST = ['sub', 'id']
MOVIE_SEARCH_URL = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAxMzA0MzU4NDUzMDg1NzU4NzM4MTpkcGR2Y3FlbGt3dyZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='

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
        return 'PelisPedia'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'repro'})
        if not fragment: return hosters
        
        iframe_url = dom_parser2.parse_dom(fragment[0].content, 'iframe', req='src')
        if not iframe_url: return hosters
        iframe_url = iframe_url[0].attrs['src']
        
        html = self._http_get(iframe_url, cache_limit=.5)
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'id': 'botones'}):
            for attrs, _content in dom_parser2.parse_dom(fragment, 'a', req='href'):
                media_url = attrs['href']
                media_url = media_url.replace(' ', '')
                if self.get_name().lower() in media_url:
                    headers = {'Referer': iframe_url[0]}
                    html = self._http_get(media_url, headers=headers, cache_limit=.5)
                    hosters += self.__get_page_links(html)
                    hosters += self.__get_pk_links(html)
#                     hosters += self.__get_gk_links(html, iframe_url)
                else:
                    host = urlparse.urlparse(media_url).hostname
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': QUALITIES.HD720, 'views': None, 'rating': None, 'url': media_url, 'direct': False}
                    hosters.append(hoster)
            
        return hosters

    def __get_page_links(self, html):
        hosters = []
        for match in re.finditer('(eval\(function\(.*?)</script>', html, re.DOTALL):
            js_data = jsunpack.unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            html += js_data

        sources = scraper_utils.parse_sources_list(self, html)
        for source in sources:
            quality = sources[source]['quality']
            hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': quality, 'host': scraper_utils.get_direct_hostname(self, source), 'rating': None, 'views': None, 'direct': True}
            hosters.append(hoster)
        return hosters

    def __get_pk_links(self, html):
        hosters = []
        match = re.search('var\s+parametros\s*=\s*"([^"]+)', html)
        if match:
            params = scraper_utils.parse_query(match.group(1))
            if 'pic' in params:
                data = {'sou': 'pic', 'fv': '25', 'url': params['pic']}
                html = self._http_get(PK_URL, headers=XHR, data=data, cache_limit=0)
                js_data = scraper_utils.parse_json(html, PK_URL)
                for item in js_data:
                    if 'url' in item and item['url']:
                        if 'width' in item and item['width']:
                            quality = scraper_utils.width_get_quality(item['width'])
                        elif 'height' in item and item['height']:
                            quality = scraper_utils.height_get_quality(item['height'])
                        else:
                            quality = QUALITIES.HD720
                        stream_url = item['url'] + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                        hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': scraper_utils.get_direct_hostname(self, item['url']), 'rating': None, 'views': None, 'direct': True}
                        hosters.append(hoster)
        return hosters
    
    def __get_gk_links(self, html, url):
        hosters = []
        for match in re.finditer('gkpluginsphp.*?link\s*:\s*"([^"]+)', html):
            data = {'link': match.group(1)}
            headers = {'Referer': url}
            headers.update(XHR)
            gk_url = scraper_utils.urljoin(self.base_url, GK_URL)
            html = self._http_get(gk_url, data=data, headers=headers, cache_limit=.5)
            js_result = scraper_utils.parse_json(html, gk_url)
            if 'link' in js_result and 'func' not in js_result:
                if isinstance(js_result['link'], list):
                    sources = dict((link['link'], scraper_utils.height_get_quality(link.get('label', 700))) for link in js_result['link'])
                else:
                    sources = {js_result['link']: QUALITIES.HD720}
                
                for source in sources:
                    if source:
                        hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': sources[source], 'host': scraper_utils.get_direct_hostname(self, source), 'rating': None, 'views': None, 'direct': True}
                        hosters.append(hoster)
        return hosters
        
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+-season-%s-episode-%s(?!\d)[^"]*)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+-season-\d+-episode-\d+[^"]*).*?class="[^"]*ml5[^"]*">(?P<title>[^<]+)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        parts = dom_parser2.parse_dom(html, 'article', {'class': 'SeasonList'})
        fragment = '\n'.join(part.content for part in parts)
        return self._default_get_episode_url(fragment, video, episode_pattern, title_pattern)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        if video_type == VIDEO_TYPES.TVSHOW:
            results = self.__tv_search(title, year)
        else:
            results = self.__movie_search(title, year)
        return results

    def __tv_search(self, title, year):
        results = []
        if title:
            url = '/series/letra/%s/' % (title[0])
            results = self.__proc_results(url, title, year)
                        
        return results

    def __movie_search(self, title, year):
        results = []
        search_url = base64.decodestring(MOVIE_SEARCH_URL) % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=1)
        js_data = scraper_utils.parse_json(html)
        if 'results' in js_data:
            norm_title = scraper_utils.normalize_title(title)
            for item in js_data['results']:
                match_url = urllib.unquote(item['url'])
                if '/pelicula/' not in match_url: continue
                match_title_year = item['titleNoFormatting']
                match_title_year = re.sub('^Ver\s+', '', match_title_year)
                match = re.search('(.*?)(?:\s+\(?(\d{4})\)?)', match_title_year)
                if match:
                    match_title, match_year = match.groups()
                else:
                    match_title = match_title_year
                    match_year = ''
                
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
        
        if not results and title and year:
            url = '/movies/all/?year=%s&gender=&letra=%s' % (year, title[0])
            results = self.__proc_results(url, title, year)
            
        return results

    def __proc_results(self, url, title, year):
        results = []
        url = scraper_utils.urljoin(self.base_url, url)
        html = self._http_get(url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(html, 'li', {'class': 'bpM12'}):
            title_frag = dom_parser2.parse_dom(item, 'h2')
            year_frag = dom_parser2.parse_dom(item, 'div', {'class': 'sectionDetail'})
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            if title_frag and match_url:
                match_url = match_url[0].attrs['href']
                match = re.search('(.*?)<br>', title_frag[0].content)
                if match:
                    match_title = match.group(1)
                else:
                    match_title = title_frag[0]
                    
                match_year = ''
                if year_frag:
                    match = re.search('(\d{4})', year_frag[0].content)
                    if match:
                        match_year = match.group(1)

                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        
        return results
