'''
    Istream
    movie4u
    Copyright (C) 2013 Coolwave

    version 0.2

'''


from entertainment.plugnplay import Plugin
from entertainment import common

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource

class movie4u(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
	
    name = "movie4u.cc"
    source_enabled_by_default = 'true'
    display_name = "Movie4uCC"
    base_url = 'http://movie4u.cc/'
    
    def GetFileHosts(self, url, list, lock, message_queue,type,season,episode):
        import re

        from entertainment.net import Net
        net = Net(cached=False)


        headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4','Referer':'http://movie4u.cc/'}
        
        content = net.http_GET(url,headers=headers).content
        if type == 'tv_episodes':
            headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4','Referer':url}
        
            r='%sx%s/' % (season,episode)
            match=re.compile('<a href="(.+?)">').findall(content)
            for url in match:
                if r in url:
                    url=url
                    break
            content = net.http_GET(url,headers=headers).content    

            
        if 'grab.php' in content:
            
            match  = re.compile('file:"(.+?)".+?label:"(.+?)"').findall(content)
            for FINAL , quality in match:
                
                if '1080P' in quality.upper():
                    Q ='1080P'
                elif '720P' in quality.upper():
                    Q ='720P'                
                elif '480P' in quality.upper():
                    Q ='HD'
                else:
                    Q ='SD'
                
                self.AddFileHost(list, Q, FINAL)


        
        FINAL  = re.compile('metaframe rptss" src="(.+?)"',re.DOTALL).findall(content)[0]
        
        if '1080P' in FINAL.upper():
            Q ='1080P'
        elif '720P' in FINAL.upper():
            Q ='720P'                
        elif '480P' in FINAL.upper():
            Q ='HD'
        else:
            Q ='SD'
        
        self.AddFileHost(list, Q, FINAL)



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import urllib2
        import re
        from entertainment.net import Net
        net = Net(cached=False)

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)


        
        if type == 'movies':
            search='%s %s' %(name,year)
        else:
            search=name
            
        movie_url='http://movie4u.cc/?s=%s' % search.replace(' ','+')
        
        headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4','Referer':'http://movie4u.cc/'}
        
            
        html = net.http_GET(movie_url,headers=headers).content
        link=html.split('<div class="image">')

        for p in link:
            try:
                item_url=re.compile('href="(.+?)"').findall(p)[0]
                TITLE=re.compile('alt="(.+?)"').findall(p)[0]
                
                if type == 'movies':
                    if search ==self.CleanTextForSearch(TITLE):
                        self.GetFileHosts(item_url, list, lock, message_queue,type,season,episode)

                else:
                    if name in self.CleanTextForSearch(TITLE):
                        self.GetFileHosts(item_url, list, lock, message_queue,type,season,episode)
            except:pass

                        
                
