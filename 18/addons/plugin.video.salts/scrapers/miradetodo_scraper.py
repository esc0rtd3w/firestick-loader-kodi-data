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
import base64
import log_utils  # @UnusedImport
import kodi
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper


BASE_URL = 'http://miradetodo.io'
GK_KEY1 = base64.urlsafe_b64decode('QjZVTUMxUms3VFJBVU56V3hraHI=')
GK_KEY2 = base64.urlsafe_b64decode('aUJocnZjOGdGZENaQWh3V2huUm0=')

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.gk_url = self.base_url + '/stream/plugins/gkpluginsphp.php'

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'MiraDeTodo'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        sources = {}
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'movieplay'}):
            for attrs, _content in dom_parser2.parse_dom(fragment, 'iframe', req='src') + dom_parser2.parse_dom(fragment, 'iframe', req='data-lazy-src'):
                iframe_url = attrs.get('src', '')
                if not iframe_url.startswith('http'):
                    iframe_url = attrs.get('data-lazy-src', '')
                    if not iframe_url.startswith('http'): continue
                    
                if 'miradetodo' in iframe_url:
                    html = self._http_get(iframe_url, cache_limit=.5)
                    fragment = dom_parser2.parse_dom(html, 'nav', {'class': 'nav'})
                    if fragment:
                        stream_url = dom_parser2.parse_dom(fragment[0].content, 'a', req='href')
                        if stream_url:
                            html = self._http_get(stream_url[0].attrs['href'], cache_limit=.5)
                            
                    sources.update(self.__get_gk_links(html))
                    sources.update(self.__get_gk_links2(html))
                    sources.update(self.__get_amazon_links(html))
                    sources.update(scraper_utils.parse_sources_list(self, html))
                else:
                    host = urlparse.urlparse(iframe_url).hostname
                    source = {'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'direct': False}
                    sources.update({iframe_url: source})
                    
        for source in sources:
            stream_url = source + '|User-Agent=%s' % (scraper_utils.get_ua())
            direct = sources[source]['direct']
            quality = sources[source]['quality']
            host = scraper_utils.get_direct_hostname(self, source) if direct else urlparse.urlparse(source).hostname
            hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': host, 'rating': None, 'views': None, 'direct': direct}
            hosters.append(hoster)
            
        return hosters

    def __get_amazon_links(self, html):
        sources = {}
        match = re.search('AmazonPlayer.*?file\s*:\s*"([^"]+)', html, re.DOTALL)
        if match:
            html = self._http_get(match.group(1), allow_redirect=False, method='HEAD', cache_limit=0)
            if html.startswith('http'):
                sources = {html: {'quality': QUALITIES.HD720, 'direct': True}}
        return sources
    
    def __get_gk_links2(self, html):
        sources = {}
        match = re.search('proxy\.link=([^"&]+)', html)
        if match:
            proxy_link = match.group(1)
            proxy_link = proxy_link.split('*', 1)[-1]
            if len(proxy_link) <= 224:
                vid_url = scraper_utils.gk_decrypt(self.get_name(), GK_KEY1, proxy_link)
            else:
                vid_url = scraper_utils.gk_decrypt(self.get_name(), GK_KEY2, proxy_link)
            
            if scraper_utils.get_direct_hostname(self, vid_url) == 'gvideo':
                for source in self._parse_gdocs(vid_url):
                    sources[source] = {'quality': scraper_utils.gv_get_quality(source), 'direct': True}
        return sources
        
    def __get_gk_links(self, html):
        sources = {}
        match = re.search('{link\s*:\s*"([^"]+)', html)
        if match:
            iframe_url = match.group(1)
            data = {'link': iframe_url}
            headers = {'Referer': iframe_url}
            html = self._http_get(self.gk_url, data=data, headers=headers, cache_limit=.5)
            js_data = scraper_utils.parse_json(html, self.gk_url)
            links = js_data.get('link', [])
            if isinstance(links, basestring):
                links = [{'link': links}]
                
            for link in links:
                stream_url = link['link']
                if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                    direct = True
                elif 'label' in link:
                    quality = scraper_utils.height_get_quality(link['label'])
                    direct = True
                else:
                    quality = QUALITIES.HIGH
                    direct = False
                sources[stream_url] = {'quality': quality, 'direct': direct}
        return sources
        
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=1)
        results = []
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'item'}):
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_title = dom_parser2.parse_dom(item, 'span', {'class': 'tt'})
            year_frag = dom_parser2.parse_dom(item, 'span', {'class': 'year'})
            if match_url and match_title:
                match_url = match_url[0].attrs['href']
                match_title = match_title[0].content
                if re.search('\d+\s*x\s*\d+', match_title): continue  # exclude episodes
                match_title, match_year = scraper_utils.extra_year(match_title)
                if not match_year and year_frag:
                    match_year = year_frag[0].content

                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results
