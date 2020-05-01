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


import re,json
from resources.lib.libraries import client


def resolve(url):
    try:
        url = re.compile('//.+?/.+?/([\w]+)').findall(url)[0]
        url = 'http://ok.ru/dk?cmd=videoPlayerMetadata&mid=%s' % url
 
        result = client.request(url)
        result = re.sub(r'[^\x00-\x7F]+',' ', result)

        result = json.loads(result)['videos']

        try: hd = [{'quality': '1080p', 'url': i['url']} for i in result if i['name'] == 'full']
        except: pass
        try: hd += [{'quality': 'HD', 'url': i['url']} for i in result if i['name'] == 'hd']
        except: pass
        try: sd = [{'quality': 'SD', 'url': i['url']} for i in result if i['name'] == 'sd']
        except: pass
        try: sd += [{'quality': 'SD', 'url': i['url']} for i in result if i['name'] == 'low']
        except: pass
        try: sd += [{'quality': 'SD', 'url': i['url']} for i in result if i['name'] == 'lowest']
        except: pass
        try: sd += [{'quality': 'SD', 'url': i['url']} for i in result if i['name'] == 'mobile']
        except: pass

        url = hd + sd[:1]
        if not url == []: return url

    except:
        return


