'''
    Cartoon HD    
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import os

class cartoonhd(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "Cartoon HD"
    display_name = "Cartoon HD"
    base_url = 'http://cartoonhd.website/'
   
    source_enabled_by_default = 'true'

    #cookie_file = os.path.join(common.cookies_path, 'cartoonhd.cookie')            
    
    def GetFileHosts(self, url, list, lock, message_queue,type,domain,cookie,year):

        import re,time,base64
        from entertainment import requests

     


        YEARWAY=url.replace('-bollox','')
        url=url.replace('-%s'%year,'')
        host=domain.split('//')[1]        

        headers={'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':host,
                'Origin':domain,
                'Pragma':'no-cache',
                'Referer':domain,
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest'}
        
        #cookie=net.get_cookies()
        #print cookie
        #print '###########################################'
        #print url
        #net.save_cookies(self.cookie_file)
        #COOKIE=re.compile('__utmx="(.+?)"').findall(open(self.cookie_file).read())[0]
        #print COOKIE
        #net.set_cookies(self.cookie_file)                         
     
        
        content = requests.get(domain+url,headers=headers,verify=False).content
        if '%TITLE% (%YEAR%)' in content:
            
            content = requests.get(domain+YEARWAY,headers=headers,verify=False).content

        if '?ckattempt=' in content:

            while True:
                if 'location.href' in content:
                    new=re.compile('location.href="(.+?)"').findall(content)[0]
                    content = requests.get(new,headers=headers,verify=False).content
                    if not '?ckattempt=' in content:
                        break
                else:break                             
                
        TIME = time.time()- 3600
  
        TIME= str(TIME).split('.')[0]
  
        TIME= base64.b64encode(TIME,'strict')
 
        TIME=TIME.replace('==','%3D%3D')
        
        token=re.compile("var tok.+?'(.+?)'").findall(content)[0]        
        match=re.compile('elid.+?"(.+?)"').findall(content)
        id = match[0]
        #COOKIE='flixy=%s; %s=%s' % (token,id,TIME)

        headers={'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Content-Length':'94',
                #'Cookie':COOKIE,
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':host,
                'Origin':domain,
                'Pragma':'no-cache',
                'Referer':url,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest'}
                #'Authorization': 'Bearer '+COOKIE.replace('%3D','=')


        if type == 'tv_episodes':
            get='getEpisodeEmb'
        else:
            get='getMovieEmb'

        new_search=domain+'/ajax/nembeds.php'

        data={'action':get,'idEl':id,'token':token,'elid':TIME}
   
     
        content = requests.post(new_search, data=data, headers=headers,verify=False).content
        if '?ckattempt=' in content:

            while True:
                if 'location.href' in content:
                    new=re.compile('location.href="(.+?)"').findall(content)[0]
                    content = requests.post(new, data=data, headers=headers,verify=False).content
                    if not '?ckattempt=' in content:
                        break
                else:
                    break
             
            

    

        quality ='HD'

            
        r = '"type":"(.+?)".+?iframe src="(.+?)"' #% option
        
        if '1080P' in quality.upper():
            quality ='1080P'
        elif '720P' in quality.upper():
            quality ='720P'                
        elif '480P' in quality.upper():
            quality ='HD'
        else:
            quality ='SD'
            
        FINAL  = re.compile(r,re.IGNORECASE).findall(content.replace('\\',''))
        for quality , FINAL_URL in FINAL:
            if '1080P' in quality.upper():
                Q ='1080P'
            elif '720P' in quality.upper():
                Q ='720P'                
            elif '480P' in quality.upper():
                Q ='HD'
            else:
                Q ='SD'
            if 'openload' in quality.lower():
                Q='HD'
            self.AddFileHost(list, Q, FINAL_URL.split('"')[0])
    
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
  
      domain,cookie = self.GetDomain()
      domain=domain.rsplit('/', 1)[0]
      name=self.CleanTextForSearch(name.lower())
      
      if type == 'tv_episodes':
        name=name.lower()
        item_url = '/show/%s/season/%s/episode/%s' %(name.replace(' ','-'),season,episode)
        self.GetFileHosts(item_url, list, lock, message_queue,type,domain,cookie,year)
      else:
        if not year:
            year='bollox'
        item_url = '/movie/%s-%s' % (name.replace(' ','-'),year)
        
        #print item_url
        self.GetFileHosts(item_url, list, lock, message_queue,type,domain,cookie,year)
           
       


    def GrabMailRu(self,url,list):
        #print url
        
        from entertainment.net import Net
        net = Net(cached=False)

        
        import json,re
        items = []

        data = net.http_GET(url).content
        cookie = net.get_cookies()
        for x in cookie:

             for y in cookie[x]:

                  for z in cookie[x][y]:
                       
                       l= (cookie[x][y][z])
                       
        link=json.loads(data)
        data=link['videos']
        for j in data:
            stream = 'http:'+j['url']
            quality = j['key']
            test = str(l)
            test = test.replace('<Cookie ','')
            test = test.replace(' for .my.mail.ru/>','')
            url=stream +'|Cookie='+test
            Q=quality.upper()
            if Q == '1080P':
                Q ='1080P'
            elif Q == '720P':
                Q ='720P'                
            elif Q == '480P':
                Q ='HD'
            else:
                Q ='SD'                
            self.AddFileHost(list, Q, url,host='MAIL.RU') 


    def GetDomain(self):                 
        

        from entertainment import requests
  

        
        url=['https://cartoonhd.cc/','https://cartoonhd.online/']
        for URL in url:
            headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4','Referer':URL}
            try:
               hello = requests.get(URL, headers=headers,verify=False)
              
               domain=hello.url
               cookie=hello.content
               return domain,cookie
            except:pass 
                  
                 






            
