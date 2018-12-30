# -*- coding: UTF-8 -*-
#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # @tantrumdev wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Placenta
# Addon id: script.placenta.artwork
# Addon Provider: MuadDib

#######################################################################
#Import Modules Section
import xbmc,xbmcaddon
import os,re
#######################################################################

def Apply_Theme(new_theme):
    try:
        __settings__ = xbmcaddon.Addon(id='plugin.video.placenta')
        __settings__.setSetting("appearance.1", new_theme)
        print '[PLACENTA] #### Theme Setter: Theme Set To ' + str(new_theme)
    except:
        pass
