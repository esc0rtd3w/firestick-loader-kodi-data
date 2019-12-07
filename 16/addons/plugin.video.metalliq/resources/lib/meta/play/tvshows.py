import re
import json
from xbmcswift2 import xbmc
import urllib
import datetime
from meta import plugin, import_tmdb, import_tvdb, create_tvdb, LANG
from meta.gui import dialogs
from meta.utils.properties import set_property
from meta.utils.text import to_unicode, to_utf8
from meta.library.tvshows import get_tv_player_plugin_from_library
from meta.info import get_tvshow_metadata_trakt, get_tvshow_metadata_tvdb, get_tvshow_metadata_tmdb, get_tvshow_metadata_tvmaze, get_season_metadata_trakt, get_season_metadata_tvdb, get_season_metadata_tmdb, get_season_metadata_tvmaze, get_episode_metadata_trakt, get_episode_metadata_tvdb, get_episode_metadata_tmdb, get_episode_metadata_tvmaze
from meta.navigation.base import get_icon_path, get_background_path, get_banner_path
from meta.play.players import get_needed_langs, get_players, ADDON_SELECTOR
from meta.play.channelers import get_needed_langs, ADDON_PICKER
from meta.play.base import get_trakt_ids, active_players, active_channelers, action_cancel, action_play, on_play_video
from settings import SETTING_USE_SIMPLE_SELECTOR, SETTING_TV_DEFAULT_PLAYER, SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, SETTING_TV_DEFAULT_PLAYER_FROM_CONTEXT, SETTING_TV_DEFAULT_CHANNELER
from language import get_string as _

def play_episode(id, season, episode, mode):
    import_tvdb()
    id = int(id)
    season = int(season)
    episode = int(episode)
    # Get database id
    dbid = xbmc.getInfoLabel("ListItem.DBID")
    try:
        dbid = int(dbid)
    except:
        dbid = None
    # Get show data from TVDB
    show = tvdb[id]
    show_info = get_tvshow_metadata_tvdb(show, banners=False)
    # Get players to use
    if mode == 'select':
        play_plugin = ADDON_SELECTOR.id
    elif mode == 'context':
        play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_CONTEXT, unicode)
    elif mode == 'library':
        play_plugin = get_tv_player_plugin_from_library(id)
        if not play_plugin or play_plugin == "default":
            play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    elif mode == 'default':
        play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER, unicode)
    else:
        play_plugin = mode
    if mode != 'context': players = active_players("tvshows", filters = {'network': show.get('network')})
    else: players = get_players("tvshows", filters = {'network': show.get('network')})
    players = [p for p in players if p.id == play_plugin] or players
    if not players or len(players) == 0: return xbmc.executebuiltin( "Action(Info)")
    # Get show ids from Trakt
    trakt_ids = get_trakt_ids("tvdb", id, show['seriesname'], "show", show.get('year', 0))
    # Get parameters
    params = {}
    for lang in get_needed_langs(players):
        if lang == LANG:
            tvdb_data = show
        else:
            tvdb_data = create_tvdb(lang)[id]
        if tvdb_data['seriesname'] is None:
            continue
        episode_parameters = get_episode_parameters(tvdb_data, season, episode)
        if episode_parameters is not None:
            params[lang] = episode_parameters
        else:
            if trakt_ids["tmdb"] != None and trakt_ids["tmdb"] != "":
                return tmdb_play_episode(trakt_ids["tmdb"], season, episode, mode)
            elif trakt_ids["tvdb"] == None or trakt_ids["tvdb"] == "":
                msg = "{0} {1} - S{2}E{3}".format(_("No TVDb information found for"), show_info['name'], season, episode)
                return dialogs.ok(_("%s not found") % _("Episode information"), msg)
            else:
                msg = "{0} {1} - S{2}E{3}".format(_("No TVDb or TMDb information found for"), show_info['name'], season, episode)
                return dialogs.ok(_("%s not found") % _("Episode information"), msg)
        if trakt_ids != None: params[lang].update(trakt_ids)
        params[lang]['info'] = show_info
        params[lang] = to_unicode(params[lang])
    # Go for it
    link = on_play_video(mode, players, params, trakt_ids)
    if link:
        # set properties
        set_property("data", json.dumps({'dbid': dbid, 'tvdb': id, 
            'season': season, 'episode': episode}))
        # Play
        season_info = get_season_metadata_tvdb(show_info, show[season], banners=False)
        episode_info = get_episode_metadata_tvdb(season_info, show[season][episode])
        action_play({
            'label': episode_info['title'],
            'path': link,
            'info': episode_info,
            'is_playable': True,
            'info_type': 'video',
            'thumbnail': episode_info['poster'],
            'poster': episode_info['poster'],
            'properties' : {'fanart_image' : episode_info['fanart']},
        })

