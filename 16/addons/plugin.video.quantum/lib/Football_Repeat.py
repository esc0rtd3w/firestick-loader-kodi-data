'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import sys
import urlparse
import urllib,urllib2,datetime,re,os,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,traceback,cookielib,urlparse,httplib,time
import urlresolver
import yt
import process

Dialog = xbmcgui.Dialog()
Decode = base64.decodestring
footy = 'http://footytube.com'
League_Table_Url = 'http://www.sportinglife.com'
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.quantum/')
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
icon = ICON
addon_handle = int(sys.argv[1])

def footy_Main_Menu():
    process.Menu('Highlights','',403,ICON,FANART,'','')
    process.Menu('Fixtures','',404,ICON,FANART,'','')
    process.Menu('League Tables',League_Table_Url+'/football/tables',409,ICON,FANART,'','')
    process.Menu('Team Search',League_Table_Url+'/football/tables',410,ICON,FANART,'','')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def FootballFixturesDay():
    html=process.OPEN_URL('http://liveonsat.com/quickindex.html')
    match = re.compile('<a target="_self" href="(.+?)">.+?src="(.+?)" alt="(.+?)"',re.DOTALL).findall(html)
    for url,img,name in match:
        if '</a>' in img:
            pass
        if name == 'World Cup 2018':
            pass
        elif 'Handball' in name:
            pass
        elif 'bet365' in name:
            pass
        else:
            process.Menu((name).replace('amp;',''),'http://liveonsat.com/' + url,405,'http://liveonsat.com/' + img,FANART,'','')
		
def FootballFixturesGame(url,img):
    if 'daily' in url:
        get_daily(url)
    else:
        HTML = process.OPEN_URL(url)
        block = re.compile('<h2 class = time_head>(.+?)</h2>(.+?)<div class=float',re.DOTALL).findall(HTML)
        for date,block in block:
            process.Menu(date,'',420,img,FANART,block,'')
	
def get_daily(url):
    HTML = process.OPEN_URL(url)
    block = re.compile('comp_head>(.*?)</span>.*?<div class = fLeft width = ".*?"><img src="(.*?)">.*?</div>.*?ST:(.*?)</div>(.+?)<!-- around all of channel types ENDS 2-->',re.DOTALL).findall(HTML)
    for comp,img,time,chan in block:
        channel = re.compile(",CAPTION, '(.+?)&nbsp").findall(chan)
        channel_final = (str(channel)).replace('[$]','').replace('\\xc3','n').replace('\'','').replace('[','').replace(']','').replace('\\xe2','').replace('\\x80','').replace('\\x99','').replace('\\xb1a','i')
        name = str(comp) + ' - ' + str(time)
        image = Decode('aHR0cDovL2xpdmVvbnNhdC5jb20=') + str(img)
        process.Menu(name,'',405,image,FANART,channel_final,'')

def FootballFixturesSingle(block):
    game2 = re.compile('comp_head>(.*?)</span>.*?<div class = fLeft width = ".*?"><img src="(.*?)">.*?</div>.*?ST:(.*?)</div>(.+?)<!-- around all of channel types ENDS 2-->',re.DOTALL).findall(str(block))
    for comp,img,time,chan in game2:
        channel = re.compile(",CAPTION, '(.+?)&nbsp").findall(chan)
        channel_final = (str(channel)).replace('[$]','').replace('\\xc3','n').replace('\'','').replace('[','').replace(']','').replace('\\xe2','').replace('\\x80','').replace('\\x99','').replace('\\xb1a','i')
        name = str(comp) + ' - ' + str(time)
        image = Decode('aHR0cDovL2xpdmVvbnNhdC5jb20=') + str(img)
        process.Menu(name,'',405,image,FANART,channel_final,'')
    if len(block)<= 0:
        process.Menu('No Fixtures available yet, come back when season has started','','','','','','')
			
def Search():
    search_name = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    url = Decode('aHR0cDovL3d3dy5mdWxsbWF0Y2hlc2FuZHNob3dzLmNvbS8/cz0=')+(search_name).replace(' ','+')
    origin_url = Decode('http://www.footballorgin.com/?s=')+(search_name).replace(' ','+')
    Origin_Highlights(origin_url)
    Get_the_rows(url,ICON)
    
def Origin_Highlights(url):
    HTML = process.OPEN_URL(url)
    match = re.compile('<article id=".+?" class=".+?<img width=".+?" height=".+?" src="(.+?)" class=.+?<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h2>',re.DOTALL).findall(HTML)
    for img,url,name in match:
        name = (name).replace('&#8211;','-')
        process.Menu(name,url,418,img,FANART,'','')
		
def get_origin_playlink(url,img,FANART):
    List = []
    HTML = process.OPEN_URL(url)
    match = re.compile('1st Half<br />.+?<script data-config="(.+?)" data-height',re.DOTALL).findall(HTML)
    match2 = re.compile('2nd Half<br />.+?<script data-config="(.+?)" data-height',re.DOTALL).findall(HTML)
    match3 = re.compile('2nd Half<br />.+?<script data-config="(.+?)" data-height',re.DOTALL).findall(HTML)
    match4 = re.compile('<p>Watch Online Full Match Replay</p>.+?<p><script data-config="(.+?)" data-height',re.DOTALL).findall(HTML)
    match5 = re.compile('<p>&nbsp;<br />.+?<script data-config="(.+?)" data-height',re.DOTALL).findall(HTML)
    match6 = re.compile('<p>&nbsp;</p>.+?data-config="(.+?)" data-height=',re.DOTALL).findall(HTML)
    for url in match:
        Playlink = (url).replace('/v2', '').replace('zeus.json', 'video-sd.mp4?hosting_id=21772').replace('config.playwire.com', 'cdn.video.playwire.com')
        play_link = 'http:'+Playlink
        process.Play('1st Half',play_link,419,img,FANART,'','')
    for url in match2:
        Playlink = (url).replace('/v2', '').replace('zeus.json', 'video-sd.mp4?hosting_id=21772').replace('config.playwire.com', 'cdn.video.playwire.com')
        play_link = 'http:'+Playlink
        process.Play('2nd Half',play_link,419,img,FANART,'','')
        List.append('2nd Half')
    for url in match3:
        if '2nd Half' not in List:
            Playlink = (url).replace('/v2', '').replace('zeus.json', 'video-sd.mp4?hosting_id=21772').replace('config.playwire.com', 'cdn.video.playwire.com')
            play_link = 'http:'+Playlink
            process.Play('2nd Half',play_link,419,img,FANART,'','')
    for url in match4:
        if '2nd Half' not in List:
            if 'Full Match' not in List:
                Playlink = (url).replace('/v2', '').replace('zeus.json', 'video-sd.mp4?hosting_id=21772').replace('config.playwire.com', 'cdn.video.playwire.com')
                play_link = 'http:'+Playlink
                process.Play('Full Match',play_link,419,img,FANART,'','')
                List.append('Full Match')
    for url in match5:
        if '2nd Half' not in List:
            if 'Full Match' not in List:
                Playlink = (url).replace('/v2', '').replace('zeus.json', 'video-sd.mp4?hosting_id=21772').replace('config.playwire.com', 'cdn.video.playwire.com')
                play_link = 'http:'+Playlink
                process.Play('Full Match',play_link,419,img,FANART,'','')
                List.append('Full Match')
    for url in match6:
        if '2nd Half' not in List:
            if 'Full Match' not in List:
                Playlink = (url).replace('/v2', '').replace('zeus.json', 'video-sd.mp4?hosting_id=21772').replace('config.playwire.com', 'cdn.video.playwire.com')
                play_link = 'http:'+Playlink
                process.Play('Full Match',play_link,419,img,FANART,'','')
                List.append('Full Match')
 
	
def League_Tables(url):
    process.Menu('Premier League','http://www.bbc.co.uk/sport/football/premier-league/table',406,ICON,FANART,'','20')
#    process.Menu('Scottish Premier','http://www.sportinglife.com/football/scottish-premier/table',406,ICON,FANART,'','')
#    process.Menu('Championship','http://www.sportinglife.com/football/championship/table',406,ICON,FANART,'','')
#    process.Menu('Champions League','http://www.sportinglife.com/football/champions-league/table',412,ICON,FANART,'','')
#    process.Menu('Europa League','http://www.sportinglife.com/football/europa-league/table',412,ICON,FANART,'','')
#    process.Menu('League One','http://www.bbc.co.uk/sport/football/tables',411,ICON,FANART,'','')
#    process.Menu('League Two','http://www.sportinglife.com/football/league-two/table',411,ICON,FANART,'','')
#    process.Menu('Scottish Championship','http://www.sportinglife.com/football/scottish-championship/table',411,ICON,FANART,'','')
#    process.Menu('Scottish League One','http://www.sportinglife.com/football/scottish-league-one/table',411,ICON,FANART,'','')
#    process.Menu('Scottish League Two','http://www.sportinglife.com/football/scottish-league-two/table',411,ICON,FANART,'','')
#    process.Menu('National League','http://www.sportinglife.com/football/national-league/table',411,ICON,FANART,'','')
#    process.Menu('La Liga','http://www.sportinglife.com/football/la-liga/table',411,ICON,FANART,'','')
#    process.Menu('Serie A','http://www.sportinglife.com/football/serie-a/table',411,ICON,FANART,'','')
#    process.Menu('Bundesliga','http://www.sportinglife.com/football/bundesliga/table',411,ICON,FANART,'','')
#    process.Menu('Ligue 1','http://www.sportinglife.com/football/ligue-1/table',411,ICON,FANART,'','')
#    process.Menu('Eredivisie','http://www.sportinglife.com/football/eredivisie/table',411,ICON,FANART,'','')
#    process.Menu('Portuguese Liga','http://www.sportinglife.com/football/portuguese-liga/table',411,ICON,FANART,'','')

def Prem_Table(url,team_total):
    results = []
    sp1 = '                                                    '
    sp2 = '        '
    process.Menu('[COLORwhite]'+sp1+'pl'+sp2+'w'+sp2+'d'+sp2+'l'+sp2+'f'+sp2+'a'+sp2+'pts[/COLOR]','','','','','','')
    html=process.OPEN_URL('http://www.bbc.co.uk/sport/football/premier-league/table')
    match = re.compile('<td class="team-name"><a href=.+?>(.+?)</a>.+?<td class="played">(.+?)</td>.+?<td class="won"><span>(.+?)</span></td>.+?<td class="drawn">(.+?)</td>.+?<td class="lost">(.+?)</td>.+?<td class="for">(.+?)</td>.+?<td class="against">(.+?)</td>.+?<td class="goal-difference">(.+?)</td>.+?<td class="points">(.+?)</td>',re.DOTALL).findall(html)
    for team,pl,w,d,l,f,a,dif,pts in match:
        team = team.replace('West Bromwich Albion','West Brom').replace('Tottenham Hotspur','Spurs').replace('Manchester City','Man City').replace('Manchester United','Man United')
        team = team.replace('West Ham United','West Ham')
        pl_sp = gap(pl)
        w_sp = gap(w)
        d_sp = gap(d)
        l_sp = gap(l)
        f_sp = gap(f)
        a_sp = gap(a)
        results.append(team[0])
        pos = len(results)
        thing = Cleaner(team.upper())
        image = thing[1]
        sp_no = thing[0]
        if len(results)<=int(team_total):
            process.Menu(str(pos)+' '+team.upper()+sp_no+pl+pl_sp+w+w_sp+d+d_sp+l+l_sp+f+f_sp+a+a_sp+' '+pts,'','',image,'','','')

def clean_space(space):
    if len(space)>1:
        no = 8-len(space)
        space = int(no)*' '
    elif len(space)==1:
        space = '       '
    return space	
			
