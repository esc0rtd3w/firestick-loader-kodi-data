"""
    CBS Radio Mystery Theater
    Copyright (C) 2018, Team OTB
    Version 1.0.2

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
          Make the tag relevant to your plugin. <temp_movie> is the example below-----

    Returns the CBS Radio Mystery Theater list-

    <dir>
    <title>CBS Radio Mystery Theater</title>
    <mystery_theater>all</mystery_theater>
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
table_id = "appAY1W1mCvB7qsdk"
table_name = "CBS Radio Mystery Theater 1"
workspace_api_key = "keyikW1exArRfNAWj"
table_id2 = "appXpjnOO50WbF5F3"
table_name2 = "CBS Radio Mystery Theater 2"
workspace_api_key = "keyikW1exArRfNAWj"

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



class Mystery_Theater_List(Plugin):

    name = "mystery_theater"


    def process_item(self, item_xml):
        if "<mystery_theater>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("mystery_theater", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_mystery_theater_movies",
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

            elif "genre" in item.get("mystery_theater", ""):    
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_mystery_theater_genre_movies",
                    'url': item.get("mystery_theater", ""),
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


@route(mode='open_mystery_theater_movies')
def open_movies():
    pins = "PLuginmysterytheatre"
    Items = fetch_from_db2(pins)
    if Items:
        display_data(Items)  
    else:    
        xml = ""
        at = Airtable(table_id, table_name, api_key=workspace_api_key)
        match = at.get_all(maxRecords=1500, view='Grid view')  
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
        at2 = Airtable(table_id2, table_name2, api_key=workspace_api_key)
        match2 = at2.get_all(maxRecords=1500, view='Grid view')  
        for field2 in match2:
            try:
                res = field2['fields']   
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

@route(mode='open_mystery_theater_genre_movies',args=["url"])
def open_genre_movies(url):
    pins = "PLuginmysterytheatre"+url
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
                       "<sublink>%s(Link 1)</sublink>"\
                       "<sublink>%s(Link 2)</sublink>"\
                       "<sublink>%s(Link 3)</sublink>"\
                       "<sublink>%s(Link 4)</sublink>"\
                       "<sublink>%s(Link 5)</sublink>"\
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
   
