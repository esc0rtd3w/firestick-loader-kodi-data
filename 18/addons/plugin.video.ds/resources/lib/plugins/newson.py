"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you can do 
    whatever you want with this stuff. Just Ask first when not released through
    the tools and parser GIT. If we meet some day, and you think this stuff is
    worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------

    Version:
        2018.8.18:
            - Initial Release

    Overview:

        This is a scraper plugin for local news broadcasts and video clips in
            the United States.
        Newscasts can be viewed by the following methods:
            - List all States - Select state to view channels that live cast
            - By single State - Select state to view channels that live cast
        Newsclips can be viewed by the following methods:
            - List all States - Select state to view channels that have clips
            - By single State - Select state to view channels that have clips
            - By region - Select region to view channels that have clips

    Installing this Plugin:
        - Add the following line to your addon.xml file:
            <import addon="script.module.feedparser" version="5.1.3"/>
        - To adjust colors of "State" icons, modify the logo_bg_color and logo_font_color
            variables in the code below using hex colors

    Usage Examples:

        <dir>
            <title>Newscasts By State</title>
            <newson>states/newscast</newson>
        </dir>

        <dir>
            <title>California Newscasts</title>
            <newson>newscasts/California</newson>
        </dir>

        <dir>
            <title>Newsclips by State</title>
            <newson>states/newsclips</newson>
        </dir>

        <dir>
            <title>Nebraska Newsclips</title>
            <newson>newsclips/state/Nebraska</newson>
        </dir>

        <dir>
            <title>Midwest Newsclips</title>
            <newson>newsclips/region/Midwest</newson>
        </dir>

        <dir>
            <title>West Newsclips</title>
            <newson>newsclips/region/West</newson>
        </dir>

        <dir>
            <title>East Newsclips</title>
            <newson>newsclips/region/East</newson>
        </dir>

        <dir>
            <title>Southeast Newsclips</title>
            <newson>newsclips/region/Southeast</newson>
        </dir>

        <dir>
            <title>Southwest Newsclips</title>
            <newson>newsclips/region/Southwest</newson>
        </dir>

        <dir>
            <title>Northeast Newsclips</title>
            <newson>newsclips/region/Northeast</newson>
        </dir>

        <dir>
            <title>Northwest Newsclips</title>
            <newson>newsclips/region/Northwest</newson>
        </dir>


