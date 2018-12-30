'''
    iStream Extension
    M4U
    Copyright (C) 2017 mucky duck
'''
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin

import xbmc


class m4u(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = 'M4U'
    display_name = 'M4U'
    base_url = 'http://m4ufree.info'
    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'

    source_enabled_by_default = 'true'


    def fetch(self,list,link):


        import re

        match = re.findall(r'"file":"([^"]+)".*?"label":"([^"]+)"', str(link), re.I|re.DOTALL)
        fail = match[0]

        for url, res in match:

            if not '.srt' in url:
                if '1080' in res:
                    res = '1080P'
                elif '720' in res:
                    res = '720P'
                elif '480' in res:
                    res = 'DVD'
                elif '360' in res:
                    res = 'SD'
                else:
                    res = '720P'

                if 'google' in url or 'usercdn' in url or self.base_url in url:
                    final_url = url

                else:
                    final_url = '%s/%s' %(self.base_url,url)
                    final_url = final_url.replace('../view.php?','view.php?')
                    final_url = final_url.replace('./view.php?','view.php?')

                #HOST = final_url.split('//')[1]
                #HOST = HOST.split('/')[0].split('.')[0]  

                self.AddFileHost(list, res, final_url)
    


    def GetFileHosts(self, url, list, lock, message_queue, season, episode, type, year, query, RES):


        from entertainment.net import Net
        import re
        net = Net(cached=False)

        
        season_pull = "0%s"%season if len(season)<2 else season
        episode_pull = "0%s"%episode if len(episode)<2 else episode

        
        referer = url

        headers = {'User-Agent':self.User_Agent, 'Referer':self.base_url}
        html = net.http_GET(url, headers=headers).content
        
        if type == 'tv_episodes':
            
            link = html.split('"target"')
            for p in link:
                
                try:

                    p = p.replace(' ','')
                    name = re.compile('"episode">(.+?)<').findall(p)[0]
                    URL = re.compile('href="(.+?)"').findall(p)[0]
                    
                    data = name.replace('-','').upper()
                    data=data.replace('S','').replace('E','')
                    
                    
                    if ',' in data:
                            data = data.split(',')[0]
                    
                    BOTH=season_pull+episode_pull
                    if BOTH in data:
                        link = net.http_GET(URL, headers=headers).content
                except:pass
        else:
            
            request_url = re.findall(r'href="([^"]+)">Watch', str(html), re.I|re.DOTALL)[0]
            link = net.http_GET(request_url, headers=headers).content
            

	try:
            
            self.fetch(list,link)

	except:

            request_url2 = '%s/demo.php' %self.base_url
            match2 = re.findall(r'link="([^"]+)".*?>Server .*?</span>', str(link), re.I|re.DOTALL)

            for a in match2:
                link2 = net.http_GET('%s?v=%s' %(request_url2,a), headers=headers).content

                try:

                    self.fetch(list,link2)

                except:

                    url = re.findall(r'source.*?"([^"]+)"', str(link2), re.I|re.DOTALL)[0]
                    
                    if 'google' in url or 'usercdn' in url or self.base_url in url:
                        final_url = url

                    else:
                        final_url = '%s/%s' %(self.base_url,url)
                        final_url = final_url.replace('../view.php?','view.php?')
                        final_url = final_url.replace('./view.php?','view.php?')

                    HOST = final_url.split('//')[1].replace('redirector.','')
                    HOST = HOST.split('/')[0].split('.')[0]  

                    import urllib

                    if 'usercdn' in final_url: ###this isa the link that wont resolve serach film moana to test

                        final_url = final_url.replace(':443','')
                        host = final_url.split('//')[1].split('/')[0]  
                        headers = {'Referer': referer, 'Host':host, 'User-Agent':self.User_Agent}
                        final_url = final_url.strip() + '|' + urllib.urlencode(headers)

                    res = RES.replace('-','').strip()

                    self.AddFileHost(list, res, final_url)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  


        from entertainment.net import Net
        import re
        net = Net(cached=False)

        title = self.CleanTextForSearch(title) 
        query = self.CleanTextForSearch(name)

        headers={'User-Agent':self.User_Agent, 'Referer':self.base_url}

        if type == 'movies':
            movie_url = '%s/tag/%s' %(self.base_url,query.replace(' ','-'))
            link = net.http_GET(movie_url,headers=headers).content

        elif type == 'tv_episodes':
            tv_url = '%s/tagtvs/%s' %(self.base_url,query.replace(' ','-'))
            link = net.http_GET(tv_url,headers=headers).content

        links = link.split('"top-item"')

        for p in links:

            try:

               media_url = re.compile('href="([^"]+)"').findall(p)[0]

               if type == 'tv_episodes':
                   media_title = re.compile('href=.*?>(.*?)<').findall(p)[0]
                   if query.lower() in self.CleanTextForSearch(media_title.lower()):
                       self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type, year, query, '')
                        
               elif type == 'movies':
                   media_title = re.compile('<cite>(.*?)</').findall(p)[0]
                   qual = re.compile('class="h3-quality".*?>(.*?)<').findall(p)[0]
                   if query.lower() in self.CleanTextForSearch(media_title.lower()):
                       if year in self.CleanTextForSearch(media_title.lower()):
                           self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type, year, query, qual)

            except:pass

