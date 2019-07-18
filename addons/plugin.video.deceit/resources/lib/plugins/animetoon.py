#!/usr/bin/python
# encoding=utf8
"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------

    Changelog:
        2018.7.11:
            - Added cache clearing
            - Indentation fix (Digital)

        2018.6.21:
            - Added caching to primary menus (Cache time is 3 hours)


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

CACHE_TIME = 10800  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'


class WatchCartoon(Plugin):
    name = "wctoon"

    def process_item(self, item_xml):
        if "<wctoon>" in item_xml:
            item = JenItem(item_xml)
            if "wcepisode/" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "WCEpisodes",
                    'url': item.get("wctoon", ""),
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
            elif "wcsearch" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "WCSearch",
                    'url': item.get("wctoon", ""),
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
            elif "list-videos/" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "WCListVideos",
                    'url': item.get("wctoon", ""),
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
            elif "direct/" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "WCPlayVideo",
                    'url': item.get("wctoon", ""),
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
            elif "main/" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "WCMain",
                    'url': item.get("wctoon", ""),
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
            elif "popular-list" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "WCPopular",
                    'url': item.get("wctoon", ""),
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
            elif "wcdaily-updates" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "WCDaily",
                    'url': item.get("wctoon", ""),
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
            elif "category/" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "WatchCartoon",
                    'url': item.get("wctoon", ""),
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

    def clear_cache(self):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear AnimeToon Plugin Cache?"):
            koding.Remove_Table("animetoon_com_plugin")


@route(mode='WatchCartoon', args=["url"])
def get_wcstream(url):
    url = url.replace('category/', '') # Strip our category tag off.
    url = urlparse.urljoin('http://www.animetoon.org/', url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url).content
            sections = dom_parser.parseDOM(html, 'table', attrs={'class':'series_index'})

            for table in sections:
                try:
                    the_cols = dom_parser.parseDOM(table, 'td')
                    for column in the_cols:
                        if '&nbsp;' in column:
                            continue
                        show_url, title = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(column)[0]
                        title = refreshtitle(title)
                        title = remove_non_ascii(title)
                        xml += "<dir>"\
                               "    <title>[B][COLORwhite]%s[/COLOR][/B]</title>"\
                               "    <wctoon>wcepisode/%s</wctoon>"\
                               "    <thumbnail>%s</thumbnail>"\
                               "    <summary>%s</summary>"\
                               "</dir>" % (title,show_url,addon_icon,title)
                except:
                    continue
            save_to_db(xml, url)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='WCMain', args=["url"])
def get_wcmainstream(subid):
    xml = ""
    subid = subid.replace('main/', '', 1) # Strip our category tag off.
    subid = subid.split('/')

    try:
        html = requests.get('http://www.animetoon.org/').content
        if subid[0] == 'popular_series':
            thedivs = dom_parser.parseDOM(html, 'div', attrs={'id':subid[0]})[int(subid[1])]
            list_items = dom_parser.parseDOM(thedivs, 'li')
            for content in list_items:
                try:
                    info_div = dom_parser.parseDOM(content, 'div', attrs={'class':'slink'})[0]
                    show_url, title = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(info_div)[0]
                    title = refreshtitle(title).replace('Episode ', 'EP:')
                    title = remove_non_ascii(title)
                    show_icon = re.compile('src="(.+?)"',re.DOTALL).findall(content)[0]
                    xml += "<dir>"\
                           "    <title>[B][COLORwhite]%s[/COLOR][/B]</title>"\
                           "    <wctoon>wcepisode/%s</wctoon>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "    <summary>%s</summary>"\
                           "</dir>" % (title,show_url,show_icon,title)
                except:
                    continue
        elif subid[0] == 'updates':
            thetable = dom_parser.parseDOM(html, 'table', attrs={'id':subid[0]})[int(subid[1])]
            the_rows = dom_parser.parseDOM(thetable, 'tr')
            for content in the_rows:
                try:
                    the_lists = dom_parser.parseDOM(content, 'li')
                    for item in the_lists:
                        show_url, title = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(item)[0]
                        title = refreshtitle(title).replace('Episode ', 'EP:')
                        title = remove_non_ascii(title)
                        xml += "<dir>"\
                               "    <title>[B][COLORwhite]%s[/COLOR][/B]</title>"\
                               "    <wctoon>wcepisode/%s</wctoon>"\
                               "    <thumbnail>%s</thumbnail>"\
                               "    <summary>%s</summary>"\
                               "</dir>" % (title,show_url,addon_icon,title)
                except:
                    continue
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='WCPopular', args=["url"])
def get_wcpopular(url):
    url = urlparse.urljoin('http://www.animetoon.org/', url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url).content
            thedivs = dom_parser.parseDOM(html, 'div', attrs={'class':'series_list'})[1]
            list_items = dom_parser.parseDOM(thedivs, 'li')
            for content in list_items:
                try:
                    info_header = dom_parser.parseDOM(content, 'h3')[0]
                    show_url, title = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(info_header)[0]
                    title = refreshtitle(title).replace('Episode ', 'EP:')
                    title = remove_non_ascii(title)
                    show_icon = re.compile('src="(.+?)"',re.DOTALL).findall(content)[0]
                    xml += "<dir>"\
                           "    <title>[B][COLORwhite]%s[/COLOR][/B]</title>"\
                           "    <wctoon>wcepisode/%s</wctoon>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "    <summary>%s</summary>"\
                           "</dir>" % (title,show_url,show_icon,title)
                except:
                    continue

            pagination = dom_parser.parseDOM(html, 'ul', attrs={'class':'pagination'})[0]
            if len(pagination) > 0:
                list_items = dom_parser.parseDOM(pagination, 'li')
                next_li = list_items[(len(list_items)-1)]
                next_url = 'popular-list/%s' % (re.compile('href="http://www.animetoon.org/popular-list/(.+?)"',re.DOTALL).findall(next_li)[0])
                xml += "<dir>"\
                       "    <title>[B][COLORorange]Next Page >>[/COLOR][/B]</title>"\
                       "    <wctoon>%s</wctoon>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "    <summary>Next Page</summary>"\
                       "</dir>" % (next_url,show_icon)
            save_to_db(xml, url)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='WCDaily', args=["url"])
