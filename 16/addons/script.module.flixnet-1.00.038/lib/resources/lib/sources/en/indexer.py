import re
import requests
import xbmc
from ..scraper import Scraper
from ..common import clean_title, random_agent, clean_search

class Indexer(Scraper):
    domains = ['https://www.google.com']
    name = "Indexer"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.google.com'

                          

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_term = clean_search(title.lower())
            #print 'GWGW'+search_term
            theyear='+'+year
            search = 'https://www.google.com/search?q=index+of+%s%s'  %(search_term.replace(' ','+'),theyear)
            #print 'SEARCH > '+search
            contents = requests.get(search,timeout=3).content
            match1=re.compile('<a href="\/url\?q=(.+?)&.+?">(.+?)</a>').findall(contents)
            for movie_url , NAME in match1:
                
                movie_url=movie_url.replace('%2520','%20')
                #print 'FILTER ME___ >'+movie_url
                if 'index of /' in NAME.replace('<b>','').replace('</b>','').lower(): 
                    try:                
                        content = requests.get(movie_url,timeout=3).content
                    except:pass 
                
                    match=re.compile('href="(.+?)"').findall(content)
                    for URL in match:
                        if not 'http' in URL:
                            MOVIE = movie_url + URL
                            if MOVIE[-4]=='.':
                                CLEANURL = URL.replace('%20','.').lower()
                                if search_term.replace(' ','.') in CLEANURL.replace(' ','.').lower():
                                    if year in MOVIE.lower():
                                        if '1080p' in MOVIE:                                          
                                            qual = '1080p'
                                        elif '720p' in MOVIE: 
                                            qual = '720p'
                                        elif '480p' in MOVIE:
                                            qual = '480p'
                                        else:
                                            qual = 'SD'
                                        if '.mkv' in MOVIE:
                                            self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': MOVIE,'direct': True})
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []           
             

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            SS = "0%s"%season if len(season)<2 else season
            EE = "0%s"%episode if len(episode)<2 else episode
            
            search_term = clean_search(title.lower())+'+'+'S'+SS+'E'+EE
            #print 'GWGW'+search_term

            search = 'https://www.google.com/search?q=index+of+%s'  %(search_term.replace(' ','+'))
            #print 'SEARCH > '+search
            contents = requests.get(search,timeout=3).content
            match1=re.compile('<a href="\/url\?q=(.+?)&.+?">(.+?)</a>').findall(contents)
            for movie_url , NAME in match1:
                movie_url=movie_url.replace('%2520','%20')
                x=clean_title(title).lower()
                y=clean_title(movie_url).lower()
                if 'index of /' in NAME.replace('<b>','').replace('</b>','').lower(): 
                    #print 'FILTER ME___ >'+movie_url
                    if 'plex' not in movie_url:
                        try:                
                            PAGE = requests.get(movie_url,timeout=3).content
                        except:pass 
                
                        match=re.compile('href="(.+?)"').findall(PAGE)
                        for URL in match:
                            if not 'http' in URL:
                                MOVIE = movie_url + URL
                                if MOVIE[-4]=='.':
                                    CLEANURL = URL.replace('%20','.').lower()
                                    if title.lower().replace(' ','.') in CLEANURL.replace(' ','.'):
                                        if 's'+SS in CLEANURL.replace(' ',''):
                                            if 'e'+EE in CLEANURL.replace(' ',''):
                                                if '1080p' in MOVIE:                                          
                                                    qual = '1080p'
                                                elif '720p' in MOVIE: 
                                                    qual = '720p'
                                                elif '480p' in MOVIE:
                                                    qual = '480p'
                                                else:
                                                    qual = 'SD'
                                                if '.mkv' in MOVIE:
                                                    self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': MOVIE,'direct': True})
            return self.sources
        except Exception as e:
            print repr(e)
            pass
            return []  
