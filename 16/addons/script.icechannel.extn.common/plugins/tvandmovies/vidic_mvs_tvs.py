'''
    Istream
    Scenelog.org
    Copyright (C) 2013 Mikey1234

    version 0.2

'''


from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings


class vidic(MovieSource,TVShowSource,CustomSettings):
    implements = [MovieSource,TVShowSource,CustomSettings]
	
    #unique name of the source
    name = "vidic.ch"
    source_enabled_by_default = 'true'
    #display name of the source
    display_name = "Vidics.ch"
    
    #base url of the source website
    base_url = 'http://www.vidics.ch'

    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="General">\n'
        xml += '<setting id="custom_urls" type="labelenum" label="Preferred Language Results" default="All" values="Custom|All|English|French|Spanish|Italian|German|Dutch|Swedish|Polish|Russian|Indian" />\n'
        xml += '<setting id="custom_text_url" type="text" label="     Custom Language Results" default="English" enable="eq(-1,0)" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
        
    def get_lang(self):
        custom_url = self.Settings().get_setting('custom_urls')
        if custom_url == 'Custom':
            custom_url = self.Settings().get_setting('custom_text_url')

        return custom_url
    
    
    def GetFileHosts(self, url, list, lock, message_queue,name):
 
            self.AddFileHost(list, 'UNKOWN', url,host=name)



    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        import urllib2
        import re
        from entertainment.net import Net

        net = Net(cached=False)
        
        title = self.CleanTextForSearch(title) 
        

        tv_series=name.lower().replace(' ','_')
        
   
        
        
        

        if type == 'tv_episodes':

                if 'the_' in tv_series:
                    try:
                        new_url='http://www.vidics.ch/Serie/%s-Season-%s-Episode-%s'% (tv_series,season,episode)
                        content = net.http_GET(new_url).content

                    except:
                        new_url='http://www.vidics.ch/Serie/%s-Season-%s-Episode-%s'% (tv_series.replace('the_',''),season,episode)
                        content = net.http_GET(new_url).content

                else:
                        new_url='http://www.vidics.ch/Serie/%s-Season-%s-Episode-%s'% (tv_series,season,episode)
                        content = net.http_GET(new_url).content                    
                        
                link=content.split('title="Language')
                for p in link:
                        if ' Flag ' in p:
                            language=re.compile(' Flag (.+?)">').findall(p)[0]
                            
                            match=re.compile('href="(.+?)" target="_blank" rel="nofollow">(.+?)<',re.DOTALL).findall(p)
                            for url , name in match:
                                if self.get_lang()== 'All':
                                    self.GetFileHosts('http://www.vidics.ch'+url, list, lock, message_queue,name.upper()+' - [COLOR orange]'+language.upper() + '[/COLOR]')                
                                else:
                                    if self.get_lang().lower() in language.lower():
                                        self.GetFileHosts('http://www.vidics.ch'+url, list, lock, message_queue,name.upper()+' - [COLOR orange]'+language.upper() + '[/COLOR]')                
        else:

                new_url='http://www.vidics.ch/Film/%s'% (name.replace(' ','_'))                                                
                content = net.http_GET(new_url).content
                
                if not year +' year' in content:
                    #print 'year not found trying again......'
                    new_url='http://www.vidics.ch/Film/%s_(%s)'% (name.replace(' ','_'),year)                                      
                    content = net.http_GET(new_url).content
                    
                link=content.split('title="Language')
                for p in link:
                        if ' Flag ' in p:
                            language=re.compile(' Flag (.+?)">').findall(p)[0]
                           
                            match=re.compile('href="(.+?)" target="_blank" rel="nofollow">(.+?)<',re.DOTALL).findall(p)
                            for url , name in match:
                                if self.get_lang()== 'All':
                                    self.GetFileHosts('http://www.vidics.ch'+url, list, lock, message_queue,name.upper()+' - [COLOR orange]'+language.upper() + '[/COLOR]')                
                                else:
                                    if self.get_lang().lower() in language.lower():
                                        self.GetFileHosts('http://www.vidics.ch'+url, list, lock, message_queue,name.upper()+' - [COLOR orange]'+language.upper() + '[/COLOR]')   

    def Resolve(self, url):

   
        #print url
        from entertainment import istream
        import requests

        redirect= requests.head(url, allow_redirects=True).url
        
        return istream.ResolveUrl(redirect)
                                
