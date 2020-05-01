# -*- coding: utf-8 -*-
# Universal Scrapers
# checked 25/04/2019

import re
import urllib
import xbmc, xbmcaddon, time
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")            


class moviejes(Scraper):
    domains = ['https://moviejesus.com']
    name = "Movie Jesus"
    sources = []

    def __init__(self):
        self.base_link = 'https://moviejesus.com'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s/search/%s' % (self.base_link, urllib.quote_plus(search_id))
            #print start_url
            headers = {'User-Agent': client.agent()}
            r = client.request(start_url, headers=headers)
            #print r
            grab=re.compile('class="title"><a href="(.+?)">(.+?)</a></div>.+?class="year">(.+?)</span>',re.DOTALL).findall(r)
            for url, name, date in grab:
                #print url+'>>>>>>'
                name =name.lower()
                #print name+'<<<<<<<<<<'
                if clean_title(title) == clean_title(name):
                    if date==year:
                        self.get_source(url,title, year, '', '', start_time)
            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            seaepi_chk = '%sx%s' %(season,episode)
            search_id = urllib.quote_plus(title)
            start_url = '%s/search/%s' % (self.base_link, urllib.quote_plus(search_id)) 
            headers={'User-Agent': client.agent()}
            r = client.request(start_url, headers=headers)
            match = re.compile('class="result-item".+?<a href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(r)
            #print match
            for link, name in match:
                #print link+'@@@@@@@@'
                #print name+'@@@@@@@@'
                headers={'User-Agent': client.agent()}
                r = client.request(link, headers=headers)
                nextpg= re.compile("class='episodiotitle'><a href='(.+?)'",re.DOTALL).findall(r)
                for url in nextpg:
                    #print url+'>>>>>>>>>>'
                    if seaepi_chk in url:
                        #print url + '<<<<<<<<<<<'

                        self.get_source(url, title, year, season, episode, start_time)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources
            
    def get_source(self,url,title,year,season,episode,start_time):
        try:
            #print 'URL PASSED OK'+url
            count = 0
            headers = {'User-Agent': client.agent()}
            r = client.request(url, headers=headers)
            Endlinks=re.compile("<tr id=.+?a href='(.+?)'.+?class='quality'>(.+?) BR<",re.DOTALL).findall(r)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for link1,qual in Endlinks:
                #link1=link1.replace('#038;','&')
                #print link1+qual+">>>>>>>>>>"
                headers = {'User-Agent': client.agent()}
                r = client.request(link1, headers=headers)
                #print r
                Endlinks1=re.compile('id="link".+?href="(.+?)"',re.DOTALL).findall(r)
                for link in Endlinks1:
                    #print 'scraperchk - scrape_movie - link: '+str(link)
                    count+=1
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    self.sources.append({'source':host, 'quality':qual, 'scraper':self.name, 'url':link, 'direct':False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]