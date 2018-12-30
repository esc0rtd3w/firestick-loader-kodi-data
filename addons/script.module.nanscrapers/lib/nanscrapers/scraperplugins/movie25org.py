import re,time
import requests
import resolveurl as urlresolver
import xbmc,xbmcaddon
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log


dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'


class movie25org(Scraper):
    domains = ['movie25.org']
    name = "Movie25"
    sources = []

    def __init__(self):
        self.base_link = 'http://www.movies25.org'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print 'search>>>'+start_url
            headers = {'User_Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            
            Regex = re.compile('id="mt-.+?href="(.+?)".+?class="tt">(.+?)</span>',re.DOTALL).findall(html)
            for item_url,item_name in Regex:

                if not clean_title(title).lower() == clean_title(item_name).lower():
                    continue
                if not year in item_name:
                    continue
                #print item_url
                self.get_source(item_url)
            
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources
            
    def get_source(self,item_url):
        try:
            html = requests.get(item_url).content
            frame_holder = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(html)[0]
            #print 'somovie link ' +frame_holder
            links_page = requests.get(frame_holder).content
            grab = re.compile('data-src="(.+?)"',re.DOTALL).findall(links_page)
            count = 0
            for link in grab:

                if urlresolver.HostedMediaFile(link).valid_url():
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    if '1080' in link:
                        res='1080p'
                    elif '720' in link:
                        res = '720p'
                    else:res='DVD'
                    count +=1
                    self.sources.append({'source': host,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
                else:
                    link = 'http:' + link
                    get_end_link = requests.get(link).content

                    try:
                        final_url = re.compile("src='(.+?)'",re.DOTALL).findall(get_end_link)[0]
                
                        if urlresolver.HostedMediaFile(final_url).valid_url():
                            host = final_url.split('//')[1].replace('www.','')
                            host = host.split('/')[0].split('.')[0].title()
                            if '1080' in link:
                                res='1080p'
                            elif '720' in link:
                                res = '720p'
                            else:res='DVD'
                            count +=1
                            self.sources.append({'source': host,'quality': 'DVD','scraper': self.name,'url': final_url,'direct': False})
                        
                    except:
                        final_url = re.compile('"file": "(.+?)"',re.DOTALL).findall(get_end_link)[0]
                        count +=1
                        self.sources.append({'source': 'GoogleLink','quality': 'HD','scraper': self.name,'url': final_url,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:
            pass
