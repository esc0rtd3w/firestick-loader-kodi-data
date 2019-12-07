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

import re,urllib,urlparse,json

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import cache
from resources.lib.libraries import control
from resources.lib.libraries import source_utils
from resources.lib.libraries import dom_parser



class source:
    def __init__(self):
        self.base_link = 'http://sezonlukdizi.net'
        self.search_link = '/js/dizi10.js'
        self.video_link = '/ajax/dataEmbed.asp'

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            #result = cache.get(self.sezonlukdizi_tvcache, 120)
            result = self.sezonlukdizi_tvcache()

            tvshowtitle = cleantitle.get(tvshowtitle)

            for i in result:
                print("I",i)

            result = [i[0] for i in result if tvshowtitle == cleantitle.get(i[1])]

            print result
            url = urlparse.urljoin(self.base_link, result[0])
            url = urlparse.urlparse(url).path
            url = client.replaceHTMLCodes(url)
            url = urlparse.urljoin('/diziler',url)
            url = url.encode('utf-8')
            return url
        except Exception as e:
            print("Error",e)
            return


    def sezonlukdizi_tvcache(self):
        try:
            url = urlparse.urljoin(self.base_link, self.search_link)

            result = client.request(url, redirect=False)

            if not result:
                r = client.request(self.base_link)
                r = dom_parser.parse_dom(r, 'script', attrs={'type': 'text/javascript', 'src': re.compile('.*/js/dizi.*')}, req='src')[0]
                url = urlparse.urljoin(self.base_link, r.attrs['src'])
                result = client.request(url)

            result = re.compile('{(.+?)}').findall(result)
            result = [(re.findall('u\s*:\s*(?:\'|\")(.+?)(?:\'|\")', i), re.findall('d\s*:\s*(?:\'|\")(.+?)(?:\',|\")', i)) for i in result]
            result = [(i[0][0], i[1][0]) for i in result if len(i[0]) > 0 and len(i[1]) > 0]
            result = [(re.compile('/diziler(/.+?)(?://|\.|$)').findall(i[0]), re.sub('&#\d*;', '', i[1])) for i in result]
            result = [(i[0][0] + '/', cleantitle.query(i[1])) for i in result if len(i[0]) > 0]

            return result
        except:
            return []


    def get_episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            url = '%s%01d-sezon-%01d-bolum.html' % (url.replace('.html', ''), int(season), int(episode))
            return source_utils.strip_domain(url)
        except:
            return []


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        #{'source': host, 'quality': i[1], 'provider': 'Sezonlukdizi', 'url': i[0]})
        sources = []

        try:
            if not url:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            result = client.request(url)
            result = re.sub(r'[^\x00-\x7F]+', ' ', result)

            pages = dom_parser.parse_dom(result, 'div', attrs={'class': 'item'}, req='data-id')
            pages = [i.attrs['data-id'] for i in pages]

            for page in pages:
                try:
                    url = urlparse.urljoin(self.base_link, self.video_link)

                    result = client.request(url, post={'id': page})
                    if not result: continue

                    url = dom_parser.parse_dom(result, 'iframe', req='src')[0].attrs['src']
                    if url.startswith('//'): url = 'http:' + url
                    if url.startswith('/'): url = urlparse.urljoin(self.base_link, url)

                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid: sources.append({'source': host, 'quality': 'HD', 'url': url,'provider': 'Sezonlukdizi'})

                    if '.asp' not in url: continue

                    result = client.request(url)

                    captions = re.search('kind\s*:\s*(?:\'|\")captions(?:\'|\")', result)
                    if not captions: continue

                    matches = [(match[0], match[1]) for match in re.findall('''["']?label\s*["']?\s*[:=]\s*["']?(?P<label>[^"',]+)["']?(?:[^}\]]+)["']?\s*file\s*["']?\s*[:=,]?\s*["'](?P<url>[^"']+)''', result, re.DOTALL | re.I)]
                    matches += [(match[1], match[0]) for match in re.findall('''["']?\s*file\s*["']?\s*[:=,]?\s*["'](?P<url>[^"']+)(?:[^}>\]]+)["']?\s*label\s*["']?\s*[:=]\s*["']?(?P<label>[^"',]+)''', result, re.DOTALL | re.I)]

                    result = [(source_utils.label_to_quality(x[0]), x[1].replace('\/', '/')) for x in matches]
                    result = [(i[0], i[1]) for i in result if not i[1].endswith('.vtt')]

                    for quality, url in result: sources.append({'source': 'gvideo', 'quality': quality, 'url': url, 'provider': 'Sezonlukdizi'})
                except:
                    pass

            return sources
        except Exception as e:
            control.log('ERROR sezonlukidz %s' % e)
            return sources


    def resolve(self, url):
        try:
            #url = client.request(url, output='geturl')
            if 'sezonlukdizi.com' in url: url = client.request(url, output='geturl')
            control.log('############ SEZONLUKIDZ res-0 %s' % url)
            url = client.request(url, output='geturl')
            # control.log('############ SEZONLUKIDZ res-1 %s' % url)
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            #else: url = url.replace('https://', 'http://')
            return url
        except:
            return


