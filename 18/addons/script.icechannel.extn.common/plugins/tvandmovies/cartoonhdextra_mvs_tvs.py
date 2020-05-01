'''
    Cartoon HD Extra   
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin



class cartoonhdextra(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "CARTOONEXTRA"
    display_name = "CARTOONEXTRA"
    GETLINK='http://wowcartoon.com:8182/C4C/api/C4C/GetGenreDetail'
    HEADERS={'xKey': 'eae09beb57d6b1823e872eded0a3a054','User-Agent':'MyApp/2.2.2 (iPhone; iOS 8.4; Scale/2.00','Host': 'wowcartoon.com:8182'}

    source_enabled_by_default = 'true'
    SEARCHLINK ='http://wowcartoon.com:8182/C4C/api/C4C/FindCategory'


    

        
    def GetFileHosts(self, url, list, lock, message_queue,type,season,episode):

        if not type == 'tv_episodes':
            FINAL_URL=url.split('//')[1]
            FINAL_URL=FINAL_URL.split('/')[0]
            self.AddFileHost(list, '720P', url,host=FINAL_URL.upper())
        else:    
            import json
            from entertainment.net import Net
            net = Net(cached=False)

  

            data={'DeviceId':'6a48880da9855891b8baad7d7b34570d998b28c5',
                      'Hash':'f93e3156637c9fce37154e2d091bca8a',
                      'Key':'AA9FSK1323X3F',
                      'Id':url,
                      'PageSize':'20',
                      'StartIndex':'0',
                      'Version':'5'}

           
            link = json.loads(net.http_POST(self.GETLINK,data,headers=self.HEADERS).content)

             
            data=link['Data']
            
            for field in data:
                TITLE=field['Name'].encode('utf8')
                id=field['VideoId']
                if 'S%s Epi %s' % (season,episode) in TITLE:
                    FINAL_URL=id.split('//')[1]
                    FINAL_URL=FINAL_URL.split('/')[0]                    
                    self.AddFileHost(list, '720P', id,host=FINAL_URL.upper())

        
                    
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
    
        import json
        from entertainment.net import Net
        net = Net(cached=False)

        name=self.CleanTextForSearch(name)
        data={'DeviceId':'6a48880da9855891b8baad7d7b34570d998b28c5',
              'Hash':'f93e3156637c9fce37154e2d091bca8a',
              'Key':'AA9FSK1323X3F',
              'Pagesize':'-1',
              'Keyword':name,
              'StartIndex':'0',
              'Version':'5'}
        
        link = json.loads(net.http_POST(self.SEARCHLINK,data,headers=self.HEADERS).content)
     
        data=link['Data']

        for field in data:
            TITLE=field['Name'].encode('utf8')
            iconimage=field['ThumbnailUrl'].encode('utf8') 
            id=field['Link']
            if not id:
                id=field['Id']
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                    self.GetFileHosts(id, list, lock, message_queue,type,season,episode)                
            else:    
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                    if year in TITLE:
                        self.GetFileHosts(id, list, lock, message_queue,type,season,episode)

     



    def Resolve(self, url):

        if 'google' in url:
            return url
        elif 'blogspot' in url:
            return url

        else:
            from entertainment import istream
            return istream.ResolveUrl(url)









            
