import re
import requests
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'


class azmovies(Scraper):
    domains = ['https://azmovies.ws']
    name = "azmovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://azmovies.ws/'   # added / here dont make work 4 self
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%ssearch.php?q=%s' %(self.base_link,search_id.replace(' ','+'))
            #xbmc.log('************ START '+repr(start_url),xbmc.LOGNOTICE)
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            Regex = re.compile('span class="play-btn".+?href="(.+?)".+?class="card-title title">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,name in Regex:
                #xbmc.log('************ URL '+repr(item_url),xbmc.LOGNOTICE)
                #xbmc.log('************ NAME '+repr(name),xbmc.LOGNOTICE)
                if not clean_title(title).lower() == clean_title(name).lower():  # think quicker
                    continue
                movie_link = self.base_link + item_url   # will now suffice
                #xbmc.log('************ MOVIE LINK '+repr(movie_link),xbmc.LOGNOTICE)
                self.get_source(movie_link,year)

            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/search.php?q=%s' %(self.base_link,search_id.replace(' ','+'))
            #xbmc.log('************ START '+repr(start_url),xbmc.LOGNOTICE)
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            Regex = re.compile('span class="play-btn".+?href="(.+?)".+?class="card-title title">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,name in Regex:

                show_check = '%s - Season%s' %(search_id,season)
                
                if not clean_title(show_check).lower() == clean_title(name).lower():
                    continue
                
                item_url = self.base_link + item_url
                print 'Psaee '+item_url                
                headers = {'User_Agent':User_Agent}
                season_page = requests.get(item_url,headers=headers,timeout=5).content
                episodes = re.compile('target="iframe" href="(.+?)"',re.DOTALL).findall(season_page)
                for link in episodes:

                    season_pull = "0%s"%season if len(season)<2 else season
                    episode_pull = "0%s"%episode if len(episode)<2 else episode
                    exact_episode = 's%se%s' %(season_pull,episode_pull)
                    
                    if not exact_episode.lower() in link.lower():
                        continue
                    if urlresolver.HostedMediaFile(link):
                        if '1080' in link:
                            qual = '1080p'
                        elif '720' in link:
                            qual='720p'
                        else:
                            qual='DVD'
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        self.sources.append({'source': host,'quality': qual,'scraper': self.name,'url': link,'direct': False})
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources            

            
    def get_source(self,movie_link,year):
        try:
            html = requests.get(movie_link).content
            year_confirm = re.compile('Release:(.+?)<br>',re.DOTALL).findall(html)[0]
            if year in year_confirm:
                Regex = re.compile("<ul id='serverul'(.+?)</ul>",re.DOTALL).findall(html)
                links = re.compile('<a href="(.+?)"',re.DOTALL).findall(str(Regex)) 
                count = 0
                for link in links:
                    if urlresolver.HostedMediaFile(link):
                        #xbmc.log('************ SOURCE'+repr(link),xbmc.LOGNOTICE)
                        if '1080' in link:
                            qual = '1080p'
                        elif '720' in link:
                            qual='720p'
                        else:
                            qual='DVD'
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        count +=1
                        self.sources.append({'source': host,'quality': qual,'scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:
            pass

