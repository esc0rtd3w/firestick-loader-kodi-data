# -*- coding: utf-8 -*-
"""
    air_table.py
    Copyright (C) 2018,
    Version 2.0.2

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


    Returns the Tv Channels-

    <dir>
    <title>Tv Channels</title>
    <Airtable>tv_channels</Airtable>
    </dir>

    Tv Channels2 are links that dont require plugins

    <dir>
    <title>Tv Channels2</title>
    <Airtable>channels2</Airtable>
    </dir>

    Returns the Sports Channels-

    <dir>
    <title>Sports Channels</title>
    <Airtable>sports_channels</Airtable>
    </dir>


    Returns the 24-7 Channels
    <dir>
    <title>24-7 Channels</title>
    <Airtable>247</Airtable>
    </dir>

    --------------------------------------------------------------

"""



from __future__ import absolute_import
import requests
import re
import os
import xbmc
import xbmcaddon
import json
from koding import route
from ..plugin import Plugin
from resources.lib.external.airtable.airtable import Airtable
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from requests.exceptions import HTTPError
import time
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
AddonName = xbmcaddon.Addon(AddonName).getAddonInfo('id')


class AIRTABLE(Plugin):
    name = "airtable"

    def process_item(self, item_xml):
        if "<Airtable>" in item_xml:
            item = JenItem(item_xml)
            if "tv_channels" in item.get("Airtable", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "Tv_channels",
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

            elif "sports_channels" in item.get("Airtable", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "Sports_channels",
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
                

            elif "247" in item.get("Airtable", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "247",
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

            elif "channels2" in item.get("Airtable", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "channels2",
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
            elif "cats/" in item.get("Airtable", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "show_category_channels",
                    'url': item.get("Airtable", ""),
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



@route(mode='Tv_channels')
def new_releases():
    xml = ""
    table_key = 'appw1K6yy7YtatXbm'
    table_name = 'TV_channels'
    at = Airtable(table_key, table_name, api_key='keyikW1exArRfNAWj')
    match = at.search('category', 'type' ,view='Grid view')
    for field in match:
        try:
            res = field['fields']
            channel = res['channel']
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link = res['link']
            link2 = res['link2']
            link3 = res['link3']
            category = res['category']
            xml +=  "<item>"\
                    "<title>%s</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<Airtable>cats/%s/%s/%s</Airtable>"\
                    "</link>"\
                    "</item>" % (channel,thumbnail,fanart,table_key,table_name,channel)
        except:
            pass                
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='Sports_channels')
def new_releases():
    xml = ""
    table_key = 'appFVmVwiMw0AS1cJ'
    table_name = 'Sports_channels'
    at = Airtable(table_key, table_name, api_key='keyikW1exArRfNAWj')
    match = at.search('category', 'type' ,view='Grid view')
    for field in match:
        try:
            res = field['fields']
            channel = res['channel']
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link = res['link']
            link2 = res['link2']
            link3 = res['link3']
            category = res['category']
            xml +=  "<item>"\
                    "<title>%s</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<Airtable>cats/%s/%s/%s</Airtable>"\
                    "</link>"\
                    "</item>" % (channel,thumbnail,fanart,table_key,table_name,channel)

        except:
            pass                
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='247')
def twenty_four_seven():
    xml = ""
    table_key = 'appMiehwc18Akz8Zv'
    table_name = 'twenty_four_seven'
    at = Airtable(table_key, table_name, api_key='keyikW1exArRfNAWj')
    match = at.search('category', 'type' ,view='Grid view')
    for field in match:
        try:
            res = field['fields']
            channel = res['channel']
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link = res['link']
            link2 = res['link2']
            link3 = res['link3']
            category = res['category']
            xml +=  "<item>"\
                    "<title>%s</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<Airtable>cats/%s/%s/%s</Airtable>"\
                    "</link>"\
                    "</item>" % (channel,thumbnail,fanart,table_key,table_name,channel)

        except:
            pass                
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())        

@route(mode='channels2')
def get_channels2():
    xml = ""
    at = Airtable('appycq5PhSS0tygok', 'TV_channels2', api_key='keyikW1exArRfNAWj')
    match = at.get_all(maxRecords=1200, sort=['channel'])
    for field in match:
        try:
            res = field['fields']
            channel = res['channel']
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link = res['link']                  
            xml +=  "<item>"\
                    "<title>%s</title>"\
                    "<meta>"\
                    "<content>movie</content>"\
                    "<imdb></imdb>"\
                    "<title>%s</title>"\
                    "<year></year>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<summary></summary>"\
                    "</meta>"\
                    "<link>"\
                    "<sublink>%s</sublink>"\
                    "</link>"\
                    "</item>" % (channel,channel,thumbnail,fanart,link)
        except:
            pass                
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='show_category_channels',args=["url"])
def get_channels2(url):
    xml = ""
    table_key = url.split("/")[-3]
    table_name = url.split("/")[-2]
    cat = url.split("/")[-1]
    at = Airtable(table_key, table_name, api_key='keyikW1exArRfNAWj')
    match = at.search('category', cat ,view='Grid view')
    for field in match:
        try:
            res = field['fields']
            channel = res['channel']
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            link = res['link']
            link2 = res['link2']
            link3 = res['link3']
            if "plugin" in link:
                if link2 == "-":
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<meta>"\
                           "<content>movie</content>"\
                           "<imdb></imdb>"\
                           "<title>%s</title>"\
                           "<year></year>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>%s</fanart>"\
                           "<summary></summary>"\
                           "</meta>"\
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "</plugin>" % (channel,channel,thumbnail,fanart,link)
                elif link3 == "-":
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<meta>"\
                           "<content>movie</content>"\
                           "<imdb></imdb>"\
                           "<title>%s</title>"\
                           "<year></year>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>%s</fanart>"\
                           "<summary></summary>"\
                           "</meta>"\
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "</plugin>" % (channel,channel,thumbnail,fanart,link,link2)
                else:
                    xml += "<plugin>"\
                           "<title>%s</title>"\
                           "<meta>"\
                           "<content>movie</content>"\
                           "<imdb></imdb>"\
                           "<title>%s</title>"\
                           "<year></year>"\
                           "<thumbnail>%s</thumbnail>"\
                           "<fanart>%s</fanart>"\
                           "<summary></summary>"\
                           "</meta>"\
                           "<link>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "<sublink>%s</sublink>"\
                           "</link>"\
                           "</plugin>" % (channel,channel,thumbnail,fanart,link,link2,link3)                                                                         
            else:
                if link2 == "-":
                    xml +=  "<item>"\
                            "<title>%s</title>"\
                            "<meta>"\
                            "<content>movie</content>"\
                            "<imdb></imdb>"\
                            "<title>%s</title>"\
                            "<year></year>"\
                            "<thumbnail>%s</thumbnail>"\
                            "<fanart>%s</fanart>"\
                            "<summary></summary>"\
                            "</meta>"\
                            "<link>"\
                            "<sublink>%s</sublink>"\
                            "</link>"\
                            "</item>" % (channel,channel,thumbnail,fanart,link)
                elif link3 == "-":
                    xml +=  "<item>"\
                            "<title>%s</title>"\
                            "<meta>"\
                            "<content>movie</content>"\
                            "<imdb></imdb>"\
                            "<title>%s</title>"\
                            "<year></year>"\
                            "<thumbnail>%s</thumbnail>"\
                            "<fanart>%s</fanart>"\
                            "<summary></summary>"\
                            "</meta>"\
                            "<link>"\
                            "<sublink>%s</sublink>"\
                            "<sublink>%s</sublink>"\
                            "</link>"\
                            "</item>" % (channel,channel,thumbnail,fanart,link,link2)
                else:
                    xml +=  "<item>"\
                            "<title>%s</title>"\
                            "<meta>"\
                            "<content>movie</content>"\
                            "<imdb></imdb>"\
                            "<title>%s</title>"\
                            "<year></year>"\
                            "<thumbnail>%s</thumbnail>"\
                            "<fanart>%s</fanart>"\
                            "<summary></summary>"\
                            "</meta>"\
                            "<link>"\
                            "<sublink>%s</sublink>"\
                            "<sublink>%s</sublink>"\
                            "<sublink>%s</sublink>"\
                            "</link>"\
                            "</item>" % (channel,channel,thumbnail,fanart,link,link2,link3)                                                                                      

        except:
            pass                
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

def remove_non_ascii(text):
    return unidecode(text)
