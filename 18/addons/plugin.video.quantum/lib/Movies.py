# -*- coding: utf-8 -*-
import urllib,re,xbmcgui,xbmcplugin,xbmc,sys,process,requests,re

base_icons = 'http://herovision.x10host.com/freeview/'
BAMF_ICON = base_icons + 'BAMF.png'

def Movie_Main(url):
    if 'cunts' in url:
        import Pandora
        Pandora.Pandoras_Box('http://genietvcunts.co.uk/PansBox/ORIGINS/moviecat.php')
    process.Menu('Genre','',202,'','','','')
    process.Menu('IMDB top 250 Films','http://www.imdb.com/chart/top',206,'','','','')
    process.Menu('Movie Channels','',208,'','','','')
    process.Menu('Search','',207,'','','','')
	
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def scrape_movie(url):
    process.Menu('[COLORblue][B]MOVIES BY GENRE[/B][/COLOR]','',100071,'http://2.bp.blogspot.com/_s8fgo2oOrGA/TJniXdGtoJI/AAAAAAAAAHM/EE43v4CdIU4/s1600/5803926-movie-poster-of-film-genres-vintage-background.jpg',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]MOVIES BY YEAR[/B][/COLOR]','',100073,'https://e.snmc.io/lk/l/s/5b799d8ed01a5bbcfa9dd2bb0290b642/5942704.png',BAMF_ICON,'','','','')
    html = requests.get(url).text
    Next = re.compile('<li><a class="next page-numbers" href="(.+?)">Next .+?</a>',re.DOTALL).findall(html)
    block = re.compile("Archives: Movies </h3>.+?<div class=\"item-img\">(.+?)<ul class=\"pagination\"><li>",re.DOTALL).findall(html)
    match = re.compile('<div class="col-sm-4 col-xs-6 item responsive-height">.+?<a href="(.+?)"><img width=.+?src="(.+?)" class=.+?alt="(.+?)"',re.DOTALL).findall(str(block))
    for url, img, name in match:
        html2 = requests.get(url).text
        frame = re.compile('<div class="process.Player.+?">.+?<IFRAME SRC="(.+?)" FRAMEBORDER',re.DOTALL).findall(html2)
        for source in frame:
            html3 = requests.get(source).text
            match = re.compile('\|vvad\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|.+?var\|100\|(.+?)\|',re.DOTALL).findall(html3)
            for a,b,c,d,link in match:
                if a == 'xyz':
                    fin_url = 'http://xyz.streamjunkie.tv/hls/'+link+',.urlset/master.m3u8'
                    process.Play(name,fin_url,906,img,img,'','')
                else:
                    fin_url = 'http://'+d+'.'+c+'.'+b+'.'+a+'/hls/,'+link+',.urlset/master.m3u8'
                    process.Play(name,fin_url,906,img,img,'','')
    for nxt in Next:
        process.Menu('[COLORblue][B]NEXT[/B][/COLOR]',nxt,100070,'',BAMF_ICON,'','','','')
        


def movie_genre():
    process.Menu('[COLORblue][B] ACTION[/B][/COLOR]','http://onlinemoviescinema.com/genre/action/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] ADVENTURE[/B][/COLOR]','http://onlinemoviescinema.com/genre/adventure/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] ANIMATION[/B][/COLOR]','http://onlinemoviescinema.com/genre/animation/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] COMEDY[/B][/COLOR]','http://onlinemoviescinema.com/genre/comedy/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] CRIME[/B][/COLOR]','http://onlinemoviescinema.com/genre//',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] DOCUMENTARY[/B][/COLOR]','http://onlinemoviescinema.com/genre/documentary/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] DRAMA[/B][/COLOR]','http://onlinemoviescinema.com/genre/drama/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] FAMILY[/B][/COLOR]','http://onlinemoviescinema.com/genre//family',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] FANTASY[/B][/COLOR]','http://onlinemoviescinema.com/genre/fantasy/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] FOREIGN[/B][/COLOR]','http://onlinemoviescinema.com/genre/foreign/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] HISTORY[/B][/COLOR]','http://onlinemoviescinema.com/genre/history/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] HORROR[/B][/COLOR]','http://onlinemoviescinema.com/genre/horror/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] MUSIC[/B][/COLOR]','http://onlinemoviescinema.com/genre/music/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] MYSTERY[/B][/COLOR]','http://onlinemoviescinema.com/genre/mystery/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] ROMANCE[/B][/COLOR]','http://onlinemoviescinema.com/genre/romance/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] SCIENCE FICTION[/B][/COLOR]','http://onlinemoviescinema.com/genre/science-fiction/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] SPORTS[/B][/COLOR]','http://onlinemoviescinema.com/genre/sports/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] THRILLER[/B][/COLOR]','http://onlinemoviescinema.com/genre/thriller/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] TV MOVIE[/B][/COLOR]','http://onlinemoviescinema.com/genre/tv-movie/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] WAR[/B][/COLOR]','http://onlinemoviescinema.com/genre/war/',100072,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B] WESTERN[/B][/COLOR]','http://onlinemoviescinema.com/genre/western/',100072,'',BAMF_ICON,'','','','')
    

def scrape_movie_genre(url,name):
    process.Menu(name,'','','',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]BACK TO GENRES[/B][/COLOR]','',100071,'http://2.bp.blogspot.com/_s8fgo2oOrGA/TJniXdGtoJI/AAAAAAAAAHM/EE43v4CdIU4/s1600/5803926-movie-poster-of-film-genres-vintage-background.jpg',BAMF_ICON,'','','','')
    html = requests.get(url).text
    Next = re.compile('<li><a class="next page-numbers" href="(.+?)">Next .+?</a>',re.DOTALL).findall(html)
    block = re.compile("<h3>Movie Genre.+?</h3>.+?<div class=\"item-img\">(.+?)<ul class=\"pagination\"><li>",re.DOTALL).findall(html)
    match = re.compile('<div class="col-sm-4 col-xs-6 item responsive-height">.+?<a href="(.+?)"><img width=.+?src="(.+?)" class=.+?alt="(.+?)"',re.DOTALL).findall(str(block))
    for url, img, name in match:
        html2 = requests.get(url).text
        frame = re.compile('<div class="process.Player.+?">.+?<IFRAME SRC="(.+?)" FRAMEBORDER',re.DOTALL).findall(html2)
        for source in frame:
            html3 = requests.get(source).text
            match = re.compile('\|vvad\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|.+?var\|100\|(.+?)\|',re.DOTALL).findall(html3)
            for a,b,c,d,link in match:
                if a == 'xyz':
                    fin_url = 'http://xyz.streamjunkie.tv/hls/'+link+',.urlset/master.m3u8'
                    process.Play(name,fin_url,906,img,img,'','')
                else:
                    fin_url = 'http://'+d+'.'+c+'.'+b+'.'+a+'/hls/,'+link+',.urlset/master.m3u8'
                    process.Play(name,fin_url,906,img,img,'','')
            
    for nxt in Next:
        process.Menu('[COLORblue][B]NEXT[/B][/COLOR]',nxt,100072,'',BAMF_ICON,'','','','')

        
def scrape_year():
    process.Menu('[COLORblue][B]2017[/B][/COLOR]','http://onlinemoviescinema.com/watch-2017-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2016[/B][/COLOR]','http://onlinemoviescinema.com/watch-2016-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2015[/B][/COLOR]','http://onlinemoviescinema.com/watch-2015-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2014[/B][/COLOR]','http://onlinemoviescinema.com/watch-2014-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2013[/B][/COLOR]','http://onlinemoviescinema.com/watch-2013-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2012[/B][/COLOR]','http://onlinemoviescinema.com/watch-2012-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2011[/B][/COLOR]','http://onlinemoviescinema.com/watch-2011-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2010[/B][/COLOR]','http://onlinemoviescinema.com/watch-2010-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2009[/B][/COLOR]','http://onlinemoviescinema.com/watch-2009-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2008[/B][/COLOR]','http://onlinemoviescinema.com/watch-2008-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2007[/B][/COLOR]','http://onlinemoviescinema.com/watch-2007-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2006[/B][/COLOR]','http://onlinemoviescinema.com/watch-2006-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2005[/B][/COLOR]','http://onlinemoviescinema.com/watch-2005-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2004[/B][/COLOR]','http://onlinemoviescinema.com/watch-2004-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2003[/B][/COLOR]','http://onlinemoviescinema.com/watch-2003-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2002[/B][/COLOR]','http://onlinemoviescinema.com/watch-2002-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2001[/B][/COLOR]','http://onlinemoviescinema.com/watch-2001-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]2000[/B][/COLOR]','http://onlinemoviescinema.com/watch-2000-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1999[/B][/COLOR]','http://onlinemoviescinema.com/watch-1999-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1998[/B][/COLOR]','http://onlinemoviescinema.com/watch-1998-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1997[/B][/COLOR]','http://onlinemoviescinema.com/watch-1997-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1996[/B][/COLOR]','http://onlinemoviescinema.com/watch-1996-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1995[/B][/COLOR]','http://onlinemoviescinema.com/watch-1995-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1994[/B][/COLOR]','http://onlinemoviescinema.com/watch-1994-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1993[/B][/COLOR]','http://onlinemoviescinema.com/watch-1993-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1992[/B][/COLOR]','http://onlinemoviescinema.com/watch-1992-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1991[/B][/COLOR]','http://onlinemoviescinema.com/watch-1991-movies/',100074,'',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]1990[/B][/COLOR]','http://onlinemoviescinema.com/watch-1990-movies/',100074,'',BAMF_ICON,'','','','')
    
    
     
