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
import re,urllib,urlparse,json,time,requests
from resources.lib.libraries import cleantitle
from resources.lib.libraries import client
from resources.lib.libraries import control
from resources.lib import resolvers



class source:
    def __init__(self):
        self.domains = ['alluc.ee']
        self.base_link = 'http://alluc.ee'
        self.moviesearch_link = ''
        self.stream_url = []


    def get_movie(self, imdb, title, year):
        try:
            if control.setting('alluc_user'):
                if control.setting('realdebrid_token') or control.setting('premiumize_user'):
                    self.moviesearch_link = '/api/search/download?user=%s&password=%s&query=%s+%s'
                else:
                    self.moviesearch_link = '/api/search/stream/?user=%s&password=%s&query=%s+%s'
                
                url = self.moviesearch_link % (control.setting('alluc_user'), control.setting('alluc_password'),cleantitle.geturl(title), year)
                r = urlparse.urljoin(self.base_link, url)
                r = r + "+%23newlinks"
                r = client.request(r)
                r1 = json.loads(r)

                for item in r1['result']:
                    if len(item['hosterurls']) == 1 and 'en' in item['lang']:
                        tmp = item['hosterurls'][0]['url']
                        tmp = client.replaceHTMLCodes(tmp)
                        tmp = tmp.encode('utf-8')
                        title = item['title'].encode('utf-8')
                        self.stream_url.append({'url': tmp, 'hoster': item['hostername'], 'title': title })
            return self.stream_url
        except Exception as e: 
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
            if control.setting('alluc_user'):
                if control.setting('realdebrid_token') or control.setting('premiumize_user'):
                    self.moviesearch_link = '/api/search/download?user=%s&password=%s&query=%s'
                else:
                    self.moviesearch_link = '/api/search/stream/?user=%s&password=%s&query=%s'

            tvshowtitle, year = re.compile('(.+?) [(](\d{4})[)]$').findall(url)[0]
            season, episode = season.zfill(2), episode.zfill(2)
            query = '%s s%se%s' % (tvshowtitle, season, episode)
            query = self.moviesearch_link % (control.setting('alluc_user'), control.setting('alluc_password'), urllib.quote_plus(query))
            r = urlparse.urljoin(self.base_link, query)
            r = r + "+%23newlinks"
            r = requests.get(r).json()

            for item in r['result']:   
                if len(item['hosterurls']) == 1 and 'en' in item['lang']:
                    tmp = item['hosterurls'][0]['url']
                    tmp = client.replaceHTMLCodes(tmp)
                    tmp = tmp.encode('utf-8')
                    title = item['title'].encode('utf-8')
                    self.stream_url.append({'url': tmp, 'hoster': item['hostername'], 'title': title })
            return self.stream_url
        except Exception as e: 
            control.log('alluc error tv')
            control.log(e)
            return


    def get_sources(self, url, hosthdDict, hostDict, locDict):
        try:
            sources = []

            if url == None: return sources
            
            for link in url:
                if re.match('((?!\.part[0-9]).)*$', link['url'], flags=re.IGNORECASE) and '://' in link['url']:
                        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(link['url'].strip().lower()).netloc)[0].split('.')[0]
                        scheme = urlparse.urlparse(link['url']).scheme
                        if host in hostDict and scheme:    
                            if '1080' in link["url"] or '1080' in link['url']: 
                                quality = "1080p"
                            elif '720' in link['title'] or '720' in link['url']: 
                                quality = 'HD'
                            else:
                                quality = 'SD'
                            sources.append({ 'source' : host, 'quality' : quality, 'provider': 'alluc', 'url': link['url'] })
            return sources
        except Exception as e:
            control.log('ERROR ALLUC %s' % e)
            return sources




    def resolve(self, url):
        control.log('>>>>>>>>>>>>>>>>>> Resolve ALLUC %s' % url)
        return resolvers.request(url)