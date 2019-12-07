# -*- coding: utf-8 -*-

'''
    Jor-El Add-on
    Copyright (C) 2016 Jor-El

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

from resources.lib.modules import directstream

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domain = 'chillax.ws'
        self.base_link = 'http://chillax.ws'
        self.search_link = 'http://chillax.ws/search/auto?q='
        self.movie_link = "http://chillax.ws/movies/getMovieLink?"
        self.login_link = 'http://chillax.ws/session/loginajax'
        self.tv_link = 'http://chillax.ws/series/getTvLink?'
        self.login_payload = {'username': '', 'password': ''}

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        url = []
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        url = []
        return url

    def sources(self, url, hostDict, hostprDict):
        sources = []
        sources.append({'source': "openload", 'quality': "HD", 'language': "en",
                        'url': ' https://openload.co/f/IYt5Vk18WdE/Malcolm.in.the.Middle.S07E21.DVDRip.x264-TASTETV.mkv.mp4',
                        'info' : i['type'],
                        'direct': False, 'debridonly': False})
        return sources


    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url