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

    Version:
        2018.7.2:
            - Added Clear Cache function
            - Minor update on fetch cache returns

        2018.6.20:
            - Added caching to primary menus (Cache time is 3 hours)

        2018.5.17
            - Initial Release


    XML Explanations:
        Tags: 
            <docuh></docuh> - Displays the entry as category's contents


    Usage Examples:

        <dir>
            <title>911</title>
            <docuh>dhcategory/911</docuh>
        </dir>

        <dir>
            <title>Activist</title>
            <docuh>dhcategory/activist</docuh>
        </dir>

        <dir>
            <title>Archaeology</title>
            <docuh>dhcategory/archaeology</docuh>
        </dir>

        <dir>
            <title>Art and Artists</title>
            <docuh>dhcategory/art-and-artists</docuh>
        </dir>

        <dir>
            <title>Atheism</title>
            <docuh>dhcategory/atheism</docuh>
        </dir>

        <dir>
            <title>Biographies</title>
            <docuh>dhcategory/biographies</docuh>
        </dir>

        <dir>
            <title>Business</title>
            <docuh>dhcategory/business</docuh>
        </dir>

        <dir>
            <title>Celebrity</title>
            <docuh>dhcategory/celebrity</docuh>
        </dir>

        <dir>
            <title>Crime</title>
            <docuh>dhcategory/crime</docuh>
        </dir>

        <dir>
            <title>Conference</title>
            <docuh>dhcategory/conference</docuh>
        </dir>

        <dir>
            <title>Conspiracy</title>
            <docuh>dhcategory/conspiracy</docuh>
        </dir>

        <dir>
            <title>Countries</title>
            <docuh>dhcategory/countries</docuh>
        </dir>

        <dir>
            <title>Drugs</title>
            <docuh>dhcategory/drugs</docuh>
        </dir>

        <dir>
            <title>Economics</title>
            <docuh>dhcategory/economics</docuh>
        </dir>

        <dir>
            <title>Educational</title>
            <docuh>dhcategory/educational</docuh>
        </dir>

        <dir>
            <title>Environment</title>
            <docuh>dhcategory/environment</docuh>
        </dir>

        <dir>
            <title>Evolution</title>
            <docuh>dhcategory/evolution</docuh>
        </dir>

        <dir>
            <title>Gangs</title>
            <docuh>dhcategory/gangs</docuh>
        </dir>

        <dir>
            <title>Health</title>
            <docuh>dhcategory/health</docuh>
        </dir>

        <dir>
            <title>History</title>
            <docuh>dhcategory/history</docuh>
        </dir>

        <dir>
            <title>Human Rights</title>
            <docuh>dhcategory/human-rights</docuh>
        </dir>

        <dir>
            <title>Lifestyle</title>
            <docuh>dhcategory/lifestyle</docuh>
        </dir>

        <dir>
            <title>Movies</title>
            <docuh>dhcategory/movies</docuh>
        </dir>

        <dir>
            <title>Music</title>
            <docuh>dhcategory/music</docuh>
        </dir>

        <dir>
            <title>Mystery</title>
            <docuh>dhcategory/mystery</docuh>
        </dir>

        <dir>
            <title>Nature</title>
            <docuh>dhcategory/nature</docuh>
        </dir>

        <dir>
            <title>News and Politics</title>
            <docuh>dhcategory/news-politics</docuh>
        </dir>

        <dir>
            <title>Performing Arts</title>
            <docuh>dhcategory/performing-arts</docuh>
        </dir>

        <dir>
            <title>Philosophy</title>
            <docuh>dhcategory/philosophy</docuh>
        </dir>

        <dir>
            <title>Preview Only</title>
            <docuh>dhcategory/preview-only</docuh>
        </dir>

        <dir>
            <title>Psychology</title>
            <docuh>dhcategory/psychology</docuh>
        </dir>

        <dir>
            <title>Religion</title>
            <docuh>dhcategory/religion</docuh>
        </dir>

        <dir>
            <title>Science</title>
            <docuh>dhcategory/science</docuh>
        </dir>

        <dir>
            <title>Society</title>
            <docuh>dhcategory/society</docuh>
        </dir>

        <dir>
            <title>Space</title>
            <docuh>dhcategory/space</docuh>
        </dir>

        <dir>
            <title>Spiritual</title>
            <docuh>dhcategory/spiritual</docuh>
        </dir>

        <dir>
            <title>Sport and Adventure</title>
            <docuh>dhcategory/sportadventure</docuh>
        </dir>

        <dir>
            <title>Technology</title>
            <docuh>dhcategory/technology</docuh>
        </dir>

        <dir>
            <title>War</title>
            <docuh>dhcategory/war</docuh>
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

