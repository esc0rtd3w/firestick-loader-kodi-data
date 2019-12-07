import re, process, urllib, urllib2, xbmc, xbmcgui, base64, sys, xbmcplugin, threading, xbmcaddon, os, clean_name

freeview_py = xbmc.translatePath('special://home/addons/plugin.video.quantum/lib/freeview/freeview.py')
addon_id = 'plugin.video.quantum'
ADDON = xbmcaddon.Addon(id=addon_id)
Dialog = xbmcgui.Dialog()
dp =  xbmcgui.DialogProgress()
Decode = base64.decodestring
addon_handle = int(sys.argv[1])
Base_Pand = (Decode('aHR0cDovL2dlbmlldHZjdW50cy5jby51ay9QYW5zQm94L09SSUdJTlMv'))
watched_list = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.quantum/watched.txt')

def Search_Menu():
    process.Menu('All previous Searches','',1501,'','','','ALL')
    process.Menu('TV','TV',1501,'','','','')
    process.Menu('Movies','Movies',1501,'','','','')
    process.Menu('Live TV','Live TV',1501,'','','','')
    process.Menu('Music','Music',1501,'','','','')
    process.Menu('Cartoons','cartoon',1501,'','','','')
    process.Menu('Football Team','Football',1501,'','','','')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def Music_Search(Search_name):
    dp.create('Checking for streams')
    if ADDON.getSetting('Quicksilver')=='true':
        dp.update((100/2)*2,'',"Checking Quicksilver",'Please Wait')
        try:Thread(target=Quicksilver_search(Search_name,Search='Quick'))
        except:pass
    if ADDON.getSetting('Rays_Ravers')=='true':
        dp.update((100/2)*2,'',"Checking Rays Ravers",'Please Wait')
        try:Thread(target=Quicksilver_search(Search_name,Search='Rays'))
        except:pass
    dp.update(100,'',"Finished checking",'Please Wait')
    dp.close()
	
def Quicksilver_search(Search_name,Search = None):
	Quick_list = ['http://quicksilver-music.com/addoncore/Texts/Fresh.txt','http://quicksilver-music.com/addoncore/Texts/Popular.txt','http://quicksilver-music.com/addoncore/Texts/classicalbums.txt',
	'http://quicksilver-music.com/addoncore/Texts/compilations/compilationsmain.txt','http://quicksilver-music.com/addoncore/Texts/legends.txt','http://quicksilver-music.com/addoncore/Texts/Collection.txt',
	'http://quicksilver-music.com/addoncore/Texts/acousticmain.txt','http://quicksilver-music.com/addoncore/Texts/greatesthits.txt']
	Ray_List = ['http://raiztv.co.uk/RaysRavers/list2/dreamscape/main.txt','http://raiztv.co.uk/RaysRavers/list2/heleterskelter/helterskeltermain.txt',
	'http://raiztv.co.uk/RaysRavers/list2/htidnye.txt','http://raiztv.co.uk/RaysRavers/list2/bonkers.txt','http://raiztv.co.uk/RaysRavers/list2/clubland.txt',
	'http://raiztv.co.uk/RaysRavers/list2/mos/theannual.txt','http://raiztv.co.uk/RaysRavers/list2/mos.txt','http://raiztv.co.uk/RaysRavers/list2/hardhouse.txt',
	'http://raiztv.co.uk/RaysRavers/list2/hardcorecomp.txt','http://raiztv.co.uk/RaysRavers/list2/randomhardcoretracks.txt']
	if Search == 'Quick':
		for item in Quick_list:
			HTML = process.OPEN_URL(item)
			match = re.compile('<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>.+?<info>(.+?)</info>',re.DOTALL).findall(HTML)
			for name,image,url,fanart,desc in match:
				if (Search_name).lower().replace(' ','') in (name).replace(' ','').lower():
					from pyramid.pyramid import addDir
					addDir('Quicksilver | '+ name,url,1101,image,fanart,'','','','')
	if Search == 'Rays':
		for item in Ray_List:
			HTML = process.OPEN_URL(item)
			match = re.compile('<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>.+?<info>(.+?)</info>',re.DOTALL).findall(HTML)
			for name,image,url,fanart,desc in match:
				if (Search_name).lower().replace(' ','') in (name).replace(' ','').lower():
					from pyramid.pyramid import addDir
					addDir('Rays Ravers | '+ name,url,1101,image,fanart,'','','','')

    

