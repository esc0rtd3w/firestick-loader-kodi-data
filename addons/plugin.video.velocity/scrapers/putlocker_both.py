import re
import urlparse
from libs import kodi

import scraper_utils
from libs import dom_parser
from libs.constants import FORCE_NO_MATCH
from libs.constants import QUALITIES
from libs.constants import VIDEO_TYPES
import scrapeit
import main_scrape


BASE_URL = 'http://putlocker9.is'


class Scraper(scrapeit.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scrapeit.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('putlocker_base_url')

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Putlocker'

    def resolve_link(self, link):
        if not link.startswith('http'):
            stream_url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(stream_url, cache_limit=0)
            iframe_url = dom_parser.parse_dom(html, 'iframe', ret='src')
            if iframe_url:
                return iframe_url[0]
        else:
            return link

    def get_sources(self, video, video_type):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'alternativesc'})
            if fragment:
                for item in dom_parser.parse_dom(fragment[0], 'div', {'class': 'altercolumn'}):
                    link = dom_parser.parse_dom(item, 'a', {'class': 'altercolumnlink'}, ret='href')
                    host = dom_parser.parse_dom(item, 'span')
                    if link and host:
                        link = link[0]
                        if not link.startswith('http'):
                            link = source_url + link
                        host = host[0]
                        quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                        hoster = {'hostname': 'PutLocker','multi-part': False, 'host': host, 'class': '', 'quality': quality, 'views': None,
                                  'rating': None, 'url': link, 'direct': False}
                        hosters.append(hoster)
        main_scrape.apply_urlresolver(hosters)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        headers = {'Referer': self.base_url}
        params = {'search': title}
        html = self._http_get(self.base_url, params=params, headers=headers, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'listCard'}):
            match_title = dom_parser.parse_dom(item, 'p', {'class': 'extraTitle'})
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            match_year = dom_parser.parse_dom(item, 'p', {'class': 'cardYear'})
            if match_url and match_title:
                match_url = match_url[0]
                match_title = match_title[0]
                match_year = match_year[0] if match_year else ''
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url),
                              'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results


    # def _get_episode_url(self, show_url, video, sea, epi):
    #     episode_pattern = 'href="([^"]+season-%s-episode-%s-[^"]+)' % (sea,epi)
    #     title_pattern = 'href="(?P<url>[^"]+season-\d+-episode-\d+-[^"]+).*?\s+-\s+(?P<title>.*?)</td>'
    #     headers = {'Referer': urlparse.urljoin(self.base_url, show_url)}
    #     return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern, headers=headers)


    def _get_episode_url(self, show_url, video):
        show_url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, headers={'Referer': self.base_url}, cache_limit=24 * 7)
        match = re.search('href="([^"]*season=0*%s(?!\d))[^"]*' % (video.season), html)
        if match:
            season_url = show_url + match.group(1)
            episode_pattern = 'href="([^"]*/0*%s-0*%s/[^"]*)' % (int(video.season), int(video.episode))
            title_pattern = 'class="episodeDetail">.*?href="(?P<url>[^"]+)[^>]*>\s*(?P<title>.*?)\s*</a>'
            headers = {'Referer': show_url}
            return self._default_get_episode_url(season_url, video, episode_pattern, title_pattern, headers=headers)