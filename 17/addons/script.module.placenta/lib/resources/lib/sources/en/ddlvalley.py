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

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import cfscrape
from resources.lib.modules import dom_parser2

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['ddlvalley.me']
        self.base_link = 'http://www.ddlvalley.me'
        self.search_link = 'search/%s/'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title).replace('-','+')
            url = urlparse.urljoin(self.base_link, self.search_link % clean_title)
            url = {'url': url, 'title': title, 'year': year}
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
      
            data = urlparse.parse_qs(url)

            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            show  = True if 'tvshowtitle' in data else False
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s' % (data['tvshowtitle']) if\
                'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            
            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)
            scraper = cfscrape.create_scraper()
            r = scraper.get(url).content
            u = r
            
            next_page = True
            num = 1
            while next_page:
                try:
                    np = re.findall('<link rel="next" href="([^"]+)', u)[0]
                    # Client Requests is causing a timeout on links for ddl valley, falling back on cfscrape
                    #u = client.request(np, headers=headers, cookie=cookie, timeout=5)  
                    u = scraper.get(np).content
                    r += u
                except: next_page = False

            items = dom_parser2.parse_dom(r, 'h2')
            items = [dom_parser2.parse_dom(i.content, 'a', req=['href','rel','title','data-wpel-link']) for i in items]
            items = [(i[0].content, i[0].attrs['href']) for i in items]
            items = [(i[0], i[1]) for i in items if cleantitle.get_simple(title.lower()) in cleantitle.get_simple(i[0].lower())]
            
            for item in items:
                try:
                    name = item[0]
                    name = client.replaceHTMLCodes(name)
                    # Client Requests is causing a timeout on links for ddl valley, falling back on cfscrape
                    #r = client.request(item[1], headers=headers, cookie=cookie,  timeout=15)  
                    r = scraper.get(item[1]).content
                    links = dom_parser2.parse_dom(r, 'a', req=['href','rel','data-wpel-link','target'])
                    links = [i.attrs['href'] for i in links]
                    if show:
                        links = [i for i in links if hdlr.lower() in i.lower()]
                        
                    for url in links:
                        try:
                            if hdlr in name:
                                fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', name.upper())
                                fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
                                fmt = [i.lower() for i in fmt]

                                if any(i.endswith(('subs', 'sub', 'dubbed', 'dub')) for i in fmt): raise Exception()
                                if any(i in ['extras'] for i in fmt): raise Exception()

                                if '1080p' in fmt: quality = '1080p'
                                elif '720p' in fmt: quality = '720p'
                                else: quality = 'SD'
                                if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): quality = 'SCR'
                                elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): quality = 'CAM'

                                info = []

                                if '3d' in fmt: info.append('3D')

                                try:
                                    size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', name[2])[-1]
                                    div = 1 if size.endswith(('GB', 'GiB')) else 1024
                                    size = float(re.sub('[^0-9|/.|/,]', '', size))/div
                                    size = '%.2f GB' % size
                                    info.append(size)
                                except:
                                    pass

                                if any(i in ['hevc', 'h265', 'x265'] for i in fmt): info.append('HEVC')

                                info = ' | '.join(info)

                                if not any(x in url for x in ['.rar', '.zip', '.iso']):
                                    url = client.replaceHTMLCodes(url)
                                    url = url.encode('utf-8')

                                    host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                                    host = client.replaceHTMLCodes(host)
                                    host = host.encode('utf-8')
                                    if host in hostDict:
                                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
                                    elif host in hostprDict: 
                                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
                        except:
                            pass
                except:
                    pass
            check = [i for i in sources if not i['quality'] == 'CAM']
            if check: sources = check

            return sources
        except:
            return sources

    def resolve(self, url):
        return url
