# -*- coding: utf-8 -*-
# Universal Scrapers
# 15/12/2018 -BUG

import re, requests
import urllib, urlparse
import xbmc, xbmcaddon, time
from universalscrapers.scraper import Scraper
from universalscrapers.common import filter_host, clean_search, clean_title, send_log, error_log
from universalscrapers.modules import client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class cmovies(Scraper):
    domains = ['https://cmovies.cc']
    name = "Cmovies"

    def __init__(self):
        self.base_link = 'https://cmovies.cc'
        self.search_link = 'search/%s/feed/rss2/'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        count = 0
        try:
            start_time = time.time()
            search_id = '%s %s' % (clean_search(title), year)
            start_url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(search_id))
            #xbmc.log('scraperchk - scrape_movie - start_url:%s' % start_url, xbmc.LOGNOTICE)

            headers = {'User-Agent': client.agent()}
            html = requests.get(start_url, headers=headers, timeout=5).content
            posts = client.parseDOM(html, 'item')
            posts = [(client.parseDOM(i, 'title')[0], client.parseDOM(i, 'a', ret='href')) for i in posts if i]
            posts = [i[1] for i in posts if clean_title(i[0]) == clean_title(title)][0]
            #xbmc.log('$#$POSTS:%s' % posts, xbmc.LOGNOTICE)
            for url in posts:
                # print 'scraperchk - scrape_movie - link: '+str(link1)
                if 'cmovies' in url: continue
                link = 'https:' + url if url.startswith('//') else url
                # print link+'?<<<<<<<<<<<<<<<<<<<,,,'
                if '1080' in link:
                    qual = '1080p'
                elif '720' in link:
                    qual = '720p'
                else:
                    qual = 'SD'
                host = url.split('//')[1].replace('www.', '')
                host = host.split('/')[0].split('.')[0].title()
                count += 1
                self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

