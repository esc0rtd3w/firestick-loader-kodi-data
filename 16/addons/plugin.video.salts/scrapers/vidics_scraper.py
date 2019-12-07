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
import urllib
import re
import urllib2
import kodi
import log_utils  # @UnusedImport
import dom_parser2
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

logger = log_utils.Logger.get_logger(__name__)

BASE_URL = 'https://www.vidics.to'
FRAGMENTS = {VIDEO_TYPES.MOVIE: '/film/', VIDEO_TYPES.TVSHOW: '/serie/'}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'vidics.ch'

    def resolve_link(self, link):
        url = scraper_utils.urljoin(self.base_url, link)
        request = urllib2.Request(url)
        request.add_header('User-Agent', scraper_utils.get_ua())
        request.add_unredirected_header('Host', request.get_host())
        request.add_unredirected_header('Referer', url)
        response = urllib2.urlopen(request)
        return response.geturl()

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        headers = {'Referer': self.base_url}
        html = self._http_get(url, headers=headers, cache_limit=.5)
        for _attrs, fragment in dom_parser2.parse_dom(html, 'div', {'class': 'lang'}):
            section_label = dom_parser2.parse_dom(fragment, 'div', {'title': re.compile('Language Flag\s+[^"]*')})
            lang, subs = self.__get_section_label(section_label)
            if lang.lower() == 'english':
                for attrs, host in dom_parser2.parse_dom(fragment, 'a', {'class': 'p1'}, req='href'):
                    stream_url = attrs['href']
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': host, 'rating': None, 'views': None, 'direct': False}
                    if subs: hoster['subs'] = subs
                    hosters.append(hoster)

        return hosters

    def __get_section_label(self, label):
        lang, subs = '', ''
        if label:
            label = label[0].attrs['title']
            label = re.sub(re.compile('^Language Flag\s*', re.I), '', label)
            match = re.search('(-(.*?) SUBS)', label)
            if match:
                subs = match.group(2) + ' Subtitles'
                lang = re.sub(match.group(1), '', label)
            else:
                lang = label
            
        return lang, subs
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        search_url = '/Category-FilmsAndTV/Genre-Any/Letter-Any/ByPopularity/1/Search-%s.htm' % (urllib.quote(title))
        search_url = scraper_utils.urljoin(self.base_url, search_url)
        html = self._http_get(search_url, cache_limit=8)

        results = []
        for _attrs, result in dom_parser2.parse_dom(html, 'div', {'class': 'searchResult'}):
            match_url = dom_parser2.parse_dom(result, 'a', {'itemprop': 'url'}, req='href')
            match_title = dom_parser2.parse_dom(result, 'span', {'itemprop': 'name'})
            match_year = dom_parser2.parse_dom(result, 'span', {'itemprop': 'copyrightYear'})
            match_year = match_year[0].content if match_year else ''
            
            if match_url and match_title and (not year or not match_year or year == match_year):
                match_url = match_url[0].attrs['href']
                match_title = match_title[0].content
                if FRAGMENTS[video_type] not in match_url.lower(): continue
                result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+-Season-%s-Episode-%s)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+).*?class="episode_title">\s*-\s*(?P<title>.*?)\s+\('
        airdate_pattern = 'href="([^"]+)(?:[^>]+>){2}[^<][^<]+\({year} {month_name} {p_day}\)'
        show_url = scraper_utils.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, headers={'Referer': self.base_url}, cache_limit=2)
        parts = dom_parser2.parse_dom(html, 'div', {'class': 'season'})
        fragment = '\n'.join(part.content for part in parts)
        return self._default_get_episode_url(fragment, video, episode_pattern, title_pattern, airdate_pattern)
