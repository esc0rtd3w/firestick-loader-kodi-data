# -*- coding: utf-8 -*-

'''
    Exodus Add-on
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


import re,urllib,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviefree.to']
        self.base_link = 'http://moviefree.to'
        self.search_link = '/watch/%s-%s.html'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.search_link % (cleantitle.geturl(title), year)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url, limit='1')
            r = client.parseDOM(r, 'title')[0]
            if r == '': raise Exception()

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            url = url.replace('-online.html', '.html')

            r = client.request(url)

            s = re.findall('data-film\s*=\s*"(.+?)"\s+data-name\s*=\s*"(.+?)"\s+data-server\s*=\s*"(.+?)"', r)

            ref = url

            for u in s:
                try:
                    if not u[2] in ['1', '11', '4']: raise Exception() 
                    url = urlparse.urljoin(self.base_link, '/ip.file/swf/plugins/ipplugins.php')

                    post = {'ipplugins': '1', 'ip_film': u[0], 'ip_name': u[1] , 'ip_server': u[2]}
                    post = urllib.urlencode(post)

                    r = client.request(url, post=post, XHR=True, referer=ref)
                    r = json.loads(r)

                    url = urlparse.urljoin(self.base_link, '/ip.file/swf/ipplayer/ipplayer.php')

                    post = {'u': r['s'], 'w': '100%', 'h': '500' , 's': r['v'], 'n':'0'}
                    post = urllib.urlencode(post)

                    r = client.request(url, post=post, XHR=True, referer=ref)
                    r = json.loads(r)

                    try: url = [i['files'] for i in r['data']]
                    except: url = [r['data']]

                    for i in url:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass

                    if 'openload' in url[0]:
                        sources.append({'source': 'openload.co', 'quality': 'HD', 'language': 'en', 'url': i, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


