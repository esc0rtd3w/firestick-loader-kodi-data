import re,urllib,urlparse
import xbmc,xbmcaddon,time
import resolveurl as urlresolver
from ..scraper import Scraper
import requests
from ..common import clean_title,clean_search, filter_host,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'



class seriescravings(Scraper):
    domains = ['http://series-craving.me']
    name = "SeriesCraving"
    sources = []

    def __init__(self):
        self.base_link = 'http://series-craving.me'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()
                     

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:

            episode_bollox ='-season-%s-episode-%s-' %(season,episode)
            
            start_url = "%s/search/%s" % (self.base_link, title.replace(' ','+').lower())
            #print start_url
            headers = {'User_Agent':User_Agent}
            OPEN = requests.get(start_url,headers=headers,timeout=5).content
            #print OPEN
            content = re.compile('<h1 class="entry-title".+?href="(.+?)" rel="bookmark">(.+?)</a>',re.DOTALL).findall(OPEN)
            for show_url,item_title in content:

                item_title=item_title.replace('Watch','').replace('Online','').replace('Free','')

                if not clean_title(title).lower() == clean_title(item_title).lower():
                    continue
                headers = {'User_Agent':User_Agent}
                page = requests.get(self.base_link+show_url,headers=headers,timeout=5).content 
                epis = re.compile('<li>.+?href="(.+?)"',re.DOTALL).findall(page)
                for url in epis:
                    if not episode_bollox in url:
                        continue
                    self.get_source(url)                        
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources  

            
    def get_source(self,url):
        try:   
            print 'checsspase '+url
            headers = {'User_Agent':User_Agent}
            links = requests.get(url,headers=headers,timeout=3).content   
            LINK = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(links)
            count = 0            
            for final_url in LINK:
                host = final_url.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                if 'openload' in final_url:
                    chk = requests.get(final_url).content
                    rez = re.compile('"description" content="(.+?)"',re.DOTALL).findall(chk)[0]
                    if '1080' in rez:
                        res='1080p'
                    elif '720' in rez:
                        res='720p'
                    else:
                        res ='SD'
                else: res = 'SD'
                if urlresolver.HostedMediaFile(final_url).valid_url():
                    count +=1
                    self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': final_url,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:pass

#seriescravings().scrape_episode('game of thrones', '', '', '7', '7', '', '')
