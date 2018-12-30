# -*- coding: utf-8 -*-
# Universal Scrapers

import re, requests, time, urllib
import xbmcaddon, json
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, send_log, error_log
from universalscrapers.modules.unjuice import run

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class moviefull(Scraper):
    domains = ['moviefull-hd.org']
    name = "MovieFull"
    sources = []

    def __init__(self):
        self.base_link = 'https://moviefull-hd.org/'
        self.search_url = self.base_link + 'search/%s'
        self.sources = []
        if dev_log == 'true':
            self.start_time = time.time()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search_id = urllib.quote_plus(title+' '+year).replace('+', '%2B')

            r = requests.get(self.search_url % search_id).content

            page = re.findall('id="main-col">(.+?)</section></div>', r, re.DOTALL)[0]
            Regex = re.compile('''-title.+?href=['"]([^'"]+)['"]>([^<]+)</a></div>''', re.DOTALL).findall(page)
            for item_url, name in Regex:
                #print '@#@(grabbed url) %s  (title) %s' %(item_url, name)
                if not clean_title(title).lower() == clean_title(name).lower():
                    continue
                if not year in name:
                    continue
                #print '@#@URL check> ' + item_url
                self.get_source(item_url, title, year, '', '', start_time)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_source(self, item_url, title, year, season, episode, start_time):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                       'Referer': item_url}
            r = requests.get(item_url, headers=headers).content

            link = re.compile('''<iframe.+?src=['"]([^'"]+)['"]''', re.DOTALL).findall(r)[0]
            count = 0

            html = requests.get(link, headers=headers).content
            juice = run(str(html))

            links = re.findall('sources:(\[\{.+?\}\])', juice, re.DOTALL)[0]
            links = json.loads(links)
            for i in links:
                url = i['file']
                qual = i['label']
                count += 1
                self.sources.append(
                    {'source': 'filehost', 'quality': qual, 'scraper': self.name, 'url': url + '|Referer='+link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season='', episode='')
        except:
            pass