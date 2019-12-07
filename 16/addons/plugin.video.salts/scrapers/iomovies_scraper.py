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
import json
import re
import time
import random
import hashlib
import scraper
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib import jsunpack
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import XHR
from salts_lib.constants import QUALITIES

logger = log_utils.Logger.get_logger()
BASE_URL = 'http://iomovies.net'
VID_URL = '/api/get_episode/{data_i}/{data_e}'

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
        return 'IOMovies'

    def get_sources(self, video):
        sources = []
        streams = {}
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return sources
        
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=8)
        match = dom_parser2.parse_dom(html, 'a', {'title': re.compile('click to play', re.I)}, req='href')
        if not match: return sources
        
        page_url = scraper_utils.urljoin(self.base_url, match[0].attrs['href'])
        headers = {'Referer': page_url}
        html = self._http_get(page_url, headers=headers, cache_limit=.02)
        for attrs, _content in dom_parser2.parse_dom(html, 'a', {'class': 'mw-episode-btn'}, req=['data-target-i', 'data-target-e', 'title']):
            try:
                if "wasn't alive" in attrs['title']: continue
                vid_url = scraper_utils.urljoin(self.base_url, VID_URL)
                vid_url = vid_url.format(data_i=attrs['data-target-i'], data_e=attrs['data-target-e'])
                headers = {'Referer': page_url}
                headers.update(XHR)
                cookies = self.__get_cookies(html, attrs)
                vid_html = self._http_get(vid_url, headers=headers, cookies=cookies, cache_limit=.02)
                streams.update(self.__get_js_sources(vid_html, vid_url, cookies, page_url))
            except scraper.ScrapeError as e:
                logger.log('IOMovies Error (%s): %s in %s' % (e, vid_url, page_url))
                    
        for stream_url, values in streams.iteritems():
            if values['direct']:
                host = scraper_utils.get_direct_hostname(self, stream_url)
                if host == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                else:
                    quality = scraper_utils.height_get_quality(values['label'])
                    stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            else:
                host = urlparse.urlparse(stream_url).hostname
                quality = QUALITIES.HIGH
                 
            source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': values['direct']}
            sources.append(source)

        return sources

    def __get_js_sources(self, html, url, cookies, page_url, allow_framed=True):
        streams = {}
        js_data = scraper_utils.parse_json(html, url)
        for key, stream_url in js_data.get('data', {}).get('sources', {}).iteritems():
            if key == 'framed' and allow_framed:
                streams.update(self.__get_framed_streams(url, cookies, stream_url, page_url))
            elif key == 'OpenLoad':
                direct = False
            else:
                direct = True
            if not stream_url.startswith('http'): continue
            streams[stream_url] = {'label': key, 'direct': direct}
        return streams
            
    def __get_framed_streams(self, vid_url, cookies, html, page_url):
        streams = {}
        iframe_url = dom_parser2.parse_dom(html, 'iframe', req='src')
        if not iframe_url: raise scraper.ScrapeError('No Iframe in: %s' % (vid_url))

        iframe_url = iframe_url[0].attrs['src']
        html = self._http_get(iframe_url, headers={'Referer': page_url}, cache_limit=.02)
        match = re.search('getScript\("([^"]+)', html)
        if not match: raise scraper.ScrapeError('No Script in: %s' % (iframe_url))
            
        script_url = match.group(1)
        html = self._http_get(script_url, headers={'Referer': iframe_url}, cache_limit=.02)
        match = re.search("responseJson\s*=\s*'([^']+)", html)
        if not match: raise scraper.ScrapeError('No JSON in: %s' % (script_url))

        js_data = scraper_utils.parse_json(match.group(1), script_url)
        media = js_data.get('medias', {})
        if media:
            headers = {'Referer': page_url}
            headers.update(XHR)
            data = {'data': json.dumps({'medias': media, 'original': ''})}
            vid_html = self._http_get(vid_url, data=data, headers=headers, cookies=cookies, cache_limit=.02)
            streams.update(self.__get_js_sources(vid_html, vid_url, cookies, page_url, allow_framed=False))
            
        return streams

    def __get_cookies(self, html, attrs):
        ts = int(time.time()) - random.randint(1, 60)
        token = hashlib.md5(self.__get_slice(html) + attrs['data-target-e'] + attrs['data-target-i'] + str(ts)).hexdigest()
        return {'timestamp': ts, 'token': token}
    
    def __get_slice(self, html):
        alphabet = re.search("alphabet\s*=\s*'([^']+)", html)
        if not alphabet: raise scraper.ScrapeError('No Alphabet Found')
        
        alphabet = alphabet.group(1)
        js_code = ''
        for match in re.finditer('(eval\(function\(.*?)</script>', html, re.DOTALL):
            js_data = jsunpack.unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            js_code += js_data
        
        if 'charCodeAt' in js_code:
            s = self.__get_slice1(js_code, alphabet)
        else:
            s = self.__get_slice2(js_code, alphabet)

        return s
        
    def __get_slice1(self, js_code, alphabet):
        values = {}
        for var in re.finditer("var\s+([^=]+)='([^']+)'\.charCodeAt\((\d+)\)", js_code):
            values[var.group(1)] = ord(var.group(2)[int(var.group(3))])
        if not values: raise scraper.ScrapeError('No Vars in js_data')

        match = re.search('slice\(([^,]+),([^)]+)\)', js_code)
        if not match: raise scraper.ScrapeError('No Slice in js_data')
        
        start, end = match.groups()
        for key, value in values.iteritems():
            start = start.replace(key, str(value))
            end = end.replace(key, str(value))
        
        try:
            start = eval(start)
            end = eval(end)
        except Exception as e:
            raise scraper.ScrapeError('Eval Failed (%s): |%s|%s|' % (e, start, end))

        return alphabet[start: end]
    
    def __get_slice2(self, js_code, alphabet):
        s = ''
        alpha_len = str(len(alphabet))
        for match in re.finditer('slice\(([^,]+),([^)]+)\)', js_code):
            start, end = match.groups()
            start = start.replace('input.length', alpha_len)
            end = end.replace('input.length', alpha_len)
            try:
                start = eval(start)
                end = eval(end)
            except Exception as e:
                raise scraper.ScrapeError('Eval Failed (%s): |%s|%s|' % (e, start, end))

            s += alphabet[start: end]
        
        if not s: raise scraper.ScrapeError('No Slice from: %s' % (js_code))
        return s
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search')
        html = self._http_get(search_url, params={'q': title}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'movie-item'}):
            match = dom_parser2.parse_dom(item, 'a', {'itemprop': 'url'}, req='href')
            if not match: continue

            match_url, match_title_year = match[0].attrs['href'], match[0].content
            match_title, match_year = scraper_utils.extra_year(match_title_year)
            if not match_year:
                try: match_year = dom_parser2.parse_dom(item, 'div', {'class': 'overlay-year'})[0].content
                except: match_year = ''
                    
            if not year or not match_year or year == match_year:
                result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                results.append(result)

        return results