def play_episode_from_guide(id, season, episode, mode):  
    import_tvdb()
    id = int(id)
    season = int(season)
    episode = int(episode)
    dbid = xbmc.getInfoLabel("ListItem.DBID")
    try:
        dbid = int(dbid)
    except:
        dbid = None
    show = tvdb[id]
    show_info = get_tvshow_metadata_tvdb(show, banners=False)
    if mode == 'select':
        play_plugin = ADDON_PICKER.id
    elif mode == 'default':
        play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_CHANNELER, unicode)
    else:
        play_plugin = mode
    channelers = active_channelers("tvshows", filters = {'network': show.get('network')})
    channelers = [p for p in channelers if p.id == play_plugin] or channelers
    if not channelers or len(channelers) == 0:
        xbmc.executebuiltin( "Action(Info)")
        action_cancel()
        return
    trakt_ids = get_trakt_ids("tvdb", id, show['seriesname'],
                    "show", show.get('year', 0))
    params = {}
    for lang in get_needed_langs(channelers):
        if lang == LANG:
            tvdb_data = show
        else:
            tvdb_data = create_tvdb(lang)[id]
        if tvdb_data['seriesname'] is None:
            continue
        episode_parameters = get_episode_parameters(tvdb_data, season, episode)
        if episode_parameters is not None:
            params[lang] = episode_parameters
        else:
            msg = "{0} {1} - S{1}E{2}".format(_("No tvdb information found for"), show['seriesname'], season, episode)
            dialogs.ok(_("%s not found") % _("Episode information"), msg)
            return
        if trakt_ids != None:
            params[lang].update(trakt_ids)
        params[lang]['info'] = show_info
        params[lang] = to_unicode(params[lang])
    link = on_play_video(mode, channelers, params, trakt_ids)
    if link:
        set_property("data", json.dumps({'dbid': dbid, 'tvdb': id, 
            'season': season, 'episode': episode}))
        season_info = get_season_metadata_tvdb(show_info, show[season], banners=False)
        episode_info = get_episode_metadata_tvdb(season_info, show[season][episode])
        action_play({
            'label': episode_info['title'],
            'path': link,
            'info': episode_info,
            'is_playable': True,
            'info_type': 'video',
            'thumbnail': episode_info['poster'],
            'poster': episode_info['poster'],
            'properties' : {'fanart_image' : episode_info['fanart']},
        })

