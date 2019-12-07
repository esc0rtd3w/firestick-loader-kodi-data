"""
    trakt.py --- Jen Plugin for accessing trakt data
    Copyright (C) 2017, Jen

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

    Version:
        2018-10-13
            - Added customizable settings for 2 colors (COLOR1 for Movie/Show titles; COLOR2 for Season/Episode numbers as well as for "Next Page >>")
            - Updated the display for seasons (added ":" between season and season number) as well as for episodes (added season & episode number to title)
            - Updated so that season and episode numbers less than 10 are displayed as double digits with a leading "0" (example: Season 1, Episode 9 ==> S01E09).
            - Added thumbnail for "Next Page >>" (same as tmdb.py)
        2018-08-19
            - Added next page option for trakt limits urls
                http://api.trakt.tv/movies/trending?limit=25&page=1
        2018-07-02
            - Updated Clear Cache Hook
        2018-05-14
            Latest version to include with a Jen Release
            

    *** COLORS ***
        Set your desired colors for the COLOR1 & COLOR2 variables within "" on lines 237 & 238 below.
        COLOR1 is for Movie/Show titles; COLOR2 is for Season/Episode numbers as well as for "Next Page >>".
        The color values can be alphanumeric (example: red, limegreen) or Hex (example: ffff0000, FF00FF00).
        If colors are left blank, they will display as the default color set within the skin you're using.
        
        -- Note:  In order for the Color settings to work as intended, Metadata must be DISABLED in the addon settings!!!

    -------------------------------------------------------------

    Usage Examples:
	
	
	### Search ###
	
	** Returns A List Of Items Searched For From Trakt
    <dir>
      <title>Search Trakt</title>
      <trakt>search</trakt>
    </dir>
	
	
	### Movies ###
	
	** Returns A List Of Your Personal Trakt Movie Watchlist (Requires Trakt Authorization)
    <dir>
      <title>My Trakt Movie Watchlist (Authorize)</title>
      <trakt>https://api.trakt.tv/sync/watchlist/movies</trakt>
    </dir>

	** Returns A List Of Your Personal Trakt Movie Collection (Requires Trakt Authorization)
    <dir>
      <title>My Trakt Movie Collection (Authorize)</title>
      <trakt>https://api.trakt.tv/sync/collection/movies</trakt>
    </dir>
	
	** Returns The Trakt Trending Movies List
    <dir>
      <title>Trakt Trending Movies</title>
      <trakt>https://api.trakt.tv/movies/trending?limit=25&page=1</trakt>
    </dir>
	
	** Returns The Trakt Most Popular Movies List
    <dir>
      <title>Trakt Popular Movies</title>
      <trakt>https://api.trakt.tv/movies/popular?limit=25&page=1</trakt>
    </dir>
	
	** Returns The Trakt Box Office Top 10 Movies List
    <dir>
      <title>Trakt Box Office Top 10 Movies</title>
      <trakt>https://api.trakt.tv/movies/boxoffice</trakt>
    </dir>
	
	** Returns The Trakt Most Watched Movies (Last Week) List
    <dir>
      <title>Trakt Most Watched Movies (Last Week)</title>
      <trakt>https://api.trakt.tv/movies/watched/weekly?limit=25&page=1</trakt>
    </dir>
	
	** Returns The Trakt Most Collected Movies (Last Week) List
    <dir>
      <title>Trakt Most Collected Last Week</title>
      <trakt>https://api.trakt.tv/movies/collected/weekly?limit=25&page=1</trakt>
    </dir>
	
	** Returns The Trakt Most Anticipated Movies List
    <dir>
      <title>Trakt Most Anticipated</title>
      <trakt>https://api.trakt.tv/movies/anticipated?limit=25&page=1</trakt>
    </dir>
	
	** Returns A List Of Trakt Movies By Actor
    <dir>
      <title>Trakt: Bryan Cranston Movies</title>
      <trakt>https://api.trakt.tv/people/bryan-cranston/movies</trakt>			
    </dir>
	
	** Returns A List Of Trakt Movies By Actress  
    <dir>
      <title>Angelina Jolie</title>
      <trakt>https://api.trakt.tv/people/Angelina-Jolie/movies</trakt>
    </dir>

	
	### TV Shows ###

	** Returns A List Of Your Personal Trakt TV Show Watchlist (Requires Trakt Authorization)
    <dir>
      <title>My Trakt TV Show Watchlist (Authorize)</title>
      <trakt>https://api.trakt.tv/sync/watchlist/shows</trakt>
    </dir>

	** Returns A List Of Your Personal Trakt TV Show Collection (Requires Trakt Authorization)
    <dir>
      <title>My Trakt TV Show Collection (Authorize)</title>
      <trakt>https://api.trakt.tv/sync/collection/shows</trakt>
    </dir>
	
	** Returns The Trakt Trending TV Shows List
    <dir>
      <title>Trakt Trending Shows</title>
      <trakt>https://api.trakt.tv/shows/trending?limit=50&page=1</trakt>
    </dir>
	
	** Returns The Trakt Most Popular TV Shows List
    <dir>
      <title>Trakt Most Popular Shows</title>
      <trakt>https://api.trakt.tv/shows/popular?limit=50&page=1</trakt>
    </dir>
	
	** Returns The Trakt Most Watched TV Shows (Last Week) List
    <dir>
      <title>Trakt Most Watched TV Shows (Last Week)</title>
      <trakt>https://api.trakt.tv/shows/watched/weekly?limit=50&page=1</trakt>
    </dir>
	
	** Returns The Trakt Most Collected TV Shows (Last Week) List
    <dir>
      <title>Trakt Most Collected TV Shows (Last Week)</title>
      <trakt>https://api.trakt.tv/shows/collected/weekly?limit=50&page=1</trakt>
    </dir>
	
	** Returns The Trakt Most Anticipated TV Shows List
    <dir>
      <title>Trakt Most Anticipated TV Shows</title>
      <trakt>https://api.trakt.tv/shows/anticipated?limit=50&page=1</trakt>
    </dir>
	
	** Returns A List Of Trakt TV Shows By Actor

    <dir>
      <title>Trakt: Bryan Cranston Shows</title>
      <trakt>https://api.trakt.tv/people/bryan-cranston/shows</trakt>
    </dir>

	
	### Lists ###
	
	** Returns A List Of Your Personal Trakt Lists
	<dir>
      <title>My Trakt Lists</title>
      <trakt>https://api.trakt.tv/users/me/lists/</trakt>
    </dir>
	
	** Returns A List Of Your Personal Trakt Liked Lists
    <dir>
      <title>My Trakt Liked Lists</title>
      <trakt>https://api.trakt.tv/users/likes/lists</trakt>
    </dir>
	
	** Returns A List Of The Reddit Top 250 Movies
    <dir>
      <title>Reddit Top 250 (2017 Edition)</title>
      <trakt>https://api.trakt.tv/users/philrivers/lists/reddit-top-250-2017-edition/items?limit=50&page=1</trakt>
    </dir>
	
	** Returns A List Of The Rotten Tomatoes Best Movies Of 2017
    <dir>
      <title>Rotten Tomatoes: Best of 2017</title>
      <trakt>https://api.trakt.tv/users/lish408/lists/rotten-tomatoes-best-of-2017/items?limit=50&page=1</trakt>
    </dir>

    <dir>
      <title>Bryan Cranston shows Trakt</title>
      <trakt>https://api.trakt.tv/people/bryan-cranston/shows</trakt>
    </dir>

    <dir>
      <title>Search Trakt</title>
      <trakt>search</trakt>
    </dir>

    -------------------------------------------------------------

"""

