'''
    mydownloadtubeonline
'''

from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment.xgoogle.search import GoogleSearch

class mydownloadtubeonline(MovieSource):
    implements = [MovieSource]
    
    name = "mydownloadtubeonline"
    display_name = "MyDownloadTubeOnline"
    base_url = 'http://www.mydownloadtube.com/'
    
    source_enabled_by_default = 'true'

    def GetQuality(self, quality):
        if '1080p' in quality:
            quality = '1080P'
        elif '720p' in quality:
            quality = '720P'
        elif 'HD' in quality:
            quality = 'HD'
        elif 'CAM' in quality:
            quality = 'CAM'
        elif 'TS' in quality:
            quality = 'TS'
        else:
            quality = 'SD'
            
        return quality
    
    def GetFileHosts(self, url, list, lock, message_queue, season, episode,type,year):

        from entertainment.net import Net
        import re
        net = Net(cached=False,user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')

        movie_links_url = self.base_url + 'movies/play_online'
        query = {'movie': url}
        
        content = net.http_POST(movie_links_url, query).content
        
        server_quality_list = {}
        servers_content = re.compile('<a class="servers[^"]+?" value="([^"]+?)">(.+?)</a>', re.DOTALL).findall(content)
        for server_number, quality in servers_content:
            server_quality = self.GetQuality(quality)                
            server_quality_list['server' + server_number] = server_quality
            
        sources_list = content.split('<div class="popup1 popup" ')
        for source in sources_list:
            if source.startswith('id='):
                server_id = re.search('id="([^"]+?)"', source)
                if server_id:
                    server_id = server_id.group(1)
                    server_quality = server_quality_list[server_id]
                    if 'sources:' in source:
                        import base64
                        import urllib
                        source_sources = re.search('sources:(.+?)</script>', source, re.DOTALL)
                        if source_sources:
                            source_sources = source_sources.group(1)
                            source_sources_details = re.compile('\'([^\']+?)\'[^"]+?"([^"]+?)"', re.DOTALL).findall(source_sources)
                            for source_sources_details_url, source_sources_details_quality in  source_sources_details:
                                source_sources_details_quality = self.GetQuality(source_sources_details_quality)
                                self.AddFileHost(list, source_sources_details_quality.upper(), base64.b64decode(source_sources_details_url).replace(' ', '%20'), host=self.display_name.upper().replace(' ', ''))
                    elif '<table' in source:
                        source_sources_details_url = re.search('src="([^"]+?)"', source, re.IGNORECASE)
                        if source_sources_details_url:
                            source_sources_details_url = source_sources_details_url.group(1)
                            self.AddFileHost(list, server_quality.upper(), source_sources_details_url)                        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):  
    
        from entertainment.net import Net
        import urllib
        
        import re

        net = Net(cached=False)        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name)
        
        url = self.base_url + 'search/movies/' + urllib.quote(name)
        LINK=net.http_GET(url).content
        match=re.compile('<a href="movies/[^"]+?".+?class="movie_poster_imagedisplay".+?<img.+?data-url="movies/tooltip_content/([0-9]*).+?alt="([^"]+?)"',re.DOTALL).findall(LINK)
        
        names = name.lower().split(' ')
        names_count = len(names)
        
        found_item_url = ''
        for movie_id, movie_name in match:   
            item_title = movie_name.lower()
            names_match_count = 0
            for names_item in names:
                if names_item in item_title:
                    names_match_count = names_match_count + 1
            if names_match_count / names_count * 100 >= 85:
                found_item_url = movie_id
                break;
        
        if found_item_url:
            self.GetFileHosts(found_item_url, list, lock, message_queue,season,episode,type,year)
    
