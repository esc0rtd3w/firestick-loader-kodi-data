import requests,xbmcaddon,time,re
import resolveurl as urlresolver
from ..common import clean_title, clean_search,send_log,error_log
from ..scraper import Scraper
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")            

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
                                           
class moviewatcher(Scraper):
    domains = ['http://moviewatcher.is/']
    name = "moviewatcher"
    sources = []

    def __init__(self):
        self.base_link = 'http://moviewatcher.is'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/search?query=%s' %(self.base_link,search_id.replace(' ','+'))
            #print start_url
            headers={'User-Agent':User_Agent}
            r = requests.get(start_url,headers=headers,timeout=5).content
            #print r
            match = re.compile('<a class="movie-title" href="(.+?)">(.+?)</a>',re.DOTALL).findall(r)
            for url,name in match:
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                if not year in url:
                    continue
                url = self.base_link + url
                #print 'Pass '+url
                self.get_source(url)            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    # def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        # try:
        
            # season_pull = "0%s"%season if len(season)<2 else season
            # episode_pull = "0%s"%episode if len(episode)<2 else episode
            # sep = 's%se%s' %(season_pull,episode_pull)
        
            # search_id = clean_search(title.lower())
            # start_url = '%s/search?query=%s' %(self.base_link,search_id.replace(' ','+'))
            # headers={'User-Agent':User_Agent}
            # r = requests.get(start_url,headers=headers,timeout=5)
            # page = r.url
            # if 'search?query' in page:   #why this ?
                # match = re.compile('class="movie-title" href="(.+?)">(.+?)</a>',re.DOTALL).findall(r.content)
                # for url,name in match:
                    # if not clean_title(title).lower() == clean_title(name).lower():
                        # continue
                    # if '-tv-' in url:
                        # url = self.base_link + url +'/%s' %(sep)
                        # print 'pass_moviewatcherURL> '+url

                        # self.get_source(url)
            # else:
                # self.get_source(page,'unknown')
        # except Exception, argument:        
            # if dev_log == 'true':
                # error_log(self.name,'Check Search')
            # return self.sources
            
    def get_source(self,url):
        try:
            OPEN = requests.get(url).content
            Regex = re.compile(">Play:.+?window.open.+?'(/redirect/.+?)'",re.DOTALL).findall(OPEN)
            count = 0
            for link in Regex:
                #print link
                link = self.base_link + link
                headers={'User-Agent':User_Agent}
                r = requests.get(link,headers=headers,allow_redirects=False)
                stream_url = r.headers['location']
                if not urlresolver.HostedMediaFile(stream_url).valid_url():
                    continue
                host = stream_url.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                count +=1
                self.sources.append({'source': host, 'quality': 'SD', 'scraper': self.name, 'url': stream_url,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)               
        except:
            pass
