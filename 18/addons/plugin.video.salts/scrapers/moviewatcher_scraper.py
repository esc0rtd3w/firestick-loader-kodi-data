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
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib import pyaes
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

logger = log_utils.Logger.get_logger(__name__)
BASE_URL = 'http://moviewatcher.io'

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
        return 'MovieWatcher'

    def resolve_link(self, link):
        url = scraper_utils.urljoin(self.base_url, link)
        html = self._http_get(url, allow_redirect=False, cache_limit=0)
        if html.startswith('http'):
            return html
        else:
            return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=1)
        for _attrs, item in dom_parser2.parse_dom(html, 'a', {'class': 'full-torrent1'}):
            stream_url = dom_parser2.parse_dom(item, 'span', req='onclick')
            host = dom_parser2.parse_dom(item, 'div', {'class': 'small_server'})
            match = re.search('Views:\s*(?:</[^>]*>)?\s*(\d+)', item, re.I)
            views = match.group(1) if match else None
            match = re.search('Size:\s*(?:</[^>]*>)?\s*(\d+)', item, re.I)
            size = int(match.group(1)) * 1024 * 1024 if match else None
            if not stream_url or not host: continue
            
            stream_url = stream_url[0].attrs['onclick']
            host = host[0].content.lower()
            host = host.replace('stream server: ', '')
            match = re.search("'(/redirect/[^']+)", stream_url)
            if match: stream_url = match.group(1)
            quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': views, 'rating': None, 'url': stream_url, 'direct': False}
            if size is not None: hoster['size'] = scraper_utils.format_size(size, 'B')
            hosters.append(hoster)
        return hosters

    def _get_episode_url(self, show_url, video):
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'div', {'id': 'show_season%s' % (video.season)})
        episode_pattern = 'href="([^"]+)[^>]*>0*%s<' % (video.episode)
        return self._default_get_episode_url(fragment, video, episode_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search')
        search_type = 'movies' if video_type == VIDEO_TYPES.MOVIE else 'series'
        html = self._http_get(search_url, params={'query': title.lower(), 'type': search_type}, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'one_movie-item'}):
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_title = dom_parser2.parse_dom(item, 'img', req='alt')
            media_type = dom_parser2.parse_dom(item, 'div', {'class': 'movie-series'})
            if not media_type:
                media_type = VIDEO_TYPES.MOVIE
            elif media_type[0].content == 'TV SERIE':
                media_type = VIDEO_TYPES.TVSHOW
                
            if match_url and match_title and video_type == media_type:
                match_url = match_url[0].attrs['href']
                match_title = match_title[0].attrs['alt']
                
                match_year = re.search('-(\d{4})-', match_url)
                if match_year:
                    match_year = match_year.group(1)
                else:
                    match_year = ''
        
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results

    def _http_get(self, url, params=None, data=None, multipart_data=None, headers=None, cookies=None, allow_redirect=True, method=None, require_debrid=False, read_error=False, cache_limit=8):
        html = super(self.__class__, self)._http_get(url, params=params, data=data, multipart_data=multipart_data, headers=headers, cookies=cookies, allow_redirect=allow_redirect, method=method, require_debrid=require_debrid, read_error=read_error, cache_limit=cache_limit)
        if 'toNumbers' in html:
            if cookies is None: cookies = {}
            cookies.update(self.__get_cookie(html))
            logger.log('Cookie JS Detected: %s' % (cookies), log_utils.LOGDEBUG)
            html = super(self.__class__, self)._http_get(url, params=params, data=data, multipart_data=multipart_data, headers=headers, cookies=cookies, allow_redirect=allow_redirect, method=method, require_debrid=require_debrid, read_error=read_error, cache_limit=0)
        
        return html
            
    def __get_cookie(self, html):
        try:
            in_vars = [self.__to_numbers(match.group(1)) for match in re.finditer('toNumbers\("([^"]+)', html)]
            aes_key, iv, message = in_vars
            match = re.search('cookie="([^=]+)', html)
            try: key = match.group(1)
            except: key = 'BPC'
            value = self.__to_hex(self.__decrypt(message, aes_key, iv))
            return {key: value}
        except ValueError:
            return {}

    def __to_numbers(self, s):
        return s.decode('hex')
    
    def __to_hex(self, s):
        return s.encode('hex')
    
    def __decrypt(self, message, key, iv):
        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
        plain_text = decrypter.feed(message)
        plain_text += decrypter.feed()
        plain_text = plain_text.split('\0', 1)[0]
        return plain_text