def Search_Input(name,url,extra):
    if extra == 'NEW':
		Dialog = xbmcgui.Dialog()
		Search_title = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
		Search_name = Search_title.lower()
		if Search_name == '':
			pass
		else:
			xbmc.log('SEARCH NAME ='+Search_name+'    URL= '+url)
			write_to_file(Search_name,url)
			if url == 'TV':
				TV(Search_name)
			elif url == 'Movies':
				Movies(Search_name)
			elif url == 'Music':
				Music_Search(Search_name)
			elif url == 'cartoon':
				Cartoons(Search_name)
			elif url == 'Football':
				Football(Search_name)
			elif url == 'Live TV':
				Live_TV(Search_name)
			else:
				process.Menu('Search failed - '+url,'','','','','','')
    elif extra == 'OLD':
		Search_name = name
		if Search_name == '':
			pass
		else:
			if url == 'TV':
				TV(Search_name)
			elif url == 'Movies':
				Movies(Search_name)
			elif url == 'Music':
				Music_Search(Search_name)
			elif url == 'cartoon':
				Cartoons(Search_name)
			elif url == 'Football':
				Football(Search_name)
			elif url == 'Live TV':
				Live_TV(Search_name)
			else:
				process.Menu('Search failed - '+url,'','','','','','')
    elif extra == 'ALL':
		read_from_file('full')
    else:
		process.Menu('[COLOR darkgoldenrod][B]New Search[/B][/COLOR]',url,1501,'','','','NEW')
		read_from_file(url)
			
class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)
		
def Movies(Search_name):
    if '(' in Search_name:
		Search_name = re.compile('(.+?)\(').findall(str(Search_name))
		for thing in Search_name:
			Search_name = thing
    dp.create('Checking for streams')
    Silent_urls = ['http://silentstream.srve.io/silenthunter/main/4k.xml','http://silentstream.srve.io/silenthunter/main/2016.xml','http://silentstream.srve.io/silenthunter/main/disney.xml','http://silentstream.srve.io/silenthunter/main/pixar.xml','http://silentstream.srve.io/silenthunter/main/dreamworks.xml','http://silentstream.srve.io/silenthunter/main/boxsets.xml','http://silentstream.srve.io/silenthunter/main/FeelGood.xml']
    Raider_urls = ['http://tombraiderbuilds.co.uk/addon/movies/A-D/A-D.txt','http://tombraiderbuilds.co.uk/addon/movies/E-H/E-H.txt','http://tombraiderbuilds.co.uk/addon/movies/I-L/I-L.txt','http://tombraiderbuilds.co.uk/addon/movies/0-1000000/0-1000000.txt',
	'http://tombraiderbuilds.co.uk/addon/movies/M-P/M-P.txt','http://tombraiderbuilds.co.uk/addon/movies/Q-S/Q-S.txt','http://tombraiderbuilds.co.uk/addon/movies/T/T.txt','http://tombraiderbuilds.co.uk/addon/movies/U-Z/U-Z.txt']
    if ADDON.getSetting('Pandoras_Box_Search')=='true':
        dp.update(100/7,'',"Checking Pandoras Box",'Please Wait')
        Thread(target=Pans_Search_Movies(Search_name))
    if ADDON.getSetting("Tigen's_World_Search")=='true':
        dp.update((100/7)*2,'',"Checking Tigen\'s World",'Please Wait')
        Thread(target=Raider_Loop(Search_name,'MULTILINK-TIGEN'))
    if ADDON.getSetting('Pyramid_Search')=='true':
        for item in Raider_urls:
            dp.update((100/7)*3,'',"Checking Pyramid",'Please Wait')
            Thread(target=Raider_Loop(Search_name,item))
    if ADDON.getSetting('Silent_Hunter_Search')=='true':
        for item in Silent_urls:
            dp.update((100/7)*5,'',"Checking Silent Hunter",'Please Wait')
            Thread(target=Raider_Loop(Search_name,item))
    if ADDON.getSetting('Dojo_Search')=='true':
        dp.update((100/7)*6,'',"Checking Dojo",'Please Wait')
        Thread(target=Dojo(Search_name,'http://herovision.x10host.com/dojo/dojo.php'))
    if ADDON.getSetting('Reaper_Search')=='true':
        dp.update((100/7)*7,'',"Checking Reaper",'Please Wait')
        Thread(target=Reaper(Search_name,'http://cerberus.x10.bz/add-on/mov/atoz.php'))
    dp.update(100,'',"Finished checking",'Enjoy')
    dp.close()
	
def Reaper(Search_name,url):
    OPEN = process.OPEN_URL(url)
    Regex = re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART><DESC>(.+?)</DESC>').findall(OPEN)
    for name,url,icon,fanart,desc in Regex:
        if (Search_name).replace(' ','') in (name).replace(' ','').lower():
            if 'php' in url:
                process.Menu('[COLORlightslategray]Reaper[/COLOR] '+name,url,2301,icon,fanart,desc,'')
            else:
                process.Play('[COLORlightslategray]Reaper[/COLOR] '+name,url,906,icon,fanart,desc,'')

