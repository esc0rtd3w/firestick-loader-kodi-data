# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    adapted for universalscrapers
    Copyright (C) 2016 Exodus

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import xbmc, xbmcaddon,time
import re, urllib, urlparse, json
import random
from universalscrapers.common import clean_title, get_rd_domains, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, workers, dom_parser as dom, quality_tags, cfscrape

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class Releasebb(Scraper):
    domains = ['rlsbb.com']
    name = "Releasebb"
    sources = []

    def __init__(self):
        self.domains = ['rlsbb.ru']
        self.base_link = 'http://rlsbb.ru'
        self.referer_link = 'http://search.rlsbb.ru/search/{0}'
        self.search_link = 'http://search.rlsbb.ru/lib/search45224149886049641.php'
        self.search_phrase = '?phrase={0}&pindex=1&code={1}&radit={2}'


    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            if not debrid: return self.sources

            query = '%s %s' % (title, year)
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            query = urllib.quote_plus(query).replace('+', '%2B')

            scraper = cfscrape.create_scraper()
            headers = {'User-Agent': client.agent(),
                       'Referer': self.referer_link.format(query)}
            code = scraper.get(self.referer_link.format(query), headers=headers).content
            code = client.parseDOM(code, 'script', ret='data-code-rlsbb')[0]
            rand = '0.%s' % random.randint(00000000000000001, 99999999999999999)
            url = urlparse.urljoin(self.search_link, self.search_phrase.format(query.replace('+', '%2B'), str(code), str(rand)))
            r = scraper.get(url, headers=headers).content
            posts = json.loads(r)['results']
            posts = [(i['post_title'], i['post_name']) for i in posts]
            posts = [(i[0], i[1]) for i in posts if
                     clean_title(i[0].lower().split(year)[0]) == clean_title(title)]

            filter = ['uhd', '4K', '2160', '1080', '720', 'hevc', 'bluray', 'web']
            posts = [(urlparse.urljoin(self.base_link, i[1]), year) for i in posts if any(x in i[1] for x in filter)]

            threads = []
            for i in posts: threads.append(workers.Thread(self.get_sources, i, title, year, '', '', str(start_time)))
            [i.start() for i in threads]

            alive = [x for x in threads if x.is_alive() is True]
            while alive:
                alive = [x for x in threads if x.is_alive() is True]
                time.sleep(0.1)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            if not debrid: return self.sources

            hdlr = 'S%02dE%02d' % (int(season), int(episode))
            query = '%s S%02dE%02d' % (title, int(season), int(episode))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            scraper = cfscrape.create_scraper()
            headers = {'User-Agent': client.agent(),
                       'Referer': self.referer_link.format(query)}
            code = scraper.get(self.referer_link.format(query), headers=headers).content
            code = client.parseDOM(code, 'script', ret='data-code-rlsbb')[0]
            rand = '0.%s' % random.randint(00000000000000001, 99999999999999999)
            url = urlparse.urljoin(self.search_link, self.search_phrase.format(query.replace('+', '%2B'), str(code), str(rand)))
            r = scraper.get(url, headers=headers).content
            posts = json.loads(r)['results']

            if not posts:
                hdlr = 'S%02d' % int(season)
                query = '%s %s' % (title, hdlr)
                query = urllib.quote_plus(query)
                url = urlparse.urljoin(self.search_link, self.search_phrase.format(query.replace('+', '%2B'), str(code), str(rand)))
                r = scraper.get(url, headers=headers).content
                posts = json.loads(r)['results']

            posts = [(i['post_title'], i['post_name']) for i in posts]
            posts = [(i[0], i[1]) for i in posts if
                     clean_title(i[0].lower().split(hdlr.lower())[0]) == clean_title(title)]
            filter = ['uhd', '4K', '2160', '1080', '720', 'hevc', 'bluray', 'web']
            posts = [(urlparse.urljoin(self.base_link, i[1]), hdlr) for i in posts if any(x in i[1] for x in filter)]

            threads = []
            for i in posts: threads.append(workers.Thread(self.get_sources, i, title, year, season, episode, str(start_time)))
            [i.start() for i in threads]

            alive = [x for x in threads if x.is_alive() is True]
            while alive:
                alive = [x for x in threads if x.is_alive() is True]
                time.sleep(0.1)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_sources(self, url, title, year, season, episode, start_time):
        try:
            if url is None: return self.sources

            count = 0
            url, hdlr = url[0], url[1]
            main = []
            try:
                headers = {'User-Agent': client.agent(), 'Referer': self.base_link}
                scraper = cfscrape.create_scraper()
                data = scraper.get(url, headers=headers).content
                main = dom.parse_dom(data, 'div', {'class': 'postContent'})
                main = [i.content for i in main]

                comments = dom.parse_dom(data, 'div', {'class': re.compile('content')})
                main += [i.content for i in comments]
            except:
                pass

            for con in main:
                try:
                    frames = client.parseDOM(con, 'a', ret='href')

                    for link in frames:

                        if 'youtube' in link: continue
                        if any(x in link for x in ['.rar', '.zip', '.iso']) or any(
                                link.endswith(x) for x in ['.rar', '.zip', '.iso']): continue
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link.strip().lower()).netloc)[0]
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')

                        if not hdlr.lower() in link.lower(): continue

                        quality, info = quality_tags.get_release_quality(link, link)

                        if link in str(self.sources): continue
                        rd_domains = get_rd_domains()
                        if host in rd_domains:
                            count += 1
                            self.sources.append(
                                {'source': host, 'quality': quality, 'scraper': self.name, 'url': link, 'direct': False,
                                 'debridonly': True})

                except:
                    pass
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season=season, episode=episode)
            # xbmc.log('@#@SOURCES:%s' % self._sources, xbmc.LOGNOTICE)
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

#Releasebb().scrape_movie('Black Panther', '2018', '', True)