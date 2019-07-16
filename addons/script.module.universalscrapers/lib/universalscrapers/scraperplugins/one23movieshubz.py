# -*- coding: utf-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################
# Universal Scrapers scraper convirted from tantrum scrapers to work with SMUS

import re, requests, time, urllib,json,urlparse
import xbmcaddon, xbmc
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, filter_host, send_log, error_log
from universalscrapers.modules import client, dom_parser, quality_tags, cfscrape

dev_log =xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class m4ufree(Scraper):
    domains = ['123movieshubz.com']
    name = "One23moviesHubz"
    sources = []

    def __init__(self):
        self.base_link = 'http://123movieshubz.com'
        self.search_link = '/watch/%s-%s-online-123movies.html'
        self.scraper = cfscrape.create_scraper()


    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search_id = title.replace(' ','-').lower()
            query = urlparse.urljoin(self.base_link, (self.search_link %(search_id,year)))
            self.get_source(query, title, year, '', '', start_time)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, 'Check Search')
            return self.sources


    def get_source(self, url, title, year, season, episode, start_time):
        try:
            count = 0
            if url == None:
                return self.sources
            r = self.scraper.get(url).content
            quality = re.findall(">(\w+)<\/p",r)
            if quality[0] == "HD":
                quality = "720p"
            else:
                quality = "SD"
            r = dom_parser.parse_dom(r, 'div', {'id': 'servers-list'})
            r = [dom_parser.parse_dom(i, 'a', req=['href']) for i in r if i]
            for i in r[0]:
                url = {'url': i.attrs['href'], 'data-film': i.attrs['data-film'], 'data-server': i.attrs['data-server'], 'data-name' : i.attrs['data-name']}
                url = urllib.urlencode(url)
                count +=1
                self.sources.append({'source': i.content, 'quality': quality, 'scraper': self.name, 'url': url, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season='', episode='')
        except:
            pass


    def resolve(self, url):
        try:
            urldata = urlparse.parse_qs(url)
            urldata = dict((i, urldata[i][0]) for i in urldata)
            post = {'ipplugins': 1,'ip_film': urldata['data-film'], 'ip_server': urldata['data-server'], 'ip_name': urldata['data-name'],'fix': "0"}
            self.scraper.headers.update({'Referer': urldata['url'], 'X-Requested-With': 'XMLHttpRequest'})
            p1 = self.scraper.post('http://123movieshubz.com/ip.file/swf/plugins/ipplugins.php', data=post).content
            p1 = json.loads(p1)
            p2 = self.scraper.get('http://123movieshubz.com/ip.file/swf/ipplayer/ipplayer.php?u=%s&s=%s&n=0' %(p1['s'],urldata['data-server'])).content
            p2 = json.loads(p2)
            p3 = self.scraper.get('http://123movieshubz.com/ip.file/swf/ipplayer/api.php?hash=%s' %(p2['hash'])).content
            p3 = json.loads(p3)
            n = p3['status']
            if n == False:
                p2 = self.scraper.get('http://123movieshubz.com/ip.file/swf/ipplayer/ipplayer.php?u=%s&s=%s&n=1' %(p1['s'],urldata['data-server'])).content
                p2 = json.loads(p2)
            url = p2["data"].replace("\/","/")
            if not url.startswith('http'):
                url =  "https:" + url
            return url
        except:
            return


