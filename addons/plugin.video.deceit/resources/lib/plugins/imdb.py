"""
    imdb.py --- Jen Plugin for accessing iMDB data
    Copyright (C) 2018

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

    
#####EXAMPLES#####
### NEW FEATURES ADDED ###
- <imdburl>user/ur19947955/lists</imdburl>      # Now if you have a IMDB account with lists. Add your user ID like this and it will grab all public list on your account
- <imdburl>searchboth</imdburl>             # Search Movies and TV Shows in same search
- <imdburl>searchkeywords</imdburl>         # Search Keywords in iMDB
### NEW FEATURES ADDED ###
- <imdburl>user/ur19947955/lists</imdburl>      # Now if you have a IMDB account with lists. Add your user ID like this and it will grab all public list on your account
- <imdburl>searchboth</imdburl>             # Search Movies and TV Shows in same search
- <imdburl>searchkeywords</imdburl>         # Search Keywords in iMDB
###genres just switch out key word 
<dir>
<title>IMDB Action TV Shows</title>
<imdburl>genrestv/action</imdburl>
</dir>

<dir>
<title>IMDB Action Movies</title>
<imdburl>genres/action</imdburl>
</dir>

###Movies
<dir>
<title>Chart Moviemeter</title>
<imdburl>chart/moviemeter</imdburl>
</dir>

<dir>
<title>Chart Best Rated</title>
<imdburl>chart/top</imdburl>
</dir>

###switch out year
<dir>
<title>[COLORwhite][B]2018  MOVIES</title>
<imdburl>years/2018</imdburl>
</dir>

###Tv show
<dir>
<title>Popular TV</title>
<imdburl>charttv/tvmeter</imdburl>
</dir>
"""



import urllib, urllib2, os, base64, xbmcplugin, xbmcgui, xbmcvfs, traceback, cookielib, xbmc, sys, requests
import pickle
import time
import re, json, urlparse
import koding
import xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode
import __builtin__

CACHE_TIME = 3600  # change to wanted cache time in seconds

TMDB_api_key = __builtin__.tmdb_api_key
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'


class IMDB(Plugin):
    name = "imdb"

    def process_item(self, item_xml):
        if "<imdburl>" in item_xml:
            item = JenItem(item_xml)
            if "season/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbseason",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "episode/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbepisode",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "years/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbyears",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "yearstv/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbyearstv",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "list/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdblists",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "keyword/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdblists",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "actors/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbactors",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "name/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbactorspage",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "www.imdb.com" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbNextPage",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "genres/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbgenres",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "genrestv/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbgenrestv",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "chart/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbchart",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "charttv/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbcharttv",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "searchmovies" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "searchmovies",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "searchseries" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "searchseries",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "searchboth" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "searchboth",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "searchkeywords" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "searchkeywords",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
            elif "/lists" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbuser",
                    'url': item.get("imdburl", ""),
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
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item
                