def Reaper_TV(Search_name,url):
	if 'season' in Search_name.lower():
		Type = 'single_ep'
		name_splitter = Search_name + '<>'
		name_split = re.compile('(.+?) - season (.+?) episode (.+?)<>').findall(str(name_splitter.lower()))
		for name,season,episode in name_split:
			title = name
			season = season
			episode = episode
		year = ''
	else:
		title = Search_name
		Type = 'full_show'
	OPEN = process.OPEN_URL(url+title[0].upper()+'.php')
	Regex = re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART><DESC>(.+?)</DESC>').findall(OPEN)
	for name,url2,icon,fanart,desc in Regex:
		if (title).replace(' ','').lower() in (name).replace(' ','').lower():
			if Type == 'full_show':
				if 'php' in url:
					process.Menu('[COLORlightslategray]Reaper[/COLOR] '+name,url,2301,icon,fanart,desc,'')
				else:
					process.Play('[COLORlightslategray]Reaper[/COLOR] '+name,url,906,icon,fanart,desc,'')
			elif Type == 'single_ep':
				HTML2 = process.OPEN_URL(url2)
				match = re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART><DESC>(.+?)</DESC>').findall(HTML2)
				for name2,url3,icon,fanart,desc in match:
					seas_no = re.compile('season (.+?)\.').findall(str(name2.lower()))
					for item in seas_no:
						seas_no = item
						if seas_no[0] == '0':
							seas_no = seas_no[1]
					if season == seas_no:
						HTML3 = process.OPEN_URL(url3)
						match2 = re.compile('<NAME>(.+?)</NAME><URL>(.+?)</URL><ICON>(.+?)</ICON><FANART>(.+?)</FANART><DESC>(.+?)</DESC>').findall(HTML3)
						for name3,url4,image,pic,info in match2:
							ep_no = re.compile('EP(.+?)\.').findall(str(name3))
							for item in ep_no:
								ep_no = item
							if episode == ep_no:
								process.Play('[COLORlightslategray]Reaper[/COLOR] | '+name3,url4,906,image,pic,info,'')
							
def Dojo(Search_name,url):
    OPEN = process.OPEN_URL(url)
    Regex = re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(OPEN)
    for url,icon,desc,fanart,name in Regex:
        if (Search_name).replace(' ','') in (name).replace(' ','').lower():
            if 'php' in url:
                process.Menu('[COLORred]Dojo Streams[/COLOR] '+name,url,2300,icon,fanart,desc,'')
            else:
                process.Play('[COLORred]Dojo Streams[/COLOR] '+name,url,906,icon,fanart,desc,'')

def write_to_file(Search_name,file_name):
	addon_data = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.quantum/')
	full_file = addon_data + 'full.txt'
	Stream_file = addon_data+file_name+'.txt'
	if not os.path.exists(Stream_file):
		print_text_file = open(Stream_file,"w")
		print_text_file.write('<NAME=>'+Search_name+'</NAME><URL=>'+file_name+'</URL>\n')
	else:
		print_text_file = open(Stream_file,"a")
		print_text_file.write('<NAME=>'+Search_name+'</NAME><URL=>'+file_name+'</URL>\n')
	if not os.path.exists(full_file):
		print_text_file = open(full_file,"w")
		print_text_file.write('<NAME=>'+Search_name+'</NAME><URL=>'+file_name+'</URL>\n')
	else:
		print_text_file = open(full_file,"a")
		print_text_file.write('<NAME=>'+Search_name+'</NAME><URL=>'+file_name+'</URL>\n')
	
def read_from_file(file_name):
	addon_data = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.quantum/')
	Stream_file = addon_data+file_name+'.txt'
	if not os.path.exists(Stream_file):
		print_text_file = open(Stream_file,"w")
	html = open(Stream_file).read()
	match = re.compile('<NAME=>(.+?)</NAME><URL=>(.+?)</URL>').findall(html)
	for result,type in match:
		process.Menu(result,type,1501,'','','','OLD')
	process.Menu('[COLORred][B]Clear previous search\'s[/B][/COLOR]',file_name,1504,'','','','')
	
def Clear_Search(file_name):
	addon_data = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.quantum/')
	Stream_file = addon_data+file_name+'.txt'
	if os.path.exists(Stream_file):
		print_text_file = open(Stream_file,"w")
	
def TV(Search_name):
    dp.create('Checking for streams')
    if 'season' in Search_name.lower():
        Type = 'single_ep'
        name_splitter = Search_name + '<>'
        name_split = re.compile('(.+?) - season (.+?) episode (.+?)<>').findall(str(name_splitter).lower())
        for name,season,episode in name_split:
            title = name
            season = season
            episode = episode
    else:
        title = Search_name
        season = ''
        episode = ''
    if ADDON.getSetting('Pandoras_Box_Search')=='true':
        dp.update((100/7),'',"Checking Pandoras Box",'Please Wait')
        try:Thread(target=Pans_Search_TV(Search_name))
        except:pass
    xbmc.log('<<<<<<<<'+Search_name)
    if ADDON.getSetting('Pyramid_Search')=='true':
        dp.update((100/7)*2,'',"Checking Pyramid",'Please Wait')
        try:Thread(target=Raider_TV(Search_name,'http://tombraiderbuilds.co.uk/addon/tvseries/tvzonemain.txt'))
        except:pass
    if ADDON.getSetting("Tigen's_World_Search")=='true':
        dp.update((100/7)*3,'',"Checking Tigen's World",'Please Wait')
        try:Thread(target=Raider_TV(Search_name,'http://kodeeresurrection.com/TigensWorldtxt/TvShows/Txts/OnDemandSub.txt'))
        except:pass
    if ADDON.getSetting('Dojo_Search')=='true':
        dp.update((100/7)*4,'',"Checking Dojo",'Please Wait')
        try:Thread(target=Dojo(title,'http://herovision.x10host.com/dojo/dojo.php'))
        except:pass
    if ADDON.getSetting('Reaper_Search')=='true':
        dp.update((100/7)*5,'',"Checking Reaper",'Please Wait')
        try:Thread(target=Reaper_TV(Search_name,'http://cerberus.x10.bz/add-on/tv/alpha/'))
        except:pass
    dp.update((100/7)*6,'',"Checking Origin",'Please Wait')
    Thread(target=animetoon_search(Search_name))
    process.rmWatched(title)
    process.Addwatched(title,season,episode)
    dp.update(100,'',"Finished checking",'Please Wait')
    dp.close()

