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
        This is a scraper plugin for a specific specialty site

    Version:
        2018.8.7:
            - Initial Release

    XML Explanations:
        Tags: 
            <mtorture></mtorture> - Displays the full archive list


    Usage Examples:

         <dir>
            <title>Movies</title>
            <mtorture>category/movies/1</mtorture>
        </dir>

        <dir>
            <title>Documentaries</title>
            <mtorture>category/docus/1</mtorture>
        </dir>

        <dir>
            <title>1950s</title>
            <mtorture>tag/36/1</mtorture>
        </dir>

        <dir>
            <title>1960s</title>
            <mtorture>tag/33/1</mtorture>
        </dir>

        <dir>
            <title>1970s</title>
            <mtorture>tag/17/1</mtorture>
        </dir>

        <dir>
            <title>1980s</title>
            <mtorture>tag/18/1</mtorture>
        </dir>

        <dir>
            <title>1990s</title>
            <mtorture>tag/22/1</mtorture>
        </dir>

        <dir>
            <title>2000s</title>
            <mtorture>tag/26/1</mtorture>
        </dir>

        <dir>
            <title>2010s</title>
            <mtorture>tag/23/1</mtorture>
        </dir>

        <dir>
            <title>Action</title>
            <mtorture>tag/19/1</mtorture>
        </dir>

        <dir>
            <title>Adventure</title>
            <mtorture>tag/15/1</mtorture>
        </dir>

        <dir>
            <title>B-Movie Queen</title>
            <mtorture>tag/29/1</mtorture>
        </dir>

        <dir>
            <title>Best of the Worst</title>
            <mtorture>tag/28/1</mtorture>
        </dir>

        <dir>
            <title>Comedy</title>
            <mtorture>tag/13/1</mtorture>
        </dir>

        <dir>
            <title>Comics</title>
            <mtorture>tag/32/1</mtorture>
        </dir>

        <dir>
            <title>Crime</title>
            <mtorture>tag/40/1</mtorture>
        </dir>

        <dir>
            <title>Drama</title>
            <mtorture>tag/37/1</mtorture>
        </dir>

        <dir>
            <title>Exploitation</title>
            <mtorture>tag/25/1</mtorture>
        </dir>

        <dir>
            <title>Fantasy</title>
            <mtorture>tag/16/1</mtorture>
        </dir>

        <dir>
            <title>Horror</title>
            <mtorture>tag/12/1</mtorture>
        </dir>

        <dir>
            <title>Martial Arts</title>
            <mtorture>tag/20/1</mtorture>
        </dir>

        <dir>
            <title>Music</title>
            <mtorture>tag/42/1</mtorture>
        </dir>

        <dir>
            <title>Revenge</title>
            <mtorture>tag/39/1</mtorture>
        </dir>

        <dir>
            <title>Science Fiction</title>
            <mtorture>tag/14/1</mtorture>
        </dir>

        <dir>
            <title>Snake!</title>
            <mtorture>tag/43/1</mtorture>
        </dir>

        <dir>
            <title>Sting!</title>
            <mtorture>tag/44/1</mtorture>
        </dir>

        <dir>
            <title>Vanity</title>
            <mtorture>tag/35/1</mtorture>
        </dir>

        <dir>
            <title>WTF?!</title>
            <mtorture>tag/34/1</mtorture>
        </dir>


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

per_page = '50'

base_main_link = 'http://www.movietorture.com/%s'
json_cat_url   = 'wp-json/wp/v2/posts/?per_page=%s&categories=%s&page=%s'
json_tag_url   = 'wp-json/wp/v2/posts/?per_page=%s&tags=%s&page=%s'

