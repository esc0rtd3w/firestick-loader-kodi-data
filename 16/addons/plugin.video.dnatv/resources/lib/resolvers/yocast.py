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
        referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]

        page = urlparse.parse_qs(urlparse.urlparse(url).query)['live'][0]
        page = 'http://www.yocast.tv/embedcr.php?live=%s&vw=640&vh=360' % page

        result = client.request(page, referer=referer)

        streamer = re.compile('streamer\s*:\s*[\'|\"](.+?)[\'|\"]').findall(result)[0]

        file = re.compile('file\s*:\s*[\'|\"](.+?)[\'|\"]').findall(result)[0]
        file = file.rsplit('.', 1)[0]

        url = '%s playpath=%s pageUrl=%s swfUrl=http://www.yocast.tv/myplayer/jwplayer.flash.swf live=1 timeout=15' % (streamer, file, page)

        return url
    except:
        return


