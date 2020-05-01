'''
    Ice Channel
'''
# load lib directory
# begin
import xbmc
import re
xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
if xbmc_version:
    xbmc_version = int(xbmc_version.group(1))
else:
    xbmc_version = 1


if xbmc_version >= 16.9:
        dependencies = ['repository.istream','repository.xunitytalk','script.module.requests','script.module.elementtree','script.common.plugin.cache','script.istream.dialogs', 'script.module.addon.common', 'script.module.beautifulsoup', 'script.module.dnspython', 'script.module.f4mproxy', 'script.module.feedparser', 'script.module.metahandler', 'script.module.myconnpy', 'script.module.parsedom', 'script.module.pyamf', 'script.module.simple.downloader', 'script.module.socksipy', 'script.module.t0mm0.common', 'script.module.unidecode', 'script.module.universal', 'script.module.urlresolver']
        import glob


        folder = xbmc.translatePath('special://home/addons/')

        for DEPEND in glob.glob(folder+'script.icechannel*'):
            try:dependencies.append(DEPEND.rsplit('\\', 1)[1])
            except:dependencies.append(DEPEND.rsplit('/', 1)[1])


        for THEPLUGIN in dependencies:
            xbmc.log(str(THEPLUGIN))
            query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
         
            xbmc.executeJSONRPC(query)

    
if xbmc_version >= 14:
    addon_id = 'script.icechannel'
    lib_addon_dir_name = "lib"
    import xbmcaddon
    import os
    from os.path import join, basename
    import sys
    addon = xbmcaddon.Addon(id=addon_id)
    addon_path = addon.getAddonInfo('path')
    sys.path.append(addon_path)
    lib_addon_dir_path = os.path.join( addon_path, lib_addon_dir_name)
    sys.path.append(lib_addon_dir_path)
    for dirpath, dirnames, files in os.walk(lib_addon_dir_path):
        sys.path.append(dirpath)
# end


import sys
import xbmcgui
import xbmcaddon
import xbmcplugin

from entertainment import common

from entertainment import istream as entertainment

mode = common.addon.queries['mode']
indexer = common.addon.queries.get('indexer', '')
indexer_id = common.addon.queries.get('indexer_id', '')
source = common.addon.queries.get('source', '')
source_id = common.addon.queries.get('source_id', '')
section = common.addon.queries.get('section', '')
url = common.addon.queries.get('url', '')
type = common.addon.queries.get('type', '') # content type: movie, tv-show, tv-episode etc.
urls = common.addon.queries.get('urls', '')
individual_total_pages = common.addon.queries.get('individual_total_pages', '')
playable_url = common.addon.queries.get('playable_url', '')

id = common.addon.queries.get('id', '')

title = common.addon.queries.get('title', 'iStream')
import urllib
title = urllib.unquote_plus(title)

name = common.addon.queries.get('name', '')
year = common.addon.queries.get('year', '')
season = common.addon.queries.get('season', '')
episode = common.addon.queries.get('episode', '')

page = common.addon.queries.get('page', '')
total_pages = common.addon.queries.get('total_pages', '')
sort_by = common.addon.queries.get('sort_by', '')
sort_order = common.addon.queries.get('sort_order', '')

play = common.addon.queries.get('play', '')
queued = common.addon.queries.get('queued', '')

ui_item_mode = common.addon.queries.get('ui_item_mode', '')

search_term = common.addon.queries.get('search_term', '')

settings_section = common.addon.queries.get('settings_section', '')

trailer_url = common.addon.queries.get('trailer', '')

hleveler = '.....'

img = common.addon.queries.get('img', '')
fanart = common.addon.queries.get('fanart', '')
imdb_id = common.addon.queries.get('imdb_id', '')

favorite = common.addon.queries.get('favorite', 'false')
library = common.addon.queries.get('library', 'false')

video_type = common.addon.queries.get('video_type', '')

watch_status = int(common.addon.queries.get('watch_status', '6'))

source_names = common.addon.queries.get('source_names', '')
source_urls = common.addon.queries.get('source_urls', '')
source_tried = common.addon.queries.get('source_tried', '')

contextmenu = common.addon.queries.get('contextmenu', 'false')

service = common.addon.queries.get('service', 'false')

other_names = common.addon.queries.get('other_names', '')

istream_path = common.addon.queries.get('istream_path', '')

autoplay_from_queries = common.addon.queries.get('autoplay', '')

show_hosts_autoplay_dialog = common.addon.queries.get('show_hosts_autoplay_dialog', '')

# GLOBAL VARS
global favs
favs = None

global subs
subs = None

global tmdb_api_key
tmdb_api_key = 'f1f59e2a6c8eacbf5c78ad39d0fe17d1'


# quality color map
quality_to_color = {
    '4K'  : 'purple'   ,
    '3D'  : 'cyan'   ,    
    '720P'  : 'green'   ,
    '1080P' : 'green'   ,
    'HD'    : 'green'   ,
    'MKV'   : 'green'   ,
    'SD'    : 'gold'    ,
    'DVD'   : 'gold'    ,
    'CAM'   : 'red'     ,
    'LOW'   : 'red'     ,
    'TS'    : 'red'     
    }

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if common.addon.get_setting('auto-view') == 'true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % common.addon.get_setting(viewType) )

def setViewForMode(mode):
    global type
    
    content_type = None
    view_setting_id = 'default-view'
    if mode in (common.mode_Section, common.mode_Content):
        
        if section=='main' and not type:
            type = get_video_type('','','',indexer)
        
        if 'movie' in type or 'lists' in type:
            content_type = 'movies'
            view_setting_id = 'movie-view'
        elif 'tv' in type and 'show' in type:
            content_type = 'tvshows'
            view_setting_id = 'tvshow-view'
        elif 'tv' in type and 'season' in type:
            content_type = 'seasons'
            view_setting_id = 'season-view'
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
        elif 'tv' in type and 'episode' in type:
            content_type = 'episodes'
            view_setting_id = 'episode-view'
        elif 'live tv' in type:
            xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
            view_setting_id = 'livetv-view'
    elif mode in (common.mode_Search):
        if indexer == common.indxr_Movies:
            content_type = 'movies'
            view_setting_id = 'movie-view'
        elif indexer == common.indxr_TV_Shows:
            content_type = 'tvshows'
            view_setting_id = 'tvshow-view'
            
    if indexer == 'file_stores':
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED  )
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
    elif indexer == common.indxr_Live_TV and ( 
            (section=='main2' and mode == common.mode_Indexer) or 
            (mode in (common.mode_Live_TV_Region, common.mode_Live_TV_Regions, common.mode_Live_TV_Language,common.mode_Live_TV_Languages, common.mode_Live_TV_Genre, common.mode_Live_TV_Genres ))
            ):
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
        if (section=='main2' and mode == common.mode_Indexer) or (mode in (common.mode_Live_TV_Region, common.mode_Live_TV_Regions, common.mode_Live_TV_Language,common.mode_Live_TV_Genre)):
            view_setting_id = 'livetv-view'
        else:
            view_setting_id = 'default-view'
            
    setView(content_type, view_setting_id)


def add_contextmenu(video_type, indexer, indexer_id, mode, section, url, imdb_id, title, name, year, season, episode, type, use_meta, meta_img, meta_fanart, meta_watched, favorite, trailer='', urls=''):
    contextMenuItems = [
            ('[COLOR royalblue]Search[/COLOR]', 'Container.Update(%s, True)' % common.addon.build_plugin_url({'title':'Search', 'mode':common.mode_Search, 'indexer':indexer, 'section':'search'})),
            ('[COLOR gold]Settings[/COLOR]', 'Container.Update(%s)' % common.addon.build_plugin_url({'title':'Settings', 'mode':common.mode_Settings, 'indexer':'settings', 'section':'settings'}))
        ]
    
    title = common.CleanText2(title, True, True)
    name = common.CleanText2(name, True, True)
    
    if mode == common.mode_Section: return contextMenuItems
    
    if mode == common.mode_Live_TV and favorite == 'false':
        contextMenuItems.insert( len(contextMenuItems) - 2 , ('Hide', 'RunPlugin(%s)' % common.addon.build_plugin_url({'mode':common.mode_Hide_Channel, 'indexer':indexer, 'indexer_id':indexer_id})))
    
    if indexer not in (common.indxr_Sports, common.indxr_Live_TV):
        if video_type in (common.VideoType_Movies, common.VideoType_Episode, common.VideoType_TV):
            contextMenuItems.insert( len(contextMenuItems) - 2 , ('Show Information', 'XBMC.Action(Info)'))
            
        if video_type in (common.VideoType_Movies) and trailer and 'plugin://plugin.video.youtube/' in trailer:
            contextMenuItems.insert( len(contextMenuItems) - 2 , ('Play Trailer', 'RunPlugin(%s)' % common.addon.build_plugin_url({'mode':common.mode_Play_Trailer, 'url':trailer}) ))
        
    if indexer in (common.indxr_Sports, common.indxr_Live_TV) or video_type in (common.VideoType_Movies, common.VideoType_Episode, common.VideoType_Season, common.VideoType_TV):
    
        global favs
        if not favs:
            from universal import favorites
            favs = favorites.Favorites(common.addon_id, sys.argv)    
        
        if indexer in (common.indxr_Sports, common.indxr_Live_TV):
            fav_title = name
        else:
            fav_title = name + ( ' (' + year + ')' if year != '' else '' )
        
        if video_type == common.VideoType_Season:
            fav_title = fav_title + ' - Season: ' + season
        elif video_type == common.VideoType_Episode:
            fav_title = fav_title + ' - S' + season + 'E' + episode + ' - ' + title
            
        fav_section_title = ''
        fav_subsection_title = ''
        if indexer == common.indxr_Live_TV:
            fav_section_title = 'Live TV'
        if indexer == common.indxr_Sports:
            fav_section_title = 'Live Sports'
        if video_type == common.VideoType_Movies:
            fav_section_title = 'Movies'
        elif video_type == common.VideoType_TV:
            fav_section_title = 'TV'
            fav_subsection_title = 'Shows'
        elif video_type == common.VideoType_Season:
            fav_section_title = 'TV'
            fav_subsection_title = 'Seasons'
        elif video_type == common.VideoType_Episode:
            fav_section_title = 'TV'
            fav_subsection_title = 'Episodes'

        if favorite == 'false':
            already_in_favorites = False
            try:
                already_in_favorites = favs.is_already_in_favorites(fav_section_title, '', fav_subsection_title, '', fav_title)
            except:
                fav_title = {'title':fav_title}
                fav_title_str = common.dict_to_paramstr(fav_title)
                fav_title=common.parse_query(fav_title_str)
                fav_title=fav_title['title']
                already_in_favorites = favs.is_already_in_favorites(fav_section_title, '', fav_subsection_title, '', fav_title)
            if already_in_favorites == True:
                contextMenuItems.insert( len(contextMenuItems) - 2 , ('[COLOR red]Delete[/COLOR] from Favorites', favs.delete_item(fav_title, section_title=fav_section_title, 
                    sub_section_title=fav_subsection_title)))
            else:
                fav_queries = {'indexer':indexer, 'mode':common.mode_Add_To_Favorites, 'item_mode':mode, 'section':section, 
                    'title':title, 'name':name, 'year':year, 'season':season, 'episode':episode, 'fav_supports_meta':'true', 'fav_video_type':video_type,
                    'type':type, 'img':meta_img.replace('\\', '\\\\'), 'fanart':meta_fanart.replace('\\', '\\\\'), 'imdb_id':imdb_id, 'fav_title':fav_title, 'fav_section_title':fav_section_title,
                    'fav_subsection_title':fav_subsection_title, 'urls':urls.replace('\\', '\\\\') }
        
                if video_type not in (common.VideoType_Movies, common.VideoType_Episode):
                    fav_queries.update({'url':url, 'indexer_id':indexer_id})
                
                #fav_url = favs.build_url(fav_queries)
                #fav_queries.update({'supports_meta':'true', 'video_type':video_type})
                
                contextMenuItems.insert( len(contextMenuItems) - 2 , ('[COLOR green]Add[/COLOR] to Favorites', 'RunPlugin(%s)' % common.addon.build_plugin_url(fav_queries)))
        else:
            contextMenuItems.insert( len(contextMenuItems) - 2 , ('[COLOR red]Delete[/COLOR] from Favorites', favs.delete_item(fav_title, section_title=fav_section_title, 
                sub_section_title=fav_subsection_title)))
        
        if indexer not in (common.indxr_Sports, common.indxr_Live_TV):
            lib_queries = {'indexer':indexer, 'mode':common.mode_Add_To_Library, 'item_mode':mode, 'section':section, 
                'title':title, 'item_title':fav_title, 'name':name, 'year':year, 'season':season, 'episode':episode, 'video_type':video_type,
                'type':type, 'img':meta_img, 'fanart':meta_fanart, 'imdb_id':imdb_id, 'urls':urls}
            if video_type not in (common.VideoType_Movies, common.VideoType_Episode):
                lib_queries.update({'url':url, 'indexer_id':indexer_id})
            contextMenuItems.insert( len(contextMenuItems) - 2 , ('Add to [COLOR white][B]XBMC[/B][/COLOR] Library', 'RunPlugin(%s)' % common.addon.build_plugin_url(lib_queries)))
            
            if video_type == common.VideoType_TV:
                global subs
                if not subs:
                    from entertainment import subscriptions
                    subs = subscriptions.Subscriptions()
                    
                subs_queries = {'indexer':indexer, 'indexer_id':indexer_id, 'title':title, 'item_title':fav_title, 'name':name, 'year':year, 'video_type':video_type,
                    'type':type, 'imdb_id':imdb_id, 'url':url, 'urls':urls}
                menu_text = ''
                if subs.is_subscribed(indexer, indexer_id, type, video_type, name, year, url, title, imdb_id) == True:
                    subs_queries.update({'mode':common.mode_Unsubscribe})
                    menu_text = '[COLOR red]Unsubscribe[/COLOR]'
                else:
                    subs_queries.update({'mode':common.mode_Subscribe })
                    menu_text = '[COLOR green]Subscribe[/COLOR]'
                contextMenuItems.insert( len(contextMenuItems) - 2 , (menu_text, 'RunPlugin(%s)' % common.addon.build_plugin_url(subs_queries)))

            if use_meta == True:
                overlay_queries = {'mode':common.mode_Change_Watched, 'type':video_type, 'imdb_id':imdb_id, 'title':title, 'name':name, 'year':year, 'season':season, 'episode':episode, 'watch_status':str(meta_watched)}
                overlay_label = ''
                if meta_watched == 6:
                    overlay_label = 'Mark as Watched'
                elif meta_watched == 7:
                    overlay_label = 'Mark as Unwatched'
                contextMenuItems.insert( len(contextMenuItems) - 2 , (overlay_label, 'RunPlugin(%s)' % common.addon.build_plugin_url(overlay_queries)))
                
                refresh_metadata_queries = {'mode':common.mode_Refresh_Meta, 'type':video_type, 'imdb_id':imdb_id, 'title':title, 'name':name, 'year':year, 'season':season, 'episode':episode}
                contextMenuItems.insert( len(contextMenuItems) - 2 , ('Refresh Metadata', 'RunPlugin(%s)' % common.addon.build_plugin_url(refresh_metadata_queries)))

    return contextMenuItems

def get_metadata(metaget, video_type, vidtitle, vidname='', year='', imdb=None, season_list=None, season_num=0, episode_num=0, img=''):    
    
    try:
        year = int(year)
    except:
        year = 0
    year = str(year)
    
    meta = {'title': title, 'year': year, 'imdb_id': '', 'overlay': ''}
    
    returnlist = True
    
    try:
        if video_type in (common.VideoType_TV, common.VideoType_Season, common.VideoType_Episode ) :
            tv_title = common.CleanTextForSearch(vidname, strip=True) 
            meta = metaget.get_meta(common.VideoType_TV, tv_title, year=year, imdb_id=imdb)
            if not (meta['imdb_id'] or meta['tvdb_id']):
                meta = metaget.get_meta(video_type, tv_title, imdb_id=imdb, year=year)
            imdb = meta.get('imdb_id', '')
        elif video_type == common.VideoType_Movies:
            meta = metaget.get_meta(video_type, common.CleanTextForSearch(vidtitle, strip=True), imdb_id=imdb, year=year)
                    
        if video_type == common.VideoType_Season:            
            if not season_list:
                season_list = []
                season_list.append(str(season_num))
                returnlist = False
            meta = metaget.get_seasons(common.CleanTextForSearch(vidname, strip=True), imdb, season_list)
            if not returnlist:
                meta = meta[0]

        if video_type == common.VideoType_Episode:
            meta=metaget.get_episode_meta(common.CleanTextForSearch(vidname, strip=True), imdb, season_num, episode_num)
    
    except Exception, e:
        common.addon.log(' Metadata exception occured: %s' % e)
        
            
    if not returnlist:
        if meta.get('title', '') == '':
            meta['title'] = vidname
        if meta.get('cover_url', '') == '':
            meta['cover_url'] = img
        if meta.get('imdb_id', '') == '':
            meta['imdb_id'] = imdb
        if meta.get('backdrop_url', '') == '':
            meta['backdrop_url'] = ''
        if meta.get('year', '') == '':
            meta['year'] = year
        if meta.get('overlay', '') == '':
            meta['overlay'] = 0

    return meta

def get_info_from_xbmc_library(video_type, name, season, episode, year, properties=[], toplevel=False):
    import json
    xbmcdbid = ''
    return_dict = {}
    info_item = None
    try:
        if video_type == common.VideoType_Movies:
            json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{ "and" : [{"field" : "title", "operator" : "is", "value" : "%s"}, {"field" : "year", "operator" : "is", "value" : "%s" }] }, "properties" : %s }, "id": 1 }'
            json_rpc_request = json_rpc_request % ( name, year, str(properties).replace("'", '"') )
            info = json.loads(xbmc.executeJSONRPC(json_rpc_request))
            if info['id'] == 1:
                info_result = info['result']
                info_total = info_result['limits']['total']
                if info_total > 0:                                
                    info_item = info_result['movies'][0]
                else:
                    json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"field" : "title", "operator" : "is", "value" : "%s"}, "properties" : %s }, "id": 1 }'
                    json_rpc_request = json_rpc_request % (name, str(properties).replace("'", '"') )
                    if info['id'] == 1:
                        info_result = info['result']
                        info_total = info_result['limits']['total']

                        if info_total > 0:
                            info_item = info_result['movies'][0]
            
            if info_item:
                xbmcdbid = str(info_item['movieid'])
            
        elif video_type == common.VideoType_Episode and toplevel == True:
            json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{ "and" : [{"field" : "title", "operator" : "is", "value" : "%s"}, {"field" : "year", "operator" : "is", "value" : "%s" }] }, "properties" : %s }, "id": 1 }'            
            json_rpc_request = json_rpc_request % ( name, year, str(properties).replace("'", '"') )
            info = json.loads(xbmc.executeJSONRPC(json_rpc_request))
            if info['id'] == 1:
                info_result = info['result']
                info_total = info_result['limits']['total']
                if info_total > 0:                                
                    info_item = info_result['tvshows'][0]
                else:
                    json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{ "and" : [{"field" : "title", "operator" : "is", "value" : "%s"}] }, "properties" : %s }, "id": 1 }'
                    json_rpc_request = json_rpc_request % (name, str(properties).replace("'", '"'))
                    if info['id'] == 1:
                        info_result = info['result']
                        info_total = info_result['limits']['total']

                        if info_total > 0:
                            info_item = info_result['tvshows'][0]
                            
            if info_item:
                xbmcdbid = str(info_item['tvshowid'])
                            
        elif video_type == common.VideoType_Episode and toplevel == False:
            json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{ "and" : [{"field" : "tvshow", "operator" : "is", "value" : "%s"}, {"field" : "season", "operator" : "is", "value" : "%s" }, {"field" : "episode", "operator" : "is", "value" : "%s" }] }, "properties" : %s }, "id": 1 }'
            json_rpc_request = json_rpc_request % ( name, season, episode, str(properties).replace("'", '"') )
            info = json.loads(xbmc.executeJSONRPC(json_rpc_request))
            if info['id'] == 1:
                info_result = info['result']
                info_total = info_result['limits']['total']
                if info_total > 0:                                
                    info_item = info_result['episodes'][0]
                else:
                    json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{ "and" : [{"field" : "tvshow", "operator" : "is", "value" : "%s"}, {"field" : "season", "operator" : "is", "value" : "%s" }, {"field" : "episode", "operator" : "is", "value" : "%s" }, {"field" : "year", "operator" : "is", "value" : "%s" }] }, "properties" : %s }, "id": 1 }'
                    json_rpc_request = json_rpc_request % (name, str(properties).replace("'", '"'))
                    if info['id'] == 1:
                        info_result = info['result']
                        info_total = info_result['limits']['total']

                        if info_total > 0:
                            info_item = info_result['episodes'][0]
            
            if info_item:
                xbmcdbid = str(info_item['episodeid'])
    except:
        xbmcdbid = ''
        info_item = None
        pass
    
    return_dict['xbmcdbid'] = xbmcdbid

    for prprty in properties:
        if not info_item:
            prprt_val = ''
        else:
            prprt_val = info_item[prprty]
            if isinstance(prprt_val, (str, unicode) ):
                prprt_val = urllib.unquote_plus(prprt_val.replace('image://', ''))
                if prprt_val.endswith('/'): prprt_val = prprt_val [:-1]
        return_dict[prprty] = prprt_val

    return return_dict
    
def mark_as_watched_in_xbmc_library(video_type, xbmcdbid):
    json_rpc_request = ''
    if video_type == common.VideoType_Movies:
        json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : 1 }, "id": 1 }'
    elif video_type == common.VideoType_Episode:
        json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : 1 }, "id": 1 }'
        
    if json_rpc_request:
        json_rpc_request = json_rpc_request % xbmcdbid
        xbmc.executeJSONRPC(json_rpc_request)

def change_watched_in_xbmc_library(video_type, name, season, episode, year, watched=None):
    xbmcdbid = xbmc.getInfoLabel('ListItem.DBID')
    playcount = xbmc.getInfoLabel('ListItem.PlayCount')
    if not xbmcdbid or int(xbmcdbid) <= 0:
        xbmclibinfo = get_info_from_xbmc_library(video_type, name, season, episode, year, properties=["playcount"])
        xbmcdbid = xbmclibinfo['xbmcdbid']
        playcount = xbmclibinfo.get('playcount', '0')
    
    if xbmcdbid:        
        
        json_rpc_request = ''
        if video_type == common.VideoType_Movies:
            json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid" : %s, "playcount" : %d }, "id": 1 }'
        elif video_type == common.VideoType_Episode:
            json_rpc_request = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %s, "playcount" : %d }, "id": 1 }'
            
        if json_rpc_request:
            try:
                playcount = int(playcount)
            except:
                playcount = 0

            if watched == True: playcount += 1
            elif watched == False: playcount = 0
            else:
                if playcount > 0: playcount = 0
                else: playcount = 1
            json_rpc_request = json_rpc_request % ( xbmcdbid, playcount )

            xbmc.executeJSONRPC(json_rpc_request)
        
def WatchedCallbackwithParams(video_type, name, imdb_id, season, episode, year):
    
    entertainment.loadiStreamPlugins(load_settings=True)
    
    use_meta = False
    if video_type == common.VideoType_Movies:
        use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
    elif video_type == common.VideoType_Episode:
        use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
    
    if use_meta == False:
        return
        
    from metahandler import metahandlers
    metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
    
    if not imdb_id or imdb_id == '':
        watched_meta = get_metadata(metaget, video_type, name, vidname=name, year=year, season_num=season, episode_num=episode)
        imdb_id = watched_meta.get('imdb_id', '')
    
    metaget.change_watched(video_type, name, imdb_id, season=season, episode=episode, year=year, watched=7)
    
    if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'sync_watched_status_with_lib') == 'true':
        change_watched_in_xbmc_library(video_type, name, season, episode, year, watched=True)
    
    #xbmc.executebuiltin("Container.Refresh")    
        

def add_dir_title(forced_title = ''):
    return ''
    common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':  '[COLOR royalblue][B]* * * * * ' + ( forced_title if forced_title != '' else title ) + ' * * * * *[/B][/COLOR]'})

def get_video_type(indexer, section, item_type, type):
    item_video_type = item_type
    if indexer == common.indxr_Lists or 'list' in section :
        if item_type == 'tv_seasons':
            item_video_type = 'tv_shows'
        elif item_type == 'tv_episodes':
            item_video_type = 'tv_seasons'
    else:
        item_video_type = type

    video_type=''
    if 'movie' in item_video_type:
        video_type = common.VideoType_Movies
    elif 'tv' in item_video_type and 'show' in item_video_type:
        video_type = common.VideoType_TV
    elif 'tv' in item_video_type and 'season' in item_video_type:
        video_type = common.VideoType_Season
    elif 'tv' in item_video_type and 'episode' in item_video_type:
        video_type = common.VideoType_Episode
        
    return video_type

