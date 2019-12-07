import re
import requests
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log 
#from nanscrapers.modules import cfscrape 
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'


class OpenLoadMovie(Scraper):
    domains = ['https://openloadmovie.me']
    name = "openloadmovie"
    sources = []

    def __init__(self):
        self.base_link = 'https://openloadmovie.me'
        #self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            # start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            # headers = {'User_Agent':User_Agent}
            # html = requests.get(start_url,headers=headers,timeout=5).content
            # #xbmc.log('************ Passed'+repr(html),xbmc.LOGNOTICE)
            # Regex = re.compile('class="result-item".+?href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)   
            # for item_url,name in Regex:    # removed date as date isnt seperate
                # if not clean_title(title).lower() == clean_title(name).lower():
                    # continue
                # if not year in name:
                    # continue
                # movie_link = item_url
                # #print 'Grabbed movie url to pass > ' + movie_link   
            movie_link = '%s/movies/%s-%s/' %(self.base_link,search_id.replace(' ','-'),year)
            print 'Grabbed movie url to pass > ' + movie_link 
            self.get_source(movie_link)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    # def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        # try:
            # search_id = clean_search(title.lower())
            # # start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            # # headers = {'User_Agent':User_Agent}
            # # html = requests.get(start_url,headers=headers,timeout=5).content
            # # Regex = re.compile('class="result-item".+?href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
            # # for item_url,name in Regex:
                # # if not clean_title(title).lower() == clean_title(name).lower():
                    # # continue
                # # if "/tvshows/" in item_url:
                    # # movie_link = item_url[:-5].replace('/tvshows/','/episodes/')+'%sx%s/'%(season,episode)
            # movie_link = '%s/episodes/%s-%sx%s/' %(self.base_link,search_id.replace(' ','-'),season,episode)  
            # print 'Grabbed movie url to pass > ' + movie_link
            # self.get_source(movie_link)
                
            # return self.sources
        # except Exception, argument:        
            # if dev_log == 'true':
                # error_log(self.name,'Check Search')
            # return self.sources

    def get_source(self,movie_link):
        try:
            #print 'passed show '+movie_link
            html = requests.get(movie_link).content
            links = re.compile('data-lazy-src="(.+?)"',re.DOTALL).findall(html)
            count = 0
            for link in links:                
                if 'youtube' not in link:   
                    if '1080p' in link:
                        qual = '1080p'
                    elif '720p' in link:
                        qual='720p'
                    else:
                        qual='SD'

                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    count +=1
                    self.sources.append({'source': host,'quality': qual,'scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:
            pass

