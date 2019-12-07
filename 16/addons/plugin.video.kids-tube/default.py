# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Kids Tube Addon by coldkeys
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

addonID = 'plugin.video.kids-tube'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCSWRu9m-HZANpMBBQuEf14g"
YOUTUBE_CHANNEL_ID_2 = "UC7Pq3Ko42YpkCB_Q4E981jw"
YOUTUBE_CHANNEL_ID_3 = "PLDt4VQajKv8xKH1YB4kzGMMcnVRwtrk8F"
YOUTUBE_CHANNEL_ID_4 = "UC3KknIJZXRygH2pZ6MDtGbg"
YOUTUBE_CHANNEL_ID_5 = "UC4iRwR3TPWhz1Gstf0sGZhg"
YOUTUBE_CHANNEL_ID_6 = "UCyXWYhbJomJcTUg98MR5PFA"
YOUTUBE_CHANNEL_ID_7 = "UCaeCuyKgxngpD4DXoYwQRwQ"
YOUTUBE_CHANNEL_ID_8 = "UC-exISJxZ6hYgRSJVKshpeA"
YOUTUBE_CHANNEL_ID_9 = "UCv7TYWhF5jhtuY3FDPf06Aw"
YOUTUBE_CHANNEL_ID_10 = "UCpnDeduW4x-ww_UOaUAH6WQ"
YOUTUBE_CHANNEL_ID_11 = "UCQgcmn4OVaKczXEo45iT_fA"
YOUTUBE_CHANNEL_ID_12 = "UCpq1tEJYbykozES2oqwdwlw"
YOUTUBE_CHANNEL_ID_13 = "UCUbu9zPKclGL4quBu1IUelA"
YOUTUBE_CHANNEL_ID_14 = "UCJkWoS4RsldA1coEIot5yDA"
YOUTUBE_CHANNEL_ID_15 = "UCKAqou7V9FAWXpZd9xtOg3Q"

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
        title="Toddler World TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-qMAZNNmYbo0/AAAAAAAAAAI/AAAAAAAAAAA/UNMnnj2SuAI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kids TV (check playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-Vas4UzOl0KE/AAAAAAAAAAI/AAAAAAAAAAA/_fWZBwq0qnA/s100-c-k-no-mo/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kids TV Nursery Rhymes",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-Vas4UzOl0KE/AAAAAAAAAAI/AAAAAAAAAAA/_fWZBwq0qnA/s100-c-k-no-mo/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kids Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-08bC4ULIwPQ/AAAAAAAAAAI/AAAAAAAAAAA/71B5YHtofOw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kids Baby Club",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-hzuxfRs1E4Q/AAAAAAAAAAI/AAAAAAAAAAA/jZhq1P1Ed_c/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kids Play Time",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-E7hAbAy0J7k/AAAAAAAAAAI/AAAAAAAAAAA/8x2tzmPluTI/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Kids ABC TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-lmb7DtfTiRc/AAAAAAAAAAI/AAAAAAAAAAA/PU53XacjZYE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Rainbow Kids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-HaiJISRArdc/AAAAAAAAAAI/AAAAAAAAAAA/m77-kxw9FKI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nursery Rhymes ABC TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-BPO6jTG7M2A/AAAAAAAAAAI/AAAAAAAAAAA/fyUDG8qy4Rk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Pre School Baby Nursery Rhymes And Children's Songs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-8iAOQLyqyvI/AAAAAAAAAAI/AAAAAAAAAAA/xwYwNpShnds/s100-c-k-no/photo.jpg",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Oh My Genius (check playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-C-8v0iL7EyU/AAAAAAAAAAI/AAAAAAAAAAA/az0Pym6l5bY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Kids Play Doh",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-lem-4FgoESY/AAAAAAAAAAI/AAAAAAAAAAA/jkJYoBcC4XM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Finger Family Children's Nursery Rhymes- Kids & Baby Songs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-1d8pxVPaYuw/AAAAAAAAAAI/AAAAAAAAAAA/XIitiKcyy4s/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mother Goose Club",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-CjtfMnhAf90/AAAAAAAAAAI/AAAAAAAAAAA/9x0cv1cw3-8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Little Baby Bum",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-KLfbkE3zovQ/AAAAAAAAAAI/AAAAAAAAAAA/gMZ_6qxvEXw/s100-c-k-no/photo.jpg",
        folder=True )
run()
