"""
    tmdb.py --- Jen Plugin for accessing tmdb data
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


    Usage Examples:
    Returns The TMDB Popular Movies List
    <dir>
      <title>TMDB Popular</title>
      <tmdb>movies/popular</tmdb>
    </dir>

    Returns Upcoming Movies Then Trailers For The Movies.  Second Tag Must Be movie/upcoming
    <dir>
      <title>TMDB Upcoming</title>
      <tmdb>movie/upcoming</tmdb>
      <summary>Shows Trailers For Upcoming Movies</summary>
    </dir>

    Returns A List Of Now Playing Movies
    <dir>
      <title>TMDB Now Playing</title>
      <tmdb>movies/now_playing</tmdb>
    </dir>

    Returns A List Of TMDB Top Rated Movies
    <dir>
      <title>TMDB Top Rated</title>
      <tmdb>movies/top_rated</tmdb>
    </dir>

    Returns A List Of Movies By A Specific Genre.  Must Change Id At The End Of The Second Tag
    <dir>
      <title>TMDB Action Movies</title>
      <tmdb>genre/movies/28</tmdb>
    </dir>

    Returns A List Of Movies By Specific Years. Must Change Year At The End Of The Second Tag
    <dir>
      <title>Movies Released In 2014</title>
      <tmdb>year/movies/2014</tmdb>
    </dir>

    Returns A List Of Movies By Production Companies. Must Change Id At The End Of The Second Tag
    <dir>
        <title>Pixar Animation</title>
        <tmdb>company/movies/3</tmdb>
    </dir>

    Returns A List Of Movies By A Specific Keyword. Must Change Id At The End Of The Second Tag
    <dir>
      <title>TMDB Army Movies</title>
      <tmdb>keyword/movies/6092</tmdb>
    </dir>

    Returns A List Of A Specific Collection. Must Change Id At The End Of The Second Tag
    <dir>
      <title>TMDB Star Wars Collection</title>
      <tmdb>collection/10</tmdb>
    </dir>

    Returns The TMDB Popular TV Shows List
    <dir>
      <title>TMDB Popular</title>
      <tmdb>tv/popular</tmdb>
    </dir>

    Returns The TMDB Top Rated TV Shows List
    <dir>
      <title>TMDB Top Rated</title>
      <tmdb>tv/top_rated</tmdb>
    </dir>

    Returns A List Of Shows Airing Today
    <dir>
      <title>TMDB Airing Today</title>
      <tmdb>tv/today</tmdb>
    </dir>

    Returns A List Of Shows Airing In The Next 7 Days
    <dir>
      <title>TMDB On The Air</title>
      <tmdb>tv/on_the_air</tmdb>
    </dir>

    Returns A List Of Shows By Genre. Must Change Id At The End Of The Second Tag
    <dir>
      <title>TMDB Animation Shows</title>
      <tmdb>genre/shows/16</tmdb>
    </dir>

    Returns A List Of TV Shows By Network. Must Change Id At The End Of The Second Tag
    <dir>
        <title>ABC</title>
        <tmdb>network/shows/2</tmdb>
    </dir>

    Returns A List By A Specific Keyword. Must Change Id At The End Of The Second Tag
    <dir>
      <title>TMDB King Shows</title>
      <tmdb>keyword/shows/13084</tmdb>
    </dir>

    Returns A Specific TMDB List. Must Change Id At The End Of The Second Tag
    <dir>
      <title>TMDB List: Animal Kingdom</title>
      <tmdb>list/13488</tmdb>
    </dir>

    Returns The TMDB Popular People List.  Results Show Only Movie Titles Currently
    <dir>
      <title>Popular People</title>
      <tmdb>people/popular</tmdb>
    </dir>

    Returns A List Of Shows By A Person. Must Change Id At The End Of The Second Tag
    <dir>
      <title>Bryan Cranston Shows TMDB</title>
      <tmdb>person/shows/17419</tmdb>
    </dir>

    Returns A List Of Movies By A Person.  Must Change Id At The End Of The Second Tag
    <dir>
      <title>Bryan Cranston Movies TMDB</title>
      <tmdb>person/movies/17419</tmdb>
    </dir>

    Returns Movie Trailers For Any Movies You Want.  You Must Change The Id At The End Of The Second Tag
   <dir>
      <title>Star Wars: The Last Jedi TRAILER</title>
      <tmdb>trailer/181808</tmdb>
    </dir>

    Returns A List Of Items Searched For From TMDB
    <dir>
      <title>Search TMDB</title>
      <tmdb>search</tmdb>
    </dir>
"""

