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


import re,urlparse,base64
from resources.lib.libraries import client
from resources.lib.resolvers import openload


def resolve(url):
    try:
        try: quality = urlparse.parse_qs(urlparse.urlparse(url).query)['quality'][0]
        except: quality = '1080P'

        url = url.rsplit('?', 1)[0]

        result = client.request(url, close=False)

        url = client.parseDOM(result, 'div', attrs = {'class': 'player'})[0]
        url = client.parseDOM(url, 'iframe', ret='src')[0]

        result = client.request(url)

        url = client.parseDOM(result, 'iframe', ret='src')
        if len(url) > 0: return resolvers.request(url[0], debrid)

        result = re.compile("\('(.+?)'\)").findall(result)[0]
        result = base64.b64decode(result)

        result = re.compile('(\d*p)="([^"]+)"').findall(result)

        url = [i for i in result if i[0].upper() == quality]
        if len(url) > 0: url = url[0][1]
        else: url = result[0][1]

        return url
    except:
        return


