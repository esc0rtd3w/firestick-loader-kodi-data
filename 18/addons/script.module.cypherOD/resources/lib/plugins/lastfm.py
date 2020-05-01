"""
    lastfm.py --- Jen Plugin for accessing lastfm data
    Copyright (C) 2017

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
        2018-05-14
            Latest version to include with a Jen Release

    Usage Examples:

    <dir>
    <title>Muse Tracks</title>
    <lastfm>artist/muse/tracks</lastfm>
    </dir>

    <dir>
    <title>ZZ Top Albums</title>
    <lastfm>artist/zz_top/albums</lastfm>
    </dir>

    <dir>
    <title>Search Artist</title>
    <lastfm>search/artist</lastfm>
    </dir>

    <dir>
    <title>Search Album</title>
    <lastfm>search/album</lastfm>
    </dir>

"""

import __builtin__
import pickle
import time
import urllib
import urlparse
import json
import requests
import re
import koding
import xbmc
import xbmcaddon
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode


CACHE_TIME = 3600  # change to wanted cache time in seconds
LASTFM_API_KEY = "3ec34c514a9230ebf006c8e24a8419d6"
LASTFM_SECRET = "41314c7fc8a8d391d28fa9721e08fdf2"

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
BASE_URL = "http://ws.audioscrobbler.com/2.0/"


class LASTFM(Plugin):
    name = "lastfm"

    def process_item(self, item_xml):
        if "<lastfm>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "lastfm",
                'url': item.get("lastfm", ""),
                'folder': True,
                'imdb': "0",
                'content': item.get("content", "files"),
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


@koding.route("lastfm", ["url"])
def lastfm(url):
    req_url = BASE_URL
    response_key = None
    __builtin__.content_type = "files"
    if url.startswith("artist"):
        artist = url.split("/")[1]
        if url.endswith("info"):
            req_url += "?method=artist.getinfo&artist=%s" % artist
        elif "albums" in url:
            req_url += "?method=artist.gettopalbums&artist=%s" % artist
            response_key = "topalbums"
            __builtin__.content_type = "albums"
        elif "tracks" in url:
            req_url += "?method=artist.gettoptracks&artist=%s" % artist
            response_key = "toptracks"
            __builtin__.content_type = "songs"
    elif url.startswith("album"):
        splitted = url.split("/")
        artist = splitted[1]
        album = splitted[2]
        if splitted[-1] == "tracks":
            req_url += "?method=album.getinfo&artist=%s&album=%s" % (
                artist, album)
            response_key = "album"
            __builtin__.content_type = "songs"
    elif url.startswith("chart"):
        if "artists" in url:
            req_url += "?method=chart.gettopartists"
            response_key = "artists"
            __builtin__.content_type = "artists"
        elif "tracks" in url:
            req_url += "?method=chart.gettoptracks"
            response_key = "tracks"
            __builtin__.content_type = "songs"
        elif "tags" in url:
            req_url += "?method=chart.gettoptags"
            response_key = "tags"
    elif url.startswith("tag"):
        splitted = url.split("/")
        tag = splitted[1]
        if splitted[-1] == "tracks":
            req_url += "?method=tag.gettoptracks&tag=%s" % tag
            response_key = "tracks"
            __builtin__.content_type = "songs"
        elif splitted[-1] == "artists":
            req_url += "?method=tag.gettopartists&tag=%s" % tag
            response_key = "topartists"
            __builtin__.content_type = "artists"
        elif splitted[-1] == "albums":
            req_url += "?method=tag.gettopalbums&tag=%s" % tag
            response_key = "albums"
            __builtin__.content_type = "albums"
    elif url.startswith("search"):
        splitted = url.split("/")
        if splitted[-1] == "artist":
            term = koding.Keyboard("Search For Artist")
            response_key = "results"
            req_url += "?method=artist.search&artist=%s" % term
        elif splitted[-1] == "album":
            term = koding.Keyboard("Search For Album")
            response_key = "results"
            req_url += "?method=album.search&album=%s" % term

    req_url += "&api_key=%s&format=json" % LASTFM_API_KEY 
    last = url.split("/")[-1]
    if last.isdigit():
        req_url += "&page=%s" % last

    # xml = fetch_from_db(url)
    # if not xml:
    xml = ""
    response = requests.get(req_url)
    response = response.json()
    if response_key:
        response = response[response_key]
    for key in response:
        if key == "album":
            for album in response["album"]:
                xml += get_album_xml(album)
        elif key == "tracks":
            images = response["image"]
            try:
                image = images[-1]["#text"]
            except Exception:
                image = ""
            for track in response["tracks"]["track"]:
                xml += get_track_xml(track, image)
        elif key == "track":
            for track in response["track"]:
                xml += get_track_xml(track)
        elif key == "artist" and "artist" in url:
            for artist in response["artist"]:
                xml += get_artist_xml(artist)
        elif key == "tag":
            for tag in response["tag"]:
                xml += get_tag_xml(tag)
        elif key == "artistmatches":
            matches = response['artistmatches']
            for artist in matches['artist']:
                xml += get_artist_xml(artist)
        elif key == "albummatches":
            matches = response['albummatches']
            for album in matches['album']:
                xml += get_search_album_xml(album)
    try:  

        if "@attr" in response:    
            pages = int(response["@attr"]["totalPages"])

        else:
            pages = 1
        if pages > 1:
            current_page = int(response["@attr"]["page"])
            if current_page < pages:
                last = url.split("/")[-1]
                if last.isdigit():
                    next_url = "/".join(url.split("/")[:-1])
                else:
                    next_url = url
                next_url += "/%s" % str(current_page + 1)
                xml += "<dir>\n"\
                       "\t<title>Next Page >></title>\n"\
                       "\t<lastfm>%s</lastfm>\n"\
                       "\t<summary>Go To Page %s</summary>\n"\
                       "</dir>" % (next_url, current_page + 1)

    except:
        pass

    xml = remove_non_ascii(xml)
    #save_to_db(xml, url)

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), __builtin__.content_type)


