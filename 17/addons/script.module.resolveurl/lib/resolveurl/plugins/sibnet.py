"""
    vshare resolver for ResolveURL
    Copyright (C) 2018 holisticdioxide

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

import re
from lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError
from lib import jsunpack, helpers

class SibnetResolver(ResolveUrl):
    name = "sibnet"
    domains = ['sibnet.ru']
    pattern = '(?:\/\/|\.)(sibnet\.(?:ru|co))\/shell\.php\?videoid=([0-9a-zA-Z\/]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = "http://video.sibnet.ru/shell_config_xml.php?videoid=%s&partner=null&playlist_position=null&playlist_size=0&related_albid=0&related_tagid=0&related_ids=null&repeat=null&nocache" % (media_id)
        headers = {'User-Agent': """"Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; androVM for VirtualBox ('Tablet' version with phone caps) Build/JRO03S) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30""",
                   'Referer': web_url}
        html = self.net.http_GET(web_url, headers=headers).content
        video = re.findall("""(https:\/\/video\.sibnet\.ru\/v\/.*.mp4)""", html)[0]
        return video + helpers.append_headers(headers)

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://video.{host}/video{media_id}')
