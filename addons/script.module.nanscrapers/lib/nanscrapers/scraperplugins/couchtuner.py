import re
import urllib,time,xbmcaddon
import requests,base64

from ..common import clean_title,clean_search, random_agent,filter_host,send_log,error_log
from ..scraper import Scraper

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'


class couchtuner(Scraper):
    domains = ['couchtuner']
    name = "CouchTuner"

    def __init__(self):
        self.base_link = 'http://couchtuner.unblocked.lol'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time() 

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            scrape = clean_search(title.lower())
            headers = {'User_Agent':User_Agent,'referer':self.base_link}
            link = requests.get(self.base_link+'/tv-lists/', headers=headers,timeout=5).content
            #print 'couch'+link
            Regex = re.compile('<h2>Tv Listing</h2>(.+?)<div class="comments_part">',re.DOTALL).findall(link)
            links = re.findall(r'<a href="([^"]+)".+?<strong>([^<>]*)</strong></a>', str(Regex), re.I|re.DOTALL)
            for media_url, media_title in links:
                if not clean_title(title).lower() == clean_title(media_title).lower():
                    continue
                print 'couchTUNER >>>> ' +media_url
                self.get_sources(media_url,season, episode)
 
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_sources(self,media_url,season,episode):
        print '::::::::::::::'+media_url
        try:
            epi_format = ('-season-%s-episode-%s-') %(season,episode)
            epi_format2 = ('-s%s-e%s-') %(season,episode)
            
            headers = {'User_Agent':User_Agent}
            link = requests.get(media_url, headers=headers, timeout=10).content
            episode_urls = re.compile('<li.+?strong><a href="([^"]+)"',re.DOTALL).findall(link)
            for eps in episode_urls:
                if epi_format in eps.lower() or epi_format2 in eps.lower():
                    #print 'This episode '+eps
                    headers = {'User_Agent':User_Agent}
                    EPISODE = requests.get(eps, headers=headers, timeout=10).content
                    holderpage = re.compile('<div class="entry".+?href="([^"]+)"',re.DOTALL).findall(EPISODE)[0]
                    #print 'HOLDERPAGE '+holderpage
                    headers = {'User_Agent':User_Agent}
                    final_page=requests.get(holderpage, headers=headers, timeout=10).content
                    sources = re.compile('<iframe src="([^"]+)"',re.DOTALL).findall(final_page)
                    count = 0
                    for final_url in sources:
                        host = final_url.split('//')[1].replace('www.','')
                        host = host.split('/')[0].lower()
                        if not filter_host(host):
                            continue
                        host = host.split('.')[0].title()
                        count +=1
                        self.sources.append({'source': host,'quality': 'DVD','scraper': self.name,'url': final_url,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                            

        except:pass
