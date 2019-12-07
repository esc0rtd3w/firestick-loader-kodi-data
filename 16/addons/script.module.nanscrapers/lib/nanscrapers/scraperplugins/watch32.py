import requests,re,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
                                           
class watch32(Scraper):
    domains = ['watch32hd.co']
    name = "Watch32hd"
    sources = []

    def __init__(self):
        self.base_link = 'https://watch32hd.co'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/watch?v=%s_%s' %(self.base_link,search_id.replace(' ','_'),year)
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            varid = re.compile('var frame_url = "(.+?)"',re.DOTALL).findall(html)[0].replace('/embed/','/streamdrive/info/')
            res_chk = re.compile('class="title"><h1>(.+?)</h1>',re.DOTALL).findall(html)[0]
            varid = 'http:'+varid
            holder = requests.get(varid,headers=headers,timeout=5).content
            links = re.compile('"src":"(.+?)"',re.DOTALL).findall(holder)
            count = 0
            for link in links:
                movie_link = link.replace('\\','')
                if '1080' in res_chk:
                    res= '1080p'
                elif '720' in res_chk:
                    res='720p'
                else:
                    res='DVD'
                count +=1    
                self.sources.append({'source': 'Googlelink','quality': res,'scraper': self.name,'url': movie_link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)   
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

