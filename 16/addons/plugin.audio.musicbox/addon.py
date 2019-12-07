#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 2015 Techdealer

##############LIBRARIES TO IMPORT AND SETTINGS####################

import urllib,urllib2,urlparse,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,time,datetime,os,xbmcvfs
import json
import random
import requests
import hashlib
import cookielib
import vkAuth

import SimpleDownloader as downloader
downloader = downloader.SimpleDownloader()
from random import randint
from mutagen.mp3 import MP3
import mutagen.id3

addon_id = 'plugin.audio.musicbox'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'
translation = selfAddon.getLocalizedString
datapath = xbmc.translatePath('special://profile/addon_data/%s' % addon_id ).decode("utf-8")

VKCookie = os.path.join(datapath,'cookies.txt')

VK_useragent = "Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0"
addon_useragent = "Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0"

def translate(text):
	return translation(text).encode('utf-8')
	  
###################################################################################
#MAIN MENU

def Main_menu():
	#flag if a vk.com cookie is valid
	validVKCookie = False

	#if empty vk.com email xor password
	if bool(selfAddon.getSetting('vk_email')=="") ^ bool(selfAddon.getSetting('vk_password')==""):
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30866))
		xbmcaddon.Addon(addon_id).openSettings()
		return	
	#if empty vk.com email and password
	elif selfAddon.getSetting('vk_email')=="" and selfAddon.getSetting('vk_password')=="":
		selfAddon.setSetting('vk_auth_email','')
		selfAddon.setSetting('vk_auth_password','')
		if xbmcvfs.exists(VKCookie): xbmcvfs.delete(VKCookie)
		#display vk.com account need message
		if selfAddon.getSetting('playing_type') == "0":
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400),translate(30878))
			xbmcaddon.Addon(addon_id).openSettings()
			return
	#if credentials are given
	else:
		#check if user changed vk_email/vk_password or if vk_auth_email/vk_auth_password is empty (need reauth)
		if selfAddon.getSetting('vk_auth_email')!=selfAddon.getSetting('vk_email') or selfAddon.getSetting('vk_auth_password')!=selfAddon.getSetting('vk_password'):
			selfAddon.setSetting('vk_auth_email','')
			selfAddon.setSetting('vk_auth_password','')
			if xbmcvfs.exists(VKCookie): xbmcvfs.delete(VKCookie)
		#check current cookie
		if xbmcvfs.exists(VKCookie): validVKCookie = vkAuth.isCookieValid(VKCookie)
		else: validVKCookie = False
		#if the cookie provided is not valid, login again
		if validVKCookie != True:
			#login in vk.com - get the cookie
			email = selfAddon.getSetting('vk_email')
			passw = selfAddon.getSetting('vk_password')
			try: auth_status = vkAuth.auth(email, passw)
			except: auth_status = False
			#check login status
			if auth_status == False:
				dialog = xbmcgui.Dialog()
				ok = dialog.ok(translate(30400),translate(30867))
				xbmcaddon.Addon(addon_id).openSettings()
				return
			else:
				#test the new cookie
				validVKCookie = vkAuth.isCookieValid(VKCookie)
				#if there was an error, inform the user
				if validVKCookie != True:
					dialog = xbmcgui.Dialog()
					ok = dialog.ok(translate(30400),translate(30867))
					xbmcaddon.Addon(addon_id).openSettings()
					return
				else:
					selfAddon.setSetting('vk_auth_email',email)
					selfAddon.setSetting('vk_auth_password',passw)
					notification(translate(30861),translate(30865),'4000',addonfolder+artfolder+'notif_vk.png')
	
	#everything should be fine now
	addDir(translate(30401),'1',1,addonfolder+artfolder+'recomended.png')
	addDir(translate(30402),'1',2,addonfolder+artfolder+'digster.png')
	if selfAddon.getSetting('hide_soundtrack')=="false": addDir(translate(30403),'0',7,addonfolder+artfolder+'whatsong.png')
	if selfAddon.getSetting('hide_8tracks')=="false": addDir(translate(30404),'1',9,addonfolder+artfolder+'8tracks.png')
	addDir(translate(30405),'1',11,addonfolder+artfolder+'charts.png')
	addDir(translate(30406),'1',25,addonfolder+artfolder+'search.png')
	addDir(translate(30407),'1',38,addonfolder+artfolder+'mymusic.png')
	addDir(translate(30408),'',44,addonfolder+artfolder+'favorites.png')
	addDir(translate(30409),'',48,addonfolder+artfolder+'userspace.png')
	addDir(translate(30410),'',53,addonfolder+artfolder+'fingerprint.png')
	addDir(translate(30411),'',54,addonfolder+artfolder+'configs.png',False)

###################################################################################
#RECOMENDATIONS

def Recomendations(url):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=chart.getTopTracks&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['tracks']['track'])):
		artist = decoded_data['tracks']['track'][x]['artist']['name'].encode("utf8")
		track_name = decoded_data['tracks']['track'][x]['name'].encode("utf8")
		try: iconimage = decoded_data['tracks']['track'][x]['image'][3]['#text'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
	total_pages = decoded_data['tracks']['@attr']['totalPages']
	if int(url)<int(total_pages): addDir(translate(30412),str(int(url)+1),1,addonfolder+artfolder+'next.png')

###################################################################################
#DIGSTER	

def Digster_menu():
	addDir('[COLOR blue][B]'+translate(30112)+':[/B][/COLOR] '+['Adria','Denmark','Estonia','Finland','Latvia','Lithuania','Mexico','Netherlands','New Zeland','Norway','Portugal','Romania','Spain'][int(selfAddon.getSetting('digster_country'))],'',2,'',False)
	addDir(translate(30425),'',3,'')
	addDir(translate(30426),'genre',4,'')
	addDir(translate(30427),'mood',4,'')
	addDir(translate(30428),'suitable',4,'')

def Digster_sections():
	digster_domain = ['http://digster-adria.com/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/sections')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['sections'])):
		slug = decoded_data['sections'][x]['slug'].encode("utf8")
		title = decoded_data['sections'][x]['name'].encode("utf8")
		addDir(title,'1',5,'',search_query = '&section='+slug)

def Digster_categories(url):
	digster_domain = ['http://digster-adria.com/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/taxonomies/'+url)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['taxonomy'])):
		slug = decoded_data['taxonomy'][x]['slug'].encode("utf8")
		title = decoded_data['taxonomy'][x]['title'].encode("utf8").replace("&amp;", "&")
		addDir(title,'1',5,'',search_query = '&'+url+'='+slug)

def List_digster_playlists(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	digster_domain = ['http://digster-adria.com/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/'][int(selfAddon.getSetting('digster_country'))]	
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists?posts_per_page='+str(items_per_page)+'&paged='+str(url)+search_query)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['playlists'])):
		slug = decoded_data['playlists'][x]['slug'].encode("utf8")
		title = decoded_data['playlists'][x]['title'].encode("utf8")
		try: iconimage = decoded_data['playlists'][x]['image']['large'][0].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir(title,slug,6,iconimage,country = selfAddon.getSetting('digster_country'),type='playlist')
	#check if next page exist
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists?posts_per_page='+str(items_per_page)+'&paged='+str(int(url)+1)+search_query)
	decoded_data = json.loads(codigo_fonte)
	if len(decoded_data['playlists'])>0: addDir(translate(30412),str(int(url)+1),5,addonfolder+artfolder+'next.png',search_query = search_query)

def List_digster_tracks(url,country):
	digster_domain = ['http://digster-adria.com/','http://www.digster.dk/','http://digster.ee/','http://www.digster.fi/','http://digster.lv/','http://digster.lt/','http://digster.mx/','http://www.digster.nl/','http://www.digster.co.nz/','http://www.digster.no/','http://www.digster.pt/','http://www.digster.ro/','http://www.digster.es/'][int(selfAddon.getSetting('digster_country'))]
	codigo_fonte = abrir_url(digster_domain+'api/2.0.0/playlists/'+url)
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['playlist']['tracks'])):
		if len(decoded_data['playlist']['tracks'][x]['artists'])==1: artist = decoded_data['playlist']['tracks'][x]['artists'][0].encode("utf8")
		elif len(decoded_data['playlist']['tracks'][x]['artists'])==2: artist = decoded_data['playlist']['tracks'][x]['artists'][0].encode("utf8")+' feat. '+decoded_data['playlist']['tracks'][x]['artists'][1].encode("utf8")
		elif len(decoded_data['playlist']['tracks'][x]['artists'])>2:
			artist = ''
			for y in range(0, len(decoded_data['playlist']['tracks'][x]['artists'])): artist = artist+decoded_data['playlist']['tracks'][x]['artists'][y].encode("utf8")+' & '
			artist = artist[:-3] # remove last ' & '
		track_name = decoded_data['playlist']['tracks'][x]['title'].encode("utf8")
		iconimage = addonfolder+artfolder+'no_cover.png'
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)

###################################################################################
#WHATSONG SOUNDTRACK

def List_whatsong_movies(url):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url_custom('http://www.api.what-song.com/recent-movies?limit='+str(items_per_page)+'&skip='+str(int(items_per_page)*int(url)), headers = {'Referer': 'http://www.what-song.com/movies', 'Origin': 'http://www.what-song.com'})
	decoded_data = json.loads(codigo_fonte)
	total_items = decoded_data['total_items_count']
	for x in range(0, len(decoded_data['data'])):
		try:
			name = decoded_data['data'][x]['title'].encode("utf8")
			movie_id = str(decoded_data['data'][x]['_id'])
			iconimage = decoded_data['data'][x]['poster_url']
			addDir(name,movie_id,8,iconimage,type='soundtrack')
		except: pass
	#check if next page exist
	if int((int(url)+1)*items_per_page)<total_items: addDir(translate(30412),str(int(url)+1),7,addonfolder+artfolder+'next.png')

def List_whatsong_tracks(url):
	codigo_fonte = abrir_url_custom('http://www.api.what-song.com/movie-info?movieID='+url, headers = {'Referer': 'http://www.what-song.com/movies', 'Origin': 'http://www.what-song.com'})
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['data']['CompleteListOfSongs'])):
		artist = decoded_data['data']['CompleteListOfSongs'][x]['artist']['name'].encode("utf8")
		track_name = decoded_data['data']['CompleteListOfSongs'][x]['title'].encode("utf8")
		try: iconimage = decoded_data['data']['CompleteListOfSongs'][x]['spotifyImg300']
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)

###################################################################################
#8TRACKS

def Eighttracks_menu():
	addDir(translate(30475),'1',10,'',search_query = 'all:popular')
	addDir(translate(30476),'1',10,'',search_query = 'collection:staff-picks')
	addDir(translate(30477),'1',10,'',search_query = 'collection:homepage')
	addDir(translate(30478),'1',10,'',search_query = 'all:hot')
	addDir(translate(30479),'1',10,'',search_query = 'all:recent')

