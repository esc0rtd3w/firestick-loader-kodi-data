import re,time
import requests,xbmcaddon
from ..scraper import Scraper

from ..common import clean_title,clean_search,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

requests.packages.urllib3.disable_warnings()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

class Watchcartoons(Scraper):
    name = "Watchcartoon"
    domains = ['watchcartoononline.io']
    sources = []

    def __init__(self):
        self.start_time = time.time() 
        self.base_link_cartoons = 'http://www.watchcartoononline.io/cartoon-list'
        self.dubbed_link_cartoons = 'https://www.watchcartoononline.io/dubbed-anime-list'
        self.base_link_movies = 'https://www.watchcartoononline.io/movie-list'
        if dev_log=='true':
            self.start_time = time.time()
        
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            uniques = []
            for link in [self.base_link_cartoons,self.dubbed_link_cartoons]:
                html = requests.get(link,timeout=5).content
                match = re.compile('<a href="(.+?)" title=".+?">(.+?)</a>',re.DOTALL).findall(html)
                
                bollox = '%s season %s' %(title,season)
                #print 'if season in title > ' + bollox
                
                for url, name in match:
                    if clean_title(title).lower() == clean_title(name).lower():
                        #print 'title 1> ' + url
                        headers = {'User-Agent':User_Agent}
                        show_page = requests.get(url,headers=headers,allow_redirects=False).content

                        Regex = re.compile('class="cat-listview cat-listbsize">(.+?)</ul>',re.DOTALL).findall(show_page)
                        get_episodes = re.compile('<li><a href="(.+?)"',re.DOTALL).findall(str(Regex))
                        for link in get_episodes:
                            #print link
                            if not '-season-' in link:
                                episode_format = '-episode-%s-' %(episode)
                            else:
                                episode_format = 'season-%s-episode-%s-' %(season, episode)
                            if episode_format in link:
                                if link not in uniques:
                                    uniques.append(link)
                                    #print 'Pass this episode_url watchcartoon>> ' + link
                                    self.check_for_play(link)
                    else:
                        
                        if clean_title(bollox).lower() == clean_title(name).lower():
                            #print 'title 2> ' + url
                            headers = {'User-Agent':User_Agent}
                            show_page = requests.get(url,headers=headers,allow_redirects=False).content

                            Regex = re.compile('class="cat-listview cat-listbsize">(.+?)</ul>',re.DOTALL).findall(show_page)
                            get_episodes = re.compile('<li><a href="(.+?)"',re.DOTALL).findall(str(Regex))
                            for link in get_episodes:
                                #print link
                                if not '-season-' in link:
                                    episode_format = '-episode-%s-' %(episode)
                                else:
                                    episode_format = 'season-%s-episode-%s-' %(season, episode)
                                if episode_format in link:
                                    if link not in uniques:
                                        uniques.append(link)
                                        #print 'Pass this episode_url watchcartoon>> ' + link
                                        self.check_for_play(link)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            uniques = []
            html = requests.get(self.base_link_movies,timeout=5).content
            match = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(html)
            for link, name in match:
                name = name.replace('English Subbed','').replace('English Dubbed','')
                name = name.rstrip(' Movie')
                name = name.rstrip('1234567890')

                if clean_title(title).lower() == clean_title(name).lower():
                    if link not in uniques:
                        uniques.append(link)
                        #print 'Pass this episode_url watchcartoon>> ' + link
                        self.check_for_play(link)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources


    def check_for_play(self, link):
        try:
            #print 'Pass url '+ link
            episodeREQ = link.replace('https://www.watchcartoononline.io/','')[:-4]
            #print 'episode REQ ' + episodeREQ
            OPEN = requests.get(link).content   
            getplaylist = re.compile('class="wcobtn".+?href="(.+?)"',re.DOTALL).findall(OPEN)[0]
            #print 'getplay '+ getplaylist
            listpage = requests.get(getplaylist).content
            list = re.compile('playlist: "(.+?)"',re.DOTALL).findall(listpage)[0]
            list = 'https://www.watchcartoononline.io' + list
            #print 'List url xml ' + list
            headers = {'User_Agent':User_Agent}
            xml_list = requests.get(list,headers=headers,timeout=5).content
            #print 'xml list' +xml_list
            REGEX = re.compile('<jwplayer:image>(.+?)</jwplayer:image>.+?source file="(.+?)"',re.DOTALL).findall(xml_list)
            count = 0
            for play_episode,final_url in REGEX:
                
                if clean_title(episodeREQ).lower() in clean_title(play_episode).lower():
                    final_url = final_url.replace('amp;','')
                    #print 'got Ep '+ play_episode
                    #print 'send url '+ final_url
                    count +=1
                    self.sources.append({'source': 'watchcartoons', 'quality': 'SD', 'scraper': self.name, 'url': final_url, 'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:
            pass

