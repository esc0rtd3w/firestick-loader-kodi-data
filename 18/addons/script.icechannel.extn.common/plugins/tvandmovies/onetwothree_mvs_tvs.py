'''
    Ice Channel
    onetwothree
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os



class onetwothree(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "123Movies"
    display_name = "123Movies"
    #base_url = 'https://123movies.is'

    UA ='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    
    profile_path = common.profile_path
    cookie_file = os.path.join(profile_path, 'cookies', '123moviesNEW.cookies')

    source_enabled_by_default = 'true'


                    
    def GrabAdditional(self, url, list,episode,type):


        REF=url

        from entertainment import requests

        import re,json,hashlib,urllib
      
        
        
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':REF,'Host':'123moviesfree.com'}
        
      
        LINK = requests.get(url,headers=headers,verify=False).content
        #net.save_cookies(self.cookie_file)

        headers={'Host':'123moviesfree.com',
                'Accept':'*/*',
                'Origin':'http://123moviesfree.com',
                'X-Requested-With':'XMLHttpRequest',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer':REF,
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8'}

        uniques=[]
        if type == 'tv_episodes':
            match=re.compile('<a class="episode_(.+?) .+?" href="(.+?)".+?data-film="(.+?)".+?data-name="(.+?)"',re.DOTALL).findall(LINK)
            
            for EP,ip_server , ip_film ,ip_name in match:

                if episode == EP:
                    if ip_server not in uniques:
                        uniques.append(ip_server) 
                        REF=ip_server

                        LINK = requests.get(ip_server,headers=headers,verify=False).content
                  
                        headers={'Host':'123moviesfree.com',
                                'Accept':'*/*',
                                'Origin':'http://123moviesfree.com',
                                'X-Requested-With':'XMLHttpRequest',
                                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                                'Referer':REF,
                                'Accept-Encoding':'gzip, deflate',
                                'Accept-Language':'en-US,en;q=0.8'}
                        
                        match=re.compile('ip_build_player\((.+?),(.+?),(.+?),(.+?)\)').findall(LINK)
            
                        for ip_film ,ip_server  ,ip_name , fix in match:
                            ip_name=ip_name.replace("'",'')
                            ip_server=ip_server.replace("'",'')
                            data={'ipplugins':'1',
                                'ip_film':ip_film,
                                'ip_server':ip_server,
                                'ip_name':ip_name,
                                'fix':fix}

                            LOAD =requests.post('http://123moviesfree.com/ip.file/swf/plugins/ipplugins.php',data,headers=headers,verify=False).content
                            LINKS=json.loads(str(LOAD))

                            s=LINKS['s']
                            NEW_URL='http://123moviesfree.com/ip.file/swf/ipplayer/ipplayer.php?u=%s%s%s&n=0' % (s,'&w=100%25&h=500&s=',ip_server)
                            LINKED =json.loads(requests.get(NEW_URL,headers=headers,verify=False).content)
                            DATA=LINKED['data']
                            
                            if not 'google' in str(LINKED):
                                FINAL_URL =DATA
                                res ='720P'
                                HOST=FINAL_URL.split('//')[1]
                                HOST=HOST.split('/')[0]  

                                self.AddFileHost(list, res, FINAL_URL,host=HOST.upper())
                                
                            else:
                                
                                
                                for field in DATA:
                                    FINAL_URL =field['files']
                                    res =field['quality']

                                    res=res.replace('p','').replace('P','').replace('CAM','360')
                                    if not res.isdigit():
                                        res='720'

                                    if res =='1080':
                                        res='1080P'
                                    elif res =='720':
                                        res='720P'
                                    elif res =='480':
                                        res='DVD'
                                    elif res =='360':
                                        res='SD'

                                    else:
                                        res='SD'

                                    HOST=FINAL_URL.split('//')[1]
                                    HOST=HOST.split('/')[0]  

                                    self.AddFileHost(list, res, FINAL_URL,host=HOST.upper())


                    
        else:
            match=re.compile('ip_build_player\((.+?),(.+?),(.+?),(.+?)\)',re.DOTALL).findall(LINK)

            for ip_film ,ip_server  ,ip_name , fix in match:
                ip_name=ip_name.replace("'",'')
                ip_server=ip_server.replace("'",'')
                data={'ipplugins':'1',
                    'ip_film':ip_film,
                    'ip_server':ip_server,
                    'ip_name':ip_name,
                    'fix':fix}

                LOAD =requests.post('http://123moviesfree.com/ip.file/swf/plugins/ipplugins.php',data,headers=headers,verify=False).content
                LINKS=json.loads(str(LOAD))

                s=LINKS['s']
                NEW_URL='http://123moviesfree.com/ip.file/swf/ipplayer/ipplayer.php?u=%s%s%s&n=0' % (s,'&w=100%25&h=500&s=',ip_server)
                LINKED =json.loads(requests.get(NEW_URL,headers=headers,verify=False).content)
                DATA=LINKED['data']
                
                if not 'google' in str(LINKED):
                    FINAL_URL =DATA
                    res ='720P'
                    HOST=FINAL_URL.split('//')[1]
                    HOST=HOST.split('/')[0]  

                    self.AddFileHost(list, res, FINAL_URL,host=HOST.upper())
                    
                else:
                    
                    
                    for field in DATA:
                        FINAL_URL =field['files']
                        res =field['quality']
                 
                        if not '.srt' in FINAL_URL:
                            res=res.replace('p','').replace('P','').replace('CAM','360')
                            if not res.isdigit():
                                res='720'

                            if res =='1080':
                                res='1080P'
                            elif res =='720':
                                res='720P'
                            elif res =='480':
                                res='DVD'
                            elif res =='360':
                                res='SD'

                            else:
                                res='SD'

                            HOST=FINAL_URL.split('//')[1]
                            HOST=HOST.split('/')[0]  

                            self.AddFileHost(list, res, FINAL_URL,host=HOST.upper())


    def GetFileHosts(self, url, list, lock, message_queue, season, episode,type,year,again):


        REF=url

        from entertainment import requests

        import re,json

       
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':REF,'Host':'123moviesfree.com'}
        
      
        LINK = requests.get(url,headers=headers,verify=False).content
        #net.save_cookies(self.cookie_file)

        headers={'Host':'123moviesfree.com',
                'Accept':'*/*',
                'Origin':'http://123moviesfree.com',
                'X-Requested-With':'XMLHttpRequest',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer':REF,
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8'}

        #uniques=[REF]

        LINK2=re.compile('server_servername.+?href="(.+?)"',re.DOTALL).findall(LINK)
        for NEW_URL in LINK2:
            self.GrabAdditional(NEW_URL, list,episode,type)



                            
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment import requests

        import re
        
        season_pull = "0%s"%season if len(season)<2 else season
        
        
        
        title = self.CleanTextForSearch(title) 
        query = self.CleanTextForSearch(name).lower()
        #print ':::::::::::::::::::::::::::::::::'
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Referer':'http://123moviesfree.com/','Host':'123moviesfree.com'}
                
        url='http://123moviesfree.com/movie/search/' + str(query).replace(' ','+')+'.html'

        #net.set_cookies(self.cookie_file)
        LINK=requests.get(url,headers=headers,verify=False).content

                              
        LINK = LINK.split('ml-item')
        for p in LINK:
            try:
               movie_url=re.compile('href="(.+?)"').findall(p)[0]
               name=re.compile('title="(.+?)"').findall(p)[0]

               if type == 'tv_episodes':
                   if query.lower() in self.CleanTextForSearch(name.lower()):                
                       if 's'+season_pull in name.lower():
                           self.GrabAdditional(movie_url, list,episode,type)
                        
               else:
                   if query.lower() == self.CleanTextForSearch(name.lower()):
                       self.GrabAdditional(movie_url, list,episode,type)

            except:pass


                        
            



