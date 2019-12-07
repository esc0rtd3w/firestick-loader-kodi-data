import re,base64,time,xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search, filter_host, get_rd_domains,send_log,error_log            
import requests

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
 
class extramovies(Scraper):
    domains = ['http://extramovies.cc']
    name = "ExtraMovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://extramovies.cc'
        self.base_tv_link = 'https://extramovies.info'  
        if dev_log=='true':
            self.start_time = time.time()        

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            if not debrid:
                return []
            search_id = clean_search(title.lower())
            start_url = self.base_link + '/?s=' + search_id.replace(' ','+')
            #print '@@@@@'+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=10).content
            match = re.compile('<div class="thumbnail".+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(html)
            for url,item_name in match:
                if not clean_title(title).lower() in clean_title(item_name).lower():
                    continue
                if not year in item_name:
                    continue
                self.get_source(url)

            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = self.base_tv_link + '/?s=' + search_id.replace(' ','+')
            #print '@@@@@'+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content

            match = re.compile('class="post-item.+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(html)
            for url,item_name in match:
                
                if not clean_title(title).lower() in clean_title(item_name).lower():
                    continue
                    
                season_url = "0%s"%season if len(season)<2 else season
                episode_url = "0%s"%episode if len(episode)<2 else episode
                sea_epi ='S%sE%s'%(season_url,episode_url)
                count = 0
                headers={'User-Agent':User_Agent}
                OPEN = requests.get(url,headers=headers,timeout=5).content
                Regex = re.compile('href="(.+?)"',re.DOTALL).findall(OPEN)
                    
                for ep_url in Regex:
                    if not sea_epi in ep_url:
                        continue
                    if '1080p' in ep_url:
                        qual = '1080p'
                    elif '720p' in ep_url:
                        qual = '720p'
                    elif '480p' in ep_url:
                        qual = '480p'
                    else:
                        qual = 'SD'
                    count +=1
                    self.sources.append({'source': 'DirectLink', 'quality': qual, 'scraper': self.name, 'url': ep_url,'direct': True})
                if dev_log=='true':
                    end_time = time.time() - self.start_time
                    send_log(self.name,end_time,count)      
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources
            
    def get_source(self,url):
        try:
            #print 'CHKURL >'+url
            rez = url
            if '1080' in rez:
                res = '1080p'
            elif '720' in rez:
                res = '720p'
            else: 
                res = 'DVD'
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(url,headers=headers,timeout=10).content
            Regex = re.compile('href="/download.php.+?link=(.+?)"',re.DOTALL).findall(OPEN)
            count = 0

            for link in Regex:
                if 'server=' not in link:
                    #print 'base64 '+link
                    try:
                        link = base64.b64decode(link)
                    except:pass
                    #print 'pass me '+link
                    try:
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].lower()
                    except:pass
                    if not filter_host(host):
                        continue
                    rd_domains = get_rd_domains()
                    if host in rd_domains:
                        count +=1
                        self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': link,'direct': False,'debridonly': True})
                    else:
                        count +=1
                        self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': link,'direct': False})
            # if dev_log=='true':
                # end_time = time.time() - self.start_time
                # send_log(self.name,end_time,count)    # left off as multi prints due to multi pages
                             
        except:
            pass

