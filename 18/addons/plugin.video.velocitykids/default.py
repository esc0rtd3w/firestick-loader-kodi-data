# -*- coding: utf-8 -*-
"""
    Velocity Kodi Addon
    Copyright (C) 2016 blazetamer

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
"""

from urllib2 import Request, urlopen
import urllib2,urllib,re,os
import sys
import time,datetime
import urlresolver

import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
import tools
from libs import kodi,trakt_auth,trakt
from tm_libs import dom_parser
from tm_libs import dl_control,cache_stat,watched_cache
from libs import log_utils,message
from libs import window_utils
import datetime

from t0mm0.common.net import Net
from t0mm0.common.addon import Addon
from scrapers import main_scrape ,primewire,twomovies,zmovies,merdb,iwatchonline,nine_movies,icefilms
import cookielib
import operator





ADDON = xbmcaddon.Addon(id=kodi.addon_id)
net = Net()
addon_id=kodi.addon_id
addon = Addon(addon_id, sys.argv)
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))
fanart = artwork+'fanart.jpg'
messages = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','messages/'))
execute = xbmc.executebuiltin
trakt_api=trakt.TraktAPI()

#==========NEW AUTOUPDATE FUNCTION START===============
#********************AutoUpdate******************
from autoupdate import autoupdates
#Author Info Variable

autoupdates.provider_name = "Blazetamer"

#add-on variables

autoupdates.addon_id_name ='plugin.video.velocitykids'
autoupdates.addon_xml_loca = "https://offshoregit.com/Blazetamer/repo/raw/master/plugin.video.velocitykids/addon.xml"
autoupdates.addon_name ="Velocity Kids"
autoupdates.addon_zip_loca ="https://offshoregit.com/Blazetamer/repo/raw/master/zips/plugin.video.velocitykids"


#repo variables

autoupdates.repo_name = "repository.BlazeRepo"
autoupdates.repo_xml_loca ="https://offshoregit.com/Blazetamer/repo/raw/master/zips/repository.BlazeRepo/addon.xml"
autoupdates.repo_zip_loca ="https://offshoregit.com/Blazetamer/repo/raw/master/zips/repository.BlazeRepo"
autoupdates.repo_entry_version="3.1"


#********************AutoUpdate END******************




def LogNotify(title,message,times,icon):
		xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")


def OPEN_URL(url):
	req=urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
	response=urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link


def menu():
	autoupdates.STARTUP()
	if  kodi.get_setting('trakt_authorized') =='true':
		kodi.addDir("Parent Approved Movies",'','custom_movie_lists',artwork+'movies.png','',1,'','',fanart=fanart)
		kodi.addDir("Parent Approved TV Shows",'','custom_tv_lists',artwork+'tvshows.png','',1,'','',fanart=fanart)
	if  kodi.get_setting('trakt_authorized') =='false':
		kodi.addDir("[COLOR gold]Requires Trakt Integration[/COLOR]",messages+'trakt_auth.txt','get_pin',artwork+'trakt.png','',1,'','',fanart=fanart,is_playable=False,is_folder=True)
	kodi.auto_view('menu')


# def movie_menu():
# 		media='movies'#addon(addonname).getSetting()
# 		if kodi.get_setting('trakt_authorized') == 'true':
# 			kodi.addDir("[COLOR gold]Parent Approved Movies[/COLOR]",'','custom_movie_lists',artwork+'custom_lists.png','',1,'',media,fanart=fanart)
# 		kodi.auto_view('menu')
#
#         #(name,url,mode,thumb,movie_title,total_items,trakt_id,media,fanart=None,meta_data=None, is_folder=None, is_playable=None, menu_items=None, replace_menu=False):
#
# def tv_menu():
#
# 	media ='shows'
#
# 	if kodi.get_setting('trakt_authorized') == 'true':
# 			kodi.addDir("[COLOR gold]Parent Approved TV Lists[/COLOR]",'','custom_tv_lists',artwork+'special_movie_lists.png','',1,'',media,fanart=fanart)
# 	kodi.auto_view('menu')
#

