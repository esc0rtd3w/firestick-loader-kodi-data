# -*- coding: utf-8 -*-
# Universal Scrapers
# checked 10/11/2018 -BUG

import urllib, re, time
import xbmc, xbmcaddon
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, send_log, error_log
from universalscrapers.modules import client, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class joymovies(Scraper):
    domains = ['oceanofmovies.bz']
    name = "OceanofMovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://oceanofmovies.info'
        self.search_link = '/search/%s/feed/rss2/'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = '%s %s' % (title, year)
            start_url = self.base_link + self.search_link % urllib.quote_plus(search_id)

            r = client.request(start_url)
            items = client.parseDOM(r, 'item')
            items = [i for i in items if imdb in i]
            for item in items:
                self.get_source(item, title, year, '', '', start_time)

            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_source(self, item_url, title, year, season, episode, start_time):
        count = 0
        try:
            #print '%s %s %s' %(item_url,title,year)
            if item_url is None:
                return self.sources
            qual = re.search('Quality\s*:(.+?)<br', item_url, re.DOTALL).groups()[0]
            qual = re.sub('<.+?>', '', qual)
            qual, info = quality_tags.get_release_quality(qual, qual)


            headers = {'Origin': self.base_link, 'Referer': client.parseDOM(item_url, 'link')[0],
                       'X-Requested-With': 'XMLHttpRequest', 'User_Agent': client.agent()}

            fn = client.parseDOM(item_url, 'input', attrs={'name': 'FName'}, ret='value')[0]
            fs = client.parseDOM(item_url, 'input', attrs={'name': 'FSize'}, ret='value')[0]
            fsid = client.parseDOM(item_url, 'input', attrs={'name': 'FSID'}, ret='value')[0]
            #params = re.compile('<input name="FName" type="hidden" value="(.+?)" /><input name="FSize" type="hidden" value="(.+?)" /><input name="FSID" type="hidden" value="(.+?)"').findall(html)

            post_url = self.base_link + '/thanks-for-downloading/'
            form_data = {'FName': fn, 'FSize': fs, 'FSID': fsid}
            #link = requests.post(request_url, data=form_data, headers=headers).content
            link = client.request(post_url, post=form_data, headers=headers)

            stream_url = client.parseDOM(link, 'meta', attrs={'http-equiv': 'refresh'}, ret='content')[0]
            stream_url = client.replaceHTMLCodes(stream_url).split('url=')[-1]

            stream_url += '|User-Agent=%s' % urllib.quote(client.agent())
            count += 1
            self.sources.append({'source': 'DirectLink', 'quality': qual, 'scraper': self.name, 'url': stream_url, 'direct': True})

            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title + stream_url, year, season=season, episode=episode)

        except:
            pass