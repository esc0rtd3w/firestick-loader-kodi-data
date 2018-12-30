import re,requests,xbmc,urllib,base64,xbmcaddon,time 
from ..scraper import Scraper
from ..common import clean_title,clean_search, filter_host, get_rd_domains,send_log,error_log  
from nanscrapers.modules import cfscrape 

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

class zoocinema(Scraper):
    domains = ['http://zoocine.net/']
    name = "ZooCinema"
    sources = []

    def __init__(self):
        self.base_link = 'http://zoocine.net/'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time() 
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            name = clean_search(title.lower())
            
            headers = {'User_Agent':User_Agent,'Referer':self.base_link}
            grab_token = self.scraper.get(self.base_link,headers=headers, timeout=3).content
            token = re.compile('name="tok" value="(.+?)"',re.DOTALL).findall(grab_token)[0]
            #print 'zooTOKEN '+token
            
            search = {'do':'search', 'subaction':'search','tok':token, 'story':name}
            link = self.scraper.post(self.base_link, data=search,headers=headers, timeout=3).content
            #print 'ZOOO post '+link
            links = link.split('-in">')[1:]
            
            for p in links:

                media_url = re.compile('href="(.+?)"').findall(p)[0]
                if self.base_link not in media_url:
                   media_url = self.base_link + media_url
                media_title = re.compile('title="(.+?)"').findall(p)[0]
                if name in clean_search(media_title).lower():
                    if year in media_title:
                        #print '###########zoo#####################'+str(media_url)
            
                        self.get_source(media_url)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            name = clean_search(title.lower())
            
            season_pull = '0%s' %season if len(season) <2 else season
            episode_pull = '0%s' %episode if len(episode) <2 else episode
            sep = 'S%sE%s' %(season_pull,episode_pull)

            headers = {'User_Agent':User_Agent,'Referer':self.base_link}
            grab_token = self.scraper.get(self.base_link,headers=headers, timeout=3).content
            token = re.compile('name="tok" value="(.+?)"',re.DOTALL).findall(grab_token)[0]
            #print 'zooTOKEN '+token
                       
            search = {'do':'search', 'subaction':'search','tok':token, 'story':'%s %s' %(name,sep)}            

            link = self.scraper.post(self.base_link, data=search,headers=headers, timeout=3).content
            
            links = link.split('-in">')[1:]
            
            for p in links:

                media_url = re.compile('href="(.+?)"').findall(p)[0]
                if self.base_link not in media_url:
                   media_url = self.base_link + media_url
                media_title = re.compile('title="(.+?)"').findall(p)[0]
               
                if name in clean_search(media_title).lower():
                    if sep.lower() in media_title.lower():
                        #print '###########zoo#####################'+str(media_url)
                        self.get_source(media_url)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def get_source(self,movie_url):
        try:
            #print ':::::::::::::::::::::::'+movie_url
            count = 0
            link = self.scraper.get(movie_url, timeout=3).content
            qual = link.split('>Source:<')[1:]
            for p in qual:
                res = re.findall(r'class="finfo-text">([^<]+)</div>', str(link), re.I|re.DOTALL)[0]
                if '1080' in res:
                    res='1080p'                   
                elif '720' in res:
                    res='720p'
                elif  '480' in res:
                    res='DVD'
                else:
                    res='SD'
                #print 'quality ######## = ' + res
            try:

                iframe = link.split('"video-responsive"')[1:]
                for p in iframe:

                    iframe_url = re.findall(r'iframe.*?src="([^"]+)"', p, re.I|re.DOTALL)[0]
                    if 'goo.gl' not in iframe_url:
                        if 'youtube' not in iframe_url:
                            #print 'BLOBK  '+iframe_url
                            host = iframe_url.split('//')[1].replace('www.','')
                            host = host.split('/')[0].lower()
                            if not filter_host(host):
                                continue
                            rd_domains = get_rd_domains()
                            if host in rd_domains:
                                count +=1
                                self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': iframe_url,'direct': False,'debridonly': True})
                            else:
                                count +=1
                                self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': iframe_url,'direct': False})
                if dev_log=='true':
                    end_time = time.time() - self.start_time
                    send_log(self.name,end_time,count) 
            except:pass

            try:
                    
                match2 = re.findall(r'<a href="([^"]+)"  .+?</a>', str(link), re.I|re.DOTALL)
                if not match2:
                    match2 = re.findall(r'target="_blank" href="(.+?)">Watch',str(link), re.I|re.DOTALL)
                for a in match2:
                    if '=' in a:
                        base64_url = a.split('=')[1]
                        base64_url = urllib.unquote(base64_url).decode('base64')
                        host = base64_url.split('//')[1].replace('www.','')
                        host = host.split('/')[0].lower()
                        if not filter_host(host):
                            continue
                        rd_domains = get_rd_domains()
                        
                        if host in rd_domains:
                            count +=1
                            self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': base64_url,'direct': False,'debridonly': True})
                        else:
                            count +=1
                            self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': base64_url,'direct': False})
                    else:
                        host = a.split('//')[1].replace('www.','')
                        host = host.split('/')[0].lower()
                        if not filter_host(host):
                            continue
                        rd_domains = get_rd_domains()
                        if host in rd_domains:
                            count +=1
                            self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': a,'direct': False, 'debridonly': True})
                        else:
                            count +=1
                            self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': a,'direct': False})
                if dev_log=='true':
                    end_time = time.time() - self.start_time
                    send_log(self.name,end_time,count) 
            except:pass
       
        except:
            pass
