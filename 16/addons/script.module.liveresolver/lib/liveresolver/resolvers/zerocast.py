# -*- coding: utf-8 -*-

'''
    Liveresolver Add-on
    Copyright (C) 2016 natko1412

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


import re,urlparse,base64, urllib,json
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = 'http://zerocast.tv/channels'
        if 'chan=' in url:
            result = client.request(url, referer=referer)
            url = re.findall('src=[\'"](.+?)[\'"]>', result)[-1]

        page = url
        r = re.findall('.+?a=([0-9]+)', url)[0]

        url = 'http://zerocast.tv/embed.php?a=%s&id=&width=640&height=480&autostart=true&strech=exactfit' % r


        result = client.request(url, referer=referer)
        unpacked = ''
        packed = result.split('\n')
        for i in packed:
            try:
                unpacked += jsunpack.unpack(i)
            except:
                pass
        result += unpacked
        js = re.findall('getJSON\([\"\'](http://zerocast.tv/file[^\"\']+)',result)[0]
        token = json.loads(client.request(js))['token']
        r = re.findall('curl\s*=\s*[\'"](.+?)[\'"]', result)
        r = r[0].decode('base64', 'strict')

        if '.m3u8' in r or 'rtmp' in r:
            url = r
            return url + ' swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf flashver=' + constants.flash_ver() + ' token=' + token + ' timeout=15 live=true swfVfy=1 pageUrl=' + page
    except:
        return


