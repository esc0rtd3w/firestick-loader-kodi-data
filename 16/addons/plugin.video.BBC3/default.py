# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Movies on YouTube Addon by coldkeys
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: coldkeys
#------------------------------------------------------------
#------------------------------------------------------------
# BBC 3 VOD By Project Cypher Addon by Cypher
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: coldkeys/Cypher
#------------------------------------------------------------
import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.BBC3'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCcjoLhqu3nyOFmdqF17LeBQ"
YOUTUBE_CHANNEL_ID_2 = "PL64ScZt2I7wGWb_FNSaCC7F0_UgEYPJXt"
YOUTUBE_CHANNEL_ID_3 = "PL64ScZt2I7wHf5JK4mvBn-s78ULPPQ2rD"
YOUTUBE_CHANNEL_ID_4 = "PL64ScZt2I7wHHR5wVglJ9DcgfMh-iHQ5A"
YOUTUBE_CHANNEL_ID_5 = "PL64ScZt2I7wGUTijkBjNE_nG7BctSq4A4"
YOUTUBE_CHANNEL_ID_6 = "PL64ScZt2I7wFCqfcDRqtrF9TueuySwjzo"
YOUTUBE_CHANNEL_ID_7 = "PL64ScZt2I7wEUnKeX9r4FUlWhiVtGdlEb"
YOUTUBE_CHANNEL_ID_8 = ""
YOUTUBE_CHANNEL_ID_9 = ""
YOUTUBE_CHANNEL_ID_10 = ""

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
        title="Click for FULL BBC 3 ONLINE, By Project Cypher",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="http://static.standard.co.uk/s3fs-public/styles/story_large/public/thumbnails/image/2016/01/04/10/bbc3newlogo0401a.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BBC 3 People Just Do Nothing",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="http://www.vmusic.com.au/content/shows/thumbnails/people_just_do_nothing_01.jpg.ashx?width=620&height=350&mode=crop&scale=both",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BBC 3 Live at The Electric",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="http://res.cloudinary.com/uktv/image/upload/b_rgb:000000,w_660,h_371,c_fill,q_75/v1397482435/ye2waeegxdhr5obeaqbh.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BBC 3 Bad Education",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="http://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2012/8/16/1345111687884/Bad-Education-010.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BBC 3 Comedy Feeds",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="http://ichef.bbci.co.uk/images/ic/480x270/p022x8p7.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BBC Three at T in the Park",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://pbs.twimg.com/media/CJs_GpTWwAAXXaT.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BBC Music Sound Of 2016 - The Short List",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="http://routenote.com/blog/wp-content/uploads/2015/12/bbc-music-sound-of-2016.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="",
        folder=True )                
run()
