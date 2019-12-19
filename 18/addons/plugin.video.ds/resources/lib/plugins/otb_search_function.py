# -*- coding: utf-8 -*-
"""
    OTB Search Function
    Version 1.0.2
    Copyright (C) 2018,

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
    Searches the OTB Big Movies List with a fuzzy search

    Usage Examples:


    <dir>
    <title>OTB Movie Search</title>
    <otbser>movies</otbser>
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


class OTB_Search_Function(Plugin):
    name = "otb_search_function"

    def process_item(self, item_xml):
        if "<otbser>" in item_xml:
            item = JenItem(item_xml)
            if "movies" in item.get("otbser", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_search_movies",
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
                

@route(mode='open_otb_search_movies')
def open_movie_results():
    pins = ""
    xml = ""
    show = koding.Keyboard(heading='Movie Name')
    movie_list = []
    at = Airtable('app27kXZLXlXw0gRh', 'the_duke', api_key='keyikW1exArRfNAWj')
    match = at.get_all(maxRecords=1200, sort=["name"])
    for field in match:
        res = field['fields']        
        name = res['name']
        name = remove_non_ascii(name)
        try:
            movie_list.append(name)
        except:
            pass
    at2 = Airtable('appvv8DXDsLjqkekU', 'Creature', api_key='keyikW1exArRfNAWj')

    match2 = at2.get_all(maxRecords=1200, sort=["name"])
    for field2 in match2:
        res2 = field2['fields']        
        name2 = res2['name']
        name2 = remove_non_ascii(name2)
        try:
            movie_list.append(name2)
        except:
            pass       
    at3 = Airtable('appbXfuDDhnWqYths', 'bnw_movies', api_key='keyikW1exArRfNAWj')
    match5 = at3.get_all(maxRecords=1200, sort=["name"])
    for field3 in match5:
        res3 = field3['fields']        
        name3 = res3['name']
        name3 = remove_non_ascii(name3)
        try:
            movie_list.append(name3)
        except:
            pass                                                         
    search_result = koding.Fuzzy_Search(show, movie_list)
    if not search_result:
        xbmc.log("--------no results--------",level=xbmc.LOGNOTICE)
        xml += "<item>"\
            "<title>[COLOR=orange][B]Movie was not found[/B][/COLOR]</title>"\
            "</item>"
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)                     
    for item in search_result:
        item2 = str(item)
        item2 = remove_non_ascii(item2)
        xbmc.log(item2,level=xbmc.LOGNOTICE)
        try:          
            match3 = at.search("name", item2)
            for field2 in match3:
                res2 = field2['fields']        
                name2 = res2["name"]
                name3 = remove_non_ascii(name2)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link_a = res2['link_a']
                link_b = res2['link_b']
                link_c = res2['link_c']
                link_d = res2['link_d']
                link_e = res2['link_e']
                trailer = res2['trailer']
                xml += display_xml(name2,trailer,summary,thumbnail,fanart,link_a,link_b,link_c,link_d,link_e)
        except:
            pass 
        try:                                          
            match4 = at2.search("name", item2)
            for field2 in match4:
                res2 = field2['fields']        
                name2 = res2["name"]
                name3 = remove_non_ascii(name2)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link_a = res2['link_a']
                link_b = res2['link_b']
                link_c = res2['link_c']
                link_d = res2['link_d']
                link_e = res2['link_e']
                trailer = res2['trailer']
                xml += display_xml(name2,trailer,summary,thumbnail,fanart,link_a,link_b,link_c,link_d,link_e)
        except:
            pass
        try:            
            match6 = at3.search("name", item2)
            for field2 in match6:
                res2 = field2['fields']        
                name2 = res2["name"]
                name3 = remove_non_ascii(name2)
                fanart = res2['fanart']
                thumbnail = res2['thumbnail']
                summary = res2['summary']
                summary = remove_non_ascii(summary)
                link1 = res2['link1']
                link2 = res2['link2']
                link3 = res2['link3']
                link4 = res2['link4']
                trailer = res2['trailer']
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
                         "<sublink>%s(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name2,thumbnail,fanart,summary,link1,trailer)
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
                         "<sublink>%s(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name2,thumbnail,fanart,summary,link1,link2,trailer) 
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
                         "<sublink>%s(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name2,thumbnail,fanart,summary,link1,link2,link3,trailer)
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
                         "<sublink>%s(Trailer)</sublink>"\
                         "</link>"\
                         "</item>" % (name2,thumbnail,fanart,summary,link1,link2,link3,link4,trailer)
        except:
            pass                 
        
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

def display_xml(name2,trailer,summary,thumbnail,fanart,link_a,link_b,link_c,link_d,link_e):
    xml = ""

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
             "</item>" % (name2,thumbnail,fanart,summary,link_a,trailer)
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
             "</item>" % (name2,thumbnail,fanart,summary,link_a,link_b,trailer) 
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
             "</item>" % (name2,thumbnail,fanart,summary,link_a,link_b,link_c,trailer)
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
             "</item>" % (name2,thumbnail,fanart,summary,link_a,link_b,link_c,link_d,trailer)
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
             "</item>" % (name2,thumbnail,fanart,summary,link_a,link_b,link_c,link_d,link_e,trailer)
    return (xml)

          
def remove_non_ascii(text):
    return unidecode(text)
        