# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2015 lambda

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


import re,urllib,urlparse,random
import hashlib, string, json
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control


class source:
    def __init__(self):
        self.base_link = 'http://chillnflix.to'
        self.movie_link = '/%s-%s-watch-online-for-free/'
        self.shows_link = '/tvshows/%s-season-%s-watch-online-free/?action=watching&server=1&movie=%s-%s&auto=true'


    def get_movie(self, imdb, title, year):
        try:

            url = self.movie_link % (cleantitle.geturl(title), year)
            url = urlparse.urljoin(self.base_link, url)
            r = client.request(url, timeout='10')
            print("Chillflix url", url)

            r = re.findall('<a href="(.+?)" class="bwac-btn"', r)[0]
            url = r.encode('utf-8')
            print("Chillflix url", url)
            return url
        except:
            return

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            ep_id = "%01dx%01d" % (int(season), int(episode))
            url = self.shows_link % (cleantitle.geturl(title), season, cleantitle.geturl(title), ep_id)
            url = urlparse.urljoin(self.base_link, url)

            url = url.encode('utf-8')
            print("Chillflix shows url", url)
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        #sources.append({'source': host.split('.')[0], 'quality': 'SD', 'provider': 'Movie25', 'url': url})
        sources = []
        try:
            sources = []

            if url == None: return sources
            r = client.request(url)
            try:
                s = re.compile('file"?:\s*"([^"]+)"').findall(r)

                for u in s:
                    try:
                        url = u.encode('utf-8')
                        if quality == 'ND': quality = "SD"
                        # if ".vtt" in url: raise Exception()
                        sources.append({'source': 'gvideo', 'quality': client.googletag(u)[0]['quality'], 'provider': 'Chillflix', 'url': url})

                    except:
                        pass
            except:
                pass

            try:
                iframe = client.parseDOM(r, 'iframe', ret='src')[0]
                print ("CHILLFLIX IFRAME CHECK 2", iframe)
                if "wp-embed.php" in iframe:
                    if iframe.startswith('//'): iframe = "http:" + iframe

                    s = client.request(iframe)
                    print ("CHILLFLIX IFRAME CHECK 3", s)
                    s = get_sources(s)

                    for u in s:
                        try:
                            files = get_files(u)
                            for url in files:
                                url = url.replace('\\', '')
                                quality = google_tag(url)

                                url = url.encode('utf-8')
                                if quality == 'ND': quality = "SD"
                                # if ".vtt" in url: raise Exception()
                                sources.append(
                                    {'source': 'gvideo', 'quality': quality, 'provider': 'Chillflix', 'url': url,
                                     'direct': True, 'debridonly': False})

                        except:
                            pass
            except:
                pass
            return sources
        except:
            return sources

    def resolve(self, url):
        return url