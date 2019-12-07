"""
    air_table All Sports Replays
    Copyright (C) 2018,
    Version 1.0.3
    Jen Live Chat group

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
    <title>All Sports Replays</title>
    <all_sports_replays>all</all_sports_replays>
    </dir> 
 
    <dir>
    <title>NFL Replays</title>
    <all_sports_replays>leagues/NFL/appSJCjNYAtA6KEfA</all_sports_replays>
    </dir> 

    <dir>
    <title>MLB Replays</title>
    <all_sports_replays>leagues/MLB/app8KZcIqmCP2GfTV</all_sports_replays>
    </dir>

    <dir>
    <title>Fottball Replays</title>
    <all_sports_replays>leagues/FOOTBALL/appGrvFmUpnlMqKE4</all_sports_replays>
    </dir>

    <dir>
    <title>Combat Sports Replays</title>
    <all_sports_replays>leagues/COMBAT_SPORTS/app2clmvReSTvxNTy</all_sports_replays>
    </dir>

    <dir>
    <title>Golf Replays</title>
    <all_sports_replays>leagues/GOLF_REPLAY/app3HVqPpxzqVUaGg</all_sports_replays>
    </dir>

    <dir>
    <title>NHL Replays</title>
    <all_sports_replays>leagues/NHL_REPLAY/app5BBPSzTk4D8ij0</all_sports_replays>
    </dir>

    <dir>
    <title>Motor Sports Replays</title>
    <all_sports_replays>leagues/MOTOR_SPORTS/appxkpEmICFgullUz</all_sports_replays>
    </dir>                    

    --------------------------------------------------------------

"""



from __future__ import absolute_import
import requests
import re
import os
import xbmc
import xbmcaddon
from koding import route
from ..plugin import Plugin
from resources.lib.external.airtable.airtable import Airtable
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from requests.exceptions import HTTPError
import datetime, time
from unidecode import unidecode
try: import json
except ImportError: import simplejson as json

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
AddonName = xbmcaddon.Addon(AddonName).getAddonInfo('id')


