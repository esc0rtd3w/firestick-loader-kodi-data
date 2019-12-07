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
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
import scraper

VIDEO_URL = '/video_info/iframe'

class Scraper(scraper.Scraper):
    OPTIONS = ['https://xmovies8.org', 'https://putlockerhd.co', 'https://afdah.org', 'https://watch32hd.co']
    
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'xmovies8'

    def resolve_link(self, link):
        link = link.split('|', 1)[0]
        html = self._http_get(link, allow_redirect=False, method='HEAD', cache_limit=0)
        if html.startswith('http'):
            return html
        else:
            return link

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=0)
        match = re.search('var\s*video_id\s*=\s*"([^"]+)', html)
        if not match: return hosters
        
        video_id = match.group(1)
        headers = {'Referer': page_url}
        headers.update(XHR)
        _html = self._http_get(scraper_utils.urljoin(self.base_url, 'av'), headers=headers, method='POST', cache_limit=0)
        
        vid_url = scraper_utils.urljoin(self.base_url, VIDEO_URL)
        html = self._http_get(vid_url, data={'v': video_id}, headers=headers, cache_limit=0)
        for source, value in scraper_utils.parse_json(html, vid_url).iteritems():
            match = re.search('url=(.*)', value)
            if not match: continue
            stream_url = urllib.unquote(match.group(1))

            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
            else:
                quality = scraper_utils.height_get_quality(source)
            stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua()})
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
            hosters.append(hoster)
        return hosters
        
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/results')
        params = {'q': title}
        referer = search_url + '?' + urllib.urlencode(params)
        headers = {'Referer': referer}
        headers.update(XHR)
        _html = self._http_get(scraper_utils.urljoin(self.base_url, 'av'), headers=headers, method='POST', cache_limit=0)

        cookies = {'begin_referer': referer, 'prounder': 1}
        html = self._http_get(search_url, params=params, cookies=cookies, cache_limit=8)
        if any('jquery.js' in match.attrs['src'] for match in dom_parser2.parse_dom(html, 'script', req='src')):
            html = self._http_get(search_url, params=params, cookies=cookies, cache_limit=0)
            
        for _attrs, result in dom_parser2.parse_dom(html, 'div', {'class': 'cell'}):
            title_frag = dom_parser2.parse_dom(result, 'div', {'class': 'video_title'})
            year_frag = dom_parser2.parse_dom(result, 'div', {'class': 'video_quality'})
            if not title_frag: continue
            match = dom_parser2.parse_dom(title_frag[0].content, 'a', req='href')
            if not match: continue
            match_url = match[0].attrs['href']
            match_title = match[0].content
            try:
                match = re.search('\s+(\d{4})\s+', year_frag[0].content)
                match_year = match.group(1)
            except:
                match_year = ''

            if not year or not match_year or year == match_year:
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)
        return results

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings.append('         <setting id="%s-default_url" type="text" visible="false"/>' % (cls.get_name()))
        return settings

scraper_utils.set_default_url(Scraper)
