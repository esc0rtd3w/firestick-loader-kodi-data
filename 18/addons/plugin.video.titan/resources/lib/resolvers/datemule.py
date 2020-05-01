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
from resources.lib.libraries import cloudflare
from resources.lib.libraries import client


def resolve(url):
    try:
        headers = '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': url})

        result = cloudflare.request(url, mobile=True)

        result = re.compile('file *: *"(http.+?)"').findall(result)

        result = [(i, urlparse.urlparse(i).path) for i in result]
        result = [i for i in result if not i[1].endswith('.mpd')]

        url = [i for i in result if i[1].endswith('.m3u8')]
        url += [i for i in result if not i[1].endswith('.m3u8')]
        url = url[0][0] + headers

        return url
    except:
        return


