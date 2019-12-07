import requests
import resolveurl as urlresolver
import urlparse
import re,xbmcaddon,time 
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
import base64
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
  
class kakitube(Scraper):
    domains = ['http://kakitube.se']
    name = "KakiTube"
    sources = []

    def __init__(self):
        self.base_link = 'http://kakitube.se/'
        if dev_log=='true':
            self.start_time = time.time()                                                    


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                                                                                                           #(movie name keeping spaces removing excess characters)

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))  
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content     
            match = re.compile('class="image"><div.+?href="(.+?)".+?alt="(.+?)".+?class="year">(.+?)<',re.DOTALL).findall(html)
            for item_url, name, year in match:
                if year in year:                                                        
                    if clean_title(search_id).lower() == clean_title(name).lower():
                        movie_link = item_url
                        self.get_source(movie_link)  
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self,title,show_year,year,season,episode,imdb,tvdb,debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            match = re.compile('class="image"><div.+?href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
            for item_url, name in match:
                if not clean_title(search_id).lower() == clean_title(name).lower():
                    continue
                if "/tvshows/" in item_url:
                    movie_link = item_url[:-1].replace('/tvshows/','/episodes/')+'-%sx%s/'%(season,episode)
                    self.get_source(movie_link)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources                                


            
    def get_source(self,item_url):
        try:
            #print 'kakitube ' + item_url
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content
            Endlinks = re.compile('<iframe id=.+?show=(.+?)"',re.DOTALL).findall(OPEN)
            count = 0
            for link in Endlinks:
                host_url = base64.b64decode(link)
                if 'openload' in host_url:
                    try:
                        headers = {'User_Agent':User_Agent}
                        get_res=requests.get(host_url,headers=headers,timeout=5).content
                        rez = re.compile('',re.DOTALL).findall(get_res)[0]
                        if '1080' in rez:
                            qual = '1080p'
                        elif '720' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                    except: qual='DVD' 
                    count +=1
                    self.sources.append({'source': 'Openload','quality': qual,'scraper': self.name,'url': host_url,'direct': False})

                elif 'streamango' in host_url:
                    try:  
                        headers = {'User_Agent':User_Agent}
                        get_res=requests.get(host_url,headers=headers,timeout=5).content
                        rez = re.compile('',re.DOTALL).findall(get_res)[0]
                        if '1080' in rez:
                            qual = '1080p'
                        elif '720' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                    except: qual='DVD'  
                    count +=1
                    self.sources.append({'source': 'Streamango','quality': qual,'scraper': self.name,'url': host_url,'direct': False})


                else:
                    if urlresolver.HostedMediaFile(host_url):
                        
                        host = host_url.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        count +=1
                        self.sources.append({'source': host,'quality': 'DVD','scraper': self.name,'url': host_url,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)       
        except:
            pass 