@route(mode='searchmovies', args=["url"])
def searchmovies(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search iMDB Movies')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://www.imdb.com/search/title?title=' + search_entered
        progress = xbmcgui.DialogProgress()
        imdbmovies(url)

@route(mode='searchseries', args=["url"])
def searchseries(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search iMDB Series')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://www.imdb.com/search/title?title=' + search_entered + '&title_type=tv_series'
        progress = xbmcgui.DialogProgress()
        imdbseries(url)

@route(mode='searchboth', args=["url"])
def searchboth(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search iMDB Movies & Series')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + search_entered + '&s=all'
        progress = xbmcgui.DialogProgress()
        imdbBothSearch(url)

@route(mode='searchkeywords', args=["url"])
def searchkeywords(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search iMDB Keywords')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + search_entered + '&s=kw'
        progress = xbmcgui.DialogProgress()
        imdbKeywords(url)
    
def imdbKeywords(url):
    xml = ""
    listhtml = getHtml(url)
    match = re.compile(
            '<a href="/keyword/(.+?)/.+?ref_=fn_kw_kw_.+?" >.+?</a>(.+?)</td>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for keywords, count in match:
            name = keywords + count
            xml += "<dir>"\
                   "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                   "<imdburl>keyword/%s</imdburl>"\
                   "<thumbnail></thumbnail>"\
                   "</dir>" % (name, keywords)  
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


def imdbBothSearch(url):
    xml = ""
    listhtml = getHtml(url)
    match = re.compile(
            '<img src="(.+?)" /></a> </td> <td class="result_text"> <a href="/title/(.+?)/.+?ref_=fn_al_tt_.+?" >(.+?)</a>(.+?)</td>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
            tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
            tmdbhtml = requests.get(tmdb_url).content
            Poster_path = re.compile(
                            '"poster_path":"(.+?)"', 
                            re.DOTALL).findall(tmdbhtml)
            Backdrop_path = re.compile(
                            '"backdrop_path":"(.+?)"', 
                            re.DOTALL).findall(tmdbhtml)
            for poster_path in Poster_path:
                for backdrop_path in Backdrop_path:
                    if not 'Series' in year:
                        year = year.split(')', 1)[0]
                        name = title + " " + year + ')'
                        year = year.replace("(","").replace(")","")
                        xml += "<item>"\
                                "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                                "<meta>"\
                                "<content>movie</content>"\
                                "<imdb>%s</imdb>"\
                                "<title>%s</title>"\
                                "<year>%s</year>"\
                                "</meta>"\
                                "<link>"\
                                "<sublink>search</sublink>"\
                                "<sublink>searchsd</sublink>"\
                                "</link>"\
                                "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
                                "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
                                "</item>" % (name, imdb, title, year, poster_path, backdrop_path)
                    else:
                        name = title + " " + year
                        xml += "<dir>"\
                               "<title>%s</title>"\
                               "<imdburl>season/%s</imdburl>"\
                               "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
                               "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
                               "</dir>" % (name, imdb, poster_path, backdrop_path)  
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
    

def imdbmovies(url):
    xml = ""
    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
        tmdbhtml = requests.get(tmdb_url).content
        Poster_path = re.compile(
                        '"backdrop_path":"(.+?)".+?"overview":".+?","poster_path":"(.+?)"}', 
                        re.DOTALL).findall(tmdbhtml)
        for backdrop_path, poster_path in Poster_path:
            name = title + " " + year
            year = year.replace("(","").replace(")","")
            xml += "<item>"\
                    "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                    "<meta>"\
                    "<content>movie</content>"\
                    "<imdb>%s</imdb>"\
                    "<title>%s</title>"\
                    "<year>%s</year>"\
                    "</meta>"\
                    "<link>"\
                    "<sublink>search</sublink>"\
                    "<sublink>searchsd</sublink>"\
                    "</link>"\
                    "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
                    "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
                    "</item>" % (name, imdb, title, year, poster_path, backdrop_path)
    next_page = re.compile(
                '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />', 
                re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    xml += "<dir>"\
           "<title>[COLOR white]Next Page >>[/COLOR]</title>"\
           "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
           "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
           "</dir>" % (next_page)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
    
    
def imdbseries(url):
    xml = ""
    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight=".+?"\nsrc=".+?"\nwidth=".+?" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
        tmdbhtml = requests.get(tmdb_url).content
        Poster_path = re.compile(
                    '"poster_path":"(.+?)".+?"backdrop_path":"(.+?)"', 
                    re.DOTALL).findall(tmdbhtml)
        for poster_path, backdrop_path in Poster_path:
            name = title + " " + year
            year = year.replace("(","").replace(")","")
            xml += "<dir>"\
                   "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                   "<meta>"\
                   "<content>tvshow</content>"\
                   "<imdb>%s</imdb>"\
                   "<imdburl>season/%s</imdburl>"\
                   "<tvdb></tvdb>"\
                   "<tvshowtitle>%s</tvshowtitle>"\
                   "<year>%s</year>"\
                   "</meta>"\
                   "<link></link>"\
                   "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
                   "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
                   "</dir>" % (name, imdb, imdb, title, year, poster_path, backdrop_path)
    try:
        next_page = re.compile(
                    '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />', 
                    re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        xml += "<dir>"\
               "<title>[COLOR white]Next Page >>[/COLOR]</title>"\
               "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
    

@route(mode='imdbchart', args=["url"])
def imdbchart(url):
    xml = ""
    url = 'http://www.imdb.com/' + url
    listhtml = getHtml(url)
    match = re.compile(
            '<a href="/title/(.+?)/.+?pf_rd_m=.+?pf_rd_i=.+?&ref_=.+?"\n> <img src="(.+?)" width=".+?" height=".+?"/>\n</a>.+?</td>\n.+?<td class="titleColumn">\n.+?\n.+?<a href=".+?"\ntitle=".+?" >(.+?)</a>\n.+?<span class="secondaryInfo">(.+?)</span>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for imdb, thumbnail, title, year in match:
        tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
        tmdbhtml = requests.get(tmdb_url).content
        Poster_path = re.compile(
                        '"backdrop_path":"(.+?)".+?"overview":".+?","poster_path":"(.+?)"}', 
                        re.DOTALL).findall(tmdbhtml)
        for backdrop_path, poster_path in Poster_path:
            name = title + " " + year
            year = year.replace("(","").replace(")","")
            xml += "<item>"\
                    "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                    "<meta>"\
                    "<content>movie</content>"\
                    "<imdb>%s</imdb>"\
                    "<title>%s</title>"\
                    "<year>%s</year>"\
                    "</meta>"\
                    "<link>"\
                    "<sublink>search</sublink>"\
                    "<sublink>searchsd</sublink>"\
                    "</link>"\
                    "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
                    "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
                    "</item>" % (name, imdb, title, year, poster_path, backdrop_path)
        jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
    

@route(mode='imdbcharttv', args=["url"])
def imdbcharttv(url):
    xml = ""
    url = url.replace("charttv/","chart/")
    url = 'http://www.imdb.com/' + url
    listhtml = getHtml(url)
    match = re.compile(
            '<a href="/title/(.+?)/.+?pf_rd_m=.+?pf_rd_i=.+?&ref_=.+?"\n> <img src="(.+?)" width=".+?" height=".+?"/>\n</a>.+?</td>\n.+?<td class="titleColumn">\n.+?\n.+?<a href=".+?"\ntitle=".+?" >(.+?)</a>\n.+?<span class="secondaryInfo">(.+?)</span>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for imdb, thumbnail, title, year in match:
        tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
        tmdbhtml = requests.get(tmdb_url).content
        Poster_path = re.compile(
                    '"poster_path":"(.+?)".+?"backdrop_path":"(.+?)"', 
                    re.DOTALL).findall(tmdbhtml)
        for poster_path, backdrop_path in Poster_path:
            name = title + " " + year
            year = year.replace("(","").replace(")","")
            xml += "<dir>"\
                   "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                   "<meta>"\
                   "<content>tvshow</content>"\
                   "<imdb>%s</imdb>"\
                   "<imdburl>season/%s</imdburl>"\
                   "<tvdb></tvdb>"\
                   "<tvshowtitle>%s</tvshowtitle>"\
                   "<year>%s</year>"\
                   "</meta>"\
                   "<link></link>"\
                   "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
                    "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
                   "</dir>" % (name, imdb, imdb, title, year, poster_path, backdrop_path)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
    
    
@route(mode='imdbseason', args=["url"])
def imdbseason(url):
    xml = ""
    url = url.replace("season/","")
    imdb = url
    url = 'http://www.imdb.com/title/' + imdb
    listhtml = getHtml(url)
    match = re.compile(
            'href="/title/'+imdb+'/episodes.+?season=.+?&ref_=tt_eps_sn_.+?"\n>(.+?)</a>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for season in match:
            episodeURL = 'http://www.imdb.com/title/' + imdb + "/episodes?season=" + season
            name = "Season: [COLOR white]" + season + "[/COLOR]"
            xml +=  "<dir>"\
                    "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                    "<meta>"\
                    "<content>season</content>"\
                    "<imdb>%s</imdb>"\
                    "<imdburl>theepisode/%s</imdburl>"\
                    "<tvdb></tvdb>"\
                    "<tvshowtitle></tvshowtitle>"\
                    "<year></year>"\
                    "<season>%s</season>"\
                    "</meta>"\
                    "<link></link>"\
                    "<thumbnail></thumbnail>"\
                    "<fanart></fanart>"\
                    "</dir>" % (name, imdb, episodeURL, season)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='imdbepisode', args=["url"])
def imdbepisode(url):
    xml = ""
    url = url.replace("theepisode/","")
    listhtml = getHtml(url)
    match = re.compile(
            '<div data-const="(.+?)" class="hover-over-image zero-z-index ">\n<img width=".+?" height=".+?" class="zero-z-index" alt="(.+?)" src="(.+?)">\n<div>S(.+?), Ep(.+?)</div>\n</div>\n</a>.+?</div>\n.+?<div class="info" itemprop="episodes" itemscope itemtype=".+?">\n.+?<meta itemprop="episodeNumber" content=".+?"/>\n.+?<div class="airdate">\n.+?([^"]+)\n.+?</div>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for imdb, title, thumbnail, season, episode, premiered in match:
            tvshowtitle = re.compile(
                            '<h3 itemprop="name">\n<a href="/title/.+?/.+?ref_=ttep_ep_tt"\nitemprop=.+?>(.+?)</a>', 
                            re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
            Year = re.compile(
                            '<meta itemprop="name" content=".+?TV Series ([^"]+).+? .+?"/>', 
                            re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
            thumbnail = thumbnail.replace("@._V1_UX200_CR0,0,200,112_AL_.jpg","@._V1_UX600_CR0,0,600,400_AL_.jpg")
            name = "[COLOR white]%sx%s[/COLOR] . %s" % (season, episode, title)
            xml +=  "<item>"\
                    "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                    "<meta>"\
                    "<content>episode</content>"\
                    "<imdb>%s</imdb>"\
                    "<tvdb></tvdb>"\
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
                    "<fanart></fanart>"\
                    "</item>" % (name, imdb, tvshowtitle, Year, title, premiered, season, episode, thumbnail)
    if not match:
        match = re.compile(
                '<a href="/title/(.+?)/.+?ref_=ttep_ep.+?"\ntitle="(.+?)" itemprop="url"> <div data-const=".+?" class="hover-over-image zero-z-index no-ep-poster">\n<a href=".+?"\nonclick=".+?" class="add-image" > <span class="add-image-container episode-list" style="width:200px;height:112px">\n<span class="add-image-icon episode-list" />\n<span class="add-image-text episode-list">Add Image</span>\n</span>\n</a> <div>S(.+?), Ep(.+?)</div>\n</div>', 
                re.IGNORECASE | re.DOTALL).findall(listhtml)
        for imdb, title, season, episode in match:
                tvshowtitle = re.compile(
                            '<h3 itemprop="name">\n<a href="/title/.+?/.+?ref_=ttep_ep_tt"\nitemprop=.+?>(.+?)</a>', 
                            re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
                Year = re.compile(
                            '<meta itemprop="name" content=".+?TV Series ([^"]+).+? .+?"/>', 
                            re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
                name = "[B][COLOR yellow]%s[/COLOR][/B]" % (title)
                xml +=  "<item>"\
                        "<title>%s</title>"\
                        "<meta>"\
                        "<content>episode</content>"\
                        "<imdb>%s</imdb>"\
                        "<tvdb></tvdb>"\
                        "<tvshowtitle>%s</tvshowtitle>"\
                        "<year>%s</year>"\
                        "<title>%s</title>"\
                        "<premiered></premiered>"\
                        "<season>%s</season>"\
                        "<episode>%s</episode>"\
                        "</meta>"\
                        "<link>"\
                        "<sublink>search</sublink>"\
                        "<sublink>searchsd</sublink>"\
                        "</link>"\
                        "<thumbnail>https://image.ibb.co/ew7xZG/not_Aired_Yet.png</thumbnail>"\
                        "<fanart></fanart>"\
                        "</item>" % (name, imdb, tvshowtitle, Year, title, season, episode)     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

    
@route(mode='imdbuser', args=["url"])
def imdbuser(url):
    xml = ""
    link = 'http://www.imdb.com/' + url
    listhtml = getHtml(link)
    match = re.compile(
            '<a class="list-name" href="(.+?)">(.+?)</a>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for url, name in match:
        xml += "<dir>"\
               "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
               "<imdburl>%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/fR6AOm/download.jpg</thumbnail>"\
               "</dir>" % (name, url)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
               
@route(mode='imdblists', args=["url"])
def imdblists(url):
    xml = ""
    link = 'http://www.imdb.com/' + url
    listhtml = requests.get(link).content
    block = re.compile('<div class="lister-list">.+?<div class="row text-center lister-working hidden"></div>',re.DOTALL).findall(listhtml)
    match = re.compile('<img alt="(.+?)".+?data-tconst="(.+?)".+?<span class="lister-item-year text-muted unbold">(.+?)</span>',re.DOTALL).findall(str(block))
    for title, imdb, year in match:
        try:            
            tmdb_url = 'http://api.themoviedb.org/3/find/' +imdb+ '?api_key=' +TMDB_api_key+ '&external_source=imdb_id'
            #30551812602b96050a36103b3de0163b
            title = clean_search(title)
            title = remove_non_ascii(title)
            headers = {'User-Agent':User_Agent}
            tmdbhtml = requests.get(tmdb_url,headers=headers,timeout=20).content
            match = json.loads(tmdbhtml)
            if 'movie_results' in match:      
                result = match['movie_results'][0]
                poster_path = result['poster_path']
                if not poster_path:
                    poster_path = "none"        
                backdrop_path = result['backdrop_path']
                if not backdrop_path:
                    backdrop_path = "none"
            else:
                poster_path = "none"
                backdrop_path = "none"            
        except:
            poster_path = "none"
            backdrop_path = "none"            

        name = title + " " + year
        year = year.replace("(","").replace(")","")
        xml += "<item>"\
                "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                "<meta>"\
                "<content>movie</content>"\
                "<imdb>%s</imdb>"\
                "<title>%s</title>"\
                "<year>%s</year>"\
                "</meta>"\
                "<link>"\
                "<sublink>search</sublink>"\
                "<sublink>searchsd</sublink>"\
                "</link>"\
                "<thumbnail>https://image.tmdb.org/t/p/w1280%s</thumbnail>"\
                "<fanart>https://image.tmdb.org/t/p/w1280%s</fanart>"\
                "</item>" % (name, imdb, title, year, poster_path, backdrop_path)           
            # if len(year) >= 8:
            #     tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
            #     tmdbhtml = requests.get(tmdb_url).content
            #     match = json.loads(tmdbhtml)
            #     if 'movie_results' in match:      
            #         result = match['movie_results'][0]
            #         poster_path = result['poster_path']
            #         if not poster_path:
            #             poster_path = "none"        
            #         backdrop_path = result['backdrop_path']
            #         if not backdrop_path:
            #             backdrop_path = "none"
            #     else:
            #         poster_path = "none"
            #         backdrop_path = "none"
            #         name = title + " " + year
            #         year = year.replace("(","").replace(")","")
            #         xml += "<dir>"\
            #              "<title>%s</title>"\
            #              "<meta>"\
            #              "<content>tvshow</content>"\
            #              "<imdb>%s</imdb>"\
            #              "<imdburl>season/%s</imdburl>"\
            #              "<tvdb></tvdb>"\
            #              "<tvshowtitle>%s</tvshowtitle>"\
            #              "<year>%s</year>"\
            #              "</meta>"\
            #              "<link></link>"\
            #              "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
            #              "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
            #              "</dir>" % (name, imdb, imdb, title, year, poster_path, backdrop_path)
            # else:               
            #     tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
            #     tmdbhtml = requests.get(tmdb_url).content
            #     match = json.loads(tmdbhtml)
            #     if 'movie_results' in match:      
            #         result = match['movie_results'][0]
            #         poster_path = result['poster_path']
            #         if not poster_path:
            #             poster_path = "none"        
            #         backdrop_path = result['backdrop_path']
            #         if not backdrop_path:
            #             backdrop_path = "none"
            #     else:
            #         poster_path = "none"
            #         backdrop_path = "none"
            #         name = title + " " + year
            #         year = year.replace("(","").replace(")","")
            #         xml += "<item>"\
            #                 "<title>%s</title>"\
            #                 "<meta>"\
            #                 "<content>movie</content>"\
            #                 "<imdb>%s</imdb>"\
            #                 "<title>%s</title>"\
            #                 "<year>%s</year>"\
            #                 "</meta>"\
            #                 "<link>"\
            #                 "<sublink>search</sublink>"\
            #                 "<sublink>searchsd</sublink>"\
            #                 "</link>"\
            #                 "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
            #                 "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
            #                 "</item>" % (name, imdb, title, year, poster_path, backdrop_path)

    try:
        next_page = re.compile(
                    '<a class=".+?next-page" href="(.+?)">', 
                    re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        next_page = next_page.split("/")[1:4]
        next_page = next_page[0]+"/"+next_page[1]+"/"+next_page[2]
        xml += "<dir>"\
               "<title>[COLOR white]Next Page >>[/COLOR]</title>"\
               "<imdburl>%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
    
            
                
@route(mode='imdbyears', args=["url"])
def imdbyears(url):
    xml = ""
    url = url.replace("years/","")
    url = 'http://www.imdb.com/search/title?year=' + url + '&title_type=feature'
    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
        tmdbhtml = requests.get(tmdb_url).content
        Poster_path = re.compile(
                        '"backdrop_path":"(.+?)".+?"overview":".+?","poster_path":"(.+?)"}', 
                        re.DOTALL).findall(tmdbhtml)
        for backdrop_path, poster_path in Poster_path:
            name = title + " " + year
            year = year.replace("(","").replace(")","")
            thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_SY1000_SX800_AL_.jpg")
            xml += "<item>"\
                    "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                    "<meta>"\
                    "<content>movie</content>"\
                    "<imdb>%s</imdb>"\
                    "<title>%s</title>"\
                    "<year>%s</year>"\
                    "</meta>"\
                    "<link>"\
                    "<sublink>search</sublink>"\
                    "<sublink>searchsd</sublink>"\
                    "</link>"\
                    "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
                    "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
                    "</item>" % (name, imdb, title, year, poster_path, backdrop_path)
    next_page = re.compile(
                '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />', 
                re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    xml += "<dir>"\
           "<title>[COLOR white]Next Page >>[/COLOR]</title>"\
           "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
           "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
           "</dir>" % (next_page)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='imdbyearstv', args=["url"])
def imdbyearstv(url):
    xml = ""
    url = url.replace("yearstv/","")
    url = 'http://www.imdb.com/search/title?title_type=tv_series&release_date=' + url
    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
        tmdbhtml = requests.get(tmdb_url).content
        Poster_path = re.compile(
                    '"poster_path":"(.+?)".+?"backdrop_path":"(.+?)"', 
                    re.DOTALL).findall(tmdbhtml)
        for poster_path, backdrop_path in Poster_path:
            name = title + " " + year
            year = year.replace("(","").replace(")","")
            xml += "<dir>"\
                   "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                   "<meta>"\
                   "<content>tvshow</content>"\
                   "<imdb>%s</imdb>"\
                   "<imdburl>season/%s</imdburl>"\
                   "<tvdb></tvdb>"\
                   "<tvshowtitle>%s</tvshowtitle>"\
                   "<year>%s</year>"\
                   "</meta>"\
                   "<link></link>"\
                   "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
                   "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
                   "</dir>" % (name, imdb, imdb, title, year, poster_path, backdrop_path)
    next_page = re.compile(
                '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />', 
                re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    xml += "<dir>"\
           "<title>[COLOR white]Next Page >>[/COLOR]</title>"\
           "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
           "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
           "</dir>" % (next_page)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
    
    
@route(mode='imdbgenres', args=["url"])
def imdbgenres(url):
    xml = ""
    url = url.replace("genres/","")
    url = 'http://www.imdb.com/search/title?genres=' + url + '&explore=title_type,genres&title_type=Movie&sort=moviemeter,asc'
    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        tmdb_url = 'http://api.themoviedb.org/3/find/' + imdb + '?api_key=30551812602b96050a36103b3de0163b&external_source=imdb_id'
        tmdbhtml = requests.get(tmdb_url).content
        Poster_path = re.compile(
                    '"backdrop_path":"(.+?)".+?"overview":".+?","poster_path":"(.+?)"}', 
                    re.DOTALL).findall(tmdbhtml)
        for backdrop_path, poster_path in Poster_path:      
            name = title + " " + year
            year = year.replace("(","").replace(")","").replace(" TV Movie","")
            xml += "<item>"\
                    "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                    "<meta>"\
                    "<content>movie</content>"\
                    "<imdb>%s</imdb>"\
                    "<title>%s</title>"\
                    "<year>%s</year>"\
                    "</meta>"\
                    "<link>"\
                    "<sublink>search</sublink>"\
                    "<sublink>searchsd</sublink>"\
                    "</link>"\
                    "<thumbnail>https://image.tmdb.org/t/p/w1280/%s</thumbnail>"\
                    "<fanart>https://image.tmdb.org/t/p/w1280/%s</fanart>"\
                    "</item>" % (name, imdb, title, year, poster_path, backdrop_path)
    next_page = re.compile(
                '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />', 
                re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    xml += "<dir>"\
           "<title>[COLOR white]Next Page >>[/COLOR]</title>"\
           "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
           "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
           "</dir>" % (next_page)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

    
@route(mode='imdbgenrestv', args=["url"])
def imdbgenrestv(url):
    xml = ""
    url = url.replace("genrestv/","")
    url = 'http://www.imdb.com/search/title?genres=' + url + '&explore=title_type,genres&title_type=tvSeries&ref_=adv_explore_rhs'
    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_SY1000_SX800_AL_.jpg")
        xml += "<dir>"\
               "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
               "<meta>"\
               "<content>tvshow</content>"\
               "<imdb>%s</imdb>"\
               "<imdburl>season/%s</imdburl>"\
               "<tvdb></tvdb>"\
               "<tvshowtitle>%s</tvshowtitle>"\
               "<year>%s</year>"\
               "</meta>"\
               "<link></link>"\
               "<thumbnail>%s</thumbnail>"\
               "<fanart></fanart>"\
               "</dir>" % (name, imdb, imdb, title, year, thumbnail)
    next_page = re.compile(
                '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />', 
                re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    xml += "<dir>"\
           "<title>[COLOR white]Next Page >>[/COLOR]</title>"\
           "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
           "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
           "</dir>" % (next_page)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
    
    

@route(mode='imdbactors', args=["url"])
def imdbactors(url):
    xml = ""
    url = url.replace("http://www.imdb.com","").replace("actors","list").replace("actor","")
    link = 'http://www.imdb.com/' + url
    listhtml = getHtml(link)
    match = re.compile(
            '<img alt=".+?"\nheight="209"\nsrc="(.+?)"\nwidth="140" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n.+?<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n<a href="/name/(.+?)"\n>(.+?)\n</a>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, name in match:
        thumbnail = thumbnail.replace("@._V1_UY209_CR10,0,140,209_AL_.jpg","@._V1_SY1000_SX800_AL_.jpg")
        thumbnail = thumbnail.replace("._V1_UY209_CR5,0,140,209_AL_.jpg","._V1_UX520_CR0,0,520,700_AL_.jpg")
        xml += "<dir>"\
               "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
               "<imdburl>name/%s</imdburl>"\
               "<thumbnail>%s</thumbnail>"\
               "</dir>" % (name, imdb ,thumbnail)
    next_page = re.compile(
                '<a class="flat-button lister-page-next next-page" href="(.+?)">\n.+?Next\n.+?</a>', 
                re.IGNORECASE | re.DOTALL).findall(listhtml)
    for url in next_page:
        try:
            xml += "<dir>"\
                   "<title>[COLOR white]Next Page >>[/COLOR]</title>"\
                   "<imdburl>actor%s</imdburl>"\
                   "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
                   "</dir>" % (url)
        except:
            pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='imdbactorspage', args=["url"])
def imdbactorspage(url):
    xml = ""
    link = 'http://www.imdb.com/' + url
    listhtml = getHtml(link)
    match = re.compile(
            '<div class="film.+?" id="act.+?">\n<span class="year_column">\n&nbsp;(.+?)\n</span>\n<b><a href="/title/(.+?)/.+?ref_=.+?"\n>(.+?)</a></b>', 
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for year, imdb, title in match:
        name = title + " (" + year + ")"
        xml += "<item>"\
                "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                "<meta>"\
                "<content>movie</content>"\
                "<imdb>%s</imdb>"\
                "<title>%s</title>"\
                "<year>%s</year>"\
                "</meta>"\
                "<link>"\
                "<sublink>search</sublink>"\
                "<sublink>searchsd</sublink>"\
                "</link>"\
                "<thumbnail></thumbnail>"\
                "<fanart></fanart>"\
                "</item>" % (name, imdb, title, year)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())    


@route(mode='imdbNextPage', args=["url"])
def imdbNextPage(url):
    xml = ""
    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight=".+?"\nsrc=".+?"\nwidth=".+?" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>',
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_SY1000_SX800_AL_.jpg")
        xml += "<item>"\
                "<title>%s</title>"\
                "<meta>"\
                "<content>movie</content>"\
                "<imdb>%s</imdb>"\
                "<title>%s</title>"\
                "<year>%s</year>"\
                "</meta>"\
                "<link>"\
                "<sublink>search</sublink>"\
                "<sublink>searchsd</sublink>"\
                "</link>"\
                "<thumbnail>%s</thumbnail>"\
                "<fanart></fanart>"\
                "</item>" % (name, imdb, title, year, thumbnail)
    next_page = re.compile(
                '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />', 
                re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
    xml += "<dir>"\
           "<title>[COLOR white]Next Page >>[/COLOR]</title>"\
           "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
           "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
           "</dir>" % (next_page)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
    

def getHtml(url, referer=None, hdr=None, data=None):
    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}
    if not hdr:
        req = urllib2.Request(url, data, headers)
    else:
        req = urllib2.Request(url, data, hdr)
    if referer:
        req.add_header('Referer', referer)
    response = urllib2.urlopen(req, timeout=60)
    data = response.read()    
    response.close()
    return data

def remove_non_ascii(text):
    return unidecode(text)    

def clean_search(title):
    if title == None: return
    title = title.replace("xc2","")
    title = title.replace("xb7","")
    title = title.replace("\\","")
    return title    