import __builtin__
import pickle
import time
import urlparse
import urllib
import base64

import requests

import koding
import resources.lib.external.tmdbsimple as tmdbsimple
import xbmc,xbmcaddon,xbmcgui
from ..plugin import Plugin
from koding import route
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds
CACHE_TMDB_TIME = 3600 * 24 * 360
SKIP_TMDB_INFO = False

TRAKT_API_KEY = __builtin__.trakt_client_id
TRAKT_SECRET = __builtin__.trakt_client_secret
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
addon_name = xbmcaddon.Addon().getAddonInfo('name')
COLOR1 = ""
COLOR2 = ""


class Trakt(Plugin):
    name = "trakt"

    def process_item(self, item_xml):
        #item_xml = remove_non_ascii(item_xml)
        if "<trakt>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "trakt",
                'url': item.get("trakt", ""),
                'folder': True,
                'imdb': "0",
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "trakt_tv_show(" in item_xml:
            item = JenItem(item_xml)
            url = item.get("link", ")").replace("trakt_tv_show(", "")[:-1]
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "trakt_tv_show",
                'url': "trakt_id" + url,
                'folder': True,
                'imdb': item.get("imdb", ""),
                'content': "tvshows",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': item.get("year", ""),
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "trakt_season(" in item_xml:
            item = JenItem(item_xml)
            url = item.get("link", ")").replace("trakt_season(", "")[:-1]
            season = url.split(",")[1]
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "trakt_season",
                'url': "trakt_id" + url,
                'folder': True,
                'imdb': item.get("imdb", ""),
                'content': "seasons",
                'season': str(season),
                'episode': "0",
                'info': {},
                'year': item.get("year", ""),
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "trakt_list(" in item_xml:
            item = JenItem(item_xml)
            url = item.get("link", ")").replace("trakt_list(", "")[:-1]
            user_id, list_id = url.split(",")
            list_url = "https://api.trakt.tv/users/%s/lists/%s/items/" % (
                user_id, list_id)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "trakt",
                'url': list_url,
                'folder': True,
                'imdb': item.get("imdb", ""),
                'content': "files",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': item.get("year", ""),
                'context': {},
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item

        return False

    def clear_cache(self):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear Trakt Plugin Cache?"):
            koding.Remove_Table("trakt_plugin")