def RetrieveAndDisplayMessagesiStreamProgressDialog(message_queue, dialog=''):
    msg = message_queue.get()
    
    while( str(msg) != 'done'):
        
        if dialog != '':
            index = msg.get('index', -1)
            message = msg['message']
            wait_time = msg.get('wait_time', 100)
            dialog.addUpdateItem(message, index)
            xbmc.sleep(wait_time)
        
        msg = message_queue.get()
    
def RetrieveAndDisplayMessages(message_queue, dialog=''):    
    if dialog != '':
        dialog.update(25)
        import xbmc
        percent = 25
        percent_step = 5 
        
    msg = message_queue.get()
    
    while( str(msg) != 'done'):
        
        if dialog != '':
            line1 = msg['line1']
            line2 = msg['line2']
            line3 = msg['line3']
            percent_step = msg.get('percent_step', percent_step)
            wait_time = msg.get('wait_time', 100)
            percent = percent + percent_step
            dialog.update(percent, line1, line2, line3)
            xbmc.sleep(wait_time)
        
        msg = message_queue.get()
        
    if dialog != '':
        dialog.update(75)
   
def GetIStream(show_mystream=True):

    add_dir_title()

    items = entertainment.GetMainSection()
    
    for item in items:
        if item['mode'] == common.mode_Dummy:
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':item.get('title', '')  })
        elif item['mode'] == common.mode_MyStream:
            if show_mystream==True:
                item_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':item['indexer'], 'mode':item['mode'], 'section':item['section'], 'title': item['title'], 'img':item.get('img', ''), 'fanart':item.get('fanart', '')}
                common.addon.add_directory(item_query_dict, {'title': '[B][COLOR royalblue]my[/COLOR]Stream[/B]'}, img=item.get('img', ''), fanart=item.get('fanart', ''))
        else:            
            item_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':item['indexer'], 'mode':item['mode'], 'section':item['section'], 'title': item['title'], 'img':item.get('img', ''), 'fanart':item.get('fanart', '')}
            
            contextMenuItems = []
            
            contextMenuItems.insert( 0 , ('[B]Reload Plugins[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url( {'mode':common.mode_Reload_Plugins} )))
            
            istream_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':item['indexer'], 'mode':common.mode_Add_to_MyStream, 'item_mode':item['mode'], 'section':item['section'], 'title': item['title'], 'img':item.get('img', ''), 'fanart':item.get('fanart', '')}
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))
            
            common.addon.add_directory(item_query_dict, {'title': item['title']}, img=item.get('img', ''), fanart=item.get('fanart', ''), contextmenu_items=contextMenuItems )
            
    setViewForMode(mode)    
    common.addon.end_of_directory()        

def GetMyStream(show_istream=True):
    
    if show_istream==True:
        item_query_dict = {'istream_path':'', 'indexer':'istream', 'mode':common.mode_iStream, 'section':'istream', 'title': 'iStream', 'img':common.get_themed_icon('mystream.png'), 'fanart':common.get_themed_fanart('mystream.jpg')}
        common.addon.add_directory(item_query_dict, {'title': '[B][COLOR royalblue]i[/COLOR]Stream[/B]'}, img=common.get_themed_icon('mystream.png'), fanart=common.get_themed_fanart('mystream.jpg'))
    
    from entertainment.mystream import MyStream
    mystream = MyStream()
    
    items = mystream.get_mystream_items()
    
    item_count = len(items)
    for item in items:
        listitem = xbmcgui.ListItem(item['display_title'], iconImage=item['img'], thumbnailImage=item['img'])
        listitem.setProperty('fanart_image', item['fanart'])
        contextMenuItems = []
        contextMenuItems.insert( 0 , ('[COLOR red]Remove[/COLOR]', 'RunPlugin(%s)' % common.addon.build_plugin_url({'mode':common.mode_Remove_from_MyStream, 'title':item['title'], 'display_title':item['display_title']})))            
        contextMenuItems.insert( 1 , ('[COLOR yellow]Rename[/COLOR]', 'RunPlugin(%s)' % common.addon.build_plugin_url({'mode':common.mode_Rename_MyStream_Item, 'title':item['title'], 'display_title':item['display_title']})))            
        contextMenuItems.insert( 2 , ('[B]Reload Plugins[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url( {'mode':common.mode_Reload_Plugins} )))
        listitem.addContextMenuItems(contextMenuItems, replaceItems=False)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), item['path'], listitem, isFolder=True, totalItems=item_count)
    xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=False)

