import requests
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
from ..common import clean_title, clean_search,send_log,error_log
from ..scraper import Scraper

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")            
requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class movie4u(Scraper):
    domains = ['https://movie4u.ch']
    name = "movie4u"
    sources = []

    def __init__(self):
        self.base_link = 'https://movie4u.ch'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print 'GW> '+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            match = re.compile('<div class="title">.+?href="(.+?)">(.+?)</a>.+?class="year">(.+?)</span>',re.DOTALL).findall(html)
            for url,name,date in match:
                if ' 20' in name:
                    name = name.split(' 20')[0]
                elif ' 19' in name:
                    name = name.split(' 19')[0]
                else: name = name
                    
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                if not year in date:
                    continue
                self.get_source(url)
            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))

            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers, timeout=3).content
            #print 'PAGE>>>>>>>>>>>>>>>>>'+html
            Regex = re.compile('class="title".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(html)
            for item_url,name in Regex:

                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                headers = {'User_Agent':User_Agent}
                content = requests.get(item_url,headers=headers, timeout=3).content

                epi_link='%sx%s/' % (season,episode)
                    
                match=re.compile('class="imagen"><a href="(.+?)">').findall(content)
                for ep_url in match:
                    if not epi_link in ep_url:
                        continue
                    movie_link = ep_url
                    #error_log(self.name + ' PassUrl',movie_link)
                    self.get_source(movie_link)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources
            
    def get_source(self,url):
        try:
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(url,headers=headers,timeout=10).content
            Regex = re.compile('class="metaframe rptss" src="(.+?)"',re.DOTALL).findall(OPEN)
            count = 0
            for link in Regex:
                if not urlresolver.HostedMediaFile(link).valid_url():
                    continue
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                #print 'm4u link > '+link

                if '1080' in link:
                    rez = '1080p'
                elif '720' in link:
                    rez = '720p'
                else: rez = 'SD'
                count +=1
                self.sources.append({'source': host,'quality': rez,'scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                   
        except:
            pass
