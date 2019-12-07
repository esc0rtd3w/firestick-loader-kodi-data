#!/usr/bin/python
# encoding=utf8
"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you can do
    whatever you want with this stuff. Just Ask first when not released through
    the tools and parser GIT. If we meet some day, and you think this stuff is
    worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------

<dir>
<title>Swift streams</title>
<swift>allthespice</swift>
</dir>

"""

import __builtin__

import requests
# import traceback
import koding
import xbmc
import xbmcaddon
import xbmcgui

from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent = 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)'

base_api_url = 'http://swiftstreamz.com/SwiftLive/api.php'
base_dta_url = 'http://swiftstreamz.com/SwiftLive/swiftlive.php'
base_cat_url = 'http://swiftstreamz.com/SwiftLive/api.php?cat_id=%s'
base_ico_url = 'http://swiftstreamz.com/SwiftLive/images/thumbs/%s'


class SwiftLive(Plugin):
    name = "swiftstreamz"

    def process_item(self, item_xml):
        if "<swift>" in item_xml:
            item = JenItem(item_xml)
            if "allthespice" in item.get("swift", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "SwiftMain",
                    'url': item.get("swift", ""),
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
            elif "swiftcategory" in item.get("swift", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "SwiftCat",
                    'url': item.get("swift", ""),
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
            elif "swiftplay/" in item.get("swift", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "SwiftPlay",
                    'url': item.get("swift", ""),
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


@route(mode='SwiftMain', args=["url"])
def get_swiftstreamz(url):
    pins = ""
    xml = ""
    url = url.replace('allthespice/', '')  # Strip our category tag off.
    try:
        headers = {'Authorization': 'Basic U3dpZnRTdHJlYW16OkBTd2lmdFN0cmVhbXpA', 'User-Agent': User_Agent}
        response = requests.get(base_api_url, headers=headers)
        if 'Erreur 503' in response.content:
            xml += "<dir>"\
                   "    <title>[B]System down for maintenance[/B]</title>"\
                   "    <meta>"\
                   "        <summary>System down for maintenance</summary>"\
                   "    </meta>"\
                   "    <heading></heading>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "</dir>" % (addon_icon)
        else:
            response = response.json(strict=False)
            # xbmcgui.Dialog().textviewer('Whatevs', str(response))
            for a in response['LIVETV']:
                try:
                    name = a['category_name']
                    id = a['cid']
                    icon = base_ico_url % (a['category_image'])
                    xml += "<dir>"\
                           "    <title>%s</title>"\
                           "    <meta>"\
                           "        <summary>%s</summary>"\
                           "    </meta>"\
                           "    <swift>swiftcategory/%s</swift>"\
                           "    <thumbnail>%s</thumbnail>"\
                           "</dir>" % (name, name, id, icon)
                except Exception:
                    pass
    except Exception:
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='SwiftCat', args=["url"])
def get_swiftstreamz_category(url):
    pins = ""
    xml = ""
    url = url.replace('swiftcategory/', '')  # Strip our category tag off.
    try:
        url = base_cat_url % (url)
        headers = {'Authorization': 'Basic @Swift11#:@Swift11#', 'User-Agent': User_Agent}
        response = requests.get(url, headers=headers)
        if 'Erreur 503' in response.content:
            xml += "<dir>"\
                   "    <title>[B]System down for maintenance[/B]</title>"\
                   "    <meta>"\
                   "        <summary>System down for maintenance</summary>"\
                   "    </meta>"\
                   "    <heading></heading>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "</dir>" % (addon_icon)
        else:
            response = response.json(strict=False)
            for a in response['LIVETV']:
                if 'm3u8' not in a['channel_url'] and '2ts' not in a['channel_url']:
                    continue
                name = a['channel_title']
                url = a['channel_url']
                icon = base_ico_url % (a['channel_thumbnail'])
                desc = a['channel_desc']
                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <meta>"\
                       "        <summary>%s</summary>"\
                       "    </meta>"\
                       "    <swift>swiftplay/%s/%s</swift>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (name, desc, name, url, icon)
    except Exception:
        # xbmcgui.Dialog().textviewer('Whatevs', str(response))
        pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type(), pins)


@route(mode='SwiftPlay', args=["url"])
def get_swiftstreamz_play(url):
    url = url.replace('swiftplay/', '')  # Strip our category tag off.
    tmp = url.split('/', 1)
    title = tmp[0]
    url = tmp[1]
    try:
        repair = False
        response = requests.get(
            base_dta_url,
            headers={'Authorization': 'Basic U3dpZnRTdHJlYW16OkBTd2lmdFN0cmVhbXpA', 'User-Agent': User_Agent})
        data = response.json(strict=False)

        if data['DATA'][0]['HelloUrl'] in url \
                or data['DATA'][0]['HelloUrl1'] in url:
            auth_url = data['DATA'][0]['HelloLogin']
            auth_auth = tuple(data['DATA'][0]['PasswordHello'].split(':'))
        elif data['DATA'][0]['LiveTvUrl'] in url:
            auth_url = data['DATA'][0]['LiveTvLogin']
            auth_auth = tuple(data['DATA'][0]['PasswordLiveTv'].split(':'))
            repair = True
        elif data['DATA'][0]['nexgtvUrl'] in url:
            auth_url = data['DATA'][0]['nexgtvToken']
            auth_auth = tuple(data['DATA'][0]['nexgtvPass'].split(':'))
        else:
            auth_url = data['DATA'][0]['loginUrl']
            auth_auth = tuple(data['DATA'][0]['Password'].split(':'))
            repair = True

        r = requests.get(auth_url, headers={'User-Agent': User_Agent}, auth=auth_auth, timeout=10)
        auth_token = r.text.partition('=')[2]

        if repair:
            auth_token = ''.join(
                [auth_token[: -59],
                 auth_token[-58: -47],
                 auth_token[-46: -35],
                 auth_token[-34: -23],
                 auth_token[-22: -11],
                 auth_token[-10:]])

        if 'playlist.m3u8' in url or '.2ts' in url:
            url = url + '?wmsAuthSign=' + auth_token + '|User-Agent=123456'
            item = xbmcgui.ListItem(label=title, path=url, iconImage=addon_icon, thumbnailImage=addon_icon)
            item.setInfo(type="Video", infoLabels={"Title": title})
            import resolveurl
            koding.Play_Video(url, showbusy=False, ignore_dp=True, item=item, resolver=resolveurl)
            # xbmc.executebuiltin("PlayMedia(%s)" % url)
        else:
            url = url + '|User-Agent=123456'
            item = xbmcgui.ListItem(label=title, path=url, iconImage=addon_icon, thumbnailImage=addon_icon)
            item.setInfo(type="Video", infoLabels={"Title": title})
            import resolveurl
            koding.Play_Video(url, showbusy=False, ignore_dp=True, item=item, resolver=resolveurl)
            # xbmc.executebuiltin("PlayMedia(%s)" % url)
    except Exception:
        xbmcgui.Dialog().ok('Stream', 'Unable to play stream')
