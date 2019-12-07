import requests,re,time,xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
  
class MovieTV(Scraper):
    domains = ['http://movietv.ws/']
    name = "MovieTV"
    sources = []

    def __init__(self):
        self.base_link = 'https://movietv.ws/'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s?s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print start_url
            html = requests.get(start_url,timeout=10).content
            #print html
            block = re.compile('class="page-category">(.+?)alert-bottom-content"><p',re.DOTALL).findall(html)
            match = re.compile('class="mli-quality">(.+?)</span>.+?<h2>(.+?)</h2>.+?rel="tag">(.+?)</a>.+?class="jtip-bottom">.+?href="(.+?)".+?class="btn\s*btn-block').findall(str(block))
            for qaul,name,yrs,item_url in match:
                #item_url = 'http:%s' % (item_url)
                if not year in yrs:
                    continue
                if not clean_title(search_id).lower() == clean_title(name).lower():
                    continue
                self.get_source(item_url,qaul)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

            
    def get_source(self,item_url,qaul):
        print item_url
        try:
            OPEN = requests.get(item_url,timeout=10).content
            block1 = re.compile('id="content-embed"(.+?)id="button-favorite">',re.DOTALL).findall(OPEN)
            Endlinks = re.compile('src="(.+?)"\s*scrolling',re.DOTALL).findall(str(block1))
            count = 0
            for link in Endlinks:
                #link = 'http:%s' % (link)
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                host = host.split('.')[0]
                count +=1
                #print link
                self.sources.append({'source': host, 'quality': qaul, 'scraper': self.name, 'url': link,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:
            pass