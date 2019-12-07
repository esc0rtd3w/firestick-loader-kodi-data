'''
    Ice Channel
    icefilms.info
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.xgoogle.search import GoogleSearch
import os

class IceFilms(MovieIndexer, MovieSource, TVShowIndexer, TVShowSource, CustomSettings):
    implements = [MovieIndexer, MovieSource, TVShowIndexer, TVShowSource, CustomSettings]
    
    name = "IceFilms"
    display_name ="Ice Films"
    base_url = 'http://www.icefilms.info/'
    img = 'https://raw.githubusercontent.com/Coolwavexunitytalk/images/93da52d618fa7c27b00eee25018f6a6d3fee7b04/icefilms.png'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'true'
	
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'
    ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    
    cookie_file = os.path.join(common.cookies_path, 'icefilms.cookie')
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="General">\n'
        xml += '<setting id="custom_urls" type="labelenum" label="URL" default="http://ipv6.icefilms.info/" values="Custom|http://ipv6.icefilms.info/|http://www.icefilms.info/|http://80.82.65.150/" />\n'
        xml += '<setting id="custom_text_url" type="text" label="     Custom" default="http://ipv6.icefilms.info/" enable="eq(-1,0)" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
        
    def get_url(self):
        custom_url = self.Settings().get_setting('custom_urls')
        if custom_url == 'Custom':
            custom_url = self.Settings().get_setting('custom_text_url')
        if not custom_url.startswith('http://'):
            custom_url = ('http://' + custom_url)
        if not custom_url.endswith('/'):
            custom_url += '/'
        return custom_url
    
    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 

        import urllib
        url = urllib.unquote_plus(url)
        
        custom_url = self.get_url()
        
        import re
        new_url = url
        if not new_url.startswith(custom_url):
            new_url = re.sub("http\://.*?/", custom_url, url)
        
        if sort_by == '' and 'added' not in new_url and 'release' not in new_url and 'popular' not in new_url and 'rating' not in new_url and 'a-z' not in new_url:
            sort_by = 'popular'            
        if 'added' not in new_url and 'release' not in new_url and 'popular' not in new_url and 'rating' not in new_url and 'a-z' not in new_url:
            new_url = new_url + sort_by + '/' + section
        
        from entertainment.net import Net
        net = Net(cached=False)
        headers = {
            'Referer': self.get_url(),
            'Accept': self.ACCEPT,
            'User-Agent': self.USER_AGENT
        }        
        content = net.http_GET(new_url,headers=headers).content
        
        self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
        
        if type == 'movies':
            for item in re.finditer(r"<a href=/ip\.php\?v=(.+?)>(.+?)</a>", content):
                item_v_id = item.group(1)
                item_title = item.group(2)
                item_year = re.search("\(([0-9]+)\)", item_title)
                if item_year:
                    item_year = item_year.group(1)
                else:
                    item_year = ''
                item_name = re.sub(" \([0-9]+\)", "", item_title )
                
                item_url = custom_url+'membersonly/components/com_iceplayer/video.php?h=331&w=719&vid='+item_v_id+'img='        
                
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, '', type, url=item_url, name=item_name, year=item_year)
        elif type == 'tv_shows':
            for item in re.finditer(r"<a href=/tv/series/(.+?)>(.+?)</a>", content):
                item_v_id = item.group(1)
                item_title = item.group(2)
                item_year = re.search("\(([0-9]+)\)", item_title)
                if item_year:
                    item_year = item_year.group(1)
                else:
                    item_year = ''
                item_name = re.sub(" \([0-9]+\)", "", item_title )
                
                item_url = custom_url+'tv/series/'+item_v_id                    
                
                self.AddContent(list, indexer, common.mode_Content, item_title, '', 'tv_seasons', url=item_url, name=item_name, year=item_year)
    
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        
        custom_url = self.get_url()
        
        import re
        new_url = url
        if not new_url.startswith(custom_url):
            new_url = re.sub("http\://.*?/", custom_url, url)
        
        from entertainment.net import Net
        net = Net(cached=False)
        headers = {
            'Referer': self.get_url(),
            'Accept': self.ACCEPT,
            'User-Agent': self.USER_AGENT
        }     		
        content = net.http_GET(new_url, headers=headers).content
        
        if type == 'tv_seasons':
            for item in re.finditer('</a>Season ([0-9]+)', content):
                item_url = new_url
                item_v_id = item.group(1)
                
                item_title = 'Season ' + item_v_id
                
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                
                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, year=year, season=item_v_id)
        elif type == 'tv_episodes':
            season_content = re.search('>Season ' + season + ' (.*)', content).group(1)
            
            for item in re.finditer(r"<a href=/ip\.php\?v=(.+?)>" + season + "x([0-9]+) (.+?)</a>", season_content):
                
                item_v_id = item.group(1)
                item_v_id_2 = str(int(item.group(2)))
                item_title = item.group(3)
                
                item_url = custom_url+'membersonly/components/com_iceplayer/video.php?h=331&w=719&vid='+item_v_id+'img='
                
                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + season + '_episode_' + item_v_id_2)
                                
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, year=year, season=season, episode=item_v_id_2)
            
    
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        url_type = ''
        content_type = ''
        
        custom_url = self.get_url()
        
        if indexer == common.indxr_Movies:
            url_type = 'movies/'
        elif indexer == common.indxr_TV_Shows:
            url_type = 'tv/'
            
        if section == 'main':
            self.AddSection(list, indexer, 'a_z', 'A-Z')
            self.AddSection(list, indexer, 'genres', 'Genres')
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer, 'hd', 'HD', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'popular', 'Most Popular', custom_url+url_type+'popular/1', indexer)
            self.AddSection(list, indexer, 'rating', 'Highly Rated', custom_url+url_type+'rating/1', indexer)
            self.AddSection(list, indexer, 'release', 'Date Released', custom_url+url_type+'release/1', indexer)
            self.AddSection(list, indexer, 'added', 'Date Added', custom_url+url_type+'added/1', indexer)
        elif section == 'a_z':
            self.AddSection(list, indexer, '123', '#123', custom_url+url_type+'a-z/1', indexer)
            A2Z=[chr(i) for i in xrange(ord('A'), ord('Z')+1)]
            for letter in A2Z:
                self.AddSection(list, indexer, letter.lower(), letter, custom_url+url_type+'a-z/' + letter, indexer)
        elif section == 'genres':
            self.AddSection(list, indexer, 'action', 'Action', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'animation', 'Animation', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'comedy', 'Comedy', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'documentary', 'Documentary', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'drama', 'Drama', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'family', 'Family', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'horror', 'Horror', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'romance', 'Romance', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'sci-fi', 'Sci-Fi', custom_url+url_type, indexer)
            self.AddSection(list, indexer, 'thriller', 'Thriller', custom_url+url_type, indexer)
        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)    
                
            
    def GetFileHosts(self, url, list, lock, message_queue): 

        from entertainment.net import Net
        net = Net(cached=False)
        
        custom_url = self.get_url()
        
        source_args = {
              'iqs': '',
              'url': '',
              'cap': ' '
          }
        headers = {
            'Referer': self.get_url(),
            'Accept': self.ACCEPT,
            'User-Agent': self.USER_AGENT
        }        
        content = net.http_GET(url, headers=headers).content
   
        import random
        import copy
        import urllib
        import re
        
        sec = re.search("f\.lastChild\.value=\"(.+?)\",a", content).group(1)        
        source_args['sec'] = sec
        
        t = re.search('"&t=([^"]+)",', content).group(1)
        source_args['t'] = t           
        
        ajax_url = custom_url + 'membersonly/components/com_iceplayer/video.phpAjaxResp.php'
        ajax_referrer = url 
        headers = {'Referer':ajax_referrer, 'Content-type':'application/x-www-form-urlencoded', 'Accept': '*/*','User-Agent': self.USER_AGENT}
        for sq in re.finditer(r"<div class=ripdiv><b>(.+?)</b><p>(.+?)<p></div>", content):
            
            quality = sq.group(1)
            if 'DVD' in quality:
                quality = 'DVD'

            elif '1080' in quality:
                quality = '1080P'                
            elif '720' in quality:
                quality = '720P'
                
            else:
                quality = 'SD'
            for source in re.finditer(r"onclick.+?go\((.+?)\)", sq.group(2)):                
                a = source.group(1)
                
                m = int(re.search('(?:\s+|,)m\s*=(\d+)', content).group(1)) + random.randrange(20, 500)
                s = int(re.search('(?:\s+|,)s\s*=(\d+)', content).group(1)) + random.randrange(2, 500)
                source_params = copy.copy(source_args)
                cache_source_params = copy.copy(source_args)
                source_params['id'] = a
                cache_source_params['id'] = a
                source_params['m'] = m
                source_params['s'] = s
              
                ajax_content = net.http_POST(ajax_url+"?s="+a+"&t="+t, source_params, headers=headers, form_data_for_cache=cache_source_params).content
            
                host_url = 'http'+urllib.unquote(re.search(r"http(.*)", ajax_content).group(1))
             
                self.AddFileHost(list, quality, host_url)
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        custom_url = self.get_url()
        
        found_in_recent_added = False
        
        from entertainment.net import Net
        net = Net(cached=False)
        import re
        if type == 'movies':
            headers = {
                'Referer': self.get_url(),
                'Accept': self.ACCEPT,
                'User-Agent': self.USER_AGENT
            }        
            content = net.http_GET(custom_url+'movies/added/1', headers=headers).content
            content = content.replace('><', '>\n<')
            item = re.search(r"<a href=/ip\.php\?v=(.+?)>" + 
                    title.replace('(', '\\(').replace(')', '\\)').replace('-', '\\-').replace('?', '\\?').replace('*', '\\*').replace('+', '\\+') + 
                    "</a>", content)
            if item:
                item_v_id = item.group(1)
                item_url = custom_url+'membersonly/components/com_iceplayer/video.php?h=331&w=719&vid='+item_v_id+'img='                    
                self.GetFileHosts(item_url, list, lock, message_queue)
                found_in_recent_added = True
        
        if found_in_recent_added == True:
            return
        
        search_term = self.CleanTextForSearch(name)
        ttl_extrctr = '(.+?) \('
        if type == 'tv_episodes':
            se = season + 'x'
            if int(episode) < 10:
                se = se + '0' + episode
            else:
                se = se + episode
                
            search_term = search_term + ' ' + se
            
            ttl_extrctr = '(.+? [0-9]+x[0-9]+)'
            
        movie_url = self.GoogleSearchByTitleReturnFirstResultOnlyIfValid(self.base_url, search_term, 'ip', item_count=5, 
            title_extrctr=ttl_extrctr, exact_match=True)

        if movie_url != '':
            import re
            import urllib
            movie_v_id = re.search('ip\.php\?v=(.*)', urllib.unquote(movie_url))
            if movie_v_id:
                movie_v_id = movie_v_id.group(1)
                movie_url = movie_url = custom_url+'membersonly/components/com_iceplayer/video.php?h=331&w=719&vid='+movie_v_id+'img='   
                self.GetFileHosts(movie_url, list, lock, message_queue)
                
    def GetSortByOptions(self): 
        
        from entertainment import odict
        sort_by_dict = odict.odict()
        
        sort_by_dict['added'] = 'Date Added'
        sort_by_dict['release'] = 'Date Released'
        sort_by_dict['popular'] = 'Popular'
        sort_by_dict['rating'] = 'Rating'
        
        return sort_by_dict
    
    def GetSortOrderOptions(self): 
        
        from entertainment import odict
        sort_order_dict = odict.odict()
        
        return sort_order_dict
        
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        
        custom_url = self.get_url()
        
        if type != 'movies':
            return
        
        if page != '' and total_pages != '' and int(page) > int(total_pages):
            self.AddInfo(list, srcr, 'search', self.base_url, type, page, total_pages)
            return
            
        import re
        
        keywords = self.CleanTextForSearch(keywords)
        
        if page == '':
            page = '1'
        
        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'
        
        results = self.GoogleSearch(self.base_url, keywords, 'ip.php', int(page) )
        
        result_avlbl = False
        
        for result in results:

            result_title = result['title']
            result_url = result['url']
            
            if re.search('([0-9]+x[0-9]+)', result_title):
                continue
            
            result_name = re.search('(.+?)\(', result_title)            
            if result_name:
                result_name = result_name.group(1)
            else:
                continue
                 
            result_year = re.search('\((.+?)\)', result_title)
            if result_year:
                result_year = result_year.group(1)
            else:
                continue
                
            result_v_id = re.search('ip\.php\?v=(.*)', result_url)
            if result_v_id:
                result_v_id = result_v_id.group(1)
                result_url = custom_url+'membersonly/components/com_iceplayer/video.php?h=331&w=719&vid='+result_v_id+'img='              
            else:
                continue
            
                
            if result_avlbl == False:
                total_pages = str(int(page) + 1)
                self.AddInfo(list, srcr, 'search', self.base_url, type, page, total_pages)
                result_avlbl = True
                
            self.AddContent(list, srcr, mode, result_name + ' (' + result_year + ')', '', type, url=result_url, name=result_name, year=result_year)
        
        if result_avlbl == False:
            total_pages = str(int(page) - 1)
            self.AddInfo(list, srcr, 'search', self.base_url, type, '0' if total_pages == '0' else page, total_pages)
            result_avlbl = True
