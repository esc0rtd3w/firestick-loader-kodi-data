# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Sourced From Online Templates And Guides
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Thanks To: Google Search For This Template
# Modified: Merlin
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.merlinkids'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCaeCuyKgxngpD4DXoYwQRwQ"
YOUTUBE_CHANNEL_ID_2 = "UC4iRwR3TPWhz1Gstf0sGZhg"
YOUTUBE_CHANNEL_ID_3 = "UC3KknIJZXRygH2pZ6MDtGbg"
YOUTUBE_CHANNEL_ID_4 = "UC7Pq3Ko42YpkCB_Q4E981jw"
YOUTUBE_CHANNEL_ID_5 = "UCKAqou7V9FAWXpZd9xtOg3Q"
YOUTUBE_CHANNEL_ID_6 = "UCJkWoS4RsldA1coEIot5yDA"
YOUTUBE_CHANNEL_ID_7 = "PLDt4VQajKv8xKH1YB4kzGMMcnVRwtrk8F"
YOUTUBE_CHANNEL_ID_8 = "UCUbu9zPKclGL4quBu1IUelA"
YOUTUBE_CHANNEL_ID_9 = "UCv7TYWhF5jhtuY3FDPf06Aw"
YOUTUBE_CHANNEL_ID_10 = "UCQgcmn4OVaKczXEo45iT_fA"
YOUTUBE_CHANNEL_ID_11 = "UCpq1tEJYbykozES2oqwdwlw"
YOUTUBE_CHANNEL_ID_12 = "UCyXWYhbJomJcTUg98MR5PFA"
YOUTUBE_CHANNEL_ID_13 = "UCpnDeduW4x-ww_UOaUAH6WQ"
YOUTUBE_CHANNEL_ID_14 = "UC-exISJxZ6hYgRSJVKshpeA"
YOUTUBE_CHANNEL_ID_15 = "UCSWRu9m-HZANpMBBQuEf14g"
YOUTUBE_CHANNEL_ID_16 = "PLRi1o_CMkCQIdX7RFmPPa4FJMsKplJngO"
YOUTUBE_CHANNEL_ID_17 = "PLMGtaBqSTiEbxW4TegF1wMp5JJw6SKg9u"
YOUTUBE_CHANNEL_ID_18 = "PLY8yiT5t9ThJVCjkufbjVGEEIayLl7iXg"
YOUTUBE_CHANNEL_ID_19 = "PLyUkLo8OvFU6pPVTZUHob6pP3FY-wUSlq"
YOUTUBE_CHANNEL_ID_20 = "PLZVMGCh7sZUh_jIqrYMKYyyPNJtpng_ZC"
YOUTUBE_CHANNEL_ID_21 = "PLZs0gQed9tMRnuIg0Jv-t8bDLBrpUko-r"
YOUTUBE_CHANNEL_ID_22 = "PLZs0gQed9tMRAfBGlQhHCcqaJipEknlVM"
YOUTUBE_CHANNEL_ID_23 = "PLIEbITAtGBebu6sbY14JHRSCgLWAWhcvV"
YOUTUBE_CHANNEL_ID_24 = "PLZs0gQed9tMQHMLLeD-A95riO1dX4yGsU"
YOUTUBE_CHANNEL_ID_25 = "PL1E1DDEA933CD12FF"
YOUTUBE_CHANNEL_ID_26 = "PLTLP-p6a1SEPXfKtkDEfBL2nM9kZ97jpb"
YOUTUBE_CHANNEL_ID_27 = "PLZs0gQed9tMSHvfjWzZ2VOBU6GWh00slk"
YOUTUBE_CHANNEL_ID_28 = "PLKav3i3U4Xl58bqa1gmIxehnpDxA32HHc"
YOUTUBE_CHANNEL_ID_29 = "PLZs0gQed9tMQX8dw4CiIjwFhsrNT-JRq6"
YOUTUBE_CHANNEL_ID_30 = "PLeagipoZmyfl46t2ABPQitVy1V7qu2vrG"
YOUTUBE_CHANNEL_ID_31 = "PLZs0gQed9tMT5KX9M_PYxrVeVUiJ8aWuS"
YOUTUBE_CHANNEL_ID_32 = "PLqcNVz8UuCsLhpzTjL0JGj3YuMyWWd5Ug"
YOUTUBE_CHANNEL_ID_33 = "PLZs0gQed9tMRRuoTVbL47sSk-tgRCINvP"
YOUTUBE_CHANNEL_ID_34 = "PLnhtGTQWc2dumToZlzsKI8RCOwgzpykly"
YOUTUBE_CHANNEL_ID_35 = "PLOLEQVkmI9eugSKUsrQBH0rxMN-qBLUyV"
YOUTUBE_CHANNEL_ID_36 = "PLZs0gQed9tMQ2iX2H5PCWLCI9xPlIPyYk"
YOUTUBE_CHANNEL_ID_37 = "PLeagipoZmyfm_yCiyU_LYR86ZcJFc0k6d"
YOUTUBE_CHANNEL_ID_38 = "PLtfPnJye9L3dxlbWP7OlJH-_yI3PYsh9r"
YOUTUBE_CHANNEL_ID_39 = "PLaE8D0PEpUTtHl3NzB3VfscnmW68cZC58"
YOUTUBE_CHANNEL_ID_40 = "PLiBi9LVIrC-fVelw2-I2r-yrEk6SpXfO8"
YOUTUBE_CHANNEL_ID_41 = "PLtXcJHjzQOdOJyKUf4N_im5szCADvUbb_"
YOUTUBE_CHANNEL_ID_42 = "PLDJplukjMGFMD9ix6GOiKWc5sTnYih8OX"
YOUTUBE_CHANNEL_ID_43 = "PLZs0gQed9tMQdK9a6D3T0yfZtsc4fpMUx"
YOUTUBE_CHANNEL_ID_44 = "PLZs0gQed9tMQtGV1ZuPglUryJWuJECZ5D"
YOUTUBE_CHANNEL_ID_45 = "PLZs0gQed9tMSMFfClSEL8EOZjayLKNINx"
YOUTUBE_CHANNEL_ID_46 = "PL2469F219C9FEABC0"
YOUTUBE_CHANNEL_ID_47 = "PLZxHX9waSzmv8CeVWGzqSPJK7KPC0HlSF"
YOUTUBE_CHANNEL_ID_48 = "PLZs0gQed9tMS9BLYfxtyyd7OQlQe1n_-f"
YOUTUBE_CHANNEL_ID_49 = "PLrhuB2KrXOjikfPLJhTmz2qKDkltz9L8Y"
YOUTUBE_CHANNEL_ID_50 = "PLZs0gQed9tMS9_E1aN8oCn0XopWZWopyn"
YOUTUBE_CHANNEL_ID_51 = "PLZs0gQed9tMSJwsr7nELmSe_wHWw-gFxL"
YOUTUBE_CHANNEL_ID_52 = "PLCD5B9AD1151F3E0B"
YOUTUBE_CHANNEL_ID_53 = "PLS3SOlSTtJcDe-vQ-T46r_cB1U_ENAuKF"
YOUTUBE_CHANNEL_ID_54 = "PLZs0gQed9tMQzdY8EKdrADeCZ7OJS-AZK"
YOUTUBE_CHANNEL_ID_55 = "PLeagipoZmyfkWkyetCWsJMGy8yBvHdJs-"
YOUTUBE_CHANNEL_ID_56 = "PLeagipoZmyfkwcDThw6yIE3cqQAb8-KQ-"
YOUTUBE_CHANNEL_ID_57 = "PL67492B3700EA9340"

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
        title="3 STOOGES",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="60S DC HEROES",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ABC TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ARCHIE SHOW",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BABY CLUB",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BABY JAKE",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BATFINK",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BATTLE OF THE PLANETS",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_51+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BIBLE STORIES",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="CAPTAIN PLANET",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="CASPER",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="CHILLY WILLY",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="CLUTCH CARGO",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DENNIS THE MENACE",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DR SEUSS",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_56+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DUDLEY DO-RIGHT",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DUNGEONS AND DRAGONS",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="GUMMI BEARS",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="HE-MAN",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="HERMAN AND KATNIP",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="KIDS CHANNEL",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="KIDS TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="KIRBY RIGHT BACK",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="KUNG FU PANDA",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LEARNING",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LITTLE BABY BUM",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LONE RANGER",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LOONEY TUNES",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LUCKY LUKE",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_52+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="MASK",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="MIGHTY HERCULES",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="MOTHER GOOSE CLUB",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="NURSERY RHYMES",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NURSERY RHYMES (FINGER FAMILY)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="NURSERY RHYMES (MORE)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="OCTONAUTS",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="OH MY GENIUS",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="PINK PANTHER",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="PIPPI LONGSTOCKING",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_55+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="PLAY DOH",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="PLAY TIME",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="PRE-SCHOOL SONGS & RHYMES",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="RAINBOW KIDS",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="RUFF AND REDDY",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SHE-RA",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SMURFS",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SNUFFY SMITH",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_57+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SPEED RACER",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="STAR WARS DROIDS",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_54+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="STREETFIGHTER",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SUPER MARIO BROTHERS",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="THE LITTLES",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="TMNT 87-96",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="TODDLER WORLD",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="TOM AND JERRY",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="WIZARD OF OZ",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_53+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="X MEN EVOLUTION",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="special://home/addons/plugin.video.merlinkids/resources/play.png",
        folder=True )
run()