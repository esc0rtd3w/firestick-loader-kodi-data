'''
    Istream
    myvideolinks
    Copyright (C) 2013 Mikey1234

    version 0.2

'''

from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common






class myvideolinks(MovieSource, TVShowSource):
    implements = [MovieSource, TVShowSource]
	
    name = "myvideolinks"
    source_enabled_by_default = 'false'
    display_name = "Myvideolinks"
    base_url = 'http://newmyvideolink.xyz/'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    
    def GetFileHosts(self, url, list, lock, message_queue, RES):


        from entertainment.net import Net
        import re
        net = Net(cached=False)

        
        headers={'User-Agent':self.User_Agent}
        
        content = net.http_GET(url,headers).content

        match  = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(content)
        
        for url, host in match:
            
            if 'HDCAM' in RES.upper():
                res='CAM'
            elif 'CAM' in RES.upper():
                res='CAM'
            elif 'HDTS' in RES.upper():
                res='CAM'
            elif ' TS ' in RES.upper():
                res='CAM'
            elif 'DVD' in RES.upper():
                res='DVD'
            elif '720' in RES:
                res='720P'                   
            elif '1080' in RES:
                res='1080P'
            elif 'HD' in RES.upper():
                res='HD'
            else:
                res='720P'
                
            self.AddFileHost(list, res, url, host=host)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from entertainment.net import Net
        import re
        net = Net(cached=False)

        
        headers={'User-Agent':self.User_Agent}

        name = self.CleanTextForSearch(name.lower())

        base_link = net.http_GET(self.base_url,headers=headers).content
        baseurl = re.compile('href="(.+?newmyvideolink.+?)"').findall(base_link)[0]

        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode
        if type == 'movies':
            movie_url = '%s/?s=%s' %(baseurl,name.replace(' ','+'))
            link = net.http_GET(movie_url,headers=headers).content
        elif type == 'tv_episodes':
            tv_url = '%s/?s=%s+S%sE%s' %(baseurl,name.replace(' ','+'),season_pull,episode_pull)
            link = net.http_GET(tv_url,headers=headers).content

        links = link.split('post-title')

        for p in links:
            try:
                m_url = re.compile('href="([^"]+)"').findall(p)[0]
                m_title = re.compile('title="([^"]+)"').findall(p)[0]
                
                if type == 'movies':
                    if name.lower() in self.CleanTextForSearch(m_title.lower()):
                        if year in m_title:
                            self.GetFileHosts(m_url, list, lock, message_queue, m_title)

                elif type == 'tv_episodes':
                    if 's%se%s' %(season_pull,episode_pull) in m_title.lower():
                        self.GetFileHosts(m_url, list, lock, message_queue, m_title)
            except:pass