@route(mode='trakt', args=["url"])
def trakt(url):
    if url == "search":
        term = koding.Keyboard("Search For")
        url = "https://api.trakt.tv/search/movie,show,person,list?query=%s" % term
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_API_KEY
    }
    if "sync" in url or "user" in url or "recommendations" in url:
        if "list" not in url or "/me/" in url or "like" in url or "sync" in url:
            auth = authenticate()
            if auth:
                headers['Authorization'] = 'Bearer ' + auth
            else:
                return ""
    pages = None
    xml, __builtin__.content_type = fetch_from_db(url) or (None, None)

    if not xml:
        xml = ""
        response = requests.get(url, headers=headers)
        response_headers = response.headers
        response = response.json()

        page = response_headers.get("X-Pagination-Page", "")

        if page:
            pages = response_headers.get("X-Pagination-Page-Count")
            response = (response, pages)

        if type(response) == tuple:  # paginated
            pages = response[1]
            response = response[0]

        __builtin__.content_type = "files"
        if type(response) == dict:
            if "people" in url:
                for job in response:
                    for item in response[job]:
                        if "movie" in item:
                            xml += get_movie_xml(item["movie"])
                            __builtin__.content_type = "movies"
                        elif "show" in item:
                            xml += get_show_xml(item["show"])
                            __builtin__.content_type = "tvshows"

        elif type(response) == list:
            for item in response:
                if "/search/" in url:
                    xml += get_search_xml(item)
                elif "lists" in url:
                    if "items" not in url and "likes" not in url:
                        user_id = url.split("/")[4]
                        xml += get_lists_xml(item, user_id)
                    if "likes/lists" in url:
                        xml += get_likes_xml(item)
                if "movie" in item:
                    xml += get_movie_xml(item["movie"])
                    __builtin__.content_type = "movies"
                elif "show" in item:
                    xml += get_show_xml(item["show"])
                    __builtin__.content_type = "tvshows"
                elif "person" in item:
                    xml += get_person_xml(item)
                else:  # one of the annoying types
                    if "movies" in url:
                        xml += get_movie_xml(item)
                        __builtin__.content_type = "movies"
                    elif "shows" in url and "season" not in url:
                        xml += get_show_xml(item)
                        __builtin__.content_type = "tvshows"
        if pages:
            if 'limit' in url:
                link, page = url.split('&page=')
                page = int(page)
                next_page = page + 1
                next_url = '%s&page=%s' % (link, next_page)

            else:
                splitted = url.split("?")
                if len(splitted) > 1:
                    args = urlparse.parse_qs(splitted[1])
                    page = int(args.get("page", [1])[0])
                    if not args.get("page", ""):
                        args["page"] = 2
                    else:
                        args["page"] = str(page + 1)
                    next_url = "%s?%s" % (splitted[0], urllib.urlencode(args))
                else:
                    page = 1
                    next_url = urlparse.urljoin(splitted[0], "?page=2")

            if not COLOR2 == "":
                myPage = "[COLOR %s]Next Page >>[/COLOR]" % COLOR2
            else:
                myPage = "Next Page >>"
            xml += "<dir>\n"\
                   "\t<title>%s</title>\n"\
                   "\t<trakt>%s</trakt>\n"\
                   "\t<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>\n"\
                   "\t<summary>Go To Page %s</summary>\n"\
                   "</dir>" % (myPage, next_url, page + 1)
        xml = remove_non_ascii(xml)
        save_to_db((xml, __builtin__.content_type), url)

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), __builtin__.content_type)


