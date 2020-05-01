import requests
import re
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search            
requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class Movie321(Scraper):
    domains = ['321movies.cc']
    name = "Movie321cc"
    sources = []

    def __init__(self):
        self.base_link = 'https://321movies.cc'
        self.search_url = '/?s='

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link + '/episodes/' + title.replace(' ','-') + '-' + season + 'x' + episode
            #print 'GW> '+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            #print 'PAGE > '+html
            match = re.compile('class="metaframe rptss" src="(.+?)"').findall(html)
            for link in match: 
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                if 'streamango.com' in link:
                    holder = requests.get(link).content
                    qual = re.compile('type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(holder)[0]
                    self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})            
                else:
                    self.sources.append({'source': host, 'quality': '720', 'scraper': self.name, 'url': link,'direct': False})
                                    
  
            return self.sources
        except Exception, argument:
            return self.sources                          

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = self.base_link + '/?s=' + search_id.replace(' ','+')
            #print 'GW> '+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            match = re.compile('class="thumbnail.+?href="(.+?)">.+?alt="(.+?)".+?class="year">(.+?)</span>',re.DOTALL).findall(html)
            for url,name,date in match:
                print 'CHK>>'+name
                if search_id in name.lower():
                    if date.replace(' ','') == year.replace(' ',''):
                        xbmc.log('year:'+year,xbmc.LOGNOTICE)
                        self.get_source(url)
            
            return self.sources
        except:
            pass
            return[]

    def get_source(self,url):
        try:
            
            #print 'FILM_URL= '+url
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(url,headers=headers,timeout=5).content
            Regex = re.compile('</iframe>.+?class="metaframe rptss" src="(.+?)"',re.DOTALL).findall(OPEN)
            for link in Regex: 
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                if 'streamango.com' in link:
                    holder = requests.get(link).content
                    qual = re.compile('type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(holder)[0]
                    self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})              
                else:
                    self.sources.append({'source': host, 'quality': '720', 'scraper': self.name, 'url': link,'direct': False})           
        except:
            pass

