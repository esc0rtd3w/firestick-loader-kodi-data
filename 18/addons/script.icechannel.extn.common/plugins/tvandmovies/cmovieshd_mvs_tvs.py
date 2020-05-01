

#iStream Extension
#CMoviesHD
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import requests
import xbmc


requests.packages.urllib3.disable_warnings()
s = requests.session()




class cmovieshd(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]

    name = 'CMoviesHD'
    display_name = 'CMoviesHD'
    base_url = 'http://cmovieshd.com'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

    source_enabled_by_default = 'true'




    def random_generator(self):
        import string,random
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))




    def open_url(self, url, params=None, headers=''):
        
        if not headers:
            headers={'User-Agent':self.User_Agent,'Referer':self.base_url}

        link = s.get(url, params=params, headers=headers, verify=False, timeout=3)
        return link




    def AddMedia(self, list, url, episode_id, key_gen, referer):

        try:

            import hashlib

            key = '!@#$%^&*('
            cookie = '%s=%s' %(hashlib.md5(key[::1] + episode_id + key_gen).hexdigest(),
                               hashlib.md5(key_gen + referer + episode_id).hexdigest())

            headers = {'Accept-Encoding':'gzip, deflate, sdch', 'Cookie': cookie, 'Referer': referer,
                       'Origin':self.base_url, 'User-Agent':self.User_Agent}

            final_link = self.open_url(url, '', headers).json()
            data = final_link['playlist'][0]['sources']
            uniques = []

            for field in data:
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

        except:pass




    def AddEmbed(self, list, url, referer):

        try:

            import re
            
            headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Accept-Encoding':'gzip, deflate, sdch', 'Accept-Language':'en-US,en;q=0.8',
                       'Referer':referer, 'User-Agent':self.User_Agent}

            final_link = self.open_url(url, '', headers).content
            final_url = re.findall(r'embed_src: "([^"]+)"', str(final_link), re.I|re.DOTALL)[0]

            if 'hdcam' in final_url.lower():
                res='CAM'
            elif 'cam' in final_url.lower():
                res='CAM'
            elif '360p' in final_url.lower():
                res='SD'
            elif  '480p' in final_url.lower():
                res='DVD'
            elif '720p' in final_url.lower():
                res='720P'
            elif '1080p' in final_url.lower():
                res='1080P'
            else:
                res='HD'

            self.AddFileHost(list, res, final_url)

        except:pass




    def GetLinks(self, list, server, referer):

        import re

        if 'openload' in server:

            self.AddEmbed(list, server, referer)

        else:
            
            link = self.open_url(server).content
            episode_id = re.findall(r'episode: "([^"]+)"', str(link), re.I|re.DOTALL)[2]
            hash_id = re.findall(r'hash: "([^"]+)"', str(link), re.I|re.DOTALL)[0]
            base_id = self.base_url.replace('http://','').replace('https://','')
            key_gen = self.random_generator()
            request_url = 'http://play.%s/grabber-api/episode/%s?token=%s' %(base_id,episode_id,key_gen)
            self.AddMedia(list, request_url, episode_id, key_gen, referer)




    def GetFileHosts(self, url, list, lock, message_queue, season, episode, type, year, query):

        import re

        referer = url + 'watch/'
        link = self.open_url(referer).content
        media_title = re.compile('<h1.*?>Watch</div>([^<>]*)<').findall(link)[0].strip()
        links = link.split('server">')[1:]
        
        for p in links:

            if type == 'tv_episodes':

                try:
                    
                    p = p.replace('Episode 0','Episode ')
                    data = p.split('<a')[1:]
                    
                    for d in data:
                        if ' %s:' %episode in d:
                            server = re.compile('href="([^"]+)"').findall(d)[0].strip()
                            self.GetLinks(list, server, referer)

                except:pass
                
            else:

                try:

                    data = p.split('<a')[1:]
                    
                    for d in data:
                        if query == self.CleanTextForSearch(media_title.lower().split('(')[0].strip()):
                            if year in media_title:
                                server = re.compile('href="([^"]+)"').findall(d)[0].strip()
                                self.GetLinks(list, server, referer)
                                
                        elif query == self.CleanTextForSearch(media_title.lower().split(':')[0].strip()):
                            if year in media_title:
                                server = re.compile('href="([^"]+)"').findall(d)[0].strip()
                                self.GetLinks(list, server, referer)

                except:pass




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import re
                
        name = self.CleanTextForSearch(name.lower())
        search =  '%s/search/?q=%s' %(self.base_url,str(name).replace(' ','+'))
        link = self.open_url(search).content
        links = link.split('item">')[1:]

        for p in links:

            try:

                media_url = re.compile('a href="([^"]+)"').findall(p)[0]
                media_title = re.compile('title="([^"]+)"').findall(p)[0]
                
                if type == 'tv_episodes':
                    if name in self.CleanTextForSearch(media_title.lower()):
                        if 'season %s' %season in media_title.lower() or name == 'iron fist':
                            self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type, year, name)
                else:
                    if name in self.CleanTextForSearch(media_title.lower()):
                        self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type, year, name)

            except:pass
            
                
                
