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


def resolve(url):
    try:
        headers = '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': url})

        fid = url.replace('/embed-', '/')
        fid = re.compile('//.+?/([\w]+)').findall(fid)[0]

        url = 'http://vidce.tv/%s' % fid ; cookie = 'fid=%s' % fid

        result = client.request(url, cookie=cookie, close=False)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': '' })
        f += client.parseDOM(result, 'form', attrs = {'action': '' })
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post.update({'method_free': 'Proceed to File/Video'})
        post = urllib.urlencode(post)

        result = client.request(url, cookie=cookie, post=post, close=False)

        post = {}
        f = client.parseDOM(result, 'Form', attrs = {'action': '' })
        f += client.parseDOM(result, 'form', attrs = {'action': '' })
        k = client.parseDOM(f, 'input', ret='name', attrs = {'type': 'hidden'})
        for i in k: post.update({i: client.parseDOM(f, 'input', ret='value', attrs = {'name': i})[0]})
        post = urllib.urlencode(post)

        result = client.request(url, cookie=cookie, post=post)

        url = result.replace('\\', '')
        url = re.compile('(<a\s.+?</a>)').findall(url)
        url = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a')) for i in url]
        url = [i[0][0] for i in url if len(i[0]) > 0 and len(i[1]) > 0 and 'download.png' in i[1][0]][0]
        url += headers

        return url
    except:
        return


