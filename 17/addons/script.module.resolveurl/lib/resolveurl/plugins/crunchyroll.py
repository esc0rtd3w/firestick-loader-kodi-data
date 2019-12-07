"""
    OVERALL CREDIT TO:
        t0mm0, Eldorado, VOINAGE, BSTRDMKR, tknorris, smokdpi, TheHighway

    resolveurl XBMC Addon
    Copyright (C) 2011 t0mm0

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
"""
import re, json
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError

class crunchyrollResolver(ResolveUrl):
    name = "crunchyroll"
    domains = ['crunchyroll.com']
    pattern = '(?://|\.)(www\.crunchyroll\.com)/(.*)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        html = self.net.http_GET(web_url).content
        try:
            streams = json.loads(re.findall(""""streams":(\[.*?\])""", html)[0])
        except:
            raise ResolverError('File Not Found or removed')
        lang = re.findall('''vilos\.config\.player\.language = "(.*?)"''', html)[0]
        for item in streams:
            if item[u'hardsub_lang'] == lang:
                return item['url']
        raise ResolverError('File Not Found or removed')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/{media_id}')
