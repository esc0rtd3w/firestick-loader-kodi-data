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
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

logger = log_utils.Logger.get_logger(__name__)

BASE_URL = 'http://www.dizist1.com'
ALLOWED = [u'odnok', u'rodi', u'odnokaltyazısız', u'openload']

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
        return 'Dizist'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=1)
        pages = self.__get_alt_pages(html, page_url)
        sources = self.__get_sources(html, page_url, pages.get(page_url, True))
        for page in pages:
            if page == page_url: continue
            page_url = scraper_utils.urljoin(self.base_url, page, pages[page])
            html = self._http_get(page_url, cache_limit=1)
            sources.update(self.__get_sources(html, page, pages[page]))
            
        for stream_url, values in sources.iteritems():
            host = scraper_utils.get_direct_hostname(self, stream_url)
            if host == 'gvideo':
                quality = scraper_utils.gv_get_quality(stream_url)
                direct = True
            elif values['direct']:
                quality = values['quality']
                direct = True
            else:
                quality = values['quality']
                direct = False
                host = urlparse.urlparse(stream_url).hostname
            
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': direct}
            if values['subs']: hoster['subs'] = 'Turkish Subtitles'
            hosters.append(hoster)
                
        return hosters

    def __get_alt_pages(self, html, page_url):
        pages = {}
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'video-alternatives'})
        if fragment:
            active = dom_parser2.parse_dom(fragment[0].content, 'div', {'class': 'active'})
            for _attrs, div in dom_parser2.parse_dom(fragment[0].content, 'div'):
                match = re.search('href="([^"]+)[^>]>(.*?)</a>', div, re.DOTALL)
                if not match: continue
                
                alt_url, alt_label = match.groups()
                alt_label = alt_label.lower().strip()
                alt_label = re.sub('</?span>', '', alt_label)
                if alt_label not in ALLOWED: continue
                
                subs = False if u'altyazısız' in alt_label else True
                if active and active[0].content == div:
                    pages[page_url] = subs
                else:
                    pages[alt_url] = subs
                        
        return pages
    
    def __get_sources(self, html, page_url, subs):
        sources = {}
        player_div = dom_parser2.parse_dom(html, 'div', {'class': 'dzst-player'}, req='data-dzst-player')
        if player_div:
            js_html = scraper_utils.cleanse_title(player_div[0].attrs['data-dzst-player'].replace('&#x3D;', '='))
            js_data = scraper_utils.parse_json(js_html, page_url)
            links = js_data.get('tr', {})
            for height in links:
                stream_url = links[height]
                if scraper_utils.get_direct_hostname(self, stream_url) == 'gvideo':
                    quality = scraper_utils.gv_get_quality(stream_url)
                else:
                    quality = scraper_utils.height_get_quality(height)
                sources[stream_url] = {'direct': True, 'subs': subs, 'quality': quality}
        else:
            fragment = dom_parser2.parse_dom(html, 'div', {'class': 'video-player'})
            if fragment:
                fragment = fragment[0].content
                for _attrs, div in dom_parser2.parse_dom(fragment, 'div', {'class': 'ad-player'}):
                    fragment = fragment.replace(div, '')
    
                iframe_url = dom_parser2.parse_dom(fragment, 'iframe', req='src')
                if iframe_url:
                    iframe_url = iframe_url[0].attrs['src']
                    if 'dizist' in iframe_url:
                        html = self._http_get(iframe_url, headers={'Referer': page_url}, cache_limit=1)
                        return self.__get_sources(html, page_url, subs)
                    else:
                        parts = urlparse.urlparse(iframe_url)
                        if not parts.hostname:
                            iframe_url = scraper_utils.urljoin(self.base_url, iframe_url)
                            html = self._http_get(iframe_url, headers={'Referer': page_url}, cache_limit=1)
                            sources = scraper_utils.parse_sources_list(self, html, var='sources')
                            for value in sources.itervalues(): value['subs'] = subs
                        else:
                            if scraper_utils.get_direct_hostname(self, iframe_url) == 'gvideo':
                                direct = True
                            else:
                                direct = False
                            sources[iframe_url] = {'direct': direct, 'subs': subs, 'quality': QUALITIES.HD720}
                else:
                    sources = scraper_utils.parse_sources_list(self, fragment, var='sources')
                    for value in sources.itervalues(): value['subs'] = subs
            
        return sources
    
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+-%s-sezon-%s-bolum[^"]*)"' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+).*?class="ep-t">(?P<title>[^<]+)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, cache_limit=2)
        episodes = dom_parser2.parse_dom(html, 'div', {'class': 'episode-row'})
        fragment = '\n'.join(ep.content for ep in episodes)
        return self._default_get_episode_url(fragment or html, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        url = scraper_utils.urljoin(self.base_url, '/arsiv')
        html = self._http_get(url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        fragment = dom_parser2.parse_dom(html, 'div', {'class': 'ts-list-content'})
        if not fragment: return results
        
        items = dom_parser2.parse_dom(fragment[0].content, 'h1', {'class': 'ts-list-name'})
        details = dom_parser2.parse_dom(fragment[0].content, 'ul')
        for item, detail in zip(items, details):
            match = dom_parser2.parse_dom(item.content, 'a', req='href')
            match_year = re.search('<span>(\d{4})</span>', detail.content)
            if not match: continue

            match_url = match[0].attrs['href']
            match_title = match[0].content
            match_year = match_year.group(1) if match_year else ''
            
            if norm_title in scraper_utils.normalize_title(match_title):
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)

        return results
