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
import scraper


BASE_URL = 'http://onlinedizi.com'

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
        return 'OnlineDizi'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        page_url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(page_url, cache_limit=.25)
        fragment = dom_parser2.parse_dom(html, 'ul', {'class': 'dropdown-menu'})
        if not fragment: return hosters
        
        for match in re.finditer('''href=['"]([^'"]+)[^>]*>(Altyaz.{1,3}s.{1,3}z|ok\.ru|openload)<''', fragment[0].content, re.I):
            sources = []
            subs = True if not match.group(2).startswith('Altyaz') else False
            option_url = scraper_utils.urljoin(self.base_url, match.group(1))
            html = self._http_get(option_url, cache_limit=2)
            fragment = dom_parser2.parse_dom(html, 'div', {'class': 'video-player'})
            if not fragment: continue
            
            iframes = dom_parser2.parse_dom(fragment[0].content, 'iframe', req='src')
            for attrs, _content in iframes:
                iframe_url = attrs['src']
                if attrs.get('id') == 'ifr':
                    html = self._http_get(iframe_url, allow_redirect=False, method='HEAD', cache_limit=.25)
                    if html.startswith('http'):
                        sources.append({'stream_url': html, 'subs': subs})
                else:
                    html = self._http_get(iframe_url, cache_limit=.25)
                    for match in re.finditer('"((?:\\\\x[A-Fa-f0-9]+)+)"', html):
                        s = match.group(1).replace('\\x', '').decode('hex')
                        if s.startswith('http'):
                            s = urllib.unquote(s)
                            match = re.search('videoPlayerMetadata&mid=(\d+)', s)
                            if match:
                                s = 'http://ok.ru/video/%s' % (match.group(1))
                                sources.append({'stream_url': s, 'subs': subs})

                    iframes += dom_parser2.parse_dom(html, 'iframe', req='src')
                        
            for source in sources:
                stream_url = source['stream_url']
                host = urlparse.urlparse(stream_url).hostname
                quality = QUALITIES.HIGH
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                if source['subs']: hoster['subs'] = 'Turkish Subtitles'
                hosters.append(hoster)
    
        return hosters

    def _get_episode_url(self, show_url, video):
        season_url = show_url
        if video.season != 1:
            show_url = scraper_utils.urljoin(self.base_url, show_url)
            html = self._http_get(show_url, cache_limit=24)
            fragment = dom_parser2.parse_dom(html, 'div', {'class': 'page-numbers'})
            if fragment:
                match = re.search('href="([^"]+-%s-sezon[^"]*)' % (video.season), fragment[0].content)
                if match:
                    season_url = match.group(1)
            
        episode_pattern = '''href=['"]([^'"]+-%s-sezon-%s-bolum[^'"]*)''' % (video.season, video.episode)
        season_url = scraper_utils.urljoin(self.base_url, season_url)
        html = self._http_get(season_url, cache_limit=2)
        fragment = dom_parser2.parse_dom(html, 'ul', {'class': 'posts-list'})
        return self._default_get_episode_url(fragment or html, video, episode_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        seen_urls = set()
        search_url = scraper_utils.urljoin(self.base_url, '/yabanci-diziler/')
        html = self._http_get(search_url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        for _attrs, item in dom_parser2.parse_dom(html, 'div', {'class': 'category-post'}):
            match_url = dom_parser2.parse_dom(item, 'a', req='href')
            match_title = dom_parser2.parse_dom(item, 'h3')
            if match_url and match_title:
                match_url = scraper_utils.pathify_url(match_url[0].attrs['href'])
                match_title = match_title[0].content
                if match_url in seen_urls: continue
                seen_urls.add(match_url)
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': match_url, 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results
