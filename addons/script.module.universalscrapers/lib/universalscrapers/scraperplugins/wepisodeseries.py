# -*- coding: utf-8 -*-
# Universal Scrapers Bug
#checked 29/10/2018

import re, xbmcaddon, xbmc, time
import urllib, urlparse, json

from universalscrapers.common import clean_title, clean_search, filter_host, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, dom_parser as dom

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'


class Watchepisodes(Scraper):
    domains = ['www.watchepisodeseries.com/']
    name = "wEpisodesSeries"

    def __init__(self):
        self.base_link = 'http://www.watchepisodeseries.com/'
        self.search_link = 'home/search?q=%s'
        self.sources = []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            scrape = clean_search(title.lower())
            start_url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(clean_search(title)))
            #xbmc.log('@#@START: %s' % start_url, xbmc.LOGNOTICE)
            html = client.request(start_url)
            data = json.loads(html)
            posts = data['series']
            post = [i['seo_name'] for i in posts if clean_title(title) == clean_title(i['original_name'])][0]
            show_page = self.base_link + post

            r = client.request(show_page)
            sepi = 'season-%s-episode-%s' % (int(season), int(episode))
            epi_link = client.parseDOM(r, 'a', ret='href')
            epi_link = [i for i in epi_link if sepi in i][0]

            self.get_sources(epi_link, title, year, season, episode, start_time)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_sources(self, episode_url, title, year, season, episode, start_time):
        try:
            links = client.request(episode_url)
            links = client.parseDOM(links, 'div', attrs={'class': 'll-item'})
            count = 0
            for link in links:
                data = dom.parse_dom(link, 'a')[0]

                host = data.content
                if not filter_host(host):
                    continue
                count += 1
                url = data.attrs['href']
                self.sources.append(
                    {'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': url, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)


        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def resolve(self, link):
        try:
            r = client.request(link)
            r = client.parseDOM(r, 'div', attrs={'class': 'wb-main'})[0]
            url = client.parseDOM(r, 'a', ret='href')[0]
            return url
        except:
            return link