def tmdb_play_episode(id, season, episode, mode):
    tried = "tvdb"
    import_tmdb()
    id = int(id)
    season = int(season)
    episode = int(episode)
    dbid = xbmc.getInfoLabel("ListItem.DBID")
    try: dbid = int(dbid)
    except: dbid = None
    show = tmdb.TV(id).info(language=LANG, append_to_response="external_ids,images,similar,videos")
    if 'first_air_date' in show and show['first_air_date'] != None: year = show['first_air_date'][:4]
    else: year = None
    trakt_ids = get_trakt_ids("tmdb", id)
    if "status_code" in show: return trakt_play_episode(trakt_ids["trakt"], season, episode, mode)
    if 'name' in show: title = show['name']
    else: title = None
    show_info = get_tvshow_metadata_tmdb(show)
    title = show_info['name']
    preason = tmdb.TV_Seasons(id, season).info(language=LANG, append_to_response="external_ids,images,similar,videos")
    if "The resource you requested could not be found" in str(preason): return trakt_play_episode(trakt_ids["trakt"], season, episode, mode)
    season_info = get_season_metadata_tmdb(show_info, preason)
    prepisode = tmdb.TV_Episodes(id, season, episode).info(language=LANG, append_to_response="external_ids,images,similar,videos")
    if prepisode == "{u'status_code': 34, u'status_message': u'The resource you requested could not be found.'}": return trakt_play_episode(trakt_ids["tmdb"], season, episode, mode)
    episode_info = get_episode_metadata_tmdb(season_info, prepisode)
    if show_info['poster'] != None and show_info['poster'] != "": show_poster = show_info['poster']
    else: show_poster = ""
    if show_info['fanart'] != None and show_info['fanart'] != "": show_fanart = show_info['fanart']
    else: show_fanart = ""
    episodes = preason['episodes']
    items = []
    if mode == 'select': play_plugin = ADDON_SELECTOR.id
    elif mode == 'context': play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_CONTEXT, unicode)
    elif mode == 'library':
        play_plugin = get_tv_player_plugin_from_library(id)
        if not play_plugin or play_plugin == "default": play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    elif mode == 'default': play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER, unicode)
    else: play_plugin = mode
    if mode == 'default' or mode == 'select': players = active_players("tvshows")
    else: players = get_players("tvshows")
    players = [p for p in players if p.id == play_plugin] or players
    if not players: return xbmc.executebuiltin( "Action(Info)")
    trakt_ids = get_trakt_ids("tmdb", id, show_info['name'], "show", show['first_air_date'][:4])
    params = {}
    for lang in get_needed_langs(players):
        if show['name'] is None: continue
        episode_parameters = get_tmdb_episode_parameters(show, preason, prepisode)
        if episode_parameters is not None: params[lang] = episode_parameters
        else:
            if trakt_ids["trakt"] != None and trakt_ids["trakt"] != "":
                return trakt_play_episode(trakt_ids["trakt"], season, episode, mode)
            else:
                msg = "{0} {1} - S{2}E{3}".format(_("No TMDb information found for"), show_info['name'], season, episode)
                dialogs.ok(_("%s not found") % _("Episode information"), msg)
                return
        if trakt_ids != None: params[lang].update(trakt_ids)
        params[lang]['info'] = show_info
        params[lang] = to_unicode(params[lang])
    link = on_play_video(mode, players, params, trakt_ids)
    if link:
        set_property("data", json.dumps({'dbid': dbid, 'tmdb': id, 'season': season, 'episode': episode}))
        episode_metadata = get_episode_metadata_tmdb(season_info, prepisode)
        action_play({
            'label': episode_info['title'],
            'path': link,
            'info': [],
            'is_playable': True,
            'info_type': 'video',
            'thumbnail': episode_info['poster'],
            'poster': episode_info['poster'],
            'properties' : {'fanart_image' : str(show_info['fanart'])},
        })

def trakt_play_episode(id, season, episode, mode):
    from trakt import trakt
    id = int(id)
    season = int(season)
    episode = int(episode)
    show = None
    preason = None
    prepisode = None
    dbid = xbmc.getInfoLabel("ListItem.DBID")
    try: dbid = int(dbid)
    except: dbid = None
    show = trakt.get_show(id)
    if 'name' in show: show_title = show['name']
    elif 'title' in show: show_title = show['title']
    if show:
        if show['first_aired']: year = show['first_aired'][:4]
        else: year = None
        trakt_ids = get_trakt_ids("trakt", id, show_title, "show", year)
        preason = trakt.get_season(id, season)
        if preason:
            prepisode = trakt.get_episode(id, season, episode)
        elif not preason and season > 1900: 
            seasons = trakt.get_seasons(id)
            for item in seasons:
                if item['first_aired'] != None:
                    if int(item['first_aired'][:4]) == season: 
                        season_number = item['number']
                        preason = trakt.get_season(id, season_number)
    if not prepisode or not preason or not show: return tvmaze_play_episode(show_title, season, episode, mode)
    show_info = get_tvshow_metadata_trakt(show)
    season_info = get_season_metadata_trakt(show_info, preason)
    episode_info = get_episode_metadata_trakt(season_info, prepisode)
    title = show_info['name']
    if show_info['poster'] != None and show_info['poster'] != "": show_poster = show_info['poster']
    else: show_poster = ""
    if show_info['fanart'] != None and show_info['fanart'] != "": show_fanart = show_info['fanart']
    else: show_fanart = ""
    items = []
    if mode == 'select': play_plugin = ADDON_SELECTOR.id
    elif mode == 'context': play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_CONTEXT, unicode)
    elif mode == 'library':
        play_plugin = get_tv_player_plugin_from_library(id)
        if not play_plugin or play_plugin == "default": play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    elif mode == 'default': play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER, unicode)
    else: play_plugin = mode
    if mode == 'default' or mode == 'select': players = active_players("tvshows")
    else: players = get_players("tvshows")
    players = [p for p in players if p.id == play_plugin] or players
    if not players: return xbmc.executebuiltin( "Action(Info)")
    params = {}
    for lang in get_needed_langs(players):
        if show['name'] is None: continue
        episode_parameters = get_trakt_episode_parameters(show, preason, prepisode)
        if episode_parameters is not None: params[lang] = episode_parameters
        else:
            if trakt_ids["tmdb"] != None and trakt_ids["tmdb"] != "" and tried != "tmdb": 
                tried = "tmdb"
                return tvdb_play_episode(trakt_ids["tvdb"], season, episode, mode)
            elif tried == "tmdb":
                msg = "{0} {1} - S{2}E{3}".format(_("No TVDb or TMDb information found for"), show_info['name'], season, episode)
                dialogs.ok(_("%s not found") % _("Episode information"), msg)
                return
            else:
                msg = "{0} {1} - S{2}E{3}".format(_("No TMDb information found for"), show_info['name'], season, episode)
                dialogs.ok(_("%s not found") % _("Episode information"), msg)
                return
        if trakt_ids != None: params[lang].update(trakt_ids)
        params[lang]['info'] = show_info
        params[lang] = to_unicode(params[lang])
    link = on_play_video(mode, players, params, trakt_ids)
    if link:
        set_property("data", json.dumps({'dbid': dbid, 'trakt': id, 'season': season, 'episode': episode}))
        episode_metadata = get_episode_metadata_trakt(season_info, prepisode)
        action_play({
            'label': episode_info['title'],
            'path': link,
            'info': episode_info,
            'is_playable': True,
            'info_type': 'video',
            'thumbnail': episode_info['poster'],
            'poster': episode_info['poster'],
            'properties' : {'fanart_image' : str(show_info['fanart'])},
        })

