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


import re,urllib,urlparse
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        headers = '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': url})

        url = urlparse.urlparse(url).query
        url = urlparse.parse_qsl(url)[0][1]
        url = 'http://videomega.tv/cdn.php?ref=%s' % url

        result = client.request(url)

        unpacked = ''
        packed = result.split('\n')
        for i in packed: 
            try: unpacked += jsunpack.unpack(i)
            except: unpacked += i
        result = unpacked
        result = re.sub('\s\s+', ' ', result)

        url = re.compile('"video".+?"src"\s*\,\s*"(.+?)"').findall(result)
        url += client.parseDOM(result, 'source', ret='src', attrs = {'type': 'video.+?'})
        url = url[0] + headers

        return url
    except:
        return


