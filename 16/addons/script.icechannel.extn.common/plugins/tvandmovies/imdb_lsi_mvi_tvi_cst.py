'''
    IMDb
'''

from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay import Plugin
from entertainment import common

class IMDb(MovieIndexer, TVShowIndexer, CustomSettings, ListIndexer):
    implements = [MovieIndexer, TVShowIndexer, CustomSettings, ListIndexer]

    name = "IMDb"
    display_name = "IMDb"
    
    
    img = common.get_themed_icon('imdb.png')
    fanart = common.get_themed_fanart('imdb.jpg')
    
    default_indexer_enabled = 'true'
    
    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="IMDb SETTINGS">\n'
        xml += '<setting id="en_us" type="bool" label="Show English Language Only" default="true" />\n'        
        xml += '<setting id="get_url()" label="Base Url" type="labelenum" default="http://www.imdb.com/" values="http://www.imdb.com/|http://akas.imdb.com/" />\n'
        xml += '<setting id="imdb_user_number" label="User Number" type="text" default="" />\n'
        xml += '<setting id="future" type="bool" label="Show Future Episodes" default="false" />\n'
        xml += '<setting id="watch_list_main" type="bool" label="Show Main Watchlist" default="true" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        
        self.CreateSettings(self.name, self.display_name, xml)


    def get_url(self):
        url = self.Settings().get_setting('get_url()')
        if '//imdb' in url:
            url=url.replace('//','//www.')
        return url
    
    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        
        import urllib

            
       
        if section != 'search':
            url = urllib.unquote_plus(url)
            
            
            
        if section == 'search_celeb':
            import xbmc
            search_entered = ''
            keyboard = xbmc.Keyboard(search_entered, '[COLOR blue]i[/COLOR]Stream')
            keyboard.doModal()
            if keyboard.isConfirmed():
                search_entered = keyboard.getText()
            if search_entered=='':return    
            url = urllib.unquote_plus(url)+search_entered.replace(' ','+')
            
        
        import re
        
        new_url = url
        
         
        if not new_url.startswith(self.get_url()):
            new_url = re.sub("http\://.*?/", self.get_url(), url)

        if page == '':
            page = '1'

        #change page length to 100.
        page_item_count = (100 if section == 'watchlist' else 50)

        start = str( ( (int(page) - 1) * page_item_count ) + 1 )
        count = str(page_item_count)
        if section != 'watchlist_people':
            if not '?' in new_url:
                new_url = new_url + '?start=' + start + '&count=' + count
            else:
                new_url = new_url + '&start=' + start + '&count=' + count    

        if sort_by == '' and 'sort' not in new_url:
            sort_by = 'moviemeter'
        if sort_order == '' and 'sort' not in new_url:
            sort_order = 'asc'
        
        if 'sort' not in new_url:
            new_url = new_url + '&sort=' + ('title' if section == 'watchlist' and sort_by == 'alpha' else sort_by) + (':' if section == 'watchlist' else ',') + sort_order

            #print 'new_url ' + new_url

        if sort_by == '' and 'sort=user_rating,desc' in new_url:
            sort_by = 'user_rating'
            sort_order = 'desc'
            url = url.replace("sort=user_rating,desc", "")
        elif sort_by == '' and 'sort=num_votes,desc' in new_url:
            sort_by = 'num_votes'
            sort_order = 'desc'
            url = url.replace("sort=num_votes,desc", "")
        elif sort_by == '' and 'sort=boxoffice_gross_us,desc' in new_url:
            sort_by = 'boxoffice_gross_us'
            sort_order = 'desc'
            url = url.replace("sort=boxoffice_gross_us,desc", "")
        elif sort_by == '' and 'sort=release_date_us,desc' in new_url:
            sort_by = 'release_date_us'
            sort_order = 'desc'
            url = url.replace("sort=release_date_us,desc", "")
        elif sort_by == '' and 'sort=year,desc' in new_url:
            sort_by = 'year'
            sort_order = 'desc'
            url = url.replace("sort=year,desc", "")

        from entertainment.net import Net
        cached = False if section == 'watchlist' else True
        net = Net(cached=cached)
        
        if self.Settings().get_setting('en_us')=='true':
            
            content = net.http_GET(new_url,{'Accept-Language':'en-US'}).content
        else:
            content = net.http_GET(new_url).content
            
        if total_pages == '':

            #page problem watchlist solved.
            #re_page =  '<span>\(.+? of ([0-9,]+)' if section == 'watchlist' else '(?s)<div id="left">.+? of ([0-9,]+)'
            if section == 'watchlist':
                if not 'watchlist?' in new_url:
                    re_page = '<span>\(.+? of ([0-9,]+)'
                else:
                    re_page = 'of ([0-9,]+) titles'

            else:
                re_page = 'of ([0-9,]+) titles'

            total_pages = re.search(re_page, content)
            if total_pages:
                total_count = total_pages.group(1)
                total_count = int ( total_count.replace(',', '') )
                total_pages = str( total_count / page_item_count + ( 1 if total_count % page_item_count > 0 else 0 ) )
            else:
                if re.search('0 items found', content):
                    page = '0'
                    total_pages = '0'
                else:
                    page = '1'
                    total_pages = '1'

        self.AddInfo(list, indexer, section, url, type, page, total_pages, sort_by, sort_order)

        
        if section == 'search_celeb':
            
            match=re.compile('<img src="(.+?)" /></a> </td> <td class="result_text"> <a href="(.+?)" >(.+?)<.+?<small>\((.+?),').findall(content)
            for img,url , name , gender in match:
                img=img.split(',')[0]
                if 'Actress' in gender or 'Actor' in gender:
                    self.AddSection(list, indexer, 'celeb_result', name+' (%s)'%gender, self.get_url()+url, indexer,img=img.replace('SX32','SX280'))


        if section == 'watchlist_people':
            
            match=re.compile('<a href="/(.+?)"><img src="(.+?)".+?alt="(.+?)">').findall(content)

            for url ,img, name in match:
                img=img.split(',')[0]
                self.AddSection(list, indexer, 'celeb_result', name, self.get_url()+url, indexer,img=img.replace('SX140','SX280'))

                    
                    
        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'
        
        item_re = r'<a href="/title/(.+?)/.+?"\n> <img alt="(.+?)"'
        if section == 'theaters':
            item_re = r'<h4 itemprop="name"><a href="/title/(.+?)/.+?title="(.+?)"'

        if section == 'watchlist':

            if not 'watchlist?' in new_url:
                item_re = r'(?s)<b><a.+?href="/title/(.+?)/".+?>(.+?)</a>.+?<span class="year_type">(.+?)<.+?<div class="(.+?)"'
            else:
                item_re= r'\{"href":"/title/([^"]+?)","year":\["(.+?)"\],"title":"([^"]+?)"\}'
                
                
        if section=='celeb_result':
            
            match=re.compile('<div class="filmo-row .+?" id=".+?">.+?span class="year_column">.+?nbsp;(.+?)</span>.+?<b><a href="/title/(.+?)/.+?>(.+?)</a>(.+?)<br/>',re.DOTALL).findall(content)
            for year , tt , title, id_type in match:

                if 'TV Series' in id_type:
                    type = 'tv_seasons'
                    mode = common.mode_Content
                    indexer = common.indxr_TV_Shows

                else:
                    type = common.indxr_Movies 
                    mode = common.mode_File_Hosts
                    indexer = common.indxr_Movies
                item_title = common.addon.unescape(title)
                item_url = self.get_url()+'title/'+tt+'/'
                year=year.strip()
                if '-' in year:
                    year=year.split('-')[0]
    
                self.AddContent(list, indexer, mode, item_title.strip(), '', type, url=item_url, name=item_title.strip(), year=year, imdb_id=tt)
        else:   
            for item in re.finditer(item_re, content):


                item_v_id = item.group(1)
                item_title = common.addon.unescape( item.group(3) if section == 'watchlist' and 'watchlist?' in new_url else item.group(2))

                item_type = item_title
                if section =='watchlist':
                    if not 'watchlist?' in new_url:
                        item_type = item.group(3)
                    else:
                        if '",' in item.group(2):
                            item_type = "(" + item.group(2).split('",')[0]+' ' + ")"
                        else:
                            item_type = "(" + item.group(2) + ")"
                
                item_type =item_type.replace(' Video)',')').replace(' Short Film)','')
                item_year = re.search("\(([0-9]+)", item_type)
                
                if item_year:
                    item_year = item_year.group(1)
                else:
                    r='>%s</a>\n    <span class=".+?">\((.+?)\)<'%item_title.replace('?','\?')
                    item_year=re.search(r, content)
                    item_year = re.search("([0-9]+)", item_year.group(1))
                    if item_year:
                        item_year = item_year.group(1)
                    else:
                        item_year=''
                    

                item_name = item_title if section == 'watchlist' else re.sub(" \([0-9]+.+?\)", "", item_title )
                
                item_title = item_name.strip()
                if item_year != '':
                    item_title = item_title + ' (' + item_year.replace('-','') + ')'
                
                item_url = self.get_url()+'title/'+item_v_id+'/'
               
                if total_pages == '':
                    total_pages = '1'
                
                if section == 'watchlist':                
                    if 'movie' in item_type.lower() or re.sub("[0-9]+", "", item_type) == "()":
                        type = common.indxr_Movies 
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies                     
                    elif 'series' in item_type.lower() or ' ' in item_type:
                        type = 'tv_seasons'
                        mode = common.mode_Content
                        indexer = common.indxr_TV_Shows 
                    else:
                        type = common.indxr_Movies 
                        mode = common.mode_File_Hosts
                        indexer = common.indxr_Movies
                
                self.AddContent(list, indexer, mode, item_title.strip(), '', type, url=item_url, name=item_name.strip(), year=item_year, imdb_id=item_v_id)
            
    def get_formated_date(self, date_str):
        
        import re
        import datetime
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
        date=item_air_date.split('.')[0]

        date = re.search('([0-9]{1,2})', date)

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
            
        try:
            item_fmtd_air_date = datetime.datetime.strptime(item_fmtd_air_date, "%m-%d-%Y")
        except TypeError:
            import time
            item_fmtd_air_date = datetime.datetime(*(time.strptime(item_fmtd_air_date, "%m-%d-%Y")[0:6]))
 
        return item_fmtd_air_date

    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        import urllib
        url = urllib.unquote_plus(url)
        title = urllib.unquote_plus(title)
        name = urllib.unquote_plus(name)
        
        import re
        
        new_url = url
        if not new_url.startswith(self.get_url()):
            new_url = re.sub("http\://.*?/", self.get_url(), url)
        
        from entertainment.net import Net
        net = Net(cached=False)
        print new_url
        print '########################################'
        content = net.http_GET(new_url).content
        
        import datetime
        todays_date = datetime.date.today()
        
        if type == 'tv_seasons':
            check_season = 0
            last_season = 0
            season_url = None
            seasons = re.search('<a href="/(title/.+?/episodes\?season=)([0-9]+)', content)
            if seasons:
                last_season = int(seasons.group(2))
                season_url = seasons.group(1)
            
            for season_num in xrange(last_season, 0, -1):
                item_v_id = str(season_num)
                item_url = self.get_url() + season_url + item_v_id
                
                if check_season < 2:
                    check_season += 1
                    item_content = net.http_GET(item_url).content
                    season_item = re.search('<div>S' + item_v_id +', Ep([0-9]+)</div>', item_content)
                    if not season_item: 
                        check_season -= 1
                        continue          
                    item_item = re.search('(?s)<div class="list_item.+?href="(.+?)".+?title="(.+?)".+?<div>S' + item_v_id +', Ep([0-9]+)</div>.+?<div class="airdate">(.+?)</div>', item_content)
                    if 'unknown' in item_item.group(4).lower(): continue 
                    item_fmtd_air_date = self.get_formated_date( item_item.group(4) )

                    if item_fmtd_air_date.date() > todays_date or item_fmtd_air_date.date() == '0001-12-01': continue
                
                
                item_title = 'Season ' + item_v_id
                
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                
                self.AddContent(list, indexer, common.mode_Content, item_title.strip(), item_id, 'tv_episodes', url=item_url, name=name.strip(), year=year, season=item_v_id)
            
            
        elif type == 'tv_episodes':
            season_item = re.search('<div>S' + season +', Ep([0-9]+)</div>', content)
            if not season_item: 
                return

            for item in re.finditer('(?s)<div class="list_item.+?href="(.+?)".+?title="(.+?)".+?<div>S' + season +', Ep([0-9]+)</div>.+?<div class="airdate">(.+?)</div>', content):
                item_fmtd_air_date = self.get_formated_date( item.group(4) )

                if self.Settings().get_setting('future')=='false':
                    if item_fmtd_air_date.date() > todays_date: break
                
                item_url = self.get_url() + item.group(1)
                item_v_id = item.group(3)
                item_title = item.group(2).strip()
                if item_title == None:
                    item_title = ''
                
                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + season + '_episode_' + item_v_id)
                
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title.strip(), item_id, type, url=item_url, name=name.strip(), year=year, season=season, episode=item_v_id)
        
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        url_type = ''
        #added filters
        url_filter = ''
        url_filter_less = ''
        url_filter_rated = ''
        url_filter_small = ''

        if indexer == common.indxr_Movies:
            url_type = 'title_type=feature,tv_movie&'

            #added filters movies.
            #request: add some of the values as user settings variables.
            #moviemeter_default_movies = 50000
            #num_votes_default_movies = 3000
            #num_votes_small_collection_movies = 200
            #num_votes_rated_movies = 25000

            url_filter = 'has=technical&moviemeter=,50000&num_votes=3000,&production_status=released&'
            url_filter_less = 'has=technical&moviemeter=,200000&num_votes=1000,&production_status=released&'
            url_filter_small = 'has=technical&moviemeter=,200000&num_votes=200,&production_status=released&'
            url_filter_rated = 'has=technical&moviemeter=,50000&num_votes=25000,&production_status=released&'

        elif indexer == common.indxr_TV_Shows:
            url_type = 'title_type=tv_series,mini_series&'

            #num_votes_default_tv_shows = 1500
            #num_votes_small_collection_tv_shows = 200
            #num_votes_rated_tv_shows = 25000

            #added filters tv shows.
            url_filter = 'has=technical&moviemeter=,50000&num_votes=1500,&'
            url_filter_less = 'has=technical&moviemeter=,200000&num_votes=500,&'
            url_filter_small = 'has=technical&moviemeter=,200000&num_votes=200,&'
            url_filter_rated = 'has=technical&moviemeter=,50000&num_votes=25000,&'

        elif indexer == common.indxr_Lists:
            url_type = ''#title_type=feature,tv_movie,tv_series,mini_series&'

        if section == 'main':
            user_number = self.Settings().get_setting('imdb_user_number')
            
            if user_number:
                list_url_type = ''#title_type=feature,tv_movie,tv_series,mini_series&'
                if self.Settings().get_setting('watch_list_main')=='true':
                    self.AddSection(list, indexer, 'watchlist', 'Watchlist', self.get_url()+'user/' + user_number + '/watchlist?' + list_url_type + 'view=detail', indexer)

                from entertainment.net import Net
                net = Net(cached=False)
                import re

                named_lists_url = self.get_url()+'user/' + user_number + '/lists?tab=public'
                named_lists = net.http_GET(named_lists_url).content
               
                match = re.compile('<div class="list_name"><b><a.+?href="(.+?)".+?>(.+?)</a>.+?\n.+?div class="list_meta">(.+?)</div>').findall(named_lists)
                for url, name ,TYPE in match:
                    custom_name='%s List' % name   
                    url=str(url).replace('/list','list')
                    if 'people' in TYPE:
                        custom_url=self.get_url() + str(url)  +'?view=grid&sort=listorian:asc'             
                        self.AddSection(list, indexer, 'watchlist_people', '%s' % custom_name, custom_url, indexer, hlevel=1)
                    else:
                        custom_url=self.get_url() + str(url) + '?' + list_url_type + 'view=detail'
                        self.AddSection(list, indexer, 'watchlist', '%s' % custom_name, custom_url, indexer, hlevel=1) 
                            
            #seperated movies and tv shows.
            #added filters to commands for movies.
            if indexer == common.indxr_Movies:
                #self.AddSection(list, indexer, 'a_z', 'A-Z')
                
                self.AddSection(list, indexer, 'moviemeter', 'Most Popular', self.get_url()+'search/title?' + url_filter + url_type, indexer, img=common.get_themed_icon('imdb_pop.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'genres', 'Genres', img=common.get_themed_icon('imdb_genres.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'boxoffice_gross_us', 'Box Office', self.get_url()+'search/title?' + url_filter + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_box.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'year', 'Box Office By Year', img=common.get_themed_icon('imdb_year.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'decade', 'Box Office By Decade', img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'user_rating', 'Highly Rated', self.get_url()+'search/title?' + url_filter_rated + url_type + 'sort=user_rating,desc', indexer, img=common.get_themed_icon('imdb_high.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'top_250', 'IMDb Top 250', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=top_250&sort=user_rating,desc', indexer, img=common.get_themed_icon('imdb_250.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'num_votes', 'Most Voted', self.get_url()+'search/title?' + url_filter + url_type + 'sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_vote.png'), fanart=common.get_themed_fanart('imdb.jpg'))

                self.AddSection(list, indexer, 'kids', 'Kids Zone', self.get_url()+'search/title?' + url_filter_small + 'certificates=us:g&genres=family&' + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_kids.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'now-playing-us', 'Now Playing', self.get_url()+'search/title?' + url_filter_less + url_type + 'groups=now-playing-us&sort=release_date_us,desc', indexer, img=common.get_themed_icon('imdb_play.png'), fanart=common.get_themed_fanart('imdb.jpg'))

                #added list of companies and award list
                self.AddSection(list, indexer, 'company', 'Company Lists', img=common.get_themed_icon('imdb_comp.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'award_lists', 'Award Lists', img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'search_celeb', 'Celebrity Search', self.get_url()+'find?q=', indexer, img=common.get_themed_icon('imdb_cel.png'), fanart=common.get_themed_fanart('imdb.jpg'))

            #added filters to commands for tv shows.
            elif indexer == common.indxr_TV_Shows:
                #self.AddSection(list, indexer, 'a_z', 'A-Z')
                self.AddSection(list, indexer, 'moviemeter', 'Most Popular', self.get_url()+'search/title?' + url_filter + url_type, indexer, img=common.get_themed_icon('imdb_pop.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'genres', 'Genres', img=common.get_themed_icon('imdb_genres.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'num_votes', 'Most Voted', self.get_url()+'search/title?' + url_filter + url_type + 'sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_vote.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'year', 'Most Voted By Year', img=common.get_themed_icon('imdb_year.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'decade', 'Most Voted By Decade', img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'user_rating', 'Highly Rated', self.get_url()+'search/title?' + url_filter_rated + url_type + 'sort=user_rating,desc', indexer, img=common.get_themed_icon('imdb_high.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'award_lists', 'Award Lists', img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                self.AddSection(list, indexer, 'search_celeb', 'Celebrity Search', self.get_url()+'find?q=', indexer, img=common.get_themed_icon('imdb_cel.png'), fanart=common.get_themed_fanart('imdb.jpg'))
              
                
        elif section == 'genres':
            
            import re
            
            from entertainment.net import Net
            net = Net()
            
            genre_url = self.get_url()         
            genre_re = ''
            
            genre_url = genre_url + 'genre/'

            #genre different for movies and tv shows.
            if indexer == common.indxr_Movies:
                genre_re = '(?s)<h2>On Amazon Prime Instant Video.+?<table(.+?)</table>'
            elif indexer == common.indxr_TV_Shows:
                genre_re = '(?s)<h2>Television.+?<table(.+?)</table>'

            content = net.http_GET(genre_url).content
            
            genres = re.search(genre_re, content)
            if genres:
                genres = genres.group(1)
                for genre in re.finditer('<a href=".+?">(.+?)</a>', genres):                    
                    genre_title = genre.group(1)
                    genre_section = genre_title.lower()

                    #added filter for movies and tv shows
                    #solved - sign problem in url
                    #request: some of the genres are empty, empty genres shouldn't be visible, by example game-show for movies.
                    genre_section = genre_section.replace("-", "_")

                    if indexer == common.indxr_TV_Shows and genre_section == 'sitcom':
                        genre_section = 'comedy&keywords=sitcom'
                    if indexer == common.indxr_Movies and genre_section == 'documentary':
                        url_type2 = 'title_type=documentary&'
                        genre_url = self.get_url() +'search/title?' + url_filter_less + url_type2 + 'genres=' + genre_section + '&sort=boxoffice_gross_us,desc'
                    elif indexer == common.indxr_Movies:
                        genre_url = self.get_url() +'search/title?' + url_filter_less + url_type + 'genres=' + genre_section + '&sort=boxoffice_gross_us,desc'
                    elif indexer == common.indxr_TV_Shows:
                        genre_url = self.get_url() +'search/title?' + url_filter_less + url_type + 'genres=' + genre_section + '&sort=num_votes,desc'

                    self.AddSection(list, indexer, genre_section, genre_title, genre_url, indexer, img=common.get_themed_icon('genres.png'))

        #not working a-z.
        elif section == 'a_z':
            self.AddSection(list, indexer, '123', '#123', self.get_url()+'?' + url_type + 'letter=123', indexer)
            A2Z=[chr(i) for i in xrange(ord('A'), ord('Z')+1)]
            for letter in A2Z:
                self.AddSection(list, indexer, letter.lower(), letter, self.get_url()+'?' + url_type + 'letter=' + letter.lower(), indexer)                
        elif section == 'year':
            start = 1900
            import datetime
            end   = datetime.datetime.today().year
            year = []
            for yr in range(end, start-1, -1):
                str_year = str(yr)
                #added filter for movies and tv shows
                #changed to one line, removed sort method moviemeter, sort method is default moviemeter, but the user can also sort on rated, alphabet.

                if indexer == common.indxr_Movies:
                    self.AddSection(list, indexer, str_year, str_year, self.get_url()+'search/title?' + url_filter_less + 'year=' + str_year+','+str_year + '&' + url_type + 'sort=boxoffice_gross_us,desc', indexer)
                elif indexer == common.indxr_TV_Shows:
                    self.AddSection(list, indexer, str_year, str_year, self.get_url()+'search/title?' + url_filter_less + 'year=' + str_year+','+str_year + '&' + url_type + 'sort=num_votes,desc', indexer)

        #added decade lists.
        #the sort order can be changed by all of the lists.
        elif section == 'decade':
                if indexer == common.indxr_Movies:
                    self.AddSection(list, indexer, '2010s', '2010-2016', self.get_url()+'search/title?' +'release_date=2010,2016&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '2000s', '2000-2009', self.get_url()+'search/title?' +'release_date=2000,2009&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1990s', '1990-1999', self.get_url()+'search/title?' +'release_date=1990,1999&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1980s', '1980-1989', self.get_url()+'search/title?' +'release_date=1980,1989&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1970s', '1970-1979', self.get_url()+'search/title?' +'release_date=1970,1979&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1960s', '1960-1969', self.get_url()+'search/title?' +'release_date=1960,1969&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1950s', '1950-1959', self.get_url()+'search/title?' +'release_date=1950,1959&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1940s', '1940-1949', self.get_url()+'search/title?' +'release_date=1940,1949&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1930s', '1930-1939', self.get_url()+'search/title?' +'release_date=1930,1939&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1920s', '1920-1929', self.get_url()+'search/title?' +'release_date=1920,1929&' + url_filter_less + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1910s', '1910-1919', self.get_url()+'search/title?' +'release_date=1910,1919&' + url_filter_small + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))

                elif indexer == common.indxr_TV_Shows:
                    self.AddSection(list, indexer, '2010s', '2010-2016', self.get_url()+'search/title?' +'release_date=2010,2016&' + url_filter_less + url_type + 'sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '2000s', '2000-2009', self.get_url()+'search/title?' +'release_date=2000,2009&' + url_filter_less + url_type + 'sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1990s', '1990-1999', self.get_url()+'search/title?' +'release_date=1990,1999&' + url_filter_less + url_type + 'sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1980s', '1980-1989', self.get_url()+'search/title?' +'release_date=1980,1989&' + url_filter_less + url_type + 'sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1970s', '1970-1979', self.get_url()+'search/title?' +'release_date=1970,1979&' + url_filter_less + url_type + 'sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1960s', '1960-1969', self.get_url()+'search/title?' +'release_date=1960,1969&' + url_filter_less + url_type + 'sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, '1950s', '1949-1959', self.get_url()+'search/title?' +'release_date=1949,1959&' + url_filter_less + url_type + 'sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_dec.png'), fanart=common.get_themed_fanart('imdb.jpg'))

        #added companies lists.
        #the sort order can be changed by all of the lists.
        elif section == 'company':
                if indexer == common.indxr_Movies:
                    self.AddSection(list, indexer, 'fox', '20th Century Fox', self.get_url()+'search/title?' + url_filter_small + 'companies=fox&' + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_comp.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'dreamworks', 'DreamWorks', self.get_url()+'search/title?' + url_filter_small + 'companies=dreamworks&' + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_comp.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'mgm', 'MGM', self.get_url()+'search/title?' + url_filter_small + 'companies=mgm&' + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_comp.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'paramount', 'Paramount', self.get_url()+'search/title?' + url_filter_small + 'companies=paramount&' + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_comp.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'columbia', 'Sony', self.get_url()+'search/title?' + url_filter_small + 'companies=columbia&' + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_comp.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'universal', 'Universal', self.get_url()+'search/title?' + url_filter_small + 'companies=universal&' + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_comp.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'disney', 'Walt Disney', self.get_url()+'search/title?' + url_filter_small + 'companies=disney&' + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_comp.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'warner', 'Warner Bros.', self.get_url()+'search/title?' + url_filter_small + 'companies=warner&' + url_type + 'sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_comp.png'), fanart=common.get_themed_fanart('imdb.jpg'))

        #added additional lists.
        #the sort order can be changed by most of the lists.
        #not all lists need filters.
        elif section == 'award_lists':
                if indexer == common.indxr_Movies:
                    #changed name to Best Picture-Winning, so I could add oscar winners list.
                    self.AddSection(list, indexer, 'oscar_best_picture_winners', 'Best Picture-Winning', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=oscar_best_picture_winners&sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'oscar_winners', 'Oscar-Winning', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=oscar_winners&sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'oscar_nominees', 'Oscar-Nominated', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=oscar_nominees&sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'golden_globe_winners', 'Golden Globe-Winning', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=golden_globe_winners&sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'golden_g lobe_nominees', 'Golden Globe-Nominated', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=golden_globe_nominees&sort=boxoffice_gross_us,desc', indexer, img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))

                elif indexer == common.indxr_TV_Shows:
                    self.AddSection(list, indexer, 'emmy_winners', 'Emmy Award-Winning', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=emmy_winners&sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'emmy_nominees', 'Emmy Award-Nominated', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=emmy_nominees&sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'golden_globe_winners', 'Golden Globe-Winning', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=golden_globe_winners&sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))
                    self.AddSection(list, indexer, 'golden_globe_nominees', 'Golden Globe-Nominated', self.get_url()+'search/title?' + url_filter_small + url_type + 'groups=golden_globe_nominees&sort=num_votes,desc', indexer, img=common.get_themed_icon('imdb_awa.png'), fanart=common.get_themed_fanart('imdb.jpg'))

        else:
             self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)

    #request: it would be nice when you select user rating that the sort order would change to descending automatic.
    #sorting alphabet is not working 100%.

    def GetSortByOptions(self): 

        from entertainment import odict
        sort_by_dict = odict.odict()
        
        sort_by_dict['alpha'] = 'Alphabet'
        sort_by_dict['user_rating'] = 'Ratings'
        sort_by_dict['boxoffice_gross_us'] = 'US Box Office'
        sort_by_dict['moviemeter'] = 'Views'
        sort_by_dict['num_votes'] = 'Votes'
        sort_by_dict['year'] = 'Year'
        sort_by_dict['release_date_us'] = 'Release Date US'
        
        return sort_by_dict
    
    def GetSortOrderOptions(self): 
        
        from entertainment import odict
        sort_order_dict = odict.odict()
        
        sort_order_dict['asc'] = 'Ascending'
        sort_order_dict['desc'] = 'Descending'
        
        return sort_order_dict
        
    def Search(self, indexer, keywords, type, list, lock, message_queue, page='', total_pages=''): 

        from entertainment.net import Net
        net = Net() 
        
        keywords = self.CleanTextForSearch(keywords) 
        
        keywords_lower = keywords.lower().split(' ')
        match_total = float( len(keywords_lower) )
        
        from entertainment import odict
        search_dict = odict.odict({ 's' : 'tt', 'q' : keywords})
        
        if indexer == common.indxr_Movies:
            search_dict.update({'ttype':'ft'})
        elif indexer == common.indxr_TV_Shows:
            search_dict.update({'ttype':'tv'})
        
        search_dict.sort(key=lambda x: x[0].lower())
                
        import urllib
        search_for_url = self.get_url() + 'find?' + urllib.urlencode(search_dict)
        
        content = net.http_GET(search_for_url).content        
        
        if '<h1 class="findHeader">No results found' in content:            
            return
            
        self.AddInfo(list, indexer, 'search', self.get_url(), type, '1', '1')
      
        
        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'
        
        import re
        
        search_results = re.search('(?s)<table class="findList">(.+?)</table>', content)
        
        if search_results:            
            search_results = search_results.group(1)
            
            search_term_not_found_count = 0
            for search_item in re.finditer('<td class="result_text"> <a href="/title/(.+?)/.+?" >(.+?)</a> (.+?) </td>', content):
            
                item_id = search_item.group(1)
                item_url = self.get_url() + 'title/' + item_id
                
                item_name = search_item.group(2).strip()
                item_name_lower = item_name.lower().strip()
                
                match_count = 0
                for kw in keywords_lower:
                    if kw in item_name_lower:
                        match_count = match_count + 1

                match_fraction = ( match_count / match_total )

                if not ( match_fraction >= 0.8  ):

                    aka_item = search_item.group(4)

                    aka_name = re.search('aka <i>"(.+?)"</i>', aka_item)
                    if aka_name:
                        item_name = aka_name.group(1)
                        item_name_lower = item_name.lower()
                        match_count = 0
                        for kw in keywords_lower:
                            if kw in item_name_lower:
                                match_count = match_count + 1
                        match_fraction = ( match_count / match_total )
                        if not ( match_fraction >= 0.8  ):
                            search_term_not_found_count += 1
                            if search_term_not_found_count >= 2:
                                break
                            else:
                                continue
                    else:
                        search_term_not_found_count += 1
                        if search_term_not_found_count >= 2:
                            break
                        else:
                            continue
                
                item_title = item_name.strip()
                item_other_info = search_item.group(3)
                item_year = re.search('\(([0-9]+)\)', item_other_info)
                if item_year:
                    item_year = item_year.group(1)
                    item_title += ' (' + item_year + ')'
                else:
                    item_year = ''
        
        
                if 'movie' in item_other_info.lower():
                    type = common.indxr_Movies 
                    mode = common.mode_File_Hosts
                    indexer = common.indxr_Movies                     
                elif 'series' in item_other_info.lower():
                    type = 'tv_seasons'
                    mode = common.mode_Content
                    indexer = common.indxr_TV_Shows 
                    
                self.AddContent(list, indexer, mode, item_title.strip(), '', type, url=item_url, name=item_name.strip(), year=item_year, imdb_id=item_id)
