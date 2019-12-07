# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 lambda

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


import re,os,json,urllib,urlparse

from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import workers


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['torba.se']
        self.base_link = 'http://torba.se'
        self.search_mv_link = '/movies/autocomplete?order=relevance&title=%s'
        self.search_tv_link = '/series/autocomplete?order=relevance&title=%s'
        self.tv_link = '/series/%s/%s/%s'
        self.mv_link = '/v/%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            query = self.search_mv_link % (urllib.quote_plus(title))
            query = urlparse.urljoin(self.base_link, query)

            r = client.request(query, XHR=True)
            r = json.loads(r)

            t = cleantitle.get(title)

            r = [(i['slug'], i['title'], i['year']) for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == str(i[2])][0]

            url = r.encode('utf-8')
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            query = self.search_tv_link % (urllib.quote_plus(tvshowtitle))
            query = urlparse.urljoin(self.base_link, query)

            r = client.request(query, XHR=True)
            r = json.loads(r)

            t = cleantitle.get(tvshowtitle)

            r = [(i['slug'], i['title'], i['year']) for i in r]
            r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == str(i[2])][0]

            url = r.encode('utf-8')
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if url == None: return

        url = '%s/%01d/%01d' % (url, int(season), int(episode))
        url = url.encode('utf-8')
        return url


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            try: url = self.tv_link % re.findall('(.+?)/(\d*)/(\d*)$', url)[0]
            except: url = self.mv_link % url

            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)

            url = client.parseDOM(r, 'a', ret='href', attrs = {'class': 'video-play.+?'})[0]
            url = re.findall('(?://|\.)streamtorrent\.tv/.+?/([0-9a-zA-Z/]+)', url)[0]

            u = 'https://streamtorrent.tv/api/torrent/%s.json' % url

            r = client.request(u)
            r = json.loads(r)

            r = [i for i in r['files'] if 'streams' in i and len(i['streams']) > 0][0]
            r = [{'height': i['height'], 'stream_id': r['_id'], 'vid_id': url} for i in r['streams']]

            links = []
            links += [{'quality': '1080p', 'url': urllib.urlencode(i)} for i in r if int(i['height']) >= 1080]
            links += [{'quality': 'HD', 'url': urllib.urlencode(i)} for i in r if 720 <= int(i['height']) < 1080]
            links += [{'quality': 'SD', 'url': urllib.urlencode(i)} for i in r if int(i['height']) <= 720]
            links = links[:3]

            for i in links: sources.append({'source': 'torba.se', 'quality': i['quality'], 'language': 'en', 'url': i['url'], 'direct': True, 'debridonly': False, 'autoplay': False})

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            m3u8 = [
                '#EXTM3U',
                '#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",DEFAULT=YES,AUTOSELECT=YES,NAME="Stream 1",URI="{audio_stream}"',
                '',
                '#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=0,NAME="{stream_name}",AUDIO="audio"',
                '{video_stream}'
                ]


            query = urlparse.parse_qs(url)
            query = dict([(key, query[key][0]) if query[key] else (key, '') for key in query])

            auth = 'http://streamtorrent.tv/api/torrent/%s/%s.m3u8?json=true' % (query['vid_id'], query['stream_id'])

            r = client.request(auth)
            r = json.loads(r)
            try: url = r['url']
            except: url = None


            if not url == None:

                def dialog(url):
                    try: self.disableScraper = control.yesnoDialog('Torba requires you visit, on any device, the following url to watch this video:', '[COLOR skyblue]%s[/COLOR]' % url, '', 'Torba', 'Cancel', 'Settings')
                    except: pass

                workers.Thread(dialog, url).start()
                control.sleep(3000)

                for i in range(100):
                    try:
                        if not control.condVisibility('Window.IsActive(yesnoDialog)'): break

                        r = client.request(auth)
                        r = json.loads(r)
                        try: url = r['url']
                        except: url = None

                        if url == None: break

                        workers.Thread(dialog, url).start()
                        control.sleep(3000)
                    except:
                        pass

                if self.disableScraper:
                    control.openSettings(query='2.0')
                    return ''

                control.execute('Dialog.Close(yesnoDialog)')


            if not url == None: return


            stream_name = '%sp' % (query['height'])
            video_stream = r[stream_name]

            if not 'audio' in r: return video_stream

            audio_stream = r['audio']

            content = ('\n'.join(m3u8)).format(**{'audio_stream': audio_stream, 'stream_name': stream_name, 'video_stream': video_stream})


            path = os.path.join(control.dataPath, 'torbase.m3u8')

            control.makeFile(control.dataPath) ; control.deleteFile(path)

            file = control.openFile(path, 'w') ; file.write(content) ; file.close()

            return path
        except:
            return