def PreLoadiStreamPlugins(force=True):
    global preloaded
    if preloaded == True:
        return
    
    preload = False
    if force:
        preload = True
    else:
        last_preload = "" #common.addon.get_setting('plugin_load_timestamp')
        if last_preload == "" or not last_preload:
            preload = True
        else:
            import datetime
            try:
                last_preload_dt = datetime.datetime.strptime(last_preload, "%Y-%m-%d %H:%M:%S")
            except:
                try:
                    import time
                    last_preload_dt = datetime.datetime(*(time.strptime(last_preload, "%Y-%m-%d %H:%M:%S")[0:6]))
                except:
                    last_preload_dt = None
            if not last_preload_dt:
                preload=True
            else:
                curr_dt = datetime.datetime.today()
                time_diff = curr_dt - last_preload_dt
                interval = datetime.timedelta ( hours = 24)
                if time_diff > interval:
                    preload = True
    if preload == True:    
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create("iStream", "Loading plugins... ", " ", " " )
        pDialog.update(0)
        
        import xbmc
        
        # get window progress
        WINDOW_PROGRESS = xbmcgui.Window( 10101 )
        # give window time to initialize
        xbmc.sleep( 100 )
        try:
            # get our cancel button    
            CANCEL_BUTTON = WINDOW_PROGRESS.getControl( 10 )
            # desable button (bool - True=enabled / False=disabled.)
            CANCEL_BUTTON.setEnabled( False )
        except:
            pass
        
        message_queue = entertainment.PreLoadiStreamPluginsThreaded()
        RetrieveAndDisplayMessages(message_queue, pDialog)
        pDialog.update( 100, 'Plugins loaded. ', 
                ' ', 
                ' ' )
        
        import datetime
        common.addon.set_setting( "plugin_load_timestamp", datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') )
        
        xbmc.sleep(500)
        try:
            # enable button
            CANCEL_BUTTON.setEnabled( True )
        except:
            pass
        pDialog.close() 
        xbmc.sleep(100)
        preloaded = True
    
    
def GetMainSection():
    
    PreLoadiStreamPlugins(False)
    
    entertainment.loadiStreamPlugins(load_settings=True)
    if common.addon.get_setting('mystream_default') == 'false':
        GetIStream()
    else:
        GetMyStream()
    
     
    
def GetIndexers(indexer):

    entertainment.loadiStreamPlugins(type=indexer, load_indexer=True, load_settings=True, load_webproxyproviders=True)
    
    global section
    if indexer == common.indxr_Live_TV and section == 'main':
                
        live_tv_regions = True if entertainment.GetiStreamSettings(common.settings_Live_TV,'live_tv_regions') == "true" else False
        live_tv_languages = True if entertainment.GetiStreamSettings(common.settings_Live_TV,'live_tv_languages') == "true" else False
        live_tv_genres = True if entertainment.GetiStreamSettings(common.settings_Live_TV,'live_tv_genres') == "true" else False
        
        if live_tv_regions or live_tv_languages or live_tv_genres:
            item_query_dict = { 'istream_path':istream_path + ' : ' + 'Channels', 'indexer':indexer, 'indexer_id':indexer_id, 'mode':mode, 'section':'main2' }
            istream_query_dict = { 'istream_path':istream_path + ' : ' + 'Channels', 'indexer':indexer, 'indexer_id':indexer_id, 'mode':common.mode_Add_to_MyStream, 'item_mode':mode, 'section':'main2' }
            contextMenuItems = []
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
            common.addon.add_directory( item_query_dict, { 'title': 'Channels' }, contextmenu_items=contextMenuItems )
            
            if live_tv_regions:
                item_query_dict = { 'istream_path':istream_path + ' : ' + 'Countries','indexer':indexer, 'indexer_id':indexer_id, 'mode':common.mode_Live_TV_Regions }
                istream_query_dict = { 'istream_path':istream_path + ' : ' + 'Countries','indexer':indexer, 'indexer_id':indexer_id, 'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Live_TV_Regions }
                contextMenuItems = []
                contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
                common.addon.add_directory(item_query_dict , { 'title': 'Countries' }, contextmenu_items=contextMenuItems )
                
            if live_tv_languages:
                item_query_dict = { 'istream_path':istream_path + ' : ' + 'Languages', 'indexer':indexer, 'indexer_id':indexer_id, 'mode':common.mode_Live_TV_Languages }
                istream_query_dict = { 'istream_path':istream_path + ' : ' + 'Languages', 'indexer':indexer, 'indexer_id':indexer_id, 'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Live_TV_Languages }
                contextMenuItems = []
                contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
                common.addon.add_directory(item_query_dict , { 'title': 'Languages' }, contextmenu_items=contextMenuItems )
                
            if live_tv_genres:
                item_query_dict = { 'istream_path':istream_path + ' : ' + 'Genres', 'indexer':indexer, 'indexer_id':indexer_id, 'mode':common.mode_Live_TV_Genres }
                istream_query_dict = { 'istream_path':istream_path + ' : ' + 'Genres', 'indexer':indexer, 'indexer_id':indexer_id, 'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Live_TV_Genres }
                contextMenuItems = []
                contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
                common.addon.add_directory(item_query_dict , { 'title': 'Genres' }, contextmenu_items=contextMenuItems )
                
            setViewForMode(mode)
            common.addon.end_of_directory()
            
            return
        else:            
            section = 'main2'

    items = entertainment.GetIndexers(indexer)

    if indexer not in (common.indxr_Sports, common.indxr_Live_TV) and len(items) == 1:
        item = items[0]
        GetSection(item['indexer'], item['indexer_id'], 'main', '', '')
        return
        
    add_dir_title()
    
    items.sort(key=lambda k: k['title'])
    for item in items:
        if item['mode'] == common.mode_Dummy:
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':item.get('title', '')  })
        else:
            contextMenuItems = add_contextmenu(None, item['indexer'], item['indexer_id'], item['mode'], item['section'], '', '', item['title'], item['title'], '', 
                '', '', '', '', item.get('img', ''), item.get('fanart', ''), '', 'false', '')
            display_title = item['title']
            if '[COLOR red]Delete[/COLOR] from Favorites' in str(contextMenuItems):
                display_title  = '[B][COLOR green]|*|[/COLOR][/B] ' + item['title']
            item_query_dict = {'istream_path':istream_path + ' : ' + display_title,'indexer':item['indexer'], 'indexer_id':item['indexer_id'], 'mode':item['mode'], 
                'section':item['section'], 'title': item['title'], 'img':item.get('img', ''), 'fanart':item.get('fanart', ''),
                'other_names':item.get('other_names', ''), 'region':item.get('region', ''), 'language':item.get('language', ''),
                'genre':item.get('genre', '')}
            istream_query_dict = {'istream_path':istream_path + ' : ' + display_title,'indexer':item['indexer'], 'indexer_id':item['indexer_id'], 'mode':common.mode_Add_to_MyStream, 'item_mode':item['mode'], 
                'section':item['section'], 'title': item['title'], 'img':item.get('img', ''), 'fanart':item.get('fanart', ''),
                'other_names':item.get('other_names', ''), 'region':item.get('region', ''), 'language':item.get('language', ''),
                'genre':item.get('genre', '')}
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
            common.addon.add_directory(item_query_dict, {'title': display_title}, img=item.get('img', ''), fanart=item.get('fanart', ''),
                contextmenu_items=contextMenuItems, context_replace=True)
            
    if indexer == common.indxr_TV_Shows:
        subs_img = common.get_themed_icon('subscriptions.png')
        subs_fanart = common.get_themed_fanart('subscriptions.jpg')
        item_query_dict = {'istream_path':istream_path + ' : ' + 'Subscriptions','mode':common.mode_Manage_Subs, 'indexer':indexer, 'type':'tv_seasons', 'video_type':common.VideoType_TV,
            'title':'Subscriptions', 'img':subs_img, 'fanart':subs_fanart}
        istream_query_dict = {'istream_path':istream_path + ' : ' + 'Subscriptions','mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Manage_Subs, 'indexer':indexer, 'type':'tv_seasons', 'video_type':common.VideoType_TV,
            'title':'Subscriptions', 'img':subs_img, 'fanart':subs_fanart}
        contextMenuItems = []
        contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
        common.addon.add_directory(item_query_dict, {'title': 'Subscriptions'}, img=subs_img, fanart=subs_fanart, contextmenu_items=contextMenuItems )
    elif indexer == common.indxr_Lists:
        pl_img = common.get_themed_icon('playlists.png')
        pl_fanart = common.get_themed_fanart('playlists.jpg')
        item_query_dict = {'istream_path':istream_path + ' : ' + 'Playlists','title':'Playlists', 'mode':common.mode_File_Stores, 'indexer':'file_stores', 'section':'file_stores',
            'img':pl_img, 'fanart':pl_fanart}
        istream_query_dict = {'istream_path':istream_path + ' : ' + 'Playlists','title':'Playlists', 'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_File_Stores, 'indexer':'file_stores', 'section':'file_stores',
            'img':pl_img, 'fanart':pl_fanart}
        contextMenuItems = []
        contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
        common.addon.add_directory(item_query_dict, {'title': 'Playlists'}, img=pl_img, fanart=pl_fanart, contextmenu_items=contextMenuItems )
            
        
    search_item = entertainment.GetSearchItem(indexer)
    if search_item and len(search_item) > 0:
        search_item = search_item[0]
        item_query_dict = {'istream_path':istream_path + ' : ' + search_item['title'], 'indexer':search_item['indexer'], 'indexer_id':search_item['indexer_id'], 'mode':search_item['mode'], 
            'section':search_item['section'], 'title': search_item['title'], 'img':search_item.get('img', ''), 'fanart':search_item.get('fanart', '')}
        istream_query_dict = {'istream_path':istream_path + ' : ' + search_item['title'], 'indexer':search_item['indexer'], 'indexer_id':search_item['indexer_id'], 'mode':common.mode_Add_to_MyStream, 'item_mode':search_item['mode'], 
            'section':search_item['section'], 'title': search_item['title'], 'img':search_item.get('img', ''), 'fanart':search_item.get('fanart', '')}
        contextMenuItems = []
        contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
        common.addon.add_directory(item_query_dict,{'title': search_item['title']}, img=search_item.get('img', ''), fanart=search_item.get('fanart', ''), contextmenu_items=contextMenuItems )
        
    setViewForMode(mode)
    common.addon.end_of_directory()            

def GetMetas(metas, metadata_queue, indexer, indexer_id, section, url, type, content_items):
    
    use_meta = True    
    metaget = ''
    
    if 'movie' in type:
        use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
    elif 'tv' in type:
        use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
    
    if use_meta == True and not metaget:
        from metahandler import metahandlers
        metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
    
    import xbmcgui
    mainWindow = xbmcgui.Window(10000)
    
    content_items_count = len(content_items)
    content_items_loop = 0
    first_content_item = True
    
    for item in content_items:
        video_type = ''
        item_fav = item.get('favorite', 'false')
        item_bmk = item.get('bookmark', 'false')
        item_type=item.get('type', '') 
            
        video_type = get_video_type(indexer, section, item_type, type) if item_fav=='false' and item_bmk == 'false' else item.get('video_type', '')
        
        if section=='main' and not type and item.get('mode', '') == common.mode_Content:
        
            video_type=get_video_type('','','',indexer)
            
            if 'movie' in item_type:
                use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
            elif 'tv' in item_type:
                use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
                
            if use_meta == True and not metaget:
                from metahandler import metahandlers
                metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
        
        if indexer == common.indxr_Lists or 'list' in section or item_fav == 'true':
            if video_type == common.VideoType_Movies:
                use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies,'metadata_movies') == 'true' else False
            elif video_type in (common.VideoType_Season, common.VideoType_Episode, common.VideoType_TV):
                use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows,'metadata_tv_shows') == 'true' else False

            if use_meta == True and not metaget:
                from metahandler import metahandlers
                metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)

        if use_meta == True:

            sn = item.get('season', '0')
            sn = '0' if sn == '' else sn
            
            en = item.get('episode', '0')
            en = '0' if en == '' else en
            
            if first_content_item == True:
                first_content_item = False
                metadata_queue.put({'message':'...'})
                metadata_queue.put({'message':str(content_items_loop) + ' of ' + str(content_items_count) + ' content(s) metadata fetched'})
            
            if mainWindow.getProperty('ISTREAM-PROGRES-DIALOG-CANCELLED') ==  'FALSE':
                metadata_queue.put({'message':item.get('name', ''), 'index':1})
                metas[content_items_loop] = get_metadata(metaget, video_type, 
                    item.get('name', '') if video_type in (common.VideoType_Movies, common.VideoType_TV) else item.get('title', ''), 
                    item.get('name', ''), item.get('year', ''), imdb = item.get('imdb_id', None) if (imdb_id == None or imdb_id == '') else imdb_id, 
                    season_num=int(sn), episode_num=int(en))
                content_items_loop = content_items_loop + 1
                metadata_queue.put({'message':str(content_items_loop) + ' of ' + str(content_items_count) + ' content(s) metadata fetched', 'index':2})
                
            if content_items_loop == content_items_count or mainWindow.getProperty('ISTREAM-PROGRES-DIALOG-CANCELLED') == 'TRUE':
                metadata_queue.put('done')

    
def GetSection(indexer, indexer_id, section, url, type, page='', total_pages='', sort_by='', sort_order=''): 

    add_dir_title()
    
    import urllib
    from entertainment import htmlcleaner
    
    #if section in ('main', 'main2'):
    #    entertainment.loadiStreamPlugins(type=indexer, load_indexer=True, load_settings=True )
    #else:
    #entertainment.loadiStreamPlugins(type=indexer, load_indexer=True, load_settings=True, load_webproxyproviders=True )

    (items,meta) = entertainment.GetSection (indexer, indexer_id, section, url, type, page, total_pages, sort_by, sort_order)
    
    next_page_dict = None
    last_page_dict = None
    
    use_meta = True
    if len(meta) <= 0:
        use_meta = False    
    
    metaget = ''
    if 'movie' in type:
        use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
    elif 'tv' in type:
        use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
        
    if use_meta == True:
        from metahandler import metahandlers
        metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
    
    content_items = [ci for ci in items if ci['mode'] not in (common.mode_Dummy, common.mode_Info, common.mode_Section) ]
    content_items_count = len(content_items)
    
    if content_items_count > 0:
        this_metas = [ {} ] * content_items_count
        try:
            import Queue as queue
        except:
            import queue
        message_queue = queue.Queue()
        from istreams.dialogs import DialogiStreamProgress
        DialogiStreamProgress.show("iStream Metadata", "[COLOR yellow][B]Fetching content metadata...[/B][/COLOR]")
        import threading
        threading.Thread(target=GetMetas, args=(this_metas, message_queue, indexer, indexer_id, section, url, type, content_items)).start()
        RetrieveAndDisplayMessagesiStreamProgressDialog(message_queue, DialogiStreamProgress)
        DialogiStreamProgress.addUpdateItem('Displaying retrieved links...')
        xbmc.sleep(1000)
  
    else:
        use_meta = False
        
    totalitems = len(items)
    content_items_loop = 0
    item_list_index = 0
    for item in items:
        item['title'] = item.get('title', '')
        item['name'] = item.get('name', '')
        
        if item['mode'] == common.mode_Dummy:
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':item.get('title', '')  })
        elif item['mode'] == common.mode_Info:
            curr_page = item.get('page', '')
            curr_page_count = item.get('total_pages', '')
            curr_sort_by = item.get('sort_by', '')
            currt_sort_order = item.get('sort_order', '')
            
            if curr_page != '':
                common.addon.add_directory( { 'indexer':item['indexer'], 'indexer_id':indexer_id, 'mode':common.mode_Section, 'section':item.get('section',''), 
                    'url':item.get('url', ''), 'type':item.get('type', ''), 'page':curr_page, 'total_pages': curr_page_count, 'title':urllib.quote_plus(title),
                    'sort_by': curr_sort_by, 'sort_order':currt_sort_order, 'ui_item_mode':'gotopage' }, {'title': '[COLOR white][B]Page ' + curr_page + ' of ' + curr_page_count + '[/B][/COLOR]' }, 
                    img=common.get_themed_icon('page.png'), fanart=common.get_themed_fanart('page.jpg') ) 
                
            if curr_sort_by != '':
                sort_by_options = entertainment.GetSortByOptions(indexer, indexer_id)
                curr_sort_by_title = sort_by_options[curr_sort_by]
                common.addon.add_directory( { 'indexer':item['indexer'], 'indexer_id':indexer_id, 'mode':common.mode_Section, 'section':item.get('section',''), 
                'url':item.get('url', ''), 'type':item.get('type', ''), 'page':curr_page, 'total_pages': curr_page_count, 'title':urllib.quote_plus(title),
                'sort_by': curr_sort_by, 'sort_order':currt_sort_order, 'ui_item_mode':'sortby' }, {'title': '[B][COLOR white]Sort By: [/COLOR][COLOR yellow]' + curr_sort_by_title + '[/COLOR][/B]' },
                img=common.get_themed_icon('sort.png'), fanart=common.get_themed_fanart('sort.jpg') ) 
                
            if currt_sort_order != '':
                sort_order_options = entertainment.GetSortOrderOptions(indexer, indexer_id)
                currt_sort_order_title = sort_order_options[currt_sort_order]
                common.addon.add_directory( { 'indexer':item['indexer'], 'indexer_id':indexer_id, 'mode':common.mode_Section, 'section':item.get('section',''), 
                'url':item.get('url', ''), 'type':item.get('type', ''), 'page':curr_page, 'total_pages': curr_page_count, 'title':urllib.quote_plus(title),
                'sort_by': curr_sort_by, 'sort_order':currt_sort_order, 'ui_item_mode':'sortorder' }, {'title': '[B][COLOR white]Sort Order: [/COLOR][COLOR yellow]' + currt_sort_order_title + '[/COLOR][/B]' },
                img=common.get_themed_icon('sort.png'), fanart=common.get_themed_fanart('sort.jpg') ) 
                
            if curr_page != '' and curr_page != '1':
                common.addon.add_directory( { 'indexer':item['indexer'], 'indexer_id':indexer_id, 'mode':common.mode_Section, 'section':item.get('section',''), 
                'url':item.get('url', ''), 'type':item.get('type', ''), 'page': '1', 'total_pages': curr_page_count, 'title':urllib.quote_plus(title),
                'sort_by': curr_sort_by, 'sort_order':currt_sort_order }, {'title': '[COLOR white][B]<< First Page[/B][/COLOR]' },
                img=common.get_themed_icon('firstpage.png'), fanart=common.get_themed_fanart('firstpage.jpg') ) 
                
                common.addon.add_directory( { 'indexer':item['indexer'], 'indexer_id':indexer_id, 'mode':common.mode_Section, 'section':item.get('section',''), 
                'url':item.get('url', ''), 'type':item.get('type', ''), 'page': str(int(curr_page) - 1), 'total_pages': curr_page_count, 'title':urllib.quote_plus(title),
                'sort_by': curr_sort_by, 'sort_order':currt_sort_order }, {'title': '[COLOR white][B]< Previous Page[/B][/COLOR]' },
                img=common.get_themed_icon('previouspage.png'), fanart=common.get_themed_fanart('previouspage.jpg') ) 
                
            if curr_page != curr_page_count:
                next_page_dict = { 'indexer':item['indexer'], 'indexer_id':indexer_id, 'mode':common.mode_Section, 'section':item.get('section',''), 
                    'url':item.get('url', ''), 'type':item.get('type', ''), 'page':str(int(curr_page) + 1), 'total_pages': item.get('total_pages', ''),
                    'title':urllib.quote_plus(title), 'sort_by': curr_sort_by, 'sort_order':currt_sort_order }            
                    
                last_page_dict = { 'indexer':item['indexer'], 'indexer_id':indexer_id, 'mode':common.mode_Section, 'section':item.get('section',''), 
                    'url':item.get('url', ''), 'type':item.get('type', ''), 'page':curr_page_count, 'total_pages': item.get('total_pages', ''),
                    'title':urllib.quote_plus(title), 'sort_by': curr_sort_by, 'sort_order':currt_sort_order }            
        else:
        
            this_meta = {}
            video_type = ''
            
            item_fav = item.get('favorite', 'false')
            item_bmk = item.get('bookmark', 'false')
            item_type=item.get('type', '') 
            
            video_type = get_video_type(indexer, section, item_type, type) if item_fav=='false' and item_bmk == 'false' else item.get('video_type', '')
            
            if section=='main' and not type and item.get('mode', '') == common.mode_Content:
            
                video_type=get_video_type('','','',indexer)
                
                if 'movie' in item_type:
                    use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
                elif 'tv' in item_type:
                    use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
                    
                if use_meta == True and not metaget:
                    from metahandler import metahandlers
                    metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
            
            if (indexer == common.indxr_Lists or 'list' in section or item_fav == 'true') and item.get('mode', "") not in (common.mode_Dummy, common.mode_Info, common.mode_Section):
                if video_type == common.VideoType_Movies:
                    use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies,'metadata_movies') == 'true' else False
                elif video_type in (common.VideoType_Season, common.VideoType_Episode, common.VideoType_TV):
                    use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows,'metadata_tv_shows') == 'true' else False

                if use_meta == True and not metaget:
                    from metahandler import metahandlers
                    metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)

            if use_meta == True:                
                this_meta = this_metas[content_items_loop]
                content_items_loop = content_items_loop + 1
                    
            if item_bmk == 'true':
                 item['item_title'] = item['title']
                 
            if not item['title']:
                if use_meta == True:
                    item['title'] = this_meta['title']
                else:
                    item['title'] = '-'
                    
                if item_bmk == 'true':
                    item['item_title'] = item['title']
                    item['title'] = item['name'] + ' ' + ( '(' + item['year'] + ') ' if item['year'] else '') + '- S' + item['season'] + 'E' + item['episode'] + ' - ' + item['title']
            this_meta.update({'title': ( hleveler * int ( item.get('hlevel', '0') ) ) + htmlcleaner.clean(item['title'])})
            meta_img = item.get('img', '') if this_meta.get('cover_url', '') == '' else this_meta.get('cover_url', '')
            meta_fanart = item.get('fanart', '') if this_meta.get('backdrop_url', '') == '' else this_meta.get('backdrop_url', '')
            meta_imdb_id = this_meta.get('imdb_id', '')
            meta_watched = this_meta.get('overlay', 6)

            this_meta.update({'plot': item.get('plot', '') if this_meta.get('plot', '' ) == '' else this_meta.get('plot', '' ) })
            
            item_indexer=item['indexer']
            item_indexer_id=item['website']
            item_mode=item['mode']
            item_section=item.get('section','')
            item_url=item.get('url', '') 
            item_urls=item.get('urls', '') 
            item_title=item.get('item_title', '') if item_indexer not in (common.indxr_Sports, common.indxr_Live_TV) and (item_fav == 'true' or item_bmk == 'true') else item.get('title', '')
            item_name=item.get('name', '')
            item_year=item.get('year', '')
            item_season=item.get('season', '')
            item_episode=item.get('episode', '')            
            item_meta_img=meta_img
            item_meta_fanart=meta_fanart

            if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'sync_watched_status_with_lib') == 'true':
                xbmclibinfo = get_info_from_xbmc_library(video_type, item_name, item_season, item_episode, item_year, properties=["playcount"])
                xbmcdbid = xbmclibinfo['xbmcdbid']
                if xbmcdbid:
                    playcount = xbmclibinfo['playcount']
                    if not playcount:
                        playcount = 0
                    if (meta_watched == 6 and playcount <= 0) or (meta_watched == 7 and playcount > 0):
                        common.addon.log('Watch status is same in iStream and XBMC library.')
                    else:
                        if use_meta == True:
                            metaget.change_watched(video_type, item_name, meta_imdb_id, season=item_season, episode=item_episode, year=item_year)
                            if meta_watched == 6: meta_watched = 7
                            elif meta_watched == 7: meta_watched = 6                            
                            
                        if playcount <= 0: meta_watched = 6
                        elif playcount > 0: meta_watched = 7
                        
                        this_meta['playcount'] = playcount
            
            contextMenuItems = add_contextmenu(video_type, item_indexer, item_indexer_id, item_mode, item_section, 
                    item_url, meta_imdb_id, item_title, item_name, item_year, item_season, item_episode, item_type, use_meta, 
                    item_meta_img, item_meta_fanart, meta_watched, item_fav, trailer=this_meta.get('trailer', ''), urls=item_urls )
            
            cmi_str = str(contextMenuItems)
            if '[COLOR red]Unsubscribe[/COLOR]' in cmi_str and '[COLOR red]Delete[/COLOR] from Favorites' in cmi_str:
                this_meta.update({'title':'[B][COLOR gold]|||[/COLOR] [COLOR green]|*|[/COLOR][/B] ' + this_meta['title']})
            elif '[COLOR red]Unsubscribe[/COLOR]' in cmi_str:
                this_meta.update({'title':'[B][COLOR gold]|||[/COLOR][/B] ' + this_meta['title']})
            elif '[COLOR red]Delete[/COLOR] from Favorites' in cmi_str:
                this_meta.update({'title':'[B][COLOR green]|*|[/COLOR][/B] ' + this_meta['title']})
            
            try:
                item_query_dict = {'istream_path':istream_path + ' : ' + this_meta['title'], 'indexer':item_indexer, 'indexer_id':item_indexer_id, 'mode':item_mode, 'section':item_section, 
                        'title':common.CleanText2(item_title, True, True), 'name':common.CleanText2(item_name, True, True), 'year':item_year, 'season':item_season, 'episode':item_episode, 'favorite':item_fav,
                        'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'urls':item_urls, 'imdb_id':meta_imdb_id}
                istream_query_dict = {'istream_path':istream_path + ' : ' + this_meta['title'], 'indexer':item_indexer, 'indexer_id':item_indexer_id, 'mode':common.mode_Add_to_MyStream, 'item_mode':item_mode, 'section':item_section, 
                        'title':common.CleanText2(item_title, True, True), 'name':common.CleanText2(item_name, True, True), 'year':item_year, 'season':item_season, 'episode':item_episode, 'favorite':item_fav,
                        'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'urls':item_urls, 'imdb_id':meta_imdb_id}
            except:
                item_query_dict = {'istream_path':istream_path + ' : ' + this_meta['title'],'indexer':item_indexer, 'indexer_id':item_indexer_id, 'mode':item_mode, 'section':item_section, 
                        'title':urllib.quote_plus(common.CleanText2(item_title, True, True)), 
                        'name':urllib.quote_plus(common.CleanText2(item_name, True, True)), 'year':item_year, 'season':item_season, 'favorite':item_fav, 
                        'episode':item_episode, 'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'urls':item_urls, 'imdb_id':meta_imdb_id}
                istream_query_dict = {'istream_path':istream_path + ' : ' + this_meta['title'],'indexer':item_indexer, 'indexer_id':item_indexer_id, 'mode':common.mode_Add_to_MyStream, 'item_mode':item_mode, 'section':item_section, 
                        'title':urllib.quote_plus(common.CleanText2(item_title, True, True)), 
                        'name':urllib.quote_plus(common.CleanText2(item_name, True, True)), 'year':item_year, 'season':item_season, 'favorite':item_fav, 
                        'episode':item_episode, 'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'urls':item_urls, 'imdb_id':meta_imdb_id}
            
            trailer = this_meta.get('trailer', '')
            if trailer and 'plugin://plugin.video.youtube/' in trailer:
                trailer = '%s' % common.addon.build_plugin_url({'mode':common.mode_Play_Trailer, 'url':trailer})
            item_query_dict.update({'trailer':trailer})
            istream_query_dict.update({'trailer':trailer})
            
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))                            
            if video_type in (common.VideoType_Movies, common.VideoType_Episode):
                auto_or_host_item = item_query_dict.copy()
                autoplaysetting = entertainment.GetiStreamSettings(indexer, 'autoplay')
                autoplay = (autoplaysetting == 'true')
                if autoplay:
                    auto_or_host_item.update({'autoplay':'false'})
                    contextMenuItems.insert(1, ('[COLOR gold]Hosts...[/COLOR]', 'Container.Update(%s, True)' % common.addon.build_plugin_url(auto_or_host_item)))
                else:
                    auto_or_host_item.update({'autoplay':'true'})
                    contextMenuItems.insert(1, ('[COLOR gold]Autoplay...[/COLOR]', 'Container.Update(%s, True)' % common.addon.build_plugin_url(auto_or_host_item)))
                #show_hosts_auto_dialog = item_query_dict.copy()
                #show_hosts_auto_dialog.update( {'show_hosts_autoplay_dialog' : 'true'})
                #contextMenuItems.insert(1, ('[COLOR gold][B]-= Hosts/Autoplay =-[/B][/COLOR]', 'Container.Update(%s, True)' % common.addon.build_plugin_url(show_hosts_auto_dialog)))
            common.addon.add_directory(item_query_dict, this_meta, 
                    contextmenu_items=contextMenuItems, context_replace=True, img=meta_img, fanart=meta_fanart, total_items=totalitems)
        item_list_index = item_list_index + 1
                
    if next_page_dict:
        common.addon.add_directory(next_page_dict, {'title': '[COLOR white][B]Next Page >[/B][/COLOR]'},
            img=common.get_themed_icon('nextpage.png'), fanart=common.get_themed_fanart('nextpage.jpg') ) 
        
    if last_page_dict:
        common.addon.add_directory(last_page_dict, {'title': '[COLOR white][B]Last Page >>[/B][/COLOR]'},
            img=common.get_themed_icon('lastpage.png'), fanart=common.get_themed_fanart('lastpage.jpg') ) 
        
    if section == 'main':
        if indexer == common.indxr_TV_Shows:
            item_query_dict = {'istream_path':istream_path + ' : ' + 'Subscriptions','mode':common.mode_Manage_Subs, 'indexer':indexer, 'type':'tv_seasons', 'video_type':common.VideoType_TV,
                'title':'Subscriptions'}
            istream_query_dict = {'istream_path':istream_path + ' : ' + 'Subscriptions','mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Manage_Subs, 'indexer':indexer, 'type':'tv_seasons', 'video_type':common.VideoType_TV,
                'title':'Subscriptions'}
            contextMenuItems = []
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
            common.addon.add_directory(item_query_dict, {'title': 'Subscriptions'}, contextmenu_items=contextMenuItems, img=common.get_themed_icon('subscriptions.png'), fanart=common.get_themed_fanart('subscriptions.jpg') )
            
        search_item = entertainment.GetSearchItem(indexer)
        
        if search_item and len(search_item) > 0:
            search_item = search_item[0]
            item_query_dict = {'istream_path':istream_path + ' : ' + search_item['title'],'indexer':search_item['indexer'], 'indexer_id':search_item['indexer_id'], 'mode':search_item['mode'], 'section':search_item['section']}
            istream_query_dict = {'istream_path':istream_path + ' : ' + search_item['title'],'indexer':search_item['indexer'], 'indexer_id':search_item['indexer_id'], 'mode':common.mode_Add_to_MyStream, 'item_mode':search_item['mode'], 'section':search_item['section']}
            contextMenuItems = []
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
            common.addon.add_directory(item_query_dict, {'title': search_item['title']}, contextmenu_items=contextMenuItems, img=common.get_themed_icon('search.png'), fanart=common.get_themed_fanart('search.jpg') )
    
    try:
        DialogiStreamProgress.close()
    except:
        pass
    
    setViewForMode(mode)
    common.addon.end_of_directory(updateListing = (False if (page=='' and sort_by=='' and sort_order=='') else True ) )

def GetContent(indexer, indexer_id, url, title, name, year, season, episode, type):
    ttl = name
    if year:
        ttl += ' (' + year + ')'
    if season and not episode:
        ttl += ' - Season: ' + season
    if season and episode:
        ttl += ' - S' + season + 'E' + episode + ' - ' + title
    add_dir_title( ttl )
    
    entertainment.loadiStreamPlugins(type=indexer, load_indexer=True, load_settings=True, load_webproxyproviders=True )
    
    if urls and len(common.ConvertStringToDict(urls)) > 1:
        (items,message_queue) = entertainment.GetContent (indexer, indexer_id, url, title, name, year, season, episode, type, urls=urls)
        RetrieveAndDisplayMessages(message_queue)
        meta = []
    else:
        (items,meta) = entertainment.GetContent (indexer, indexer_id, url, title, name, year, season, episode, type)

    
    use_meta = True
    if len(meta) <= 0:
        use_meta = False
       
    metaget = ''    
    if 'movie' in type:
        use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
    elif 'tv' in type:
        use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
        
    if use_meta == True:
        from metahandler import metahandlers
        metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
        
    totalitems = len(items)
    
    item_list_index = 0
    for item in items:
    
        item['title'] = item.get('title', '')
        item['name'] = item.get('name', '')
    
        from entertainment import htmlcleaner
        episode = item.get('episode', '')
        if episode != '':
            episode = 'Episode ' + episode + ' - '
        
        this_meta = {}
        video_type = ''
            
        item_type=item.get('type', '')
        item_fav = item.get('favorite', 'false')
            
        video_type = get_video_type(indexer, section, item_type, type) if item_fav=='false' else item.get('video_type', '')
            
        if indexer == common.indxr_Lists or 'list' in section or item_fav == 'true':
            if video_type == common.VideoType_Movies:
                use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies,'metadata_movies') == 'true' else False
            elif video_type in (common.VideoType_Season, common.VideoType_Episode, common.VideoType_TV):
                use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows,'metadata_tv_shows') == 'true' else False
                
            if use_meta == True and not metaget:
                from metahandler import metahandlers
                metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)

        
        if use_meta == True:                                
            sn = item.get('season', '0')
            sn = '0' if sn == '' else sn
            
            en = item.get('episode', '0')
            en = '0' if en == '' else en
            
            this_meta = get_metadata(metaget, video_type, 
                item.get('name', '') if video_type in (common.VideoType_Movies, common.VideoType_TV) else item.get('title', ''), 
                item.get('name', ''), item.get('year', ''), imdb = item.get('imdb_id', None) if (imdb_id == None or imdb_id == '') else imdb_id, 
                season_num=int(sn), episode_num=int(en))
        
        if not item['title']:
            if use_meta == True:
                item['title'] = this_meta['title']
            else:
                item['title'] = '-'
        this_meta.update({'title': ( hleveler * int ( item.get('hlevel', '0') ) ) + episode + htmlcleaner.clean(item['title'])})
                
        meta_img = item.get('img', '') if this_meta.get('cover_url', '') == '' else this_meta.get('cover_url', '')
        meta_fanart = item.get('fanart', '') if this_meta.get('backdrop_url', '') == '' else this_meta.get('backdrop_url', '')
        meta_imdb_id = this_meta.get('imdb_id', '')
        meta_watched = this_meta.get('overlay', 6)
        
        this_meta.update({'plot': item.get('plot', '') if this_meta.get('plot', '' ) == '' else this_meta.get('plot', '' ) })
        
        item_indexer=item['indexer']
        item_indexer_id=item['website']
        item_mode=item['mode']
        item_section=item.get('section','')
        item_url=item.get('url', '') 
        item_title=item.get('title', '')
        item_title=item.get('item_title', '') if item_fav == 'true' else item.get('title', '')
        item_name=item.get('name', '')
        item_year=item.get('year', '')
        item_season=item.get('season', '')
        item_episode=item.get('episode', '')
        item_meta_img=meta_img
        item_meta_fanart=meta_fanart
        item_urls = item.get('urls', '')
        
        if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'sync_watched_status_with_lib') == 'true':
            xbmclibinfo = get_info_from_xbmc_library(video_type, item_name, item_season, item_episode, item_year, properties=["playcount"])
            xbmcdbid = xbmclibinfo['xbmcdbid']
            if xbmcdbid:
                playcount = xbmclibinfo['playcount']
                if not playcount:
                    playcount = 0
                if (meta_watched == 6 and playcount <= 0) or (meta_watched == 7 and playcount > 0):
                    common.addon.log('Watch status is same in iStream and XBMC library.')
                else:
                    if use_meta == True:
                        metaget.change_watched(video_type, item_name, meta_imdb_id, season=item_season, episode=item_episode, year=item_year)
                        if meta_watched == 6: meta_watched = 7
                        elif meta_watched == 7: meta_watched = 6                            
                        
                    if playcount <= 0: meta_watched = 6
                    elif playcount > 0: meta_watched = 7
                    
                    this_meta['playcount'] = playcount
    
        contextMenuItems = add_contextmenu(video_type, item_indexer, item_indexer_id, item_mode, item_section, 
                item_url, meta_imdb_id, item_title, item_name, item_year, item_season, item_episode, item_type, 
                use_meta, item_meta_img, item_meta_fanart, meta_watched, item_fav, trailer=this_meta.get('trailer', ''),
                urls=item_urls)
        
        cmi_str = str(contextMenuItems)
        if '[COLOR red]Unsubscribe[/COLOR]' in cmi_str and '[COLOR red]Delete[/COLOR] from Favorites' in cmi_str:
            this_meta.update({'title':'[B][COLOR gold]|||[/COLOR] [COLOR green]|*|[/COLOR][/B] ' + this_meta['title']})
        elif '[COLOR red]Unsubscribe[/COLOR]' in cmi_str:
            this_meta.update({'title':'[B][COLOR gold]|||[/COLOR][/B] ' + this_meta['title']})
        elif '[COLOR red]Delete[/COLOR] from Favorites' in cmi_str:
            this_meta.update({'title':'[B][COLOR green]|*|[/COLOR][/B] ' + this_meta['title']})
        
        try:
            item_query_dict = {'indexer':item_indexer, 'indexer_id':item_indexer_id, 'mode':item_mode, 'section':item_section, 
                    'title':common.CleanText2(item_title, True, True), 'name':common.CleanText2(item_name, True, True), 'year':item_year, 'season':item_season, 'episode':item_episode, 'favorite':item_fav, 
                    'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'urls':item_urls, 'imdb_id':meta_imdb_id}            
        except:
            item_query_dict = {'indexer':item_indexer, 'indexer_id':item_indexer_id, 'mode':item_mode, 'section':item_section, 
                    'title':urllib.quote_plus(common.CleanText2(item_title, True, True)), 'name':urllib.quote_plus(common.CleanText2(item_name, True, True)), 'year':item_year, 'season':item_season, 'favorite':item_fav, 
                    'episode':item_episode, 'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'urls':item_urls, 'imdb_id':meta_imdb_id}                
        
        trailer = this_meta.get('trailer', '')
        if trailer and 'plugin://plugin.video.youtube/' in trailer:
            trailer = '%s' % common.addon.build_plugin_url({'mode':common.mode_Play_Trailer, 'url':trailer})
        item_query_dict.update({'trailer':trailer})
    
        if video_type in (common.VideoType_Movies, common.VideoType_Episode):
            auto_or_host_item = item_query_dict.copy()
            autoplaysetting = entertainment.GetiStreamSettings(indexer, 'autoplay')
            autoplay = (autoplaysetting == 'true')
            if autoplay:
                auto_or_host_item.update({'autoplay':'false'})
                contextMenuItems.insert(1, ('[COLOR gold]Hosts...[/COLOR]', 'Container.Update(%s, True)' % common.addon.build_plugin_url(auto_or_host_item)))
            else:
                auto_or_host_item.update({'autoplay':'true'})
                contextMenuItems.insert(1, ('[COLOR gold]Autoplay...[/COLOR]', 'Container.Update(%s, True)' % common.addon.build_plugin_url(auto_or_host_item)))
            #show_hosts_auto_dialog = item_query_dict.copy()
            #show_hosts_auto_dialog.update( {'show_hosts_autoplay_dialog' : 'true'})
            #contextMenuItems.insert(1, ('[COLOR gold][B]-= Hosts/Autoplay =-[/B][/COLOR]', 'Container.Update(%s, True)' % common.addon.build_plugin_url(show_hosts_auto_dialog)))
        common.addon.add_directory(item_query_dict, this_meta, 
                contextmenu_items=contextMenuItems, context_replace=True, img=meta_img, fanart=meta_fanart, total_items=totalitems)
    
        item_list_index = item_list_index + 1                
    
    setViewForMode(mode)
    common.addon.end_of_directory()
    
def GetSportsContent(indexer, indexer_id, title):
    add_dir_title()
    
    entertainment.loadiStreamPlugins(type=indexer, load_source=True, load_settings=True, load_webproxyproviders=True)
    
    (items, message_queue) = entertainment.GetSportsContent(indexer, indexer_id)
        
    RetrieveAndDisplayMessages(message_queue)
    
    for item in items:
        
        game_time = item['time']
        time_format = common.addon.get_setting('timeformat')
        time_zone_src = common.addon.get_setting('timezonesource')
        time_zone = common.get_gmt_offset() if time_zone_src == '0' else int(common.addon.get_setting('timezone'))
        str_time_format = '%I:%M %p' if time_format == '0' else '%H:%M'
        
        import datetime        
        import time
        try:
            local_time = (datetime.datetime.strptime(game_time, '%Y %m %d %H:%M') + datetime.timedelta(hours=time_zone)).time().strftime(str_time_format)
        except TypeError:
            local_time = (datetime.datetime.fromtimestamp(time.mktime(time.strptime(game_time, '%Y %m %d %H:%M'))) + datetime.timedelta(hours=time_zone)).time().strftime(str_time_format)
        
        new_title = '[COLOR yellow][ ' + local_time + ' ][/COLOR] - ' + item['title'].upper().replace(' VS ', '[COLOR red] VS [/COLOR]')
        common.addon.add_directory({'indexer':indexer, 'indexer_id':indexer_id, 'source':indexer, 'source_id':item['website'], 'mode':item['mode'],
            'type': item['type'], 'id':item['id'], 'url':item['url'], 'title':new_title, 'urls':item.get('urls', '') },
            {'title': new_title } 
            )
            
    setViewForMode(mode)
    common.addon.end_of_directory()     
    
def GetLiveTVContent(indexer, indexer_id, title):
    
    add_dir_title()
    
    region = common.addon.queries.get('region', '')
    language = common.addon.queries.get('language', '')
    
    (items, message_queue) = entertainment.GetLiveTVLinks(indexer, indexer_id, other_names, region, language)
        
    RetrieveAndDisplayMessages(message_queue)

    if len(items) == 1:
        entertainment.loadiStreamPlugins(type=indexer, load_resolvers=True, load_settings=True, load_webproxyproviders=True)
        ResolveAndPlay(indexer, items[0]['website'], items[0]['url'], title, title, '', '', '', '')
    else:
        for item in items:
            common.addon.add_directory({'indexer':indexer, 'indexer_id':indexer_id, 'source':indexer, 'source_id':item['website'], 'mode':item['mode'],
                'id':item['id'], 'url':item['url'], 'img':img, 'fanart':fanart, 'name':title, 'title':title, 'urls':item.get('urls', ''), 'play':'true' },
                {'title': ':: ' + item['title'] + ' :: [COLOR gold][' + item['region'] + ' | ' + item['language'] +'] : [/COLOR][COLOR ' + quality_to_color.get(item['quality'], 'white') + '][' + item['quality'] + '][/COLOR] [COLOR royalblue]: ' + item['host'].upper() + '[/COLOR]' }, 
                img=item['img'] if item['img'] else img, fanart=item['fanart'] if item['fanart']  else fanart 
                )
    
        setViewForMode(mode)
        common.addon.end_of_directory()     

class PlaybackFailed(Exception):
    '''Raised to indicate that xbmc failed to play the stream'''
class Unresolvable(Exception):
    '''Raised to indicate that urlresolver failed to resolve the url'''
class HostSkipped(Exception):
    '''Raised to indicate that user pressed stop within first 5 seconds and want to skip to the next host in line'''

xbmc_auto_play_progress_dialog = None
def GetFileHosts(indexer, indexer_id, url, title, name, year, season, episode, type, urls=''):
    global library
    
    global source_names
    global source_urls
    global source_tried
    
    global xbmc_auto_play_progress_dialog
    
    entertainment.loadiStreamPlugins(type=indexer, load_source=True, load_settings=True, load_webproxyproviders=True, load_fileformats=True )
    
    autoplaysetting = entertainment.GetiStreamSettings(indexer, 'autoplay')
    autoplay = ( (autoplaysetting == 'true' and autoplay_from_queries == '') or autoplay_from_queries=='true')
    
    # hosts/autoplay selection dialog.
    #
    #if common.addon.queries.get('autoplayhostseldialogshown', 'false') == 'false' and ( (autoplay and not queued) or not autoplay ):
    #    common.addon.queries.update({'autoplayhostseldialogshown':'true'})
    #    showautoplayhostdialog = entertainment.GetiStreamSettings(indexer, 'autoplay_host_sel_dialog')
    #    if showautoplayhostdialog == 'true' or show_hosts_autoplay_dialog == 'true':
    #        xbmcauotplayhostseldlg = xbmcgui.Dialog()
    #        list_autoplay_host_sel = ['[B]Hosts List:[/B] List of playable links for selection', '[B]Autoplay:[/B] Auto try links until one plays', '[B]Hosts List (Default):[/B] Always display the list of playable links', '[B]Autoplay (Default):[/B] Always try the links automatically until one plays', '', '[B][COLOR yellow]INFORMATION[/COLOR][/B]','Selecting a [B]DEFAULT[/B] item will disable this dialog.', 'Use [B]Hosts/Autoplay[/B] from context menu to bring back this dialog.']
    #        ret_autoplay_host_sel = xbmcauotplayhostseldlg.select('Please select from below', list_autoplay_host_sel)
    #        if ret_autoplay_host_sel < 0 or ret_autoplay_host_sel > 3:
    #            xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem(title))
    #            return
    #        if ret_autoplay_host_sel == 0 or ret_autoplay_host_sel == 1:
    #            entertainment.SetiStreamSettings(indexer, 'autoplay_host_sel_dialog', 'true')
    #        if ret_autoplay_host_sel == 2 or ret_autoplay_host_sel == 3:
    #            entertainment.SetiStreamSettings(indexer, 'autoplay_host_sel_dialog', 'false')
    #        if ret_autoplay_host_sel == 0 or ret_autoplay_host_sel == 2:
    #            entertainment.SetiStreamSettings(indexer, 'autoplay', 'false')        
    #        if ret_autoplay_host_sel == 1 or ret_autoplay_host_sel == 3:
    #            entertainment.SetiStreamSettings(indexer, 'autoplay', 'true')
    #        
    #        autoplaysetting = entertainment.GetiStreamSettings(indexer, 'autoplay')
    #        autoplay = ( (autoplaysetting == 'true' and autoplay_from_queries == '') or autoplay_from_queries=='true')
    
    if autoplay and not queued:
        entertainment.loadiStreamPlugins(type=indexer, load_resolvers=True)
        ResolveAndPlay(indexer, indexer_id, url, title, name, year, season, episode, type)
        return
        
    list_key = []
    list_value = []
    
    import xbmc
    
    if not source_names:
        if library != 'true':
            ttl = name
            if year:
                ttl += ' (' + year + ')'
            if season and not episode:
                ttl += ' - Season: ' + season
            if season and episode:
                ttl += ' - S' + season + 'E' + episode + ' - ' + title
            add_dir_title( ttl )

        from istreams.dialogs import DialogiStreamProgress
        DialogiStreamProgress.show("iStream: Search Hosts", "Searching for links on the web...")
        (items, message_queue) = entertainment.GetFileHosts (indexer, indexer_id, url, title, name, year, season, episode, type, urls, autoplay=autoplay)        
        RetrieveAndDisplayMessagesiStreamProgressDialog(message_queue, DialogiStreamProgress)
        DialogiStreamProgress.addUpdateItem('Displaying retrieved links...')
        xbmc.sleep(1000)        
        
        if trailer_url:
            common.addon.add_item({}, {'title':'Trailer'}, None, '', False, img, fanart, total_items=0, resolved=trailer_url, is_folder=True, is_playable=None ) 
        
        for item in items:
            if indexer == common.indxr_Sports:
                common.addon.add_directory({'source':indexer, 'source_id':item['website'], 'mode':item['mode'],
                    'play':'true' if item['mode'] == common.mode_Play else '', 'url':item['url'], 
                    'title':title, 'type':type, 'img':img, 'fanart':fanart}, 
                    {'title': ':: ' + item['website'].upper() + ' :: [COLOR yellow]' + item['title'] + '[/COLOR]'}, img=img, fanart=fanart )
            else:
                item_queries = {'source':indexer, 'source_id':item['website'], 'mode':item['mode'],
                        'play':'true' if item['mode'] == common.mode_Play else '', 'section':item['id'], 'url':item['hosturl'], 
                        'title':title, 'name':name, 'year':year, 'season':season, 'episode':episode, 'type':type, 'img':img, 'fanart':fanart, 'imdb_id':imdb_id}

                if library != 'true' and autoplay == False:
                    if '|||part|||' in item['hosturl']:
                        common.addon.add_directory(item_queries, {'title': ':: ' + item['website'].upper() + ' :: [COLOR ' + quality_to_color.get(item['quality'], 'white') + '][' + item['quality'] + '][/COLOR] [COLOR royalblue]: ' + item['title'] + ' :[/COLOR] [COLOR white][B]||| Play All |||[/B][/COLOR]'}, img=img, fanart=fanart )
                        i=0
                        host_urls = item['hosturl'].split('|||part|||')
                        host_urls = filter(bool, host_urls)
                        host_count = len(host_urls)
                        for host_url in host_urls:
                            if not host_url or len(host_url) <= 0: continue
                            item_queries.update({'url':host_url})
                            item_queries.update({'name':name + '- Part ' + str(i+1) + ' of ' + str(host_count)})
                            common.addon.add_directory(item_queries, {'title': '.....Part %s' % str(i+1)}, img=img, fanart=fanart )
                            i+=1
                    else:
                        common.addon.add_directory(item_queries, {'title': ':: ' + item['website'].upper() + ' :: [COLOR ' + quality_to_color.get(item['quality'], 'white') + '][' + item['quality'] + '][/COLOR] [COLOR royalblue]: ' + item['title'] + '[/COLOR]'}, img=img, fanart=fanart )
                        
                else:
                    if autoplay == True and '|||part|||' in item['hosturl']: continue
                    if '|||part|||' in item['hosturl']:
                        list_key.append(':: ' + item['website'].upper() + ' :: [COLOR ' + quality_to_color.get(item['quality'], 'white') + '][' + item['quality'] + '][/COLOR] [COLOR royalblue]: ' + item['title'] + ' :[/COLOR] [COLOR white][B]||| Play All |||[/B][/COLOR]')
                        list_value.append(item_queries)
                        i=0
                        host_urls = item['hosturl'].split('|||part|||')
                        host_urls = filter(bool, host_urls)
                        host_count = len(host_urls)
                        for host_url in host_urls:
                            if not host_url or len(host_url) <= 0: continue
                            host_item_queries=item_queries.copy()
                            host_item_queries.update({'url':host_url})
                            host_item_queries.update({'name':name + '- Part ' + str(i+1) + ' of ' + str(host_count)})
                            list_key.append('.....Part %s' % str(i+1))
                            list_value.append(host_item_queries)
                            i+=1
                    else:
                        list_key.append(':: ' + item['website'].upper() + ' :: [COLOR ' + quality_to_color.get(item['quality'], 'white') + '][' + item['quality'] + '][/COLOR] [COLOR royalblue]: ' + item['title'] + '[/COLOR]')
                        list_value.append(item_queries)
                        
        DialogiStreamProgress.close()
    else:
        list_key = common.ConvertStringToList(source_names) if len(source_names) > 2 else []
        list_value = common.ConvertStringToList(source_urls) if len(source_urls) > 2 else []
        
    if autoplay and not list_key:
        return

    
    if not source_names:
        source_names = common.ConvertListToString(list_key)
        source_urls = common.ConvertListToString(list_value)        
        
        if autoplay == True:
            import time
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(title))
            time.sleep(1)
            xbmc.executebuiltin('Dialog.Close(all,true)')
            time.sleep(1)
            common.addon.queries.update({'source_names':source_names, 'source_urls':source_urls, 'source_tried':source_tried, 'queued':'', 'autoplayhostseldialogshown':'true'})
            xbmc.executebuiltin('RunPlugin(%s)' % common.addon.build_plugin_url(common.addon.queries))        
            return
    
    host_count = len(list_key)
    if host_count > 0:
        
        if autoplay == False:            
            xbmcdlg = xbmcgui.Dialog()
        
            ret = xbmcdlg.select('Please select from below', list_key)
            if ret < 0:
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem(title))
                return
                
            queries = list_value[ret]

            if queries != None and queries != '':
                entertainment.loadiStreamPlugins(type=indexer, load_resolvers=True)
                ResolveAndPlay(queries['source'], queries['source_id'], queries['url'], queries['title'], queries['name'], 
                    queries['year'], queries['season'], queries['episode'], queries['type'])
        else:            
            
            entertainment.loadiStreamPlugins(type=indexer, load_resolvers=True)
            
            xbmc_auto_play_progress_dialog = xbmcgui.DialogProgress()
            action = '[COLOR white][B]Trying Sources...[/B][/COLOR]'
            xbmc_auto_play_progress_dialog.create('iStream', action, ' ', ' ')
            host_index = 0
            x = 0
            success = False
            for host in list_key:                
                if xbmc_auto_play_progress_dialog.iscanceled() or xbmc.abortRequested or success: return    
                host_index += 1

                if host.startswith("'"): host = host[1:]
                if host[1] == "'": host = host[2:]
                if host.endswith("'"): host = host[:-1]

                xbmc_auto_play_progress_dialog.create('iStream', action, host, ' ')
                percent = int((host_index * 100) / host_count)
                xbmc_auto_play_progress_dialog.update(percent)
                try:
                    queries = list_value[x]
                    x += 1
                    queries_url = queries['url']
                    if queries_url in source_tried:
                        continue
                    else:
                        source_tried += queries_url + ','
                    ResolveAndPlay(queries['source'], queries['source_id'], queries_url, queries['title'], queries['name'], 
                        queries['year'], queries['season'], queries['episode'], queries['type'])                    
                    xbmc_auto_play_progress_dialog.close()
                    success = True
                    break
                except PlaybackFailed:
                    xbmc_auto_play_progress_dialog.create('iStream', action, host, 'XBMC failed to play the file.')
                    xbmc_auto_play_progress_dialog.update(percent)
                    common.addon.log('Playback Failed.')
                    common.addon.queries.update({'source_names':source_names, 'source_urls':source_urls, 'source_tried':source_tried, 'queued':''})
                    xbmc.executebuiltin('RunPlugin(%s)' % common.addon.build_plugin_url(common.addon.queries))
                    break
                except HostSkipped:
                    xbmc_auto_play_progress_dialog.create('iStream', action, host, 'Skip Host.')
                    xbmc_auto_play_progress_dialog.update(percent)
                    common.addon.log('Host Skipped.')
                    common.addon.queries.update({'source_names':source_names, 'source_urls':source_urls, 'source_tried':source_tried, 'queued':''})
                    xbmc.executebuiltin('RunPlugin(%s)' % common.addon.build_plugin_url(common.addon.queries))
                    break
                except Unresolvable:
                    xbmc_auto_play_progress_dialog.create('iStream', action, host, 'Unable to resolve url.')
                    xbmc_auto_play_progress_dialog.update(percent)
                    common.addon.log('Unresolvable.')
                except Exception, e:
                    xbmc_auto_play_progress_dialog.create('iStream', action, host, str(e))
                    xbmc_auto_play_progress_dialog.update(percent)
                    common.addon.log(str(e))
          
            
    if library != 'true' and autoplay == False:
        setViewForMode(mode)
        common.addon.end_of_directory()     
    
