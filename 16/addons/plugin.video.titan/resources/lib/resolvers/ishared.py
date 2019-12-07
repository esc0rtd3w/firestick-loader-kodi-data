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


import re,urllib
from resources.lib.libraries import client
from resources.lib.libraries import jsunpack


def resolve(url):
    try:
        headers = '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': url})

        url = url.replace('/video/', '/embed/')

        result = client.request(url)

        unpacked = ''
        packed = result.split('\n')
        for i in packed: 
            try: unpacked += jsunpack.unpack(i)
            except: pass
        result += unpacked
        result = re.sub('\s\s+', ' ', result)

        var = re.compile('var\s(.+?)\s*=\s*\'(.+?)\'').findall(result)
        for i in range(100):
            for v in var: result = result.replace("' %s '" % v[0], v[1]).replace("'%s'" % v[0], v[1])

        url = re.compile('sources\s*:\s*\[.+?file\s*:\s*(.+?)\s*\,').findall(result)[0]
        var = re.compile('var\s+%s\s*=\s*\'(.+?)\'' % url).findall(result)
        if len(var) > 0: url = var[0].strip()
        url += headers

        if url.startswith('http'): return url 
    except:
        return


