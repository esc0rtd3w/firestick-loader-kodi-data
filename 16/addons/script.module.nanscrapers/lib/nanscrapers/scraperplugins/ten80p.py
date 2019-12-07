import requests,re,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log 

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
                                           
class ten80p(Scraper):
    domains = ['1080pMovies.com']
    name = "1080pMovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://1080pmovie.com'
        if dev_log=='true':
            self.start_time = time.time()                     

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = self.base_link + '/?s=%s' %search_id.replace(' ','+')
            #print 'STARTURL:::::::::::::::: '+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content

            Links = re.compile('class="video-item" href="(.+?)".+?<h4>(.+?)</h4>',re.DOTALL).findall(html)
            count = 0
            for link,name in Links:

                if not clean_title(title).lower() == clean_title(name).lower(): 
                    continue
                if not year in name:
                    continue
                #print 'pass link> ' + link
                holder = requests.get(link,headers=headers,timeout=5).content
                new = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(holder)[0]
                end = requests.get(new,headers=headers,timeout=5).content
                final_url = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(end)[0]
                count +=1
                self.sources.append({'source': 'Openload','quality': '1080p','scraper': self.name,'url': final_url,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

