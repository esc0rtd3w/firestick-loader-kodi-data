# -*- coding: utf-8 -*-

'''
    Covenant Add-on
    Copyright (C) 2017 Covenant

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


import re, urllib, urlparse, json, base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import dom_parser
from resources.lib.modules import directstream
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['pubfilm.to']
        self.base_link = 'http://www.pubfilm.to'

        self.tvsearch_link = '?c=movie&m=quickSearch&keyword=%s'
        self.tvsearch_link_2 = '?c=movie&m=filter&keyword=%s'
        

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            return self.__search([title] + source_utils.aliases_to_array(aliases), year)
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'aliases': aliases, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            tvshowtitle = data['tvshowtitle']
            aliases = source_utils.aliases_to_array(eval(data['aliases']))
            # maybe ignore the year because they use wrong dates on seasons
            url = self.__search([tvshowtitle] + aliases, data['year'], season)

            #if url == None: raise Exception()
            if not url: return

            url = url.replace('episode=0','episode=%01d' % int(episode))
            url = urlparse.urljoin(self.base_link, url)
            url = url.encode('utf-8')
            return url
        
        except:
            return

    def __search(self, titles, year, season='0'):
        try:
            url = urlparse.urljoin(self.base_link, self.tvsearch_link) % (urllib.quote_plus(titles[0]))
            url2 = urlparse.urljoin(self.base_link, self.tvsearch_link_2) % (urllib.quote_plus(titles[0]))
            cookie = '; approve_search=yes'   
            result = client.request(url,  cookie=cookie)
            if season <> '0':
                try:
                    id = [j['id'] for j in json.loads(result) if str.upper(str(j['title'])) == str.upper(titles[0] + ' - Season ' + season) ]
                    page = '%s-season-%s-stream-%s.html' % (str.replace(titles[0],' ','-'), season, id[0])
                except:       
                     result = client.request(url2, cookie=cookie)
                     result = client.parseDOM(result, 'div', attrs={'class': 'recent-item'})
                     page = [re.findall(r'class=\'title_new\'>.*?Season\s+%s.*?<.*?href="([^"]+)">'%season, r, re.DOTALL) for r in result if bool(re.search(r'class=\'title_new\'>.*?Season\s+%s.*?<'%season, r, re.DOTALL))][0][0]
             
            else:
                try:
                    id = [j['id'] for j in json.loads(result) if str.upper(str(j['title'])) == str.upper(titles[0]) and j['year'] == year ]
                    page = '%s-stream-%s.html' % (str.replace(titles[0],' ','-'), id[0])
                except:       
                    result = client.request(url2, cookie=cookie)
                    result = client.parseDOM(result, 'div', attrs={'class': 'recent-item'})
                    page = [re.findall(r'class=\'title_new\'>.*?\(%s\).*?href="([^"]+)"' % year, r, re.DOTALL) for r in result if bool(re.search(r'class=\'title_new\'>.*?\(%s\)'%year, r, re.DOTALL))][0][0]

            
            url = page if 'http' in page else urlparse.urljoin(self.base_link, page)
            result = client.request(url)
            url = re.findall(u'<center><iframe\s+id="myiframe".*?src="([^"]+)', result)[0]
        
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources
            content = 'episode' if 'episode' in url else 'movie'
            result = client.request(url)
            try:
                url = re.findall(r"class\s*=\s*'play_container'\s+href\s*=\s*'([^']+)", result)[0]
                result = client.request(url, timeout='10')
            except:
                pass
            try:
                url = re.compile('ajax\(\{\s*url\s*:\s*[\'"]([^\'"]+)').findall(result)[0]
                post = 'post'
            except:
                url = re.compile(r'onclick=.*?show_player.*?,.*?"([^\\]+)').findall(result)[0]
                post = None            

            if content <> 'movie':
                try:
                    if post == 'post':
                        id, episode = re.compile('id=(\d+).*?&e=(\d*)').findall(url)[0]
                        post = {'id': id, 'e': episode, 'cat': 'episode'}                        
                except:
                    pass
            else:                
                if post == 'post':
                    id = re.compile('id=(\d+)').findall(url)[0]
                    post = {'id': id, 'cat': 'movie'}               

            if post <> None:
                result = client.request(url, post=post)
                url = re.findall(r"(https?:.*?)'\s+id='avail_links",result)[0]
            
            try:
                if 'google' in url:
                    valid, hoster = source_utils.is_host_valid(url, hostDict)
                    urls, host, direct = source_utils.check_directstreams(url, hoster)
                    for x in urls: sources.append({'source': host, 'quality': x['quality'], 'language': 'en', 'url': x['url'], 'direct': direct, 'debridonly': False})
              
                else:
                    valid, hoster = source_utils.is_host_valid(url, hostDict)
                    sources.append({'source': hoster, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

            except:
                pass
                
            return sources
        except:
            return sources


    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url