def tvmaze_play_episode(id, season, episode, mode, title=None):
    title = ""
    try: id = int(id)
    except: title = id
    if title and title != "":
        url = "http://api.tvmaze.com/search/shows?q=%s" % id
        response = urllib.urlopen(url)
        shows = json.loads(response.read())
        if len(shows) > 0:
            show = shows[0]
            id = show['show']['id']
    url = "http://api.tvmaze.com/shows/%d?embed[]=seasons&embed[]=episodes" % int(id)
    response = urllib.urlopen(url)
    show = json.loads(response.read())
    season = int(season)
    episode = int(episode)
    dbid = xbmc.getInfoLabel("ListItem.DBID")
    try: dbid = int(dbid)
    except: dbid = None
    if show['externals']:
        if show['externals']['thetvdb']: trakt_ids = get_trakt_ids("tvdb", show['externals']['thetvdb'], show['name'], "show", show['premiered'][:4])
        elif show['externals']['imdb']: trakt_ids = get_trakt_ids("imdb", show['externals']['imdb'], show['name'], "show", show['premiered'][:4])
        else: trakt_ids = get_trakt_ids(query=show['name'], type="show", year=show['premiered'][:4])
    else: trakt_ids = get_trakt_ids(query=show['name'], type="show", year=show['premiered'][:4])
    show_info = get_tvshow_metadata_tvmaze(show)
    preasons = show['_embedded']['seasons']
    for item in preasons:
        if item['number'] == season: 
            preason = item
            season = preasons.index(item) + 1
        elif item['premiereDate'] and item['endDate']:
            if int(item['premiereDate'][:4]) <= season and int(item['endDate'][:4]) >= season: 
                preason = item
                season = preasons.index(item) + 1
    prepisodes = show['_embedded']['episodes']
    for item in prepisodes:
        if item['number'] == episode: prepisode = item
    season_info = get_season_metadata_tvmaze(show_info, preason)
    episode_info = get_episode_metadata_tvmaze(season_info, prepisode)
    if show_info['poster'] != None and show_info['poster'] != "": show_poster = show_info['poster']
    else: show_poster = ""
    if show_info['fanart'] != None and show_info['fanart'] != "": show_fanart = show_info['fanart']
    else: show_fanart = ""
    items = []
    if mode == 'select': play_plugin = ADDON_SELECTOR.id
    elif mode == 'context': play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_CONTEXT, unicode)
    elif mode == 'library':
        play_plugin = get_tv_player_plugin_from_library(id)
        if not play_plugin or play_plugin == "default": play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER_FROM_LIBRARY, unicode)
    elif mode == 'default': play_plugin = plugin.get_setting(SETTING_TV_DEFAULT_PLAYER, unicode)
    else: play_plugin = mode
    if mode == 'default' or mode == 'select': players = active_players("tvshows")
    else: players = get_players("tvshows")
    players = [p for p in players if p.id == play_plugin] or players
    if not players: return xbmc.executebuiltin( "Action(Info)")
    params = {}
    for lang in get_needed_langs(players):
        if show['name'] is None: continue
        episode_parameters = get_tvmaze_episode_parameters(show, preason, prepisode)
        if episode_parameters is not None: params[lang] = episode_parameters
        else:
            if trakt_ids["tmdb"] != None and trakt_ids["tmdb"] != "" and tried != "tmdb": 
                tried = "tmdb"
                return tvdb_play_episode(trakt_ids["tvdb"], season, episode, mode)
            elif tried == "tmdb":
                msg = "{0} {1} - S{2}E{3}".format(_("No TVDb or TMDb information found for"), show_info['name'], season, episode)
                dialogs.ok(_("%s not found") % _("Episode information"), msg)
                return
            else:
                msg = "{0} {1} - S{2}E{3}".format(_("No TMDb information found for"), show_info['name'], season, episode)
                dialogs.ok(_("%s not found") % _("Episode information"), msg)
                return
        if trakt_ids != None: params[lang].update(trakt_ids)
        params[lang]['info'] = show_info
        params[lang] = to_unicode(params[lang])
    link = on_play_video(mode, players, params, trakt_ids)
    if link:
        set_property("data", json.dumps({'dbid': dbid, 'tvdb': trakt_ids['tvdb'], 'season': season, 'episode': episode}))
        episode_metadata = get_episode_metadata_tvmaze(season_info, prepisode)
        action_play({
            'label': episode_info['title'],
            'path': link,
            'info': [],
            'is_playable': True,
            'info_type': 'video',
            'thumbnail': episode_info['poster'],
            'poster': episode_info['poster'],
            'properties' : {'fanart_image' : str(show_info['fanart'])},
        })

