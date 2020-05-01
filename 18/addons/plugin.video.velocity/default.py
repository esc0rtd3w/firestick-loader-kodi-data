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
import urlresolver
import xbmcplugin,xbmcgui,xbmc, xbmcaddon, downloader, extract, time
import tools
from libs import kodi,trakt_auth,trakt
from libs import dl_control,cache_stat,watched_cache
from libs import log_utils,message
from libs import window_utils
import datetime
from libs import viewsetter
from libs import image_scraper
from libs.modules.addon import Addon
from scrapers import main_scrape,primewire,iwatchonline,icefilms
import json
from libs import trakt_auth



ADDON = xbmcaddon.Addon(id=kodi.addon_id)
addon_id=kodi.addon_id
addon = Addon(addon_id, sys.argv)
artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))
fanart = artwork+'fanart.jpg'
messages = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','messages/'))
execute = xbmc.executebuiltin
use_https = kodi.get_setting('use_https') == 'false'
trakt_api = trakt.TraktAPI(use_https=use_https)



orig_ids = addon.queries.get('orig_ids', [])


#==========NEW AUTOUPDATE FUNCTION START===============
#********************AutoUpdate******************
from autoupdate import autoupdates
#Author Info Variable

autoupdates.provider_name = "Blazetamer"

#add-on variables

autoupdates.addon_id_name ='plugin.video.velocity'
autoupdates.addon_xml_loca = "https://offshoregit.com/Blazetamer/repo/raw/master/plugin.video.velocity/addon.xml"
autoupdates.addon_name ="Velocity"
autoupdates.addon_zip_loca ="https://offshoregit.com/Blazetamer/repo/raw/master/zips/plugin.video.velocity"


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
	# active_plugin = xbmc.getInfoLabel('Container.PluginName')
	# kodi.log("RUNNING ADDON IS = "+active_plugin)
	autoupdates.STARTUP()
	kodi.addDir("Movies",'','movie_menu',artwork+'movies.png','',1,'','',fanart=fanart,description="View and Search for Movies.")
	kodi.addDir("TV Shows",'','tv_menu',artwork+'tvshows.png','',1,'','',fanart=fanart,description="View and Search for TV Shows.")
	kodi.addDir("Settings", '', 'do_settings', artwork + 'gen_settings.png', '', 1, '', '', fanart=fanart,
				description="View and Change Addon and System Settings.")
	#kodi.addDir("Manage Downloads",'','viewQueue',artwork+'manage_downloads.png','',1,'','',fanart=fanart,description="View and Manage Your Downloads.")
	#kodi.addDir("VERSION TEST ",'','get_kversion',artwork+'update.png','',1,'','',fanart=fanart)

	if  kodi.get_setting('trakt_authorized') =='true':
		kodi.addItem("[COLOR gold]Clear Trakt User[/COLOR] ",'','de_auth',artwork+'sign_out.png',fanart=fanart,description="Clear and Log Out Your Trakt Account.")
	if  kodi.get_setting('trakt_authorized') =='false':
		kodi.addItem("[COLOR gold]Trakt Integration[/COLOR]",'','get_pin',artwork+'trakt.png', fanart=fanart,description="Authorize your Trakt Account.")
	kodi.addItem("[COLOR blue]This addon is developed and supported at www.tvaddons.ag [/COLOR]", '', '', artwork + 'tvaddons_logo.png', fanart=fanart,description="This software and addon is and always has been FREE, If you have paid for this software , request a refund, You have been duped!!.")
	kodi.addItem("[COLOR red]Disclaimer [/COLOR]", '', '',
				 artwork + 'tvaddons_logo.png', fanart=fanart,
				 description="All videos are hosted by 3rd parties. All content linked to from this addon is intended for space shifting, time shifting, format shifting, backup, fair use, public domain, and educational purposes only. You are responsible for ensuring you have the right to access any linked content.")
	viewsetter.set_view("seasons")
	#xbmc.executebuiltin("Container.SetViewMode()")

def do_settings():
	kodi.addItem("General Settings", '', 'display_settings', artwork + 'gen_settings.png', fanart=fanart,
				 description="Adjust The General Addon Settings.")
	kodi.addItem("Sorting Methods", '', 'display_sort_settings', artwork + 'gen_settings.png', fanart=fanart,
				 description="Enable and Pick Sorting Methods.")
	kodi.addItem("Enable Providers", '', 'display_scraper_settings', artwork + 'scraper_settings.png', fanart=fanart,
				 description="Adjust Your Provider/Scraper Settings.")
	kodi.addItem("Trakt Settings", '', 'display_trakt_settings', artwork + 'trakt_settings.png', fanart=fanart,
				 description="Adjust and Set Trakt Intergration Settings.")
	kodi.addItem("Url Resolver Settings", '', 'resolver_settings', artwork + 'resolver_settings.png', fanart=fanart,
				 description="Adjust and Set The Url Resolver Settings.")
	#kodi.addItem("Set Download Folder", '', 'display_download_settings', artwork + 'down_settings.png', fanart=fanart,
				 #description="Set The Path For Your Downloaded Files.")
	viewsetter.set_view("seasons")
def get_kversion():
	full_version_info = xbmc.getInfoLabel('System.BuildVersion')
	baseversion = full_version_info.split(".")
	return  baseversion[0]

def movie_menu():
		media='movies'#addon(addonname).getSetting()
		kodi.addDir("Popular",'popular','call_trakt_movies',artwork+'popular.png','',1,'','',fanart=fanart,description="Popular Movies Section.")
		kodi.addDir("Trending",'trending','call_trakt_movies',artwork+'trending.png','',1,'','',fanart=fanart,description="Trending Movies Section.")
		kodi.addDir("Most Watched",'most_watched','call_trakt_movies',artwork+'most_watched.png','',1,'','',fanart=fanart,description="Most Watched Movies Section.")
		kodi.addDir("Most Played",'most_played','call_trakt_movies',artwork+'most_played.png','',1,'','',fanart=fanart,description="Most Played Movies Section.")
		kodi.addDir("Most Collected",'most_collected','call_trakt_movies',artwork+'most_collected.png','',1,'','',fanart=fanart,description="Most Collected Movies.")
		kodi.addDir("Box Office",'box_office','call_trakt_movies',artwork+'box_office.png','',1,'','',fanart=fanart,description="Movies in the Box Office.")
		kodi.addDir("Search",'','trakt_search_movies',artwork+'search.png','',1,'','', fanart=fanart,description="Search for Movies.")
		if kodi.get_setting('trakt_authorized') == 'true':
			kodi.addDir("[COLOR gold]My Movie Collection[/COLOR]",'my_collected','call_trakt_movies',artwork+'my_collection.png','',1,'','',fanart=fanart,description="View Your own Movie Collection.")
			kodi.addDir("[COLOR gold]Recomended for me[/COLOR]",'my_recomends','call_trakt_movies',artwork+'recomended.png','',1,'','',fanart=fanart,description="Movies recomended just for you!")
			kodi.addDir("[COLOR gold]Movie Watchlist[/COLOR]",'get_watchlist_movies','call_trakt_movies',artwork+'watchlist.png','',1,'','',fanart=fanart,description="Your Own Movie Watchlist.")
			kodi.addDir("[COLOR gold]Movies Watched Recently[/COLOR]",'get_watched_history','call_trakt_movies',artwork+'watchhistory.png','',1,'','',fanart=fanart,description="Your Watched Movie History.")
			kodi.addDir("[COLOR gold]My Custom Movie Lists[/COLOR]",'','custom_movie_lists',artwork+'custom_lists.png','',1,'',media,fanart=fanart,description="Here you will find your Custom Movie Lists and Creation.")
			#kodi.addDir("[COLOR gold]Search Other Users Movie Lists[/COLOR]",' ','get_user_lists',artwork+'other_user_lists.png','',1,'',media,fanart=fanart)

			#kodi.addDir("[COLOR gold]Special Movie Lists[/COLOR]",'','public_lists',artwork+'special_movie_lists.png','',1,'',media,fanart=fanart)
		viewsetter.set_view("seasons")