def List_8tracks_suggestions(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://8tracks.com/mix_sets/'+search_query+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['mixes'])):
		username = decoded_data['mixes'][x]['user']['login'].encode("utf8")
		playlist_name = decoded_data['mixes'][x]['name'].encode("utf8")
		tracks_count = str(decoded_data['mixes'][x]['tracks_count'])
		playlist_id = str(decoded_data['mixes'][x]['id'])
		try: iconimage = decoded_data['mixes'][x]['cover_urls']['max200'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir('[B]'+username+'[/B] - '+playlist_name+' [I]('+tracks_count+' tracks)[/I]','1',33,iconimage,playlist_id = playlist_id,type='playlist')
	total_pages = decoded_data['total_pages']
	if int(url)<int(total_pages): addDir(translate(30412),str(int(url)+1),10,addonfolder+artfolder+'next.png',search_query = search_query)
		
###################################################################################
#CHARTS

def Top_charts_menu():
	addDir(translate(30500),'1',13,'')
	addDir(translate(30501),'1',14,'')
	addDir(translate(30502),'1',18,'')
	addDir(translate(30503),'1',19,'')
	addDir(translate(30504),'1',20,'')
	addDir(translate(30505),'1',22,'',playlist_id = 'http://www.billboard.com/rss/charts/hot-100')
	addDir(translate(30506),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/billboard-200')
	addDir(translate(30507),'1',22,'',playlist_id = 'http://www.billboard.com/rss/charts/heatseekers-songs')
	addDir(translate(30508),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/heatseekers-albums')
	addDir(translate(30509),'1',22,'',playlist_id = 'http://www.billboard.com/rss/charts/pop-songs')
	addDir(translate(30510),'1',22,'',playlist_id = 'http://www.billboard.com/rss/charts/country-songs')
	addDir(translate(30511),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/country-albums')
	addDir(translate(30512),'1',22,'',playlist_id = 'http://www.billboard.com/rss/charts/rock-songs')
	addDir(translate(30513),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/rock-albums')
	addDir(translate(30514),'1',22,'',playlist_id = 'http://www.billboard.com/rss/charts/r-b-hip-hop-songs')
	addDir(translate(30515),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/r-b-hip-hop-albums')
	addDir(translate(30516),'1',22,'',playlist_id = 'http://www.billboard.com/rss/charts/hot-r-and-b-hip-hop-airplay')
	addDir(translate(30517),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/dance-electronic-albums')
	addDir(translate(30518),'1',22,'',playlist_id = 'http://www.billboard.com/rss/charts/latin-songs')
	addDir(translate(30519),'1',23,'',playlist_id = 'http://www.billboard.com/rss/charts/latin-albums')
	addDir(translate(30523),'1',24,'',playlist_id = 'http://www.traxsource.com/scripts/builder.php/top/tracks?rpc=1')
	addDir(translate(30524),'1',24,'',playlist_id = 'http://www.traxsource.com/scripts/builder.php/top/singles?rpc=1')

def Itunes_countries_menu(mode):
	country_name = ["Albania","Algeria","Angola","Anguilla","Antigua and Barbuda","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Botswana","Brazil","British Virgin Islands","Brunei Darussalam","Bulgaria","Burkina Faso","Cambodia","Canada","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo, Republic of the","Costa Rica","Croatia","Cyprus","Czech Republic","Denmark","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Estonia","Fiji","Finland","France","Gambia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea-Bissau","Guyana","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Korea, Republic Of","Kuwait","Kyrgyzstan","Lao, People's Democratic Republic","Latvia","Lebanon","Liberia","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Mali","Malta","Mauritania","Mauritius","Mexico","Micronesia, Federated States of","Moldova","Mongolia","Montserrat","Mozambique","Namibia","Nepal","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Qatar","Romania","Russia","Saudi Arabia","Senegal","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","South Africa","Spain","Sri Lanka","St. Kitts and Nevis","St. Lucia","St. Vincent and The Grenadines","Suriname","Swaziland","Sweden","Switzerland","São Tomé and Príncipe","Taiwan","Tajikistan","Tanzania","Thailand","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Turks and Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan","Venezuela","Vietnam","Yemen","Zimbabwe"]
	country_code = ["al","dz","ao","ai","ag","ar","am","au","at","az","bs","bh","bb","by","be","bz","bj","bm","bt","bo","bw","br","vg","bn","bg","bf","kh","ca","cv","ky","td","cl","cn","co","cg","cr","hr","cy","cz","dk","dm","do","ec","eg","sv","ee","fj","fi","fr","gm","de","gh","gr","gd","gt","gw","gy","hn","hk","hu","is","in","id","ie","ir","it","jm","jp","jo","kz","ke","kr","kw","kg","la","lv","lb","lr","lt","lu","mo","mk","mg","mw","my","ml","mt","mr","mu","mx","fm","md","mn","ms","mz","na","np","nl","nz","ni","ne","ng","no","om","pk","pw","pa","pg","py","pe","ph","pl","pt","qa","ro","ru","sa","sn","sc","sl","sg","sk","si","sb","za","es","lk","kn","lc","vc","sr","sz","se","ch","st","tw","tj","tz","th","tt","tn","tr","tm","tc","ug","ua","ae","gb","us","uy","uz","ve","vn","ye","zw"]
	for x in range(0, len(country_name)):
		if country_code[x] not in ["al","dz","ao","bj","bt","td","cn","cg","gy","is","jm","kr","kw","lr","mk","mg","mw","ml","mr","ms","pk","pw","sn","sc","sl","sb","lc","vc","sr","st","tz","tn","tc","uy","ye"]: #Countries without music store
			if mode==13: addDir(country_name[x],'1',15,'http://www.geonames.org/flags/x/'+country_code[x]+'.gif',country = country_code[x])
			elif mode==14: addDir(country_name[x],'1',16,'http://www.geonames.org/flags/x/'+country_code[x]+'.gif',country = country_code[x])

def Itunes_track_charts(url,country):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('https://itunes.apple.com/'+country+'/rss/topsongs/limit=100/explicit=true/json')
	decoded_data = json.loads(codigo_fonte)
	total_items = len(decoded_data['feed']['entry'])
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		try:
			artist = decoded_data['feed']['entry'][x]['im:artist']['label'].encode("utf8")
			track_name = decoded_data['feed']['entry'][x]['im:name']['label'].encode("utf8")
			try: iconimage = decoded_data['feed']['entry'][x]['im:image'][2]['label'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
		except: pass
	if int(int(url)*items_per_page)<total_items: addDir(translate(30412),str(int(url)+1),15,addonfolder+artfolder+'next.png',country = country)

def Itunes_album_charts(url,country):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('https://itunes.apple.com/'+country+'/rss/topalbums/limit=100/explicit=true/json')
	decoded_data = json.loads(codigo_fonte)
	total_items = len(decoded_data['feed']['entry'])
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		try:
			artist = decoded_data['feed']['entry'][x]['im:artist']['label'].encode("utf8")
			album_name = decoded_data['feed']['entry'][x]['im:name']['label'].encode("utf8")
			id = decoded_data['feed']['entry'][x]['id']['attributes']['im:id'].encode("utf8")
			try: iconimage = decoded_data['feed']['entry'][x]['im:image'][2]['label'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir('[COLOR yellow]'+str(x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,id,17,iconimage,album = album_name,artist = artist,country = country,type = 'album')
		except: pass
	if int(int(url)*items_per_page)<total_items: addDir(translate(30412),str(int(url)+1),16,addonfolder+artfolder+'next.png',country = country)

def Itunes_list_album_tracks(url,album,country):
	#api documentation: https://www.apple.com/itunes/affiliates/resources/documentation/itunes-store-web-service-search-api.html
	codigo_fonte = abrir_url('https://itunes.apple.com/lookup?id='+url+'&country='+country+'&entity=song&limit=200')
	decoded_data = json.loads(codigo_fonte)
	try:
		if int(decoded_data['resultCount'])>0:
			for x in range(1, len(decoded_data['results'])):
				artist = decoded_data['results'][x]['artistName'].encode("utf8")
				track_name = decoded_data['results'][x]['trackName'].encode("utf8")
				try: iconimage = decoded_data['results'][x]['artworkUrl100'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
	except: pass

def Deezer_top_tracks(url):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	session = requests.session()
	#get api_token
	p = session.get('http://www.deezer.com/charts/track')
	api_token = re.search('var checkForm = "(.+?)";', p.text.encode('utf-8')).group(1)
	print api_token
	#get json data
	p = session.post('http://www.deezer.com/ajax/gw-light.php?api_version=1.0&api_token=%s&input=3' % api_token, data='[{"method":"deezer.pageTops","params":{"TYPE":"track","GENRE_ID":0,"START":%s,"NB":%s}}]' % (str((int(url)-1)*items_per_page),str(items_per_page)), headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://www.deezer.com/tops/track'})
	#process data
	decoded_data = json.loads(p.text.encode('utf-8'))
	for x in range(0, len(decoded_data[0]['results']['ITEMS']['data'])):
		artist = decoded_data[0]['results']['ITEMS']['data'][x]['ART_NAME'].encode("utf8")
		track_name = decoded_data[0]['results']['ITEMS']['data'][x]['SNG_TITLE'].encode("utf8")
		album = decoded_data[0]['results']['ITEMS']['data'][x]['ALB_TITLE'].encode("utf8")
		iconimage = 'http://cdn-images.deezer.com/images/cover/%s/250x250-000000-80-0-0.jpg' % decoded_data[0]['results']['ITEMS']['data'][x]['ALB_PICTURE']
		if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str((x+1)+((int(url)-1)*items_per_page))+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
		elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str((x+1)+((int(url)-1)*items_per_page))+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
	#check if next page exist
	if int(int(url)*items_per_page)<300: addDir(translate(30412),str(int(url)+1),18,addonfolder+artfolder+'next.png')	

def Beatport_top100(url):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('https://pro.beatport.com/top-100')
	json_data = re.findall('"tracks"\: (.+?)\};', codigo_fonte, re.DOTALL)[0]
	decoded_data = json.loads(json_data)
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		try:
			track_number = str(x+1)
			if len(decoded_data[x]['artists'])==1: artist = decoded_data[x]['artists'][0]['name'].encode("utf8")
			elif len(decoded_data[x]['artists'])==2: artist = decoded_data[x]['artists'][0]['name'].encode("utf8")+' feat. '+decoded_data[x]['artists'][1]['name'].encode("utf8")
			elif len(decoded_data[x]['artists'])>2:
				artist = ''
				for y in range(0, len(decoded_data[x]['artists'])): artist = artist+decoded_data[x]['artists'][y]['name'].encode("utf8")+' & '
				artist = artist[:-3] # remove last ' & '
			title_primary = decoded_data[x]['name'].encode("utf8")
			remixed = '('+decoded_data[x]['mix'].encode("utf8")+')'
			track_name = title_primary+' '+remixed
			iconimage = decoded_data[x]['images']['large']['url']
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
		except: pass
	if int(int(url)*items_per_page)<len(decoded_data): addDir(translate(30412),str(int(url)+1),19,addonfolder+artfolder+'next.png')

def Officialcharts_uk(url,mode,playlist_id):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	if playlist_id==None or playlist_id=='':
		options_name = ['Singles','Albums','Dance Singles','Dance Albums','Indie Singles','Indie Albums','RnB Singles','RnB Albums','Rock Singles','Rock Albums','Compilations Albums']
		options_mode = [20,21,20,21,20,21,20,21,20,21,21]
		options_playlist_id = ['http://www.bbc.co.uk/radio1/chart/singles','http://www.bbc.co.uk/radio1/chart/albums','http://www.bbc.co.uk/radio1/chart/dancesingles','http://www.bbc.co.uk/radio1/chart/dancealbums','http://www.bbc.co.uk/radio1/chart/indiesingles','http://www.bbc.co.uk/radio1/chart/indiealbums','http://www.bbc.co.uk/radio1/chart/rnbsingles','http://www.bbc.co.uk/radio1/chart/rnbalbums','http://www.bbc.co.uk/radio1/chart/rocksingles','http://www.bbc.co.uk/radio1/chart/rockalbums','http://www.bbc.co.uk/radio1/chart/compilations']
		id = xbmcgui.Dialog().select(translate(30520), options_name)
		if id != -1:
			mode = options_mode[id]
			playlist_id = options_playlist_id[id]
		else:
			sys.exit(0)
	codigo_fonte = abrir_url(playlist_id)
	if url=='1': addDir(translate(30521),'1',20,'')
	match = re.findall('<div class="cht-entry-wrapper">.*?<div class="cht-entry-position">[^\d]*?([\d]+).*?</div>.*?<img.*?class="cht-entry-image".*?src="(.+?)".*?>.*?<div class="cht-entry-details">.*?<div class="cht-entry-title">(.*?)</div>.*?<div class="cht-entry-artist">.*?<a.*?>(.*?)</a>.*?</div>', codigo_fonte, re.DOTALL)
	for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
		if mode==20: #track charts
			try:
				track_number = match[x][0]
				track_name = match[x][2].strip()
				artist = match[x][3].strip()
				iconimage = match[x][1]
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
			except: pass
		elif mode==21: #album charts
			try:
				album_number = match[x][0]
				album_name = match[x][2].strip()
				artist = match[x][3].strip()
				iconimage = match[x][1]
				addDir('[COLOR yellow]'+album_number+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',28,iconimage,artist = artist,album = album_name,type = 'album')
			except: pass
	if int(int(url)*items_per_page)<len(match): addDir(translate(30412),str(int(url)+1),mode,addonfolder+artfolder+'next.png',playlist_id = playlist_id)
	
def Billboard_charts(url,mode,playlist_id):
	#if mode==22: list billboard track charts
	#if mode==23: list billboard album charts
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str(int(url)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
	decoded_data = json.loads(codigo_fonte)
	try:
		if len(decoded_data['query']['results']['item']) > 0:
			if mode==22:
				#checks if output has only an object or various and proceeds according
				if 'artist' in decoded_data['query']['results']['item'] and 'chart_item_title' in decoded_data['query']['results']['item']:
					artist = decoded_data['query']['results']['item']['artist'].encode("utf8")
					track_name = decoded_data['query']['results']['item']['chart_item_title'].encode("utf8")
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,search_query = artist+' '+track_name)
				else:
					for x in range(0, len(decoded_data['query']['results']['item'])):
						artist = decoded_data['query']['results']['item'][x]['artist'].encode("utf8")
						track_name = decoded_data['query']['results']['item'][x]['chart_item_title'].encode("utf8")
						if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,type = 'song')
						elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,search_query = artist+' '+track_name)
			elif mode==23:
				#checks if output has only an object or various and proceeds according
				if 'artist' in decoded_data['query']['results']['item'] and 'chart_item_title' in decoded_data['query']['results']['item']:
					artist = decoded_data['query']['results']['item']['artist'].encode("utf8")
					track_name = decoded_data['query']['results']['item']['chart_item_title'].encode("utf8")
					addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',28,addonfolder+artfolder+'no_cover.png',artist = artist,album = album_name,type = 'album')
				else:
					for x in range(0, len(decoded_data['query']['results']['item'])):
						artist = decoded_data['query']['results']['item'][x]['artist'].encode("utf8")
						album_name = decoded_data['query']['results']['item'][x]['chart_item_title'].encode("utf8")
						addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+album_name,'',28,addonfolder+artfolder+'no_cover.png',artist = artist,album = album_name,type = 'album')
	except: pass
	try:
		codigo_fonte_2 = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM feed(' + str((int(url)+1)*items_per_page-items_per_page+1) + ',' + str(items_per_page) + ') WHERE url="' + playlist_id + '"') + '&format=json&diagnostics=true&callback=', timeout=30)
		decoded_data_2 = json.loads(codigo_fonte_2)
		if len(decoded_data_2['query']['results']['item']) > 0: addDir(translate(30412),str(int(url)+1),mode,addonfolder+artfolder+'next.png',playlist_id = playlist_id)
	except: pass

def Traxsource_top(url,playlist_id):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	if playlist_id == 'http://www.traxsource.com/scripts/builder.php/top/tracks?rpc=1':
		codigo_fonte = abrir_url(playlist_id)
		match = re.findall('\<tr.*?\>.*?\<div class\="tnum"\>(.+?)\</div\>.*?\<td class\="thumb"\>.*?\<img.*?src\="(.+?)".*?\>.*?\</td\>.*?\<td class\="r\-pad"\>(.+?)\<span class\="duration"\>.*?\</td\>.*?\<td class\="r\-pad"\>(.+?)\</td\>.*?\</tr\>', codigo_fonte, re.DOTALL)
		for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
			try:
				track_number = match[x][0]
				track_name = match[x][2]
				if track_name.endswith('<span class="version"> '): #track without version name
					track_name = re.sub('<[^>]*>', '', track_name)
					track_name = track_name.strip()
				else: #track with version name
					track_name = track_name.replace("<br />", " (")
					track_name = re.sub('<[^>]*>', '', track_name)
					track_name = track_name.strip()
					track_name = track_name+')'
				artist = re.sub('<[^>]*>', '', match[x][3])
				artist = artist.strip()
				artist = artist.replace("&amp;", "&")
				iconimage = match[x][1].replace('/44x44/','/300x300/')
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
			except: pass
	elif playlist_id == 'http://www.traxsource.com/scripts/builder.php/top/singles?rpc=1':
		codigo_fonte = abrir_url(playlist_id)
		match = re.findall('\<tr.*?\>.*?\<div class\="tnum"\>(.+?)\</div\>.*?\<td class\="thumb"\>.*?\<img.*?src\="(.+?)".*?\>.*?\</td\>.*?\<td class\="r\-pad"\>(.+?)\</td\>.*?\<td class\="r\-pad"\>(.+?)\</td\>.*?\</tr\>', codigo_fonte, re.DOTALL)
		for x in range(int(int(url)*items_per_page-items_per_page), int(int(url)*items_per_page)):
			try:
				track_number = match[x][0]
				track_name = match[x][2]
				if track_name.endswith('<span class="version"></span>'): #track without version name
					track_name = re.sub('<[^>]*>', '', track_name)
					track_name = track_name.strip()
				else: #track with version name
					track_name = track_name.replace("<br />", " (")
					track_name = re.sub('<[^>]*>', '', track_name)
					track_name = track_name.strip()
					track_name = track_name+')'
				artist = re.sub('<[^>]*>', '', match[x][3])
				artist = artist.strip()
				artist = artist.replace("&amp;", "&")
				iconimage = match[x][1].replace('/44x44/','/300x300/')
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+track_number+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
			except: pass
	if int(int(url)*items_per_page)<len(match): addDir(translate(30412),str(int(url)+1),24,addonfolder+artfolder+'next.png',playlist_id = playlist_id)

###################################################################################
#SEARCH AND LIST CONTENT

def Search_main():
	if not xbmcvfs.exists(os.path.join(datapath,'searchdata.txt')):
		keyb = xbmc.Keyboard('', translate(30600))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
			save(os.path.join(datapath,'searchdata.txt'),search_query)
		else: sys.exit(0)
	else: search_query = readfile(os.path.join(datapath,'searchdata.txt'))
	if search_query.startswith('tags:'):
		if search_query!='tags:':
			#playlists by tags
			if selfAddon.getSetting('hide_8tracks')=="false":
				codigo_fonte = abrir_url('http://8tracks.com/mix_sets/tags:'+urllib.quote(search_query[5:].replace(', ', '+').replace(',', '+'))+'.json?include=mixes+pagination&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
				decoded_data = json.loads(codigo_fonte)
				total_items = decoded_data['total_entries']
				if total_items>0: addDir(translate(30609)+str(total_items)+translate(30610),'1',32,'',search_query = search_query)
	else:
		#tracks
		codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=track.search&track='+urllib.quote(search_query)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		decoded_data = json.loads(codigo_fonte)
		try: total_items = decoded_data['results']['opensearch:totalResults']
		except: total_items = 0
		if int(total_items)>0: addDir(translate(30601)+str(total_items)+translate(30602),'1',26,'',search_query = search_query)
		#albums
		codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.search&album='+urllib.quote(search_query)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		decoded_data = json.loads(codigo_fonte)
		try: decoded_data['error']
		except:
			try:
				total_items = decoded_data['results']['opensearch:totalResults']
				if int(total_items)>0: addDir(translate(30603)+str(total_items)+translate(30604),'1',27,'',search_query = search_query)
			except: pass
		#toptracks
		codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.getTopTracks&artist='+urllib.quote(search_query)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		decoded_data = json.loads(codigo_fonte)
		try: total_items = decoded_data['toptracks']['@attr']['total']
		except:
			try: total_items = decoded_data['toptracks']['total']
			except: total_items = 0
		if int(total_items)>0: addDir(translate(30605)+str(total_items)+translate(30606),'1',29,'',search_query = search_query)
		#setlists
		try: codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/search/setlists.json?artistName='+urllib.quote(search_query))
		except urllib2.URLError, e: codigo_fonte = "not found"
		if codigo_fonte != "not found":
			decoded_data = json.loads(codigo_fonte)
			total_items = decoded_data['setlists']['@total']
			addDir(translate(30607)+str(total_items)+translate(30608),'1',30,'',search_query = search_query)
		#playlists
		if selfAddon.getSetting('hide_8tracks')=="false":
			try:
				codigo_fonte = abrir_url('http://8tracks.com/mix_sets/keyword:'+urllib.quote(search_query)+'.json?include=mixes+pagination&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
				decoded_data = json.loads(codigo_fonte)
				total_items = decoded_data['total_entries']
				if total_items>0: addDir(translate(30609)+str(total_items)+translate(30610),'1',32,'',search_query = search_query)
			except: pass
		#soundtracks
		if selfAddon.getSetting('hide_soundtrack')=="false":
			try:
				codigo_fonte = abrir_url('http://www.api.what-song.com/search?type=movie&field='+urllib.quote(search_query))
				decoded_data = json.loads(codigo_fonte)
				total_items = len(decoded_data['data'][0]['data'])
				if total_items>0: addDir(translate(30611)+str(total_items)+translate(30612),'',34,'',search_query = search_query)
			except:pass

def Search_by_tracks(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=track.search&track='+urllib.quote(search_query)+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['results']['trackmatches']['track']:
			artist = decoded_data['results']['trackmatches']['track']['artist'].encode("utf8")
			track_name = decoded_data['results']['trackmatches']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['results']['trackmatches']['track']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['results']['trackmatches']['track'])):
				artist = decoded_data['results']['trackmatches']['track'][x]['artist'].encode("utf8")
				track_name = decoded_data['results']['trackmatches']['track'][x]['name'].encode("utf8")
				try: iconimage = decoded_data['results']['trackmatches']['track'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
			total_items = decoded_data['results']['opensearch:totalResults']
			if int(url)*items_per_page<int(total_items): addDir(translate(30412),str(int(url)+1),26,addonfolder+artfolder+'next.png',search_query = search_query)
	except: pass
	
def Search_by_albums(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.search&album='+urllib.quote(search_query)+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['results']['albummatches']['album']:
			artist = decoded_data['results']['albummatches']['album']['artist'].encode("utf8")
			album_name = decoded_data['results']['albummatches']['album']['name'].encode("utf8")
			mbid = decoded_data['results']['albummatches']['album']['mbid'].encode("utf8")
			try: iconimage = decoded_data['results']['albummatches']['album']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir('[B]'+artist+'[/B] - '+album_name,mbid,28,iconimage,artist = artist,album = album_name,type = 'album')
		else:
			for x in range(0, len(decoded_data['results']['albummatches']['album'])):
				artist = decoded_data['results']['albummatches']['album'][x]['artist'].encode("utf8")
				album_name = decoded_data['results']['albummatches']['album'][x]['name'].encode("utf8")
				mbid = decoded_data['results']['albummatches']['album'][x]['mbid'].encode("utf8")
				try: iconimage = decoded_data['results']['albummatches']['album'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album_name,mbid,28,iconimage,artist = artist,album = album_name,type = 'album')
			total_items = decoded_data['results']['opensearch:totalResults']
			if int(url)*items_per_page<int(total_items): addDir(translate(30412),str(int(url)+1),27,addonfolder+artfolder+'next.png',search_query = search_query)
	except: pass

def List_album_tracks(url,artist,album):
	if url: codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.getInfo&mbid='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	else: codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=album.getInfo&artist='+urllib.quote(artist)+'&album='+urllib.quote(album)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	count = 0
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['album']['tracks']['track']:
			artist = decoded_data['album']['tracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['album']['tracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['album']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
			count += 1
		else:
			for x in range(0, len(decoded_data['album']['tracks']['track'])):
				artist = decoded_data['album']['tracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['album']['tracks']['track'][x]['name'].encode("utf8")
				try: iconimage = decoded_data['album']['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
				count += 1
	except: pass
	#if none result was found with last.fm api, we use 7digital api
	if artist and album and count==0:
		try:
			codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM xml WHERE url="http://api.7digital.com/1.2/release/search?q='+urllib.quote(artist+' '+album)+'&type=album&oauth_consumer_key=7drjpjvng4ph"') + '&format=json&diagnostics=true&callback=', timeout=30)
			decoded_data = json.loads(codigo_fonte)
			releaseid_xml = decoded_data['query']['results']['response']['searchResults']['searchResult'][0]['release']['id']
			title_xml = decoded_data['query']['results']['response']['searchResults']['searchResult'][0]['release']['title']
			artist_xml = decoded_data['query']['results']['response']['searchResults']['searchResult'][0]['release']['artist']['name']
			codigo_fonte = abrir_url_custom('http://query.yahooapis.com/v1/public/yql?q=' + urllib.quote_plus('SELECT * FROM xml WHERE url="http://api.7digital.com/1.2/release/tracks?releaseid='+releaseid_xml+'&oauth_consumer_key=7drjpjvng4ph&country=GB"') + '&format=json&diagnostics=true&callback=', timeout=30)
			decoded_data = json.loads(codigo_fonte)
			if artist.lower() == artist_xml.lower():
				for x in range(0, len(decoded_data['query']['results']['response']['tracks']['track'])):
					artist = decoded_data['query']['results']['response']['tracks']['track'][x]['artist']['name'].encode("utf8")
					track_name = decoded_data['query']['results']['response']['tracks']['track'][x]['title'].encode("utf8")
					try: iconimage = decoded_data['query']['results']['response']['tracks']['track'][x]['release']['image'].encode("utf8")
					except: iconimage = addonfolder+artfolder+'no_cover.png'
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,album = album,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
					count += 1
		except: pass

def Search_by_toptracks(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=artist.getTopTracks&artist='+urllib.quote(search_query)+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['toptracks']['track']:
			artist = decoded_data['toptracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['toptracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['toptracks']['track']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]1[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]1[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['toptracks']['track'])):
				artist = decoded_data['toptracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['toptracks']['track'][x]['name'].encode("utf8")
				#mbid = decoded_data['toptracks']['track'][x]['mbid'].encode("utf8")
				try: iconimage = decoded_data['toptracks']['track'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR yellow]'+str(((int(url)-1)*items_per_page)+x+1)+'[/COLOR] - [B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
			total_pages = decoded_data['toptracks']['@attr']['totalPages']
			if int(url)<int(total_pages): addDir(translate(30412),str(int(url)+1),29,addonfolder+artfolder+'next.png',search_query = search_query)
	except: pass

def Search_by_setlists(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = 20 #impossible to use a custom value currently
	codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/search/setlists.json?artistName='+urllib.quote(search_query)+'&p='+url)
	if codigo_fonte != "not found":
		decoded_data = json.loads(codigo_fonte)
		try:
			#checks if output has only an object or various and proceeds according
			if 'artist' in decoded_data['setlists']['setlist']:
				date = decoded_data['setlists']['setlist']['@eventDate'].encode("utf8")
				artist = decoded_data['setlists']['setlist']['artist']['@name'].encode("utf8")
				location = decoded_data['setlists']['setlist']['venue']['@name'].encode("utf8")
				id = decoded_data['setlists']['setlist']['@id'].encode("utf8")
				iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+location+' ('+date+')',id,31,iconimage,type='setlist')
			else:
				for x in range(0, len(decoded_data['setlists']['setlist'])):
					date = decoded_data['setlists']['setlist'][x]['@eventDate'].encode("utf8")
					artist = decoded_data['setlists']['setlist'][x]['artist']['@name'].encode("utf8")
					location = decoded_data['setlists']['setlist'][x]['venue']['@name'].encode("utf8")
					id = decoded_data['setlists']['setlist'][x]['@id'].encode("utf8")
					iconimage = addonfolder+artfolder+'no_cover.png'
					addDir('[B]'+artist+'[/B] - '+location+' ('+date+')',id,31,iconimage,artist = artist,type='setlist')
				total_items = decoded_data['setlists']['@total']
				if int(url)*items_per_page<int(total_items): addDir(translate(30412),str(int(url)+1),30,addonfolder+artfolder+'next.png',search_query = search_query)
		except: pass

def List_setlist_tracks(url):
	codigo_fonte = abrir_url('http://api.setlist.fm/rest/0.1/setlist/'+url+'.json')
	decoded_data = json.loads(codigo_fonte)
	try:
		artist = decoded_data['setlist']['artist']['@name'].encode("utf8")
		for x in range(0, len(decoded_data['setlist']['sets']['set']['song'])):
			track_name = decoded_data['setlist']['sets']['set']['song'][x]['@name'].encode("utf8")
			iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
	except: pass

def Search_8tracks_playlists(url,search_query):
	if search_query==None:
		keyb = xbmc.Keyboard('', translate(30613))
		keyb.doModal()
		if (keyb.isConfirmed()):
			search_query = keyb.getText()
			if search_query=='': sys.exit(0)
		else: sys.exit(0)
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	if search_query.startswith('tags:'): codigo_fonte = abrir_url('http://8tracks.com/mix_sets/tags:'+urllib.quote(search_query[5:].replace(', ', '+').replace(',', '+'))+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
	else: codigo_fonte = abrir_url('http://8tracks.com/mix_sets/keyword:'+urllib.quote(search_query)+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['mixes'])):
		username = decoded_data['mixes'][x]['user']['login'].encode("utf8")
		playlist_name = decoded_data['mixes'][x]['name'].encode("utf8")
		tracks_count = str(decoded_data['mixes'][x]['tracks_count'])
		playlist_id = str(decoded_data['mixes'][x]['id'])
		try: iconimage = decoded_data['mixes'][x]['cover_urls']['max200'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir('[B]'+username+'[/B] - '+playlist_name+' [I]('+tracks_count+' tracks)[/I]','1',33,iconimage,playlist_id = playlist_id,type='playlist')
	total_pages = decoded_data['total_pages']
	if int(url)<int(total_pages): addDir(translate(30412),str(int(url)+1),32,addonfolder+artfolder+'next.png',search_query = search_query)

def List_8tracks_tracks(url,iconimage,playlist_id):
	#official resolver method - more stable but no cache
	last_track = 0
	total_tracks = int(json.loads(abrir_url('http://8tracks.com/mixes/'+playlist_id+'.json?api_key=e165128668b69291bf8081dd743fa6b832b4f477&api_version=3'))['mix']['tracks_count'])
	play_token = json.loads(abrir_url('http://8tracks.com/sets/new.json&api_key=e165128668b69291bf8081dd743fa6b832b4f477&api_version=3'))['play_token']
	progress = xbmcgui.DialogProgress()
	progress.create(translate(30400),translate(30614))
	progress.update(0)
	playlist = xbmc.PlayList(1)
	playlist.clear()
	if progress.iscanceled(): sys.exit(0)
	#load first track
	codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/play.json?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477')
	decoded_data = json.loads(codigo_fonte)
	progress.update(int(((0)*100)/(total_tracks)),translate(30614),translate(30615)+str(last_track+1)+translate(30616)+str(total_tracks))
	artist = decoded_data['set']['track']['performer'].encode("utf8")
	track_name = decoded_data['set']['track']['name'].encode("utf8")
	link = decoded_data['set']['track']['url'].encode("utf8")
	addLink('[B]'+artist+'[/B] - '+track_name,link,100,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,songinfo = False,type = 'song')
	duration = int(decoded_data['set']['track']['play_duration'])
	listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
	listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
	playlist.add(link,listitem)
	if progress.iscanceled(): sys.exit(0)
	xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(playlist) #lets try to force a player to avoid no codec error
	#load remaining tracks
	if (last_track+1)<total_tracks:
		for x in range(last_track+1, total_tracks):
			try: codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/next?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477&format=jsonh&api_version=2')
			except urllib2.HTTPError, e: codigo_fonte = e.fp.read() #bypass 403 error
			decoded_data = json.loads(codigo_fonte)
			if progress.iscanceled(): sys.exit(0)
			try:
				progress.update(int(((x)*100)/(total_tracks)),translate(30614),translate(30615)+str(x+1)+translate(30616)+str(total_tracks))
				artist = decoded_data['set']['track']['performer'].encode("utf8")
				track_name = decoded_data['set']['track']['name'].encode("utf8")
				link = decoded_data['set']['track']['url'].encode("utf8")
				addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,songinfo = False,type = 'song')
				duration = int(decoded_data['set']['track']['play_duration'])
				listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
				listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
				playlist.add(link,listitem)
				print 'Debug: carregado track '+str(x)+' from official2'
			except:
				if decoded_data['status']=='403 Forbidden':
					for y in range((duration/2)+7, 0, -1):
						time.sleep(1)
						progress.update(int(((x)*100)/(total_tracks)),translate(30614),translate(30615)+str(x+1)+translate(30616)+str(total_tracks),translate(30617)+str(y)+translate(30618))
						if progress.iscanceled(): sys.exit(0)
					try:
						try: codigo_fonte = abrir_url('http://8tracks.com/sets/'+play_token+'/next?mix_id='+playlist_id+'&api_key=e165128668b69291bf8081dd743fa6b832b4f477&format=jsonh&api_version=2')
						except urllib2.HTTPError, e: codigo_fonte = e.fp.read() #bypass 403 error
						decoded_data = json.loads(codigo_fonte)
						progress.update(int(((x)*100)/(total_tracks)),translate(30614),translate(30615)+str(x+1)+translate(30616)+str(total_tracks))
						artist = decoded_data['set']['track']['performer'].encode("utf8")
						track_name = decoded_data['set']['track']['name'].encode("utf8")
						link = decoded_data['set']['track']['url'].encode("utf8")
						addLink('[B]'+artist+'[/B] - '+track_name,link,39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,manualsearch = False,songinfo = False,type = 'song')
						duration = int(decoded_data['set']['track']['play_duration'])
						listitem = xbmcgui.ListItem('[B]'+artist+'[/B] - '+track_name, thumbnailImage=iconimage)
						listitem.setInfo('music', {'Title':track_name, 'Artist':artist, 'duration':duration})
						playlist.add(link,listitem)
						print 'Debug: carregado track '+str(x)+' from official3'
					except:
						dialog = xbmcgui.Dialog()
						ok = dialog.ok(translate(30400), translate(30619))
						break
	if progress.iscanceled(): sys.exit(0)
	progress.update(100)
	progress.close()

def Search_whatsong_soundtrack(search_query):
	#items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://www.api.what-song.com/search?type=movie&field='+urllib.quote(search_query))
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['data'][0]['data'])):
		try:
			name = decoded_data['data'][0]['data'][x]['title'].encode("utf8")
			movie_id = str(decoded_data['data'][0]['data'][x]['_id'])
			iconimage = "http://www.what-song.com/images/posters/"+movie_id+".jpg"
			addDir(name,movie_id,8,iconimage,type='soundtrack')
		except: pass

def Search_by_similartracks(artist,track_name):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=track.getSimilar&artist='+urllib.quote(artist)+'&track='+urllib.quote(track_name)+'&limit='+str(items_per_page)+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'name' in decoded_data['similartracks']['track']:
			artist = decoded_data['similartracks']['track']['artist']['name'].encode("utf8")
			track_name = decoded_data['similartracks']['track']['name'].encode("utf8")
			try: iconimage = decoded_data['similartracks']['track']['image'][3]['#text'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['similartracks']['track'])):
				artist = decoded_data['similartracks']['track'][x]['artist']['name'].encode("utf8")
				track_name = decoded_data['similartracks']['track'][x]['name'].encode("utf8")
				try: iconimage = decoded_data['similartracks']['track'][x]['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
	except: pass

def Search_videoclip(artist,track_name,album):
	try:	
		search_string = urllib.quote(artist + ' ' + track_name + ' music video')
		codigo_fonte = abrir_url("https://www.googleapis.com/youtube/v3/search?part=id%2Csnippet&q="+ search_string +"&type=Music&maxResults=1&key=AIzaSyBbDY0UzvF5Es77M7S1UChMzNp0KsbaDPI")
	except: codigo_fonte = ''
	if codigo_fonte:
		try:
			match = re.compile('"videoId": "(.+?)"').findall(codigo_fonte)
		except: match = []
		if match:
			print 'Grabbed youtube id',match[0]
			video_path = "plugin://plugin.video.youtube/play/?video_id="+match[0] 
			if selfAddon.getSetting('playing_type') == "0": #context menu
				xbmc.Player().play(video_path)
			elif selfAddon.getSetting('playing_type') == "1": #atraci like behavior
				item = xbmcgui.ListItem(path=video_path)
				item.setInfo(type="music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)		
		else: 
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400), translate(30622))

###################################################################################
#DOWNLOADS AND RESOLVERS

def List_my_songs(search_query):
	#Note: search_query is the relative path
	if selfAddon.getSetting('downloads_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30800))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		if search_query: search_query = os.path.join(selfAddon.getSetting('downloads_folder'), search_query)
		else: search_query = selfAddon.getSetting('downloads_folder')
		dirs = os.listdir(search_query)
		tmp_list = []
		for filename in dirs:
			if not os.path.isdir(os.path.join(search_query, filename)):
				extension = os.path.splitext(filename)[1]
				if extension in ['.mp3','.m4a','.wma','.wav','.aac','.ape','.flac']:
					tmp_list.append(filename)
			else:
				try: addDir('[B]'+filename.decode('latin-1').encode("utf8")+'[/B]','',38,'',search_query = os.path.join(search_query, filename))
				except: addDir('[B]'+filename+'[/B]','',38,'',search_query = os.path.join(search_query, filename))
		for filename in tmp_list:
			try: musicfile = mutagen.id3.ID3(os.path.join(search_query, filename))
			except: musicfile = None
			try: artist = musicfile.getall('TPE1')[0][0].encode("utf8")
			except: artist = None
			try: track_name = musicfile.getall('TIT2')[0][0].encode("utf8")
			except: track_name = None
			try: album = musicfile.getall('TALB')[0][0].encode("utf8")
			except: album = None
			if artist and track_name:
				try: addLink(filename.decode('latin-1').encode("utf8"),os.path.join(search_query, filename).decode('latin-1').encode("utf8"),39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,album = album,type = 'mymusic')
				except: addLink(filename.decode('latin-1').encode("utf8"),os.path.join(search_query, filename),39,addonfolder+artfolder+'no_cover.png',artist = artist,track_name = track_name,album = album,type = 'mymusic')
			else:
				try: addLink(filename.decode('latin-1').encode("utf8"),os.path.join(search_query, filename).decode('latin-1').encode("utf8"),39,addonfolder+artfolder+'no_cover.png',type = 'mymusic')
				except: addLink(filename.decode('latin-1').encode("utf8"),os.path.join(search_query, filename),39,addonfolder+artfolder+'no_cover.png',type = 'mymusic')

def Get_songfile_from_name(artist,track_name,duration=False):
	cj = cookielib.LWPCookieJar()
	cj.load(VKCookie)
	#perform search
	post = {'_ajax':'1'}
	data = urllib.urlencode(post)
	req = urllib2.Request('https://m.vk.com/audio?act=search&q='+urllib.quote(artist+' '+track_name)+'&offset=0',data)
	req.add_header('Content-Type', 'application/x-www-form-urlencoded')
	req.add_header('X-Requested-With', 'XMLHttpRequest')
	req.add_header('User-Agent', VK_useragent)
	openervk = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	response = openervk.open(req)
	source = response.read()
	try:
		url=re.compile('\\"(https?.*?\.mp3.*?)\\"').findall(source)[0]
		url=url.replace('\/','/')+"|User-Agent="+urllib.quote(VK_useragent)
		try: dur = re.compile('data-dur.*?"([\d]+)').findall(source)[0]
		except: dur = 0
		if duration: return dur,url
		else: return url
	except:
		if duration: return 0, 'track_not_found'
		else: return 'track_not_found'

def Resolve_songfile(url,artist,track_name,album,iconimage):
	#if a url is provided, the function reproduce it
	#else it gets the file from vk.com API using the artist and track_name info
	success = True
	if url=='' or url==None:
		cj = cookielib.LWPCookieJar()
		cj.load(VKCookie)
		#perform search
		post = {'_ajax':'1'}
		data = urllib.urlencode(post)
		req = urllib2.Request('https://m.vk.com/audio?act=search&q='+urllib.quote(artist+' '+track_name)+'&offset=0',data)
		req.add_header('Content-Type', 'application/x-www-form-urlencoded')
		req.add_header('X-Requested-With', 'XMLHttpRequest')
		req.add_header('User-Agent', VK_useragent)
		openervk = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		response = openervk.open(req)
		source = response.read()
		try:
			url=re.compile('\\"(https?.*?\.mp3.*?)\\"').findall(source)[0]
			url=url.replace('\/','/')+"|User-Agent="+urllib.quote(VK_useragent)
		except:
			url=''
			success = False
		item = xbmcgui.ListItem(path=url)
		item.setInfo(type="Music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)
	else:
		item = xbmcgui.ListItem(path=url)
		item.setInfo(type="Music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), success, item)

def Download_songfile(url,artist,track_name):
	if selfAddon.getSetting('downloads_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30800))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		if url=="track_not_found":
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400),translate(30802))
			return
		elif url=='':
			url = Get_songfile_from_name(artist,track_name)
			if url=="track_not_found":
				dialog = xbmcgui.Dialog()
				ok = dialog.ok(translate(30400),translate(30802))
				return
		#get file extension
		if "|" in url: temp_url = url.split("|")[0]
		else: temp_url = url
		try: file_extension = re.findall('(\.[A-Za-z0-9]+).*?', temp_url)[-1]
		except: file_extension = '.mp3'
		#get the name
		name = artist+' - '+track_name
		name = re.sub('[<>:"/\|?*]', '', name) #remove not allowed characters in the filename
		params = { "url": url, "download_path": selfAddon.getSetting('downloads_folder'), "Title": name }
		downloader.download(name.decode("utf-8")+file_extension, params, async=False)

def Download_whole_album(artist,album,url,country,iconimage):
	if selfAddon.getSetting('downloads_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30800))
		xbmcaddon.Addon(addon_id).openSettings()
	if not xbmcvfs.exists(os.path.join(selfAddon.getSetting('downloads_folder'),artist+' - '+album)):
		xbmcvfs.mkdir(os.path.join(selfAddon.getSetting('downloads_folder'),artist+' - '+album))
		albumfolder = os.path.join(selfAddon.getSetting('downloads_folder'),artist+' - '+album)
	else:
		count = 2
		while xbmcvfs.exists(os.path.join(selfAddon.getSetting('downloads_folder'),artist+' - '+album+' ('+str(count)+')')):
			count += 1
		xbmcvfs.mkdir(os.path.join(selfAddon.getSetting('downloads_folder'),artist+' - '+album+' ('+str(count)+')'))
		albumfolder = os.path.join(selfAddon.getSetting('downloads_folder'),artist+' - '+album+' ('+str(count)+')')
	progress = xbmcgui.DialogProgress()
	progress.create(translate(30400),translate(30818))
	progress.update(0)
	#albums from itunes charts
	if country: json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory" : "plugin://'+addon_id+'/?mode=17&url='+url+'&album='+album+'&country='+country+'"}, "id": 1 }')
	#other albums from last.fm/7digital
	else: json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory" : "plugin://'+addon_id+'/?mode=28&url='+url+'&artist='+artist+'&album='+album+'"}, "id": 1 }')
	decoded_data = json.loads(json_response)
	if 'files' in decoded_data['result']:
		total_items = len(decoded_data['result']['files'])
		for x in range(0, total_items):
			if progress.iscanceled(): progress.close(); sys.exit(0)
			progress.update(int((x)*100/total_items),translate(30818),translate(30819)+str(x+1)+translate(30820)+str(total_items))
			params_list = eval(str(urlparse.parse_qs(decoded_data['result']['files'][x]['file'].split('?',1)[1].decode('string_escape'))))
			artist = params_list['artist'][0].decode('string_escape')
			track_name = params_list['track_name'][0].decode('string_escape')
			name = artist+' - '+track_name
			url = Get_songfile_from_name(artist,track_name)
			if url!="track_not_found":
				#get file extension
				if "|" in url: temp_url = url.split("|")[0]
				else: temp_url = url
				try: file_extension = re.findall('(\.[A-Za-z0-9]+).*?', temp_url)[-1]
				except: file_extension = '.mp3'
				#get the name
				name = re.sub('[<>:"/\|?*]', '', name) #remove not allowed characters in the filename
				params = { "url": url, "download_path": albumfolder, "Title": name }
				downloader.download(name.decode("utf-8")+file_extension, params, async=False)
				#properly tag the downloaded album
				try: musicfile = MP3(os.path.join(albumfolder, name+file_extension).decode('utf8').encode("latin-1"))
				except: musicfile = MP3(os.path.join(albumfolder, name+file_extension).decode('utf8'))
				try: musicfile.add_tags()
				except mutagen.id3.error:
					musicfile.delete()
					musicfile.save()
					try: musicfile = MP3(os.path.join(albumfolder, name+file_extension).decode('utf8').encode("latin-1"))
					except: musicfile = MP3(os.path.join(albumfolder, name+file_extension).decode('utf8'))
					musicfile.add_tags()
				musicfile.tags.add(mutagen.id3.TRCK(encoding=3, text=str(x+1).encode("utf8"))) #Track Number
				musicfile.tags.add(mutagen.id3.TIT2(encoding=3, text=unicode(track_name, 'utf8'))) #Track Title
				musicfile.tags.add(mutagen.id3.TALB(encoding=3, text=unicode(album, 'utf8'))) #Album Title
				musicfile.tags.add(mutagen.id3.TPE1(encoding=3, text=unicode(artist, 'utf8'))) #Lead Artist/Performer/Soloist/Group
				try: cover_extension = re.findall('(\.[A-Za-z0-9]+).*?', iconimage)[-1]
				except: cover_extension = ''
				if cover_extension == '.png': musicfile.tags.add(mutagen.id3.APIC(encoding=3, mime='image/png', type=3, desc=u'Cover', data=urllib2.urlopen(iconimage).read()))
				elif cover_extension == '.jpg': musicfile.tags.add(mutagen.id3.APIC(encoding=3, mime='image/jpg', type=3, desc=u'Cover', data=urllib2.urlopen(iconimage).read()))
				musicfile.save()
		if progress.iscanceled(): progress.close(); sys.exit(0)
		progress.update(100)
		progress.close()
	else:
		progress.update(100)
		progress.close()
		os.rmdir(albumfolder)
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30821))

def Export_as_m3u(name,artist,album,url,country,iconimage,type):
	if selfAddon.getSetting('library_folder')=='':
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30822))
		xbmcaddon.Addon(addon_id).openSettings()
	else:
		if type=='album' or type=='fav_album':
			file_content = "#EXTM3U\n"
			#albums from itunes charts
			if country: json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory" : "plugin://'+addon_id+'/?mode=17&url='+url+'&album='+album+'&country='+country+'"}, "id": 1 }')
			#other albums from last.fm/7digital
			else: json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory" : "plugin://'+addon_id+'/?mode=28&url='+url+'&artist='+artist+'&album='+album+'"}, "id": 1 }')
			decoded_data = json.loads(json_response)
			if 'files' in decoded_data['result']:
				total_items = len(decoded_data['result']['files'])
				for x in range(0, total_items):
					params_list = eval(str(urlparse.parse_qs(decoded_data['result']['files'][x]['file'].split('?',1)[1].decode('string_escape'))))
					artist = params_list['artist'][0].decode('string_escape')
					track_name = params_list['track_name'][0].decode('string_escape')
					if len(str(total_items)) <= 2:
						file_content += "#EXTINF:0,"+str(x+1).rjust(2, '0')+". "+artist+" - "+track_name+"\nplugin://plugin.audio.musicbox/?mode=300&artist="+urllib.quote_plus(artist)+"&track_name="+urllib.quote_plus(track_name)+"\n"
					else:
						file_content += "#EXTINF:0,"+str(x+1).rjust(len(str(total_items)), '0')+". "+artist+" - "+track_name+"\nplugin://plugin.audio.musicbox/?mode=300&artist="+urllib.quote_plus(artist)+"&track_name="+urllib.quote_plus(track_name)+"\n"
			save(os.path.join(selfAddon.getSetting('library_folder'),str(artist+' - '+album+'.m3u').decode("utf8").encode("latin-1")),file_content)
			if selfAddon.getSetting('save_library_tbn')=="true":
				f = open(os.path.join(selfAddon.getSetting('library_folder'),str(artist+' - '+album+'.tbn').decode("utf8").encode("latin-1")),'wb')
				f.write(urllib2.urlopen(iconimage).read())
				f.close()
			notification(artist+' - '+album,translate(30824),'4000',iconimage)
		elif type=='setlist' or type=='fav_setlist':
			file_content = "#EXTM3U\n"
			json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory" : "plugin://'+addon_id+'/?mode=31&url='+url+'"}, "id": 1 }')
			decoded_data = json.loads(json_response)
			if 'files' in decoded_data['result']:
				total_items = len(decoded_data['result']['files'])
				for x in range(0, total_items):
					params_list = eval(str(urlparse.parse_qs(decoded_data['result']['files'][x]['file'].split('?',1)[1].decode('string_escape'))))
					artist = params_list['artist'][0].decode('string_escape')
					track_name = params_list['track_name'][0].decode('string_escape')
					file_content += "#EXTINF:0,"+artist+" - "+track_name+"\nplugin://plugin.audio.musicbox/?mode=300&artist="+urllib.quote_plus(artist)+"&track_name="+urllib.quote_plus(track_name)+"\n"
			save(os.path.join(selfAddon.getSetting('library_folder'),str(re.sub("\[/?(?:COLOR|B|I)[^]]*\]", "", name)+'.m3u').decode("utf8").encode("latin-1")),file_content)
			notification(re.sub("\[/?(?:COLOR|B|I)[^]]*\]", "", name),translate(30824),'4000','')
		elif type=='soundtrack' or type=='fav_soundtrack':
			file_content = "#EXTM3U\n"
			json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Files.GetDirectory", "params": {"directory" : "plugin://'+addon_id+'/?mode=8&url='+url+'"}, "id": 1 }')
			decoded_data = json.loads(json_response)
			if 'files' in decoded_data['result']:
				total_items = len(decoded_data['result']['files'])
				for x in range(0, total_items):
					params_list = eval(str(urlparse.parse_qs(decoded_data['result']['files'][x]['file'].split('?',1)[1].decode('string_escape'))))
					artist = params_list['artist'][0].decode('string_escape')
					track_name = params_list['track_name'][0].decode('string_escape')
					file_content += "#EXTINF:0,"+artist+" - "+track_name+"\nplugin://plugin.audio.musicbox/?mode=300&artist="+urllib.quote_plus(artist)+"&track_name="+urllib.quote_plus(track_name)+"\n"
			save(os.path.join(selfAddon.getSetting('library_folder'),name+'.m3u'),file_content)
			if selfAddon.getSetting('save_library_tbn')=="true":
				f = open(os.path.join(selfAddon.getSetting('library_folder'),name+'.tbn'),'wb')
				f.write(urllib2.urlopen(iconimage).read())
				f.close()
			notification(name,translate(30824),'4000',iconimage)

def Song_info(url,artist,track_name,duration):
	if url:
		#non-vk audio files
		if url.startswith('http://') or url.startswith('https://') and duration:
			size = urllib.urlopen(url).info()['content-length']
		else: #song info not available
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400),translate(30813))
			return
	else:
		duration, url = Get_songfile_from_name(artist,track_name,True)
		if url!="track_not_found":
			if "|" in url: url = url.split("|")[0]
			size = urllib.urlopen(url).info()['content-length']
		else:
			dialog = xbmcgui.Dialog()
			ok = dialog.ok(translate(30400),translate(30802))
			return
	if size:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30814)+str(duration)+' s',translate(30815)+str(round(((float(size)/1024)/1024),2))+' MB',translate(30816)+str(int(round(float(size)*8/int(duration)/1000,0)))+' kbps')

def Artist_info(artist):
	apiKey = '7jxr9zggt45h6rg2n4ss3mrj'
	apiSecret = 'XUnYutaAW6'
	apiSig =  hashlib.md5(apiKey+apiSecret+str(int(time.time()))).hexdigest()
	bio_text = ''
	try: codigo_fonte = abrir_url('http://api.rovicorp.com/data/v1.1/name/info?apikey='+apiKey+'&sig='+apiSig+'&name='+urllib.quote(artist)+'&include=musicbio,aliases,memberof,groupmembers,musicstyles')
	except urllib2.HTTPError, error: codigo_fonte = '{}'
	decoded_data = json.loads(codigo_fonte)
	if 'name' in decoded_data:
		bio_text += translate(30827)+decoded_data['name']['name'].encode('utf-8')+'\n'
		if decoded_data['name']['active']:
			if len(decoded_data['name']['active'])==1:
				bio_text += translate(30828)+decoded_data['name']['active'][0].encode('utf-8')+'\n' #Name
			elif len(decoded_data['name']['active'])>1:
				bio_text += translate(30828)+decoded_data['name']['active'][0].encode('utf-8')+' - '+decoded_data['name']['active'][len(decoded_data['name']['active'])-1].encode('utf-8')+'\n' #Active
		if decoded_data['name']['isGroup'] == False:
			if decoded_data['name']['birth']['date']:
				if decoded_data['name']['birth']['place']: bio_text += translate(30829)+decoded_data['name']['birth']['date'].encode('utf-8')+translate(30840)+decoded_data['name']['birth']['place'].encode('utf-8')+'\n' #Born
				else: bio_text += translate(30829)+decoded_data['name']['birth']['date'].encode('utf-8')+'\n' #Born
			if decoded_data['name']['death']['date']:
				if decoded_data['name']['death']['place']: bio_text += translate(30830)+decoded_data['name']['death']['date'].encode('utf-8')+translate(30840)+decoded_data['name']['death']['place'].encode('utf-8')+'\n' #Death
				else: bio_text += translate(30830)+decoded_data['name']['death']['date'].encode('utf-8')+'\n' #Death
		elif decoded_data['name']['isGroup'] == True:
			if decoded_data['name']['birth']['date']:
				if decoded_data['name']['birth']['place']: bio_text += translate(30831)+decoded_data['name']['birth']['date'].encode('utf-8')+translate(30840)+decoded_data['name']['birth']['place'].encode('utf-8')+'\n' #Formed
				else: bio_text += translate(30831)+decoded_data['name']['birth']['date']+'\n' #Formed
			if decoded_data['name']['death']['date']:
				if decoded_data['name']['death']['place']: bio_text += translate(30832)+decoded_data['name']['death']['date'].encode('utf-8')+translate(30840)+decoded_data['name']['death']['place'].encode('utf-8')+'\n' #Disbanded
				else: bio_text += translate(30832)+decoded_data['name']['death']['date'].encode('utf-8')+'\n' #Disbanded
		if decoded_data['name']['musicGenres'] and len(decoded_data['name']['musicGenres'])>0:
			bio_text += translate(30833) #Genre
			for x in range(0,len(decoded_data['name']['musicGenres'])):
				bio_text += decoded_data['name']['musicGenres'][x]['name'].encode('utf-8')+', '
			bio_text = bio_text[:-2] # remove last ', '
			bio_text += '\n'
		if decoded_data['name']['musicStyles'] and len(decoded_data['name']['musicStyles'])>0:
			tmp_list = []
			musicstyles_list = []
			for x in range(0,len(decoded_data['name']['musicGenres'])):
				tmp_list.append(decoded_data['name']['musicGenres'][x]['name'])
			for x in range(0,len(decoded_data['name']['musicStyles'])):
				if decoded_data['name']['musicStyles'][x]['name'] not in tmp_list:
					musicstyles_list.append(decoded_data['name']['musicStyles'][x]['name'])
			if len(musicstyles_list)>0:
				bio_text += translate(30834) #Styles
				for x in range(0,len(musicstyles_list)):
					bio_text += musicstyles_list[x].encode('utf-8')+', '
				bio_text = bio_text[:-2] # remove last ', '
				bio_text += '\n'
		if decoded_data['name']['isGroup'] == True:
			if decoded_data['name']['groupMembers'] and len(decoded_data['name']['groupMembers'])>0:
				bio_text += translate(30835) #Group Members
				for x in range(0,len(decoded_data['name']['groupMembers'])):
					bio_text += decoded_data['name']['groupMembers'][x]['name'].encode('utf-8')+', '
				bio_text = bio_text[:-2] # remove last ', '
				bio_text += '\n'
		elif decoded_data['name']['isGroup'] == False:
			if decoded_data['name']['aliases'] and len(decoded_data['name']['aliases'])>0:
				bio_text += translate(30836) #Also Known As
				for x in range(0,len(decoded_data['name']['aliases'])):
					bio_text += decoded_data['name']['aliases'][x].encode('utf-8')+', '
				bio_text = bio_text[:-2] # remove last ', '
				bio_text += '\n'
			if decoded_data['name']['memberOf'] and len(decoded_data['name']['memberOf'])>0:
				bio_text += translate(30837) #Member Of
				for x in range(0,len(decoded_data['name']['memberOf'])):
					bio_text += decoded_data['name']['memberOf'][x]['name'].encode('utf-8')+', '
				bio_text = bio_text[:-2] # remove last ', '
				bio_text += '\n'
		if decoded_data['name']['musicBio']:
			bio_text += '\n'+translate(30838)+re.sub("(\[/?roviLink.*?\])", "",decoded_data['name']['musicBio']['text']).encode('utf-8').replace("[muzeItalic]", "[I]").replace("[/muzeItalic]", "[/I]") #Biography
		else:
			bio_text = translate(30839) #No info found...
	else:
		bio_text += translate(30839) #No info found...
	xbmc.executebuiltin("ActivateWindow(10147)")
	window = xbmcgui.Window(10147)
	xbmc.sleep(100)
	window.getControl(1).setLabel("%s - %s - %s" % (translate(30400),translate(30826),artist))
	window.getControl(5).setText(bio_text)

###################################################################################
#FAVORITES

#Info: version_fav is used to check/update favorites struture in future (if necessary)
#Current version: 0.01

def Favorites_menu():
	addDir(translate(30701),'songs',45,'')
	addDir(translate(30702),'albums',45,'')
	addDir(translate(30703),'setlists',45,'')
	addDir(translate(30704),'playlists',45,'')
	addDir(translate(30705),'soundtracks',45,'')

def List_favorites(url):
	favoritesfile = os.path.join(datapath,"favorites.json")
	if not xbmcvfs.exists(favoritesfile): save(favoritesfile,"{\n  \"albums\": [], \n  \"playlists\": [], \n  \"setlists\": [], \n  \"soundtracks\": [], \n  \"songs\": [], \n  \"version_fav\": 0.01\n}")
	favorites_json = readfile(favoritesfile)
	decoded_data = json.loads(favorites_json)
	if url=='songs':
		for x in range(0, len(decoded_data['songs'])):
			if decoded_data['songs'][x]['type'].encode("utf8")=='vk.com': #get the direct link for a specific vk.com audio file id
				artist = decoded_data['songs'][x]['artist'].encode("utf8")
				track_name = decoded_data['songs'][x]['track_name'].encode("utf8")
				if decoded_data['songs'][x]['iconimage']: iconimage = decoded_data['songs'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addLink('[B]'+artist+'[/B] - '+track_name,url,39,iconimage,artist = artist,track_name = track_name,duration = duration,manualsearch = False,item_id = str(x),type='fav_song')
			elif decoded_data['songs'][x]['type'].encode("utf8")=='default': #call default song resolver method
				artist = decoded_data['songs'][x]['artist'].encode("utf8")
				track_name = decoded_data['songs'][x]['track_name'].encode("utf8")
				url = decoded_data['songs'][x]['url'].encode("utf8")
				if decoded_data['songs'][x]['iconimage']: iconimage = decoded_data['songs'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				if url or selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,url,39,iconimage,artist = artist,track_name = track_name,item_id = str(x),type='fav_song')
				else: addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,search_query = artist+' '+track_name,item_id = str(x),type='fav_song')
	elif url=='albums':
		for x in range(0, len(decoded_data['albums'])):
			if decoded_data['albums'][x]['provider'].encode("utf8")=='itunes': #albums from itunes charts
				artist = decoded_data['albums'][x]['artist'].encode("utf8")
				album = decoded_data['albums'][x]['album'].encode("utf8")
				country = decoded_data['albums'][x]['country'].encode("utf8")
				url = decoded_data['albums'][x]['url'].encode("utf8")
				if decoded_data['albums'][x]['iconimage']: iconimage = decoded_data['albums'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album,url,17,iconimage,album = album,artist = artist,country = country,item_id = str(x),type='fav_album')
			elif decoded_data['albums'][x]['provider'].encode("utf8")=='default': #other albums from last.fm/7digital
				artist = decoded_data['albums'][x]['artist'].encode("utf8")
				album = decoded_data['albums'][x]['album'].encode("utf8")
				url = decoded_data['albums'][x]['url'].encode("utf8")
				if decoded_data['albums'][x]['iconimage']: iconimage = decoded_data['albums'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album,url,28,iconimage,artist = artist,album = album,item_id = str(x),type='fav_album')
	elif url=='setlists':
		for x in range(0, len(decoded_data['setlists'])):
			name = decoded_data['setlists'][x]['name'].encode("utf8")
			artist = decoded_data['setlists'][x]['artist'].encode("utf8")
			url = decoded_data['setlists'][x]['url'].encode("utf8")
			if decoded_data['setlists'][x]['iconimage']: iconimage = decoded_data['setlists'][x]['iconimage'].encode("utf8")
			else: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir(name,url,31,iconimage,artist = artist,item_id = str(x),type='fav_setlist')
	elif url=='playlists':
		for x in range(0, len(decoded_data['playlists'])):
			if decoded_data['playlists'][x]['provider'].encode("utf8")=='digster': #playlists from digster
				name = decoded_data['playlists'][x]['name'].encode("utf8")
				url = decoded_data['playlists'][x]['playlist_id'].encode("utf8")
				country = decoded_data['playlists'][x]['country'].encode("utf8")
				if decoded_data['playlists'][x]['iconimage']: iconimage = decoded_data['playlists'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir(name,url,6,iconimage,country = country,item_id = str(x),type='fav_playlist')
			elif decoded_data['playlists'][x]['provider'].encode("utf8")=='last.fm': #playlists from last.fm
				name = decoded_data['playlists'][x]['name'].encode("utf8")
				playlist_id = decoded_data['playlists'][x]['playlist_id'].encode("utf8")
				if decoded_data['playlists'][x]['iconimage']: iconimage = decoded_data['playlists'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir(name,'',51,iconimage,playlist_id = playlist_id,item_id = str(x),type = 'fav_playlist')
			elif decoded_data['playlists'][x]['provider'].encode("utf8")=='8tracks': #playlists from 8tracks
				name = decoded_data['playlists'][x]['name'].encode("utf8")
				playlist_id = decoded_data['playlists'][x]['playlist_id'].encode("utf8")
				if decoded_data['playlists'][x]['iconimage']: iconimage = decoded_data['playlists'][x]['iconimage'].encode("utf8")
				else: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir(name,'1',33,iconimage,playlist_id = playlist_id,item_id = str(x),type='fav_playlist')
	elif url=='soundtracks':
		for x in range(0, len(decoded_data['soundtracks'])):
			name = decoded_data['soundtracks'][x]['name'].encode("utf8")
			url = decoded_data['soundtracks'][x]['url'].encode("utf8")
			if decoded_data['soundtracks'][x]['iconimage']: iconimage = decoded_data['soundtracks'][x]['iconimage'].encode("utf8")
			else: iconimage = addonfolder+artfolder+'no_cover.png'
			addDir(name,url,8,iconimage,item_id = str(x),type='fav_soundtrack')

def Add_to_favorites(type,artist,album,country,name,playlist_id,track_name,url,iconimage,item_id):
	favoritesfile = os.path.join(datapath,"favorites.json")
	if not xbmcvfs.exists(favoritesfile): save(favoritesfile,"{\n  \"albums\": [], \n  \"playlists\": [], \n  \"setlists\": [], \n  \"soundtracks\": [], \n  \"songs\": [], \n  \"version_fav\": 0.01\n}")
	favorites_json = readfile(favoritesfile)
	decoded_data = json.loads(favorites_json)
	if iconimage == addonfolder+artfolder+'no_cover.png': iconimage = None
	if type=='song':
		decoded_data["songs"].append({"type": 'default',"artist": artist,"track_name": track_name,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification('[B]'+artist+'[/B] - '+track_name,translate(30700),'4000',iconimage)
	elif type=='album':
		#albums from itunes charts
		if country: decoded_data["albums"].append({"provider": 'itunes',"artist": artist,"album": album,"country": country,"url": url,"iconimage": iconimage})
		#other albums from last.fm/7digital
		else: decoded_data["albums"].append({"provider": 'default',"artist": artist,"album": album,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification('[B]'+artist+'[/B] - '+album,translate(30700),'4000',iconimage)
	elif type=='setlist':
		decoded_data["setlists"].append({"name": name,"artist": artist,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification(name,translate(30700),'4000',iconimage)
	elif type=='playlist':
		#digster playlists
		if country: decoded_data["playlists"].append({"provider": 'digster',"name": name,"playlist_id": url,"country": country,"iconimage": iconimage})
		else:
			#last.fm playlists
			if playlist_id.startswith('lastfm://playlist/'): decoded_data["playlists"].append({"provider": 'last.fm',"name": name,"playlist_id": playlist_id,"iconimage": iconimage})
			#8tracks playlists
			else: decoded_data["playlists"].append({"provider": '8tracks',"name": name,"playlist_id": playlist_id,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification(name,translate(30700),'4000',iconimage)
	elif type=='soundtrack':
		decoded_data["soundtracks"].append({"name": name,"url": url,"iconimage": iconimage})
		save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		if not iconimage: iconimage = addonfolder+artfolder+'no_cover.png'
		notification(name,translate(30700),'4000',iconimage)

def Edit_favorites(url,type,item_id):
	favoritesfile = os.path.join(datapath,"favorites.json")
	if not xbmcvfs.exists(favoritesfile):
		save(favoritesfile,"{\n  \"albums\": [], \n  \"playlists\": [], \n  \"setlists\": [], \n  \"soundtracks\": [], \n  \"songs\": [], \n  \"version_fav\": 0.01\n}")
		return
	favorites_json = readfile(favoritesfile)
	decoded_data = json.loads(favorites_json)
	if url=='moveup':#move up the item
		if type=='fav_song':
			if int(item_id)==0: decoded_data["songs"].insert(len(decoded_data["songs"])+1, decoded_data["songs"].pop(int(item_id)))
			else: decoded_data["songs"].insert(int(item_id)-1, decoded_data["songs"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_album':
			if int(item_id)==0: decoded_data["albums"].insert(len(decoded_data["albums"])+1, decoded_data["albums"].pop(int(item_id)))
			else: decoded_data["albums"].insert(int(item_id)-1, decoded_data["albums"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_setlist':
			if int(item_id)==0: decoded_data["setlists"].insert(len(decoded_data["setlists"])+1, decoded_data["setlists"].pop(int(item_id)))
			else: decoded_data["setlists"].insert(int(item_id)-1, decoded_data["setlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_playlist':
			if int(item_id)==0: decoded_data["playlists"].insert(len(decoded_data["playlists"])+1, decoded_data["playlists"].pop(int(item_id)))
			else: decoded_data["playlists"].insert(int(item_id)-1, decoded_data["playlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_soundtrack':
			if int(item_id)==0: decoded_data["soundtracks"].insert(len(decoded_data["soundtracks"])+1, decoded_data["soundtracks"].pop(int(item_id)))
			else: decoded_data["soundtracks"].insert(int(item_id)-1, decoded_data["soundtracks"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
	elif url=='movedown':#move down the item
		if type=='fav_song':
			if int(item_id)==(len(decoded_data["songs"])-1): decoded_data["songs"].insert(0, decoded_data["songs"].pop(int(item_id)))
			else: decoded_data["songs"].insert(int(item_id)+1, decoded_data["songs"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_album':
			if int(item_id)==(len(decoded_data["albums"])-1): decoded_data["albums"].insert(0, decoded_data["albums"].pop(int(item_id)))
			else: decoded_data["albums"].insert(int(item_id)+1, decoded_data["albums"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_setlist':
			if int(item_id)==(len(decoded_data["setlists"])-1): decoded_data["setlists"].insert(0, decoded_data["setlists"].pop(int(item_id)))
			else: decoded_data["setlists"].insert(int(item_id)+1, decoded_data["setlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_playlist':
			if int(item_id)==(len(decoded_data["playlists"])-1): decoded_data["playlists"].insert(0, decoded_data["playlists"].pop(int(item_id)))
			else: decoded_data["playlists"].insert(int(item_id)+1, decoded_data["playlists"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_soundtrack':
			if int(item_id)==(len(decoded_data["soundtracks"])-1): decoded_data["soundtracks"].insert(0, decoded_data["soundtracks"].pop(int(item_id)))
			else: decoded_data["soundtracks"].insert(int(item_id)+1, decoded_data["soundtracks"].pop(int(item_id)))
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
	elif url=='delete':#delete the item
		if type=='fav_song':
			del decoded_data["songs"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_album':
			del decoded_data["albums"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_setlist':
			del decoded_data["setlists"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_playlist':
			del decoded_data["playlists"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
		elif type=='fav_soundtrack':
			del decoded_data["soundtracks"][int(item_id)]
			save(favoritesfile,json.dumps(decoded_data,indent=2,sort_keys=True))
	xbmc.executebuiltin('Container.Refresh')

###################################################################################
#USER SPACE

def Userspace_main():
	#last.fm user space
	if selfAddon.getSetting('lastfm_email')!='' and selfAddon.getSetting('lastfm_password')!='':
		selfAddon.setSetting('lastfm_token','')
		api_sig = hashlib.md5('api_key' + 'ca7bcdef4fda919aae12cb85be1b6794' + 'methodauth.getMobileSession' + 'password' + selfAddon.getSetting('lastfm_password') + 'username' + selfAddon.getSetting('lastfm_email') + 'b282ea6c4e937cc200ae43900304b506').hexdigest()
		codigo_fonte = abrir_url_custom('https://ws.audioscrobbler.com/2.0/', post = {'format': 'json', 'method': 'auth.getMobileSession', 'password': selfAddon.getSetting('lastfm_password'), 'username': selfAddon.getSetting('lastfm_email'), 'api_key': 'ca7bcdef4fda919aae12cb85be1b6794', 'api_sig': api_sig})
		decoded_data = json.loads(codigo_fonte)
		if 'error' in decoded_data:
			notification(translate(30862),translate(30864),'4000',addonfolder+artfolder+'notif_lastfm.png')
			selfAddon.setSetting('lastfm_token',value='')
		else:
			notification(translate(30862),translate(30865),'4000',addonfolder+artfolder+'notif_lastfm.png')
			selfAddon.setSetting('lastfm_token',value=decoded_data['session']['key'])
			userid_lastfm = decoded_data['session']['name']
		#dislay lastfm menu
		if selfAddon.getSetting('lastfm_token')!='':
			addDir(translate(30852),'1',50,'',search_query = 'user.getLovedTracks'+':'+userid_lastfm)
			addDir(translate(30853),'1',50,'',search_query = 'user.getRecentTracks'+':'+userid_lastfm)
			addDir(translate(30854),'1',50,'',search_query = 'user.getTopTracks'+':'+userid_lastfm)
			addDir(translate(30855),'1',50,'',search_query = 'user.getTopAlbums'+':'+userid_lastfm)
			addDir(translate(30856),'1',50,'',search_query = 'user.getPlaylists'+':'+userid_lastfm)
	#8tracks user space
	if selfAddon.getSetting('hide_8tracks')=="false":
		if selfAddon.getSetting('8tracks_email')!='' and selfAddon.getSetting('8tracks_password')!='':
			selfAddon.setSetting('8tracks_token','')
			codigo_fonte = abrir_url_custom('https://8tracks.com/sessions.json', post = {'login': selfAddon.getSetting('8tracks_email'), 'password': selfAddon.getSetting('8tracks_password'), 'api_version': '3'})
			decoded_data = json.loads(codigo_fonte)
			if decoded_data['status']!='200 OK':
				notification(translate(30863),translate(30864),'4000',addonfolder+artfolder+'notif_8tracks.png')
				selfAddon.setSetting('8tracks_token',value='')
			else:
				notification(translate(30863),translate(30865),'4000',addonfolder+artfolder+'notif_8tracks.png')
				selfAddon.setSetting('8tracks_token',value=decoded_data['user']['user_token'])
				userid_8tracks = str(decoded_data['user']['id'])
			#display 8tracks menu
			if selfAddon.getSetting('8tracks_token')!='':
				addDir(translate(30857),'1',52,'',search_query = 'liked:'+userid_8tracks)
				addDir(translate(30858),'1',52,'',search_query = 'listened:'+userid_8tracks)
				addDir(translate(30859),'1',52,'',search_query = 'dj:'+userid_8tracks)
				addDir(translate(30860),'1',52,'',search_query = 'recommended:'+userid_8tracks)

def My_lastfm(url,search_query,duration):
	#duration variable is used to pass the period of time in some methods
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	method = search_query.split(':', 1 )[0]
	userid_lastfm = search_query.split(':', 1 )[1]
	if method=='user.getPlaylists': codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method='+method+'&user='+userid_lastfm+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	else:
		if method=='user.getTopTracks' or method=='user.getTopAlbums':
			if not duration:
				id = xbmcgui.Dialog().select(translate(30870),[translate(30872),translate(30873),translate(30874),translate(30875),translate(30876),translate(30877)])
				if id != -1: duration = ['overall','7day','1month','3month','6month','12month'][id]
				else: sys.exit(0)
			print duration
			codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method='+method+'&user='+userid_lastfm+'&period='+duration+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
		else: codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method='+method+'&user='+userid_lastfm+'&limit='+str(items_per_page)+'&page='+url+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	if method=='user.getTopAlbums': # retrieve user data regarding albums
		if url=='1': addDir(translate(30871)+{'overall':translate(30872), '7day':translate(30873), '1month':translate(30874), '3month':translate(30875), '6month':translate(30876), '12month':translate(30877)}[duration],'1',50,'',search_query = 'user.getTopAlbums'+':'+userid_lastfm)
		try:
			#checks if output has only an object or various and proceeds according
			if 'name' in decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']:
				artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']['artist']['name'].encode("utf8")
				album_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']['name'].encode("utf8")
				mbid = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']['mbid'].encode("utf8")
				try: iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album']['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir('[B]'+artist+'[/B] - '+album_name,mbid,28,iconimage,artist = artist,album = album_name,type = 'album')
			else:
				for x in range(0, len(decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'])):
					artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'][x]['artist']['name'].encode("utf8")
					album_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'][x]['name'].encode("utf8")
					mbid = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'][x]['mbid'].encode("utf8")
					try: iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['album'][x]['image'][3]['#text'].encode("utf8")
					except: iconimage = addonfolder+artfolder+'no_cover.png'
					addDir('[B]'+artist+'[/B] - '+album_name,mbid,28,iconimage,artist = artist,album = album_name,type = 'album')
				total_pages = decoded_data[method[method.find('.get')+len('.get'):].lower()]['@attr']['totalPages']
				if int(url)<int(total_pages): addDir(translate(30412),str(int(url)+1),50,addonfolder+artfolder+'next.png',search_query = search_query,duration = duration)
		except: pass
	elif method=='user.getPlaylists': # retrieve user data regarding playlists
		try:
			#checks if output has only an object or various and proceeds according
			if 'title' in decoded_data[method[method.find('.get')+len('.get'):].lower()]['playlist']:
				playlist_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['playlist']['title'].encode("utf8")
				playlist_id = decoded_data[method[method.find('.get')+len('.get'):].lower()]['playlist']['id']
				try:
					iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['playlist']['image'][3]['#text'].encode("utf8")
					if iconimage=='' or iconimage==None: iconimage = addonfolder+artfolder+'no_cover.png'
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				addDir(playlist_name,'',51,iconimage,playlist_id = 'lastfm://playlist/'+playlist_id,type = 'playlist')
			else:
				for x in range(0, len(decoded_data[method[method.find('.get')+len('.get'):].lower()]['playlist'])):
					playlist_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['playlist'][x]['title'].encode("utf8")
					playlist_id = decoded_data[method[method.find('.get')+len('.get'):].lower()]['playlist'][x]['id']
					try: 
						iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['playlist'][x]['image'][3]['#text'].encode("utf8")
						if iconimage=='' or iconimage==None: iconimage = addonfolder+artfolder+'no_cover.png'
					except: iconimage = addonfolder+artfolder+'no_cover.png'
					addDir(playlist_name,'',51,iconimage,playlist_id = 'lastfm://playlist/'+playlist_id,type = 'playlist')
		except: pass
	else: # retrieve user data regarding tracks
		if duration and url=='1' and method=='user.getTopTracks': addDir(translate(30871)+{'overall':translate(30872), '7day':translate(30873), '1month':translate(30874), '3month':translate(30875), '6month':translate(30876), '12month':translate(30877)}[duration],'1',50,'',search_query = 'user.getTopTracks'+':'+userid_lastfm)
		try:
			#checks if output has only an object or various and proceeds according
			if 'name' in decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']:
				try: artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']['artist']['name'].encode("utf8")
				except: artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']['artist']['#text'].encode("utf8")
				track_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']['name'].encode("utf8")
				try: iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track']['image'][3]['#text'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if method=='user.getRecentTracks' and '@attr' in decoded_data['recenttracks']['track'] and 'nowplaying' in decoded_data['recenttracks']['track']['@attr'] and decoded_data['recenttracks']['track']['@attr']['nowplaying']=='true':
					if selfAddon.getSetting('track_resolver_method')=="0": addLink(translate(30869)+'[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir(translate(30869)+'[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
				else:
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
			else:
				for x in range(0, len(decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'])):
					try: artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'][x]['artist']['name'].encode("utf8")
					except: artist = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'][x]['artist']['#text'].encode("utf8")
					track_name = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'][x]['name'].encode("utf8")
					try: iconimage = decoded_data[method[method.find('.get')+len('.get'):].lower()]['track'][x]['image'][3]['#text'].encode("utf8")
					except: iconimage = addonfolder+artfolder+'no_cover.png'
					if method=='user.getRecentTracks' and '@attr' in decoded_data['recenttracks']['track'][x] and 'nowplaying' in decoded_data['recenttracks']['track'][x]['@attr'] and decoded_data['recenttracks']['track'][x]['@attr']['nowplaying']=='true':
						if selfAddon.getSetting('track_resolver_method')=="0": addLink(translate(30869)+'[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
						elif selfAddon.getSetting('track_resolver_method')=="1": addDir(translate(30869)+'[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
					else:
						if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
						elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
				total_pages = decoded_data[method[method.find('.get')+len('.get'):].lower()]['@attr']['totalPages']
				if int(url)<int(total_pages):
					if duration: addDir(translate(30412),str(int(url)+1),50,addonfolder+artfolder+'next.png',search_query = search_query,duration = duration)
					else: addDir(translate(30412),str(int(url)+1),50,addonfolder+artfolder+'next.png',search_query = search_query)
		except: pass

def List_lastfm_playlist_tracks(playlist_id):
	codigo_fonte = abrir_url('http://ws.audioscrobbler.com/2.0/?method=playlist.fetch&playlistURL='+playlist_id+'&api_key=d49b72ffd881c2cb13b4595e67005ac4&format=json')
	decoded_data = json.loads(codigo_fonte)
	try:
		#checks if output has only an object or various and proceeds according
		if 'title' in decoded_data['playlist']['trackList']['track']:
			artist = decoded_data['playlist']['trackList']['track']['creator'].encode("utf8")
			track_name = decoded_data['playlist']['trackList']['track']['title'].encode("utf8")
			try: iconimage = decoded_data['playlist']['trackList']['track']['image'].encode("utf8")
			except: iconimage = addonfolder+artfolder+'no_cover.png'
			if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
			elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
		else:
			for x in range(0, len(decoded_data['playlist']['trackList']['track'])):
				artist = decoded_data['playlist']['trackList']['track'][x]['creator'].encode("utf8")
				track_name = decoded_data['playlist']['trackList']['track'][x]['title'].encode("utf8")
				try: iconimage = decoded_data['playlist']['trackList']['track'][x]['image'].encode("utf8")
				except: iconimage = addonfolder+artfolder+'no_cover.png'
				if selfAddon.getSetting('track_resolver_method')=="0": addLink('[B]'+artist+'[/B] - '+track_name,'',39,iconimage,artist = artist,track_name = track_name,type = 'song')
				elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[B]'+artist+'[/B] - '+track_name,'1',26,iconimage,artist = artist,track_name = track_name,search_query = artist+' '+track_name)
	except: pass

def My_8tracks(url,search_query):
	items_per_page = int(selfAddon.getSetting('items_per_page'))
	codigo_fonte = abrir_url_custom('http://8tracks.com/mix_sets/'+search_query+'.json?include=mixes+pagination&page='+url+'&per_page='+str(items_per_page)+'api_key=e165128668b69291bf8081dd743fa6b832b4f477', headers={'X-User-Token': selfAddon.getSetting('8tracks_token') })
	decoded_data = json.loads(codigo_fonte)
	for x in range(0, len(decoded_data['mixes'])):
		username = decoded_data['mixes'][x]['user']['login'].encode("utf8")
		playlist_name = decoded_data['mixes'][x]['name'].encode("utf8")
		tracks_count = str(decoded_data['mixes'][x]['tracks_count'])
		playlist_id = str(decoded_data['mixes'][x]['id'])
		try: iconimage = decoded_data['mixes'][x]['cover_urls']['max200'].encode("utf8")
		except: iconimage = addonfolder+artfolder+'no_cover.png'
		addDir('[B]'+username+'[/B] - '+playlist_name+' [I]('+tracks_count+' tracks)[/I]','1',33,iconimage,playlist_id = playlist_id,type='playlist')
	total_pages = decoded_data['total_pages']
	if int(url)<int(total_pages): addDir(translate(30412),str(int(url)+1),52,addonfolder+artfolder+'next.png',search_query = search_query)

###################################################################################
#AUDIO FINGERPRINT
	
def Fingerprint_audio(url):
	import tempfile
	#input file (if not provided)
	if not url:
		dialog = xbmcgui.Dialog()
		url = dialog.browse(1,translate(30900),'myprograms')
		if not url: sys.exit(0)
	if os.path.splitext(url)[1] not in ['.mp3','.m4a','.wma','.wav','.aac','.ape','.flac']:
		dialog = xbmcgui.Dialog()
		ok = dialog.ok(translate(30400),translate(30901))
		sys.exit(0)
	#get the cookies
	session = requests.session()
	p = session.get('http://audiotag.info/index.php?simplehtml=1')
	#upload audio file
	p = session.post('http://audiotag.info/index.php', data={'step':'21'}, files={'uploadedfile': open(url, "rb")})
	#ask for captcha
	uploadedfilename = re.search('<input.*?name="uploadedfilename".*?value="(.+?)".*?>', p.text.encode('utf-8'))
	if uploadedfilename:
		tf = tempfile.NamedTemporaryFile(prefix='captcha_',suffix='.png',delete=False)
		tf.write(session.get('http://audiotag.info/captcha/captcha_img.php').content)
		tf.close()
		img = xbmcgui.ControlImage(450,13,400,130,tf.name)
		windlg = xbmcgui.WindowDialog()
		windlg.addControl(img)
		windlg.show()
		captchaInput = xbmcgui.Dialog().numeric(0,translate(30902))
		windlg.close()
		os.unlink(tf.name)
		#request results
		if captchaInput:
			p = session.post('http://audiotag.info/index.php', data={'step':'3','uploadedfilename':uploadedfilename.group(1),'capt':captchaInput,'Submit':'Next'})
			math = re.findall('<table border="0" class="restable">.*?<th colspan="3" class="resheader"><SPAN class="percent">(.+?)</SPAN></th>.*?<tr><td align="right" class="column1"><strong> Title: </strong></td><td>(.+?)</td>.*?<tr><td align="right" class="column1"><strong> Artist: </strong></td><td>(.+?)</td></tr>.*?<tr><td align="right" class="column1"><strong> Album:  </strong></td><td>(.+?)</td></tr>.*?<tr><td align="right" class="column1"><strong> Year:   </strong></td><td>(.+?)</td></tr>.*?</table>	', p.text.encode('utf-8'), re.DOTALL)
			if math:
				for probability, track_name, artist, album, year in math:
					if selfAddon.getSetting('track_resolver_method')=="0": addLink('[COLOR red]'+probability.strip()+'[/COLOR] - [B]'+artist.strip()+'[/B] - '+track_name.strip(),'',39,addonfolder+artfolder+'no_cover.png',artist = artist.strip(),track_name = track_name.strip(),type = 'song')
					elif selfAddon.getSetting('track_resolver_method')=="1": addDir('[COLOR red]'+probability.strip()+'[/COLOR] - [B]'+artist.strip()+'[/B] - '+track_name.strip(),'1',26,addonfolder+artfolder+'no_cover.png',artist = artist.strip(),track_name = track_name.strip(),search_query = artist.strip()+' '+track_name.strip())
			else:
				errormessage = re.search('<DIV id="plaintext">.*?<h2>Oops! Something is wrong!</h2>.*?<p>(.+?)</p>.*?</DIV>', p.text.encode('utf-8'), re.DOTALL)
				if errormessage:
					dialog = xbmcgui.Dialog()
					ok = dialog.ok(translate(30400),errormessage.group(1))
					sys.exit(0)
		else:
			sys.exit(0)
				
###################################################################################
#SETTINGS

def Open_settings():
	xbmcaddon.Addon(addon_id).openSettings()

###################################################################################
#XBMC RANDOM FUNCTIONS: OPEN_URl; ADDLINK; ADDDIR, FANART, NOTIFICATION, ETC...

def get_artist_fanart(artist):
	if not xbmcvfs.exists(os.path.join(datapath,"artistfanart")): xbmcvfs.mkdir(os.path.join(datapath,"artistfanart"))
	artistfile = os.path.join(datapath,"artistfanart",urllib.quote(artist) + '.txt')
	if xbmcvfs.exists(artistfile):
		fanart_list = eval(readfile(artistfile))
		return str(fanart_list[randint(0,len(fanart_list))-1])
	else:
		try:
			codigo_fonte = abrir_url('http://www.theaudiodb.com/api/v1/json/1/search.php?s=' + urllib.quote(artist))
		except:
			codigo_fonte = ''
		if codigo_fonte:
			decoded_data = json.loads(codigo_fonte)
			if len(decoded_data) >= 1:
    				fanart_list = []
    				if decoded_data['artists'][0]['strArtistFanart']:
        				fanart_list.append(decoded_data['artists'][0]['strArtistFanart'])
    				if decoded_data['artists'][0]['strArtistFanart2']:
        				fanart_list.append(decoded_data['artists'][0]['strArtistFanart2'])
    				if decoded_data['artists'][0]['strArtistFanart3']:
        				fanart_list.append(decoded_data['artists'][0]['strArtistFanart3'])
        			if fanart_list:
        				save(artistfile,str(fanart_list))
    					return str(fanart_list[randint(0,len(fanart_list)-1)])
    				else:
    					return ''
     		else:
     			return ''

#Function to write to txt files
def save(filename,contents):
    fh = open(filename, 'w')
    fh.write(contents)
    fh.close()

#Function to read txt files
def readfile(filename):
	f = open(filename, "r")
	string = f.read()
	return string

def notification(title,message,time,iconimage):
    xbmc.executebuiltin("XBMC.notification("+title+","+message+","+time+","+iconimage+")")

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', addon_useragent)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def abrir_url_custom(url,**kwargs):
	for key, value in kwargs.items(): exec('%s = %s' % (key, repr(value)))
	if 'post' in locals():
		data = urllib.urlencode(post)
		req = urllib2.Request(url,data)
	else: req = urllib2.Request(url)
	if 'headers' in locals():
		for x in range(0, len(headers)):
			req.add_header(headers.keys()[x], headers.values()[x])
	if 'user_agent' in locals(): req.add_header('User-Agent', user_agent)
	else: req.add_header('User-Agent', addon_useragent)
	if 'referer' in locals(): req.add_header('Referer', referer)
	if 'timeout' in locals(): response = urllib2.urlopen(req, timeout=timeout)
	else: response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,mode,iconimage,**kwargs):
	extra_args = ''
	for key, value in kwargs.items():
		exec('%s = %s' % (key, repr(value)))
		extra_args = extra_args + '&' + str(key) + '=' + urllib.quote_plus(str(value))
	if selfAddon.getSetting('get_artist_fanart')=="true":
		try:
			fanart = get_artist_fanart(artist)
		except:
			fanart = ''
	else: fanart = ''
	u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+extra_args
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
	liz.setInfo(type="Music", infoLabels={'title':track_name, 'artist':artist, 'album':album})
	liz.setProperty('IsPlayable', 'true')
	liz.setProperty('fanart_image', fanart)
	cm = []
	if type and type!='mymusic':
		#if 'manualsearch' in locals() and manualsearch==True or not 'manualsearch' in locals():
			#if selfAddon.getSetting('playing_type') == "0": cm.append((translate(30803), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=26&url=1&search_query='+urllib.quote_plus(str(artist)+' '+str(track_name))+')'))
		cm.append((translate(30804), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=35&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+')'))
		if type=='song':
			if item_id: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=46&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+'&url='+urllib.quote_plus(url)+'&item_id='+urllib.quote_plus(item_id)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			else: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=46&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='fav_song':
			cm.append((translate(30808), 'RunPlugin(plugin://'+addon_id+'/?mode=47&url=moveup&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30809), 'RunPlugin(plugin://'+addon_id+'/?mode=47&url=movedown&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30810), 'RunPlugin(plugin://'+addon_id+'/?mode=47&url=delete&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
		if selfAddon.getSetting('display_songinfo_cmenu')=="true":
			if 'songinfo' in locals() and songinfo==True or not 'songinfo' in locals():
				if selfAddon.getSetting('playing_type') == "0": cm.append((translate(30812), 'RunPlugin(plugin://'+addon_id+'/?mode=42&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
		if selfAddon.getSetting('display_artistinfo_cmenu')=="true": cm.append((translate(30826), 'RunPlugin(plugin://'+addon_id+'/?mode=55&artist='+urllib.quote_plus(artist)+')'))
		if selfAddon.getSetting('playing_type') == "0": cm.append((translate(30805), 'RunPlugin(plugin://'+addon_id+'/?mode=40&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
		if selfAddon.getSetting('playing_type') == "0": cm.append((translate(30806), 'RunPlugin(plugin://'+addon_id+'/?mode=37&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
	elif type=='mymusic':
		cm.append((translate(30825), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=53&url='+urllib.quote_plus(url)+')'))
		if artist and track_name: #sounds tagged with ID3 tags
			cm.append((translate(30804), 'XBMC.Container.Update(plugin://'+addon_id+'/?mode=35&artist='+urllib.quote_plus(artist)+'&track_name='+urllib.quote_plus(track_name)+')'))
			if selfAddon.getSetting('display_artistinfo_cmenu')=="true": cm.append((translate(30826), 'RunPlugin(plugin://'+addon_id+'/?mode=55&artist='+urllib.quote_plus(artist)+')'))
			cm.append((translate(30806), 'RunPlugin(plugin://'+addon_id+'/?mode=37&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
	liz.addContextMenuItems(cm, replaceItems=True)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,folder=True,**kwargs):
	extra_args = ''
	for key, value in kwargs.items():
		exec('%s = %s' % (key, repr(value)))
		extra_args = extra_args + '&' + str(key) + '=' + urllib.quote_plus(str(value))
	if selfAddon.getSetting('get_artist_fanart')=="true":
		try:
			fanart = get_artist_fanart(artist)
		except:
			fanart = ''
	else: fanart = ''
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+extra_args
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	cm = []
	if type:
		if type=='album':
			if country:
				cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=46&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&country='+urllib.quote_plus(country)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
				if selfAddon.getSetting('display_artistinfo_cmenu')=="true": cm.append((translate(30826), 'RunPlugin(plugin://'+addon_id+'/?mode=55&artist='+urllib.quote_plus(artist)+')'))
				cm.append((translate(30823), 'RunPlugin(plugin://'+addon_id+'/?mode=43&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+'&iconimage='+iconimage+extra_args+')'))
				cm.append((translate(30817), 'RunPlugin(plugin://'+addon_id+'/?mode=41&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&country='+urllib.quote_plus(country)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			else: 
				cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=46&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
				if selfAddon.getSetting('display_artistinfo_cmenu')=="true": cm.append((translate(30826), 'RunPlugin(plugin://'+addon_id+'/?mode=55&artist='+urllib.quote_plus(artist)+')'))
				cm.append((translate(30823), 'RunPlugin(plugin://'+addon_id+'/?mode=43&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+'&iconimage='+iconimage+extra_args+')'))
				cm.append((translate(30817), 'RunPlugin(plugin://'+addon_id+'/?mode=41&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='setlist':
			cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=46&name='+urllib.quote_plus(name)+'&url='+urllib.quote_plus(url)+'&artist='+urllib.quote_plus(artist)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			if selfAddon.getSetting('display_artistinfo_cmenu')=="true": cm.append((translate(30826), 'RunPlugin(plugin://'+addon_id+'/?mode=55&artist='+urllib.quote_plus(artist)+')'))
			cm.append((translate(30823), 'RunPlugin(plugin://'+addon_id+'/?mode=43&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
		elif type=='playlist':
			if country: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=46&name='+urllib.quote_plus(name)+'&url='+urllib.quote_plus(url)+'&country='+urllib.quote_plus(country)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			else: cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=46&name='+urllib.quote_plus(name)+'&playlist_id='+urllib.quote_plus(playlist_id)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
		elif type=='soundtrack':
			cm.append((translate(30807), 'RunPlugin(plugin://'+addon_id+'/?mode=46&name='+urllib.quote_plus(name)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30823), 'RunPlugin(plugin://'+addon_id+'/?mode=43&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+'&iconimage='+iconimage+extra_args+')'))
		elif type=='fav_song' or type=='fav_album' or type=='fav_setlist' or type=='fav_playlist' or type=='fav_soundtrack':
			cm.append((translate(30808), 'RunPlugin(plugin://'+addon_id+'/?mode=47&url=moveup&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30809), 'RunPlugin(plugin://'+addon_id+'/?mode=47&url=movedown&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			cm.append((translate(30810), 'RunPlugin(plugin://'+addon_id+'/?mode=47&url=delete&item_id='+urllib.quote_plus(item_id)+'&type='+urllib.quote_plus(type)+')'))
			if type=='fav_album':
				if selfAddon.getSetting('display_artistinfo_cmenu')=="true": cm.append((translate(30826), 'RunPlugin(plugin://'+addon_id+'/?mode=55&artist='+urllib.quote_plus(artist)+')'))
				if country:
					cm.append((translate(30823), 'RunPlugin(plugin://'+addon_id+'/?mode=43&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+'&iconimage='+iconimage+extra_args+')'))
					cm.append((translate(30817), 'RunPlugin(plugin://'+addon_id+'/?mode=41&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&country='+urllib.quote_plus(country)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
				else:
					cm.append((translate(30823), 'RunPlugin(plugin://'+addon_id+'/?mode=43&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+'&iconimage='+iconimage+extra_args+')'))
					cm.append((translate(30817), 'RunPlugin(plugin://'+addon_id+'/?mode=41&artist='+urllib.quote_plus(artist)+'&album='+urllib.quote_plus(album)+'&url='+urllib.quote_plus(url)+'&iconimage='+urllib.quote_plus(iconimage)+'&type='+urllib.quote_plus(type)+')'))
			elif type=='fav_setlist':
				if selfAddon.getSetting('display_artistinfo_cmenu')=="true": cm.append((translate(30826), 'RunPlugin(plugin://'+addon_id+'/?mode=55&artist='+urllib.quote_plus(artist)+')'))
				cm.append((translate(30823), 'RunPlugin(plugin://'+addon_id+'/?mode=43&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+extra_args+')'))
			elif type=='fav_soundtrack':
				cm.append((translate(30823), 'RunPlugin(plugin://'+addon_id+'/?mode=43&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(name)+'&iconimage='+iconimage+extra_args+')'))
	liz.addContextMenuItems(cm, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
                                
        return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None
artist=None
album=None
track_name=None
type=None
search_query=None
country=None
item_id=None
playlist_id=None
duration=None
fanart=None


try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: artist=urllib.unquote_plus(params["artist"])
except: pass
try: album=urllib.unquote_plus(params["album"])
except: pass
try: track_name=urllib.unquote_plus(params["track_name"])
except: pass
try: type=urllib.unquote_plus(params["type"])
except: pass
try: search_query=urllib.unquote_plus(params["search_query"])
except: pass
try: country=urllib.unquote_plus(params["country"])
except: pass
try: item_id=urllib.unquote_plus(params["item_id"])
except: pass
try: playlist_id=urllib.unquote_plus(params["playlist_id"])
except: pass
try: duration=urllib.unquote_plus(params["duration"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)
print "Fanart: "+str(fanart)
if artist: print "Artist: "+str(artist)
if album: print "Album: "+str(album)
if track_name: print "Track Name: "+str(track_name)
if type: print "Type: "+str(type)
if search_query: print "Search Query: "+str(search_query)
if country: print "Country: "+str(country)
if item_id: print "Item Id: "+str(item_id)
if playlist_id: print "Playlist Id: "+str(playlist_id)
if duration: print "Duration: "+str(duration)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

# Main Menu
if mode==None: Main_menu()
# Recomendations
elif mode==1: Recomendations(url)
# Digster
elif mode==2: Digster_menu()
elif mode==3: Digster_sections()
elif mode==4: Digster_categories(url)
elif mode==5: List_digster_playlists(url,search_query)
elif mode==6: List_digster_tracks(url,country)
# Whatsong soundtrack
elif mode==7: List_whatsong_movies(url)
elif mode==8: List_whatsong_tracks(url)
# 8tracks playlists
elif mode==9: Eighttracks_menu()
elif mode==10: List_8tracks_suggestions(url,search_query)
# Charts
elif mode==11: Top_charts_menu()
elif mode==13 or mode==14: Itunes_countries_menu(mode)
elif mode==15: Itunes_track_charts(url,country)
elif mode==16: Itunes_album_charts(url,country)
elif mode==17: Itunes_list_album_tracks(url,album,country)
elif mode==18: Deezer_top_tracks(url)
elif mode==19: Beatport_top100(url)
elif mode==20 or mode==21: Officialcharts_uk(url,mode,playlist_id)
elif mode==22 or mode==23: Billboard_charts(url,mode,playlist_id)
elif mode==24: Traxsource_top(url,playlist_id)
# Search and list content
elif mode==25: Search_main()
elif mode==26: Search_by_tracks(url,search_query)
elif mode==27: Search_by_albums(url,search_query)
elif mode==28: List_album_tracks(url,artist,album)
elif mode==29: Search_by_toptracks(url,search_query)
elif mode==30: Search_by_setlists(url,search_query)
elif mode==31: List_setlist_tracks(url)
elif mode==32: Search_8tracks_playlists(url,search_query)
elif mode==33: List_8tracks_tracks(url,iconimage,playlist_id)
elif mode==34: Search_whatsong_soundtrack(search_query)
elif mode==35: Search_by_similartracks(artist,track_name)
elif mode==37: Search_videoclip(artist,track_name,album)
# Downloads and Resolvers
elif mode==38: List_my_songs(search_query)
elif mode==39:
	if selfAddon.getSetting('playing_type') == "0" or type=='mymusic':
		Resolve_songfile(url,artist,track_name,album,iconimage)
	elif selfAddon.getSetting('playing_type') == "1":
		Search_videoclip(artist,track_name,album)
	else:pass
elif mode==40: Download_songfile(url,artist,track_name)
elif mode==41: Download_whole_album(artist,album,url,country,iconimage)
elif mode==43: Export_as_m3u(name,artist,album,url,country,iconimage,type)
elif mode==42: Song_info(url,artist,track_name,duration)
elif mode==55: Artist_info(artist)
# Favorites
elif mode==44: Favorites_menu()
elif mode==45: List_favorites(url)
elif mode==46: Add_to_favorites(type,artist,album,country,name,playlist_id,track_name,url,iconimage,item_id)
elif mode==47: Edit_favorites(url,type,item_id)
# User space
elif mode==48: Userspace_main()
elif mode==50: My_lastfm(url,search_query,duration)
elif mode==51: List_lastfm_playlist_tracks(playlist_id)
elif mode==52: My_8tracks(url,search_query)
# Audio fingerprint
elif mode==53: Fingerprint_audio(url)
# Settings
elif mode==54: Open_settings()
# External Calls
elif mode==300: Resolve_songfile(url,artist,track_name,album,iconimage)
# Search fix
if mode==None or mode in [1,2,11,38,44,48,53,54]:
	try: xbmcvfs.delete(os.path.join(datapath,'searchdata.txt'))
	except: pass

xbmcplugin.endOfDirectory(int(sys.argv[1]))
