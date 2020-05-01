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

# TODO: get Hosts Dict from urlresolver2


import re,urllib,urlparse,base64

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control

from resources.lib import resolvers


class source:
    def __init__(self):
        self.base_link = 'http://www.watchfree.to'
        self.moviesearch_link = '/?keyword=%s&search_section=1'
        self.tvsearch_link = '/?keyword=%s&search_section=2'


    def get_movie(self, imdb, title, year):
        try:
            query = self.moviesearch_link % urllib.quote_plus(cleantitle.query(title))
            query = urlparse.urljoin(self.base_link, query)

            result = str(client.request(query, 'item'))
            if 'page=2' in result or 'page%3D2' in result: result += str(client.request(query + '&page=2', 'item'))

            result = client.parseDOM(result, 'div', attrs = {'class': 'item'})

            title = 'watch' + cleantitle.get(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]

            r = []
            for i in result:
                u = i[0]
                try: u = urlparse.parse_qs(urlparse.urlparse(u).query)['u'][0]
                except: pass
                try: u = urlparse.parse_qs(urlparse.urlparse(u).query)['q'][0]
                except: pass
                r += [(u, i[1])]

            match = [i[0] for i in r if title == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]

            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]
            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    r = client.request(urlparse.urljoin(self.base_link, i), 'link_ite')
                    if imdb in str(r): url = i ; break
                except:
                    pass

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            query = self.tvsearch_link % urllib.quote_plus(cleantitle.query(tvshowtitle))
            query = urlparse.urljoin(self.base_link, query)

            result = str(client.request(query, 'item'))
            if 'page=2' in result or 'page%3D2' in result: result += str(client.request(query + '&page=2', 'item'))

            result = client.parseDOM(result, 'div', attrs = {'class': 'item'})

            tvshowtitle = 'watch' + cleantitle.get(tvshowtitle)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i for i in result if any(x in i[1] for x in years)]
            print "Resu", result

            r = []
            for i in result:
                u = i[0]
                try: u = urlparse.parse_qs(urlparse.urlparse(u).query)['u'][0]
                except: pass
                try: u = urlparse.parse_qs(urlparse.urlparse(u).query)['q'][0]
                except: pass
                r += [(u, i[1])]
            match = [i[0] for i in r if tvshowtitle == cleantitle.get(i[1]) and '(%s)' % str(year) in i[1]]
            match2 = [i[0] for i in r]
            match2 = [x for y,x in enumerate(match2) if x not in match2[:y]]

            if match2 == []: return

            for i in match2[:5]:
                try:
                    if len(match) > 0: url = match[0] ; break
                    print "i",i
                    r = client.request(urlparse.urljoin(self.base_link, i), 'tv_episode_item')
                    print "r",imdb
                    print "r",r
                    if imdb in str(r):
                        url = i
                        break
                except:
                    pass

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            print "URL",url
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return

            url = urlparse.urljoin(self.base_link, url)

            result = client.request(url, 'tv_episode_item')
            result = client.parseDOM(result, 'div', attrs = {'class': 'tv_episode_item'})

            title = cleantitle.get(title)
            premiered = re.compile('(\d{4})-(\d{2})-(\d{2})').findall(date)[0]
            premiered = '%s %01d %s' % (premiered[1].replace('01','January').replace('02','February').replace('03','March').replace('04','April').replace('05','May').replace('06','June').replace('07','July').replace('08','August').replace('09','September').replace('10','October').replace('11','November').replace('12','December'), int(premiered[2]), premiered[0])

            result = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs = {'class': 'tv_episode_name'}), client.parseDOM(i, 'span', attrs = {'class': 'tv_num_versions'})) for i in result]
            result = [(i[0], i[1][0], i[2]) for i in result if len(i[1]) > 0] + [(i[0], None, i[2]) for i in result if len(i[1]) == 0]
            result = [(i[0], i[1], i[2][0]) for i in result if len(i[2]) > 0] + [(i[0], i[1], None) for i in result if len(i[2]) == 0]
            result = [(i[0][0], i[1], i[2]) for i in result if len(i[0]) > 0]

            url = [i for i in result if title == cleantitle.get(i[1]) and premiered == i[2]][:1]
            if len(url) == 0: url = [i for i in result if premiered == i[2]]
            if len(url) == 0 or len(url) > 1: url = [i for i in result if 'season-%01d-episode-%01d' % (int(season), int(episode)) in i[0]]

            url = client.replaceHTMLCodes(url[0][0])
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
            except: pass
            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        control.log('### WATCHFREE %s' %url)
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.request(url, 'link_ite')

            links = client.parseDOM(result, 'table', attrs = {'class': 'link_ite.+?'})
            print links
            for i in links:
                #control.log('### i %s' % i)

                try:
                    url = client.parseDOM(i, 'a', ret='href')
                    url = [x for x in url if 'gtfo' in x][-1]
                    print "URL", url
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['q'][0]
                    except: pass
                    url = urlparse.parse_qs(urlparse.urlparse(url).query)['gtfo'][0]
                    url = base64.b64decode(url)
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                    print "Host", host
                    if not host in hostDict: raise Exception()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    quality = client.parseDOM(i, 'div', attrs = {'class': 'quality'})
                    if any(x in ['[CAM]', '[TS]'] for x in quality): quality = 'CAM'
                    else:  quality = 'SD'
                    quality = quality.encode('utf-8')
                    sources.append({'source': host, 'quality': quality, 'provider': 'Watchfree', 'url': url})


                except:
                    pass

            return sources
        except Exception as e:
            control.log('ERROR Watchfree %s' % e)
            return sources


    def resolve(self, url):
        try:
            url = resolvers.request(url)
            return url
        except:
            return