def get_album_xml(album):
    xml = ""
    album_title = album["name"]
    artist_name = album["artist"]["name"]
    images = album["image"]
    try:
        image = images[-1]["#text"]
    except Exception:
        image = ""
    url = "album/%s/%s/tracks" % (artist_name, album_title)

    xml += "<dir>\n"\
           "\t<title>%s</title>\n"\
           "\t<meta>\n"\
           "\t\t<content>album<content>\n"\
           "\t</meta>"\
           "\t<lastfm>%s</lastfm>\n"\
           "\t<thumbnail>%s</thumbnail>"\
           "</dir>\n\n" % (album_title, url, image)
    return xml

def get_search_album_xml(album):
    xml = ""
    album_title = album["name"]
    artist_name = album["artist"]
    images = album["image"]
    try:
        image = images[-1]["#text"]
    except Exception:
        image = ""
    url = "album/%s/%s/tracks" % (artist_name, album_title)

    xml += "<dir>\n"\
           "\t<title>%s - %s</title>\n"\
           "\t<meta>\n"\
           "\t\t<content>album<content>\n"\
           "\t</meta>"\
           "\t<lastfm>%s</lastfm>\n"\
           "\t<thumbnail>%s</thumbnail>"\
           "</dir>\n\n" % (album_title, artist_name, url, image)
    return xml    

def get_track_xml(track, image=None):
    xml = ""
    track_title = track["name"]
    artist_name = track["artist"]["name"]

    if image is None:
        try:
            images = track["image"]
            image = images[-1]["#text"]
        except Exception:
            image = ""

    xml += "<item>\n"\
           "\t<title>%s - %s</title>\n"\
           "\t<meta>\n"\
           "\t\t<content>song</content>\n"\
           "\t\t<artist>%s</artist>\n"\
           "\t\t<title>%s</title>\n"\
           "\t</meta>\n"\
           "\t<link>\n"\
           "\t\t<sublink>search</sublink>\n"\
           "\t\t<sublink>searchsd</sublink>\n"\
           "\t</link>\n"\
           "\t\t<thumbnail>%s</thumbnail>\n"\
           "</item>\n" % (track_title, artist_name,
                          artist_name, track_title, image)
    return xml


def get_artist_xml(artist):
    xml = ""
    name = artist["name"]
    url = "artist/%s/albums" % (name)
    try:
        images = artist["image"]
        image = images[-1]["#text"]
    except Exception:
        image = ""

    xml += "<dir>\n"\
           "\t<title>%s</title>\n"\
           "\t<lastfm>%s</lastfm>\n"\
           "\t<meta>"\
           "\t\t<content>artist<content>\n"\
           "\t</meta>"\
           "\t<thumbnail>%s</thumbnail>"\
           "</dir>\n\n" % (name, url, image)
    return xml


def get_tag_xml(tag):
    xml = ""
    name = tag["name"]
    url = "tag/%s/tracks" % (name)
    try:
        images = tag["image"]
        image = images[-1]["#text"]
    except Exception:
        image = ""
    summary = tag["wiki"].get("content", "")

    xml += "<dir>\n"\
           "\t<title>%s</title>\n"\
           "\t<lastfm>%s</lastfm>\n"\
           "\t<thumbnail>%s</thumbnail>" % (name, url, image)
    if summary:
        xml += "\t<summary>%s</summary>" % summary
    xml += "</dir>\n\n"
    return xml


def save_to_db(item, url):
    koding.reset_db()
    koding.Remove_From_Table("lastfm_plugin", {"url": url})

    koding.Add_To_Table("lastfm_plugin", {
        "url": url,
        "item": pickle.dumps(item).replace("\"", "'"),
        "created": time.time()
    })


def fetch_from_db(url):
    koding.reset_db()
    lastfm_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("lastfm_plugin", lastfm_plugin_spec)
    match = koding.Get_From_Table("lastfm_plugin", {"url": url})
    if match:
        match = match[0]
        if not match["item"]:
            return None
        created_time = match["created"]
        if created_time and float(created_time) + float(CACHE_TIME) >= time.time():
            match_item = match["item"].replace("'", "\"")
            return pickle.loads(match_item)
        else:
            return []
    else:
        return []


def remove_non_ascii(text):
    return unidecode(unicode(text))
