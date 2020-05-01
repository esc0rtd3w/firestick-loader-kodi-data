# -*- coding: utf-8 -*-

'''
    Covenant Add-on
    Copyright (C) 2017 homik
    Based on MrKnow fanfilm addon

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


import re, urllib, urlparse

from resources.lib.modules import cleantitle, client

import HTMLParser

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['pl']
        self.domains = ['filmy.to']
        
        self.base_link = 'http://filmy.to'
        self.search_link = '/szukaj?q=%s'
        self.ajax_link = '/ajax/provision/%s'
        self.html_parser = HTMLParser.HTMLParser()


    def name_matches(self, given_name, names):
        for splitted_name in given_name.split('/'):
            simplified = cleantitle.get(splitted_name)
            for name in names:
                if name == simplified:
                    return True            
        return False
    
    
    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            query = self.search_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)
            result = client.request(query)
            result = client.parseDOM(result, 'div', attrs={'class': 'movie clearfix'})
            result = [(client.parseDOM(i, 'a', ret='href'),
                  client.parseDOM(i, 'span', attrs={'class': 'title-pl'}),
                  client.parseDOM(i, 'span', attrs={'class': 'title-en'}),
                  client.parseDOM(i, 'img', ret='src'),
                  client.parseDOM(i, 'p'),
                  client.parseDOM(i, 'p', attrs={'class': 'plot'})) for i in result ]

            result = [(i[0][0], u" ".join(i[1] + i[2]), re.findall('(\d{4})', i[4][0])) for i in result]
                          
            names = [cleantitle.get(i) for i in [title, localtitle]]

            result = [i for i in result if self.name_matches(i[1], names)]
            years = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1)]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]


            try: url = re.compile('//.+?(/.+)').findall(result)[0]
            except: url = result
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except :
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            query = self.search_link % (urllib.quote_plus(tvshowtitle))
            query = urlparse.urljoin(self.base_link, query)
            result = client.request(query)
            result = client.parseDOM(result, 'div', attrs={'class': 'movie clearfix'})
            result = [(client.parseDOM(i, 'a', ret='href'),
                  client.parseDOM(i, 'span', attrs={'class': 'title-pl'}),
                  client.parseDOM(i, 'span', attrs={'class': 'title-en'}),
                  client.parseDOM(i, 'img', ret='src'),
                  client.parseDOM(i, 'p'),
                  client.parseDOM(i, 'p', attrs={'class': 'plot'})) for i in result ]

            result = [(i[0][0], u" ".join(i[1] + i[2]), re.findall('(\d{4})', i[4][0])) for i in result]
            result = [i for i in result if 'serial' in i[0]]
            names = [cleantitle.get(i) for i in [tvshowtitle, localtvshowtitle]]
            result = [i for i in result if self.name_matches(i[1], names)]
            years = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1)]
            result = [i[0] for i in result if any(x in i[2] for x in years)][0]
            url = result
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.urljoin(self.base_link, url)
            result = client.request(url)
            result = client.parseDOM(result, 'select', attrs={'id': 'sezon'})[0]
            sezons = client.parseDOM(result, 'option')
            urls = client.parseDOM(result, 'option', ret='value')
            
            index = sezons.index("Sezon " + season);
            
            seasonUrl = urlparse.urljoin(self.base_link, urls[index])          
            result = client.request(seasonUrl)
            result = client.parseDOM(result, 'div', attrs={'class': 'episodeLinks'})[0]
            epUrls = client.parseDOM(result, 'a', ret='href')
            rows = client.parseDOM(result, 'a')
            for row in rows:
                episodeNo = client.parseDOM(row, 'span')[0]
                episodeNo = episodeNo[:-1]
                if episodeNo == episode:
                    return epUrls[rows.index(row)]                                 
        except:
            return

    def get_lang_by_type(self, lang_type):
        if lang_type == 'Lektor PL':
            return 'pl', 'Lektor'
        if lang_type == 'Dubbing PL': 
            return 'pl', 'Dubbing'
        if lang_type == 'Napisy PL':
            return 'pl', 'Napisy'
        if lang_type == 'Film polski': 
            return 'pl', None
        return 'en', None
    
    def sources(self, url, hostDict, hostprDict):
        try:

            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            h = {'User-Agent': client.randomagent()}
            
            result = client.request(url, output='extended', headers=h)
            cookie = result[4]
            ajax_prov = client.parseDOM(result[0], 'meta', attrs={'property': 'provision'}, ret='content')[0]
            
            ajax_url = urlparse.urljoin(self.base_link, self.ajax_link) % ajax_prov
            h['X-CSRFToken'] = re.findall ('csrftoken=(.*?);', cookie)[0]
            result = client.request(ajax_url, cookie=cookie, XHR=True, headers=h)
            
            r = client.parseDOM(result, 'div', attrs={'class':'host-container pull-left'})
            r = [(client.parseDOM(i, 'div', attrs={'class': 'url'}, ret='data-url'),
                  client.parseDOM(i, 'span', attrs={'class':'label label-default'}),
                  client.parseDOM(i, 'img', attrs={'class': 'ttip'}, ret='title'),
                  client.parseDOM(i, 'span', attrs={'class': 'glyphicon glyphicon-hd-video ttip'}, ret='title'),
                  ) for i in r]

            r = [(self.html_parser.unescape(i[0][0]), i[1][0], i[2][0], len(i[3]) > 0) for i in r]
            r = [(client.parseDOM(i[0], 'iframe', ret='src'), i[1], i[2], i[3]) for i in r]
            r = [(i[0][0], i[1], i[2], i[3]) for i in r if len(i[0]) > 0]

            for i in r:
                try:

                    host = urlparse.urlparse(i[0]).netloc
                    host = host.replace('www.', '').replace('embed.', '')
                    host = host.lower()
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    lang, info = self.get_lang_by_type(i[1])

                    q = 'SD'
                    if 'Wysoka' in i[2]: q = 'HD'
                    if i[3] == True: q = '1080p'

                    sources.append({'source': host, 'quality': q, 'language': lang, 'url': i[0], 'info': info, 'direct': False, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        return url;
