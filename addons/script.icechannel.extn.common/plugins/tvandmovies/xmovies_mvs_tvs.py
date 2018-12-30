'''
    Ice Channel
    buzzfilms.co
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment.xgoogle.search import GoogleSearch

class xmovies(MovieSource,TVShowSource):
    implements = [MovieSource,TVShowSource]
    
    name = "XMovies8"
    display_name = "XMovies8"
    base_url = 'https://xmovies8.ru'
    
    source_enabled_by_default = 'false'

    
    def GetFileHosts(self, url, list, lock, message_queue, season, episode,type,year):

        from entertainment import requests
        import re,json




        
        headers= {'accept':'application/json, text/javascript, */*; q=0.01',
                  'accept-encoding':'gzip, deflate, br',
                  'accept-language':'en-US,en;q=0.8',
                  'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                  'origin':'https://xmovies8.ru', 'referer':url,
                  'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                  'x-requested-with':'XMLHttpRequest'}

        html = requests.get(url,headers=headers,verify=False).content
        
        if type == 'tv_episodes':
            grrr=url.split('https://')[1]
            r='<a href="(.+?%s.+?)" class="active ">episode (.+?)<' % grrr
            match=re.compile(r).findall(html.lower())
            
            for new_url , ep in match:
                if episode ==ep:
                    html = requests.get(new_url,headers=headers,verify=False).content            
                    
                    matched=re.compile("load_player\('(.+?)'\)").findall(html)
                    for id in matched:

                        data={'id':id}
                        content = json.loads(requests.post('https://xmovies8.ru/ajax/movie/load_player_v3',data,headers=headers,verify=False).content)
                        second_url=content['value']
                        if not 'http' in second_url:
                            second_url='http:'+second_url
                        headers = {'accept':'application/json, text/javascript, */*; q=0.01',
                                   'accept-encoding':'gzip, deflate, sdch, br',
                                   'accept-language':'en-US,en;q=0.8', 'origin':'https://xmovies8.ru',
                                   'referer':second_url, 'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

                        content = requests.post(second_url,data,headers=headers,verify=False).content
                        link= json.loads(content)
                        DATA= link['playlist'][0]['sources']
                        for field in DATA:
                            FINAL_URL =field['file']
                            res=field['label'].upper()

                             
                            self.AddFileHost(list, res, FINAL_URL)  
        else:
            
            html = requests.get(url,headers=headers,verify=False).content            
            
            matched=re.compile("load_player\('(.+?)'\)").findall(html)
            for id in matched:

                data={'id':id}
                content = json.loads(requests.post('https://xmovies8.ru/ajax/movie/load_player_v3',data,headers=headers,verify=False).content)
                second_url=content['value']
                if not 'http' in second_url:
                    second_url='http:'+second_url
                headers = {'accept':'application/json, text/javascript, */*; q=0.01',
                           'accept-encoding':'gzip, deflate, sdch, br',
                           'accept-language':'en-US,en;q=0.8', 'origin':'https://xmovies8.ru',
                           'referer':second_url, 'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

                content = requests.post(second_url,data,headers=headers,verify=False).content
                link= json.loads(content)
                DATA= link['playlist'][0]['sources']
                for field in DATA:
                    FINAL_URL =field['file']
                    res=field['label'].upper()

                     
                    self.AddFileHost(list, res, FINAL_URL)  
                  

                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment import requests
        import re
  
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        #print ':::::::::::::::::::::::::::::::::'
        
        headers= {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                  'x-requested-with':'XMLHttpRequest'}
        
        URL='https://xmovies8.ru/movies/search?s=' + name.replace(' ','+')

        html = requests.get(URL,headers=headers,verify=False).content

        match=re.compile('<h2 class="tit"><a href="(.+?)" title="(.+?)"').findall(html)
        uniques=[]
        for movie_url, TITLE in match:


            if type == 'tv_episodes':
                if name.lower() in TITLE.lower():
                    if 'season '+season in TITLE.lower():
                        if movie_url not in uniques:
                            uniques.append(movie_url)                        
                            self.GetFileHosts(movie_url+'watching.html', list, lock, message_queue,season, episode,type,year)
            else:
                if name.lower() in TITLE.lower():
                   
                    if year in TITLE.lower():
                        if movie_url not in uniques:
                            uniques.append(movie_url)
             
                            self.GetFileHosts(movie_url+'watching.html', list, lock, message_queue,season, episode,type,year)
                        

    def googletag(self,url):
        import re
        quality = re.compile('itag=(\d*)').findall(url)
        quality += re.compile('=m(\d*)$').findall(url)
        try: quality = quality[0]
        except: return []

        if quality in ['37', '137', '299', '96', '248', '303', '46']:
            return [{'quality': '1080P', 'url': url}]
        elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
            return [{'quality': '720P', 'url': url}]
        elif quality in ['35', '44', '135', '244', '94']:
            return [{'quality': 'SD', 'url': url}]
        elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
            return [{'quality': 'SD', 'url': url}]
        elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
            return [{'quality': 'SD', 'url': url}]
        else:
            return []

    
    def Resolve(self, url):
        #if 'http' in url:
            #from entertainment import istream
            #url =istream.ResolveUrl(url)
        #else:

            
        return url
            
                
                
