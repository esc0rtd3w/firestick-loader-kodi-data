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


import re,urllib,urlparse,json,base64

from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['pubfilmno1.com', 'pubfilm.com', 'pidtv.com', 'pubfilm.ac']
        self.base_link = 'http://pubfilm.ac'
        self.moviesearch_link = '/%s-%s-full-hd-pubfilm-free.html'
        self.moviesearch_link_2 = '/%s-%s-pubfilm-free.html'
        self.tvsearch_link = '/wp-admin/admin-ajax.php'
        self.tvsearch_link_2 = '/?s=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = (title.translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()

            query = self.moviesearch_link % (title, year)
            query = urlparse.urljoin(self.base_link, query)

            for i in range(3):
                result = client.request(query, timeout='10')
                if not result == None: break

            if result == None:
                query = self.moviesearch_link_2 % (title, year)
                query = urlparse.urljoin(self.base_link, query)

                for i in range(3):
                    result = client.request(query, limit='5', timeout='10')
                    if not result == None: break

            if result == None:
                raise Exception()

            url = re.findall('(?://.+?|)(/.+)', query)[0]
            url = url.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            year = re.findall('(\d{4})', premiered)[0]
            season = '%01d' % int(season) ; episode = '%01d' % int(episode)
            tvshowtitle = '%s %s: Season %s' % (data['tvshowtitle'], year, season)

            url = cache.get(self.pidtv_tvcache, 120, tvshowtitle)

            if url == None: raise Exception()

            url += '?episode=%01d' % int(episode)
            url = url.encode('utf-8')
            return url
        except:
            return


    def pidtv_tvcache(self, tvshowtitle):
        try:
            post = urllib.urlencode({'aspp': tvshowtitle, 'action': 'ajaxsearchpro_search', 'options': 'qtranslate_lang=0&set_exactonly=checked&set_intitle=None&customset%5B%5D=post', 'asid': '5', 'asp_inst_id': '5_1'})
            url = urlparse.urljoin(self.base_link, self.tvsearch_link)
            for i in range(3):
                url = client.request(url, post=post, XHR=True, timeout='10')
                if not url == None: break
            url = zip(client.parseDOM(url, 'a', ret='href', attrs={'class': 'asp_res_url'}), client.parseDOM(url, 'a', attrs={'class': 'asp_res_url'}))
            url = [(i[0], re.findall('(.+?: Season \d+)', i[1].strip())) for i in url]
            url = [i[0] for i in url if len(i[1]) > 0 and tvshowtitle == i[1][0]][0]
            url = urlparse.urljoin(self.base_link, url)
            url = re.findall('(?://.+?|)(/.+)', url)[0]
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            content = re.compile('(.+?)\?episode=\d*$').findall(url)
            content = 'movie' if len(content) == 0 else 'episode'

            try: url, episode = re.compile('(.+?)\?episode=(\d*)$').findall(url)[0]
            except: pass

            for i in range(3):
                result = client.request(url, timeout='10')
                if not result == None: break
            result = result.replace('"target="EZWebPlayer"', '" target="EZWebPlayer"')
            url = zip(client.parseDOM(result, 'a', ret='href', attrs={'target': 'EZWebPlayer'}), client.parseDOM(result, 'a', attrs={'target': 'EZWebPlayer'}))
            url = [(i[0], re.compile('(\d+)').findall(i[1])) for i in url]
            url = [(i[0], i[1][-1]) for i in url if len(i[1]) > 0]

            if content == 'episode':
                url = [i for i in url if i[1] == '%01d' % int(episode)]

            links = [client.replaceHTMLCodes(i[0]) for i in url]


            for u in links:
                try:
                    for i in range(3):
                        result = client.request(u, timeout='10')
                        if not result == None: break
                    result = re.findall('sources\s*:\s*\[(.+?)\]', result)[0]
                    result = re.findall('"file"\s*:\s*"(.+?)"', result)

                    for url in result:
                        try:
                            url = url.replace('\\', '')
                            url = directstream.googletag(url)[0]
                            sources.append({'source': 'gvideo', 'quality': url['quality'], 'language': 'en', 'url': url['url'], 'direct': True, 'debridonly': False})
                        except:
                            pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


