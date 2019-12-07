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


import re,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import dom_parser2

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['icefilms.is']
        self.base_link = 'https://icefilms.is'
        self.search_link_movie = '/newmov.php?menu=search&query=%s'
        self.search_link_show = 'show/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title)
            search_url = urlparse.urljoin(self.base_link, self.search_link_movie % clean_title.replace('-','+'))
            r = cache.get(client.request, 6, search_url)
            r = dom_parser2.parse_dom(r, 'div', {'class': 'movie'})
            r = [(dom_parser2.parse_dom(i.content, 'a', req='href'), \
                  dom_parser2.parse_dom(i.content, 'div', {'class': 'year'})) \
                  for i in r]
            r = [(urlparse.urljoin(self.base_link, i[0][0].attrs['href']), i[1][0].content) for i in r if i[1][0].content == year]
            url = r[0][0]
            return url
        except Exception:
            return
            
    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(tvshowtitle)
            url = urlparse.urljoin(self.base_link, self.search_link_show % clean_title + '/')
            return url
        except Exception:
            return
            
    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            print url
            url = urlparse.urljoin(url, 'season/%s/episode/%s' % (season, episode))
            print url
            return url
        except Exception:
            return
            
    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []          
            r = cache.get(client.request, 6, url)
            try:
                v = re.findall('\$\.get\(\'(.+?)(?:\'\,\s*\{\"embed\":\")([\d]+)', r)
                for i in v:
                    url = urlparse.urljoin(self.base_link, i[0] + '?embed=%s' % i[1])
                    ri = cache.get(client.request, 6, search_url)
                    url = dom_parser2.parse_dom(ri, 'iframe', req='src')[0]
                    url = url.attrs['src']
                    try:
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                        if host in hostDict:
                            host = client.replaceHTMLCodes(host)
                            host = host.encode('utf-8')
                            sources.append({
                                'source': host,
                                'quality': 'SD',
                                'language': 'en',
                                'url': url.replace('\/','/'),
                                'direct': False,
                                'debridonly': False
                            })
                    except: pass
            except: pass
            r = dom_parser2.parse_dom(r, 'div', {'class': ['btn','btn-primary']})
            r = [dom_parser2.parse_dom(i.content, 'a', req='href') for i in r]
            r = [(i[0].attrs['href'], re.search('<\/i>\s*(\w+)', i[0].content)) for i in r]
            r = [(i[0], i[1].groups()[0]) for i in r if i[1]]
            if r:
                for i in r:
                    try:
                        host = i[1]
                        url = i[0]
                        host = client.replaceHTMLCodes(host)
                        host = host.encode('utf-8')
                        sources.append({
                            'source': host,
                            'quality': 'SD',
                            'language': 'en',
                            'url': url.replace('\/','/'),
                            'direct': False,
                            'debridonly': False
                        })
                    except: pass
            return sources
        except Exception:
            return

    def resolve(self, url):
        if self.base_link in url:
            url = client.request(url, output='geturl')
        return url
