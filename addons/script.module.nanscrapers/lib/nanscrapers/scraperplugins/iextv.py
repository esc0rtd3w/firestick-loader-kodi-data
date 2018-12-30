import re
import requests
import resolveurl as urlresolver
import xbmc,time
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent


User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'
#seach off

class iextv(Scraper):
    domains = ['http://iextv.com']
    name = "iExTV"
    sources = []

    def __init__(self):
        self.base_link = 'http://iextv.com'
        self.goog = 'https://www.google.co.uk'
        self.sources = []
        self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            scrape = clean_search(title.lower()).replace(' ','-').replace(',','')

            start_url = '%s/search?as_q=&as_epq=-%s&as_sitesearch=%s' %(self.goog,scrape,self.base_link)
            #print 'Google search URL> '+start_url
            
            headers = {'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers).content
            #print html
            results = re.compile('href="(.+?)"',re.DOTALL).findall(html)
            uniques =[]
            for item_url in results:
                #print 'grab '+ item_url
                item_url=item_url.replace('https','http')
                if not self.base_link in item_url:
                    continue
                if '/movies/' in item_url:
                    check_mov = item_url.split('/movies/')[1].lstrip('0123456789')
                    #print 'cmgw '+check_mov
                    if not clean_title(check_mov).lower() == clean_title(title).lower(): 
                        continue
                    item_url = item_url.replace('/index.php','')
                    movie_link = item_url
                    if movie_link not in uniques:
                        uniques.append(movie_link)
                        #print 'Final_Pass this ' + movie_link
                        self.mov_source(movie_link,year)
                
            return self.sources
        except Exception, argument:
            return self.sources

    # def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        # try:
            # search_id = clean_search(title.lower())
            # start_url = '%s/search?q=%s+%s' %(self.base_link,search_id.replace(' ','+'),year)
            # #print 'SEARCH > '+start_url
            # html = requests.get(start_url, timeout=3).content
            # Regex = re.compile('<a href="([^"]*)">([^<>]*)</a>').findall(html)
            # uniques = []
            # for item_url,item_name in Regex:
                # if clean_title(title).lower() in clean_title(item_name).lower():
                    # TV_link = item_url
                    # self.TV_source(TV_link,year,season,episode)
                
            # return self.sources
        # except Exception, argument:
            # return self.sources
            
            
    def mov_source(self,movie_link,year):
        try:
            link = requests.get(movie_link, timeout=3).content
            #print link
            links = re.compile('"url":"(.+?)".+?"quality":"(.+?)"',re.DOTALL).findall(link)
            item_year = re.compile('Release Date : </strong><span>(.+?)</span>',re.DOTALL).findall(link)[0]
            if not str(year) in str(item_year):
                return false
            uniques = []
            for final_url,res in links:
                #print '%s %s' %(final_url,res)
                if '.rar' not in final_url:
                    final_url = final_url.replace('\\', '')
                    if '4K' not in res:
                        if '3D' not in res:
                            if '1080' in res:
                                res='1080p'                   
                            elif '720' in res:
                                res='720p'
                            elif 'HD' in res:
                                res='HD'
                            else:
                                res='SD'
                            
                            if not urlresolver.HostedMediaFile(final_url):
                                continue
                            if final_url not in uniques:
                                uniques.append(final_url)
                                    
                                host = final_url.split('//')[1].replace('www.','')
                                host = host.split('/')[0].split('.')[0].title()

                                self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': final_url,'direct': False})

        except:
            pass

    # def TV_source(self,TV_link,year,season,episode):
        # try:
            # link = requests.get(TV_link, timeout=3).content
            # links = re.compile('"url":"([^"]+)",.*?"season":(.*?),"episode":(.*?),.*?"quality":"([^"]+)"',re.DOTALL).findall(link)
            # item_year = re.compile('Release Date : </strong><span>([^<>]*)</span>',re.DOTALL).findall(link)[0]
            # uniques = []

            # for final_url, sea, epi, res in links:
                # final_url = final_url.replace('\\', '')
                # if '4K' not in res:
                    # if '3D' not in res:
                        # if '1080' in res:
                            # res='1080p'                   
                        # elif '720' in res:
                            # res='720p'
                        # elif 'HD' in res:
                            # res='HD'
                        # else:
                            # res='SD'

                        # if str(year) in str(item_year):
                            # if int(season) == int(sea):
                                # if int(episode) == int(epi):
                                    # if final_url not in uniques:
                                        # uniques.append(final_url)
                                        # if urlresolver.HostedMediaFile(final_url).valid_url():
                                            # if not '.rar' in final_url:
                                                # host = final_url.split('//')[1].replace('www.','')
                                                # host = host.split('/')[0].split('.')[0].title()

                                                # self.sources.append({'source': host,'quality': res,'scraper': self.name,'url': final_url,'direct': False})
                                                # end_time = time.time()
                                                # total_time = end_time - self.start_time
                                                # print (repr(total_time))+"<<<<<<<<<<<<<<<<<<<<<<<<<"+self.name+">>>>>>>>>>>>>>>>>>>>>>>>>total_time"
        # except:
            # pass