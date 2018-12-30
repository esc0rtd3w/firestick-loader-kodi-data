import re
import requests
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log
import base64

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'


class one23moviess(Scraper):
    domains = ['123moviess.online']
    name = "123moviess"
    sources = []

    def __init__(self):
        self.base_link = 'http://123moviess.online'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/filter/?cat=movie&search=%s&actor=&director=&sg[]=All&year=&advanced_search=true' %(self.base_link,search_id.replace(' ','+'))
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            Regex = re.compile('<div class="movie-item">.+?href="(.+?)".+?<h2>(.+?)</h2>.+?div class="jt-info">.+?class="jt-info">(.+?)</div>',re.DOTALL).findall(html)
            for item_url,name,date in Regex:
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                if not year in date:
                    continue
                movie_link = self.base_link + item_url
                self.get_source(movie_link)

            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/filter/?cat=tv&search=%s&actor=&director=&sg[]=All&year=&advanced_search=true' %(self.base_link,search_id.replace(' ','+'))
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            Regex = re.compile('<div class="movie-item">.+?href="(.+?)".+?<h2>(.+?)</h2>',re.DOTALL).findall(html)
            for item_url,name in Regex:
                if clean_title(title).lower() == clean_title(name).lower():
                    show_link = self.base_link + item_url
                    episode_format = '-season-%s-episode-%s-' %(season,episode)
                    headers = {'User_Agent':User_Agent}
                    show_page = requests.get(show_link,headers=headers,timeout=5).content
                    episodes = re.compile('class="tv_episode.+?href="(.+?)"',re.DOTALL).findall(show_page)
                    for epis_link in episodes:
                        if episode_format in epis_link:
                            movie_link = self.base_link + epis_link
                            self.get_source(movie_link)

            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_source(self,movie_link):
        try:
            headers = {'User-Agent':User_Agent}
            html = requests.get(movie_link,headers=headers,timeout=5).content
            sources = re.compile("onClick=\"showplayer\('(.+?)'",re.DOTALL).findall(html)
            count = 0
            for link in sources:
                link = base64.b64decode(link)
                host_url = re.compile("(http.+?)&",re.DOTALL).findall(link)[0]
                if 'streamango' in host_url:
                    try:
                        headers = {'User-Agent':User_Agent}
                        get_res = open_url(host_url, headers=headers,timeout=5).content
                        rez = re.compile('{type:"video/mp4".+?height:(.+?),',re.DOTAll).findall(get_res)[0]
                        if '1080' in rez:
                            qual = '1080p'
                        elif '720' in rez:
                            qual = '720p'
                        else:
                            qual = 'DVD'
                    except: qual = 'DVD'
                    count+=1
                    self.sources.append({'source': 'Streamango','quality': qual,'scraper': self.name,'url': host_url,'direct': False})
                elif 'openload' in host_url:
                    try:
                        headers = {'User-Agent':User_Agent}
                        get_res = open_url(host_url, headers=headers,timeout=5).content
                        rez = re.compile('description" content="(.+?)"',re.DOTAll).findall(get_res)[0]

                        if '1080' in rez:
                            qual = '1080p'
                        elif '720' in rez:
                            qual = '720p'
                        else:
                            qual = 'DVD'
                    except: qual = 'DVD'
                    count+=1
                    self.sources.append({'source': 'Openload','quality': qual,'scraper': self.name,'url': host_url,'direct': False})
                else:
                    if not urlresolver.HostedMediaFile(host_url).valid_url():
                        continue
                    host = host_url.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    count +=1
                    self.sources.append({'source': host,'quality': 'DVD','scraper': self.name,'url': host_url,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                        

        except:
            pass

