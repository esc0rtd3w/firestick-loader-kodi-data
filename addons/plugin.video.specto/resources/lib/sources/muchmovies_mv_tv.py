# -*- coding: utf-8 -*-

'''
    Specto Add-on
    Copyright (C) 2016 mrknow

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

# TODO: Check gvideo resolving

import re,urllib,urlparse, json, hashlib
import base64
import random, string
import hashlib
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib import resolvers
from resources.lib.libraries import control
import requests




class source:
    def __init__(self):
        self.base_link = 'https://gomovies.to'
        #self.base_link_2 = 'https://123movies.net.ru'
        self.search_link = '/ajax/suggest_search?keyword=%s'
        self.search_link_2 = '/search?keyword=%s'
        self.info_link = '/ajax/movie_load_info/%s/'
        self.server_link = '/ajax/get_episodes/%s'
        self.direct_link = '/ajax/v2_load_episode/'
        self.embed_link = '/ajax/load_embed/'

        #http://123movies.to/ajax/suggest_search


    def request(self, url, post=None, headers=None, XHR=False):
        try:
            r = client.request(url, post=post, headers=headers, XHR=XHR, output='extended')

            if r[0] == None: return r

            if 'internetmatters.org' in r[0]:
                url = re.findall('(?://.+?|)(/.+)', url)[0]
                url = urlparse.urljoin(self.base_link, url)
                r = client.request(url, post=post, headers=headers, XHR=XHR, output='extended')

            return r
        except:
            return

    def get_movie(self, imdb, title, year):
        try:
            t = cleantitle.get(title)

            q = self.search_link_2 % (urllib.quote_plus(cleantitle.query(title)))
            q = urlparse.urljoin(self.base_link, q)


            r = self.request(q)[0]
            r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), client.parseDOM(i, 'a', ret='data-tip')) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if i[0] and i[1]]
            #else:
            #    r = zip(client.parseDOM(r, 'a', ret='href', attrs = {'class': 'ss-title'}), client.parseDOM(r, 'a', attrs = {'class': 'ss-title'}))

            r = [(i[0],i[2]) for i in r if cleantitle.get(t) == cleantitle.get(i[1])][:2]
            r = [(i[0], re.findall('(\d+)', i[1])[-1]) for i in r]

            for i in r:
                try:
                    y, q = cache.get(self.muchmovies_info, 9000, i[1])
                    if not y == year: raise Exception()
                    return urlparse.urlparse(i[0]).path
                except:
                    pass
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            t = cleantitle.get(data['tvshowtitle'])
            year = re.findall('(\d{4})', date)[0]
            years = [str(year), str(int(year)+1), str(int(year)-1)]
            season = '%01d' % int(season)
            episode = '%01d' % int(episode)

            q = self.search_link_2 % (urllib.quote_plus('%s-Season-%s' % (data['tvshowtitle'], season)))
            q = q.replace('+','-')

            q = urlparse.urljoin(self.base_link, q)


            r = self.request(q)[0]
            r = client.parseDOM(r, 'div', attrs = {'class': 'ml-item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title'), client.parseDOM(i, 'a', ret='data-url')) for i in r]
            r = [(i[0][0], i[1][0].split('- Season'), re.findall('(\d+)', i[2][0])[-1]) for i in r if i[0] and i[1]]
            r = [(i[0],i[1][0], i[1][1], i[2]) for i in r]



            r = [i for i in r if t == cleantitle.get(i[1])]
            r = [(i[0],i[3]) for i in r if season == '%01d' % int(i[2])][:2]

            for i in r:
                try:
                    y, q = cache.get(self.muchmovies_info, 9000, i[1])
                    if not y in years: raise Exception()
                    return urlparse.urlparse(i[0]).path + '?episode=%01d' % int(episode)
                except:
                    pass
        except:
            return

    def muchmovies_info(self, url):
        try:
            u = urlparse.urljoin(self.base_link, self.info_link)
            headers = {'Referer' : self.base_link}
            #https://123movieshd.tv/ajax/movie_load_info/11669/
            u = self.request(u % url, headers=headers,XHR=True)[0]

            q = client.parseDOM(u, 'div', attrs = {'class': 'jtip-quality'})[0]

            y = client.parseDOM(u, 'div', attrs = {'class': 'jt-info'})
            y = [i.strip() for i in y if i.strip().isdigit() and len(i.strip()) == 4][0]

            return (y, q)
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        #            for i in links: sources.append({'source': i['source'], 'quality': quality, 'provider': 'Muchmovies', 'url': i['url'] + head_link})
        try:
            sources = []

            if url == None: return sources

            if url.startswith('http'): self.base_link = url

            url = urlparse.urljoin(self.base_link, url)
            url = referer = url.replace('/watching.html', '')

            try: url, episode = re.findall('(.+?)\?episode=(\d*)$', url)[0]
            except: episode = None

            r = self.request(url+ '/watching.html')[0]
            vid_id = re.findall('name="movie_id" value="(\d+)"', r)[-1]

            quality = cache.get(self.muchmovies_info, 9000, vid_id)[1].lower()
            if quality == 'cam' or quality == 'ts': quality = 'CAM'
            elif quality == 'hd': quality = 'HD'
            else: quality = 'SD'


            try:
                headers = {'Referer': url}

                #u = urlparse.urljoin(self.base_link, self.server_link % vid_id)

                #r = self.request(u, headers=headers, XHR=True)[0]

                r = client.parseDOM(r, 'div', attrs={'id': 'list-eps'})[0]
                r = client.parseDOM(r, 'div', attrs={'class': 'les-content'})

                if episode != None:
                    #ep = episode
                    r = client.parseDOM(r, 'a', attrs={'episode-data': str(episode)}, ret='player-data')
                else:
                    r = client.parseDOM(r, 'a', ret='player-data')

                #r = [client.parseDOM(i, 'a', ret='player-data')[0] for i in r]

                links = []


                for link in r:
                    if '123movieshd' in link or 'seriesonline' in link:
                        r = client.request(link, timeout='10')
                        r = re.findall('(https:.*?redirector.*?)[\'\"]', r)

                        for i in r:
                            try:
                                sources.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'],
                                                'url': i, 'provider': 'Muchmovies'})
                            except:
                                pass
                    else:
                        try:
                            host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link.strip().lower()).netloc)[0]
                            if not host in hostDict: raise Exception()
                            host = client.replaceHTMLCodes(host)
                            host = host.encode('utf-8')

                            sources.append(
                                {'source': host, 'quality': 'SD', 'url': link, 'provider': 'Muchmovies'})
                        except:
                            pass

            except:
                pass

            return sources
        except:
            return sources

    def resolve(self, url):
        control.log('RESSS %s' % url)
        try:
            if 'openload.co' in url:
                url = resolvers.request(url)
                return url
            if 'movieshd' in url:
                r = self.request(url)[0]
                r = re.findall("file: '([^']+)',label: '(\d+)", r)
                r1 = sorted(r, key=lambda k: k[1])
                r2  = client.replaceHTMLCodes(r1[-1][0])
                #r2 = client.googlepass(url)
                return r2
            if 'seriesonline' in url:
                r = self.request(url)[0]
                r = [client.parseDOM(r, 'source', ret='src'), client.parseDOM(r,'source', ret='label')]
                r = zip(r[0],r[1])
                r1 = sorted(r, key=lambda k: k[1])
                r2  = client.replaceHTMLCodes(r1[-2][0])
                r2 = client.googlepass(url)
                return r2


            return False

        except Exception as e:
            control.log('RESSS %S' % e)
            pass

    def _updateParams(params):
        _myFun = None
        if _myFun == None:
            try:
                tmp = 'ZGVmIHphcmF6YShpbl9hYmMpOg0KICAgIGRlZiByaGV4KGEpOg0KICAgICAgICBoZXhfY2hyID0gJzAxMjM0NTY3ODlhYmNkZWYnDQogICAgICABiID0gZmYoYiwgYywgZCwgYSwgdGFiQlszXSwgMjIsIC0xMDQ0NTI1MzMwKTsN\rZGVmIHphcmF6YShwYXJhbXMpOg0KICAgIGRlZiBuKHQsIGUpOg0KICAgICAgICBuID0gMA0KICAgICAgICByID0gMA0KICAgICAgICBpID0gW10NCiAgICAgICAgZm9yIHMgaW4gcmFuZ2UoMCwgMjU2KToNCiAgICAgICAgICAgIGkuYXBwZW5kKHMpDQogICAgICAgIGZvciBzIGluIHJhbmdlKDAsIDI1Nik6DQogICAgICAgICAgICBuID0gKG4gKyBpW3NdICsgb3JkKHRbcyAlIGxlbih0KV0pKSAlIDI1Ng0KICAgICAgICAgICAgYSA9IGlbc10NCiAgICAgICAgICAgIGlbc10gPSBpW25dDQogICAgICAgICAgICBpW25dID0gYQ0KICAgICAgICBzID0gMA0KICAgICAgICBuID0gMCANCiAgICAgICAgZm9yIG8gaW4gcmFuZ2UobGVuKGUpKToNCiAgICAgICAgICAgIHMgPSAocysxKSAlIDI1Ng0KICAgICAgICAgICAgbiA9IChuICsgaVtzXSkgJSAyNTYNCiAgICAgICAgICAgIGEgPSBpW3NdDQogICAgICAgICAgICBpW3NdID0gaVtuXQ0KICAgICAgICAgICAgaVtuXSA9IGENCiAgICAgICAgICAgIHIgKz0gb3JkKGVbb10pIF4gaVsoaVtzXSArIGlbbl0pICUgMjU2XSAqIG8gKyBvDQogICAgICAgIHJldHVybiByDQogICAgaGFzaCA9IDANCiAgICBmb3Iga2V5IGluIHBhcmFtczoNCiAgICAgICAgaGFzaCArPSBuKHN0cihrZXkpLCBzdHIocGFyYW1zW2tleV0pKQ0KICAgIHBhcmFtcyA9IGRpY3QocGFyYW1zKQ0KICAgIHBhcmFtc1snXyddID0gaGFzaA0KICAgIHJldHVybiBwYXJhbXMNCg=='
                tmp = base64.b64decode(tmp.split('\r')[-1]).replace('\r', '')
                _myFun = compile(tmp, '', 'exec')
                vGlobals = {"__builtins__": None, 'len': len, 'dict': dict, 'list': list, 'ord': ord, 'range': range,
                            'str': str}
                vLocals = {'zaraza': ''}
                exec _myFun in vGlobals, vLocals
                _myFun = vLocals['zaraza']
            except Exception as e:
                print "Error", e
        try:
            params = _myFun(params)
        except Exception as e:
            print "Error", e
        return params