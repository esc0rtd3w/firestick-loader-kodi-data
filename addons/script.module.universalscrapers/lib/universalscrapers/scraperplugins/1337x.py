# -*- coding: utf-8 -*-
# Universal Scrapers Bug
# 24/02/2019

import re, time, xbmcaddon, xbmc
import urllib, urlparse
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, send_log, error_log
from universalscrapers.modules import client, dom_parser as dom, workers, quality_tags, cfscrape


dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class one337x(Scraper):
    domain = ['1337x.to']
    name = 'one337x'
    sources = []

    def __init__(self):
        self.base_link = 'https://1337x.is/'
        self.tvsearch = 'https://1337x.is/sort-category-search/{0}/TV/seeders/desc/{1}/'
        self.moviesearch = 'https://1337x.is/sort-category-search/{0}/Movies/size/desc/{1}/'


    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            if not debrid:
                return self.sources
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            self.get_source(url, title, year, '', '', str(start_time))
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources


    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            if not debrid:
                return self.sources

            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': title, 'year': show_year, 'season': season,
                   'episode': episode}
            url = urllib.urlencode(url)
            self.get_source(url, title, show_year, season, episode, str(start_time))
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_source(self, url, title, year, season, episode, start_time):
        try:
            self.items = []
            count = 0
            if url is None:
                return self.sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            urls = []
            if 'tvshowtitle' in data:
                urls.append(self.tvsearch.format(urllib.quote(query), '1'))
                urls.append(self.tvsearch.format(urllib.quote(query), '2'))
                urls.append(self.tvsearch.format(urllib.quote(query), '3'))
            else:
                urls.append(self.moviesearch.format(urllib.quote(query), '1'))
                urls.append(self.moviesearch.format(urllib.quote(query), '2'))
                urls.append(self.moviesearch.format(urllib.quote(query), '3'))
            threads = []
            for url in urls:
                threads.append(workers.Thread(self._get_items, url))
            [i.start() for i in threads]
            [i.join() for i in threads]

            threads2 = []
            for i in self.items:
                count += 1
                threads2.append(workers.Thread(self._get_sources, i))
            [i.start() for i in threads2]
            [i.join() for i in threads2]

            if dev_log == 'true':
                end_time = time.time() - float(start_time)
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)
            # xbmc.log('@#@SOURCES:%s' % self._sources, xbmc.LOGNOTICE)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def _get_items(self, url):
        try:
            headers = {'User-Agent': client.agent()}
            scraper = cfscrape.create_scraper()
            r = scraper.get(url, headers=headers)
            #r = client.request(url, headers=headers)
            posts = client.parseDOM(r.content, 'tbody')[0]
            posts = client.parseDOM(posts, 'tr')
            for post in posts:
                data = dom.parse_dom(post, 'a', req='href')[1]
                link = urlparse.urljoin(self.base_link, data.attrs['href'])
                name = data.content
                t = name.split(self.hdlr)[0]

                if not clean_title(re.sub('(|)', '', t)) == clean_title(self.title): continue

                try:
                    y = re.findall('[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
                except BaseException:
                    y = re.findall('[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()
                if not y == self.hdlr: continue

                try:
                    size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                    div = 1 if size.endswith(('GB', 'GiB')) else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                    size = '%.2f GB' % size

                except BaseException:
                    size = '0'

                self.items.append((name, link, size))

            return self.items
        except BaseException:
            return self.items

    def _get_sources(self, item):
        try:
            name = item[0]
            quality, info = quality_tags.get_release_quality(item[1], name)
            info.append(item[2])
            info = ' | '.join(info)
            qual = '{0} | {1}'.format(quality, info)
            data = client.request(item[1])
            data = client.parseDOM(data, 'a', ret='href')
            url = [i for i in data if 'magnet:' in i][0]
            url = url.split('&tr')[0]

            self.sources.append(
                {'source': 'MAGNET', 'quality': qual, 'scraper': self.name, 'url': url, 'direct': False, 'debridonly': True})
        except BaseException:
            pass
