import requests,re,xbmcaddon,time 
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log         
requests.packages.urllib3.disable_warnings()
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
                                           
class Movie321(Scraper):
    domains = ['321movies.cc']
    name = "Movie321cc"
    sources = []

    def __init__(self):
        self.base_link = 'https://321movies.cc'
        if dev_log=='true':
            self.start_time = time.time() 

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            movie_id= clean_search(title.lower().replace(' ','-'))
            show_url = '%s/episodes/%s-%sx%s' %(self.base_link,movie_id,season,episode)
            
            #print '321tv url> '+show_url
            
            headers={'User-Agent':User_Agent}
            html = requests.get(show_url,headers=headers,timeout=5).content

            match = re.compile('class="metaframe rptss" src="(.+?)"').findall(html)
            count = 0
            for link in match: 
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                if 'streamango.com' in link:
                    holder = requests.get(link).content
                    qual = re.compile('type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(holder)[0]
                    count +=1
                    self.sources.append({'source': host, 'quality': qual+'p', 'scraper': self.name, 'url': link,'direct': False})
                elif 'goo.gl' in link:
                    headers = {'User-Agent': User_Agent}
                    r = requests.get(link,headers=headers,allow_redirects=False)
                    link = r.headers['location'] 
                    count +=1
                    self.sources.append({'source': 'Waaw', 'quality': '720p', 'scraper': self.name, 'url': link,'direct': False})
                
                else:
                    count +=1
                    self.sources.append({'source': host, 'quality': '720p', 'scraper': self.name, 'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                       
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources                          

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            mock_ID = clean_search(title.lower())
            #print mock_ID
            loop_url = ['online-free','for-free','free','']
            for attempt in loop_url:
                movie_url = '%s/film/watch-%s-%s' %(self.base_link,mock_ID.replace(' ','-'),attempt)
                if movie_url.endswith('-'):
                    movie_url=movie_url.replace('watch-','')[:-1]
                #print 'allurls '+movie_url
                headers={'User-Agent':User_Agent}
                html = requests.get(movie_url,headers=headers,timeout=5).content
                #print 'PAGE > '+html
                match = re.compile('name="title" value="(.+?)"',re.DOTALL).findall(html)
                for item_title in match:
                    if not clean_title(title.lower()) == clean_title(item_title.lower()):
                        continue
                    #print 'clean321movie pass '+ movie_url
                    Regex = re.compile('</iframe>.+?class="metaframe rptss" src="(.+?)"',re.DOTALL).findall(html)
                    count = 0
                    for link in Regex: 
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        if 'streamango.com' in link:
                            holder = requests.get(link).content
                            qual = re.compile('type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(holder)[0]
                            count +=1
                            self.sources.append({'source': host, 'quality': qual + 'p', 'scraper': self.name, 'url': link,'direct': False})
                        elif 'goo.gl' in link:
                            headers = {'User-Agent': User_Agent}
                            r = requests.get(link,headers=headers,allow_redirects=False)
                            link = r.headers['location']
                            count +=1                            
                            self.sources.append({'source': 'Waaw', 'quality': '720p', 'scraper': self.name, 'url': link,'direct': False})
                        else:
                            count +=1
                            self.sources.append({'source': host, 'quality': '720p', 'scraper': self.name, 'url': link,'direct': False})
                    if dev_log=='true':
                        end_time = time.time() - self.start_time
                        send_log(self.name,end_time,count)  
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources


