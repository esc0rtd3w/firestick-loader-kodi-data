import re
import requests
import xbmc,xbmcaddon,time
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

session = requests.Session()

class cooltv(Scraper):
    domains = ['https://cooltvseries.com']
    name = "CoolTV"
    sources = []

    def __init__(self):
        self.base_link = 'https://cooltvseries.com'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()


    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search = clean_search(title.lower())
            start_url = '%s/search.php?search=%s' %(self.base_link,search)
            #print 'SEARCH > '+start_url
            headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Accept-Encoding':'gzip, deflate, sdch', 'User-Agent':random_agent()}
            link = requests.get(start_url,headers=headers,timeout=5).content
            #print link
            links = link.split('class="box"')
            for p in links:

                media_url = re.compile('href="([^"]+)"').findall(p)[0]
                media_title = re.compile('title="([^"]+)"').findall(p)[0]
                if search in clean_search(media_title.lower()):
                    if 'season %s' %season in media_title.lower():
                        self.get_source(media_url, season, episode)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources
                

    def get_source(self,media_url, season, episode):
        #print 'source season ' + media_url
        season_bollox = "0%s"%season if len(season)<2 else season
        episode_bollox = "0%s"%episode if len(episode)<2 else episode
        all_bollox = 's%se%s' %(season_bollox,episode_bollox)
            

        try:
            headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Accept-Encoding':'gzip, deflate, sdch', 'Accept-Language':'en-US,en;q=0.8',
                        'User-Agent':random_agent()}
            html = requests.get(media_url,headers=headers,timeout=5).content
            match = re.findall(r'<li><a href="([^"]+)">([^<>]*)<span.+?>', str(html), re.I|re.DOTALL)
            count = 0
            for media_url, media_title in match:

                if all_bollox in media_title.lower():
             
                    link = requests.get(media_url, headers=headers).content
                    
                    frame = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(link)
                    for frame_link in frame:
                        self.sources.append({'source':'Openload','quality': 'DVD','scraper': self.name,'url': frame_link,'direct': False})
                    

                    cool_links = re.compile('"dwn-box".+?ref="(.+?)" rel="nofollow">(.+?)<span',re.DOTALL).findall(link)
                    for vid_url,res in cool_links:
                        if '1080' in res:
                            res='1080p'                   
                        elif '720' in res:
                            res='720p'
                        elif 'HD' in res:
                            res='HD'
                        else:
                            res='SD'
                        count +=1    
                        self.sources.append({'source':'Direct','quality': res,'scraper': self.name,'url': vid_url,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)    
        except:
            pass