def find_season(name,trakt_id):

	try:
		media = 'shows'
		movie_title =name
		print "TRAKT ID IS : "+trakt_id
		link = trakt_api.get_show_seasons(trakt_id)
		for e in link:
					infoLabels = trakt_api.process_show(e)
					infoLabels.update(make_infoLabels(e))
					#trakt_id = str(infoLabels['trakt_id'])
					if infoLabels['cover_url'] == None:
						infoLabels['cover_url'] = artwork+'place_poster.png'
					menu_items=[]
					menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
					#if kodi.get_setting('trakt_authorized') == 'true':
						#menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
					kodi.addDir('Season '+str(infoLabels['number']),'','find_episode',infoLabels['cover_url'],movie_title,5,trakt_id,'shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=True)
					kodi.auto_view('season')
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Trakt Seasons',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)


def find_episode(name,trakt_id,movie_title):

	try:
		media ='episode'
		season = name.replace('Season ','')
		#print "SHOW TRAKT IS : "+trakt_id
		link = trakt_api.get_show_episodes(trakt_id,season)
		for e in link:
			ep_trakt_id= e['ids']['trakt']
			#print "Episode TRAKT ID IS  : "+str(ep_trakt_id)
			infoLabels={}
			infoLabels.update(make_infoLabels(e))
			episode = infoLabels['episode']
			infoLabels = trakt_api.get_episode_details(trakt_id,season,episode)
			menu_items=[]
			trailer = infoLabels['trailer_url']
			year = str(infoLabels['year'])
			name = infoLabels['title'].encode('utf-8')
			thumb=infoLabels['cover_url']
			# ################
			was_watched=watched_cache.get_watched_cache(ep_trakt_id)
			if was_watched is not None:
				infoLabels['playcount'] = 1
			# ################
			if thumb is None:
				thumb = ''
			#print infoLabels['premiered'][:10]
			#if (episode['first_aired'] != None and utils2.iso_2_utc(episode['first_aired']) <= time.time()) or (include_unknown and episode['first_aired'] == None):
			d1 = str(infoLabels['premiered'])
			d2 = str(datetime.date.today())
			#print today - was_aired
			#if infoLabels['premiered'] =='':
			if d1 >= d2 or infoLabels['premiered'] == '':
				if name is not '':
					menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
					kodi.addDir('[COLOR maroon]S'+str(season)+'E'+str(episode)+'  '+name+'[/COLOR]','','findsource',thumb,movie_title,5,'','shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=True)
					#name = name+" [COLOR red]Coming Soon[/COLOR]"
			else:
				menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
				kodi.addDir('S'+str(season)+'E'+str(episode)+'  '+name,'','findsource',thumb,movie_title,5,'','shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=True)
			kodi.auto_view('episode')
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Trakt Episodes',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)


#Start Ketboard Function
def _get_keyboard( default="", heading="", hidden=False ):
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default



def custom_movie_lists():
	media = 'movies'
	get_lists = trakt_api.get_custom_lists()
	for e in get_lists:
		list_id = e['ids']
		slug_id=list_id['slug']
		print "FIRST SLUG ID IS "+slug_id
		trakt_id=str(list_id['trakt'])
		name_id = e['name']
		if slug_id =='kids':
			print "SLUG ID IS " +slug_id
			custom_list_view(slug_id,media)


def custom_list_view(trakt_id,media):
	try:
		lists = trakt_api.get_special_list(trakt_id,media)#is actually SLUG ID
		for e in lists:
			infoLabels = trakt_api.process_movie(e)
			infoLabels.update(make_infoLabels(e))
			menu_items=[]
			trakt_id = str(infoLabels['trakt_id'])
			trailer = infoLabels['trailer_url']
			year = str(infoLabels['year'])
			name = infoLabels['title'].encode('utf-8')
			thumb=infoLabels['cover_url']
			if thumb is None:
				thumb = ''
			menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
			if trailer:
				utube = tools.make_trailer(trailer)
				menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))


			kodi.addDir(name+' ('+year+')','','findsource',thumb,name,5,'','movies',meta_data=infoLabels,menu_items=menu_items,replace_menu=False)
			kodi.auto_view('movies')
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Custom List Error',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)




def custom_tv_lists():
	media = 'shows'

	get_lists = trakt_api.get_custom_lists()
	for e in get_lists:
		list_id = e['ids']
		slug_id=list_id['slug']
		print "SLUG ID IS "+slug_id
		trakt_id=str(list_id['trakt'])
		name_id = e['name']
		if slug_id =='kids':
			custom_list_view_tv(slug_id,media)

def custom_list_view_tv(trakt_id,media):
	try:
		lists = trakt_api.get_special_list('kids',media)#is actually SLUG ID
		for e in lists:
			infoLabels = trakt_api.process_movie(e)
			infoLabels.update(make_infoLabels(e))
			menu_items=[]
			trakt_id = str(infoLabels['trakt_id'])
			trailer = infoLabels['trailer_url']
			year = str(infoLabels['year'])
			name = infoLabels['title'].encode('utf-8')
			thumb=infoLabels['cover_url']
			if thumb is None:
				thumb = ''
			menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
			if trailer:
				utube = tools.make_trailer(trailer)
				menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))


			kodi.addDir(name+' ('+year+')','','find_season',thumb,name,5,trakt_id,'shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=False)
			kodi.auto_view('tvshows')
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Custom List Error',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)


#################
def make_infoLabels(item, show=None, people=None):
	try:
			item = item['movie']
	except:
		try:
			item = item['show']
		except:
			item = item
	if kodi.get_setting('debug') == "true":
		print "ITEM IS : = "+str(item)
	if people is None: people = {}
	if show is None: show = {}
	infoLabels = {}
	if 'title' in item: infoLabels['title'] = item['title']
	if 'overview' in item: infoLabels['plot'] = infoLabels['plotoutline'] = item['overview']
	if 'runtime' in item and item['runtime'] is not None: infoLabels['duration'] = item['runtime'] * 60
	if 'certification' in item: infoLabels['mpaa'] = item['certification']
	if 'year' in item: infoLabels['year'] = item['year']
	if 'season' in item: infoLabels['season'] = item['season']  # needs check
	if 'episode' in item: infoLabels['episode'] = item['episode']  # needs check
	if 'number' in item: infoLabels['episode'] = item['number']  # needs check
	if 'network' in item: infoLabels['studio'] = item['network']
	if 'status' in item: infoLabels['status'] = item['status']
	if 'tagline' in item: infoLabels['tagline'] = item['tagline']
	if 'watched' in item and item['watched']: infoLabels['playcount'] = 1
	if 'plays' in item and item['plays']: infoLabels['playcount'] = item['plays']
	if 'rating' in item: infoLabels['rating'] = item['rating']
	if 'votes' in item: infoLabels['votes'] = item['votes']
	if 'released' in item: infoLabels['premiered'] = item['released']
	if 'trailer' in item and item['trailer']: infoLabels['trailer'] = tools.make_trailer(item['trailer'])
	if 'trailer' in item and item['trailer']:
		infoLabels['trailer_url'] = item['trailer']
	else: infoLabels['trailer_url'] = False
	if 'first_aired' in item: infoLabels['aired'] = infoLabels['premiered'] = make_air_date(item['first_aired'])
	infoLabels.update(make_ids(item))
	infoLabels.update(make_art(item))
	if 'genres' in item:
		infoLabels.update(make_genre(item))
	if 'aired_episodes' in item:
		infoLabels['episode'] = infoLabels['TotalEpisodes'] = item['aired_episodes']
		infoLabels['WatchedEpisodes'] = item['watched_count'] if 'watched_count' in item else 0
		infoLabels['UnWatchedEpisodes'] = infoLabels['TotalEpisodes'] - infoLabels['WatchedEpisodes']
	# override item params with show infoLabels if it exists
	if 'certification' in show: infoLabels['mpaa'] = show['certification']
	if 'year' in show: infoLabels['year'] = show['year']
	if 'runtime' in show and show['runtime'] is not None: infoLabels['duration'] = show['runtime'] * 60
	if 'title' in show: infoLabels['tvshowtitle'] = show['title']
	if 'network' in show: infoLabels['studio'] = show['network']
	if 'status' in show: infoLabels['status'] = show['status']
	if 'trailer' in show and show['trailer']: infoLabels['trailer'] = tools.make_trailer(show['trailer'])
	infoLabels.update(make_ids(show))
	# infoLabels.update(make_people(people))
	return infoLabels


def make_ids(item):
	infoLabels= {}
	if 'ids' in item:
		ids = item['ids']
		if 'imdb' in ids: infoLabels['code'] = infoLabels['imdbnumber'] = infoLabels['imdb_id'] = ids['imdb']
		if 'tmdb' in ids: infoLabels['tmdb_id'] = ids['tmdb']
		if 'tvdb' in ids: infoLabels['tvdb_id'] = ids['tvdb']
		if 'trakt' in ids: infoLabels['trakt_id'] = ids['trakt']
		if 'slug' in ids: infoLabels['slug'] = ids['slug']
	return infoLabels


def make_art(item):
	infoLabels= {}
	infoLabels['thumb_url'] = meta_map(['images', 'thumb', 'full'], item)
	infoLabels['cover_url'] = meta_map(['images', 'poster', 'full'], item)
	infoLabels['backdrop_url'] = meta_map(['images', 'fanart', 'full'], item)
	if 'screenshot' in item:
		infoLabels['cover_url'] = meta_map(['images','screenshot','full'], item)
	return infoLabels

def make_genre(item):
	infoLabels= {}
	infoLabels['genre'] = meta_map(['genres'], item)
	return infoLabels

def make_air_date(first_aired):
	utc_air_time = iso_2_utc(first_aired)
	try: air_date = time.strftime('%Y-%m-%d', time.localtime(utc_air_time))
	except ValueError:  # windows throws a ValueError on negative values to localtime
		d = datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds=utc_air_time)
		air_date = d.strftime('%Y-%m-%d')
	return air_date

