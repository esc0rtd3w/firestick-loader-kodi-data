'''
    urlresolver XBMC Addon
    Copyright (C) 2016 Gujal

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
'''
import re
from urlresolver import common
from urlresolver.plugins.lib import helpers
from urlresolver.resolver import UrlResolver, ResolverError

class TubePornClassicResolver(UrlResolver):
    name = 'tubepornclassic'
    domains = ['tubepornclassic.com']
    pattern = '(?://|\.)(tubepornclassic\.com)/videos/(\d+/[^/\s]+)'
    
    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):  
        
        try:
            headers = {'User-Agent': common.RAND_UA}
            web_url = self.get_url(host, media_id)
            html = self.net.http_GET(web_url, headers=headers).content
            
            if html:
                sources = re.findall('''['"]file['"]:\s*['"](?P<label>[^'"]+)['"],\s*['"]type['"]:\s*['"](?P<url>[^'"]+)["']''', html, re.DOTALL)
                sources = [(i[1], i[0]) for i in sorted(sources)]
                return self.net.http_GET(helpers.pick_source(sources), headers=headers).get_url() + helpers.append_headers(headers)

            raise ResolverError('File not found')
        except:
            raise ResolverError('File not found')
    
    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://www.{host}/videos/{media_id}/')
        
    @classmethod
    def _is_enabled(cls):
        return True
