

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import CustomSettings
from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay import Plugin
from entertainment import common
from entertainment.net import Net
import json, re

class tmdb(MovieIndexer,CustomSettings, ListIndexer):
    implements = [MovieIndexer,CustomSettings, ListIndexer]
	
    name = "tmdb"
    display_name = "TMDb"
    base_url = 'https://www.themoviedb.org'
    img = common.get_themed_icon('tmdb.png')
    fanart = common.get_themed_fanart('tmdb.jpg')
    default_indexer_enabled = 'false'

    def __init__(self):
        xml = '<settings>\n'
        xml += '<category label="Account">\n'
        xml += '<setting id="trakt_wl" type="bool" label="Enable Trakt.tv Watchlist:" default="false" />\n'
        xml += '<setting id="username" type="text" label="Trakt Username:" default="Enter your trakt username" enable="eq(-1,true)" />\n'
        xml += '</category>\n' 
        xml += '</settings>\n'
        self.CreateSettings(self.name, self.display_name, xml)

    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):
        net = Net(cached=False)
        type = common.indxr_Movies 
        mode = common.mode_File_Hosts
        indexer = common.indxr_Movies
        if section == 'new_releases':
            response = net.http_GET(url).content
            stuff = json.loads(response)
            for movies in stuff['movies']:
                title = movies['title']
                num = movies['year']
                name = title.encode('utf8')
                year = str(num)
                self.AddContent(list, indexer, common.mode_File_Hosts, name + ' (' + year +')', '', type, '', name, year)
        elif section == 'trakt_watchlist':
            response = net.http_GET(url).content
            stuff = json.loads(response)
            for movies in stuff:
                name = movies['title']
                if name:
                    name = name.encode('utf8')
                    year = str(movies['year'])
                    self.AddContent(list, indexer, mode, name + ' (' + year +')', '', type, '', name, year)
        elif section == 'list_name':
            response = net.http_GET(url).content
            stuff = json.loads(response)
            for items in stuff['items']:
                movies = items['movie']
                name = movies['title']
                if name:
                    name = name.encode('utf8')
                    year = str(movies['year'])
                    self.AddContent(list, indexer, mode, name + ' (' + year +')', '', type, '', name, year)    
        else:
            if page == '':
                page = '1'
            else:
                page = str(int(page))
                url = url + '&page=' + page
            response = net.http_GET(url).content
            stuff = json.loads(response)
            total_pages = stuff['total_pages']
            self.AddInfo(list, indexer, section, url, type, str(page), str(total_pages))
            for movies in stuff['results']:
                name = movies['title']
                date = movies['release_date']
                year = str(date)[0:4]
                name = name.encode('utf8')
                self.AddContent(list, indexer, common.mode_File_Hosts, name + ' (' + year +')', '', type, '', name, year)

    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):

        base_api = 'https://api.themoviedb.org/3/'
        key = '?api_key=3c31868688cafdc8d01a799aef97c69f'
        
        if section == 'main':
            if indexer == common.indxr_Movies:
                self.AddSection(list, indexer,'popular','Popular',base_api + 'movie/popular' + key,indexer, img=common.get_themed_icon('tmdb_pop.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
                self.AddSection(list, indexer,'top_rated','Top Rated',base_api + 'movie/top_rated' + key,indexer, img=common.get_themed_icon('tmdb_rated.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
                self.AddSection(list, indexer,'genres', 'Genres', img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
                self.AddSection(list, indexer,'studio','Studios', img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
                self.AddSection(list, indexer,'mpaa','MPAA Ratings', img=common.get_themed_icon('tmdb_mpaa.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
                self.AddSection(list, indexer,'new_releases','New Releases (DVD)','http://api.rottentomatoes.com/api/public/v1.0/lists/dvds/new_releases.json?page_limit=50&page=1&country=us&apikey=45nbuknsud2wjrp4tmhs6typ',indexer, img=common.get_themed_icon('tmdb_new.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            if self.Settings().get_setting('trakt_wl')=='true':
                self.AddSection(list, indexer,'trakt_watchlist','Trakt Watchlist','http://api.trakt.tv/user/watchlist/movies.json/fa6f7ac72530fe6393b5fb5d3a772198/' + self.Settings().get_setting('username'),indexer)
                self.AddSection(list, indexer,'trakt_lists','Trakt Lists','http://trakt.tv/user/%s/lists/' % self.Settings().get_setting('username'),indexer)
                
        elif section == 'genres':
            base_genre = base_api + 'discover/movie' + key +'&sort_by=popularity.desc&with_genres='
            self.AddSection(list, indexer,'action','Action',base_genre + '28',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'adventure','Adventure',base_genre + '12',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'animation','Animation',base_genre + '16',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'comedy','Comedy',base_genre + '35',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'crime','Crime',base_genre + '80',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'disaster','Disaster',base_genre + '105',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'documentary','Documentary',base_genre + '99',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'drama','Drama',base_genre + '18',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'eastern','Eastern',base_genre + '82',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'family','Family',base_genre + '10751',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'fanfilm','Fan Film',base_genre + '10750',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'fantasy','Fantasy',base_genre + '14',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'filmnoir','Film Noir',base_genre + '10753',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'foreign','Foreign',base_genre + '10769',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'history','History',base_genre + '36',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'holiday','Holiday',base_genre + '10595',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'horror','Horror',base_genre + '27',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'indie','Indie',base_genre + '10756',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'music','Music',base_genre + '10402',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'musical','Musical',base_genre + '22',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'mystery','Mystery',base_genre + '9648',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'neo-noir','Neo-noir',base_genre + '10754',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'roadmovie','Road Movie',base_genre + '1115',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'romance','Romance',base_genre + '10749',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'sci-fi','Sci-Fi',base_genre + '878',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'short','Short',base_genre + '10755',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'sport','Sport',base_genre + '9805',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'suspense','Suspense',base_genre + '10748',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'tvmovie','TV movie',base_genre + '10770',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'thriller','Thriller',base_genre + '53',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'war','War',base_genre + '10752',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'western','Western',base_genre + '37',indexer, img=common.get_themed_icon('tmdb_gen.png'), fanart=common.get_themed_fanart('tmdb.jpg'))

        elif section == 'studio':
            base_studio = base_api + 'discover/movie' + key + '&sort_by=popularity.desc&with_companies='
            self.AddSection(list, indexer,'warner_bros','Warner Bros.',base_studio + '6194',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'universal ','Universal',base_studio + '33',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'disney_Pictures','Walt Disney Pictures',base_studio + '2',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'disney_productions','Walt Disney Productions',base_studio + '3166',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'columbia','Columbia',base_studio + '5',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'fox','20th Century Fox',base_studio + '25',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'paramount','Paramount',base_studio + '4',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'lionsgate','Lionsgate',base_studio + '1632',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'dreamworks','DreamWorks',base_studio + '27',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'mgm','Metro Goldwyn Mayer',base_studio + '21',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'new_line','New Line Cinema',base_studio + '12',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'pixar','Pixar',base_studio + '3',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'Lucasfilm','Lucasfilm',base_studio + '1',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'rko','RKO Radio',base_studio + '6',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'miramax','Miramax',base_studio + '14',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'weinstein','Weinstein Company',base_studio + '308',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'relativity_media','Relativity Media',base_studio + '7295',indexer, img=common.get_themed_icon('tmdb_stud.png'), fanart=common.get_themed_fanart('tmdb.jpg'))

        elif section == 'mpaa':
            base_mpaa = base_api + 'discover/movie' + key + '&sort_by=popularity.desc&certification_country=US&certification='
            self.AddSection(list, indexer,'g','G',base_mpaa + 'G',indexer, img=common.get_themed_icon('tmdb_mpaa.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'pgl ','PG',base_mpaa + 'PG',indexer, img=common.get_themed_icon('tmdb_mpaa.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'pg13','PG-13',base_mpaa + 'PG-13',indexer, img=common.get_themed_icon('tmdb_mpaa.png'), fanart=common.get_themed_fanart('tmdb.jpg'))
            self.AddSection(list, indexer,'r','R',base_mpaa + 'R',indexer, img=common.get_themed_icon('tmdb_mpaa.png'), fanart=common.get_themed_fanart('tmdb.jpg'))

        elif section == 'trakt_lists':
            net = Net(cached=False)
            response = net.http_GET(url).content
            stuff = re.compile('<div class="title-overflow"></div>\n.+?<a href="/user/(.+?)/lists/(.+?)">(.+?)</a>').findall(response)
            for user, slug, list_name in stuff:
                self.AddSection(list, indexer,'list_name',list_name,'http://api.trakt.tv/user/list.json/fa6f7ac72530fe6393b5fb5d3a772198/%s/%s' %(user, slug),indexer)
            response_two = net.http_GET(url + 'liked').content
            stuff_two = re.compile('<div class="title-overflow"></div>\n.+?<a href="/user/(.+?)/lists/(.+?)">(.+?)</a>').findall(response_two)
            for user, slug, list_name in stuff_two:
                self.AddSection(list, indexer,'list_name','%s (%s)' % (list_name, user),'http://api.trakt.tv/user/list.json/fa6f7ac72530fe6393b5fb5d3a772198/%s/%s' %(user, slug),indexer)

        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
            
    def Search(self, srcr, keywords, type, list, lock, message_queue, page='', total_pages=''): 
        import urllib       
        query = urllib.quote_plus(keywords)
        search_url = 'https://api.themoviedb.org/3/search/movie?api_key=3c31868688cafdc8d01a799aef97c69f&sort_by=popularity.desc&query=' + query 
        self.ExtractContentAndAddtoList(srcr, 'search', search_url, type, list, page=page, total_pages=total_pages)
        
                

