import re,xbmcaddon,time,requests
from ..scraper import Scraper
from ..common import random_agent,send_log,error_log
requests.packages.urllib3.disable_warnings()
s = requests.session()
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
from nanscrapers.modules import cfscrape 
class watchstream(Scraper):
    domains = ['https://putlockers.movie']
    name = "Watchstream"
    sources = []

    def __init__(self):
        self.base_link = 'https://putlockers.movie/embed/'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time() 
                      
    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            get_link = self.base_link + '%s/' %(imdb)
            headers={'User-Agent':random_agent(),'referrer':get_link}
            data = {'tmp_chk':'1'}
            html = self.scraper.post(get_link,headers=headers,data=data,verify=False,timeout=5).content
            #print html
            link = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(html)[0]
            #print link
            count = 0
            try:
                chk = requests.get(link).content
                rez = re.compile('"description" content="(.+?)"',re.DOTALL).findall(chk)[0]
                if '1080' in rez:
                    res='1080p'
                elif '720' in rez:
                    res='720p'
                else:
                    res ='DVD'
            except: res = 'DVD'
            count +=1
            self.sources.append({'source': 'Openload', 'quality': res, 'scraper': self.name, 'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources