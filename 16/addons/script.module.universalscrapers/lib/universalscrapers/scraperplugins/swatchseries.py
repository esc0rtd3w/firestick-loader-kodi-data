
import re,requests,base64
import urllib,time,xbmcaddon
from ..common import clean_title,clean_search, random_agent,filter_host,send_log,error_log
from ..scraper import Scraper

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'


class mywatchseries(Scraper):
    domains = ['swatchseries.to']
    name = "SwatchSeries"


    def __init__(self):
        self.base_link = 'https://www1.swatchseries.to'
        self.sources = []


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time() 
            scrape = clean_search(title.lower())
            start_url = '%s/search/%s' %(self.base_link,scrape.replace(' ','%20'))
            headers = {'User_Agent':User_Agent,'referer':self.base_link}
            link = requests.get(start_url, headers=headers,timeout=5).content
            link = link.split('Search results')[1:]
            links = re.findall(r'<a href="([^"]+)" title=".*?" target="_blank"><strong>([^<>]*)</strong></a>', str(link), re.I|re.DOTALL)
            for media_url, media_title in links:
                if not clean_title(title).lower() == clean_title(media_title).lower():
                    continue
                self.get_sources(media_url,title,year,season,episode,start_time)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources


    def get_sources(self,url,title,year,season,episode,start_time):
        try:
            headers = {'User_Agent':User_Agent}
            link = requests.get(url, headers=headers, timeout=10).content
            links = link.split('<li id="episode')[1:]
            count = 0
            for p in links:
                media_url = re.compile('href="([^"]+)"').findall(p)[0]
                sep = 's%s_e%s' %(season, episode)
                if sep in media_url.lower():
                    link2 = requests.get(media_url, headers=headers, timeout=10).content
                    sources = re.findall(r'cale\.html\?r=(.*?)"', str(link2), re.I|re.DOTALL)
                    uniques = []
                    for hosts in sources:
                        final_url = hosts.decode('base64')
                        if final_url not in uniques:
                            uniques.append(final_url)
                            host = final_url.split('//')[1].replace('www.','')
                            host = host.split('/')[0].lower()
                            if host in str(self.sources):
                                continue
                            if not filter_host(host):
                                continue
                            host = host.split('.')[0].title()
                            count +=1
                            self.sources.append({'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': final_url, 'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)                            
        except:
            pass


