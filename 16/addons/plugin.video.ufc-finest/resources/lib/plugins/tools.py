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
        2018.7.14
            - Updated password code to cache a session for X amt of time
            - Adjust the timer via the SESSION_HOURS in settings.xml (or in code)

        2018.6.23
            - Updated link for pairing The Video Me

        2018.6.14
            - Fix for pairing on Mac OSX

        2018.6.8
            - Added Streamango and Streamcherry pairing sites
            - Added <passreq> tag to password protect submenus

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
            <passreq></passreq> - Used to password protect submenus. Format is base64 encoded string formatted like this:
                Password|link_to_xml
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
            <title>Password Protected Local File</title>
            <passreq>VGhpc0lzVGhlUGFzc3dvcmR8ZmlsZTovL3N1Ym1lbnUueG1s</passreq>
        </item>

        <item>
            <title>Password Protected Remote File</title>
            <passreq>VGhpc0lzVGhlUGFzc3dvcmR8aHR0cDovL3d3dy5leGFtcGxlLmNvbS9zdWJtZW51LnhtbA==</passreq>
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

import collections,requests,re,os,time,traceback,webbrowser
import koding
import __builtin__
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

addon_id = xbmcaddon.Addon().getAddonInfo('id')
this_addon   = xbmcaddon.Addon(id=addon_id)
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
addon_path   = xbmcaddon.Addon().getAddonInfo('path')

PAIR_LIST = [ ("flashx", "https://www.flashx.tv/?op=login&redirect=https://www.flashx.tv/pairing.php"),
        ("openload", "https://olpair.com/pair"),
        ("streamango", "https://streamango.com/pair"),
        ("streamcherry", "https://streamcherry.com/pair"),
        ("the_video_me", "https://vev.io/pair"),
        ("vid_up_me", "https://vidup.me/pair"),
        ("vshare", "http://vshare.eu/pair") ]


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
        elif "<passreq>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "PASSREQ",
                'url': item.get("passreq", ""),
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
            return result_item
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


@route(mode="PASSREQ", args=["url"])
def password_handler(url):
    prot_xml = ''
    sep_list = url.decode('base64').split('|')
    dec_pass = sep_list[0]
    xml_loc = sep_list[1]
    
    SESSION_HOURS = this_addon.getSetting('SESSION_HOURS')
    if SESSION_HOURS == '':
        SESSION_HOURS = '1'
    expires_at = this_addon.getSetting('PASS_EXIRES_AT')
    if time.time() > expires_at or expires_at == '':
        input = ''
        keyboard = xbmc.Keyboard(input, '[COLOR red]Are you worthy?[/COLOR]')
        keyboard.doModal()
        if keyboard.isConfirmed():
            input = keyboard.getText()
        if input == dec_pass:
            expires_at = time.time() + 60 * 60 * int(SESSION_HOURS)
            this_addon.setSetting("PASS_EXIRES_AT", str(expires_at))
            if 'http' in xml_loc:
                prot_xml = requests.get(xml_loc).content
            else:
                import xbmcvfs
                xml_loc = xml_loc.replace('file://', '')
                xml_file = xbmcvfs.File(os.path.join(addon_path, "xml", xml_loc))
                prot_xml = xml_file.read()
                xml_file.close()
        else:
            prot_xml += "<dir>"\
                    "    <title>[COLOR yellow]Wrong Answer! You are not worthy[/COLOR]</title>"\
                    "    <thumbnail>https://nsx.np.dl.playstation.net/nsx/material/c/ce432e00ce97a461b9a8c01ce78538f4fa6610fe-1107562.png</thumbnail>"\
                    "</dir>"
    else:
        if 'http' in xml_loc:
            prot_xml = requests.get(xml_loc).content
        else:
            import xbmcvfs
            xml_loc = xml_loc.replace('file://', '')
            xml_file = xbmcvfs.File(os.path.join(addon_path, "xml", xml_loc))
            prot_xml = xml_file.read()
            xml_file.close()

    jenlist = JenList(prot_xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


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
           os.system("open " + site)
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