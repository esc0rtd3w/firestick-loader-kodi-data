import base64
import re,time,xbmcaddon

import requests
from ..common import clean_title,clean_search,random_agent,filter_host,send_log,error_log
from ..scraper import Scraper
import xbmcaddon

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

class primealt(Scraper):
    domains = ['primewire.io']
    name = "Primeio"
    sources = []

    def __init__(self):
        self.base_link = 'http://www.primewire.io'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):        
        try:                       
            movie_id  = clean_search(title.lower().replace(' ','%20'))

            headers={'User-Agent':random_agent()}

            start_url = "%s/search/%s" % (self.base_link, movie_id)
            #print 'Search primeURL>  '+start_url
            headers = {'User_Agent':random_agent()}
            OPEN = requests.get(start_url,headers=headers,timeout=5).content
            content = re.compile('<p><b><a href="(.+?)".+?FONTSIZE.+?>(.+?)<font color="#8B4513">(.+?)</font>',re.DOTALL).findall(OPEN)
            for show_url,item_title,date in content:

                if not clean_title(title).lower() == clean_title(item_title).lower():
                    continue
                if not year in date:
                    continue
                self.get_source(show_url)   
                        
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:           
            show_id  = clean_search(title.lower().replace(' ','%20'))

            headers={'User-Agent':random_agent()}

            start_url = "%s/searchtv/%s" % (self.base_link, show_id)
            #print 'Search primeURL>  '+start_url
            headers = {'User_Agent':random_agent()}
            OPEN = requests.get(start_url,headers=headers,timeout=5).content
            content = re.compile('<div class="item".+?href="(.+?)"',re.DOTALL).findall(OPEN)
            for show_url in content:

                if clean_title(title).lower() in clean_title(show_url).lower():
                    #if year in show_url:   ##year not passed in bob

                        headers = {'User_Agent':random_agent()}
                        episodes = requests.get(show_url,headers=headers,timeout=5).content

                        eps = re.compile('class="tv_episode_item".+?href="(.+?)"',re.DOTALL).findall(episodes)
                        for episode_url in eps:
                            #print episode_url
                            
                            ep_chk = '-season-%s-episode-%s.html' %(season,episode)
                            if not episode_url.endswith(ep_chk):
                                continue
                            self.get_source(episode_url)                        
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources  






    def get_source(self,episode_url):
        try: 
            #print 'xPassedPrimewire URL >'+episode_url       
            headers = {'User_Agent':random_agent()}
            content = requests.get(episode_url,headers=headers,timeout=3).content 

            links = re.compile('data-height="460">(.+?)<',re.DOTALL).findall(content)
            count = 0
            for host_url in links:
                if self.base_link in host_url:
                    host = re.compile('movie=(.+?)&',re.DOTALL).findall(host_url)[0]
                    final_url = base64.b64decode(host)

                else:
                    final_url = host_url
                host = final_url.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                if not filter_host(host):
                    continue
                host = host.split('.')[0].title()
                count +=1
                self.sources.append({'source': host,'quality': 'SD','scraper': self.name,'url': final_url,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                

        except:pass


