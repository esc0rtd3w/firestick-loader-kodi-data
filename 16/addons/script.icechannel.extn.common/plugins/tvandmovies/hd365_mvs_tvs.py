

#iStream Extension
#HD365
#Copyright (C) 2017 mucky duck


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc


class sockshare(MovieSource,TVShowSource):

    implements = [MovieSource,TVShowSource]
    
    name = 'HD365'
    display_name = 'HD365'
    base_url = 'http://hdmovies365.net'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    source_enabled_by_default = 'true'




    def add_media(self, list, data):

        for field in data['data']['level']:

            final_url = field['file']
            res = field['label'].upper()

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




    def GetFileHosts(self, url, list, lock, message_queue, season, episode, type, year):

        from entertainment import requests
        import hashlib,re,time

        referer = url
        headers = {'User-Agent':self.User_Agent}
        link = requests.get(url, headers=headers).content
        headers = {'Accept-Encoding':'gzip, deflate, sdch', 'Accept-Language':'en-US,en;q=0.8',
                   'Referer':referer, 'User-Agent':self.User_Agent, 'X-Requested-With':'XMLHttpRequest'}
        request_url = '%s/play/play' %self.base_url
        time_now = int(time.time() * 1000)
        uniques = []

        key = '*@'
        key2 = 'ai'
        key3 = 'e12b950be6ed61fa6a89f390bd9a0ec6'

        media_year = re.compile('Release:</b>(.+?)</').findall(link)[0]

        if year in media_year:

            if type == 'tv_episodes':

                try:
                    
                    match = re.compile('<a class="btn-eps.+?" data-episode="(.+?)" data-film="(.+?)".+?>(.+?)</a>').findall(link)

                    for episode_id, film_id, title in match:
                        episode_pull = '0%s' %episode if len(episode) <2 else episode
                        
                        if 'episode %s' %episode_pull in title.lower():
                            hash_id = hashlib.md5(episode_id + key + film_id + key2 + str(time_now) + key3).hexdigest()
                            params = {'f':film_id, 'e':episode_id, 'p':'', 't':time_now, 'a':hash_id, 's':0}
                            final_link = requests.get(request_url, params=params, headers=headers).json()
                            self.add_media(list, final_link)

                except:pass

            else:

                try:

                    film_id = re.compile('data-film="([^"]+)"').findall(link)[0]
                    episode_id = re.compile('data-eposide="([^"]+)"').findall(link)[0]
                    hash_id = hashlib.md5(episode_id + key + film_id + key2 + str(time_now) + key3).hexdigest()
                    params = {'f':film_id, 'e':episode_id, 'p':'', 't':time_now, 'a':hash_id, 's':0}
                    final_link = requests.get(request_url, params=params, headers=headers).json()
                    self.add_media(list, final_link)

                except:pass




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        from entertainment import requests
        import re

        name = self.CleanTextForSearch(name.lower())
        headers = {'User-Agent':self.User_Agent}
        search = '%s/search?keyword=%s' %(self.base_url,name.replace(' ','+'))
        link = requests.get(search, headers=headers).content
        links = link.split('item">')
        
        for p in links:

            try:

               media_url = re.compile('href="(.+?)"').findall(p)[0]
               if self.base_url not in media_url:
                   media_url = self.base_url + media_url
               media_title = re.compile('title="(.+?)"').findall(p)[0]
               qual = re.compile('class="label">(.+?)</').findall(p)[0].strip()

               if type == 'tv_episodes':
                   if name in self.CleanTextForSearch(media_title.lower()):
                       if 'season %s' %season in media_title.lower():
                           self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type, year)
                        
               else:
                   if name in self.CleanTextForSearch(media_title).lower():
                       self.GetFileHosts(media_url, list, lock, message_queue, '', '', type, year)

            except:pass
 
