'''
    http://afdah.com/    
    Copyright (C) 2013 Mikey1234
'''


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch



class indexof(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Index_Of"
    display_name = "Index Of"
    source_enabled_by_default = 'false'
    icon = common.notify_icon
    
        
    def GetFileHosts(self, url, list, lock, message_queue):
        if '4k' in url.lower():
            quality ='4K'
            
        elif '3d' in url.lower():
            quality ='3D'
                        
        elif '1080' in url:
            quality ='1080P'
        elif '720' in url:
            quality ='720P'
        elif 'hd' in url:
            quality ='HD'     
        else:           
            quality='DVD'
        self.AddFileHost(list, quality, url)
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False,user_agent='/Apple iPhone')
        name = self.CleanTextForSearch(name)

        SS = "0%s"%season if len(season)<2 else season
        EE = "0%s"%episode if len(episode)<2 else episode
        
        search_term = name.lower()
        theyear='+'+year
        if type == 'tv_episodes': 
            search_term = name.lower()+'+'+'S'+SS+'E'+EE
            theyear=''
        helper_term = ''
        ttl_extrctr = ''
        
        


        search = 'https://www.google.com/search?q=index+of+%s%s'  % (search_term.replace(' ','+'),theyear)
        
        contents= net.http_GET(search).content
        match1=re.compile('<a href="\/url\?q=(.+?)&.+?">(.+?)</a>').findall(contents)
        for movie_url , NAME in match1:
            try:
                movie_url=movie_url.replace('%2520','%20')
                if 'index of /' in NAME.replace('<b>','').replace('</b>','').lower():             
                    content= net.http_GET(movie_url).content
                   
                    match=re.compile('href="(.+?)"').findall(content)
                    for URL in match:
                        if not 'http' in URL:
                            MOVIE =movie_url+URL
                            if MOVIE[-4]=='.':
                                CLEANURL=URL.replace('%20','.').lower()
                                if type == 'tv_episodes':
                                 
                                    if name.lower().replace(' ','.') in CLEANURL.replace(' ','.'):
                                        if 's'+SS in CLEANURL.replace(' ',''):
                
                                            if 'e'+EE in CLEANURL.replace(' ',''):
                        
                                                self.GetFileHosts(MOVIE, list, lock, message_queue)
                                       
                                else:       
                                    if search_term.replace(' ','.') in CLEANURL.replace(' ','.'):
                                        
                                        if year in MOVIE.lower():
                                            self.GetFileHosts(MOVIE, list, lock, message_queue)
            except:pass


    def Resolve(self, url):

        return url
