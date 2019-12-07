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
        self.base_link = 'http://onlinemovies.tube'
        self.movie_link = '/watch/%s-%s/'
        self.ep_link = '/episode/%s-%s/'

    def get_movie(self, imdb, title, year):
        try:
            # print("WATCHCARTOON")
            title = cleantitle_query(title)
            title = cleantitle_geturl(title)
            query = self.movie_link % (title, year)
            url = urlparse.urljoin(self.base_link, query)

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
            data['season'], data['episode'] = season, episode
            episodeid = "s%02de%02d" % (int(data['season']), int(data['episode']))
            title = cleantitle_query(title)
            title = cleantitle_geturl(title)

            query = self.ep_link % (title, episodeid)
            url = urlparse.urljoin(self.base_link, query)
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        #sources.append({'source': host.split('.')[0], 'quality': 'SD', 'provider': 'Movie25', 'url': url})
        sources = []

        try:
            if url == None: return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            html = self.player %  data['url']
            r = client.request(html, headers=self.headers)
            if 'episode' in data:
                match = re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)\..+?</a>').findall(r)
                match = [i for i in match if int(i[1]) == int(data['episode']) ]
            else:
                match = re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)</a>').findall(r)

            for i in match:
                print "i", i[0]
                print "i", i[1]

            for href, res in match:
                if 'webapp' in href:
                    href = href.split('embed=')[1]

                if 'google' in href:
                    sources.append({'source': 'gvideo', 'quality': client.googletag(href)[0]['quality'],
                                            'url': href, 'provider': 'Bobby'})
                else:
                    try:
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(href.strip().lower()).netloc)[0]
                        if not host in hostDict: raise Exception()
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')

                        sources.append({'source': host, 'quality': 'SD', 'url': href, 'provider': 'Bobby'})
                    except:
                        pass
            return sources
        except Exception as e:
            control.log('ERROR Boby %s' % e)
            return sources

    def resolve(self, url):
        return url