def animetoon_search(Search_name):
	List = []
	if 'season' in Search_name.lower():
		Type = 'single_ep'
		name_splitter = Search_name + '<>'
		name_split = re.compile('(.+?) - season (.+?) episode (.+?)<>').findall(str(name_splitter).lower())
		for name,season,episode in name_split:
			title = name
			season = season
			episode = episode
		year = ''
		if season == '1':
			url = 'http://www.animetoon.org/' + title.replace(' ', '-').replace('!', '') + '-episode-' + episode
		elif season == '01':
			url = 'http://www.animetoon.org/' + title.replace(' ', '-').replace('!', '') + '-episode-' + episode
		else:
			url = 'http://www.animetoon.org/' + title.replace(' ','-').replace('!', '') +'-season-'+season+'-episode-'+episode
		html=process.OPEN_URL(url)
		match = re.compile('"playlist">.+?</span></div><div><iframe src="(.+?)"').findall(html)
		for url2 in match:
			if 'panda' in url2:
				HTML = process.OPEN_URL(url2)
				match2 = re.compile("url: '(.+?)'").findall(HTML)
				for url3 in match2:
					if 'http' in url3:
						if url3 not in List:
							process.Play('[COLORwhite]Origin[/COLOR] | Playpanda | '+title,url3,906,'','','','')
							List.append(url3)
			elif 'easy' in url2:
				HTML2 = process.OPEN_URL(url2)
				match3 = re.compile("url: '(.+?)'").findall(HTML2)
				for url3 in match3:
					if 'http' in url3:
						if url3 not in List:
							process.Play('[COLORwhite]Origin[/COLOR] | Easyvideo | '+title,url3,906,'','','','')
							List.append(url3)
			elif 'zoo' in url2:
				HTML3 = process.OPEN_URL(url2)
				match4 = re.compile("url: '(.+?)'").findall(HTML3)
				for url3 in match4:
					if 'http' in url3:
						if url3 not in List:
							process.Play('[COLORwhite]Origin[/COLOR] | Videozoo | '+title,url3,906,'','','','')
							List.append(url3)

	else:
		pass

	
def Cold_AS_Ice(Search_name):
	HTML = process.OPEN_URL('http://g10.x10host.com/coldasice/Boxsets/Index.txt')
	match= re.compile('<link>(.+?)</link><thumbnail>(.+?)</thumbnail><title>(.+?)</title>').findall(HTML)
	for url,image,name in match:
		if (Search_name).replace(' ','') in (name).replace(' ','').lower():
			name = '[COLORsteelblue]Cold As Ice [/COLOR]' + name
			if '/coldasice/' in url:
				process.Menu(name,url,1801,image,'','','')
			elif 'letwatch' in url:
				name = '[COLORred]*[/COLOR]'+name
				from freeview.freeview import addLink
				addLink(name,url,1802,iconimage)
			else:
				from freeview.freeview import addLink
				addLink(name,url,1802,iconimage)
		

def Search_GetUpStandUp(Search_name):
    filename = ['Movies','yt_standup_playlist','TV_Shows']
    for file_name in filename:
        Search_Url = 'http://herovision.x10host.com/GetUpStandUp/'+file_name+'.php'
        HTML = process.OPEN_URL(Search_Url)
        match = re.compile('<NAME="(.+?)"<URL="(.+?)"<MODE="(.+?)"<IMAGE="(.+?)"<FANART="(.+?)"<DESC="(.+?)"').findall(HTML)
        for name,url,mode,image,fanart,desc in match:
            if (Search_name).replace(' ','') in (name).replace(' ','').lower():
                name = '[COLORred]Origin [/COLOR]' + name
                if image == 'IMAGES':
                    image = ''
                if fanart == 'FANART':
                    fanart = ''
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

def Search_WatchSeries(Search_name):
    Search_url = 'http://www.watchseriesgo.to/search/' + (Search_name).replace(' ','%20')
    OPEN = process.OPEN_URL(Search_url)
    match3 = re.compile('<div class="block-left-home-inside col-sm-9 col-xs-12" title=".+?">.+?<a href="(.+?)" title=.+?<img src="(.+?)" alt=.+?<b>(.+?)</b></a><br>(.+?)<br>',re.DOTALL).findall(OPEN)
    for url,img,name,desc in match3:
        name = (name).replace('&nbsp;','-').replace('---',' - ').replace('&#039;','\'').replace('&amp;','&').replace('&quot;','"')
        url3 = 'http://www.watchseriesgo.to/' + url
        image = 'http://www.watchseriesgo.to/' + img
        fanart=''
        description = (desc).replace('<b>','').replace('</b>','').replace('&nbsp;','-').replace('---',' - ').replace('&#039;','\'').replace('&amp;','&').replace('&quot;','"').replace('Description: ','').replace('  ','')
        name = '[COLORred]Origin [/COLOR]' + name
        process.Menu(name,url3,305,image,fanart,description,name)		
	
	
				
