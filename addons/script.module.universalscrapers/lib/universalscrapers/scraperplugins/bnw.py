# -*- coding: utf-8 -*-
# Universal Scrapers checked 27/08/2018

import urllib, urlparse
import xbmc, xbmcaddon, time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.modules import client, dom_parser

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'


class bnw(Scraper):
    name = "BnwMovies"
    domains = ['http://www.bnwmovies.com']
    sources = []

    def __init__(self):
        self.base_link = 'http://www.bnwmovies.com'
        self.search_link = "/?s=%s"

    def scrape_movie(self, title, year, imdb, debrid=False):
        if int(year) > 1980: return self.sources
        try:
            start_time = time.time()
            query = urllib.quote_plus(clean_search(title.lower()))
            start_url = urlparse.urljoin(self.base_link, self.search_link % query)

            headers = {'User-Agent': client.agent(), 'Referer': self.base_link}
            count = 0
            html = client.request(start_url, headers=headers)
            posts = client.parseDOM(html, 'div',  attrs={'class': 'post'})
            posts = [(dom_parser.parse_dom(i, 'a', req='href')[0]) for i in posts if i]
            posts = [(i.attrs['href'], i.content) for i in posts if i]
            post = [(i[0]) for i in posts if clean_title(i[1]) == clean_title(title)][0]
            r = client.request(post, headers=headers)

            y = client.parseDOM(r, 'h1')[0]
            if not year in y: return self.sources

            links = client.parseDOM(r, 'source', ret='src')
            link = [i for i in links if i.endswith('mp4')][0]
            link += '|User-Agent=%s&Referer=%s' % (client.agent(), post)
            link = urllib.quote(link, ':/-_|&+=')
            count += 1
            self.sources.append({'source': 'bnw', 'quality': 'SD', 'scraper': self.name, 'url': link, 'direct': True})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources
#bnw().scrape_movie('Black Panther', '1998', '', False)
#bnw().scrape_movie('going my way', '1944', '', False)
# Movie (Trail Riders) 1942             
