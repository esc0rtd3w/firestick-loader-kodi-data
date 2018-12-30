# -*- coding: utf-8 -*-
# Universal Scrapers
# 30/10/2018 -BUG

import urllib
import re, xbmcaddon, time, xbmc
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, send_log, error_log
from universalscrapers.modules import client, dom_parser
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
  
class coolmoviezone(Scraper):
    domains = ['http://coolmoviezone.info']
    name = "CoolMovieZone"
    sources = []

    def __init__(self):
        self.base_link = 'http://coolmoviezone.biz'

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()                                                    
            search_id = urllib.quote_plus('%s %s' % (title, year))

            # search_id.replace(' ','+') = urllib.quote_plus(search_id)
            start_url = '%s/index.php?s=%s' % (self.base_link, search_id)
            #print 'CoolMovieZone - scrape_movie - start_url:  ' + start_url
            
            headers = {'User-Agent': client.agent()}
            html = client.request(start_url, headers=headers)

            match = client.parseDOM(html, 'h1')
            match = [dom_parser.parse_dom(i, 'a', req='href') for i in match if i]
            match = [(i[0].attrs['href'], i[0].content) for i in match if i]
            for item_url, name in match:
                if year not in name: continue
                if not clean_title(title) == clean_title(name): continue #.lower() added on clean_title function

                self.get_source(item_url, title, year, '', '', start_time)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)

    def get_source(self, item_url, title, year, season, episode, start_time):
        try:
            #print 'coolmovies pass ' + item_url
            headers={'User-Agent': client.agent()}
            r = client.request(item_url, headers=headers)
            #xbmc.log('@#@HTML:%s' % r, xbmc.LOGNOTICE)

            data = client.parseDOM(r, 'table', attrs={'class': 'source-links'})[0]
            data = client.parseDOM(data, 'tr')
            data = [(client.parseDOM(i, 'a', ret='href')[0],
                     client.parseDOM(i, 'td')[1]) for i in data if 'version' in i.lower()] #Watch Version
            Endlinks = [(i[0], re.sub('<.+?>', '', i[1])) for i in data if i]

            #Endlinks = re.compile('<td align="center"><strong><a href="(.+?)"',re.DOTALL).findall(r)
            #print 'coolmoviezone - scrape_movie - EndLinks: '+str(Endlinks)
            count = 0
            for link, host in Endlinks:
                if 'filebebo' in host: continue #host with captcha
                if 'fruitad' in host:
                    link = client.request(link)
                    link = client.parseDOM(link, 'meta', attrs={'name': 'og:url'}, ret='content')[0]#returns the real url
                    if not link: continue

                import resolveurl
                if resolveurl.HostedMediaFile(link):
                    from universalscrapers.modules import quality_tags
                    quality, info = quality_tags.get_release_quality(link,link)
                    if quality == 'SD':
                        quality = 'DVD'
                    host = host.split('/')[0].split('.')[0].title()
                    count +=1
                    self.sources.append({'source': host, 'quality': quality, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season='', episode='')
        except:
            pass 