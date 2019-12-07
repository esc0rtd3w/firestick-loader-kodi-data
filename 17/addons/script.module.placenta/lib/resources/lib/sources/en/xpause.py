# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: MuadDib

import re,urllib,urlparse

from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['xpau.se']
        self.base_link = 'http://xpau.se/'
        self.watch_link = '/watch/%s'
        self.watch_series_link = '/watch/%s/s%s/e%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            url = {'imdb': imdb, 'title': data['title'], 'year': data['year'], 'season': season, 'episode': episode}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = (data['title'].translate(None, '\/:*?"\'<>|!,')).replace(' ', '-').replace('--', '-').lower()
            try:
                is_movie = not (int(data['episode']) > 0)
            except:
                is_movie = True

            if is_movie:
                url = urlparse.urljoin(self.base_link, self.watch_link % title)
            else:
                url = urlparse.urljoin(self.base_link, self.watch_series_link % (title, data['season'], data['episode']))

            r = client.request(url, output='geturl')

            if r is None: raise Exception()

            r = client.request(url)
            r = re.sub(r'[^\x00-\x7F]+',' ', r)
            result = r

            y = re.findall('Date\s*:\s*.+?>.+?(\d{4})', r)
            y = y[0] if len(y) > 0 else None

            if is_movie:
                if not (data['imdb'] in r or data['year'] == y): raise Exception()


            q = client.parseDOM(r, 'title')
            q = q[0] if len(q) > 0 else None

            quality = '1080p' if ' 1080' in q else 'HD'
            r = client.parseDOM(r, 'div', attrs = {'id': '5throw'})[0]
            r = client.parseDOM(r, 'a', ret='href', attrs = {'rel': 'nofollow'})

            links = []

            for url in r:
                try:
                    if 'yadi.sk' in url:
                        url = directstream.yandex(url)
                    elif 'mail.ru' in url:
                        url = directstream.cldmailru(url)
                    else:
                        raise Exception()

                    if url == None: raise Exception()
                    links += [{'source': 'cdn', 'url': url, 'quality': quality, 'direct': False}]
                except:
                    pass

            try:
                r = client.parseDOM(result, 'iframe', ret='src')
                if is_movie:
                    r = [i for i in r if 'pasmov' in i][0]
                else:
                    r = [i for i in r if 'pasep' in i][0]

                for i in range(0, 4):
                    try:
                        if not r.startswith('http'):
                            r = urlparse.urljoin(self.base_link, r)
                        r = client.request(r)
                        r = re.sub(r'[^\x00-\x7F]+',' ', r)
                        r = client.parseDOM(r, 'iframe', ret='src')[0]
                        if 'google' in r: break
                    except:
                        break

                if not 'google' in r: raise Exception()

                valid, hoster = source_utils.is_host_valid(r, hostDict)
                links, host, direct = source_utils.check_directstreams(r, hoster)

            except:
                pass

            for i in links:
                if 'google' in i['url']:
                    i['source'] = 'gvideo'
                    i['direct'] = False
                    
                sources.append({'source': i['source'], 'quality': i['quality'], 'language': 'en', 'url': i['url'], 'direct': i['direct'], 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url