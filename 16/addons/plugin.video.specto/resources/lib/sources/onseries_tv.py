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


import re,urllib,urlparse,time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.resolvers import control
from resources.lib import resolvers
import json

class source:
    def __init__(self):
        self.base_link = 'http://onwatchseries.to'
        self.search_link = 'http://onwatchseries.to/show/search-shows-json'
        self.search_link_2 = 'http://onwatchseries.to/search/%s'


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            t = cleantitle.get(tvshowtitle)

            q = urllib.quote_plus(cleantitle.query(tvshowtitle))
            p = urllib.urlencode({'term': q})
            h = {'X-Requested-With': 'XMLHttpRequest'}

            r = client.request(self.search_link, post=p, headers=h)
            try: r = json.loads(r)
            except: r = None

            if r:
                r = [(i['seo_url'], i['value'], i['label']) for i in r if 'value' in i and 'label' in i and 'seo_url' in i]
            else:
                r = client.request(self.search_link_2 % q, '/search/')
                r = client.parseDOM(r, 'div', attrs = {'valign': '.+?'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), client.parseDOM(i, 'a')) for i in r]
                r = [(i[0][0], i[1][0], i[2][0]) for i in r if i[0] and i[1] and i[2]]

            r = [(i[0], i[1], re.findall('(\d{4})', i[2])) for i in r]
            r = [(i[0], i[1], i[2][-1]) for i in r if i[2]]
            r = [i for i in r if t == cleantitle.get(i[1]) and year == i[2]]

            url = r[0][0]

            url = url.strip('/').split('/')[-1]
            url = url.encode('utf-8')

            return url
        except:
            return



    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = '%s/serie/%s' % (self.base_link, url)
            myses = 's%s_e%s' %(season, episode)

            r = client.request(url)
            r = client.parseDOM(r, 'li', attrs = {'itemprop': 'episode'})

            t = cleantitle.get(title)

            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'itemprop': 'name'}), re.compile('(\d{4}-\d{2}-\d{2})').findall(i)) for i in r]
            r = [(i[0], i[1][0].split('&nbsp;')[-1], i[2]) for i in r if i[1]] + [(i[0], None, i[2]) for i in r if not i[1]]
            r = [(i[0], i[1], i[2][0]) for i in r if i[2]] + [(i[0], i[1], None) for i in r if not i[2]]
            r = [(i[0][0], i[1], i[2]) for i in r if i[0]]

            url = [i for i in r if t == cleantitle.get(i[1]) and myses in i[0]][:1]

            if not url: url = [i for i in r if t == cleantitle.get(i[1])]
            if len(url) > 1 or not url: url = [i for i in r if date == i[2]]
            if len(url) > 1 or not url: raise Exception()

            url = url[0][0]

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return



    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            links = client.parseDOM(r, 'a', ret='href', attrs = {'target': '.+?'})
            links = [x for y,x in enumerate(links) if x not in links[:y]]
            print "Links", links
            for i in links:
                try:
                    url = i

                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['r'][0]
                    url = url.decode('base64')
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    #if not host in hostDict: raise Exception()

                    host = host.encode('utf-8')
                    #control.log('Host onseries "%s"' % host)

                    sources.append({'source': host, 'quality': 'SD', 'provider': 'OnSeries','url': url})
                except:
                    pass

            return sources
        except Exception as e:
            control.log('ERROR onseries %s' % e)
            return sources




    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return False


