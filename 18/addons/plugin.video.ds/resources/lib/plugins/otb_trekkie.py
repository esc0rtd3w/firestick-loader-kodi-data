# -*- coding: utf-8 -*-
"""
    OTB Trekkie
    Copyright (C) 2018,
    Version 1.0.1
    Team OTB

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


    Returns the OTB trekkie List

    <dir>
    <title>OTB Trekkie</title>
    <trekkie>all</trekkie>
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

class Otb_Trekkie(Plugin):
    name = "otb_trekkie"

    def process_item(self, item_xml):
        if "<trekkie>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("trekkie", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_trekkie_list",
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
            elif "open|" in item.get("trekkie", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otb_items",
                    'url': item.get("trekkie", ""),
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
            elif "shows|" in item.get("trekkie", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_trek_shows",
                    'url': item.get("trekkie", ""),
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
            elif "tv_shows|" in item.get("trekkie", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_trek_tv_shows",
                    'url': item.get("trekkie", ""),
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
            elif "season|" in item.get("trekkie", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_trek_season",
                    'url': item.get("trekkie", ""),
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


@route(mode='open_otb_trekkie_list')
def open_list():
    pins = "PLuginotbtrekkiemain"
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:
        xml = ""
        at = Airtable('appRSOovERyPqtopl', 'otb_trekkie', api_key='keyikW1exArRfNAWj')
        match = at.get_all(maxRecords=1200, view='Grid view') 
        for field in match:
            try:
                res = field['fields']   
                name = res['Name']
                name = remove_non_ascii(name)
                summary = res['summary']
                summary = remove_non_ascii(summary)                                                 
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
                       "<trekkie>open|%s</trekkie>"\
                       "</item>" % (name,res['thumbnail'],res['fanart'],summary,res['link1'])
            except:
                pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)

@route(mode='open_otb_items',args=["url"])
def open_items(url):
    xml = ""
    title = url.split("|")[-2]
    key = url.split("|")[-1]
    at = Airtable(key, title, api_key='keyikW1exArRfNAWj')
    match = at.get_all(maxRecords=1200, view='Grid view')
    if title == "Star_Trek_Movies":
        pins = "PLuginotbtrekkiemovies"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['Name']
                    name = remove_non_ascii(name)
                    trailer = res['trailer']
                    imdb = res['imdb']
                    link1 = res['link1']
                    link2 = res['link2']
                    link3 = res['link3']
                    link4 = res['link4']                                                 
                    xml += "<item>"\
                           "<title>%s</title>"\
                           "<meta>"\
                           "<content>movie</content>"\
                           "<imdb>%s</imdb>"\
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
                           "</item>" % (name,imdb,thumbnail,fanart,summary,link1,link2,link3,link4,trailer)
                except:
                    pass                                                                     
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)                               
    elif title == "Star_Trek_Extras":
        pins = "PLuginotbtrekkieextras"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['Name']
                    name = remove_non_ascii(name)
                    link1 = res['link1']
                    link2 = res['link2']
                    link3 = res['link3']
                    link4 = res['link4']                                                 
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
                           "</link>"\
                           "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)
                except:
                    pass                                                                     
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)        
    elif title == "Unofficial_Movies":
        pins = "PLuginotbtrekkieunofficialmovies"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['Name']
                    name = remove_non_ascii(name)
                    trailer = res['trailer']
                    link1 = res['link1']
                    link2 = res['link2']
                    link3 = res['link3']
                    link4 = res['link4']                                                 
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
                           "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4,trailer)
                except:
                    pass                                                                     
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)
    elif title == "TV_Shows":
        pins = "PLuginotbtrekkietvshows"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['Name']
                    name = remove_non_ascii(name)
                    link1 = res['link1']                                                 
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
                           "<trekkie>shows|%s</trekkie>"\
                           "</link>"\
                           "</item>" % (name,thumbnail,fanart,summary,link1)
                except:
                    pass                                                                     
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)
    elif title == "Unofficial_Series":
        pins = "PLuginotbtrekkieseries"
        Items = fetch_from_db2(pins)
        if Items: 
            display_data(Items) 
        else:        
            for field in match:
                try:
                    res = field['fields']   
                    thumbnail = res['thumbnail']
                    fanart = res['fanart']
                    summary = res['summary']
                    summary = remove_non_ascii(summary)                   
                    name = res['Name']
                    name = remove_non_ascii(name)
                    link1 = res['link1']                                                 
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
                           "<trekkie>shows|%s</trekkie>"\
                           "</link>"\
                           "</item>" % (name,thumbnail,fanart,summary,link1)
                except:
                    pass                                                                     
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='open_trek_shows',args=["url"])
def open_items(url):
    pins = "PLuginotbtrekkieshows"+url
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:    
        xml = ""
        title = url.split("|")[-2]
        key = url.split("|")[-1]
        result = title+"_season"
        at = Airtable(key, title, api_key='keyikW1exArRfNAWj')
        match = at.search('category', result,view='Grid view')
        for field in match:
            try:
                res = field['fields']   
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                summary = res['summary']
                summary = remove_non_ascii(summary)                   
                name = res['Name']
                name = remove_non_ascii(name)
                link1 = res['link1']
                url2 = title+"|"+key+"|"+name                                                 
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
                       "<trekkie>season|%s</trekkie>"\
                       "</link>"\
                       "</item>" % (name,thumbnail,fanart,summary,url2)
            except:
                pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)    

@route(mode='open_trek_season',args=["url"])
def open_items(url):
    pins = "PLuginotbtrekkieseason"+url
    Items = fetch_from_db2(pins)
    if Items: 
        display_data(Items) 
    else:    
        xml = ""
        title = url.split("|")[-3]
        key = url.split("|")[-2]
        sea_name = url.split("|")[-1]
        result = title+"_"+sea_name
        at = Airtable(key, title, api_key='keyikW1exArRfNAWj')
        match = at.search('category', result,view='Grid view')
        for field in match:
            try:
                res = field['fields']
                thumbnail = res['thumbnail']
                fanart = res['fanart']
                summary = res['summary']
                summary = remove_non_ascii(summary)                   
                name = res['Name']
                name = remove_non_ascii(name)
                link1 = res['link1']
                link2 = res['link2']
                link3 = res['link3']
                link4 = res['link4']
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
                       "</link>"\
                       "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3,link4)                                                               
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
        
