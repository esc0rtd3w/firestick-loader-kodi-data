import re,xbmcaddon,time,requests
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log    
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log") 

headers = {"User-Agent": random_agent()}

class mp3Guild(Scraper):
    name = "Mp3guild"
    sources = []
    

    def __init__(self):
        self.base_link = 'http://mp3guild.com'
        self.sources = []
        if dev_log=='true':
            self.start_time = time.time()
    
    def scrape_music(self, title, artist, debrid=False):
        try:
            song_search = clean_title(title.lower()).replace(' ','_')
            artist_search = clean_title(artist.lower()).replace(' ','_')
            start_url = 'http://mp3guild.com/mp3/%s_%s' % (artist_search,song_search)
            html = requests.get(start_url, headers=headers, timeout=20).content
            match = re.compile('<div id="mp3list" class="unplaying">.+?<div class="unselectable">(.+?)<span.+?class="dropbox-download">.+?<a href="(.+?)"',re.DOTALL).findall(html)
            title = match[0][0]
            link = match[0][1]
            self.sources.append({'source': self.name,'quality': 'mp3','scraper': title,'url': link,'direct': True})

            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)             

            return self.sources    
        except Exception, argument:
            return self.sources
