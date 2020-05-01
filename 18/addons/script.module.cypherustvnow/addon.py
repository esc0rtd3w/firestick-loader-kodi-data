# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 RACC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from xbmcgui import ListItem
from routing import Plugin

import requests
import urllib
import time
import json
import io
import os
import string
import random
import datetime
import uuid
from hashlib import md5
from base64 import b64encode,b64decode
from itertools import chain

addon = xbmcaddon.Addon()
plugin = Plugin()
plugin.name = addon.getAddonInfo('name')

#plugin conf
USER_DATA_DIR = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
ADDON_DATA_DIR = xbmc.translatePath(addon.getAddonInfo('path')).decode('utf-8')
RESOURCES_DIR = os.path.join(ADDON_DATA_DIR, 'resources')
amf_request_file = os.path.join(RESOURCES_DIR, 'request.amf')
channel_list_file = os.path.join(USER_DATA_DIR, 'channels.json')
app_config_file = os.path.join(USER_DATA_DIR, 'config.json')
implemented = ['0', '29', '32', '33', '38', '44', '48']

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

#apk secrets
user_agent = 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)'
device_name = 'Fire TV'
package_name = 'com.streams.androidnettv'
version_sub = '30'
version = '4.6 ({0})'.format(version_sub)
apk_cert_sha1 = 'EA:32:78:87:BF:88:8F:AD:C9:88:81:09:9A:31:69:F7:BE:E9:91:CE'
kinvey_app_id = 'kid_rkUF38Fbz'
kinvey_app_secret = '5fef3dcf83b74eaba14d87f1fe15747b'
user = 'EtSBR38Y'
passwd = 'c63Chg986t'

kinvey_login_url = 'https://baas.kinvey.com/user/{0}/login'.format(kinvey_app_id)
kinvey_config_url = 'https://baas.kinvey.com/appdata/{0}/AppConfigCharlie'.format(kinvey_app_id)

adduser_url = 'http://195.154.26.54:8080/data/i/adduserinfo.nettv/'
list_url = 'http://195.154.26.54:8080/data/i/data.nettv/'


def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

_reset = addon.getSetting('reset') or '0'
if int(_reset) < int(version_sub):
    addon.setSetting('user_id', '')
    addon.setSetting('kinvey_auth', '')
    addon.setSetting('kinvey_user', '')
    addon.setSetting('data_time', '')
    addon.setSetting('android_id', '')
    addon.setSetting('reset', version_sub)

android_id = addon.getSetting('android_id')
if not android_id:
    android_id = id_generator()
    addon.setSetting('android_id', android_id)


def kinvey_login():
    body = json.dumps({'username':user, 'password':passwd})
    r = requests.post(kinvey_login_url, data=body, headers = {'User-Agent': user_agent, 'Content-Type':'application/json'}, auth=(kinvey_app_id, kinvey_app_secret))
    kinvey_login_response = r.json()
    kinvey_user = kinvey_login_response.get('_id')
    kinvey_auth = kinvey_login_response['_kmd'].get('authtoken')
    addon.setSetting('kinvey_user', kinvey_user)
    addon.setSetting('kinvey_auth', kinvey_auth)
    return kinvey_auth


def kinvey_get_config():
    kinvey_auth = kinvey_login()
    r = requests.get(kinvey_config_url, headers = {'User-Agent': user_agent,
                                                   'Authorization': 'Kinvey {0}'.format(kinvey_auth),
                                                   'Content-Type':'application/json'})

    config = r.json()[0]
    with io.open(app_config_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(config, indent=2, sort_keys=True, ensure_ascii=False))
    return config


def backendless_get_config():
    from pyamf import remoting
    _url = 'https://api.backendless.com/762F7A10-3072-016F-FF64-33280EE6EC00/E9A27666-CD62-10CD-FF05-ED45B12ABE00/binary'
    headers = {'User-Agent': user_agent,
               'Content-Type':'application/x-amf'}

    with io.open(amf_request_file, 'rb') as f:
        r = requests.post(_url, headers = headers, data=f)

    dec = remoting.decode(r.content)

    config = dict(dec['null'].body.body)

    with io.open(app_config_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(config, default=lambda obj: obj.strftime('%H:%M:%S'), indent=2, sort_keys=True, ensure_ascii=False))

    return config