def Pans_Search_Movies(Search_name):
	Pans_files_Movies = ['hey1080p','hey3D','hey','mov'+Search_name[0].lower()]
	for file_name in Pans_files_Movies:
		search_URL = Base_Pand + file_name + '.php'
		HTML = process.OPEN_URL(search_URL)
		if HTML != 'Opened':
			match=re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(HTML)
			for url,iconimage,desc,fanart,name in match:
				if Search_name.lower().replace(' ','') in (name).replace(' ','').lower():
					name = '[COLOR darkgoldenrod]Pandora [/COLOR]| ' + name
					process.Play(name,url,906,iconimage,fanart,desc,'')

def Pans_Search_TV (Search_name):
	if 'season' in Search_name.lower():
		Type = 'single_ep'
		name_splitter = Search_name + '<>'
		name_split = re.compile('(.+?) - season (.+?) episode (.+?)<>').findall(str(name_splitter).lower())
		for name,season,episode in name_split:
			title = name
			season = season
			episode = episode
		year = ''
	else:
		Type = 'full_show'
		title = Search_name
	if Search_name[0].lower() in 'abcdefghijklmnopqrstuvwxyz':
		url_extra = Search_name[0].lower()
	else:
		url_extra = 'tvnum'
	search_URL2 = Base_Pand + url_extra + '.php'
	HTML = process.OPEN_URL(search_URL2)
	if HTML != 'Opened':
		match = re.compile('<item>.+?<title>(.+?)</title>.+?<description>(.+?)</description>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)</fanart>.+?<mode>(.+?)</mode>.+?</item>',re.DOTALL).findall(HTML)
		for name,desc,url,img,fanart,mode in match:
			if Type == 'full_show':
				if (Search_name).replace(' ','') in (name).replace(' ','').lower():
					name = '[COLOR darkgoldenrod]Pandora [/COLOR]' + name
					process.Menu(name,url,mode,img,fanart,desc,'')
			elif Type == 'single_ep':
				if title.replace(' ','').lower() in name.replace(' ','').lower():
					HTML5 = process.OPEN_URL(url)
					match5=re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(HTML5)
					for url5,iconimage,desc5,background,name5 in match5:
						if len(episode) == 1:
							episode = '0'+episode
						if 'E'+episode in name5:
							process.PLAY('[COLOR darkgoldenrod]Pandora | [/COLOR]' + name5,url5,906,iconimage,background,desc5,'')
					HTML2 = process.OPEN_URL(url)
					match2 = re.compile('<item>.+?<title>(.+?)</title>.+?<description>(.+?)</description>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)</fanart>.+?<mode>(.+?)</mode>.+?</item>',re.DOTALL).findall(HTML2)
					for name2,desc2,url2,img2,fanart2,mode2 in match2:
						if 's' in name2.lower() and season in name2.lower():
							HTML3 = process.OPEN_URL(url2)
							match3=re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(HTML3)
							for url3,iconimage,desc3,background,name3 in match3:
								if len(episode) == 1:
									episode = '0'+episode
								if 'E'+episode in name3:
									process.PLAY('[COLOR darkgoldenrod]Pandora | [/COLOR]' + name3,url3,906,iconimage,background,desc3,'')
	if Type == 'single_ep':
		HTML4 = process.OPEN_URL(Base_Pand + 'recenttv.php')
		match4=re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" style="max-width:200px;" /><description = "(.+?)" /><background = "(.+?)" </background></a><br><b>(.+?)</b>').findall(HTML4)
		for url4,iconimage,desc4,background,name4 in match4:
			if len(episode) == 1:
				episode = '0'+episode
			if 'E'+episode in name4 and title.lower().replace(' ','') in name4.lower().replace(' ',''):
				process.PLAY('[COLOR darkgoldenrod]Pandora Recent | [/COLOR]' + name4,url4,906,iconimage,background,desc4,'')
			
def Cartoons(Search_name):
    HTML2 = process.OPEN_URL(Decode('aHR0cDovL3d3dy5hbmltZXRvb24ub3JnL2NhcnRvb24='))
    match2 = re.compile('<td><a href="(.+?)">(.+)</a></td>').findall(HTML2)
    for url,name in match2:
        if (Search_name).replace(' ','') in (name).replace(' ','').lower():
            name = '[COLORred]Origin [/COLOR]' + name
            process.Menu(name,url,803,'','','','')
	