def get_wcdaily(url):
    url = url.replace('wcdaily-', '') # Strip our episode tag off.
    url = urlparse.urljoin('http://www.animetoon.org/', url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url).content
            thetable = dom_parser.parseDOM(html, 'table', attrs={'id':'updates'})[0]
            the_rows = dom_parser.parseDOM(thetable, 'tr')
            for content in the_rows:
                try:
                    the_lists = dom_parser.parseDOM(content, 'li')
                    for item in the_lists:
                        show_url, title = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(item)[0]
                        title = refreshtitle(title).replace('Episode ', 'EP:')
                        title = remove_non_ascii(title)
                        xml += "<dir>"\
                               "    <title>[B][COLORwhite]%s[/COLOR][/B]</title>"\
                               "    <wctoon>wcepisode/%s</wctoon>"\
                               "    <thumbnail>%s</thumbnail>"\
                               "    <summary>%s</summary>"\
                               "</dir>" % (title,show_url,addon_icon,title)
                except:
                    continue

            pagination = dom_parser.parseDOM(html, 'ul', attrs={'class':'pagination'})[0]
            if len(pagination) > 0:
                list_items = dom_parser.parseDOM(pagination, 'li')
                next_li = list_items[(len(list_items)-1)]
                next_url = 'wcdaily-updates/%s' % (re.compile('href="http://www.animetoon.org/updates/(.+?)"',re.DOTALL).findall(next_li)[0])
                xml += "<dir>"\
                       "    <title>[B][COLORorange]Next Page >>[/COLOR][/B]</title>"\
                       "    <wctoon>%s</wctoon>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "    <summary>Next Page</summary>"\
                       "</dir>" % (next_url,addon_icon)
            save_to_db(xml, url)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='WCEpisodes', args=["url"])
def get_wcepisodes(url):
    url = url.replace('wcepisode/', '') # Strip our episode tag off.
    url = urlparse.urljoin('http://www.animetoon.org/', url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url).content
            thediv = dom_parser.parseDOM(html, 'div', attrs={'id':'videos'})[0]
            lists = dom_parser.parseDOM(thediv, 'li')

            for entry in lists:
                show_url, title = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(entry)[0]
                title = refreshtitle(title).replace('Episode ', 'EP:')
                title = remove_non_ascii(title)
                show_icon = dom_parser.parseDOM(html, 'div', attrs={'id':'series_info'})[0]
                show_icon = re.compile('src="(.+?)"',re.DOTALL).findall(show_icon)[0]
                xml += "<item>"\
                       "    <title>[B][COLORwhite]%s[/COLOR][/B]</title>"\
                       "    <wctoon>list-videos/%s</wctoon>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "    <summary>%s</summary>"\
                       "</item>" % (title,show_url,show_icon,title)
            save_to_db(xml, url)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='WCSearch', args=["url"])