@route(mode='trakt_tv_show', args=["url"])
def trakt_tv_show(trakt_id):
    __builtin__.content_type = "seasons"
    splitted = trakt_id.replace("trakt_id", "").split(",")
    trakt_id = splitted[0]
    year = splitted[1]
    tvtitle = ",".join(splitted[2:-2])
    tmdb = splitted[-2]
    imdb = splitted[-1]
    url = "https://api.trakt.tv/shows/%s/seasons" % trakt_id
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_API_KEY
    }
    xml, __builtin__.content_type = fetch_from_db(url) or (None, None)
    if not xml:
        xml = ""
        __builtin__.content_type = "seasons"
        response = requests.get(url, headers=headers).json()

        if type(response) == list:
            for item in response:
                xml += get_season_xml(item, trakt_id, year, tvtitle, tmdb,
                                      imdb)
            xml = remove_non_ascii(xml)
            save_to_db((xml, __builtin__.content_type), url)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), __builtin__.content_type)


@route(mode='trakt_season', args=["url"])
def trakt_season(slug):
    __builtin__.content_type = "episodes"
    splitted = slug.replace("trakt_id", "").split(",")
    trakt_id = splitted[0]
    season = splitted[1]
    year = splitted[2]
    tvtitle = ",".join(splitted[3:-2])
    tmdb = splitted[-2]
    imdb = splitted[-1]
    url = "https://api.trakt.tv/shows/%s/seasons/%s?extended=full"
    url = url % (trakt_id, season)
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': TRAKT_API_KEY
    }
    xml, __builtin__.content_type = fetch_from_db(url) or (None, None)
    if not xml:
        __builtin__.content_type = "episodes"
        xml = ""
        response = requests.get(url, headers=headers).json()

        if type(response) == list:
            for item in response:
                xml += get_episode_xml(item, trakt_id, year, tvtitle, tmdb,
                                       imdb)
            xml = remove_non_ascii(xml)
            save_to_db((xml, __builtin__.content_type), url)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), __builtin__.content_type)


def get_movie_xml(item):
    if "movie" in item:
        item = item["movie"]
    title = remove_non_ascii(item["title"])
    year = item["year"]
    imdb = item["ids"]["imdb"]
    tmdb = item["ids"]["tmdb"]
    info = fetch_from_db("tmdb/%s/movie" % (tmdb))
    if not info:
        if not SKIP_TMDB_INFO and tmdb:
            info = tmdbsimple.Movies(tmdb).info()
            new_info = {
                "poster_path": info.get("poster_path", ""),
                "backdrop_path": info.get("backdrop_path", "")
            }
            save_to_db(new_info, "tmdb/%s/movie" % (tmdb))
        else:
            info = {}
    if info.get("poster_path"):
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + info["poster_path"]
    else:
        thumbnail = ""
    if info.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + info["backdrop_path"]
    else:
        fanart = ""
    #name = title + " (" + year + ")"
    if not COLOR1 == "":
        name = "[COLOR %s]%s[/COLOR]" % (COLOR1, title)
    else:
        name = title
    xml = "<item>" \
          "<title>%s</title>" \
          "<meta>" \
          "<content>movie</content>" \
          "<imdb>%s</imdb>" \
          "<title>%s</title>" \
          "<year>%s</year>" \
          "</meta>" \
          "<link>" \
          "<sublink>search</sublink>" \
          "<sublink>searchsd</sublink>" \
          "</link>" \
          "<thumbnail>%s</thumbnail>" \
          "<fanart>%s</fanart>" \
          "</item>" % (name, imdb, title, year, thumbnail, fanart)
    return xml


def get_show_xml(item):
    if "show" in item:
        item = item["show"]
    title = remove_non_ascii(item["title"])
    year = item["year"]
    imdb = item["ids"]["imdb"]
    trakt_id = item["ids"]["trakt"]
    tmdb = item["ids"]["tmdb"]
    info = fetch_from_db("tmdb/%s/show" % (tmdb))
    if not info:
        if not SKIP_TMDB_INFO and tmdb:
            info = tmdbsimple.TV(tmdb).info()
            new_info = {
                "poster_path": info.get("poster_path", ""),
                "backdrop_path": info.get("backdrop_path", "")
            }
            save_to_db(new_info, "tmdb/%s/show" % (tmdb))
        else:
            info = {}
    if info.get("poster_path", ""):
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + info["poster_path"]
    else:
        thumbnail = ""
    if info.get("backdrop_path", ""):
        fanart = str("https://image.tmdb.org/t/p/w1280" +
                     info["backdrop_path"])
    else:
        fanart = ""
    #name = title + " (" + year + ")"
    if not COLOR1 == "":
        name = "[COLOR %s]%s[/COLOR]" % (COLOR1, title)
    else:
        name = title
    xml = "<dir>"\
          "<title>%s</title>"\
          "<meta>"\
          "<content>tvshow</content>"\
          "<imdb>%s</imdb>"\
          "<tvshowtitle>%s</tvshowtitle>"\
          "<year>%s</year>"\
          "</meta>"\
          "<link>trakt_tv_show(%s, %s, %s, %s, %s)</link>"\
          "<thumbnail>%s</thumbnail>" \
          "<fanart>%s</fanart>" \
          "</dir>" % (name, imdb, title, year, trakt_id, year, title, tmdb,
                      imdb, thumbnail, fanart)
    return xml


def get_season_xml(item, trakt_id, year, tvtitle, tmdb, imdb):
    imdb = imdb.lstrip()
    tmdb = tmdb.lstrip()
    season = item["number"]
    if season == 0:
        return ""
    info = fetch_from_db("tmdb/%s/%s" % (tmdb, season))
    if not info:
        if not SKIP_TMDB_INFO and tmdb:
            info = tmdbsimple.TV_Seasons(tmdb, season).info()
            show_info = fetch_from_db("tmdb/%s/show" % (tmdb))
            if not show_info:
                show_info = {}
            new_info = {
                "poster_path": info.get("poster_path", ""),
                "backdrop_path": show_info.get("backdrop_path", "")
            }
            save_to_db(new_info, "tmdb/%s/%s" % (tmdb, season))
        else:
            info = {}
    if info.get("poster_path", ""):
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + info["poster_path"]
    else:
        thumbnail = ""
    if info.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + info["backdrop_path"]
    else:
        fanart = ""
    if not COLOR1 == "" and not COLOR2 == "":
        name = "[COLOR %s]Season: [COLOR %s]%s[/COLOR]" % (COLOR1, COLOR2, season)
    else:
        name = "Season: %s" % (season)
    xml = "<dir>"\
          "<title>%s</title>"\
          "<meta>"\
          "<imdb>%s</imdb>"\
          "<content>season</content>"\
          "<season>%s</season>"\
          "</meta>"\
          "<link>trakt_season(%s,%s, %s, %s, %s, %s)</link>"\
          "<thumbnail>%s</thumbnail>" \
          "<fanart>%s</fanart>" \
          "</dir>" % (name, imdb, season, trakt_id, season, year,
                      tvtitle, tmdb,
                      imdb, thumbnail, fanart)
    return xml


