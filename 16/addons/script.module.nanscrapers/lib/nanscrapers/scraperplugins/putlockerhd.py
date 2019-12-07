import requests
import re
import urllib 
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class putlockerhd(Scraper):
    domains = ['putlockerhd.co']
    name = "PutlockerHD"
    sources = []
 
    def __init__(self):
        self.base_link = 'http://putlockerhd.co'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title).title()
            start_url = '%s/watch?v=%s_%s' %(self.base_link,search_id.replace(' ','_'),year)
            #print 'putloc '+start_url
            headers = {'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content
            varid = re.compile('var frame_url = "(.+?)"',re.DOTALL).findall(html)[0].replace('/embed/','/streamdrive/info/')
            res_chk = re.compile('class="title"><h1>(.+?)</h1>',re.DOTALL).findall(html)[0]
            varid = 'http:'+varid
            holder = requests.get(varid,headers=headers,timeout=5).content
            #print holder
            links = re.compile('"src":"(.+?)"',re.DOTALL).findall(holder)
            count = 0
            for link in links:
                #print link
                link = link.replace('\\/redirect?url=','')
                link = urllib.unquote(link).decode('utf8')
                if '1080' in res_chk:
                    res= '1080p'
                elif '720' in res_chk:
                    res='720p'
                else:
                    res='DVD'
                count +=1    
                self.sources.append({'source': 'Googlelink','quality': res,'scraper': self.name,'url':link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)    
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources