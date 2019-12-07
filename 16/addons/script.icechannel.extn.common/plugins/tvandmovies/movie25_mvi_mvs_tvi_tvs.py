'''
    iStream
    Movie25 - by Coolwave    
    
'''

from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import TVShowIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay.interfaces import TVShowSource
from entertainment.plugnplay import Plugin
from entertainment import common
import xbmc



class movie25(MovieIndexer, MovieSource, TVShowIndexer, TVShowSource):

    implements = [MovieIndexer, MovieSource, TVShowIndexer, TVShowSource]
    
    name = "movie25"
    display_name ="Movie25"
    base_url = 'http://5movies.to/'
    img = common.get_themed_icon('m25.png')
    fanart = common.get_themed_fanart('m25.jpg')
    default_indexer_enabled = 'false'
    source_enabled_by_default = 'true'


    def ExtractContentAndAddtoList(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 

        if page == '':
            page = '1'
        from md_request import open_url
        import re,urllib

        url = urllib.unquote_plus(url)
            
        new_url = url
        html = open_url(new_url+str(page)).content
     
        if total_pages == '':
            if type == 'tv_shows':
                lastlist = '/tv/'+section.lower()+'/'
            else:
                lastlist = '/'+section.lower()+'/'
            r= ">Next</a>&nbsp;&nbsp;&nbsp;<a href='%s(.+?)/'>Last</a>" % lastlist
            try:
                total_pages = re.compile(r).findall(html)[0]
            except:
                total_pages = '1'
            
        self.AddInfo(list, indexer, section, new_url, type, str(page), total_pages)

        mode = common.mode_File_Hosts
        if type == 'tv_shows':
            mode = common.mode_Content
            type = 'tv_seasons'

        if section == 'featured' or 'new-release' or 'latest-added' or 'latest-hd' or 'latest-ts' or 'most-popular' or 'popular-today' or 'top-rated' or 'most-voted' or 'az' or 'genres' or 'year':
            match=re.compile('<div class="ml-img"><a href="(.+?)".+?target="_self".+?title="Watch (.+?) \((.+?)\)',re.DOTALL).findall(html.replace(' Online Free',''))
            for url,name,year in match:
                if url[1] == '/':
                    url = 'http:' + url
                if url[0] == '/':
                    url = url[1:]
                    url = self.base_url + url
                name = self.CleanTextForSearch(name)
                self.AddContent(list,indexer,mode,name + ' (' + year +')' ,'',type, url=url, name=name, year=year)




    def GetContent(self, indexer, url, title, name, year, season, episode, type, list):      
        
        
        from md_request import open_url
        import re,urllib
        
        url = urllib.unquote_plus(url)

        content = open_url(url).content
        
        if type == 'tv_seasons':
            for item in re.finditer("<a data-id='.+?' class='season-toggle' href='(.+?)'.+?>.+? Season ([0-9]+)<", content):
                item_url = item.group(1)
                if item_url[1] == '/':
                    item_url = 'http:' + item_url
                if item_url[0] == '/':
                    item_url = item_url[1:]
                    item_url = self.base_url + item_url

                item_v_id = item.group(2)
                item_title = 'Season ' + item_v_id
                
                item_id = common.CreateIdFromString(title + ' ' + item_title)
                
                self.AddContent(list, indexer, common.mode_Content, item_title, item_id, 'tv_episodes', url=item_url, name=name, year=year, season=item_v_id)
                
        elif type == 'tv_episodes':
        
            for item in re.finditer("<a href='(.+?)' title=.+?><strong>Episode</strong> ([0-9]+) .+?<", content):
                item_url = item.group(1)
                if item_url[1] == '/':
                    item_url = 'http:' + item_url
                if item_url[0] == '/':
                    item_url = item_url[1:]
                    item_url = self.base_url + item_url
                item_v_id = item.group(2)
                #item_title = item.group(3)
                #if item_title == None:
                item_title = ''
                
                item_id = common.CreateIdFromString(name + '_' + year + '_season_' + season + '_episode_' + item_v_id)
                
                self.AddContent(list, indexer, common.mode_File_Hosts, item_title, item_id, type, url=item_url, name=name, year=year, season=season, episode=item_v_id) 

        
            

    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''):

        from md_request import open_url

        if section == 'main':

            if indexer == common.indxr_Movies:

                self.AddSection(list, indexer,'featured','Featured',self.base_url +'featured/',indexer, img=common.get_themed_icon('m25_feat.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'new-release','New Releases',self.base_url +'new-release/',indexer, img=common.get_themed_icon('m25_rel.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'latest-added','Latest Added',self.base_url +'latest-added/',indexer, img=common.get_themed_icon('m25_late.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'latest-hd','Latest HD',self.base_url +'latest-hd/',indexer, img=common.get_themed_icon('m25_hd.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'latest-ts','Latest TS',self.base_url +'latest-ts/',indexer, img=common.get_themed_icon('m25_ts.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'most-popular','Most Popular',self.base_url +'most-popular/',indexer, img=common.get_themed_icon('m25_pop.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'popular-today','Popular Today',self.base_url +'popular-today/',indexer, img=common.get_themed_icon('m25_pop2day.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'top-rated','Top Rated',self.base_url +'top-rated/',indexer, img=common.get_themed_icon('m25_toprate.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'most-voted','Most Voted',self.base_url +'most-voted/',indexer, img=common.get_themed_icon('m25_voted.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'az','A-Z',self.base_url,indexer, img=common.get_themed_icon('m25_a_z.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'genres','Genres',self.base_url,indexer, img=common.get_themed_icon('m25_genres.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'year','Release Year',self.base_url,indexer, img=common.get_themed_icon('m25_year.png'), fanart=common.get_themed_fanart('m25.jpg'))

            elif indexer == common.indxr_TV_Shows:

                self.AddSection(list, indexer,'latest-added','Latest Added',self.base_url +'tv/latest-added/',indexer, img=common.get_themed_icon('m25_late.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'most-popular','Most Popular',self.base_url +'tv/most-popular/',indexer, img=common.get_themed_icon('m25_pop.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'popular-today','Popular Today',self.base_url +'tv/popular-today/',indexer, img=common.get_themed_icon('m25_pop2day.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'az','A-Z',self.base_url +'tv/',indexer, img=common.get_themed_icon('m25_a_z.png'), fanart=common.get_themed_fanart('m25.jpg'))
                self.AddSection(list, indexer,'genres','Genres',self.base_url +'tv/',indexer, img=common.get_themed_icon('m25_genres.png'), fanart=common.get_themed_fanart('m25.jpg'))




        elif section == 'az':

            if indexer == common.indxr_Movies:
                az_url = self.base_url
            elif indexer == common.indxr_TV_Shows:
                az_url = self.base_url + 'tv/'

            link = open_url(az_url).content
            get_all = common.md.regex_get_all(link, '>A-Z<', '</ul>')
            all_links = common.md.regex_get_all(str(get_all), '<li>', '</li>')

            for a in all_links:
                name = common.md.regex_from_to(a, 'title="', '"')
                url = common.md.regex_from_to(a, 'href="', '"')

                if url[1] == '/':
                    url = 'http:' + url
                if url[0] == '/':
                    url = url[1:]
                    url = self.base_url + url

                self.AddSection(list, indexer,name.split(' ')[0],name,url,indexer, img=common.get_themed_icon('m25_a_z.png'), fanart=common.get_themed_fanart('m25.jpg'))
            
                
                                   
        elif section == 'genres':

            if indexer == common.indxr_Movies:
                genres_url = self.base_url
            elif indexer == common.indxr_TV_Shows:
                genres_url = self.base_url + 'tv/'

            link = open_url(genres_url).content
            get_all = common.md.regex_get_all(link, '>Genres<', '</ul>')
            all_links = common.md.regex_get_all(str(get_all), '<li>', '</li>')

            for a in all_links:
                name = common.md.regex_from_to(a, 'title="', '"')
                url = common.md.regex_from_to(a, 'href="', '"')

                if url[1] == '/':
                    url = 'http:' + url
                if url[0] == '/':
                    url = url[1:]
                    url = self.base_url + url

                self.AddSection(list, indexer,name.split(' ')[0],name,url,indexer, img=common.get_themed_icon('m25_genres.png'), fanart=common.get_themed_fanart('m25.jpg'))




        elif section == 'year':

            if indexer == common.indxr_Movies:
                year_url = self.base_url

                link = open_url(year_url).content
                get_all = common.md.regex_get_all(link, '>Release Year<', '</ul>')
                all_links = common.md.regex_get_all(str(get_all), '<li>', '</li>')

                for a in all_links:
                    name = common.md.regex_from_to(a, 'title="', '"')
                    url = common.md.regex_from_to(a, 'href="', '"')

                    if url[1] == '/':
                        url = 'http:' + url
                    if url[0] == '/':
                        url = url[1:]
                        url = self.base_url + url

                    self.AddSection(list, indexer,'year/'+name.split(' ')[0],name,url,indexer, img=common.get_themed_icon('m25_year.png'), fanart=common.get_themed_fanart('m25.jpg'))
        

        else:
            self.ExtractContentAndAddtoList(indexer, section, url, type, list, page, total_pages, sort_by, sort_order)
            


          
    def GetFileHosts(self, url, list, lock, message_queue, season, episode, type, year, name):

        from md_request import open_url
        import urlresolver,re

        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}

        if type == 'tv_episodes':
            link = open_url(url,headers=headers).content
            data = re.findall(r"<a href='([^']*)'.*?'><strong>Episode<", str(link), re.I|re.DOTALL)
            for epi in data:
                if 'season-%s-episode-%s' %(season,episode) in epi:
                    url = epi
        else:
            url = url

        if url[1] == '/':
            url = 'http:' + url
        if url[0] == '/':
            url = url[1:]
            url = self.base_url + url

        content = open_url(url,headers=headers).content
        content = content.replace('\r','').replace('\n','').replace('\t','').replace('\b','')

        
        try:
            QUALITY  = content.split('>Links - Quality')[1]
            RES = QUALITY.split('</h1')[0].strip()
        except:
            RES = 'SD'


        data = re.findall(r'"links">(.*?)</div>', str(content), re.I|re.DOTALL)[0]
        match = re.findall(r'"link-name">(.*?)<li.*?class="link-button"><a.*?href="([^"]*)"', str(data), re.I|re.DOTALL)
        for host, host_id in match:

            host = host.replace('</li>','')

            try:
                
                if '4K' in RES.upper():
                    res='4K'
                elif '3D' in RES.upper():
                    res='3D'
                elif '1080' in RES.upper():
                    res='1080P'                   
                elif '720' in RES.upper():
                    res='720P'
                elif 'HD' in RES.upper():
                    res='HD'
                elif 'DVD' in RES.upper():
                    res='DVD'
                elif 'HDTS' in RES.upper():
                    res='TS'
                elif '-TS-' in RES.upper():
                    res='TS'
                elif 'TS' in RES.upper():
                    res='TS'
                elif 'CAM' in RES.upper():
                    res='CAM'
                elif 'HDCAM' in RES.upper():
                    res='CAM'
                else:
                    res='SD'

                if urlresolver.HostedMediaFile(host=host, media_id='ABC123XYZ'):
                    self.AddFileHost(list, res, host_id, host.upper())

            except:pass
            


            

    def GetFileHostsForContent(self, title, name, year, season, episode, type, list, lock, message_queue):

        from md_request import open_url
        import re

        name = self.CleanTextForSearch(name).lower().strip()

        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}

        search = '%ssearch.php?q=%s+%s' %(self.base_url,name.replace(' ','+'),year) 
        
        link = open_url(search,headers=headers,timeout=3).content
        links = link.split('list">')[1:]

        for p in links:

            try:

                media_url = re.compile('a href="([^"]+)"',re.DOTALL).findall(p)[0]
                if media_url[1] == '/':
                    media_url = 'http:' + media_url
                if media_url[0] == '/':
                    media_url = media_url[1:]
                    media_url = self.base_url + media_url
                media_title = re.compile('title="([^"]+)"',re.DOTALL).findall(p)[0]
                if type == 'tv_episodes':
                    if name in self.CleanTextForSearch(media_title.lower()):
                        if year in media_title.lower():
                            self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type, year, name)
                else:
                    if name in self.CleanTextForSearch(media_title.lower()):
                        if year in media_title.lower():
                            self.GetFileHosts(media_url, list, lock, message_queue, season, episode, type, year, name)

            except:pass




    def Resolve(self, url):

        from md_request import open_url
        import re

        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        request_url = '%s/getlink.php' %self.base_url
        link_id = url.split('=')
        form_data = {'Action':'get',link_id[0].replace('?',''):link_id[1]}
        play_url = open_url(request_url,method='post',data=form_data,headers=headers).text
        if play_url[1] == '/':
            play_url = 'http:' + play_url
        if play_url[0] == '/':
            play_url = play_url[1:]
            play_url = self.base_url + play_url

        from entertainment import istream
        play_url = istream.ResolveUrl(play_url.strip())
        return play_url
