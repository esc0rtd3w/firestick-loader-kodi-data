# -*- coding: utf-8 -*-
#
# Copyright (C) 2016,2017 RACC
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

import sys
import time
import os
import warnings
import traceback

import requests
import requests_cache
import json
from datetime import timedelta
from base64 import urlsafe_b64encode
from binascii import a2b_hex
from hashlib import md5

try:
    from http.cookiejar import LWPCookieJar
except ImportError:
    from cookielib import LWPCookieJar
try:
    from urllib.parse import quote_from_bytes as orig_quote
except ImportError:
    from urllib import quote as orig_quote

warnings.filterwarnings("ignore")

addon = xbmcaddon.Addon()
plugin = Plugin()
plugin.name = addon.getAddonInfo("name")

USER_DATA_DIR = xbmc.translatePath(addon.getAddonInfo("profile")).decode("utf-8")  # !!
if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

COOKIE_FILE = os.path.join(USER_DATA_DIR, "lwp_cookies.dat")
CACHE_FILE = os.path.join(USER_DATA_DIR, "cache")
expire_after = timedelta(hours=2)

user_agent = "Mozilla/5.0 (Linux; Android 5.1.1; AFTT Build/LVY48F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36"
auth_url = a2b_hex("68747470733a2f2f6170692e6d6f6264726f2e746f2f7574696c732f61757468").decode("utf-8")
lb_url = a2b_hex("68747470733a2f2f6170692e6d6f6264726f2e746f2f7574696c732f6c6f616462616c616e636572").decode("utf-8")
list_url = a2b_hex("68747470733a2f2f6170692e6d6f6264726f2e746f2f73747265616d626f742f76342f73686f77").decode("utf-8")
app_signature = str(0xd43b3efa)  # 0x17cab638a 0x7007c21c 0xceed20e0

s = requests_cache.CachedSession(CACHE_FILE, allowable_methods="POST", expire_after=expire_after, old_data_on_error=True, ignored_parameters=["token"])
s.hooks = {"response": lambda r, *args, **kwargs: r.raise_for_status()}
s.headers.update({"User-Agent": user_agent})
s.cookies = LWPCookieJar(filename=COOKIE_FILE)
if os.path.isfile(COOKIE_FILE):
    s.cookies.load(ignore_discard=True, ignore_expires=True)

auth_token_time = int(addon.getSetting("auth_token_time") or "0")
auth_token = addon.getSetting("auth_token")

current_time = int(time.time())
if current_time - auth_token_time > 7200:
    with s.cache_disabled():
        r = s.post(auth_url, data={"signature": app_signature}, timeout=10)

    if r.content.strip():
        auth_token = r.json().get("token")
        addon.setSetting("auth_token_time", str(current_time))
        addon.setSetting("auth_token", auth_token)


def quote(s, safe=""):
    return orig_quote(s.encode("utf-8"), safe.encode("utf-8"))


def get_lb_media_url(relayer):
    data = {"referer": a2b_hex("6d6f6264726f2e6d65").decode("utf-8"), "token": auth_token}
    try:
        with s.cache_disabled():
            r = s.post(lb_url, data=data, timeout=10)
        lb_info = r.json()
    except Exception:
        lb_info = {}

    time_stamp = str(int(lb_info.get("epoch", time.time())) + int(relayer.get("expiration_time", "20400")))
    to_hash = "{password}{time_stamp}/{dir}/{playpath}".format(time_stamp=time_stamp, **relayer).encode("utf-8")
    out_hash = urlsafe_b64encode(md5(to_hash).digest()).rstrip(b"=").decode("utf-8")

    headers = [
        "Referer={0}".format(quote(lb_info.get("referer", a2b_hex("6d6f6264726f2e6d65").decode("utf-8")))),
        "User-Agent={0}".format(quote(user_agent)),
        "Cookie={0}".format(quote(lb_info.get("cookie", "token=null"))),
        a2b_hex("582d5265717565737465642d576974683d322e312e3132253230467265656d69756d").decode("utf-8"),
    ]

    url = "{0}://{1}/{2}/{3}/{4}/{5}".format(
        relayer.get("protocol", "http"),
        lb_info.get("server", relayer.get("server")),
        relayer.get("app", "live"),
        out_hash,
        time_stamp,
        relayer.get("playpath").replace(relayer.get("replace"), ""),
    )

    return "{url}|{headers}".format(url=url, headers="&".join(headers))


def get_lb_rtmfp_url(relayer):
    data = {"referer": a2b_hex("6d6f6264726f2e6d65").decode("utf-8"), "token": auth_token}
    try:
        with s.cache_disabled():
            r = s.post(lb_url, data=data, timeout=10)
        lb_info = r.json()
    except Exception:
        lb_info = {}

    return "rtmfp://{0}/{1} netgroup={2} fallbackUrl=rtmfp://{0}/{3}".format(
        lb_info.get("server", relayer.get("server")), relayer.get("playpath"), relayer.get("netgroup"), relayer.get("fallbackUrl")
    )


