# -*- coding: utf-8 -*-
# Universal Scrapers Bug
# 25/12/2018
# Site to get more urls to use.  https://piratebayproxy.info/

import re, time, xbmcaddon, xbmc
import urllib, urlparse
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, get_rd_domains, send_log, error_log
from universalscrapers.modules import client, dom_parser as dom, workers, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class piratebay(Scraper):
    domain = ['pirateproxy.live', 'thepiratebay.org', 'thepiratebay.fun', 'thepiratebay.asia', 'tpb.party', 'thepiratebay3.org', 'thepiratebayz.org', 'thehiddenbay.com', 'piratebay.live', 'thepiratebay.zone']
    name = 'PirateBay'
    sources = []


    def __init__(self):
        self.base_link = 'https://tpb.cool'
        self.search_link = '/search/%s/0/99/0'


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
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': title, 'year': show_year, 'season': season, 'episode': episode}
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
            tit = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) \
                    if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            url = urlparse.urljoin(self.base_link, self.search_link%(urllib.quote(query)))
            r = client.request(url)
            r = client.parseDOM(r, 'table', attrs={'id': 'searchResult'})[0]
            posts = client.parseDOM(r, 'td')
            posts = [i for i in posts if 'detName' in i]
            for post in posts:
                post = post.replace('&nbsp;', ' ')
                name = client.parseDOM(post, 'a')[0]
                t = name.split(hdlr)[0]
                if not clean_title(re.sub('(|)', '', t)) == clean_title(tit):
                    continue
                try:
                    y = re.findall('[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
                except BaseException:
                    y = re.findall('[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()
                if not y == hdlr:
                    continue
                links = client.parseDOM(post, 'a', ret='href')
                magnet = [i for i in links if 'magnet:' in i][0]
                url = magnet.split('&tr')[0]
                count += 1
                quality, info = quality_tags.get_release_quality(name, name)
                try:
                    size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                    div = 1 if size.endswith(('GB', 'GiB')) else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                    size = '%.2f GB' % size
                except BaseException:
                    size = '0'
                info.append(size)
                info = ' | '.join(info)
                qual = '{0} | {1}'.format(quality, info)
                self.sources.append({'source': 'Torrent', 'quality': qual, 'scraper': self.name, 'url': url, 'direct': False, 'debridonly': True})
            if dev_log == 'true':
                end_time = time.time() - float(start_time)
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources


    def resolve(self, url):
        return url