import __builtin__
import pickle
import base64
import time

import koding
import resources.lib.external.tmdbsimple as tmdbsimple
import xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode


CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')


class TMDB(Plugin):
    name = "tmdb"

    def process_item(self, item_xml):
        if "<tmdb>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "tmdb",
                'url': item.get("tmdb", ""),
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
        elif "tmdb_tv_show" in item_xml:
            item = JenItem(item_xml)
            url = item.get("link", ")").replace("tmdb_tv_show(", "")[:-1]
            result_item = {
                'label': item["title"],
                'icon': item["thumbnail"],
                'fanart': item.get("fanart", addon_fanart),
                'mode': "tmdb_tv_show",
                'url': "tmdb_id" + url,
                'folder': True,
                'content': "tvshows",
                'season': "0",
                'episode': "0",
                'info': {},
                "imdb": item.get("imdb", "0"),
                'year': item.get("year", ""),
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item
        elif "tmdb_season(" in item_xml:
            item = JenItem(item_xml)
            url = item.get("link", ")").replace("tmdb_season(", "")[:-1]
            season = url.split(",")[1]
            result_item = {
                'label': item["title"],
                'icon': item["thumbnail"],
                'fanart': item.get("fanart", addon_fanart),
                'mode': "tmdb_season",
                'url': "tmdb_id" + url,
                'folder': True,
                'content': "seasons",
                'season': str(season),
                'episode': "0",
                'info': {},
                "imdb": item.get("imdb", "0"),
                'year': item.get("year", ""),
                'context': {},
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item


@route(mode='tmdb', args=["url"])
def tmdb(url):
    page = 1
    try:
        xml, __builtin__.content_type = fetch_from_db(url) or (None, None)
    except Exception:
        xml, __builtin__.content_type = None, None
    if not xml:
        content = "files"
        xml = ""
        response = None
        if url.startswith("movies"):
            if url.startswith("movies/popular"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.Movies().popular(page=page)
            if url.startswith("movies/now_playing"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.Movies().now_playing(page=page)
            if url.startswith("movies/top_rated"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.Movies().top_rated(page=page)

            for item in response["results"]:
                xml += get_movie_xml(item)
                content = "movies"
        elif url.startswith("people"):
            if url.startswith("people/popular"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.People().popular(page=page)
            for item in response["results"]:
                xml += get_person_xml(item)
                content = "movies"
        elif url.startswith("movie"):
            if url.startswith("movie/upcoming"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.Movies().upcoming(page=page)
            for item in response["results"]:
                xml += get_trailer_xml(item)
                content = "movies"
        elif url.startswith("tv"):
            if url.startswith("tv/popular"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.TV().popular(page=page)
            elif url.startswith("tv/top_rated"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.TV().top_rated(page=page)
            elif url.startswith("tv/today"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.TV().airing_today(page=page)
            elif url.startswith("tv/on_the_air"):
                last = url.split("/")[-1]
                if last.isdigit():
                    page = int(last)
                if not response:
                    response = tmdbsimple.TV().on_the_air(page=page)
            for item in response["results"]:
                xml += get_show_xml(item)
                content = "tvshows"
        elif url.startswith("list"):
            list_id = url.split("/")[-1]
            if not response:
                response = tmdbsimple.Lists(list_id).info()
            for item in response.get("items", []):
                if "title" in item:
                    xml += get_movie_xml(item)
                    content = "movies"
                elif "name" in item:
                    xml += get_show_xml(item)
                    content = "tvshows"
        elif url.startswith("trailer"):
            movie_id = url.split("/")[-1]
            if not response:
                response = tmdbsimple.Movies(movie_id).videos()
            for item in response["results"]:
                if "type" in item:
                    xml += get_trailer_video_xml(item)
                    content = "movies"
        elif url.startswith("person"):
            split_url = url.split("/")
            person_id = split_url[-1]
            media = split_url[-2]
            if media == "movies":
                if not response:
                    response = tmdbsimple.People(person_id).movie_credits()
            elif media == "shows":
                if not response:
                    response = tmdbsimple.People(person_id).tv_credits()

            for job in response:
                if job == "id":
                    continue
                for item in response[job]:
                    if media == "movies":
                        xml += get_movie_xml(item)
                        content = "movies"
                    elif media == "shows":
                        xml += get_show_xml(item)
                        content = "tvshows"
        elif url.startswith("genre"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            genre_id = split_url[-2]
            media = split_url[-3]
            if media == "movies":
                if not response:
                    response = tmdbsimple.Discover().movie(with_genres=genre_id,
                                                           page=page)
            elif media == "shows":
                if not response:
                    response = tmdbsimple.Discover().tv(with_genres=genre_id,
                                                        page=page)

            for item in response["results"]:
                if media == "movies":
                    xml += get_movie_xml(item)
                    content = "movies"
                elif media == "shows":
                    xml += get_show_xml(item)
                    content = "tvshows"
        elif url.startswith("year"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            release_year = split_url[-2]
            media = split_url[-3]
            if media == "movies":
                if not response:
                    response = tmdbsimple.Discover().movie(primary_release_year=release_year,
                                                           page=page)
            for item in response["results"]:
                if media == "movies":
                    xml += get_movie_xml(item)
                    content = "movies"
        elif url.startswith("network"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            network_id = split_url[-2]
            media = split_url[-3]
            if media == "shows":
                if not response:
                    response = tmdbsimple.Discover().tv(with_networks=network_id,
                                                        page=page)
            for item in response["results"]:
                if media == "shows":
                    xml += get_show_xml(item)
                    content = "tvshows"
        elif url.startswith("company"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            company_id = split_url[-2]
            media = split_url[-3]
            if media == "movies":
                if not response:
                    response = tmdbsimple.Discover().movie(with_companies=company_id,
                                                           page=page)
            for item in response["results"]:
                if media == "movies":
                    xml += get_movie_xml(item)
                    content = "movies"
        elif url.startswith("keyword"):
            split_url = url.split("/")
            if len(split_url) == 3:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            keyword_id = split_url[-2]
            media = split_url[-3]
            if media == "movies":
                if not response:
                    response = tmdbsimple.Discover().movie(with_keywords=keyword_id,
                                                           page=page)
            elif media == "shows":
                if not response:
                    response = tmdbsimple.Discover().tv(with_keywords=keyword_id,
                                                        page=page)

            for item in response["results"]:
                if media == "movies":
                    xml += get_movie_xml(item)
                    content = "movies"
                elif media == "shows":
                    xml += get_show_xml(item)
                    content = "tvshows"
        elif url.startswith("collection"):
            split_url = url.split("/")
            collection_id = split_url[-1]
            if not response:
                response = tmdbsimple.Collections(collection_id).info()

            for item in response["parts"]:
                xml += get_movie_xml(item)
                content = "movies"
        elif url.startswith("search"):
            if url == "search":
                term = koding.Keyboard("Search For")
                url = "search/%s" % term
            split_url = url.split("/")
            if len(split_url) == 2:
                url += "/1"
                split_url.append(1)
            page = int(split_url[-1])
            term = split_url[-2]
            response = tmdbsimple.Search().multi(query=term, page=page)

            for item in response["results"]:
                if item["media_type"] == "movie":
                    xml += get_movie_xml(item)
                elif item["media_type"] == "tv":
                    xml += get_show_xml(item)
                elif item["media_type"] == "person":
                    name = item["name"]
                    person_id = item["id"]
                    if item.get("profile_path", ""):
                        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["profile_path"]
                    else:
                        thumbnail = ""
                    xml += "<dir>\n"\
                           "\t<title>%s Shows TMDB</title>\n"\
                           "\t<tmdb>person/shows/%s</tmdb>\n"\
                           "\t<thumbnail>%s</thumbnail>\n"\
                           "</dir>\n\n" % (name.capitalize(),
                                           person_id,
                                           thumbnail)

                    xml += "<dir>\n"\
                           "\t<title>%s Movies TMDB</title>\n"\
                           "\t<tmdb>person/movies/%s</tmdb>\n"\
                           "\t<thumbnail>%s</thumbnail>\n"\
                           "\t</dir>\n\n" % (name.capitalize(),
                                             person_id,
                                             thumbnail)

        if response and page < response.get("total_pages", 0):
            base = url.split("/")
            if base[-1].isdigit():
                base = base[:-1]
            next_url = "/".join(base) + "/" + str(page + 1)
            xml += "<dir>"\
                   "<title>Next Page >></title>"\
                   "<tmdb>%s</tmdb>"\
                   "<summary>Go To Page %s</summary>"\
                   "</dir>" % (next_url, page + 1)
        __builtin__.content_type = content
        save_to_db((xml, __builtin__.content_type), url)

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), __builtin__.content_type)


def get_movie_xml(item):
    title = remove_non_ascii(item["title"])
    tmdb_id = item["id"]

    if "release_date" not in item:
        year = ""
    else:
        year = item["release_date"].split("-")[0]
        if not year:
            year = tmdbsimple.Movies(tmdb_id).info()["release_date"]
    url = "tmdb_imdb({0})".format(tmdb_id)
    imdb = fetch_from_db(url)
    if not imdb:
        imdb = item.get("imdb_id", "")
        if not imdb:
            imdb = tmdbsimple.Movies(tmdb_id).info()["imdb_id"]
        save_to_db(imdb, url)
    if item["poster_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["poster_path"]
    else:
        thumbnail = ""
    if item.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    xml = "<item>" \
          "<title>[COLORwhite][B]%s[/COLOR][/B]</title>" \
          "<meta>" \
          "<imdb>%s</imdb>"\
          "<content>movie</content>" \
          "<title>%s</title>" \
          "<year>%s</year>" \
          "</meta>" \
          "<link>" \
          "<sublink>search</sublink>" \
          "<sublink>searchsd</sublink>" \
          "</link>" \
          "<thumbnail>%s</thumbnail>" \
          "<fanart>%s</fanart>" \
          "</item>" % (title, imdb, title, year, thumbnail, fanart)
    return xml


def get_trailer_xml(item):
    title = remove_non_ascii(item["title"])
    tmdb_id = item["id"]
    # url = "tmdb_imdb({0})".format(tmdb_id)
    summary = remove_non_ascii(item["overview"])
    if item["poster_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["poster_path"]
    else:
        thumbnail = ""
    if item["backdrop_path"]:
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    xml = "<dir>" \
          "<title>[COLORwhite][B]%s[/COLOR][/B]</title>" \
          "<tmdb>trailer/%s</tmdb>"\
          "<thumbnail>%s</thumbnail>" \
          "<fanart>%s</fanart>" \
          "<summary>%s</summary>" \
          "</dir>" % (title, tmdb_id, thumbnail, fanart, summary)
    return xml


def get_trailer_video_xml(item):
    title = remove_non_ascii(item["name"])
    # tmdb_id = item["id"]
    key = item["key"]
    # url = "tmdb_imdb({0})".format(tmdb_id)

    xml = "<item>" \
          "<title>[COLORwhite][B]%s[/COLOR][/B]</title>" \
          "<link>https://www.youtube.com/watch?v=%s&feature=youtube</link>"\
          "<summary>%s</summary>" \
          "</item>" % (title, key, title)
    return xml


def get_person_xml(item):
    title = remove_non_ascii(item["name"])
    tmdb_id = item["id"]
    # url = "tmdb_imdb({0})".format(tmdb_id)
    if item["profile_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["profile_path"]
    else:
        thumbnail = ""
    if item["profile_path"]:
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["profile_path"]
    else:
        fanart = ""
    xml = "<dir>" \
          "<title>[COLORwhite][B]%s[/COLOR][/B]</title>" \
          "<tmdb>person/movies/%s</tmdb>"\
          "<thumbnail>%s</thumbnail>" \
          "<fanart>%s</fanart>" \
          "<summary>%s</summary>" \
          "</dir>" % (title, tmdb_id, thumbnail, fanart, title)
    return xml


def get_show_xml(item):
    title = remove_non_ascii(item["name"])
    year = item["first_air_date"].split("-")[0]
    tmdb_id = item["id"]
    if item["poster_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["poster_path"]
    else:
        thumbnail = ""
    if item.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    if tmdb_id:
        url = "tmdb_imdb({0})".format(tmdb_id)
        imdb = fetch_from_db(url)
        if not imdb:
            try:
                imdb = tmdbsimple.TV(tmdb_id).external_ids()['imdb_id']
                save_to_db(imdb, url)
            except KeyError:
                imdb = "0"
    else:
        imdb = "0"

    xml = "<dir>"\
          "<title>[COLORwhite][B]%s[/COLOR][/B]</title>" \
          "<meta>"\
          "<imdb>%s</imdb>"\
          "<content>tvshow</content>"\
          "<tvshowtitle>%s</tvshowtitle>"\
          "<year>%s</year>"\
          "</meta>"\
          "<link>tmdb_tv_show(%s, %s, %s)</link>"\
          "<thumbnail>%s</thumbnail>" \
          "<fanart>%s</fanart>"\
          "</dir>" % (title, imdb, title, year, tmdb_id, year, title,
                      thumbnail, fanart)
    return xml


def get_season_xml(item, tmdb_id, year, tvtitle):
    season = item["season_number"]
    if item["poster_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["poster_path"]
    else:
        thumbnail = ""
    if item.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    if tmdb_id:
        url = "tmdb_imdb({0})".format(tmdb_id)
        imdb = fetch_from_db(url)
        if not imdb:
            imdb = tmdbsimple.TV(tmdb_id).external_ids()['imdb_id']
            save_to_db(imdb, url)
    else:
        imdb = "0"

    xml = "<dir>"\
          "<title>[COLORwhite][B]Season %s[/COLOR][/B]</title>" \
          "<meta>"\
          "<imdb>%s</imdb>"\
          "<content>season</content>"\
          "<season>%s</season>"\
          "</meta>"\
          "<thumbnail>%s</thumbnail>"\
          "<fanart>%s</fanart>"\
          "<link>tmdb_season(%s,%s, %s, %s)</link>"\
          "</dir>" % (season, imdb, season, thumbnail, fanart, tmdb_id,
                      season, year, tvtitle)
    return xml


def get_episode_xml(item, tmdb_id, year, tvtitle):
    title = remove_non_ascii(item["name"])
    season = item["season_number"]
    episode = item["episode_number"]
    if tmdb_id:
        url = "tmdb_imdb({0})".format(tmdb_id)
        imdb = fetch_from_db(url)
        if not imdb:
            imdb = tmdbsimple.TV(tmdb_id).external_ids()['imdb_id']
            save_to_db(imdb, url)
    else:
        imdb = "0"
    premiered = item["air_date"]
    if item["still_path"]:
        thumbnail = "https://image.tmdb.org/t/p/w1280/" + item["still_path"]
    else:
        thumbnail = ""
    if item.get("backdrop_path", ""):
        fanart = "https://image.tmdb.org/t/p/w1280/" + item["backdrop_path"]
    else:
        fanart = ""
    xml = "<item>"\
          "<title>[COLORwhite][B]%s[/COLOR][/B]</title>" \
          "<meta>"\
          "<imdb>%s</imdb>"\
          "<content>episode</content>"\
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
          "</item>" % (title, imdb, tvtitle, year, title,
                       premiered, season, episode, thumbnail, fanart)
    return xml


@route(mode='tmdb_tv_show', args=["url"])
def tmdb_tv_show(url):
    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        splitted = url.replace("tmdb_id", "").split(",")
        tmdb_id = splitted[0]
        year = splitted[1]
        tvtitle = ",".join(splitted[2:])
        response = tmdbsimple.TV(tmdb_id).info()
        seasons = response["seasons"]
        xml = ""
        for season in seasons:
            xml += get_season_xml(season, tmdb_id, year, tvtitle)
        save_to_db(xml, url)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='tmdb_season', args=["url"])
def tmdb_season(url):
    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        splitted = url.replace("tmdb_id", "").split(",")
        tmdb_id = splitted[0]
        season = splitted[1]
        year = splitted[2]
        tvtitle = ",".join(splitted[3:])
        response = tmdbsimple.TV_Seasons(tmdb_id, season).info()
        episodes = response["episodes"]
        xml = ""
        for episode in episodes:
            xml += get_episode_xml(episode, tmdb_id, year, tvtitle)
        save_to_db(xml, url)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


def remove_non_ascii(text):
    return unidecode(text)


def save_to_db(item, url):
    if not item or not url:
        return False
    koding.reset_db()
    koding.Remove_From_Table(
        "tmdb_plugin",
        {
            "url": url
        })

    koding.Add_To_Table("tmdb_plugin",
                        {
                            "url": url,
                            "item": base64.b64encode(pickle.dumps(item)),
                            "created": time.time()
                        })


def fetch_from_db(url):
    koding.reset_db()
    tmdb_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("tmdb_plugin", tmdb_plugin_spec)
    match = koding.Get_From_Table(
        "tmdb_plugin", {"url": url})
    if match:
        match = match[0]
        if not match["item"]:
            return None
        created_time = match["created"]
        if created_time and float(created_time) + CACHE_TIME >= time.time():
            match_item = match["item"]
            try:
                    result = pickle.loads(base64.b64decode(match_item))
            except:
                    return None
            return result
        else:
            return []
    else:
        return []
