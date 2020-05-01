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


import re,urllib,urlparse,json,base64,time

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watch5s.to', 'watch5s.is', 'watch5s.rs']
        self.base_link = 'https://watch5s.rs'
        self.search_link = '/search?q=%s'
        self.token_link = 'https://play.watch5s.to/token.php'
        self.token_v2_link = 'https://play.watch5s.to/token_v2.php?&eid=%s&mid=%s&_=%s'
        self.grabber_link = 'https://play.watch5s.to/grabber-api-v2/episode/%s?hash=%s&token=%s&_=%s'
        self.backup_token_link = 'https://play.watch5s.to/embed/go?type=token&eid=%s&mid=%s&_=%s'
        self.backup_link = 'https://play.watch5s.to/embed/go?type=sources&eid=%s&x=%s&y=%s'
        self.backup_token_link_v2 = 'https://embed.streamdor.co/?type=token&eid=%s&mid=%s&_=%s'
        self.backup_link_v2 = 'https://embed.streamdor.co/?type=sources&eid=%s&x=%s&y=%s'

    def matchAlias(self, title, aliases):
        try:
            for alias in aliases:
                if cleantitle.get(title) == cleantitle.get(alias['title']):
                    return True
        except:
            return False

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
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

    def searchShow(self, title, season, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            search = '%s Season %01d' % (title, int(season))
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.getsearch(search)))
            r = client.request(url, headers=headers, timeout='15')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            r = [(i[0], i[1], re.findall('(.*?)\s+-\s+Season\s+(\d)', i[1])) for i in r]
            r = [(i[0], i[1], i[2][0]) for i in r if len(i[2]) > 0]
            url = [i[0] for i in r if self.matchAlias(i[2][0], aliases) and i[2][1] == season][0]
            url = '%s/watch/' % url
            return url
        except:
            return

    def searchMovie(self, title, year, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.getsearch(title)))
            r = client.request(url, headers=headers, timeout='15')
            r = client.parseDOM(r, 'div', attrs={'class': 'ml-item'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a', ret='title'))
            results = [(i[0], i[1], re.findall('\((\d{4})', i[1])) for i in r]
            try:
                r = [(i[0], i[1], i[2][0]) for i in results if len(i[2]) > 0]
                url = [i[0] for i in r if self.matchAlias(i[1], aliases) and (year == i[2])][0]
            except:
                url = None
                pass

            if (url == None):
                url = [i[0] for i in results if self.matchAlias(i[1], aliases)][0]
            url = '%s/watch/' % url
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            headers = {}

            if 'tvshowtitle' in data:
                year = re.compile('(\d{4})-(\d{2})-(\d{2})').findall(data['premiered'])[0][0]
                episode = '%01d' % int(data['episode'])
                url = '%s/tv-series/%s-season-%01d/watch/' % (self.base_link, cleantitle.geturl(data['tvshowtitle']), int(data['season']))
                url = client.request(url, headers=headers, timeout='10', output='geturl')

                if url == None:
                    url = self.searchShow(data['tvshowtitle'], data['season'], aliases, headers)

            else:
                episode = None
                year = data['year']
                url = self.searchMovie(data['title'], data['year'], aliases, headers)

            referer = url
            r = client.request(url, headers=headers)

            y = re.findall('Release\s*:\s*.+?\s*(\d{4})', r)[0]

            if not year == y: raise Exception()


            r = client.parseDOM(r, 'div', attrs = {'class': 'les-content'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a'))
            r = [(i[0], ''.join(re.findall('(\d+)', i[1])[:1])) for i in r]

            if not episode == None:
                r = [i[0] for i in r if '%01d' % int(i[1]) == episode]
            else:
                r = [i[0] for i in r]

            r = [i for i in r if '/server-' in i]

            for u in r:
                try:
                    p = client.request(u, headers=headers, referer=referer, timeout='10')

                    t = re.findall('player_type\s*:\s*"(.+?)"', p)[0]
                    if t == 'embed': raise Exception()

                    headers = {'Origin': self.base_link}
                    eid = client.parseDOM(p, 'input', ret='value', attrs = {'name': 'episodeID'})[0].encode('utf-8')
                    r = client.request(self.token_link, post=urllib.urlencode({'id': eid}), headers=headers, referer=referer, timeout='10', XHR=True)
                    isV2 = False

                    try:
                        js = json.loads(r)
                        hash = js['hash']
                        token = js['token']
                        _ = js['_']
                        url = self.grabber_link % (eid, hash, token, _)
                        u = client.request(url, headers=headers, referer=referer, timeout='10', XHR=True)
                        js = json.loads(u)
                    except:
                        isV2 = True
                        pass

                    if isV2:
                        mid = re.compile('.?id:\s+"(\d+)"').findall(p)[0].encode('utf-8')
                        timestamp = str(int(time.time() * 1000))
                        url = self.token_v2_link % (eid, mid, timestamp)
                        script = client.request(url, headers=headers, referer=referer, timeout='10', XHR=True)
                        script = self.aadecode(script)
                        if 'hash' in script and 'token' in script:
                            hash = re.search('''hash\s+=\s+['"]([^"']+)''', script).group(1).encode('utf-8')
                            token = re.search('''token\s+=\s+['"]([^"']+)''', script).group(1).encode('utf-8')
                            _ = re.search('''_\s+=\s+['"]([^"']+)''', script).group(1).encode('utf-8')
                            url = self.grabber_link % (eid, hash, token, _)
                            u = client.request(url, headers=headers, referer=referer, timeout='10', XHR=True)
                            js = json.loads(u)


                    try:
                        u = js['playlist'][0]['sources']
                        u = [i['file'] for i in u if 'file' in i]

                        for i in u:
                            try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                            except: pass
                    except:
                        pass

                    try:
                        u = js['backup']
                        u = urlparse.parse_qs(urlparse.urlsplit(u).query)
                        u = dict([(i, u[i][0]) if u[i] else (i, '') for i in u])
                        eid = u['eid']
                        mid = u['mid']

                        if isV2:
                            p = client.request(self.backup_token_link_v2 % (eid, mid, _), XHR=True, referer=referer, timeout='10')
                            x = re.search('''_x=['"]([^"']+)''', p).group(1)
                            y = re.search('''_y=['"]([^"']+)''', p).group(1)
                            u = client.request(self.backup_link_v2 % (eid, x, y), referer=referer, XHR=True, timeout='10')
                            js = json.loads(u)
                        else:
                            p = client.request(self.backup_token_link % (eid, mid, _), XHR=True, referer=referer, timeout='10')
                            x = re.search('''_x=['"]([^"']+)''', p).group(1)
                            y = re.search('''_y=['"]([^"']+)''', p).group(1)
                            u = client.request(self.backup_link % (eid, x, y), referer=referer, XHR=True, timeout='10')
                            js = json.loads(u)

                        try:
                            u = js['playlist'][0]['sources']
                            u = [i['file'] for i in u if 'file' in i]

                            for i in u:
                                try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                                except: pass
                        except:
                            pass
                    except:
                        pass

                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return directstream.googlepass(url)


    def aadecode(self, text):
        text = re.sub(r"\s+|/\*.*?\*/", "", text)
        data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
        chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]

        txt = ""
        for char in chars:
            char = char \
                .replace("(oﾟｰﾟo)", "u") \
                .replace("c", "0") \
                .replace("(ﾟДﾟ)['0']", "c") \
                .replace("ﾟΘﾟ", "1") \
                .replace("!+[]", "1") \
                .replace("-~", "1+") \
                .replace("o", "3") \
                .replace("_", "3") \
                .replace("ﾟｰﾟ", "4") \
                .replace("(+", "(")
            char = re.sub(r'\((\d)\)', r'\1', char)

            c = ""
            subchar = ""
            for v in char:
                c += v
                try:
                    x = c
                    subchar += str(eval(x))
                    c = ""
                except:
                    pass
            if subchar != '': txt += subchar + "|"
        txt = txt[:-1].replace('+', '')

        txt_result = "".join([chr(int(n, 8)) for n in txt.split('|')])

        return txt_result
