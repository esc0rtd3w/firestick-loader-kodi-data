import sys, process
import urllib2,re,os,base64,xbmc,xbmcplugin,xbmcaddon,xbmcgui,urlparse,urllib
import urlresolver,yt
try:
    import json
except:
    import simplejson as json
from threading import Thread

BASE = 'http://www.couchtripper.com/forum2/page.php?page=3'
Sources = ['daclips','filehoot','allmyvideos','vidspot','vodlocker']
List = []
Global_list = []
Main_link = 'http://www.watchseriesgo.to/link/'
addon_handle = int(sys.argv[1])
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.quantum/')
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'

Main 		= 'http://www.watchseriesgo.to/'


def Comedy_Main():

    process.Menu('Stand Up','',106,ICON,FANART,'','')
    process.Menu('Tv Shows','http://herovision.x10host.com/GetUpStandUp/TV_Shows.php',104,ICON,FANART,'','')
    process.Menu('Movies','',110,ICON,FANART,'','')
    process.Menu('Search','',108,ICON,FANART,'','')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	
def Movies_Menu():
    process.Menu('Comedy Movies','http://www.pubfilm.biz/movies/comedy/',111,ICON,FANART,'','')
    process.Menu('Youtube Playlist Movies','http://herovision.x10host.com/GetUpStandUp/Movies.php',104,ICON,FANART,'','')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	
def Pubfilm_Comedy_Grab(url):
    HTML = process.OPEN_URL(url)
    match = re.compile('<a class="short-img" href="(.+?)" data-label=".+?">.+?<img src="(.+?)" height="317".+?title="(.+?)" />',re.DOTALL).findall(HTML)
    for url,img,name in match:
        image = 'http://www.pubfilm.biz' + img
        Next(name,url,image)
    Next_Page = re.compile('<a href="(.+?)">Next</a></span>').findall(HTML)
    for item in Next_Page:
        process.Menu('Next Page',item,111,ICON,FANART,'','')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	

def Next(name,url,image):
    HTML = process.OPEN_URL(url)
    match = re.compile('<iframe width="660" height="400" scrolling="no" frameborder="0" src="http://mystream.la/external/(.+?)" allowFullScreen></iframe>').findall(HTML)
    for end in match:
        url = 'http://mystream.la/external/'+end
        process.Play(name,url,116,image,FANART,'','')        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	

def final(url):
    HTML = process.OPEN_URL(url)
    match = re.compile('file:"(.+?)",label:"(.+?)"}').findall(HTML)
    for playlink,quality in match:
        process.Resolve(playlink)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	
def Stand_up_Menu():
    process.Menu('Youtube Playlists','http://herovision.x10host.com/GetUpStandUp/yt_standup_playlist.php',104,ICON,FANART,'','')
#    process.Menu('Couch Tripper','',101,ICON,FANART,'','')
    process.Menu('Stand up','http://herovision.x10host.com/GetUpStandUp/standup_playlist.php',104,ICON,FANART,'','')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	
	
def Regex(url):
    HTML = process.OPEN_URL(url)
    match = re.compile('<NAME="(.+?)"<URL="(.+?)"<MODE="(.+?)"<IMAGE="(.+?)"<FANART="(.+?)"<DESC="(.+?)"').findall(HTML)
    for name,url,mode,image,fanart,desc in match:
        if image == 'IMAGES':
            image = ICON
        if fanart == 'FANART':
            fanart = FANART
        if '.php' in url:
            process.Menu(name,url,104,image,fanart,desc,'')
        if mode == 'single':
            process.Play(name,url,109,image,fanart,desc,'')
        elif mode == 'playlist':
            process.Menu(name,url,107,image,fanart,desc,'')
        elif mode == 'watchseries':
            process.Menu(name,url,112,image,fanart,desc,name)
        elif mode == 'normal':
            process.Play(name,url,105,image,fanart,desc,'')
            
    	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);		
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	

