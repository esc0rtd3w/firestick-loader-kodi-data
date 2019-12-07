import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_title

class hasthd(Scraper):
    domains = ['http://dl.hastidl.net']
    name = "hasthd"
    sources = []

    def __init__(self):
        self.base_link = 'http://dl.hastidl.net/remotes/'
                          

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url= self.base_link
            html = requests.get(start_url,timeout=5).content 
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                new_title = name.split('20')[0]
                if clean_title(title).lower()==clean_title(new_title).lower():
                    if year in url:
                        url = self.base_link+url
                        if '3D' in url:                                          
                            qual = '3D'
                        elif '1080p' in url:
                            qual = '1080p'
                        elif '720p' in url: 
                            qual = '720p'
                        elif '480p' in url:
                            qual = '480p'
                        else:
                            qual = 'SD'
                        self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []      


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url= self.base_link
            html = requests.get(start_url,timeout=5).content
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                if clean_title(title.lower()) in clean_title(name.lower()):

                       if len(season)==1:
                            season = '0'+season
                       if len(episode)==1:
                            episode = '0'+episode

                       episode_chk = 's%se%s' %(season,episode)
                       if episode_chk.lower() in url.lower():
                                    if '1080p' in url:
                                        qual = '1080p'
                                    elif '720p' in url:
                                        qual = '720p'
                                    elif '560p' in url:
                                        qual = '560p'
                                    elif '480p' in url:
                                        qual = '480p'
                                    else:
                                        qual = 'SD'
                                    url = self.base_link+url
                                    self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': url,'direct': True})
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []                     

#dl3().scrape_episode('the blacklist','','','4','1','','')
