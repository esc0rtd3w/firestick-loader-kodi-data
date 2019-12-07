#!/usr/bin/python
# encoding=utf8
"""

    Copyright (C) 2018, MuadDib

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
<title>50 Latest Releases</title>
<wctoon>topfifty/last-50-recent-release</wctoon>
</dir>

<dir>
<title>Today's Picks</title>
<wctoon>main/today</wctoon>
</dir>

<dir>
<title>Most Popular</title>
<wctoon>main/popular</wctoon>
</dir>

<dir>
<title>Dubbed Anime</title>
<wctoon>category/dubbed-anime-list</wctoon>
</dir>

<dir>
<title>Subbed Anime</title>
<wctoon>category/subbed-anime-list</wctoon>
</dir>

<dir>
<title>Cartoons</title>
<wctoon>category/cartoon-list</wctoon>
</dir>

<dir>
<title>Movies</title>
<wctoon>category/movie-list</wctoon>
</dir>

<dir>
<title>Ova Series</title>
<wctoon>category/ova-list</wctoon>
</dir>

<dir>
<title>Search Site</title>
<wctoon>wcsearch</wctoon>
</dir>

<dir>
<title>Everything 101 Dalmatians</title>
<wctoon>wcsearch/101 dalmatians</wctoon>
</dir>

<dir>
<title>Action Genre</title>
<wctoon>wcgenre/14</wctoon>
</dir>



"""

import base64,json,re,requests,os,traceback,urlparse
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