def Settings(section = ''):

    items = entertainment.GetSettingsSections(section)
    
    if items and len(items) > 0:
    
        for item in items:
            item_query_dict = {'istream_path':istream_path + ' : ' + item['name'],'mode':common.mode_Settings, 'title': item['name'], 'settings_section':item['id'], 'type':item.get('type','')}
            istream_query_dict = {'istream_path':istream_path + ' : ' + item['name'],'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Settings, 'title': item['name'], 'settings_section':item['id'], 'type':item.get('type','')}
            contextMenuItems = []
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
            common.addon.add_directory(item_query_dict, {'title': item['name']}, img=item['img'], fanart=item['fanart'], contextmenu_items=contextMenuItems )
                
        setViewForMode(mode)
        common.addon.end_of_directory()
        
    else:
        if type:
            entertainment.loadiStreamPlugins(load_settingsxml=False, type=type, load_indexer=True, load_source=True, load_settings=True)
        from entertainment.addon import Addon
        settings = Addon(section)
        settings.show_settings()
        settings = None

    """
    if section == '':
        add_dir_title('Settings')
        
        common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR white][B]iStream[/B][/COLOR]'  })
        items = entertainment.GetiStreamSettings()        
        for item in items:
            common.addon.add_directory({'mode':common.mode_Settings, 'title': item['settings_name'], 'settings_section':item['settings_id']}, {'title': hleveler + item['settings_name']} )
        
        common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR white][B]ADVANCED[/B][/COLOR]'  })
        items = entertainment.GetSettings()
        for item in items:
            common.addon.add_directory({'mode':common.mode_Settings, 'title': item['settings_name'], 'settings_section':item['settings_id']}, {'title': hleveler + item['settings_name']} )
            
        common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR white][B]EXTERNAL[/B][/COLOR]'  })
        items = entertainment.GetExternalSettings()
        for item in items:
            common.addon.add_directory({'mode':common.mode_Settings, 'title': item['settings_name'], 'settings_section':item['settings_id']}, {'title': hleveler + item['settings_name']} )
        
        setViewForMode(mode)
        common.addon.end_of_directory()
    else:
        from entertainment.addon import Addon
        settings = Addon(section)
        settings.show_settings()
    """
    
def Search(indexer, type, page='', total_pages='', search_term='', individual_total_pages=''):

    if indexer == 'search':
        items = entertainment.GetAllSearchItems()
        for item in items:
                item_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':item['indexer'], 'mode':item['mode'], 'section':item['section'], 'title': item['title'], 'img':item.get('img', ''), 'fanart':item.get('fanart', '')}
                istream_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':item['indexer'], 'mode':common.mode_Add_to_MyStream, 'item_mode':item['mode'], 'section':item['section'], 'title': item['title'], 'img':item.get('img', ''), 'fanart':item.get('fanart', '')}
                contextMenuItems = []
                contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
                common.addon.add_directory(item_query_dict, {'title': item['title']}, img=item.get('img', ''), fanart=item.get('fanart', ''), contextmenu_items=contextMenuItems )
    
        setViewForMode(mode)    
        common.addon.end_of_directory()        
        return
    
    from entertainment import searchhistory
    SH = searchhistory.SearchHistory()    
    search_terms = SH.get_searchhistory(indexer)
    len_search_terms = 0 if common.addon.get_setting('search_history') == "false" else len(search_terms)
    
    if search_term == '' and (len_search_terms <= 0 or (title and '...' in title)):
        srch_dlg_hdr = '[COLOR royalblue]i[/COLOR]Stream '
        if indexer == common.indxr_Movies:
            srch_dlg_hdr = srch_dlg_hdr + 'Movies'
        elif indexer == common.indxr_TV_Shows:
            srch_dlg_hdr = srch_dlg_hdr + 'TV Shows'
        elif indexer == common.indxr_Live_TV:
            srch_dlg_hdr = srch_dlg_hdr + 'Live TV'
        srch_dlg_hdr = srch_dlg_hdr + ' Search'
        kb = xbmc.Keyboard('', srch_dlg_hdr, False)
        kb.doModal()
        if (kb.isConfirmed()):
            search = kb.getText()            
            if search != '':            
                search_term = search
                SH.add_search_term(indexer, search_term)

    elif search_term == '' and len_search_terms > 0:
    
        search_item = entertainment.GetSearchItem(indexer)
        if search_item and len(search_item) > 0:
            search_item = search_item[0]
            common.addon.add_directory({'indexer':search_item['indexer'], 'indexer_id':search_item['indexer_id'], 'mode':search_item['mode'], 
                'section':search_item['section'], 'title': search_item['title'] + '...'}, {'title': search_item['title'] + '...'} )
        
        for st in search_terms:
            common.addon.add_directory({'indexer':indexer, 'indexer_id':indexer_id, 'type':type, 'mode':mode, 'search_term':st, 'section':section}, 
                {'title': st} )
        common.addon.end_of_directory()
                
    if search_term != '':
    
        dialog = ''
        if page=='' and total_pages=='':
            dialog = xbmcgui.DialogProgress()
            dialog.create('Please wait: searching...', 'Searching... "' + search_term + '"')
            dialog.update(0)
    
        add_dir_title('Search: ' + search_term)
    
        (items, message_queue) = entertainment.Search (indexer, search_term, type, page, total_pages, individual_total_pages)
        
        RetrieveAndDisplayMessages(message_queue, dialog)
        
        next_page_dict = None
        last_page_dict = None
        
        metaget = ''
        if 'movie' in type:
            use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies,'metadata_movies') == 'true' else False
        elif 'tv' in type:
            use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows,'metadata_tv_shows') == 'true' else False
            
        if use_meta == True:
            from metahandler import metahandlers
            metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
        
        totalitems = len(items)
        
        from entertainment import htmlcleaner
                
        for item in items:
            
            item['title'] = item.get('title', '')
            item['name'] = item.get('name', '')
        
            if item['mode'] == common.mode_Dummy:
                common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':item.get('title', '')  })
            elif item['mode'] == common.mode_Info:
                curr_page = item.get('page', '')
                curr_page_count = item.get('total_pages', '')
                
                if curr_page != '' and curr_page != '0':
                    update_list_queries = { 'indexer':item['indexer'], 'indexer_id':item['website'], 'mode':common.mode_Search, 'section':item.get('section',''), 
                        'url':item.get('url', ''), 'urls':item.get('urls', ''), 'type':item.get('type', ''), 'page': curr_page, 'total_pages': curr_page_count, 'search_term':search_term, 
                        'individual_total_pages':item.get('individual_total_pages', ''), 'title':'search_update_listing'}
                    if page == '' and total_pages=='':                         
                        xbmc.executebuiltin('Container.Update(%s)' % common.addon.build_plugin_url(update_list_queries) )
                        common.addon.end_of_directory()
                        return
                    
                    common.addon.add_directory( { 'indexer':item['indexer'], 'indexer_id':item['website'], 'mode':common.mode_Search, 'section':item.get('section',''), 
                        'url':item.get('url', ''), 'urls':item.get('urls', ''), 'type':item.get('type', ''), 'page':curr_page, 'total_pages': curr_page_count,
                        'ui_item_mode':'gotopage', 'search_term':search_term, 'individual_total_pages':item.get('individual_total_pages', '') }, 
                        {'title': '[B][COLOR white]Page ' + curr_page + ' of ' + curr_page_count + '[/COLOR][/B]' },
                        img=common.get_themed_icon('page.png') ) 
                    
                if curr_page != '' and curr_page != '0' and curr_page != '1':
                    common.addon.add_directory( { 'indexer':item['indexer'], 'indexer_id':item['website'], 'mode':common.mode_Search, 'section':item.get('section',''), 
                        'url':item.get('url', ''), 'urls':item.get('urls', ''), 'type':item.get('type', ''), 'page': '1', 'total_pages': curr_page_count, 'search_term':search_term, 
                        'individual_total_pages':item.get('individual_total_pages', '')}, {'title': '[B][COLOR white]<< First Page[/COLOR][/B]' },
                        img=common.get_themed_icon('firstpage.png') ) 
                    
                    common.addon.add_directory( { 'indexer':item['indexer'], 'indexer_id':item['website'], 'mode':common.mode_Search, 'section':item.get('section',''), 
                        'url':item.get('url', ''), 'urls':item.get('urls', ''), 'type':item.get('type', ''), 'page': str(int(curr_page) - 1), 'total_pages': curr_page_count, 
                        'search_term':search_term, 'individual_total_pages':item.get('individual_total_pages', '') },{'title': '[B][COLOR white]< Previous Page[/COLOR][/B]' },
                        img=common.get_themed_icon('previouspage.png') ) 
                    
                if curr_page != curr_page_count:
                    next_page_dict = { 'indexer':item['indexer'], 'indexer_id':item['website'], 'mode':common.mode_Search, 'section':item.get('section',''), 
                        'url':item.get('url', ''), 'urls':item.get('urls', ''), 'type':item.get('type', ''), 'page':str(int(curr_page) + 1), 'total_pages': item.get('total_pages', ''), 
                        'search_term':search_term, 'individual_total_pages':item.get('individual_total_pages', '') }            
                        
                    last_page_dict = { 'indexer':item['indexer'], 'indexer_id':item['website'], 'mode':common.mode_Search, 'section':item.get('section',''), 
                        'url':item.get('url', ''), 'urls':item.get('urls', ''), 'type':item.get('type', ''), 'page':curr_page_count, 'total_pages': item.get('total_pages', ''), 
                        'search_term':search_term, 'individual_total_pages':item.get('individual_total_pages', '') }            
            else:
            
                this_meta = {}
                video_type = ''
            
                item_type=item.get('type', '')
                item_fav = item.get('favorite', 'false')
            
                video_type = get_video_type(indexer, section, item_type, type) if item_fav=='false' else item.get('video_type', '')
            
                if indexer == common.indxr_Lists or 'list' in section or item_fav == 'true':
                    if video_type == common.VideoType_Movies:
                        use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies,'metadata_movies') == 'true' else False
                    elif video_type in (common.VideoType_Season, common.VideoType_Episode, common.VideoType_TV):
                        use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows,'metadata_tv_shows') == 'true' else False
                        
                    if use_meta == True and not metaget:
                        from metahandler import metahandlers
                        metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)

                
                if use_meta == True:                                
                    sn = item.get('season', '0')
                    sn = '0' if sn == '' else sn
                    
                    en = item.get('episode', '0')
                    en = '0' if en == '' else en
                    
                    this_meta = get_metadata(metaget, video_type, 
                        item.get('name', '') if video_type in (common.VideoType_Movies, common.VideoType_TV) else item.get('title', ''), 
                        item.get('name', ''), item.get('year', ''), imdb = item.get('imdb_id', None) if (imdb_id == None or imdb_id == '') else imdb_id, 
                        season_num=int(sn), episode_num=int(en))
                
                if not item['title']:
                    if use_meta == True:
                        item['title'] = this_meta['title']
                    else:
                        item['title'] = '-'
                this_meta.update({'title': ( hleveler * int ( item.get('hlevel', '0') ) ) + htmlcleaner.clean(item['title'])})
                                
                meta_img = item.get('img', '') if this_meta.get('cover_url', '') == '' else this_meta.get('cover_url', '')
                meta_fanart = item.get('fanart', '') if this_meta.get('backdrop_url', '') == '' else this_meta.get('backdrop_url', '')
                meta_imdb_id = this_meta.get('imdb_id', '')
                meta_watched = this_meta.get('overlay', 6)
                
                this_meta.update({'plot': item.get('plot', '') if this_meta.get('plot', '' ) == '' else this_meta.get('plot', '' ) })
                
                item_indexer=item.get('indexer', indexer)
                item_indexer_id=item['website'] 
                item_mode=item['mode']
                item_section=item.get('section','')
                item_url=item.get('url', '') 
                item_urls=item.get('urls', '')
                item_title=item.get('item_title', '') if item_fav == 'true' else item.get('title', '')
                item_name=item.get('name', '')
                item_year=item.get('year', '')
                item_season=item.get('season', '')
                item_episode=item.get('episode', '')
                item_meta_img=meta_img
                item_meta_fanart=meta_fanart
                
                if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'sync_watched_status_with_lib') == 'true':
                    xbmclibinfo = get_info_from_xbmc_library(video_type, item_name, item_season, item_episode, item_year, properties=["playcount"])
                    xbmcdbid = xbmclibinfo['xbmcdbid']
                    if xbmcdbid:
                        playcount = xbmclibinfo['playcount']
                        if not playcount:
                            playcount = 0
                        if (meta_watched == 6 and playcount <= 0) or (meta_watched == 7 and playcount > 0):
                            common.addon.log('Watch status is same in iStream and XBMC library.')
                        else:
                            if use_meta == True:
                                metaget.change_watched(video_type, item_name, meta_imdb_id, season=item_season, episode=item_episode, year=item_year)
                                if meta_watched == 6: meta_watched = 7
                                elif meta_watched == 7: meta_watched = 6                            
                                
                            if playcount <= 0: meta_watched = 6
                            elif playcount > 0: meta_watched = 7
                            
                            this_meta['playcount'] = playcount
                
                contextMenuItems = add_contextmenu(video_type, item_indexer, item_indexer_id, item_mode, item_section, 
                        item_url, meta_imdb_id, item_title, item_name, item_year, item_season, item_episode, item_type, 
                        use_meta, item_meta_img, item_meta_fanart, meta_watched, item_fav, trailer=this_meta.get('trailer', ''), urls=item_urls)
                        
                cmi_str = str(contextMenuItems)
                if '[COLOR red]Unsubscribe[/COLOR]' in cmi_str and '[COLOR red]Delete[/COLOR] from Favorites' in cmi_str:
                    this_meta.update({'title':'[B][COLOR gold]|||[/COLOR] [COLOR green]|*|[/COLOR][/B] ' + this_meta['title']})
                elif '[COLOR red]Unsubscribe[/COLOR]' in cmi_str:
                    this_meta.update({'title':'[B][COLOR gold]|||[/COLOR][/B] ' + this_meta['title']})
                elif '[COLOR red]Delete[/COLOR] from Favorites' in cmi_str:
                    this_meta.update({'title':'[B][COLOR green]|*|[/COLOR][/B] ' + this_meta['title']})
                    
                if indexer in (common.indxr_Live_TV):
                    live_title = ':: %s :: [COLOR blue]%s[/COLOR]' % (this_meta['title'], 
                        'ISTREAM' if item.get('indexer', None) == common.indxr_Live_TV else item.get('host', 'ISTREAM') )
                    this_meta.update({'title':live_title})
                    
                trailer = this_meta.get('trailer', '')
                if trailer and 'plugin://plugin.video.youtube/' in trailer:
                    trailer = '%s' % common.addon.build_plugin_url({'mode':common.mode_Play_Trailer, 'url':trailer})
                        
                try:
                    search_queries = {'indexer':item_indexer, 'indexer_id':item_indexer_id, 'source':item_indexer, 'source_id':item_indexer_id, 'mode':item_mode, 'section':item_section, 
                            'title':common.CleanText2(item_title, True, True), 'name':common.CleanText2(item_name, True, True), 'year':item_year, 'season':item_season, 'episode':item_episode, 'favorite':item_fav, 
                            'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'urls':item_urls, 'imdb_id':meta_imdb_id,
                            'other_names':item.get('other_names', ''), 'region':item.get('region', ''), 'language':item.get('language', ''),
                            'genre':item.get('genre', ''), 'trailer':trailer }
                    item_play = item.get('play', None)
                    if item_play:
                        search_queries.update( {'play':item_play} )
                    common.addon.add_directory( search_queries, this_meta, 
                            contextmenu_items=contextMenuItems, context_replace=True, img=meta_img, fanart=meta_fanart, total_items=totalitems)
                except:
                    search_queries = {'indexer':item_indexer, 'indexer_id':item_indexer_id, 'source':item_indexer, 'source_id':item_indexer_id, 'mode':item_mode, 'section':item_section, 
                            'title':urllib.quote_plus(common.CleanText2(item_title, True, True)), 'name':urllib.quote_plus(common.CleanText2(item_name, True, True)), 'year':item_year, 'season':item_season, 'favorite':item_fav, 
                            'episode':item_episode, 'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'urls':item_urls, 'imdb_id':meta_imdb_id,
                            'other_names':item.get('other_names', ''), 'region':item.get('region', ''), 'language':item.get('language', ''),
                            'genre':item.get('genre', ''), 'trailer':trailer }
                    item_play = item.get('play', None)
                    if item_play:
                        search_queries.update( {'play':item_play} )
                    common.addon.add_directory( search_queries, this_meta, 
                            contextmenu_items=contextMenuItems, context_replace=True, img=meta_img, fanart=meta_fanart, total_items=totalitems)

        if next_page_dict:
            common.addon.add_directory(next_page_dict, {'title': '[B][COLOR white]Next Page >[/COLOR][/B]'},
                img=common.get_themed_icon('nextpage.png') ) 
            
        if last_page_dict:
            common.addon.add_directory(last_page_dict, {'title': '[B][COLOR white]Last Page >>[/COLOR][/B]'},
                img=common.get_themed_icon('lastpage.png') ) 
            
        if page=='' and total_pages=='':            
            dialog.update(100)
            dialog.close()
        
        setViewForMode(mode)        
        common.addon.end_of_directory(updateListing = True )