def get_channel_list(config):
    if config.get('_acl'):
        provider = '1'
    else:
        provider = '2'
    login_index_php = b64decode(config.get('YXBpS2V5TGluazAw')[1:])
    referer = b64decode(config.get('SXNpc2VrZWxvX3Nlc2lzdGltdV95ZXppbm9tYm9sbzAw')[1:])
    auth = b64decode(config.get('amFnX3Ryb3JfYXR0X2Vu')[1:])
    time_stamp = str(int(time.time() * 1000))
    allow = b64encode(bytes('{time_md5}${package_name}${apk_cert_sha1}${time_stamp}$${provider}'.format(
                      time_md5=md5(bytes(time_stamp)).hexdigest(),
                      package_name=package_name,
                      apk_cert_sha1=apk_cert_sha1,
                      time_stamp=time_stamp,
                      provider=provider)))

    data = {'ALLOW': allow}
    r = requests.post(login_index_php, headers = {'User-Agent': user_agent}, data=data)
    funguo = r.json().get('funguo')
    meta = r.headers['etag'].split(':')[0]


    user_id = addon.getSetting('user_id')
    if not user_id:
        user_id = get_user_id(config, funguo)

    time_stamp = str(int(time.time() * 1000))

    data = {'provider': provider,
            'time': time_stamp,
            'user_id': user_id,
            'check': '11', # ????
            'key': funguo,
            'version': version_sub
            }

    r = requests.post(list_url, headers = {'User-Agent': user_agent, 'Referer': referer, 'Meta': meta, 'Authorization': auth}, data=data)
    channel_list = r.json()

    with io.open(channel_list_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(channel_list, indent=2, sort_keys=True, ensure_ascii=False))

    return channel_list


def get_user_id(config, funguo):
    if config.get('_acl'):
        provider = '1'
    else:
        provider = '2'
    referer = b64decode(config.get('SXNpc2VrZWxvX3Nlc2lzdGltdV95ZXppbm9tYm9sbzAw')[1:])
    auth = b64decode(config.get('amFnX3Ryb3JfYXR0X2Vu')[1:])
    if provider == '1':
        kinvey_auth = addon.getSetting('kinvey_auth')
        kinvey_user = addon.getSetting('kinvey_user')
    elif provider == '2':
        kinvey_user = ''
        addon.setSetting('kinvey_user', kinvey_user)
        _new_id = uuid.uuid4()
        kinvey_auth = '{0}.{1}'.format(str(_new_id), _new_id.hex)
        addon.setSetting('kinvey_auth', kinvey_auth)

    kinvey_pass = kinvey_auth.split('.')[0]
    time_stamp = str(int(time.time() * 1000))

    _string2 = b'|'.join([b'19',
                        b64encode(version_sub.encode()),
                        b64encode(time_stamp.encode()),
                        b64encode('000000000000000'.encode()),
                        b64encode(kinvey_pass.encode()) ])

    _id = b'|'.join([md5(time_stamp.encode()).hexdigest().encode(),
                b64encode(package_name.encode()),
                b64encode(apk_cert_sha1.encode()),
                b64encode(device_name.encode()),
                b64encode(_string2) ] )

    data = {'id': b64encode(_id),
            'api_level': '19',
            'android_id': android_id,
            'time': time_stamp,
            'device_name': device_name,
            'kinvey': kinvey_user,
            'provider': provider,
            'device_id': 'unknown',
            'key': funguo,
            'version': version }

    r = requests.post(adduser_url, headers = {'User-Agent': user_agent, 'Referer': referer, 'Authorization': auth}, data=data)
    user_id = r.json().get('user_id')
    addon.setSetting('user_id', user_id)
    return user_id


