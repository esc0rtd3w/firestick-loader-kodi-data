import requests
import re
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")  
                                           
class freedownload(Scraper):
    domains = ['http://freemoviedownloads6.com']
    name = "FreeDownload"
    sources = []

    def __init__(self):
        self.base_link = 'http://freemoviedownloads6.com'
        self.goog = 'https://www.google.co.uk'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
        
            scrape = clean_search(title.lower()).replace(' ','+')

            start_url = '%s/search?q=freemoviedownloads6.com+%s+%s' %(self.goog,scrape,year)
            #print 'START> '+start_url
            headers = {'User-Agent':random_agent()}

            html = requests.get(start_url,headers=headers,timeout=3).content

            results = re.compile('href="(.+?)"',re.DOTALL).findall(html)
            for url in results:

                if self.base_link in url:

                    if scrape.replace('+','-') in url:
                        if 'webcache' in url:
                            continue
                        self.get_source(url,title,year)

            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_source(self,url,title,year):
        try:
            #print 'cfwds %s %s %s' %(url,title,year)
            confirm_name = clean_title(title.lower()) + year 

            
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(url,headers=headers,timeout=5).content
            
            getTit = re.compile('<title>(.+?)</title>',re.DOTALL).findall(OPEN)[0]
            getTit = getTit.split('Free')[0]
            
            if clean_title(getTit.lower()) == confirm_name:
                #print 'This Movie + '+getTit
                OPEN = OPEN.split("type='video/mp4'")[1]
                Regex = re.compile('href="(.+?)"',re.DOTALL).findall(OPEN)
                count = 0
                for link in Regex:
                    if '1080' in link:
                        res = '1080p'
                    elif '720' in link:
                        res = '720p'
                    elif '480' in link:
                        res = '480p'
                    else:
                        res = 'SD'                
                    if '.mkv' in link:
                        count +=1
                        self.sources.append({'source': 'DirectLink', 'quality': res, 'scraper': self.name, 'url': link,'direct': True})
                    if '.mp4' in link:
                        count +=1
                        self.sources.append({'source': 'DirectLink', 'quality': res, 'scraper': self.name, 'url': link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                                
        except:
            pass

