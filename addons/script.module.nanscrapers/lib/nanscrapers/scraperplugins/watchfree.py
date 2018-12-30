import base64
import re,time
import urllib
import urlparse

from BeautifulSoup import BeautifulSoup
from ..import proxy
from ..common import replaceHTMLCodes, clean_title
from ..scraper import Scraper
import xbmcaddon
import xbmc

class Watchfree(Scraper):
    domains = ['watchfree.to']
    name = "watchfree"

    def __init__(self):
        self.base_link = self.base_link = xbmcaddon.Addon('script.module.nanscrapers').getSetting("%s_baseurl" % (self.name))
        self.moviesearch_link = '/?keyword=%s&search_section=1'
        self.tvsearch_link = '/?keyword=%s&search_section=2'
        self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            query = self.moviesearch_link % urllib.quote_plus(title.replace('\'', '').rsplit(':', 1)[0])
            query = urlparse.urljoin(self.base_link, query)

            html = proxy.get(query, 'item')
            page = 1
            while True:
                sources = self.scrape_movie_page(html, title, year)
                if sources is not None:
                    return sources
                else:
                    page +=1
                    if 'page=%s' % page in html or 'page%3D' + '%s' % page in html:
                        html2 = proxy.get(query + '&page=%s' % page, 'item')
                        html = html2
                    else:
                        break
        except:
            pass
        return []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            query = urlparse.urljoin(self.base_link,
                                     self.tvsearch_link % urllib.quote_plus(title.replace('\'', '').rsplit(':', 1)[0]))

            html = proxy.get(query, 'item')
            if 'page=2' in html or 'page%3D2' in html:
                html2 = proxy.get(query + '&page=2', 'item')
                html += html2

            html = BeautifulSoup(html)

            cleaned_title = 'watchputlocker' + clean_title(title)
            years = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1)]

            items = html.findAll('div', attrs={'class': 'item'})

            show_url = None
            for item in items:
                links = item.findAll('a')
                for link in links:
                    href = link['href']
                    link_title = link['title']
                    try:
                        href = urlparse.parse_qs(urlparse.urlparse(href).query)['u'][0]
                    except:
                        pass
                    try:
                        href = urlparse.parse_qs(urlparse.urlparse(href).query)['q'][0]
                    except:
                        pass
                    if cleaned_title == clean_title(link_title) and show_year in link_title:
                        url = re.findall('(?://.+?|)(/.+)', href)[0]
                        show_url = urlparse.urljoin(self.base_link, replaceHTMLCodes(url))
                    else:
                        continue

                    html = BeautifulSoup(proxy.get(show_url, 'tv_episode_item'))
                    season_items = html.findAll('div', attrs={'class': 'show_season'})
                    for season_item in season_items:
                        if season_item["data-id"] != season:
                            continue
                        episode_items = season_item.findAll('div', attrs={'class': 'tv_episode_item'})
                        for episode_item in episode_items:
                            link = episode_item.findAll('a')[-1]
                            href = link["href"]
                            link_episode = link.contents[0].strip()
                            if link_episode != "E%s" % (episode):
                                continue
                            link_airdate = link.findAll('span', attrs={'class': 'tv_num_versions'})[-1]  # WTF
                            link_airdate = link_airdate.contents[0]
                            if any(candidate_year in link_airdate for candidate_year in years):
                                return self.sources(href)

        except:
            pass
        return []

    def sources(self, url):
        sources = []
        try:
            if url == None: return sources
            absolute_url = urlparse.urljoin(self.base_link, url)
            html = BeautifulSoup(proxy.get(absolute_url, 'link_ite'))
            tables = html.findAll('table', attrs={'class': re.compile('link_ite.+?')})
            for table in tables:
                rows = table.findAll('tr')
                for row in rows:
                    link = row.findAll('a')[-1]
                    href = link['href']

                    if not 'gtfo' in href:
                        continue

                    try:
                        href = urlparse.parse_qs(urlparse.urlparse(href).query)['u'][0]
                    except:
                        pass
                    try:
                        href = urlparse.parse_qs(urlparse.urlparse(href).query)['q'][0]
                    except:
                        pass

                    href = base64.b64decode(urlparse.parse_qs(urlparse.urlparse(href).query)['gtfo'][0])
                    href = replaceHTMLCodes(href)

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(href.strip().lower()).netloc)[0]
                    host = replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    if "qertewrt" in host:
                        continue

                    quality = row.findAll('div', attrs={'class': 'quality'})[0].text
                    if "CAM" in quality or 'TS' in quality:
                        quality = 'CAM'
                    if 'HD' in quality:
                        pass
                    else:
                        quality = 'SD'

                    sources.append(
                        {'source': host, 'quality': quality, 'scraper': self.name, 'url': href, 'direct': False})
            end_time = time.time()
            total_time = end_time - self.start_time
            print (repr(total_time))+"<<<<<<<<<<<<<<<<<<<<<<<<<"+self.name+">>>>>>>>>>>>>>>>>>>>>>>>>total_time"        
        except:
            pass

        return sources

    def scrape_movie_page(self, html, title, year):
        try:
            html = BeautifulSoup(html)

            cleaned_title = 'watchputlocker' + clean_title(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year) + 1), '(%s)' % str(int(year) - 1)]

            items = html.findAll('div', attrs={'class': 'item'})

            for item in items:
                links = item.findAll('a')
                for link in links:
                    href = link['href']
                    link_title = link['title']
                    if any(candidate_year in link_title for candidate_year in years):
                        try:
                            href = urlparse.parse_qs(urlparse.urlparse(href).query)['u'][0]
                        except:
                            pass
                        try:
                            href = urlparse.parse_qs(urlparse.urlparse(href).query)['q'][0]
                        except:
                            pass
                        if cleaned_title == clean_title(link_title):
                            url = re.findall('(?://.+?|)(/.+)', href)[0]
                            url = replaceHTMLCodes(url)
                            return self.sources(url)
        except:
            pass

    @classmethod
    def get_settings_xml(clas):
        xml = [
            '<setting id="%s_enabled" ''type="bool" label="Enabled" default="true"/>' % (clas.name),
            '<setting id= "%s_baseurl" type="text" label="Base Url" default="http://www.gowatchfreemovies.to"/>' % (clas.name)
        ]
        return xml
