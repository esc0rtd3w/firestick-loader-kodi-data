import requests
import re
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,filter_host,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
from nanscrapers.modules import cfscrape           
requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
                                           
class hollymoviehd(Scraper):
    domains = ['https://www.hollymoviehd.com']
    name = "HollyMovieHD"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.hollymoviehd.com'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time()

                        

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?rs=search&s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print ':::::::::::::######################## '+start_url
            headers={'User-Agent':User_Agent,'referer':self.base_link}
            html = self.scraper.get(start_url,headers=headers,timeout=5).content
            #print ':::::::::::::######################## '+html
            match = re.compile('data-movie-id=.+?href="(.+?)".+?class="mli-info"><h2>(.+?)</h2>',re.DOTALL).findall(html)
            for item_url, name in match:
                if not year in name:
                    continue
                name=name.split('(')[0]
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                        
                self.get_source(item_url)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    # def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        # try:
            # search_id = clean_search(title.lower())
            # start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))

            # headers={'User-Agent':User_Agent}
            # html = requests.get(start_url,headers=headers,timeout=5).content

            # match = re.compile("<a class='suf-mosaic-post-title' href='(.+?)'>(.+?)</a>",re.DOTALL).findall(html)
            # for item_url, name in match:
                # name = name.replace('Second','2').replace('Third','3').replace('Fourth','4').replace('Fifth','5').replace('Sixth','6').replace('Seventh','7').replace('Eighth','8')
                # if clean_title(search_id).lower() in clean_title(name).lower():
                    # if '-season' in item_url:
                        # if season in name:
                            # if episode == '1':
                                # item_url=item_url
                            # else:
                                # item_url = item_url + '/%s' %(episode)
                            # print '@@' +item_url
                            # self.get_source(item_url)
            # return self.sources
                
            # return self.sources
        # except Exception, argument:
            # return self.sources
            
    def get_source(self,item_url):
        try:
            #print 'MOVIE cfwd '+item_url
            headers={'User-Agent':User_Agent}
            OPEN = self.scraper.get(item_url,headers=headers,timeout=5).content
            #print OPEN
            holder = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(OPEN)
            count = 0
            for sources in holder:
                if sources.startswith('//'):
                    sources = 'https:' + sources
                #print 'embfile>> '+sources
            
                headers={'User-Agent':User_Agent,'referer':item_url}

                Page = self.scraper.get(sources,headers=headers,timeout=5).content
                #print 'page1234'+Page
                Endlinks = re.compile("<iframe src=['\"](.+?)['\"]",re.DOTALL).findall(Page)
                
                for link in Endlinks:
                    #print 'TRY ME > '+link
                    if 'openload' in link:
                        try:
                            headers = {'User_Agent':User_Agent}
                            get_res=requests.get(link,headers=headers,timeout=5).content
                            rez = re.compile('description" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                            if '1080p' in rez:
                                qual = '1080p'
                            elif '720p' in rez:
                                qual='720p'
                            else:
                                qual='DVD'
                        except: qual='DVD'
                        count +=1 
                        self.sources.append({'source': 'Openload','quality': qual,'scraper': self.name,'url': link,'direct': False})
                    elif 'streamango.com' in link:
                        get_res=requests.get(link,headers=headers,timeout=5).content
                        rez = re.compile('{type:"video/mp4".+?height:(.+?),',re.DOTALL).findall(get_res)[0]
                        if '1080' in rez:
                            qual = '1080p'
                        elif '720' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                        count +=1
                        self.sources.append({'source': 'Streamango', 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})
                    else:
                        #print 'OTHER '+link
                        try:
                            link = link.replace('/preview','/edit')
                            host = link.split('//')[1].replace('www.','')
                            host = host.split('/')[0].lower()
                            if not filter_host(host):
                                continue
                            host = host.split('.')[0].title()
                            count +=1
                            self.sources.append({'source': host, 'quality': 'DVD', 'scraper': self.name, 'url': link,'direct': False})
             
                        except:pass
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)                                  
        except:
            pass

