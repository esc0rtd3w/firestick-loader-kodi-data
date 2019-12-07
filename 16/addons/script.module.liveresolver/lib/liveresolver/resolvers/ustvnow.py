# -*- coding: utf-8 -*-


import urllib,urlparse,json
from liveresolver.modules import client
from liveresolver.modules import control
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        addonid = 'script.module.liveresolver'

        user, password = control.setting('ustvnow_email'), control.setting('ustvnow_pass')
        if (user == '' or password == ''):
            user, password = control.addon(addonid).getSetting('ustvnow_email'), control.addon(addonid).getSetting('ustvnow_pass')
        if (user == '' or password == ''): return ''

        token = urllib.urlencode({'username': user, 'password': password})
        token = 'http://m-api.ustvnow.com/gtv/1/live/login?%s&device=gtv&redir=0' % token
        token = json.loads(client.request(token))['token']

        result = 'http://m-api.ustvnow.com/gtv/1/live/playingnow?token=%s' % token
        result = json.loads(client.request(result))

        try:
            scode = urlparse.parse_qs(urlparse.urlparse(url).query)['scode'][0]
        except:
            stream_code = urlparse.parse_qs(urlparse.urlparse(url).query)['stream_code'][0]
            scode = [i['scode'] for i in result['results'] if i['stream_code'] == stream_code][0]

        key = (result['globalparams']['passkey']).replace('key=', '')

        url = 'http://m-api.ustvnow.com/stream/1/live/view?token=%s&key=%s&scode=%s' % (token, key, scode)
        url = json.loads(client.request(url))['stream']

        return url
    except:
        return ''

