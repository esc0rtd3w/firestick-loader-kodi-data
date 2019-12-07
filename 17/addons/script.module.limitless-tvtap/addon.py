# -*- coding: utf-8 -*-
#
# Copyright (C) 2016,2017,2018 RACC
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

import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
from xbmcgui import ListItem
from routing import Plugin

import os
import traceback
import requests
import requests_cache
from datetime import timedelta
from base64 import b64decode, urlsafe_b64encode
from pyDes import des, PAD_PKCS5

try:
    from urllib.parse import quote_from_bytes as orig_quote
except ImportError:
    from urllib import quote as orig_quote

addon = xbmcaddon.Addon()
plugin = Plugin()
plugin.name = addon.getAddonInfo("name")
user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)"
player_user_agent = "mediaPlayerhttp/2.4 (Linux;Android 5.1) ExoPlayerLib/2.6.1"
USER_DATA_DIR = xbmc.translatePath(addon.getAddonInfo("profile")).decode("utf-8")  # !!
CACHE_TIME = int(addon.getSetting("cache_time"))
CACHE_FILE = os.path.join(USER_DATA_DIR, "cache")
expire_after = timedelta(hours=CACHE_TIME)

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

s = requests_cache.CachedSession(CACHE_FILE, allowable_methods="POST", expire_after=expire_after, old_data_on_error=True)
s.hooks = {"response": lambda r, *args, **kwargs: r.raise_for_status()}
s.headers.update({"User-Agent": "USER-AGENT-tvtap-APP-V2"})
token_url = "http://tvtap.net/tvtap1/index_tvtappro.php?case=get_channel_link_with_token_tvtap_updated"
list_url = "http://tvtap.net/tvtap1/index_tvtappro.php?case=get_all_channels"


def quote(s, safe=""):
    return orig_quote(s.encode("utf-8"), safe.encode("utf-8"))


@plugin.route("/")
def root():
    list_items = []
    r = s.post(list_url, headers={"app-token": "9120163167c05aed85f30bf88495bd89"}, data={"username": "603803577"}, timeout=15)
    if "Could not connect" in r.content:
        s.cache.clear()
    ch = r.json()
    category_list = []
    for c in ch["msg"]["channels"]:
        category = '{0}'.format(c.get('cat_name'))
        if category not in category_list:
            category_list.append(category)
            li = ListItem(category)
            url = plugin.url_for(list_channels, cat_id=c.get('cat_id'))
            list_items.append((url, li, True))

    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/list_channels/<cat_id>")
def list_channels(cat_id=None):
    list_items = []
    r = s.post(list_url, headers={"app-token": "9120163167c05aed85f30bf88495bd89"}, data={"username": "603803577"}, timeout=15)
    if "Could not connect" in r.content:
        s.cache.clear()
    ch = r.json()

    for c in ch["msg"]["channels"]:
        if c["cat_id"] == cat_id:
            image = "http://tvtap.net/tvtap1/{0}|User-Agent={1}".format(quote(c.get("img"), "/"), quote(user_agent))
            title = '{0} - {1}'.format(c.get('country'),c.get('channel_name').rstrip('.,-'))
            li = ListItem(title)
            li.setProperty("IsPlayable", "true")
            li.setArt({"thumb": image, "icon": image})
            li.setInfo(type="Video", infoLabels={"Title": title, "mediatype": "video"})
            try:
                li.setContentLookup(False)
            except AttributeError:
                pass
            url = plugin.url_for(play, ch_id=c["pk_id"])
            list_items.append((url, li, False))

    xbmcplugin.addSortMethod(plugin.handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addDirectoryItems(plugin.handle, list_items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route("/play/<ch_id>/play.pvr")
def play(ch_id):
    # 178.132.6.54 81.171.8.162
    key = b"98221122"

    r = s.post(list_url, headers={"app-token": "9120163167c05aed85f30bf88495bd89"}, data={"username": "603803577"}, timeout=15)
    ch = r.json()
    for c in ch["msg"]["channels"]:
        if c["pk_id"] == ch_id:
            selected_channel = c
            break

    title = selected_channel.get("channel_name")
    image = "http://tvtap.net/tvtap1/{0}|User-Agent={1}".format(quote(c.get("img"), "/"), quote(user_agent))

    with s.cache_disabled():
        r = s.post(token_url, headers={"app-token": "9120163167c05aed85f30bf88495bd89"}, data={"channel_id": ch_id, "username": "603803577"}, timeout=15)

    links = []
    for stream in r.json()["msg"]["channel"][0].keys():
        if "stream" in stream or "chrome_cast" in stream:
            d = des(key)
            link = d.decrypt(b64decode(r.json()["msg"]["channel"][0][stream]), padmode=PAD_PKCS5)
            if link:
                link = link.decode("utf-8")
                if not link == "dummytext" and link not in links:
                    links.append(link)

    if addon.getSetting("autoplay") == "true":
        link = links[0]
    else:
        dialog = xbmcgui.Dialog()
        ret = dialog.select("Choose Stream", links)
        link = links[ret]

    if link.startswith("http"):
        media_url = "{0}|User-Agent={1}".format(link, quote(player_user_agent))
    else:
        media_url = link

    if "playlist.m3u8" in media_url:
        if addon.getSetting("inputstream") == "true":
            li = ListItem(title, path=media_url)
            li.setArt({"thumb": image, "icon": image})
            li.setMimeType("application/vnd.apple.mpegurl")
            li.setProperty("inputstreamaddon", "inputstream.adaptive")
            li.setProperty("inputstream.adaptive.manifest_type", "hls")
            li.setProperty("inputstream.adaptive.stream_headers", media_url.split("|")[-1])
        elif addon.getSetting("livestreamer") == "true":
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
            livestreamer_url = "http://127.0.0.1:19001/livestreamer/" + urlsafe_b64encode("hlsvariant://" + media_url)
            li = ListItem(title, path=livestreamer_url)
            li.setArt({"thumb": image, "icon": image})
            li.setMimeType("video/x-mpegts")
        else:
            li = ListItem(title, path=media_url)
            li.setArt({"thumb": image, "icon": image})
            li.setMimeType("application/vnd.apple.mpegurl")
    else:
        li = ListItem(title, path=media_url)
        li.setArt({"thumb": image, "icon": image})

    try:
        li.setContentLookup(False)
    except AttributeError:
        pass

    xbmcplugin.setResolvedUrl(plugin.handle, True, li)


if __name__ == "__main__":
    try:
        plugin.run(sys.argv)
        s.close()
    except requests.exceptions.RequestException as e:
        dialog = xbmcgui.Dialog()
        dialog.notification(plugin.name, str(e), xbmcgui.NOTIFICATION_ERROR)
        traceback.print_exc()
        xbmcplugin.endOfDirectory(plugin.handle, False)
