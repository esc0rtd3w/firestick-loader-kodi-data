'''
    Exodus Add-on
    Copyright (C) 2017 Exodus

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
import re
import urllib
import urlparse
import json
import xbmc

from resources.lib.modules import client, cleantitle, directstream
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        '''
        Constructor defines instances variables

        '''
        self.priority = 0
        self.language = ['en']
        self.domains = ['putlocker.rs', 'putlockertv.to', 'putlockertv.se']
        self.base_link = 'https://putlockertv.se'
        self.movie_search_path = ('/search?keyword=%s')
        self.episode_search_path = ('/filter?keyword=%s&sort=post_date:Adesc'
                                    '&type[]=series')
        self.film_path = '/watch/%s'
        self.info_path = '/ajax/episode/info?ts=%s&_=%s&id=%s&update=0'
        self.grabber_path = '/grabber-api/?ts=%s&id=%s&token=%s&mobile=0'

    def movie(self, imdb, title, localtitle, aliases, year):
        '''
        Takes movie information and returns a set name value pairs, encoded as
        url params. These params include ts
        (a unqiue identifier, used to grab sources) and list of source ids

        Keyword arguments:

        imdb -- string - imdb movie id
        title -- string - name of the movie
        localtitle -- string - regional title of the movie
        year -- string - year the movie was released

        Returns:

        url -- string - url encoded params

        '''
        try:
            clean_title = cleantitle.geturl(title)
            query = (self.movie_search_path % (clean_title))
            url = urlparse.urljoin(self.base_link, query)

            search_response = client.request(url)

            results_list = client.parseDOM(
                search_response, 'div', attrs={'class': 'item'})[0]
            film_id = re.findall('(\/watch\/)([^\"]*)', results_list)[0][1]

            query = (self.film_path % film_id)
            url = urlparse.urljoin(self.base_link, query)

            film_response = client.request(url)

            ts = re.findall('(data-ts=\")(.*?)(\">)', film_response)[0][1]

            sources_dom_list = client.parseDOM(
                film_response, 'ul', attrs={'class': 'episodes range active'})
            sources_list = []

            for i in sources_dom_list:
                source_id = re.findall('([\/])(.{0,6})(\">)', i)[0][1]
                sources_list.append(source_id)

            data = {
                'imdb': imdb,
                'title': title,
                'localtitle': localtitle,
                'year': year,
                'ts': ts,
                'sources': sources_list
            }
            url = urllib.urlencode(data)

            return url

        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        '''
        Takes TV show information, encodes it as name value pairs, and returns
        a string of url params

        Keyword arguments:

        imdb -- string - imdb tv show id
        tvdb -- string - tvdb tv show id
        tvshowtitle -- string - name of the tv show
        localtvshowtitle -- string - regional title of the tv show
        year -- string - year the movie was released

        Returns:

        url -- string - url encoded params

        '''
        try:
            data = {
                'imdb': imdb,
                'tvdb': tvdb,
                'tvshowtitle': tvshowtitle,
                'year': year
            }
            url = urllib.urlencode(data)

            return url

        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        '''
        Takes episode information, finds the ts and list sources, encodes it as
        name value pairs, and returns a string of url params

        Keyword arguments:

        url -- string - url params
        imdb -- string - imdb tv show id
        tvdb -- string - tvdb tv show id
        title -- string - episode title
        premiered -- string - date the episode aired (format: year-month-day)
        season -- string - the episodes season
        episode -- string - the episode number

        Returns:

        url -- string - url encoded params

        '''
        try:
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)

            clean_title = cleantitle.geturl(data['tvshowtitle'])
            query = (self.movie_search_path % clean_title)
            url = urlparse.urljoin(self.base_link, query)

            search_response = client.request(url)

            results_list = client.parseDOM(
                search_response, 'div', attrs={'class': 'items'})[0]

            film_id = []

            film_tries = [
             '\/' + (clean_title + '-0' + season) + '[^-0-9](.+?)\"',
             '\/' + (clean_title + '-' + season) + '[^-0-9](.+?)\"',
             '\/' + clean_title + '[^-0-9](.+?)\"'
             ]

            for i in range(len(film_tries)):
                if not film_id:
                    film_id = re.findall(film_tries[i], results_list)
                else:
                    break

            film_id = film_id[0]

            query = (self.film_path % film_id)
            url = urlparse.urljoin(self.base_link, query)

            film_response = client.request(url)

            ts = re.findall('(data-ts=\")(.*?)(\">)', film_response)[0][1]

            sources_dom_list = client.parseDOM(
                film_response, 'ul', attrs={'class': 'episodes range active'})

            if not re.findall(
             '([^\/]*)\">' + episode + '[^0-9]', sources_dom_list[0]):
                episode = '%02d' % int(episode)

            sources_list = []

            for i in sources_dom_list:
                source_id = re.findall(
                    ('([^\/]*)\">' + episode + '[^0-9]'), i)[0]
                sources_list.append(source_id)

            data.update({
                'title': title,
                'premiered': premiered,
                'season': season,
                'episode': episode,
                'ts': ts,
                'sources': sources_list
            })

            url = urllib.urlencode(data)

            return url

        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        '''
        Loops over site sources and returns a dictionary with corresponding
        file locker sources and information

        Keyword arguments:

        url -- string - url params

        Returns:

        sources -- string - a dictionary of source information

        '''

        sources = []

        try:
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)
            data['sources'] = re.findall("[^', u\]\[]+", data['sources'])

            for i in data['sources']:
                token = str(self.__token(
                    {'id': i, 'update': 0, 'ts': data['ts']}))
                query = (self.info_path % (data['ts'], token, i))
                url = urlparse.urljoin(self.base_link, query)
                info_response = client.request(url, XHR=True)
                grabber_dict = json.loads(info_response)

                try:
                    if grabber_dict['type'] == 'direct':
                        token64 = grabber_dict['params']['token']
                        query = (self.grabber_path % (data['ts'], i, token64))
                        url = urlparse.urljoin(self.base_link, query)

                        response = client.request(url, XHR=True)

                        sources_list = json.loads(response)['data']

                        for j in sources_list:

                            quality = j['label'] if not j['label'] == '' else 'SD'
                            quality = source_utils.label_to_quality(quality)

                            if 'googleapis' in j['file']:
                                sources.append({'source': 'GVIDEO', 'quality': quality, 'language': 'en', 'url': j['file'], 'direct': True, 'debridonly': False})
                                continue

                            valid, hoster = source_utils.is_host_valid(j['file'], hostDict)
                            urls, host, direct = source_utils.check_directstreams(j['file'], hoster)
                            for x in urls:
                                sources.append({
                                    'source': 'gvideo',
                                    'quality': quality,
                                    'language': 'en',
                                    'url': x['url'],
                                    'direct': True,
                                    'debridonly': False
                                })

                    elif not grabber_dict['target'] == '':
                        url = 'https:' + grabber_dict['target'] if not grabber_dict['target'].startswith('http') else grabber_dict['target']
                        valid, hoster = source_utils.is_host_valid(url, hostDict)
                        if not valid: continue
                        urls, host, direct = source_utils.check_directstreams(url, hoster)
                        url = urls[0]['url']

                        if 'cloud.to' in host:
                            headers = {
                                'Referer': self.base_link
                            }
                            url = url + source_utils.append_headers(headers)

                        sources.append({
                            'source': hoster,
                            'quality': urls[0]['quality'],
                            'language': 'en',
                            'url': url,
                            'direct': False,
                            'debridonly': False
                        })
                except: pass

            return sources

        except Exception:
            return sources

    def resolve(self, url):
        '''
        Takes a scraped url and returns a properly formatted url

        Keyword arguments:

        url -- string - source scraped url

        Returns:

        url -- string - a properly formatted url

        '''
        try:
            if not url.startswith('http'):
                url = 'http:' + url

            for i in range(3):
                if 'google' in url and not 'googleapis' in url:
                    url = directstream.googlepass(url)

                if url:
                    break

            return url

        except Exception:
            return

    def __token(self, d):
        '''
        Takes a dictionary containing id, update, and ts, then returns a
        token which is used by info_path to retrieve grabber api
        information

        Keyword arguments:

        d -- dictionary - containing id, update, ts

        Returns:

        token -- integer - a unique integer

        '''
        try:
            token = 0

            for s in d:

                o = 0
                r = 0
                i = [i for i in range(0, 256)]
                n = 0
                a = 0
                j = s
                e = str(d[s])

                for t in range(0, 256):
                    n = (n + i[t] + ord(j[t % len(j)])) % 256

                    r = i[t]
                    i[t] = i[n]
                    i[n] = r

                s = 0
                n = 0

                for o in range(len(e)):
                    s = (s + 1) % 256
                    n = (n + i[s]) % 256

                    r = i[s]
                    i[s] = i[n]
                    i[n] = r

                    a += ord(e[o]) ^ i[(i[s] + i[n]) % 256] * o + o

                token += a

            return token

        except Exception:
            return 0
