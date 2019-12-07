# -*- coding: utf-8 -*-
"""
openload.io urlresolver plugin
Copyright (C) 2015 tknorris

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import requests,re
from resolveurl.resolver import ResolveUrl, ResolverError

class FileOneResolver(ResolveUrl):
    name = 'fileone'
    domains = ['fileone.tv']
    pattern = '(?:\/\/|\.)(fileone\.tv)\/(?:e\/|v\/)?([a-zA-Z0-9].*)'

    def get_media_url(self, host, media_id):
        url = self.get_url(host, media_id)
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        content = requests.get(url)
        test = content.content
        test = re.search('file: \'(.*)\'',test)
        test = test.group(1).replace(' ', '%20')
        return test + "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0&Referer=%s" % url

    def get_url(self, host, media_id):
        test = self._default_get_url(host, media_id, template='http://fileone.tv/v/{media_id}')
        return test