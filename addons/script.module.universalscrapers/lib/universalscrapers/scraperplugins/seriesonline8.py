# -*- coding: utf-8 -*-
# Universal Scrapers Bug
#checked 15/12/2018

import re
import xbmc, xbmcaddon, time, urllib
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.modules import client, dom_parser, quality_tags
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class seriesonline8(Scraper):
    domains = ['https://seriesonline8.co', 'https://www2.series9.io']
    name = "Series9"
    sources = []

    def __init__(self):
        self.base_link = 'https://www2.seriesonline8.co'
        self.search_link = '/movie/search'

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search = clean_search(title)
            start_url = '%s/%s/%s' % (self.base_link, self.search_link, search.replace(' ', '-'))
            #print 'series - scrape_movie - start_url:  ' + start_url
            
            html = client.request(start_url)
            match = re.compile('class="ml-item".+?href="(.+?)".+?alt="(.+?)"', re.DOTALL).findall(html)
            for item_url1, name in match:
                item_url = self.base_link +item_url1 + '/watching.html'
                #print 'series8 - scrape_movie - item_url: '+item_url
                if clean_title(search) == clean_title(name):
                    #print 'series8 - scrape_movie - Send this URL: ' + item_url
                    self.get_source(item_url, title, year, start_time)

            #print self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            season_chk = '-season-%s' % season
            #print season_chk
            search_id = clean_search(title.lower())
            start_url = '%s/%s/%s' % (self.base_link, self.search_link, search_id.replace(' ', '-'))
            html = client.request(start_url, redirect=True)
            match = re.compile('class="ml-item".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for season_url, title in match:
                #print season_url
                if not season_chk in season_url:
                    continue
                #print 'PASSED season URL### ' +season_url
                episode_grab = 'Season %s Episode %s ' % (season, episode)

                item_url = self.base_link + season_url + '/watching.html'

                self.get_source(item_url, title, episode_grab, start_time)

            #print self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_source(self, item_url, title, year, start_time):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            headers = {'User-Agent': client.agent()}
            OPEN = client.request(item_url, headers=headers)
            #print OPEN
            Endlinks = dom_parser.parse_dom(OPEN, 'a', req='player-data')

            Endlinks = [(i.attrs['player-data'], i.content) for i in Endlinks if i]
            if 'Season' in year:
                Endlinks = [(i[0], 'SD') for i in Endlinks if i[1] in year]
            else:
                Endlinks = [(i[0], i[1]) for i in Endlinks if i]

            #print 'series8 - scrape_movie - EndLinks: '+str(Endlinks)
            for link, quality in Endlinks:
                qual = quality_tags.check_sd_url(quality)

                if 'vidcloud' in link:
                    link = 'https:' + link if link.startswith('//') else link
                    data = client.request(link, headers=headers)
                    link = re.findall('''file\s*:\s*['"](.+?)['"].+?type['"]\s*:\s*['"](.+?)['"]''', data, re.DOTALL)[0]
                    host = link[1]
                    link = link[0] + '|User-Agent=%s&Referer=https://vidcloud.icu/' % urllib.quote(client.agent())
                    direct = True
                else:
                    host = link.split('//')[1].replace('www.', '')
                    host = host.split('/')[0].split('.')[0].title()
                    direct = False

                count += 1
                self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': direct})

            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

#seriesonline8().scrape_movie('Black Panther', '2018', 'tt1825683', False)
#seriesonline8().scrape_episode('Suits','2011','','8','5','','')