def scrape_movie_year(url,name):
    process.Menu(name,'','','',BAMF_ICON,'','','','')
    process.Menu('[COLORblue][B]BACK TO YEARS[/B][/COLOR]','',100071,'https://e.snmc.io/lk/l/s/5b799d8ed01a5bbcfa9dd2bb0290b642/5942704.png ',BAMF_ICON,'','','','')
    html = requests.get(url).text
    Next = re.compile('<li><a class="next page-numbers" href="(.+?)">Next .+?</a>',re.DOTALL).findall(html)
    block = re.compile('<h3>Movies of:.+?</h3>(.+?)<ul class="pagination"><li>',re.DOTALL).findall(html)
    match = re.compile('<div class="col-sm-4 col-xs-6 item responsive-height">.+?<a href="(.+?)"><img width=.+?src="(.+?)" class=.+?alt="(.+?)"',re.DOTALL).findall(str(block))    
    for url, img, name in match:
        html2 = requests.get(url).text
        frame = re.compile('<div class="process.Player.+?">.+?<IFRAME SRC="(.+?)" FRAMEBORDER',re.DOTALL).findall(html2)
        for source in frame:
            html3 = requests.get(source).text
            match = re.compile('\|vvad\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|.+?var\|100\|(.+?)\|',re.DOTALL).findall(html3)
            for a,b,c,d,link in match:
                if a == 'xyz':
                    fin_url = 'http://xyz.streamjunkie.tv/hls/'+link+',.urlset/master.m3u8'
                    process.Play(name,fin_url,906,img,img,'','')
                else:
                    fin_url = 'http://'+d+'.'+c+'.'+b+'.'+a+'/hls/,'+link+',.urlset/master.m3u8'
                    process.Play(name,fin_url,906,img,img,'','')
            
    for nxt in Next:
        process.Menu('[COLORblue][B]NEXT[/B][/COLOR]',nxt,100074,'',BAMF_ICON,'','','','')


def movie_channels():
    from datetime import datetime
    Year = datetime.now().strftime('%Y')
    Month = datetime.now().strftime('%m')
    Day = datetime.now().strftime('%d')
    Hour = datetime.now().strftime('%H')
    Minute = datetime.now().strftime('%M')
    time_now_number = str((int(Hour)*60)+int(Minute))
    url = 'http://www.tvguide.co.uk/?catcolor=000000&systemid=5&thistime='+Hour+'&thisDay='+Month+'/'+Day+'/'+Year+'&gridspan=03:00&view=0&gw=1323'
    try:
        html = requests.get(url).text
        channel_block = re.compile('<div class="div-epg-channel-progs">.+?<div class="div-epg-channel-name">(.+?)</div>(.+?)</div></div></div>',re.DOTALL).findall(html)
        for channel,block in channel_block:
            prog = re.compile('<a qt-title="(.+?)"(.+?)onmouse',re.DOTALL).findall(str(block.encode('utf-8')))
            for show_info, info in prog:
                time_finder = re.compile('(.+?)-(.+?) ').findall(str(show_info))
                for start,finish in time_finder:
                    stop = []
                    if len(stop)<10:
                        if 'am' in start:
                            time_split = re.compile('(.+?):(.+?)am').findall(str(start))
                            for hour,minute in time_split:
                                start_number = (int(hour) * 60) + int(minute)
                        elif 'pm' in start:
                            time_split = re.compile('(.+?):(.+?)pm').findall(str(start))
                            for hour,minute in time_split:
                                if hour =='12':
                                    start_number = (int(hour) * 60) + int(minute)
                                else:
                                    start_number = (int(hour) + 12) * 60 + int(minute)
                        if 'am' in finish:
                            time_split = re.compile('(.+?):(.+?)am').findall(str(finish))
                            for hour,minute in time_split:
                                finish_number = (int(hour) * 60) + int(minute)
                        elif 'pm' in finish:
                            time_split = re.compile('(.+?):(.+?)pm').findall(str(finish))
                            for hour,minute in time_split:
                                if hour =='12':
                                    finish_number = (int(hour) * 60) + int(minute)
                                else:
                                    finish_number = (int(hour) + 12) * 60 + int(minute)
                        if int(start_number)<int(time_now_number)<int(finish_number):
                            clean_channel = channel.replace('BBC1 London','BBC1').replace('BBC2 London','BBC2').replace('ITV London','ITV1')
                            splitter = show_info + '>'
                            movie_search = re.compile('m (.+?)>').findall(str(splitter))
                            for item in movie_search:
                                fin_item = item
                            process.Menu(clean_channel.encode('utf-8') + ': '+ show_info.encode('utf-8'),'',209,'','','',fin_item)

    except:
        pass
		
