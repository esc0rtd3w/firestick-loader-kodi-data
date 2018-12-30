# -*- coding: utf-8 -*-
# Universal Scrapers
# 30/10/2018 -BUG

import requests
import re, urllib, urlparse
import xbmc, xbmcaddon, time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.modules import client, dom_parser, cfscrape, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

s = requests.session()


class hdpopcorn(Scraper):
    domains = ['hdpopcorns.com']
    name = "HD Popcorns"
    sources = []

    def __init__(self):
        self.base_link = 'http://hdpopcorns.co/'
        self.search_link = '?s=%s'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time() 
            search_id = '%s %s' % (clean_search(title.lower()), year)
            start_url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(search_id))

            headers={'User-Agent': client.agent()}
            scraper = cfscrape.create_scraper()
            html = scraper.get(start_url, headers=headers).content
            #xbmc.log('@#@DATA:%s' % html, xbmc.LOGNOTICE)
            data = client.parseDOM(html, 'div', attrs={'id': 'content_box'})[0]
            data = client.parseDOM(data, 'h2') #returns a list with all search results
            data = [dom_parser.parse_dom(i, 'a', req=['href', 'title'])[0] for i in data if i] #scraping url-title
            links = [(i.attrs['href'], i.attrs['title']) for i in data if i] #list with link-title for each result
            #xbmc.log('@#@LINKS:%s' % links, xbmc.LOGNOTICE)
            for m_url, m_title in links:
                movie_year = re.findall("(\d{4})", re.sub('\d{3,4}p', '', m_title))[-1]
                movie_name = m_title.split(movie_year)[0]

                if not clean_title(title) == clean_title(movie_name):
                    continue
                if not year in movie_year:
                    continue
                url = m_url

                #error_log(self.name + ' Pass',url)
                self.get_source(url, title, year, '', '', start_time)
            #print self.sources
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)

    def get_source(self,url, title, year, season, episode, start_time):
        try:
            scraper = cfscrape.create_scraper()
            headers = {'Origin': 'http://hdpopcorns.com', 'Referer': url,
                       'X-Requested-With': 'XMLHttpRequest',
                       'User-Agent': client.agent()}
            count = 0
            data = scraper.get(url, headers=headers).content
            data = client.parseDOM(data, 'div', attrs={'class': 'thecontent'})[0]
            FN720p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FileName720p'})[0]
            FS720p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FileSize720p'})[0]
            FSID720p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FSID720p'})[0]
            FN1080p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FileName1080p'})[0]
            FS1080p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FileSize1080p'})[0]
            FSID1080p = client.parseDOM(data, 'input', ret='value', attrs={'name': 'FSID1080p'})[0]
            post = {'FileName720p': FN720p, 'FileSize720p': FS720p, 'FSID720p': FSID720p,
                    'FileName1080p': FN1080p, 'FileSize1080p': FS1080p, 'FSID1080p': FSID1080p,
                    'x': 173, 'y': 22}
            data = scraper.post('%s/select-movie-quality.php' % self.base_link, data=post).content
            data = client.parseDOM(data, 'div', attrs={'id': 'btn_\d+p'})

            u = [client.parseDOM(i, 'a', ret='href')[0] for i in data]
            for url in u:
                quality, info = quality_tags.get_release_quality(url, url)

                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                url += '|User-Agent=%s' % client.agent()
                count += 1
                self.sources.append(
                    {'source': 'DirectLink', 'quality': quality, 'scraper': self.name, 'url': url, 'direct': True})

            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season,episode=episode)
        except:
            pass

#hdpopcorn().scrape_movie('Blade Runner 2049', '2017', '', False) #title contains 2 years
#hdpopcorn().scrape_movie('Deadpool 2', '2018', '', False) #title contains number