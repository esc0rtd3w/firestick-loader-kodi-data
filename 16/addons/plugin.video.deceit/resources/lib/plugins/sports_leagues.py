"""
    Air_table Sports Leagues
    Copyright (C) 2018,
    Version 2.0.0
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

        NOTHING TO SEE HERE NOSEY  ;-)

    --------------------------------------------------------------

"""



from __future__ import absolute_import
import requests
import re
import os
import xbmc
import xbmcaddon
import base64
from koding import route
from ..plugin import Plugin
from resources.lib.external.airtable.airtable import Airtable
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from requests.exceptions import HTTPError
import datetime, time
from unidecode import unidecode
from dateutil.parser import parse
from dateutil.tz import gettz
from dateutil.tz import tzlocal
try: import json
except ImportError: import simplejson as json

CACHE_TIME = 3600  # change to wanted cache time in seconds
bec = base64.b64encode
bdc = base64.b64decode
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
AddonName = xbmcaddon.Addon(AddonName).getAddonInfo('id')
yai = bec(AddonName)
tid = bdc('YXBweHNIWGJ3RWVhYVd0S2Y=')
tnm = bdc('cGx1Z2luX2lk')
atk = bdc('a2V5T0hheHNUR3pIVTlFRWg=')

try:
    local_tzinfo = tzlocal()
    locale_timezone = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": "locale.timezone"}, "id": 1}'))
    if locale_timezone['result']['value']:
        local_tzinfo = gettz(locale_timezone['result']['value'])
except:
    pass

def convDateUtil(timestring, newfrmt='default', in_zone='UTC'):
    if newfrmt == 'default':
        newfrmt = xbmc.getRegion('time').replace(':%S','')
    try:
        in_time = parse(timestring)
        in_time_with_timezone = in_time.replace(tzinfo=gettz(in_zone))
        local_time = in_time_with_timezone.astimezone(local_tzinfo)
        return local_time.strftime(newfrmt)
    except:
        return timestring
