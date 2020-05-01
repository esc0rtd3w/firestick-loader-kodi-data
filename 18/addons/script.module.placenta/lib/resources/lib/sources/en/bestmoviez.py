# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: Mr.Blamo

import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['best-moviez.ws']
        self.base_link = 'http://www.best-moviez.ws'
        self.search_link = '/?s=%s&submit=Search'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
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
            if url == None: return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            if debrid.status() == False: raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            posts = client.parseDOM(r, 'article', attrs={'id': 'post-\d+'})
            posts = client.parseDOM(posts, 'h1')
            posts = zip(client.parseDOM(posts, 'a', ret= 'href'),(client.parseDOM(posts, 'a', attrs={'rel': 'bookmark'})))

            for item in posts:

                try:
                    name = item[1]
                    name = client.replaceHTMLCodes(name)

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', name, re.I)

                    if not cleantitle.get(t) == cleantitle.get(title): raise Exception()

                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d+E\d+|S\d+)[\.|\)|\]|\s]', name, re.I)[-1].upper()

                    if not y == hdlr: raise Exception()

                    r = client.request(item[0], referer= self.base_link)
                    r = client.parseDOM(r, 'article', attrs={'id': 'post-\d+'})
                    #links = re.findall('>Single Links</b>(.+?)<p><b><span', data, re.DOTALL)
                    links = [i for i in client.parseDOM(r, 'p') if 'Single Links' in i]
                    links = zip(client.parseDOM(links, 'a', ret='href'),
                                client.parseDOM(links, 'a', attrs={'href': '.+?'}))

                    for item in links:
                        try:
                            quality, info = source_utils.get_release_quality(item[1], item[0])
                            try:
                                size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', r[0], re.DOTALL)[0].strip()
                                div = 1 if size.endswith(('GB', 'GiB')) else 1024
                                size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                                size = '%.2f GB' % size
                                info.append(size)
                            except:
                                pass

                            info = ' | '.join(info)

                            if any(x in item[0] for x in ['.rar', '.zip', '.iso']): raise Exception()
                            url = client.replaceHTMLCodes(item[0])
                            url = url.encode('utf-8')

                            hostDict = hostDict + hostprDict

                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if not valid: continue
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                            'info': info, 'direct': False, 'debridonly': True})
                        except:
                            pass

                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url


