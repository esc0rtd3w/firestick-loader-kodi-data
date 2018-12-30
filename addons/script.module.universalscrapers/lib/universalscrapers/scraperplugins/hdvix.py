# -*- coding: utf-8 -*-
# Universal Scrapers
# checked 10/11/2018 -BUG

import re, urllib
import xbmc, xbmcaddon, time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, filter_host, clean_search, send_log, error_log
from universalscrapers.modules import client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class hdvix(Scraper):
    domains = ['hdvix.com']
    name = "HDvix"
    sources = []

    def __init__(self):
        self.base_link = 'http://hdvix.com/'  # hdvix is a mirror. this site has 2 links

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            count = 0
            start_time = time.time()
            search_id = urllib.quote_plus('%s %s' % (clean_search(title), year))
            start_url = '%s/?s=%s' % (self.base_link, search_id)

            # print 'scraperchk - scrape_movie - start_url:  ' + start_url
            html = client.request(start_url, referer=self.base_link)
            match = re.compile('class="thumb".+?title="(.+?)".+?href="(.+?)">', re.DOTALL).findall(html)
            for name, item_url in match:
                if not year in name:
                    continue
                # print 'scraperchk - scrape_movie - name: '+name
                if not clean_title(title) == clean_title((name.split(year)[0][:-1])):
                    continue
                # print 'scraperchk - scrape_movie - Send this URL: ' + item_url
                OPEN = client.request(item_url, referer=self.base_link)
                link = client.parseDOM(OPEN, 'iframe', ret='src')[0]

                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0]
                if not filter_host(host): continue
                count += 1
                self.sources.append(
                    {'source': host, 'quality': 'HD', 'scraper': self.name, 'url': link, 'direct': False})

            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources


#hdvix().scrape_movie('Black Panther', '2018', 'tt1825683', False)