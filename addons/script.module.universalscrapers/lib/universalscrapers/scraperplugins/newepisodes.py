# -*- coding: utf-8 -*-
# Universal Scrapers

import re
import requests
import xbmc, xbmcaddon
import time
import urllib
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.modules import client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class newepis(Scraper):
    domains = ['newepisodes.co']
    name = "New episodes"
    sources = []

    def __init__(self):
        self.base_link = 'http://newepisodes.co/'
        self.search_url = '%sall#' % (self.base_link)
        self.sources = []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            count = 0
            start_time = time.time()
            search_link = '%s%s' % (self.search_url, title[0].upper())
            # print search_link
            html = requests.get(search_link).content
            match = re.compile('<a href="(.+?)">(.+?)</a> <span>(.+?)</span><br/>', re.DOTALL).findall(html)
            for link, name, rel in match:
                if name.upper() == title.upper() and year in rel:
                    link = 'https:' + link
                    # print name+'\n'+link+'\n'+rel
                    html = requests.get(link).content
                    check = 'season-%s-episode-%s-' % (season, episode)
                    match = re.compile('<a href="(.+?)"', re.DOTALL).findall(html)
                    for ep_link in match:
                        if check in ep_link:
                            ep_link = 'https:' + ep_link
                            html = requests.get(ep_link).content
                            block = re.compile('<div class="playlist_inner">(.+?)</ol>', re.DOTALL).findall(html)
                            match = re.compile('id="(.+?)".+?<div class="list_number">.+?</div>(.+?)<span>',
                                               re.DOTALL).findall(str(block))
                            for iD, host in match:
                                link = 'http://newepisodes.co/embed/' + iD
                                count += 1
                                self.sources.append(
                                    {'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': link,
                                     'direct': False})

            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources
        
    def resolve(self, link):
        try:
            html = requests.get(link).content
            url = re.compile('src="(.+?)"', re.DOTALL).findall(html)[1]
            return url
        except:
            return link

# newepis().scrape_episode('suits','2011','','8','1','','')