#'mode': "open_the_league_main",
class Sports_Leagues(Plugin):
    name = "sports_leagues"

    def process_item(self, item_xml):
        if "<sports_leagues>" in item_xml:
            item = JenItem(item_xml)              
            if item.get("sports_leagues", "") == "all":
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_the_all_league",
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
            elif "league/" in item.get("sports_leagues", ""):
                sports = ['NFL','NBA','NHL']
                info = item.get("sports_leagues", "")
                tag = info.split("/")[1]
                if tag in sports:                
                    result_item = {
                        'label': item["title"],
                        'icon': item.get("thumbnail", addon_icon),
                        'fanart': item.get("fanart", addon_fanart),
                        'mode': "open_the_league_seasons",
                        'url': item.get("sports_leagues", ""),
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
                        'mode': "open_the_other_league_main",
                        'url': item.get("sports_leagues", ""),
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
            elif "season/" in item.get("sports_leagues", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_the_league_seasons",
                    'url': item.get("sports_leagues", ""),
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
            elif "week/" in item.get("sports_leagues", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_the_week_list",
                    'url': item.get("sports_leagues", ""),
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

@route(mode='open_the_all_league')
def open_table():
    xml = ""
    lai = []
    at1 = Airtable(tid, tnm, api_key=atk)
    m1 = at1.get_all(maxRecords=700, view='Grid view') 
    for f1 in m1:
        r1 = f1['fields']   
        n1 = r1['au1']
        lai.append(n1)
    if yai in lai:
        pass
    else:
        exit()    
    at = Airtable('appbwmFXMwN9WaOu2', 'Leagues', api_key='keyikW1exArRfNAWj')
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
                    "<title>%s</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<sports_leagues>league/%s</sports_leagues>"\
                    "</link>"\
                    "</item>" % (name,thumbnail,fanart,link)                                          

        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_the_league_main',args=["url"])
def open_table(url):
    xml = ""
    lai = []
    at1 = Airtable(tid, tnm, api_key=atk)
    m1 = at1.get_all(maxRecords=700, view='Grid view') 
    for f1 in m1:
        r1 = f1['fields']   
        n1 = r1['au1']
        lai.append(n1)
    if yai in lai:
        pass
    else:
        exit()    
    table = url.split("/")[-2]
    key = url.split("/")[-1]
    at = Airtable(key, table, api_key='keyikW1exArRfNAWj')
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
                    "<title>%s</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<sports_leagues>season/%s</sports_leagues>"\
                    "</link>"\
                    "</item>" % (name,thumbnail,fanart,link)                                          

        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='open_the_other_league_main',args=["url"])
def open_table(url):
    xml = ""
    lai = []
    at1 = Airtable(tid, tnm, api_key=atk)
    m1 = at1.get_all(maxRecords=700, view='Grid view') 
    for f1 in m1:
        r1 = f1['fields']   
        n1 = r1['au1']
        lai.append(n1)
    if yai in lai:
        pass
    else:
        exit()    
    table = url.split("/")[-2]
    key = url.split("/")[-1]
    at = Airtable(key, table, api_key='keyikW1exArRfNAWj')
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
            link5 = res['link5']
            link6 = res['link6']
            time = res['Time']
            if time == "-":
                time = ""
                dsp = name    
            else:
                if "Final Score" in time:
                    time2 = time
                    dec = ""
                else:    
                    time2 = time.split("@")[-1]
                    dec = time.split("@")[0]    
                (display_time) = convDateUtil(time2, 'default', 'US/Eastern')
                dsp = ("[B][COLORdodgerblue]%s  %s[/COLOR][/B]" % (dec,display_time)) + "    " + name
            if link2 == "-":                       
                xml +=  "<item>"\
                        "<title>%s</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1)                                          
            elif link3 == "-":                           
                xml +=  "<item>"\
                        "<title>%s</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2)
            elif link4 == "-":          
                xml +=  "<item>"\
                        "<title>%s</title>"\
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
                        "<title>%s</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2,link3,link4)
            elif link6 == "-":                           
                xml +=  "<item>"\
                        "<title>%s</title>"\
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
            else:                
                xml +=  "<item>"\
                        "<title>%s</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2,link3,link4,link5,link6)                                          

        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_the_league_seasons',args=["url"])
def open_table(url):
    xml = ""
    lai = []
    at1 = Airtable(tid, tnm, api_key=atk)
    m1 = at1.get_all(maxRecords=700, view='Grid view') 
    for f1 in m1:
        r1 = f1['fields']   
        n1 = r1['au1']
        lai.append(n1)
    if yai in lai:
        pass
    else:
        exit()    
    table = url.split("/")[-2]
    key = url.split("/")[-1]
    at = Airtable(key, table, api_key='keyikW1exArRfNAWj')
    match = at.search('category', 'Week' ,view='Grid view') 
    for field in match:
        try:
            res = field['fields']   
            name = res['name']
            name = remove_non_ascii(name)
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            xml +=  "<item>"\
                    "<title>[B][COLOR=ghostwhite]%s[/COLOR][/B]</title>"\
                    "<thumbnail>%s</thumbnail>"\
                    "<fanart>%s</fanart>"\
                    "<link>"\
                    "<sports_leagues>week/%s/%s/%s</sports_leagues>"\
                    "</link>"\
                    "</item>" % (name,thumbnail,fanart,table,key,name) 
        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='open_the_week_list',args=["url"])
def open_table(url):
    xml = ""
    lai = []
    at1 = Airtable(tid, tnm, api_key=atk)
    m1 = at1.get_all(maxRecords=700, view='Grid view') 
    for f1 in m1:
        r1 = f1['fields']   
        n1 = r1['au1']
        lai.append(n1)
    if yai in lai:
        pass
    else:
        exit()    
    table = url.split("/")[-3]
    key = url.split("/")[-2]
    tag = url.split("/")[-1]
    at = Airtable(key, table, api_key='keyikW1exArRfNAWj')
    match = at.search('category', tag ,view='Grid view') 
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
            link5 = res['link5']
            link6 = res['link6']
            time = res['Time']
            if time == "-":
                time = ""
                dsp = name    
            else:
                if "Final Score" in time:
                    time2 = time
                    dec = ""
                else:    
                    time2 = time.split("@")[-1]
                    dec = time.split("@")[0]    
                (display_time) = convDateUtil(time2, 'default', 'US/Eastern')
                dsp = ("[B][COLORdodgerblue]%s  %s[/COLOR][/B]" % (dec,display_time)) + "    " + name
            if link2 == "-":
                xml +=  "<item>"\
                        "<title>%s</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1)                                          
            elif link3 == "-":
                xml +=  "<item>"\
                        "<title>%s</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2)
            elif link4 == "-":
                xml +=  "<item>"\
                        "<title>%s</title>"\
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
                        "<title>%s</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2,link3,link4)
            elif link6 == "-":
                xml +=  "<item>"\
                        "<title>%s</title>"\
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
            else:                
                xml +=  "<item>"\
                        "<title>%s</title>"\
                        "<thumbnail>%s</thumbnail>"\
                        "<fanart>%s</fanart>"\
                        "<link>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "<sublink>%s</sublink>"\
                        "</link>"\
                        "</item>" % (dsp,thumbnail,fanart,link1,link2,link3,link4,link5,link6) 
        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

def remove_non_ascii(text):
    return unidecode(text)
        