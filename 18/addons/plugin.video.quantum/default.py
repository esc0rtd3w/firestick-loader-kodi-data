# -*- coding: utf-8 -*-

'''
    Qauntum Add-on
    Copyright (C) 2016 Origin

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
	
    Just don't be a nob about it....

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
	
    This addon could not of became what it is without the help and generosity of everyone involved.
    Not all of the coding is my original work but i have tried my best to utilise and learn from others.
    If i have used code that you wrote i can only apologise for not thanking you personally and ensure you no offence was meant.
    Just sometimes i find it best not to rewrite what works well, mostly to a higher standard that my current understanding
'''
import xbmcplugin, xbmc, xbmcaddon, urllib, xbmcgui, traceback, requests, re, os, base64 , liveresolver 
from lib import process
from BeautifulSoup import BeautifulSoup
import os, shutil, xbmcgui
from lib import cloudflare
from lib.modules import cfscrape
scraper = cfscrape.create_scraper()
addon_id = 'plugin.video.quantum'
Dialog = xbmcgui.Dialog()
addons = xbmc.translatePath('special://home/addons/')
ADDON = xbmcaddon.Addon(id=addon_id)
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.quantum/')
ICON = ADDON_PATH + 'icon.png'
ADDON = xbmcaddon.Addon(id=addon_id)
FANART = ADDON_PATH + 'fanart.jpg'
Adult_Pass = ADDON.getSetting('Adult')
Adult_Default = ADDON.getSetting('Porn_Pass')
base_icons = 'http://herovision.x10host.com/freeview/'
ORIGIN_ICON = ADDON_PATH + 'icon.png'
ORIGIN_FANART = ADDON_PATH + 'fanart.jpg'
PANDORA_ICON = 'https://s32.postimg.org/ov9s6ipf9/icon.png'
RAIDER_ICON = base_icons + 'pyramid.png'
FREEVIEW_ICON = base_icons + 'freeview.png'
NINJA_ICON = base_icons + 'ninja2.png'
BRETTUS_ICON = base_icons + 'brettus_anime.png'
OBLIVION_ICON = base_icons + 'oblivion.png'
TIGEN_ICON = base_icons + 'Tigen.png'
COLD_ICON = base_icons + 'Cold.png'
BAMF_ICON = base_icons + 'BAMF.png'
RENEGADES_ICON = base_icons + 'renegades.png'
QUICK_ICON = base_icons + 'quick.png'
RAY_ICON = base_icons + 'raysraver.png'
SILENT_ICON = base_icons + 'silent.png'
REAPER_ICON = base_icons + 'reaper.png'
DOJO_ICON = base_icons + 'dojo.png'
ULTRA_ICON = base_icons + 'Ultra.png'
FIDO_ICON = base_icons + 'fido.png'
MIDNIGHT_IMAGE = base_icons + 'midnight2.png'
SUPREM_ICON = base_icons + 'supremacy.png'
app_icon = base_icons + 'app.jpg'
INTRO_VID = base_icons + 'Intro.mp4'
INTRO_VID_TEMP = xbmc.translatePath('special://home/addons/plugin.video.quantum/DELETE_ME')

ADDONS      =  xbmc.translatePath(os.path.join('special://home','addons',''))
addon_id='plugin.video.quantum'
current_folder = ADDONS+'/'+addon_id+'/'
full_file = current_folder.replace('\\','/') + '/welcome.txt'

