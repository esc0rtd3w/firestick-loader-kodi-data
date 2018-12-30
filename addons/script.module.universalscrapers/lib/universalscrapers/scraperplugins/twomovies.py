# -*- coding: utf-8 -*-
# Universal Scrapers
# made 22/11/2018

import re, xbmcaddon, xbmc, time
import urlparse

from universalscrapers.common import filter_host, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class Watchepisodes(Scraper):
    domains = ['www1.two-movies.name']
    name = "Twomovies"

    def __init__(self):
        self.base_link = 'https://www1.two-movies.name/'
        self.search_link = 'https://www1.two-movies.name/search/?search_query=%s&criteria=all' #imdb
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            start_url = self.search_link % imdb

            post = client.request(start_url, XHR=True, output='geturl')
            self.get_sources(post, title, year, '', '', start_time)

            return self.sources
        except Exception as argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return[]

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            start_url = self.search_link % imdb
            post = client.request(start_url, XHR=True, output='geturl')
            #//www1.two-movies.name/watch_episode/The_Walking_Dead/2/5/
            epi_link = '%s/%01d/%01d' % (post.replace('tv_show', 'episode'), int(season), int(episode))

            self.get_sources(epi_link, title, year, season, episode, start_time)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_sources(self, url, title, year, season, episode, start_time):
        try:
            count = 0
            if url is None:
                return self.sources

            r = client.request(url)
            frame = client.parseDOM(r, 'table', attrs={'class': 'striped'})[0]
            frame = client.parseDOM(frame, 'a', ret='href')[0]
            frame = urlparse.urljoin(self.base_link, frame) if frame.startswith('/') else frame
            r = client.request(frame)
            hash = re.findall('''var\s*hash\s*=\s*['"]([^'"]+)''', r, re.MULTILINE)[0]#var hash = '9fafa6c0c1771b38a1c72a5bd893c503';
            pdata = 'hash=%s&confirm_continue=I+understand%s+I+want+to+continue' % (str(hash), '%2C')
            data = client.request(frame, post=pdata, referer=frame)
            frames = re.compile('''vlink.+?title=['"]([^'"]+).+?href=['"]([^'"]+).+?onclick.+?>(.+?)</a''', re.M | re.DOTALL).findall(data.replace('\n', ''))
            #xbmc.log('@#@Frames:%s' % frames, xbmc.LOGNOTICE)

            for name, link, host in frames:
                try:
                    host = host.replace('\xc5\x8d', 'o').replace('\xc4\x93', 'e').replace('\xc4\x81', 'a').replace('\xc4\xab', 'i')#.replace('\u014d', 'o').replace('\u0113', 'e').replace('\u0101', 'a').replace('\u012b', 'i')
                    if not filter_host(host): continue

                    count += 1
                    quality, info = quality_tags.get_release_quality(name, name)
                    if quality == '4K':
                        quality = '1080p'
                    elif quality == '1080p' and not 'openload' in host:
                        quality = '720p'

                    link = urlparse.urljoin(self.base_link, link) if link.startswith('/') else link

                    self.sources.append(
                        {'source': host, 'quality': quality, 'scraper': self.name, 'url': link, 'direct': False})
                except:
                    pass

            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)

        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def resolve(self, url):
        try:
            if self.base_link in url:
                data = client.request(url, referer=self.base_link)
                link = client.parseDOM(data, 'iframe', ret='src')[0]
                link = 'https:' + link if link.startswith('//') else link
            else:
                link = url
            return link
        except:
            return
