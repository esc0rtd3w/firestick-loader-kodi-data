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
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'https://www.hdmoviefree.org'
SERVER_URL = '/ajax/loadsv/%s'
EP_URL = '/ajax/loadep/%s'
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
        return 'HDMovieFree'

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if not source_url or source_url == FORCE_NO_MATCH: return sources
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=8)
        for attrs, _content in dom_parser2.parse_dom(html, 'img', req=['data-id', 'data-name']):
            film_id, data_name = attrs['data-id'], attrs['data-name']
            data = {'id': film_id, 'n': data_name}
            server_url = scraper_utils.urljoin(self.base_url, SERVER_URL)
            server_url = server_url % (film_id)
            headers = {'Referer': page_url}
            headers.update(XHR)
            html = self._http_get(server_url, data=data, headers=headers, cache_limit=.5)
            for attrs, _content in dom_parser2.parse_dom(html, 'a', req='data-id'):
                data = {'epid': attrs['data-id']}
                ep_url = scraper_utils.urljoin(self.base_url, EP_URL)
                ep_url = ep_url % (attrs['data-id'])
                headers = {'Referer': page_url}
                headers.update(XHR)
                html = self._http_get(ep_url, data=data, headers=headers, cache_limit=.5)
                js_data = scraper_utils.parse_json(html, ep_url)
                try:
                    links = [r.attrs['src'] for r in dom_parser2.parse_dom(js_data['link']['embed'], 'iframe', req='src')]
                except:
                    try: links = js_data['link']['l']
                    except: links = []
                try: heights = js_data['link']['q']
                except: heights = []
                for stream_url, height in map(None, links, heights):
                    match = re.search('movie_url=(.*)', stream_url)
                    if match:
                        stream_url = match.group(1)
                        
                    host = scraper_utils.get_direct_hostname(self, stream_url)
                    if host == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                        stream_url += scraper_utils.append_headers({'User-Agent': scraper_utils.get_ua(), 'Referer': page_url})
                        direct = True
                    else:
                        host = urlparse.urlparse(stream_url).hostname
                        if height:
                            quality = scraper_utils.height_get_quality(height)
                        else:
                            quality = QUALITIES.HD720
                        direct = False
                    source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                    sources.append(source)

        return sources

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search/%s.html')
        search_url = search_url % (scraper_utils.to_slug(title))
        html = self._http_get(search_url, cache_limit=8)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'slideposter'}):
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_title_year = dom_parser2.parse_dom(item, 'img', req='alt')
            if match_url and match_title_year:
                match_url = match_url[0].attrs['href']
                match_title_year = match_title_year[0].attrs['alt']
                match_title, match_year = scraper_utils.extra_year(match_title_year)
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)

        return results

    def __to_slug(self, title):
        slug = title.lower()
        slug = re.sub('[^A-Za-z0-9 -]', ' ', slug)
        slug = re.sub('\s\s+', ' ', slug)
        slug = re.sub(' ', '-', slug)
        return slug
