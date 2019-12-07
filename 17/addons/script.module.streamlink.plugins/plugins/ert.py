# -*- coding: utf-8 -*-

import re
import requests

from streamlink.plugin import Plugin
from streamlink.plugin.api import http, validate

YOUTUBE_URL = "https://www.youtube.com/watch?v={0}"
UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
html = requests.get('http://www.ipinfodb.com/my_ip_location.php', params={'User-Agent': UA}).text

if 'Greece' in html:
    _youtube_id = re.compile(r'GR.+?"https://www\.youtube\.com/embed/([\w-]+)\?', re.M | re.S)
else:
    _youtube_id = re.compile(r'else.+?"https://www\.youtube\.com/embed/([\w-]+)\?', re.M | re.S)

_url_re = re.compile(r'http(s)?://webtv\.ert\.gr/.*')

_youtube_url_schema = validate.Schema(
    validate.all(
        validate.transform(_youtube_id.search),
        validate.any(
            None,
            validate.all(
                validate.get(1),
                validate.text
            )
        )
    )
)


class Ert(Plugin):

    @classmethod
    def can_handle_url(cls, url):

        return _url_re.match(url)

    def _get_streams(self):

        channel_id = http.get(self.url, schema=_youtube_url_schema)

        if channel_id:
            return self.session.streams(YOUTUBE_URL.format(channel_id))


__plugin__ = Ert