def Search():
    Dialog = xbmcgui.Dialog()
    filename = ['Movies','yt_standup_playlist','TV_Shows']
    Search_Name = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM) 
    Search_Title = Search_Name.lower()
    for file_name in filename:
        Search_Url = 'http://herovision.x10host.com/GetUpStandUp/'+file_name+'.php'
        HTML = process.OPEN_URL(Search_Url)
        match = re.compile('<NAME="(.+?)"<URL="(.+?)"<MODE="(.+?)"<IMAGE="(.+?)"<FANART="(.+?)"<DESC="(.+?)"').findall(HTML)
        for name,url,mode,image,fanart,desc in match:
            if Search_Title in name.lower():
                if image == 'IMAGES':
                    image = ICON
                if fanart == 'FANART':
                    fanart = FANART
                if '.php' in url:
                    process.Menu(name,url,104,image,fanart,desc,'')
                if mode == 'single':
                    process.Play(name,url,109,image,fanart,desc,'')
                elif mode == 'playlist':
                    process.Menu(name,url,107,image,fanart,desc,'')
                elif mode == 'watchseries':
                    process.Menu(name,url,112,image,fanart,desc,name)
                elif mode == 'normal':
                    process.Play(name,url,105,image,fanart,desc,'')
            
    	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);		
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	
        
	
def grab_youtube_playlist(url):

    HTML = process.OPEN_URL(url)
    block_set = re.compile('<tr class="pl-video yt-uix-tile(.+?)</tr>',re.DOTALL).findall(HTML)
    for block in block_set:
        image = re.compile('data-thumb="(.+?)"').findall(str(block))
        for image in image:
            image = image
        name = re.compile('data-title="(.+?)"').findall(str(block))
        for name in name:
            if 'elete' in name:
                pass
            elif 'rivate Vid' in name:
                pass
            else:
    			name = (name).replace('&quot;','').replace('&#39;','\'').replace('&amp;','&')
        duration = re.compile('<div class="timestamp"><span aria-label=".+?">(.+?)</span>').findall(str(block))
        for duration in duration:
            duration = duration
        url = re.compile('data-video-ids="(.+?)"').findall(str(block))
        for url in url:
            url = url
        process.Play('[COLORred]'+str(duration)+'[/COLOR] : '+str(name),str(url),109,str(image),FANART,'','' )
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	


def Stand_up():
    HTML = process.OPEN_URL(BASE)
    Block = re.compile('<tr>.+?<td width=".+?" align=".+?">.+?<img border=".+?" src="..(.+?)" width=".+?" height=".+?"></td>.+?<td width=".+?" valign=".+?" align=".+?"><font size=".+?">(.+?)</font></td>.+?<td width=".+?">(.+?)</td>',re.DOTALL).findall(HTML)
    for img, comic, c in Block:
	find_URL = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(c)
        for url, name in find_URL:
            if 'tube' in url:
                url = (url).replace('http://www.youtube.com/watch?v=','')
                process.Play(url,url,109,'','','','')
            elif 'stage' in url:
				process.Play(comic + '   -   ' + name,(url).replace('" target="_blank',''),103,'http://couchtripper.com/'+img,FANART,'','')
            elif 'vee' in url:
                pass
			    

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);	
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	
###########################Watch series Grab##########################################

def Grab_Season(iconimage,url):
    image = ' '
    description = ' '
    fanart = ' '
    season = ' '
    OPEN = process.OPEN_URL(url)
    image = re.compile('<img src="(.+?)">').findall(OPEN)
    for image in image:
        image = image
    background = re.compile('style="background-image: url\((.+?)\)">').findall(OPEN)
    for fanart in background:
        fanart = fanart	
    match = re.compile('itemprop="season".+?href=".+?" href="(.+?)".+?aria-hidden=".+?"></i>.+?S(.+?)</span>',re.DOTALL).findall(OPEN)
    for url,season in match:
        season = 'S'+(season).replace('  ','').replace('\n','').replace('    ','').replace('	','')
        url = Main + url
        process.Menu((season).replace('  ',''),url,113,image,fanart,description,'')
        process.setView('Movies', 'INFO')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	
	
