# -*- coding: utf-8 -*-
#------------------------------------------------------------
# New Kids Tv by @random_robbie
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: random_robbie
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.newkidstv'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "littlebabybum"
YOUTUBE_CHANNEL_ID_2 = "firemansamchanne"
YOUTUBE_CHANNEL_ID_3 = "theofficialpeppa"
YOUTUBE_CHANNEL_ID_4 = "BabyTVChannel"
YOUTUBE_CHANNEL_ID_5 = "cbeebiesgrownups"
YOUTUBE_CHANNEL_ID_7 = "inthenightgardenuk"
YOUTUBE_CHANNEL_ID_8 = "PostmanPatSDS"
YOUTUBE_CHANNEL_ID_10 = "ChildrenGamesTV"

skin_used = xbmc.getSkinDir()
if skin_used == 'skin.confluence':
    xbmc.executebuiltin('Container.SetViewMode(500)') # "Thumbnail" view
elif skin_used == 'skin.aeon.nox':
    xbmc.executebuiltin('Container.SetViewMode(512)') # "Info-wall" view. 

#hakamac thanks Roman_V_M
def SetViewThumbnail():
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(500)')
    elif skin_used == 'skin.aeon.nox':
        xbmc.executebuiltin('Container.SetViewMode(511)') 
    else:
        xbmc.executebuiltin('Container.SetViewMode(500)')
# Entry point
def run():
    plugintools.log("docu.run")
    SetViewThumbnail()
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
        title="Little Babybum",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://i.ytimg.com/vi/WixFbdS-Bv8/maxresdefault.jpg",
        folder=True )
     
    plugintools.add_item( 
        #action="", 
        title="Fireman Sam",
        url="plugin://plugin.video.youtube/user/firemansamchannel/",
        thumbnail="http://www.firemansam.com/en-us/Images/news-feature-01_tcm993-160907.jpg",
        folder=True )	 
    

    plugintools.add_item( 
        #action="", 
        title="Thomas & Friends",
        url="plugin://plugin.video.youtube/user/thomasandfriends/",
        thumbnail="http://www.thomasandfriends.com/en-gb/Images/TF_ThomasLandLogo_UK_260x260_tcm1109-190709.png",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Barney & Friends",
        url="plugin://plugin.video.youtube/user/HITBarney/",
        thumbnail="http://cdn8.nflximg.net/images/3031/3913031.jpg",
        folder=True )
		
		
    plugintools.add_item( 
        #action="", 
        title="Bob the Builder UK",
        url="plugin://plugin.video.youtube/user/bobthebuilderchannel/",
        thumbnail="http://images.zap2it.com/assets/p186054_b_h3_aa/bob-the-builder.jpg",
        folder=True )
		
		
    
    plugintools.add_item( 
        #action="", 
        title="Offical Peppa Pig",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://upload.wikimedia.org/wikipedia/en/6/61/Peppa_Pig.png",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Baby TV Channel",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-w1gbvReuRqM/AAAAAAAAAAI/AAAAAAAAAAA/ve40E-bIMjs/s900-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Cbeebies",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="http://www.stmp.camden.sch.uk/wp-content/uploads/2015/03/CBeebies.png",
        folder=True )
        
        
    plugintools.add_item( 
        #action="", 
        title="In The Night Garden",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="http://www.outpostfacilities.co.uk/images/In-the-Night-Garden.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Postman Pat",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="http://www.drusillas.co.uk/img/news/image/main/postman-pat-approved-73.jpg",
        folder=True )
        
        
    plugintools.add_item( 
        #action="", 
        title="The Kids Club",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail=icon,
        folder=True )
		        
    plugintools.add_item( 
        #action="", 
        title="KidsGames HD",
        url="plugin://plugin.video.youtube/channel/UCjNUHgBv6rvGHIdXNaHBz8g",
        thumbnail="https://yt3.ggpht.com/-ARsBQ3nmfO8/AAAAAAAAAAI/AAAAAAAAAAA/GYoFkNgBsKU/s900-c-k-no/photo.jpg",
        folder=True )
		        
    plugintools.add_item( 
        #action="", 
        title="KidsTV",
        url="plugin://plugin.video.youtube/channel/UC7Pq3Ko42YpkCB_Q4E981jw",
        thumbnail=icon,
        folder=True )
		
		        
    plugintools.add_item( 
        #action="", 
        title="HooplaKidz TV",
        url="plugin://plugin.video.youtube/user/HooplaKidzTv/",
        thumbnail="https://yt3.ggpht.com/-KWRYIA7c9zg/AAAAAAAAAAI/AAAAAAAAAAA/kut-rS4LEFU/s100-c-k-no/photo.jpg",
        folder=True )
		
		        
    plugintools.add_item( 
        #action="", 
        title="BabyFirst TV",
        url="plugin://plugin.video.youtube/user/BabyFirstTV/",
        thumbnail=icon,
        folder=True )
		
		        
    plugintools.add_item( 
        #action="", 
        title="Peter Rabbit",
        url="plugin://plugin.video.youtube/channel/UCngkVoq8aayyK6qX9JJitRg/",
        thumbnail="https://yt3.ggpht.com/-ZeMoemv18J8/AAAAAAAAAAI/AAAAAAAAAAA/eWXtndNWbNY/s100-c-k-no/photo.jpg",
        folder=True )
		
		        
    plugintools.add_item( 
        #action="", 
        title="Baby Jake",
        url="plugin://plugin.video.youtube/channel/UCjonc-9WOA15sLdggTYQGwA/",
        thumbnail="https://yt3.ggpht.com/-HffJaIQI428/AAAAAAAAAAI/AAAAAAAAAAA/UTtd2qT8YcE/s100-c-k-no/photo.jpg",
        folder=True )
		
		        
    plugintools.add_item( 
        #action="", 
        title="Horrid Henry",
        url="plugin://plugin.video.youtube/user/TheRealHorridHenry/",
        thumbnail="https://yt3.ggpht.com/-9WPGFAZ5q6w/AAAAAAAAAAI/AAAAAAAAAAA/b_3b8zQ639A/s100-c-k-no/photo.jpg",
        folder=True )
		
		        
    plugintools.add_item( 
        #action="", 
        title="Teletubbies",
        url="plugin://plugin.video.youtube/channel/UCOk55dAgB8VnMlhaTEMeX5A/",
        thumbnail="https://yt3.ggpht.com/-qZxbvRiVZ6E/AAAAAAAAAAI/AAAAAAAAAAA/bpvaVTC9NfU/s100-c-k-no/photo.jpg",
        folder=True )
    
run()
