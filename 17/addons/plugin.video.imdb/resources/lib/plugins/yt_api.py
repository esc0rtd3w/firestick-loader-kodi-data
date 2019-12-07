"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------


    Usage Examples:

<item>
    <title>Apply the Addon's Youtube API Keys to Kodi</title>
    <ytapi>titleforyouapigoeshere/apikeygoeshere/clientgoeshere/secretgoeshere</ytapi>
</item>




"""

import requests,re,json,os,urlparse
import koding
import __builtin__
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class YTAPI(Plugin):
    name = "ytapi"

    def process_item(self, item_xml):
        if "<ytapi>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "YTAPI",
                'url': item.get("ytapi", ""),
                'folder': False,
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


@route(mode='YTAPI', args=["url"])
def apply_ytapi(url):
    xml = ""
    try:
        yt_path = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.youtube'))
        if not os.path.exists(yt_path):
            dialog = xbmcgui.Dialog()
            dialog.ok('Youtube',"[COLOR red]The Youtube Addon is not installed. Canceling API update....[/COLOR]")
            quit()
        try:
            ytapi_set = url.split('/')
            dialog = xbmcgui.Dialog()
            if dialog.yesno(ytapi_set[0], "Do you want to apply this Youtube API Key to Kodi?"):
                yt_settings = xbmcaddon.Addon(id='plugin.video.youtube')
                yt_settings.setSetting("youtube.api.enable", 'true')
                yt_settings.setSetting("youtube.api.last.switch", 'own')
                yt_settings.setSetting("youtube.api.key", ytapi_set[1])
                yt_settings.setSetting("youtube.api.id", ytapi_set[2])
                yt_settings.setSetting("youtube.api.secret", ytapi_set[3])
                dialog.ok(ytapi_set[0],"[COLOR snow]The Youtube addon has been updated.[/COLOR]")
        except:
            pass
    except:
        pass


def remove_non_ascii(text):
    return unidecode(text)

