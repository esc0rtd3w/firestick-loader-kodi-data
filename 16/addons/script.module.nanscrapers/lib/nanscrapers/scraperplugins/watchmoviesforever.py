import re
import requests
import xbmc,time,xbmcaddon
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log 
from nanscrapers.modules import cfscrape
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'



class watchmoviesforever(Scraper):
    domains = ['watchmoviesforever.com']
    name = "WatchMoviesForever"
    sources = []

    def __init__(self):
        self.base_link = 'http://watchmoviesforever.com'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time() 

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers = {'User_Agent':User_Agent}
            html = self.scraper.get(start_url,headers=headers,timeout=5).content
            Regex = re.compile('<div class="boxinfo">.+?<a href="(.+?)">.+?<span class="tt">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,name in Regex:
                if clean_title(title).lower() == clean_title(name).lower():
                    if year in name:
                        movie_link = item_url
                        self.get_source(movie_link)
                
            return self.sources
        except Exception, argument:
            return self.sources

    def get_source(self,movie_link):
        try:
            html = self.scraper.get(movie_link).content
            links = re.compile('<div class="movieplay".+?href="(.+?)"',re.DOTALL).findall(html)
            count = 0
            for link in links:
                if 'openload' in link:
                    try:
                        headers = {'User_Agent':User_Agent}
                        get_res=self.scraper.get(link,headers=headers,timeout=5).content
                        rez = re.compile('description" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                        if '1080p' in rez:
                            qual = '1080p'
                        elif '720p' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                    except: qual='DVD'
                    count +=1                    
                    self.sources.append({'source': 'Openload','quality': qual,'scraper': self.name,'url': link,'direct': False})
                elif 'streamango' in link:
                    try:
                        headers = {'User_Agent':User_Agent}
                        get_res=self.scraper.get(link,headers=headers,timeout=5).content
                        rez = re.compile('{type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(get_res)[0]
                        if '1080' in rez:
                            qual = '1080p'
                        elif '720' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                    except: qual='DVD'    
                    count +=1
                    self.sources.append({'source': 'Streamango','quality': qual,'scraper': self.name,'url': link,'direct': False})

                elif 'vidoza' in link:
                    try:
                        headers = {'User_Agent':User_Agent}
                        get_res=self.scraper.get(link,headers=headers,timeout=5).content
                        rez = re.compile('label:"(.+?)"',re.DOTALL).findall(get_res)[0]
                        if '1080p' in rez:
                            qual = '1080p'
                        elif '720p' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                    except: qual='DVD'
                    count +=1                    
                    self.sources.append({'source': 'Vidoza','quality': qual,'scraper': self.name,'url': link,'direct': False})
                elif 'rapidvideo' in link:
                    try:
                        headers = {'User_Agent':User_Agent}
                        get_res=self.scraper.get(link,headers=headers,timeout=5).content
                        rez = re.compile('og:title" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                        if '1080p' in rez:
                            qual = '1080p'
                        elif '720p' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                    except: qual='DVD'  
                    count +=1
                    self.sources.append({'source': 'Rapidvideo','quality': qual,'scraper': self.name,'url': link,'direct': False})
                else:
                    qual = 'DVD'
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    count +=1
                    self.sources.append({'source': host,'quality': qual,'scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)

        except:
            pass

