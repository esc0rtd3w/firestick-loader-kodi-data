# -*- coding: utf-8 -*-

'''
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

import re, urllib, urlparse, hashlib, random, string, json, base64
from ..common import random_agent, clean_title, googletag, filter_host, clean_search, get_rd_domains,send_log,error_log
import requests
from ..scraper import Scraper
import xbmcaddon
import xbmc,time
from BeautifulSoup import BeautifulSoup

# alluc_debrid = control.setting('alluc_debrid')
alluc_debrid = False
# alluc_status = control.setting('enable_alluc')
alluc_status = 'true'
host_string = 'host%3Arapidgator.net%2Cuploaded.net%2Cfilefactory.com'
dev_log = xbmcaddon.Addon('script.module.nanscrapers').getSetting("dev_log")

# %s&query=%s+host%3Arapidgator.net%2Cuploaded.net%2Cfilefactory.com&count=%s'
class Alluc(Scraper):
    name = "Alluc"

    def __init__(self):
        self.base_link = 'https://www.alluc.ee'
        if alluc_debrid == 'true':
            self.api_link = 'http://www.alluc.ee/api/search/download/?user=%s&password=%s&query=%s'
        else:
            self.api_link = 'http://www.alluc.ee/api/search/stream/?user=%s&password=%s&query=%s'
        if dev_log=='true':
            self.start_time = time.time() 
        self.alluc_user = xbmcaddon.Addon('script.module.nanscrapers').getSetting("%s_user" % (self.name))
        self.alluc_pw = xbmcaddon.Addon('script.module.nanscrapers').getSetting("%s_pw" % (self.name))
        self.max_items = int(xbmcaddon.Addon('script.module.nanscrapers').getSetting("%s_max" % (self.name)))
        self.max_result_string = '&count=%s' % self.max_items


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            if debrid:
                global alluc_debrid
                alluc_debrid = "true"
                self.api_link = 'http://www.alluc.ee/api/search/download/?user=%s&password=%s&query=%s'
            url = self.movie(imdb, title, year)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def movie(self, imdb, title, year):
        self.zen_url = []
        try:
            if not alluc_status == 'true': raise Exception()
            #print ("ALLUC STARTED", self.alluc_user, self.alluc_pw, self.max_items)
            headers = {'User-Agent': random_agent()}
            search_title = clean_search(title)
            #search_title = title
            cleanmovie = (clean_title(title) + year).translate(None, '\/:*?"\'<>|!,').replace(' ', '-').replace('--', '-').lower()
            query = "%s+%s" % (urllib.quote_plus(search_title), year)
            query = self.api_link % (self.alluc_user, self.alluc_pw, query)
            if alluc_debrid == 'true':
                query = query + self.max_result_string
            else:
                query = query + '+%23newlinks' + self.max_result_string
            query += "&getmeta=0"
            # xbmc.log("ALLUC r2" + query)
            html = requests.get(query, headers=headers, timeout=15).json()
            for result in html['result']:
                if len(result['hosterurls']) > 1: continue
                if result['extension'] == 'rar': continue
                #lang = result.get("lang", "")
                #xbmc.log("language: " + lang)
                #if not lang == "en":
                #    xbmc.log("result: " + result)
                #    continue
                stream_url = result['hosterurls'][0]['url'].encode('utf-8')
                stream_title = result['title'].encode('utf-8')
                stream_title = clean_search(stream_title)
                if cleanmovie in clean_title(stream_title):
                    self.zen_url.append([stream_url, stream_title])
                    #print ("ALLUC r3", self.zen_url)
            return self.zen_url
        except:
            return

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            if debrid:
                global alluc_debrid
                alluc_debrid = "true"
                self.api_link = 'http://www.alluc.ee/api/search/download/?user=%s&password=%s&query=%s'
            show_url = self.tvshow(imdb, tvdb, title, show_year)
            url = self.episode(show_url, imdb, tvdb, title, year, season, episode)
            sources = self.sources(url, [], [])
            for source in sources:
                source["scraper"] = source["provider"]
            return sources
        except:
            return []

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        self.zen_url = []
        try:
            if not alluc_status == 'true': raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            cleanmovie = clean_title(title)
            data['season'], data['episode'] = season, episode
            year = data['year']
            ep_id = int(episode)
            season_id = int(season)
            ep_check = season_id + ep_id
            headers = {'User-Agent': random_agent()}
            search_title = title
            ep_check = "s%02de%02d" % (season_id, ep_id)
            cleanmovie = (clean_title(title) + ep_check).translate(None, '\/:*?"\'<>|!,').replace(' ', '-').replace('--', '-').lower()
            query = "%s+%s" % (urllib.quote_plus(search_title), ep_check)
            #print ("ALLUC r1", query)
            query = self.api_link % (self.alluc_user, self.alluc_pw, query)
            if alluc_debrid == 'true':
                query = query + self.max_result_string
            else:
                query = query + '+%23newlinks' + self.max_result_string
            #print ("ALLUC r2", query)
            html = requests.get(query, headers=headers, timeout=15).json()
            for result in html['result']:
                if len(result['hosterurls']) > 1: continue
                if result['extension'] == 'rar': continue
                stream_url = result['hosterurls'][0]['url'].encode('utf-8')
                stream_title = result['title'].encode('utf-8')
                stream_title = clean_search(stream_title)

                if cleanmovie in clean_title(stream_title):
                    self.zen_url.append([stream_url, stream_title])
                    print ("ALLUC r3", self.zen_url)
            return self.zen_url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            count = 0
            sources = []
            for url, quality in self.zen_url:
                if "1080" in quality:
                    quality = "1080p"
                elif "720" in quality:
                    quality = "HD"
                else:
                    quality = "SD"
                try:
                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                except:
                    host = 'alluc'

                if not filter_host(host) and not host == 'alluc':
                    if alluc_debrid == "true":
                        rd_domains = get_rd_domains()
                        if host not in rd_domains:
                            continue
                    else:
                        continue
                    count +=1
                #print ("ALLUC SOURCES", url, quality)
                # if not host in hostDict: continue
                if alluc_debrid == 'true':
                    count +=1
                    sources.append(
                        {'source': host, 'quality': quality, 'provider': 'Alluc', 'url': url, 'direct': False,
                         'debridonly': True})
                else:
                    count +=1
                    sources.append(
                        {'source': host, 'quality': quality, 'provider': 'Alluc', 'url': url, 'direct': False,
                         'debridonly': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)    
            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    @classmethod
    def get_settings_xml(clas):
        xml = [
            '<setting id="%s_enabled" ''type="bool" label="Enabled" default="true"/>' % (clas.name),
            '<setting id="%s_max" type="slider" label="Max Results for Search" default="20" range="5,200" option="int"/>' %(clas.name),
            '<setting id= "%s_user" type="text" label="Username" default=Username />' % (clas.name),
            '<setting id= "%s_pw" type="text" label="Password" default=Password />' % (clas.name)
        ]
        return xml
