# -*- coding: utf-8 -*-
# Universal Scrapers
# checked 30/8/2018

import re
import urllib
import xbmc, xbmcaddon, time
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")            


class movie4u(Scraper):
    domains = ['https://movie4u.ch']
    name = "movie4u"
    sources = []

    def __init__(self):
        self.base_link = 'https://movie4u.live'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' % (self.base_link, urllib.quote_plus(search_id))
            headers = {'User-Agent': client.agent()}
            html = client.request(start_url, headers=headers)
            posts = client.parseDOM(html, 'div', attrs={'class': 'result-item'})
            posts = [(client.parseDOM(i, 'div', attrs={'class': 'details'})[0]) for i in posts if i]
            posts = [i for i in posts if not 'SEO Checker' in i]
            for post in posts:
                try:
                    name = client.parseDOM(post, 'a')[0]
                    url = client.parseDOM(post, 'a', ret='href')[0]
                    date = client.parseDOM(post, 'span', attrs={'class': 'year'})[0]
                except:
                    raise Exception()
                name = re.sub('<.+?>', '', name)
                tit = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+)(\.|\)|\]|\s|)(.+|)', '', name, flags=re.I)

                if not clean_title(title) == clean_title(tit):
                    continue
                if not year == date:
                    continue
                self.get_source(url, title, year, '', '', start_time)
            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s+season+%s' % (self.base_link, urllib.quote_plus(search_id), season)
            headers = {'User_Agent': client.agent()}
            html = client.request(start_url, headers=headers)
            #print 'PAGE>>>>>>>>>>>>>>>>>'+html
            posts = client.parseDOM(html, 'div', attrs={'class': 'result-item'})
            posts = [(client.parseDOM(i, 'div', attrs={'class': 'details'})[0]) for i in posts if i]
            posts = [i for i in posts if not 'SEO Checker' in i]
            for post in posts:
                try:
                    name = client.parseDOM(post, 'a')[0]
                    name = re.sub('<.+?>', '', name)
                    url = client.parseDOM(post, 'a', ret='href')[0]
                except:
                    raise Exception()
                tit = re.sub('(\.|\(|\[|\s)(Season)(\.|\)|\]|\s|)(.+|)', '', name, flags=re.I)
                if not clean_title(title).lower() == clean_title(tit).lower():
                    continue

                epi_id = '%sx%s/' % (season, episode)
                ep_link = url.replace('/seasons/', '/episodes/')
                ep_link = ep_link.split('-season')[0] + '-%s' % epi_id

                self.get_source(ep_link, title, year, season, episode, start_time)
                
            #print self.sources
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources
            
    def get_source(self,url,title,year,season,episode,start_time):
        try:
            headers = {'User-Agent': client.agent()}
            OPEN = client.request(url, headers=headers)
            holder = client.parseDOM(OPEN, 'div', attrs={'class':'bwa-content'})[0]
            holder = client.parseDOM(holder, 'a', ret='href')[0]
            links = client.request(holder, headers=headers)
            Regex = client.parseDOM(links, 'iframe', ret='src', attrs={'class': 'metaframe rptss'})
            count = 0
            for link in Regex:
                if 'player.php' in link:
                    link = client.request(link, headers=headers, output='geturl')
                    qual = client.request(link, headers=headers)
                    qual = client.parseDOM(qual, 'meta', ret='content')[0]
                else:
                    link = link

                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()

                if '1080p' in qual:
                    rez = '1080p'
                elif '720p' in qual:
                    rez = '720p'
                else: rez = 'SD'
                count += 1
                self.sources.append({'source': host, 'quality': rez, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)
        except:
            pass

#movie4u().scrape_movie('Wonder Woman', '2017','')
#movie4u().scrape_episode('Suits','2011','','8','5','','')