def iso_2_utc(iso_ts):
    if not iso_ts or iso_ts is None: return 0
    delim = -1
    if not iso_ts.endswith('Z'):
        delim = iso_ts.rfind('+')
        if delim == -1: delim = iso_ts.rfind('-')

    if delim > -1:
        ts = iso_ts[:delim]
        sign = iso_ts[delim]
        tz = iso_ts[delim + 1:]
    else:
        ts = iso_ts
        tz = None

    if ts.find('.') > -1:
        ts = ts[:ts.find('.')]

    try: d = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S')
    except TypeError: d = datetime.datetime(*(time.strptime(ts, '%Y-%m-%dT%H:%M:%S')[0:6]))

    dif = datetime.timedelta()
    if tz:
        hours, minutes = tz.split(':')
        hours = int(hours)
        minutes = int(minutes)
        if sign == '-':
            hours = -hours
            minutes = -minutes
        dif = datetime.timedelta(minutes=minutes, hours=hours)
    utc_dt = d - dif
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = utc_dt - epoch
    try: seconds = delta.total_seconds()  # works only on 2.7
    except: seconds = delta.seconds + delta.days * 24 * 3600  # close enough
    return seconds


def meta_map(path, object, default=''):
	try:
		if isinstance(path, list):
			for k in path:
				object = object[k]
		else:
			object = object[path]
			object = object if object is not None else default
		return object
	except:
		return default


