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
import re
import urlparse
import urllib
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import XHR
import scraper

logger = log_utils.Logger.get_logger()
BASE_URL = 'http://www.dizibox1.com'
LINKS = ['king.php', 'zeus.php', 'hades.php', 'juliet.php']
QUALITY_MAP = {'HD': QUALITIES.HD720}

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
        return 'Dizibox'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=1)
        hosters = self.__extract_links(html)
        fragment = dom_parser2.parse_dom(html, 'section', {'id': 'video-area'})
        if not fragment: return hosters
        
        for match in re.finditer('''value=["']([^'"]+)[^>]*>(?:DBX|King|Odnok|Play|Juliet)''', fragment[0].content, re.I):
            html = self._http_get(match.group(1), cache_limit=1)
            hosters += self.__extract_links(html)
    
        return hosters

    def __extract_links(self, html):
        hosters = []
        fragment = dom_parser2.parse_dom(html, 'span', {'class': 'video-wrapper'})
        if fragment:
            iframe_url = dom_parser2.parse_dom(fragment[0].content, 'iframe', req='src')
            if iframe_url:
                iframe_url = iframe_url[0].attrs['src']
                if any([link for link in LINKS if link in iframe_url]):
                    hosters += self.__get_king_links(iframe_url)
                else:
                    html = self._http_get(iframe_url, cache_limit=.5)
                    hosters += self.__get_embed_links(html)
                    flashvars = dom_parser2.parse_dom(html, 'param', {'name': 'flashvars'}, req='value')
                    embed = dom_parser2.parse_dom(html, 'object', req='data')
                    if embed and flashvars:
                        hosters += self.__get_ok(embed, flashvars)
        return hosters
        
    def __get_king_links(self, iframe_url):
        hosters = []
        match = re.search('v=(.*)', iframe_url)
        if match:
            data = {'ID': match.group(1)}
            headers = {'Referer': iframe_url}
            headers.update(XHR)
            xhr_url = iframe_url.split('?')[0]
            html = self._http_get(xhr_url, params={'p': 'GetVideoSources'}, data=data, headers=headers, cache_limit=.5)
            js_data = scraper_utils.parse_json(html, xhr_url)
            try:
                for source in js_data['VideoSources']:
                    stream_url = source['file'] + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                    host = scraper_utils.get_direct_hostname(self, source['file'])
                    label = source.get('label', '')
                    if host == 'gvideo':
                        quality = scraper_utils.gv_get_quality(source['file'])
                    elif re.search('\d+p?', label):
                        quality = scraper_utils.height_get_quality(label)
                    else:
                        quality = QUALITY_MAP.get(label, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True, 'subs': 'Turkish Subtitles'}
                    hosters.append(hoster)
            except:
                pass
            
        return hosters
    
    def __get_embed_links(self, html):
        hosters = []
        sources = scraper_utils.parse_sources_list(self, html)
        for source in sources:
            quality = source['quality']
            stream_url = source + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            hoster = {'multi-part': False, 'host': scraper_utils.get_direct_hostname(self, source), 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True, 'subs': 'Turkish Subtitles'}
            hosters.append(hoster)
        return hosters
        
    def __get_ok(self, embed, flashvars):
        hosters = []
        link = flashvars[0].attrs['value']
        match = re.search('metadataUrl=([^"]+)', link)
        if match:
            referer = scraper_utils.cleanse_title(urllib.unquote(embed[0].attrs['data']))
            ok_url = scraper_utils.cleanse_title(urllib.unquote(match.group(1)))
            html = self._http_get(ok_url, data='ok', headers={'Referer': referer}, cache_limit=.25)
            js_data = scraper_utils.parse_json(html, ok_url)
            stream_url = js_data.get('movie', {}).get('url')
            if stream_url is not None:
                host = urlparse.urlparse(stream_url).hostname
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': QUALITIES.HD720, 'views': None, 'rating': None, 'url': stream_url, 'direct': False, 'subs': 'Turkish Subtitles'}
                hosters.append(hoster)
        return hosters
    
    def _get_episode_url(self, show_url, video):
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=8)
        pattern = '''href=['"]([^'"]+)[^>]+>\s*%s\.\s*Sezon<''' % (video.season)
        match = re.search(pattern, html)
        if match:
            episode_pattern = '''href=['"]([^'"]+-%s-sezon-%s-bolum[^'"]*)''' % (video.season, video.episode)
            season_url = scraper_utils.urljoin(self.base_url, match.group(1))
            html = self._http_get(season_url, cache_limit=2)
            ep_url = self._default_get_episode_url(html, video, episode_pattern)
            if ep_url: return ep_url
        
        # front page fallback
        html = self._http_get(self.base_url, cache_limit=2)
        for slug in reversed(show_url.split('/')):
            if slug: break
            
        ep_url_frag = 'href="([^"]+/{slug}-{season}-sezon-{episode}-bolum[^"]*)'.format(slug=slug, season=video.season, episode=video.episode)
        match = re.search(ep_url_frag, html)
        if match:
            return scraper_utils.pathify_url(match.group(1))

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, cache_limit=8)
        norm_title = scraper_utils.normalize_title(title)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'all-tv-series-list'})
        if not fragment: return results
        
        for attrs, match_title in dom_parser2.parse_dom(fragment[0].content, 'a', req='href'):
            match_url = attrs['href']
            match_title = re.sub('</?i[^>]*>', '', match_title)
            if norm_title in scraper_utils.normalize_title(match_title):
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                results.append(result)

        return results