CACHE_TIME = 10800  # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')

docu_link = 'http://documentaryheaven.com'
docu_cat_list = 'http://documentaryheaven.com/category/'

"""
Add strings to the reg_items for domains that are supported naturally by resolveurl
"""
reg_items = {'vimeo','dailymotion','rutube','vid.ag','thevideobee','vidzi.tv'}
unreg_items = {'myspace','nfb.ca','snagfilms','dotsub','en.musicplayon.com','vkontakte.ru','veehd.com','liveleak.com','imdb.com','disclose.tv','videoweed.es','putlocker','vid.ag','vice.com'}
"""
Examples for unreg_items, to look into future support or if requested to fix by adding to/fixing in resolveurl

thevideobee: Music - Amy
snagfiles: Music - Jimi Hendrix the Uncut Story
dotsub: Music - The Man in the Mirror
en.musicplayon.com: Music - Prince: The Glory Years
vkontakte.ru: Music - Paul Kalkbrenner: A live documentary
veehd.com: The Abandoned Marsh
liveleak.com: Lost Nuke
imdb.com: Eceti Ranch
disclose.tv: The Revelation of the Pyramids
videoweed.es: EP2/4 Wonders of the Universe
putlocker: EP 1/6 The Private Life of Plants
vid.ag: Jim: The James Foley Story
vice.com: Our Rising Oceans

"""

