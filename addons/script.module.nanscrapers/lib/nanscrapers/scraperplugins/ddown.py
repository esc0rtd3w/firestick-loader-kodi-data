import re
import requests
import xbmc,xbmcaddon,time
import urllib
from ..common import get_rd_domains, filter_host,send_log,error_log
from ..scraper import Scraper

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class ddown(Scraper):
    domains = ['https://directdownload.tv/']
    name = "Direct Download"
    sources = []

    def __init__(self):
        self.base_link = 'https://directdownload.tv/'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()
           
            

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:            
            if not debrid:
                return [] 
            season_url = "0%s"%season if len(season)<2 else season
            episode_url = "0%s"%episode if len(episode)<2 else episode

            start_url = 'https://directdownload.tv/api?key=4B0BB862F24C8A29&qualities/disk-480p,disk-1080p-x265,tv-480p,tv-720p,web-480p,web-720p,web-1080p,web-1080p-x265,movie-480p-x265,movie-1080p-x265&limit=50&keyword=%s+s%se%s' %(title.lower(),season_url,episode_url)
            start_url=start_url.replace(' ','%20')
            #SEND2LOG(start_url)

            content = requests.get(start_url).content
            #print 'content >> ' +content
            links=re.compile('"http(.+?)"',re.DOTALL).findall(content)
            count = 0
            for url in links:
                url = 'http' + url.replace('\/', '/')
                if '720p' in url:
                     res = '720p'
                elif '1080p' in url:
                    res = '1080p'  
                else:
                    res='480p'
                host = url.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower() 
                rd_domains = get_rd_domains() 
                if host in rd_domains:
                    if 'k2s.cc' not in url:
                        count +=1
                        self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': url,'direct': False, 'debridonly': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources  

    # def resolve(self, url):

            # return url
            

        
def SEND2LOG(Txt):
    print ':::::::::::::::::::::::::::::::::::::::::::::::::'
    print ':'
    print ': LOG string: ' + (str(Txt))
    print ':'
    print ':::::::::::::::::::::::::::::::::::::::::::::::::'
    return 