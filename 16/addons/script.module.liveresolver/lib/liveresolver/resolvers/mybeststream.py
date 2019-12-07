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
from liveresolver.modules import client,decryptionUtils,constants
from liveresolver.modules.log_utils import log 


def resolve(url):
    #try:
        referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        page = url.replace(referer, '').replace('&referer=', '').replace('referer=', '')

        result = client.request(page, referer=referer)
        result = decryptionUtils.doDemystify(result)
        token = re.findall(r'(\["\\x.+?[^\]]+\])',result)[0]
        token = eval(token)[1]
        rtmp = re.findall('.*(?:file|streamer|hestia):\s*["\']([^\'"]+).*',result)[0]
        url = rtmp + ' swfUrl=http://mybeststream.xyz/YjFlMTI0MT/jwplayer.flash.swf token=' + token + ' flashver=' + constants.flash_ver() + ' live=1 timeout=15 swfVfy=1 pageUrl=' + page
        return url
    #except:
    #   return