@plugin.route("/")
def root():
    categories = ["channels", "news", "sports", "music"]
    list_items = []
    for c in categories:
        li = ListItem(c)
        url = plugin.url_for(list_channels, cat=c)
        list_items.append((url, li, True))

    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/list_channels/<cat>")
def list_channels(cat=None):
    data = {"data": cat, "parental": "no", "languages": "all", "alphabetical": "no", "token": auth_token}
    r = s.post(list_url, data=data, timeout=10)

    list_ids = []
    list_items = []
    for ch in r.json():
        if "relayer" in ch:
            channel = json.loads(ch.get("relayer"))
            image = "{0}|User-Agent={1}".format(ch.get("img"), quote(user_agent))
            li = ListItem(ch.get("name"))
            if not addon.getSetting("rtmfp") == "true":
                li.setProperty("IsPlayable", "true")
            li.setInfo(type="Video", infoLabels={"Title": ch.get("name"), "mediatype": "video"})
            li.setArt({"thumb": image, "icon": image})
            # kodi 16/17
            try:
                li.setContentLookup(False)
            except AttributeError:
                # kodi 14/15
                pass
            url = plugin.url_for(play, cat=cat, _id=ch.get("_id"))
            if channel.get("protocol") == "http":
                if ch.get("_id") not in list_ids:
                    list_items.append((url, li, False))
                    list_ids.append(ch.get("_id"))
            if channel.get("protocol") == "rtmfp":
                if addon.getSetting("rtmfp") == "true":
                    if ch.get("_id") not in list_ids:
                        list_items.append((url, li, False))
                        list_ids.append(ch.get("_id"))

    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/play/<cat>/<_id>/play.pvr")
def play(cat, _id):
    channel = None
    data = {"data": cat, "parental": "no", "languages": "all", "alphabetical": "no", "token": auth_token}
    r = s.post(list_url, data=data, timeout=10)

    stream_list = [stream for stream in r.json() if stream["_id"] == _id]
    media_urls = {}
    for stream in stream_list:
        if "relayer" in stream:
            relayer = json.loads(stream.get("relayer"))
            label = stream.get("name")
            image = "{0}|User-Agent={1}".format(stream.get("img"), quote(user_agent))
            if relayer.get("protocol") == "http":
                media_urls[relayer.get("playpath")] = relayer
            elif relayer.get("protocol") == "rtmfp":
                if addon.getSetting("rtmfp") == "true":
                    media_urls[relayer.get("playpath")] = relayer

    keys = media_urls.keys()
    if len(keys) > 1:
        dialog = xbmcgui.Dialog()
        ret = dialog.select("Choose Stream", keys)
        relayer = media_urls[keys[ret]]
    else:
        relayer = media_urls[keys[0]]

    if relayer.get("protocol") == "http":
        media_url = get_lb_media_url(relayer)
    elif relayer.get("protocol") == "rtmfp":
        media_url = get_lb_rtmfp_url(relayer)

    if addon.getSetting("livestreamer") == "true" and relayer.get("protocol") == "http":
        serverPath = os.path.join(xbmc.translatePath(addon.getAddonInfo("path")), "livestreamerXBMCLocalProxy.py")
        runs = 0
        while not runs > 10:
            try:
                requests.get("http://127.0.0.1:19001/version")
                break
            except Exception:
                xbmc.executebuiltin("RunScript(" + serverPath + ")")
                runs += 1
                xbmc.sleep(600)

        livestreamer_url = "http://127.0.0.1:19001/livestreamer/" + urlsafe_b64encode("hls://" + media_url)
        li = ListItem(label, path=livestreamer_url)
        li.setArt({"thumb": image, "icon": image})
        li.setMimeType("video/x-mpegts")
    else:
        li = ListItem(label, path=media_url)
        li.setArt({"thumb": image, "icon": image})
        li.setMimeType("application/vnd.apple.mpegurl")

    # kodi 18
    try:
        li.setContentLookup(False)
    except AttributeError:
        # kodi 14/15
        pass

    if addon.getSetting("rtmfp") == "true":
        xbmc.Player().play(item=media_url)  # kodi 18 bug
    else:
        xbmcplugin.setResolvedUrl(plugin.handle, True, li)


if __name__ == "__main__":
    try:
        plugin.run(sys.argv)
        s.cookies.save(ignore_discard=True, ignore_expires=True)
        s.close()
    except requests.exceptions.RequestException as e:
        dialog = xbmcgui.Dialog()
        dialog.notification(plugin.name, str(e), xbmcgui.NOTIFICATION_ERROR)
        traceback.print_exc()
        xbmcplugin.endOfDirectory(plugin.handle, False)
