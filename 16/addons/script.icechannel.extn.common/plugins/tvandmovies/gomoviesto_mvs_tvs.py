'''
    Ice Channel
    buzzfilms.co
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os



class gomovies(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "GoMovies"
    display_name = "GoMovies"
    #base_url = 'https://123movies.is'

    UA ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', 'gomoviesNEW.cookies')

    source_enabled_by_default = 'true'




    def __uncensored1(self, script):
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
        except Exception as e:
            xbmc.log('Exception in x/y decode (1)')
        return {'x': x, 'y': y}




    def __uncensored2(self, script):
        import jsunfuck
        import re,xbmc
        try:
            js = jsunfuck.JSUnfuck(script).decode()
            x = re.search('''_x=['"]([^"']+)''', js).group(1)
            y = re.search('''_y=['"]([^"']+)''', js).group(1)
            return {'x': x, 'y': y}
        except Exception as e:
            xbmc.log('Exception in x/y decode (2)')




    def __uncensored3(self, script):
        import re,xbmc
        try:
            xx = re.search('''_x=['"]([^"']+)''', script).group(1)
            xy = re.search('''_y=['"]([^"']+)''', script).group(1)
            return {'x': xx, 'y': xy}
        except Exception as e:
            xbmc.log('Exception in xx/xy decode (3)')
    

    

    def GetFileHosts(self, url, list, lock, message_queue, season, episode,type,year,query,base_url):

        THEHOST=url.split('//')[1]
        THEHOST=THEHOST.split('/')[0]

        REF=url

        from entertainment import requests
        requests.packages.urllib3.disable_warnings()
        
        import re,json,urllib,time
       
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':base_url + ''}
        
      
        LINK = requests.get(url,headers=headers,verify=False).content
        #net.save_cookies(self.cookie_file)
        User_Agent ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        
        try:media_id = re.compile('name="movie_id" value="(.+?)"').findall(LINK)[0]
        except:media_id = re.compile('id: "(.+?)"').findall(LINK)[0]
        


        headers = {'Accept': 'image/webp,image/*,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br',
                   'Accept-Language': 'en-US,en;q=0.8', 'Referer': REF, 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



        
        #net.set_cookies(self.cookie_file)
        LOAD =requests.get(base_url + 'ajax/movie_episodes/%s'%(media_id),headers=headers,verify=False).content.replace('\\','')
        LOAD=LOAD.replace('Episode 0','Episode ')
        link=LOAD.split('<div id="sv-')
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':base_url + ''}
      
        for p in link:

            #try:
                
                res ='720P'
               
                    

                if type == 'tv_episodes':
                        server=p.split('"')[0]
                        HTML=p.split('<a title="')
                        
                        for d in HTML:
                            try:
                           
                                if ' '+episode+':' in d.lower():

                                    episode_id=re.compile('id="ep-(.+?)"').findall(d)[0]
                                    time_now = int(time.time() * 10000)



                                    if int(server) > 10:
                                        try:
                                            HEADERS={'Accept':'application/json, text/javascript, */*; q=0.01',
                                                    'X-Requested-With':'XMLHttpRequest',
                                                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                                                    'Referer':REF+'?ep='+episode_id,
                                                    'Accept-Encoding':'gzip, deflate, sdch, br','HOST':THEHOST}
                                            
                                            URL=base_url + '/ajax/load_embed/%s' % (episode_id)
                                            HTML1=requests.get(URL,headers=HEADERS,verify=False).content
                                            HTML2 = json.loads(HTML1)
                                            FINAL_URL = HTML2['embed_url']
                                            if '720p' in FINAL_URL.lower():
                                                res='720P'
                                            if '1080p' in FINAL_URL.lower():
                                                res='1080P'
                                            else:
                                                res='720P'                                                

                                            self.AddFileHost(list, res, FINAL_URL)
                                        except:pass
                                    else:
                                        

                                        try:

                                            slug = '%sajax/movie_token' %base_url
                                            params = {'eid':episode_id, 'mid':media_id, '_':time_now}
                                            headers = {'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                                                       'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8',
                                                       'Referer':REF+'?ep='+episode_id, 'User-Agent':User_Agent, 'X-Requested-With':'XMLHttpRequest','HOST':THEHOST}
                                            data = requests.get(slug, params=params, headers=headers).content

                                            if '$_$' in data:
                                                params = self.__uncensored1(data)
                                            elif data.startswith('[]') and data.endswith('()'):
                                                params = self.__uncensored2(data)
                                            else:
                                                params = self.__uncensored3(data)
                                                
                                            if params is None:
                                                params = {}

                                            if 'x' in params:
                                                
                                                request_url2 = '%sajax/movie_sources/%s' %(base_url,episode_id)
                                                headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                                                           'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8',
                                                           'Referer':REF+'?ep='+episode_id, 'User-Agent':User_Agent, 'X-Requested-With':'XMLHttpRequest','HOST':THEHOST}
                                                HTML2 = requests.get(request_url2, params=params, headers=headers,verify=False).json()
                                                DATA=HTML2['playlist'][0]['sources']
                                                for field in DATA:
                                                    FINAL_URL= field['file']
                                                    res= field['label']#.upper()
                                                
                               
                                                    if not '.srt' in FINAL_URL:
                                                        res=res.replace('p','').replace('P','').replace('CAM','360')
                                                        if not res.isdigit():
                                                            res='720'

                                                        if res =='360':
                                                            res='SD'
                                                        if res =='480':
                                                            res='DVD'
                                                        if res =='720':
                                                            res='720P'
                                                        if res =='1080':
                                                            res='1080P'
                                                          

                                                        HOST=FINAL_URL.split('//')[1]
                                                        HOST=HOST.split('/')[0]  
                                                        

                                                        

                                                        self.AddFileHost(list, res, FINAL_URL,host=HOST.upper())                            
                                        except:pass

                            except:pass                                    
                else:
                        server=p.split('"')[0]
                        
                        HTML=p.split('<a title="')
                        
                        for d in HTML:
                            try:

                                YEAR=re.compile('Release:</strong>(.+?)<').findall(LINK)[0].strip()
                                THETITLE=re.compile('"og:title" content="(.+?)"').findall(LINK)[0].strip()
                                if not year:
                                    if query.lower() in THETITLE.lower():
                                        PASS=True
                                else:        
                                    if year == YEAR:
                                        PASS=True
                                if PASS==True:


                                    episode_id=re.compile('id="ep-(.+?)"').findall(d)[0]
                                    time_now = int(time.time() * 10000)


                                    
                                    if int(server) > 10:
                                        
                                        HEADERS={'Accept':'application/json, text/javascript, */*; q=0.01',
                                                'X-Requested-With':'XMLHttpRequest',
                                                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                                                'Referer':REF+'?ep='+episode_id,
                                                'Accept-Encoding':'gzip, deflate, sdch, br','HOST':THEHOST}
                                        URL=base_url + 'ajax/load_embed/%s' % (episode_id)

                                        EMBEDHTML=requests.get(URL,headers=HEADERS,verify=False).content
                                        THEEMBED=json.loads(EMBEDHTML)
                                        FINAL_URL = THEEMBED['embed_url']
                                       
                                        if '720p' in FINAL_URL.lower():
                                            res='720P'
                                        elif '1080p' in FINAL_URL.lower():
                                            res='1080P'
                                        else:
                                            res='HD'                                                

                                        self.AddFileHost(list, res, FINAL_URL)
                                    else:

                                        try:
                                            
                                            slug = '%sajax/movie_token' %base_url
                                            params = {'eid':episode_id, 'mid':media_id, '_':time_now}
                                            headers = {'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                                                       'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8',
                                                       'Referer':REF+'?ep='+episode_id, 'User-Agent':User_Agent, 'X-Requested-With':'XMLHttpRequest','HOST':THEHOST}
                                            data = requests.get(slug, params=params, headers=headers).content

                                            if '$_$' in data:
                                                params = self.__uncensored1(data)
                                            elif data.startswith('[]') and data.endswith('()'):
                                                params = self.__uncensored2(data)
                                            else:
                                                params = self.__uncensored3(data)
                                                
                                            if params is None:
                                                params = {}

                                            if 'x' in params:
                                                
                                                request_url2 = '%sajax/movie_sources/%s' %(base_url,episode_id)
                                                headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
                                                           'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-US,en;q=0.8',
                                                           'Referer':REF+'?ep='+episode_id, 'User-Agent':User_Agent, 'X-Requested-With':'XMLHttpRequest','HOST':THEHOST}
                                                HTML2 = requests.get(request_url2, params=params, headers=headers,verify=False).json()
                                                DATA=HTML2['playlist'][0]['sources']

                                                
                                                for field in DATA:
                                                    FINAL_URL= field['file']
                                                    res= field['label']#.upper()
                                                
                                                #if 'google' in FINAL_URL or 'blogspot' in FINAL_URL or '123movies.ru' in FINAL_URL:                             
                                                    if not '.srt' in FINAL_URL:
                                                        res=res.replace('p','').replace('P','').replace('CAM','360')
                                                        if not res.isdigit():
                                                            res='720'
                                                        #print res
                                                        #res=int(res)
                                                        #print res
                                                        if res =='360':
                                                            res='SD'
                                                        if res =='480':
                                                            res='DVD'
                                                        if res =='720':
                                                            res='720P'
                                                        if res =='1080':
                                                            res='1080P'
                                                          

                                                        HOST=FINAL_URL.split('//')[1]
                                                        HOST=HOST.split('/')[0]  
                                                        

                                                        

                                                        self.AddFileHost(list, res, FINAL_URL,host=HOST.upper()) 
                                        except:pass 
                            except:pass

                            


    def GetDomain(self):                 
        
        from entertainment import requests
        requests.packages.urllib3.disable_warnings()

        headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'}
        url = ['https://gomovies.tech/']
        
        for URL in url:
            HOST=URL.split('//')[1]

            try:
               hello = requests.get(URL,headers=headers,verify=False).content
               if HOST in hello:
                   return URL
            except:pass 

            
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment import requests
        requests.packages.urllib3.disable_warnings()

        import re

        base_url = self.GetDomain()
      
        title = self.CleanTextForSearch(title) 
        query = self.CleanTextForSearch(name)
        #print ':::::::::::::::::::::::::::::::::'
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':base_url}
                
        url=base_url + 'movie/search/' + str(query).replace(' ','+')

        #net.set_cookies(self.cookie_file)
        LINK=requests.get(url,headers=headers,verify=False).content

                              
        LINK = LINK.split('"ml-item">')
        for p in LINK:
            try:
               movie_url=re.compile('a href="(.+?)"',re.DOTALL).findall(p)[0]
               name=re.compile('title="(.+?)"',re.DOTALL).findall(p)[0]         

               movie_url=movie_url+'watching.html'
               if type == 'tv_episodes':
                   if query.lower() in self.CleanTextForSearch(name.lower()):                
                       if 'Season '+season in name:
                           self.GetFileHosts(movie_url, list, lock, message_queue,season, episode,type,year,query,base_url)
                        
               else:
                   if query.lower() in self.CleanTextForSearch(name.lower()):
                       self.GetFileHosts(movie_url, list, lock, message_queue,season, episode,type,year,query,base_url)

            except:pass

                    
            



                
                