def Cleaner(team):
    image = ICON
    gap = ' '
    if '<a href' in team:
        pass
    else:
        if 'ARSENAL' in team:
            image = 'http://s018.radikal.ru/i519/1210/74/a0965770c1bd.png'
            gap = '                             '
        elif 'BOURNEMOUTH' in team:
            image = 'http://soccerlogo.net/uploads/posts/2015-02/1424200737_fc-afc-bournemouth.png'
            gap = '               '
        elif 'BURNLEY' in team:
            image = 'http://s019.radikal.ru/i627/1212/a9/cc25ae83d515.png'
            gap = '                            '
        elif 'CHELSEA' in team:
            image = 'http://soccerlogo.net/uploads/posts/2014-09/1410462243_fc-chelsea.png'
            gap = '                              '
        elif 'CRYSTAL' in team:
            image = 'http://jonwant.com/wp-content/uploads/2015/04/crystalpalace.png'
            gap = '            '
        elif 'EVERTON' in team:
            image = 'http://megaicons.net/static/img/icons_sizes/257/622/256/everton-fc-icon.png'
            gap = '                             '
        elif 'HULL CITY' in team:
            image = 'http://www.fm-base.co.uk/forum/attachments/football-manager-2013-manager-stories/367359d1373707600-molineux-theatre-dreams-wolves-story-hull.png'
            gap = '                         '
        elif 'LEICE' in team:
            image = 'http://soccerlogo.net/uploads/posts/2014-09/1410463960_fc-leicester-city.png'
            gap = '               '
        elif 'LIVERPOOL' in team:
            image = 'http://i641.photobucket.com/albums/uu140/marveljoe_bucket/Liverpool-FC-256x256.png'
            gap = '                          '
        elif 'MAN CITY' in team:
            image = 'http://icons.iconseeker.com/png/fullsize/british-football-club/manchester-city.png'
            gap = '                            '
        elif 'MAN UNITED' in team:
            image = 'https://hdlogo.files.wordpress.com/2013/11/manchester-united.png'
            gap = '                      '
        elif 'BROUGH' in team:
            image = 'http://s25.postimg.org/g611tr767/Badge_Middlesbrough256x256.png'
            gap = '            '
        elif 'SOUTHAMPTON' in team:
            image = 'http://s019.radikal.ru/i639/1210/48/3326d080e375.png'
            gap = '               '
        elif 'STOKE CITY' in team:
            image = 'http://s55.radikal.ru/i147/1210/96/e3f610ab745c.png'
            gap = '                         '
        elif 'SUNDERLAND' in team:
            image = 'http://futhead.cursecdn.com/static/img/16/clubs/106.png'
            gap = '                   '
        elif 'SWANSEA' in team:
            image = 'http://soccerlogo.net/uploads/posts/2014-09/1410462864_fc-swansea_city.png'
            gap = '                '
        elif 'SPURS' in team:
            image = 'http://s14.radikal.ru/i187/1210/d2/243ffe6f2f90.png'
            gap = '                                   '
        elif 'WATFORD' in team:
            image = 'http://s25.postimg.org/bclw2n027/Badge_Watford256x256.png'
            gap = '                          '
        elif 'BROM' in team:
            image = 'http://s018.radikal.ru/i516/1210/6c/d0990201b8d2.png'
            gap = '                        '
        elif 'WEST HAM' in team:
            image = 'http://s018.radikal.ru/i502/1210/60/c38b78fbbdb1.png'
            gap = '                         '
        return gap,image

def gap(space):
    spacer = '        '
    if int(space)>=100:
        spacer = '     '
    elif int(space)>=10:
        spacer = '      '
    return spacer


