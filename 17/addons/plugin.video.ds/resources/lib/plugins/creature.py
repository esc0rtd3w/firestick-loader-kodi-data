# -*- coding: utf-8 -*-
"""
    air_table The Creature Feature
    Copyright (C) 2018,
    Version 1.0.2
    Kyle Adams

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


    Returns the Creature Feature List-

    <dir>
    <title>The Creature Feature List</title>
    <creature>all</creature>
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

class Creature_Feature(Plugin):
    name = "creature"

    def process_item(self, item_xml):
        if "<creature>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("creature", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_the_creature_feature_table",
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
            elif "type/" in item.get("creature", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_the_creature_type",
                    'url': item.get("creature", ""),
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


@route(mode='open_the_creature_feature_table')
def open_table():
    pins = "PLugincreature"
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:    
        xml = ""
        at = Airtable('appvv8DXDsLjqkekU', 'Creature', api_key='keyikW1exArRfNAWj')
        match = at.search('type', 'type' ,view='Grid view') 
        for field in match:
            try:
                res = field['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                trailer = res['trailer']
                summary = res['summary']
                summary = remove_non_ascii(summary)                                                 
                xml += "<item>"\
                       "<title>%s</title>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>%s</fanart>"\
                       "<creature>type/%s</creature>"\
                       "</item>" % (name,res['thumbnail'],res['fanart'],name)
            except:
                pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)
                       
@route(mode='open_the_creature_type',args=["url"])
def open_table(url):
    pins = "PLugincreature"+ url
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:    
        xml = ""
        category = url.split("/")[-1]
        at = Airtable('appvv8DXDsLjqkekU', 'Creature', api_key='keyikW1exArRfNAWj')
        match = at.search('type', category ,view='Grid view') 
        for field in match:
            try:
                res = field['fields']   
                name = res['name']
                name = remove_non_ascii(name)
                trailer = res['trailer']
                summary = res['summary']
                summary = remove_non_ascii(summary)
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                link_a = res['link_a']
                link_b = res['link_b']
                link_c = res['link_c']
                link_d = res['link_d']
                link_e = res['link_e']                                                           
                if link_b == "-":
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
                         "<sublink>%s(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link_a,trailer)
                elif link_c == "-":
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
                         "<sublink>%s(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link_a,link_b,trailer) 
                elif link_d == "-":
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
                         "<sublink>%s(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link_a,link_b,link_c,trailer)
                elif link_e == "-":
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
                         "<sublink>%s(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link_a,link_b,link_c,link_d,trailer)
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
                         "<sublink>%s(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name,thumbnail,fanart,summary,link_a,link_b,link_c,link_d,link_e,trailer)
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
        print created_time + "created"
        print time.time() 
        print CACHE_TIME
        test_time = float(created_time) + CACHE_TIME 
        print test_time
        if float(created_time) + CACHE_TIME <= time.time():
            koding.Remove_Table(url2)
            db = sqlite3.connect('%s' % (database_loc))        
            cursor = db.cursor()
            db.execute("vacuum")
            db.commit()
            db.close()
            display_list2(result, "video", url2)
        else:
            pass                     
        return result
    else:
        return []

def remove_non_ascii(text):
    return unidecode(text)
        
