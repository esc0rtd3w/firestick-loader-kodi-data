"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------

    Props:
        MetalKettle - Original Dev of the addon called ToonMania, which this plugin
            is heavily based on. The ToonMania addon was used as a base and ported 
            over to be supported as a Jen Plugin.

    Changelog:
        2018.7.11:
            - Added cache clearing
            - Indentation fix (Digital)

        2018.6.20:
            - Added caching to primary menus (Cache time is 3 hours)

        2018-06-16:
            Initial Build

    Usage Examples:

        <dir>
            <title>New Movies</title>
            <toonmania>category/GetNewMovies</toonmania>
        </dir>

        <dir>
            <title>All Movies</title>
            <toonmania>category/GetAllMovies</toonmania>
        </dir>

        <dir>
            <title>Popular Movies</title>
            <toonmania>category/GetPopularMovies</toonmania>
        </dir>

        <dir>
            <title>New Cartoons</title>
            <toonmania>category/GetNewCartoon</toonmania>
        </dir>

        <dir>
            <title>All Cartoons</title>
            <toonmania>category/GetAllCartoon</toonmania>
        </dir>

        <dir>
            <title>Popular Cartoons</title>
            <toonmania>category/GetPopularCartoon</toonmania>
        </dir>

        <dir>
            <title>New Dubbed Anime</title>
            <toonmania>category/GetNewDubbed</toonmania>
        </dir>

        <dir>
            <title>All Dubbed Anime</title>
            <toonmania>category/GetAllDubbed</toonmania>
        </dir>

        <dir>
            <title>Popular Dubbed Anime</title>
            <toonmania>category/GetPopularDubbed</toonmania>
        </dir>



"""

import __builtin__
import base64,time
import json,re,requests,os,traceback,urlparse
import koding
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
next_icon = os.path.join(xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')), 'resources', 'media', 'next.png')

header = {'User-Agent':'okhttp/2.3.0',
         'App-LandingPage':'http://www.mobi24.net/toon.html',
         'App-Name':'#Toonmania',
         'Connection':'Keep-Alive',
         'Host':'api.animetoon.tv',
         'App-Version':'7.7'}

base_main_link    = 'http://api.animetoon.tv/'
base_details_link = 'http://api.animetoon.tv/GetDetails/'
base_videos_link  = 'http://api.animetoon.tv/GetVideos/'

class ToonMania(Plugin):
    name = "ToonMania"
    priority = 200

    def process_item(self, item_xml):
        if "<toonmania>" in item_xml:
            item = JenItem(item_xml)
            if "category/" in item.get("toonmania", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "TMCategories",
                    'url': item.get("toonmania", ""),
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
            elif "subitem/" in item.get("toonmania", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "TMSubItem",
                    'url': item.get("toonmania", ""),
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
            result_item['fanart_small'] = result_item["fanart"]
            return result_item

    def clear_cache(self):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear ToonMania Plugin Cache?"):
            koding.Remove_Table("toonmania_com_plugin")


@route(mode='TMCategories', args=["url"])
def get_TMCategories(url):
    pins = ""
    url = url.replace('category/', '')
    url = urlparse.urljoin(base_main_link, url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url,headers=header).content
            js = json.loads(html)
            for item in js:
                try:
                    title = clean_hex(item['name'])
                    id = clean_hex(item['id'])
                    desc = clean_hex(item['description'])
                    thumbnail = 'http://www.animetoon.tv/images/series/big/'+item['id']+'.jpg'
                    xml += "<dir>"\
                           "    <title>%s</title>"\
                           "    <meta>"\
                           "        <summary>%s</summary>"\
                           "    </meta>"\
                           "    <toonmania>subitem/%s</toonmania>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "</dir>" % (title,desc,id,thumbnail)
                except:
                    continue
            save_to_db(xml, url)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='TMSubItem', args=["url"])
def get_TMSubItem(url):
    pins = ""
    url = url.replace('subitem/', '')
    imgid = url
    url = urlparse.urljoin(base_details_link, url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url,headers=header).content
            id2 = re.compile('"id":"(.+?)"').findall(html) # THERE IS MORE THAN 1 ID
            i=0
            for num in id2:
                try:
                    nurl   = urlparse.urljoin(base_videos_link, num)
                    page  = requests.get(nurl,headers=header).content
                    links = re.compile('"(.+?)"').findall(page.replace('\/','/'))
                    for link in links:
                        if 'videozoome' in link:
                            page = requests.get(link).content
                            try:
                                link = re.compile('file: "(.+?)"').findall(page)[-1]
                            except:
                                link = re.compile('src: "(.+?)"').findall(page)[-1]
                            i=i+1
                            title = 'Part ' + str(i)
                            xml += "<item>"\
                                   "    <title>%s</title>"\
                                   "    <meta>"\
                                   "        <summary>%s</summary>"\
                                   "    </meta>"\
                                   "    <link>%s</link>"\
                                   "    <thumbnail>%s</thumbnail>"\
                                   "</item>" % (title,title,link,addon_icon)
                except:
                    continue
            save_to_db(xml, url)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


def clean_hex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    try: return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
    except: return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))


def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "toonmania_com_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("toonmania_com_plugin",
                            {
                                "url": url,
                                "item": base64.b64encode(item),
                                "created": time.time()
                            })
    except:
        return False


def fetch_from_db(url):
    koding.reset_db()
    toonmania_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("toonmania_com_plugin", toonmania_plugin_spec)
    match = koding.Get_From_Table(
        "toonmania_com_plugin", {"url": url})
    if match:
        match = match[0]
        if not match["item"]:
            return None
        created_time = match["created"]
        if created_time and float(created_time) + CACHE_TIME >= time.time():
            match_item = match["item"]
            try:
                result = base64.b64decode(match_item)
            except:
                return None
            return result
        else:
            return
    else:
        return 


def remove_non_ascii(text):
    try:
        text = text.decode('utf-8').replace(u'\xc2', u'A').replace(u'\xc3', u'A').replace(u'\xc4', u'A').replace(u'\xe2', u'a')
    except:
        pass
    return unidecode(text)
