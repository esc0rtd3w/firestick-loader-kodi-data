'''
    MvGee
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin



class bobby(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "mvgee"
    display_name = "MvGee"

    source_enabled_by_default = 'true'
    BASE ='http://mvgee.com'



        
    def GetFileHosts(self, url, list, lock, message_queue,type,REF):

    
        import json
        from entertainment.net import Net
        net = Net(cached=False)


        headers={'Host':'mvgee.com',
                'Accept':'text/plain, */*; q=0.01',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'Accept-Language':'en-US,en;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Referer':REF}

        
       
        
        link = net.http_GET(url,headers=headers).content
        link = json.loads(link)

        data=link['streams']

        for field in data:
            RES=field['label']
            URL =field['src']
            
           
            
            if '720' in RES:
                res='720P'
            elif '360' in RES:
                res='SD'                    
            elif '1080' in RES:
                res='1080P'
            elif '480' in RES:
                res='HD'
            else:
                res='HD'
            
            FINAL_URL=URL.split('//')[1]
            FINAL_URL=FINAL_URL.split('/')[0]
            

            self.AddFileHost(list, res, URL,host=FINAL_URL.upper())

        
                    
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
    
        import re,json
        from entertainment.net import Net
        net = Net(cached=False)
        seasonshit = "0%s"%season if len(season)<2 else season
        episodeshit = "0%s"%episode if len(episode)<2 else episode
        name=self.CleanTextForSearch(name.lower())
        
        headers={'Host':'mvgee.com',
                'Accept':'text/plain, */*; q=0.01',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'Accept-Language':'en-US,en;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch'}

        new_url='http://mvgee.com/search?q='+name.replace(' ','+')
        
        link = net.http_GET(new_url,headers=headers).content
     
        link=json.loads(link)
        data=link['suggestions']
       
        for field in data:
            TITLE=field['value']
            URL =field['data']['href']
            IMAGE=field['data']['image']
            
   
            imdb =re.compile('(tt[0-9]+?)(_|-.+?)').findall(IMAGE)[0][0]
            
            if type=='tv_episodes':
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                      if season in TITLE:

                         THEJSON = 'http://mvgee.com/io/1.0/stream?imdbId=%s&season=%s&provider=gd&name=s%se%s' % (imdb,season,seasonshit,episodeshit)

                         self.GetFileHosts(THEJSON, list, lock, message_queue,type,self.BASE+URL)
            else:
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                    if year in TITLE:
                        THEJSON = 'http://mvgee.com/io/1.0/stream?imdbId=%s&season=0&provider=gd&name=720p' % imdb
                        
                        self.GetFileHosts(THEJSON, list, lock, message_queue,type,self.BASE+URL)


                

    def Resolve(self, url):                 
        url=url.replace('amp;','')
        if 'requiressl=yes' in url:
            url = url.replace('http://', 'https://')
        from entertainment import istream
        resolved =istream.ResolveUrl(url)
        return resolved  



                
    




            