addon_fanart = 'https://wallup.net/wp-content/uploads/2017/10/25/487188-umbrella-anime_girls-neon-748x477.jpg'
addon_icon   = 'https://www.watchcartoononline.io/wp-content/themes/animewp78712/images/logo.gif'
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
            elif "wcgenre" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "WCGenre",
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
            elif "topfifty/" in item.get("wctoon", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "TopFifty",
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


@route(mode='WatchCartoon', args=["url"])
def get_wcstream(url):
    xml = ""
    url = url.replace('category/', '') # Strip our category tag off.
    try:
        url = urlparse.urljoin('https://www.watchcartoononline.io', url)

        html = requests.get(url).content
        ddmcc = dom_parser.parseDOM(html, 'div', attrs={'class':'ddmcc'})[0]
        # pull root List, as all the minor lists are contained within it
        lists = dom_parser.parseDOM(ddmcc, 'li')

        for entry in lists:
            try:
                movie_style = 0
                try:
                    # if this fails, means it is a movie/ova series entry as they use different html for those categories
                    show_url, title = re.compile('<a href="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(entry)[0]
                except:
                    show_url, title = re.compile('<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(entry)[0]
                    movie_style = 1
                title = refreshtitle(title)
                title = remove_non_ascii(title)

                if movie_style == 1:
                    xml += "<item>"\
                           "    <title>%s</title>"\
                           "    <wctoon>direct/%s</wctoon>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "    <summary>%s</summary>"\
                           "</item>" % (title,show_url,addon_icon,title)
                else:
                    xml += "<dir>"\
                           "    <title>%s</title>"\
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


@route(mode='TopFifty', args=["url"])
def get_wctopfiftystream(url):
    xml = ""
    url = url.replace('topfifty/', '') # Strip our category tag off.

    try:
        url = urlparse.urljoin('https://www.watchcartoononline.io', url)
        html = requests.get(url).content
        thediv = dom_parser.parseDOM(html, 'div', attrs={'class':'menulaststyle'})[0]
        lists = dom_parser.parseDOM(thediv, 'li')

        for entry in lists:
            try:
                show_url, title = re.compile('<a href="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(entry)[0]
                title = refreshtitle(title)
                title = remove_non_ascii(title)

                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <wctoon>direct/%s</wctoon>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "    <summary>%s</summary>"\
                       "</item>" % (title,show_url,addon_icon,title)
            except:
                continue
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='WCMain', args=["url"])
def get_wcmainstream(subid):
    xml = ""
    subid = subid.replace('main/', '') # Strip our category tag off.

    try:
        html = requests.get('https://www.watchcartoononline.io').content
        thedivs = dom_parser.parseDOM(html, 'div', attrs={'id':'sidebar'})
        for content in thedivs:
            try:
                header = dom_parser.parseDOM(content, 'h3')[0]
                if header == None:
                    continue
                if subid in header.lower():
                    lists = dom_parser.parseDOM(content, 'li')
                    for entry in lists:
                        show_url, title = re.compile('<a href="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(entry)[0]
                        title = refreshtitle(title).replace('Episode ', 'EP:')
                        title = remove_non_ascii(title)

                        if 'popular' in subid:
                            xml += "<dir>"\
                                   "    <title>%s</title>"\
                                   "    <wctoon>wcepisode/%s</wctoon>"\
                                   "    <thumbnail>%s</thumbnail>"\
                                   "    <summary>%s</summary>"\
                                   "</dir>" % (title,show_url,addon_icon,title)
                        else:
                            xml += "<item>"\
                                   "    <title>%s</title>"\
                                   "    <wctoon>direct/%s</wctoon>"\
                                   "    <thumbnail>%s</thumbnail>"\
                                   "    <summary>%s</summary>"\
                                   "</item>" % (title,show_url,addon_icon,title)
                else:
                    continue
            except:
                continue
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='WCEpisodes', args=["url"])
def get_wcepisodes(url):
    xml = ""
    url = url.replace('wcepisode/', '') # Strip our episode tag off.

    try:
        url = urlparse.urljoin('https://www.watchcartoononline.io', url)

        html = requests.get(url).content
        thediv = dom_parser.parseDOM(html, 'div', attrs={'id':'catlist-listview'})[0]
        lists = dom_parser.parseDOM(thediv, 'li')

        for entry in lists:
            show_url, title = re.compile('<a href="(.+?)".+?>(.+?)</a>',re.DOTALL).findall(entry)[0]
            title = refreshtitle(title).replace('Episode ', 'EP:')
            title = remove_non_ascii(title)
            show_icon = dom_parser.parseDOM(html, 'meta', attrs={'property':'og:image'}, ret='content')[0]

            xml += "<item>"\
                   "    <title>%s</title>"\
                   "    <wctoon>direct/%s</wctoon>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <summary>%s</summary>"\
                   "</item>" % (title,show_url,show_icon,title)
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='WCGenre', args=["url"])
def get_wcgenre(url):
    xml = ""
    if 'all' in url:
        get_wcgenrelist()
        return
    else:
        url = url.replace('wcgenre/', '') # Strip our genre tag off.

    try:
        url = urlparse.urljoin('https://www.watchcartoononline.io/search-by-genre/', url)
        html = requests.get(url).content
        ddmcc = dom_parser.parseDOM(html, 'div', attrs={'class':'ddmcc'})[0]
        # pull root List, as all the minor lists are contained within it
        lists = dom_parser.parseDOM(ddmcc, 'li')

        for entry in lists:
            show_url, title = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(entry)[0]
            title = refreshtitle(title)
            title = remove_non_ascii(title)

            xml += "<dir>"\
                   "    <title>%s</title>"\
                   "    <wctoon>wcepisode/%s</wctoon>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <summary>%s</summary>"\
                   "</dir>" % (title,show_url,addon_icon,title)
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


def get_wcgenrelist():
    xml = ""

    try:
        url = 'https://www.watchcartoononline.io/search-by-genre/'
        html = requests.get(url).content
        ddmcc = dom_parser.parseDOM(html, 'div', attrs={'class':'ddmcc'})[0]
        # pull root List, as all the minor lists are contained within it
        lists = dom_parser.parseDOM(ddmcc, 'li')

        for entry in lists:
            show_url, title = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(entry)[0]
            # convert show_url to get last tag in the url for the xml creation
            show_url =  show_url.split('/')[-1]
            title = refreshtitle(title)
            title = remove_non_ascii(title)

            xml += "<dir>"\
                   "    <title>%s</title>"\
                   "    <wctoon>wcgenre/%s</wctoon>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "    <summary>%s</summary>"\
                   "</dir>" % (title,show_url,addon_icon,title)
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
        keyboard = xbmc.Keyboard('', 'Search for')
        keyboard.doModal()
        if keyboard.isConfirmed() != None and keyboard.isConfirmed() != "":
            search = keyboard.getText()
        else:
            return

    if search == None or search == "":
        xml += "<item>"\
               "    <title>Search Cancelled</title>"\
               "    <link>plugin://plugin.video.squadcontrol/?mode=section_item</link>"\
               "    <thumbnail>%s</thumbnail>"\
               "</item>" % (addon_icon)
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())
        return

    total = 0

    try:
        search_url = 'https://www.watchcartoononline.io/wp-json/wp/v2/posts?per_page=100&search=%s' % search.replace(' ', '%20')
        html = requests.get(search_url).content
        results = re.compile('"post","link":"(.+?)","title".+?"rendered":"(.+?)"',re.DOTALL).findall(html)
        if len(results) == 0:
            dialog = xbmcgui.Dialog()
            dialog.ok('Search Results', 'Search Results are empty')
            return
        for link,name in results:
            link = link.replace('\\','')
            name = refreshtitle(name).replace('Episode ', 'EP:')
            name = remove_non_ascii(name)
            if search.lower() in name.lower() or search.lower() in link.lower(): 
                xml += "<dir>"\
                       "    <title>%s</title>"\
                       "    <wctoon>direct/%s</wctoon>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</dir>" % (name,link,addon_icon)
                total += 1
    except:
        pass

    if total > 0:
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())


"""

    Kudos to the team over at Incursion on updates for the parsing to get links

"""
@route(mode='WCPlayVideo', args=["url"])
def get_wcplayvideo(url):
    url = url.replace('direct/', '') # Strip our episode tag off.
    html = requests.get(url)
    url = ''
    try:
        match = re.findall('''var\s*[a-zA-Z]{3}\s*\=\s*\[([^\]]+)''', html.text)[0]
        spread = re.findall('''-\s*(\d+)\)\;\s*\}''', html.text)[0]
        match = re.findall('''['"]([^'"]+)['"]''', match)

        for i in match:
            i = base64.b64decode(i)
            i = re.findall(r'(\d+)',i)[0]
            i = chr(int(i) - int(spread))
            url += i
        url = re.findall(r'src="(.*?)"', url.replace("embed", "embed-adh"))[0]
        url = urlparse.urljoin('https://www.watchcartoononline.io', url)
        url = requests.get(url)
        url = re.findall(r'''file:\s*['\"]([^'\"]+)['\"](?:\,\s*label:\s*|)(?:['\"]|)([\d]+|)''', url.text)
        url = [(i[0],'0' if i[1] == '' else i[1]) for i in url]
        url = sorted(url, key=lambda x: int(x[1]),reverse=True)

        xbmc.executebuiltin("PlayMedia(%s)" % (url[0][0]))
        quit()
        return
    except:
        pass

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

