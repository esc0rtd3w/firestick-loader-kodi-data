'''
    watchmoviespro
    Copyright (C) 2014 Coolwave
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

do_no_cache_keywords_list = ['Sorry for this interruption but we have detected an elevated amount of request from your IP']

class watchmoviespro(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "movietvhub"
    display_name = "movietvhub"
    cookie_file = os.path.join(common.cookies_path, 'movietvhub.lwp')
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue,REF):
        import re
        from entertainment.net import Net
        net = Net(cached=False)

        headers={'Host':'123movies4u.net',
                 'Origin':'https://123movies4u.net',
                 'Referer':REF,
                 'Connection':'keep-alive',
                 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}        
   
        content = net.http_GET(url,headers=headers).content
     
             #onclick=\"window.open\('(.+?)', '_blank'\);\">(.+?)  (.+?)</a>
        #r = 'SRC="(.+?)" target="_blank">Play Now<'

        link=content.split('embeds[')

        for p in link:
            try:
                URL  = 'http'+re.compile('http(.+?)"').findall(p)[0]
                uniques=[]
                if not '123movies4u' in URL:
                    if URL not in uniques:
                        uniques.append(URL)
                        self.AddFileHost(list, 'SD', URL)
            except:pass    
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        import re,json,time
        from entertainment.net import Net
        
        net = Net(cached=False)
        
        if os.path.exists(self.cookie_file):
                try: os.remove(self.cookie_file)
                except: pass
                
        time=time.time()
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        REF='https://123movies4u.net/index.php?menu=search&query='+name.replace(' ','+')
        headers={'Host':'123movies4u.net',
                 'Origin':'https://123movies4u.net',
                 'Referer':REF,
                 'Connection':'keep-alive',
                 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

        
        form_data={'q':name,'limit':'5','timestamp':str(time).split('.')[0],'verifiedCheck':''}
        
        content = net.http_POST('https://123movies4u.net/ajax/search.php',form_data, headers).content
        
        data=json.loads(content)
        
        for field in data:
            movie_url=field['permalink']
            _name=field['title']
            if type == 'tv_episodes':
                
                if name.lower() in self.CleanTextForSearch(_name.lower()):
                        movie_url=movie_url+'/season/%s/episode/%s' % (season,episode)
                        self.GetFileHosts(movie_url, list, lock, message_queue,REF)
            else:        
                if name.lower() in self.CleanTextForSearch(_name.lower()):
                    self.GetFileHosts(movie_url, list, lock, message_queue,REF)
                    

    
    def Resolve(self, url):
        

        from entertainment import istream
        play_url = istream.ResolveUrl(url)
        return play_url
