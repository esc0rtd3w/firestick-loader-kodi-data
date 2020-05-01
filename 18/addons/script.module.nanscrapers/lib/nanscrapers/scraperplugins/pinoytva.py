import requests
import re
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log 

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

class pinoytva(Scraper):
    domains = ['https://pinoytva.su']
    name = "Pinoytva"
    sources = []

    def __init__(self):
        self.base_link = 'https://pinoytva.su'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            search_link = '/search/%s.html' %(search_id.replace(" ","-"))
            start_url = self.base_link+search_link
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            match = re.compile('<li class="film-item ">.+?<a href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            count = 0
            for link,name in match:
                if clean_title(search_id).lower() == clean_title(name).lower():
                    html2 = requests.get(link).content
                    block = re.compile('var playerInstance.+?file: "(.+?)"',re.DOTALL).findall(html2)
                    #match2 = re.compile('file.+?"(.+?)"',re.DOTALL).findall(str(block))
                    #print block
                    for link2 in block:
                        count +=1
                        final_link = link2.replace("\\","")
                        self.sources.append({'source': self.name, 'quality': 'SD', 'scraper': self.name, 'url': final_link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)            
                    
            return self.sources
        except:
            pass
            return[]



