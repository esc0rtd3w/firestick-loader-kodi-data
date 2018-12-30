# -*- coding: utf-8 -*-
# Universal Scrapers
# 30/10/2018 -BUG

import re, requests, urllib
import xbmcaddon
import xbmc
import time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.modules import client
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
  
class moviefishers(Scraper):
    domains = ['http://moviefishers.org']
    name = "moviefishers"
    sources = []

    def __init__(self):
        self.base_link = 'http://moviefishers.org'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            start_url = "http://moviefishers.org/wp-json/wp/v2/posts?search=%s" % urllib.quote_plus(clean_search(title))
            self.get_source(start_url, title, year, start_time)
            return self.sources
        except Exception as E:
            xbmc.log(str(E),2)
                        
    def get_source(self, item_url, title, year, start_time):
        try:
            count = 0
            data = requests.get(item_url).json()
            for item in data:
                title = item["title"]["rendered"]
                content = item["content"]["rendered"]
                year2 = item["date"][:4]
                if int(year) != int(year2):
                    continue
                #Links = re.findall(r"(http.*streamango.com\/embed\/\w{1,}|https:\/\/openload\.co\/embed\/\w{1,}\/)",content)
                Links = client.parseDOM(content, 'iframe', ret='src')
                for link in Links:
                    count += 1
                    host = link.split('//')[1].replace('www.', '')
                    host = host.split('/')[0].split('.')[0].title()
                    label = "DVD"
                    self.sources.append({'source': host, 'quality': label, 'scraper': self.name, 'url': link,'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)

#moviefishers().scrape_movie('Black Panther', '2018','')
