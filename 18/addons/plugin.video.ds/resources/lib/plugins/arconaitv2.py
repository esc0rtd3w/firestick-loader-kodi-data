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

    Version:
        Sep 24th, 2018
            - Updated so that thumbnails are displayed for all items in each category (Movies, Shows, Cable Channels).
        May 9th, 2018
            - Updated so that Movies, TV Shows & Cable Channels are displayed in separate categories with the contents listed in alphabetical order.
            - Updated get_shows mode so that this plugin can co-exit with the arconaitv.py plugin.

    -------------------------------------------------------------            

    *** COLORS ***
        Set your desired color for MYCOLOR within '' on line 73 and all items will be displayed in that color.
        The color value can be alphanumeric (example: red, limegreen) or Hex (example: ffff0000, FF00FF00).
        If MYCOLOR is left blank, it will display as the default color set within the skin you're using.

    -------------------------------------------------------------

    Usage Examples:
    
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
    pins = ""
    xml = ""
    try:
        url = "https://www.arconaitv.us/"
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        block1 = re.compile('<div class="stream-nav shows" id="shows">(.+?)<div class="acontainer">',re.DOTALL).findall(html)
        match1 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block1))
        for link1,title1 in match1:
            title1 = title1.replace("\\'", "")
            title1 = remove_non_ascii(title1)
            link1 = link1.replace("\\'", "")
            link1 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/"+link1
            image1 = get_thumb(title1,html)
            if image1:
                xml += "<plugin>"\
                       "<title>%s</title>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>https://lerablog.org/wp-content/uploads/2014/05/tv-series.jpg</fanart>"\
                       "<summary>Random Episodes</summary>"\
                       "</plugin>" % (title1,link1,image1)                       
            elif not image1:
                image2 = get_other(title1,html)
                xml += "<plugin>"\
                       "<title>%s</title>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>https://lerablog.org/wp-content/uploads/2014/05/tv-series.jpg</fanart>"\
                       "<summary>Random Episodes</summary>"\
                       "</plugin>" % (title1,link1,image2)
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)
	
	
@route(mode='get_cable2', args=["url"])
def get_cable2(url):
    pins = ""
    xml = ""
    try:    
        url = "https://www.arconaitv.us/"
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        block4 = re.compile('<div class="stream-nav cable" id="cable">(.+?)<div class="acontainer">',re.DOTALL).findall(html)
        match4 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block4))
        for link4,title4 in match4:
            title4 = title4.replace("\\'", "")
            title4 = remove_non_ascii(title4)
            link4 = link4.replace("\\'", "")
            link4 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/"+link4
            image4 = get_thumb(title4,html)
            if image4:
                xml += "<plugin>"\
                       "<title>%s</title>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>http://static.wixstatic.com/media/7217cd_6b6840f1821147ffa0380918a2110cdd.jpg</fanart>"\
                       "<summary>Random TV Shows</summary>"\
                       "</plugin>" % (title4,link4,image4)                       
            elif not image4:
                image5 = get_other(title4,html)
                if title4 == "ABC":
                    image5 = "https://vignette.wikia.nocookie.net/superfriends/images/f/f2/Abc-logo.jpg/revision/latest?cb=20090329152831"
                elif title4 == "Animal Planet":
                    image5 = "https://seeklogo.com/images/D/discovery-animal-planet-logo-036312EA16-seeklogo.com.png"
                elif title4 == "Bravo Tv":
                    image5 = "https://kodi.tv/sites/default/files/styles/medium_crop/public/addon_assets/plugin.video.bravo/icon/icon.png?itok=VXH52Iyf"
                elif title4 == "CNBC":
                    image5 = "https://i2.wp.com/republicreport.wpengine.com/wp-content/uploads/2014/06/cnbc1.png?resize=256%2C256"
                elif title4 == "NBC":
                    image5 = "https://designobserver.com/media/images/mondrian/39684-NBC_logo_m.jpg"
                elif title4 == "SYFY":
                    image5 = "https://kodi.tv/sites/default/files/styles/medium_crop/public/addon_assets/plugin.video.syfy/icon/icon.png?itok=ZLTAqywa"
                elif title4 == "USA Network ":
                    image5 = "https://crunchbase-production-res.cloudinary.com/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/v1442500192/vzcordlt6w0xsnhcsloa.png"
                elif title4 == "WWOR-TV":
                    image5 = "https://i.ytimg.com/vi/TlhcM0jciZo/hqdefault.jpg"
                                                                                                                                                                
                xml += "<plugin>"\
                       "<title>%s</title>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>http://static.wixstatic.com/media/7217cd_6b6840f1821147ffa0380918a2110cdd.jpg</fanart>"\
                       "<summary>Random TV Shows</summary>"\
                       "</plugin>" % (title4,link4,image5)
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)
              

def remove_non_ascii(text):
    return unidecode(text)