"""

import __builtin__
import base64, feedparser, datetime
import json,re,requests,os,traceback,urlparse
import koding
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')

logo_bg_color = '035e8b'
logo_font_color = 'FFFFFF'
logo_url = 'https://dummyimage.com/512x512/' + logo_bg_color + '/' + logo_font_color + '.png&text=%s'

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon   = xbmcaddon.Addon().getAddonInfo('icon')
headers = {'User_Agent':'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'} 

base_main_link = 'http://watchnewson.com/api/linear/channels'


class NewsON(Plugin):
    name = "newson"
    priority = 200

    def process_item(self, item_xml):
        if "<newson>" in item_xml:
            item = JenItem(item_xml)
            if "states/" in item.get("newson", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "StateList",
                    'url': item.get("newson", ""),
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
            elif "newscasts/" in item.get("newson", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "Newscasts",
                    'url': item.get("newson", ""),
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
            elif "newsclips/" in item.get("newson", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "Newsclips",
                    'url': item.get("newson", ""),
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
            elif "feed/" in item.get("newson", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "NewsFeed",
                    'url': item.get("newson", ""),
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


@route(mode='StateList', args=["url"])
def get_StateList(list_type):
    list_type = list_type.replace('states/', '') # clear our category tag off
    xml = ""
    pins = ""
    try:
        states = get_states()
        if len(states) == 0:
            xml += "<dir>"\
                   "    <title>[B]System down for maintenance[/B]</title>"\
                   "    <meta>"\
                   "        <summary>System down for maintenance</summary>"\
                   "    </meta>"\
                   "    <heading></heading>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "</dir>" % (addon_icon)
        else:
            for state in states:
                try:
                    icon = logo_url % (state)
                    xml += "<dir>"\
                           "    <title>%s</title>"\
                           "    <meta>"\
                           "        <summary>%s</summary>"\
                           "    </meta>" % (state, state)
                    if list_type == 'newscast':
                        xml += "    <newson>newscasts/%s</newson>" % (state)
                    else:
                        xml += "    <newson>newsclips/state/%s</newson>" % (state)
                    xml +=  "    <thumbnail>%s</thumbnail>"\
                            "</dir>" % (icon)
                except:
                    continue
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


# We do not pull the channel id from the JSON, because this is NOT local channel, but NewsOn channel
@route(mode='Newscasts', args=["url"])
def get_Newscasts(state):
    state = state.replace('newscasts/', '') # clear our type tag off
    xml = ""
    pins = ""
    try:
        newscasts = []
        chan_list = requests.get(base_main_link,headers).json()
        if len(chan_list) == 0:
            xml += "<dir>"\
                   "    <title>[B]System down for maintenance[/B]</title>"\
                   "    <meta>"\
                   "        <summary>System down for maintenance</summary>"\
                   "    </meta>"\
                   "    <heading></heading>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "</dir>" % (addon_icon)
        else:
            for channel in chan_list:
                try:
                    json_state = channel['config']['state'].strip(',').strip()
                except:
                    json_state = channel['config']['locations'][0]['state'].strip(',').strip()
                if json_state in state:
                    try:
                        title  = channel['title']
                        icon   = (channel['icon'] or addon_icon)
                        for cast in channel['streams']:
                            streamType = cast['StreamType']
                            if cast['StreamType'] == 'website':
                                continue
                            url = cast['Url']
                            if url in newscasts: # We already collected this one, tis a duplicate so we skip it
                                continue
                            else:
                                newscasts.append(url)
                            xml += "<item>"\
                                   "    <title>%s</title>"\
                                   "    <meta>"\
                                   "        <summary>%s</summary>"\
                                   "    </meta>"\
                                   "    <link>%s</link>"\
                                   "    <thumbnail>%s</thumbnail>"\
                                   "</item>" % (title,title,url,icon)
                    except:
                        continue
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='Newsclips', args=["url"])
def get_Newsclips(url):
    pins = ""
    url = url.split('/')
    list_type = url[1] # Could be state or region
    identifier = url[2] # Could be state name or region name

    xml = ""

    try:
        chan_list = requests.get(base_main_link,headers).json()
        if len(chan_list) == 0:
            xml += "<dir>"\
                   "    <title>[B]System down for maintenance[/B]</title>"\
                   "    <meta>"\
                   "        <summary>System down for maintenance</summary>"\
                   "    </meta>"\
                   "    <heading></heading>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "</dir>" % (addon_icon)
        else:
            for channel in chan_list:
                comp_item = ""
                if list_type == "state":
                    try:
                        comp_item = channel['config']['state'].strip(',').strip()
                    except:
                        comp_item = channel['config']['locations'][0]['state'].strip(',').strip()
                else:
                    try:
                        comp_item = channel['config']['region'].strip(',').strip()
                    except:
                        comp_item = channel['config']['locations'][0]['region'].strip(',').strip()
                if comp_item == identifier:
                    try: 
                        try:
                            feedurl = channel['config']['localvodfeed']
                        except:
                            continue
                        if feedurl == None or len(feedurl) == 0:
                            continue
                        title  = channel['title']
                        icon   = (channel['icon'] or addon_icon)
                        xml += "<dir>"\
                               "    <title>%s</title>"\
                               "    <meta>"\
                               "        <summary>Newsclips for %s</summary>"\
                               "    </meta>"\
                               "    <newson>feed/%s</newson>"\
                               "    <thumbnail>%s</thumbnail>"\
                               "</dir>" % (title,title,feedurl,icon)
                    except:
                        continue
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='NewsFeed', args=["url"])
def get_NewsFeed(url):
    url = url.replace('feed/', '')
    xml = ""
    pins = ""
    try:
        feed = feedparser.parse(url)
        for item in feed['entries']:
            if item and 'summary_detail' in item:
                for vids in item['media_content']:
                    try:
                        title = remove_non_ascii(item['title'])
                        vid_url = vids['url']
                        summary = remove_non_ascii(item['summary'])

                        try:
                            icon = item['media_thumbnail'][0]['url']
                        except:
                            icon = addon_icon

                        xml += "<item>"\
                               "    <title>%s</title>"\
                               "    <meta>"\
                               "        <summary>%s</summary>"\
                               "    </meta>"\
                               "    <link>%s</link>"\
                               "    <thumbnail>%s</thumbnail>"\
                               "</item>" % (title,summary,vid_url,icon)
                    except:
                        continue
    except:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


def get_states():
    states = []
    try:
        chan_list = requests.get(base_main_link,headers).json()
        if len(chan_list) == 0:
            return []
        for channel in chan_list:
            try:
                state = channel['config']['state'].strip(',').strip()
            except:
                state = channel['config']['locations'][0]['state'].strip(',').strip()
            if state in states: # We already collected this one, tis a duplicate so we skip it
                continue
            else:
                states.append(state)
        ret_list = sorted(states)
        return ret_list
    except:
        return []


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