class All_Sports_Replays(Plugin):
    name = "all_sports_replays"

    def process_item(self, item_xml):
        if "<all_sports_replays>" in item_xml:
            item = JenItem(item_xml) 
            if item.get("all_sports_replays", "") == "all":
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_the_all_sports",
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
            elif "leagues/" in item.get("all_sports_replays", ""):
                big_sports = ['NFL','MLB']
                other_sports = ['COMBAT_SPORTS','MOTOR_SPORTS','FOOTBALL']
                info = item.get("all_sports_replays", "")
                tag = info.split("/")[1]
                if tag in big_sports:   
                    result_item = {
                        'label': item["title"],
                        'icon': item.get("thumbnail", addon_icon),
                        'fanart': item.get("fanart", addon_fanart),
                        'mode': "open_the_main_leagues_replays",
                        'url': item.get("all_sports_replays", ""),
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
                elif tag in other_sports:   
                    result_item = {
                        'label': item["title"],
                        'icon': item.get("thumbnail", addon_icon),
                        'fanart': item.get("fanart", addon_fanart),
                        'mode': "open_the_main_other_leagues_replays",
                        'url': item.get("all_sports_replays", ""),
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
                else:                                               
                    result_item = {
                        'label': item["title"],
                        'icon': item.get("thumbnail", addon_icon),
                        'fanart': item.get("fanart", addon_fanart),
                        'mode': "open_the_other_leagues_replays",
                        'url': item.get("all_sports_replays", ""),
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
            elif "seasons/" in item.get("all_sports_replays", ""):
                if "NFL_SUPERBOWL" in item.get("all_sports_replays", ""):
                    result_item = {
                        'label': item["title"],
                        'icon': item.get("thumbnail", addon_icon),
                        'fanart': item.get("fanart", addon_fanart),
                        'mode': "open_the_other_leagues_replays",
                        'url': item.get("all_sports_replays", ""),
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
                else:                    
                    result_item = {
                        'label': item["title"],
                        'icon': item.get("thumbnail", addon_icon),
                        'fanart': item.get("fanart", addon_fanart),
                        'mode': "open_the_seasons_replays",
                        'url': item.get("all_sports_replays", ""),
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
            elif "week/" in item.get("all_sports_replays", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_the_weeks_replays",
                    'url': item.get("all_sports_replays", ""),
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
            elif "main/" in item.get("all_sports_replays", ""):                       
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_the_leagues_replays",
                    'url': item.get("all_sports_replays", ""),
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



@route(mode='open_the_all_sports')
def open_table():
    xml = ""
    at = Airtable('appighRQxbaYJz1um', 'sports_replay_main', api_key='keybx0HglywRKFmyS')
    match = at.get_all(maxRecords=700, view='Grid view') 
    for field in match:
        try:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link = res['link']                           
            xml +=  "<item>"\
                    "<title>[COLORred]%s[/COLOR]</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<all_sports_replays>leagues/%s</all_sports_replays>"\
                    "</link>"\
                    "</item>" % (name,thumbnail,fanart,link)                                          
        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_the_main_other_leagues_replays',args=["url"])
def open_table(url):
    xml = ""
    table = url.split("/")[-2]
    key = url.split("/")[-1]
    at = Airtable(key, table, api_key='keybx0HglywRKFmyS')
    match = at.get_all(maxRecords=700, view='Grid view')                                  
    for field in match:
        try:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link = res['link']                        
            xml +=  "<item>"\
                    "<title>[COLORred]%s[/COLOR]</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<all_sports_replays>leagues/%s</all_sports_replays>"\
                    "</link>"\
                    "</item>" % (name,thumbnail,fanart,link)                                          

        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_the_main_leagues_replays',args=["url"])
def open_table(url):
    xml = ""
    table = url.split("/")[-2]
    key = url.split("/")[-1]
    at = Airtable(key, table, api_key='keybx0HglywRKFmyS')
    match = at.get_all(maxRecords=700, view='Grid view')                                  
    for field in match:
        try:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link = res['link']                        
            xml +=  "<item>"\
                    "<title>[COLORred]%s[/COLOR]</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<all_sports_replays>main/%s</all_sports_replays>"\
                    "</link>"\
                    "</item>" % (name,thumbnail,fanart,link)                                          

        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_the_leagues_replays',args=["url"])
def open_table(url):
    xml = ""
    table = url.split("/")[-2]
    key = url.split("/")[-1]
    at = Airtable(key, table, api_key='keybx0HglywRKFmyS')
    match = at.get_all(maxRecords=700, view='Grid view')                                  
    for field in match:
        try:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link = res['link']                        
            xml +=  "<item>"\
                    "<title>[COLORred]%s[/COLOR]</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<all_sports_replays>seasons/%s</all_sports_replays>"\
                    "</link>"\
                    "</item>" % (name,thumbnail,fanart,link)                                          

        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_the_other_leagues_replays',args=["url"])
def open_table(url):
    xml = ""
    table = url.split("/")[-2]
    key = url.split("/")[-1]
    at = Airtable(key, table, api_key='keybx0HglywRKFmyS')
    match = at.get_all(maxRecords=700, view='Grid view') 
    for field in match:
        try:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']                                   
            if link2 == "-":
                xml +=  "<item>"\
                        "<title>[COLORred]%s[/COLOR]</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (name,thumbnail,fanart,link1)                                          
            elif link3 == "-":
                xml +=  "<item>"\
                        "<title>[COLORred]%s[/COLOR]</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (name,thumbnail,fanart,link1,link2)
            elif link4 == "-":
                xml +=  "<item>"\
                        "<title>[COLORred]%s[/COLOR]</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (name,thumbnail,fanart,link1,link2,link3)
            else:                
                xml +=  "<item>"\
                        "<title>[COLORred]%s[/COLOR]</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (name,thumbnail,fanart,link1,link2,link3,link4)                                          

        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_the_seasons_replays',args=["url"])
def open_table(url):
    xml = ""
    table = url.split("/")[-2]
    key = url.split("/")[-1]
    at = Airtable(key, table, api_key='keybx0HglywRKFmyS')
    match = at.search('category', 'Week' ,view='Grid view') 
    for field in match:
        try:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            category = res['category']                        
            xml +=  "<item>"\
                    "<title>[COLORred]%s[/COLOR]</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<all_sports_replays>week/%s/%s/%s</all_sports_replays>"\
                    "</link>"\
                    "</item>" % (name,thumbnail,fanart,name,table,key)                                          

        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_the_weeks_replays',args=["url"])
def open_table(url):
    xml = ""
    table = url.split("/")[-2]
    key = url.split("/")[-1]
    cat = url.split("/")[-3]
    at = Airtable(key, table, api_key='keybx0HglywRKFmyS')
    match = at.search('category', cat ,view='Grid view') 
    for field in match:
        try:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            category = res['category']
            score = res['score']
            if score == "-":
                score = ""
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            link4 = res['link4']
            link5 = res['link5']          
            dsp = name + "    " + "[B][COLORdodgerblue]%s[/COLOR][/B]" % score                        
            if link2 == "-":
                xml +=  "<item>"\
                        "<title>[COLORred]%s[/COLOR]</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1)                                          
            elif link3 == "-":
                xml +=  "<item>"\
                        "<title>[COLORred]%s[/COLOR]</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2)
            elif link4 == "-":
                xml +=  "<item>"\
                        "<title>[COLORred]%s[/COLOR]</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2,link3)
            elif link5 == "-":
                xml +=  "<item>"\
                        "<title>[COLORred]%s[/COLOR]</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2,link3,link4)
            else:                
                xml +=  "<item>"\
                        "<title>[COLORred]%s[/COLOR]</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2,link3,link4,link5)                                          

        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


def remove_non_ascii(text):
    return unidecode(text)
        