def Grab_Episode(url,name,fanart,iconimage):
    main_name = '' 
    season = name
    OPEN = process.OPEN_URL(url)
    image = iconimage
    match = re.compile('<li itemprop="episode".+?<meta itemprop="url" content="(.+?)">.+?<span class="" itemprop="name">(.+?)</span>.+?<span itemprop="datepublished">(.+?)</span></span>.+?</li>',re.DOTALL).findall(OPEN)
    for url,name,date in match:
        name = (name).replace('&nbsp;','-').replace('---',' - ').replace('&#039;','\'').replace('&amp;','&').replace('&quot;','"')
        url = Main+url
        date = date
        full_name = name+' - [COLORred]'+date+'[/COLOR]'
        process.Menu(full_name,url,114,image,fanart,'Aired : '+date,full_name)

def Get_Sources(name,URL,iconimage,fanart):
    HTML = process.OPEN_URL(URL)
    match = re.compile('<td>.+?<a href="/link/(.+?)".+?title="(.+?)"',re.DOTALL).findall(HTML)
    for url,name in match:
        for item in Sources:
            if item in url:
                URL = Main_link + url
                List.append(name)
                selector(name,URL)
    if len(match)<=0:
        process.Menu('[COLORred]NO STREAMS AVAILABLE[/COLOR]','','','','','','')

def selector(name, URL):
    qty_check = List.count(name)
    if str(qty_check)>1:
        name = name + ' - Link '+ str(qty_check)
        process.Play(name,URL,115,ICON,FANART,'','')
    else:
        process.Play(name,URL,115,ICON,FANART,'','')
    
		
def Get_site_link(url,name):
    season_name = name
    HTML = process.OPEN_URL(url)
    match = re.compile('<iframe style=.+?" src="(.+?)"').findall(HTML)
    match2 = re.compile('<IFRAME SRC="(.+?)"').findall(HTML)
    match3 = re.compile('<IFRAME style=".+?" SRC="(.+?)"').findall(HTML)
    for url in match:
        main(url,season_name)
    for url in match2:
        main(url,season_name)
    for url in match3:
        main(url,season_name)

def main(url,season_name):
    if 'daclips.in' in url:
        daclips(url,season_name)
    elif 'filehoot.com' in url:
        filehoot(url,season_name)
    elif 'allmyvideos.net' in url:
        allmyvid(url,season_name)
    elif 'vidspot.net' in url:
        vidspot(url,season_name)
    elif 'vodlocker' in url:
        vodlocker(url,season_name)	
    elif 'vidto' in url:
        vidto(url,season_name)	


def vidto(url,season_name):
    HTML = process.OPEN_URL(url)
    match = re.compile('"file" : "(.+?)",\n.+?"default" : .+?,\n.+?"label" : "(.+?)"',re.DOTALL).findall(HTML)
    for Link,name in match:
        Printer(Link,season_name)

												
def allmyvid(url,season_name):
    HTML = process.OPEN_URL(url)
    match = re.compile('"file" : "(.+?)",\n.+?"default" : .+?,\n.+?"label" : "(.+?)"',re.DOTALL).findall(HTML)
    for Link,name in match:
        Printer(Link,season_name)

def vidspot(url,season_name):
    HTML = process.OPEN_URL(url)
    match = re.compile('"file" : "(.+?)",\n.+?"default" : .+?,\n.+?"label" : "(.+?)"').findall(HTML)
    for Link,name in match:
        Printer(Link,season_name)

def vodlocker(url,season_name):
    HTML = process.OPEN_URL(url)
    match = re.compile('file: "(.+?)",.+?skin',re.DOTALL).findall(HTML)
    for Link in match:
        Printer(Link,season_name)

def daclips(url,season_name):
    HTML = process.OPEN_URL(url)
    match = re.compile('{ file: "(.+?)", type:"video" }').findall(HTML)
    for Link in match:
        Printer(Link,season_name)

def filehoot(url,season_name):
    HTML = process.OPEN_URL(url)
    match = re.compile('file: "(.+?)",.+?skin',re.DOTALL).findall(HTML)
    for Link in match:
        Printer(Link,season_name)

def Printer(Link,season_name):
    if 'http:/' in Link:
        process.Resolve(Link)
###########################################Watch series end###########################################			
	
def Play_Stage(url):
    HTML = process.OPEN_URL(url)
    playlink = re.compile("url\[.+?\] = '(.+?)';").findall(HTML)
    for url in playlink:
        process.Resolve((url).replace('[','').replace(']','').replace('\'',''))

		
