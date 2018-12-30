# -*- coding: utf-8 -*-
#Universal-Scraper checked 11/11/2018 - DEN

import re, urllib, urlparse, time
import xbmc, xbmcaddon
from universalscrapers.scraper import Scraper
from universalscrapers.common import filter_host, clean_search, send_log, error_log
from universalscrapers.modules import client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class cotun(Scraper):
    domains = ['couchtuner.unblocked']
    name = "Couchtuner"
    sources = []

    def __init__(self):
        self.base_link = 'https://couchtuner.mrunlock.pw'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            count = 0 
            search_id = clean_search(title.lower()) .replace(' ', '-')
            sepi = 's%01de%01d' % (int(season), int(episode))
            epi_link = 'https://stream2watch.mrunlock.pw/%s-%s' % (search_id, sepi)
            r = client.request(epi_link)
            if not r: return
            #link1 = re.compile('<p><ul.+?iframe.+?src="(.+?)".+?frameborder',re.DOTALL).findall(r)
            links = client.parseDOM(r, 'iframe', ret='src')
            for link in links:
                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0]
                if not filter_host(host): continue
                count += 1
                self.sources.append({'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': link, 'direct': False})

                if dev_log == 'true':
                    end_time = time.time() - start_time
                    send_log(self.name, end_time, count, title, year, season=season, episode=episode)

            return self.sources
        except Exception as argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources


#cotun().scrape_episode('suits', '2011', '', '8', '1', '', '', False)
