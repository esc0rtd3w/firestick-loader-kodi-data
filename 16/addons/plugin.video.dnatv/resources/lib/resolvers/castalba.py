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


import re,urlparse
from resources.lib.libraries import client


def resolve(url):
    try:
        try: page = re.compile('//.+?/(?:channel)/([0-9a-zA-Z-_]+)').findall(url)[0]
        except: pass
        try: page = urlparse.parse_qs(urlparse.urlparse(url).query)['cid'][0]
        except: pass

        page = 'http://castalba.tv/channel/%s' % page

        result = client.request(page, referer='http://castalba.tv', close=False)

        m3u8 = re.compile("'(http.+?\.m3u.+?)'").findall(result)
        m3u8 = [i for i in m3u8 if '.m3u8' in i]
        if len(m3u8) > 0: return m3u8[0]

        strm = re.compile("'streamer'\s*:\s*'(.+?)'").findall(result)[0]
        file = re.compile("'file'\s*:\s*'(.+?)'").findall(result)[0]
        swf = re.compile("'flashplayer'\s*:\s*\"(.+?)\"").findall(result)[0]

        url = '%s playpath=%s swfUrl=%s pageUrl=%s swfVfy=1 live=1 timeout=20' % (strm, file, swf, page)
        return url
    except:
        return


