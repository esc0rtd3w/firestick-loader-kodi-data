import re
import requests,time
import difflib
import xbmcaddon
from universalscrapers.scraper import Scraper
from universalscrapers.common import random_agent,send_log,error_log
from universalscrapers.modules import cfscrape

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
heads = {'User-Agent':random_agent}

class serieswatch(Scraper):
    domains = ['watch-series.co']
    name = "serieswatch"
    sources = []
    def __init__(self):
        self.base_link = 'https://ww1.watch-series.co'
        self.search_link = '/search.html?keyword='

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            start_url = self.base_link+self.search_link+title.replace(' ','%20')+'%20season%20'+season
            #print start_url
            scraper = cfscrape.create_scraper()
            html = scraper.get(start_url,timeout=10).content
            match = re.compile('<div class="video-thumbimg">.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                season_name_check = title.lower().replace(' ','')+'season'+season
                name_check = name.replace('-','').replace(' ','').lower()
                check = difflib.SequenceMatcher(a=season_name_check,b=name_check)
                d = check.ratio()*100
                if int(d)>80:
                    html2 = scraper.get(self.base_link+url+'/season',timeout=10).content
                    episodes = re.findall('<div class="video_container">.+?<a href="(.+?)" class="view_more"></a></div>.+?class="videoHname"><b>(.+?)</b></a></span>.+?<div class="video_date icon-calendar">.+?, (.+?)</div>',html2,re.DOTALL)
                    for url2,ep_no,aired_year in episodes:
                        url2 = self.base_link+url2
                        ep_no = ep_no.replace('Episode ','').replace(':','')
                        if ep_no == episode:
                            #print url2
                            self.get_sources(url2,title,year,season,episode,start_time)
            return self.sources
                                            
        except Exception as argument:
            if dev_log == 'true':
                error_log(self.name,argument)
            return []                           

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            start_url = self.base_link+self.search_link+title.replace(' ','%20')
            scraper = cfscrape.create_scraper()
            html = scraper.get(start_url,timeout=10).content
            match = re.compile('<div class="video-thumbimg">.+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for url,name in match:
                season_name_check = title.lower().replace(' ','')
                name_check = name.replace('-','').replace(' ','').lower()
                check = difflib.SequenceMatcher(a=season_name_check,b=name_check)
                d = check.ratio()*100
                if int(d)>80:
                    #print name
                    html2 = scraper.get(self.base_link+url,timeout=10).content
                    final_page_match = re.compile('<div class="vc_col-sm-8 wpb_column column_container">.+?Released:(.+?)<.+?/series/(.+?)"',re.DOTALL).findall(html2)
                    for release_year,fin_url in final_page_match:
                        release_year = release_year.replace(' ','')
                        fin_url = self.base_link+'/series/'+fin_url
                        if release_year == year:
                            self.get_sources(fin_url,title,year,'','',start_time)
            return self.sources
        except Exception as argument:
            if dev_log == 'true':
                error_log(self.name,argument)
            return[]

    def get_sources(self,url2,title,year,season,episode,start_time):
        try:
            #print url2
            quality = 'SD'
            html = requests.get(url2).content
            count = 0
            match = re.compile('href="#".+?data-video="(.+?)".+?class=".+?">(.+?)<',re.DOTALL).findall(html)
            for url,source_name in match:
                if 'm1' in source_name:
                    source_name = 'Gvideo'
                if 'vidnode' in url:
                    url = 'http:'+url
                    html2 = requests.get(url,timeout=3).content
                    single = re.findall("file: '(.+?)'.+?label: '(.+?)'",html2)
                    for playlink,quality in single:
                        
                        #print playlink
                        quality = quality.replace(' ','').lower()
                        if quality.lower() == 'auto' or quality.lower() == 'autop':
                            if 'm22' in quality:
                                quality = '720p'
                            elif 'm37' in quality:
                                quality = '1080p'
                            else:
                                quality = 'SD'
                        count +=1
                        self.sources.append({'source': source_name, 'quality': quality, 'scraper': self.name, 'url': playlink,'direct': True})
                elif 'ocloud' in url:
                    html2 = requests.get(url,timeout=3,headers=heads).content
                    base_url = re.findall('base href="(.+?)"',html2)[0]
                    try:
                        link,ID = re.findall("<div id=\"quality\">.+?href='(.+?)'.+?id=\"(.+?)\"",html2,re.DOTALL)[0]
                        if '720' in ID:
                            link = base_url+link[1:].replace('.','').replace('/embed','embed')
                            #print link
                            #print '##############'
                            html2 = requests.get(link,headers=heads,timeout=3).content
                            #print html2
                    except Exception as e:
                        print str(e)
                    try:
                        playlink,quality = re.findall("ifleID = '(.+?)'.+?quality = '(.+?)'",str(html2),re.DOTALL)[0]
                        #print playlink
                        count +=1
                        self.sources.append({'source': 'Ocloud', 'quality': quality, 'scraper': self.name, 'url': playlink,'direct': False})
                    except Exception as e:
                        print str(e)
                else:
                    count +=1
                    self.sources.append({'source': source_name, 'quality': quality, 'scraper': self.name, 'url': url,'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)
        except:
            pass
