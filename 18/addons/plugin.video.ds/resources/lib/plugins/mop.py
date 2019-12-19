"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you can do 
    whatever you want with this stuff. Just Ask first when not released through
    the tools and parser GIT. If we meet some day, and you think this stuff is
    worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------


    Overview:

        Drop this PY in the plugins folder. See examples below on use.
        This is a scraper plugin for the Massively Overpowered Podcast show

    Version:
        2018.8.2:
            - Initial Release

    XML Explanations:
        Tags: 
            <mop></mop> - Displays the full archive list


    Usage Examples:

        <dir>
            <title>Massively OP Podcast</title>
            <mop>list/1</mop>
        </dir>

        <item>
            <title>EPISODE 180: SUPERSTOKED FOR HEROIC MMOS</title>
            <mop>https://massivelyop.com/2018/07/31/massively-op-podcast-episode-180-superstoked-for-heroic-mmos/</mop>
        </item>


"""


import base64,json,re,requests,os,time,traceback,urlparse
import koding
import __builtin__
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 10800  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
headers = {'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'} 

base_main_link = 'https://massivelyop.com/%s'
json_cat_url   = 'wp-json/wp/v2/posts/?per_page=%s&categories=%s&page=%s'

class MassivelyOP(Plugin):
    name = "massivelyop"

    def process_item(self, item_xml):
        if "<mop>" in item_xml:
            item = JenItem(item_xml)
            if "list/" in item.get("mop", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "MassivelyOP",
                    'url': item.get("mop", ""),
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
            elif "http" in item.get("mop", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PlayMOP",
                    'url': item.get("mop", ""),
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

    def clear_cache(self):
        skip_prompt = xbmcaddon.Addon().getSetting("quiet_cache")
        dialog = xbmcgui.Dialog()
        if skip_prompt == 'false':
            if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear MOP Plugin Cache?"):
                koding.Remove_Table("mop_plugin")
        else:
            koding.Remove_Table("mop_plugin")

@route(mode='MassivelyOP', args=["url"])
def get_MassivelyOP(url):
    url = url.replace('list/', '')
    page_id = url
    url = base_main_link % ((json_cat_url % ('50', '16', page_id))) 

    count = 0

    xml = fetch_from_db(url)
    if not xml:
        try:
            xml = ""
            response = requests.get(url,headers).json()
            try:
                if 'invalid' in response['code']:
                    return
            except:
                pass
            count = len(response)
            for post in response:
                title   = remove_non_ascii(replaceHTMLCodes(post['title']['rendered'])).replace('Massively OP Podcast','')
                description = remove_non_ascii(replaceHTMLCodes(post['excerpt']['rendered']))
                description = re.sub('<[^<]+?>', '', description)
                icon = addon_icon

                page_link = post['link'].replace('\/','/')
                if len(page_link) > 0:
                    xml += "<item>"\
                           "    <title>%s</title>"\
                           "    <meta>"\
                           "        <summary>%s</summary>"\
                           "    </meta>"\
                           "    <mop>%s</mop>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "</item>" % (title,description,page_link,icon)

            try:
                if count == 50:
                    xml += "<dir>"\
                           "    <title>Next Page >></title>"\
                           "    <meta>"\
                           "        <summary>Click here for the next page</summary>"\
                           "    </meta>"\
                           "    <mop>list/%s</mop>"\
                           "</dir>" % (str(int(page_id)+1))
            except:
                pass

            save_to_db(xml, url)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='PlayMOP', args=["url"])
def play_MOPEpisode(url):
    try:
        html = requests.get(url,headers).content
        link = re.compile('a href="(.+?).mp3"').findall(html)[0] + '.mp3'
        title = re.compile('property="og:title" content="(.+?)"').findall(html)[0]

        item = xbmcgui.ListItem(label=title, path=link, iconImage=addon_icon, thumbnailImage=addon_icon)
        item.setInfo( type="Audio", infoLabels={ "Title": title } )
        import resolveurl
        koding.Play_Video(link,showbusy=False,ignore_dp=True,item=item,resolver=resolveurl)
    except:
        failure = traceback.format_exc()
        xbmcgui.Dialog().textviewer('Item Exception',str(failure))
        xbmcgui.Dialog().ok('Stream', 'Unable to play stream')


def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "mop_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("mop_plugin",
                            {
                                "url": url,
                                "item": base64.b64encode(item),
                                "created": time.time()
                            })
    except:
        return False


def fetch_from_db(url):
    koding.reset_db()
    mop_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("mop_plugin", mop_plugin_spec)
    match = koding.Get_From_Table(
        "mop_plugin", {"url": url})
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
            return None
    else:
        return None


def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    try:
        import html.parser as html_parser
    except:
        import HTMLParser as html_parser
    txt = html_parser.HTMLParser().unescape(txt)
    txt = html_parser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.strip()
    return txt

def replaceEscapeCodes(txt):
    try:
        import html.parser as html_parser
    except:
        import HTMLParser as html_parser
    txt = html_parser.HTMLParser().unescape(txt)
    return txt

def remove_non_ascii(text):
    try:
        text = text.decode('utf-8').replace(u'\xc2', u'A').replace(u'\xc3', u'A').replace(u'\xc4', u'A')
    except:
        pass
    return unidecode(text)

