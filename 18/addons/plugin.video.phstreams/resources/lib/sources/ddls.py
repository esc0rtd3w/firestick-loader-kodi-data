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


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import debrid


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['ddlseries.net', 'ddlseries.me']
        self.base_link = 'http://www.ddlseries.me'
        self.search_link = '/?s=%s'


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


    def ddlseries_tvcache(self):
        try:
            r = urlparse.urljoin(self.base_link, '/tv-series-list.html')
            r = client.request(r)
            r = client.parseDOM(r, 'div', attrs = {'class': 'downpara-list'})[0]
            r = re.compile('<a href="([^"]+)[^>]*>(.*?)</a>').findall(r)
            r = [i for i in r if not '(Pack)' in i[1]]
            r = [(i[0], i[1], 'HD') for i in r if 'HD ' in i[1] and not '1080p' in i[1]] + [(i[0], i[1], '1080p') for i in r if '1080p' in i[1]]
            r = [(i[0], re.findall('(.+?) - (?:S|s)eason (\d*)', i[1]), i[2]) for i in r]
            r = [(i[0], i[1][0][0], str(i[1][0][1]), i[2]) for i in r if i[1]]
            return r
        except:
            return

	
    def sources(self, url, hostDict, hostprDict):
        try:
			sources = []

			if url == None: return sources

			if debrid.status() == False: raise Exception()

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle']
			season = '%01d' % int(data['season'])
			episode = '%02d' % int(data['episode'])

			r = cache.get(self.ddlseries_tvcache, 120)

			r = [(i[0], i[3]) for i in r if cleantitle.get(title) == cleantitle.get(i[1]) and season == i[2]]

			links = []

			for url, quality in r:
				try:
					link = client.request(url)
					vidlinks = client.parseDOM(link, 'span', attrs = {'class': 'overtr'})[0]
					match = re.compile('href="([^"]+)[^>]*>\s*Episode\s+(\d+)<').findall(vidlinks)
					match = [(i[0], quality) for i in match if episode == i[1]]
					links += match
				except:
					pass

			for url, quality in links:
				try:
					if "protect-links" in url:
						redirect = client.request(url)
						url = re.findall('<a href="(.*?)" target="_blank">', redirect)
						url = url[0]

					host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
					if not host in hostprDict: raise Exception()
					host = client.replaceHTMLCodes(host)
					host = host.encode('utf-8')

					sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': True})
				except:
					pass

			return sources
        except:
            return sources


    def resolve(self, url):
        return url


