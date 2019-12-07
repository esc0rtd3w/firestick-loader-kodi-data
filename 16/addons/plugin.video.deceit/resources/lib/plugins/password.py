"""
    password.py --- Jen Plugin for protecting some sections with a password
    Copyright (C) 2018, Mister-X

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
		<title>THE NAME OF YOUR SECTION</title>
		<link>THE LINK OF YOUR XML</link>
		<password>get/BASE64 CODE</password>
		<thumbnail>THUMBNAIL</thumbnail>
	</dir>
"""

import urllib, urllib2, os, base64, xbmcplugin, xbmcgui, xbmcvfs, traceback, cookielib, xbmc, sys, base64
import pickle
import time
import re
import koding
import xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode


addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')


class PASSWORD(Plugin):
    name = "password"

    def process_item(self, item_xml):
        if "<password>" in item_xml:
			item = JenItem(item_xml)
			if "get/" in item.get("password", ""):
				result_item = {
					'label': item["title"],
					'icon': item.get("thumbnail", addon_icon),
					'fanart': item.get("fanart", addon_fanart),
					'mode': "showing",
					'url': item.get("link", "") + ' ' + item.get("password", ""),
					'folder': True,
					'content': "files",
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
				
		
@route(mode='showing', args=["url"])
def showing(url):
	xml = ''
	string = url.split()
	TheXml,TheCode = string[0],string[1]
	TheCode = TheCode.replace("get/","")
	TheCode = base64.b64decode(TheCode)
	input = ''
	keyboard = xbmc.Keyboard(input, '[COLOR red]So Your Wanting The Naughty Bits Are You ?? Get The Tissues At The Ready[/COLOR]')
	keyboard.doModal()
	if keyboard.isConfirmed():
		input = keyboard.getText()
	if input == TheCode: 
		listhtml = getHtml(TheXml)
		match = re.compile(
				'([^"]+)', 
				re.IGNORECASE | re.DOTALL).findall(listhtml)
		for xmlContent in match:
			xml += xmlContent
	else:
		xml += "<dir>"\
			   "<title>[COLOR yellow]Wrong Answer, Are you sure your old enough ??[/COLOR]</title>"\
			   "<thumbnail>https://nsx.np.dl.playstation.net/nsx/material/c/ce432e00ce97a461b9a8c01ce78538f4fa6610fe-1107562.png</thumbnail>"\
			   "</dir>"
	jenlist = JenList(xml)
	display_list(jenlist.get_list(), jenlist.get_content_type())



def getHtml(url, referer=None, hdr=None, data=None):
    USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}
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