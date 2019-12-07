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

    <<< Usage Examples >>>
    
	** Returns a list of 24/7 Movies from the Arconaitv website
    <dir>
      <title>24/7 Movies</title>
      <arconaitv2>movies</arconaitv2>
    </dir>
    
	** Returns a list of 24/7 TV Shows from the Arconaitv website
    <dir>
      <title>24/7 TV Shows</title>
      <arconaitv2>shows</arconaitv2>
    </dir>
    
	** Returns a list of 24/7 Cable Channels from the Arconaitv website
    <dir>
      <title>24/7 Channels</title>
      <arconaitv2>cable</arconaitv2>
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
    name = "arconaitv2"

    def process_item(self, item_xml):
        if "<arconaitv2>" in item_xml:
            item = JenItem(item_xml)
            if "shows" in item.get("arconaitv2", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_shows2",
                    'url': item.get("arconaitv2", ""),
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
            elif "cable" in item.get("arconaitv2", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_cable2",
                    'url': item.get("arconaitv2", ""),
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
            elif "movies" in item.get("arconaitv2", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_movies2",
                    'url': item.get("arconaitv2", ""),
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


@route(mode='get_shows2', args=["url"])
def get_shows2(url):
    xml = ""
    try:    
        url = "https://www.arconaitv.us/"
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        block1 = re.compile('<div class="stream-nav shows" id="shows">(.+?)<div class="stream-nav cable" id="cable">',re.DOTALL).findall(html)
        match1 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block1))
        for link1,title1 in match1:
            title1 = title1.replace("\\'", "")
            link1 = link1.replace("\\'", "")
            link1 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/"+link1
            image1 = "http://www.userlogos.org/files/logos/nickbyalongshot/film.png"                
            xml += "<plugin>"\
                   "<title>%s</title>"\
                   "<link>"\
                   "<sublink>%s</sublink>"\
                   "</link>"\
                   "<thumbnail>%s</thumbnail>"\
                   "</plugin>" % (title1,link1,image1)                                                  
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
	
	
@route(mode='get_cable2', args=["url"])
def get_cable2(url):
    xml = ""
    try:    
        url = "https://www.arconaitv.us/"
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        block2 = re.compile('<div class="stream-nav cable" id="cable">(.+?)<div class="stream-nav movies" id="movies">',re.DOTALL).findall(html)
        match2 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block2))
        for link2,title2 in match2:
            title2 = title2.replace("\\'", "")
            link2 = link2.replace("\\'", "")
            link2 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/"+link2
            image2 = "http://www.userlogos.org/files/logos/nickbyalongshot/film.png"                
            xml += "<plugin>"\
                   "<title>%s</title>"\
                   "<link>"\
                   "<sublink>%s</sublink>"\
                   "</link>"\
                   "<thumbnail>%s</thumbnail>"\
                   "</plugin>" % (title2,link2,image2)                                                    
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())
              

def remove_non_ascii(text):
    return unidecode(text)


@route(mode='get_movies2', args=["url"])
def get_movies2(url):
    xml = ""
    try:    
        url = "https://www.arconaitv.us/"
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        block3 = re.compile('<div class="stream-nav movies" id="movies">(.+?)<div class="donation-form" id="donate">',re.DOTALL).findall(html)
        match3 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block3))
        for link3,title3 in match3:
            title3 = title3.replace("\\'", "")
            link3 = link3.replace("\\'", "")
            link3 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/"+link3
            image3 = "http://www.userlogos.org/files/logos/nickbyalongshot/film.png"                
            xml += "<plugin>"\
                   "<title>%s</title>"\
                   "<link>"\
                   "<sublink>%s</sublink>"\
                   "</link>"\
                   "<thumbnail>%s</thumbnail>"\
                   "</plugin>" % (title3,link3,image3)                     
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())