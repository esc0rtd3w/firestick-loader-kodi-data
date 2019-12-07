'''
    Superchillin    
    Copyright (C) 2013 Xunitytalk
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common
import os
from entertainment.xgoogle.search import GoogleSearch
import xbmc
import xbmcgui



do_no_cache_keywords_list = ["alert('Please Login!');"]

class superchillin(MovieIndexer,TVShowIndexer,MovieSource,TVShowSource,CustomSettings):
    implements = [MovieIndexer,TVShowIndexer,MovieSource,TVShowSource,CustomSettings]
    
    name = "superchillin"
    display_name = "[COLOR royalblue]S[/COLOR]uperchillin"
    base_url = 'http://superchillin.com/'
    img='http://oi60.tinypic.com/2qunhvr.jpg'
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'false'
    cookie_file = os.path.join(common.cookies_path, 'SClogin.cookie')
    icon = common.notify_icon
    
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="tv_user" type="text" label="Email" default="Enter your Superchillin email" />\n'
        xml += '<setting id="tv_pwd" type="text" option="hidden" label="Password" default="xunity" />'
        xml += '<setting label="Premium account will allow for 1080 movies and the TV Shows section" type="lsep" />\n'
        xml += '<setting id="premium" type="bool" label="Enable Premium account" default="false" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)


    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        if section == 'latest':
            
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')


            if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
                if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                              7000, self.icon)
                return
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                       'Referer': 'http://superchillin.com/login.php',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


            net.http_GET('http://superchillin.com/login.php')
            net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)


            import urllib        
            
            html = net.http_GET(url).content
            if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Noobroom',
                                              '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                              7000, self.icon)               
                
            match=re.compile("<br>(.+?) - <a[^>]+?href='(.+?)'>(.+?)</a>").findall(html)#[:25]#, [26:50]
            
            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for year,url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url + url
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + '[COLOR red]'+year+'[/COLOR]' +')','',type, url=url, name=name, year=year)


            

        elif section == 'azlist':
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')


            if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
                if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                              7000, self.icon)
                return
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                       'Referer': 'http://superchillin.com/login.php',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


            net.http_GET('http://superchillin.com/login.php')
            net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)


            import urllib        
            
            html = net.http_GET(url).content
            if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                              7000, self.icon)

            match=re.compile("href='/(.+?)'>(.+?)</a><br>").findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url + url
                self.AddContent(list,indexer,common.mode_File_Hosts,name,'',type, url=url, name=name)

        elif section == 'year':
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')


            if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
                if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                              7000, self.icon)
                return
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                       'Referer': 'http://superchillin.com/login.php',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


            net.http_GET('http://superchillin.com/login.php')
            net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)


            import urllib        
            
            html = net.http_GET(url).content
            if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                              7000, self.icon)
                
            match=re.compile("<br>(.+?) - <a[^>]+?href='(.+?)'>(.+?)</a>").findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for year,url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url + url
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + '[COLOR red]'+year+'[/COLOR]' +')','',type, url=url, name=name, year=year)

        elif section == 'rating':
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')


            if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
                if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                              7000, self.icon)
                return
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                       'Referer': 'http://superchillin.com/login.php',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


            net.http_GET('http://superchillin.com/login.php')
            net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)


            import urllib        
            
            html = net.http_GET(url).content
            if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                              7000, self.icon)
                
            match=re.compile("<br><b>(.+?)</b> - (.+?) - <a[^>]+?href='(.+?)'>(.+?)</a>").findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for rating,year,url,name in match:
                name = self.CleanTextForSearch(name)#href='/?3304'>Annie</a> - PG</div>
                url = self.base_url + url
                self.AddContent(list,indexer,common.mode_File_Hosts,name +' ('+'[COLOR royalblue]'+rating+'[/COLOR])'+' (' + '[COLOR red]'+year+'[/COLOR]' +')','',type, url=url, name=name, year=year)

        elif section == 'kids':
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')


            if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
                if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                              7000, self.icon)
                return
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                       'Referer': 'http://superchillin.com/login.php',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


            net.http_GET('http://superchillin.com/login.php')
            net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)


            import urllib        
            
            html = net.http_GET(url).content
            if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                              7000, self.icon)
                
            match=re.compile("<b><a style=\'color:#fff\' href=\'(.+?)\'>(.+?)</a> - (.+?)</div>").findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for url,name,pg in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url + url
                pg = '[COLOR royalblue]'+pg+'[/COLOR]'
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + pg +')','',type, url=url, name=name)

        elif section == 'random':
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')


            if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
                if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                              7000, self.icon)
                return
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                       'Referer': 'http://superchillin.com/login.php',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


            net.http_GET('http://superchillin.com/login.php')
            net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)


            import urllib        
            
            html = net.http_GET(url).content
            if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Noobroom',
                                              '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                              7000, self.icon)
                
            match=re.compile('<a title="The Internet Movie Database" style="text-decoration: none; color: .+? href="(.+?)"').findall(html)
            for url in match:
                html2 = net.http_GET(url).content
                match2=re.compile('<title>(.+?) (\([\d]{4}\)) - IMDb</title>').findall(html2)
                for name,year in match2:
                                    
                    name = self.CleanTextForSearch(name)
                    url = self.base_url
                    year=year.replace('(','').replace(')','')
                    self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + '[COLOR red]'+year+'[/COLOR]' +')','',type, url=url, name=name, year=year)

        elif section == 'tvshows':
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')


            if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
                if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                              7000, self.icon)
                return
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                       'Referer': 'http://superchillin.com/login.php',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


            net.http_GET('http://superchillin.com/login.php')
            net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)


            import urllib        
            
            html = net.http_GET(url).content
            if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                              7000, self.icon)
                
            match=re.compile("href='/(.+?)'>(.+?)</a></b><br><br>\s*<span style='color:.+?;font-size:14px'>.+?Latest: (.+?) - <b>").findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for url,name,eps in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url + url
                self.AddContent(list, indexer, common.mode_Content, name+ ' (' + '[COLOR red]'+eps+'[/COLOR]' +')', '', 'tv_seasons', url=url, name=name)

        elif section == 'tvshowsadded':
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')


            if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
                if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                              7000, self.icon)
                return
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                       'Referer': 'http://superchillin.com/login.php',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


            net.http_GET('http://superchillin.com/login.php')
            net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)


            import urllib        
            
            html = net.http_GET(url).content
            if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                              7000, self.icon)
                
            match=re.compile("<a href='(.+?)'><img style='border:0' src='(.+?)' width='53' height='79'></a>.+?<a style='color:#fff' href='.+?'>(.+?)</a></b><br><br>.+?Latest: (.+?) - <b><span style='color:#fff'>(.+?)</span>",re.DOTALL).findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for url,image,name,eps,title in match:
                url = 'http://superchillin.com'+url
    
                name = self.CleanTextForSearch(name)
                
                self.AddContent(list, indexer, common.mode_Content, name+ ' (' + '[COLOR red]'+eps+'[/COLOR]' +')', '', 'tv_seasons', url=url, name=name)

        else:
            from entertainment.net import Net
            import re
            net = Net(cached=False)

            tv_user = self.Settings().get_setting('tv_user')
            tv_pwd = self.Settings().get_setting('tv_pwd')


            if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
                if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass

                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                              7000, self.icon)
                return
                

            if os.path.exists(self.cookie_file):
                    try: os.remove(self.cookie_file)
                    except: pass
                    
            headers = {'Content-Type': 'application/x-www-form-urlencoded',
                       'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                       'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                       'Referer': 'http://superchillin.com/login.php',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


            net.http_GET('http://superchillin.com/login.php')
            net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
            net.save_cookies(self.cookie_file)
            net.set_cookies(self.cookie_file)


            import urllib        
            
            html = net.http_GET(url).content
            if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
                common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                              '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                              7000, self.icon)
                
            match=re.compile("<br>(.+?) - <a[^>]+?href='(.+?)'>(.+?)</a>").findall(html)

            ''' Pagination Code Start '''
            num_items_on_a_page = 25
            if page == '':                
                page = '1'
                total_items = len(match)
                total_pages = str ( ( total_items / num_items_on_a_page ) + ( 1 if total_items % num_items_on_a_page >= 1 else 0) )
                
            self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)
            
            start_index = ( int(page) - 1 ) * num_items_on_a_page
            match = match[ start_index : start_index + num_items_on_a_page  ]
            ''' Pagination Code End '''
            
            for year,url,name in match:
                name = self.CleanTextForSearch(name)
                url = self.base_url + url
                self.AddContent(list,indexer,common.mode_File_Hosts,name + ' (' + '[COLOR red]'+year+'[/COLOR]' +')','',type, url=url, name=name, year=year)           

                    
       
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        name = (name).lower()
        
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        net.set_cookies(self.cookie_file)

        content = net.http_GET(url).content
        
        if type == 'tv_seasons':
            match=re.compile('<br><br><b>(.+?)x').findall(content)
            for seasonnumber in match:                
                item_title = 'Season ' + seasonnumber
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                

                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=url, name=name, season=seasonnumber)
               
        elif type == 'tv_episodes':
            match=re.compile("<br><b>"+season+"x(.+?)\s-\s<a style=.+?color.+?\shref='/(.+?)'>(.+?)</a>").findall(content)
            for item_v_id_2,url,item_title  in match:
                season = "0%s"%season if len(season)<2 else season
                item_v_id_2 = "0%s"%item_v_id_2 if len(item_v_id_2)<2 else item_v_id_2
                item_url = self.base_url + url
                item_v_id_2 = str(int(item_v_id_2))
                item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + item_v_id_2)
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=item_v_id_2)
            

        
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        
        net = Net(cached=False)

        url_type = ''
        content_type = ''
        
        if indexer == common.indxr_Movies:#'[COLOR orange]'+year+'[/COLOR]'

            if section == 'main':
                self.AddSection(list, indexer,'latest','[COLOR royalblue]Ordered[/COLOR] by Latest',self.base_url +'latest.php',indexer)
                self.AddSection(list, indexer,'azlist','[COLOR royalblue]Ordered[/COLOR] by A-Z',self.base_url +'azlist.php',indexer)
                self.AddSection(list, indexer,'year','[COLOR royalblue]Ordered[/COLOR] by Release Date',self.base_url +'year.php',indexer)
                self.AddSection(list, indexer,'rating','[COLOR royalblue]Ordered[/COLOR] by IMDb Rating',self.base_url +'rating.php',indexer)
                self.AddSection(list, indexer,'genre','[COLOR royalblue]Ordered[/COLOR] by Genre',self.base_url +'genre.php',indexer)
                self.AddSection(list, indexer,'kids','[COLOR royalblue]Kids[/COLOR] Zone',self.base_url +'kids.php',indexer)
                self.AddSection(list, indexer,'random','[COLOR royalblue]Random[/COLOR] Movie',self.base_url + 'random.php',indexer)            
                           
            elif section == 'genre':
                self.AddSection(list, indexer,'action','Action',self.base_url +'genre.php?b=10000000000000000000000000',indexer)
                self.AddSection(list, indexer,'adventure','Adventure',self.base_url +'genre.php?b=01000000000000000000000000',indexer)
                self.AddSection(list, indexer,'animation','Animation',self.base_url +'genre.php?b=00100000000000000000000000',indexer)
                self.AddSection(list, indexer,'biography','Biography',self.base_url +'genre.php?b=00010000000000000000000000',indexer)
                self.AddSection(list, indexer,'comedy','Comedy',self.base_url +'genre.php?b=00001000000000000000000000',indexer)
                self.AddSection(list, indexer,'crime','Crime',self.base_url +'genre.php?b=00000100000000000000000000',indexer)
                self.AddSection(list, indexer,'documentary','Documentary',self.base_url +'genre.php?b=00000010000000000000000000',indexer)
                self.AddSection(list, indexer,'drama','Drama',self.base_url +'genre.php?b=00000001000000000000000000',indexer)
                self.AddSection(list, indexer,'family','Family',self.base_url +'genre.php?b=00000000100000000000000000',indexer)
                self.AddSection(list, indexer,'fantasy','Fantasy',self.base_url +'genre.php?b=00000000010000000000000000',indexer)
                self.AddSection(list, indexer,'filmnoir','Film noir',self.base_url +'genre.php?b=00000000001000000000000000',indexer)
                self.AddSection(list, indexer,'gameshow','Gameshow',self.base_url +'genre.php?b=00000000000100000000000000',indexer)            
                self.AddSection(list, indexer,'history','History',self.base_url +'genre.php?b=00000000000010000000000000',indexer)
                self.AddSection(list, indexer,'horror','Horror',self.base_url +'genre.php?b=00000000000001000000000000',indexer)
                self.AddSection(list, indexer,'music','Music',self.base_url +'genre.php?b=00000000000000100000000000',indexer)
                self.AddSection(list, indexer,'musical','Musical',self.base_url +'genre.php?b=00000000000000010000000000',indexer)
                self.AddSection(list, indexer,'mystery','Mystery',self.base_url +'genre.php?b=00000000000000001000000000',indexer)
                self.AddSection(list, indexer,'news','News',self.base_url +'genre.php?b=00000000000000000100000000',indexer)
                self.AddSection(list, indexer,'realitytv','Reality tv',self.base_url +'genre.php?b=00000000000000000010000000',indexer)            
                self.AddSection(list, indexer,'romance','Romance',self.base_url +'genre.php?b=00000000000000000001000000',indexer)
                self.AddSection(list, indexer,'sci-fi','Sci-Fi',self.base_url +'genre.php?b=00000000000000000000100000',indexer)
                self.AddSection(list, indexer,'sports','Sports',self.base_url +'genre.php?b=00000000000000000000010000',indexer)
                self.AddSection(list, indexer,'talkshow','Talkshow',self.base_url +'genre.php?b=00000000000000000000001000',indexer)
                self.AddSection(list, indexer,'thriller','Thriller',self.base_url +'genre.php?b=00000000000000000000000100',indexer)
                self.AddSection(list, indexer,'war','War',self.base_url +'genre.php?b=00000000000000000000000010',indexer)
                self.AddSection(list, indexer,'western','Western',self.base_url +'genre.php?b=00000000000000000000000001',indexer)
                
                

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

        elif indexer == common.indxr_TV_Shows:
            if section == 'main':
                self.AddSection(list, indexer,'tvshows','[COLOR royalblue]TV-Shows[/COLOR] List',self.base_url +'series.php',indexer)
                self.AddSection(list, indexer,'tvshowsadded','[COLOR royalblue]Most Recently[/COLOR] Updated','http://superchillin.com/series.php?bl=1',indexer)
                self.AddSection(list, indexer,'tvshowsadded','[COLOR royalblue]Series List[/COLOR] Alphabetically','http://superchillin.com/series.php?dl=1',indexer)

            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
            
    
    def GetFileHosts(self, url, list, lock, message_queue):
        get_1080p = False;
        if url.endswith('__movies'):
            url = url.split('__')[0];
            get_1080p = True
        import re
        from entertainment.net import Net
        net = Net(cached=False)
        net.set_cookies(self.cookie_file)
        content = net.http_GET(url).content
        
        fileid = re.compile('"file": "(.+?)"').findall(content)[0]
        resolved_url = net.http_GET('http://superchillin.com'+fileid, headers={'Rrferer':url}, auto_read_response=False).get_url()
        
        if self.Settings().get_setting('premium')=='true':                
            self.AddFileHost(list, 'HD', resolved_url, 'SUPERCHILLIN.COM')
            if 'Watch in 1080p' in content:
                self.AddFileHost(list, 'HD', resolved_url+'&hd=1', 'SUPERCHILLIN.COM 1080P')
        else:
            self.AddFileHost(list, 'HD', resolved_url, 'SUPERCHILLIN.COM')
        
        
        
                
    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):                 
        
        #if type!= 'movies': return

        from entertainment.net import Net
        import re
        net = Net(cached=False)

        tv_user = self.Settings().get_setting('tv_user')
        tv_pwd = self.Settings().get_setting('tv_pwd')


        if tv_user == 'Enter your Superchillin email' or tv_pwd == 'xunity' or tv_user == '' or tv_pwd == '':
            if os.path.exists(self.cookie_file):
                try: os.remove(self.cookie_file)
                except: pass

            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                          '[COLOR red]Please Enter Login & Password in Settings[/COLOR]',
                                          7000, self.icon)
            return
            

        if os.path.exists(self.cookie_file):
                try: os.remove(self.cookie_file)
                except: pass
                
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                   'Host': 'superchillin.com', 'Origin': 'http://superchillin.com',
                   'Referer': 'http://superchillin.com/login.php',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36'}


        net.http_GET('http://superchillin.com/login.php')
        net.http_POST('http://superchillin.com/login2.php', {'email': str(tv_user), 'password': str(tv_pwd)}, headers, auto_read_response=False).content
        net.save_cookies(self.cookie_file)
        net.set_cookies(self.cookie_file)
                       
        name = self.CleanTextForSearch(name)
        name = name.rstrip()
        #
        import urllib        
        movie_url='http://superchillin.com/search.php?q=%s' %(name.replace(' ','+'))
        
        html = net.http_GET(movie_url).content
        if not re.search(r'\"logout.php\"\>Logout\<\/a\>', html, re.I):
            common.addon.show_small_popup('[B][COLOR blue]I[/B][/COLOR]stream: Superchillin',
                                          '[COLOR red]Please Check Login & Password Are Correct[/COLOR]',
                                          7000, self.icon)
        if type == 'movies':
            name_lower = common.CreateIdFromString(name)        
            for item in re.finditer(r"href='/(.+?)'>(.+?)</a> \((.+?)\)", html):
                item_url = self.base_url + item.group(1)
                item_name = common.CreateIdFromString(item.group(2))
                item_year = item.group(3)
                #item_url = item_url+'&hd=1'
            
                if item_name == name_lower and item_year == year:
                    self.GetFileHosts(item_url + '__movies', list, lock, message_queue)
                    

        elif type == 'tv_episodes':
            name_lower = common.CreateIdFromString(name)        
            for item in re.finditer(r"<i>TV Series</i></b><br><br>.+? href='/(.+?)'>(.+?)</a>", html):
                item_url = self.base_url + item.group(1)
                item_name = common.CreateIdFromString(item.group(2))
                html = net.http_GET(item_url).content
                #<b>(.+?)x(.+?) - <a style='text.+? href='/(.+?)'>(.+?)</a></b>
                #<b>(.+?)x(.+?) .+? href='/(.+?)'>(.+?)</a>
                season_pull = "0%s"%season if len(season)<2 else season
                episode_pull = "0%s"%episode if len(episode)<2 else episode
                for item in re.finditer(r"<b>"+season+"x"+episode_pull+" - <a style='text.+? href='/(.+?)'>(.+?)</a></b>", html):
                    item_url2 = self.base_url + item.group(1)
                    item_title = item.group(2)
                    
                
                    if item_name == name_lower:
                        self.GetFileHosts(item_url2, list, lock, message_queue)
                        
            
    #def Resolve(self, url):
        #import re
        #from entertainment.net import Net
        #net = Net(cached=False)
        #net.set_cookies(self.cookie_file)
        #content = net.http_GET(url).content
        #fileid = re.compile('"file": "(.+?)"').findall(content)[0]
        
        #resolved_url = net.http_GET('http://noobroom5.com'+fileid, headers={'Rrferer':url}, auto_read_response=False).get_url()
        #return resolved_url
         

    