def TextBoxes(heading,announce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(announce); text=f.read()
      except: text=announce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()
  TextBox()

if not os.path.exists(full_file):
    Open = open(full_file,'w+')
    TextBoxes('Quantum',' [COLORorangered]UPDATED TO V 0.0.7 Fixed Quantum Cartoons section and Quantum 24/7 [/COLOR] \nFixed Fido 24/7 section \nFixed all porn sections and Removed broken sections \nBrand new addon added in addons section, Big thanks to noobsandnerds for letting me intergrate NaNscrapers \nFixed some of the porn sections Thanks to an old friend ;) although some bits still not showing\nBut keep getting distracted fixing them god knows why :) \nAdded new section for Fido 24/7 which is also in his stand alone add-on \nMORE STUFF COMING SOON :) :)\nTeam Quantum')




def Main_Menu():
    #if not os.path.exists(INTRO_VID_TEMP):
        #if ADDON.getSetting('Intro_Vid')=='true':
            #xbmc.Player().play(INTRO_VID, xbmcgui.ListItem('You have been updated'))
            #os.makedirs(INTRO_VID_TEMP)
    process.Menu('Big Bag \'O\' Tricks','',13,'',FANART,'','')
    #process.PLAY('test','http://daclips.in/embed-secaio8j2y8i-1238x696.html',906,'',FANART,'','')
    #process.Menu('dizi','',100051,'',FANART,'','')
    if ADDON.getSetting('View_Type')=='Classic':
        classic_list()
    elif ADDON.getSetting('View_Type')=='IMDB':
        IMDB_list()
    elif ADDON.getSetting('View_Type')=='TV Shows':
		TV_Men()
    elif ADDON.getSetting('View_Type')=='Movies':
		Movie_Men()
    elif ADDON.getSetting('View_Type')=='Sport':
		sports()
    elif ADDON.getSetting('View_Type')=='Music':
		Music_Men()
    elif ADDON.getSetting('View_Type')=='Kids':
		Kids_Men()
    elif ADDON.getSetting('View_Type')=='24/7':
		twenty47()
    elif ADDON.getSetting('View_Type')=='Docs':
		docs()
    elif ADDON.getSetting('View_Type')=='Live':
		Live_Men()
    elif ADDON.getSetting('View_Type')=='Adult':
		Adult()
    elif ADDON.getSetting('View_Type')=='Menu':
		process.Menu('24/7','',38,'',FANART,'','')
		process.Menu('Documentaries','',39,'',FANART,'','')
		process.Menu('Kids','',33,'',FANART,'','')
		process.Menu('Live TV','',32,'',FANART,'','')
		process.Menu('Movies','',30,'',FANART,'','')
		process.Menu('Music','',34,'',FANART,'','')
		process.Menu('Sports','',40,'',FANART,'','')
		process.Menu('TV Shows','',31,'',FANART,'','')
		if Adult_Pass == Adult_Default:
			process.Menu('Adult','',37,'',FANART,'','')
		process.Menu('Add-on\'s','',35,'',FANART,'','')
		#process.Menu('live test','',100035,'',FANART,'','')
		#process.Menu('most popular','',100036,'',FANART,'','')
		#process.Menu('returndates','',100038,'',FANART,'','')
		#process.Menu('table','',100050,'',FANART,'','')
		process.setView('movies', 'INFO')
 


        
def dmain():
    html = requests.get('https://www.laola1.tv/en-int/block/darts-europe-pdc-europe-european-tour-latest-videos').content
    block = re.compile('<h2>European Darts Tour - Latest Videos</h2>(.+?)<div class="paging-wrapper dark clearfix">',re.DOTALL).findall(html)
    match = re.compile('<a href="(.+?)".+?<img src="(.+?)".+?<p>(.+?)</p>',re.DOTALL).findall(str(block))
    for url, img, name in match:
        img = 'https:'+img
        url = 'https://www.laola1.tv'+url
        process.Menu(name,url,13,img,img,'','')       


def mpop():
    html = requests.get('http://www.imdb.com/chart/tvmeter?ref_=nv_tvv_mptv_4').content
    match = re.compile('<td class="posterColumn">.+?<img src="(.+?)".+?title=".+?" >(.+?)</a>.+?data-titleid="(.+?)">',re.DOTALL).findall(html)
    for img, name, im in match:
        imnew = 'http://imdb.com/title/'+im
        getseaseps(name,imnew)
        
        
def getseaseps(name,imnew):
    html = requests.get(imnew).content
    block = re.compile('<link rel=\'image_src\' href="(.+?)">.+?<h4 class="float-left">Years</h4><hr />(.+?)<div  >',re.DOTALL).findall(html)
    #match = re.compile('<a href="(.+?)"',re.DOTALL).findall(str(block))
    for img, All in block:
        match = re.compile('<a href="(.+?)"',re.DOTALL).findall(str(block))
        for seas in match:
            seas = seas
        process.Menu(name,'',100036,img,img,'','')

def tv_running():
    HTML = requests.get('http://www.returndates.com/index.php?running=1').content
    match = re.compile('></td><td><font size=4>(.+?)</font.+?/td><td><font size=4>(.+?)</font></td><td><font size=4>(.+?)</font></td><td><font size=4>(.+?)</font></td><td><font size=4>(.+?)</font>.+?<a href="(.+?)"',re.DOTALL).findall(HTML)
    for name,season,status,date,day,Link in match:
        Link = 'http://www.returndates.com/'+Link
        process.Menu(name,Link,100039,'','','','')
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
            
def eps(name,url):
    show_name = name
    html = requests.get(url).content
    match = re.compile("<tr bgcolor='.+?' class='.+?'><td>(.+?)</td><td>(.+?)</td>.+?<p>(.+?)</p>",re.DOTALL).findall(html)
    match2 = re.compile("</td></tr><tr><td colspan=2>.+?<a href='http://www.imdb.com/title/(.+?)'",re.DOTALL).findall(html)
    for imdb in match2:
        imdb = imdb
    for sesep, date, name in match:
        sesep = sesep.replace(' ','')
        if name == ' ':
            name = "unknown"
        year = date[0:4]
        #if sesep.lower() == 's01e01':
            #show_year = date
        season = sesep[1:3]
        eps = sesep[4:6]
        process.Menu(show_name+'- Season'+season+'- Episode'+eps+'- year'+year,'',100045,'','','',show_name)
        
def send_to_search2(name,extra):
    #xbmc.log('name:'+(str(extra)),xbmc.LOGNOTICE)
    dp =  xbmcgui.DialogProgress()
    dp.create('Checking for stream')
    from lib import Scrape_Nan
    name_splitter = name + '<>'
    name_split = re.compile('(.+?)- SEASON -(.+?)- EPISODE-(.+?)-(.+?)<>').findall(str(name_splitter))
    for title,season,episode,show_year in name_split:
        title = title
        season = season
        episode = episode
        tvdb = ''
        Scrape_Nan.scrape_episode(title,show_year,'',season,episode,'')
    #search.TV(Search_name)

def dizi_main():
    headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
    html = scraper.get('http://www.dizi720p.co/diziler').content
    match = re.compile('<div class="item-image">.+?href="(.+?)".+?<img src="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html)
    for url,img,name in match:
        process.Menu(name,url,100052,img,img,'','')


def get_dizi_eps(url):
    headers = {"host":"www.dizi720p.co",
                 "referer":url,
                 "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"
                 }
    ep

def scrape_dizi(title,season, episode):
    xbmc.log('##############'+title+season+episode,xbmc.LOGNOTICE)
    base_link = 'http://www.dizi720p.co/'
    sources = []
    
    start_url = base_link+title.replace(' ','-')+'-'+season.replace('0','')+'-sezon-'+episode+'-bolum-izle.html'
    html = scraper.get(start_url).content
    block = re.compile('<ul class="dropdown-menu" role="menu">(.+?)</ul></div><div class="pull-right">',re.DOTALL).findall(html)
    for Block in block:
        print('12345')
    match = re.compile('<iframe src="(.+?)"').findall(html)
    for frame in match:
        if not '.html' in frame:
            #print(frame)
            if 'watchserieshd.xyz' in frame:
                html2 = scraper.get(frame).content
                match2 = re.compile('file: "(.+?)",.+?label":"(.+?)"',re.DOTALL).findall(html2)
                for url,p in match2:
                    process.PLAY('test'+p,url,906,'','','','')
            if '.ru' in frame:
                if 'videoembed' in frame:
                    process.PLAY('test',frame,906,'','','','')
            if 'streamango' in frame:
                html4 = scraper.get(frame).content
                match4 = re.compile('type:"video/mp4",src:"(.+?)"').findall(html4)
                for link3 in match4:
                    link3 = 'https:'+link3
                    process.PLAY('test streamango',link3,906,'','','','')
        match_multi = re.compile('<a href="(.+?)">(.+?)</a>').findall(str(Block))
        for page,name in match_multi:
            if not 'http' in name:
                if '.ru' in name:
                    html3 = scraper.get(page).content
                    match = re.compile('<iframe.+?src="(.+?)"').findall(html3)
                    for frame in match:
                        if not '.html' in frame:
                            if name.lower() in frame:
                                
                                process.PLAY('testok.ru','https:'+frame,906,'','','','')
                elif 'Mango' in name:
                    html3 = scraper.get(page).content
                    match = re.compile('<iframe.+?src="(.+?)"').findall(html3)
                    for frame in match:
                        html4 = scraper.get(frame).content
                        match4 = re.compile('type:"video/mp4",src:"(.+?)"').findall(html4)
                        for link3 in match4:
                            link3 = 'https:'+link3
                            process.PLAY('test streamango',link3,906,'','','','')

                elif 'Raptu' in name:
                    html3 = scraper.get(page).content
                    match = re.compile('<iframe.+?src="(.+?)"').findall(html3)
                    for frame in match:
                        html4 = scraper.get(frame).content
                        match2 = re.compile('"sources"(.+?)"logo"').findall(html4)
                        for block in match2:
                            match3 = re.compile('"https:(.+?)"').findall(str(block))
                            for link3 in match3:
                                link3 = 'https:'+link3.replace('\/\/','//').replace('\/','/')
                                process.PLAY('test Raptu',link3,906,'','','','')

def table():
    results = []
    sp1 = '                                         '
    sp2 = '        '
    process.Menu('[COLORwhite][B]'+sp1+'pl'+sp2+'w'+sp2+'d'+sp2+'l'+sp2+'f'+sp2+'a'+sp2+'pts[/B][/COLOR]','','','','','','')
    html = requests.get('http://livefootball.com/football/england/premier-league/').content
    match = re.compile('</li><li><a href="/football/england/premier-league/league-table/away/".+?title="Rank">([^<]*)</td>.+?title="Played">([^<]*)</td>.+?title="Wins">([^<]*)</td>.+?title="Draws">([^<]*)</td>.+?title="Lost">([^<]*)</td>.+?title="Goals For">([^<]*)</td>.+?title="Goals Against">([^<]*)</td>.+?title="Goals Difference">([^<]*)</td>.+?title="Points">([^<]*)</td>(.+?)</table></div>',re.DOTALL).findall(html)            
    #match2 = re.compile('</li><li><a href="/football/england/premier-league/league-table/away/".+?<td class="ltn">([^<]*)</td><td class="ltg">([^<]*)</td><td class="ltw">([^<]*)</td><td class="ltd">([^<]*)</td><td class="ltl">([^<]*)</td><td class="ltgf">([^<]*)</td><td class="ltga">([^<]*)</td><td class="ltgd">([^<]*)</td><td class="ltp">([^<]*)</td></tr><tr><td class="ltid">([^<]*)</td>',re.DOTALL).findall(str(rest))
    for r,p,w,d,l,f,a,df,pts,rest in match:
        r = "POS"
        space = "       "
        rest = rest
        #process.Menu(sp1+p+sp2+w+sp2+d+sp2+l+sp2+f+sp2+a+sp2+df+sp2+pts,'','','','','','')
        match2 = re.compile('<td class="ltid">([^<]*)</td><td class="ltn">([^<]*)</td><td class="ltg">([^<]*)</td><td class="ltw">([^<]*)</td><td class="ltd">([^<]*)</td><td class="ltl">([^<]*)</td><td class="ltgf">([^<]*)</td><td class="ltga">([^<]*)</td><td class="ltgd">([^<]*)</td><td class="ltp">([^<]*)</td></tr>',re.DOTALL).findall(str(rest))
        for iD,team,pl,w,d,l,f,ga,gd,p, in match2:
            pos = iD+team
            team = team.replace('Brighton &amp; Hove Albion','Brighton').replace('AFC Bournemouth','Bournemouth')
            team = team.replace('West Bromwich Albion','West Brom').replace('Tottenham Hotspur','Spurs').replace('Manchester City','Man City').replace('Manchester United','Man United')
            team = team.replace('West Ham United','West Ham')
            pl_sp = gap(pl)
            w_sp = gap(w)
            d_sp = gap(d)
            l_sp = gap(l)
            f_sp = gap(f)
            a_sp = gap(ga)
            thing = Cleaner(team.upper())
            image = thing[1]
            sp_no = thing[0]
            process.Menu(team+sp_no+pl+pl_sp+w+w_sp+d+d_sp+l+l_sp+f+f_sp+ga+a_sp+' '+p,'','',image,'','','')

def Cleaner(team):
    image = ICON
    gap = ' '
    if '<a href' in team:
        pass
    else:
        if 'ARSENAL' in team:
            image = 'http://s018.radikal.ru/i519/1210/74/a0965770c1bd.png'
            gap = '                            '
        elif 'BRIGHTON' in team:
            image = 'http://www.northstandchat.com/attachment.php?attachmentid=72847&d=1457183704'
            gap = '                          '
        elif 'BOURNEMOUTH' in team:
            image = 'http://soccerlogo.net/uploads/posts/2015-02/1424200737_fc-afc-bournemouth.png'
            gap = '                '
        elif 'BURNLEY' in team:
            image = 'http://s019.radikal.ru/i627/1212/a9/cc25ae83d515.png'
            gap = '                            '
        elif 'CHELSEA' in team:
            image = 'http://soccerlogo.net/uploads/posts/2014-09/1410462243_fc-chelsea.png'
            gap = '                            '
        elif 'CRYSTAL' in team:
            image = 'http://jonwant.com/wp-content/uploads/2015/04/crystalpalace.png'
            gap = '                  '
        elif 'EVERTON' in team:
            image = 'http://megaicons.net/static/img/icons_sizes/257/622/256/everton-fc-icon.png'
            gap = '                             '
        elif 'HUDDERSFIELD' in team:
            image = 'http://s019.radikal.ru/i636/1301/0c/438a3af0c463.png'
            gap = '         '
        elif 'LEICE' in team:
            image = 'http://soccerlogo.net/uploads/posts/2014-09/1410463960_fc-leicester-city.png'
            gap = '                   '
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
            gap = '                  '
        elif 'STOKE CITY' in team:
            image = 'http://s55.radikal.ru/i147/1210/96/e3f610ab745c.png'
            gap = '                         '
        elif 'SUNDERLAND' in team:
            image = 'http://futhead.cursecdn.com/static/img/16/clubs/106.png'
            gap = '                   '
        elif 'SWANSEA' in team:
            image = 'http://soccerlogo.net/uploads/posts/2014-09/1410462864_fc-swansea_city.png'
            gap = '                   '
        elif 'SPURS' in team:
            image = 'http://s14.radikal.ru/i187/1210/d2/243ffe6f2f90.png'
            gap = '                                '
        elif 'WATFORD' in team:
            image = 'http://s25.postimg.org/bclw2n027/Badge_Watford256x256.png'
            gap = '                            '
        elif 'BROM' in team:
            image = 'http://s018.radikal.ru/i516/1210/6c/d0990201b8d2.png'
            gap = '                      '
        elif 'WEST HAM' in team:
            image = 'http://s018.radikal.ru/i502/1210/60/c38b78fbbdb1.png'
            gap = '                       '
        elif 'NEWCASTLE' in team:
            image = 'https://b.fssta.com/uploads/content/dam/fsdigital/fscom/global/dev/static_resources/soccer/teams/english-premier-league/retina/6151.vresize.200.200.medium.0.png'
            gap = '            '
        return gap,image

def gap(space):
    spacer = '        '
    if int(space)>=100:
        spacer = '     '
    elif int(space)>=10:
        spacer = '      '
    return spacer
    
def News(title,url):
    if "News" in title:
        News = requests.get(url).text
        match = re.compile('(.+?)',re.DOTALL).findall(str(News))
        for stuff in match:
            TextBoxes('[COLOR navy]OffShore[/COLOR] [COLOR blue]IPTV[/COLOR]',stuff)
        
def livetest():
    domain = 'http://www.footballstreamings.com/channels.html'
    html = requests.get(domain).text
    #match = re.compile('<td width="20%" align=.+?<strong>(.+?)</strong></span></td>',re.DOTALL).findall(html)
    #block = re.compile('<div id="accordion1">(.+?)p>Please give your feedback for Sports Channels at <a',re.DOTALL).findall(html)
    mach = re.compile('<td width="20%" align=.+?22px;"><strong>(.+?)</strong></span></td>.+?<td width="48%">LINK</td>(.+?)<table width="100%" border="0">',re.DOTALL).findall(html)
    for chann, rest in mach:
        Links = re.compile('<td><strong>(.+?)</strong></td>.+?<td><a href="(.+?)"',re.DOTALL).findall(str(rest))
        for watch, Plink in Links:
            if 'filmon' in Plink:
                plinking = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +Plink
                process.Play('these links may die'+' '+chann+'\n'+watch,plinking,906,'',FANART,'','')
            elif 'cine' or 'v2' or 'cric' in Plink:
                plinking = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +Plink
                process.Play(chann+'\n'+watch,plinking,906,'',FANART,'','')
        #chann+'\n'+watch
def IMDB_list():
	process.Menu('TV Shows','',300,'','','','')
	process.Menu('Movies','',200,'','','','')
	process.Menu('Favourites','',10,'','','','')
	process.setView('movies', 'INFO')
		
def twenty47():
	from lib.pyramid import pyramid
	process.Menu('quantum 24/7 Cartoons','',812,ORIGIN_ICON,FANART,'','')
	process.Menu('Fido 24/7','',100060,FIDO_ICON,FANART,'','')
	#process.Menu('Pyramid 24/7','http://tombraiderbuilds.co.uk/addon/tvseries/247shows/247shows.txt',1101,RAIDER_ICON,'','','')
	process.Menu('Supremacy 24/7','http://stephen-builds.uk/supremacy/24-7/24-7.txt',1101,SUPREM_ICON,'','','')
	#process.Random_play('Raiz TV - Play 10 Random Cartoons',1154,url='http://raiztv.co.uk/RaysRavers/list2/raiztv/kids/kidsrandom.txt',image=RAY_ICON,isFolder=False)
	
def docs():
	process.Menu('Fido Documentaries','http://fantazyrepo.uk/addonimages/fido.addon/newmovies/documentary.xml',1101,FIDO_ICON,FANART,'','','')
	process.Menu('Pyramid Documentaries','http://tombraiderbuilds.co.uk/addon/documentaries/documentaries.txt',1101,RAIDER_ICON,'','','')
	#process.Menu('Raiz Documentaries','http://raiztv.co.uk/RaysRavers/list2/raiztv/doc/doc.txt',1101,RAY_ICON,'','','')
	
def sports():
	process.Menu('Renegades Darts','',2150,RENEGADES_ICON,FANART,'','')
	process.Menu('DELIVERANCE','',1139,'https://3.bp.blogspot.com/-mRS8HrApaaY/WOI17mTddmI/AAAAAAAAXBo/CaxwCX7o47QZxaV6W1Qeff39ZyQjYuI5wCLcB/s1600/Deliverance%2BKodi%2B17%2B1.png',FANART,'','')
	process.Menu('BAMF Live Sports','http://genietvcunts.co.uk/bamffff/livesports.xml',1101,BAMF_ICON,'','','')
	process.Menu('Fido Sports','http://bit.ly/2oBKluF',1101,FIDO_ICON,FANART,'','')
	process.Menu('Football Replays','',400,ORIGIN_ICON,FANART,'','')
	process.Menu('Today\'s Football','',1750,ICON,FANART,'','')
		
def Adult():
	process.Menu('Just For Him','',1400,NINJA_ICON,FANART,'','')
	process.Menu('Fido','http://bit.ly/2nGWTl6',1101,FIDO_ICON,'','','')
	process.Menu('X Videos','',700,'https://pbs.twimg.com/profile_images/378800000578199366/cf160c1c86c13778a834bbade0c30e38.jpeg',FANART,'','')
	process.Menu('Porn Hub','',708,'http://cdimage.debian.org/mirror/addons.superrepo.org/v7/addons/plugin.video.pornhub/icon.png',FANART,'','')
	process.Menu('X Hamster','',714,'http://www.logospike.com/wp-content/uploads/2016/05/Xhamster_Logo_03.png',FANART,'','')
	process.Menu('Chaturbate','',720,'https://pbs.twimg.com/profile_images/671662441210753024/sE2tHWMB_400x400.png',FANART,'','')
	process.Menu('You Porn','',723,'http://www.ares-portal.com/wp-content/uploads/2016/12/plugin.video_.youporngay.png',FANART,'','')
	process.Menu('Red Tube','',730,'http://gosha-portal.pp.ua/1311/pic/redtube.png',FANART,'','')
	process.Menu('Tube 8','',738,'https://a3-images.myspacecdn.com/images03/1/cb9e1e694ca941abaf62f0026d18049f/300x300.jpg',FANART,'','')
	process.Menu('Thumbzilla','',745,'http://static.spark.autodesk.com/2013/02/14__13_53_32/data2cd61048-351b-4b48-bd9c-946e7e076b53Medium2.jpg',FANART,'','')
	process.Menu('XTube','',753,'https://pbs.twimg.com/profile_images/732348322044903425/xTK0J4Cz.jpg',FANART,'','')
	process.Menu('Eporner','',760,'http://kenny2u.org/wp-content/uploads/2016/09/icon-1.png',FANART,'','')
	process.Menu('YouJizz','',771,'https://pbs.twimg.com/profile_images/3332003625/23c080fbec17cfb45ca3fd40ec06afe1.png',FANART,'','')
	process.Menu('Spank Wire','',772,'http://kenny2u.org/wp-content/uploads/2016/09/icon-43.png',FANART,'','')
	process.Menu('4k','',758,'https://pbs.twimg.com/profile_images/700315084980035588/fZZO6Pf-.jpg',FANART,'','')
	process.Menu('VR','http://www.xvideos.com/?k=vr',701,'https://pbs.twimg.com/profile_images/741907565689217024/DByQczLO.jpg',FANART,'','')


def Movie_Men():
	process.Menu('Search','Movies',1501,'','','','')
	process.Menu('Recent Movies','',5,ICON,FANART,'','')
	process.Menu('4k','4k',36,'','','','')
	process.Menu('3D','3D',36,'','','','')
	process.Menu('1080p','1080p',36,'','','','')
	process.Menu('Other - Linked to add-on\'s menu as most have movies','Other',36,'','','','')

def Movie_Def(url):
	if url == '4k':
		from lib.pyramid import pyramid
		#process.Menu('Silent Hunter 4k','http://silenthunter.srve.io/main/4k.xml',1101,SILENT_ICON,FANART,'','','')
		#process.Menu('Pandora 4k','http://genietvcunts.co.uk/PansBox/ORIGINS/4Kmovies.php',426,PANDORA_ICON,'','','')
		process.Menu('Pyramid 4k','http://tombraiderbuilds.co.uk/addon/movies/uhd/uhd.txt',1101,RAIDER_ICON,'','','')
	elif url == '3D':
		#process.Menu('Pandora 3D','http://genietvcunts.co.uk/PansBox/ORIGINS/hey3D.php',426,PANDORA_ICON,'','','')
		process.Menu('Pyramid 3D','http://tombraiderbuilds.co.uk/addon/movies/3d/3d.txt',1101,RAIDER_ICON,'','','')
	elif url == '1080p':
		process.Menu('Pandora 1080p','http://genietvcunts.co.uk/PansBox/ORIGINS/hey1080p.php',426,PANDORA_ICON,'','','')
	elif url == 'Other':
		classic_list()


def TV_Men():
	process.Menu('Search','TV',1501,'','','','')
	process.Menu('Latest Episodes','',3,ICON,FANART,'','')
	from lib.pyramid import pyramid
	#process.Menu('Pandora\'s TV','http://genietvcunts.co.uk/PansBox/ORIGINS/tvcats.php',423,PANDORA_ICON,'','','')
	#process.Menu('Cerberus TV','http://roguemedia.x10.mx/cerberus/add-on/tvmenu.php',2301,REAPER_ICON,'','','')
	pyramid.not_so_anon('Pyramid TV','[QT][WI][XU][BU][ID][SS][PD][YO][LS][MW][SS][ID][UR][YO][JJ][LS][UP][WX][RJ][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YZ][WI][FA][UP][MW][SS][YO][MW][UP][YZ][WI][FA][AL][XU][QZ][MW][BU][PD][YO][QZ]Have a nice day now',RAIDER_ICON,FANART,'','','')
	#process.Menu('Tigen\'s TV','http://kodeeresurrection.com/TigensWorldtxt/TvShows/Txts/OnDemandSub.txt',1101,TIGEN_ICON,'','','')
	#process.Menu('Raiz TV','http://raiztv.co.uk/RaysRavers/list2/raiztv/tv/tv.txt',1101,RAY_ICON,'','','')
	process.Menu('Dojo TV','http://herovision.x10host.com/dojo/tvshows/tvshows.php',2300,DOJO_ICON,'','','')
	process.Menu('BAMF\'s Classics','http://genietvcunts.co.uk/bamffff/bamfoldtv.xml',1101,BAMF_ICON,FANART,'','')

def Live_Men():
	process.Menu('Search','Live TV',1501,'','','','')
	process.Menu('TV Guide','',2200,ICON,FANART,'','')
	from lib.pyramid import pyramid
	#process.Menu('Oblivion IPTV','',1129,OBLIVION_ICON,FANART,'','')
	#process.Menu('BAMF IPTV','http://genietvcunts.co.uk/bamffff/BAMF.xml',1101,BAMF_ICON,FANART,'','')
	pyramid.not_so_anon('Pyramid Live','[QT][WI][XU][BU][ID][SS][PD][YO][LS][MW][SS][ID][UR][YO][JJ][LS][UP][WX][RJ][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YZ][UR][YY][MW][QZ][WI][MW][SS][WI][PD][YO][QZ][BU][MW][QZ][WI][YZ][UR][YY][MW][QZ][WI][MW][SS][WI][PD][YO][QZ][BU][MW][QZ][WI]Have a nice day now',RAIDER_ICON,FANART,'','','')
	#process.Menu('Ultra Live',base64.decodestring('aHR0cDovL3VsdHJhdHYubmV0MTYubmV0L2lwdHZzZXJ2ZXIvcG9ydGFsLnhtbA=='),1101,ULTRA_ICON,'','','')
	pyramid.not_so_anon('Fido Live','@WI@@NL@@SE@@OF@@OU@@SE@@HE@@OT@@UQ@@ON@@OG@@FS@@OW@@RS@@PE@@PC@@SE@@AY@@AY@@FS@@OF@@LS@@LE@@SE@@YF@@ON@@KY@@PC@@NL@@LS@@AY@@FS@@OW@@SE@@AY@@AY@@FS@@OF@@PC@L@LS@@EL@@ON@@OU@@EL@@PC@@OP@@LS@@EL@@ON@@OU@@EL@@OW@@OF@@ON@@FO@Hope you enjoy the view',FIDO_ICON,FANART,'','','')
	process.Menu('FreeView - [COLORred]VPN required if you are outside UK[/COLOR]','',1200,FREEVIEW_ICON,FANART,'','')
	process.Menu('Deliverence Live','http://www.sport-xplosion.com/DELIVERANCE%20TXT%20FILES/home.txt',1101,'http://kodeeresurrection.com/LILYSPORTS/plugin.video.LILYSPORTS/icon.png','','','')
	process.Menu('Supremacy Live','http://stephen-builds.uk/supremacy/LiveTV/live.txt',1101,SUPREM_ICON,'','','')

def Kids_Men():
	process.Menu('Search','cartoon',1501,'','','','')
	from lib.pyramid import pyramid
	#process.Menu('Tigen\'s World','',1143,TIGEN_ICON,FANART,'','')
	#process.Menu('Raiz Kids','http://raiztv.co.uk/RaysRavers/list2/raiztv/kids/kidsmain.txt',1101,RAY_ICON,'','','')
	process.Menu('Quantum Kids','',800,ORIGIN_ICON,ORIGIN_FANART,'','')
	process.Menu('Oblivion Kids','http://pastebin.com/raw/Y8X1vCaV',1101,OBLIVION_ICON,'','','')
	pyramid.not_so_anon('Pyramid Kids','[QT][WI][XU][BU][ID][SS][PD][YO][LS][MW][SS][ID][UR][YO][JJ][LS][UP][WX][RJ][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YZ][YY][YO][LS][UP][RJ][KW][PD][QZ][QZ][MW][JJ][UP][YZ][YY][YO][LS][UP][RJ][KW][PD][QZ][QZ][MW][JJ][UP]Have a nice day now',RAIDER_ICON,FANART,'','','')
	pyramid.not_so_anon('Fido Live','@WI@@NL@@SE@@OF@@OU@@SE@@HE@@OT@@UQ@@ON@@OG@@FS@@OW@@RS@@PE@@PC@@SE@@AY@@AY@@FS@@OF@@LS@@LE@@SE@@YF@@ON@@KY@@PC@@NL@@LS@@AY@@FS@@OW@@SE@@AY@@AY@@FS@@OF@@PC@B@FS@@KM@S@ON@@OU@@KY@@PC@@NS@@SE@@UQ@@OU@@FS@@FS@@OF@@KY@@PC@@LS@@OF@@AY@@ON@@KM@@OW@@OF@@ON@@FO@Hope you enjoy the view',FIDO_ICON,FANART,'','','')
	process.Menu('BAMF\'s Kids','http://genietvcunts.co.uk/bamffff/lfk.xml',1101,BAMF_ICON,'','','')
	process.Menu('Supremacy Kids Live','http://stephen-builds.uk/supremacy/Kids%20Tv/Kids%20Tv.txt',1101,SUPREM_ICON,'','','')
	process.Menu('Brettus Anime','',1600,BRETTUS_ICON,FANART,'','')

	

def Music_Men():
	process.Menu('Search','',1503,'','','','')
	from lib.pyramid import pyramid
	#process.Menu('Quicksilver Music','',1133,QUICK_ICON,'','','')
	#process.Menu('Rays Ravers','',1147,RAY_ICON,'','','')
	pyramid.not_so_anon('Fido Live Music','[QT][LW][PD][QZ][WI][PD][AL][DE][SS][MW][FU][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YO][BU][PD][OI][MW][UP][YZ][LW][YO][LS][XU][WX][PD][LS][LS][XU][QZ][YZ]M[UR][UP][YO][RJ][YZ]M[UR][UP][YO][RJ]Hope you enjoy the view',FIDO_ICON,FANART,'','','')
	#process.Menu('Tigen\'s World','',1143,TIGEN_ICON,FANART,'','')
	pyramid.not_so_anon('Pyramid\'s Music','[QT][WI][XU][BU][ID][SS][PD][YO][LS][MW][SS][ID][UR][YO][JJ][LS][UP][WX][RJ][XU][WX][UR][YY][YZ][PD][LS][LS][XU][QZ][YZ][BU][UR][UP][YO][RJ][YZ][BU][UR][UP][YO][RJ]Have a nice day now',RAIDER_ICON,FANART,'','','')
	#process.Menu('Pandora\'s Music','http://genietvcunts.co.uk/PansBox/ORIGINS/seasonmusic.php',423,PANDORA_ICON,'','','')
	process.Menu('BAMF\'s Music','http://genietvcunts.co.uk/bamffff/bamfsmusic.xml',1101,BAMF_ICON,'','','')

def classic_list():
		if ADDON.getSetting('Quantum')=='true':
			process.Menu('Quantum','',4,ORIGIN_ICON,FANART,'','')
		if ADDON.getSetting('apprentice')=='true':
                        process.Menu('Apprentice','',100010,app_icon,FANART,'','')
		#if ADDON.getSetting('Pandoras_Box')=='true':
			#process.Menu('Pandora\'s Box','',900,PANDORA_ICON,FANART,'','')
		if ADDON.getSetting('Pyramid')=='true':
			process.Menu('Pyramid','',1100,RAIDER_ICON,FANART,'','')
		if ADDON.getSetting('Freeview')=='true':
			process.Menu('FreeView - [COLORred]VPN required if you are outside UK[/COLOR]','',1200,FREEVIEW_ICON,FANART,'','')
		if ADDON.getSetting('Brettus_Anime')=='true':
			process.Menu('Brettus Anime','',1600,BRETTUS_ICON,FANART,'','')
		#if ADDON.getSetting('Oblivion')=='true':
		#	process.Menu('Oblivion IPTV','',1129,OBLIVION_ICON,FANART,'','')
		#if ADDON.getSetting("Tigen's_World")=='true':
			#process.Menu('Tigen\'s World','',1143,TIGEN_ICON,FANART,'','')
		if ADDON.getSetting('Supremacy')=='true':
			process.Menu('Supremacy','',1131,SUPREM_ICON,FANART,'','')
		if ADDON.getSetting('Renegades')=='true':
			process.Menu('Renegades Darts','',2150,RENEGADES_ICON,FANART,'','')
		if ADDON.getSetting('Just_For_Him')=='true':
			process.Menu('Just For Him','',1400,NINJA_ICON,FANART,'','')
		if ADDON.getSetting('BAMF')=='true':
			process.Menu('Back In Time','',1132,BAMF_ICON,FANART,'','')
		#if ADDON.getSetting('Quicksilver')=='true':
			#process.Menu('Quicksilver Music','',1133,QUICK_ICON,'','','')
		if ADDON.getSetting('Rays_Ravers')=='true':
			process.Menu('Rays Ravers','',1147,RAY_ICON,'','','')
		#if ADDON.getSetting('Silent_Hunter')=='true':
			#process.Menu('Silent Hunter','',1134,SILENT_ICON,'','','')
		if ADDON.getSetting('Dojo')=='true':
			process.Menu('Dojo Streams','http://herovision.x10host.com/dojo/main.php',2300,DOJO_ICON,'','','')
		#if ADDON.getSetting('Cerberus')=='true':
			#process.Menu('Cerberus','http://roguemedia.x10.mx/cerberus/add-on/mainmenu.php',2301,REAPER_ICON,'','','')
		#if ADDON.getSetting('Ultra')=='true':
			#process.Menu('Ultra IPTV','',1145,ULTRA_ICON,'','','')
		if ADDON.getSetting('Fido')=='true':
			process.Menu('Fido','',1146,FIDO_ICON,'','','')
		if ADDON.getSetting('Midnight')=='true':
			process.Menu('Midnight Society','',1156,MIDNIGHT_IMAGE,FANART,'','')
		if ADDON.getSetting('Deliverance')=='true':
			process.Menu('DELIVERANCE','',1139,'https://3.bp.blogspot.com/-mRS8HrApaaY/WOI17mTddmI/AAAAAAAAXBo/CaxwCX7o47QZxaV6W1Qeff39ZyQjYuI5wCLcB/s1600/Deliverance%2BKodi%2B17%2B1.png',FANART,'','')
		process.setView('movies', 'MAIN')
		

def bagotricks():
    if ADDON.getSetting('TV_Guide')=='true':
        process.Menu('TV Guide','',2200,ICON,FANART,'','')
    if ADDON.getSetting("Today's_Football")=='true':
        process.Menu('Today\'s Football','',1750,ICON,FANART,'','')
    if ADDON.getSetting('Latest_Episodes')=='true':
        process.Menu('Latest Episodes','',3,ICON,FANART,'','')
    if ADDON.getSetting('Recent_Movies')=='true':
        process.Menu('Recent Movies','',5,ICON,FANART,'','')
    if ADDON.getSetting('Favourites')=='true':
        process.Menu('Favourites','',10,base_icons + 'favs.png',FANART,'','')
    if ADDON.getSetting('Search')=='true':
        process.Menu('Search','',1500,base_icons + 'search.png',FANART,'','')
	
def DOJO_MAIN(url):
    OPEN = process.OPEN_URL(url)
    Regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(OPEN)
    for url,icon,desc,fanart,name in Regex:
        if 'php' in url:
            process.Menu(name,url,2300,icon,fanart,desc,'')
        else:
            process.Play(name,url,906,icon,fanart,desc,'')

    process.setView('tvshows', 'Media Info 3')			
		
def Reaper_Loop(url):
    OPEN = process.OPEN_URL(url)
    Regex = re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART><DESC>(.+?)</DESC>').findall(OPEN)
    for name,url,icon,fanart,desc in Regex:
        if 'Favourites' in name:
            pass
        elif 'Search' in name:
            pass
        elif 'php' in url:
            process.Menu(name,url,2301,icon,fanart,desc,'')
        else:
            process.Play(name,url,906,icon,fanart,desc,'')



def Latest_Episodes():
    #process.Menu('Pandora Latest Episodes','http://genietvcunts.co.uk/PansBox/ORIGINS/recenttv.php',426,ICON,FANART,'','')
    process.Menu('TV Schedule','http://www.tvmaze.com/calendar',6,ICON,FANART,'','')

def Recent_Movies():
    #process.Menu('Pandora Recent Movies','http://genietvcunts.co.uk/PansBox/ORIGINS/recentmovies.php',426,PANDORA_ICON,FANART,'','')
    process.Menu('Pyramid Recent Movies','http://pyramid.areshost6.seedr.io/pyramid/newreleases.txt',1101,RAIDER_ICON,FANART,'','')
    process.Menu('Supremacy Recent Movies','https://simplekore.com/wp-content/uploads/file-manager/steboy11/New%20Releases/New%20Releases.txt',1101,SUPREM_ICON,FANART,'','')


def TV_Calender_Day(url):
	from datetime import datetime
	today = datetime.now().strftime("%d")
	this_month = datetime.now().strftime("%m")
	this_year = datetime.now().strftime("%y")
	todays_number = (int(this_year)*100)+(int(this_month)*31)+(int(today))
	HTML = process.OPEN_URL(url)
	match = re.compile('<span class="dayofmonth">.+?<span class=".+?">(.+?)</span>(.+?)</span>(.+?)</div>',re.DOTALL).findall(HTML)
	for Day_Month,Date,Block in match:
		Date = Date.replace('\n','').replace('  ','').replace('	','')
		Day_Month = Day_Month.replace('\n','').replace('  ','').replace('	','')
		Final_Name = Day_Month.replace(',',' '+Date+' ')
		split_month = Day_Month+'>'
		Month_split = re.compile(', (.+?)>').findall(str(split_month))
		for item in Month_split:
			month_one = item.replace('January','1').replace('February','2').replace('March','3').replace('April','4').replace('May','5').replace('June','6')
			month = month_one.replace('July','7').replace('August','8').replace('September','9').replace('October','10').replace('November','11').replace('December','12')
		show_day = Date.replace('st','').replace('th','').replace('nd','').replace('rd','')
		shows_number = (int(this_year)*100)+(int(month)*31)+(int(show_day))
		if shows_number>= todays_number:
			process.Menu('[COLORred]*'+'[COLORwhite]'+Final_Name+'[/COLOR]','',7,'','','',Block)
		else:
			process.Menu('[COLORgreen]*'+'[COLORwhite]'+Final_Name+'[/COLOR]','',7,'','','',Block)

def TV_Calender_Prog(extra):
	match = re.compile('<span class="show">.+?<a href=".+?">(.+?)</a>:.+?</span>.+?<a href=".+?" title=".+?">(.+?)</a>',re.DOTALL).findall(str(extra))
	for prog, ep in match:
		process.Menu(prog+' - Season '+ep.replace('x',' Episode '),'',8,'','','',prog)

def send_to_search(name,extra):
    if 'COLOR' in name:
        name = re.compile('- (.+?)>').findall(str(name)+'>')
        for name in name:
            name = name
    dp =  xbmcgui.DialogProgress()
    dp.create('Checking for stream')
    from lib import search
    search.TV(name)

#process.Menu(show_name+' - Season'+season+' Episode'+eps+' - '+year+' - '+imdb,'',100045,'','','',show_name)
'''
def send_to_search2(name,extra):
    dp =  xbmcgui.DialogProgress()
    dp.create('Checking for stream')
    from lib import search, Scrape_Nan
    Search_name = extra.lower().replace(' ','')
    name_splitter = name + '<>'
    name_split = re.compile('(.+?)- Season(.+?)- Episode(.+?)<>').findall(str(name_splitter))
    for name,season,episode,year,imdb in name_split:
        title = name.lower()
        tvdb = ''
        show_year = year
        Scrape_Nan.scrape_episode(title,'','',season,episode,'')
    #search.TV(Search_name)
'''
def send_to_movie_search(name,extra):
    from lib import Scrape_Nan
    if '(' in name:
        name_minus_year = re.compile('(.+?) \(').findall(str(name))
        for item in name:
            name = item
    dp =  xbmcgui.DialogProgress()
    dp.create('Checking for stream')
    year = extra.replace('/)','').replace('/(','')
    Scrape_Nan.scrape_movie(name,year)

def split_for_search(extra):
    from lib import Scrape_Nan
    splitter = re.compile('<(.+?)<(.+?)<').findall(str(extra))
    for name , year in splitter:
        year = year
        name = name
    
        Scrape_Nan;Scrape_Nan.scrape_movie(name,year,'')



def Origin_Main():
    process.Menu('Movies','',200,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('TV Shows','',300,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Sports Replays','',2100,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('Cartoons','',800,ORIGIN_ICON,ORIGIN_FANART,'','')
    process.Menu('AudioBooks','',600,ORIGIN_ICON,ORIGIN_FANART,'','')
    if Adult_Pass == Adult_Default:
        process.Menu('Porn','',707,ORIGIN_ICON,ORIGIN_FANART,'','')

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param

params=get_params()
title=None
show_year=None
season=None
episode=None
url=None
name=None
iconimage=None
mode=None
description=None
extra=None
fanart=None
fav_mode=None
regexs=None
playlist=None

try:
    title=urllib.unquote_plus(params["title"])
except:
    pass
try:
    show_year=urllib.unquote_plus(params["show_year"])
except:
    pass
try:
    season=urllib.unquote_plus(params["season"])
except:
    pass
try:
    episode=urllib.unquote_plus(params["episode"])
except:
    pass
try:
    regexs=params["regexs"]
except:
    pass

try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
    extra=urllib.unquote_plus(params["extra"])
except:
    pass
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:
    playitem=urllib.unquote_plus(params["playitem"])
except:
    pass
try:
    playlist=eval(urllib.unquote_plus(params["playlist"]).replace('||',','))
except:
    pass
try:
    regexs=params["regexs"]
except:
    pass


if mode == None: Main_Menu()
elif mode == 1 : process.queueItem()
elif mode == 2 : Music()
elif mode == 3 : Latest_Episodes()
elif mode == 4 : Origin_Main()
elif mode == 5 : Recent_Movies()
elif mode == 6 : TV_Calender_Day(url)
elif mode == 7 : TV_Calender_Prog(extra)
elif mode == 8 : send_to_search(name,extra)
elif mode == 10: from lib import process;process.getFavourites()
elif mode==11:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    process.addFavorite(name, url, fav_mode, iconimage, fanart, description, extra)
elif mode==12:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    process.rmFavorite(name)
elif mode == 13: bagotricks()
elif mode == 19: from lib import Live;Live.Live_Menu()
elif mode == 20: from lib import Live;Live.Live_Main()
elif mode == 21: from lib import Live;Live.Get_Channel(url)
elif mode == 22: from lib import Live;Live.Get_Playlink(name,url)
elif mode == 23: from lib import Live;Live.Ultra()
elif mode == 24: from lib import Live;Live.Get_Ultra_Channel(url)
elif mode == 25: from lib import Live;Live.Search_Ultra()
elif mode == 26: from lib import Live;Live.Check_For_200_Response()
elif mode == 27: from lib import Live;Live.search_checked()
elif mode == 30: Movie_Men()
elif mode == 31: TV_Men()
elif mode == 32: Live_Men()
elif mode == 33: Kids_Men()
elif mode == 34: Music_Men()
elif mode == 35: classic_list()
elif mode == 36: Movie_Def(url)
elif mode == 37: Adult()
elif mode == 38: twenty47()
elif mode == 39: docs()
elif mode == 40: sports()
elif mode == 41: process.check_for_episode()
elif mode == 100: from lib import comedy;comedy.Comedy_Main()
elif mode == 101: from lib import comedy;comedy.Stand_up()
elif mode == 102: from lib import comedy;comedy.Search()
elif mode == 103: from lib import comedy;comedy.Play_Stage(url)
elif mode == 104: from lib import comedy;comedy.Regex(url)
elif mode == 105: process.Resolve(url)
elif mode == 106: from lib import comedy;comedy.Stand_up_Menu()
elif mode == 107: from lib import comedy;comedy.grab_youtube_playlist(url)
elif mode == 108: from lib import comedy;comedy.Search()
elif mode == 109: from lib import yt;yt.PlayVideo(url)
elif mode == 110: from lib import comedy;comedy.Movies_Menu()
elif mode == 111: from lib import comedy;comedy.Pubfilm_Comedy_Grab(url)
elif mode == 112: from lib import comedy;comedy.Grab_Season(iconimage,url)
elif mode == 113: from lib import comedy;comedy.Grab_Episode(url,name,fanart,iconimage)
elif mode == 114: from lib import comedy;comedy.Get_Sources(name,url,iconimage,fanart)
elif mode == 115: from lib import comedy;comedy.Get_site_link(url,name)
elif mode == 116: from lib import comedy;comedy.final(url)
elif mode == 200: from lib import Movies;Movies.Movie_Main(url)
elif mode == 202 : from lib import Movies;Movies.Movie_Genre(url)
elif mode == 203 : from lib import Movies;Movies.IMDB_Grab(url)
elif mode == 204 : from lib import Movies;Movies.Check_Link(name,url,image)
elif mode == 205 : from lib import Movies;Movies.Get_playlink(url)
elif mode == 206 : from lib import Movies;Movies.IMDB_Top250(url)
elif mode == 207 : from lib import Movies;Movies.search_movies()
elif mode == 208 : from lib import Movies;Movies.movie_channels()
elif mode == 209 : from lib import Movies;Movies.split_for_search(extra)
elif mode == 300 : from lib import multitv;multitv.multiv_Main_Menu(url)
elif mode == 301 : from lib import multitv;multitv.IMDB_TOP_100_EPS(url)
elif mode == 302 : from lib import multitv;multitv.Popular(url)
elif mode == 303 : from lib import multitv;multitv.Genres()
elif mode == 304 : from lib import multitv;multitv.Genres_Page(url)
elif mode == 305 : from lib import multitv;multitv.IMDB_Get_Season_info(url,iconimage,extra)
elif mode == 306 : from lib import multitv;multitv.IMDB_Get_Episode_info(url,extra)
elif mode == 307 : from lib import multitv;multitv.SPLIT(extra)
elif mode == 308 : from lib import multitv;multitv.Search_TV()
elif mode == 400: from lib import Football_Repeat;Football_Repeat.footy_Main_Menu()
elif mode == 401: from lib import Football_Repeat;Football_Repeat.get_All_Rows(url,iconimage)
elif mode == 402: from lib import Football_Repeat;Football_Repeat.get_PLAYlink(name,url)
elif mode == 403: from lib import Football_Repeat;Football_Repeat.Football_Highlights()
elif mode == 404: from lib import Football_Repeat;Football_Repeat.FootballFixturesDay()
elif mode == 405: from lib import Football_Repeat;Football_Repeat.FootballFixturesGame(url,iconimage)
elif mode == 406: from lib import Football_Repeat;Football_Repeat.Prem_Table(url,extra)
elif mode == 407: from lib import Football_Repeat;Football_Repeat.get_Multi_Links(url,iconimage)
elif mode == 408: from lib import Football_Repeat;Football_Repeat.Get_the_rows(url,iconimage)
elif mode == 409: from lib import Football_Repeat;Football_Repeat.League_Tables(url)
elif mode == 410: from lib import Football_Repeat;Football_Repeat.Search()
elif mode == 411: from lib import Football_Repeat;Football_Repeat.Prem_Table2(url)
elif mode == 412: from lib import Football_Repeat;Football_Repeat.champ_league(url)
elif mode == 413: from lib import Football_Repeat;Football_Repeat.footytube(url)
elif mode == 414: from lib import Football_Repeat;Football_Repeat.footytube_leagues(name)
elif mode == 415: from lib import Football_Repeat;Football_Repeat.footytube_teams(url)
elif mode == 416: from lib import Football_Repeat;Football_Repeat.footytube_videos(url)
elif mode == 417: from lib import Football_Repeat;Football_Repeat.footytube_frame(name,url)
elif mode == 418: from lib import Football_Repeat;Football_Repeat.get_origin_playlink(url,iconimage,FANART)
elif mode == 419: from lib import Football_Repeat;Football_Repeat.Resolve(url)
elif mode == 420: from lib import Football_Repeat;Football_Repeat.FootballFixturesSingle(description);
elif mode == 421: from lib import Football_Repeat;Football_Repeat.METALLIQ()
elif mode == 500: from lib import radio_gaga;radio_gaga.Radio_Country()
elif mode == 501: from lib import radio_gaga;radio_gaga.Radio(url)
elif mode == 502: process.Resolve(url)
elif mode == 600: from lib import Kodible;Kodible.Kodible_Main_Menu()
elif mode == 602: process.Resolve(url)
elif mode == 603: from lib import Kodible;Kodible.Kids_Audio()
elif mode == 604: from lib import Kodible;Kodible.Kids_Play(url)
elif mode == 605: from lib import Kodible;Kodible.Kids_Play_Multi(url)
elif mode == 606: from lib import Kodible;Kodible.Kids_Menu()
elif mode == 607: from lib import Kodible;Kodible.Kids_AZ()
elif mode == 608: from lib import Kodible;Kodible.Kids_AZ_Audio(url)
elif mode == 614: from lib import Kodible;Kodible.Search_Kids()
elif mode == 700: from lib import xxx_vids;xxx_vids.X_vid_Menu()
elif mode == 701: from lib import xxx_vids;xxx_vids.XNew_Videos(url)
elif mode == 702: from lib import xxx_vids;xxx_vids.XGenres(url)
elif mode == 703: from lib import xxx_vids;xxx_vids.XPornstars(url)
elif mode == 704: from lib import xxx_vids;xxx_vids.XSearch_X()
elif mode == 705: from lib import xxx_vids;xxx_vids.Xtags(url)
elif mode == 706: from lib import xxx_vids;xxx_vids.XPlayLink(url)
elif mode == 707: from lib import xxx_vids;xxx_vids.Porn_Menu()
elif mode == 708: from lib import xxx_vids;xxx_vids.Porn_Hub()
elif mode == 709: from lib import xxx_vids;xxx_vids.get_video_item(url)
elif mode == 710: from lib import xxx_vids;xxx_vids.get_cat_item(url)
elif mode == 711: from lib import xxx_vids;xxx_vids.get_pornhub_playlinks(url)
elif mode == 712: from lib import xxx_vids;xxx_vids.get_pornstar(url)
elif mode == 713: from lib import xxx_vids;xxx_vids.search_pornhub()
elif mode == 714: from lib import xxx_vids;xxx_vids.XHamster()
elif mode == 715: from lib import xxx_vids;xxx_vids.hamster_cats(url)
elif mode == 716: from lib import xxx_vids;xxx_vids.get_hamster_vid(url)
elif mode == 717: from lib import xxx_vids;xxx_vids.chaturbate_tags(url)
elif mode == 718: from lib import xxx_vids;xxx_vids.hamster_cats_split(name,url)
elif mode == 719: from lib import xxx_vids;xxx_vids.get_hamster_playlinks(url)
elif mode == 720: from lib import xxx_vids;xxx_vids.chaturbate()
elif mode == 721: from lib import xxx_vids;xxx_vids.chaturbate_videos(url)
elif mode == 722: from lib import xxx_vids;xxx_vids.chaturbate_playlink(url)
elif mode == 723: from lib import xxx_vids;xxx_vids.YouPorn()
elif mode == 724: from lib import xxx_vids;xxx_vids.youporn_new_video(url)
elif mode == 725: from lib import xxx_vids;xxx_vids.youporn_video(url)
elif mode == 726: from lib import xxx_vids;xxx_vids.youporn_collections(url)
elif mode == 727: from lib import xxx_vids;xxx_vids.youporn_categories(url)
elif mode == 728: from lib import xxx_vids;xxx_vids.youporn_playlink(url)
elif mode == 729: from lib import xxx_vids;xxx_vids.search_youporn(url)
elif mode == 730: from lib import xxx_vids;xxx_vids.redtube()
elif mode == 731: from lib import xxx_vids;xxx_vids.redtube_video(url)
elif mode == 732: from lib import xxx_vids;xxx_vids.redtube_playlink(url)
elif mode == 733: from lib import xxx_vids;xxx_vids.redtube_channels(url)
elif mode == 734: from lib import xxx_vids;xxx_vids.redtube_pornstars(url)
elif mode == 735: from lib import xxx_vids;xxx_vids.redtube_collections(url)
elif mode == 736: from lib import xxx_vids;xxx_vids.redtube_cats(url)
elif mode == 737: from lib import xxx_vids;xxx_vids.redtube_search(url)
elif mode == 738: from lib import xxx_vids;xxx_vids.tube8()
elif mode == 739: from lib import xxx_vids;xxx_vids.tube8_videos(url)
elif mode == 740: from lib import xxx_vids;xxx_vids.tube8_playlink(url)
elif mode == 741: from lib import xxx_vids;xxx_vids.tube8_cats(url)
elif mode == 742: from lib import xxx_vids;xxx_vids.tube8_tags(url)
elif mode == 743: from lib import xxx_vids;xxx_vids.tube8_search()
elif mode == 744: from lib import xxx_vids;xxx_vids.tube8_letters(name,url)
elif mode == 745: from lib import xxx_vids;xxx_vids.thumbzilla()
elif mode == 746: from lib import xxx_vids;xxx_vids.thumbzilla_videos(url)
elif mode == 747: from lib import xxx_vids;xxx_vids.thumbzilla_tags(url)
elif mode == 748: from lib import xxx_vids;xxx_vids.thumbzilla_pornstars(url)
elif mode == 749: from lib import xxx_vids;xxx_vids.thumbzilla_cats(url)
elif mode == 750: from lib import xxx_vids;xxx_vids.thumbzilla_search()
elif mode == 751: from lib import xxx_vids;xxx_vids.thumbzilla_tags_letters(name,url)
elif mode == 752: from lib import xxx_vids;xxx_vids.thumbzilla_playlink(url)
elif mode == 753: from lib import xxx_vids;xxx_vids.xtube()
elif mode == 754: from lib import xxx_vids;xxx_vids.xtube_videos(url)
elif mode == 755: from lib import xxx_vids;xxx_vids.xtube_cats(url)
elif mode == 756: from lib import xxx_vids;xxx_vids.xtube_search(url)
elif mode == 757: from lib import xxx_vids;xxx_vids.xtube_playlink(url)
elif mode == 758: from lib import xxx_vids;xxx_vids.fourK()
elif mode == 759: from lib import xxx_vids;xxx_vids.eporner_playlink(url)
elif mode == 760: from lib import xxx_vids;xxx_vids.eporner()
elif mode == 761: from lib import xxx_vids;xxx_vids.eporner_video(url)
elif mode == 762: from lib import xxx_vids;xxx_vids.eporner_pornstar(url)
elif mode == 763: from lib import xxx_vids;xxx_vids.eporner_cats(url)
elif mode == 764: from lib import xxx_vids;xxx_vids.eporner_search()
elif mode == 765: from lib import xxx_vids;xxx_vids.youjizz_videos(url)
elif mode == 766: from lib import xxx_vids;xxx_vids.youjizz_tags(url)
elif mode == 767: from lib import xxx_vids;xxx_vids.youjizz_pornstars(url)
elif mode == 768: from lib import xxx_vids;xxx_vids.youjizz_search()
elif mode == 769: from lib import xxx_vids;xxx_vids.youjizz_playlink(url)
elif mode == 770: from lib import xxx_vids;xxx_vids.youjizz_tags_letters(name,url)
elif mode == 771: from lib import xxx_vids;xxx_vids.youjizz()
elif mode == 772: from lib import xxx_vids;xxx_vids.spank_wire()
elif mode == 773: from lib import xxx_vids;xxx_vids.spank_cats(url)
elif mode == 774: from lib import xxx_vids;xxx_vids.spank_tags(url)
elif mode == 775: from lib import xxx_vids;xxx_vids.spank_videos(url)
elif mode == 776: from lib import xxx_vids;xxx_vids.spank_search()
elif mode == 777: from lib import xxx_vids;xxx_vids.spank_playlink(url)
elif mode == 778: from lib import xxx_vids;xxx_vids.spank_tags_letter(name,url)
elif mode == 800: from lib import Big_Kids;Big_Kids.Big_Kids_Main_Menu()
elif mode == 801: from lib import Big_Kids;Big_Kids.TESTCATS()
elif mode == 802: from lib import Big_Kids;Big_Kids.Search_cartoons()
elif mode == 803: from lib import Big_Kids;Big_Kids.LISTS(url)
elif mode == 804: from lib import Big_Kids;Big_Kids.LISTS2(url,iconimage)
elif mode == 805: process.Resolve(url)
elif mode == 806: from lib import Big_Kids;Big_Kids.watch_cartoon_menu()
elif mode == 807: from lib import Big_Kids;Big_Kids.watch_cartoon_grab_episode(url)
elif mode == 808: from lib import Big_Kids;Big_Kids.watch_cartoon_final(url)
elif mode == 809: from lib import Big_Kids;Big_Kids.watch_cartoon_grab_movies(url)
elif mode == 810: from lib import Big_Kids;Big_Kids.watch_cartoon_grab_episode_second(url)
elif mode == 811: from lib import Big_Kids;Big_Kids.Search_movies()
elif mode == 812: from lib import Big_Kids;Big_Kids.Random_Lists()
elif mode == 813: from lib import Big_Kids;Big_Kids.Random_Cartoon(url)
elif mode == 814: from lib import Big_Kids;Big_Kids.Random_Movie(url)
elif mode == 816: from lib import Big_Kids;Big_Kids.Random_Play_Cartoon(url,name)
elif mode == 817: from lib import Big_Kids;Big_Kids.twenty47_select()
elif mode == 818: from lib import Big_Kids;Big_Kids.Search_247()
elif mode == 900: from lib import Pandora;Pandora.Pandora_Main()
elif mode == 901: from lib import Pandora;Pandora.Pandoras_Box(url)
elif mode == 902: from lib import Pandora;Pandora.open_normal(name,url,iconimage,fanart,description)
elif mode == 423: from lib import Pandora;Pandora.open_Menu(url)
elif mode == 426: from lib import Pandora;Pandora.Pandora_Menu(url)
elif mode == 903: from lib import Pandora;Pandora.Search_Menu()
elif mode == 904: from lib import Pandora;Pandora.Search_Pandoras_Films()
elif mode == 905: from lib import Pandora;Pandora.Search_Pandoras_TV()
elif mode == 906: process.Big_Resolve(name,url)
elif mode == 907: from lib import Pandora;Pandora.Pans_Resolve(name,url)
elif mode == 1100: from lib.pyramid import pyramid;pyramid.SKindex();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1101:from lib.pyramid import pyramid;pyramid.getData(url,fanart);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1102:from lib.pyramid import pyramid;pyramid.getChannelItems(name,url,fanart);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1103:from lib.pyramid import pyramid;pyramid.getSubChannelItems(name,url,fanart);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1104:from lib.pyramid import pyramid;pyramid.getFavorites();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1105:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    from lib.pyramid import pyramid;pyramid.addFavorite(name,url,iconimage,fanart,fav_mode)
elif mode==1106:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    from lib.pyramid import pyramid;pyramid.rmFavorite(name)
elif mode==1107:from lib.pyramid import pyramid;pyramid.addSource(url)
elif mode==1108:from lib.pyramid import pyramid;pyramid.rmSource(name)
elif mode==1109:from lib.pyramid import pyramid;pyramid.download_file(name, url)
elif mode==1110:from lib.pyramid import pyramid;pyramid.getCommunitySources()
elif mode==1111:from lib.pyramid import pyramid;pyramid.addSource(url)
elif mode==1112:
    from lib.pyramid import pyramid
    if 'google' in url:
        import urlresolver
        resolved = urlresolver.resolve(url)
        item = xbmcgui.ListItem(path=resolved)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    elif not url.startswith("plugin://plugin") or not any(x in url for x in pyramid.g_ignoreSetResolved):#not url.startswith("plugin://plugin.video.f4mTester") :
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    else:
        print 'Not setting setResolvedUrl'
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
elif mode==1113:from lib.pyramid import pyramid;pyramid.play_playlist(name, playlist)
elif mode==1114:from lib.pyramid import pyramid;pyramid.get_xml_database(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1115:from lib.pyramid import pyramid;pyramid.get_xml_database(url, True);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1116:from lib.pyramid import pyramid;pyramid.getCommunitySources(True);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1117:
    url,setresolved = getRegexParsed(regexs, url)
    if url:
        from lib.pyramid import pyramid;pyramid.playsetresolved(url,name,iconimage,setresolved)
    else:
        xbmc.executebuiltin("XBMC.Notification(ThePyramid ,Failed to extract regex. - "+"this"+",4000,"+icon+")")
elif mode==1118:
    try:
        from lib.pyramid import youtubedl
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(ThePyramid,Please [COLOR yellow]install the Youtube Addon[/COLOR] module ,10000,"")")
    stream_url=youtubedl.single_YD(url)
    from lib.pyramid import pyramid;pyramid.playsetresolved(stream_url,name,iconimage)
elif mode==1119:from lib.pyramid import pyramid;pyramid.playsetresolved (pyramid.urlsolver(url),name,iconimage,True)
elif mode==1121:from lib.pyramid import pyramid;pyramid.ytdl_download('',name,'video')
elif mode==1123:from lib.pyramid import pyramid;pyramid.ytdl_download(url,name,'video')
elif mode==1124:from lib.pyramid import pyramid;pyramid.ytdl_download(url,name,'audio')
elif mode==1125:from lib.pyramid import pyramid;pyramid.search(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1126:
    name = name.split(':')
    from lib.pyramid import pyramid;pyramid.search(url,search_term=name[1])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1127:
    from lib.pyramid import pyramid;pyramid.pulsarIMDB=search(url)
    xbmc.Player().play(pulsarIMDB)
elif mode == 1128: from lib.pyramid import pyramid;pyramid.SKindex_Joker();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1129: from lib.pyramid import pyramid;pyramid.SKindex_Oblivion();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1130: from lib.pyramid import pyramid;pyramid.GetSublinks(name,url,iconimage,fanart)
elif mode == 1131: from lib.pyramid import pyramid;pyramid.SKindex_Supremacy();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1132: from lib.pyramid import pyramid;pyramid.SKindex_BAMF();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1133: from lib.pyramid import pyramid;pyramid.SKindex_Quicksilver();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1134: from lib.pyramid import pyramid;pyramid.SKindex_Silent();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1135: from lib.pyramid import pyramid;pyramid.WizHDMenu(url,iconimage,fanart);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1136: from lib.pyramid import pyramid;pyramid.Wiz_Get_url(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1137: from lib.pyramid import pyramid;pyramid.scrape();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1138: from lib.pyramid import pyramid;pyramid.scrape_link(name,url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1139: from lib.pyramid import pyramid;pyramid.SKindex_deliverance();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1140: from lib.pyramid import pyramid;pyramid.SearchChannels();pyramid.SetViewThumbnail();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1141: from lib.pyramid import pyramid;pyramid.Search_input(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1142: from lib.pyramid import pyramid;pyramid.RESOLVE(url)
elif mode == 1143: from lib.pyramid import pyramid;pyramid.SKindex_TigensWorld();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1144: from lib.pyramid import pyramid;pyramid.queueItem();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1145: from lib.pyramid import pyramid;pyramid.SKindex_Ultra();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1146: from lib.pyramid import pyramid;pyramid.SKindex_Fido();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1147: from lib.pyramid import pyramid;pyramid.SKindex_Rays();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1153: from lib.pyramid import pyramid;pyramid.pluginquerybyJSON(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1154: from lib.pyramid import pyramid;pyramid.get_random(url);xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1156: from lib.pyramid import pyramid;pyramid.SKindex_Midnight();xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode == 1200: from lib.freeview import freeview;freeview.CATEGORIES()
elif mode == 1201: from lib.freeview import freeview;freeview.play(url)
elif mode == 1202: from lib.freeview import freeview;freeview.tvplayer(url)
elif mode == 1400 : from lib import ninja;ninja.CATEGORIES()
elif mode == 1401 : from lib import ninja;ninja.VIDEOLIST(url)
elif mode == 1402 : from lib import ninja;ninja.PLAYVIDEO(url)
elif mode == 1500 : from lib import search;search.Search_Menu()
elif mode == 1501 : from lib import search;search.Search_Input(name,url,extra)
elif mode == 1502 : from lib import search;search.MUSIC(Search_name,url)
elif mode == 1503 : from lib import search;search.Music_Search()
elif mode == 1504 : from lib import search;search.Clear_Search(url)
elif mode == 1600 : from lib import brettus_anime;brettus_anime.GetList()
elif mode == 1601 : from lib import brettus_anime;brettus_anime.GetContent(url,iconimage)
elif mode == 1602 : from lib import brettus_anime;brettus_anime.PLAYLINK(url,iconimage)
elif mode == 1700 : from lib import Now_thats_what_i_call_music;Now_thats_what_i_call_music.Now_Thats_What_I_Call_Music()
elif mode == 1701 : from lib import Now_thats_what_i_call_music;Now_thats_what_i_call_music.Now_Loop(url,iconimage,fanart)
elif mode == 1702 : from lib import Now_thats_what_i_call_music;Now_thats_what_i_call_music.Now_Playlinks(url,iconimage,fanart)
elif mode == 1750 : from lib import todays_football;todays_football.Todays_Football_Menu()
elif mode == 1751 : from lib import todays_football;todays_football.Todays_Football()
elif mode == 1752 : from lib import todays_football;todays_football.Search_Channels_Mainstream(url)
elif mode == 1753 : from lib import todays_football;todays_football.Live_On_Sat()
elif mode == 1800 : from lib import cold_as_ice;cold_as_ice.Cold_Menu()
elif mode == 1801 : from lib import cold_as_ice;cold_as_ice.GetContent(url,iconimage)
elif mode == 1802 : from lib import cold_as_ice;cold_as_ice.PLAYLINK(name,url,iconimage)
elif mode == 2000 : from lib import index_regex;index_regex.Main_Loop(url)
elif mode == 2100 : from lib import Sports_Replays;Sports_Replays.Sports_Repeats()
elif mode == 2101 : from lib import Sports_Replays;Sports_Replays.Motor_Replays(url)
elif mode == 2102 : from lib import Sports_Replays;Sports_Replays.motor_name(url)
elif mode == 2103 : from lib import Sports_Replays;Sports_Replays.motor_race(extra)
elif mode == 2104 : from lib import Sports_Replays;Sports_Replays.motor_single(name,extra)
elif mode == 2105 : from lib import Sports_Replays;Sports_Replays.F1_Replays(url)
elif mode == 2106 : from lib import Sports_Replays;Sports_Replays.F1_page(url)
elif mode == 2107 : from lib import Sports_Replays;Sports_Replays.F1_items(url,iconimage)
elif mode == 2108 : from lib import Sports_Replays;Sports_Replays.F1_Playlink(url)
elif mode == 2150 : from lib import renegades;renegades.run()
#elif mode == 2151 : import plugintools;plugintools.add_item(mode,name,url,iconimage,fanart)
elif mode == 2200 : from lib import tv_guide;tv_guide.TV_GUIDE_MENU()
elif mode == 2201 : from lib import tv_guide;tv_guide.whatsoncat()
elif mode == 2202 : from lib import tv_guide;tv_guide.whatson(url)
elif mode == 2203 : from lib import tv_guide;tv_guide.search_split(extra)
elif mode == 2204 : from lib import tv_guide;tv_guide.TV_GUIDE_CO_UK_CATS()
elif mode == 2205 : from lib import tv_guide;tv_guide.tvguide_co_uk(url)
elif mode == 2206 : from lib import tv_guide;tv_guide.WhatsOnCOUK(url,extra)
elif mode == 2207 : from lib import tv_guide;tv_guide.Select_Type()
elif mode == 2300 : DOJO_MAIN(url)
elif mode == 2301 : Reaper_Loop(url)
elif mode == 2350 : google_index_search()
elif mode == 10000: from lib import youtube_regex;youtube_regex.Youtube_Grab_Playlist_Page(url)
elif mode == 10001: from lib import youtube_regex;youtube_regex.Youtube_Playlist_Grab(url)
elif mode == 10002: from lib import youtube_regex;youtube_regex.Youtube_Playlist_Grab_Duration(url)
elif mode == 10003: from lib import yt;yt.PlayVideo(url)
elif mode == 100010: from lib import apprentice;apprentice.dud_mov()
elif mode == 100011: from lib import apprentice;apprentice.recent_dud(url)
elif mode == 100012: from lib import apprentice;apprentice.dud_play(name,url)
elif mode == 100013: from lib import apprentice;apprentice.new_rel(url)
elif mode == 9110001: from lib import apprentice;apprentice.show_main(url)
elif mode == 9110002: from lib import apprentice;apprentice.get_eps(url,name,iconimage) 
elif mode == 9110003: send_to_search2(name,extra)  
elif mode == 9110005: from lib import apprentice;apprentice.movie_search(description,url)  
elif mode == 9110004: from lib import apprentice;apprentice.nantvsearch()
elif mode == 9110006: from lib import apprentice;apprentice.app_show_men()
elif mode == 9110007: from lib import apprentice;apprentice.mov_main(url,extra)
elif mode == 9110008: from lib import apprentice;apprentice.app_mov_men()
elif mode == 100035: livetest()
elif mode == 100036: mpop()
elif mode == 100037: dmain()
elif mode == 100038: tv_running()
elif mode == 100039: eps(name,url)
elif mode == 100060: from lib import Big_Kids;Big_Kids.ac247()
elif mode == 100041: process.Big_resolve2(name,url)
elif mode == 100042: from lib.nan import onlinemovies;onlinemovies.scrape_episode(title, show_year, season, episode)
elif mode == 100043: from lib.nan import dizi720;dizi720.scrape_episode(title, show_year, season, episode)
elif mode == 100044: from lib import onlinemovies;onlinemovies.scrape_episode(title, show_year, season, episode)
elif mode == 100045: send_to_search2(name,extra)
elif mode == 100046: split_for_search(extra)
elif mode == 100050: table()
elif mode == 100051: dizi_main()
elif mode == 100060: from lib import Big_Kids;Big_Kids.ac247()
elif mode == 100061: from lib import Big_Kids;Big_Kids.actvshows()
elif mode == 100062: from lib import Big_Kids;Big_Kids.actvmovies()
elif mode == 100063: from lib import Big_Kids;Big_Kids.actvcable()
elif mode == 100064: from lib import Big_Kids;Big_Kids.actvrand()
elif mode == 100065: from lib import Big_Kids;Big_Kids.arcontv()
elif mode == 100070: from lib import Movies;Movies.scrape_movie(url)
elif mode == 100071: from lib import Movies;Movies.movie_genre()
elif mode == 100072: from lib import Movies;Movies.scrape_movie_genre(url,name)
elif mode == 100073: from lib import Movies;Movies.scrape_year()
elif mode == 100074: from lib import Movies;Movies.scrape_movie_year(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
