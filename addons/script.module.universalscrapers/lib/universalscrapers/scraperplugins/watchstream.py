import re,xbmcaddon,time,requests
from universalscrapers.scraper import Scraper
from universalscrapers.common import random_agent,send_log,error_log
requests.packages.urllib3.disable_warnings()
s = requests.session()
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class watchstream(Scraper):
    domains = ['https://putlockers.movie']
    name = "Watchstream"
    sources = []

    def __init__(self):
        self.base_link = 'https://putlockers.movie/embed/'
        #self.scraper = cfscrape.create_scraper()
                      
    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            get_link = self.base_link + '%s/' %(imdb)
            headers={'User-Agent':random_agent(),'referrer':get_link}
            data = {'tmp_chk':'1'}
            html = requests.post(get_link,headers=headers,data=data,verify=False,timeout=5).content
            #print html
            try:
                link = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(html)[0]
            except:
                link = ''
            #print link
            count = 0
            if link != '':
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
                    end_time = time.time() - start_time
                    send_log(self.name,end_time,count,title,year)
                
                return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources
