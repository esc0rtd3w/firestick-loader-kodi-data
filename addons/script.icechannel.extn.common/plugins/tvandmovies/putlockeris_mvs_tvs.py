from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common

class putlockeris(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "putlocker.is"
    display_name = "Putlocker.is"
    source_enabled_by_default = 'false'
    
    def GetFileHosts(self, url, list, lock, message_queue,season,episode,type):
        import re
        import decrypter
        from entertainment.net import Net
        net = Net(cached=False)

        if type=='tv_episodes':
            url=self.GetTvFileHosts(url,season,episode)
           
        movielink = net.http_GET(url).content

        links=re.compile('rel=".+?" href="(.+?)" target="_blank" title=".+?">Version .+?</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.+?').findall(movielink)        
        for url in links:
            hostname=re.compile('http://(.+?)/').findall(url)
            host = str(hostname).replace('www.','')
            res='SD'
            self.AddFileHost(list, res, url)



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re, urllib
        from entertainment.net import Net
        net = Net(cached=False)
        name = self.CleanTextForSearch(name)
        helper ='%s (%s)' %(name, year)
        name = urllib.quote(name)
        search_url = 'http://putlockertv.is/search/search.php?q=' + name
        #print search_url
        content = net.http_GET(search_url).content
        search_res = re.split('Search Results For: "<font color=red>', content)[1]
        match = re.compile('href="(.+?)" title="(.+?)"').findall(search_res)
        for url, title in match:
            if type=='tv_episodes':
                if name.lower() in self.CleanTextForSearch(title.lower()):
                    self.GetFileHosts(url, list, lock, message_queue,season,episode,type)
            if title == helper or title == helper.replace(':',' 2:'):
                self.GetFileHosts(url, list, lock, message_queue,season,episode,type)
                

    def GetTvFileHosts(self, url,season,episode):
        import re
        from entertainment.net import Net
        net = Net(cached=False)

        movielink = net.http_GET(url).content
        link=movielink.split('<!-- AddThis Button END -->')[1]
        links=re.compile('href="(.+?)"').findall(link)        
        for URL in links:


            r='season-%s-episode-%s' % (season,episode)

            if r in URL:
               
               return URL


