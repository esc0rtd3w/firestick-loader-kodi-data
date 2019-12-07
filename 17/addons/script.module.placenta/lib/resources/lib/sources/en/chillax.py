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

import urlparse, urllib, re, json, xbmc

from resources.lib.modules import client, cleantitle, source_utils, directstream


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['chillax.ws']
        self.base_link = 'http://chillax.ws'
        # self.referer = 'http://vumoo.li/'
        self.search_path = '/search/auto?q=%s'
        # self.imdb_path = '/?imdb=%s'
        self.series_path = '/series/getTvLink?id=%s&s=%s&e=%s'
        self.movie_path = '/movies/getMovieLink?id=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year, 'imdb': imdb}
            return urllib.urlencode(url)

        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            data = {'tvshowtitle': tvshowtitle, 'year': year, 'imdb': imdb}
            return urllib.urlencode(data)

        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)
            data.update({'season': season, 'episode': episode, 'title': title, 'premiered': premiered})

            return urllib.urlencode(data)

        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)

            if 'tvshowtitle' in data:
                url = self.__get_episode_url(data)
            else:
                url = self.__get_movie_url(data)

            response = client.request(url)
            links = json.loads(response)

            for link in links:
                try:
                    url = urlparse.urljoin(self.base_link, link['file'])

                    redirect = client.request(url, output='geturl')

                    if 'google' in redirect:
                        try:
                            quality = directstream.googletag(redirect)[0]['quality']

                        except Exception:
                            quality = link['label']

                        if 'lh3.googleusercontent' in redirect:
                            redirect = directstream.googleproxy(link)

                        sources.append({
                            'source': 'gvideo',
                            'quality': quality,
                            'language': 'en',
                            'url': redirect,
                            'direct': True,
                            'debridonly': False
                        })

                except Exception:
                    pass

            return sources

        except Exception:
            return

    def resolve(self, url):
        try:
            return url
        except Exception:
            return

    def __get_episode_url(self, data):
        try:
            path = self.search_path % urllib.quote_plus(data['tvshowtitle'])
            url = urlparse.urljoin(self.base_link, path)

            response = client.request(url)
            searchobj = json.loads(response)

            for obj in searchobj:
                if obj['title'] == data['tvshowtitle'] and obj['year'] == data['year']:
                    vid_id = obj['id']
                    break

            path = self.series_path % (vid_id, data['season'], data['episode'])
            url = urlparse.urljoin(self.base_link, path)

            return url

        except Exception:
            return

    def __get_movie_url(self, data):
        try:
            path = self.search_path % urllib.quote_plus(data['title'])
            url = urlparse.urljoin(self.base_link, path)

            response = client.request(url)
            searchobj = json.loads(response)

            for obj in searchobj:
                if obj['title'] == data['title'] and obj['year'] == data['year']:
                    vid_id = obj['id']
                    break

            path = self.movie_path % vid_id
            url = urlparse.urljoin(self.base_link, path)

            return url

        except Exception:
            return
