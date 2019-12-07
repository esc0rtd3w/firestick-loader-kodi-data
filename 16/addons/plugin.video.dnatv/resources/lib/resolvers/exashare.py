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


def resolve(url):
    try:
        headers = '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': url})

        video = url.replace('/embed-', '/')
        video = re.compile('//.+?/([\w]+)').findall(video)[0]

        url = 'http://exashare.com/embed-%s.html' % video

        result = client.request(url)

        netloc = client.parseDOM(result, 'iframe', ret='src')[0]
        netloc = urlparse.urlparse(netloc).netloc

        url = 'http://%s/embed-%s.html' % (netloc, video)

        result = client.request(url)

        url = re.compile('file *: *"(http.+?)"').findall(result)[-1]
        url += headers
        return url
    except:
        return


