import requests
import re,xbmcaddon,time 
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log            
from nanscrapers.modules import cfscrape     

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
                                           
class joymovies(Scraper):
    domains = ['oceanofmovies.bz']
    name = "OceanofMovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://oceanofmovies.de'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time() 
                      

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s+%s' %(self.base_link,search_id.replace(' ','+'),year)
            #print 'STARTURL:::::::::::::::: '+start_url
            headers={'User-Agent':User_Agent}
            html = self.scraper.get(start_url,headers=headers,timeout=5).content
            
            results = re.compile('class="entry-title".+?href="(.+?)" rel="bookmark">(.+?)</a>',re.DOTALL).findall(html)
            for item_url,name in results:
                if clean_title(title).lower() in clean_title(name).lower():
                    self.get_source(item_url,title,year)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources
            

    def get_source(self,item_url,title,year):
        try:
            #print '%s %s %s' %(item_url,title,year)
            headers={'User-Agent':User_Agent}
            html = self.scraper.get(item_url,headers=headers,timeout=5).content

            chkdetails = re.compile('File Detail</h2>.+?Movie Name :(.+?)<br.+?Movie Quality :(.+?)<br',re.DOTALL).findall(html)
            for name_check,quality in chkdetails:
                if '1080' in quality:
                    qual = '1080p'
                elif '720' in quality:
                    qual = '720p'
                else:
                    qual='SD'
                if year in name_check:
                    if clean_title(title).lower() == clean_title(name_check[:-4]).lower():
                        count = 0
                        headers = {'Origin':self.base_link, 'Referer':item_url,
                                   'X-Requested-With':'XMLHttpRequest', 'User_Agent':User_Agent}
                        try:
                            params = re.compile('<input name="FName" type="hidden" value="(.+?)" /><input name="FSize" type="hidden" value="(.+?)" /><input name="FSID" type="hidden" value="(.+?)"').findall(html)
                            for param1, param2,param3 in params:
                                request_url = self.base_link + '/thanks-for-downloading/'
                                form_data = {'FName':param1,'FSize':param2,'FSID':param3}
                                link = self.scraper.post(request_url, data=form_data, headers=headers).content
                                stream_url = re.compile('"refresh".+?url=(.+?)"',re.DOTALL).findall(link)[0]
                        except:
                            pass
                        stream_url = stream_url.replace('#038;','')
                        count +=1
                        self.sources.append({'source': 'DirectLink','quality': qual,'scraper': self.name,'url': stream_url,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                               
        except:
            pass