data_time = int(addon.getSetting('data_time') or '0')
cache_time = int(addon.getSetting('cache_time') or '0')

current_time = int(time.time())
if current_time - data_time > cache_time * 60 * 60:
    try:
        try:
            app_config = kinvey_get_config()
        except:
            app_config = backendless_get_config()

        channel_list = get_channel_list(app_config)
        addon.setSetting('data_time', str(int(time.time())))
    except:
        with io.open(channel_list_file, 'r', encoding='utf-8') as f:
            channel_list = json.loads(f.read())

        with io.open(app_config_file, 'r', encoding='utf-8') as f:
            app_config = json.loads(f.read())
else:
    with io.open(channel_list_file, 'r', encoding='utf-8') as f:
        channel_list = json.loads(f.read())

    with io.open(app_config_file, 'r', encoding='utf-8') as f:
        app_config = json.loads(f.read())


def quote(s):
    return urllib.quote(s.encode('utf-8'), str(''))


def unquote(s):
    return urllib.unquote(s).decode('utf-8')


def fix_auth_date(auth):
    now = datetime.datetime.utcnow()
    _in = list(auth)
    _in.pop(len(_in) +2 -3 -int(str(now.year)[:2]))
    _in.pop(len(_in) +3 -4 -int(str(now.year)[2:]))
    #java January = 0
    _in.pop(len(_in) +4 -5 -(now.month -1 +1 +10))
    _in.pop(len(_in) +5 -6 -now.day)

    return ''.join(_in)

# star sports
def get_auth_token_33(referer):
    wms_url = b64decode(app_config.get('ZmFtYW50YXJhbmFfdGF0aTAw')[1:])
    auth = b64decode(app_config.get('dGVydHRleWFj')[1:])
    mod_value = int(b64decode(app_config.get('TW9vbl9oaWsx')[1:]))
    modified = lambda value: ''.join(chain(*zip(str(int(time.time()) ^ value),'0123456789')))
    fix_auth = lambda auth: ''.join([auth[:-56], auth[-55:-50], auth[-49:-42], auth[-41:-34], auth[-33:]])

    r = requests.get(wms_url, headers = {'User-Agent': user_agent, 'Referer': referer, 'Modified': modified(mod_value), 'Authorization': auth} )
    return fix_auth(r.text)


# eurosport
def get_auth_token_38(referer):
    wms_url = b64decode(app_config.get('YmVsZ2lfMzgw')[1:])
    auth = b64decode(app_config.get('Z2Vsb29mc2JyaWVm')[1:])
    mod_value = int(b64decode(app_config.get('TW9vbl9oaWsx')[1:]))
    modified = lambda value: ''.join(chain(*zip(str(int(time.time()) ^ value),'0123456789')))
    fix_auth = lambda auth: ''.join([auth[:-66], auth[-65:-56], auth[-55:-46], auth[-45:-36], auth[-35:]])

    r = requests.get(wms_url, headers = {'User-Agent': user_agent, 'Referer': referer, 'Modified': modified(mod_value), 'Authorization': auth} )
    return fix_auth(r.text)

# ane
def get_auth_token_44():
    wms_url = b64decode(app_config.get('YmVsa2lpdW1uXzk2')[1:])
    auth = b64decode(app_config.get('dGVydHRleWFj')[1:])
    mod_value = int(b64decode(app_config.get('TW9vbl9oaWsx')[1:]))
    modified = lambda value: ''.join(chain(*zip(str(int(time.time()) ^ value),'0123456789')))

    r = requests.get(wms_url, headers = {'User-Agent': user_agent, 'Modified': modified(mod_value), 'Authorization': auth} )
    return fix_auth_date(r.text)


