import requests
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")           
requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class filmapik(Scraper):
    domains = ['https://www.filmapik.tv']
    name = "Filmapik"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.filmapik.co'
        if dev_log=='true':
            self.start_time = time.time() 

                        

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print 'start>>>>  '+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content

            match = re.compile('data-movie-id=.+?href="(.+?)".+?<h2>(.+?)</h2>',re.DOTALL).findall(html)
            for item_url, name in match:
                #print 'clean name >  '+clean_title(name).lower()
                if not clean_title(search_id).lower() == clean_title(name).lower():
                    continue
                if not year in name:
                    continue
                item_url = item_url + '/play'
                self.get_source(item_url)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))

            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content

            match = re.compile('data-movie-id=.+?href="(.+?)".+?<h2>(.+?)</h2>',re.DOTALL).findall(html)
            for item_url, name in match:
                if not clean_title(search_id).lower() == clean_title(name).lower():
                    continue
                item_url = item_url.replace('/tvshows/','/episodes/') + '-%sx%s' %(season,episode)
                self.get_source(item_url)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources
            
    def get_source(self,item_url):
        try:
            #print 'cfwd > '+item_url
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content
            sources = re.compile("Onclick=\"loadPage.+?'(.+?)'",re.DOTALL).findall(OPEN)
            count = 0
            for embFile in sources:
                    #print embFile
                    if 'streamango' in embFile:
                        holder = requests.get(embFile).content
                        qual = re.compile('type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(holder)[0]
                        count +=1
                        self.sources.append({'source': 'Streamango', 'quality': qual, 'scraper': self.name, 'url': embFile,'direct': False})
                    elif 'drive.google' in embFile:
                        embFile=embFile.replace('/preview','/edit')
                        count +=1
                        self.sources.append({'source': 'GoogleLink', 'quality': '720p', 'scraper': self.name, 'url': embFile,'direct': False}) 
                    elif 'oload' in embFile or 'openload' in embfile:
                        get_res=requests.get(embFile,timeout=5).content
                        rez = re.compile('description" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                        if '1080p' in rez:
                            qual = '1080p'
                        elif '720p' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                        count +=1
                        self.sources.append({'source': 'Openload', 'quality': qual, 'scraper': self.name, 'url': embFile,'direct': False})
                    else:
                        if not urlresolver.HostedMediaFile(embFile).valid_url():
                            continue
                        host = embFile.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        count +=1
                        self.sources.append({'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': embFile,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                      
        except:
            pass

