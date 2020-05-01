
#iStream Extension
#CoolTV
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc


class cooltv(TVShowSource):

    implements = [TVShowSource]
    
    name = "CoolTV"
    display_name = "CoolTV"
    base_url = 'https://cooltvseries.com'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    source_enabled_by_default = 'true'




    def open_url(self, url, headers=''):
        
        from entertainment import requests

        if not headers:
            headers = {}
            headers['User-Agent'] = self.User_Agent

        import sys
        if sys.version_info < (2, 7, 9):

            if 'myaddrproxy' in url:
                url = 'https://ssl-proxy.my-addr.org' + url
            else:
                url = 'https://ssl-proxy.my-addr.org/myaddrproxy.php/' + url

        else:
            url = url

        link = requests.get(url, headers=headers, verify=False).content
        return link




    def GetFileHosts(self, url, list, lock, message_queue, season, episode, type): 
        
        import re

        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode
        sep = 's%se%s' %(season_pull,episode_pull)

        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding':'gzip, deflate, sdch', 'Accept-Language':'en-US,en;q=0.8',
                   'User-Agent':self.User_Agent}

        link = self.open_url(url, headers)

        match = re.findall(r'<li><a href="([^"]+)">([^<>]*)<span.+?>', str(link), re.I|re.DOTALL)
        for media_url, media_title in match:
    
            try:

                if sep in media_title.lower():

                    final_link = self.open_url(media_url, headers=headers)
                    final_links = str(final_link).split('dwn-box">')[1:]
                    
                    for p in final_links:

                        final_url = re.compile('href="([^"]+)"').findall(p)[0]

                        try:
                            final_url = final_url.replace('/myaddrproxy.php/https/','https://')
                        except:pass

                        res = re.compile('"nofollow">([^<>]*)<').findall(p)[0].upper()

                        if '1080' in res:
                            res='1080P'                   
                        elif '720' in res:
                            res='720P'
                        elif 'HD' in res:
                            res='HD'
                        elif  '480' in res:
                            res='DVD'
                        elif '360' in res:
                            res='SD'
                        else:
                            res='DVD'

                        self.AddFileHost(list, res, final_url)

            except:pass




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        import re

        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding':'gzip, deflate, sdch', 'User-Agent':self.User_Agent}

        name = self.CleanTextForSearch(name.lower())
        search = '%s/search.php?search=%s' %(self.base_url,name.lower())
        link = self.open_url(search, headers)
        links = link.split('box">')
        
        for p in links:

            try:

               media_url = re.compile('href="([^"]+)"').findall(p)[0]
               media_title = re.compile('title="([^"]+)"').findall(p)[0]
               
               if name in self.CleanTextForSearch(media_title.lower()):
                    if 'season %s' %season in media_title.lower():
                        self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type)

            except:pass