def Football(Search_name):
    url = Decode('aHR0cDovL3d3dy5mdWxsbWF0Y2hlc2FuZHNob3dzLmNvbS8/cz0=')+(Search_name).replace(' ','+')
    origin_url = Decode('aHR0cDovL3d3dy5mb290YmFsbG9yZ2luLmNvbS8/cz0=')+(Search_name).replace(' ','+')
    Football_Repeat.Origin_Highlights(origin_url)
    Football_Repeat.Get_the_rows(url,'')
					
def Live_TV(Search_name):
    if Search_name.lower() == 'w':
        Search_name = 'Watch'
    dp.create('Checking for streams - ' + Search_name)
    Oblivion_list = ['9SPSsLS2','fdpfhagD','jt4xbSEN','vmxWvdb9','7fFXG8hf']
    Raider_live_list = ['http://tombraiderbuilds.co.uk/addon/btsportslive/btsportslive.txt','http://tombraiderbuilds.co.uk/addon/skysportslive/skysportslive.txt'
    'http://tombraiderbuilds.co.uk/addon/sportschannels/','http://tombraiderbuilds.co.uk/addon/ukentertainment/freeworldiptv.txt',
    'http://tombraiderbuilds.co.uk/addon/ukentertainment/freeworldiptv.txt','http://tombraiderbuilds.co.uk/addon/ukentertainment/usfreeview.txt']
    Lily_List = ['http://kodeeresurrection.com/LILYSPORTStxts/livetv.txt','http://kodeeresurrection.com/LILYSPORTStxts/musictv.txt.txt','http://kodeeresurrection.com/LILYSPORTStxts/sport.txt']
    BAMF_List = ['http://genietvcunts.co.uk/bamffff/bamff4m.xml','http://genietvcunts.co.uk/bamffff/livesports.xml']
    Supremecy_List = ['https://simplekore.com/wp-content/uploads/file-manager/steboy11/LiveTV/live.txt',
    'https://simplekore.com/wp-content/uploads/file-manager/steboy11/Kids%20Tv/Kids%20Tv.txt',
    'https://simplekore.com/wp-content/uploads/file-manager/steboy11/Sky%20Movies/Sky%20Movies.txt',
    'https://simplekore.com/wp-content/uploads/file-manager/steboy11/Sport/sport.txt']
    Ultra_List = ['http://ultratv.net16.net/iptvserver/ukiptv1.xml','http://ultratv.net16.net/iptvserver/usaiptv1.xml',
    'http://ultratv.net16.net/iptvserver/canadaiptv1.xml','http://ultratv.net16.net/iptvserver/indiaiptv1.xml']
    HTML = open(freeview_py).read()
    block = re.compile('def CATEGORIES(.+?)#4Music',re.DOTALL).findall(HTML)
    match = re.compile("addLink\('(.+?)','(.+?)',(.+?),(.+?)\)").findall(str(block))
    if ADDON.getSetting('Freeview_Search')=='true':
        dp.update(0,'',"Checking Freeview",'Please Wait')
        for name,url,mode,img in match:
    	    if (Search_name).replace(' ','') in (name).replace(' ','').lower():
                from freeview.freeview import addLink
                addLink('[COLORred]Freeview [/COLOR]'+name,url,mode,img)
    if ADDON.getSetting('Oblivion_Search')=='true':
        dp.update(15,'',"Checking Oblivion",'Please Wait')
        for item in Oblivion_list:
            import base64
            OblivionMain = base64.decodestring('aHR0cDovL3Bhc3RlYmluLmNvbS9yYXcv')
            Thread(target=Raider_Live_Loop(Search_name,OblivionMain.replace('Free.xml',item)))
    if ADDON.getSetting('Pyramid_Search')=='true':
        dp.update(30,'',"Checking Pyramid",'Please Wait')
        for item in Raider_live_list:
            Thread(target=Raider_Live_Loop(Search_name,item))
    if ADDON.getSetting("Tigen's_World_Search")=='true':
        dp.update(50,'',"Checking Deliverance",'Please Wait')
        for item in Lily_List:
            Thread(target=Raider_Live_Loop(Search_name,item))
    if ADDON.getSetting('Supremacy_Search')=='true':
        for item in Supremecy_List:
            dp.update(60,'',"Checking Supremacy",'Please Wait')
            Thread(target=Raider_Live_Loop(Search_name,item))
    if ADDON.getSetting('BAMF_Search')=='true':
        for item in BAMF_List:
            dp.update(70,'',"Checking BAMF",'Please Wait')
            Thread(target=Raider_Live_Loop(Search_name,item))	
    if ADDON.getSetting('Ultra_Search')=='true':
        for item in Ultra_List:
            dp.update(80,'',"Checking Ultra",'Please Wait')
            Thread(target=Raider_Live_Loop(Search_name,item))	
    if ADDON.getSetting('Vendetta_Search')=='true':
            dp.update(90,'',"Checking Ultra",'Please Wait')
            import Live
            Thread(target=Live.search_next(Search_name))	
    dp.update(100,'',"Finished checking",'Please Wait')
    dp.close()

