"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------


    Overview:
        Drop this PY in the plugins folder, and use whatever tools below you want.

    Version:
        2018.5.25
            - Added <pairwith> tags
                - Can use pairlist to show all sites, or specific entry from PAIR_LIST to load that site from menu
            - Added <trailer> tag support to load your custom YT trailer (via plugin url) for non-imdb items

        2018.5.1a
            - Added <mode> and <modeurl> tags (used together in same item)

        2018.5.1
            - Initial Release

    XML Explanations:
        Tags: 
            <heading></heading> - Displays the entry as normal, but performs no action (not a directory or "item")
            <mysettings>0/0</mysettings> - Opens settings dialog to the specified Tab and section (0 indexed)
            <pairwith></pairwith> - Used for pairing with sites. See list below of supported sites with this plugin
            <trailer>plugin://plugin.video.youtube/play/?video_id=ChA0qNHV1D4</trailer>

    Usage Examples:

        <item>
            <title>[COLOR limegreen]Don't forget to folow me on twitter @tantrumdev ![/COLOR]</title>
            <heading></heading>
        </item>

        <item>
            <title>JEN: Customization</title>
            <mysettings>0/0</mysettings>
            <info>Open the Settings for the addon on the Customization tab</info>
        </item>

        <item>
            <title>Pair With Sites</title>
            <pairwith>pairlist</pairwith>
        </item>

        <item>
            <title>Pair Openload</title>
            <pairwith>openload</pairwith>
        </item>

        <item>
            <title>Dune (1984)</title>
            <trailer>plugin://plugin.video.youtube/play/?video_id=ChA0qNHV1D4</trailer>
            <info>Provides the Trailer context link for this movie when Metadata is DISABLED in your addon.</info>
        </item>

        <item>
            <title>JEN: General</title>
            <mysettings>1/0</mysettings>
            <info>Open the Settings for the addon on the General tab</info>
        </item>

        <item>
            <title>Custom Mode</title>
            <mode>Whatever</mode>
            <modeurl>query=Iwant</modeurl>
            <info>Sets a specific Mode for the menu item, to utilize Jen modes not normally accessible. Setting modeurl passes a custom built url= variable to go with it</info>
        </item>


"""

import collections,requests,re,os,traceback,webbrowser
import koding
import __builtin__
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')

PAIR_LIST = [ ("openload", "https://olpair.com/pair"),
        ("the_video_me", "https://thevideo.us/pair"),
        ("vid_up_me", "https://vidup.me/pair"),
        ("vshare", "http://vshare.eu/pair"),
        ("flashx", "https://www.flashx.tv/?op=login&redirect=https://www.flashx.tv/pairing.php") ]

class JenTools(Plugin):
    name = "jentools"
    priority = 200

    def process_item(self, item_xml):
        result_item = None
        if "<heading>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "HEADING",
                'url': item.get("heading", ""),
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
            return result_item
        elif "<mysettings>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "MYSETTINGS",
                'url': item.get("mysettings", ""),
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
            return result_item
        elif "<mode>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': item.get("mode", ""),
                'url': item.get("modeurl", ""),
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
        elif "<pairwith>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "PAIRWITH",
                'url': item.get("pairwith", ""),
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
            return result_item
        elif "<trailer>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "PAIRWITH",
                'url': item.get("pairwith", ""),
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
            result_item["info"]["trailer"] = item.get("trailer", None)
            return result_item


@route(mode='HEADING')
def heading_handler():
    try:
        quit()
    except:
        pass


@route(mode="MYSETTINGS", args=["url"])
def mysettings_handler(query):
    try:
        xbmc.executebuiltin('Dialog.Close(busydialog)')
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % addon_id)
        c, f = query.split('/')
        xbmc.executebuiltin('SetFocus(%i)' % (int(c) + 100))
        xbmc.executebuiltin('SetFocus(%i)' % (int(f) + 200))
    except:
        return

@route(mode="PAIRWITH", args=["url"])
def pairing_handler(url):
    try:
        site = ''
        if 'pairlist' in url:
            names = []
            for item in PAIR_LIST:
                the_title = 'Pair for %s' % (item[0].replace('_', ' ').capitalize())
                names.append(the_title)
            selected = xbmcgui.Dialog().select('Select Site',names)

            if selected ==  -1:
                return

            # If you add [COLOR] etc to the title stuff in names loop above, this will strip all of that out and make it usable here
            pair_item = re.sub('\[.*?]','',names[selected]).replace('Pair for ', '').replace(' ', '_').lower()
            for item in PAIR_LIST:
                if str(item[0]) == pair_item:
                    site = item[1]
                    break
        else:
            for item in PAIR_LIST:
                if str(item[0]) == url:
                    site = item[1]
                    break

        check_os = platform()
        if check_os == 'android': 
            spam_time = xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' % (site))
        elif check_os == 'osx':
           os.system("open -a /Applications/Safari.app %s") % (site)
        else:
            spam_time = webbrowser.open(site)
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('Exception',str(failure))
        pass


def platform():
    if xbmc.getCondVisibility('system.platform.android'):   return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):   return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'): return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):     return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):    return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):     return 'ios'