def split_for_search(extra):
	year = re.compile('\((.+?)\)').findall(str(extra))
	for item in year:
		year = item
	name = extra.replace('\(','').replace('\)','').replace(year,'')
	import Scrape_Nan;Scrape_Nan.scrape_movie(name,year)

def search_movies():
	Search_title = xbmcgui.Dialog().input('Search', type=xbmcgui.INPUT_ALPHANUM)
	url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='+Search_title.replace(' ','+')+'&s=all'
	html = requests.get(url).text
	match = re.compile('<tr class="findResult.+?"> <td class="primary_photo"> <a href=".+?" ><img src="(.+?)" /></a> </td> <td class="result_text"> <a href=".+?" >(.+?)</a>(.+?)</td>').findall(html)
	for image,title,year in match:
		if '<' in year:
			pass
		else:
			if '(TV Series)' in year:
				pass
			else:
				image = image.replace('32,44','174,256').replace('UY67','UY256').replace('UX32','UX175').replace('UY44','UY256')
				process.Menu(title,'Movies',1501,image,'','','OLD')
				process.setView('movies', 'INFO')
	
def Movie_Genre(url):
	html = requests.get('http://www.imdb.com/genre/').text
	match = re.compile('<h3><a href="(.+?)">(.+?)<span class="normal">').findall(html)
	for url, name in match:
		url = 'http://www.imdb.com/search/title?genres='+name.replace(' ','').lower()+'&title_type=feature&sort=moviemeter,asc'
		process.Menu(name,url,203,'','','','')
		process.setView('movies', 'INFO')
		
def IMDB_Top250(url):
	html = requests.get(url).text
	film = re.compile('<td class="posterColumn">.+?<img src="(.+?)".+?<td class="titleColumn">(.+?)<a.+?title=".+?" >(.+?)</a>.+?<span class="secondaryInfo">(.+?)</span>',re.DOTALL).findall(html)
	for img,no,title,year in film:
		no = no.replace('\n','').replace('	','').replace('  ','')
		try:
			img = img.replace('45,67','174,256').replace('UY67','UY256').replace('UX45','UX175')
			process.Menu(title + ' ' + year,'Movies',1501,img,'','','OLD')
		except:
			pass
		
def IMDB_Grab(url):
	try:
		List = []
		xbmc.log(url)
		html = requests.get(url).text	
		match = re.compile('<div class="lister-item-image float-left">.+?<a href="(.+?)".+?<img alt="(.+?)".+?loadlate="(.+?)".+?<span class="lister-item-year text-muted unbold">(.+?)</span>.+?<p class="text-muted">\n(.+?)</p>',re.DOTALL).findall(html)
		for url,name,image,year,desc in match:
			image = image.replace('45,67','174,256').replace('UY67','UY256').replace('UX67','UX175').replace('UY98','UY256').replace('SX54','SX170').replace('54,74','174,256').replace('67,98','174,256')
			try:
				if '(2018)' in year:
					pass
				else:
					xbmc.log(image)
					year = year.replace('(I) ','').replace('II','')
					process.Menu(name + ' ' + year,'Movies',1501,image,'',desc,'OLD')
					process.setView('movies', 'INFO')
			except:
				pass
		next_page = re.compile('<a href="(.+?)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>').findall(html)
		for item in next_page:
			if item not in List:
				process.Menu('Next Page','http://imdb.com/search/title'+item,203,'','','','')
				List.append(item)
	except:
		pass