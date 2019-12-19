#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    plugin.audio.squeezebox
    Squeezelite Player for Kodi
    Main plugin entry point
'''

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "resources", "lib"))
from plugin_content import PluginContent

#main entrypoint
if __name__ == "__main__":
    PluginContent()
