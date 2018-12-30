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


import re,urllib,urlparse,json,time

from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib import resolvers

class source:
    def __init__(self):
        self.domains = ['wrzcraft.net']
        self.base_link = 'http://wrzcraft.net'
        self.moviesearch_link = '/?s=%s+%s'
        self.search_link = '/?s=%s'

    def get_movie(self, imdb, title, year):
        try:
            urls = []
            url = self.moviesearch_link % (cleantitle.geturl(title), year)
            r = urlparse.urljoin(self.base_link, url)
            r = client.request(r)
            posts = client.parseDOM(r, 'div', attrs = {'class': 'post'})

            for post in posts:
                extra = False
                tags = client.parseDOM(post, 'a', attrs = {'rel' : 'category tag'})
                for tag in tags:
                    #Make sure it isnt an extra
                    if tag == 'Extras':
                        extra = True
                        break
            
                if extra == False:
                    containerDiv = client.parseDOM(post, 'div', attrs = {'class' : 'posttitle'})

                    if not containerDiv:
                        containerDiv = client.parseDOM(post, 'div', attrs = {'class' : 'expandposttitle'})

                    href = client.parseDOM(containerDiv, 'a', ret='href')[0]
                    title = client.parseDOM(containerDiv,'a', ret='title')[0]
                    href = href.encode('utf-8')
                    title = title.encode('utf-8')
                    urls.append({'url' : href, 'title' : title})
                    
            return urls
        except Exception as e:
            control.log('wrzcraft error')
            control.log(e)
            return

    def get_show(self, imdb, tvdb, tvshowtitle, year):
        try:
            url = '%s (%s)' % (tvshowtitle, year)
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

    def get_episode(self, url, imdb, tvdb, title, date, season, episode):
        try:
            control.log('wrzcraft episode begin')
            urls = []
            tvshowtitle, year = re.compile('(.+?) [(](\d{4})[)]$').findall(url)[0]
            season, episode = season.zfill(2), episode.zfill(2)
            control.log('got before query')
            query = '%s s%se%s' % (tvshowtitle, season, episode)
            query = self.search_link % (urllib.quote_plus(query))
            control.log('wrzcraft query')
            control.log(query)
            r = urlparse.urljoin(self.base_link, query)
            r = client.replaceHTMLCodes(r)
            r = r.encode('utf-8')
            r = client.request(r)
            posts = client.parseDOM(r, 'div', attrs = {'class': 'post'})

            for post in posts:
                containerDiv = client.parseDOM(post, 'div', attrs = {'class' : 'posttitle'})

                if not containerDiv:
                    containerDiv = client.parseDOM(post, 'div', attrs = {'class' : 'expandposttitle'})

                href = client.parseDOM(containerDiv, 'a', ret='href')[0]
                title = client.parseDOM(containerDiv,'a', ret='title')[0]
                href = href.encode('utf-8')
                title = title.encode('utf-8')
                urls.append({'url' : href, 'title' : title})
            return urls
        except Exception as e:
            control.log('wrzcraft error')
            control.log(e)
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []
            if url == None: return sources
            for item in url:
                newLink = client.request(item['url'])
                divArea = client.parseDOM(newLink, 'div', attrs = {"class": "postarea"})
                match = client.parseDOM(divArea, "a", ret = "href", attrs = {'rel': 'nofollow'}) 

                for link in match:
                    if re.match('((?!\.part[0-9]).)*$', link, flags=re.IGNORECASE) and '://' in link:
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link.strip().lower()).netloc)[0].split('.')[0]
                        scheme = urlparse.urlparse(link).scheme
                        if host in hostDict and scheme:                                    
                            if '1080' in link: 
                                quality = '1080p'
                            elif '720' in link: 
                                quality = 'HD'
                            else: 
                                quality = 'SD'
                            fileLink = client.replaceHTMLCodes(link)
                            fileLink = fileLink.encode('utf-8')
                            sources.append({ 'source': host, 'quality': quality, 'provider': 'wrzcraft', 'url': fileLink })
            return sources
        except Exception as e:
            control.log('ERROR wrzcraft sources %s' % e)
            return sources

    def resolve(self, url):
        control.log('>>>>>>>>>>>>>>>>>> Resolve WRZCRAFT %s' % url)
        return resolvers.request(url)


