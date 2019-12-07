'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class onlinemovies(MovieSource):
    implements = [MovieSource]
    
    name = "Online Movies"
    display_name = "Online Movies"

    base_url='http://theonlinemovies.pro'
    
    source_enabled_by_default = 'false'
    
    
    def GetFileHosts(self, url, list, lock, message_queue,res):

            
        self.AddFileHost(list, res, url)

        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re
        from entertainment.net import Net

        from entertainment import bing
        
        net = Net(cached=False)
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        
        search_term = name + ' '+year
        RESULT_TERM = 'Watch %s (%s) Full HD' % (name,year)    
        try:GOOGLED = self.GoogleSearch('theonlinemovies.pro', search_term)
        except:GOOGLED = bing.Search('theonlinemovies.pro', search_term)

       
        uniques =[]
        for result in GOOGLED:
            movie_url= result['url']
            TITLE = result['title']
            if RESULT_TERM.lower() in TITLE.lower():

                if 'full-hd-movie-online' in movie_url:
                    from entertainment import cloudflare            
                    content = cloudflare.solve(movie_url,UA='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.3')
                              
                    
                    match=re.compile("iframe.php\?ref=(.+?)&").findall(content)
                    
                   
                    for ID in match:
                        

                        self.GetFileHosts('http://videomega.tv/iframe.php?ref='+ID, list, lock, message_queue,'HD')



 
        
