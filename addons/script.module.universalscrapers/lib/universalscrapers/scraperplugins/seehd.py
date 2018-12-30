# -*- coding: utf-8 -*-
# Universal Scrapers
# 30/10/2018 -BUG

import re
import xbmcaddon,time
import xbmc, urllib
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, filter_host, get_rd_domains, send_log, error_log
from universalscrapers.modules import client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class seehd(Scraper):
    domains = ['http://www.seehd.pl']
    name = "SeeHD"
    sources = []

    def __init__(self):
        self.base_link = 'http://www.seehd.pl'
        self.search_link = '/search/%s/feed/rss2/'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            #scraper = cfscrape.create_scraper()
            search_id = '%s %s' % (title, year)
            start_url = self.base_link + self.search_link % urllib.quote_plus(search_id)
            #print '::::::::::::: START URL '+start_url
            html = client.request(start_url)

            items = client.parseDOM(html, 'item')
            item = [i for i in items if imdb in i][0]

            self.get_source(item, title, year, "", "", debrid, start_time)

            #print self.sources
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            hdlr = 'S%02dE%02d' % (int(season), int(episode))
            search_id = '%s %s' % (title, hdlr)
            start_url = self.base_link + self.search_link % urllib.quote_plus(search_id)

            html = client.request(start_url)

            items = client.parseDOM(html, 'item')
            for item in items:
                name = client.parseDOM(item, 'title')[0]
                name = client.replaceHTMLCodes(name)
                t = name.split(hdlr)[0]

                if not clean_title(title) == clean_title(t):
                    continue
                if not hdlr in name:
                    continue
                self.get_source(item, title, year, season, episode, debrid, start_time)
            #print self.sources
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)

    def get_source(self,item_url, title, year, season, episode, debrid, start_time):
        try:
            count = 0

            frames = []
            frames += client.parseDOM(item_url, 'iframe', ret='src')
            frames += client.parseDOM(item_url, 'a', ret='href')
            frames += client.parseDOM(item_url, 'source', ret='src')
            frames += client.parseDOM(item_url, 'enclosure', ret='url')

            #xbmc.log('@#@LINKS: %s' % frames, xbmc.LOGNOTICE)
            try:
                q = re.findall('<strong>Quality:</strong>([^<]+)', item_url, re.DOTALL)[0]
                if 'high' in q.lower():
                    qual = '720p'
                elif 'cam' in q.lower():
                    qual = 'CAM'
                else:
                    qual = 'SD'
            except:
                qual = 'SD'

            for link in frames:
                if 'http://24hd.org' in link: continue
                if '.pl/link/' in link: continue
                if 'seehd.pl/d/' in link:
                    #scraper = cfscrape.create_scraper()
                    r = client.request(link)
                    link = client.parseDOM(r, 'iframe', ret='src')[0]

                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].lower()
                if debrid is True:
                    rd_domains = get_rd_domains()
                    if host not in rd_domains: continue
                    #xbmc.log('@#@RD-LINKS: %s' % link, xbmc.LOGNOTICE)
                    count += 1
                    self.sources.append(
                        {'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False, 'debridonly': True})


                if not filter_host(host): continue
                #xbmc.log('@#@NORMAL-LINKS: %s' % link, xbmc.LOGNOTICE)
                count += 1
                self.sources.append(
                    {'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False})

            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name,argument)

#seehd().scrape_movie('Deadpool 2', '2018', '', False)