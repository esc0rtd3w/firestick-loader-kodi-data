import re
import requests
import threading
from ..common import clean_title,clean_search,send_log,error_log 
import xbmc,xbmcaddon,time 
from ..scraper import Scraper
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")
sources = []

class scrape_thread(threading.Thread):
    def __init__(self,m,match,qual):
        self.m = m
        self.match = match
        self.qual = qual
        threading.Thread.__init__(self)
        if dev_log=='true':
            self.start_time = time.time() 
		
    def run(self):
        try:
            qual = self.qual
            url = 'https://yesmovies.to/ajax/movie_token?eid='+self.m+'&mid='+self.match
            html3 = requests.get(url).content
            x,y = re.findall("_x='(.+?)', _y='(.+?)'",html3)[0]
            fin_url = 'https://yesmovies.to/ajax/movie_sources/'+self.m+'?x='+x+'&y='+y
            h = requests.get(fin_url).content
            playlink = re.findall('"file":"(.+?)"(.+?)}',h)
            count = 0
            for p,rest in playlink:
                try:
                    qual = re.findall('"label":"(.+?)"',str(rest))[0]
                except:
                    qual = self.qual
                p = p.replace('\\','')
                if 'srt' in p:
                    pass
                elif 'spanish' in qual:
                    pass
                elif 'googleapis' in p:
                    pass
                else:
                    if 'english' in qual:
                        qual = '720p'
                    if 'lemon' in p:
                        p = p+'|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0&Host=streaming.lemonstream.me:1443&Referer=https://yesmovies.to'
                    if 'http' in p:
                        count +=1
                        sources.append({'source': 'Gvideo', 'quality': qual, 'scraper': 'yesmovies', 'url': p,'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except Exception as e:
            xbmc.log('get sources: '+str(e),xbmc.LOGNOTICE)


class Yesmovies(Scraper):
    domains = ['yesmovies.to']
    name = "yesmovies"

    def __init__(self):
        self.base_link = 'https://yesmovies.to'
        self.search_link = '/search/'

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link+self.search_link+title.replace(' ','+')+'.html'
            html = requests.get(start_url).content
            match = re.compile('<div class="ml-item">.+?<a href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                if clean_title(title)+'season'+season == clean_title(name):
                    html2 = requests.get(url).content
                    match2 = re.findall('favorite\((.+?),',html2)[0]
                    get_ep = requests.get('https://yesmovies.to/ajax/v4_movie_episodes/'+match2).content
                    block = re.compile('data-id="(.+?)".+?title="(.+?)">').findall(get_ep.replace('\\',''))
                    for ID,name in block:
                        if 'Episode' in name:
                            ep = re.findall('Episode (.+?):',str(name))[0]
                            if len(episode) == 1:
                                episode = '0'+episode
                            if episode == ep:
                                thread = scrape_thread(ID,match2,'SD')
                                thread.start()
            try:
                thread.join()
            except:
                pass                   
            return sources
                                        
        except Exception as e:
            xbmc.log(str(e),xbmc.LOGNOTICE)
            return []                           

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            try:
                start_url = self.base_link+self.search_link+title.replace(' ','+')+'.html'
                title = title
                m_list = self.check_for_movie(title,start_url)
            except:
                start_url2 = self.base_link+self.search_link+title.replace(' ','+')+'+'+year+'.html'
                title = title+year
                m_list = self.check_for_movie(title,start_url2)
            for item in m_list:
                m = item[0];match=item[1];qual=item[2]
                thread = scrape_thread(m,match,qual)
                thread.start()
            try:
                thread.join()
            except:
                pass                   
            return sources
        except Exception as e:
            xbmc.log('scrape movie: '+str(e),xbmc.LOGNOTICE)
            return[]



    def check_for_movie(self,title,start_url):
        try:
            m_list = []
            html = requests.get(start_url).content
            match = re.compile('<div class="ml-item">.+?<a href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                if clean_search(title.replace(' ','')) == clean_search(name).replace(' ',''):
                    html = requests.get(url).content
                    match = re.findall('favorite\((.+?),',html)[0]
                    second_url = 'https://yesmovies.to/ajax/v4_movie_episodes/'+match
                    html2 = requests.get(second_url).content
                    match2 = re.compile('<li class=.+?data-id=.+?"(.+?)".+?title=.+?"(.+?)"').findall(html2)
                    for m,qual in match2:
                        m = m.replace('\\','')
                        qual = qual.replace('\\','').replace('HD-','')
                        if len(m)==6 or len(m)==7:
                            m_list.append((m,match,qual))
                    return m_list
        except Exception as e:
            xbmc.log('check for movie '+str(e),xbmc.LOGNOTICE)

#Yesmovies().scrape_movie('baywatch','2017','')
#Yesmovies().scrape_episode('game of thrones', '', '', '7', '7', '', '')