class MovieTorture(Plugin):
    name = "movietorture"

    def process_item(self, item_xml):
        if "<mtorture>" in item_xml:
            item = JenItem(item_xml)
            if "category/" in item.get("mtorture", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "MTortureByCat",
                    'url': item.get("mtorture", ""),
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
            elif "tag/" in item.get("mtorture", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "MTortureByTag",
                    'url': item.get("mtorture", ""),
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
            elif "play/" in item.get("mtorture", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PlayMTorture",
                    'url': item.get("mtorture", ""),
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
        dialog = xbmcgui.Dialog()
        if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear Movie Torture Plugin Cache?"):
            koding.Remove_Table("mtorture_plugin")


@route(mode='MTortureByCat', args=["url"])
def get_MTortureByCat(url):
    pins = ""
    category = url.split('/')[1]
    page_id = url.split('/')[2]

    if 'movies' in category:
        cat_id = '3'
    elif 'docus' in category:
        cat_id = '6'

    url = base_main_link % ((json_cat_url % (per_page, cat_id, page_id))) 

    count = 0

    xml = fetch_from_db(url)
    if not xml == '1':
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
                title   = remove_non_ascii(replaceHTMLCodes(post['title']['rendered']))
                description = remove_non_ascii(replaceHTMLCodes(post['excerpt']['rendered'])).replace('\/','/')
                description = re.sub('<[^<]+?>', '', description).replace('\nSee More','')
                
                content = remove_non_ascii(replaceHTMLCodes(post['content']['rendered'])).replace('\/','/')
                link = re.compile('<video controls.+?src=\"(.+?)\"').findall(content)[0]
                icon = re.compile('<meta itemprop=\"thumbnailUrl\" content=\"(.+?)\"').findall(content)[0]

                if len(link) > 0:
                    xml += "<item>"\
                           "    <title>%s</title>"\
                           "    <meta>"\
                           "        <summary>%s</summary>"\
                           "    </meta>"\
                           "    <mtorture>play/%s|%s</mtorture>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "</item>" % (title,description,link,title,icon)

            try:
                if count == 50:
                    xml += "<dir>"\
                           "    <title>Next Page >></title>"\
                           "    <meta>"\
                           "        <summary>Click here for the next page</summary>"\
                           "    </meta>"\
                           "    <mtorture>category/%s/%s</mtorture>"\
                           "</dir>" % (category,str(int(page_id)+1))
            except:
                failure = traceback.format_exc()
                xbmcgui.Dialog().textviewer('Item Exception',str(failure))
                pass

            save_to_db(xml, url)
        except:
            failure = traceback.format_exc()
            xbmcgui.Dialog().textviewer('Item Exception',str(failure))
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='MTortureByTag', args=["url"])
def get_MTortureByTag(url):
    pins = ""
    tag_id = url.split('/')[1]
    page_id = url.split('/')[2]

    url = base_main_link % ((json_tag_url % (per_page, tag_id, page_id))) 

    count = 0

    xml = fetch_from_db(url)
    if not xml == '1':
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
                title   = remove_non_ascii(replaceHTMLCodes(post['title']['rendered']))
                description = remove_non_ascii(replaceHTMLCodes(post['excerpt']['rendered'])).replace('\/','/')
                description = re.sub('<[^<]+?>', '', description).replace('\nSee More','')
                
                content = remove_non_ascii(replaceHTMLCodes(post['content']['rendered'])).replace('\/','/')
                link = re.compile('<video controls.+?src=\"(.+?)\"').findall(content)[0]
                icon = re.compile('<meta itemprop=\"thumbnailUrl\" content=\"(.+?)\"').findall(content)[0]

                if len(link) > 0:
                    xml += "<item>"\
                           "    <title>%s</title>"\
                           "    <meta>"\
                           "        <summary>%s</summary>"\
                           "    </meta>"\
                           "    <mtorture>play/%s|%s</mtorture>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "</item>" % (title,description,link,title,icon)

            try:
                if count == 50:
                    xml += "<dir>"\
                           "    <title>Next Page >></title>"\
                           "    <meta>"\
                           "        <summary>Click here for the next page</summary>"\
                           "    </meta>"\
                           "    <mtorture>tag/%s/%s</mtorture>"\
                           "</dir>" % (tag_id,str(int(page_id)+1))
            except:
                failure = traceback.format_exc()
                xbmcgui.Dialog().textviewer('Item Exception',str(failure))
                pass

            save_to_db(xml, url)
        except:
            failure = traceback.format_exc()
            xbmcgui.Dialog().textviewer('Item Exception',str(failure))
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='PlayMTorture', args=["url"])
def play_PlayMTorture(url):
    try:
        url = url.replace('play/','').split('|')
        link = url[0]
        title = url[1]

        item = xbmcgui.ListItem(label=title, path=link, iconImage=addon_icon, thumbnailImage=addon_icon)
        item.setInfo( type="Video", infoLabels={ "Title": title } )
        import resolveurl
        koding.Play_Video(link,showbusy=False,ignore_dp=True,item=item,resolver=resolveurl)
    except:
        xbmcgui.Dialog().ok('Stream', 'Unable to play stream')


def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "mtorture_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("mtorture_plugin",
                            {
                                "url": url,
                                "item": base64.b64encode(item),
                                "created": time.time()
                            })
    except:
        return False


def fetch_from_db(url):
    koding.reset_db()
    mtorture_plugin = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("mtorture_plugin", mtorture_plugin)
    match = koding.Get_From_Table(
        "mtorture_plugin", {"url": url})
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