def Football_Highlights():

    process.Menu('Footy Tube','http://www.footytube.com/leagues',413,ICON,FANART,'','')
    process.Menu('Latest','http://www.fullmatchesandshows.com',408,'http://www.fancyicons.com/free-icons/125/miscellaneous/png/256/football_256.png',FANART,'','')
    process.Menu('Shows','http://www.fullmatchesandshows.com/category/show/',408,'http://www.fm-base.co.uk/forum/attachments/club-competition-logos/3885-soccer-am-logo-socceram.png',FANART,'','')
    process.Menu('Premier League','http://www.fullmatchesandshows.com/premier-league/',408,'https://footballseasons.files.wordpress.com/2013/05/premier-league.png',FANART,'','')
    process.Menu('La Liga','http://www.fullmatchesandshows.com/la-liga/',408,'http://1.bp.blogspot.com/-c6kQ40ryhyo/U19cUlz25sI/AAAAAAAABak/qtn5chSFZm0/s1600/la-liga-logo_display_image.png',FANART,'','')
    process.Menu('Bundesliga','http://www.fullmatchesandshows.com/bundesliga/',408,'http://m.img.brothersoft.com/iphone/189/518670189_icon175x175.jpg',FANART,'','')
    process.Menu('Champions League','http://www.fullmatchesandshows.com/champions-league/',408,'http://www.ecursuri.ro/images/teste/test-champions-league.jpg',FANART,'','')
    process.Menu('Serie A','http://www.fullmatchesandshows.com/category/serie-a/',408,'http://files.jcriccione.it/200000223-2484526782/serie%20a.png',FANART,'','')
    process.Menu('Ligue 1','http://www.fullmatchesandshows.com/category/ligue-1/',408,'http://a1.mzstatic.com/us/r30/Purple5/v4/37/c7/44/37c744ae-5824-42b7-6ce0-5f471f52baab/icon180x180.jpeg',FANART,'','')

def footytube(url):
    HTML = process.OPEN_URL(url)
    block_and_name = re.compile('<div class="headline_xlrg color_dgray"><img align="absmiddle" height="22" src="(.+?)">(.+?)</div>').findall(HTML)
    for img,name in block_and_name:
        process.Menu(name,'',414,footy+img,FANART,'','')
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	

		
def footytube_leagues(name):
    url = 'http://www.footytube.com/leagues'
    check = name
    HTML = process.OPEN_URL(url)
    block_and_name = re.compile('<div class="headline_xlrg color_dgray"><img align="absmiddle" height="22" src="(.+?)">'+name+'</div>(.+?)<div style="margin-bottom: 15px">',re.DOTALL).findall(HTML)
    for img,block in block_and_name:
        leagues = re.compile('<div>.+?<a href="(.+?)" class="standard_link">(.+?)</a><br>.+?<span class="text_xsml">(.+?)</span>.+?</div>',re.DOTALL).findall(str(block))
        for url,name,qty in leagues:
            process.Menu(name + ' - ' + qty,footy+url,415,ICON,FANART,'','')
        else:
            pass		
			
def footytube_teams(url):
    HTML = process.OPEN_URL(url)
    match = re.compile('<div class=".+?" style = ".+?"><a href="(.+?)" class=".+?" >(.+?)</a></div>').findall(HTML)
    for url,name in match:
        process.Menu(name,footy+url,416,ICON,FANART,'','')
        	
def footytube_videos(url):
    HTML = process.OPEN_URL(url)
    match = re.compile(' <div class="thumboverlay"> .+?<div><a href="(.+?)".+?<img src="(.+?)" width="165px" height="97px" /></a></div>.+?<div class="vid_title".+?class="standard_link">(.+?)</a><div class="vid_info">(.+?)</div>',re.DOTALL).findall(HTML)
    for url,img,name,age in match:
        process.Play(name + ' - ' + age, footy+url,417,img,FANART,'','')

		
def footytube_frame(name,url):
	HTML = process.OPEN_URL(url)
	match = re.compile('<iframe src="(.+?)" width=').findall(HTML)
	for url in match:
		url = footy + url
		get_footytube_PLAYlink(url)	
	match_youtube = re.compile('<iframe id="ft_player" width="100%" height="100%" src="http://www.youtube.com/embed/(.+?)?rel=0&autoplay=1&enablejsapi=1" frameborder="0" allowfullscreen></iframe>').findall(HTML)
	for url in match_youtube:
		import process
		url = 'plugin://plugin.video.youtube/play/?video_id='+url
		process.Big_Resolve(name,url)

		
