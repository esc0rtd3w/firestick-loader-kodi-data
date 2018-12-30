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
import dom_parser2
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib import jsunpack
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper
import xml.etree.ElementTree as ET

try:
    from xml.parsers.expat import ExpatError
except ImportError:
    class ExpatError(Exception): pass
try:
    from xml.etree.ElementTree import ParseError
except ImportError:
    class ParseError(Exception): pass

logger = log_utils.Logger.get_logger()
BASE_URL = 'http://dizipas.net'
AJAX_URL = 'http://dizipas.org/player/ajax.php'
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
        return 'Dizipas'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        sources = self.__get_posts(html)
        sources.update(self.__get_ajax(html, url))
        sources.update(self.__get_embedded(html, url))
        for source in sources:
            stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            host = scraper_utils.get_direct_hostname(self, source)
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': sources[source], 'views': None, 'rating': None, 'url': stream_url, 'direct': True, 'subs': 'Turkish subtitles'}
            hosters.append(hoster)

        return hosters

    def __get_embedded(self, html, page_url):
        sources = {}
        match = dom_parser2.parse_dom(html, 'div', {'id': 'videoreklam'})
        if not match: return sources
        match = dom_parser2.parse_dom(match[0].content, 'iframe', req='src')
        if not match: return sources
        headers = {'Referer': page_url}
        html = self._http_get(match[0].attrs['src'], headers=headers, cache_limit=.5)
        for match in re.finditer('(eval\(function\(.*?)</script>', html, re.DOTALL):
            js_data = jsunpack.unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            html += js_data
        return dict((key, value['quality']) for key, value in scraper_utils.parse_sources_list(self, html, var='source').iteritems())
        
    def __get_posts(self, html):
        sources = {}
        pattern = '\$\.post\("([^"]+)"\s*,\s*\{(.*?)\}'
        match = re.search(pattern, html)
        if not match: return sources

        post_url, post_data = match.groups()
        data = self.__get_data(post_data)
        html = self._http_get(post_url, data=data, cache_limit=.5)
        js_result = scraper_utils.parse_json(html, post_url)
        for key in js_result:
            stream_url = js_result[key]
            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
            else:
                quality = scraper_utils.height_get_quality(key)
            sources[stream_url] = quality
        return sources
    
    def __get_ajax(self, html, page_url):
        sources = {}
        pattern = '\$\.ajax\(\s*"([^"]+)'
        match = re.search(pattern, html)
        if not match: return sources

        post_url = match.group(1)
        headers = {'Referer': page_url}
        html = self._http_get(post_url, headers=headers, cache_limit=.5)
        js_result = scraper_utils.parse_json(html, post_url)
        for key in js_result:
            stream_url = js_result[key]
            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
            else:
                quality = scraper_utils.height_get_quality(key)
            sources[stream_url] = quality
        return sources
    
    def __get_linked(self, html):
        sources = {}
        match = re.search('dizi=([^"]+)', html)
        if not match: return sources
        html = self._http_get(AJAX_URL, params={'dizi': match.group(1)}, headers=XHR, cache_limit=.5)
        js_result = scraper_utils.parse_json(html, AJAX_URL)
        for source in js_result.get('success', []):
            stream_url = source.get('src')
            if stream_url is None: continue

            if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
            elif 'label' in source:
                quality = scraper_utils.height_get_quality(source['label'])
            else:
                quality = QUALITIES.HIGH
            sources[stream_url] = quality
        return sources
    
    def __get_data(self, post_data):
        data = {}
        post_data = re.sub('\s+|"|\'', '', post_data)
        for element in post_data.split(','):
            key, value = element.split(':')
            data[key] = value
        return data
    
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'class="episode"\s+href="([^"]+/sezon-%s/bolum-%s)"' % (video.season, video.episode)
        title_pattern = 'class="episode-name"\s+href="(?P<url>[^"]+)">(?P<title>[^<]+)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        episodes = dom_parser2.parse_dom(html, 'div', {'class': 'tv-series-episodes'})
        episodes = '\n'.join([ep.content for ep in episodes])
        return self._default_get_episode_url(episodes, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        xml_url = scraper_utils.urljoin(self.base_url, '/series.xml')
        xml = self._http_get(xml_url, cache_limit=24)
        if not xml: return results
        try:
            norm_title = scraper_utils.normalize_title(title)
            match_year = ''
            for element in ET.fromstring(xml).findall('.//dizi'):
                name = element.find('adi')
                if name is not None and norm_title in scraper_utils.normalize_title(name.text):
                    url = element.find('url')
                    if url is not None and (not year or not match_year or year == match_year):
                        result = {'url': scraper_utils.pathify_url(url.text), 'title': scraper_utils.cleanse_title(name.text), 'year': ''}
                        results.append(result)
        except (ParseError, ExpatError) as e:
            logger.log('Dizilab Search Parse Error: %s' % (e), log_utils.LOGWARNING)

        return results