@route(mode='get_movies2', args=["url"])
def get_movies2(url):
    pins = ""
    xml = ""
    try:    
        url = "https://www.arconaitv.us/"
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        block5 = re.compile('<div class="stream-nav movies" id="movies">(.+?)<div class="acontainer">',re.DOTALL).findall(html)
        match5 = re.compile('href=(.+?) title=(.+?)>',re.DOTALL).findall(str(block5))
        for link5,title5 in match5:
            title5 = title5.replace("\\'", "")
            title5 = remove_non_ascii(title5)
            link5 = link5.replace("\\'", "")
            link5 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=https://www.arconaitv.us/"+link5
            image5 = get_other(title5,html)
            if image5:
                xml += "<plugin>"\
                       "<title>%s</title>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>http://listtoday.org/wallpaper/2015/12/movies-in-theaters-1-desktop-background.jpg</fanart>"\
                       "<summary>Random Movies</summary>"\
                       "</plugin>" % (title5,link5,image5)
            elif not image5:
                image6 = "http://www.userlogos.org/files/logos/nickbyalongshot/film.png"
                if title5 == "Action":
                    image6 = "http://icons.iconarchive.com/icons/sirubico/movie-genre/256/Action-3-icon.png"
                if title5 == "Animation Movies":
                    image6 = "http://www.filmsite.org/images/animated-genre.jpg"
                if title5 == "Christmas Movies":
                    image6 = "https://i2.wp.com/emailsantanow.com/wp-content/uploads/2015/11/cropped-email-santa-2015.png?fit=512%2C512&ssl=1"
                if title5 == "Comedy Movies":
                    image6 = "https://thumb9.shutterstock.com/display_pic_with_logo/882263/116548462/stock-photo-clap-film-of-cinema-comedy-genre-clapperboard-text-illustration-116548462.jpg"
                if title5 == "Documentaries ":
                    image6 = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRc8s5haFPMPgDNmfetzNm06V3BB918tV8TG5JiJe7FaEqn-Cgx"
                if title5 == "Harry Potter ":
                    image6 = "http://icons.iconarchive.com/icons/aaron-sinuhe/tv-movie-folder/256/Harry-Potter-2-icon.png"
                if title5 == "Horror Movies":
                    image6 = "http://www.filmsite.org/images/horror-genre.jpg"
                if title5 == "Mafia Movies":
                    image6 = "https://cdn.pastemagazine.com/www/blogs/lists/2012/04/05/godfather-lead.jpg"
                if title5 == "Movie Night":
                    image6 = "http://jesseturri.com/wp-content/uploads/2013/03/Movie-Night-Logo.jpg"
                if title5 == "Musical Movies":
                    image6 = "http://ww1.prweb.com/prfiles/2016/03/18/13294162/Broadway_Movie_Musical_Logo.jpg"
                if title5 == "Mystery Movies":
                    image6 = "http://icons.iconarchive.com/icons/limav/movie-genres-folder/256/Mystery-icon.png"
                if title5 == "Random Movies":
                    image6 = "https://is1-ssl.mzstatic.com/image/thumb/Purple118/v4/a2/93/b8/a293b81e-9781-5129-32e9-38fb63ff52f8/source/256x256bb.jpg"
                if title5 == "Romance Movies":
                    image6 = "http://icons.iconarchive.com/icons/limav/movie-genres-folder/256/Romance-icon.png"
                if title5 == "Star Wars ":
                    image6 = "http://icons.iconarchive.com/icons/aaron-sinuhe/tv-movie-folder/256/Star-Wars-2-icon.png"
                if title5 == "Studio Ghibli":
                    image6 = "https://orig00.deviantart.net/ec8a/f/2017/206/5/a/studio_ghibli_collection_folder_icon_by_dahlia069-dbho9mx.png"                                      
                                                                                                                                                                                                                                                                
                xml += "<plugin>"\
                       "<title>%s</title>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>http://listtoday.org/wallpaper/2015/12/movies-in-theaters-1-desktop-background.jpg</fanart>"\
                       "<summary>Random Movies</summary>"\
                       "</plugin>" % (title5,link5,image6)
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)
          
          
def get_thumb(name,html):
    block2 = re.compile('<div class="content">(.+?)<div class="stream-nav shows" id="shows">',re.DOTALL).findall(html)
    match2 = re.compile('<img src=(.+?) alt=(.+?) />',re.DOTALL).findall(str(block2))
    for image,name2 in match2:
        if name in name2:
            image = image.replace("\\'", "")
            image = "https://www.arconaitv.us"+image
            return image

            
def get_other(name,html):
    block3 = re.compile("<div class='row stream-list-featured'>(.+?)<div class='row stream-list'>",re.DOTALL).findall(html)
    match3 = re.compile('title=(.+?) class.+?<img src=(.+?) alt',re.DOTALL).findall(str(block3))
    for name3,image3 in match3:
        if name in name3:
            image3 = image3.replace("\\'", "")
            image3 = "https://www.arconaitv.us"+image3
            return image3 