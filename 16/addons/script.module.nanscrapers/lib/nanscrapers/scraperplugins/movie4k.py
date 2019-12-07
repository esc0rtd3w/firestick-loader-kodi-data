import re,time,xbmcaddon
import requests
import resolveurl as urlresolver
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'


class movie4k(Scraper):
    domains = ['movie4k.is']
    name = "Movie4k"
    sources = []

    def __init__(self):
        self.base_link = 'https://movie4k.is'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers = {'User_Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            #print html
            
            Regex = re.compile('<div class="boxinfo".+?href="(.+?)".+?class="tt">(.+?)</span>.+?class="year">(.+?)<',re.DOTALL).findall(html)
            for item_url,name,rel in Regex:
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                if not year == rel:
                    continue
                movie_link = item_url
                #print movie_link,name,rel
                self.get_source(movie_link,year)
            
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_source(self,movie_link,year):
        try:
            html = requests.get(movie_link).content
            qual = re.compile('<span class="calidad2">(.+?)</span>',re.DOTALL).findall(html)[0]
            links = re.compile('class="movieplay".+?src="(.+?)/"',re.DOTALL).findall(html)
            count = 0
            for link in links:
                if urlresolver.HostedMediaFile(link).valid_url():
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    count +=1
                    self.sources.append({'source': host,'quality': qual,'scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)            
        except:
            pass

#movie4k().scrape_movie('bright', '2017','') 