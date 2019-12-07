"""

    Copyright (C) 2018, Jen Team
    -- 7-2-18 Version 3.1.0 --

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

    -------------------------------------------------------------

    Usage Examples:

<dir>
<title> Moviefone Trailers</title>
<moviefone>trailers/1</moviefone>
</dir>

<dir>
<title>Search Moviefone Trailers</title>
<moviefone>search</moviefone>
</dir>

"""    

import requests,re,json,os
import koding
import __builtin__
import xbmc,xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode
from time import gmtime, strftime

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class MovieFone(Plugin):
    name = "moviefone"

    def process_item(self, item_xml):
        if "<moviefone>" in item_xml:
            item = JenItem(item_xml)
            if "trailers" in item.get("moviefone", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_moviefone_trailers",
                    'url': item.get("moviefone", ""),
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
            elif "search" in item.get("moviefone",""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "search_moviefone_trailers",
                    'url': item.get("moviefone", ""),
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
            elif "link" in item.get("moviefone",""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_moviefone_trailer_link",
                    'url': item.get("moviefone", ""),
                    'folder': False,
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
            elif "result" in item.get("moviefone",""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_moviefone_result_link",
                    'url': item.get("moviefone", ""),
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


@route(mode='get_moviefone_trailers', args=["url"])
def get_game(url):
    xml = ""
    current = url.split("/")[-1]
    try:    
        url = "https://www.moviefone.com/movie-trailers/videos/?page="+current
        html = requests.get(url).content
        match = re.compile('<a class="poster-link" href="(.+?)".+?data-src="(.+?)".+?alt="(.+?)".+?<div class="description">(.+?)</div>',re.DOTALL).findall(html)
        for link1,thumbnail,name,summary in match:
            name = name.replace("&#039;","")
            name = remove_non_ascii(name)
            summary = clean_search(summary)
            xml += "<item>"\
                   "<title>%s</title>"\
                   "<meta>"\
                   "<content>movie</content>"\
                   "<imdb></imdb>"\
                   "<title></title>"\
                   "<year></year>"\
                   "<thumbnail>%s</thumbnail>"\
                   "<fanart>%s</fanart>"\
                   "<summary>%s</summary>"\
                   "</meta>"\
                   "<moviefone>link**%s</moviefone>"\
                   "</item>" % (name,thumbnail,thumbnail,summary,link1)            
        try:
            next_page = int(current)+1
            xml += "<dir>"\
                   "<title>[COLOR dodgerblue]Next Page >>[/COLOR]</title>"\
                   "<moviefone>trailers/%s</moviefone>"\
                   "<thumbnail>http://www.clker.com/cliparts/a/f/2/d/1298026466992020846arrow-hi.png</thumbnail>"\
                   "</dir>" % (next_page)                                  
        except:
            pass
    except:
        pass        
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type()) 

@route(mode='get_moviefone_trailer_link', args=["url"])
def get_game(url):
    xml = ""
    try:
        koding.Show_Busy(status=True)
        link1 = url.split("**")[-1]
        html2 = requests.get(link1).content
        match2 = re.compile('<div id="trailer-player">.+?src="(.+?)"',re.DOTALL).findall(html2)
        link2 = "http:" + match2[0]
        html3 = requests.get(link2).content
        match3 = re.compile('"videoUrls":.+?,"(.+?)"',re.DOTALL).findall(html3)
        link3 = match3[0]
        koding.Show_Busy(status=False )
        xbmc.Player().play(link3)
    except:
        pass                        

@route(mode='get_moviefone_result_link', args=["url"])
def get_result(url):
    xml = ""
    try:
        open_url = url.split("**")[-1]
        open_url = open_url.replace("main/","trailers/")
        html3 = requests.get(open_url).content
        block3 = re.compile('Movie Trailers</a>(.+?)<h2>Top Trailers</h2>',re.DOTALL).findall(html3)
        match3 = re.compile('<div class="trailer-item">.+?href="(.+?)".+?data-src="(.+?)".+?<div class="photo-name">(.+?)</div>',re.DOTALL).findall(str(block3))
        for link2,thumbnail,name in match3:
            name = name.replace("&#039;","")
            name = remove_non_ascii(name)
            xml += "<item>"\
                   "<title>%s</title>"\
                   "<meta>"\
                   "<content>movie</content>"\
                   "<imdb></imdb>"\
                   "<title></title>"\
                   "<year></year>"\
                   "<thumbnail>%s</thumbnail>"\
                   "<fanart>%s</fanart>"\
                   "<summary></summary>"\
                   "</meta>"\
                   "<moviefone>link**%s</moviefone>"\
                   "</item>" % (name,thumbnail,thumbnail,link2)
    except:
        pass                                               
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type()) 

@route(mode='search_moviefone_trailers', args=["url"])
def search_trailers(url):
    xml = ""
    try:
        search_query = koding.Keyboard(heading='Search for Trailers')
        search_query = search_query.replace(" ","%20")
        url = "https://www.moviefone.com/search/%s/" % search_query
        headers = {'User_Agent' : User_Agent}
        html = requests.get(url,headers=headers).content
        block = re.compile('<h1>Search results for(.+?)<h2>Top Trailers',re.DOTALL).findall(html)
        try:
            match = re.compile('data-src="(.+?)".+?alt="(.+?)".+?<a href="(.+?)".+?<p class="search-description">(.+?)</p>.+?<div class="search-more-links">.+?">(.+?)</a>',re.DOTALL).findall(str(block))
            for thumbnail,name,link1,summary,key2 in match:
                if key2 == "Trailers":
                    name = name.replace("&#039;","")
                    name = remove_non_ascii(name)
                    summary = clean_search(summary)
                    xml += "<item>"\
                           "<title>%s</title>"\
                           "<meta>"\
                           "<content>movie</content>"\
                           "<imdb></imdb>"\
                           "<title></title>"\
                           "<year></year>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>%s</fanart>"\
                           "<summary>%s</summary>"\
                           "</meta>"\
                           "<moviefone>result**%s</moviefone>"\
                           "</item>" % (name,thumbnail,thumbnail,summary,link1)
       
            if xml == "":
                xml += "<item>"\
                       "<title>No Results</title>"\
                       "<meta>"\
                       "<content>movie</content>"\
                       "<imdb></imdb>"\
                       "<title></title>"\
                       "<year></year>"\
                       "<thumbnail></thumbnail>"\
                       "<fanart></fanart>"\
                       "<summary></summary>"\
                       "</meta>"\
                       "<link></link>"\
                       "</item>"                                      
        except:
            pass                                 
    except:
        pass                                                              
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type()) 

def remove_non_ascii(text):
    return unidecode(text)

def clean_search(title):
    if title == None: return
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\\\|/|\(|\)|\[|\]|\{|\}|-|:|;|\*|\?|"|\'|<|>|\_|\.|\?', ' ', title)
    title = ' '.join(title.split())
    return title            
            