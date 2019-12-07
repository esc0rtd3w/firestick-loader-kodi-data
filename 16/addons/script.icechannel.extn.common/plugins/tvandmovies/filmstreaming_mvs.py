'''
    Ice Channel
    Film-Streaming
'''


from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common
       
        
class filmstreaming(MovieSource):
    implements = [MovieSource]
    
    name = "Film-Streaming"
    display_name = "Film-Streaming"
    base_url = 'http://film-streaming.in'
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
    source_enabled_by_default = 'true'
    
    def GetFileHosts(self, url, list, lock, message_queue, qual):
        
        from entertainment.net import Net
        import re
        net = Net(cached=False) 

        headers = {'User-Agent':self.User_Agent}
        link = net.http_GET(url,headers=headers).content
        url = re.compile('iframe src="(.+?)"').findall(link)[0]
       

        label = qual.upper()   
        if label == '1080P':
            label = '1080P'
        elif label == '720P':
            label = '720P'                
        elif label == '480P':
            label = 'HD'
        else:
            label = 'SD'


        self.AddFileHost(list, label, url)




    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):
        
        from entertainment.net import Net
        import re
        net = Net(cached=False)

        
        name = self.CleanTextForSearch(name)
        headers = {'User-Agent':self.User_Agent}
        item_url = '%s/?s=%s' %(self.base_url,name.replace(' ','+'))
        link = net.http_GET(item_url,headers=headers).content
        links = link.split('class="item">')

        for p in links:
            try:
                m_url = re.compile('href="(.+?)"').findall(p)[0]
                m_title = re.compile('<h2>(.+?)</').findall(p)[0]
                qual = re.compile('"calidad2">(.+?)</').findall(p)[0]
                if name.lower() in self.CleanTextForSearch(m_title.lower()):
                    if year in m_title:
                        self.GetFileHosts(m_url, list, lock, message_queue, qual)
            except:pass




        
                