def tv_menu():

	media ='shows'
	kodi.addDir("Popular TV",'popular_tv','call_trakt_tv',artwork+'popular_tv.png','',1,'','',fanart=fanart,description="Popular TV Section.")
	kodi.addDir("Trending TV",'trending_tv','call_trakt_tv',artwork+'trending_tv.png','',1,'','',fanart=fanart,description="Trending TV Section.")
	kodi.addDir("Most Watched TV",'most_watched_tv','call_trakt_tv',artwork+'most_watched_tv.png','',1,'','',fanart=fanart,description="Most Watched TV Section.")
	kodi.addDir("Most Played TV",'most_played_tv','call_trakt_tv',artwork+'most_played_tv.png','',1,'','',fanart=fanart,description="Here you will find the Tv Shows that have been played the most.")
	kodi.addDir("Most Collected TV",'most_collected_tv','call_trakt_tv',artwork+'most_collected_tv.png','',1,'','',fanart=fanart,description="Here you will find the Tv Shows that have been collected the most..")
	kodi.addDir("Search",'','trakt_search_shows',artwork+'search.png','',1,'','',fanart=fanart,description="Search for any TV Show you would like.")
	if kodi.get_setting('trakt_authorized') == 'true':
			##kodi.addDir("[COLOR gold]Collected Episodes Not Watched[/COLOR]",'need_to_watch','call_trakt_tv',artwork+'tv_watchlist.png','',1,'','',fanart=fanart)
			kodi.addDir("[COLOR gold]Collected TV Shows[/COLOR]",'my_collected_tvshows','call_trakt_tv',artwork+'my_tv_collection.png','',1,'','',fanart=fanart,description="View Your own TV Show Collection.")
			kodi.addDir("[COLOR gold]Recomended TV Shows for me[/COLOR]",'my_recomends_tvshows','call_trakt_tv',artwork+'tv_recomended.png','',1,'','',fanart=fanart,description="TV Shows recomended just for you!.")
			kodi.addDir("[COLOR gold]TV Shows Watchlist [/COLOR]",'get_watchlist_tvshows','call_trakt_tv',artwork+'my_tv_watchlist.png','',1,'','',fanart=fanart,description="Your Own TV Show Watchlist..")
			#kodi.addDir("[COLOR gold]TV Shows Calendar[/COLOR]",'get_shows_calendar','call_trakt_tv',artwork+'watchlist.png','',1,'','',fanart=fanart)
			kodi.addDir("[COLOR gold]Anticipated TV Shows[/COLOR]",'get_anticipated_tvshows','call_trakt_tv',artwork+'tv_antic.png','',1,'','',fanart=fanart,description="Look through anticipated TV Shows.")
			kodi.addDir("[COLOR gold]Shows Watched Recently[/COLOR]",'get_watched_history','call_trakt_tv',artwork+'tv_watchhistory.png','',1,'','',fanart=fanart)
			kodi.addDir("[COLOR gold]My Custom TV Lists[/COLOR]",'','custom_movie_lists',artwork+'custom_lists.png','',1,'',media,fanart=fanart,description="Here you will find your Custom TV Show Lists and Creation.")
			kodi.addDir("[COLOR gold]Network TV Lists[/COLOR]",'','public_lists',artwork+'networks.png','',1,'',media,fanart=fanart,description="Look through all the greatest Tv Show Networks.")
	viewsetter.set_view("seasons")



