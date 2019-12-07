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
<title>Arconaitv 24-7</title>
<arconaitv>shows</arconaitv>
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

class ARCONAITV(Plugin):
    name = "arconaitv"

    def process_item(self, item_xml):
        if "<arconaitv>" in item_xml:
            item = JenItem(item_xml)
            if "shows" in item.get("arconaitv", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_shows",
                    'url': item.get("arconaitv", ""),
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


@route(mode='get_shows', args=["url"])
def get_shows(url):
    xml = ""
    try:    
        url = "https://www.arconaitv.us/"
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        block2 = re.compile('<div class="content">(.+?)<div class="stream-nav shows" id="shows">',re.DOTALL).findall(html)
        match2 = re.compile('href=(.+?) title=(.+?)<img src=(.+?) alt=(.+?) />',re.DOTALL).findall(str(block2))
        for link2,title2,image2,name2 in match2:
            name2 = name2.replace("\\'", "")
            link2 = link2.replace("\\'", "")
            image2 = image2.replace("\\'", "")
            title2 = title2.replace("\\'", "")
            title2 = title2.replace(" class=poster-link>","")
            image2 = "https://www.arconaitv.us"+image2
            link2 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/"+link2                
            if not name2:            
                xml += "<plugin>"\
                       "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "<thumbnail>%s</thumbnail>"\
                       "</plugin>" % (title2,link2,image2)
            else:
                xml += "<plugin>"\
                       "<title>[COLORwhite][B]%s[/COLOR][/B]</title>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "<thumbnail>%s</thumbnail>"\
                       "</plugin>" % (name2,link2,image2)                       
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type()) 
              

def remove_non_ascii(text):
    return unidecode(text)
           
            