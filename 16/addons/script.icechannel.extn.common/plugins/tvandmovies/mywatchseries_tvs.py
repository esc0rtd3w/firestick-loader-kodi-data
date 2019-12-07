
#iStream Extension
#My Watch Series
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc


class mywatchseries(TVShowSource):

    implements = [TVShowSource]
    
    name = 'MyWatchSeries'
    display_name = 'MyWatchSeries'
    base_url = 'http://mywatchseries.to'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue, season, episode): 
        
        from entertainment import requests
        import urlresolver,re
        
        headers = {'User-Agent':self.User_Agent}
        link = requests.get(url, headers=headers, timeout=15).content
        links = link.split('<li id="episode')[1:]
        for p in links:
            media_url = re.compile('href="([^"]+)"').findall(p)[0]
            sep = 's%s_e%s' %(season, episode)
            if sep in media_url.lower():
                link2 = requests.get(media_url, headers=headers, timeout=15).content
                sources = re.findall(r'cale\.html\?r=(.*?)"', str(link2), re.I|re.DOTALL)
                uniques = []
                for hosts in sources:
                    final_url = hosts.decode('base64')
                    if urlresolver.HostedMediaFile(final_url):
                        if final_url not in uniques:
                            uniques.append(final_url)
                            self.AddFileHost(list, 'SD', final_url)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        from entertainment import requests
        import re

        name = self.CleanTextForSearch(name.lower())
        headers = {'User-Agent':self.User_Agent}
        search = '%s/search/%s' %(self.base_url,name.replace(' ','%20'))
        link = requests.get(search, headers=headers, timeout=15).content
        link = link.split('Search results')[1:]
        links = re.findall(r'<a href="([^"]+)" title=".*?" target="_blank"><strong>([^<>]*)</strong></a>', str(link), re.I|re.DOTALL)
        for media_url, media_title in links:
            if name in self.CleanTextForSearch(media_title.lower()):
                if year in media_title:
                    self.GetFileHosts(media_url, list, lock, message_queue, season, episode)
