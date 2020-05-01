import re,xbmcaddon,time 
import resolveurl as urlresolver
import requests 
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class mvlinks(Scraper):
    domains = ['http://dl.newmyvideolink.xyz']
    name = "MyVideoLinks"
    sources = []

    def __init__(self):
        self.base_link = 'http://to.newmyvideolink.xyz'
        if dev_log=='true':
            self.start_time = time.time()        

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            season_pull = "0%s"%season if len(season)<2 else season
            episode_pull = "0%s"%episode if len(episode)<2 else episode
            
            movie_url = '%s/?s=%s+S%sE%s' %(self.base_link,search_id.replace(' ','+'),season_pull,episode_pull)

            headers = {'User_Agent':User_Agent}
            link = requests.get(movie_url,headers=headers,timeout=5).content
            
            links = link.split('post-title')
            for p in links:

                m_url = re.compile('href="([^"]+)"').findall(p)[0]
                m_title = re.compile('title="([^"]+)"').findall(p)[0]

                if not 's%se%s' %(season_pull,episode_pull) in m_title.lower():
                    continue
                self.get_source(m_url)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources
        
    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            
            search_id = clean_search(title.lower())
            movie_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers = {'User_Agent':User_Agent}
            
            link = requests.get(movie_url,headers=headers,timeout=5).content
            
            links = link.split('post-title')
            for p in links:

                m_url = re.compile('href="([^"]+)"').findall(p)[0]
                m_title = re.compile('title="([^"]+)"').findall(p)[0]
                if ' 20' in m_title:
                    name = m_title.split(' 20')[0]
                elif ' 19' in m_title:
                    name = m_title.split(' 19')[0]
                else:
                    name = m_title
                    
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                if not year in m_title.lower():
                    continue
                self.get_source(m_url)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_source(self,m_url):
        try:         
            OPEN = requests.get(m_url).content
            match = re.compile('<li><a href="(.+?)"').findall(OPEN)
            count = 0
            for link in match:
                if not urlresolver.HostedMediaFile(link).valid_url(): 
                    continue                
                label = link.split('//')[1].replace('www.','')
                label = label.split('/')[0].split('.')[0].title()
                label = label.replace('Ul','Uploaded')
                if '720' in link:
                    rez='720p'
                elif '1080' in link:
                    rez='1080p'
                else: 
                    rez='DVD'
                count +=1    
                self.sources.append({'source': label,'quality': rez,'scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                
        except:
            pass
