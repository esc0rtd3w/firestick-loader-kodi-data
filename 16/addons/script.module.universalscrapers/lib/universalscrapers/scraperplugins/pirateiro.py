# -*- coding: utf-8 -*-
# Universal Scrapers
# checked 06/07/2019

import re
import urllib
import xbmc, xbmcaddon, time
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, quality_tags, cfscrape

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")            


class piriro(Scraper):
    domains = ['pirateiro.com']
    name = "PirateIro"
    sources = []

    def __init__(self):
        self.base_link = 'http://pirateiro.com'
        self.search_link = ''

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            if not debrid:
                return self.sources
            search_id = clean_search(title.lower())
            start_url = '%s/torrents/?search=%s+%s' % (self.base_link, urllib.quote_plus(search_id),year)
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
            query = query.replace('%27','')
            start_url='%s/torrents/?search=%s' %(self.base_link, query)
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
            #scraper= cfscrape.create_scraper()
            #r=scraper.get(start_url, headers=headers)
            r = client.request(start_url, headers=headers)
            #print r
            Endlinks=re.compile('class="imagnet icon16"   href="(.+?)">.+?<font color=#004E98>(.+?)</font>.+?><b>(.+?)</b></a',re.DOTALL).findall(r)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for Magnet,size, quality in Endlinks:
                #Magnet=Magnet.replace('https://mylink.me.uk/?url=', '')
                qual = quality_tags.get_release_quality(quality, None)[0]
                #print Magnet + '<><><><><>'
                count+=1
                self.sources.append({'source':'Torrent', 'quality':qual+' '+size, 'scraper':self.name, 'url':Magnet, 'direct':False, 'debridonly': True})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]