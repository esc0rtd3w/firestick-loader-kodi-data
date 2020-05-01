'''
    Ice Channel
    1channel.ch primewire.ag letmewatchthis.ch
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

do_no_cache_keywords_list = ['<title>Are You a Robot']

class primewireag(MovieIndexer, MovieSource, TVShowIndexer, TVShowSource, CustomSettings):
    implements = [MovieIndexer, MovieSource, TVShowIndexer, TVShowSource, CustomSettings]
    
    name = "primewireag"
    display_name = "Prime Wire"
    base_url = 'http://www.primewire.org/'
    img = 'https://raw.githubusercontent.com/Coolwavexunitytalk/images/93da52d618fa7c27b00eee25018f6a6d3fee7b04/primewire.png'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'true'
    
    codes = [
        17,
        #14,
        #15
        ]
    
    proxies = [
        [102, 49, 101, 56, 70, 56, 72, 46, 116, 57, 82, 53, ],
        [77, 46, 36, 53, 123, 48, 107, 46, 97, 49, 89, 50, ],
        [68, 49, 67, 48, 68, 56, 87, 48, ],
        #[41, 50, 78, 48, 108, 57, 56, 46, 98, 50, 82, 48, 74, 56, 110, 46, ],
        #[101, 49, 51, 48, 45, 56, 124, 46, 116, 53, 83, 49, ],
        #[126, 49, 43, 48, 43, 56, 69, 48, ],
        #[88, 50, 105, 48, 36, 57, 48, 46, 107, 50, 37, 48, 124, 56, 124, 46, ],
        #[103, 49, 65, 49, 93, 49, 35, 46, 121, 49, 98, 55, 126, 54, ],
        #[114, 49, 39, 48, 32, 56, 118, 48, ]
        ]
        
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="General">\n'
        xml += '<setting id="custom_url" type="labelenum" label="URL" default="http://www.primewire.org/" values="Custom|http://www.1channel.ch/|http://www.primewire.org/|http://www.letmewatchthis.ch/|http://www.primewire.ag/" />\n'
        xml += '<setting id="custom_text_url" type="text" label="     Custom" default="" enable="eq(-1,0)" />\n'
        xml += '<setting id="proxy" type="bool" label="Proxy for UK" default="false"/>\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)
        
    def get_url(self):
        custom_url = self.Settings().get_setting('custom_url')
        if custom_url == 'Custom':
            custom_url = self.Settings().get_setting('custom_text_url')
        if not custom_url.startswith('http://'):
            if custom_url.startswith('https://'):
                custom_url=custom_url
            else:    
                custom_url = ('http://' + custom_url)
        if not custom_url.endswith('/'):
            custom_url += '/'
        return custom_url
        
    def get_proxy(self):    
        from random import randint
        times = ( len(self.proxies) / 3 )
        idx = randint(0, 0x7fffffff) % times
        idx = idx * times
        
        return ( common.ttTTtt(self.codes[idx/times], self.proxies[idx], self.proxies[idx+1]), int ( common.ttTTtt(4, self.proxies[idx+2]) ) )
                
    
    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        import urllib
        
        if section != 'search':
            url = urllib.unquote_plus(url)
            
        custom_url = self.get_url()
        
        import re
        new_url = url
        if not new_url.startswith(custom_url):
            new_url = re.sub("http\://.*?/", custom_url, url)
        
        if page == '':
            page = '1'
        else:
            page = str( int(page) )
            new_url = new_url + '&page=' + page
            
        if sort_by == '' and 'sort' not in new_url:
            sort_by = 'date'            
        if 'sort' not in new_url:
            new_url = new_url + '&sort=' + sort_by    
        
        from entertainment.net import Net
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        if self.Settings().get_setting('proxy') == "true":
            import socks
            ( proxy, port ) = self.get_proxy()
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy, port )
            net.set_socket_class(socks.socksocket)
        
        new_url_for_cache = re.sub('\?key=.+?&', '?', new_url)
        content = net.http_GET(new_url, url_for_cache=new_url_for_cache).content

        if total_pages == '' :
            total_pages = re.search('</a> <a href="/.+?&page=([0-9]*)"> >> </a></div>', content)
            if total_pages:
                total_pages = total_pages.group(1)
            else:
                if re.search('0 items found', content):
                    page = '0'
                    total_pages = '0'
                else:
                    page = '1'
                    total_pages = '1'
            
        self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
        
        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'
                
        for item in re.finditer(r'<a href="(.+?)" title="Watch (.+?)"><img src=', content):
            item_v_id = item.group(1)            
            item_title = common.addon.unescape(item.group(2))
            item_year = re.search("\(([0-9]+)\)", item_title)
            if item_year:
                item_year = item_year.group(1)
            else:
                item_year = ''
            item_name = re.sub(" \([0-9]+\)", "", item_title )
            
            if item_v_id[0] == '/':
                item_v_id = item_v_id[1:]
                item_url = custom_url + item_v_id
            else:
                item_url = item_v_id
            
            if total_pages == '':
                total_pages = '1'
                
            self.AddContent(list, indexer, mode, item_title, '', type, url=item_url, name=item_name, year=item_year)

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
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        if self.Settings().get_setting('proxy') == "true":
            import socks
            ( proxy, port ) = self.get_proxy()
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy, port )
            net.set_socket_class(socks.socksocket)
        
        content = net.http_GET(new_url).content
        
        if type == 'tv_seasons':#<h2><a href="(.+?)">Season ([0-9]+)</a></h2>
            for item in re.finditer('<a data-id=".+?" class="season-toggle" href="(.+?)">.+? Season ([0-9]+)<', content):
                item_url = item.group(1)
                if item_url[0] == '/':
                    item_url = item_url[1:]
                    item_url = custom_url + item_url

                item_v_id = item.group(2)
                item_title = 'Season ' + item_v_id
                
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                
                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, year=year, season=item_v_id)
                
        elif type == 'tv_episodes':#<div class="tv_episode_item"> <a href="(.+?)">E[0-9]+)\s*<span class="tv_episode_name"> - (.+?)</span>
        
            for item in re.finditer('<div class="tv_episode_item"> <a href="(.+?)">E([0-9]+)\s*<span class="tv_episode_name"> - (.+?)</span>', content):
                item_url = item.group(1)
                if item_url[0] == '/':
                    item_url = item_url[1:]
                    item_url = custom_url + item_url
                item_v_id = item.group(2)
                item_title = item.group(3)
                if item_title == None:
                    item_title = ''
                
                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + season + '_episode_' + item_v_id)
                
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, year=year, season=season, episode=item_v_id)
        
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        url_type = ''
        content_type = ''
        
        custom_url = self.get_url()

        if indexer == common.indxr_Movies:
            url_type = ''
        elif indexer == common.indxr_TV_Shows:
            url_type = 'tv&'
            
        if section == 'main':
            self.AddSection(list, indexer, 'a_z', 'A-Z')
            self.AddSection(list, indexer, 'genres', 'Genres')
            self.AddSection(list, indexer, 'featured', 'Featured', custom_url+'?' + url_type + 'sort=featured', indexer)
            self.AddSection(list, indexer, 'views', 'Most Popular', custom_url+'?' + url_type + 'sort=views', indexer)
            self.AddSection(list, indexer, 'ratings', 'Highly Rated', custom_url+'?' + url_type + 'sort=ratings', indexer)
            self.AddSection(list, indexer, 'release', 'Date Released', custom_url+'?' + url_type + 'sort=release', indexer)
            self.AddSection(list, indexer, 'date', 'Date Added', custom_url+'?' + url_type + 'sort=date', indexer)
        elif section == 'genres':
            
            from entertainment.net import Net
            net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
            
            if self.Settings().get_setting('proxy') == "true":
                import socks
                ( proxy, port ) = self.get_proxy()
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy, port )
                net.set_socket_class(socks.socksocket)
            
            content = net.http_GET(custom_url + '?' + url_type).content
            
            import re
            genres = re.compile('<ul class="menu-genre-list">(.+?)</ul>').findall(content)[0]
            if genres:
                #genres = genres.group(1)
                for genre in re.finditer('<li><a href="(.+?)">(.+?)</a></li>', genres):
                    genre_url = genre.group(1)
                    if genre_url[0] == '/':
                        genre_url = genre_url[1:]
                        genre_url = custom_url + genre_url
                    genre_title = genre.group(2)
                    genre_section = genre_title.lower()
                    
                    self.AddSection(list, indexer, genre_section, genre_title, genre_url, indexer)
            
        elif section == 'a_z':
            self.AddSection(list, indexer, '123', '#123', custom_url+'?' + url_type + 'letter=123', indexer)
            A2Z=[chr(i) for i in xrange(ord('A'), ord('Z')+1)]
            for letter in A2Z:
                self.AddSection(list, indexer, letter.lower(), letter, custom_url+'?' + url_type + 'letter=' + letter.lower(), indexer)                
        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
            
    def GetFileHosts(self, url, list, lock, message_queue): 
        from entertainment.net import Net
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        custom_url = self.get_url()
        
        if self.Settings().get_setting('proxy') == "true":
            import socks
            ( proxy, port ) = self.get_proxy()
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy, port )
            net.set_socket_class(socks.socksocket)

        content = common.unescape(common.str_conv(net.http_GET(url).content))

        import re
        #print content
        for sq in re.finditer(r"quality_(.+?)>.+?url=(.+?)&", content):

            quality = sq.group(1).upper()
            quality = quality.replace('"','')
            
            if quality == 'UNKNOWN':
                continue

            import base64
            host_url = base64.b64decode(sq.group(2))
   
            if not 'affbuzz' in host_url.lower():
                if not 'ads.ad-center.com' in host_url.lower():
                    if not 'offer?' in host_url.lower():
                        #print quality
                        self.AddFileHost(list, quality, host_url)
    
    def SearchContent(self, search_key, search_keywords, type, year):
        from entertainment.net import Net
        net = Net(do_not_cache_if_any=do_no_cache_keywords_list)
        
        if self.Settings().get_setting('proxy') == "true":
            import socks
            ( proxy, port ) = self.get_proxy()
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy, port )
            net.set_socket_class(socks.socksocket)
        
        custom_url = self.get_url()

        import re
        
        import urllib
        search_dict = {'key':search_key,
            'search_keywords':search_keywords,
            'search_section':'1' if type == 'movies' else '2',
            'year':year
            }        
        search_for_url = custom_url + 'index.php?' + urllib.urlencode(search_dict)
        
        from entertainment import odict
        search_dict_for_cache = odict.odict(search_dict)
        search_dict_for_cache.update({'key': ''})
        search_dict_for_cache.sort(key=lambda x: x[0].lower())
        search_for_url_for_cache = custom_url + 'index.php?' + urllib.urlencode(search_dict_for_cache)
        
        search_results = common.unescape(common.str_conv(net.http_GET(search_for_url, url_for_cache=search_for_url_for_cache).content))
        search_content = None
        

        #print search_results    
        for search_item in re.finditer(r"<div class=\"index_item.+?\"><a href=\"(.+?)\" title=\"Watch (.+?)\"", search_results):            
            
            searchitem = search_item.group(2)
            if year == '0' or year == '':
                searchitem = re.sub(' \([0-9]+\)', '', searchitem)

            if common.CreateIdFromString(searchitem) == common.CreateIdFromString( search_keywords + (' (' + year + ')' if year != '0' and year != '' else '') ):
                search_content = search_item
                break
                
        return search_content
    
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue): 
        from entertainment.net import Net
        net = Net(cached = False, do_not_cache_if_any=do_no_cache_keywords_list)
        
        if self.Settings().get_setting('proxy') == "true":
            import socks
            ( proxy, port ) = self.get_proxy()
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy, port )
            net.set_socket_class(socks.socksocket)


            
        custom_url = self.get_url()


        if 'primeware.racing' in custom_url:

            import xbmcaddon
            ADDON=xbmcaddon.Addon(id='script.icechannel.primewireag.settings')           
            ADDON.setSetting('custom_text_url','http://www.primewire.ch/')
        

        title = self.CleanTextForSearch(title) 
        name = self.CleanTextForSearch(name) 
        
        search_page_url = custom_url + 'index.php?search'
        
        search_page_content = common.unescape(common.str_conv(net.http_GET(search_page_url).content))

        if 'virginmedia.com/courtorders' in search_page_content.lower() or 'ukispcourtorders' in search_page_content.lower() or 'is not available through bskyb' in search_page_content.lower() or 'ACCESS TO THE WEBSITES LISTED ON THIS PAGE HAS BEEN BLOCKED PURSUANT TO ORDERS OF THE HIGH COURT' in search_page_content.upper():
            import xbmcaddon
            ADDON=xbmcaddon.Addon(id='script.icechannel.primewireag.settings')   
            ADDON.setSetting('custom_url','Custom')   
            ADDON.setSetting('custom_text_url','http://www.primewire.ch/')        
        
        import re
        
        search_key = re.compile('input type="hidden" name="key" value="([0-9a-f]*)"',re.DOTALL).findall(search_page_content)[0]
        
        search_content = None
        name = name.replace("'", " ")
        search_content = self.SearchContent(search_key, name, type, year)
                
        if search_content == None and ':' in name:        
            new_name = name.replace(':', ' -')
            search_content = self.SearchContent(search_key, new_name, type, year)
                    
            if search_content == None and (new_name.endswith('s') or new_name.endswith('?')):
                new_name = new_name[:len(new_name)-1]
                search_content = self.SearchContent(search_key, new_name, type, year)
                
                if search_content == None:
                    search_content = self.SearchContent(search_key, new_name, type, '0')
                
            if search_content == None:
                new_name = name.replace(':', '')
                search_content = self.SearchContent(search_key, new_name, type, year)
                
                if search_content == None and (new_name.endswith('s') or new_name.endswith('?')):
                    new_name = new_name[:len(new_name)-1]
                    search_content = self.SearchContent(search_key, new_name, type, year)
                
                    if search_content == None:
                        search_content = self.SearchContent(search_key, new_name, type, '0')
                    
        if search_content == None:
            search_content = self.SearchContent(search_key, name, type, '')

        if type == 'tv_episodes' and search_content:
            show_url = search_content.group(1)
            show_url = re.sub('watch-', 'tv-', show_url)
            show_url = show_url + '/season-' + season + '-episode-' + episode
            
            search_content = re.search('(.*)', show_url)
        
        if search_content:
            self.GetFileHosts(custom_url+search_content.group(1), list, lock, message_queue)
    
    def GetSortByOptions(self): 
        
        from entertainment import odict
        sort_by_dict = odict.odict()
        
        sort_by_dict['alphabet'] = 'Alphabet'
        sort_by_dict['date'] = 'Date Added'
        sort_by_dict['release'] = 'Date Released'
        sort_by_dict['featured'] = 'Featured'
        sort_by_dict['ratings'] = 'Ratings'
        sort_by_dict['views'] = 'Views'
        
        
        return sort_by_dict
    
    def GetSortOrderOptions(self): 
        
        from entertainment import odict
        sort_order_dict = odict.odict()
        
        return sort_order_dict
        
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
    
        from entertainment.net import Net
        net = Net(cached=False, do_not_cache_if_any=do_no_cache_keywords_list)
        
        if self.Settings().get_setting('proxy') == "true":
            import socks
            ( proxy, port ) = self.get_proxy()
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy, port )
            net.set_socket_class(socks.socksocket)
        
        custom_url = self.get_url()

            
              
        keywords = self.CleanTextForSearch(keywords) 
        
        search_page_url = custom_url + 'index.php?search'
        
        search_page_content = common.unescape(common.str_conv(net.http_GET(search_page_url).content))
        
        import re
        
        search_key = re.compile('input type="hidden" name="key" value="([0-9a-f]*)"',re.DOTALL).findall(search_page_content)[0]
        
        import urllib
        from entertainment import odict
        search_dict = odict.odict({'key':search_key,
            'search_keywords':keywords,
            'search_section':'1' if type == 'movies' else '2',
            'sort':'featured'
            })
        search_dict.sort(key=lambda x: x[0].lower())
                
        search_for_url = custom_url + 'index.php?' + urllib.urlencode(search_dict)
        
        self.ExtractContentAndAddtoList(srcr, 'search', search_for_url, type, list, page=page, total_pages=total_pages)
        
