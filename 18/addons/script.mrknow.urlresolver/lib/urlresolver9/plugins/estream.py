"""
    OVERALL CREDIT TO:
        t0mm0, Eldorado, VOINAGE, BSTRDMKR, tknorris, smokdpi, TheHighway

    urlresolver XBMC Addon
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


from lib import helpers
from urlresolver9 import common
from urlresolver9.resolver import UrlResolver, ResolverError
from lib import jsunpack
import re

class EstreamResolver(UrlResolver):
    name = "estream"
    domains = ['estream.to']
    pattern = '(?://|\.)(estream\.to)/(?:embed-)?([a-zA-Z0-9]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        response = self.net.http_GET(web_url)
        html = response.content
        file_id = re.findall("'file_id', '(\d+)',", html)[0]
        headers = {'X-Requested-With': "XMLHttpRequest", 'Referer': web_url}

        if html:
            video_url = None
            js = html

            packed = re.search('(eval\(function.*?)\s*</script>', html, re.DOTALL)
            if packed:
                js1 = jsunpack.unpack(packed.group(1))
            else:
                js1 = html

            video_url = None

            link = re.search("(/dl\?op=view&file_code=[^']+)", js1)
            if link:
                #$.cookie('file_id', '1675923', {expires: 10});

                headers['Cookie'] = {'file_id':file_id}
                response = self.net.http_GET('https://%s%s'% (host,link.group(1)) , headers=headers).content

                common.log_utils.log_debug('to Link Found: %s' % video_url)
            headers = {'Referer': web_url}

            if video_url == None:
                link = re.search('(http[^"]*.mp4)', js)
                if link:
                    video_url = link.group(1)
                    common.log_utils.log_debug('watchers.to Link Found: %s' % video_url)

            if video_url != None:
                return video_url+ helpers.append_headers(headers)
            else:
                raise ResolverError('No playable video found.')


        return helpers.get_media_url(self.get_url(host, media_id)) + helpers.append_headers(headers)

    def get_url(self, host, media_id):
        return 'https://estream.to/%s.html' % media_id
        return self._default_get_url(host, media_id)