#################


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

url=None
name=None
mode=None
trakt_id=None
thumb = None


try:
		iconimage=urllib.unquote_plus(params["iconimage"])
except:
		pass

try:
		thumb=urllib.unquote_plus(params["thumb"])
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
		filetype=urllib.unquote_plus(params["filetype"])
except:
		pass


try:
		url=urllib.unquote_plus(params["url"])
except:
		pass

try:
		media=urllib.unquote_plus(params["media"])
except:
		pass

try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		mode=urllib.unquote_plus(params["mode"])
except:
		pass

try:
		year=urllib.unquote_plus(params["year"])
except:
		pass

try:
		imdb_id=urllib.unquote_plus(params["imdb_id"])
except:
		pass

try:
		movie_title=urllib.unquote_plus(params["movie_title"])
except:
		pass


try:
		trakt_id=urllib.unquote_plus(params["trakt_id"])
except:
		pass


ext = addon.queries.get('ext', '')


if kodi.get_setting('debug') == "true":
	print "Mode: "+str(mode)
	print "URL: "+str(url)
	print "Name: "+str(name)
	print "Thumb: "+str(thumb)


if mode==None :
		menu()

# elif mode=='menu':
# 		menu(url)



elif mode=='movie_menu':
		movie_menu()

elif mode=='tv_menu':
		tv_menu()




