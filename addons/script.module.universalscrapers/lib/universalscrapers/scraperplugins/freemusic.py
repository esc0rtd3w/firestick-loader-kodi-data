# -*- coding: utf-8 -*-
# Universal Scrapers
import xbmc,xbmcaddon,time
import re
import requests
from universalscrapers.common import clean_title,clean_search,random_agent,send_log,error_log
from ..scraper import Scraper

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

headers = {"User-Agent": random_agent()}

class freemusic(Scraper):
    domains = ['freemusicdownloads']
    name = "Freemusic"
    sources = []
    

    def __init__(self):
        self.base_link = 'http://down.freemusicdownloads.world/'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()
    
    def scrape_music(self, title, artist, debrid=False):
        try:
            song_search = clean_title(title.lower()).replace(' ','+')
            artist_search = clean_title(artist.lower()).replace(' ','+')
            start_url = '%sresults?search_query=%s+%s'    %(self.base_link,artist_search,song_search)
            html = requests.get(start_url, headers=headers, timeout=20).content
            match = re.compile('<h4 class="card-title">.+?</i>(.+?)</h4>.+?id="(.+?)"',re.DOTALL).findall(html)
            count = 0
            for m, link in match:
                match4 = m.replace('\n','').replace('\t','').replace('  ',' ').replace('   ',' ').replace('    ',' ').replace('     ',' ')
                match5 = re.sub('&#(\d+);', '', match4)
                match5 = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', match5)
                match5 = match5.replace('&quot;', '\"').replace('&amp;', '&')
                match5 = re.sub('\\\|/|\(|\)|\[|\]|\{|\}|-|:|;|\*|\?|"|\'|<|>|\_|\.|\?', ' ', match5)
                match5 = ' '.join(match5.split())
                match2 = m.replace('\n','').replace('\t','').replace(' ','')
                if clean_title(title).lower() in clean_title(match2).lower():
                    if clean_title(artist).lower() in clean_title(match2).lower():
                        final_link = 'https://www.youtube.com/watch?v='+link
                        count +=1
                        self.sources.append({'source':match5, 'quality':'SD', 'scraper':self.name, 'url':final_link, 'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)             

            return self.sources    
        except Exception, argument:
            return self.sources
