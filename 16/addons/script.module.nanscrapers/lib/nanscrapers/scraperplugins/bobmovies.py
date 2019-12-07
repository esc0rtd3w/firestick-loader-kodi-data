import re,xbmcaddon,time,requests
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log    
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")           

class bobmovies(Scraper):
    domains = ['bobmovies.com']
    name = "Bobmovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://bobmovies.net'
        self.sources = []
        self.start_time = ''

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            if dev_log=='true':
                self.start_time = time.time()
            scrape = clean_search(title.lower())
            
            headers = {'User-Agent':random_agent(),'referrer':self.base_link}

            data = {'do':'search','subaction':'search','story':scrape}
        
            html = requests.post(self.base_link,headers=headers,data=data,verify=False,timeout=5).content
            
            results = re.compile('class="nnoo short_story".+?href="(.+?)".+?class="genre short_story_genre">(.+?)</span>.+?<p>(.+?)</p>',re.DOTALL).findall(html)
            for url,date,item_title in results:

                if not clean_title(title).lower() == clean_title(item_title).lower():
                    continue
                if not year in date: 
                    continue
                #error_log(self.name + ' passed_bobURL',start_url)
                self.get_source(url)
                        
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_source(self,url):
        try:
            headers={'User-Agent':random_agent()}
            html = requests.get(url,headers=headers,timeout=5).content
            
            vidpage = re.compile('id="tab-movie".+?data-file="(.+?)"',re.DOTALL).findall(html)
            count = 0
            for link in vidpage:
                if 'trailer' not in link.lower():
                    link = self.base_link + link
                    count +=1
                    self.sources.append({'source': 'DirectLink','quality': '720p','scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                          
        except:
            pass