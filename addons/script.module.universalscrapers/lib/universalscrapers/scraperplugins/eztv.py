# -*- coding: utf-8 -*-
# Universal Scrapers Bug
# 27/12/2018

import re, time, xbmcaddon, xbmc
import urllib, urlparse
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, get_rd_domains, send_log, error_log
from universalscrapers.modules import client, dom_parser as dom, workers, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class eztv(Scraper):
    domain = ['eztv.io']
    name = 'EZTV'
    sources = []

    def __init__(self):
        self.base_link = 'https://eztv.io/'
        self.tvsearch = 'https://eztv.io/search/{0}'

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
        sources = []
        try:
            count = 0
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            self.title = data['tvshowtitle']
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))

            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            url = self.tvsearch.format(urllib.quote_plus(query).replace('+', '-'))

            items = self._get_items(url)

            for item in items:
                try:
                    name = item[0]
                    quality, info = quality_tags.get_release_quality(name, name)
                    info.append(item[2])
                    info = ' | '.join(info)
                    url = item[1]
                    url = url.split('&tr')[0]
                    count += 1
                    qual = '{0} | {1}'.format(quality, info)
                    self.sources.append({'source': 'MAGNET', 'quality': qual, 'scraper': self.name, 'url': url,
                                         'direct': False, 'debridonly': True})
                except BaseException:
                    pass
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
        items = []
        try:
            headers = {'User-Agent': client.agent()}
            r = client.request(url, headers=headers)
            posts = client.parseDOM(r, 'tr', attrs={'name': 'hover'})
            for post in posts:
                data = dom.parse_dom(post, 'a', {'class': 'magnet'}, req=['href', 'title'])[0]
                url = data.attrs['href']
                name = data.attrs['title']
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

                items.append((name, url, size))
            return items
        except BaseException:
            return items