def ResolveAndPlay(source, source_id, url, title, name, year, season, episode, type):

    from universal import playbackengine
    
    global img
    
    autoplaysetting = entertainment.GetiStreamSettings(indexer, 'autoplay')
    autoplay = ( (autoplaysetting == 'true' and autoplay_from_queries == '') or autoplay_from_queries=='true')
    
    if queued or (library == 'true' and not autoplay):
        
        if '|||part|||' in url:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem(title))
            import time
            time.sleep(1)
            xbmc.executebuiltin('Dialog.Close(all,true)')
            time.sleep(1)            
            common.addon.queries.update({'mode':'play', 'play':'true', 'library':'false', 'source':source, 'source_id':source_id})
            if library == 'true' and not autoplay:                
                common.addon.queries.pop("queued", None)
                common.addon.queries.update({'url':url})
                xbmc.executebuiltin('RunPlugin(%s)' % common.addon.build_plugin_url(common.addon.queries))
            else:
                infolabels = {}
        
                if 'tv' in type:
                    infolabels['TVShowTitle'] = name 
                    infolabels['season']= int(season)
                    infolabels['episode']= int(episode)
                    infolabels['title'] = title
                else:
                    infolabels['title'] = name
                
                if not year:
                    year = '0'            
                infolabels['year'] = int(year)
                
                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playlist.clear()
                
                host_urls = url.split('|||part|||')
                for host_url in host_urls:
                    if host_url:        
                        common.addon.queries.update({'url':host_url})
                        playbackengine.AddToPL(title, url=common.addon.build_plugin_url(common.addon.queries), img=img, fanart=fanart, infolabels=infolabels)
                playbackengine.Player().play(playlist)
            return    

        resolved_url = entertainment.ResolveFileHostUrl(source, source_id, url)

        from entertainment import odict
        if isinstance(resolved_url, odict.odict) or isinstance(resolved_url, dict):
            xbmcdlg = xbmcgui.Dialog()
            list_key = []
            list_value = []
            for key, value in resolved_url.items():
                list_key.append(key)
                list_value.append(value)
            ret = xbmcdlg.select('Please select from below', list_key)
            if ret < 0:
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem(title))
                return
            resolved_url = list_value[ret]
        
        if not resolved_url:
            resolved_url = url
        
        if resolved_url != None and isinstance(resolved_url, (str, unicode) ) and resolved_url!='':
        
            is_f4m_format = False
            if '.f4m' in resolved_url.lower(): is_f4m_format=True
            if is_f4m_format==True:
                from f4mproxy import f4mProxyHelper
                f4mHelper=f4mProxyHelper()
                resolved_url,f4mProxyStopEvent = f4mHelper.start_proxy(resolved_url, name)
        
            player = None
            
            if library != 'true':
                '''
                player = playbackengine.Play(resolved_url=resolved_url, addon_id=common.addon_id, video_type=get_video_type('','','',type), 
                                            title=name,season=season, episode=episode, year=year,
                                            watchedCallbackwithParams=WatchedCallbackwithParams,imdb_id=imdb_id)
                '''
                player = playbackengine.Player()
                player.set(addon_id=common.addon_id, video_type=get_video_type('','','',type), title=name, season=season, 
                    episode=episode, year=year, watchedCallbackwithParams=WatchedCallbackwithParams, imdb_id=imdb_id)
                    
                listitem = xbmcgui.ListItem(path=resolved_url)
                
                infolabels = {}       
                if 'tv' in type:
                    infolabels['TVShowTitle'] = name 
                    infolabels['season']= int(season)
                    infolabels['episode']= int(episode)
                    infolabels['title'] = title
                else:
                    infolabels['title'] = name
                
                if not year:
                    year = '0'            
                infolabels['year'] = int(year)
                
                listitem.setInfo("Video", infolabels)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
            else:
            
                playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playlist.clear()
            
                video_type=get_video_type('','','',type)
                
                xbmcdbid = xbmc.getInfoLabel('ListItem.DBID')
                img = xbmc.getInfoImage('ListItem.Thumb')
                if not title or title == 'iStream':
                    title = xbmc.getInfoLabel('ListItem.Title')
                
                if not xbmcdbid:
                    # if xbmcdbid is None, the item is being played from recently added list on home screen
                    # lets search for the item in the library
                    xbmclibinfo = get_info_from_xbmc_library(video_type, name, season, episode, year, properties=["thumbnail", "title"])
                    xbmcdbid = xbmclibinfo['xbmcdbid']
                    img = xbmclibinfo['thumbnail']
                    if not title or title == 'iStream':
                        title = xbmclibinfo['title']
                
                player = playbackengine.Player()                
                player.set(addon_id=common.addon_id, video_type=video_type, title=name, season=season, 
                    episode=episode, year=year, watchedCallbackwithParams=WatchedCallbackwithParams, imdb_id=imdb_id)
                
                listitem = xbmcgui.ListItem(title, iconImage=img, thumbnailImage=img)
                if fanart:
                    listitem.setProperty('fanart_image', fanart)
                    
                infolabels = {}       
                if 'tv' in type:
                    infolabels['TVShowTitle'] = name 
                    infolabels['season']= int(season)
                    infolabels['episode']= int(episode)
                    infolabels['title'] = title
                else:
                    infolabels['title'] = name
                
                if not year:
                    year = '0'            
                infolabels['year'] = int(year)
                
                listitem.setInfo("Video", infolabels)
                
                listitem.setProperty('IsPlayable', 'true')
                listitem.setProperty('DBID', xbmcdbid)
                listitem.setPath(resolved_url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
            if player:
                
                if autoplay:
                    while player._playbackLock.isSet() and player._lastPos == 0:
                        xbmc.sleep(250)
                    if player._playbackLock.isSet() and player._lastPos > 0:
                        global xbmc_auto_play_progress_dialog
                        if xbmc_auto_play_progress_dialog:
                            xbmc_auto_play_progress_dialog.close()                        
                player.KeepAlive()
                if is_f4m_format==True:
                    f4mProxyStopEvent.set()

                if autoplay:                    
                    if player._lastPos == 0 and player._totalTime == 999999:
                        import time
                        time.sleep(1)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        time.sleep(1)
                        raise PlaybackFailed('Playback Failed')
                    elif player._lastPos <= int(entertainment.GetiStreamSettings(indexer, 'autoplay_skip_interval')):
                        autoplay_q = xbmcgui.Dialog()
                        autoplay_q = autoplay_q.yesno("iStream: Auto-play", '', 'Continue auto-play OR stop playing?', '', "Stop Playing", "Continue Auto-play")  # 20132 = Restart Video 13404 = Resume
                        if autoplay_q: raise HostSkipped('Host Skipped')
                
        else:
            if autoplay:
                raise Unresolvable('Unresolvable')
        
    else:
        infolabels = {}
        
        if 'tv' in type:
            infolabels['TVShowTitle'] = name 
            infolabels['season']= int(season)
            infolabels['episode']= int(episode)
            infolabels['title'] = title
        else:
            infolabels['title'] = name
        
        if not year:
            year = '0'            
        infolabels['year'] = int(year)
        
        host_urls = url.split('|||part|||')
        host_urls = filter(bool, host_urls)
        host_count = len(host_urls)
        if len(host_urls) > 1:
        
            playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            playlist.clear()
            
            part=0
            for host_url in host_urls:
                if host_url:        
                    common.addon.queries.update({'url':host_url, 'queued':'true', 'name':infolabels['title'] + '- Part ' + str(part+1) + ' of ' + str(host_count) })
                    playbackengine.AddToPL(title, url=common.addon.build_plugin_url(common.addon.queries), img=img, fanart=fanart, infolabels=infolabels)
                    part+=1
            playbackengine.Player().play(playlist)
                    
        else:
            playbackengine.PlayInPL(title, img=img, fanart=fanart, infolabels=infolabels)
            
def add_item_to_library(item_title, item_path, item_url):
    error = False
    
    if item_path:
        
        import xbmcvfs
        import os
        
        if isinstance( item_path, list ):
            item_list_length = len(item_path)
            item_last_dir = ''
            for index in range(0, item_list_length):
                                    
                i_p = item_path[index]
                i_u = item_url[index]
                
                i_dir = os.path.dirname(i_p)
                if item_last_dir != i_dir:                    
                    item_last_dir = i_dir
                    if not xbmcvfs.exists(i_dir):
                        try:
                            xbmcvfs.mkdirs(i_dir)
                        except Exception, e:
                            common.addon.log('Failed to create directory %s' % i_p)
                        
                try:
                    file_desc = xbmcvfs.File(i_p, 'w')
                    file_desc.write(i_u)
                    file_desc.close()
                except Exception, e:
                    common.addon.log('Failed to create .strm file: %s\n%s' % (item_path, e))
                    error = True                    
        else:
            if not xbmcvfs.exists(os.path.dirname(item_path)):
                try:
                    xbmcvfs.mkdirs(os.path.dirname(item_path))
                except Exception, e:
                    common.addon.log('Failed to create directory %s' % item_path)
            
            try:
                file_desc = xbmcvfs.File(item_path, 'w')
                file_desc.write(item_url)
                file_desc.close()                
            except Exception, e:
                common.addon.log('Failed to create .strm file: %s\n%s' % (item_path, e))
                error = True
    else:
        error = True        
        
    return (item_title, error)

def add_to_library(indexer, indexer_id, url, title, name, year, season, episode, type, video_type, imdb_id):
    lib_path = None
    if video_type == common.VideoType_Movies:
        lib_path = entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'movies_lib_folder')
        if not lib_path:
            lib_path = 'special://profile/addon_data/script.icechannel/Movies'
    elif video_type in (common.VideoType_TV, common.VideoType_Season, common.VideoType_Episode):
        lib_path = entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'tv_shows_lib_folder')
        if not lib_path:
            lib_path = 'special://profile/addon_data/script.icechannel/TVShows'
            
    new_lib_items = []
    
    if lib_path:
    
        import xbmc
        import xbmcvfs
        import os
        import re
        
        common.addon.queries.update({'mode':common.mode_File_Hosts, 'library':'true'})

        lib_path = xbmc.translatePath(lib_path)
        item_title = name
        if video_type == common.VideoType_Movies and year and year != '0': item_title += " (" + year + ")"
        item_dir = re.sub(r'[^\w\-_\. ]', '_', item_title)
        if video_type in (common.VideoType_TV, common.VideoType_Season, common.VideoType_Episode) and year and year != '0': item_title += " (" + year + ")"
        
        item_path = None
        item_url = None
        
        if video_type == common.VideoType_TV:
            if urls and len(common.ConvertStringToDict(urls)) > 1:
                (s_items,message_queue) = entertainment.GetContent (indexer, indexer_id, url, title, name, year, season, episode, type, urls=urls)
                RetrieveAndDisplayMessages(message_queue)
                meta = []
            else:
                (s_items,meta) = entertainment.GetContent (indexer, indexer_id, url, title, name, year, season, episode, type)
            
            update_subs_level = int(entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'update_subs_level'))
            episodes_to_fetch = 5 if update_subs_level == 3 else 10
            episodes_fetched = 0
            
            if mode == common.mode_Update_Subs and s_items and update_subs_level > 0:
                s_items.sort(key=lambda k: int(k['season']), reverse=True)
                if update_subs_level in (1,4):
                    temp_s_items = []
                    temp_s_items.append(s_items[0])
                    s_items = temp_s_items
            
            episode_item_paths = []
            episode_item_urls = []
            
            for s_item in s_items:
                s_item_indexer=s_item['indexer']
                s_item_indexer_id=s_item['website'] 
                s_item_url=s_item.get('url', '') 
                s_item_title=s_item.get('title', '')
                s_item_name=s_item.get('name', '')
                s_item_year=s_item.get('year', '')
                s_item_season=s_item.get('season', '')
                s_item_episode=s_item.get('episode', '')
                s_item_type=s_item.get('type', '')
                s_item_urls=s_item.get('urls', '')
                
                season_dir = 'Season ' + s_item_season
                
                if s_item_urls and len(common.ConvertStringToDict(s_item_urls)) > 1:
                    (items,message_queue) = entertainment.GetContent (s_item_indexer, s_item_indexer_id, s_item_url, s_item_title, 
                                        s_item_name, s_item_year, s_item_season, s_item_episode, s_item_type, urls=s_item_urls)
                    RetrieveAndDisplayMessages(message_queue)
                    meta = []
                else:
                    (items,meta) = entertainment.GetContent (s_item_indexer, s_item_indexer_id, s_item_url, s_item_title, 
                                        s_item_name, s_item_year, s_item_season, s_item_episode, s_item_type)
                                    
                if mode == common.mode_Update_Subs and items and update_subs_level > 1:
                    items.sort(key=lambda k: int(k['episode']), reverse=True)
                    if update_subs_level == 4:
                        temp_items = []
                        temp_items.append(items[0])
                        items = temp_items
                                    
                for item in items:
                    item_indexer=item['indexer']
                    item_section=item.get('section','')
                    e_item_title=item.get('title', '')
                    item_name=item.get('name', '')
                    item_year=item.get('year', '')
                    item_season=item.get('season', '')
                    item_episode=item.get('episode', '')
                    item_type=item.get('type', '')
                    
                    filename = '%s S%sE%s.strm' % (item_dir, item_season, item_episode)
                    
                    episode_item_path = os.path.join(lib_path, item_dir, season_dir, filename)
                    
                    try:
                        episode_item_queries = {'indexer':item_indexer, 'mode':common.mode_File_Hosts, 'section':item_section, 'title':e_item_title, 
                                'name':item_name, 'year':item_year, 'season':item_season, 'episode':item_episode, 'type':item_type, 'imdb_id': imdb_id,
                                'video_type':common.VideoType_Episode, 'library':'true'}
                        episode_item_url = common.addon.build_plugin_url(episode_item_queries)
                    except:
                        episode_item_queries = {'indexer':item_indexer, 'mode':common.mode_File_Hosts, 'section':item_section, 'title':urllib.quote_plus(e_item_title), 
                                'name':urllib.quote_plus(item_name), 'year':item_year, 'season':item_season, 'episode':item_episode, 'type':item_type, 'imdb_id': imdb_id,
                                'video_type':common.VideoType_Episode, 'library':'true'}
                        episode_item_url = common.addon.build_plugin_url(episode_item_queries)
                        
                    xbmclibinfo = get_info_from_xbmc_library(common.VideoType_Episode, item_name, item_season, item_episode, item_year)
                    if not xbmclibinfo['xbmcdbid']:
                        new_lib_items.append({'video_type' : common.VideoType_Episode, 'name' : item_name, 'season' : item_season, 'episode' : item_episode, 'year' : item_year, 'imdb_id': imdb_id})
                        
                    episode_item_paths.append(episode_item_path)
                    episode_item_urls.append(episode_item_url)
                    
                    episodes_fetched += 1
                    if mode == common.mode_Update_Subs and update_subs_level in (2,3) and episodes_fetched == episodes_to_fetch: break
                    
                if mode == common.mode_Update_Subs and update_subs_level in (2,3) and episodes_fetched == episodes_to_fetch: break
                                                
            if len(episode_item_paths) > 0:
                item_path = episode_item_paths
                item_url = episode_item_urls
                
            
        
        elif video_type == common.VideoType_Season:
            item_title = item_title + ' - Season: ' + season
            season_dir = 'Season ' + season
            
            if urls and len(common.ConvertStringToDict(urls)) > 1:
                (items,message_queue) = entertainment.GetContent (indexer, indexer_id, url, title, name, year, season, episode, type, urls=urls)
                RetrieveAndDisplayMessages(message_queue)
                meta = []
            else:
                (items,meta) = entertainment.GetContent (indexer, indexer_id, url, title, name, year, season, episode, type)
            
            episode_item_paths = []
            episode_item_urls = []
            
            for item in items:
                            
                item_indexer=item['indexer']
                item_section=item.get('section','')
                e_item_title=item.get('title', '')
                item_name=item.get('name', '')
                item_year=item.get('year', '')
                item_season=item.get('season', '')
                item_episode=item.get('episode', '')
                item_type=item.get('type', '')
                
                filename = '%s S%sE%s.strm' % (item_dir, item_season, item_episode)
                
                episode_item_path = os.path.join(lib_path, item_dir, season_dir, filename)
                
                try:
                    episode_item_queries = {'indexer':item_indexer, 'mode':common.mode_File_Hosts, 'section':item_section, 'title':e_item_title, 
                            'name':item_name, 'year':item_year, 'season':item_season, 'episode':item_episode, 'type':item_type, 'imdb_id': imdb_id,
                            'video_type':common.VideoType_Episode, 'library':'true'}
                    episode_item_url = common.addon.build_plugin_url(episode_item_queries)
                except:
                    episode_item_queries = {'indexer':item_indexer, 'mode':common.mode_File_Hosts, 'section':item_section, 'title':urllib.quote_plus(e_item_title), 
                            'name':urllib.quote_plus(item_name), 'year':item_year, 'season':item_season, 'episode':item_episode, 'type':item_type, 'imdb_id': imdb_id,
                            'video_type':common.VideoType_Episode, 'library':'true'}
                    episode_item_url = common.addon.build_plugin_url(episode_item_queries)
                    
                xbmclibinfo = get_info_from_xbmc_library(common.VideoType_Episode, item_name, item_season, item_episode, item_year)
                if not xbmclibinfo['xbmcdbid']:
                    new_lib_items.append({'video_type' : common.VideoType_Episode, 'name' : item_name, 'season' : item_season, 'episode' : item_episode, 'year' : item_year, 'imdb_id': imdb_id})
                    
                episode_item_paths.append(episode_item_path)
                episode_item_urls.append(episode_item_url)
            
            if len(episode_item_paths) > 0:
                item_path = episode_item_paths
                item_url = episode_item_urls
            
        elif video_type == common.VideoType_Episode:

            item_title = item_title + ' - S' + season + 'E' + episode + ' - ' + title
            season_dir = 'Season ' + season
            filename = '%s S%sE%s.strm' % (item_dir, season, episode)
            item_path = os.path.join(lib_path, item_dir, season_dir, filename)

            item_url = common.addon.build_plugin_url(common.addon.queries)
            xbmclibinfo = get_info_from_xbmc_library(video_type, name, season, episode, year)
            if not xbmclibinfo['xbmcdbid']:
                new_lib_items.append({'video_type' : video_type, 'name' : name, 'season' : season, 'episode' : episode, 'year' : year, 'imdb_id': imdb_id})
        elif video_type == common.VideoType_Movies:
            filename = '%s.strm' % item_dir
            item_path = os.path.join(lib_path, item_dir, filename)
            item_path = xbmc.makeLegalFilename(item_path)
            item_url = common.addon.build_plugin_url(common.addon.queries)        
            xbmclibinfo = get_info_from_xbmc_library(video_type, name, season, episode, year)
            if not xbmclibinfo['xbmcdbid']:
                new_lib_items.append({'video_type' : video_type, 'name' : name, 'season' : season, 'episode' : episode, 'year' : year, 'imdb_id': imdb_id})
    
    (item_title, error) = add_item_to_library( item_title, item_path, item_url)
    
    return (item_title, error, new_lib_items)
    
def FIRST_RUN():
    from istreams.dialogs import DialogiStreamTerms
    DialogiStreamTerms.show()



def ISTREAM_SETUP():
    import xbmc
    import os
    #if os.path.exists(xbmc.translatePath(os.path.join('special://home/addons','repository.xunity.tv')))==False:
    if os.path.exists(xbmc.translatePath(os.path.join('special://xbmc/addons','repository.xunity.tv')))==False:
        common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR orange][B]iStream Extensions Installer[/B][/COLOR]'  })
        common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':' '  })
        common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'This feature is only available on [B]Xunity Products[/B].'  })
        common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'Please visit [COLOR gold][B]http://www.xunity.tv/[/B][/COLOR] for more details.'  })
    else:
    
        from istreams.dialogs import DialogiStreamDisclaimer
        ACTION = DialogiStreamDisclaimer.show()
        
        if ACTION == DialogiStreamDisclaimer.extn_act_OK:
        
            pDialog = xbmcgui.DialogProgress()
            ret = pDialog.create("iStream Extensions Store", "Searching for extensions... ", " ", " " )
            pDialog.update(0)

            # get window progress
            WINDOW_PROGRESS = xbmcgui.Window( 10101 )
            # give window time to initialize
            xbmc.sleep( 100 )
            try:
                # get our cancel button    
                CANCEL_BUTTON = WINDOW_PROGRESS.getControl( 10 )
                # desable button (bool - True=enabled / False=disabled.)
                CANCEL_BUTTON.setEnabled( False )
            except:
                pass
                
            pDialog.update( 10, 'Searching for extensions... ', 
                '[B]Searching: [COLOR gold]Xunity TV (xunity.tv)[/COLOR][/B]', 
                'Found %s extensions' % 0 )
            
            (items1, message_queue) = entertainment.LoadExtensionStore ()
            RetrieveAndDisplayMessages(message_queue)
            
            pDialog.update( 15, 'Searching for extensions... ', 
                '[B]Searching: [COLOR gold]Xunity TV (xunity.tv)[/COLOR][/B]', 
                'Found %s extensions' % str(len(items1) - 1 ) )
                        
            xbmc.sleep(1000) 
        
            (items2, message_queue) = entertainment.SearchForExtensions ()
            RetrieveAndDisplayMessages(message_queue, pDialog)
            
            pDialog.update( 100, 'Searching for extensions... ', 
                '[B][COLOR gold]Retrieving Extensions from source(s)[/COLOR][/B]', 
                'Found %s extensions' % str(len(items1) - 1 + len(items2) - 1) )

            import xbmc
            xbmc.sleep(1000)        
        
            #item_query_dict = {'istream_path':istream_path + ' : ' + 'Search for Third Party extensions...', 'mode' : 'THIRD-PARTY-EXTN-SEARCH'}
            #istream_query_dict = {'istream_path':istream_path + ' : ' + 'Search for Third Party extensions...', 'mode':common.mode_Add_to_MyStream, 'item_mode' : 'THIRD-PARTY-EXTN-SEARCH'}
            #contextMenuItems = []
            #contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
            #common.addon.add_directory(item_query_dict, {'title':'[COLOR green][I]Click Here For iStream Extension Part 2...[/COLOR][/I]'  }, contextmenu_items=contextMenuItems )
            #common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':' '  })
            
            #common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR orange][B]Official Xunity TV Extensions[/B][/COLOR]'  })
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR orange][I](Click on the extensions below to install)[/I][/COLOR]'  })
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':' '  })
            LIST=[]
            for extn in items1:
                #extn_id = extn['extn_id']
                #extn_version = extn['extn_version']
                extn_name = extn['extn_name']
                #extn_provider = extn['extn_provider']
                #extn_zip = extn['extn_zip']
                extn_icon = extn['extn_icon']
                extn_fanart = extn['extn_fanart']
                #extn_summary = extn['extn_summary']
                #extn_desc = extn['extn_desc']
                #extn_repo_id = extn['extn_repo_id']
                #extn_repo_version = extn['extn_repo_version']
                #extn_repo_zip = extn['extn_repo_zip']
                extn.update({'mode' : 'OFFICIAL-EXTN'})
                LIST.append([extn_name, extn_name+' [COLOR yellow]   -   OFFICIAL[/COLOR]',extn_icon,extn_fanart, extn, 'RunPlugin(%s)' % common.addon.build_plugin_url(extn)])
                #common.addon.add_directory(extn, {'title':extn_name  }, img=extn_icon, fanart=extn_fanart, 
                    #contextmenu_items=[ ('Information','RunPlugin(%s)' % common.addon.build_plugin_url(extn)) ], 
                    #context_replace=True)
                    
    
        
            #common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':' '  })
           # common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':' '  })
           # common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR orange][B]Third Party Extensions[/B][/COLOR]'  })
            #common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR orange][I](Click on the extensions below to install)[/I][/COLOR]'  })
            #common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':' '  })
            
            for extn in items2:
                if extn.get('extn_id', None) == None: continue
                extn_name = extn['extn_name']
                extn_icon = extn['extn_icon']
                extn_fanart = extn['extn_fanart']            
                extn.update({'mode' : extn.get('mode', 'OFFICIAL-EXTN')})
                LIST.append([extn_name, extn_name+' [COLOR orange]   -   THIRD PARTY[/COLOR]',extn_icon,extn_fanart, extn, 'RunPlugin(%s)' % common.addon.build_plugin_url(extn)])
            
            LIST.sort(key=lambda k:k[0].lower())
            
            for name, title , icon , fanart, extn, url in LIST:    
                common.addon.add_directory(extn, {'title':title  }, img=icon, fanart=fanart, 
                    contextmenu_items=[ ('Information',url) ], 
                    context_replace=True)
        
        common.addon.end_of_directory()
        
        try:
            # enable button
            CANCEL_BUTTON.setEnabled( True )
        except:
            pass
        
        pDialog.close()
                
    
 
