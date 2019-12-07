import requests,re,time,xbmcaddon
import resolveurl as urlresolver
from ..common import clean_title, clean_search,send_log,error_log
from ..scraper import Scraper
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class wmz(Scraper):
    domains = ['http://www.watchmovieszone.com']
    name = "WatchMoviesZone"
    sources = []

    def __init__(self):
        self.base_link = 'http://www.watchmovieszone.com'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/Movie/searchMovieName/?movie=%s' %(self.base_link,search_id)

            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content

            match = re.compile('"ID":"(.+?)","movieName":"(.+?)"',re.DOTALL).findall(html)
            for ID,item_name in match:
                if 'dubbed' not in item_name.lower(): 
                    if clean_title(title).lower() in clean_title(item_name).lower():
                        if year in item_name:
                            item_name = item_name.replace(' ','_')
                            url = '%s/Movie/Index/%s/%s' %(self.base_link,ID,item_name)
                            #print 'wmz Movie pass '+url
                            #print 'wmz ID ' +ID
                            self.get_source(url,ID)
            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_source(self,url,ID):
        try:
            # url not needed
            new_url = '%s/Movie/getmyLinks/?movID=%s' %(self.base_link,ID) 
            #print '###### '+new_url
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(new_url,headers=headers,timeout=5).content
            #print OPEN
            Regex = re.compile('"picLink":"(.+?)"',re.DOTALL).findall(OPEN)
            count = 0
            for link in Regex:
                #print link
                if 'streamango.com' in link:
                    try:
                        get_res=requests.get(link,timeout=5).content
                        qual = re.compile('{type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(get_res)[0]
                        if '1080' in qual:
                            rez='1080p'
                        elif '720' in qual:
                            rez = '720p'
                        else:rez= 'DVD'
                    except:rez='DVD'
                    count +=1
                    self.sources.append({'source': 'Streamango', 'quality': rez, 'scraper': self.name, 'url': link,'direct': False})            
                if 'openload' in link:
                    try:
                        chk = requests.get(link).content
                        rez = re.compile('"description" content="(.+?)"',re.DOTALL).findall(chk)[0]
                        if '1080' in rez:
                            res='1080p'
                        elif '720' in rez:
                            res='720p'
                        else:res='DVD' 
                    except: res = 'DVD'
                    count +=1
                    self.sources.append({'source': 'Openload', 'quality': res, 'scraper': self.name, 'url': link,'direct': False})              
                else:
                    if urlresolver.HostedMediaFile(link).valid_url():
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        count +=1
                        self.sources.append({'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                    
        except:
            pass
