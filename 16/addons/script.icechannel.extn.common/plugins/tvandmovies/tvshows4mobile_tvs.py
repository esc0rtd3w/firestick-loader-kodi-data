'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch

class tvshows4mobile(TVShowSource):
    implements = [TVShowSource]
    
    name = "tvshows4mobile"
    display_name = "TvShows4Mobile"
    base_url = 'http://tvshows4mobile.com'
    
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue): 
    
        import re        
        from entertainment.net import Net
        net = Net(cached=False)
        
        content = net.http_GET(url).content
                
        media_url = re.compile('<a href="(.+?)">(.+?)</a> <span class="count">.+?Downloads\)</span>',re.DOTALL).findall(content)
        for show,codec in media_url:
            if codec.endswith('mp4'):
                self.AddFileHost(list, 'SD', show)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        

        import re        
        from entertainment.net import Net
        net = Net(cached=False)
        content = net.http_GET('http://tvshows4mobile.com/search/list_all_tv_series').content

        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        match=re.compile('<a href="http://tvshows4mobile.com/(.+?)/index.html">(.+?)</a>').findall(content)
        
        for url, NAME in match:
            if name.lower() in NAME.lower():
 
                if len(episode)< 2:
                    episode = '0'+episode.replace(' ','-')
                if len(season)< 2:
                    season = '0'+season.replace(' ','-')    
                season='Season-'+season
                episode='Episode-'+episode
                tv_url='http://tvshows4mobile.com/%s/%s/%s/index.html'%(url,season,episode)
                
                self.GetFileHosts(tv_url, list, lock, message_queue)
                    
            
    def Resolve(self, url):

        return url
            
                
