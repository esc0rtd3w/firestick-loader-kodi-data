'''
    http://afdah.com/    
    Copyright (C) 2013 Mikey1234
'''


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common



class mailru(MovieSource):
    implements = [MovieSource]
    
    name = "MailRu"
    display_name = "MailRu"

    source_enabled_by_default = 'true'
    icon = common.notify_icon
    
        
    def GetFileHosts(self, url, list, lock, message_queue,title):
        if not 'http:' in url:
            url='http:'+url  
        self.GrabMailRu(url,list,title)
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re,urllib,json

        net = Net(cached=False,user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        name = self.CleanTextForSearch(name)

        search_term = name.lower()
        linkme='http://my.mail.ru/cgi-bin/my/ajax?user=&ajax_call=1&func_name=video.get_list&mna=&mnb=&arg_tag=%s&arg_duration=long&arg_sort=&arg_sort_order=desc&arg_hd_exists=&arg_unsafe=0&arg_type=search&arg_offset=0&arg_limit=300'
  
        new_url=linkme % (name.replace(' ','+').lower()+'+'+year)
        response= net.http_GET(new_url).content
        link=json.loads(response)[-1]
        data=link['items']
        for i in data:
            _url_=i['UrlHtml'].replace('video/','').replace('.html','.json')
            title=i['Title']
            time=i['DurationFormat']
            if len(time)>5:
                if name.lower().replace('the ','') in title.lower() or name.lower().replace('the ','').replace(' ','.') in title.lower().replace(' ','.'):
                    if year in title:
                                                          # /inbox/nichols91/video/_myvideo/21.html
                        #http://videoapi.my.mail.ru/videos/inbox/nichols91/_myvideo/21.json
                        movie_url='http://videoapi.my.mail.ru/videos/'+_url_
                        #print movie_url
                        self.GetFileHosts(movie_url, list, lock, message_queue,title)                           

    def GrabMailRu(self,url,list,title):
        
        
        from entertainment.net import Net
        net = Net(cached=False)

        
        import json,re
        items = []

        data = net.http_GET(url).content
        cookie = net.get_cookies()
        
        for x in cookie:
             if '.my.mail.ru' in x: 
                 for y in cookie[x]:
                      for z in cookie[x][y]:
                           l= (cookie[x][y][z])
                       
        link=json.loads(data)
        data=link['videos']
        for j in data:
            stream = j['url']
            if not 'http:' in stream:
                stream='http:'+stream
            Q = j['key'].upper()
            test = str(l)
            test = test.replace('<Cookie ','')
            test = test.replace(' for .my.mail.ru/>','')
            url=stream +'|Cookie='+test
            if Q == '1080P':
                Q ='1080P'
            elif Q == '720P':
                Q ='720P'                
            elif Q == '480P':
                Q ='HD'
            else:
                Q ='SD'          
            self.AddFileHost(list, Q, url,host=title.title()) 



    def Resolve(self, url):

        return url
