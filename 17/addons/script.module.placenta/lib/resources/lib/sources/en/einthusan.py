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


import re,urllib,urllib2,urlparse,json

from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['einthusan.com', 'einthusan.tv']
        self.base_link = 'https://einthusan.tv'
        self.search_link = '/movie/results/?lang=%s&query=%s'
        self.movie_link = '/movie/watch/%s/'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            langMap = {'hi':'hindi', 'ta':'tamil', 'te':'telugu', 'ml':'malayalam', 'kn':'kannada', 'bn':'bengali', 'mr':'marathi', 'pa':'punjabi'}

            lang = 'http://www.imdb.com/title/%s/' % imdb
            lang = client.request(lang)
            lang = re.findall('href\s*=\s*[\'|\"](.+?)[\'|\"]', lang)
            lang = [i for i in lang if 'primary_language' in i]
            lang = [urlparse.parse_qs(urlparse.urlparse(i).query) for i in lang]
            lang = [i['primary_language'] for i in lang if 'primary_language' in i]
            lang = langMap[lang[0][0]]

            q = self.search_link % (lang, urllib.quote_plus(title))
            q = urlparse.urljoin(self.base_link, q)

            t = cleantitle.get(title)

            r = client.request(q)

            r = client.parseDOM(r, 'li')
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'h3'), client.parseDOM(i, 'div', attrs = {'class': 'info'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if i[0] and i[1] and i[2]]
            r = [(re.findall('(\d+)', i[0]), i[1], re.findall('(\d{4})', i[2])) for i in r]
            r = [(i[0][0], i[1], i[2][0]) for i in r if i[0] and i[2]]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]

            url = str(r)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = self.movie_link % url
            url = urlparse.urljoin(self.base_link, url)

            return sources

            r = client.request(url)

            sources.append({'source': 'einthusan', 'quality': 'HD', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


