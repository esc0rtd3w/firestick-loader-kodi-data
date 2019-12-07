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
import urllib
import urllib2
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://sezonlukdizi.net'
SEASON_URL = '/ajax/dataDizi.asp'
EMBED_URL = '/ajax/dataEmbed.asp'
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
        return 'SezonLukDizi'

    def resolve_link(self, link):
        if 'v.asp' in link:
            try:
                headers = dict([item.split('=') for item in (link.split('|')[1]).split('&')])
                for key in headers: headers[key] = urllib.unquote(headers[key])
            except:
                headers = {}
            request = urllib2.Request(link.split('|')[0], headers=headers)
            response = urllib2.urlopen(request)
            return response.geturl()
        else:
            return link
            
    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'playerMenu'})
        if not fragment: return hosters
        
        sources = []
        for attrs, _content in dom_parser2.parse_dom(fragment[0].content, 'div', {'class': 'item'}, req='data-id'):
            data_id = attrs['data-id']
            headers = {'Referer': page_url}
            headers.update(XHR)
            embed_url = scraper_utils.urljoin(self.base_url, EMBED_URL)
            html = self._http_get(embed_url, data={'id': data_id}, headers=headers, cache_limit=.5)
            iframe_url = dom_parser2.parse_dom(html, 'iframe', req='src')
            if not iframe_url: continue
            
            iframe_url = iframe_url[0].attrs['src']
            if urlparse.urlparse(self.base_url).hostname in iframe_url:
                sources += self.__get_direct_links(iframe_url, page_url)
            else:
                sources += [{'stream_url': iframe_url, 'subs': 'Turkish subtitles', 'quality': QUALITIES.HIGH, 'direct': False}]
                            
        for source in sources:
            if source['direct']:
                stream_url = source['stream_url'] + scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
                host = scraper_utils.get_direct_hostname(self, stream_url)
                if host == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                else:
                    quality = source['quality']
            else:
                stream_url = source['stream_url']
                host = urlparse.urlparse(stream_url).hostname
                quality = source['quality']
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': source['direct'], 'subs': source['subs']}
            hosters.append(hoster)

        return hosters
    
    def __get_direct_links(self, iframe_url, page_url):
        sources = []
        headers = {'Referer': page_url}
        html = self._http_get(iframe_url, headers=headers, cache_limit=.5)
        
        # if captions exist, then they aren't hardcoded
        subs = '' if re.search('kind\s*:\s*"captions"', html) else 'Turkish subtitles'
         
        streams = scraper_utils.parse_sources_list(self, html, key='VideoSources')
        streams.update(scraper_utils.parse_sources_list(self, html, var='video'))
        for stream_url in streams:
            quality = streams[stream_url]['quality']
            if 'v.asp' in stream_url:
                stream_url = scraper_utils.urljoin(self.base_url, stream_url)
                stream_redirect = self._http_get(stream_url, allow_redirect=False, method='HEAD', cache_limit=0)
                if stream_redirect.startswith('http'):
                    stream_url = stream_redirect

            sources.append({'stream_url': stream_url, 'subs': subs, 'quality': quality, 'direct': True})
        
        if sources: return sources
        iframe_url = dom_parser2.parse_dom(html, 'iframe', req='src')
        if not iframe_url: return sources
        sources.append({'stream_url': iframe_url[0].attrs['src'], 'subs': subs, 'quality': QUALITIES.HD720, 'direct': False})
                
        return sources
    
    def _get_episode_url(self, show_url, video):
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        headers = {'Referer': self.base_url}
        html = self._http_get(show_url, headers=headers, cache_limit=.25)
        data = dom_parser2.parse_dom(html, 'div', {'id': 'dizidetay'}, req=['data-dizi', 'data-id'])
        if not data: return
        
        episode_pattern = '''href=['"]([^'"]*/%s-sezon-%s-[^'"]*bolum[^'"]*)''' % (video.season, video.episode)
        title_pattern = '''href=['"](?P<url>[^'"]+)[^>]*>(?P<title>[^<]+)'''
        airdate_pattern = '''href=['"]([^"']+)[^>]*>[^<]*</a>\s*</td>\s*<td class="right aligned">{p_day}\.{p_month}\.{year}'''

        season_url = scraper_utils.urljoin(self.base_url, SEASON_URL)
        queries = {'sekme': 'bolumler', 'id': data[0].attrs['data-id'], 'dizi': data[0].attrs['data-dizi']}
        headers = {'Referer': show_url, 'Content-Length': 0}
        headers.update(XHR)

        html = self._http_get(season_url, params=queries, headers=headers, method='POST', cache_limit=2)
        result = self._default_get_episode_url(html, video, episode_pattern, title_pattern, airdate_pattern)
        if result and 'javascript:;' not in result:
            return result

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, cache_limit=24)
        norm_title = scraper_utils.normalize_title(title)
        for attrs, _content in dom_parser2.parse_dom(html, 'script', {'type': 'text/javascript'}, req='src'):
            html = self._http_get(attrs['src'], cache_limit=48)
            match_year = ''
            for match in re.finditer('d\s*:\s*"([^"]+).*?u\s*:\s*"([^"]+)', html):
                match_title, match_url = match.groups()
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results