elif mode=='tmovies':
		twomovies.tmovies(name)

elif mode=='tmlinkpage':
		twomovies.tmlinkpage(url,movie_title,thumb,media)

elif mode=='playmerdblink':
		merdb.playmerdblink(url,movie_title,thumb)

elif mode=='playiwatchonlink':
		iwatchonline.playiwatchonlink(url,movie_title,thumb)

elif mode=='playzmovieslink':
		zmovies.playzmovieslink(url,movie_title,thumb)

elif mode=='playprimelink':
		primewire.playprimelink(url,movie_title,thumb)  #########MAY REMOVE###########

elif mode=='get_link':
		main_scrape.get_link(url,movie_title,thumb,media)

elif mode=='get_tv_link':
		main_scrape.get_tv_link(url,movie_title,thumb,media)

elif mode=='findsource':
		main_scrape.find_source(name,thumb,media,movie_title)

elif mode=='find_episode':
		find_episode(name,trakt_id,movie_title)

elif mode=='find_season':
		find_season(name,trakt_id)

elif mode=='get_token':
		trakt_api=trakt.TraktAPI()
		trakt_api.authorize()

elif mode=='pininput':
		message.pininput()

elif mode=='message_stat':
		message.message_stat(url)

elif mode=='playlink':
		main_scrape.playlink()


####Custom Stuff
elif mode=='custom_movie_lists':
		custom_movie_lists()

elif mode=='custom_tv_lists':
		custom_tv_lists()


#Settings Openings

# elif mode=='resolver_settings':
# 		urlresolver.display_settings()
#
# elif mode=='display_settings':
# 		kodi.openSettings(addon_id,id1=9,id2=0)
#
# elif mode=='display_download_settings':
# 		kodi.openSettings(addon_id,id1=9,id2=1)
#
# elif mode=='display_trakt_settings':
# 		kodi.openSettings(addon_id,id1=9,id2=2)
#
# elif mode=='display_scraper_settings':
# 		kodi.openSettings(addon_id,id1=9,id2=3)
#
#
# #Download Function
#
# elif mode=='setup_download':
# 		dl_control.setup_download(name,url,thumb,media,movie_title)
#
# elif mode=='add_to_queue':
# 		dl_control.add_to_queue(name,url,thumb,ext,media)
#
# elif mode=='viewQueue':
# 		dl_control.viewQueue()
#
# elif mode=='download':
# 		dl_control.download()
#
# elif mode=='removeFromQueue':
# 		dl_control.removeFromQueue(name,url,thumb,ext,media)
#
# elif mode=='download_now':
# 		dl_control.download_now(name, url, thumb, ext, media)
#
# elif mode=='download_stats':
# 		dl_control.download_stats(name, url, thumb, ext, media)


###WATCHED STATUS DB

elif mode=='repair_watched_items':
		watched_cache.repair_watched_items()


elif mode=='get_watched_items':
		watched_cache.get_watched_items()


elif mode=='flush_watched_cache':
		watched_cache.flush_watched_cache()

elif mode=='get_watched_cache':
		watched_cache.get_watched_cache(trakt_id)


###Standard Cache Operations
elif mode=='get_cache':
		cache_stat.get_cache()

elif mode=='flush_url_cache':
		cache_stat.flush_url_cache()

#############WINDOW UTILS#########
elif mode=='get_pin':
		window_utils.get_pin()


xbmcplugin.endOfDirectory(int(sys.argv[1]))



# TODO  PutMV and 9Movies
'''
http://miradetodo.com.ar/videos/
http://movie.pubfilmno1.com
http://xmovies8.tv
http://www.izlemeyedeger.com
http://tunemovie.is
http://cyberreel.com
http://123movies.to
'''

'''
.decode('utf-8')
'''