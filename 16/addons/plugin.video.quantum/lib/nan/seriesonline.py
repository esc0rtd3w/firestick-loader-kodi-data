# -*- coding: utf-8 -*-
'''
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
'''


import re,urllib,urlparse,hashlib,random,string,json,base64
import xbmc
import requests
from BeautifulSoup import BeautifulSoup
from ..common import  clean_title, random_agent, replaceHTMLCodes, clean_search, filter_host
from ..scraper import Scraper
from nanscrapers.modules import cfscrape

class SeriesOnline(Scraper):
    name = "SeriesOnline"

    def __init__(self):
        self.language = ['en']
        self.domains = ['123movieshd.net', '123movies.to', '123movies.ru', '123movies.is', '123movies.gs', '123-movie.ru', '123movies-proxy.ru', '123movies.moscow', '123movies.msk.ru', '123movies.msk.ru', '123movies.unblckd.me']

        self.base_link = 'https://theseriesonline.com'


        self.search_link = '/movie/search/%s'
        self.info_link = '/ajax/movie_load_info/%s'
        self.server_link = '/ajax/get_episodes/%s'
        self.direct_link = '/ajax/v2_load_episode/'
        self.embed_link = '/ajax/load_embed/'
        self.session = requests.Session()
        self.scraper = cfscrape.create_scraper()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            self.elysium_url = []

            cleaned_title = clean_title(title)
            q = (title.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
            q = self.search_link % (q)

            url = urlparse.urljoin(self.base_link, q)
            html = BeautifulSoup(scraper.get(url).content)
            containers = html.findAll('div', attrs={'class': 'ml-item'})
            for result in containers:
                links = result.findAll('a')
                for link in links:
                    link_title = link['title'].encode('utf-8')
                    href = link['href'].encode('utf-8')
                    href = urlparse.urljoin(self.base_link, href)
                    href = re.sub('/watching.html','', href)
                    href = href + '/watching.html'

                    if clean_title(link_title) == cleaned_title:
                        referer = href
                        html = scraper.get(href).content

                        match = re.findall('<strong>Release:</strong>(.+?)</p>', html)[0]
                        if year in match:
                            s1 = BeautifulSoup(html)
                            s = s1.findAll('div', attrs={'class': 'les-content'})
                            for u in s:
                                print("SERIESONLINE PASSED u", u)
                                player = u.findAll('a')[0]['player-data'].encode('utf-8')
                                quality = u.findAll('a')[0].text.strip()
                                if quality == "1" or "episode" in quality.lower():
                                    try:
                                        quality = s1.find("span", attrs={"class":"quality"}).text
                                    except:
                                        quality = "SD"
                                if player not in self.elysium_url:	self.elysium_url.append([player, referer, quality])
                            return self.sources(self.elysium_url)
        except:
            return

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            self.elysium_url = []
            print ("SERIESONLINE EPISODES STARTED")
            season = '%01d' % int(season)
            episode = '%01d' % int(episode)
            query = (title.translate(None, '\/:*?"\'<>|!,()')).replace(' ', '-').replace('--', '-').lower() + "-season-" + season
            q = self.search_link % (query)
            r = urlparse.urljoin(self.base_link, q)
            cleaned_title = clean_title(title) + "season" + season
            print ("SERIESONLINE EPISODES", q)
            html = BeautifulSoup(scraper.get(r).content)
            containers = html.findAll('div', attrs={'class': 'ml-item'})
            for result in containers:
                links = result.findAll('a')
                for link in links:
                    link_title = link['title'].encode('utf-8')
                    href = link['href'].encode('utf-8')
                    href = urlparse.urljoin(self.base_link, href)
                    href = re.sub('/watching.html','', href)
                    href = href + '/watching.html'

                    # print("SERIESONLINE", link_title, href)
                    if clean_title(link_title) == cleaned_title:
                        print("SERIESONLINE FOUND MATCH", link_title, href)
                        referer = href
                        html = scraper.get(href).content
                        s1 = BeautifulSoup(html)

                        s = s1.findAll('div', attrs={'class': 'les-content'})
                        for x in s:
                            try:
                                items = x.findAll('a')
                                for u in items:

                                    player = u['player-data'].encode('utf-8')
                                    ep_id = u['episode-data'].encode('utf-8')
                                    try:
                                        quality = s1.find("span", attrs={"class":"quality"}).text
                                    except:
                                        quality = "SD"
                                    if ep_id == episode:
                                        if not player in self.elysium_url:	self.elysium_url.append([player, referer, quality])
                            except:
                                pass

            print("SERIESONLINE PASSED", self.elysium_url)
            return self.sources(self.elysium_url)

        except:
            return

    def sources(self, urlarr):

        sources = []
        try:

            for url,referer, quality in urlarr:
                print ("SERIESONLINE SOURCES", url, referer)
                headers = {}
                headers['Referer'] = referer

                if "embed.php" in url:
                    html = scraper.get(url, headers=headers).content
                    html = BeautifulSoup(html)
                    try:
                            r = html.findAll('source')
                            for u in r:
                                print ("SERIESONLINE TRY 3c", r)
                                href = u['src'].encode('utf-8')
                                gquality = googletag(href)
                                if gquality:
                                    quality = gquality[0]["quality"]
                                sources.append({'source': 'gvideo', 'quality': quality, 'scraper': self.name, 'url': href, 'direct': True, 'debridonly': False})
                    except:
                        try:
                            r = html.findAll('iframe')
                            for frame in r:
                                link = r["src"]
                                host = meta_host(link)
                                sources.append({'source': host, 'quality': quality, 'scraper': self.name, 'url': href, 'direct': False, 'debridonly': False})
                        except:
                            pass

                else:
                    try:
                        if not filter_host(url):
                            continue
                        href = url.encode('utf-8')
                        host = meta_host(url)
                        #quality = "SD"
                        sources.append({'source': host, 'quality': quality, 'scraper': self.name, 'url': href, 'direct': False, 'debridonly': False})
                    except:
                        pass


        except:
            pass
        return sources

    def resolve(self, url):
            return url


def googletag(url):
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try:
        quality = quality[0]
    except:
        return []

    if quality in ['37', '137', '299', '96', '248', '303', '46']:
        return [{'quality': '1080', 'url': url}]
    elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
        return [{'quality': '720', 'url': url}]
    elif quality in ['35', '44', '135', '244', '94']:
        return [{'quality': '480', 'url': url}]
    elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
        return [{'quality': '480', 'url': url}]
    elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
        return [{'quality': '480', 'url': url}]
    else:
        return None


def meta_host(url):
    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
    return host
