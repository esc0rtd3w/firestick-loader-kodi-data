import requests
import re
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class hdpopcorn(Scraper):
    domains = ['hdpopcorns.com']
    name = "HD Popcorns"
    sources = []

    def __init__(self):
        self.base_link = 'http://hdpopcorns.com'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url ='%s/search/%s' %(self.base_link,search_id.replace(' ','+'))
            #print 'starturl > '+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
           
            links = re.compile('<header>.+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(html)
            for m_url,m_title in links:
                if clean_title(title).lower() in clean_title(m_title).lower():
                    if year in m_title:
                        url = m_url
                        self.get_source(url)
            return self.sources
        except:
            pass
            return[]

    def get_source(self,url):
        try:
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(url,headers=headers,timeout=5).content
            headers = {'Origin':'http://hdpopcorns.com', 'Referer':url,
                       'X-Requested-With':'XMLHttpRequest', 'User-Agent':User_Agent}
        
            try:
                params = re.compile('FileName1080p.+?value="(.+?)".+?FileSize1080p.+?value="(.+?)".+?value="(.+?)"',re.DOTALL).findall(OPEN)
                for param1, param2,param3 in params:
                    request_url = '%s/select-movie-quality.php' %(self.base_link)
                    form_data = {'FileName1080p':param1,'FileSize1080p':param2,'FSID1080p':param3}
                link = requests.post(request_url, data=form_data, headers=headers,timeout=3).content
                final_url = re.compile('<strong>1080p</strong>.+?href="(.+?)"',re.DOTALL).findall(link)[0]
                res = '1080p'
                self.sources.append({'source': 'DirectLink', 'quality': res, 'scraper': self.name, 'url': final_url,'direct': True})
            except:pass
            try:
                params = re.compile('FileName720p.+?value="(.+?)".+?FileSize720p".+?value="(.+?)".+?value="(.+?)"',re.DOTALL).findall(OPEN)
                for param1, param2,param3 in params:
                    request_url = '%s/select-movie-quality.php' %(self.base_link)
                    form_data = {'FileName720p':param1,'FileSize720p':param2,'FSID720p':param3}
                link = requests.post(request_url, data=form_data, headers=headers,timeout=3).content
                final_url = re.compile('<strong>720p</strong>.+?href="(.+?)"',re.DOTALL).findall(link)[0]
                res = '720p'
                self.sources.append({'source': 'DirectLink', 'quality': res, 'scraper': self.name, 'url': final_url,'direct': True})
            except:pass                
        except:
            pass