def public_lists(media):
	if media == 'movies':
		kodi.addDir("[COLOR gold]Movist Movie Lists[/COLOR]",'','movistapp_lists',artwork+'special_movie_lists.png','',1,'',media,fanart=fanart)
		kodi.addDir('Marvel-Cinematic-Universe','donxy','get_public_lists',artwork+'special_movie_lists.png','',1,'marvel-cinematic-universe',media,fanart=fanart)
		kodi.addDir('Action Movie','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'action',media,fanart=fanart)
		kodi.addDir('Underground','justin','get_public_lists',artwork+'special_movie_lists.png','',1,'underground-network',media,fanart=fanart)

	if media == 'shows':
		kodi.addDir("[COLOR gold]NBC [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'nbc',media,fanart=fanart)
		kodi.addDir("[COLOR gold]CBS [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'cbs',media,fanart=fanart)
		kodi.addDir("[COLOR gold]ABC [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'abc',media,fanart=fanart)
		kodi.addDir("[COLOR gold]FOX [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'fox',media,fanart=fanart)
		kodi.addDir("[COLOR gold]CW [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'cw',media,fanart=fanart)
		kodi.addDir("[COLOR gold]HBO [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'hbo',media,fanart=fanart)

		kodi.addDir("[COLOR gold]A&E [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'a-and-e',media,fanart=fanart)
		kodi.addDir("[COLOR gold]AMC [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'amc',media,fanart=fanart)
		kodi.addDir("[COLOR gold]Animal Planet [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'animal-planet',media,fanart=fanart)
		kodi.addDir("[COLOR gold]BBC [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'bbc',media,fanart=fanart)
		kodi.addDir("[COLOR gold]Discovery Channel [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'discovery-channel',media,fanart=fanart)
		kodi.addDir("[COLOR gold]Hallmark [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'hallmark',media,fanart=fanart)

		kodi.addDir("[COLOR gold]Lifetime [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'lifetime',media,fanart=fanart)
		kodi.addDir("[COLOR gold]MTV [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'mtv',media,fanart=fanart)
		kodi.addDir("[COLOR gold]National GeographicC [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'nat-geo',media,fanart=fanart)
		kodi.addDir("[COLOR gold]TLC [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'tlc',media,fanart=fanart)
		kodi.addDir("[COLOR gold]TNT [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'tnt',media,fanart=fanart)
		kodi.addDir("[COLOR gold]Travel Channel [/COLOR]",'velocity2','get_public_lists',artwork+'networks.png','',1,'travel-channel',media,fanart=fanart)
	viewsetter.set_view("sets")



def movistapp_lists():
	kodi.addDir('[COLOR gold]Upcoming[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Upcoming',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Now Playing[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Now-Playing',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Popular Movies[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Popular-Movies',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Top Rated[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Top-Rated',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Action[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Action',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Adventure[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Adventure',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Animation[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Animation',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Comedy[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Comedy',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Crime[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Crime',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Drama[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Drama',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Family[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Family',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Fantasy[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Fantasy',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Foreign[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Foreign',media,fanart=fanart)
	kodi.addDir('[COLOR gold]History[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'History',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Horror[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Horror',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Music[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Music',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Mystery[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Mystery',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Romance[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Romance',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Science Fiction[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Science-Fiction',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Thriller[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Thriller',media,fanart=fanart)
	kodi.addDir('[COLOR gold]War[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'War',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Western[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Western',media,fanart=fanart)
	kodi.addDir('[COLOR gold]MARVEL[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'MARVEL',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Walt Disney Animated feature films[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Walt-Disney-Animated-feature-films',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Wallimage[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Wallimage',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Batman[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Batman',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Superman[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Superman',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Star Wars[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Star-Wars',media,fanart=fanart)
	kodi.addDir('[COLOR gold]007[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'007',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Pixar Animation Studios[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Pixar-Animation-Studios',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Quentin Tarantino Collection[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Quentin-Tarantino-Collection',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Rocky[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Rocky',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Box Office [/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Box-Office-',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Top Rental[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Top-Rental',media,fanart=fanart)
	kodi.addDir('[COLOR gold]New DVD Releases[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'New-DVD-Releases',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Upcoming DVD Releases[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Upcoming-DVD-Releases',media,fanart=fanart)
	kodi.addDir('[COLOR gold]DreamWorks Animation[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'DreamWorks-Animation',media,fanart=fanart)
	kodi.addDir('[COLOR gold]DC Comics[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'DC-Comics',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Christmas Movies[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Christmas-Movies',media,fanart=fanart)
	kodi.addDir('[COLOR gold]EMPIRE best of 2015[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'EMPIRE-best-of-2015',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Golden Globe Awards 2016[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Golden-Globe-Awards-2016',media,fanart=fanart)
	kodi.addDir('[COLOR gold]Documentary[/COLOR]','movistapp','get_public_lists',artwork+'special_movie_lists.png','',1,'Documentary',media,fanart=fanart)
	viewsetter.set_view("sets")


def call_trakt_tv(url):
	try:
		#Auth TV SHOWS
		media = 'shows'
		#TODO FIX THIS
		if url == 'need_to_watch':
			try:
				#link = trakt_api.get_calendar_shows()
				link = trakt_api.get_my_collected_tvshows()#*** THIS ALMOST WORKS
				#link = trakt_api.get_watched_history('shows')
				#link = trakt_api.get_calendar_episodes(delta=1, number=2)
				#link = trakt_api.get_calendar_daily_shows(delta=0, number=1)
				for e in link:
					infoLabels={}
					infoLabels.update(make_infoLabels(e,media=media))
					orig_ids1 = e
					orig_ids = json.dumps(orig_ids1)
					show_trakt_id = str(infoLabels['trakt_id'])
					show_year = str(infoLabels['year'])
					show_name = infoLabels['title'].encode('utf-8')
					orig_name = show_name+' ('+show_year+')'
					link = trakt_api.get_show_progress(show_trakt_id)
					if link['next_episode'] is not None:
						epi = link['next_episode']
						title = epi['title'].encode('utf-8')
						season = epi['season']
						episode = epi['number']
						trakt = epi['ids']
						trakt_id = trakt['trakt']
						infoLabels = trakt_api.get_episode_details(show_trakt_id,season,episode)
						aired = infoLabels['premiered']
						menu_items=[]
						trailer = infoLabels['trailer_url']
						year = str(infoLabels['year'])
						name = infoLabels['title'].encode('utf-8')
						if name == 'TBA':
							name = '[COLORred]'+name+'[/COLOR]'
						else:
							name = '[COLORgreen]'+name+'[/COLOR]'

						thumb=infoLabels['cover_url']
						if thumb is None:
							thumb = ''
						d1 = str(infoLabels['premiered'])
						d2 = str(datetime.date.today())
						#print today - was_aired
						#if infoLabels['premiered'] =='':
						if d1 >= d2 or infoLabels['premiered'] == '':
							if name :
								menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))

								kodi.addDir('[COLOR red]S'+str(season)+'E'+str(episode)+'  '+orig_name+' / '+name+'[/COLOR]','','findsource',thumb,orig_name,5,'','shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=True,orig_ids=orig_ids)
						else:
							if 'null' in trailer or trailer == '':
								menu_items.append(('[COLOR gold]Add to Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'pick_custom_list', 'name':name, 'media':media})))
								menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
								menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
								#menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
							else:
								utube = tools.make_trailer(trailer)
								menu_items.append(('[COLOR gold]Add to Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'pick_custom_list', 'name':name, 'media':media})))
								menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
								menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
								#menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
								menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))
							kodi.addDir('S'+str(season)+'E'+str(episode)+'  '+orig_name+' / '+name,'','findsource',thumb,orig_name,5,'','shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=True,orig_ids=orig_ids)
						viewsetter.set_view('tvshows')
			except Exception as e:
				log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
				if kodi.get_setting('error_notify') == "true":
					kodi.notify(header='On Deck TV',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)
		else:
			if url == 'get_watched_history':
				link = trakt_api.get_history('show')

			if url == 'get_anticipated_tvshows':
				link = trakt_api.get_anticipated_tvshows()
			if url == 'get_shows_calendar':
				link = trakt_api.get_calendar_shows()
			if url == 'get_watchlist_tvshows':
				link = trakt_api.get_watchlist_tvshows()
			if url == 'my_recomends_tvshows':
				link = trakt_api.get_recommended_tvshows()
			if url == 'my_collected_tvshows':
				link = trakt_api.get_my_collected_tvshows()

			#TV STANDARD LISTS
			if url =='popular_tv':
				link = trakt_api.get_popular_tvshows()
			if url == 'trending_tv':
				link = trakt_api.get_trending_tvshows()
			if url == 'most_watched_tv':
				link = trakt_api.get_most_watched_tvshows()
			if url == 'most_played_tv':
				link = trakt_api.get_most_played_tvshows()
			if url == 'most_collected_tv':
				link = trakt_api.get_most_collected_tvshows()
#Sorting Here
			if  kodi.get_setting('sort_tv') == "2":
				try:
					sorted_list = sorted(link, key=lambda k: (str(k['year'])))
				except:
					sorted_list = sorted(link, key=lambda k: (str(k['show']["year"])))
			elif  kodi.get_setting('sort_tv') == "1":
				try:
					sorted_list =sorted(link, key=lambda k: re.sub('(^the |^a )', '', k['title'].lower()))
				except:
					sorted_list = sorted(link, key=lambda k: re.sub('(^the |^a )','',(str(k['show']["title"].lower()))))
			else:
					sorted_list = link
#End Sort Order
			for e in sorted_list:
					if url == 'get_watched_history' and e['type'] == 'movie':
						print "THIS IS A MOVIE >>> " + e['movie']['title']
					else:
						# print "THIS IS A TV SHOW >>> " + e['episode']['title']
						infoLabels={}
						infoLabels.update(make_infoLabels(e,media=media))
						trailer = infoLabels['trailer_url']
						trakt_id = str(infoLabels['trakt_id'])
						orig_ids1 = e
						orig_ids=json.dumps(orig_ids1)
						imdb = str(infoLabels['imdb_id'])
						year = str(infoLabels['year'])
						name = infoLabels['title'].encode('utf-8')
						thumb=infoLabels['cover_url']
						################
						was_watched=watched_cache.get_watched_cache(trakt_id)
						if was_watched is not None:
							infoLabels['playcount'] = 1
						################
						if thumb is None:
							thumb = ''
						##WATCHED STATS

						#WATCHED STUFF
							# TODO FIX REFRESH
						menu_items=[]
						if kodi.get_setting('trakt_authorized') == 'true':
							menu_items.append(('[COLOR gold]Add to Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'pick_custom_list', 'name':name, 'media':media})))
							menu_items.append(('[COLOR gold]Find Similar Shows[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'similar_shows', 'name':name})))
						menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
						if url == 'my_collected_tvshows':
							menu_items.append(('[COLOR gold]Remove From Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_collection', 'name':name, 'media':media})))
						else:
							if kodi.get_setting('trakt_authorized') == 'true':
								menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
						if url == 'get_watchlist_tvshows':
							menu_items.append(('[COLOR gold]Remove From Watchlist[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_watchlist', 'name':name, 'media':media})))
						else:
							if kodi.get_setting('trakt_authorized') == 'true':
								menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
						if trailer:
							utube = tools.make_trailer(trailer)
							menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))
						kodi.addDir(name+' ('+year+')','','find_season',thumb,name,5,trakt_id,'shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=False,orig_ids=orig_ids)
						viewsetter.set_view('tvshows')
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Trakt TV',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)





def find_season(name,trakt_id,orig_ids):

	try:
		media = 'shows'
		movie_title =name
		link = trakt_api.get_show_seasons(trakt_id)
		for e in link:
					eid = e['ids']
					infoLabels={}
					infoLabels.update(trakt_api.process_show(e))
					infoLabels.update(make_show_seasons_art(orig_ids))
					if infoLabels['cover_url'] == None:
						infoLabels['cover_url'] = artwork+'place_poster.png'
					infoLabels['plot'] = movie_title+ " Season "+str(infoLabels['number'])
					menu_items=[]
					menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
					kodi.addDir('Season '+str(infoLabels['number']),'','find_episode',infoLabels['cover_url'],movie_title,5,trakt_id,'shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=True)
					viewsetter.set_view('seasons')
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Trakt Seasons',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)


def find_episode(name,trakt_id,movie_title):

	try:
		media ='episode'
		season = name.replace('Season ','')
		link = trakt_api.get_show_episodes(trakt_id,season)
		for e in link:
			ep_trakt_id= e['ids']['trakt']
			infoLabels={}
			infoLabels.update(make_infoLabels(e,media='episodes'))
			episode = infoLabels['episode']
			infoLabels = trakt_api.get_episode_details(trakt_id,season,episode)
			infoLabels.update(make_infoLabels(e, media='episodes'))
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
			d1 = str(infoLabels['premiered'])
			d2 = str(datetime.date.today())
			if d1 >= d2 or infoLabels['premiered'] == '':
				if name is not '':
					menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
					kodi.addDir('[COLOR maroon]S'+str(season)+'E'+str(episode)+'  '+name+'[/COLOR]','','findsource',thumb,movie_title,5,'','shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=True)
			else:
				menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
				if kodi.get_setting('trakt_authorized') == 'true':
					menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':ep_trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
				kodi.addDir('S'+str(season)+'E'+str(episode)+'  '+name,'','findsource',thumb,movie_title,5,'','shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=True)
			viewsetter.set_view('episodes')
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Trakt Episodes',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)




# TODO FIX MENU LISTING
def similar_shows(trakt_id):
	try:
		media = 'shows'
		link =trakt_api.get_similar_tvshows(trakt_id)
		for e in link:
					infoLabels = trakt_api.process_show(e)
					menu_items=[]
					trailer = infoLabels['trailer_url']
					trakt_id = str(infoLabels['trakt_id'])
					# ################TODO     FIX WATCHES
					# was_watched=watched_cache.get_watched_cache(trakt_id)
					# if was_watched is not None:
					# 	infoLabels['playcount'] = 1
					# ################
					imdb = str(infoLabels['imdb_id'])
					year = str(infoLabels['year'])
					name = infoLabels['title'].encode('utf-8')
					thumb=infoLabels['cover_url']
					if thumb is None:
						thumb = ''
					menu_items=[]
					if kodi.get_setting('trakt_authorized') == 'true':
						menu_items.append(('[COLOR gold]Find Similar Shows[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'similar_shows', 'name':name})))
					menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
					if url == 'get_watchlist_tvshows':
						menu_items.append(('[COLOR gold]Remove From Watchlist[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_watchlist', 'name':name, 'media':media})))
					else:
						if kodi.get_setting('trakt_authorized') == 'true':
							menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
					if trailer:
						utube = tools.make_trailer(trailer)
						menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))
					kodi.addDir(name+' ('+year+')','','find_season',thumb,name,5,trakt_id,'shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=False)
					viewsetter.set_view('tvshows')
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Similar SHows Error',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)


def call_trakt_movies(url):

	try:
		media = 'movies'
		if url == 'get_watched_history':
			link = trakt_api.get_history('movie')
		if url == 'get_watchlist_movies':
			link = trakt_api.get_watchlist_movies()
		if url == 'my_recomends':
			link = trakt_api.get_recommended_movies()
		if url == 'my_collected':
			link = trakt_api.get_my_collected()
		#MOVIE Standard Lists
		if url == 'trending':
			link = trakt_api.get_trending_movies()
		if url =='popular':
			link = trakt_api.get_popular_movies()
		if url == 'most_watched':
			link = trakt_api.get_most_watched_movies()
		if url == 'most_played':
			link = trakt_api.get_most_played_movies()
		if url == 'most_collected':
			link = trakt_api.get_most_collected_movies()
		if url == 'box_office':
			link = trakt_api.get_boxoffice_movies()
#Sorting Here
		if  kodi.get_setting('sort_movies') == "2":
			try:
				sorted_list = sorted(link, key=lambda k: (str(k['year'])))
			except:
				sorted_list = sorted(link, key=lambda k: (str(k['movie']["year"])))
		elif  kodi.get_setting('sort_movies') == "1":
			try:
				sorted_list =sorted(link, key=lambda k: re.sub('(^the |^a )', '', k['title'].lower()))
			except:
				sorted_list = sorted(link, key=lambda k: re.sub('(^the |^a )','',(str(k['movie']["title"].lower()))))
		else:
				sorted_list = link
#End Sort Order
		for e in sorted_list:
			if url != 'get_watched_history' or e['type'] == 'movie':
				infoLabels={}
				infoLabels.update(make_infoLabels(e,media=media))
				menu_items=[]
				trakt_id = str(infoLabels['trakt_id'])
				################
				was_watched=watched_cache.get_watched_cache(trakt_id)
				if was_watched is not None:
					infoLabels['playcount'] = 1
				################
				trailer = infoLabels['trailer_url']
				year = str(infoLabels['year'])
				name = infoLabels['title'].encode('utf-8')
				thumb=infoLabels['cover_url']
				if thumb is None:
					thumb = ''
				if url == 'my_collected':
					menu_items.append(('[COLOR gold]Remove From Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_collection', 'name':name, 'media':media})))
				else:
					if kodi.get_setting('trakt_authorized') == 'true':
						menu_items.append(('[COLOR gold]Add to Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'pick_custom_list', 'name':name, 'media':media})))
						menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
						menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
				if url == 'get_watchlist_movies':
						menu_items.append(('[COLOR gold]Remove From Watchlist[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_watchlist', 'name':name, 'media':media})))
				else:
					if kodi.get_setting('trakt_authorized') == 'true':
						menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
				menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
				if trailer:
					utube = tools.make_trailer(trailer)
					menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))


				kodi.addDir(name+' ('+year+')','','findsource',thumb,name,5,'','movies',meta_data=infoLabels,menu_items=menu_items,replace_menu=False,movie_meta=e)
				viewsetter.set_view("movies")
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Trakt Movies',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)


def pick_source_dialog(hosters):
    for item in hosters:
        if item['multi-part']:
            continue
        item['label'] = utils2.format_source_label(item)

    dialog = xbmcgui.Dialog()
    index = dialog.select(i18n('choose_stream'), [item['label'] for item in hosters if 'label' in item])
    if index > -1:
        try:
            hoster = hosters[index]
            if hoster['url']:
                hoster_url = hoster['class'].resolve_link(hoster['url'])
                log_utils.log('Attempting to play url: %s as direct: %s from: %s' % (hoster_url, hoster['direct'], hoster['class'].get_name()))
                return hoster_url, hoster['direct']
        except Exception as e:
            log_utils.log('Error (%s) while trying to resolve %s' % (str(e), hoster['url']), xbmc.LOGERROR)

    return None, None


def pick_custom_list(media,trakt_id):
	get_lists = trakt_api.get_custom_lists()
	for e in get_lists:
		list_id = e['ids']
		slug_id=list_id['slug']
		name_id = e['name']
		dialog = xbmcgui.Dialog()
		index = dialog.select('Choose Custom List', [e['name'] for e in get_lists if 'name' in e])
		if index >=-1:
			picked_item = int(index)
			picked_list =  [e['name'] for e in get_lists if 'name' in e]
			end_list = picked_list[picked_item]
			print "PICKED ITEM< :"+media+trakt_id+'  '+end_list
			add_to_custom(media,trakt_id,end_list)
			break


def add_to_custom(media,trakt_id,list):
	list = list.replace(' ','-')
	link =trakt_api.add_to_custom_list(media,list,trakt_id)
	xbmc.executebuiltin("XBMC.Container.Refresh")
	if media == 'movies': media = 'movie'
	if media == 'shows': media = 'show'
	kodi.notify(header='Trakt Says:',msg='Your '+media+' has been added',duration=3000,sound=None)


def del_from_custom(media,trakt_id,name):
	list = name.replace(' ','-')
	print media + trakt_id + list
	link =trakt_api.delete_from_custom_list(media,list,trakt_id)
	xbmc.executebuiltin("XBMC.Container.Refresh")
	if media == 'movies': media = 'movie'
	if media == 'shows': media = 'show'
	kodi.notify(header='Trakt Says:',msg='Your '+media+' has been removed',duration=3000,sound=None)

def add_collection(media,trakt_id):
	trakt_api.add_to_collection(media, trakt_id)
	xbmc.executebuiltin("XBMC.Container.Refresh")
	if media == 'movies': media = 'movie'
	if media == 'shows': media = 'show'
	kodi.notify(header='Trakt Says:',msg='Your '+media+' has been added',duration=3000,sound=None)
	#return

def remove_collection(media,trakt_id):
	trakt_api.remove_from_collection(media, trakt_id)
	xbmc.executebuiltin("XBMC.Container.Refresh")
	if media == 'movies': media = 'movie'
	if media == 'shows': media = 'show'
	kodi.notify(header='Trakt Says:',msg='Your '+media+' has been removed',duration=3000,sound=None)
	#return



def add_watchlist(media,trakt_id):
	link =trakt_api.add_to_watchlist(media,trakt_id)
	xbmc.executebuiltin("XBMC.Container.Refresh")
	if media == 'movies': media = 'movie'
	if media == 'shows': media = 'show'
	kodi.notify(header='Trakt Says:',msg='Your '+media+' has been added',duration=3000,sound=None)
# 	TODO Add Notificatiopn of success



def remove_watchlist(media,trakt_id):
	link =trakt_api.delete_from_watchlist(media,trakt_id)
	xbmc.executebuiltin("XBMC.Container.Refresh")
	if media == 'movies': media = 'movie'
	if media == 'shows': media = 'show'
	kodi.notify(header='Trakt Says:',msg='Your '+media+' has been removed',duration=3000,sound=None)

#TODO  FIX CACHING ISSUES WITH WATCHED STATUS UPDATES

def add_watched_history(media,trakt_id,season=None):
	trakt_api.set_watched_state(media, trakt_id, watched=True, season=None)
	watched_cache.set_watch_cache(trakt_id,media)
	if media == 'movies': media = 'movie'
	if media == 'shows': media = 'show'
	xbmc.executebuiltin("XBMC.Container.Refresh")
	kodi.notify(header='Trakt Says:',msg='Your '+media+' has been added as watched',duration=3000,sound=None)
	return

def del_watched_history(media,trakt_id,season=None):
	trakt_api.set_watched_state(media, trakt_id, watched=False, season=None)
	watched_cache.del_watch_cache(trakt_id,media)
	xbmc.executebuiltin("XBMC.Container.Refresh")
	if media == 'movies': media = 'movie'
	if media == 'shows': media = 'show'
	kodi.notify(header='Trakt Says:',msg='Your '+media+' has been removed',duration=3000,sound=None)



#Start Ketboard Function
def _get_keyboard( default="", heading="", hidden=False ):
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default

def custom_movie_lists(media):
	kodi.addDir('[COLOR gold]Create New Custom List[/COLOR]','','make_new_list',artwork+'new_list_trakt.png','',1,'',media,fanart=fanart)

	get_lists = trakt_api.get_custom_lists()
	for e in get_lists:
		list_id = e['ids']
		slug_id=list_id['slug']
		trakt_id=str(list_id['trakt'])
		name_id = e['name']
		if media =='movies':
			kodi.addDir(name_id,'','custom_list_view',artwork+'custom_list_trakt.png','',1,slug_id,media,fanart=fanart)
		if media == 'shows':
			kodi.addDir(name_id,'','custom_list_view_tv',artwork+'custom_list_trakt.png','',1,slug_id,media,fanart=fanart)
	viewsetter.set_view("movies")



def make_new_list():
	trakt_api=trakt.TraktAPI()
	vq = _get_keyboard( heading="Enter New Custom List Name Desired" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	title = title.replace('+',' ')
	trakt_api.create_custom_list(title)


def custom_list_view(trakt_id,media):
	try:
		if media =='movies':media = 'movie'
		slug_id = trakt_id
		lists = trakt_api.get_custom_list(slug_id,media)#is actually SLUG ID
		for e in lists:
			infoLabels = trakt_api.process_movie(e)
			infoLabels.update(make_infoLabels(e,media='movies'))
			menu_items=[]
			trakt_id = str(infoLabels['trakt_id'])
			trailer = infoLabels['trailer_url']
			year = str(infoLabels['year'])
			name = infoLabels['title'].encode('utf-8')
			thumb=infoLabels['cover_url']
			if thumb is None:
				thumb = ''
			menu_items.append(('[COLOR gold]Remove From Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'del_from_custom', 'name':slug_id, 'media':media})))
			menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
			menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
			menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
			menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
			if trailer:
				utube = tools.make_trailer(trailer)
				menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))
			kodi.addDir(name+' ('+year+')','','findsource',thumb,name,5,'','movies',meta_data=infoLabels,menu_items=menu_items,replace_menu=False)
			viewsetter.set_view("sets")
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Custom List Error',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)

def custom_list_view_tv(trakt_id,media):
	try:
		if media=='shows':media = 'show'
		slug_id = trakt_id
		lists = trakt_api.get_custom_list(slug_id,media)#is actually SLUG ID
		for e in lists:
			infoLabels = trakt_api.process_movie(e)
			infoLabels.update(make_infoLabels(e,media='shows'))
			orig_ids1 = e
			orig_ids = json.dumps(orig_ids1)
			menu_items=[]
			trakt_id = str(infoLabels['trakt_id'])
			trailer = infoLabels['trailer_url']
			year = str(infoLabels['year'])
			name = infoLabels['title'].encode('utf-8')
			thumb=infoLabels['cover_url']
			if thumb is None:
				thumb = ''
			menu_items.append(('[COLOR gold]Remove From Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'del_from_custom', 'name':slug_id, 'media':media})))
			menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
			menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
			menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
			menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
			if trailer:
				utube = tools.make_trailer(trailer)
				menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))

			kodi.addDir(name+' ('+year+')','','find_season',thumb,name,5,trakt_id,'shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=False,orig_ids=orig_ids)
			viewsetter.set_view("sets")
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Custom List Error',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)

def get_public_lists(url,trakt_id,media):
	try:
		username = url
		link = trakt_api.get_special_list(trakt_id,media,username=username)
#Sorting Here
		if  kodi.get_setting('sort_tv') == "2":
			try:
				sorted_list = sorted(link, key=lambda k: (str(k['year'])))
			except:
				sorted_list = sorted(link, key=lambda k: (str(k['show']["year"])))
		elif  kodi.get_setting('sort_tv') == "1":
			try:
				sorted_list =sorted(link, key=lambda k: re.sub('(^the |^a )', '', k['title'].lower()))
			except:
				sorted_list = sorted(link, key=lambda k: re.sub('(^the |^a )','',(str(k['show']["title"].lower()))))
		else:
				sorted_list = link
#End Sort Order

		for e in sorted_list:
			if media =='movies':
				infoLabels={}
				infoLabels.update(make_infoLabels(e,media=media))
				menu_items=[]
				trakt_id = str(infoLabels['trakt_id'])
				################
				was_watched=watched_cache.get_watched_cache(trakt_id)
				if was_watched is not None:
					infoLabels['playcount'] = 1
				################
				trailer = infoLabels['trailer_url']
				year = str(infoLabels['year'])
				name = infoLabels['title'].encode('utf-8')
				thumb=infoLabels['cover_url']
				if thumb is None:
					thumb = ''
				if url == 'my_collected':
					menu_items.append(('[COLOR gold]Remove From Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_collection', 'name':name, 'media':media})))
				else:
					menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
				menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
				if url == 'get_watchlist_movies':
						menu_items.append(('[COLOR gold]Remove From Watchlist[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_watchlist', 'name':name, 'media':media})))
				else:
						menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
				menu_items.append(('[COLOR gold]Add to Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'pick_custom_list', 'name':name, 'media':media})))
				menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
				if trailer:
					utube = tools.make_trailer(trailer)
					menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))
				kodi.addDir(name+' ('+year+')','','findsource',thumb,name,5,'','movies',meta_data=infoLabels,menu_items=menu_items,replace_menu=False)
				viewsetter.set_view("movies")

			if media == 'shows':
				infoLabels={}####################TYPO     FIXED
				infoLabels.update(make_infoLabels(e,media=media))
				trailer = infoLabels['trailer_url']
				trakt_id = str(infoLabels['trakt_id'])
				################
				was_watched=watched_cache.get_watched_cache(trakt_id)
				if was_watched is not None:
					infoLabels['playcount'] = 1
				################
				imdb = str(infoLabels['imdb_id'])
				year = str(infoLabels['year'])
				name = infoLabels['title'].encode('utf-8')
				thumb=infoLabels['cover_url']
				if thumb is None:
					thumb = ''
					# TODO FIX REFRESH
				menu_items=[]
				menu_items.append(('[COLOR gold]Find Similar Shows[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'similar_shows', 'name':name})))
				menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
				if url == 'my_collected_tvshows':
					menu_items.append(('[COLOR gold]Remove From Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_collection', 'name':name, 'media':media})))
				else: menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
				if url == 'get_watchlist_tvshows':
					menu_items.append(('[COLOR gold]Remove From Watchlist[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_watchlist', 'name':name, 'media':media})))
				else:
					menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
				if trailer:
					utube = tools.make_trailer(trailer)
					menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))
				menu_items.append(('[COLOR gold]Add to Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'pick_custom_list', 'name':name, 'media':media})))
				kodi.addDir(name+' ('+year+')','','find_season',thumb,name,5,trakt_id,'shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=False)
				viewsetter.set_view("tvshows")
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Public List Error',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)



def get_user_lists(media):
	try:
		media = media
		name =otherinput()
		get_lists = trakt_api.get_user_lists(name,media)
		for e in get_lists:
			list_id = e['ids']
			slug_id=list_id['slug']
			trakt_id=str(list_id['trakt'])
			name_id = e['name']
			if kodi.get_setting('grab_xml') == "true":
				print '<name>'+name_id+'</name>'
				print '<slug>'+trakt_id+'</slug>'
			kodi.addDir(name_id,name,'user_list_view',artwork+'custom_list_trakt.png','',1,slug_id,media,fanart=fanart)
		viewsetter.set_view("sets")
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Search List Error',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)



def user_list_view(url,trakt_id,media):
	username= url
	lists = trakt_api.get_users_list(trakt_id,media,username=username)
	for e in lists:
		infoLabels={}
		infoLabels.update(make_infoLabels(e,media=media))
		menu_items=[]
		trakt_id = str(infoLabels['trakt_id'])
		trailer = infoLabels['trailer_url']
		year = str(infoLabels['year'])
		name = infoLabels['title'].encode('utf-8')
		thumb=infoLabels['cover_url']
		if thumb is None:
			thumb = ''
		if url == 'my_collected':
			menu_items.append(('[COLOR gold]Remove From Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_collection', 'name':name, 'media':media})))
		else:
			menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
		menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
		if url == 'get_watchlist_movies':
				menu_items.append(('[COLOR gold]Remove From Watchlist[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_watchlist', 'name':name, 'media':media})))
		else:
				menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
		menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
		if trailer:
			utube = tools.make_trailer(trailer)
			menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))
		kodi.addDir(name+' ('+year+')','','findsource',thumb,name,5,'','movies',meta_data=infoLabels,menu_items=menu_items,replace_menu=False)
		viewsetter.set_view("movies")

def otherinput():
	vq = _get_keyboard( heading="Enter Your Query" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	return title


#Start Search Function
def trakt_search_movies(url):
	if not url:
		url = _get_keyboard( heading="Searching for Movies" )
		if ( not url ): return False, 0
	media = 'movies'
	title = urllib.quote_plus(url)
	link = trakt_api.search_movies(title)
	for e in link:
		infoLabels={}
		infoLabels.update(make_infoLabels(e,media=media))
		menu_items=[]
		trakt_id = str(infoLabels['trakt_id'])
		################
		was_watched=watched_cache.get_watched_cache(trakt_id)
		if was_watched is not None:
			infoLabels['playcount'] = 1
		################
		trailer = infoLabels['trailer_url']
		year = str(infoLabels['year'])
		name = infoLabels['title'].encode('utf-8')
		thumb=infoLabels['cover_url']
		if thumb is None:
			thumb = ''
		if url == 'my_collected':
			menu_items.append(('[COLOR gold]Remove From Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_collection', 'name':name, 'media':media})))
		else:
			menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
		menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
		if url == 'get_watchlist_movies':
				menu_items.append(('[COLOR gold]Remove From Watchlist[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_watchlist', 'name':name, 'media':media})))
		else:
				menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
		menu_items.append(('[COLOR gold]Add to Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'pick_custom_list', 'name':name, 'media':media})))
		menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
		if trailer:
			utube = tools.make_trailer(trailer)
			menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))


		kodi.addDir(name+' ('+year+')','','findsource',thumb,name,5,'','movies',meta_data=infoLabels,menu_items=menu_items,replace_menu=False)
		viewsetter.set_view("movies")


def trakt_search_shows(url):
	if not url:
		url = _get_keyboard( heading="Searching for Shows" )
		if ( not url ): return False, 0
	media = 'shows'
	title = urllib.quote_plus(url)
	link = trakt_api.search_tv(title)
	for e in link:

		infoLabels = {}
		infoLabels.update(make_infoLabels(e, media=media))
		trailer = infoLabels['trailer_url']
		trakt_id = str(infoLabels['trakt_id'])
		orig_ids1 = e
		orig_ids = json.dumps(orig_ids1)
		################
		was_watched=watched_cache.get_watched_cache(trakt_id)
		if was_watched is not None:
			infoLabels['playcount'] = 1
		################
		imdb = str(infoLabels['imdb_id'])
		year = str(infoLabels['year'])
		name = infoLabels['title'].encode('utf-8')
		thumb=infoLabels['cover_url']
		if thumb is None:
			thumb = ''
			# TODO FIX REFRESH
		menu_items=[]
		menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
		#menu_items.append(('[COLOR gold]Mark as Watched[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watched_history', 'name':name, 'media':media})))
		menu_items.append(('[COLOR gold]Add to Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'pick_custom_list', 'name':name, 'media':media})))
		menu_items.append(('[COLOR gold]Find Similar Shows[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'similar_shows', 'name':name})))
		menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
		if url == 'get_watchlist_tvshows':
			menu_items.append(('[COLOR gold]Remove From Watchlist[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_watchlist', 'name':name, 'media':media})))
		else:
			menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
		if trailer:
			utube = tools.make_trailer(trailer)
			menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))
		kodi.addDir(name+' ('+year+')','','find_season',thumb,name,5,trakt_id,'shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=False,orig_ids=orig_ids)
		viewsetter.set_view("tvshows")



def fancy_list(url):
	try:
		link = trakt_api.get_popular_networks()
		searchnet = url
		for e in link:

			infoLabels={}
			infoLabels.update(make_infoLabels(e))
			trailer = infoLabels['trailer_url']
			trakt_id = str(infoLabels['trakt_id'])
			imdb = str(infoLabels['imdb_id'])
			year = str(infoLabels['year'])
			name = infoLabels['title'].encode('utf-8')
			thumb=infoLabels['cover_url']
			network=infoLabels['network']
			################
			was_watched=watched_cache.get_watched_cache(trakt_id)
			#print "RETURNED ITEM IS "+str(was_watched)
			if was_watched is not None:
				infoLabels['playcount'] = 1
			################
			if thumb is None:
				thumb = ''
			##WATCHED STATS
			if network == searchnet:
				#WATCHED STUFF
					# TODO FIX REFRESH
				menu_items=[]
				if kodi.get_setting('trakt_authorized') == 'true':
					menu_items.append(('[COLOR gold]Add to Custom List[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'pick_custom_list', 'name':name, 'media':media})))
					menu_items.append(('[COLOR gold]Find Similar Shows[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'similar_shows', 'name':name})))
				menu_items.append(('[COLOR gold]Show Information[/COLOR]', 'XBMC.Action(Info)'))
				if url == 'my_collected_tvshows':
					menu_items.append(('[COLOR gold]Remove From Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_collection', 'name':name, 'media':media})))
				else:
					if kodi.get_setting('trakt_authorized') == 'true':
						menu_items.append(('[COLOR gold]Add to Collection[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_collection', 'name':name, 'media':media})))
				if url == 'get_watchlist_tvshows':
					menu_items.append(('[COLOR gold]Remove From Watchlist[/COLOR]', 'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'remove_watchlist', 'name':name, 'media':media})))
				else:
					if kodi.get_setting('trakt_authorized') == 'true':
						menu_items.append(('[COLOR gold]Add to Watchlist[/COLOR]',      'RunPlugin(%s)' % addon.build_plugin_url({'trakt_id':trakt_id, 'mode':'add_watchlist', 'name':name, 'media':media})))
				if trailer:
					utube = tools.make_trailer(trailer)
					menu_items.append(('[COLOR gold]Play Trailer[/COLOR]', 'PlayMedia('+utube+',xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image))'))
				kodi.addDir(name+' ('+year+')','','find_season',thumb,name,5,trakt_id,'shows',meta_data=infoLabels,menu_items=menu_items,replace_menu=False)
				viewsetter.set_view("tvshows")
	except Exception as e:
		log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
		if kodi.get_setting('error_notify') == "true":
			kodi.notify(header='Trakt TV',msg='(error) %s  %s' % (str(e), ''),duration=5000,sound=None)




#################
def make_infoLabels(item,media=None, show=None, people=None, orig_ids=None):
	try:
			item = item['movie']
	except:
		try:
			item = item['show']
		except:
			item = item
	#kodi.log(item)
	if people is None: people = {}
	if show is None: show = {}
	infoLabels = {}
	infoLabels['mediatype'] = 'tvshow' if 'aired_episodes' in item else 'movie'
	if 'title' in item: infoLabels['title'] = item['title']
	if 'network' in item: infoLabels['network'] = item['network']
	if 'overview' in item: infoLabels['plot'] = infoLabels['plotoutline'] = item['overview']
	if 'runtime' in item and item['runtime'] is not None: infoLabels['duration'] = item['runtime'] * 60
	if 'certification' in item: infoLabels['mpaa'] = item['certification']
	if 'year' in item: infoLabels['year'] = item['year']
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
	if 'season' in item: infoLabels['season'] = item['season']  # needs check
	if 'episode' in item: infoLabels['episode'] = item['episode']  # needs check
	if 'number' in item: infoLabels['episode'] = item['number']  # needs check
	infoLabels.update(make_ids(item))
	if media == 'movies':
		infoLabels.update(make_art(item))
	if media == 'shows':
		infoLabels.update(make_show_art(item))
	if media == 'seasons':
		infoLabels.update(make_show_seasons_art(item))
	if media == 'episodes':
		infoLabels.update(make_show_episodes_art(item))

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


##NEW IMAGE GET
def make_art(item):
	try:
		try:
			art = image_scraper.get_images('movies', item['ids'])
		except Exception as e:
			log_utils.log('Error [%s]  %s' % (str(e), ''), xbmc.LOGERROR)
			if kodi.get_setting('error_notify') == "true":
				kodi.notify(header='Image Scraping', msg='(error) %s  %s' % (str(e), ''), duration=5000, sound=None)
		infoLabels= {}
		infoLabels['thumb_url'] = art['thumb']
		infoLabels['cover_url'] = art['poster']
		infoLabels['backdrop_url'] = art['fanart']
	except :
		infoLabels = {}

	return infoLabels

def make_show_art(item):
	try:
		art = image_scraper.get_images('shows', item['ids'])
		#kodi.log(art)
		infoLabels= {}
		infoLabels['thumb_url'] = art['thumb']
		infoLabels['cover_url'] = art['poster']
		infoLabels['backdrop_url'] = art['fanart']
	except :
		infoLabels = {}

	return infoLabels


def make_show_seasons_art(item):
	newIds = json.loads(item)
	try:
		end_ids = newIds['ids']
	except:
		end_ids = newIds['show']['ids']
	art = image_scraper.get_images('seasons', end_ids)
	infoLabels = {}
	infoLabels['thumb_url'] = art['thumb']
	infoLabels['cover_url'] = art['poster']
	infoLabels['backdrop_url'] = art['fanart']
	return infoLabels

def make_show_episodes_art(item):
	if 'season' in item: season = item['season']  # needs check
	if 'episode' in item: episode = item['episode']  # needs check
	if 'number' in item: episode = item['number']  # needs check
	try:
		art = image_scraper.get_images('episodes', item['ids'],season=season,episode=episode,screenshots=True)
		infoLabels= {}
		infoLabels['thumb_url'] = art['thumb']
		infoLabels['cover_url'] = art['poster']
		infoLabels['backdrop_url'] = art['fanart']
	except :
		infoLabels = {}
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



def de_auth():
	kodi.set_setting('trakt_oauth_token', "")
	kodi.set_setting('trakt_refresh_token', "")
	kodi.set_setting('trakt_authorized', "false")
	kodi.set_setting('trakt_username',"")



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

try:
		orig_ids=urllib.unquote_plus(params["orig_ids"])
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

elif mode=='de_auth':
		de_auth()
		xbmc.executebuiltin("XBMC.Container.Refresh")

elif mode=='call_trakt_movies':
		call_trakt_movies(url)

elif mode=='call_trakt_tv':
		call_trakt_tv(url)

elif mode=='movie_menu':
		movie_menu()

elif mode=='do_settings':
		do_settings()

elif mode=='tv_menu':
		tv_menu()

elif mode=='public_lists':
		public_lists(media)

elif mode=='similar_shows':
		similar_shows(trakt_id)

elif mode=='add_watchlist':
		add_watchlist(media,trakt_id)

elif mode=='add_collection':
		add_collection(media,trakt_id)

elif mode=='remove_collection':
		remove_collection(media,trakt_id)

elif mode=='add_watched_history':
		add_watched_history(media,trakt_id)

elif mode=='del_watched_history':
		del_watched_history(media,trakt_id)

elif mode=='remove_watchlist':
		remove_watchlist(media,trakt_id)

elif mode=='trakt_search_movies':
		trakt_search_movies(url)

elif mode=='fancy_list':
		fancy_list(url)

elif mode=='trakt_search_shows':
		trakt_search_shows(url)


elif mode=='playiwatchonlink':
		iwatchonline.playiwatchonlink(url,movie_title,thumb)


elif mode=='playprimelink':
		primewire.playprimelink(url,movie_title,thumb)  #########MAY REMOVE###########

elif mode=='get_link':
		main_scrape.get_link(url,movie_title,thumb,media)

elif mode=='get_tv_link':
		main_scrape.get_tv_link(url,movie_title,thumb,media)

elif mode=='findsource':
		main_scrape.find_source(name,thumb,media,movie_title)
		# getsources = main_scrape.Get_Sources()
		# getsources.find_source(name,thumb,media,movie_title)

elif mode=='find_episode':
		find_episode(name,trakt_id,movie_title)

elif mode=='find_season':
		find_season(name,trakt_id,orig_ids)

elif mode=='get_token':
		trakt_api=trakt.TraktAPI()
		trakt_api.authorize()

elif mode=='pininput':
		message.pininput()

elif mode=='message_stat':
		message.message_stat(url)

elif mode=='window_box':
		window_box.run_box()

elif mode=='playlink':
		main_scrape.playlink()


####Custom Stuff
elif mode=='custom_movie_lists':
		custom_movie_lists(media)

elif mode=='make_new_list':
		make_new_list()

elif mode=='custom_list_view':
		custom_list_view(trakt_id,media)

elif mode=='custom_list_view_tv':
		custom_list_view_tv(trakt_id,media)

elif mode=='get_user_lists':
		get_user_lists(media)

elif mode=='user_list_view':
		user_list_view(url,trakt_id,media)

elif mode=='get_public_lists':
		get_public_lists(url,trakt_id,media)

elif mode=='movistapp_lists':
		movistapp_lists()

elif mode=='pick_custom_list':
		pick_custom_list(media,trakt_id)

elif mode=='add_to_custom':
		add_to_custom(media,trakt_id,url)

elif mode=='del_from_custom':
		del_from_custom(media,trakt_id,name)


#Settings Openings

elif mode=='resolver_settings':
		urlresolver.display_settings()

elif mode=='display_settings':
		kodi.openSettings(addon_id,id1=9,id2=0)

elif mode=='display_download_settings':
		kodi.openSettings(addon_id,id1=9,id2=1)

elif mode=='display_trakt_settings':
		kodi.openSettings(addon_id,id1=9,id2=2)

elif mode=='display_scraper_settings':
		kodi.openSettings(addon_id,id1=9,id2=4)

elif mode=='display_sort_settings':
		kodi.openSettings(addon_id,id1=9,id2=3)


#Download Function

elif mode=='setup_download':
		dl_control.setup_download(name,url,thumb,media,movie_title)

elif mode=='add_to_queue':
		dl_control.add_to_queue(name,url,thumb,ext,media)

elif mode=='viewQueue':
		dl_control.viewQueue()

elif mode=='removeFromQueue':
		dl_control.removeFromQueue(name,url,thumb,ext,media)

elif mode=='download_now':
		dl_control.download_now(name, url, thumb, ext, media)

elif mode=='download_stats':
		dl_control.download_stats(name, url, thumb, ext, media)


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

elif mode=='flush_url_cache':
		cache_stat.flush_url_cache()

#############WINDOW UTILS#########
elif mode=='get_pin':
		trakt_auth.auth_trakt()
		xbmc.executebuiltin("XBMC.Container.Refresh")

#########TEsting Functions
elif mode=='get_kversion':
		get_kversion()

xbmcplugin.endOfDirectory(int(sys.argv[1]))




'''
.decode('utf-8')
'''
