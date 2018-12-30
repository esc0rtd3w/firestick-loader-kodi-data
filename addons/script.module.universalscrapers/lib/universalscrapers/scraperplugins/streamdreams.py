# -*- coding: utf-8 -*-
# Universal Scrapers
#checked 10/11/2018

import re, time, urllib
import xbmcaddon, xbmc
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, filter_host, clean_search, send_log, error_log
from universalscrapers.modules import client, dom_parser as dom, cfscrape

dev_log =xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class streamdreams(Scraper):
    domains = ['streamdreams.org']
    name = "StreamDreams"
    sources = []

    def __init__(self):
        self.base_link = 'https://streamdreams.org'
        self.search_url = self.base_link + '/?s=%s'

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search_id = urllib.quote_plus(clean_search(title))
            query = self.search_url % search_id

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'Referer': self.base_link}
            scraper = cfscrape.create_scraper()
            r = scraper.get(query, headers=headers).content

            posts = client.parseDOM(r, 'div', attrs={'class': 'col-xs-4 col-sm-4 col-md-3 col-lg-3'})
            posts = [dom.parse_dom(i, 'a', req='href')[0] for i in posts if year in i]
            post = [i.attrs['href'] for i in posts if clean_title(title) == clean_title(i.attrs['title'])][0]
            self.get_source(post, title, year, '', '', start_time)

        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, 'Check Search')
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            query = urllib.quote_plus(clean_search(title))
            query = self.search_url % query

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'Referer': self.base_link}
            scraper = cfscrape.create_scraper()
            r = scraper.get(query, headers=headers).content

            posts = client.parseDOM(r, 'div', attrs={'class': 'col-xs-4 col-sm-4 col-md-3 col-lg-3'})
            posts = [dom.parse_dom(i, 'a', req='href')[0] for i in posts if show_year in i]
            post = [i.attrs['href'] for i in posts if clean_title(title) == clean_title(i.attrs['title'])][0]

            start_url = '%s?session=%01d&episode=%01d' % (post, int(season), int(episode))
            self.get_source(start_url, title, year, season, episode, start_time)

        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, 'Check Search')
            return self.sources

    def get_source(self, item_url, title, year, season, episode, start_time):
        try:
            count = 0
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'Referer': self.base_link}
            scraper = cfscrape.create_scraper()
            r = scraper.get(item_url, headers=headers).content
            data = client.parseDOM(r, 'tr')
            for item in data:
                qual = client.parseDOM(item, 'span', ret='class')[0]
                qual = qual.replace('quality_', '')

                link = client.parseDOM(item, 'a', ret='data-href')[0]

                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0]
                if not filter_host(host): continue
                count += 1
                self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season='', episode='')

            return self.sources
        except BaseException:
            return self.sources
