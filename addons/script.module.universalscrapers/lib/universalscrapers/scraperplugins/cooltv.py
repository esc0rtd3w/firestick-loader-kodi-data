# -*- coding: utf-8 -*-
# Universal Scrapers
# 30/10/2018 -BUG

import re
import xbmc, xbmcaddon
import time
import urllib
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.modules import client
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class cooltv(Scraper):
    domains = ['https://cooltvseries.com']
    name = "CoolTV"
    sources = []

    def __init__(self):
        self.base_link = 'https://cooltvseries.com'
        self.sources = []

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            search = clean_search(title)
            start_url = '%s/search.php?search=%s' % (self.base_link, urllib.quote_plus(search))

            #print 'SEARCH > '+start_url
            headers = {'User-Agent': client.agent()}
            link = client.request(start_url, headers=headers, timeout=5)
            links = link.split('class="box"')
            for p in links:

                media_url = re.compile('href="([^"]+)"').findall(p)[0]
                media_title = re.compile('title="([^"]+)"').findall(p)[0]
                if search in clean_search(media_title.lower()):
                    if 'season %s' % season in media_title.lower():
                        self.get_source(media_url, title, year, season, episode, start_time)
            #print self.sources
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)

    def get_source(self, media_url, title, year, season, episode, start_time):
        #print 'source season ' + media_url
        season_bollox = "0%s" % season if len(season) < 2 else season
        episode_bollox = "0%s" % episode if len(episode) < 2 else episode
        all_bollox = 's%se%s' % (season_bollox, episode_bollox)

        try:
            headers = {'User-Agent': client.agent()}
            html = client.request(media_url,headers=headers)
            match = re.findall(r'<li><a href="([^"]+)">([^<>]*)<span.+?>', str(html), re.I | re.DOTALL)
            count = 0
            for media_url, media_title in match:

                if all_bollox in media_title.lower():
             
                    link = client.request(media_url, headers=headers)

                    frame = client.parseDOM(link, 'iframe', ret='src')
                    for frame_link in frame:
                        self.sources.append({'source': 'Openload', 'quality': 'Unknown',
                                             'scraper': self.name, 'url': frame_link, 'direct': False})

                    cool_links = re.compile('"dwn-box".+?ref="(.+?)" rel="nofollow">(.+?)<span',re.DOTALL).findall(link)
                    for vid_url, res in cool_links:
                        if '1080' in res:
                            res = '1080p'
                        elif '720' in res:
                            res = '720p'
                        elif 'HD' in res:
                            res = 'HD'
                        else:
                            res = 'SD'
                        count += 1

                        vid_url += '|User-Agent=%s&Referer=%s' % (client.agent(), media_url)
                        vid_url = urllib.quote(vid_url, '|:?/&+=_-')

                        self.sources.append({'source': 'Direct', 'quality': res, 'scraper': self.name, 'url': vid_url,
                                             'direct': True})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season='', episode='')
        except:
            pass

#cooltv().scrape_episode('the flash','2014','','1','1','','')

