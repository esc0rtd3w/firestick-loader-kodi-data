# -*- coding: utf-8 -*-
# Universal Scrapers
# 30/10/2018 -BUG

import urlparse, urllib
import re
import xbmc, xbmcaddon, time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, filter_host, send_log, error_log
from universalscrapers.modules import client, dom_parser as dom
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class movienolimit(Scraper):
    domains = ['movienolimit.to']
    name = "MovieNoLimit"
    sources = []

    def __init__(self):
        self.base_link = 'https://movienolimit.to'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        
            start_url = '%s/search?query=%s' % (self.base_link, urllib.quote_plus(search_id))
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url
            html = client.request(start_url)
            posts = client.parseDOM(html, 'div', attrs={'class': 'one_movie-item'})
            for post in posts:
                data = dom.parse_dom(post, 'a', req='href', attrs={'class': 'movie-title'})[0]
                if not clean_title(title) == clean_title(data.content): continue
                qual = client.parseDOM(post, 'span', attrs={'data-title': 'Quality'})[0]
                qual = client.replaceHTMLCodes(qual)
                item_url = urlparse.urljoin(self.base_link, data.attrs['href'])

                self.get_source(item_url, title, year, start_time, qual)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_source(self, item_url, title, year, start_time, qual):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            OPEN = client.request(item_url)

            frame = client.parseDOM(OPEN, 'iframe', ret='src')[0]
            if 'openload' in frame:
                count += 1
                self.sources.append(
                    {'source': 'openload', 'quality': qual, 'scraper': self.name, 'url': frame, 'direct': False})

            extra_links = re.findall('''window.open\(['"]([^'"]+)['"]\).+?server:([^<]+)''', OPEN, re.DOTALL)
            for link, host in extra_links:
                if not filter_host(host.replace(' ', '')): continue
                link = client.replaceHTMLCodes(link).encode('utf-8')
                link = urlparse.urljoin(self.base_link, link)
                count += 1
                self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)

        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)

    def resolve(self, link):
        try:
            if 'player.php' in link:
                url = client.request(link, output='geturl')
                return url
            elif '/redirect/' in link:
                url = client.request(link, output='geturl')
                return url
        except:
            return link


#movienolimit().scrape_movie('Venom', '2018', '')