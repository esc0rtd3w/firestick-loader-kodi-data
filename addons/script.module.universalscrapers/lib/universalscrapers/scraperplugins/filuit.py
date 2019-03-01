# -*- coding: utf-8 -*-
# Universal Scrapers
# 13/11/2018 - BUG

import xbmcaddon, xbmc
import time
import re, requests
import urllib, urlparse

from universalscrapers.common import send_log, error_log, clean_search, clean_title
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, quality_tags, workers, cache, cfscrape

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class filepursuit(Scraper):
    domains = ['filepursuit.com']
    name = "filepursuit"

    def __init__(self):
        self.sources = []
        self.base_link = 'https://filepursuit.com'
        self.search_links = ['/%s?q=%s&type=video', '/%s?q=%s&type=video&startrow=49',
                             '/%s?q=%s&type=video&startrow=98', '/%s?q=%s&type=video&startrow=147']
        self.search_referer = 'https://filepursuit.com/pursuit?q={0}'
        self.ua = client.agent()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            query = clean_search(title)
            self.query = urllib.quote_plus(query + ' ' + year).replace('+', '%20')

            threads = []
            for link in self.search_links:
                threads.append(workers.Thread(self._get_sources, link, title, year, 'movie', '', '', str(start_time)))
            [i.start() for i in threads]
            [i.join() for i in threads]

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            hdlr = 'S%02dE%02d' % (int(season), int(episode))
            query = clean_search(title)
            self.query = urllib.quote_plus(query + ' ' + hdlr).replace('+', '%20')
            threads = []
            for link in self.search_links:
                threads.append(workers.Thread(self._get_sources, link, title, year, 'show', season, episode, str(start_time)))
            [i.start() for i in threads]
            [i.join() for i in threads]

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def _get_sources(self, link, title, year, _type, season, episode, start_time):
        try:
            squery = self.query.replace('%20', '+')
            self.headers = {'User-Agent': self.ua,
                            'Referer': self.search_referer.format(squery)}

            srch = cache.get(client.request, 8, self.base_link)
            srch = client.parseDOM(srch, 'form', ret='action', attrs={'name': 'frm'})[0]
            srch = srch[1:] if srch.startswith('/') else srch

            link = urlparse.urljoin(self.base_link, link % (srch, self.query))

            r = client.request(link, headers=self.headers)
            posts = client.parseDOM(r, 'tbody')[0]
            posts = client.parseDOM(posts, 'tr')
            urls = [(client.parseDOM(i, 'a', ret='href')[1],
                     client.parseDOM(i, 'a')[1],
                     client.parseDOM(i, 'a', ret='href', attrs={'id': 'refer.+?'})[0]) for i in posts if i]

            count = 0
            for url, name, host in urls:

                name = client.replaceHTMLCodes(name).replace('%20', ' ').replace('%27', "'")
                if any(x in url.lower() for x in ['italian', 'teaser', 'bonus.disc', 'subs', 'sub',
                                                  'samples', 'extras', 'french', 'trailer', 'trailers', 'sample']):
                    continue

                if _type == 'movie':
                    t = name.split(year)[0]
                    if clean_title(t) not in clean_title(title): continue
                    y = re.findall('[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
                    if not year == y: continue
                else:
                    hdlr = 'S%02dE%02d' % (int(season), int(episode))
                    t = name.split(hdlr)[0]
                    if clean_title(t) not in clean_title(title): continue
                    y = re.findall('[\.|\(|\[|\s|\_](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_]', name, re.I)[-1].upper()
                    if not y == hdlr: continue

                quality, info = quality_tags.get_release_quality(name, url)
                info = ' | '.join(info)
                res = '{0} | {1}'.format(quality, info)

                count += 1
                url = urlparse.urljoin(self.base_link, url) if url.startswith('/') else url
                host = host.split('/')[2]
                self.sources.append({'source': host, 'quality': res, 'scraper': self.name, 'url': url, 'direct': True})

            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)

        except:
            pass

    def resolve(self, url):
        if '/file/' in url:
            r = client.request(url)
            url = client.parseDOM(r, 'a', ret='href', attrs={'id': 'download1'})[0]
            url += '|User-Agent=%s&Referer=%s' % (urllib.quote(self.ua), self.base_link)
            return url
        else:
            return url

# filepursuit().scrape_movie('Black Panther', '2018', '')