def get_episode_parameters(show, season, episode):
    articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
    import_tmdb()
    if season in show and episode in show[season]:
        season_obj = show[season]
        episode_obj = show[season][episode]
    else:
        return
    # Get parameters
    parameters = {'id': show['id'], 'season': season, 'episode': episode}
    show_info = get_tvshow_metadata_tvdb(show, banners=True)
    network = show.get('network', '')
    parameters['network'] = network
    if network:
        parameters['network_clean'] = re.sub("(\(.*?\))", "", network).strip()
    else:
        parameters['network_clean'] = network
    parameters['showname'] = show['seriesname'].replace("&", "%26")
    parameters['clearname'] = re.sub("(\(.*?\))", "", show['seriesname']).strip()
    parameters['stripname'] = ' '.join(re.compile('[\W_]+').sub(' ', show['seriesname']).split())
    parameters['sortname'] = to_utf8(parameters['clearname'])
    for article in articles:
        if to_utf8(parameters['clearname']).startswith(article): parameters['sortname'] = to_utf8(parameters['clearname']).replace(article,'')
    parameters['urlname'] = urllib.quote(to_utf8(parameters['clearname']))
    articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
    parameters['sortname'] = to_utf8(parameters['clearname'])
    for article in articles:
        if to_utf8(parameters['clearname']).startswith(article): parameters['sortname'] = to_utf8(parameters['clearname']).replace(article,'')
    parameters['shortname'] = to_utf8(parameters['clearname'][1:-1])
    try:
        parameters['absolute_number'] = int(episode_obj.get('absolute_number'))
    except:
        parameters['absolute_number'] = "na"
    parameters['title'] = episode_obj.get('episodename', str(episode)).replace("&", "%26")
    parameters['urltitle'] = urllib.quote(to_utf8(parameters['title']))
    parameters['sorttitle'] = to_utf8(parameters['title'])
    for article in articles:
        if to_utf8(parameters['title']).startswith(article): parameters['sorttitle'] = to_utf8(parameters['title']).replace(article,'')
    parameters['shorttitle'] = to_utf8(parameters['title'][1:-1])
    parameters['firstaired'] = episode_obj.get('firstaired')
    parameters['year'] = show.get('year', 0)
    if parameters['firstaired']:
        parameters['epyear'] = int(parameters['firstaired'].split("-")[0].strip())
        parameters['epmonth'] = int(parameters['firstaired'].split("-")[1].strip())
        parameters['epday'] = int(parameters['firstaired'].split("-")[2].strip())
    else:
        parameters["epyear"] = 1980
        parameters["epmonth"] = 0
        parameters["epday"] = 0
    parameters['imdb'] = show.get('imdb_id', '')
    parameters['epid'] = episode_obj.get('id')
    if episode_obj.get('id') != "": parameters['plot'] = episode_obj.get('overview')
    else: parameters['plot'] = show['overview']
    if episode_obj.get('Rating') != "": parameters['rating'] = episode_obj.get('Rating')
    else: parameters['rating'] = show['Rating']
    if episode_obj.get('RatingCount') != "": parameters['votes'] = episode_obj.get('RatingCount')
    else: parameters['votes'] = show['RatingCount']
    parameters['writers'] = episode_obj.get('Writer')
    parameters['directors'] = episode_obj.get('Director')
    parameters['status'] = show.get('Status')
    parameters['mpaa'] = show.get('ContentRating')
    if show.get('Actors') != None and show.get('Actors') != "": parameters['actors'] = show.get('Actors').split("|")
    else: parameters['actors'] = []
    if show.get('Genre') != None and '|' in show.get('Genre'): parameters['genres'] = show.get('Genre').replace('|',' / ')[3:-3]
    else: parameters['genres'] = show.get('Genre')
    parameters['runtime'] = show['runtime']
    parameters['duration'] = int(show['runtime']) * 60
    tvdb_base = "http://thetvdb.com/banners/"
    if episode_obj.get('filename') != "": parameters['thumbnail'] = tvdb_base + str(episode_obj.get('filename'))
    elif show.get('poster') != "": parameters['thumbnail'] = tvdb_base + show.get('poster')
    else: parameters['thumbnail'] = get_icon("metalliq")
    if show.get('poster') != "": parameters['poster'] = tvdb_base + show.get('poster')
    else: parameters['poster'] = get_icon("metalliq")
    parameters['thumbnail'] = "http://thetvdb.com/banners/episodes/" + str(show['id']) + "/" + str(parameters['epid']) + ".jpg"
    if show.get('banner') != "": parameters['banner'] = tvdb_base + show.get('banner')
    else: parameters['banner'] = get_banner_path()
    if show.get('fanart') != None and show.get('fanart') != "": parameters['fanart'] = tvdb_base + show.get('fanart')
    else: parameters['fanart'] = get_background_path()
    is_anime = False
    if parameters['genres'] != None and parameters['absolute_number'] and parameters['absolute_number'] != '0' and "animation" in parameters['genres'].lower():
        tmdb_results = tmdb.Find(show['id']).info(external_source="tvdb_id")
        for tmdb_show in tmdb_results.get("tv_results", []):
            if "JP" in tmdb_show['origin_country']:
                is_anime = True
    if is_anime:
        parameters['name'] = u'{showname} {absolute_number}'.format(**parameters)
    else:
        parameters['name'] = u'{showname} S{season:02d}E{episode:02d}'.format(**parameters)
    parameters['now'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    trakt_ids = get_trakt_ids("tvdb", show['id'], parameters['clearname'], "show", parameters['year'])
    if "slug" in trakt_ids:
        if trakt_ids["slug"] != "" and trakt_ids["slug"] != None:
            parameters['slug'] = trakt_ids["slug"]
        else:
            parameters['slug'] = parameters['clearname'].lower().replace('~','').replace('#','').replace('%','').replace('&','').replace('*','').replace('{','').replace('}','').replace('\\','').replace(':','').replace('<','').replace('>','').replace('?','').replace('/','').replace('+','').replace('|','').replace('"','').replace(" ","-")
    return parameters

def get_tmdb_episode_parameters(show, preason, prepisode):
    if "status_code" in str(prepisode): return None
    parameters = {'id': show['external_ids']['tvdb_id'], 'season': preason['season_number'], 'episode': prepisode['episode_number']}
    network = show['networks'][0]['name']
    parameters['network'] = network
    if network: parameters['network_clean'] = re.sub("(\(.*?\))", "", network).strip()
    else: parameters['network_clean'] = network
    parameters['imdb'] = show['external_ids']['imdb_id']
    parameters['tmdb'] = show['id']
    parameters['showname'] = show['name']
    parameters['clearname'] = re.sub("(\(.*?\))", "", show['name']).strip()
    parameters['urlname'] = urllib.quote(to_utf8(parameters['clearname']))
    articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
    parameters['sortname'] = to_utf8(parameters['clearname'])
    for article in articles:
        if to_utf8(parameters['clearname']).startswith(article): parameters['sortname'] = to_utf8(parameters['clearname']).replace(article,'')
    parameters['shortname'] = to_utf8(parameters['clearname'][1:-1])
    parameters['absolute_number'] = "na"
    parameters['title'] = prepisode['name']
    parameters['urltitle'] = urllib.quote(to_utf8(parameters['title']))
    parameters['sorttitle'] = to_utf8(parameters['title'])
    articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
    for article in articles:
        if to_utf8(parameters['title']).startswith(article): parameters['sorttitle'] = to_utf8(parameters['title']).replace(article,'')
    parameters['shorttitle'] = to_utf8(parameters['title'][1:-1])
    parameters['firstaired'] = prepisode['air_date']
    parameters['year'] = int(show['first_air_date'].split("-")[0].strip())
    if parameters['firstaired']:
        parameters['epyear'] = int(parameters['firstaired'].split("-")[0].strip())
        parameters['epmonth'] = int(parameters['firstaired'].split("-")[1].strip())
        parameters['epday'] = int(parameters['firstaired'].split("-")[2].strip())
    else:
        parameters["epyear"] = 1900
        parameters["epmonth"] = 0
        parameters["epday"] = 0
    parameters['epid'] = prepisode['id']
    if preason['episodes'][0] != None and preason['episodes'][0] != "" and preason['episodes'][0] != []:
        parameters['poster'] = u'%s%s' % ("http://image.tmdb.org/t/p/w500", preason['episodes'][0]['still_path'])
    elif show['poster_path'] != None and show['poster_path'] != "" and show['poster_path'] != []:
        parameters['poster'] = u'%s%s' % ("http://image.tmdb.org/t/p/w500", show['poster_path'])
    if show['backdrop_path'] != None and show['backdrop_path'] != "" and show['backdrop_path'] != []:
        parameters['fanart'] = u'%s%s' % ("http://image.tmdb.org/t/p/original", show['backdrop_path'])
    else: parameters['fanart'] = ""
    parameters['thumbnail'] = parameters['poster']
    parameters['icon'] = parameters['poster']
    try: genre = [x for x in show['genre'].split('|') if not x == '']
    except: genre = []
    parameters['genre'] = " / ".join(genre)
    if "JP" in show['origin_country']: is_anime = True
    else: is_anime = False
    if is_anime: parameters['name'] = u'{showname} {absolute_number}'.format(**parameters)
    else: parameters['name'] = u'{showname} S{season:02d}E{episode:02d}'.format(**parameters)
    parameters['now'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    return parameters

def get_trakt_episode_parameters(show, preason, prepisode):
    if "status_code" in str(prepisode): return None
    parameters = {'id': show['external_ids']['tvdb_id'], 'season': preason['season_number'], 'episode': prepisode['episode_number']}
    network = show['networks'][0]['name']
    parameters['network'] = network
    if network: parameters['network_clean'] = re.sub("(\(.*?\))", "", network).strip()
    else: parameters['network_clean'] = network
    parameters['imdb'] = show['external_ids']['imdb_id']
    parameters['tmdb'] = show['id']
    parameters['showname'] = show['name']
    parameters['clearname'] = re.sub("(\(.*?\))", "", show['name']).strip()
    parameters['urlname'] = urllib.quote(to_utf8(parameters['clearname']))
    articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
    parameters['sortname'] = to_utf8(parameters['clearname'])
    for article in articles:
        if to_utf8(parameters['clearname']).startswith(article): parameters['sortname'] = to_utf8(parameters['clearname']).replace(article,'')
    parameters['shortname'] = to_utf8(parameters['clearname'][1:-1])
    parameters['absolute_number'] = "na"
    parameters['title'] = prepisode['name']
    parameters['urltitle'] = urllib.quote(to_utf8(parameters['title']))
    parameters['sorttitle'] = to_utf8(parameters['title'])
    articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
    for article in articles:
        if to_utf8(parameters['title']).startswith(article): parameters['sorttitle'] = to_utf8(parameters['title']).replace(article,'')
    parameters['shorttitle'] = to_utf8(parameters['title'][1:-1])
    parameters['firstaired'] = prepisode['air_date']
    parameters['year'] = int(show['first_air_date'].split("-")[0].strip())
    if parameters['firstaired']:
        parameters['epyear'] = int(parameters['firstaired'].split("-")[0].strip())
        parameters['epmonth'] = int(parameters['firstaired'].split("-")[1].strip())
        parameters['epday'] = int(parameters['firstaired'].split("-")[2].strip())
    else:
        parameters["epyear"] = 1900
        parameters["epmonth"] = 0
        parameters["epday"] = 0
    parameters['epid'] = prepisode['id']
    if preason['episodes'][0] != None and preason['episodes'][0] != "" and preason['episodes'][0] != []:
        parameters['poster'] = u'%s%s' % ("http://image.tmdb.org/t/p/w500", preason['episodes'][0]['still_path'])
    elif show['poster_path'] != None and show['poster_path'] != "" and show['poster_path'] != []:
        parameters['poster'] = u'%s%s' % ("http://image.tmdb.org/t/p/w500", show['poster_path'])
    if show['backdrop_path'] != None and show['backdrop_path'] != "" and show['backdrop_path'] != []:
        parameters['fanart'] = u'%s%s' % ("http://image.tmdb.org/t/p/original", show['backdrop_path'])
    else: parameters['fanart'] = ""
    parameters['thumbnail'] = parameters['poster']
    parameters['icon'] = parameters['poster']
    try: genre = [x for x in show['genre'].split('|') if not x == '']
    except: genre = []
    parameters['genre'] = " / ".join(genre)
    if "JP" in show['origin_country']: is_anime = True
    else: is_anime = False
    if is_anime: parameters['name'] = u'{showname} {absolute_number}'.format(**parameters)
    else: parameters['name'] = u'{showname} S{season:02d}E{episode:02d}'.format(**parameters)
    parameters['now'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    return parameters

def get_tvmaze_episode_parameters(show, preason, prepisode):
    if "status_code" in str(prepisode): return None
    parameters = {'id': show['externals']['thetvdb'], 'season': preason['number'], 'episode': prepisode['number']}
    network = show['network']['name']
    parameters['network'] = network
    if network: parameters['network_clean'] = re.sub("(\(.*?\))", "", network).strip()
    else: parameters['network_clean'] = network
    parameters['imdb'] = show['externals']['imdb']
    parameters['tvrage'] = show['externals']['tvrage']
    parameters['showname'] = show['name']
    parameters['clearname'] = re.sub("(\(.*?\))", "", show['name']).strip()
    parameters['urlname'] = urllib.quote(to_utf8(parameters['clearname']))
    articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
    parameters['sortname'] = to_utf8(parameters['clearname'])
    for article in articles:
        if to_utf8(parameters['clearname']).startswith(article): parameters['sortname'] = to_utf8(parameters['clearname']).replace(article,'')
    parameters['shortname'] = to_utf8(parameters['clearname'][1:-1])
    parameters['absolute_number'] = "na"
    parameters['title'] = prepisode['name']
    parameters['urltitle'] = urllib.quote(to_utf8(parameters['title']))
    parameters['sorttitle'] = to_utf8(parameters['title'])
    articles = ['a ', 'A ', 'An ', 'an ', 'The ', 'the ']
    for article in articles:
        if to_utf8(parameters['title']).startswith(article): parameters['sorttitle'] = to_utf8(parameters['title']).replace(article,'')
    parameters['shorttitle'] = to_utf8(parameters['title'][1:-1])
    parameters['firstaired'] = prepisode['airdate']
    parameters['year'] = int(show['premiered'].split("-")[0].strip())
    if parameters['firstaired']:
        parameters['epyear'] = int(parameters['firstaired'].split("-")[0].strip())
        parameters['epmonth'] = int(parameters['firstaired'].split("-")[1].strip())
        parameters['epday'] = int(parameters['firstaired'].split("-")[2].strip())
    else:
        parameters["epyear"] = 1900
        parameters["epmonth"] = 0
        parameters["epday"] = 0
    parameters['epid'] = prepisode['id']
    if prepisode['image'] != None: parameters['poster'] = prepisode['image']['original']
    elif preason['image'] != None: parameters['poster'] = preason['image']['original']
    elif show['image'] != None: parameters['poster'] = show['image']['original']
    parameters['fanart'] = ""
    parameters['thumbnail'] = parameters['poster']
    parameters['icon'] = parameters['poster']
    parameters['genre'] = show['type']
    parameters['now'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    return parameters