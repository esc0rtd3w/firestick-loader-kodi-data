# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

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
'''


import re,urllib,urlparse,base64
from resources.lib.libraries import client


def resolve(url):
    try:
        referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]

        page = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]
        page = 'http://p2pcast.tv/stream.php?id=%s&live=0&p2p=0&stretching=uniform' % page

        result = client.request(page, referer=referer)

        js = re.compile('src\s*=\s*[\'|\"](.+?player.+?\.js)[\'|\"]').findall(result)[-1]
        js = client.request(js)

        try:
            token = re.findall('[\'|\"](.+?\.php)[\'|\"]',js)[-1]
            token = urlparse.urljoin('http://p2pcast.tv', token)
            token = client.request(token, referer=page, headers={'User-Agent': client.agent(), 'X-Requested-With': 'XMLHttpRequest'})
            token = re.compile('[\'|\"]token[\'|\"]\s*:\s*[\'|\"](.+?)[\'|\"]').findall(token)[0]
        except:
            token = ''


        try:
            swf = re.compile('flashplayer\s*:\s*[\'|\"](.+?)[\'|\"]').findall(js)[-1]
        except:
            swf = 'http://cdn.p2pcast.tv/jwplayer.flash.swf'


        url = re.compile('url\s*=\s*[\'|\"](.+?)[\'|\"]').findall(result)[0]
        url = base64.b64decode(url) + token
        url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': swf})

        return url
    except:
        return