def Tigen_tv(Search_name,url):
    HTML = process.OPEN_URL(url)
    match = re.compile('<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>',re.DOTALL).findall(HTML)
    for name,image,url,fanart in match:
        if (Search_name).replace(' ','').lower() in (name).replace(' ','').lower():
            from pyramid.pyramid import addDir
            addDir('[COLORpink]Tigen\'s World[/COLOR] '+name,url,1101,image,fanart,'','','','')
	
	
def Raider_Live_Loop(Search_name,url):
    if 'raider' in url:
        ADD_NAME = '[COLORblue]Pyramid[/COLOR]'
    elif 'simplekore' in url:
        ADD_NAME = '[COLORred]Supremacy[/COLOR]'
    elif 'oblivion' in url:
        ADD_NAME = '[COLORlightblue]Oblivion[/COLOR]'
    elif 'kodeeresurrection' in url:
        ADD_NAME = '[COLORlightblue]Deliverance[/COLOR]'
    elif 'cunts' in url:
        ADD_NAME = '[COLORwhite]BAMF[/COLOR]'
    elif 'ilent' in url:
        ADD_NAME = '[COLORsteelblue]Silent Hunter[/COLOR]'
    else:
        ADD_NAME = '[COLORwhite]Ultra[/COLOR]'
    HTML = process.OPEN_URL(url)
    match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)</fanart>',re.DOTALL).findall(HTML)
    for name,link,image,fanart in match2:
    	if (Search_name).lower().replace('sports','sport').replace('sport','sports').replace(' ','') in (name).lower().replace(' ','').replace('sports','sport').replace('sport','sports'):
            if 'sublink' in link:
                if 'http' in link:			 
                    from pyramid.pyramid import addDir
                    addDir(ADD_NAME + ' ' +name,link,1130,image,fanart,'','','','')
            else:
                if 'http' in link:			 
                    from pyramid.pyramid import addLink
                    addLink(link, ADD_NAME + ' ' +name,image,'','','','','',None,'',1)
    loop = re.compile('<name>.+?</name>.+?<thumbnail>.+?</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>.+?</fanart>',re.DOTALL).findall(HTML)
    for url in loop:
        if 'http' in url:			 
            Raider_Live_Loop(Search_name,url)
    match = re.compile('<title>(.+?)</title>.+?<sportsdevil>(.+?)</sportsdevil>.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall(HTML)
    for name,url,img in match: 
    	if (Search_name).replace(' ','') in (name).replace(' ','').lower():
            from pyramid.pyramid import addLink
            url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +url
            addLink(url, ADD_NAME + ' ' +name,img,'','','','','',None,'',1)
    match2 = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)').findall(HTML)
    for ignore,name,url in match2:
        total = len(match2)
    	if (Search_name).lower().replace(' ','').replace('sports','sport').replace('sport','sports') in (name).lower().replace(' ','').replace('sports','sport').replace('sport','sports'):
            if 'http' in url:
                from pyramid.pyramid import addLink
                addLink(url,ADD_NAME + ' ' +name,'','','','','','',None,'',total)
            else:
                if '{PQ},' in url:
                    from pyramid.pyramid import Decrypt_Link
                    Decrypt_Link(ignore,ADD_NAME+' '+name,url,total)

def Raider_TV(Search_name,start_url):
	if 'raider' in start_url:
		ADD_NAME = '[COLORblue]Pyramid[/COLOR]'
	elif 'kodeeresurrection' in start_url:
		ADD_NAME = '[COLORpink]Tigen\'s World[/COLOR]'
	if 'season' in Search_name.lower():
		Type = 'single_ep'
		name_splitter = Search_name + '<>'
		name_split = re.compile('(.+?) - season (.+?) episode (.+?)<>').findall(str(name_splitter).lower())
		for name,season,episode in name_split:
			title = name
			season = season
			episode = episode
		year = ''
	else:
		Type = 'full_show'
		title = Search_name
	HTML = process.OPEN_URL(start_url)
	if HTML != 'Opened':
		match = re.compile('<channel>.+?<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>.+?</channel>',re.DOTALL).findall(HTML)
		for name,image,url10,fanart in match:
			if title.lower().replace(' ','') in name.lower().replace(' ',''):
				if Type == 'full_show':
					name = '[COLORblue]Pyramid[/COLOR] ' + name
					process.Menu(name,url10,'',image,fanart,'','')
				elif Type == 'single_ep':
					xbmc.log(url10)
					html10 = process.OPEN_URL(url10)
					seasons = re.compile('<channel>.+?<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>.+?</channel>',re.DOTALL).findall(html10)
					for season_name,image,url11,fanart in seasons:
						xbmc.log('~~~~~~'+season_name)
						season_number = re.compile('season (.+?)>').findall(str(season_name.replace('[/B]','').replace('[/COLOR]','').lower())+'>')
						for seas_no in season_number:
							season_number = seas_no
							season_number = clean_name.clean_number(season_number)
						xbmc.log('SEASON NO = '+str(season_number))
						if season == season_number.replace(' ',''):
							html12 = process.OPEN_URL(url11)
							episodes = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)</fanart>',re.DOTALL).findall(html12)
							for name,url,image,fanart in episodes:
								ep_no = re.compile('s.+?e(.+?)>').findall(str(name.replace(title,'').replace('[/COLOR]','').lower()+'>'))
								for ep_no in ep_no:
									ep_no = ep_no
								if ep_no.replace(' ','').replace('480p','') == episode:
									from pyramid.pyramid import addLink
									addLink(url, ADD_NAME+' | ' + name,image,fanart,'','','','',None,'',1)


