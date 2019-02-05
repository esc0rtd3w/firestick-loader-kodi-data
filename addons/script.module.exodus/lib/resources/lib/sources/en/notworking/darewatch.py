# -*- coding: UTF-8 -*-
'''
    darewatch scraper for Exodus.
    Nov 9 2018 - Checked
    rev.3) Sep 19 2018 - Cleaned and Checked
    rev.2) Sep 18 2018 - Cleaned and Checked
    rev.1) Sep 17 2018 - Cleaned and Checked

    Updated and refactored by someone.
    Originally created by others.
'''
import re, traceback, urllib, urlparse, json, random, time
import base64
import requests
from time import time

import xbmc

from resources.lib.modules import client
from resources.lib.modules import cfscrape
from resources.lib.modules import log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['ondarewatch.com', 'dailytvfix.com']
        self.base_link = 'http://www.dailytvfix.com'

        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('DAREWATCH - Exception: \n' + str(failure))
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('DAREWATCH - Exception: \n' + str(failure))
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('RLSBB - Exception: \n' + str(failure))
            return


    def sources(self, url, hostDict, hostprDict):
        log_utils.log("DAREWATCH debug")
            
        sources = []
        query_bases  = []
        options = []
        items = []
        html    = None

        if url == None: return sources

        data = urlparse.parse_qs(url)
        data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])        
        title = (data['tvshowtitle'] if 'tvshowtitle' in data else data['title'])
        query = self.base_link + '/%s/season/%02d/episode/%02d' % (data['tvshowtitle'].replace(" ","-"), int(data['season']), int(data['episode']))
        log_utils.log("DAREWATCH query : " + str(query))

        html = self.scraper.get(query)

        log_utils.log("DAREWATCH html_code 1 : " + str(html.status_code))

        if html.status_code == 200:
            posts = client.parseDOM(html.content, "li", attrs={"class": "current"})   # get all <li class=current>...</div>
            #log_utils.log("DAREWATCH posts : " + str(posts))
            for post in posts:
                item = client.parseDOM(post, 'a', ret="href", attrs={"target": "_blank"})
                if len(item) > 0:
                    items.append(item[0])
            
            log_utils.log("DAREWATCH items : " + str(items))

        else: 
            log_utils.log("DAREWATCH return code 1 : " + str(html.status_code))

        # On some movies there's like 20+ Openload links, most of the time there's no need for so many.
        openload_limit = 10 # Set this as the maximum amount of Openload links obtained from Darewatch.
        hostDict = hostprDict + hostDict 

        for item in items :
            log_utils.log("DAREWATCH item : " + str(item))
            html = self.scraper.get(item)

            if html.status_code != 200:
                log_utils.log("DAREWATCH return code 2 : " + str(html.status_code))
                continue 
            else:
                link = client.parseDOM(html.content, "iframe", ret="src")[0]
                log_utils.log("DAREWATCH link : " + str(link))

            if 'openload' in link:
                # Avoids some duplicate Openload links, both of these come up:
                # https://openload.co/embed/dVdG-TGRkZc/Ready.Player.One.2018.(...)
                # https://openload.co/embed/dVdG-TGRkZc
                is_duplicate = next(
                        (
                            True
                            for source in sources
                            if (len(link) < len(source['url']) and link in source['url'])
                            or (len(source['url']) < len(link) and source['url'] in link)
                        ),
                        False
                )
                if is_duplicate or openload_limit < 1:
                    continue # Skip this source.
                else:
                    quality = 'HD'
                    openload_limit -= 1 # Count towards the Openload links limit.
            else:
                quality = 'SD'

            hoster = link.split('//', 1)[1].replace('www.', '', 1)
            hoster = hoster[ : hoster.find('/')]
            sources.append(
                    {
                        'source': hoster,
                        'quality': quality,
                        'language': 'en',
                        'url': link,
                        'direct': False,
                        'debridonly': False
                    }
            )
        return sources


