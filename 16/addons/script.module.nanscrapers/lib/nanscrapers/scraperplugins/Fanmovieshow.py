import re
import requests
import xbmc,time,xbmcaddon
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log
from nanscrapers.modules import cfscrape
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'


class fanmovieshow(Scraper):
    domains = ['www.fanmovieshow.com']
    name = "FanMovieShow"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.fanmovieshow.com'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers = {'User_Agent':User_Agent}
            html = self.scraper.get(start_url,headers=headers,timeout=5).content
            Regex = re.compile('<div class="title">.+?<a href="(.+?)">(.+?)</a>.+?<span class="year">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,name,date in Regex:
                if clean_title(title).lower() == clean_title(name).lower():
                    if year in date:
                        movie_link = item_url
                        self.get_source(movie_link)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers = {'User_Agent':User_Agent}
            html = self.scraper.get(start_url,headers=headers,timeout=5).content
            Regex = re.compile('<div class="title">.+?<a href="(.+?)">(.+?)</a>.+?<span class="year">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,name,year in Regex:
                if clean_title(title).lower() == clean_title(name).lower():
                    if "/tvshows/" in item_url:
                        show_link = item_url.replace('/tvshows/','/episodes/')+'-%sx%s'%(season,episode)
                        self.get_source(show_link)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_source(self,movie_link):
        try:
            html = self.scraper.get(movie_link).content
            links = re.compile('<iframe class="metaframe rptss" src="(.+?)"',re.DOTALL).findall(html)
            count = 0
            for link in links:
                if 'openload' in link:
                    try:
                        headers = {'User_Agent':User_Agent}
                        get_res=requests.get(link,headers=headers,timeout=5).content
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
                    end_time = time.time()
                    total_time = end_time - self.start_time
                    print (repr(total_time))+"<<<<<<<<<<<<<<<<<<<<<<<<<"+self.name+">>>>>>>>>>>>>>>>>>>>>>>>>total_time"
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

