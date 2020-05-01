

#iStream Extension
#ZooCinema
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc


class zoocine(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]
    
    name = 'ZooCinema'
    display_name = 'ZooCinema'
    base_url = 'http://zoocine.co'
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

                if '=download' in final_url:
                    final_url = final_url.replace('=download','=view')

                self.AddFileHost(list, res, final_url)




    def GetFileHosts(self, url, list, lock, message_queue):

        from entertainment import requests
        from entertainment import jsunpack
        import base64,re,urllib

        headers = {'User-Agent':self.User_Agent}
        link = requests.get(url, headers=headers).content

        try:
            qual = link.split('>Source:<')[1:]
            for p in qual:
                res = re.findall(r'class="finfo-text">([^<]+)</div>', str(link), re.I|re.DOTALL)[0]
                if '1080' in res:
                    res='1080P'                   
                elif '720' in res:
                    res='720P'
                elif  '480' in res:
                    res='DVD'
                elif '360' in res:
                    res='SD'
                elif 'CAM' in res:
                    RES='CAM'
                else:
                    res='DVD'

            try:

                iframe = link.split('"video-responsive"')[1:]
                for p in iframe:

                    iframe_url = re.findall(r'iframe.*?src="([^"]+)"', p, re.I|re.DOTALL)[0]
                    if 'extraload' in iframe_url:
                        link2 = requests.get(iframe_url,headers=headers).content.decode('utf8')
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
                    
                    elif 'goo.gl' not in iframe_url:
                        if 'youtube' not in iframe_url:
                            self.AddFileHost(list, res, iframe_url)

            except:pass

            try:
                    
                match2 = re.findall(r'<a href="([^"]+)"  target="_blank">Watch.+?</a>', str(link), re.I|re.DOTALL)
                if not match2:
                    match2 = re.findall(r'target="_blank" href="(.+?)">Watch',str(link), re.I|re.DOTALL)
                for a in match2:
                    if '=' in a:
                        base64_url = a.split('=')[1]
                        base64_url = urllib.unquote(base64_url).decode('base64')
                        self.AddFileHost(list, res, base64_url)
                    else:
                        self.AddFileHost(list, res, a)

            except:pass
                    
        except:pass




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        from entertainment import requests
        import re

        name = self.CleanTextForSearch(name.lower())
        headers = {'User-Agent':self.User_Agent}

        if type == 'tv_episodes':

            season_pull = '0%s' %season if len(season) <2 else season
            episode_pull = '0%s' %episode if len(episode) <2 else episode
            sep = 'S%sE%s' %(season_pull,episode_pull)
            search = {'do':'search', 'subaction':'search', 'story':'%s %s' %(name,sep)}

        else:

            search = {'do':'search', 'subaction':'search', 'story':name}

        link = requests.post(self.base_url, data=search, headers=headers).content
        links = link.split('-in">')[1:]
        
        for p in links:

            try:

               media_url = re.compile('href="(.+?)"').findall(p)[0]
               if self.base_url not in media_url:
                   media_url = self.base_url + media_url
               media_title = re.compile('title="(.+?)"').findall(p)[0]
               
               if type == 'tv_episodes':

                   if name in self.CleanTextForSearch(media_title.lower()):
                       if sep.lower() in media_title.lower():
                           self.GetFileHosts(media_url, list, lock, message_queue)
                        
               else:

                   if name in self.CleanTextForSearch(media_title).lower():
                       if year in media_title:
                           self.GetFileHosts(media_url, list, lock, message_queue)

            except:pass




    def Resolve(self, url):
        if '/docs/securesc/' not in url:
            from entertainment import istream
            url = istream.ResolveUrl(url)
        else:
            return url
 
