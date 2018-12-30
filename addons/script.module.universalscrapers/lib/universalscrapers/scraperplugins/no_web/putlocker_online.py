# -*- coding: utf-8 -*-
# 9/11/2018 -BUG

import re, urllib, urlparse
import xbmc, xbmcaddon, time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, filter_host, send_log, error_log
from universalscrapers.modules import client, cfscrape
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class putlocker_online(Scraper):
    domains = ['putlockeronlinefree.online']
    name = "Putlocker Online"
    sources = []

    def __init__(self):
        self.base_link = 'https://putlockeronlinefree.online'

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            count = 0
            urls = []
            start_time = time.time()
            search_id = clean_search(title.lower())

            start_url = '%s/search_movies?s=%s' %(self.base_link, urllib.quote_plus(search_id))
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url
            headers = {'User-Agent': client.agent(),
                       'Referer': self.base_link}
            scraper = cfscrape.create_scraper()

            html = scraper.get(start_url, headers=headers).content
            match = re.compile('class="small-item".+?href="(.+?)".+?<b>(.+?)</b>.+?<b>(.+?)</b>.+?alt="(.+?)"',re.DOTALL).findall(html)
            for item_url1, date, res, name in match:
                #print 'scraperchk - scrape_movie - name: '+name+ '  '+date
                item_url = urlparse.urljoin(self.base_link, item_url1)
                #print 'scraperchk - scrape_movie - item_url: '+item_url+' '+res
                if not clean_title(search_id) == clean_title(name): continue
                #print 'scraperchk - scrape_movie - Send this URL: ' + item_url
                OPEN = scraper.get(item_url, headers=headers).content
                Endlinks = re.compile('class="movie_links"><li(.+?)<h3><b class="icon-share-alt"', re.DOTALL).findall(OPEN)[0]

                links = re.compile('target="_blank" href="(.+?)"', re.DOTALL).findall(Endlinks)
                # print 'scraperchk - scrape_movie - link: >>>>>>>>>>>>>>>>'+str(links)
                for link in links:
                    if not link.startswith('http'): continue
                    count += 1
                    host = link.split('//')[1].replace('www.', '')
                    host = host.split('/')[0]

                    if not filter_host(host): continue

                    self.sources.append(
                        {'source': host, 'quality': res, 'scraper': self.name, 'url': link, 'direct': False})
                if dev_log == 'true':
                    end_time = time.time() - start_time
                    send_log(self.name, end_time, count, title, year)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources


#putlocker_online().scrape_movie('Black Panther', '2018', 'tt1825683', False)