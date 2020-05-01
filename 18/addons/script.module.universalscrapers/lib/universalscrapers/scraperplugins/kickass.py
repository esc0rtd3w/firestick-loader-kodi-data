# -*- coding: utf-8 -*-
# Universal Scrapers
# checked 30/3/2020

import re
import urllib
import xbmc, xbmcaddon, time
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")            


class kickass2(Scraper):
    domains = ['kickass.love']
    name = "Kickass"
    sources = []

    def __init__(self):
        self.base_link = 'https://kickass.love'
        self.search_link = '/usearch/%scategory:movies'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s/usearch/%s %s category:movies/' % (self.base_link, urllib.quote_plus(search_id),year)
            start_url = start_url.replace(' ','%20')
            #print start_url+'>>>>>>>>>>>>>>>>>>>'
            self.get_source(start_url, title, year, '', '', start_time)
            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            if not debrid:
                return self.sources
            hdlr = 'S%02dE%02d' % (int(season), int(episode))
            query = '%s+S%02dE%02d' % (urllib.quote_plus(title), int(season), int(episode))
            query = query.replace(' ','%20')
            start_url='%s/usearch/%s category:tv/' %(self.base_link, query)
            #print start_url
            self.get_source(start_url, title, show_year, season, episode, str(start_time))
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources
            
    def get_source(self,start_url,title,year,season,episode,start_time):
        try:
            #print 'URL PASSED OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK'+start_url
            count = 0
            headers = {'User-Agent': client.agent()}
            r = client.request(start_url, headers=headers)
            #print r
            Endlinks=re.compile('class="nobr center">(.+?)</span></td>.+?title="Torrent magnet link" href="(.+?)".+?class="cellMainLink">(.+?)</a>',re.DOTALL).findall(r)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for size, Magnet, qual in Endlinks:
                Magnet=Magnet.replace('https://mylink.cx/?url=', '')
                Magnet=Magnet.replace('%3A',':').replace('%3F','?').replace('%3D','=').split('%26dn')[0]
                print Magnet + '<><><><><>'
                qual = quality_tags.get_release_quality(qual, None)[0]
                count+=1
                self.sources.append({'source':'Torrent', 'quality':qual+' '+size, 'scraper':self.name, 'url':Magnet, 'direct':False, 'debridonly': True})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]