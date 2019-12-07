"""
    imdb.py --- Jen Plugin for accessing iMDB data
    Copyright (C) 2018, Mister-X

    --August 14, 2018 Added calendar support for upcoming releases by country

    --June 16, 2018 Added try and except to next page code to fix results not being displayed
    if there was only one page--

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
    <dir>
        <title>Search</title>
        <imdburl>searchseries</imdburl>
        <thumbnail></thumbnail>
    </dir>

    ####TV
    <dir>
        <title>Newest</title>
        <imdburl>tvshows/new</imdburl>
        <thumbnail></thumbnail>
    </dir>

    <dir>
        <title>Best Ratings</title>
        <imdburl>tvshows/rating</imdburl>
        <thumbnail></thumbnail>
    </dir>

    <dir>
        <title>Most Viewed</title>
        <imdburl>tvshows/mostviews</imdburl>
        <thumbnail></thumbnail>
    </dir>

    ###charts
    <dir>
        <title>Chart Best Rated</title>
        <imdburl>charttv/toptv</imdburl>
    </dir>

    ###Genres
    <dir>
        <title>IMDB Action TV Shows</title>
        <imdburl>genres/action</imdburl>
        <thumbnail></thumbnail>
    </dir>

    ### Movies
    <dir>
        <title>IMDB Trending</title>
        <imdburl>movies/trending</imdburl>
    </dir>

    <dir>
    <title>2016</title>
        <imdburl>years/2016</imdburl>
        <thumbnail></thumbnail>
    </dir>

    ###For user list
    <dir>
        <title>IMDB TOP 100 Gangster List</title>
        <imdburl>list/ls001818278</imdburl>
    </dir>

    ###For upcoming release list by country
    <dir>
        <title>IMDB Upcoming Releases in the US</title>
        <imdburl>moviecalendar/US</imdburl>
    </dir>

"""

import urllib, urllib2, os, base64, xbmcplugin, xbmcgui, xbmcvfs, traceback, cookielib, xbmc, sys
import pickle
import time
import re
import koding
import xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode


CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')


