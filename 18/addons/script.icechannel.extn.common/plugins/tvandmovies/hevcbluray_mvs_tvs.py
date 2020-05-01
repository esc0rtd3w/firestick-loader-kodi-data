'''
    HevcBluray   
    Copyright (C) 2013 Mikey1234
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin


class hevec(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "HevcBluray"
    display_name = "HevcBluray"

    source_enabled_by_default = 'true'
    base_url ='http://300mbmoviesdl.co'
    host = '300mbmoviesdl.co'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'




    def GetFileHosts(self, url, list, lock, message_queue):



        from entertainment.net import Net
        import re,urlresolver
        net = Net(cached=False)


        headers = {'User-Agent':self.User_Agent}
        
        LINK = net.http_GET(url,headers=headers).content

        #RES = re.compile('Quality:(.+?)<').findall(LINK)[0]
        RES = url
        link = LINK.split('<h3 style="text-align: center;">')
   
        uniques = []
        for p in link:
           
            try:
                final_url = re.compile('<a href="([^"]+)"').findall(p)[0]

                if '4K' in RES.upper():
                    res='4K'
                elif '3D' in RES.upper():
                    res='3D'
                elif '1080' in RES.upper():
                    res='1080P'                   
                elif '720' in RES.upper():
                    res='720P'
                elif 'HD' in RES.upper():
                    res='HD'
                elif 'DVD' in RES.upper():
                    res='DVD'
                elif 'HDTS' in RES.upper():
                    res='CAM'
                elif '-TS-' in RES.upper():
                    res='CAM'
                elif 'CAM' in RES.upper():
                    res='CAM'
                elif 'HDCAM' in RES.upper():
                    res='CAM'
                else:
                    res='720P'
                
                HOST = final_url.split('//')[1].split('/')[0]
                if urlresolver.HostedMediaFile(final_url):
                    if final_url not in uniques:
                        uniques.append(final_url)
                        self.AddFileHost(list, res, final_url,host=HOST.upper())

            except:pass   
                    
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        from entertainment.net import Net
        import re
        net = Net(cached=False)
        
        name=self.CleanTextForSearch(name.lower())
        

        headers = {'Host':self.host, 'User-Agent':self.User_Agent}
                   

        new_url = '%s/search/%s/feed/rss2/' %(self.base_url,name.replace(' ','+'))

        season_pull = "s0%s"%season if len(season)<2 else 's'+season
        episode_pull = "e0%s"%episode if len(episode)<2 else 'e'+episode        
        BOTH=season_pull+episode_pull
        
        LINK = net.http_GET(new_url,headers=headers).content
        match=re.compile('<a rel="nofollow" href="(.+?)">(.+?)<',re.DOTALL).findall(LINK)
        uniques=[]
        for item_url ,TITLE in match:

   
           
            if not 'http' in item_url:
                item_url = 'http://'+item_url
            if item_url not in uniques:
                uniques.append(item_url)
                
                if name.lower() in self.CleanTextForSearch(TITLE.lower()):
                    if type == 'tv_episodes':
                        if BOTH in TITLE.lower():
                            self.GetFileHosts(item_url, list, lock, message_queue)
                    else:        
                        if year in TITLE.lower():
                            self.GetFileHosts(item_url, list, lock, message_queue)
            
