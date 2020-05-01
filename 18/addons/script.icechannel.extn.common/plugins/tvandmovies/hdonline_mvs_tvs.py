

#iStream Extension
#HD-Online
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import requests
import xbmc


requests.packages.urllib3.disable_warnings()
s = requests.session()




class hdonline(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]

    name = 'HD-Online'
    display_name = 'HD-Online'
    base_url = 'https://hdonline.to'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

    source_enabled_by_default = 'true'




    def uncensored(self, data):

        import re,xbmc
        
        xx = ''
        xy = ''
        try:
            data = '(' + data.split("(_$$)) ('_');")[0].split("/* `$$` */")[-1].strip()
            data = data.replace('(__$)[$$$]', '\'"\'')
            data = data.replace('(__$)[_$]', '"\\\\"')
            data = data.replace('(o^_^o)', '3')
            data = data.replace('(c^_^o)', '0')
            data = data.replace('(_$$)', '1')
            data = data.replace('($$_)', '4')
            code = '''def retA():
    class Infix:
        def __init__(self, function):
            self.function = function
        def __ror__(self, other):
            return Infix(lambda x, self=self, other=other: self.function(other, x))
        def __or__(self, other):
            return self.function(other)
        def __rlshift__(self, other):
            return Infix(lambda x, self=self, other=other: self.function(other, x))
        def __rshift__(self, other):
            return self.function(other)
        def __call__(self, value1, value2):
            return self.function(value1, value2)
    def my_add(x, y):
        try: return x + y
        except Exception: return str(x) + str(y)
    x = Infix(my_add)
    return %s
param = retA()'''
            vGlobals = {"__builtins__": None, '__name__':__name__, 'str':str, 'Exception':Exception}
            vLocals = { 'param': None }
            exec( code % data.replace('+','|x|'), vGlobals, vLocals)
            data = vLocals['param'].decode('string_escape')
            data = re.compile('''=['"]([^"^']+?)['"]''').findall(data)
            xx = data[0]
            xy = data[1]
        except Exception:
            xbmc.log('Sorry Could Not Decode')
        return xx, xy




    def open_url(self, url, params=None, headers=''):
        
        if not headers:
            headers={'User-Agent':self.User_Agent,'Referer':self.base_url}

        link = s.get(url, params=params, headers=headers, verify=False, timeout=3)
        return link




    def AddMedia(self, list, url, xx, xy, referer):

        try:
            
            hash_params = {'x':xx, 'y':xy}
            headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                       'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8',
                       'Referer':referer, 'User-Agent':self.User_Agent, 'X-Requested-With':'XMLHttpRequest'}

            final_link = self.open_url(url, hash_params, headers).json()

            data = final_link['playlist'][0]['sources']

            uniques = []

            for field in data:
                final_url = field['file']
                res= field['label']

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
            
            headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                       'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8',
                       'Referer':referer, 'User-Agent':self.User_Agent, 'X-Requested-With':'XMLHttpRequest'}
                                            

            final_link = self.open_url(url, headers).json()
            final_url = final_link['src']

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




    def GetLinks(self, list, media_id, episode_id, server, referer):

        import time

        if int(server) > 10:

            request_url = '%s/ajax/movie/get_embed/%s' %(self.base_url, episode_id)
            self.AddEmbed(list, request_url, referer)

        else:

            time_now = int(time.time() * 10000)
            slug = '%s/ajax/movie/token' % self.base_url
            params = {'eid':episode_id, 'mid':media_id, '_':time_now}
            headers = {'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                       'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8',
                       'Referer':referer, 'User-Agent':self.User_Agent, 'X-Requested-With':'XMLHttpRequest'}
            data = ''
            tries = 0
            while tries < 10:
                tries += 1
                data = self.open_url(slug, params, headers).content
                if not data:
                    data = ''
                    continue

                if '[]' not in data:
                    time.sleep(1)
                    break

            xx, xy = self.uncensored(str(data))
            request_url = '%s/ajax/movie/get_sources/%s' %(self.base_url, episode_id)
            self.AddMedia(list, request_url, xx, xy, referer)




    def GetFileHosts(self, url, list, lock, message_queue, season, episode, type, year, query):

        import re

        referer = url

        info = self.open_url(url).content
        
        media_id = re.compile('data-movie="([^"]+)"').findall(info)[0]
        media_year = re.compile('>Released:([^<:]*)<').findall(info)[0].strip()
        media_title = re.compile('"dc-title">([^<>]*)<').findall(info)[0]
        request_url = '%s/ajax/movie/episodes/%s' %(self.base_url, media_id)
        headers = {'Accept-Encoding':'gzip, deflate, sdch, br', 'Referer':referer, 'User-Agent':self.User_Agent}
        link = self.open_url(request_url, '', headers).json()
        links = str(link['html']).split('<div id="sv-')
        
        for p in links:
            
            if type == 'tv_episodes':

                try:
                    
                    p = p.replace('Episode 0','Episode ')
                    data = p.split('ep-item')[1:]
                    
                    for d in data:

                        if ' %s:' %episode in d:
                                
                            server = re.compile('data-server="([^"]+)"').findall(d)[0].strip()
                            episode_id = re.compile('data-id="([^"]+)"').findall(d)[0].strip()
                            referer = '%s?ep=%s' %(referer,episode_id)
                            self.GetLinks(list, media_id, episode_id, server, referer)

                except:pass
                
            else:

                try:

                    data = p.split('<ul id=')[1:]
                    
                    for d in data:
                        if query == self.CleanTextForSearch(media_title.lower()):
                            if year == media_year:
                                server = re.compile('data-server="([^"]+)"').findall(d)[0].strip()
                                episode_id = re.compile('data-id="([^"]+)"').findall(d)[0].strip()
                                referer = '%s?ep=%s' %(referer,episode_id)
                                self.GetLinks(list, media_id, episode_id, server, referer)
                                
                        elif query == self.CleanTextForSearch(media_title.lower().split(':')[0]):
                            if year == media_year:
                                server = re.compile('data-server="([^"]+)"').findall(d)[0].strip()
                                episode_id = re.compile('data-id="([^"]+)"').findall(d)[0].strip()
                                referer = '%s?ep=%s' %(referer,episode_id)
                                self.GetLinks(list, media_id, episode_id, server, referer)

                except:pass




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import re
                
        name = self.CleanTextForSearch(name.lower())
        if name == 'agents of shield':
            name = 'agents'
        search =  '%s/search/%s' %(self.base_url,str(name).replace(' ','+'))
        link = self.open_url(search).content
        links = link.split('"movie-item"')[1:]

        for p in links:

            try:

                media_url = re.compile('a href="([^"]+)"',re.DOTALL).findall(p)[0]
                media_title = re.compile('title="([^"]+)"',re.DOTALL).findall(p)[0]
                if type == 'tv_episodes':
                    if name in self.CleanTextForSearch(media_title.lower()):
                        if 'season %s' %season in media_title.lower() or name == 'iron fist':
                            self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type, year, name)
                else:
                    if name in self.CleanTextForSearch(media_title.lower()):
                        self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type, year, name)

            except:pass
            
                
                