def Raider_Loop(Search_name,url):
	if 'raider' in url:
		ADD_NAME = '[COLORblue]Pyramid[/COLOR] '
	elif 'kodeeresurrection' in url:	
		ADD_NAME = '[COLORpink]Tigen\'s World[/COLOR] '
	elif 'ilent' in url:
		ADD_NAME = '[COLORsteelblue]Silent Hunter[/COLOR]'
	else:
		ADD_NAME = ''
	if 'MULTILINK' in url:
		if 'TIGEN' in url:
			if Search_name[0].lower() in 'abcdef':
				single = 'http://kodeeresurrection.com/LILYSPORTStxts/MovieRack/txts/A-F.txt'
			elif Search_name[0].lower() in 'ghijkl':
				single = 'http://kodeeresurrection.com/LILYSPORTStxts/MovieRack/txts/G-L.txt'
			elif Search_name[0].lower() in 'mnopqr':
				single = 'http://kodeeresurrection.com/LILYSPORTStxts/MovieRack/txts/M-R.txt'
			elif Search_name[0].lower() in 'stuvwxyz':
				single = 'http://kodeeresurrection.com/LILYSPORTStxts/MovieRack/txts/S-Z.txt'
			else:
				single = 'http://kodeeresurrection.com/LILYSPORTStxts/MovieRack/txts/NUMBER%20TITLES.txt'
			HTML = process.OPEN_URL('http://kodeeresurrection.com/LILYSPORTStxts/boxsetssub.txt')
			match = re.compile('<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>',re.DOTALL).findall(HTML)
			for name,image,url,fanart in match:
				if (Search_name).lower().replace(' ','').lower() in (name).replace(' ','').lower():
					from pyramid.pyramid import addDir
					addDir('[COLORpink]Tigen\'s World[/COLOR] '+name,url,1101,image,fanart,'','','','')
			HTML2 = process.OPEN_URL(single)
			if HTML2 != 'Opened':
				match = re.compile('<channel>.+?<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>.+?</channel>',re.DOTALL).findall(HTML2)
				for name,image,url,fanart in match:
					if 'http:' in url:
						Raider_Loop(Search_name,url)
						match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)</fanart>',re.DOTALL).findall(HTML)
						for name,url,image,fanart in match2:
							if 'http:' in url:
								if (Search_name).lower().replace(' ','').lower() in (name).replace(' ','').lower():
									from pyramid.pyramid import addLink
									addLink(url, '[COLORpink]Tigen\'s World[/COLOR] '+name,image,fanart,'','','','',None,'',1)
			HTML3 = process.OPEN_URL('http://kodeeresurrection.com/TigensWorldtxt/Movies/Txts/TigensMoviesSub.txt')
			if HTML2 != 'Opened':
				match = re.compile('<channel>.+?<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>.+?</channel>',re.DOTALL).findall(HTML2)
				for name,image,url,fanart in match:
					if 'http:' in url:
						Raider_Loop(Search_name,url)
						match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)</fanart>',re.DOTALL).findall(HTML)
						for name,url,image,fanart in match2:
							if 'http:' in url:
								if (Search_name).lower().replace(' ','').lower() in (name).replace(' ','').lower():
									from pyramid.pyramid import addLink
									addLink(url, '[COLORpink]Tigen\'s World[/COLOR] '+name,image,fanart,'','','','',None,'',1)

	else:
		HTML = process.OPEN_URL(url)
		if HTML != 'Opened':
			match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)</fanart>',re.DOTALL).findall(HTML)
			for name,link,image,fanart in match2:
				if (Search_name).lower().replace(' ','') in (name).replace(' ','').lower():
					if 'sublink' in link:
						from pyramid.pyramid import addDir
						addDir(ADD_NAME + ' ' +name,link,1130,image,fanart,'','','','')
					else:
						from pyramid.pyramid import addLink
						addLink(link, ADD_NAME + ' ' +name,image,'','','','','',None,'',1)        
			match = re.compile('<channel>.+?<name>(.+?)</name>.+?<thumbnail>(.+?)</thumbnail>.+?<externallink>(.+?)</externallink>.+?<fanart>(.+?)</fanart>.+?</channel>',re.DOTALL).findall(HTML)
			for name,image,url,fanart in match:
				if not 'http:' in url:
					pass
				else:
					Raider_Loop(Search_name,url)
			match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)</fanart>',re.DOTALL).findall(HTML)
			for name,url,image,fanart in match2:
				if 'http:' in url:
					if (Search_name).lower().replace(' ','') in (name).replace(' ','').lower():
						from pyramid.pyramid import addLink
						addLink(url, ADD_NAME + ' ' +name,image,fanart,'','','','',None,'',1)
                            
#############################Football Searches####################################

