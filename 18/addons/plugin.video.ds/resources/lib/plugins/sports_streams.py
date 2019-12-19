# -*- coding: utf-8 -*-
"""

    Copyright (C) 2018 TonyH
    Version 3.0.0

    --July 8 2018, Added Local time and changed game times to be local--
    Thanks to Bugatsinho for the Time function--

    --June 16 2018, Added GMT+3 time to the top of the page to make
    it easier to figure out when the games start--

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
<title>Sports Streams</title>
<sport_stream>games</sport_stream>
</dir>

"""

import requests, re, json, os
import koding
import __builtin__
import xbmc, xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode
import datetime, time

try: import json
except ImportError: import simplejson as json
from dateutil.parser import parse
from dateutil.tz import gettz
from dateutil.tz import tzlocal

#######################################
# Time and Date Helpers
#######################################
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


CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'


class Sports_streams(Plugin):
    name = "sports_streams"

    def process_item(self, item_xml):
        if "<sport_stream>" in item_xml:
            item = JenItem(item_xml)
            if "games" in item.get("sport_stream", ""):
                result_item = {
                    'label': item["title"],
                    'icon': "https://i.pinimg.com/736x/a2/b9/7c/a2b97c577ff82928cc53591c33ba8f75--stream-online-daytona--live.jpg",
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "Sport_Stream",
                    'url': item.get("sport_stream", ""),
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


@route(mode='Sport_Stream', args=["url"])
def get_stream(url):
    pins = ""
    xml = ""
    try:
        url = "http://www.sports-stream.net/schedule.html"
        headers = {'User_Agent': User_Agent}
        html = requests.get(url, headers=headers).content
        local_time = datetime.datetime.now().strftime('%H:%M')

        xml += "<item>"\
               "<title>[COLOR blue]Local Time  %s[/COLOR]</title>"\
               "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
               "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
               "<link></link>"\
               "</item>" % local_time
        try:
            match = re.compile('<h3>(.+?)<input onclick=', re.DOTALL).findall(html)[0]
            head1 = match.split("GMT")[0]
            xml += "<item>"\
                   "<title>[COLOR blue]%s[/COLOR]</title>"\
                   "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
                   "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                   "<link></link>"\
                   "</item>" % head1
            jenlist = JenList(xml)
            display_list(jenlist.get_list(), jenlist.get_content_type(), pins)
        except:
            pass
        try:
            xml = ""
            block3 = re.compile('<br><font color="red"><h3>(.+?)<br><font color="red"><h3>',re.DOTALL).findall(html)
            match5 = re.compile('<span style="color:#FF0000;">(.+?)</span>\s*(.+?)\s*\-\s*<a.+?href="(.+?)"',re.DOTALL).findall(str(block3))
            for time, name, link in match5:
                (display_time) = convDateUtil(time, 'default', 'Europe/Athens')
                link = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=" + link
                xml += "<plugin>"\
                       "<title>%s - %s</title>"\
                       "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
                       "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                       "<link>%s</link>"\
                       "</plugin>" % (display_time, name, link)
            if xml == "":
                block3 = re.compile('<br><font color="red"><h3>(.+?)</html>',re.DOTALL).findall(html)
                match5 = re.compile('<span style="color:#FF0000;">(.+?)</span>\s*(.+?)\s*\-\s*<a.+?href="(.+?)"',re.DOTALL).findall(str(block3))
                for time, name, link in match5:
                    (display_time) = convDateUtil(time, 'default', 'Europe/Athens')
                    link = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=" + link
                    xml += "<plugin>"\
                           "<title>%s - %s</title>"\
                           "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
                           "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                           "<link>%s</link>"\
                           "</plugin>" % (display_time, name, link)                      
        except:
            pass

        try:
            match3 = re.compile('<br><font color="red"><h3>.+?<br><font color="red"><h3>(.+?)<input onclick=', re.DOTALL).findall(html)[0]
            head2 = match3.split("GMT")[0]
            xml += "<item>"\
                   "<title>[COLOR blue]%s[/COLOR]</title>"\
                   "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
                   "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                   "<link></link>"\
                   "</item>" % head2
        except:
            pass
        try:
            block2 = re.compile('<br><font color="red"><h3>.+?<br><font color="red"><h3>(.+?)<script data-cfasync',re.DOTALL).findall(html)
            match4 = re.compile('<span style="color:#FF0000;">(.+?)</span>\s*(.+?)\s*\-\s*<a.+?href="(.+?)"', re.DOTALL).findall(str(block2))
            for time, name, link in match4:
                (display_time) = convDateUtil(time, 'default', 'Europe/Athens')
                link = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url="+link
                xml += "<plugin>"\
                       "<title>%s - %s</title>"\
                       "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
                       "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                       "<link>%s</link>"\
                       "</plugin>" % (display_time, name, link)
        except:
            pass
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


def remove_non_ascii(text):
    return unidecode(text)

