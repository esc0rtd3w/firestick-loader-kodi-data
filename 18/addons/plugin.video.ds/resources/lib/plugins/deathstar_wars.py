# -*- coding: utf-8 -*-
"""
    DeathStar Wars
    Copyright (C) 2018,
    Version 1.0.1

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

    -------- These are the xml examples you place in your xml to call the plugin
          Make the tag relevant to your plugin. <temp4_movie> is the example below-----

    Returns the temp4late Movie list-

    <dir>
    <title>Star Wars Movies</title>
    <temp4_movie>movies</temp4_movie>
	<fanart></fanart>
	<thumbnail></thumbnail>
    </dir>


    ---------------------

    Possible Genre's are:
    Documentary
    Extras
	Movie
    Audio Books
    -----------------------

    Genre tag examples

    <dir>
    <title>Star Wars Movies</title>
    <temp4_movie>genre/Movie</temp4_movie>
	<fanart>http://ukodi1.com/images/G4xUAWx.jpg</fanart>
	<thumbnail>http://uk1.site/images/movie.png</thumbnail>
	<summary>All Star Wars Movies</summary>
    </dir>

    <dir>
    <title>Star Wars Documentaries</title>
    <temp4_movie>genre/Documentary</temp4_movie>
	<fanart>http://ukodi1.com/images/G4xUAWx.jpg</fanart>
	<thumbnail>http://uk1.site/images/doc's.png</thumbnail>
	<summary>Star Wars Docs</summary>
    </dir>    
	
	<dir>
    <title>Star Wars Extras</title>
    <temp4_movie>genre/Extras</temp4_movie>
	<fanart>http://ukodi1.com/images/G4xUAWx.jpg</fanart>
	<thumbnail>http://uk1.site/images/EXTRA.png</thumbnail>
	<summary>Extras & Fan Made</summary>
    </dir> 
	
	<dir>
    <title>Star Wars Audio Books</title>
    <temp4_movie>genre/Audio Books</temp4_movie>
	<fanart>http://ukodi1.com/images/G4xUAWx.jpg</fanart>
	<thumbnail>http://uk1.site/images/AUDIO.png</thumbnail>
	<summary>Audio Books</summary>
    </dir> 

    --------------------------------------------------------------

"""


import requests,re,os,xbmc,xbmcaddon
import base64,pickle,koding,time,sqlite3
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list, display_data, clean_url
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode


"""
----------------------------------------------------------
"""
table_id = "apppxFvFzSNbUjBJn"
table_name = "Star Wars"
workspace_api_key = "keyFw4tAzBr8ximp0"
"""
----------------------------------------------------------
"""


CACHE_TIME = 86400  # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
home_folder = xbmc.translatePath('special://home/')
user_data_folder = os.path.join(home_folder, 'userdata')
addon_data_folder = os.path.join(user_data_folder, 'addon_data')
database_path = os.path.join(addon_data_folder, addon_id)
database_loc = os.path.join(database_path, 'database.db')



class temp4late_Movie_List(Plugin):

    name = "temp4late_movie_list"


    def process_item(self, item_xml):
        if "<temp4_movie>" in item_xml:
            item = JenItem(item_xml)
            if "movies" in item.get("temp4_movie", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_temp4late_movies",
                    'url': "",
                    'folder': True,
                    'imdb': "0",
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

            elif "genre" in item.get("temp4_movie", ""):    
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_temp4late_genre_movies",
                    'url': item.get("temp4_movie", ""),
                    'folder': True,
                    'imdb': "0",
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


@route(mode='open_temp4late_movies')
def open_movies():
    pins = "PLugindeathstarwarsmovies"
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items)  
    else:    
        xml = ""
        at = Airtable(table_id, table_name, api_key=workspace_api_key)
        match = at.get_all(maxRecords=1200, sort=['name'])  
        for field in match:
            try:
                res = field['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                fanart = res['fanart']
                thumbnail = res['thumbnail']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
                link5 = res['link5']
                if link2 == "-":
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1)
                elif link3 == "-":
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2) 
                elif link4 == "-":
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3)
                elif link5 == "-":
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)           
                else:
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4,link5) 
            except:
                pass                                                                     
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='open_temp4late_genre_movies',args=["url"])
def open_genre_movies(url):
    pins = "PLugindeathsarwars"+url
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items)  
    else:    
        xml = ""
        genre = url.split("/")[-1]
        at = Airtable(table_id, table_name, api_key=workspace_api_key)
        try:
            match = at.search('type', genre)
            for field in match:
                res = field['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)
                fanart = res['fanart']
                thumbnail = res['thumbnail']
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
                link5 = res['link5'] 
                if link2 == "-":
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1)
                elif link3 == "-":
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2) 
                elif link4 == "-":
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3)
                elif link5 == "-":
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)           
                else:
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
                         "<link>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>%s</sublink>"\
                         "<sublink>(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4,link5)                   
        except:
            pass                  
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

def fetch_from_db2(url):
    koding.reset_db()
    url2 = clean_url(url)
    match = koding.Get_All_From_Table(url2)
    if match:
        match = match[0]
        if not match["value"]:
            return None   
        match_item = match["value"]
        try:
                result = pickle.loads(base64.b64decode(match_item))
        except:
                return None
        created_time = match["created"]
        if float(created_time) + CACHE_TIME <= time.time():
            koding.Remove_Table(url2)
            db = sqlite3.connect('%s' % (database_loc))        
            cursor = db.cursor()
            db.execute("vacuum")
            db.commit()
            db.close()
            return result
        else:
            pass                     
        return result
    else:
        return []

def remove_non_ascii(text):
    return unidecode(text)
   