'''
    Istream
    trakt by Coolwave
    Copyright (C) 2013 

    version 0.1

'''


from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.xgoogle.search import GoogleSearch

import re

import os

class trakt(MovieIndexer,TVShowIndexer, ListIndexer, CustomSettings):
    implements = [MovieIndexer,TVShowIndexer, ListIndexer,CustomSettings]

    name = "trakt"
    default_indexer_enabled = 'false'
    display_name = "Trakt"
    img='https://raw.githubusercontent.com/Coolwavexunitytalk/images/master/trakt.png'
    
    #base url of the source website
    base_url = 'https://trakt.tv'
    
    cookie_file = os.path.join(common.profile_path, 'cookies', '%s.cookies') % name

    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="username" type="text" label="Username" default="" />\n'
        xml += '<setting id="password" type="text" label="Password" default="" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)    
    
    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        from entertainment.net import Net
        net = Net(cached=False)
        
        trakt_user = self.Settings().get_setting('username')
        trakt_password = self.Settings().get_setting('password')
        if trakt_user!="" and trakt_password != "" and section != 'search':
            net.set_cookies(self.cookie_file)     
        
        import re

        new_url = url

        if section  != 'list' or total_pages != '':        
            if page == '':
                page = '1'
            else:
                page = str( int(page) )
            
            new_url = new_url + ('&' if section=='search' else '?') + 'page=' + page               
            
            if total_pages == '':
                total_pages = '500'
                if section == 'boxoffice':
                    total_pages = '1'
                elif section == 'search':
                    total_pages = '5'
                
            self.AddInfo(list, indexer, section, url, type, str(page), total_pages)        
            
        html = net.http_GET(new_url).content
        
        if section == 'list' and page == '' and total_pages == '':
            pagination_match = re.search('<ul class="pagination">(.+?)</ul>', html, re.DOTALL)
            if pagination_match:
                if page == '':
                    page ='1'
                pagination = pagination_match.group(1)
                page_match = re.compile('<a href=[^>]+?>([^<]+?)<').findall(pagination)
                if page_match:
                    total_pages = page_match[-1].strip()                    
                    self.AddInfo(list, indexer, section, url, type, str(page), total_pages)   
                
                       
        match = re.compile('(<div class="grid-item col.+?<div class="titles[^>]+?>.+?</div>.+?</div>)', re.DOTALL).findall(html)
        for item in match:
            url_match = re.search('<a href="([^"]+?)">', item)
            if url_match:
                url = self.base_url + url_match.group(1)
                item_indexer = ''
                mode = ''
                name = ''
                year = ''
                season = ''
                episode = ''        
                item_id = ''
                displayname = ''
                if '/shows/' in url:
                    if indexer == common.indxr_Movies and section == 'list':
                        continue
                    item_indexer = common.indxr_TV_Shows
                    mode = common.mode_Content
                    type = 'tv_seasons'
                    if section == 'list':
                        name_match = re.search('<h3>(.+?)</h3>', item)
                    else:
                        name_match = re.search('<meta content="([^"]+?)" itemprop="name">', item)
                        year_match = re.search('<span class="year">(.+?)</span>', item)
                        if year_match:
                            year = year_match.group(1)
                    
                    if name_match:
                        name = name_match.group(1)
                        displayname = name
                        if year:
                            displayname = displayname + ' (' + year + ')'
                        
                    if '/seasons/' in url:                            
                        type = 'tv_episodes'
                        name_span = re.search('itemprop="partOfSeries"(.+?)</span>', item, re.DOTALL).group(1)
                        name = re.search('<meta content="([^"]+?)" itemprop="name">', name_span).group(1)
                        season = re.search('/seasons/([0-9]+)', url).group(1)
                        displayname = name + ' - Season: ' + season
                        
                    if 'episodes/' in url:
                        mode = common.mode_File_Hosts
                        type = 'tv_episode'
                        episode = re.search('/episodes/([0-9]+)', url).group(1)
                        item_id = common.CreateIdFromString(name + '_' + year + '_season_' + season + '_episode_' + episode)
                        episode_name = ''
                        episode_name_match = re.compile('<meta content="([^"]+?)" itemprop="name">').findall(item)
                        if episode_name_match:
                            episode_name = episode_name_match[-1].strip()
                        displayname = name + ' - S' + season + 'E' + episode + ' - ' + episode_name
                        item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + episode)
                        
                else:
                    if indexer == common.indxr_TV_Shows and section == 'list':
                        continue
                    item_indexer = common.indxr_Movies
                    mode = common.mode_File_Hosts
                    type = common.indxr_Movies
                    if section == 'list':
                        name = re.search('<h3>(.+?)</h3>', item).group(1)
                    else:
                        name = re.search('<meta content="([^"]+?)" itemprop="name">', item).group(1)
                    displayname = name
                    year_match = re.search('\-([0-9]{4})$', url)
                    if year_match:
                        year = year_match.group(1)
                        displayname += ' (' + year + ')'

                self.AddContent(list, item_indexer, mode, displayname, item_id, type, url=url, name=name, year=year, season=season, episode=episode)                           

       
    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        
        from entertainment.net import Net
        net = Net(cached=False)
        import re
                    
        import datetime
        todays_date = datetime.date.today()
        content = net.http_GET(url).content
        
        if type == 'tv_seasons':
            match=re.compile('<a class="titles-link" href="(.+?)"><div class="titles"><h3>Season (.+?)</h3>').findall(content)
            for url,seasonnumber in match:                
                item_url = self.base_url + url
                item_title = 'Season ' + seasonnumber
                item_id = common.CreateIdFromString(title + ' ' + item_title)               
                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, season=seasonnumber)

        elif type == 'tv_episodes':
            new_url = url
            content2 = net.http_GET(new_url).content
            match=re.compile('div class="titles"><h4(.+?)</h3><ul class="additional-stats">').findall(content2)
            
            for item in match:

                item_url = self.base_url + re.search('<a href="([^"]+?)">', item).group(1)
                item_v_id_2 = re.search('<meta content="([^"]+?)" itemprop="episodeNumber">', item).group(1)
                item_title = re.search('<meta content="([^"]+?)" itemprop="name">', item).group(1)
                item_date = re.search('<meta content="([0-9\-]+?)T[^"]+?" itemprop="datePublished">', item).group(1)
                item_fmtd_air_date = self.get_formated_date( item_date, "%Y-%m-%d" )
                if item_fmtd_air_date.date() > todays_date: break
                
                item_id = common.CreateIdFromString(name + '_season_' + season + '_episode_' + item_v_id_2)
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, season=season, episode=item_v_id_2)
                   
    def get_formated_date(self, date_str, fmt=""):
        
        import re
        import datetime

        if not fmt:
            if '00' in date_str:
                date_str = '01/Aug/2000'
            #date_str = date_str.replace('00/([0-9]{2})/([0-9]{4})','01/Aug/2000')
            date_str = date_str.replace('00/00/0000','01/Aug/2000')
            #date_str = re.sub(pattern, replace, date_str)
            
                    
            item_air_date = common.unescape(date_str).replace('      ', '')
            item_fmtd_air_date = ""
            if 'Jan' in item_air_date: item_fmtd_air_date = '01-'
            elif 'Feb' in item_air_date: item_fmtd_air_date = '02-'
            elif 'Mar' in item_air_date: item_fmtd_air_date = '03-'
            elif 'Apr' in item_air_date: item_fmtd_air_date = '04-'
            elif 'May' in item_air_date: item_fmtd_air_date = '05-'
            elif 'Jun' in item_air_date: item_fmtd_air_date = '06-'
            elif 'Jul' in item_air_date: item_fmtd_air_date = '07-'
            elif 'Aug' in item_air_date: item_fmtd_air_date = '08-'
            elif 'Sep' in item_air_date: item_fmtd_air_date = '09-'
            elif 'Oct' in item_air_date: item_fmtd_air_date = '10-'
            elif 'Nov' in item_air_date: item_fmtd_air_date = '11-'
            elif 'Dec' in item_air_date: item_fmtd_air_date = '12-'
            else: item_fmtd_air_date = '12-'
            date = re.search('([0-9]{1,2})', item_air_date)
            if date: 
                date = date.group(1)
                item_fmtd_air_date += "%02d-" % int(date)
            else:
                item_fmtd_air_date += "01-"
            year = re.search('([0-9]{4})', item_air_date)
            if year: 
                year = year.group(1)
                item_fmtd_air_date += year
            else:
                item_fmtd_air_date += "0001"
                
            fmt = "%m-%d-%Y"
        else:
            item_fmtd_air_date = date_str
            
        try:
            item_fmtd_air_date = datetime.datetime.strptime(item_fmtd_air_date, fmt)
        except TypeError:
            import time
            item_fmtd_air_date = datetime.datetime(*(time.strptime(item_fmtd_air_date, fmt)[0:6]))
        except ValueError:
            item_fmtd_air_date = "08-01-2000"
            try:
                item_fmtd_air_date = datetime.datetime.strptime(item_fmtd_air_date, fmt)
            except TypeError:
                import time
                item_fmtd_air_date = datetime.datetime(*(time.strptime(item_fmtd_air_date, fmt)[0:6]))
            
        return item_fmtd_air_date
            
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        
        self.Login()
                
        url_type = ''
        content_type = ''
        
        trakt_user = self.Settings().get_setting('username')        
        trakt_password = self.Settings().get_setting('password')
        
        if (indexer == common.indxr_Movies or indexer == common.indxr_TV_Shows) and section != 'mytrakt' and 'list' not in section:
            
            if indexer == common.indxr_Movies:
                url_type = 'movies'
            else:
                url_type = 'shows'
            
            if section == 'main':
                self.AddSection(list, indexer,'mytrakt','My Trakt',self.base_url,indexer)
                self.AddSection(list, indexer,'trending','Trending',self.base_url + '/' + url_type + '/trending',indexer)
                
                if indexer == common.indxr_Movies:
                    self.AddSection(list, indexer,'boxoffice','Box Office',self.base_url + '/' + url_type + '/boxoffice',indexer)
                    
                self.AddSection(list, indexer,'popular','Popular',self.base_url + '/' + url_type + '/popular',indexer)
                self.AddSection(list, indexer,'watched','Watched',self.base_url + '/' + url_type + '/watched/weekly',indexer)
                self.AddSection(list, indexer,'played','Played',self.base_url + '/' + url_type + '/played/weekly',indexer)
                self.AddSection(list, indexer,'collected','Collected',self.base_url + '/' + url_type + '/collected/weekly',indexer)
                self.AddSection(list, indexer,'anticipated','Anticipated',self.base_url + '/' + url_type + '/anticipated',indexer)                                                
                
            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)       
            
        else:
            if section == 'main' or section == 'mytrakt':
                if trakt_user != "":                    
                    
                    if indexer == common.indxr_Movies:
                        url_type = '/movies'
                    elif indexer == common.indxr_TV_Shows:
                        url_type = '/shows'
                    else:
                        url_type = ''
                    
                    self.AddSection(list, indexer,'list','History',self.base_url + '/users/'+trakt_user+'/history' + url_type ,indexer)
                    #self.AddSection(list, indexer,'list','Progress',self.base_url + '/users/'+trakt_user+'/progress',indexer)
                    self.AddSection(list, indexer,'list','Collection',self.base_url + '/users/'+trakt_user+'/collection' + url_type,indexer)
                    self.AddSection(list, indexer,'list','Ratings',self.base_url + '/users/'+trakt_user+'/ratings' + url_type,indexer)
                    self.AddSection(list, indexer,'lists','Lists',self.base_url + '/users/'+trakt_user+'/lists',indexer)
                
            elif section == 'lists':
                from entertainment.net import Net        
                net = Net(cached=False)
                if trakt_user!="" and trakt_password != "":
                    net.set_cookies(self.cookie_file)     
                import re
                match = re.compile(r'<div class="user-name"><a href="(.+?)"><h3 itemprop="name">(.+?)</h3></a>').findall( net.http_GET(url).content)
                for list_url, list_title in match:
                    list_url=self.base_url+list_url                    
                    self.AddSection(list, indexer, 'list', list_title, list_url, indexer)
                    
            else:
                self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
    
    def Login(self):
        trakt_user = self.Settings().get_setting('username')
        trakt_password = self.Settings().get_setting('password')
        if trakt_user=="" or trakt_password == "":
            return

        from entertainment.net import Net        
        net = Net(cached=False)            
        
        signin_page = net.http_GET(self.base_url + '/auth/signin').content
        
        import re
        signin_form = re.search('<form class="simple_form form-signin"[^>]+?>(.+?)</form>', signin_page)
        if signin_form:
            signin_form = signin_form.group(1)
            signin_params = {}
            inputs = re.compile('(<input[^>]+?>)').findall(signin_form)
            for input in inputs:
                if 'type="hidden"' in input:
                    name = re.search('name="([^"]+?)"', input).group(1)
                    value = re.search('value="([^"]+?)"', input).group(1)
                    
                    signin_params[name] = value
            
            signin_params['user[login]'] = trakt_user
            signin_params['user[password]'] = trakt_password
            
            net.http_POST(self.base_url + '/auth/signin', signin_params).content
            
            net.save_cookies(self.cookie_file)
        
    
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        from entertainment.net import Net
        net = Net(cached=False)
        
        keywords = self.CleanTextForSearch(keywords) 
        
        url_type = 'movies' if type == 'movies' else 'shows'
        
        search_page_url = self.base_url + '/search/' + url_type + '?query=' + keywords
        
        self.ExtractContentAndAddtoList(srcr, 'search', search_page_url, type, list, page=page, total_pages=total_pages)
        
        
