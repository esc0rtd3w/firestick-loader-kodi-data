# -*- coding: utf-8 -*-
# 30/10/2018 -BUG

import re
import xbmcaddon,time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, filter_host, send_log, error_log
from universalscrapers.modules import client
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class WatchFrees(Scraper):
    domains = ['watchfrees.com']
    name = "watchfrees"
    sources = []

    def __init__(self):
        self.base_link = 'https://watchfree.movie' #'https://watchfrees.com'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            ep_string = '-season-%s-episode-%s-' %(season, episode)
            search_id = clean_search(title.lower())
            start_url = '%s/search.html?keyword=%s' %(self.base_link,search_id.replace(' ','+'))
            html = client.request(start_url)
            match = re.compile('<figure>.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url, name in match:
                if clean_title(title).lower() in clean_title(name).lower():
                    season_url = self.base_link + url
                    #print 'shows >'+season_url
                    if 'Season '+season in name:
                        #print 'correct season shows >'+season_url
                        html2 = client.request(season_url)
                        ulist = re.compile('<ul>(.+?)</ul>',re.DOTALL).findall(html2)
                        match2 = re.compile('<a href="(.+?)"',re.DOTALL).findall(str(ulist))
                        for epi_url in match2:
                            if not ep_string in epi_url:
                                continue
                            url = self.base_link+epi_url
                            #print 'pass watchepisode url ' +url
                            self.get_source(url,title,year,season,episode,start_time)

            return self.sources
                                        
        except:
            return self.sources

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s/search.html?keyword=%s' %(self.base_link,search_id.replace(' ','+'))
            html = client.request(start_url)
            match = re.compile('<figure>.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url, name in match:
                name = name.replace('Movie','')
                if clean_title(title).lower() == clean_title(name).lower():
                    url = self.base_link + url
                    self.get_source(url, title, year, '', '', start_time)
            return self.sources
        except:
            return self.sources

    def get_source(self, link, title, year, season, episode, start_time):
        try:
            html = client.request(link)
            match = re.compile('var link_server.+?"(.+?)"', re.DOTALL).findall(html)
            count = 0
            for link in match:
                if not link.startswith('https:'):
                    link = 'http:' + link
                if 'vidnode' in link:
                    if not 'load.php' in link:
                        continue
                    #print 'vidnodelink >>> '+link
                    html = client.request(link)
                    
                    grab = re.compile("sources.+?file: '(.+?)',label: '(.+?)'", re.DOTALL).findall(html)
                    for end_link,rez in grab:
                        if '1080' in rez:
                            res = '1080p'
                        elif '720' in rez:
                            res = '720p'
                        else: res = 'SD'
                        count += 1
                        self.sources.append({'source': 'Vidnode', 'quality': res, 'scraper': self.name, 'url': end_link, 'direct': False})
                
                else:
                    host = link.split('//')[1].replace('www.', '')
                    host = host.split('/')[0]
                    if not filter_host(host): continue
                    count += 1
                    self.sources.append({'source': host, 'quality': 'SD', 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season,episode=episode)

        except:
            pass


