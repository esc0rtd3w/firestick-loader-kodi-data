# -*- coding: utf-8 -*-

import re,xbmcaddon,requests,time
from ..scraper import Scraper
from ..common import clean_title,clean_search, filter_host, get_rd_domains,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

class movieseriestv(Scraper):
    domains = ['movieseriestv.net']
    name = "MovieSeriesTV"
    sources = []
    
    def __init__(self):
        self.domains = ['movieseriestv.net']
        self.base_link = 'http://www.movieseriestv.net'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            if not debrid:
                return []
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print 'SEARECH ME '+start_url
            headers = {'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            #print html
            results = re.compile('<h2 class="title".+?href="(.+?)"',re.DOTALL).findall(html)
            for url in results:
                if not clean_title(title).lower() in clean_title(url).lower():
                    continue
                if not year  in url:
                    continue
                #print ' pass this> '+ url
                        
                self.get_source(url)                     
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources  

    # not lot tv on site
    # def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        # try:
            # if not debrid:
                # return []
            # season_url = "0%s"%season if len(season)<2 else season
            # episode_url = "0%s"%episode if len(episode)<2 else episode
            # sea_epi ='s%se%s'%(season_url,episode_url)
            
            # search_id = clean_search(title.lower())

            # start_url = '%s/?s=%s+%s' %(self.base_link,search_id.replace(' ','+'),sea_epi)
            # #print 'SEARECH ME '+start_url
            # headers = {'User-Agent':random_agent()}
            # html = requests.get(start_url,headers=headers,timeout=5).content
            # #print html
            # results = re.compile('<h2 class="title".+?href="(.+?)"',re.DOTALL).findall(html)
            # for url in results:
                # if clean_title(title).lower() in clean_title(url).lower():
                    # if sea_epi.lower() in clean_title(url).lower():
                        # print ' pass this> '+ url
                        
                        # self.get_source(url)                     
            # return self.sources
        # except Exception, argument:
            # return self.sources                   
 

    def get_source(self,url):
        try:        
            headers = {'User_Agent':random_agent()}
            movpage = requests.get(url,headers=headers,timeout=3).content
            link_page = re.compile('href="(http://www.links.+?)"',re.DOTALL).findall(movpage)[0]
            #print 'CHECK link> ' + link_page
            
            headers = {'User_Agent':random_agent(),'Referer':url}
            links = requests.get(link_page,headers=headers,timeout=3).content
                  
            LINK = re.compile('target="_blank" href="([^"]+)"',re.DOTALL).findall(links) 
            try:
                uniques = []
                count = 0    
                for url in LINK:
                    if '.rar' not in url:
                        if '.keeplinks' not in url:
                            if '1080' in url:
                                res = '1080p'
                            elif '.1p' in url:
                                res = '1080p'
                            elif '720' in url:
                                res = '720p'
                            elif '.7p' in url:
                                res = '720p'
                            else:
                                res = 'DVD'

                            host = url.split('//')[1].replace('www.','')
                            host = host.split('/')[0].lower()

                            rd_domains = get_rd_domains()
                            if host in rd_domains:
                                if url not in uniques:
                                    uniques.append(url)
                                    #print '####movieseries passed final url check > '+url
                                    count +=1
                                    self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': url,'direct': False, 'debridonly': True})
                if dev_log=='true':
                    end_time = time.time() - self.start_time
                    send_log(self.name,end_time,count)                                    
            except:pass
        except:pass


        