def get_episode_xml(item, trakt_id, year, tvtitle, tmdb, imdb):
    imdb = imdb.lstrip()
    title = item["title"]
    premiered = item.get("first_aired", "")
    if premiered:
        premiered = premiered.split("T")[0]
    else:
        premiered = ""
    season = item["season"]
    episode = item["number"]
    info = fetch_from_db("tmdb/%s/%s/%s" % (tmdb, season, episode))
    if not info:
        if not SKIP_TMDB_INFO and tmdb:
            info = tmdbsimple.TV_Episodes(tmdb, season, episode).info()
            show_info = fetch_from_db("tmdb/%s/show" % (tmdb))
            if not show_info:
                show_info = {}
            new_info = {
                "still_path": info.get("still_path", ""),
                "backdrop_path": show_info.get("backdrop_path", "")
            }
            save_to_db(new_info, "tmdb/%s/%s/%s" % (tmdb, season, episode))
        else:
            info = {}
    if info.get("still_path", ""):
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + info["still_path"]
    else:
        thumbnail = ""
    if info.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + info["backdrop_path"]
    else:
        fanart = ""
    if int(season) > 0 and int(season) < 10:
        mySeason = "0" + str(season)
    else:
        mySeason = str(season)
    if int(episode) > 0 and int(episode) < 10:
        myEpisode = "0" + str(episode)
    else:
        myEpisode = str(episode)
    if not COLOR1 == "" and not COLOR2 == "":
        name = "[COLOR %s]S%sE%s[/COLOR] - [COLOR %s]%s[/COLOR]" % (COLOR2, mySeason, myEpisode, COLOR1, title)
    else:
        name = "S%sE%s - %s" % (mySeason, myEpisode, title)
    xml = "<item>"\
          "<title>%s</title>"\
          "<meta>"\
          "<content>episode</content>"\
          "<imdb>%s</imdb>"\
          "<tvshowtitle>%s</tvshowtitle>"\
          "<year>%s</year>"\
          "<title>%s</title>"\
          "<premiered>%s</premiered>"\
          "<season>%s</season>"\
          "<episode>%s</episode>"\
          "</meta>"\
          "<link>"\
          "<sublink>search</sublink>"\
          "<sublink>searchsd</sublink>"\
          "</link>"\
          "<thumbnail>%s</thumbnail>"\
          "<fanart>%s</fanart>"\
          "</item>" % (name, imdb, tvtitle, year, title,
                                   premiered, season, episode, thumbnail, fanart)
    return xml


def get_lists_xml(item, user_id):
    title = item["name"]
    trakt_id = item["ids"]["trakt"]
    summary = item["description"]
    xml = "<dir>"\
          "<title>%s</title>"\
          "<link>trakt_list(%s, %s)</link>"\
          "<summary>%s</summary"\
          "</dir>" % (title, user_id, trakt_id, summary)
    return xml


def get_likes_xml(item):
    title = remove_non_ascii(item["list"]["name"])
    trakt_id = item["list"]["ids"]["trakt"]
    user_id = item["list"]["user"]["ids"]["slug"]
    summary = item["list"]["description"]
    xml = "<dir>"\
          "<title>%s</title>"\
          "<link>trakt_list(%s, %s)</link>"\
          "<summary>%s</summary"\
          "</dir>" % (title, user_id, trakt_id, summary)
    return xml


def get_search_xml(item):
    xml = ""
    itemtype = item["type"]
    if itemtype == "movie":
        xml += get_movie_xml(item["movie"])
    elif itemtype == "show":
        xml += get_show_xml(item["show"])
    elif itemtype == "list":
        userslug = item["list"]["user"]["ids"]["slug"]
        username = item["list"]["user"]["username"]
        listname = item["list"]["name"]
        title = "%s's %s List" % (username.capitalize(), listname.capitalize())
        slug = item["list"]["ids"]["slug"]
        xml += "<dir>\n"\
               "\t<title>%s</title>\n"\
               "\t<trakt>https://api.trakt.tv/users/%s/lists/%s/items</trakt>\n"\
               "</dir>\n\n" % (title, userslug, slug)

    elif itemtype == "person":
        name = item["person"]["name"]
        slug = item["person"]["ids"]["slug"]
        xml += "<dir>\n"\
               "\t<title>%s Movies Trakt</title>\n"\
               "\t<trakt>https://api.trakt.tv/people/%s/movies</trakt>\n"\
               "</dir>\n\n" % (name, slug)

        xml += "<dir>\n"\
               "\t<title>%s Shows Trakt</title>\n"\
               "\t<trakt>https://api.trakt.tv/people/%s/shows</trakt>\n"\
               "</dir>\n\n" % (name, slug)
    return xml


