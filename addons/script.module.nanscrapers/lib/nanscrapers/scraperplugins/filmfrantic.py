import requests
import resolveurl as urlresolver
import urlparse
import re,xbmcaddon,time 
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
  
class filmfrantic(Scraper):
    domains = ['http://filmfrantic.com']
    name = "FilmFrantic"
    sources = []

    def __init__(self):
        self.base_link = 'http://filmfrantic.com'
        if dev_log=='true':
            self.start_time = time.time()                                                    


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                                                                                                           #(movie name keeping spaces removing excess characters)

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))             
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content     
            
            match = re.compile('<article id=.+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(html)
            for item_url, name in match:
                if year in name:                                                        
                    if clean_title(search_id).lower() == clean_title(name).lower():  
                        self.get_source(item_url)  
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

            
    def get_source(self,item_url):
        try:
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content

            Endlinks = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(OPEN)
            count = 0
            for link in Endlinks:
                if 'openload' in link:
                    try:
                        headers = {'User_Agent':User_Agent}
                        get_res=requests.get(link,headers=headers,timeout=5).content
                        rez = re.compile('class="label" title="(.+?)"',re.DOTALL).findall(get_res)[0]
                        if '1080p' in rez:
                            qual = '1080p'
                        elif '720p' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                    except: qual='DVD' 
                    count +=1
                    self.sources.append({'source': 'Openload','quality': qual,'scraper': self.name,'url': link,'direct': False})


                else:
                    if urlresolver.HostedMediaFile(link):
                        
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        count +=1
                        self.sources.append({'source': host,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)       
        except:
            pass 