
'''
    Istream
    tv-release.net
    Copyright (C) 2013 the-one, voinage, Jas0npc, Coolwave

    version 0.2

    0/01/2014 improved regex for GetFileHostsForContent results.
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin

class Tvrelease(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    name = "Tvrelease"
    display_name = "TV-Release"
    base_url = 'http://tv-release.pw'
    source_enabled_by_default = 'false'

    def GetFileHosts(self, url, list, lock, message_queue):
        from entertainment.net import Net
        import re

        net = Net(cached=False)
        sources = []
        THENAME=url
        content = net.http_GET(url).content
        links = re.compile(r'\'_blank\'\shref=\'(.+?)\'\>', re.I|re.M|re.DOTALL).findall(content)
          
        for url in links:
            
            if 'HD' in THENAME.upper():
                res = 'HD'
            elif '720p' in THENAME.lower():
                res = '720P'
            elif '1080p' in THENAME.lower():
                res = '1080P'
            elif 'brrip' in THENAME.lower():
                res = '1080P'
            elif 'dvdrip' in THENAME.lower():
                res = 'DVD'  
            else:
                res='SD'
            if not '.rar' in url or not 'go4up' in url:
               
                self.AddFileHost(list,res,url)


    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        from entertainment.net import Net
        import re

        net = Net(cached=False)
        
        seasonshit = "0%s"%season if len(season)<2 else season
        episodeshit = "0%s"%episode if len(episode)<2 else episode
        valid_constructor='S%sE%s'%(seasonshit,episodeshit)
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)


        if type == 'tv_episodes':
        
            search_url_digit = "%s/?s=%s%sS%sE%s&cat=&cat=TV-XviD,TV-Mp4,TV-720p,TV-480p," % (self.base_url, name.replace(' ','+').lower(),
                                                          '%20', seasonshit, episodeshit)
        else:
            search_url_digit = "%s/?s=%s+%s&cat=Movies-XviD,Movies-720p,Movies-480p,Movies-Foreign,Movies-DVDR,"%(self.base_url,name.replace(' ','+').lower(),year)

        content = net.http_GET(search_url_digit).content
        match=re.compile("<a href='http://tv-release.pw/(\d*\/.+?)'").findall(content)
        
        for url in match:
            self.GetFileHosts(self.base_url+'/'+url, list, lock, message_queue)
