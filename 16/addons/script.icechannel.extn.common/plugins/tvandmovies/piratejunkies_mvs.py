'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class onlinemovies(MovieSource):
    implements = [MovieSource]
    
    name = "PirateJunkies"
    display_name = "Pirate Junkies"

    base_url='http://piratejunkies.com/javascript/movies.js'
    
    source_enabled_by_default = 'true'
    
    
    def GetFileHosts(self, url, list, lock, message_queue,res):

        url=self.grabURL(url)    
        self.AddFileHost(list, '1080P', url)

        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        import re
        from entertainment.net import Net

        from entertainment import bing
        
        net = Net(cached=False)
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)

        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.3'}
     
        html = net.http_GET(self.base_url,headers=headers).content

       
        match=re.compile('getElementById\("(.+?)"\).+?"play\(\'(.+?)\'').findall(html)

        for TITLE , URL in match:
            NAME = name.replace(' ','').lower()
            if NAME in TITLE.lower():
                self.GetFileHosts(URL, list, lock, message_queue,'720P')



    def googletag(self,url):
        import re

        url=re.compile('\|(.+?)\,').findall(url)[0]

        quality = re.compile('itag=(\d*)').findall(url)
        quality += re.compile('=m(\d*)$').findall(url)
        try: quality = quality[0]
        except: return ''

        if quality in ['37', '137', '299', '96', '248', '303', '46']:
            return url
        elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
            return url
        elif quality in ['35', '44', '135', '244', '94']:
            return url
        

 
    def grabURL(self, url):
        from entertainment.net import Net

        import re,json
        net = Net(cached=False,user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.3')

        if '/preview' in url:
                url = url.replace('drive.google.com', 'docs.google.com')
                #print url
                LINK=net.http_GET(url).content
                result = re.compile('"fmt_stream_map",(".+?")').findall(LINK)[0]
                
                result = json.loads(result)

                match = self.googletag(result)

                return match
        else:
            from entertainment import istream
            resolved =istream.ResolveUrl(url)
            return resolved                  
