# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Tales From The Crypt by coldkeys
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: coldkeys
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.talesfromthecrypt'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PLzfZaKcIQa0FO27ccAzBHfjh7iWpzOzn0"
YOUTUBE_CHANNEL_ID_2 = "PL152bjytsMC7yJcBNkl0AlZoeAO4v2LA_"
YOUTUBE_CHANNEL_ID_3 = "PL152bjytsMC4LcP_6uCSGSAwaR1mvueEw"
YOUTUBE_CHANNEL_ID_4 = "PLFY1LPbpALy4ehS_rN8fEX8L_fwhJEeGr"
YOUTUBE_CHANNEL_ID_5 = "PLE0B78C6D6C49B001"
YOUTUBE_CHANNEL_ID_6 = "PLU51FlmIJOZmB7J8HU4lThxUnNc6Rvvel"
YOUTUBE_CHANNEL_ID_7 = "PLT52XzVRtPAnFa7-RDICbbURdeuXtUvi0"

# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="Tales From the Crypt the Series",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/--jKtPK-bSuU/AAAAAAAAAAI/AAAAAAAAAAA/AQhEuzLB3BQ/s100-c-k-no/photo.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Tales From the Crypt Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/--jKtPK-bSuU/AAAAAAAAAAI/AAAAAAAAAAA/AQhEuzLB3BQ/s100-c-k-no/photo.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Tales from the Cryptkeeper (cartoon)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/--jKtPK-bSuU/AAAAAAAAAAI/AAAAAAAAAAA/AQhEuzLB3BQ/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tales From the Crypt - Demon Knight Soundtrack",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/--jKtPK-bSuU/AAAAAAAAAAI/AAAAAAAAAAA/AQhEuzLB3BQ/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Have Yourself a Scary Little Christmas - Soundtrack",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/--jKtPK-bSuU/AAAAAAAAAAI/AAAAAAAAAAA/AQhEuzLB3BQ/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tales From The Crypt Subtitulado",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/--jKtPK-bSuU/AAAAAAAAAAI/AAAAAAAAAAA/AQhEuzLB3BQ/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Tales From the Crypt (backup)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/--jKtPK-bSuU/AAAAAAAAAAI/AAAAAAAAAAA/AQhEuzLB3BQ/s100-c-k-no/photo.jpg",
        folder=True )
run()