# bt sports 1
def get_auth_token_48(referer):
    wms_url = b64decode(app_config.get('Ym9ya3lsd3VyXzQ4')[1:])
    auth = b64decode(app_config.get('dGVydHRleWFj')[1:])
    mod_value = int(b64decode(app_config.get('TW9vbl9oaWsx')[1:]))
    modified = lambda value: ''.join(chain(*zip(str(int(time.time()) ^ value),'0123456789')))

    r = requests.get(wms_url, headers = {'User-Agent': user_agent, 'Referer': referer, 'Modified': modified(mod_value), 'Authorization': auth} )
    return fix_auth_date(r.text)

#bein 1
def get_stream_32(stream):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    api_url = b64decode(app_config.get('dWt1c3VzYV91a3ViaGFsYV9iYXRlczAw')[1:])
    auth = b64decode(app_config.get('amFnX3Ryb3JfYXR0X2Vu')[1:])
    mod_value = int(b64decode(app_config.get('TW9vbl9oaWsx')[1:]))
    modified = lambda value: ''.join(chain(*zip(str(int(time.time()) ^ value),'0123456789')))

    response_body_api_url = b64decode(app_config.get('bWFya2llcmlzX2J0aXMw')[1:])
    response_body_auth = b64decode(app_config.get('bXdlbnRlcnR5')[1:])
    r = requests.get(response_body_api_url, headers = {'User-Agent': user_agent, 'Authorization': auth} )
    response_body = r.text

    data = { 'data': json.dumps({'token': 32,
                                 'response_body': response_body,
                                 'stream_url': stream})  }

    r = requests.post(api_url, headers = {'User-Agent': user_agent, 'Modified': modified(mod_value), 'Authorization': auth}, data = data )
    return r.json().get('stream_url')


# bt sports 1
def get_stream_29(stream):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    api_url = b64decode(app_config.get('Y2hlaWxlYWRoIF9DZWFuZ2FsX29udGlz')[1:])
    auth = b64decode(app_config.get('amFnX3Ryb3JfYXR0X2Vu')[1:])
    mod_value = int(b64decode(app_config.get('TW9vbl9oaWsx')[1:]))
    modified = lambda value: ''.join(chain(*zip(str(int(time.time()) ^ value),'0123456789')))

    data = { 'data': json.dumps({'token': 29,
                                 'response_body': 'f',
                                 'stream_url': stream})  }

    r = requests.post(api_url, headers = {'User-Agent': user_agent, 'Modified': modified(mod_value), 'Authorization': auth}, data = data )
    return r.json().get('stream_url')


@plugin.route('/')
def root():
    categories = channel_list.get("categories_list")
    list_items = []
    for c in categories:
        li = ListItem(c.get("cat_name"))
        url = plugin.url_for(list_channels, cat=c.get("cat_id"))
        list_items.append((url, li, True))

    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_FULLPATH)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/list_channels/<cat>')
def list_channels(cat=None):
    list_items = []
    for channel in channel_list.get("eY2hhbm5lbHNfbGlzdA=="):
        if channel.get("cat_id") == cat:
            if len([stream for stream in channel.get("Qc3RyZWFtX2xpc3Q=") if b64decode(stream.get("AdG9rZW4=")[:-1]) in implemented]) == 0:
                continue

            title = b64decode(channel.get("ZY19uYW1l")[:-1])
            icon = b64decode(channel.get("abG9nb191cmw=")[1:])
            image = "{0}|User-Agent={1}".format(icon, quote(user_agent))
            c_id = channel.get("rY19pZA==")

            li = ListItem(title)
            li.setProperty("IsPlayable", "true")
            li.setInfo(type='Video', infoLabels={'Title': title, 'mediatype': 'video', 'playcount': 0})
            li.setArt({'thumb': image, 'icon': image})
            try:
                li.setContentLookup(False)
            except:
                pass
            url = plugin.url_for(play, c_id=c_id)
            list_items.append((url, li, False))



    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/play/<c_id>')
