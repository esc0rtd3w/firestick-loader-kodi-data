"""
    m3u.py --- Jen Plugin for accessing m3u data
    Copyright (C) 2018

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


    Usage Examples:
    <dir>
    <title>M3U NAME</title>
    <thumbnail></thumbnail>
    <m3u>M3U LINK</m3u>
    <fanart></fanart>
    <info> </info>
    </dir>
"""

import urllib2
import re
import xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list

CACHE_TIME = 86400  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')


class M3U(Plugin):
    name = "m3u"

    def process_item(self, item_xml):
        if "<m3u>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "m3u",
                'url': item.get("m3u", ""),
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
            result_item["properties"] = {'fanart_image': result_item["fanart"]}
            result_item['fanart_small'] = result_item["fanart"]
            return result_item


@route(mode='m3u', args=["url"])
def m3u(url):
    xml = ""
    if not xml:
        xml = ""
        if '.m3u' in url:
            listhtml = getHtml(url)
            match = re.compile('#EXTINF:.+?,(.+?)\n([^"]+)\n',
                               re.IGNORECASE | re.DOTALL).findall(listhtml)
            for name, url in match:
                name = name
                url = url
                xml += "<item>"\
                       "<title>%s</title>"\
                       "<link>%s</link>"\
                       "<thumbnail></thumbnail>"\
                       "</item>" % (name, url)
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


def getHtml(url, referer=None, hdr=None, data=None):
    """GRAB HTML FROM THE LINK"""
    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    headers = {
        'User-Agent': USER_AGENT,
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    if not hdr:
        req = urllib2.Request(url, data, headers)
    else:
        req = urllib2.Request(url, data, hdr)
    if referer:
        req.add_header('Referer', referer)
    response = urllib2.urlopen(req, timeout=60)
    data = response.read()
    response.close()
    return data
