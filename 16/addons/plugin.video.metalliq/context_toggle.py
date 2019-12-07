#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
from meta import plugin

def main():
    url = "plugin://{0}/toggle/{1}".format(plugin.addon.getAddonInfo('id'), plugin.addon.getSetting("preferred_toggle"))
    xbmc.executebuiltin("RunPlugin({0})".format(url))

if __name__ == '__main__':
    main()
    plugin.addon.getAddonInfo('fanart')