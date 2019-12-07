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


import re,urllib,urlparse, time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client

from resources.lib.libraries import control

from resources.lib import resolvers





class source:
    def __init__(self):
        self.base_link = 'https://www.iwatchonline.cr'
        self.search_link = '/advance-search'
        self.show_link = '/tv-shows/%s'
        self.episode_link = '/episode/%s-s%02de%02d'
        self.headers = {}

    def get_movie(self, imdb, title, year):
        try:
            query = self.search_link
            post = {'searchquery': title, 'searchin': '1'}
            post = urllib.urlencode(post)
            result = ''

            headers = {"Content-Type":"application/x-www-form-urlencoded", "Referer":urlparse.urljoin(self.base_link, query)}
            result = client.request(urlparse.urljoin(self.base_link, query), post=post, headers=headers)
            #if 'widget search-page' in str(result): break
            print("R",result)
            result = client.parseDOM(result, 'div', attrs = {'class': 'widget search-page'})[0]
            result = client.parseDOM(result, 'td')

            title = cleantitle.movie(title)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(client.parseDOM(i, 'a', ret='href')[-1], client.parseDOM(i, 'a')[-1]) for i in result]
            result = [i for i in result if title == cleantitle.movie(i[1])]
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]

            url = client.replaceHTMLCodes(result)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            url = urlparse.urlparse(url).path
            url = url.encode('utf-8')
            return url
        except Exception as e:
            control.log("ERR iwatch %s" % e)
            return

    def get_show(self, imdb, tvdb, tvshowtitle, year):

        try:
            query = self.search_link
            post = {'searchquery': tvshowtitle, 'searchin': '2'}
            post = urllib.urlencode(post)

            result = ''
            links = [self.link_3]
            for base_link in links:
                headers = {'Referer': base_link+ "/advance-search"}

                result = client.request(urlparse.urljoin(base_link, query), post=post, headers=headers)
                if 'widget search-page' in str(result): break

            result = client.parseDOM(result, 'div', attrs = {'class': 'widget search-page'})[0]
            result = client.parseDOM(result, 'td')


            tvshowtitle = cleantitle.tv(tvshowtitle)
            years = ['(%s)' % str(year), '(%s)' % str(int(year)+1), '(%s)' % str(int(year)-1)]
            result = [(client.parseDOM(i, 'a', ret='href')[-1], client.parseDOM(i, 'a')[-1]) for i in result]
            result = [i for i in result if tvshowtitle == cleantitle.tv(i[1])]
            print "--!--"
            print result
            result = [i[0] for i in result if any(x in i[1] for x in years)][0]
            url = client.replaceHTMLCodes(result)
            try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
            except: pass
            url = urlparse.urlparse(url).path
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        if url == None: return

        url = url.rsplit('/', 1)[-1]
        url = self.episode_link % (url, int(season), int(episode))
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url

    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            self.sources = []
            mylinks = []
            if url == None: return []

            result = ''
            headers = {"Referer":urlparse.urljoin(self.base_link, url)}
            r100 = client.request(urlparse.urljoin(self.base_link, url), output='extended', headers=headers)
            cookie = r100[4] ; headers = r100[3] ; result = r100[0]


            links = client.parseDOM(result, 'tr', attrs = {'id': 'pt.+?'})

            for i in links:
                try:
                    lang = re.compile('<img src=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>]').findall(i)[1]

                    if not 'English' in lang: raise Exception()

                    host = re.compile('<img src=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>]').findall(i)[0]
                    host = host.split('/')[-1]
                    host = host.split('.')[-3]
                    host = host.strip().lower()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')

                    if '>Cam<' in i or '>TS<' in i: quality = 'CAM'
                    #elif '>HD<' in i and host in hostDict: quality = 'HD'
                    else: quality = 'SD'

                    #if quality == 'HD' and not host in hosthdDict: raise Exception()
                    #if quality == 'SD' and not host in hostDict: raise Exception()

                    if '>3D<' in i: info = '3D'
                    else: info = ''

                    url = re.compile('href=[\'|\"|\s|\<]*(.+?)[\'|\"|\s|\>]').findall(i)[0]
                    url = client.replaceHTMLCodes(url)

                    try: url = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
                    except: pass
                    if url.startswith('http'): url = urlparse.urlparse(url).path
                    if not url.startswith('http'): url = urlparse.urljoin(self.base_link, url)


                    url = url.encode('utf-8')
                    #control.log('########  IWATCH LINK url:%s  host:%s q:%s' % (url,host,quality))
                    self.sources.append(
                        {'source': host, 'quality': quality, 'provider': 'Iwatchonline', 'url': url})


                except:
                    pass
            #print("M",mylinks)
            #for i in mylinks:
            #    control.log(">>>>>>>>>>>>>>> ONE IWACH LINKS %s" % (i))

            #threads = []
            #for i in mylinks: threads.append(workers.Thread(self.check, i, headers, cookie,hostDict,hosthdDict))
            #[i.start() for i in threads]
            #for i in range(0, 10 * 2):
            #    is_alive = [x.is_alive() for x in threads]
            #    if all(x == False for x in is_alive): break
            #    time.sleep(0.5)

            return self.sources


        except Exception as e:
            control.log("ERR iwatch %s" % e)
            return []

    def check(self, i, headers, cookie, myhostDict, myhosthdDict):
        try:
            url = client.replaceHTMLCodes(i['url'])
            r = client.request(url, headers=headers, cookie=cookie, output='headers')
            url = r['Refresh'].replace('0;url=','')
            control.log('#%s'% url)
            host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]

            if host in myhostDict:
                self.sources.append({'source': i['source'], 'quality': i['quality'], 'provider': 'Iwatchonline', 'url': url})
        except:
            pass

    def resolve(self, url):
        try:
            r = client.request(url, output='headers')
            url = r['Refresh'].replace('0;url=','')
            #control.log('#%s'% url)
            url = resolvers.request(url)
            return url
        except:
            return

