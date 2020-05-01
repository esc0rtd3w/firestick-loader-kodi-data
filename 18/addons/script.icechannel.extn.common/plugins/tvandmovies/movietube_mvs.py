'''
    Ice Channel
    Copyright (C) 2013 the-one, Mikey1234, Coolwave
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

do_no_cache_keywords_list = ['Sorry for this interruption but we have detected an elevated amount of request from your IP']

class MovieTube(MovieSource):
    implements = [MovieSource]
    
    name = "MovieTube"
    display_name = "MovieTube"
    cookie_file = os.path.join(common.cookies_path, 'movietube')
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue):

        
        self.AddFileHost(list, '720P', url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        new_url = 'http://www.movie-tube.co/index.php'
        import re
        from entertainment.net import Net
        
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        if os.path.exists(self.cookie_file):
                try: os.remove(self.cookie_file)
                except: pass
                
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36','Origin':'http://www.movie-tube.co','Referer':'http://www.movie-tube.co','Host':'www.movie-tube.co', 'X-Requested-With':'XMLHttpRequest','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        form_data={'query':name}
        content = net.http_POST('http://www.movie-tube.co/engine/ajax/search.php', form_data, headers).content


           
        
        match=re.compile('href="(.+?)"><span class="searchheading">(.+?)</',re.DOTALL).findall(content)


        for url,TITLE in match:
            if name in self.CleanTextForSearch(TITLE):
                self.GetFileHosts(url, list, lock, message_queue)
                    

    def Resolve(self, url):
        import re        
        from entertainment.net import Net

        net = Net(cached=False)
        
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36','Origin':'http://www.movie-tube.co','Referer':'http://www.movie-tube.co/','Host':'www.movie-tube.co', 'X-Requested-With':'XMLHttpRequest','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}        
        content = net.http_GET(url,headers=headers).content
     
        match=re.compile('frameborder="0" src="(.+?)"').findall(content)[0]
        #print '############################################'
        #print match
        from entertainment import istream
        play_url = istream.ResolveUrl(match)
        return play_url


        

        
                                                
