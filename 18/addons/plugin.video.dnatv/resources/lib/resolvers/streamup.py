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
        url = (urlparse.urlparse(url).path).split('/')[1]
        url = 'https://streamup.com/%s/embeds/video' % url

        result = client.request(url)

        url = re.compile('"(.+?\.m3u8)"').findall(result)[0]
        url = url.rsplit('"', 1)[-1]

        channel = re.compile('channelName\s*:\s*"(.+?)"').findall(result)[0]
        channel = [i for i in url.split('/') if channel in i][0]

        streamer = re.compile('url\s*:\s*"(.+?)"').findall(result)[0]
        streamer += channel
        streamer = client.request(streamer)

        url = 'http://%s/%s' % (streamer, url)
        url = urlparse.urljoin(url, urlparse.urlparse(url).path.replace('//','/'))

        return url
    except:
       return