class IMDB(Plugin):
    name = "imdb"

    def process_item(self, item_xml):
        if "<imdburl>" in item_xml:
            item = JenItem(item_xml)
            if "movies/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbmovies",
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
            elif "tvshows/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbseries",
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
            elif "season/" in item.get("imdburl", ""):
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
            elif "theepisodeTwo/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "imdbepisodeTwo",
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
            elif "moviecalendar/" in item.get("imdburl", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "moviecalendar",
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

@route(mode='imdbmovies', args=["url"])
def imdbmovies(url):
    xml = ""
    url = url.replace("movies/popular","http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=40&start=1").replace("movies/voted","http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&count=40&start=1").replace("movies/trending","http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=date[365],date[60]&sort=moviemeter,asc&count=40&start=1").replace("movies/boxoffice","http://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&count=40&start=1")
    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>',
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
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
    try:
        next_page = re.compile(
                    '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />',
                    re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        xml += "<dir>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='imdbseries', args=["url"])
def imdbseries(url):
    xml = ""
    url = url.replace("tvshows/popular","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=moviemeter,asc&count=40&start=1")
    url = url.replace("tvshows/new","http://www.imdb.com/search/title?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=release_date,desc&count=40&start=1")
    url = url.replace("tvshows/rating","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&release_date=,date[0]&sort=user_rating,desc&count=40&start=1")
    url = url.replace("tvshows/mostviews","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=num_votes,desc&count=40&start=1")
    url = url.replace("tvshows/boxoffice","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date%5B0%5D&count=40&start=1&sort=boxoffice_gross_us,desc")
    url = url.replace("tvshows/alphabetical","http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date%5B0%5D&count=40&start=1&sort=alpha,asc")

    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>',
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
        xml += "<dir>"\
               "<title>%s</title>"\
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
    try:
        next_page = re.compile(
                    '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />',
                    re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        xml += "<dir>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='imdbseason', args=["url"])
def imdbseason(url):
    xml = ""
    url = url.replace("season/","title/")
    url = 'http://www.imdb.com/' + url
    listhtml = getHtml(url)
    match = re.compile(
            'href="/title/(.+?)/episodes.+?season=.+?&ref_=tt_eps_sn_.+?"\n>(.+?)</a>',
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    match2 = re.compile(
            '<h4 class="float-left">Years</h4><hr />\n.+?</div>\n.+?<br class="clear" />\n.+?<div>\n.+?<a href="/title/(.+?)/episodes.+?season=.+?&ref_=tt_eps_sn_.+?"\n>(.+?)</a>&nbsp;&nbsp;',
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for imdb, season in match2:
        thumbnail = re.compile(
                        '<img alt=".+?Poster" title=".+?Poster"\nsrc="(.+?)"',
                        re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        thumbnail = thumbnail.replace("@._V1_UY268_CR16,0,182,268_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
        episodeURL = 'http://www.imdb.com/title/' + imdb + '/episodes?season=' + season
        name = "Season: [COLOR dodgerblue]" + season + "[/COLOR]"
        xml +=  "<dir>"\
                "<title>%s</title>"\
                "<meta>"\
                "<content>season</content>"\
                "<imdb>%s</imdb>"\
                "<imdburl>theepisodeTwo/%s</imdburl>"\
                "<tvdb></tvdb>"\
                "<tvshowtitle></tvshowtitle>"\
                "<year></year>"\
                "<season>%s</season>"\
                "</meta>"\
                "<link></link>"\
                "<thumbnail>%s</thumbnail>"\
                "<fanart></fanart>"\
                "</dir>" % (name, imdb, episodeURL, season, thumbnail)
    for imdb, season in match:
        if 'fallback' in imdb:
            pass
        else:
            thumbnail = re.compile(
                        '<img alt=".+?Poster" title=".+?Poster"\nsrc="(.+?)"',
                        re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
            thumbnail = thumbnail.replace("@._V1_UY268_CR16,0,182,268_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
            episodeURL = 'http://www.imdb.com/title/' + imdb + '/episodes?season=' + season
            name = "Season: [COLOR dodgerblue]" + season + "[/COLOR]"
            xml +=  "<dir>"\
                    "<title>%s</title>"\
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
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart></fanart>"\
                    "</dir>" % (name, imdb, episodeURL, season, thumbnail)
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
            name = "[COLOR dodgerblue]%sx%s[/COLOR] . %s" % (season, episode, title)
            xml +=  "<item>"\
                    "<title>%s</title>"\
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
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='imdbepisodeTwo', args=["url"])
def imdbepisodeTwo(url):
    xml = ""
    url = url.replace("theepisodeTwo/","")
    listhtml = getHtml(url)
    match = re.compile(
            '<a href="/title/(.+?)/.+?ref_=ttep_ep.+?"\ntitle="Episode #([^"]+).+?([^"]+)" itemprop="url">',
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for imdb, season, episode in match:
                tvshowtitle = re.compile(
                                '<h3 itemprop="name">\n<a href="/title/.+?/.+?ref_=ttep_ep_tt"\nitemprop=.+?>(.+?)</a>',
                                re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
                Year = re.compile(
                                '<meta itemprop="name" content=".+?TV Series ([^"]+).+? .+?"/>',
                                re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
                name = "[COLOR yellow]Episode: " + season + "[/COLOR]"
                xml +=  "<item>"\
                        "<title>%s</title>"\
                        "<meta>"\
                        "<content>episode</content>"\
                        "<imdb>%s</imdb>"\
                        "<tvdb></tvdb>"\
                        "<tvshowtitle>%s</tvshowtitle>"\
                        "<year>%s</year>"\
                        "<title></title>"\
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
                        "</item>" % (name, imdb, tvshowtitle, Year, season, episode)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='imdblists', args=["url"])
def imdblists(url):
    xml = ""
    link = 'http://www.imdb.com/' + url
    listhtml = getHtml(link)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="209"\nsrc=".+?"\nwidth="140" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>',
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UY209_CR3,0,140,209_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
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
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
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
    try:
        next_page = re.compile(
                    '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />',
                    re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        xml += "<dir>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
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
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
        xml += "<dir>"\
               "<title>%s</title>"\
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
    try:
        next_page = re.compile(
                    '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />',
                    re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        xml += "<dir>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='imdbgenres', args=["url"])
def imdbgenres(url):
    xml = ""
    url = url.replace("genres/","")
    url = 'http://www.imdb.com/search/title?genres=' + url + '&explore=title_type,genres&title_type=tvMovie&ref_=adv_explore_rhs'
    listhtml = getHtml(url)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>',
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        name = title + " " + year
        year = year.replace("(","").replace(")","").replace(" TV Movie","")
        thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
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
    try:
        next_page = re.compile(
                    '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />',
                    re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        xml += "<dir>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
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
        thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
        xml += "<dir>"\
               "<title>%s</title>"\
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
    try:
        next_page = re.compile(
                    '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />',
                    re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        xml += "<dir>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
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
        thumbnail = thumbnail.replace("@._V1_UY209_CR10,0,140,209_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
        thumbnail = thumbnail.replace("._V1_UY209_CR5,0,140,209_AL_.jpg","._V1_UX520_CR0,0,520,700_AL_.jpg")
        xml += "<dir>"\
               "<title>%s</title>"\
               "<imdburl>name/%s</imdburl>"\
               "<thumbnail>%s</thumbnail>"\
               "</dir>" % (name, imdb ,thumbnail)
    try:
        next_page = re.compile(
                    '<a class="flat-button lister-page-next next-page" href="(.+?)">\n.+?Next\n.+?</a>',
                    re.IGNORECASE | re.DOTALL).findall(listhtml)
        for url in next_page:
            try:
                xml += "<dir>"\
                       "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
                       "<imdburl>actor%s</imdburl>"\
                       "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
                       "</dir>" % (url)
            except:
                pass
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
                "<thumbnail></thumbnail>"\
                "<fanart></fanart>"\
                "</item>" % (name, imdb, title, year)
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
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UY67_CR0,0,45,67_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
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
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UY67_CR0,0,45,67_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
        xml += "<dir>"\
               "<title>%s</title>"\
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
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='moviecalendar', args=["url"])
def moviecalendar(url):
    xml = ""
    url = url.replace("moviecalendar/","")
    url = 'https://www.imdb.com/calendar?region=%s&ref_=rlm' % (url)
    listhtml = getHtml(url)
    divcont = dom_parser.parseDOM(listhtml, 'div', attrs={'id':'main'})[0]

    if len(divcont) == 0:
        # No entries for this country
        xml += "<item>"\
               "<title>This country has no upcoming releases listed</title>"\
               "<link></link>"\
               "</item>"
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())
        return

    match = re.compile('<h4>(.+?)</h4>\s*<ul>(.+?)</ul>', re.IGNORECASE | re.DOTALL).findall(divcont)
    for date, listcont in match:
        try:
            tmp = date.split(' ')
            year = tmp[(len(tmp)-1)]
            xml += "<item>"\
                   "<title>[COLOR snow][B]-= %s =-[/B][/COLOR]</title>"\
                   "<meta>"\
                   "<summary>The below movies are for the release date %s</summary>"\
                   "</meta>"\
                   "<link></link>"\
                   "</item>" % (date, date)

            entries = re.compile('<a href="/title/(.+?)/\?ref_=rlm">(.+?)</a>', re.IGNORECASE | re.DOTALL).findall(listcont)
            for imdb, title in entries:
                xml += "<item>"\
                       "<title>%s</title>"\
                       "<meta>"\
                       "<content>movie</content>"\
                       "<imdb>%s</imdb>"\
                       "<title>%s</title>"\
                       "<year>%s</year>"\
                       "</meta>"\
                       "<link></link>"\
                       "<thumbnail></thumbnail>"\
                       "<fanart></fanart>"\
                       "</item>" % (title, imdb, title, year)
        except:
            continue

    xbmcgui.Dialog().ok('Upcoming Releases','This list is for future releases only.[CR][CR]You can view trailers and movie information, but links are not yet available for these titles.')

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='imdbNextPage', args=["url"])
def imdbNextPage(url):
    xml = ""
    link = url
    listhtml = getHtml(link)
    match = re.compile(
            '<img alt=".+?"\nclass="loadlate"\nloadlate="(.+?)"\ndata-tconst="(.+?)"\nheight="98"\nsrc=".+?"\nwidth="67" />\n</a>.+?</div>\n.+?<div class="lister-item-content">\n<h3 class="lister-item-header">\n.+?<span class="lister-item-index unbold text-primary">.+?</span>\n.+?\n.+?<a href=".+?"\n>(.+?)</a>\n.+?<span class="lister-item-year text-muted unbold">(.+?)</span>',
            re.IGNORECASE | re.DOTALL).findall(listhtml)
    for thumbnail, imdb, title, year in match:
        name = title + " " + year
        year = year.replace("(","").replace(")","")
        thumbnail = thumbnail.replace("@._V1_UX67_CR0,0,67,98_AL_.jpg","@._V1_UX520_CR0,0,520,700_AL_.jpg")
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
    try:
        next_page = re.compile(
                    '<a href="([^"]+)"\nclass="lister-page-next next-page" ref-marker=adv_nxt>Next &#187;</a>\n.+?</div>\n.+?<br class="clear" />',
                    re.DOTALL | re.IGNORECASE).findall(listhtml)[0]
        xml += "<dir>"\
               "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
               "<imdburl>http://www.imdb.com/search/title%s</imdburl>"\
               "<thumbnail>https://image.ibb.co/gtsNjw/next.png</thumbnail>"\
               "</dir>" % (next_page)
    except:
        pass
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