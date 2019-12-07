
import re
import string
import urlparse
from libs import kodi
from libs import dom_parser
import scraper_utils
from libs.constants import FORCE_NO_MATCH
from libs.constants import QUALITIES
from libs.constants import VIDEO_TYPES
from libs.constants import XHR
import main_scrape
import scrapeit

BASE_URL = 'http://afdah.tv'


BASE_URL = kodi.get_setting('afdah_base_url')


class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('afdah_base_url')
        #kodi.log(self.base_url)

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'afdah'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            match = re.search('This movie is of poor quality', html, re.I)
            if match:
                quality = QUALITIES.LOW
            else:
                quality = QUALITIES.HIGH

            for match in re.finditer('href="([^"]+/embed\d*/[^"]+)', html):
                url = match.group(1)
                embed_html = self._http_get(url, cache_limit=.5)
                hosters += self.__get_links(embed_html)

            pattern = 'href="([^"]+)[^>]*>\s*<[^>]+play_video.gif'
            for match in re.finditer(pattern, html, re.I):
                stream_url = match.group(1)
                host = urlparse.urlparse(stream_url).hostname
                quality = scraper_utils.get_quality(video, host, quality)
                hoster = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality,
                          'rating': None, 'views': None, 'direct': False}
                hosters.append(hoster)
        return hosters

    def __get_links(self, html):
        hosters = []
        r = re.search('salt\("([^"]+)', html)
        if r:
            plaintext = self.__caesar(self.__get_f(self.__caesar(r.group(1), 13)), 13)
            sources = self._parse_sources_list(plaintext)
            for source in sources:
                stream_url = source + scraper_utils.append_headers(
                    {'User-Agent': scraper_utils.get_ua(), 'Cookie': self._get_stream_cookies()})
                host = self._get_direct_hostname(stream_url)
                hoster = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self,
                          'quality': sources[source]['quality'], 'rating': None, 'views': None, 'direct': True}
                hosters.append(hoster)
        return hosters

    def __caesar(self, plaintext, shift):
        lower = string.ascii_lowercase
        lower_trans = lower[shift:] + lower[:shift]
        alphabet = lower + lower.upper()
        shifted = lower_trans + lower_trans.upper()
        return plaintext.translate(string.maketrans(alphabet, shifted))

    def __get_f(self, s):
        i = 0
        t = ''
        l = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
        while i < len(s):
            try:
                c1 = l.index(s[i])
                c2 = l.index(s[i + 1])
                t += chr(c1 << 2 & 255 | c2 >> 4)
                c3 = l.index(s[i + 2])
                t += chr(c2 << 4 & 255 | c3 >> 2)
                c4 = l.index(s[i + 3])
                t += chr(c3 << 6 & 255 | c4)
                i += 4
            except:
                break

        return t

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/wp-content/themes/afdah/ajax-search.php')
        data = {'search': title, 'type': 'title'}
        html = self._http_get(search_url, data=data, headers=XHR, cache_limit=1)
        for item in dom_parser.parse_dom(html, 'li'):
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            match_title_year = dom_parser.parse_dom(item, 'a')
            if match_url and match_title_year:
                match_url = match_url[0]
                match_title, match_year = scraper_utils.extra_year(match_title_year[0])
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url),
                              'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results