def get_footytube_PLAYlink(name,url):
	HTML = process.OPEN_URL(url)
	match_youtube = re.compile('<iframe width="560" height="315" src="https://www.youtube.com/embed/(.+?)" frameborder="0" allowfullscreen>').findall(HTML)
	for url in match_youtube:
		import process
		url = 'plugin://plugin.video.youtube/play/?video_id='+url
		process.Big_Resolve(name,url)    
	match = re.compile('<script data-config="(.+?)" data-css=".+?" data-height="100%" data-width="100%" src=".+?" type="text/javascript"></script>').findall(HTML)
	for playlink in match:
		if 'div' in playlink:
			pass
		else:
			Playlink = (playlink).replace('/v2', '').replace('zeus.json', 'video-sd.mp4?hosting_id=21772').replace('config.playwire.com', 'cdn.video.playwire.com')
			process.Big_Resolve(name,'http:'+Playlink)
		
		
def Get_the_rows(url,iconimage):
    HTML = process.OPEN_URL(url)
    match2 = re.compile('<div class="td-module-thumb"><a href="(.+?)".+?title="(.+?)".+?"entry-thumb" src="(.+?)"').findall(HTML)
    for url,name,img in match2:
        if 'Full Match' in name:
    	    Name = name.replace('&#8211;', '-').replace('&#038;', '&').replace('&#8217;', '')
            process.Menu(Name,url,407,img,'','','')
        else:
    	    Name = name.replace('&#8211;', '-').replace('&#038;', '&').replace('&#8217;', '')
            process.Play(Name,url,402,img,'','','')
    Next = re.compile('<span class="current">.+?</span><a href="(.+?)" class="page" title=".+?">(.+?)</a>').findall(HTML)
    for url,name in Next:
        process.Menu('NEXT PAGE',url,401,iconimage,FANART,'','')
		
def get_All_Rows(url,iconimage):
    HTML = process.OPEN_URL(url)
    block = re.compile('<div class="td-block-span6">(.+?)<div class="td-pb-span4 td-main-sidebar">',re.DOTALL).findall(HTML)
    match2 = re.compile('<div class="td-module-thumb"><a href="(.+?)".+?title="(.+?)".+?"entry-thumb" src="(.+?)"').findall(str(block))
    for url,name,img in match2:
        if 'Full Match' in name:
    	    Name = name.replace('&#8211;', '-').replace('&#038;', '&').replace('&#8217;', '')
            process.Menu(Name,url,407,img,'','','')
        else:
    	    Name = name.replace('&#8211;', '-').replace('&#038;', '&').replace('&#8217;', '')
            process.Play(Name,url,402,img,'','','')
    Next = re.compile('<span class="current">.+?</span><a href="(.+?)" class="page" title=".+?">(.+?)</a>').findall(HTML)
    for url,name in Next:
        process.Menu('NEXT PAGE',url,401,iconimage,FANART,'','')
    if len(match2)<=0:
        process.Menu('No Replays available sorry',url,401,iconimage,FANART,'','')


def get_Multi_Links(url,iconimage):
    process.Play('Extended Highlights',url,402,iconimage,FANART,'','')
    HTML = process.OPEN_URL(url)
    match = re.compile('<link href=".+?" rel="stylesheet" type="text/css"><li tabindex="0" class="button_style" id=".+?"><a href="(.+?)"><div class="acp_title">(.+?)</div></a></li>').findall(HTML)
    for url2,name in match:
        url = url+url2
        name = (name).replace('HL English','English Highlights')
        process.Play(name,url,402,iconimage,FANART,'','')
		
def get_PLAYlink(name,url):
    HTML = process.OPEN_URL(url)
    match_youtube = re.compile('<iframe width="560" height="315" src="https://www.youtube.com/embed/(.+?)" frameborder="0" allowfullscreen>').findall(HTML)
    for url in match_youtube:
        yt.PlayVideo(url)
    match = re.compile('<script data-config="(.+?)" data-height').findall(HTML)
    for playlink in match:
        if 'div' in playlink:
            pass
        else:
            Playlink = (playlink).replace('/v2', '').replace('zeus.json', 'video-sd.mp4?hosting_id=21772').replace('config.playwire.com', 'cdn.video.playwire.com')
            process.Big_Resolve(name,'http:'+Playlink)

	


