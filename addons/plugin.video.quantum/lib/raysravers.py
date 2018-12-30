# -*- coding: cp1252 -*-
import xbmcgui, urllib, process, base64, re

#################
dp =  xbmcgui.DialogProgress()
AddonTitle="[COLORred]RaysRavers[/COLOR]" 
dialog = xbmcgui.Dialog()
Decode = base64.decodestring
BASEURL = (Decode('aHR0cDovL3JhaXp0di5jby51ay9SYXlzUmF2ZXJzLw=='))
list = BASEURL+(Decode('bGlzdC9tYWluLnBocA=='))

def INDEX():
    process.Menu('[COLORred]RaysRavers[/COLOR]',BASEURL+(Decode('bGlzdC9tYWluLnBocA==')),2251,'','','','')
    process.Menu('[COLORgold]The Best Of...[/COLOR]',BASEURL+(Decode('bGlzdC9tai5waHA=')),2251,'','','','')
    process.Menu('[COLORgold]Guns n Roses Greatest Hits[/COLOR]',BASEURL+(Decode('bGlzdC9ndW5zbnJvc2VzLnBocA==')),2251,'','','','')
    process.Menu('[COLORgold]Garth Brooks The Ultimate Hits[/COLOR]',BASEURL+(Decode('bGlzdC9nYnJvb2tzLnBocA==')),2251,'','','','')
    process.Menu('[COLORgold]HELTER SKELTER[/COLOR]',BASEURL+(Decode('bGlzdC9oZWx0ZXJtYWluLnBocA==')),2251,'','','','')

def LISTS(url):
    process.Menu('[COLORsteelblue]Search RaysRavers[/COLOR]','',2252,'','','','')
    html=process.OPEN_URL(list)
    match=re.compile('<a href="([^"]*)" target="_blank"><img src="([^"]*)" style="max-width:200px;" /><description = "([^"]*)" /><background = "([^"]*)" </background></a><br><b>(.+?)</b>').findall(html)
    for url,iconimage,desc,fanart,name in match:
        if 'http' in url:
			if '.php' in url:
				process.Menu((name).replace('_',' '),url,2251,iconimage,fanart,desc,'')
			else:
				if 'youtube' in url:
					process.Play((name).replace('_',' '),'plugin://plugin.video.youtube/play/?video_id='+url,906,iconimage,fanart,desc,'')     
				else:
					process.Play((name).replace('_',' '),url,906,iconimage,fanart,desc,'')			
	
def LISTS2(url):
    html=process.OPEN_URL(url)
    match=re.compile('<a href="([^"]*)" target="_blank"><img src="([^"]*)" style="max-width:200px;" /><description = "([^"]*)" /><background = "([^"]*)" </background></a><br><b>(.+?)</b>').findall(html)
    for url,iconimage,desc,fanart,name in match:
        if 'http' in url:
			if '.php' in url:
				process.Menu((name).replace('_',' '),url,2251,iconimage,fanart,desc,'')
			else:
				if 'youtube' in url:
					process.Play((name).replace('_',' '),'plugin://plugin.video.youtube/play/?video_id='+url,906,iconimage,fanart,desc,'')     
				else:
					process.Play((name).replace('_',' '),url,906,iconimage,fanart,desc,'')			
		
def SEARCHLISTS():
	choices = ['[COLORsteelblue]Music[/COLOR]','[COLORsteelblue]Movies & Tv[/COLOR]','[COLORsteelblue]Kids[/COLOR]']
	choice = xbmcgui.Dialog().select('[COLORsteelblue]Search RaysRavers[/COLOR]', choices)
	if choice==0:
		search('http://raiztv.co.uk/RaysRavers/list/allmusic.php')
	if choice==1:
		search('http://raiztv.co.uk/RaysRavers/list/allmoviesandtv.php')
	if choice==2:
		search('http://raiztv.co.uk/RaysRavers/list/allkids.php')

def search(url):
    html = process.OPEN_URL(url)
    Search_Name = dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM) 
    Search_Title = Search_Name.lower()
    match=re.compile('<a href="([^"]*)" target="_blank"><img src="([^"]*)" style="max-width:200px;" /><description = "([^"]*)" /><background = "([^"]*)" </background></a><br><b>(.+?)</b>').findall(html)
    for url,iconimage,desc,fanart,name in match:
        if Search_Name in name.lower():
            process.Play((name).replace('_',' '),url,906,iconimage,fanart,desc,'')