def get_wcsearch(url):
    xml = ""
    url = url.replace('wcsearch/', '') # Strip our search tag off when used with keywords in the xml
    url = url.replace('wcsearch', '') # Catch plain case, for when overall search is used.

    if url != None and url != "":
        search = url
    else:
        keyboard = xbmc.Keyboard('', 'Search for Movies')
        keyboard.doModal()
        if keyboard.isConfirmed() != None and keyboard.isConfirmed() != "":
            search = keyboard.getText()
        else:
            return

    if search == None or search == "":
        xml += "<item>"\
               "    <title>Search Cancelled</title>"\
               "    <link>plugin://plugin.video.deceit/?mode=section_item</link>"\
               "    <thumbnail>%s</thumbnail>"\
               "</item>" % (addon_icon)
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())
        return

    total = 0

    try:
        search_url = 'http://www.animetoon.org/toon/search?key=%s' % search.replace(' ', '+')
        html = requests.get(search_url).content
        thedivs = dom_parser.parseDOM(html, 'div', attrs={'class':'series_list'})[0]
        list_items = dom_parser.parseDOM(thedivs, 'li')
        for content in list_items:
            try:
                info_header = dom_parser.parseDOM(content, 'h3')[0]
                show_url, title = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(info_header)[0]
                title = refreshtitle(title).replace('Episode ', 'EP:')
                title = remove_non_ascii(title)
                show_icon = re.compile('src="(.+?)"',re.DOTALL).findall(content)[0]
                xml += "<dir>"\
                       "    <title>[B][COLORwhite]%s[/COLOR][/B]</title>"\
                       "    <wctoon>wcepisode/%s</wctoon>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "    <summary>%s</summary>"\
                       "</dir>" % (title,show_url,show_icon,title)
                total += 1
            except:
                continue

        pagination = dom_parser.parseDOM(html, 'ul', attrs={'class':'pagination'})[0]
        if len(pagination) > 0:
            list_items = dom_parser.parseDOM(pagination, 'li')
            next_li = list_items[(len(list_items)-1)]
            next_url = 'popular-list/%s' % (re.compile('href="http://www.animetoon.org/popular-list/(.+?)"',re.DOTALL).findall(next_li)[0])
            xml += "<dir>"\
                   "    <title>[B][COLORwhite]Next Page >>[/COLOR][/B]</title>"\
                   "    <wctoon>%s</wctoon>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <summary>Next Page</summary>"\
                   "</dir>" % (next_url,show_icon)
    except:
        pass

    if total > 0:
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='WCListVideos', args=["url"])
def get_wclistvideos(url):
    url = url.replace('list-videos/', '') # Strip our episode tag off.

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url).content
            the_divs = dom_parser.parseDOM(html, 'div', attrs={'class':'vmargin'})
            for video_entry in the_divs:
                iframe = re.compile('iframe src="(.+?)"',re.DOTALL).findall(video_entry)[0]

                html = requests.get(iframe)
                nurl = re.findall(r'''file:\s*['\"]([^'\"]+)['\"](?:\,\s*label:\s*|)(?:['\"]|)([\d]+|)''', html.text)
                if len(nurl) == 1:
                    host = nurl[0][0].split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[1].upper() 
                    xml += "<item>"\
                           "    <title>[B][COLORwhite]%s[/COLOR][/B]</title>"\
                           "    <wctoon>direct/%s</wctoon>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "    <summary>%s</summary>"\
                           "</item>" % (host,str(nurl[0][0]),addon_icon,host)
            save_to_db(xml, url)
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='WCPlayVideo', args=["url"])
def get_wcplayvideo(url):
    url = url.replace('direct/', '') # Strip our episode tag off.
    try:
        xbmc.executebuiltin("PlayMedia(%s)" % (url))
        quit()
        return
    except:
        pass


def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "animetoon_com_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("animetoon_com_plugin",
                            {
                                "url": url,
                                "item": base64.b64encode(item),
                                "created": time.time()
                            })
    except:
        return False


def fetch_from_db(url):
    koding.reset_db()
    animetoon_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("animetoon_com_plugin", animetoon_plugin_spec)
    match = koding.Get_From_Table(
        "animetoon_com_plugin", {"url": url})
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


def refreshtitle(title):
    title = replaceEscapeCodes(title)
    title = replaceHTMLCodes(title).replace('English Dubbed','[COLOR yellow](English Dubbed)[/COLOR]').replace('English Subbed','[COLOR orange](English Subbed)[/COLOR]')
    return title


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

