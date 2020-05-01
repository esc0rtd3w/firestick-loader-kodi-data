import re
import requests
from ..scraper import Scraper
import xbmc,xbmcaddon,time
from ..common import clean_title,send_log,error_log
import urlparse

dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'


class Animetoon(Scraper):
    name = "Animetoon"
    domains = ['animetoon.org']
    sources = []

    def __init__(self):
        self.base_link_cartoons = 'http://www.animetoon.org/cartoon'
        self.dubbed_link_cartoons = 'http://www.animetoon.org/dubbed-anime'
        if dev_log=='true':
            self.start_time = time.time()

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        if season == "19":
            season = "1"
        try:
            uniques = []
            for base in [self.base_link_cartoons,self.dubbed_link_cartoons]:
                html = requests.get(base,timeout=5).content
                match = re.compile('<td><a href="(.+?)">(.+?)</a></td>',re.DOTALL).findall(html)
                
                bollox = '%s season %s' %(title,season)
                #print 'if season in title > ' + bollox
                
                for item_url, name in match:
                    #print 'grabbed %s %s '%(item_url, name)
                    if clean_title(title).lower() == clean_title(name).lower():
                        print 'title 1> ' + item_url
                        headers = {'User-Agent':User_Agent}
                        show_page = requests.get(item_url,headers=headers,allow_redirects=False).content
                        #print show_page
                        Regex = re.compile('<div id="videos">(.+?)</ul>',re.DOTALL).findall(show_page)
                        get_episodes = re.compile('<li>.+?href="(.+?)"',re.DOTALL).findall(str(Regex))
                        for link in get_episodes:
                            spoof = link + '#'
                            #print 'spoofed url '+spoof
                            if not '-season-' in link:
                                episode_format = '-episode-%s#' %(episode)
                            else:
                                episode_format = 'season-%s-episode-%s#' %(season, episode)
                            if episode_format in spoof:
                                if link not in uniques:
                                    uniques.append(link)
                                    #print 'title 1 routePass this episode_url aniema>> ' + link
                                    self.check_for_play(link)
                    else:
                        #print clean_title(bollox).lower()
                        #print clean_title(name).lower()
                        if clean_title(bollox).lower() == clean_title(name).lower():
                            #print 'title 2> ' + item_url
                            headers = {'User-Agent':User_Agent}
                            show_page = requests.get(item_url,headers=headers,allow_redirects=False).content

                            Regex = re.compile('<div id="videos">(.+?)</ul>',re.DOTALL).findall(show_page)
                            get_episodes = re.compile('<li>.+?href="(.+?)"',re.DOTALL).findall(str(Regex))
                            for link in get_episodes:
                                spoof = link + '#'
                                if not '-season-' in link:
                                    episode_format = '-episode-%s#' %(episode)
                                else:
                                    episode_format = 'season-%s-episode-%s#' %(season, episode)
                                if episode_format in spoof:
                                    if link not in uniques:
                                        uniques.append(link)
                                        #print 'tit2 Pass this episode_url watchcartoon>> ' + link
                                        self.check_for_play(link)

            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources


    def check_for_play(self, link):
        try:
            #print 'Pass url '+ link   
            frame_page = requests.get(link).content
            links = re.compile('class="playlist".+?src="(.+?)"',re.DOTALL).findall(frame_page)
            count = 0
            for url in links:
                url = url.replace('videozoo.me/embed.php','videozoo.me/videojs/').replace('playbb.me/embed.php','playbb.me/new/').replace('easyvideo.me/gogo/','easyvideo.me/gogo/new/').replace('play44.net/embed.php','play44.net/new/').replace('&file=','&vid=')
                host = url.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                
                url = self.resolve(url)
                count +=1
                self.sources.append({'source': host, 'quality': 'SD', 'scraper': self.name, 'url': url, 'direct': True})
                #print 'PASSED for PLAY '+url
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)

        except:
            pass
            
            
    def resolve(self, url):
        print 'resolveME url '+ url
        try:        
            open = requests.get(url,timeout=3).content

            if 'playpanda' in url:
                url = re.compile("url: '(.+?)'",re.DOTALL).findall(open)[0]

            else:
                url = re.compile('"link":"(.+?)"',re.DOTALL).findall(open)[0]
            url = url.replace('\\','')
        except:pass
        return url
        
            # if 'videozoo'in url:
                # url = re.compile('"link":"(.+?)"',re.DOTALL).findall(open)[0]
            # elif 'play44'in url:
                # url = re.compile('"link":"(.+?)"',re.DOTALL).findall(open)[0]
            # elif 'playpanda' in url:
                # url = re.compile("url: '(.+?)'",re.DOTALL).findall(open)[0]
            # elif 'playbb'in url:
                # url = re.compile('"link":"(.+?)"',re.DOTALL).findall(open)[0]
            # elif 'easyvideo'in url:
                # url = re.compile('"link":"(.+?)"',re.DOTALL).findall(open)[0]