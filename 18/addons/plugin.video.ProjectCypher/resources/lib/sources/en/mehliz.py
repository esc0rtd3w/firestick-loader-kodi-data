"""
    Jor-El Add-on
    Copyright (C) 2018 Jor-El

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
"""

# Addon Name: Project Cypher
# Addon id: plugin.video.ProjectCypher
# Addon Provider: Cypher

import urllib, re, sys
import requests as client
from resources.lib.modules import cfscrape, directstream, source_utils, cleantitle
from bs4 import BeautifulSoup

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['mehlizmovies.is']
        self.base_link = 'https://www.mehlizmovies.is'
        self.season_path = '/seasons/%s-season-%s/'
        self.search_path = '/?s=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year}
            return url

        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:

            data = {'tvshowtitle': tvshowtitle, 'year': year}
            return data

        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = url
            data.update({'season': season, 'episode': episode, 'title': title, 'premiered': premiered})
            return data

        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            data = url

            if 'tvshowtitle' in data:
                url = self.__get_episode_url(data, hostDict)
            else:
                url = self.__get_movie_url(data, hostDict)

            sources = url
            return sources

        except Exception:
            print("Unexpected error in Mehlix sources Script:")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return ""

    def resolve(self, url):
        return url

    def __get_episode_url(self, data, hostDict):
        scraper = cfscrape.create_scraper()
        try:
            value = "/seasons/" + cleantitle.geturl(data['tvshowtitle']) + '-season-' + data['season']
            url = self.base_link + value
            html = scraper.get(self.base_link)
            html = scraper.get(url)
            page_list = BeautifulSoup(html.text, 'html.parser')
            page_list = page_list.find_all('div', {'class':'episodiotitle'})
            ep_page = ''
            for i in page_list:
                if re.sub(r'\W+', '', data['title'].lower()) in re.sub(r'\W+', '', i.text.lower()):
                    ep_page = i.prettify()
            if ep_page == '': return ''
            ep_page = BeautifulSoup(ep_page, 'html.parser').find_all('a')[0]['href']
            html = scraper.get(ep_page)
            embed = re.findall('<iframe.+?src=\"(.+?)\"', html.text)[0]
            url = embed
            sources = []
            if 'mehliz' in url:
                html = scraper.get(url, headers={'referer': self.base_link + '/'})
                files = re.findall('file: \"(.+?)\".+?label: \"(.+?)\"', html.text)

                for i in files:
                    try:
                        sources.append({
                            'source': 'gvideo',
                            'quality': i[1],
                            'language': 'en',
                            'url': i[0] + "|Referer=https://www.mehlizmovies.is",
                            'direct': True,
                            'debridonly': False
                        })

                    except Exception:
                        pass

            else:
                valid, hoster = source_utils.is_host_valid(url, hostDict)
                if not valid: return ''
                urls, host, direct = source_utils.check_directstreams(url, hoster)

                sources.append({
                    'source': host,
                    'quality': urls[0]['quality'],
                    'language': 'en',
                    'url': url + "|Referer=https://www.mehlizmovies.is",
                    'direct': False,
                    'debridonly': False
                })


            return sources

        except Exception:
            print("Unexpected error in Mehlix _get_episode_url Script:")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return ""

    def __get_movie_url(self, data, hostDict):
        scraper = cfscrape.create_scraper()
        try:
            html = scraper.get(self.base_link +"/movies/"+cleantitle.geturl(data['title']))
            embeds = re.findall('play-box-iframe.+\s<iframe.+?src=\"(.+?)\"', html.text)[0]
            url = embeds
            sources = []
            if 'mehliz' in url:
                html = scraper.get(url, headers={'referer': self.base_link + '/'})
                files = re.findall('file: \"(.+?)\".+?label: \"(.+?)\"', html.text)

                for i in files:
                    try:
                        sources.append({
                            'source': 'gvideo',
                            'quality': i[1],
                            'language': 'en',
                            'url': i[0] + "|Referer=https://www.mehlizmovies.is",
                            'direct': True,
                            'debridonly': False
                        })

                    except Exception:
                        pass

            else:
                valid, hoster = source_utils.is_host_valid(url, hostDict)
                if not valid: return ''
                urls, host, direct = source_utils.check_directstreams(url, hoster)

                sources.append({
                    'source': host,
                    'quality': urls[0]['quality'],
                    'language': 'en',
                    'url': url + "|Referer=https://www.mehlizmovies.is",
                    'direct': False,
                    'debridonly': False
                })

            return sources

        except Exception:
            print("Unexpected error in Mehliz getMovieURL Script:")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            return ""

#url = source.tvshow(source(), '', '', 'Vikings','','' '','2016')
#url = source.episode(source(),url,'', '', '', '', '3', '1')
#sources = source.sources(source(),url,'','')

