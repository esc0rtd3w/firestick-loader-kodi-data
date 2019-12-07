# -*- coding: utf-8 -*-

import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, xbmcaddon, json, time, process, requests
from threading import Thread

ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.quantum/')
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
addon_handle = int(sys.argv[1])
List = []
IMDB = 'http://www.imdb.com'


def multiv_Main_Menu(url):
    if 'cunts' in url:
        import Pandora
        Pandora.Pandoras_Box('http://genietvcunts.co.uk/PansBox/ORIGINS/tvcats.php')
    process.Menu('TV Schedule','http://www.tvmaze.com/calendar',6,ICON,FANART,'','')
    process.Menu('IMDB Top 100 Programs','http://www.imdb.com/chart/tvmeter?ref_=m_nv_ch_tvm',301,ICON,FANART,'','')
    process.Menu('Genres','',303,ICON,FANART,'','')
    process.Menu('Check for episode','',41,ICON,FANART,'','')
    process.Menu('Search','',308,ICON,FANART,'','')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))	

def IMDB_TOP_100_EPS(url):	
	html = requests.get(url).text
	show = re.compile('<td class="posterColumn">.+?<a href="(.+?)".+?<img src="(.+?)".+?title=".+?" >(.+?)</a>.+?<span class="secondaryInfo">(.+?)</span>',re.DOTALL).findall(html)
	for url,img,title,year in show:
		try:
			url = 'http://www.imdb.com'+url
			img = img.replace('45,67','174,256').replace('UY67','UY256').replace('UX45','UX175')
			process.Menu(title+' '+year,url,305,img,'','',title+year)
		except:
			pass
		
def IMDB_Get_Season_info(url,image,title):
    html = process.OPEN_URL(url)
    highest_season = re.compile('<br class="clear" />.+?<a href="(.+?)"',re.DOTALL).findall(html)
    for thing in highest_season:
        if 'season' in thing:
            fin_thing = 'http://www.imdb.com'+thing+'>'
            number = re.compile('(.+?)season=(.+?)&(.+?)sn_(.+?)>').findall(str(fin_thing))
            for start,seas,other,item in number:
                number = item
            while int(number)>=1:
                url = str(start) + 'season='+str(number)+'&'+other+'sn_'+ str(number)
                process.Menu('Season '+str(number),url,306,image,'','',title)
                number = int(number) - 1

def IMDB_Get_Episode_info(url,title):
	ep_year = ''
	image = ''
	html = requests.get(url).text
	block = re.compile('<div class="list_item(.+?)itemprop="description">(.+?)</div>',re.DOTALL).findall(html)
	for block_,desc in block:
		name = re.compile('title="(.+?)"').findall(str(block_))
		for item in name:
			name = item
		image = re.compile('src="(.+?)"').findall(str(block_))
		for item in image:
			image = item
		year = re.compile('<div class="airdate">(.+?)</div>',re.DOTALL).findall(str(block_))
		for item in year:
			date = item
			splitone = item.replace('\n','').replace('  ','').replace('	','') +'>'
			show_year_split = re.compile(' .+?\. (.+?)>').findall(str(splitone))
			for item in show_year_split:
				ep_year = item
		ep_no = re.compile('<div>S(.+?)</div>').findall(str(block_))
		for item in ep_no:
			ep_no = item
		ep_split = ep_no+'<'
		Split = re.compile('(.+?),(.+?)<').findall(str(ep_split))
		for one,two in Split:
			season = one.replace('S','Season ')
			episode = two.replace('Ep','Episode ').replace(' Episode ','')
		title_split = re.compile('(.+?)\((.+?)\)').findall(str(title))
		for title,show_year in title_split:
			title = title
			show_year = show_year
		search_split = 'SPLITTER>'+title+'>'+show_year+'>'+ep_year+'>'+season+'>'+episode+'>'
		search_split = search_split.replace(' >','>')
		final_name = 'Episode '+episode+' - '+name
		try:
			process.Menu(str(final_name),'',307,str(image),'','[COLORred]AIR DATE[/COLOR] == '+str(date).replace('  ','').replace('\n','')+'\n'+str(desc),search_split)
			process.setView('movies', 'INFO')
		except:
			pass
		
def SPLIT(extra):
	#xbmc.log('#######'+extra)
	finish = re.compile('SPLITTER>(.+?)>(.+?)>(.+?)>(.+?)>(.+?)>').findall(str(extra))
	for title,show_year,ep_year,season,episode in finish:
		from lib import Scrape_Nan
		Scrape_Nan.scrape_episode(title,show_year,ep_year,season,episode,'')
def Search_TV():
	Search_title = xbmcgui.Dialog().input('Search', type=xbmcgui.INPUT_ALPHANUM)
	url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='+Search_title.replace(' ','+')+'&s=all'
	html = requests.get(url).text
	match = re.compile('<tr class="findResult.+?"> <td class="primary_photo"> <a href="(.+?)" ><img src="(.+?)" /></a> </td> <td class="result_text"> <a href=".+?" >(.+?)</a>(.+?)</td>').findall(html)
	for url,image,title,year in match:
		if '<' in year:
			pass
		else:
			if '(TV Series)' in year:
				url = 'http://imdb.com'+url
				year = year.replace('(TV Series)','')
				image = image.replace('32,44','174,256').replace('UY67','UY256').replace('UX32','UX175').replace('UY44','UY256')
				process.Menu(title+' '+year,url,305,image,'','',title+year)
					
def Genres():
	html = requests.get('http://www.imdb.com/genre/').text
	block = re.compile('<h2>Television and Mini-Series</h2>(.+?)<hr>',re.DOTALL).findall(html)
	for item in block:
		match = re.compile('<a href="(.+?)">(.+?)</a>').findall(str(item))
		for url, name in match:
			process.Menu(name,url,304,'','','','')

def Genres_Page(url):
	html = requests.get(url).text
	match = re.compile('<div class="lister-item-image float-left">.+?<a href="(.+?)".+?<img alt="(.+?)".+?loadlate="(.+?)".+?<span class="lister-item-year text-muted unbold">(.+?)</span>',re.DOTALL).findall(html)
	for url, name, image, year in match:
		url = 'http://imdb.com'+url
		year = re.sub("\D","",year)
		year = '('+year[0:4]+')'
		try:
			try:
				image = image.replace('67,98','256,385').replace('UX67','UX256').replace('UY98','UY385')
				process.Menu(name+' '+year,url,305,image,'','',name.encode('utf-8')+year.encode('utf-8'))
			except:
				process.Menu(name+' '+year,url,305,'','','',name.encode('utf-8')+year.encode('utf-8'))
		except:
			pass

