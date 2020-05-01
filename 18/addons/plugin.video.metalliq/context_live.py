#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import xbmc

pluginid = "plugin.video.metalliq"

def main():
    path = xbmc.getInfoLabel('ListItem.Path')
    stream_file = xbmc.getInfoLabel('ListItem.FileNameAndPath')
    if stream_file.endswith(".strm"):
        url = "plugin://{0}/tv/set_live_library_player/{1}".format(pluginid, urllib.quote_plus(path))
    else:
        url = "plugin://{0}/tv/set_live_library_player/{1}".format(pluginid, urllib.quote_plus(stream_file))
    xbmc.executebuiltin("RunPlugin({0})".format(url))

if __name__ == '__main__':
    main()