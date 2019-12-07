

#iStream Extension
#iTVMovie
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import requests
from entertainment import common
import xbmc


s = requests.session()


class iTVMovie(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]
    
    name = 'iTVMovie'
    display_name = 'iTVMovie'
    base_url = 'http://itvmovie.se'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    source_enabled_by_default = 'true'




    def AddMedia(self, list, res, data):

        import json

        js_data = json.loads(data)
        uniques = []

        if 'drive.amazon' in str(js_data):

            final_url = js_data['data'][0]['file']
            self.AddFileHost(list, res, final_url)

        else:

            for field in js_data['data']:
                final_url = field['file']
                res = field['label'] 

                if '.srt' not in final_url:
                    if '1080' in res:
                        res='1080P'                   
                    elif '720' in res:
                        res='720P'
                    elif  '480' in res:
                        res='DVD'
                    elif '360' in res:
                        res='SD'
                    else:
                        res='DVD'

                    if final_url not in uniques:
                        uniques.append(final_url)
                        self.AddFileHost(list, res, final_url)




    def AddBitPorn(self, list, url):

        import re,sys,urllib

        referer = url

        if sys.version_info < (2, 7, 9):
            url = 'https://ssl-proxy.my-addr.org/myaddrproxy.php/' + url

        xbmc.log('################url###='+str(url))

        headers = {'User-Agent':self.User_Agent}
        link = s.get(url, headers=headers, verify=False, timeout=3).content
        match = re.findall(r'"file":"([^"]+)","label":"([^"]+)"', str(link), re.I|re.DOTALL)
        uniques = []

        for final_url, res in match:

            if 'ssl-proxy.my-addr.org' in final_url:
                final_url = final_url.replace('https:\/\/ssl-proxy.my-addr.org\/myaddrproxy.php\/','')
                final_url = final_url.replace('https\\/','https:\\/\\/')
            xbmc.log('################final_url###='+str(final_url))
            final_url = final_url.replace('\\','')
            xbmc.log('################final_url2###='+str(final_url))
            host = final_url.split('//')[1].split('/')[0]
            xbmc.log('################host###='+str(host))
            headers = {'Host':host, 'Referer':referer, 'User-Agent':self.User_Agent}
            final_url = final_url + '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])

            if '.srt' not in final_url:
                if '1080' in res:
                    res='1080P'                   
                elif '720' in res:
                    res='720P'
                elif  '480' in res:
                    res='DVD'
                elif '360' in res:
                    res='SD'
                else:
                    res='DVD'

                if final_url not in uniques:
                    uniques.append(final_url)
                    self.AddFileHost(list, res, final_url)




    def GetFileHosts(self, url, list, lock, message_queue, season, episode, year, type, res):

        import base64,re,urlresolver
        
        headers = {'User-Agent':self.User_Agent}
        link = s.get(url, headers=headers, timeout=3).content

        media_year = ''


        try:

            res = res.upper()
            media_year = re.findall(r'Release:.*?>([^<]*)<', str(link), re.I|re.DOTALL)[0].strip()

            if '1080' in res:
                res='1080P'                   
            elif '720' in res:
                res='720P'
            elif 'HDCAM' in res:
                res='CAM'
            elif 'HDTC' in res:
                res='CAM'
            elif 'HD' in res:
                res='HD'
            elif  '480' in res:
                res='DVD'
            elif '360' in res:
                res='SD'
            elif 'SD' in res:
                res='SD'
            elif 'TC' in res:
                res='CAM'
            elif 'CAM' in res:
                res='CAM'
            else:
                res='DVD'

        except:pass

        if not res:
            res = 'HD'

        form_data = {'s':0}
        token = re.compile('class="token" name="([^"]*)" value="([^"]*)"').findall(link)
        for key, value in token:
            form_data[key] = value

        item_id = re.compile('data-film="([^"]*)"').findall(link)[0]
        form_data['id'] = item_id
        uniques = []

        try:

            if type == 'tv_episodes':

                epis = re.compile('title="Watch Episode.*?">([^<>]*)<').findall(link)
                for epi in epis:
                    if int(epi) == int(episode):
                        form_data['ep'] = int(epi)
                        request_url = '%s/watch/request-api-detail' %self.base_url
                        link2 = s.post(request_url, data=form_data, headers=headers, timeout=3).json()
                        server_id = re.compile("data-server='([^']*)'").findall(link2['server'])
                        for server in server_id:
                            form_data['s'] = int(server)
                            final_link = s.post(request_url, data=form_data, headers=headers, timeout=3).json()
                            if final_link['status'].lower() == 'embed':
                                final_url = base64.b64decode(final_link['result'])
                                final_url = final_url.replace('"','').replace('\\','')
                                '''if 'bitporno' in final_url:
                                    self.AddBitPorn(list, final_url)
                                else:'''
                                if urlresolver.HostedMediaFile(final_url):
                                    if final_url not in uniques:
                                        uniques.append(final_url)
                                        self.AddFileHost(list, res, final_url)
                            elif final_link['status'].lower() == 'api':
                                data = base64.b64decode(final_link['result'])
                                self.AddMedia(list, res, data)

            else:

                if int(media_year) == int(year):
                    request_url = '%s/watch/request-api' %self.base_url
                    link2 = s.post(request_url, data=form_data, headers=headers, timeout=3).json()
                    server_id = re.compile("data-server='([^']*)'").findall(link2['server'])
                    for server in server_id:
                        form_data['s'] = int(server)
                        final_link = s.post(request_url, data=form_data, headers=headers, timeout=3).json()
                        if final_link['status'].lower() == 'embed':
                            final_url = base64.b64decode(final_link['result'])
                            final_url = final_url.replace('"','').replace('\\','')
                            '''if 'bitporno' in final_url:
                                self.AddBitPorn(list, final_url)
                            else:'''
                            if urlresolver.HostedMediaFile(final_url):
                                uniques.append(final_url)
                                self.AddFileHost(list, res, final_url)
                        elif final_link['status'].lower() == 'api':
                            data = base64.b64decode(final_link['result'])
                            self.AddMedia(list, res, data)

        except:pass




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        
        import re
        
        name = self.CleanTextForSearch(name.lower()).strip()
        headers = {'User-Agent':self.User_Agent}
        search = '%s/search?key=%s' %(self.base_url,name.replace(' ','%20'))
        link = s.get(search, headers=headers, timeout=3).content
        
        try:

            links = link.split('item">')[1:]
            
            for p in links:

                media_url = re.compile('href="([^"]*)"').findall(p)[0]
                if self.base_url not in media_url:
                    media_url = self.base_url + media_url
                media_title = re.compile('title="([^"]*)"').findall(p)[0].strip()
                qual = ''
                try:
                    qual = re.compile('quality".*?>([^<>]*)<').findall(p)[0].strip()
                except:pass

                if type == 'tv_episodes':
                    if '%s season %s' %(name,season) in self.CleanTextForSearch(media_title.lower()):
                        self.GetFileHosts(media_url, list, lock, message_queue, season, episode, year, type, qual)

                else:
                    if name in self.CleanTextForSearch(media_title.lower()):
                        self.GetFileHosts(media_url, list, lock, message_queue, '', '', year, type, qual)

        except:pass
 