class DocuHeaven(Plugin):
    name = "docuh"
    priority = 200

    def process_item(self, item_xml):
        if "<docuh>" in item_xml:
            item = JenItem(item_xml)
            if "dhcategory/" in item.get("docuh", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "DHCats",
                    'url': item.get("docuh", ""),
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
        if dialog.yesno(xbmcaddon.Addon().getAddonInfo('name'), "Clear Documentary Heaven Plugin Cache?"):
            koding.Remove_Table("docuheaven_com_plugin")

@route(mode='DHCats', args=["url"])
def get_DHcats(url):
    pins = ""
    url = url.replace('dhcategory/', '') # Strip our category tag off.
    orig_cat = url.split("/")[0]
    url = urlparse.urljoin(docu_cat_list, url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            html = requests.get(url).content
            doc_list = dom_parser.parseDOM(html, 'article')
            for content in doc_list:
                try:
                    docu_info = re.compile('<h2>(.+?)</h2>',re.DOTALL).findall(content)[0]

                    docu_title = re.compile('<a.+?">(.+?)</a>',re.DOTALL).findall(docu_info)[0]
                    docu_title = docu_title.replace("&amp;","&").replace('&#39;',"'").replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
                    docu_summary = re.compile('<p>(.+?)</p>',re.DOTALL).findall(content)[0].replace('&quot;','"').replace('&#39;',"'").replace('&#8211;',' - ').replace('&#8217;',"'").replace('&#8216;',"'").replace('&#038;','&').replace('&acirc;','')
                    try:
                        docu_icon = re.compile('data-src="(.+?)"',re.DOTALL).findall(content)[0]
                    except:
                        docu_icon = re.compile('src="(.+?)"',re.DOTALL).findall(content)[0]

                    docu_url = re.compile('href="(.+?)"',re.DOTALL).findall(docu_info)[0]
                    docu_html = requests.get(docu_url).content

                    try:
                        docu_item = dom_parser.parseDOM(docu_html, 'meta', attrs={'itemprop':'embedUrl'}, ret='content')[0]
                    except:
                        docu_item = dom_parser.parseDOM(docu_html, 'iframe', ret='src')[0]

                    if 'http:' not in docu_item and  'https:' not in docu_item:
                        docu_item = 'https:' + docu_item
                    docu_url = docu_item

                    replaceHTMLCodes(docu_title)

                    if 'youtube' in docu_url:
                        if 'videoseries' not in docu_url:
                            xml += "<item>"\
                                   "    <title>%s</title>"\
                                   "    <link>%s</link>"\
                                   "    <thumbnail>%s</thumbnail>"\
                                   "    <summary>%s</summary>"\
                                   "</item>" % (docu_title,docu_url,docu_icon,docu_summary)
                        else:
                            # videoseries stuff?
                            video_id = docu_url.split("=")[-1]
                            docu_url = 'plugin://plugin.video.youtube/playlist/%s/' % video_id
                            xml += "<item>"\
                                   "    <title>%s</title>"\
                                   "    <link>%s</link>"\
                                   "    <thumbnail>%s</thumbnail>"\
                                   "    <summary>%s</summary>"\
                                   "</item>" % (docu_title,docu_url,docu_icon,docu_summary)
                    elif 'archive.org/embed' in docu_url:
                        docu_html = requests.get(docu_url).content
                        video_element = dom_parser.parseDOM(docu_html, 'source', ret='src')[0]
                        docu_url = urlparse.urljoin('https://archive.org/', video_element)
                        xml += "<item>"\
                               "    <title>%s</title>"\
                               "    <link>%s</link>"\
                               "    <thumbnail>%s</thumbnail>"\
                               "    <summary>%s</summary>"\
                               "</item>" % (docu_title,docu_url,docu_icon,docu_summary)
                    elif any(x in docu_url for x in reg_items):
                        xml += "<item>"\
                               "    <title>%s</title>"\
                               "    <link>%s</link>"\
                               "    <thumbnail>%s</thumbnail>"\
                               "    <summary>%s</summary>"\
                               "</item>" % (docu_title,docu_url,docu_icon,docu_summary)
                    elif any(x in docu_url for x in unreg_items):
                        # most of these gone now so screw it lol, and no valid player know yet to work with nfb
                        continue
                    else:
                        xbmcgui.Dialog().ok('Unknown Host - ' + docu_title,str(docu_url)) 
                except:
                    continue

            try:
                navi_content = dom_parser.parseDOM(html, 'div', attrs={'class':'numeric-nav'})[0]
                if '>NEXT' in navi_content:
                    links = dom_parser.parseDOM(navi_content, 'a', ret='href')
                    link = links[(len(links)-1)]
                    page = link.split("/")[-2]
                    xml += "<dir>"\
                           "    <title>Next Page >></title>"\
                           "    <docuh>dhcategory/%s/page/%s</docuh>"\
                           "</dir>" % (orig_cat,page)
            except:
                pass
        except:
            pass

        save_to_db(xml, url)

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "docuheaven_com_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("docuheaven_com_plugin",
                            {
                                "url": url,
                                "item": base64.b64encode(item),
                                "created": time.time()
                            })
    except:
        return False


def fetch_from_db(url):
    koding.reset_db()
    docuh_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("docuheaven_com_plugin", docuh_plugin_spec)
    match = koding.Get_From_Table(
        "docuheaven_com_plugin", {"url": url})
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
    txt = txt.replace("&quot;", "\"").replace("&amp;", "&")
    txt = txt.replace('&#8216;','\'').replace('&#8217;','\'').replace('&#038;','&').replace('&#8230;','....')
    txt = txt.strip()
    return txt


def remove_non_ascii(text):
    try:
        text = text.decode('utf-8').replace(u'\xc2', u'A').replace(u'\xc3', u'A').replace(u'\xc4', u'A')
    except:
        pass
    return unidecode(text)