def get_person_xml(item):
    xml = ""
    name = item["person"]["name"]
    slug = item["person"]["ids"]["slug"]
    xml += "<dir>\n"\
           "\t<title>%s Movies</title>\n"\
           "\t<trakt>https://api.trakt.tv/people/%s/movies</trakt>\n"\
           "</dir>\n\n" % (name, slug)
    xml += "<dir>\n"\
           "\t<title>%s Shows</title>\n"\
           "\t<trakt>https://api.trakt.tv/people/%s/shows</trakt>\n"\
           "</dir>\n\n" % (name, slug)
    return xml


def authenticate():
    addon = xbmcaddon.Addon()
    access_token = addon.getSetting("TRAKT_ACCESS_TOKEN")
    if access_token:
        expires = addon.getSetting("TRAKT_EXPIRES_AT")
        if time.time() > expires:
            return trakt_refresh_token()
        return access_token
    values = {"client_id": TRAKT_API_KEY}

    device_codes = requests.post(
        'https://api.trakt.tv/oauth/device/code', data=values).json()
    data = {
        "code": device_codes["device_code"],
        "client_id": TRAKT_API_KEY,
        "client_secret": TRAKT_SECRET
    }

    start = time.time()
    expires_in = device_codes["expires_in"]
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create(
        "Authenticate Trakt",
        "Please go to https://trakt.tv/activate and enter the code",
        str(device_codes["user_code"]))
    try:
        time_passed = 0
        while not xbmc.abortRequested and not progress_dialog.iscanceled(
        ) and time_passed < expires_in:
            try:
                response = requests.post(
                    'https://api.trakt.tv/oauth/device/token',
                    data=data).json()
            except Exception, e:
                progress = int(100 * time_passed / expires_in)
                progress_dialog.update(progress)
                xbmc.sleep(max(device_codes["interval"], 1) * 1000)
            else:
                response = response
                expires_at = time.time() + 60 * 60 * 24 * 30
                addon.setSetting("TRAKT_EXPIRES_AT", str(expires_at))
                addon.setSetting("TRAKT_ACCESS_TOKEN",
                                 response["access_token"])
                addon.setSetting("TRAKT_REFRESH_TOKEN",
                                 response["refresh_token"])
                return response["access_token"]
            time_passed = time.time() - start
    finally:
        progress_dialog.close()
        del progress_dialog
    return None


def trakt_refresh_token():
    addon = xbmcaddon.Addon()
    refresh_token = addon.getSetting("TRAKT_REFRESH_TOKEN")
    data = {
        "client_id": TRAKT_API_KEY,
        "client_secret": TRAKT_SECRET,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(
        'https://api.trakt.tv/oauth/token', data=data).json()
    if response:
        expires_at = time.time() + 60 * 60 * 24 * 30
        addon.setSetting("TRAKT_EXPIRES_AT", str(expires_at))
        addon.setSetting("TRAKT_ACCESS_TOKEN", response["access_token"])
        addon.setSetting("TRAKT_REFRESH_TOKEN", response["refresh_token"])
        return response["access_token"]


def remove_non_ascii(text):
    return unidecode(unicode(text))


def save_to_db(item, url):
    if not item or not url:
        return False
    if type(item) == tuple:
        content_type = item[1]
        item = item[0]
    else:
        content_type = None
    item = remove_non_ascii(item)
    koding.reset_db()
    koding.Remove_From_Table("trakt_plugin", {"url": url})

    koding.Add_To_Table("trakt_plugin", {
        "url": url,
        "item": base64.b64encode(pickle.dumps(item)),
        "content_type": content_type,
        "created": time.time()
    })


def fetch_from_db(url):
    koding.reset_db()
    trakt_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "content_type": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("trakt_plugin", trakt_plugin_spec)
    match = koding.Get_From_Table("trakt_plugin", {"url": url})
    if match:
        match = match[0]
        if not match["item"]:
            return None
        created_time = match["created"]
        if "tmdb" in url:
            if created_time and float(
                    created_time) + CACHE_TMDB_TIME >= time.time():
                match_item = match["item"]
                try:
                    result = pickle.loads(base64.b64decode(match_item))
                except:
                    return None
                if type(result) == str and result.startswith("{"):
                    result = eval(result)
                return result
        if created_time and float(created_time) + float(CACHE_TIME) >= time.time():
            match_item = match["item"]
            try:
                content_type = match["content_type"]
                result = pickle.loads(base64.b64decode(match_item))
            except:
                return None
            return (result, content_type)
        else:
            return []
    else:
        return []
