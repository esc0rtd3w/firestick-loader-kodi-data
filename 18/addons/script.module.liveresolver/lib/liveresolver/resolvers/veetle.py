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


import re,urlparse,json
from liveresolver.modules import client
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        url = url.replace('/true/default','')
        if 'index.php' in url:
            channel = url.split('/')[-1]
        else:
            channel = re.compile('[/v/|/view#|/widget#]([\w]+)').findall(url)[-1]

        url = 'http://veetle.com/v/1dd55aa6d332f4a120143c89d5898df8'
        result = client.request(url, mobile=True, output='geturl')
        ls = result.split('/')
        channel = ls[-2]
        session = ls[-1]
        url = 'http://veetle.com/index.php/hls/streamMbrFast/%s_%s/stream.m3u8'%(channel,session)
        return url
    except:
        return

