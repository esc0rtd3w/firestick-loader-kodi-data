import requests
import re
import xbmc,xbmcaddon,time
import time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

  
class tubitv(Scraper):
    domains = ['tubitv.com']
    name = "TubiTv"
    sources = []

    def __init__(self):
        self.base_link = 'https://tubitv.com'
        if dev_log=='true':
            self.start_time = time.time()                                                    


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/search/%s' %(self.base_link,search_id.replace(' ','%20'))
            #print '::::::::::::: START URL '+start_url
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            #print html
            match = re.compile('"@type":"Movie","name":"(.+?)","url":"(.+?)".+?"dateCreated":"(.+?)"',re.DOTALL).findall(html)
            for name ,item_url, rel in match:
                #print 'item_url>>>>>>>>>>>>>> '+item_url
                #print 'name>>>>>>>>>>>>>> '+name
                if year in rel:
                    
                    if clean_title(search_id).lower() == clean_title(name).lower():
                        #print 'Send this URL> ' + item_url
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

            Endlinks = re.compile('"video":.+?"url":"(.+?)"',re.DOTALL).findall(OPEN)
            count = 0
            for link in Endlinks:
                link = 'https:'+link.replace('\u002F','/')
                if '1080' in link:
                    label = '1080p'
                elif '720' in link:
                    label = '720p'
                else:
                    label = 'HD'
                count +=1    
                self.sources.append({'source': 'TubiTv', 'quality': label, 'scraper': self.name, 'url': link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)        
        except:
            pass
#tubitv().scrape_movie('bullet boy', '2005','') 
 