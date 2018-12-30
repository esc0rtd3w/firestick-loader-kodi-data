import re
import urllib
import urlparse
from libs import log_utils
from libs import kodi
import scraper_utils
import scrapeit
import main_scrape


def __enum(**enums):
    return type('Enum', (), enums)

FORCE_NO_MATCH = '***FORCE_NO_MATCH***'
QUALITIES = __enum(LOW='Low', MEDIUM='Medium', HIGH='High', HD720='HD720', HD1080='HD1080')
VIDEO_TYPES = __enum(TVSHOW='TV Show', MOVIE='Movie', EPISODE='Episode', SEASON='Season')
########ALL NEED ABOVE#############


QUALITY_MAP = {'DVD': QUALITIES.HIGH, 'TS': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}

BASE_URL = kodi.get_setting('primewire_base_url')

class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('primewire_base_url')

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'PrimeWire'

    def format_source_label(self, item):
        label = super(self.__class__, self).format_source_label(item)
        if item['verified']: label = '[COLOR yellow]%s[/COLOR]' % (label)
        return label

    def get_sources(self, video, video_type):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            #kodi.log("Source HTML  is : " + html)
            container_pattern = r'<table[^>]+class="movie_version[ "][^>]*>(.*?)</table>'
            item_pattern = (
                r'quality_(?!sponsored|unknown)([^>]*)></span>.*?'
                r'url=([^&]+)&(?:amp;)?domain=([^&]+)&(?:amp;)?(.*?)'
                r'"version_veiws"> ([\d]+) views</')
            max_index = 0
            max_views = -1
            for container in re.finditer(container_pattern, html, re.DOTALL | re.IGNORECASE):
                for i, source in enumerate(re.finditer(item_pattern, container.group(1), re.DOTALL)):
                    qual, url, host, parts, views = source.groups()

                    if host == 'ZnJhbWVndGZv': continue  # filter out promo hosts
                    source = {'hostname': 'PrimeWire', 'url': url.decode('base-64'),'class': '', 'host': host.decode('base-64'),'views': views, 'quality': qual, 'direct': False}
                    hosters.append(source)

            # if max_views > 0:
            #     for i in xrange(0, max_index):
            #         hosters[i]['rating'] = hosters[i]['views'] * 100 / max_views
        fullsource = main_scrape.apply_urlresolver(hosters)
        return fullsource

    def search(self, video_type, title, year, season=''):
        search_url = urlparse.urljoin(self.base_url, '/index.php?search_keywords=')
        search_url += urllib.quote_plus(title)
        search_url += '&year=' + urllib.quote_plus(str(year))
        if video_type == 'shows':
            search_url += '&search_section=2'
        else:
            search_url += '&search_section=1'
        results = []
        html = self. _http_get(self.base_url, cache_limit=0)
        #kodi.log("HTML is : " + html)
        match = re.search('input type="hidden" name="key" value="([0-9a-f]*)"', html)
        if match:
            key = match.group(1)
            search_url += '&key=' + key

            html = self._http_get(search_url, cache_limit=.25)
            pattern = r'class="index_item.+?href="(.+?)" title="Watch (.+?)"?\(?([0-9]{4})?\)?"?>'
            for match in re.finditer(pattern, html):
                url, title, year = match.groups('')
                result = {'url': scraper_utils.pathify_url(url), 'title': scraper_utils.cleanse_title(title), 'year': year}
                results.append(result)
        else:
            log_utils.log('Unable to locate PW search key', log_utils.LOGWARNING)
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = '"tv_episode_item">[^>]+href="([^"]+/season-%s-episode-%s)">' % (int(video.season), int(video.episode))
        title_pattern = 'class="tv_episode_item".*?href="(?P<url>[^"]+).*?class="tv_episode_name">\s+-\s+(?P<title>[^<]+)'
        airdate_pattern = 'class="tv_episode_item">\s*<a\s+href="([^"]+)(?:[^<]+<){3}span\s+class="tv_episode_airdate">\s+-\s+{year}-{p_month}-{p_day}'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern, airdate_pattern)
