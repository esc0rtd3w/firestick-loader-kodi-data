# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @Daddy_Blamo wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: plugin.video.placenta
# Addon Provider: Mr.blamo

import re,traceback,urllib,urlparse,requests,json,sys
from resources.lib.modules import source_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import control

class source:
    def __init__(self):
        self.accepted_extensions = ['mkv','mp4','avi', 'm4v', 'mpg', 'mpeg', 'webm']
        self.priority = 1
        self.language = ['en']
        self.domain = 'furk.net'
        self.meta_search_link = "/api/plugins/metasearch?api_key=%s&q=%s&cached=yes&moderated=yes" \
                                "&match=all&sort=cached&type=video&offset=0&limit=%s"
        self.base_link = 'https://www.furk.net/'
        self.api_key = control.setting('furk.api')
        self.search_limit = control.setting('furk.limit')

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = tvshowtitle
            return url
        except:
            pass

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            url = {'tvshowtitle': url, 'season': season, 'episode': episode}
            return url
        except:
            pass

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if len(url['episode']) == 1: url['episode'] = "0" + url['episode']
            if len(url['season']) == 1: url['season'] = "0" + url['season']
            s = requests.Session()
            link = url['tvshowtitle'] + "+S" + url['season'] + "e" + url['episode']
            link = (self.base_link + self.meta_search_link % (self.api_key, link.replace(' ', '+'), self.search_limit))
            p = s.get(link)
            p = json.loads(p.text)
            files = p['files']
            for i in files:
                if int(i['files_num_video']) == 1:
                    name = i['name']
                    url_dl = ''
                    for x in self.accepted_extensions:
                        if 'url_dl' in i:
                            if i['url_dl'].endswith(x):
                                if 'FRENCH' in i['url_dl']:
                                    continue
                                url_dl = i['url_dl']
                                quality = source_utils.get_release_quality(name , url_dl)
                                sources.append({'source': "CDN",
                                                'quality': quality[0],
                                                'language': "en",
                                                'url': url_dl,
                                                'info': quality[1],
                                                'direct': True,
                                                'debridonly': False})
                            else:
                                continue
                        else:
                            continue
                    if url_dl == '':
                        continue
            return sources
        except:
            print("Unexpected error in Furk Scraper: source", sys.exc_info()[0])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(exc_type, exc_tb.tb_lineno)
            pass


    def resolve(self, url):
            return url