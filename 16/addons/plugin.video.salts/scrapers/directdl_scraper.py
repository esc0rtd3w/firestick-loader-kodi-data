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
import urlparse

import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import Q_ORDER
from salts_lib.constants import VIDEO_TYPES
import scraper

logger = log_utils.Logger.get_logger()
BASE_URL = 'https://directdownload.tv'
SEARCH_URL = '/api?key=%s&%s&keyword=%s'
API_KEY = 'AFBF8E33A19787D1'

DD_QUALITIES = ['PDTV', 'DSR', 'DVDRIP', 'HDTV', '720P', 'WEBDL', 'WEBDL1080P', '1080P-X265']
Q_DICT = dict((quality, i) for i, quality in enumerate(DD_QUALITIES))
QUALITY_MAP = {'PDTV': QUALITIES.MEDIUM, 'DSR': QUALITIES.MEDIUM, 'DVDRIP': QUALITIES.HIGH,
               'HDTV': QUALITIES.HIGH, '720P': QUALITIES.HD720, 'WEBDL': QUALITIES.HD720, 'WEBDL1080P': QUALITIES.HD1080,
               '1080P-X265': QUALITIES.HD1080}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        qual_filter = 5 - int(kodi.get_setting('%s_quality' % VIDEO_TYPES.EPISODE))
        self.q_order = [dd_qual for dd_qual in DD_QUALITIES if Q_ORDER[QUALITY_MAP[dd_qual]] <= qual_filter]

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'DD.tv'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if not source_url or source_url == FORCE_NO_MATCH: return hosters
        url = scraper_utils.urljoin(self.base_url, source_url)
        html = self._http_get(url, cache_limit=.5)
        js_result = scraper_utils.parse_json(html, url)
        if 'error' in js_result:
            logger.log('DD.tv API error: "%s" @ %s' % (js_result['error'], url), log_utils.LOGWARNING)
            return hosters

        for result in js_result:
            if not scraper_utils.release_check(video, result['release'], require_title=False): continue
            if result['quality'] in self.q_order:
                for key in result['links']:
                    url = result['links'][key][0]
                    if re.search('\.rar(\.|$)', url):
                        continue
                    
                    hostname = urlparse.urlparse(url).hostname
                    hoster = {'multi-part': False, 'class': self, 'views': None, 'url': url, 'rating': None, 'host': hostname, 'quality': QUALITY_MAP[result['quality']], 'direct': False}
                    hoster['format'] = result['quality']
                    if 'x265' in result['release'] and result['quality'] != '1080P-X265': hoster['dd_qual'] += '-x265'
                    hosters.append(hoster)

        return hosters

    def get_url(self, video):
        url = None
        result = self.db_connection().get_related_url(video.video_type, video.title, video.year, self.get_name(), video.season, video.episode)
        if result:
            url = result[0][0]
            logger.log('Got local related url: |%s|%s|%s|%s|%s|' % (video.video_type, video.title, video.year, self.get_name(), url), log_utils.LOGDEBUG)
        else:
            date_match = False
            search_title = '%s S%02dE%02d' % (video.title, int(video.season), int(video.episode))
            results = self.search(video.video_type, search_title, '')
            if not results and video.ep_airdate is not None:
                search_title = '%s %s' % (video.title, video.ep_airdate.strftime('%Y.%m.%d'))
                results = self.search(video.video_type, search_title, '')
                date_match = True

            best_q_index = -1
            for result in results:
                if date_match and video.ep_airdate.strftime('%Y.%m.%d') not in result['title']:
                    continue
                
                if Q_DICT[result['quality']] > best_q_index:
                    best_q_index = Q_DICT[result['quality']]
                    url = result['url']
            self.db_connection().set_related_url(video.video_type, video.title, video.year, self.get_name(), url, video.season, video.episode)
        return url

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        settings = scraper_utils.disable_sub_check(settings)
        return settings

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = scraper_utils.urljoin(self.base_url, '/search?query=')
        search_url += title.replace("'", "")
        html = self._http_get(search_url, cache_limit=.25)
        js_result = scraper_utils.parse_json(html, search_url)
        if 'error' in js_result:
            logger.log('DD.tv API error: "%s" @ %s' % (js_result['error'], search_url), log_utils.LOGWARNING)
            return results
        
        for match in js_result:
            url = search_url + '&quality=%s' % match['quality']
            result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(match['release']), 'quality': match['quality'], 'year': ''}
            results.append(result)
        return results

    def _http_get(self, url, data=None, cache_limit=8):
        if 'search?query' in url:
            logger.log('Translating Search Url: %s' % (url), log_utils.LOGDEBUG)
            url = self.__translate_search(url)

        return super(self.__class__, self)._http_get(url, data=data, require_debrid=True, cache_limit=cache_limit)

    def __translate_search(self, url):
        query = scraper_utils.parse_query(url)
        if 'quality' in query:
            q_index = Q_DICT[query['quality']]
            q_list = [dd_qual for dd_qual in DD_QUALITIES if Q_DICT[dd_qual] <= q_index]
        else:
            q_list = self.q_order
        quality = '&'.join(['quality[]=%s' % (q) for q in q_list])
        return scraper_utils.urljoin(self.base_url, (SEARCH_URL % (API_KEY, quality, urllib.quote_plus(query['query']))))