call_from_skin = common.addon.queries.get('skin', '')
global preloaded
preloaded  = False
if call_from_skin == "true":
    xbmc.executebuiltin('Skin.SetBool(istreamfirstinstall)')
    PreLoadiStreamPlugins(False)
    
    
       
if mode == 'OFFICIAL-EXTN':
    from istreams.dialogs import DialogiStreamExtnInfo
    ACTION = DialogiStreamExtnInfo.show( common.addon.queries )
    if ACTION != DialogiStreamExtnInfo.extn_act_NONE:
        from entertainment import extninstaller
        if ACTION in (DialogiStreamExtnInfo.extn_act_INSTALL, DialogiStreamExtnInfo.extn_act_UPDATE):
            extninstaller.Install(common.addon.queries)
        elif ACTION == DialogiStreamExtnInfo.extn_act_UNINSTALL:
            extninstaller.UnInstall(common.addon.queries)
elif mode == 'THIRD-PARTY-EXTN-SEARCH':
    
    from istreams.dialogs import DialogiStreamDisclaimer
    ACTION = DialogiStreamDisclaimer.show()
    
    pDialog = None
    
    if ACTION == DialogiStreamDisclaimer.extn_act_OK:
    
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create("iStream Extensions Store", "Searching for third party extensions... ", " ", " " )
        pDialog.update(0)

        # get window progress
        WINDOW_PROGRESS = xbmcgui.Window( 10101 )
        # give window time to initialize
        xbmc.sleep( 100 )
        try:
            # get our cancel button    
            CANCEL_BUTTON = WINDOW_PROGRESS.getControl( 10 )
            # desable button (bool - True=enabled / False=disabled.)
            CANCEL_BUTTON.setEnabled( False )
        except:
            pass
    
        (items, message_queue) = entertainment.SearchForExtensions ()
        RetrieveAndDisplayMessages(message_queue, pDialog)
        
        pDialog.update( 100, 'Searching for third party extensions... ', 
            '[B][COLOR gold]Retrieving Extensions from source(s)[/COLOR][/B]', 
            'Found %s extensions' % str(len(items) - 1) )

        import xbmc
        xbmc.sleep(1000)
        
        if items[0].get('mode', 'None') == 'FEATURE_NOT_SUPPORTED':
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR orange][B]iStream Extensions Installer[/B][/COLOR]'  })
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':' '  })
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'This feature is only available on [B]Xunity Eclipse[/B].'  })
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'Please visit [COLOR gold][B]http://www.xunity.tv/[/B][/COLOR] for more details.'  })
        else:
        
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR orange][B]Third Party Extensions[/B][/COLOR]'  })
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':'[COLOR gray][I](Click on the extensions below to install)[/I][/COLOR]'  })
            common.addon.add_directory({'mode' : 'DUMMY-DIR'}, {'title':' '  })
            
            for extn in items:
                if extn.get('extn_id', None) == None: continue
                extn_name = extn['extn_name']
                extn_icon = extn['extn_icon']
                extn_fanart = extn['extn_fanart']            
                extn.update({'mode' : extn.get('mode', 'OFFICIAL-EXTN')})
                common.addon.add_directory(extn, {'title':extn_name  }, img=extn_icon, fanart=extn_fanart, 
                    contextmenu_items=[ ('Information','RunPlugin(%s)' % common.addon.build_plugin_url(extn)) ], 
                    context_replace=True)
        
        common.addon.end_of_directory()
        
        try:
            # enable button
            CANCEL_BUTTON.setEnabled( True )
        except:
            pass
        
        if pDialog:
            pDialog.close()

entertainment.loadiStreamPlugins()

if common.addon.get_setting('istream_first_run') == "true":
    FIRST_RUN()
    if common.addon.get_setting('istream_first_run') == "false":
        ISTREAM_SETUP()
    else:
        common.addon.end_of_directory()

