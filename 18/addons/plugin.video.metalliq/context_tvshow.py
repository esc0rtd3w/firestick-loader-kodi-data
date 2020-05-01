#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import xbmc

pluginid = "plugin.video.metalliq"

def main():
    path = xbmc.getInfoLabel('ListItem.Path')
    db_type = xbmc.getInfoLabel('ListItem.DBTYPE')
    if db_type == "tvshow":
        path = urllib.quote_plus(path)
        url = "plugin://{0}/tv/set_library_player/{1}".format(pluginid, path)
        xbmc.executebuiltin("RunPlugin({0})".format(url))
    
if __name__ == '__main__':
    main()