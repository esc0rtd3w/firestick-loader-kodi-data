'''
    Bobby  
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
import xbmc



class bobby(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]
    
    name = "BobbyMovies"
    display_name = "Bobby Movies"

    source_enabled_by_default = 'true'
    base_url = 'http://webapp.bobbyhd.com' #'https://bobby.kohimovie.com/jp/2.1.0/'



        
    def GetFileHosts(self, url, list, lock, message_queue,type,episode):

    
        import re
        from md_request import open_url



        headers={'Host':'webapp.bobbyhd.com',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69',
                'Accept-Language':'en-gb',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'keep-alive'}

        url = '%s/player.php?alias=%s' %(self.base_url,url)
        
        link = open_url(url,headers=headers,timeout=3).content
        
        if type=='tv_episodes':
            match=re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)\..+?</a>').findall(link)
        else:
            match=re.compile('changevideo\(\'(.+?)\'\)".+?data-toggle="tab">(.+?)</a>').findall(link)
            
        for URL , RES in match:
            if 'webapp' in URL:
                URL=URL.split('embed=')[1]
            
            
            if '720' in RES:
                res='720P'
            elif 'CAM' in RES:
                res='CAM'                    
            elif '1080' in RES:
                res='1080P'
            elif 'HD' in RES:
                res='HD'
            else:
                res='720P'
            
            FINAL_URL=URL.split('//')[1]
            FINAL_URL=FINAL_URL.split('/')[0]
            
            if type=='tv_episodes':
              
                EPISODE=int(RES)

                if int(episode)==EPISODE:
                               
                    self.AddFileHost(list, res, URL,host=FINAL_URL.upper())                    
            else:    
                    self.AddFileHost(list, res, URL,host=FINAL_URL.upper())

        
                    
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
    
        import re
        from md_request import open_url

        name = self.CleanTextForSearch(name.lower()).strip()
        
        headers={'Host':'webapp.bobbyhd.com',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13F69',
                'Accept-Language':'en-gb',
                'Accept-Encoding':'gzip, deflate',
                'Connection':'keep-alive'}
        

        search = '%s/search.php?keyword=%s' %(self.base_url,name.replace(' ','+'))
        
        link = open_url(search,headers=headers,timeout=3).content
     
        match = re.compile('alias=(.+?)\'">(.+?)</a>').findall(link)
        
        for id,TITLE in match:
         
            if type=='tv_episodes':
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                      if season in TITLE:
                          self.GetFileHosts(id, list, lock, message_queue,type,episode)
            else:
                movie_title = self.CleanTextForSearch(name + ' (%s)' %year)
                if name == self.CleanTextForSearch(TITLE.lower()) or movie_title == self.CleanTextForSearch(TITLE.lower()):
                    self.GetFileHosts(id, list, lock, message_queue,type,episode)

