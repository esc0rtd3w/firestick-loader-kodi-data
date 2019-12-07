"""

    Copyright (C) 2018

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

import requests,re,json,os
import koding
import __builtin__
import xbmc,xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

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
                    'icon': "http://www.kodi-911.com/.artwork/Mainart/sportsstreams.png",
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
    xml = ""
    try:    
        url = "http://www.sports-stream.net/schedule.html"       
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        block1 = re.compile('<br><font color="red">(.+?)',re.DOTALL).findall(html)
        try:
            match = re.compile('<h3>(.+?)<input onclick=',re.DOTALL).findall(html)
            for head1 in match:
                head1 = head1.replace("&nbsp;", "")
                xml += "<item>"\
                       "<title>[COLOR blue]%s[/COLOR]</title>"\
                       "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
                       "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                       "<link></link>"\
                       "</item>" % (head1)
        except:
            pass
        try:               
            match1 = re.compile('<span style="color:#FF0000;">(.+?)</span> (.+?)<a.+?href="(.+?)"',re.DOTALL).findall(html)
            for time,name,link in match1:
                link = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url="+link
                xml += "<plugin>"\
                       "<title>[COLORwhite][B]%s - %s[/COLOR][/B]</title>"\
                       "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
                       "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                       "<link>%s</link>"\
                       "</plugin>" % (time,name,link)
        except:
            pass
        try:               
            match3 = re.compile('<br><font color="red"><h3>.+?<br><font color="red"><h3>(.+?)<input onclick=',re.DOTALL).findall(html)
            for head2 in match3:
                head2 = head2.replace("&nbsp;", "")
                xml += "<item>"\
                       "<title>[COLOR blue]%s[/COLOR]</title>"\
                       "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
                       "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                       "<link></link>"\
                       "</item>" % (head2)
        except:
            pass
        try:               
            block2 = re.compile('<br><font color="red"><h3>.+?<br><font color="red"><h3>(.+?)<script data-cfasync',re.DOTALL).findall(html)
            match4 = re.compile('<span style="color:#FF0000;">(.+?)</span> (.+?)<a.+?href="(.+?)"',re.DOTALL).findall(str(block2))
            for time,name,link in match4:
                link = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url="+link 
                xml += "<plugin>"\
                       "<title>[COLORwhite][B]%s - %s[/COLOR][/B]</title>"\
                       "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
                       "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                       "<link>%s</link>"\
                       "</plugin>" % (time,name,link)
        except:
            pass                                                                               
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type()) 
              

def remove_non_ascii(text):
    return unidecode(text)
           
            