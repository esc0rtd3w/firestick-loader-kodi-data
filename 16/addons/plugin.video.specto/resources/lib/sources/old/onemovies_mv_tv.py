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


import re,urllib,urlparse, json, time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control

class source:
    def __init__(self):
        self.base_link = 'http://1movies.tv'
        self.search_link = '/movies/search?s=%s'
        self.episode_link = '/ajax/movie/load_episodes_v2?id=%s&episode_id=%s&link_id=%s&_=%s'
        self.load_player = '/ajax/movie/load_player_v3'

    def now_milliseconds(self):
        return int(time.time() * 1000)

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link % urllib.quote(title)
            query = urlparse.urljoin(self.base_link, query)
            result = client.request(query)
            title = cleantitle.movie(title)
            years = ['%s' % str(year), '%s' % str(int(year)+1), '%s' % str(int(year)-1)]
            r = client.parseDOM(result, 'div', attrs = {'class': 'item_movie'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][-1]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(re.sub('//.+?/','', i[0]), i[1], re.findall('(\d{4})', i[1])[0] ) for i in r]
            r = [i for i in r if any(x in i[1] for x in years)]
            r = [i for i in r if title in cleantitle.movie(i[1])]

            u = [i[0] for i in r][0]
            url = urlparse.urljoin(self.base_link, '/'+ u)
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')

            return url
        except:
            return


    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return None


    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'],  url['season'], url['episode'], url['premiered'] = title, season, episode, date
            url = urllib.urlencode(url)
            return url
        except:
            return

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        sources = []
        try:
            #control.log("one-url-0 %s" % url)

            if url == None: return sources

            if not str(url).startswith('/'):
                data = urlparse.parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
                #control.log("# DATA %s" % data)

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
                #control.log("one-date-TITLE %s" % title)
                sezon = data['season']
                episode = data['episode']
                year = re.findall('(\d{4})', data['premiered'])[0] if 'tvshowtitle' in data else data['year']
                tvtitle = '%s - Season %s' % (title, sezon)
                query = self.search_link % urllib.quote(tvtitle)
                query = urlparse.urljoin(self.base_link, query)

                result = client.request(query)
                #control.log("one-date-0 %s" % year)
                tvshowtitle = cleantitle.tv(title)
                years = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1)]

                r = client.parseDOM(result, 'div', attrs={'class': 'item_movie'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][-1]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
                r = [(re.sub('//.+?/', '', i[0]), i[1], re.findall('(\d{4})', i[1])[0]) for i in r]
                r = [(i[0], i[1].split('-')[0].strip(), i[2]) for i in r]
                r = [i for i in r if tvshowtitle == cleantitle.tv(i[1])]
                r = [i for i in r if any(x in i[2] for x in years)]

                u = [i[0] for i in r][0]
                url = urlparse.urljoin(self.base_link, '/' + u)
                result = client.request(url)

                result = client.parseDOM(result, 'div', attrs={'class': 'ep_link full'})[0]
                r = [client.parseDOM(result, 'a', ret='href'), client.parseDOM(result, 'a')]
                #control.log("one-epis-2 %s" % result)
                r = [(r[0][idx],r[1][idx]) for idx,i in enumerate(r[0])]
                r = [(i[0], re.findall('\d+',i[1])[0]) for i in r]
                #control.log("one-epis-3 %s" % r)
                u = [i[0] for i in r if i[1] == episode][0]

                #control.log("one-epis-0 %s" % u)
                url = 'http:' + u
                url = client.replaceHTMLCodes(url)
                #control.log("one-epis-0 %s" % url)

                url = url.encode('utf-8')

            ref = urlparse.urljoin(self.base_link, url)
            #control.log("one-sources-0 %s" % ref)
            headers= {'Referer':ref, "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"}
            r100 = client.request(ref,headers=headers, output='extended')
            cookie = r100[4] ; headers = r100[3] ; result = r100[0]


            r = re.compile('load_player\((\d+)\);', ).findall(result)
            if len(r) > 0:
                t = urlparse.urljoin(self.base_link, self.load_player)
                headers['x-requested-with'] = "XMLHttpRequest"
                headers['cookie']=cookie
                headers['Referer'] = ref
                post = urllib.urlencode({'id':r[0]})

                r1= client.request(t, headers=headers, post=post)
                r1 = json.loads(r1)
                r1 = client.request('http:'+r1['value'], headers=headers)
                r1 = json.loads(r1)

                for i in r1['playlist'][0]['sources']:
                    try:
                        sources.append({'source': 'gvideo', 'quality': client.googletag(i['file'])[0]['quality'],
                                                'provider': 'OneMovies', 'url': i['file']})

                        #sources.append({'source': 'gvideo', 'quality': client.googletag(i)[0]['quality'], 'provider': 'Rainierland', 'url': i})
                    except:
                        pass
                return sources

        except Exception as e:
            control.log('ERROR onemovies %s' % e)
            return sources

    def resolve(self, url):
        #control.log("rainierland-sources-0 @@@@@@@@@@@@@@@@@@@@@@@@@@@@ %s" % url)

        try:
            return url
        except:
            pass

