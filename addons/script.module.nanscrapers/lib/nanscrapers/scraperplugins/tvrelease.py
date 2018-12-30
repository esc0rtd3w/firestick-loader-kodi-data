import re
import requests
import xbmc,xbmcaddon,time
import urllib
from ..common import get_rd_domains,send_log,error_log
from ..scraper import Scraper
from nanscrapers.modules import cfscrape

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
##Multi log returns
class tvrelease(Scraper):
    domains = ['http://tv-release.pw']
    name = "TVRelease"
    sources = []

    def __init__(self):
        self.base_link = 'http://tv-release.pw/'
        self.scraper = cfscrape.create_scraper()
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            if not debrid:
                return []
            start_url = "%s?s=%s+%s&cat=Movies-XviD,Movies-720p,Movies-480p,Movies-Foreign,Movies-DVDR,"%(self.base_link,title.replace(' ','+').lower(),year)
            #SEND2LOG(start_url)
            headers = {'User_Agent':User_Agent}
            OPEN = self.scraper.get(start_url,headers=headers,verify=False).content
            
            content = re.compile("href='http://tv-release.pw/(\d*\/.+?)'",re.DOTALL).findall(OPEN)
            for url in content:
                result = '%s%s'%(self.base_link,url)
                if '1080' in url:
                    self.get_source(result)    
                elif '720' in url:
                    self.get_source(result)  
                else:pass
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources            
            

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            if not debrid:
                return []
            season_url = "0%s"%season if len(season)<2 else season
            episode_url = "0%s"%episode if len(episode)<2 else episode

            start_url = "%s?s=%s%sS%sE%s&cat=&cat=TV-XviD,TV-Mp4,TV-720p,TV-480p," % (self.base_link, title.replace(' ','+').lower(),
                                                          '%20', season_url, episode_url)
            #SEND2LOG(start_url)
            headers = {'User_Agent':User_Agent}
            OPEN = self.scraper.get(start_url,headers=headers,verify=False).content

            content = re.compile("href='http://tv-release.pw/(\d*\/.+?)'",re.DOTALL).findall(OPEN)
            for url in content:
                result = '%s%s'%(self.base_link,url)
                if '1080' in url:
                    self.get_source(result)    
                elif '720' in url:
                    self.get_source(result)  
                else:pass    
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sourcess  

            
    def get_source(self,url):
        try:    
            res_check=url
            headers = {'User_Agent':User_Agent}
            links = self.scraper.get(url,headers=headers,verify=False).content   
            link = re.compile("class=\"td_cols\".+?href='(.+?)'").findall(links)
            count = 0  
            for url in link:
                if '720' in res_check.lower():
                    res = '720p'
                elif '1080' in res_check.lower():
                    res = '1080p'
                else:
                    res='SD'
                if not '.rar' in url:
                    if not 'go4up.com' in url:
                        if not 'multiup' in url: 
                            host = url.split('//')[1].replace('www.','')
                            host = host.split('/')[0].split('.')[0].title()
                            count +=1                        
                            self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': url,'direct': False, 'debridonly': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                
        except:pass
        
# def SEND2LOG(Txt):
#     print ':::::::::::::::::::::::::::::::::::::::::::::::::'
#     print ':'
#     print ': LOG string: ' + (str(Txt))
#     print ':'
#     print ':::::::::::::::::::::::::::::::::::::::::::::::::'
#     return 