def play(c_id):
    for channel in channel_list.get("eY2hhbm5lbHNfbGlzdA=="):
        if channel.get("rY19pZA==") == c_id:
            selected_channel = channel
            break

    #stream_list = selected_channel.get("Qc3RyZWFtX2xpc3Q=")
    stream_list = [stream for stream in selected_channel.get("Qc3RyZWFtX2xpc3Q=") if b64decode(stream.get("AdG9rZW4=")[:-1]) in implemented]
    if len(stream_list) > 1:
        select_list= []
        for stream in stream_list:
            select_list.append(b64decode(stream.get("Bc3RyZWFtX3VybA==")[1:]))

        dialog = xbmcgui.Dialog()
        ret = dialog.select('Choose Stream', select_list)
        selected_stream = stream_list[ret]
    else:
        selected_stream = stream_list[0]


    if "AdG9rZW4=" in selected_stream:
        if b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "33":
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]) + get_auth_token_33(selected_stream.get("referer"))
        elif b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "38":
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]) + get_auth_token_38(selected_stream.get("referer"))
        elif b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "44":
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]) + get_auth_token_44()
        elif b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "48":
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]) + get_auth_token_48(selected_stream.get("referer"))
        elif b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "32":
            media_url = get_stream_32(b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]))
        elif b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "29":
            media_url = get_stream_29(b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]))
        elif b64decode(selected_stream.get("AdG9rZW4=")[:-1]) == "0":
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:])
        else:
            media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:]) + b64decode(selected_stream.get("AdG9rZW4=")[:-1])
    else:
        media_url = b64decode(selected_stream.get("Bc3RyZWFtX3VybA==")[1:])

    if selected_stream.get("player_user_agent", user_agent) == None \
    or selected_stream.get("player_user_agent", user_agent) == 'null':
        selected_stream["player_user_agent"] = user_agent

    media_url = "{0}|User-Agent={1}".format(media_url, quote(selected_stream.get("player_user_agent", user_agent)))

    title = b64decode(selected_channel.get("ZY19uYW1l")[:-1])
    icon = b64decode(selected_channel.get("abG9nb191cmw=")[1:])
    image = "{0}|User-Agent={1}".format(icon, quote(user_agent))


    if 'playlist.m3u8' in media_url:
        if addon.getSetting('inputstream') == 'true':
            li = ListItem(title, path=media_url)
            li.setArt({'thumb': image, 'icon': image})
            li.setMimeType('application/vnd.apple.mpegurl')
            li.setProperty('inputstreamaddon', 'inputstream.adaptive')
            li.setProperty('inputstream.adaptive.manifest_type', 'hls')
            li.setProperty('inputstream.adaptive.stream_headers', media_url.split('|')[-1])
        elif addon.getSetting('livestreamer') == 'true':
            serverPath = os.path.join(xbmc.translatePath(addon.getAddonInfo('path')), 'livestreamerXBMCLocalProxy.py')
            runs = 0
            while not runs > 10:
                try:
                    requests.get('http://127.0.0.1:19001/version')
                    break
                except:
                    xbmc.executebuiltin('RunScript(' + serverPath + ')')
                    runs += 1
                    xbmc.sleep(600)
            livestreamer_url = 'http://127.0.0.1:19001/livestreamer/'+b64encode('hlsvariant://'+media_url)
            li = ListItem(title, path=livestreamer_url)
            li.setArt({'thumb': image, 'icon': image})
            li.setMimeType('video/x-mpegts')
        else:
            li = ListItem(title, path=media_url)
            li.setArt({'thumb': image, 'icon': image})
            li.setMimeType('application/vnd.apple.mpegurl')
            try:
                li.setContentLookup(False)
            except:
                pass
    else:
        li = ListItem(title, path=media_url)
        li.setArt({'thumb': image, 'icon': image})

    xbmcplugin.setResolvedUrl(plugin.handle, True, li)

if __name__ == '__main__':
    try:
        plugin.run()
    except requests.exceptions.RequestException:
        dialog = xbmcgui.Dialog()
        dialog.notification(plugin.name, "Web Request Exception", xbmcgui.NOTIFICATION_ERROR)
        traceback.print_exc()
