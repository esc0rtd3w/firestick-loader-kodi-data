

#iStream Extension
#iOnlineMovies
#Copyright (C) 2017 mucky duck




from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc    
        
class ionlinemovies(MovieSource):
    implements = [MovieSource]
    
    name = 'iOnlineMovies'
    display_name = 'iOnlineMovies'
    base_url = 'http://www.ionlinemovies.com'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    source_enabled_by_default = 'true'


    def AddMedia(self, list, data):

        for final_url, res in data: 

            if '.srt' not in final_url:
                if '1080' in res:
                    res='1080P'                   
                elif '720' in res:
                    res='720P'
                elif  '480' in res:
                    res='DVD'
                elif '360' in res:
                    res='SD'
                else:
                    res='DVD'

                self.AddFileHost(list, res, final_url)


    
    
    def GetFileHosts(self, url, list, lock, message_queue):
        
        from entertainment import requests
        from entertainment import jsunpack
        import urlresolver,re
        
        headers = {'User-Agent':self.User_Agent}
        link = requests.get(url, headers=headers, timeout=15).content
        
        try:
            RES = re.findall(r'Quality:</strong>([^<>]*)<', str(link), re.I|re.DOTALL)[0].upper()
        except:
            RES = ''

        if '4K' in RES:
            res='4K'
        elif '3D' in RES:
            res='3D'
        elif '1080' in RES:
            res='1080P'                   
        elif '720' in RES:
            res='720P'
        elif 'HD' in RES:
            res='HD'
        elif 'DVD' in RES:
            res='DVD'
        elif 'HDTS' in RES:
            res='TS'
        elif 'TS' in RES:
            res='TS'
        elif 'CAM' in RES:
            res='CAM'
        elif 'HDCAM' in RES:
            res='CAM'
        else:
            res='720P'

        iframe_url = re.findall(r'iframe.*?src="([^"]+)"', str(link), re.I|re.DOTALL)

        for source in iframe_url:
            if '/gdp/play/' in source:
                try:

                    source = source.replace('&#038;','&')
                    link2 = requests.get(source, headers=headers, timeout=15).content
                    match = ''
                    if 'JuicyCodes' in link2:
                        try:
                            data = re.findall('type="text/javascript">([^<>]*)<', str(link2), re.I|re.DOTALL)[0]
                            data = data.replace('JuicyCodes.Run(','').replace('"+"','').decode('base64')
                            js_data = jsunpack.unpack(data)
                            match = re.findall(r'"file":"([^"]+)".*?"label":"([^"]+)"', str(js_data), re.I|re.DOTALL)
                        except:pass

                    else:
                        try:
                            if jsunpack.detect(link2):
                                js_data = jsunpack.unpack(link2)
                                match = re.findall(r'"file":"([^"]+)".*?"label":"([^"]+)"', str(js_data), re.I|re.DOTALL)
                        except:pass

                    self.AddMedia(list,match)

                except:pass

            else:
                if urlresolver.HostedMediaFile(source):
                    self.AddFileHost(list, res, source)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        from entertainment import requests
        import re
        
        name = self.CleanTextForSearch(name.lower())

        headers = {'User-Agent':self.User_Agent}

        search = '%s/?s=%s' %(self.base_url,name.replace(' ','+'))
        link = requests.get(search, headers=headers, timeout=15).content
        links = link.split('article id=')[1:]

        for p in links:
            try:
                media_url = re.compile('href="([^"]+)"').findall(p)[0]
                media_title = re.compile('title="([^"]+)"').findall(p)[0]
                if name in self.CleanTextForSearch(media_title.lower()):
                    if year in media_title:
                        self.GetFileHosts(media_url, list, lock, message_queue)
            except:pass
 
