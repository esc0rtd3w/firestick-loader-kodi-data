'''
    Cartoon HD    
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common


class playbox(MovieSource):
    implements = [MovieSource]
    
    name = "PlayBoxHD"
    display_name = "PlayBoxHD"
    API='http://playboxhd.com/api/box?'

   
    source_enabled_by_default = 'true'
    

    def GetStream(self,url):
        from entertainment import pyaes as pyaes
        import base64

        decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(base64.urlsafe_b64decode('cXdlcnR5dWlvcGFzZGZnaGprbHp4YzEyMzQ1Njc4OTA='), '\0' * 16))
        url = base64.decodestring(url)
        url = decrypter.feed(url) + decrypter.feed()
        return url


    
    
    def GetFileHosts(self, url, list, lock, message_queue):

        import re,json
        import urllib2
        from entertainment.net import Net
        net = Net(cached=False,user_agent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
     
  
        new_url = 'http://playboxhd.com/api/box?type=detail&id=%s&os=Android&v=291.0&k=0&al=key' % (url)
      
        content = net.http_GET(new_url).content

            
        link = json.loads(content)
        #print link
        data=link['data']['chapters']
        try: 
            for field in data:            
                ID=str(field['id'])
                new_url = 'http://playboxhd.com/api/box?type=stream&id=%s&os=Android&v=291.0' % ID
                  
                link = json.loads(net.http_GET(new_url).content)
                data=link['data']
          
                for field in data:
                    name=field['server'].encode('utf8').upper()
                    quality=field['quality'].upper()
                    FINAL_URL=self.GetStream(str(field['stream']))

                    if quality=='AUTO':
                        quality='HD'

                    if not 'freemovietube.tv' in FINAL_URL:
                        if 'openload' in FINAL_URL:
                            self.AddFileHost(list, quality, FINAL_URL)
                        if 'google' in FINAL_URL:
                            
                            try:
                                urllib2.urlopen(str(FINAL_URL))
                                self.AddFileHost(list, quality, FINAL_URL)
                                break
                            except urllib2.HTTPError, e:
                                AHHH=str(e)

        except:pass  

        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re,json
        net = Net(cached=False,user_agent='Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5')
        name = self.CleanTextForSearch(name)


        
        main_url= self.API+'type=search&os=Android&v=291.0&k=0&keyword=%s' %(name.replace(' ','+'))

        
        content=net.http_GET(main_url).content
        

        import json

        link=json.loads(content)
        


        data=link['data']
        for field in data['films']:
            NAME = self.CleanTextForSearch(field['title'].encode('utf8'))

            item_url=str(field['id'])
            if name.lower() in NAME.lower():
                    if year in field['publishDate']:
                        self.GetFileHosts(item_url, list, lock, message_queue)
              

            




            
