import requests
import re
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search            


s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class ten80p(Scraper):
    domains = ['1080pMovies.com']
    name = "1080pMovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://1080pmovie.com'
                      

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = self.base_link + '/wp-json/wp/v2/posts?search=%s' %search_id.replace(' ','%20')
            #print 'STARTURL:::::::::::::::: '+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            Links = re.compile('"post","link":"(.+?)","title".+?"rendered":"(.+?)"',re.DOTALL).findall(html)
            for link,name in Links:
                link = link.replace('\\','')
                if clean_title(title).lower() in clean_title(name).lower(): 
                    if year in name:
                        #print 'pass link> ' + link
                        holder = requests.get(link,headers=headers,timeout=5).content
                        new = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(holder)[0]
                        end = requests.get(new,headers=headers,timeout=5).content
                        final_url = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(end)[0]
                        self.sources.append({'source': 'openload','quality': '1080p','scraper': self.name,'url': final_url,'direct': False})
            return self.sources
        except Exception, argument:
            return self.sources

