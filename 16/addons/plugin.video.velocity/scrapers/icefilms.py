import random
import re
import string
import urllib
import urlparse
from libs import log_utils
from libs import kodi
import scraper_utils
import scrapeit
from libs import dom_parser
import main_scrape


def __enum(**enums):
    return type('Enum', (), enums)

FORCE_NO_MATCH = '***FORCE_NO_MATCH***'
QUALITIES = __enum(LOW='Low', MEDIUM='Medium', HIGH='High', HD720='HD720', HD1080='HD1080')
VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')



BASE_URL = kodi.get_setting('icefilms_base_url')

QUALITY_MAP = {'HD': QUALITIES.HIGH, 'HDTV': QUALITIES.HIGH, 'DVD': QUALITIES.HIGH, '3D': QUALITIES.HIGH,'CAM': QUALITIES.LOW}




QUALITY_MAP = {'HD720P': QUALITIES.HD720, 'HD720P+': QUALITIES.HD720, 'DVDRIP/STANDARDDEF': QUALITIES.HIGH,
               'SD/DVD480P': QUALITIES.HIGH, 'DVDSCREENER': QUALITIES.HIGH, 'FASTSTREAM/LOWQUALITY': QUALITIES.HIGH}

LIST_URL = BASE_URL + '/membersonly/components/com_iceplayer/video.php?h=374&w=631&vid=%s&img='
AJAX_URL = '/membersonly/components/com_iceplayer/video.phpAjaxResp.php?id=%s&s=%s&iqs=&url=&m=%s&cap= &sec=%s&t=%s'


class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('icefilms_base_url')

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'IceFilms'

    def resolve_link(self, link):
        url, query = link.split('?', 1)
        data = urlparse.parse_qs(query, True)
        url = urlparse.urljoin(self.base_url, url)
        url += '?s=%s&t=%s&app_id=SALTS' % (data['id'][0], data['t'][0])
        list_url = LIST_URL % (data['t'][0])
        headers = {'Referer': list_url}
        html = self._http_get(url, data=data, headers=headers, cache_limit=.25)
        match = re.search('url=(http.*)', html)
        if match:
            url = urllib.unquote_plus(match.group(1))
            return url

    def get_sources(self, video, video_type):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            try:
                url = urlparse.urljoin(self.base_url, source_url)
                html = self._http_get(url, cache_limit=2)

                pattern = '<iframe id="videoframe" src="([^"]+)'
                match = re.search(pattern, html)
                url = urlparse.urljoin(self.base_url, match.group(1))
                html = self._http_get(url, cache_limit=.5)

                match = re.search('lastChild\.value="([^"]+)"(?:\s*\+\s*"([^"]+))?', html)
                secret = ''.join(match.groups(''))

                match = re.search('"&t=([^"]+)', html)
                t = match.group(1)

                match = re.search('(?:\s+|,)s\s*=(\d+)', html)
                s_start = int(match.group(1))

                match = re.search('(?:\s+|,)m\s*=(\d+)', html)
                m_start = int(match.group(1))

                for fragment in dom_parser.parse_dom(html, 'div', {'class': 'ripdiv'}):
                    match = re.match('<b>(.*?)</b>', fragment)
                    if match:
                        q_str = match.group(1).replace(' ', '').upper()
                        quality = QUALITY_MAP.get(q_str, QUALITIES.HIGH)
                    else:
                        quality = QUALITIES.HIGH

                    pattern = '''onclick='go\((\d+)\)'>([^<]+)(<span.*?)</a>'''
                    for match in re.finditer(pattern, fragment):
                        link_id, label, host_fragment = match.groups()
                        source = {'hostname':'IceFilms','multi-part': False, 'quality': quality, 'class': '', 'version': label,
                                  'rating': None, 'views': None, 'direct': False}
                        source['host'] = re.sub('(</?[^>]*>)', '', host_fragment)
                        s = s_start + random.randint(3, 1000)
                        m = m_start + random.randint(21, 1000)
                        url = AJAX_URL % (link_id, s, m, secret, t)
                        urls = self.resolve_link(url)
                        source['url'] = urls
                        sources.append(source)
            except Exception as e:
                log_utils.log('Failure (%s) during icefilms get sources: |%s|' % (str(e), video), log_utils.LOGWARNING)

        main_scrape.apply_urlresolver(sources)
        return sources

    def search(self, video_type, title, year, season=''):
        results = []
        if video_type == 'movies':
            url = urlparse.urljoin(self.base_url, '/movies/a-z/')
        else:
            url = urlparse.urljoin(self.base_url, '/tv/a-z/')

        if title.upper().startswith('THE '):
            search_title = title[4:5]
        elif title.upper().startswith('A '):
            search_title = title[2:3]
        else:
            search_title = title

        if title[:1] in string.digits:
            first_letter = '1'
        else:
            first_letter = search_title[:1]
        url = url + first_letter.upper()

        html = self._http_get(url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        pattern = 'class=star.*?href=([^>]+)>(.*?)</a>'
        for match in re.finditer(pattern, html, re.DOTALL):
            match_url, match_title_year = match.groups()
            match = re.search('(.*?)\s+\((\d{4})\)', match_title_year)
            if match:
                match_title, match_year = match.groups()
            else:
                match_title = match_title_year
                match_year = ''

            if norm_title in scraper_utils.normalize_title(match_title) and (
                    not year or not match_year or year == match_year):
                result = {'url': match_url, 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href=(/ip\.php[^>]+)>%sx0?%s\s+' % (int(video.season), int(video.episode))
        title_pattern = 'class=star>\s*<a href=(?P<url>[^>]+)>(?:\d+x\d+\s+)+(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)
