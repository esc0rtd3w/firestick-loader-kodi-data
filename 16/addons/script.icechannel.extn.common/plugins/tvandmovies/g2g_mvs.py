'''
    g2g.cm  # OdrtKapH2dNRpVHxhBtg 
    Copyright (C) 2013 
'''

from entertainment.plugnplay.interfaces import MovieSource
#from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui


class g2g(MovieSource):
    implements = [MovieSource]
    
    name = "g2g"
    display_name = "g2g.cm"
    base_url = 'http://g2gfmmovies.com/'
    #img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/92bed8a40419803f31f90e2268956db50d306997/flixanity.png'

    source_enabled_by_default = 'true'
    cookie_file = os.path.join(common.cookies_path, 'g2glogin.cookie')
    icon = common.notify_icon
    
    '''
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Email" default="Enter your noobroom email" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="xunity" />'
        xml += '<setting label="Premium account will allow for 1080 movies and the TV Shows section" type="lsep" />\n'
        xml += '<setting id="premium" type="bool" label="Enable Premium account" default="false" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
    '''

    def GetFileHosts(self, url, list, lock, message_queue,type):

        import re
        from entertainment.net import Net
        net = Net(cached=False)
        print '################################'
        print url
        content = net.http_GET(url).content
        if type == 'movies':
            r='class="movie_version_link"> <a href="(.+?)".+?document.writeln\(\'(.+?)\'\)'
        else:
             r='class="movie_version_link"> <a href="(.+?)".+?version_host">(.+?)<'           
        match=re.compile(r,re.DOTALL).findall(content)
    
        for item_url ,HOST in match:
            self.AddFileHost(list, 'DVD', item_url,host=HOST.upper())       
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        #net = Net(cached=False)
        name = self.CleanTextForSearch(name)
        import urllib
        name = name.lower()
        net = Net(cached=False)        
               
        if type == 'movies':
            


            title = self.CleanTextForSearch(title) 
            name = self.CleanTextForSearch(name)

            URL= self.base_url+'?type=movie&keywords=%s' %name.replace(' ','+')
            content = net.http_GET(URL).content
            
            match =re.compile('href="(.+?)" target="_blank"><img class="image" src=".+?" alt="(.+?)"').findall(content)
            for item_url , name in match:
                if year in name:
                    #print item_url
                    self.GetFileHosts(item_url, list, lock, message_queue,type)

        elif type == 'tv_episodes':
            title = self.CleanTextForSearch(title) 
            name = self.CleanTextForSearch(name)

            URL= self.base_url+'?type=tv&keywords=%s' %name.replace(' ','+')
            content = net.http_GET(URL).content
            
            match =re.compile('href="(.+?)" target="_blank"><img class="image" src=".+?" alt="(.+?)"').findall(content)

            for url , NAME in match:
                if name.lower() in self.CleanTextForSearch(NAME.lower()):
                    url=url.replace('-online.html','')
                    item_url=url+'-season-%s-episode-%s-online.html' % (season,episode)
                  
                    self.GetFileHosts(item_url, list, lock, message_queue,type)
                        
            

    def Resolve(self, url):
        from entertainment.net import Net
        import re
  
        net = Net(cached=False)                
        import base64
        print url
        content = net.http_GET(url).content
        URL=base64.b64decode(re.compile('&url=(.+?)&').findall(content)[0])
        #print '###############################'
        #print URL
        from entertainment import istream
        play_url = istream.ResolveUrl(URL)
        #print play_url
        return play_url
            
            
        