else:
    if play:    
        if indexer and indexer in ('file_stores'):
            entertainment.loadiStreamPlugins(type=indexer, load_resolvers=True, load_settings=True, load_webproxyproviders=True)
            resolved_url = entertainment.ResolveUrl(url)        
            if not resolved_url:
                resolved_url = url
            is_f4m_format = False
            if '.f4m' in resolved_url.lower(): is_f4m_format=True
            if is_f4m_format==True:
                from f4mproxy import f4mProxyHelper            
                f4mHelper=f4mProxyHelper()
                resolved_url,f4mProxyStopEvent = f4mHelper.start_proxy(resolved_url, title)
            listitem = xbmcgui.ListItem(path=resolved_url, iconImage=img, thumbnailImage=img)
            if fanart:
                listitem.setProperty('fanart_image', fanart)
            if title:
                listitem.setInfo("Video", {'title':title})
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
            if is_f4m_format==True:
                import xbmc
                xbmc.sleep(5000)
                player=xbmc.Player()
                while player.isPlaying():
                    print 'XBMC playing...sleep 250ms'
                    xbmc.sleep(250)
                f4mProxyStopEvent.set()
        else:
            if queued or library == 'true':
                entertainment.loadiStreamPlugins(type=source, load_source=True, load_resolvers=True, load_settings=True, load_webproxyproviders=True)
            else:
                entertainment.loadiStreamPlugins(load_settings=True)        
            ResolveAndPlay(source, source_id, url, title, name, year, season, episode, type)

    if mode == common.mode_Play_Trailer:
        xbmc.Player().play(url)
    elif mode == common.mode_Main:    
            GetMainSection()
    elif mode == common.mode_Indexer:
        GetIndexers(indexer)
    elif mode == common.mode_Section:
        entertainment.loadiStreamPlugins(type=indexer, load_indexer=True, load_settings=True, load_webproxyproviders=True )
        if ui_item_mode == 'gotopage':
            xbmcdlg = xbmcgui.Dialog()
            ret = xbmcdlg.numeric(0, 'Goto Page', page)
            if ret != 'cancelled':
                ret_num = int(ret)
                if (ret_num > 0 and ret_num != int(page) and ret_num <= int(total_pages)):
                    page = str(ret_num)
                    GetSection(indexer, indexer_id, section, url, type, page, total_pages, sort_by, sort_order)
        elif ui_item_mode == 'sortby':
            xbmcdlg = xbmcgui.Dialog()
            list_key = []
            list_value = []
            sort_by_options = entertainment.GetSortByOptions(indexer, indexer_id)
            for key, value in sort_by_options.items():
                list_key.append(key)
                list_value.append(value)
            ret = xbmcdlg.select('Sort By', list_value)
            sort_by = list_key[ret]
            GetSection(indexer, indexer_id, section, url, type, page, total_pages, sort_by, sort_order)
        elif ui_item_mode == 'sortorder':
            xbmcdlg = xbmcgui.Dialog()
            list_key = []
            list_value = []
            sort_order_options = entertainment.GetSortOrderOptions(indexer, indexer_id)
            for key, value in sort_order_options.items():
                list_key.append(key)
                list_value.append(value)
            ret = xbmcdlg.select('Sort Order', list_value)
            sort_order = list_key[ret]
            GetSection(indexer, indexer_id, section, url, type, page, total_pages, sort_by, sort_order)    
        else:    
            GetSection(indexer, indexer_id, section, url, type, page, total_pages, sort_by, sort_order)
    elif mode == common.mode_Content:
        GetContent(indexer, indexer_id, url, title, name, year, season, episode, type)
    elif mode == common.mode_File_Hosts:
        GetFileHosts(indexer, indexer_id, url, title, name, year, season, episode, type, urls)
    elif mode == common.mode_Search:
        if ui_item_mode == 'gotopage':
            xbmcdlg = xbmcgui.Dialog()
            ret = xbmcdlg.numeric(0, 'Goto Page', page)
            if ret != 'cancelled':
                ret_num = int(ret)
                if (ret_num > 0 and ret_num != int(page) and ret_num <= int(total_pages)):
                    page = str(ret_num)
        Search(indexer, indexer, page, total_pages, search_term, individual_total_pages)
    elif mode == common.mode_Settings:    
        Settings(settings_section)
    elif mode == common.mode_Sports:
        GetSportsContent(indexer, indexer_id, title)
    elif mode == common.mode_Live_TV:
        GetLiveTVContent(indexer, indexer_id, title)
    elif mode == common.mode_Hide_Channel:
        entertainment.loadiStreamPlugins(load_settingsxml=False, type=common.settings_Live_TV, load_indexer=True, load_source=True, load_settings=True)
        entertainment.SetiStreamSettings(indexer, indexer + '_' + indexer_id + '_indexer_enabled', 'false')
        xbmc.executebuiltin("Container.Refresh")
    elif mode == common.mode_Live_TV_Regions:
        items = entertainment.GetLiveTVRegions( )
        for item in items:
            item_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':indexer, 'indexer_id':item['indexer_id'], 'mode':common.mode_Live_TV_Region}
            istream_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':indexer, 'indexer_id':item['indexer_id'], 'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Live_TV_Region}
            contextMenuItems = []
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
            common.addon.add_directory(item_query_dict ,{'title': item['title']}, img=item.get('img', ''), fanart=item.get('fanart', ''), contextmenu_items=contextMenuItems )
        setViewForMode(mode)
        common.addon.end_of_directory()    
    elif mode == common.mode_Live_TV_Region:
        items = entertainment.GetLiveTVForRegion( indexer_id )
        for item in items:
            item_img = item.get('img', img)
            if not item_img: item_img = img
            item_fanart = item.get('fanart', fanart)
            if not item_fanart: item_fanart = fanart        
            contextMenuItems = add_contextmenu(None, item['indexer'], item['indexer_id'], item['mode'], item['section'], '', '', item['title'], item['title'], '', 
                    '', '', '', '', item.get('img', ''), item.get('fanart', ''), '', 'false', '')
            display_title = item['title']
            if '[COLOR red]Delete[/COLOR] from Favorites' in str(contextMenuItems):
                display_title  = '[B][COLOR green]|*|[/COLOR][/B] ' + item['title']
            common.addon.add_directory({'indexer':indexer, 'indexer_id':item['indexer_id'], 'mode':item['mode'], 'section':item['section'],
                'region':indexer_id, 'title':item['title'], 'img':item['img'], 'fanart':item['fanart'], 'other_names':item.get('other_names','')},
                {'title': display_title}, img=item_img, fanart=item_fanart,contextmenu_items=contextMenuItems, context_replace=True )
        setViewForMode(mode)
        common.addon.end_of_directory()
    elif mode == common.mode_Live_TV_Languages:
        items = entertainment.GetLiveTVLanguages( )
        for item in items:
            item_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':indexer, 'indexer_id':item['indexer_id'], 'mode':common.mode_Live_TV_Language}
            istream_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':indexer, 'indexer_id':item['indexer_id'], 'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Live_TV_Language}
            contextMenuItems = []
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
            common.addon.add_directory(item_query_dict, {'title': item['title']}, img=item.get('img', ''), fanart=item.get('fanart', ''), contextmenu_items=contextMenuItems )
        setViewForMode(mode)
        common.addon.end_of_directory()    
    elif mode == common.mode_Live_TV_Language:
        items = entertainment.GetLiveTVForLanguage( indexer_id )
        for item in items:
            contextMenuItems = add_contextmenu(None, item['indexer'], item['indexer_id'], item['mode'], item['section'], '', '', item['title'], item['title'], '', 
                    '', '', '', '', item.get('img', ''), item.get('fanart', ''), '', 'false', '')
            display_title = item['title']
            if '[COLOR red]Delete[/COLOR] from Favorites' in str(contextMenuItems):
                display_title  = '[B][COLOR green]|*|[/COLOR][/B] ' + item['title']
            common.addon.add_directory({'indexer':indexer, 'indexer_id':item['indexer_id'], 'mode':item['mode'], 'section':item['section'],
                'language':indexer_id, 'title':item['title'], 'img':item['img'], 'fanart':item['fanart'], 'other_names':item.get('other_names','')},
                {'title': display_title}, img=item.get('img', ''), fanart=item.get('fanart', ''),contextmenu_items=contextMenuItems, context_replace=True )
        setViewForMode(mode)
        common.addon.end_of_directory()    
    elif mode == common.mode_Live_TV_Genres:
        items = entertainment.GetLiveTVGenres( )
        for item in items:
            item_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':indexer, 'indexer_id':item['indexer_id'], 'mode':common.mode_Live_TV_Genre}
            istream_query_dict = {'istream_path':istream_path + ' : ' + item['title'], 'indexer':indexer, 'indexer_id':item['indexer_id'], 'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Live_TV_Genre}
            contextMenuItems = []
            contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
            common.addon.add_directory(item_query_dict,{'title': item['title']}, img=item.get('img', ''), fanart=item.get('fanart', ''), contextmenu_items=contextMenuItems )
        setViewForMode(mode)
        common.addon.end_of_directory()    
    elif mode == common.mode_Live_TV_Genre:
        items = entertainment.GetLiveTVForGenre( indexer_id )
        for item in items:
            common.addon.add_directory({'indexer':indexer, 'indexer_id':item['indexer_id'], 'mode':item['mode'], 
                'section':item['section'], 'title':item['title'], 'img':item['img'], 'fanart':item['fanart'], 'other_names':item.get('other_names','')},
                {'title': item['title']}, img=item.get('img', ''), fanart=item.get('fanart', '') )
        setViewForMode(mode)
        common.addon.end_of_directory()    
        
    elif mode == common.mode_Change_Watched:
        entertainment.loadiStreamPlugins(load_settings=True)
        from metahandler import metahandlers
        metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
        metaget.change_watched(type, name, imdb_id, season=season, episode=episode, year=year)

        if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'sync_watched_status_with_lib') == 'true':
            change_watched_in_xbmc_library(type, name, season, episode, year, watched = ( watch_status == 6) )
        xbmc.executebuiltin("Container.Refresh")
    elif mode == common.mode_Refresh_Meta:
        from metahandler import metahandlers
        metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
        
        if type in (common.VideoType_Movies, common.VideoType_TV):        
            search_title = name
            search_meta = None
                
            if type == common.VideoType_Movies:
                search_meta = metaget.search_movies(search_title)
            elif type == common.VideoType_TV:
                api = metahandlers.TheTVDB()
                results = api.get_matching_shows(search_title)
                search_meta = []
                for item in results:
                    option = {'tmdb_id': item[0], 'title': item[1], 'imdb_id': item[2], 'year': year}
                    search_meta.append(option)
                    
            if search_meta and len(search_meta) > 0:
                selection_list = []
                for item in search_meta:
                    selection_list.append(item['title'] + ' (' + str(item['year']) + ')')
                dialog = xbmcgui.Dialog()
                index = dialog.select('Choose', selection_list)
                
                if index > -1:                
                    new_imdb_id = search_meta[index]['imdb_id']
                    new_tmdb_id = search_meta[index]['tmdb_id']
                    meta = metaget.update_meta(type, name, imdb_id=imdb_id, new_imdb_id=new_imdb_id, new_tmdb_id=new_tmdb_id, year=year)   
                    xbmc.executebuiltin("Container.Refresh")
                    
            else:
                msg = ['No matches found']
                common.addon.show_ok_dialog(msg, 'Refresh Results')
                
        elif type == common.VideoType_Season:
            metaget.update_season(name, imdb_id, season)
            xbmc.executebuiltin("Container.Refresh")
        elif type == common.VideoType_Episode:
            metaget.update_episode_meta(name, imdb_id, season, episode)        
            xbmc.executebuiltin("Container.Refresh")
    elif mode == common.mode_Add_To_Favorites:
        
        entertainment.loadiStreamPlugins()
        
        common.addon.queries.update({'mode':common.addon.queries['item_mode'], 'supports_meta':common.addon.queries['fav_supports_meta'],
            'video_type':common.addon.queries['fav_video_type']})
            
        if not favs:
            from universal import favorites
            favs = favorites.Favorites(common.addon_id, sys.argv)
        common.addon.queries.update({'item_title' : title})
        fav_url = favs.build_url(common.addon.queries)
        script = favs.add_directory(common.addon.queries['fav_title'], fav_url, section_title=common.addon.queries['fav_section_title'],
            sub_section_title=common.addon.queries.get('fav_subsection_title', ''), infolabels=common.addon.queries)
        xbmc.executebuiltin(script)    
        xbmc.executebuiltin("Container.Refresh")
            
    elif mode == common.mode_Add_To_Library:
        
        entertainment.loadiStreamPlugins(type=indexer, load_indexer=True, load_source=True, load_settings=True)
        
        if xbmc.getCondVisibility('Library.IsScanningVideo')  or common.GetGlobalProperty(common.gb_Lib_Subs_Op_Running) == 'true':
            common.addon.log('Similar operation already running.')
            common.addon.show_ok_dialog(['Library scan or subscription update in progress.', 'Please wait for it to complete.'])
        else:        
            common.SetGlobalProperty(common.gb_Lib_Subs_Op_Running, 'true')

            tn = common.Threaded_Notification(1000, 'Adding to library', common.addon.queries['item_title'])
            (item_title, error, new_items) = add_to_library(indexer, indexer_id, url, title, name, year, season, episode, type, video_type, imdb_id)        
            if error == False and entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'update_lib_after_add') == 'true':
                xbmc.executebuiltin('UpdateLibrary(video)')
                
                use_meta = False
                if video_type == common.VideoType_Movies:
                    use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
                elif video_type in (common.VideoType_TV, common.VideoType_Season, common.VideoType_Episode):
                    use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
                
                if len(new_items) > 0 and entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'sync_watched_status_with_lib') == 'true' and use_meta == True:
                    
                    xbmc.sleep(250)
                    while ( xbmc.getCondVisibility('Library.IsScanningVideo') ):
                        xbmc.sleep(250)
                        
                    from metahandler import metahandlers
                    metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
                    
                    for new_item in new_items:
                    
                        new_item_imdb_id = new_item['imdb_id']
                        new_item_video_type = new_item['video_type']
                        new_item_name = new_item['name']
                        new_item_season = new_item['season']
                        new_item_episode = new_item['episode']
                        new_item_year = new_item['year']

                        xbmclibinfo = get_info_from_xbmc_library(new_item_video_type, new_item_name, new_item_season, new_item_episode, new_item_year, 
                            properties=["imdbnumber"], toplevel=True)
                            
                        if not new_item_imdb_id:
                            new_item_imdb_id = xbmclibinfo['imdbnumber']
                        
                        meta_watched = 6
                        if new_item_video_type == common.VideoType_Episode:
                            meta_watched = metaget._get_watched_episode({'imdb_id' : new_item_imdb_id, 'title':new_item_name, 'season':new_item_season, 
                                'episode':new_item_episode, 'premiered':'', 'tvdb_id':''})
                            if meta_watched == 7: 
                                xbmclibinfo = get_info_from_xbmc_library(new_item_video_type, new_item_name, new_item_season, new_item_episode, new_item_year)
                        elif new_item['video_type'] == common.VideoType_Movies:
                            meta_watched = metaget._get_watched(common.VideoType_Movies, new_item_imdb_id, '')
                            
                        if meta_watched == 7: mark_as_watched_in_xbmc_library(new_item_video_type, xbmclibinfo['xbmcdbid'])
                        
            tn.SetTaskCompletion()
            common.notify(common.addon_id, 'small', '[B]' + common.addon.queries['item_title'] + '[/B]', 
                '[B]Unable to add to Library.[/B]' if error == True else '[B]Added to Library.[/B]' , '5000')
                
            common.ClearGlobalProperty(common.gb_Lib_Subs_Op_Running)

    elif mode == common.mode_Subscribe:
        
        entertainment.loadiStreamPlugins(type=common.settings_TV_Shows, load_indexer=True, load_source=True, load_settings=True)
        
        if xbmc.getCondVisibility('Library.IsScanningVideo')  or common.GetGlobalProperty(common.gb_Lib_Subs_Op_Running) == 'true':
            common.addon.log('Similar operation already running.')
            common.addon.show_ok_dialog(['Library scan or subscription update in progress.', 
                'Please wait for it to complete.'])
        else:        
            common.SetGlobalProperty(common.gb_Lib_Subs_Op_Running, 'true')
            
            if not subs:
                from entertainment import subscriptions
                subs = subscriptions.Subscriptions()
                
            if subs.is_subscribed(indexer, indexer_id, type, video_type, name, year, url, title, imdb_id) == True:
                common.notify(common.addon_id, 'small', '[B]' + title + '[/B]', '[B]Already subscribed.[/B]' , '5000')
            else:
                
                tn = common.Threaded_Notification(1000, 'Subscribing', title)
                            
                if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'add_to_lib_when_sub') == 'true':
                    (title, error, new_items) = add_to_library(indexer, indexer_id, url, title, name, year, season, episode, type, video_type, imdb_id)        
                else:
                    error = True
                    new_items = []
                
                subscribe_result = True
                if urls and len(common.ConvertStringToDict(urls)) > 1:
                    for url_key, url_value in common.ConvertStringToDict(urls).items():
                        if subs.add_subscription(indexer, url_key, type, video_type, name, year, url_value, title, imdb_id) == False:
                            subscribe_result = False
                else:
                    subscribe_result = subs.add_subscription(indexer, indexer_id, type, video_type, name, year, url, title, imdb_id)
                
                if subscribe_result == False:
                    
                    if error == False and entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'update_lib_after_sub') == 'true':
                        xbmc.executebuiltin('UpdateLibrary(video)')
                        
                        use_meta = False
                        if video_type == common.VideoType_Movies:
                            use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
                        elif video_type in (common.VideoType_TV, common.VideoType_Season, common.VideoType_Episode):
                            use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
                        
                        if len(new_items) > 0 and entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'sync_watched_status_with_lib') == 'true' and use_meta == True:
                    
                            xbmc.sleep(250)
                            while ( xbmc.getCondVisibility('Library.IsScanningVideo') ):
                                xbmc.sleep(250)
                                
                            from metahandler import metahandlers
                            metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
                            
                            for new_item in new_items:
                            
                                new_item_imdb_id = new_item['imdb_id']
                                new_item_video_type = new_item['video_type']
                                new_item_name = new_item['name']
                                new_item_season = new_item['season']
                                new_item_episode = new_item['episode']
                                new_item_year = new_item['year']
                            
                                xbmclibinfo = get_info_from_xbmc_library(new_item_video_type, new_item_name, new_item_season, new_item_episode, new_item_year, 
                                    properties=["imdbnumber"], toplevel=True)
                                    
                                if not new_item_imdb_id:
                                    new_item_imdb_id = xbmclibinfo['imdbnumber']
                                
                                meta_watched = 6
                                if new_item_video_type == common.VideoType_Episode:
                                    meta_watched = metaget._get_watched_episode({'imdb_id' : new_item_imdb_id, 'title':new_item_name, 'season':new_item_season, 
                                        'episode':new_item_episode, 'premiered':'', 'tvdb_id':''})
                                    if meta_watched == 7: 
                                        xbmclibinfo = get_info_from_xbmc_library(new_item_video_type, new_item_name, new_item_season, new_item_episode, new_item_year)
                                elif new_item['video_type'] == common.VideoType_Movies:
                                    meta_watched = metaget._get_watched(common.VideoType_Movies, new_item_imdb_id, '')
                                    
                                if meta_watched == 7: mark_as_watched_in_xbmc_library(new_item_video_type, xbmclibinfo['xbmcdbid'])
                                
                    tn.SetTaskCompletion()
                    common.notify(common.addon_id, 'small', '[B]' + title + '[/B]', '[B]Subscribed successfully.[/B]' , '5000')
                    xbmc.executebuiltin('Container.Refresh')
                else:
                    tn.SetTaskCompletion()
                    common.notify(common.addon_id, 'small', '[B]' + title + '[/B]', '[B]Unable to subscribe.[/B]' , '5000')
                    
            common.ClearGlobalProperty(common.gb_Lib_Subs_Op_Running)
                
    elif mode == common.mode_Unsubscribe:
        
        entertainment.loadiStreamPlugins()
        
        if not subs:
            from entertainment import subscriptions
            subs = subscriptions.Subscriptions()
            
        if subs.cancel_subscription(indexer, type, video_type, name, year) == False:
            common.notify(common.addon_id, 'small', '[B]' + title + '[/B]', '[B]Unsubscribed successfully.[/B]' , '5000')
            xbmc.executebuiltin('Container.Refresh')
        else:
            common.notify(common.addon_id, 'small', '[B]' + title + '[/B]', '[B]Unable to unsubscribe.[/B]' , '5000')

    elif mode == common.mode_Clean_Up_Subs: 

        entertainment.loadiStreamPlugins()
     
        if not subs:
            from entertainment import subscriptions
            subs = subscriptions.Subscriptions()
            
        subs_data = subs.get_subscriptions( indexer, type, video_type )
        
        totalitems = len(subs_data)
            
        from metahandler import metahandlers
        metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
        
        subs_cleaned = 0
        
        curr_name = ''
        curr_year = ''    
        for sub_data in subs_data:
            if not (sub_data['name'] == curr_name and sub_data['year'] == curr_year):
                curr_name = sub_data['name']
                curr_year = sub_data['year']
        
                if video_type == common.VideoType_TV:
                    tv_title = common.CleanTextForSearch(curr_name, strip=True)
                    meta = metaget.get_meta(video_type, tv_title, year=curr_year, imdb_id=sub_data['imdb_id'])
                    if not (meta['imdb_id'] or meta['tvdb_id']):
                        meta = metaget.get_meta(video_type, tv_title, imdb_id=sub_data['imdb_id'], year=curr_year)
                        
                if meta['status'] == 'Ended':
                    if not subs.cancel_subscription(indexer, type, video_type, curr_name, curr_year):
                        subs_cleaned += 1
        
        if subs_cleaned > 0:
            xbmc.executebuiltin("Container.Refresh")
                    
    elif mode == common.mode_Update_Subs:

        entertainment.loadiStreamPlugins(type=common.settings_TV_Shows, load_indexer=True, load_source=True, load_settings=True)
        
        if xbmc.getCondVisibility('Library.IsScanningVideo') or common.GetGlobalProperty(common.gb_Lib_Subs_Op_Running) == 'true':
            common.addon.log('Similar operation already running.')
            common.addon.show_ok_dialog(['Library scan or subscription update in progress.', 'Please wait for it to complete.'])
        else:
            common.SetGlobalProperty(common.gb_Lib_Subs_Op_Running, 'true')
            
            all_new_items = []
            
            if not subs:
                from entertainment import subscriptions
                subs = subscriptions.Subscriptions()
            
            metaget = None
            if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'clean_up_while_update_subs') == 'true':
                from metahandler import metahandlers
                metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
                
            subs_data = subs.get_subscriptions( indexer, type, video_type )
            
            totalitems = len(subs_data)
            
            tn = None
            if totalitems > 0:
                if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'show_sub_update_progress') == 'true':
                    notification_duration = 1000
                    tn = common.Threaded_Notification(notification_duration, 'Subscriptions', 'Updating...')
                else:
                    common.addon.show_small_popup('[COLOR white]Subscriptions[/COLOR]' , '[COLOR orange]Updating...[/COLOR]' , 
                        3000, common.notify_icon)
            
            subs_cleaned = 0
            
            sub_urls = {}
            curr_name = ''
            curr_year = '' 
            curr_title = ''
            curr_imdb_id = ''
            curr_indexer_id = ''
            curr_url = ''
            if totalitems > 0:
                subs_data.append( {'name':'dummy_item', 'year':'0', 'title':'dummy_item'} )
                
            for sub_data in subs_data:
                if not curr_name or ( sub_data['name'] == curr_name and sub_data['year'] == curr_year ):
                    sub_urls.update({sub_data['indexer_id'] : sub_data['url']})
                    if not curr_name:
                        curr_name = sub_data['name']
                        if not curr_year:
                            curr_year = sub_data['year']
                        if not curr_title:
                            curr_title = sub_data['title']
                        if not curr_imdb_id:
                            curr_imdb_id = sub_data['imdb_id']
                        if not curr_indexer_id:
                            curr_indexer_id = sub_data['indexer_id']
                        if not curr_url:
                            curr_url = sub_data['url']
                            
                        if tn and entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'show_sub_update_progress') == 'true':
                            tn.SetMessage2(curr_title)
                    
                elif not (sub_data['name'] == curr_name and sub_data['year'] == curr_year):
                    if metaget:    
                        if video_type == common.VideoType_TV:
                            tv_title = common.CleanTextForSearch(curr_name, strip=True)
                            meta = metaget.get_meta(video_type, tv_title, year=curr_year, imdb_id=curr_imdb_id)
                            if not (meta['imdb_id'] or meta['tvdb_id']):
                                meta = metaget.get_meta(video_type, tv_title, imdb_id=curr_imdb_id, year=curr_year)
                                
                        if meta['status'] == 'Ended':
                            if not subs.cancel_subscription(indexer, type, video_type, curr_name, curr_year):
                                subs_cleaned += 1
                    
                    urls = common.ConvertDictToString(sub_urls)
                    (il_title, il_error, new_items) = add_to_library(indexer, curr_indexer_id, curr_url, curr_title, curr_name, curr_year, '', '', type, video_type, curr_imdb_id)
                    all_new_items.extend(new_items)
                    
                    if sub_data['name'] != 'dummy_item':
                        curr_name = sub_data['name']
                        curr_year = sub_data['year']
                        curr_title = sub_data['title']
                        curr_imdb_id = sub_data['imdb_id']
                        curr_indexer_id = sub_data['indexer_id']
                        curr_url = sub_data['url']
                        if tn and entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'show_sub_update_progress') == 'true':
                            tn.SetMessage2(curr_title)
                        
                        sub_urls = {}
                        sub_urls.update({sub_data['indexer_id'] : sub_data['url']})
                        
                    urls = ''
                
            if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'update_lib_after_sub_update') == 'true':
                xbmc.executebuiltin('UpdateLibrary(video)')
                
                use_meta = False
                if video_type == common.VideoType_Movies:
                    use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
                elif video_type in (common.VideoType_TV, common.VideoType_Season, common.VideoType_Episode):
                    use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
                
                if len(all_new_items) > 0 and entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'sync_watched_status_with_lib') == 'true' and use_meta == True:
                    
                    xbmc.sleep(250)
                    while ( xbmc.getCondVisibility('Library.IsScanningVideo') ):
                        xbmc.sleep(250)
                    
                    if not metaget:
                        from metahandler import metahandlers
                        metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
                    
                    for new_item in all_new_items:
                    
                        new_item_imdb_id = new_item['imdb_id']
                        new_item_video_type = new_item['video_type']
                        new_item_name = new_item['name']
                        new_item_season = new_item['season']
                        new_item_episode = new_item['episode']
                        new_item_year = new_item['year']
                    
                        xbmclibinfo = get_info_from_xbmc_library(new_item_video_type, new_item_name, new_item_season, new_item_episode, new_item_year, 
                            properties=["imdbnumber"], toplevel=True)
                            
                        if not new_item_imdb_id:
                            new_item_imdb_id = xbmclibinfo['imdbnumber']
                                                
                        meta_watched = 6
                        if new_item_video_type == common.VideoType_Episode:
                            meta_watched = metaget._get_watched_episode({'imdb_id' : new_item_imdb_id, 'title':new_item_name, 'season':new_item_season, 
                                'episode':new_item_episode, 'premiered':'', 'tvdb_id':''})
                            if meta_watched == 7: 
                                xbmclibinfo = get_info_from_xbmc_library(new_item_video_type, new_item_name, new_item_season, new_item_episode, new_item_year)
                        elif new_item['video_type'] == common.VideoType_Movies:
                            meta_watched = metaget._get_watched(common.VideoType_Movies, new_item_imdb_id, '')
                            
                        if meta_watched == 7: mark_as_watched_in_xbmc_library(new_item_video_type, xbmclibinfo['xbmcdbid'])
            
            import datetime
            entertainment.SetiStreamSettings(common.settings_XBMC_Integration, 'update_suscription_timestamp', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            
            if totalitems > 0:
                if tn and entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'show_sub_update_progress') == 'true':
                    tn.SetTaskCompletion('Subscriptions', 'Updated Successfully.')
                else:
                    common.addon.show_small_popup('[COLOR white]Subscriptions[/COLOR]' , '[COLOR orange]Updated Successfully.[/COLOR]' , 
                            3000, common.notify_icon)
            
            if service == 'false':
                xbmc.executebuiltin("Container.Refresh")
            
            common.ClearGlobalProperty(common.gb_Lib_Subs_Op_Running)

    elif mode == common.mode_Manage_Subs:
        add_dir_title()
        
        entertainment.loadiStreamPlugins(load_settings=True)
        
        subs_last_update = entertainment.GetiStreamSettings(common.settings_XBMC_Integration, 'update_suscription_timestamp')
        common.addon.add_directory({'mode':'DUMMY-DIR'},{'title':'[B][COLOR gold]Last Update: [/COLOR][COLOR white]' + ('Never' if subs_last_update == '' or not subs_last_update else subs_last_update) + '[/COLOR][/B]'})
        
        item_query_dict = {'istream_path':istream_path + ' : ' + 'Update Subscriptions', 'mode':common.mode_Update_Subs, 'indexer':indexer, 'type':'tv_seasons', 'video_type':common.VideoType_TV}
        istream_query_dict = {'istream_path':istream_path + ' : ' + 'Update Subscriptions', 'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Update_Subs, 'indexer':indexer, 'type':'tv_seasons', 'video_type':common.VideoType_TV}
        contextMenuItems = []
        contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
        common.addon.add_directory(item_query_dict, {'title': 'Update Subscriptions'}, contextmenu_items=contextMenuItems )
        
        item_query_dict = {'istream_path':istream_path + ' : ' + 'Cleanup Subscriptions', 'mode':common.mode_Clean_Up_Subs, 'indexer':indexer, 'type':'tv_seasons', 'video_type':common.VideoType_TV}
        istream_query_dict = {'istream_path':istream_path + ' : ' + 'Cleanup Subscriptions', 'mode':common.mode_Add_to_MyStream, 'item_mode':common.mode_Clean_Up_Subs, 'indexer':indexer, 'type':'tv_seasons', 'video_type':common.VideoType_TV}
        contextMenuItems = []
        contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
        common.addon.add_directory(item_query_dict, {'title': 'Clean Up Subscriptions'}, contextmenu_items=contextMenuItems )
        
        if not subs:
            from entertainment import subscriptions
            subs = subscriptions.Subscriptions()
            
        subs_data = subs.get_subscriptions( indexer, type, video_type )
        
        metaget = ''
        if 'movie' in type:
            use_meta = True if entertainment.GetiStreamSettings(common.settings_Movies, 'metadata_movies') == 'true' else False
        elif 'tv' in type:
            use_meta = True if entertainment.GetiStreamSettings(common.settings_TV_Shows, 'metadata_tv_shows') == 'true' else False
            
        if use_meta == True:
            from metahandler import metahandlers
            metaget=metahandlers.MetaData(tmdb_api_key=tmdb_api_key)
            
        totalitems = len(subs_data)
        
        curr_name = ''
        curr_year = ''    
        for sub_data in subs_data:
            this_meta = {}
            if not (sub_data['name'] == curr_name and sub_data['year'] == curr_year):
                curr_name = sub_data['name']
                curr_year = sub_data['year']
                
                if use_meta == True:                                                
                    this_meta = get_metadata(metaget, video_type, curr_name, curr_name, curr_year, imdb = sub_data['imdb_id'])
                    
                if not sub_data['title']:
                    if use_meta == True:
                        sub_data['title'] = this_meta['title']
                    else:
                        sub_data['title'] = '-'
                
                from entertainment import htmlcleaner
                this_meta.update({'title': htmlcleaner.clean(sub_data['title'])})
                
                meta_img = this_meta.get('cover_url', '')
                meta_fanart = this_meta.get('backdrop_url', '')
                meta_imdb_id = this_meta.get('imdb_id', '')
                meta_watched = this_meta.get('overlay', 6)
                
                item_indexer=indexer
                item_indexer_id=sub_data['indexer_id']
                item_mode=common.mode_Content
                item_section=''
                item_url=sub_data['url']
                item_title=sub_data['title']
                item_name=curr_name
                item_year=curr_year
                item_season=''
                item_episode=''
                item_meta_img=meta_img
                item_meta_fanart=meta_fanart            
                item_fav = 'false'
                item_type = type
                
                if entertainment.GetiStreamSettings(common.settings_XBMC_Integration,'sync_watched_status_with_lib') == 'true':
                    xbmclibinfo = get_info_from_xbmc_library(video_type, item_name, item_season, item_episode, item_year, properties=["playcount"])
                    xbmcdbid = xbmclibinfo['xbmcdbid']
                    if xbmcdbid:
                        playcount = xbmclibinfo['playcount']
                        if not playcount:
                            playcount = 0
                        if (meta_watched == 6 and playcount <= 0) or (meta_watched == 7 and playcount > 0):
                            common.addon.log('Watch status is same in iStream and XBMC library.')
                        else:
                            if use_meta == True:
                                metaget.change_watched(video_type, item_name, meta_imdb_id, season=item_season, episode=item_episode, year=item_year)
                                if meta_watched == 6: meta_watched = 7
                                elif meta_watched == 7: meta_watched = 6                            
                                
                            if playcount <= 0: meta_watched = 6
                            elif playcount > 0: meta_watched = 7
                            
                            this_meta['playcount'] = playcount
                
                contextMenuItems = add_contextmenu(video_type, item_indexer, item_indexer_id, item_mode, item_section, 
                        item_url, meta_imdb_id, item_title, item_name, item_year, item_season, item_episode, item_type, use_meta, 
                        item_meta_img, item_meta_fanart, meta_watched, item_fav, trailer=this_meta.get('trailer', '') )
                
                cmi_str = str(contextMenuItems)
                if '[COLOR red]Unsubscribe[/COLOR]' in cmi_str and '[COLOR red]Delete[/COLOR] from Favorites' in cmi_str:
                    this_meta.update({'title':'[B][COLOR gold]|||[/COLOR] [COLOR green]|*|[/COLOR][/B] ' + this_meta['title']})
                elif '[COLOR red]Unsubscribe[/COLOR]' in cmi_str:
                    this_meta.update({'title':'[B][COLOR gold]|||[/COLOR][/B] ' + this_meta['title']})
                elif '[COLOR red]Delete[/COLOR] from Favorites' in cmi_str:
                    this_meta.update({'title':'[B][COLOR green]|*|[/COLOR][/B] ' + this_meta['title']})
                
                trailer = this_meta.get('trailer', '')
                if trailer and 'plugin://plugin.video.youtube/' in trailer:
                    trailer = '%s' % common.addon.build_plugin_url({'mode':common.mode_Play_Trailer, 'url':trailer})
                    
                try:
                    common.addon.add_directory({'indexer':item_indexer, 'indexer_id':item_indexer_id, 'mode':item_mode, 'section':item_section, 
                            'title':item_title, 'name':item_name, 'year':item_year, 'season':item_season, 'episode':item_episode, 'favorite':item_fav,
                            'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'imdb_id':meta_imdb_id, 'trailer':trailer}, this_meta, 
                            contextmenu_items=contextMenuItems, context_replace=True, img=meta_img, fanart=meta_fanart, total_items=totalitems)
                except:
                    common.addon.add_directory({'indexer':item_indexer, 'indexer_id':item_indexer_id, 'mode':item_mode, 'section':item_section, 
                            'title':urllib.quote_plus(item_title), 'name':urllib.quote_plus(item_name), 'year':item_year, 'season':item_season, 'favorite':item_fav, 
                            'episode':item_episode, 'type':item_type, 'img':item_meta_img, 'fanart':item_meta_fanart, 'url':item_url, 'imdb_id':meta_imdb_id, 'trailer':trailer}, this_meta, 
                            contextmenu_items=contextMenuItems, context_replace=True, img=meta_img, fanart=meta_fanart, total_items=totalitems)
            setViewForMode(common.mode_Section)
        common.addon.end_of_directory()
        
    #### File Stores ####
    elif mode == common.mode_File_Stores:    
        
        entertainment.loadiStreamPlugins(load_fileformats=True)
        
        from entertainment.filestore import FileStore
        filestore = FileStore()
        (file_ids, file_titles) = filestore.get_files()
        
        if len(file_ids) > 0:
            common.addon.add_directory({'istream_path':istream_path + ' : ' + 'Playlists added as iStream source...', 'indexer':indexer, 'mode':common.mode_Play_Lists, 'section':section, 'title': 'Playlists'}, 
                { 'title': '[B][COLOR yellow]Playlists added as [COLOR royalblue]i[/COLOR]Stream source...[/B][/COLOR]' }, img=common.get_themed_icon('playlists.png'), fanart=common.get_themed_fanart('playlists.jpg') )
            
        stores = filestore.get_filestores()
        
        common.addon.add_directory({'istream_path':istream_path + ' : ' + 'Add Online Playlist', 'indexer':indexer, 'mode':common.mode_Add_Http_File_Store, 'section':section, 
            'title': 'Add Online Playlist'}, { 'title': '[B][COLOR white]Add Online Playlist[/COLOR][/B]' }, img=common.get_themed_icon('playlists.png'), fanart=common.get_themed_fanart('playlists.jpg') )
        common.addon.add_directory({'istream_path':istream_path + ' : ' + 'Add Local Playlist', 'indexer':indexer, 'mode':common.mode_Add_Local_File_Store, 'section':section, 
            'title': 'Add Local Playlist'}, { 'title': '[B][COLOR white]Add Local Playlist[/COLOR][/B]' }, img=common.get_themed_icon('playlists.png'), fanart=common.get_themed_fanart('playlists.jpg') )

        file_objs = {}
        
        if stores:
            for store in stores:
                format = store['fmt_name']
                path = store['path']
                format_display_name = store['fmt_display_name'].upper()
                title = store['title']
                type = store['type']
                id = store['id']            
                img = store.get('img', '')
                fanart = store.get('fanart', '')
                
                context_menu_items = []
                query_dict = {'indexer':indexer, 'section':section, 'format':format, 'path':path, 'format_display_name':format_display_name, 
                    'name': title, 'title': title, 'type':type, 'url':path, 'img':img, 'fanart':fanart}
                
                item_title_pre = ''
                
                query_dict.update( {'mode' : common.mode_Play_File_Item } )
                context_menu_items.append( ('[COLOR royalblue][B]PLAY[/B][/COLOR]', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                
                query_dict.update( {'mode' : common.mode_Rename_File_Item } )
                context_menu_items.append( ('[B]Rename[/B] Playlist', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                
                if filestore.check_file_store(path):
                    query_dict.update( {'mode' : common.mode_Remove_Play_List_Source } )
                    context_menu_items.append( ('[COLOR red]Remove[/COLOR] Playlist', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                
                file_obj = file_objs.get(format, None)
                if not file_obj:            
                    file_obj = entertainment.GetFileFormatObj(format)
                    file_objs[format] = file_obj
                
                if file_obj.IsISTREAMImportSupported():
                    if filestore.get_file_id(path) in file_ids:
                        item_title_pre = '[B][COLOR royalblue]|||[/COLOR][/B] '
                        query_dict.update( {'mode' : common.mode_Remove_File_Item } )
                        context_menu_items.append( ('[COLOR red]Remove[/COLOR] as [COLOR royalblue]i[/COLOR]Stream Source', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                    else:
                        query_dict.update( {'mode' : common.mode_Add_File_Item } )
                        context_menu_items.append( ('[COLOR royalblue]Add[/COLOR] as [COLOR royalblue]i[/COLOR]Stream Source', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                
                query_dict.update({'mode':common.mode_Read_File_Item})        
                common.addon.add_directory(query_dict, {'title': item_title_pre + title },
                    contextmenu_items=context_menu_items, context_replace=False, img=img, fanart=fanart)
            
        setViewForMode(mode)
        common.addon.end_of_directory()

    elif mode == common.mode_Play_Lists:
        
        entertainment.loadiStreamPlugins(load_fileformats=True, load_settings=True)
        
        from entertainment.filestore import FileStore
        filestore = FileStore()
        
        file_objs = {}
        
        files = filestore.get_files_with_details()
        
        query_dict = {'indexer':indexer, 'section':section}
        
        for file in files:
            format = file['format']
            title = file['title']
            img = file.get('img', '')
            fanart = file.get('fanart', '')
            
            query_dict.update({'id':file['id'], 'title':title, 'name':file['name'], 'format':format, 'url':file['url'], 'path':file['path'],
                'img':img, 'fanart':fanart})
            file_obj = file_objs.get(format, None)
            if not file_obj:            
                file_obj = entertainment.GetFileFormatObj(format)
                file_objs[format] = file_obj
            format_display_name = file_obj.display_name
            query_dict.update({'format_display_name':format_display_name, 'type':file_obj.GetStoreItemType()})
            
            context_menu_items = []        
            
            query_dict.update( {'mode' : common.mode_Play_File_Item } )
            context_menu_items.append( ('[COLOR royalblue][B]PLAY[/B][/COLOR]', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
            
            query_dict.update( {'mode' : common.mode_Remove_File_Item } )
            context_menu_items.append( ('[COLOR red]Remove[/COLOR] as [COLOR royalblue]i[/COLOR]Stream Source', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                    
            query_dict.update({'mode':common.mode_Read_File_Item})        
            common.addon.add_directory(query_dict, {'title': title },
                contextmenu_items=context_menu_items, context_replace=True, img=img, fanart=fanart)   
            
        setViewForMode(mode)
        common.addon.end_of_directory()
        
    elif mode == common.mode_Add_Http_File_Store:

        entertainment.loadiStreamPlugins(load_fileformats=True, load_settings=True)

        dlg_hdr = 'iStream - Please type in the URL of the playlist '
        kb = xbmc.Keyboard('', dlg_hdr, False)
        kb.doModal()
        if (kb.isConfirmed()):
            file = kb.getText()
            
            if file:
            
                ( ff, raw_data ) = entertainment.DetectFileFormat(file)
                
                if ff:
                    format_name = ff.name
                    format_display_name = ff.display_name            
                else:
                
                    if raw_data == 'ISTREAM_MSG_NOT_AVAILABLE':
                        import xbmcgui
                        dialog = xbmcgui.Dialog()
                        ret_val = dialog.yesno('iSTREAM - Playlist Unavailable', 'The playlist you are trying to add is unavailable at this time.', 'Do you still want to add this playlist?')
                        if ret_val == False:	
                            common.notify(common.addon_id, 'small', '[B]Playlist Unavailable[/B]', '[B]The playlist you are trying to access is unavailable at this time. Please try again later.[/B]' , '5000')
                        else:
                    
                            formats = entertainment.GetFileFormats()
                           
                            fn = []
                            fdn = []
                           
                            for fmt in formats:
                                fn.append(fmt['name'])
                                fdn.append(fmt['display_name'])
                            
                            if fn:
                                import xbmcgui
                                dialog = xbmcgui.Dialog()
                                format_index = dialog.select('iStream - Please select the format of the playlist', fdn) 
                                
                                if format_index >= 0:
                                
                                    format_name = fn[format_index]
                                    format_display_name = fdn[format_index]
                                    
                                    ff = entertainment.GetFileFormatObj(format_name)
                            
                if ff:
                    
                    if ff.CanParseRawData():
                        (file_title, file_img, file_fanart) = ff.ParseHeader(raw_data)
                    else:
                        (file_title, file_img, file_fanart) = ff.ReadFile(file, True)
                    
                    from entertainment.filestore import FileStore
                    filestore = FileStore()
                    
                    while True:
                        kb1 = xbmc.Keyboard(file_title, 'iStream - Provide a name for the playlist', False)
                        kb1.doModal()
                        if (kb1.isConfirmed()):
                            file_title = kb1.getText()
                            if filestore.check_file_store_title(file_title):
                                common.notify(common.addon_id, 'small', '[B]' + file_title + '[/B]', '[B]Title already in use.[/B]' , '5000')
                            else:
                                break
                        else:
                            file_title = ''
                            break
                            
                    if file_title:
                        filestore.add_file_store(file_title, file_img, file_fanart, ff.GetStoreItemType(), format_name, format_display_name, file)
                        common.notify(common.addon_id, 'small', '[B]' + file_title + '[/B]', '[B]Playlist added.[/B]' , '5000')        
                        xbmc.executebuiltin('Container.Refresh')
                    
    elif mode == common.mode_Add_Local_File_Store:

        entertainment.loadiStreamPlugins(load_fileformats=True)
        
        import xbmcgui
        dialog = xbmcgui.Dialog()
        file = dialog.browse(1, 'iStream - Please select the playlist file', 'files', entertainment.GetFileFormatExtensionsMask())
        if file:
            
            ( ff, raw_data ) = entertainment.DetectFileFormat(file)
            
            if ff:
                format_name = ff.name
                format_display_name = ff.display_name
            
            else:
            
                if raw_data == 'ISTREAM_MSG_NOT_AVAILABLE':
                    ret_val = dialog.yesno('iSTREAM - Playlist Unavailable', 'The playlist you are trying to add is unavailable at this time.', 'Do you still want to add this playlist?')
                    if ret_val == False:	
                        common.notify(common.addon_id, 'small', '[B]Playlist Unavailable[/B]', '[B]The playlist you are trying to access is unavailable at this time. Please try again later.[/B]' , '5000')
                    else:

                        formats = entertainment.GetFileFormats()
                       
                        fn = []
                        fdn = []
                       
                        for fmt in formats:
                            fn.append(fmt['name'])
                            fdn.append(fmt['display_name'])
                        
                        if fn:
                            format_index = dialog.select('iStream - Please select the format of the playlist', fdn) 
                            
                            if format_index >= 0:
                            
                                format_name = fn[format_index]
                                format_display_name = fdn[format_index]
                                
                                ff = entertainment.GetFileFormatObj(format_name)
                
            if ff:
            
                if ff.CanParseRawData():
                    (file_title, file_img, file_fanart) = ff.ParseHeader(raw_data)
                else:					
                    (file_title, file_img, file_fanart) = ff.ReadFile(file, True)
                
                from entertainment.filestore import FileStore
                filestore = FileStore()
                
                while True:
                    kb1 = xbmc.Keyboard(file_title, 'iStream - Provide a name for the playlist', False)
                    kb1.doModal()
                    if (kb1.isConfirmed()):
                        file_title = kb1.getText()
                        if filestore.check_file_store_title(file_title):
                            common.notify(common.addon_id, 'small', '[B]' + file_title + '[/B]', '[B]Title already in use.[/B]' , '5000')
                        else:
                            break
                    else:
                        file_title = ''
                        break
                        
                if file_title:
                    filestore.add_file_store(file_title, file_img, file_fanart, ff.GetStoreItemType(), format_name, format_display_name, file)
                    common.notify(common.addon_id, 'small', '[B]' + file_title + '[/B]', '[B]Playlist added.[/B]' , '5000')        
                    xbmc.executebuiltin('Container.Refresh')
                    
    elif mode == common.mode_Add_File_Store:
        
        entertainment.loadiStreamPlugins(load_fileformats=True, load_settings=True)
        
        format_name = common.addon.queries['format']
        format_display_name = common.addon.queries['format_display_name']
        file = url
        
        ( ff, raw_data ) = entertainment.DetectFileFormat(file)
            
        if ff:
            format_name = ff.name
            format_display_name = ff.display_name
        
        else:
            if raw_data == 'ISTREAM_MSG_NOT_AVAILABLE':
                import xbmcgui
                dialog = xbmcgui.Dialog()
                ret_val = dialog.yesno('iSTREAM - Playlist Unavailable', 'The playlist you are trying to add is unavailable at this time', 'Do you still want to add this playlist?')
                if ret_val == False:
                    common.notify(common.addon_id, 'small', '[B]Playlist Unavailable[/B]', '[B]The playlist you are trying to access is unavailable at this time. Please try again later.[/B]' , '5000')
                else:
                    formats = entertainment.GetFileFormats()
                       
                    fn = []
                    fdn = []
                   
                    for fmt in formats:
                        fn.append(fmt['name'])
                        fdn.append(fmt['display_name'])
                    
                    if fn:
                        format_index = dialog.select('iStream - Please select the format of the playlist', fdn) 
                        
                        if format_index >= 0:
                        
                            format_name = fn[format_index]
                            format_display_name = fdn[format_index]
                            
                            ff = entertainment.GetFileFormatObj(format_name)
                    
        if ff:
            if ff.CanParseRawData():
                (file_title, file_img, file_fanart) = ff.ParseHeader(raw_data)
            else:					    
                (file_title, file_img, file_fanart) = ff.ReadFile(file, True)
            
            from entertainment.filestore import FileStore
            filestore = FileStore()
            
            while True:
                kb1 = xbmc.Keyboard(file_title, 'iStream - Provide a name for the playlist', False)
                kb1.doModal()
                if (kb1.isConfirmed()):
                    file_title = kb1.getText()
                    if filestore.check_file_store_title(file_title):
                        common.notify(common.addon_id, 'small', '[B]' + file_title + '[/B]', '[B]Title already in use.[/B]' , '5000')
                    else:
                        break
                else:
                    file_title = ''
                    break
                    
            if file_title:
                filestore.add_file_store(file_title, file_img, file_fanart, ff.GetStoreItemType(), format_name, format_display_name, file)
                common.notify(common.addon_id, 'small', '[B]' + file_title + '[/B]', '[B]Playlist added.[/B]' , '5000')        
                xbmc.executebuiltin('Container.Refresh')
        
    elif mode == common.mode_Read_File_Item:

        entertainment.loadiStreamPlugins(load_fileformats=True, load_settings=True)

        format = common.addon.queries['format']
        format_display = common.addon.queries['format_display_name']
        store_hashes = common.addon.get_setting(format + '_store')
        ff = entertainment.GetFileFormatObj(format)
        (title, img, fanart, items) = ff.ReadItem(common.addon.queries)
        
        if not items:
            common.notify(common.addon_id, 'small', '[B]Playlist Unavailable[/B]', '[B]The playlist you are trying to access is unavailable at this time. Please try again later.[/B]' , '5000')
        else:
            from entertainment.filestore import FileStore
            filestore = FileStore()
            (file_ids, file_titles) = filestore.get_files()
            
            for item in items:
                if not item: continue
                query_dict = {}
                context_menu_items = []
                for key, val in item.items():
                    query_dict[key] = val
                
                query_dict.update( {'indexer':indexer, 'section':section, 'format':format, 'format_display_name':format_display } )

                is_playable = None
                is_folder = True
                if ff.IsItemAList(item):
                    item_title_pre = ''
                    
                    query_dict.update( {'mode' : common.mode_Play_File_Item } )
                    context_menu_items.append( ('[COLOR royalblue][B]PLAY[/B][/COLOR]', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                    
                    if filestore.check_file_store(item['url']):
                        item_title_pre = '[B][COLOR yellow]PL[/COLOR][/B] '
                        query_dict.update( {'mode' : common.mode_Remove_Play_List_Source } )
                        context_menu_items.append( ('[COLOR red]Remove[/COLOR] Playlist', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                    else:
                        query_dict.update( {'mode' : common.mode_Add_File_Store } )
                        context_menu_items.append( ('[COLOR green]Add[/COLOR] Playlist', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                    
                    if ff.IsISTREAMImportSupported():
                        if filestore.get_file_id(item['url']) in file_ids:
                            item_title_pre = '[B][COLOR royalblue]|||[/COLOR][/B] ' + item_title_pre
                            query_dict.update( {'mode' : common.mode_Remove_File_Item } )
                            context_menu_items.append( ('[COLOR red]Remove[/COLOR] as [COLOR royalblue]i[/COLOR]Stream Source', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                        else:
                            query_dict.update( {'mode' : common.mode_Add_File_Item } )
                            context_menu_items.append( ('[COLOR royalblue]Add[/COLOR] as [COLOR royalblue]i[/COLOR]Stream Source', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                                
                    item.update( {'title' : item_title_pre + query_dict['title']  } )
                    query_dict.update({'mode':common.mode_Read_File_Item_2})
                elif ff.IsItemPlayable(item):
                    is_playable = 'true'
                    is_folder = False
                    query_dict.update({'mode':common.mode_Play, 'play':'true'})
                    item['title'] += ' [COLOR royalblue][' + common.GetDomainFromUrl(item['url']) + '][/COLOR] '
                else:
                    query_dict.update({'mode':common.mode_Dummy})
                
                if ff.IsItemPlayable(item):
                    common.addon.add_directory( query_dict, {'title' : item['title']},  contextmenu_items=context_menu_items, 
                        context_replace=True, is_folder=is_folder, is_playable=is_playable, img=item.get('img', ''), fanart=item.get('fanart', ''))
                else:
                    common.addon.add_directory( query_dict, {'title' : item['title']},  contextmenu_items=context_menu_items, 
                        context_replace=False, is_folder=is_folder, is_playable=is_playable, img=item.get('img', ''), fanart=item.get('fanart', ''))
                
            setViewForMode(mode)
            common.addon.end_of_directory()    
        
    elif mode == common.mode_Read_File_Item_2:
        
        entertainment.loadiStreamPlugins(load_fileformats=True, load_settings=True)

        format = common.addon.queries['format']
        format_display = common.addon.queries['format_display_name']
        
        store_hashes = common.addon.get_setting(format + '_store')
        
        ( ff, raw_data ) = entertainment.DetectFileFormat(common.addon.queries['url'])
            
        if ff:
            format = ff.name
            format_display = ff.display_name
        
        else:
            if raw_data == 'ISTREAM_MSG_NOT_AVAILABLE':
                common.notify(common.addon_id, 'small', '[B]Playlist Unavailable[/B]', '[B]The playlist you are trying to access is unavailable at this time. Please try again later.[/B]' , '5000')
            else:
                formats = entertainment.GetFileFormats()
                   
                fn = []
                fdn = []
               
                for fmt in formats:
                    fn.append(fmt['name'])
                    fdn.append(fmt['display_name'])
                
                if fn:
                    import xbmcgui
                    dialog = xbmcgui.Dialog()
                    format_index = dialog.select('iStream - Please select the format of the playlist', fdn) 
                    
                    if format_index >= 0:
                    
                        format = fn[format_index]
                        format_display = fdn[format_index]
                        
                        ff = entertainment.GetFileFormatObj(format)
                    
        if ff:

            if ff.CanParseRawData():
                (title, img, fanart, items) = ff.ParseData(raw_data)
            else:
                (title, img, fanart, items) = ff.ReadItem(common.addon.queries)
                
            from entertainment.filestore import FileStore
            filestore = FileStore()
            (file_ids, file_titles) = filestore.get_files()
            
            for item in items:
                if not item: continue
                query_dict = {}
                context_menu_items = []
                for key, val in item.items():
                    query_dict[key] = val
                
                query_dict.update( {'indexer':indexer, 'section':section, 'format':format, 'format_display_name':format_display } )

                is_playable = None
                is_folder = True
                if ff.IsItemAList(item):
                    item_title_pre = ''            
                    
                    query_dict.update( {'mode' : common.mode_Play_File_Item } )
                    context_menu_items.append( ('[COLOR royalblue][B]PLAY[/B][/COLOR]', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                    
                    if filestore.check_file_store(item['url']):
                        item_title_pre = '[B][COLOR yellow]PL[/COLOR][/B] '
                        query_dict.update( {'mode' : common.mode_Remove_Play_List_Source } )
                        context_menu_items.append( ('[COLOR red]Remove[/COLOR] Playlist', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                    else:
                        query_dict.update( {'mode' : common.mode_Add_File_Store } )
                        context_menu_items.append( ('[COLOR green]Add[/COLOR] Playlist', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                    
                    if ff.IsISTREAMImportSupported():
                        if filestore.get_file_id(item['url']) in file_ids:
                            item_title_pre = '[B][COLOR royalblue]|||[/COLOR][/B] ' + item_title_pre
                            query_dict.update( {'mode' : common.mode_Remove_File_Item } )
                            context_menu_items.append( ('[COLOR red]Remove[/COLOR] as [COLOR royalblue]i[/COLOR]Stream Source', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                        else:
                            query_dict.update( {'mode' : common.mode_Add_File_Item } )
                            context_menu_items.append( ('[COLOR royalblue]Add[/COLOR] as [COLOR royalblue]i[/COLOR]Stream Source', 'RunPlugin(%s)' % common.addon.build_plugin_url(query_dict) ) )
                                
                    item.update( {'title' : item_title_pre + query_dict['title']  } )
                    query_dict.update({'mode':common.mode_Read_File_Item_2})
                elif ff.IsItemPlayable(item):
                    is_playable = 'true'
                    is_folder = False
                    query_dict.update({'mode':common.mode_Play, 'play':'true'})
                    item['title'] += ' [COLOR royalblue][' + common.GetDomainFromUrl(item['url']) + '][/COLOR] '
                else:
                    query_dict.update({'mode':common.mode_Dummy})
                
                if ff.IsItemPlayable(item):
                    common.addon.add_directory( query_dict, {'title' : item['title']},  contextmenu_items=context_menu_items, 
                        context_replace=True, is_folder=is_folder, is_playable=is_playable, img=item.get('img', ''), fanart=item.get('fanart', ''))
                else:
                    common.addon.add_directory( query_dict, {'title' : item['title']},  contextmenu_items=context_menu_items, 
                        context_replace=False, is_folder=is_folder, is_playable=is_playable, img=item.get('img', ''), fanart=item.get('fanart', ''))
               
            setViewForMode(mode)
            common.addon.end_of_directory()        
        
    elif mode == common.mode_Add_File_Item:

        entertainment.loadiStreamPlugins(load_fileformats=True, load_settings=True)

        format = common.addon.queries['format']
        format_display = common.addon.queries['format_display_name']
        
        from entertainment.filestore import FileStore
        filestore = FileStore()
       
        name = ''
        while True:
            dlg_hdr = 'Add to iStream as... (15 characters max) '
            kb = xbmc.Keyboard('', dlg_hdr, False)
            kb.doModal()
            if ( kb.isConfirmed() ):
                name = kb.getText()
                name = name[:15]
                
                if filestore.check_file_title(name):
                    common.notify(common.addon_id, 'small', '[B]' + name + '[/B]', '[B]Title already in use.[/B]' , '5000')
                else:
                    break
            else:
                name = ''
                break

        if name:
        
            ( ff, raw_data ) = entertainment.DetectFileFormat(common.addon.queries['url'])
            
            if ff:
                format = ff.name
                format_display = ff.display_name
            
            else:
                if raw_data == 'ISTREAM_MSG_NOT_AVAILABLE':
                    import xbmcgui
                    dialog = xbmcgui.Dialog()
                    ret_val = dialog.yesno('iSTREAM - Playlist Unavailable', 'The playlist you are trying to add is unavailable at this time.', 'Do you still want to add this playlist?')
                    if ret_val == False:	
                        common.notify(common.addon_id, 'small', '[B]Playlist Unavailable[/B]', '[B]The playlist you are trying to access is unavailable at this time. Please try again later.[/B]' , '5000')
                    else:
                        formats = entertainment.GetFileFormats()
                           
                        fn = []
                        fdn = []
                       
                        for fmt in formats:
                            fn.append(fmt['name'])
                            fdn.append(fmt['display_name'])
                        
                        if fn:
                            format_index = dialog.select('iStream - Please select the format of the playlist', fdn) 
                            
                            if format_index >= 0:
                            
                                format = fn[format_index]
                                format_display = fdn[format_index]
                                
                                ff = entertainment.GetFileFormatObj(format)
                        
            if ff:
            
                content_types = {'Movies':'MovieSource', 'Live TV':'LiveTVSource'}            
                content_type_keys = []
                content_type_values = []
                for key, value in content_types.items():
                    content_type_keys.append(key)
                    content_type_values.append(value)
                    
                import xbmcgui
                dialog = xbmcgui.Dialog()
                
                content_type_index = dialog.select('iStream - Please select list content type', content_type_keys) 
                            
                if content_type_index >= 0:
                    content_type = content_type_values[content_type_index]
                    ff.AddItem(common.addon.queries, common.CleanText(title, True, True), name, content_type)
                    common.notify(common.addon_id, 'small', '[B]' + name + '[/B]', '[B]Added to iStream.[/B]' , '5000')
                    xbmc.executebuiltin('Container.Refresh' )
            
            
    elif mode == common.mode_Remove_File_Item:

        entertainment.loadiStreamPlugins(load_fileformats=True)
        
        format = common.addon.queries['format']
        ff = entertainment.GetFileFormatObj(format)

        error = ff.Remove(url)
        if error:
            common.notify(common.addon_id, 'small', '[B]' + name.replace(',', '') + '[/B]', '[B]Failed to remove from iStream.[/B]' , '5000')        
        else:
            common.notify(common.addon_id, 'small', '[B]' + name.replace(',', '') + '[/B]', '[B]Successfully removed from iStream.[/B]' , '5000')
            xbmc.executebuiltin('Container.Refresh')
            
    elif mode == common.mode_Remove_Play_List_Source:
        
        entertainment.loadiStreamPlugins(load_fileformats=True)
        
        from entertainment.filestore import FileStore
        filestore = FileStore()
        filestore.remove_file_store(url)
        xbmc.executebuiltin('Container.Refresh')
    elif mode == common.mode_Rename_File_Item:    

        entertainment.loadiStreamPlugins(load_fileformats=True)
        
        from entertainment.filestore import FileStore
        filestore = FileStore()
        
        while True:
            kb1 = xbmc.Keyboard(title, 'iStream - Provide a name for the playlist', False)
            kb1.doModal()
            if (kb1.isConfirmed()):
                file_title = kb1.getText()
                if filestore.check_file_store_title(file_title):
                    common.notify(common.addon_id, 'small', '[B]' + file_title + '[/B]', '[B]Title already in use.[/B]' , '5000')
                else:
                    break
            else:
                file_title = ''
                break
                
        if file_title:
            filestore.rename_file_store(url, file_title)
            common.notify(common.addon_id, 'small', '[B]' + file_title + '[/B]', '[B]Playlist renamed.[/B]' , '5000')        
            xbmc.executebuiltin('Container.Refresh')
            
    elif mode == common.mode_Play_File_Item:       
        
        entertainment.loadiStreamPlugins(load_fileformats=True, load_settings=True)
        
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        player = xbmc.Player() 
        
        if not player.isPlayingVideo():
            playlist.clear()
            
        format = common.addon.queries['format']
        format_display = common.addon.queries['format_display_name']
        
        store_hashes = common.addon.get_setting(format + '_store')
        
        ( ff, raw_data ) = entertainment.DetectFileFormat(common.addon.queries['url'])
            
        if ff:
            format = ff.name
            format_display = ff.display_name
        
        else:
            if raw_data == 'ISTREAM_MSG_NOT_AVAILABLE':
                common.notify(common.addon_id, 'small', '[B]Playlist Unavailable[/B]', '[B]The playlist you are trying to access is unavailable at this time. Please try again later.[/B]' , '5000')
            else:
                formats = entertainment.GetFileFormats()
                   
                fn = []
                fdn = []
               
                for fmt in formats:
                    fn.append(fmt['name'])
                    fdn.append(fmt['display_name'])
                
                if fn:
                    import xbmcgui
                    dialog = xbmcgui.Dialog()
                    format_index = dialog.select('iStream - Please select the format of the playlist', fdn) 
                    
                    if format_index >= 0:
                    
                        format = fn[format_index]
                        format_display = fdn[format_index]
                        
                        ff = entertainment.GetFileFormatObj(format)
                    
        if ff:

            if ff.CanParseRawData():
                (title, img, fanart, items) = ff.ParseData(raw_data)
            else:
                (title, img, fanart, items) = ff.ReadItem(common.addon.queries)
                
            from entertainment.filestore import FileStore
            filestore = FileStore()
            (file_ids, file_titles) = filestore.get_files()
            
            for item in items:
                if not item: continue
                query_dict = {}
                for key, val in item.items():
                    query_dict[key] = val
                
                query_dict.update( {'indexer':indexer, 'section':section, 'format':format, 'format_display_name':format_display } )
                
                if ff.IsItemPlayable(item):
                
                    listitem = xbmcgui.ListItem(item['title'], iconImage=item['img'], thumbnailImage=item['img'])
                    
                    listitem.setProperty('fanart_image', item['fanart'])    
                    
                    query_dict.update({'mode':common.mode_Play, 'play':'true'})
                    
                    playlist.add(url=common.addon.build_plugin_url(query_dict), listitem=listitem)
                else:
                    continue
                    
        if len(playlist) > 0 and not player.isPlayingVideo():
            player.play(playlist)
        
    #### Tools ####
    elif mode == common.mode_Tools:

        if name:
            if entertainment.ExecuteTool(name):
                common.notify(common.addon_id, 'small', '[B]' + common.addon.queries['notify_msg_header'].replace(',', '') + '[/B]', 
                    '[B]'+common.addon.queries['notify_msg_success']+'[/B]' , '5000')
            else:
                common.notify(common.addon_id, 'small', '[B]' + common.addon.queries['notify_msg_header'].replace(',', '') + '[/B]', 
                    '[B]'+common.addon.queries['notify_msg_failure']+'[/B]' , '5000')
        else:
            tools = entertainment.GetTools()
            for tool in tools:
                item_query_dict = {'istream_path':istream_path + ' : ' + tool['title'], 'title':tool['title'], 'mode':tool['mode'], 'indexer':tool['indexer'], 'section':tool['section'], 'name':tool['name'],
                    'img':tool['img'], 'fanart':tool['fanart'], 'notify_msg_header':tool['notify_msg_header'], 'notify_msg_success':tool['notify_msg_success'],
                    'notify_msg_failure':tool['notify_msg_failure']}
                istream_query_dict = {'istream_path':istream_path + ' : ' + tool['title'], 'title':tool['title'], 'mode':common.mode_Add_to_MyStream, 'item_mode':tool['mode'], 'indexer':tool['indexer'], 'section':tool['section'], 'name':tool['name'],
                    'img':tool['img'], 'fanart':tool['fanart'], 'notify_msg_header':tool['notify_msg_header'], 'notify_msg_success':tool['notify_msg_success'],
                    'notify_msg_failure':tool['notify_msg_failure']}
                
                contextMenuItems = []
                contextMenuItems.insert( 0 , ('[COLOR green]Add[/COLOR] to [B][COLOR royalblue]my[/COLOR]Stream[/B]', 'RunPlugin(%s)' % common.addon.build_plugin_url(istream_query_dict)))            
                
                common.addon.add_directory( item_query_dict, {'title' : tool['title']},  contextmenu_items=contextMenuItems,             
                    context_replace=True, img=tool['img'], fanart=tool['fanart'])
                  
            setViewForMode(mode)
            common.addon.end_of_directory()    
            
    elif mode == common.mode_Installer:
        ISTREAM_SETUP()
        
    elif mode == common.mode_EULA:
        from istreams.dialogs import DialogiStreamTerms
        DialogiStreamTerms.show(btn_OK=True)
        
    elif mode == common.mode_iStream:
        GetIStream(show_mystream=False)
        
    elif mode == common.mode_MyStream:
        GetMyStream(show_istream=False)

    elif mode == common.mode_Add_to_MyStream:
        from entertainment.mystream import MyStream
        mystream = MyStream()
        if mystream.check_mystream(istream_path):
            common.notify(common.addon_id, 'small', '[B]' + istream_path + '[/B]', '[B]Already exists in [COLOR royalblue]my[/COLOR]Stream.[/B]' , '5000')
        else:
            common.addon.queries.update({'mode':common.addon.queries['item_mode']})
            if mystream.add_mystream_item(istream_path, img, fanart, common.addon.build_plugin_url(common.addon.queries)):
                common.notify(common.addon_id, 'small', '[B]' + istream_path + '[/B]', '[B]Successfully added to [COLOR royalblue]my[/COLOR]Stream.[/B]' , '5000')
            else:
                common.notify(common.addon_id, 'small', '[B]' + istream_path + '[/B]', '[B]Failed to add to [COLOR royalblue]my[/COLOR]Stream[/B].' , '5000')
            
    elif mode == common.mode_Remove_from_MyStream:
        from entertainment.mystream import MyStream
        mystream = MyStream()
        if mystream.remove_mystream_item(title):
            common.notify(common.addon_id, 'small', '[B]' + common.addon.queries.get('display_title', title) + '[/B]', '[B]Successfully deleted from [COLOR roy7alblue]my[/COLOR]Stream.[/B]' , '5000')
            xbmc.executebuiltin('Container.Refresh')
        else:
            common.notify(common.addon_id, 'small', '[B]' + common.addon.queries.get('display_title', title) + '[/B]', '[B]Failed to delete from [COLOR royalblue]my[/COLOR]Stream.[/B]' , '5000')
    
    elif mode == common.mode_Rename_MyStream_Item:
        
        mystream_item_title = common.addon.queries.get('display_title', title)
        new_mystream_item_title = ''
        kb = xbmc.Keyboard(mystream_item_title, 'Rename', False)
        kb.doModal()
        if (kb.isConfirmed()):
            new_mystream_item_title = kb.getText()
            if new_mystream_item_title != '' and len(new_mystream_item_title) > 0 and new_mystream_item_title != mystream_item_title:
                from entertainment.mystream import MyStream
                mystream = MyStream()
        
                if mystream.rename_mystream_item(title, new_mystream_item_title):
                    common.notify(common.addon_id, 'small', '[B]' + mystream_item_title + '[/B]', '[B]Successfully renamed to: ' + new_mystream_item_title , '5000')
                    xbmc.executebuiltin('Container.Refresh')
                else:
                    common.notify(common.addon_id, 'small', '[B]' + mystream_item_title + '[/B]', '[B]Failed to rename.' , '5000')
    
    elif mode == common.mode_Reload_Plugins:
       PreLoadiStreamPlugins() 
    
    common.stop_local_proxy()
