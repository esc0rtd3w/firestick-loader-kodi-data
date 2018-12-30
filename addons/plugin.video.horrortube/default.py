# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Horror Movies, TV Shows and Trailers on YouTube by coldkeys
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

addonID = 'plugin.video.horrortube'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCu0bxC7vG_HKWJ7ijO9QKwg"
YOUTUBE_CHANNEL_ID_2 = "UCpWnVkh7OffpObDuqzb9gCA"
YOUTUBE_CHANNEL_ID_3 = "UCp6KXQaoJr3gtAE7OWDqX_A"
YOUTUBE_CHANNEL_ID_4 = "UCthjjEowaInDmJsrT-Mn3xQ"
YOUTUBE_CHANNEL_ID_5 = "UCdlxrbT0ox6QoxdCd2GYY1w"
YOUTUBE_CHANNEL_ID_6 = "UCQAQtYz_gbBnowj5fo8NYNg"
YOUTUBE_CHANNEL_ID_7 = "UCe3_6MmyVMvnY3VnkQSjlqQ"
YOUTUBE_CHANNEL_ID_8 = "UCoCO4dJ05Mo-Jdy0P7jG0FA"
YOUTUBE_CHANNEL_ID_9 = "UCJLserGxR1lji6aQsfnE9SA"
YOUTUBE_CHANNEL_ID_10 = "UCjBQP_IAKuNZ_t3VYNlCAmg"
YOUTUBE_CHANNEL_ID_11 = "PLeagipoZmyfkzpV_h8IHGUQx6WvelM54j"
YOUTUBE_CHANNEL_ID_12 = "UC49qAywwrDrLNDgQEe3vYuA"
YOUTUBE_CHANNEL_ID_13 = "PLmHgXUJMN1TUtIOqNXDYVesjjWKOziQq5"
YOUTUBE_CHANNEL_ID_14 = "PLeagipoZmyflMOu9SoIBHmjcgj2kQjEjF"
YOUTUBE_CHANNEL_ID_15 = "PL6fJmjt84zZhVlt_nTOeWQM8FCOEg4V4s"
YOUTUBE_CHANNEL_ID_16 = "PL6fJmjt84zZhQOPSC6BJJtUDdqAkndNCw"
YOUTUBE_CHANNEL_ID_17 = "PL1j14gtz6BiuGUi3a01JzHSXqbMODWFrH"
YOUTUBE_CHANNEL_ID_18 = "PL1j14gtz6BiuvRH8badB32kevoKBWi4P0"
YOUTUBE_CHANNEL_ID_19 = "PL1j14gtz6BiurbB_jVhu_psZ6WEC8zXt0"
YOUTUBE_CHANNEL_ID_20 = "PL1j14gtz6BisIm4czU8u2yPkvWkIM63ZH"
YOUTUBE_CHANNEL_ID_21 = "PL1j14gtz6BitQFJxyeXhMZv8mKxNytnR2"
YOUTUBE_CHANNEL_ID_22 = "PL1j14gtz6BivjGd6FU2H2TRYLhD7l1IVb"
YOUTUBE_CHANNEL_ID_23 = "PL152bjytsMC65uUA0EWQi42PdqqM-ceY5"
YOUTUBE_CHANNEL_ID_24 = "PL05405B961D7A0F9E"
YOUTUBE_CHANNEL_ID_25 = "PLE3B07DD0EA17D1FE"
YOUTUBE_CHANNEL_ID_26 = "PL1j14gtz6BiulrLcP6mCk5iIGviO8KqzJ"
YOUTUBE_CHANNEL_ID_27 = "PL1j14gtz6BitpphBSf9bgSsc_sE2dP8mc"
YOUTUBE_CHANNEL_ID_28 = "PL1j14gtz6Biv6DYP6Z9lStG1jTY7Qqvpm"
YOUTUBE_CHANNEL_ID_29 = "UCYD9OeyUBUPIkoj_P33EyKw"
YOUTUBE_CHANNEL_ID_30 = "UCKeWqUaTPc7ielesYSJE0vg"
YOUTUBE_CHANNEL_ID_31 = "UCbIy2yMxN28Y_N9K34wqezQ"
YOUTUBE_CHANNEL_ID_32 = "PL1j14gtz6BisyWXBcewUlXi7fcaKKysYh"
YOUTUBE_CHANNEL_ID_33 = "PL1j14gtz6BivLcKK4r3VoVhs3HHwMAEoM"
YOUTUBE_CHANNEL_ID_34 = "PL1j14gtz6BitfSmmespqh3TeZupN83wC1"
YOUTUBE_CHANNEL_ID_35 = "PL1j14gtz6BivG5syasSASFvdYl2YE-YUN"
YOUTUBE_CHANNEL_ID_36 = "PLX4ZCfhRSeC7HAnOlr9oFtB9XIMSxrtUy"
YOUTUBE_CHANNEL_ID_37 = "PLgTLZSbwbEZw0XUwZEmM-yi5SRHQzadap"
YOUTUBE_CHANNEL_ID_38 = "PLFC7773999850FF60"
YOUTUBE_CHANNEL_ID_39 = "PLvmIe53-AVGJ0tPB3qqHOLBfPZHsm4OFz"
YOUTUBE_CHANNEL_ID_40 = "PLzovi87vDfzIAeQ8OR1qLBw6NVzaAeIKV"
YOUTUBE_CHANNEL_ID_41 = "PLzovi87vDfzIIcI4-Rx5s0YqiOaT3uF0-"
YOUTUBE_CHANNEL_ID_42 = "PLG6H-orfARGQgnQcVlunOJhK654EFeHYn"
YOUTUBE_CHANNEL_ID_43 = "PLzovi87vDfzIQ1ixRTN_lPzc2YYmiDexC"
YOUTUBE_CHANNEL_ID_44 = "PLIRDxaBH8SqPxTtIY_anoAdjSWPJ7Rugh"
YOUTUBE_CHANNEL_ID_45 = "PLyu7jyopDrFEtj5O1_M6K67mudZoPf-E1"
YOUTUBE_CHANNEL_ID_46 = "PLA2404D2AC554EE8A"
YOUTUBE_CHANNEL_ID_47 = "UC8LSXlypv4C5FjTed50USng"
YOUTUBE_CHANNEL_ID_48 = "UCV8NbuI_Q3FcLfH2_3-6tXA"
YOUTUBE_CHANNEL_ID_49 = "UCNalSveQauMmPhkXkAVRCVg"
YOUTUBE_CHANNEL_ID_50 = "UCmXMUE-aowQu94qrulWc6aA"


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
        title="Kings of Horror (check playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-kQJTY1j3FwM/AAAAAAAAAAI/AAAAAAAAAAA/WYLXCrtBTGE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Horror Show",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-VkJSkl5lgE0/AAAAAAAAAAI/AAAAAAAAAAA/Up8y0zUHO9M/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Horror Hive (see playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-7W6Tzt-DHes/AAAAAAAAAAI/AAAAAAAAAAA/2wG1tFaNz94/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bloodbath and Beyond Movie Reviews",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-rjk1WocEWgU/AAAAAAAAAAI/AAAAAAAAAAA/9bUUP_xEM9Y/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Full Horror",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-Y2CXkDfA2jo/AAAAAAAAAAI/AAAAAAAAAAA/7gl5qWST43w/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Horrorville Creepshow",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-EExbNnYnWRk/AAAAAAAAAAI/AAAAAAAAAAA/CZBV4M7bP9E/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="The Burial Ground 4",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-9-XTjSDSo-4/AAAAAAAAAAI/AAAAAAAAAAA/JPCdzxZgs0k/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Horrorfan Baby",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-aKc8UIw1vTM/AAAAAAAAAAI/AAAAAAAAAAA/Mc5lQPy5dtI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vintage Horror Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-TgNFf63OR4c/AAAAAAAAAAI/AAAAAAAAAAA/fRspuBnVHA0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="WOW tv Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-fc2Eit2qRFI/AAAAAAAAAAI/AAAAAAAAAAA/mOZJZbRSCdY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="One Step Beyond (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-hFyL8l5MUTs/AAAAAAAAAAI/AAAAAAAAAAA/tJr2V8acY74/s100-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Horror Radio Shows & Creepy Tales",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-fCIdmK6QC6Y/AAAAAAAAAAI/AAAAAAAAAAA/jgVl76cfBUk/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Pizza Creatures",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-1XPQgwWQHkA/AAAAAAAAAAI/AAAAAAAAAAA/Dv47-1UZMrk/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Ghost Story-Circle of Fear (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/vWWrSdiA9LqRp_Iz1aZue2X1F5O_pIRf-TAfrySwvzQvtTX6Y9cYz9xwITjIYKRcS738kRynxbBK7UGjZw=s100-nd",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="The Others (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/QVYPFy2LZ-bJtQWQlOxZyMgXbMR-zhfB-UpjTAynliQKQJzfBLK5c-9HL0Xhy5CwK04QHhLreEyjhisAqQ=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sea of Souls (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-NoBw-WTfttk/AAAAAAAAAAI/AAAAAAAAAAA/qN03awCftwU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Horror and Scary Movies 2000-",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-QuNI8hE39-0/AAAAAAAAAAI/AAAAAAAAAAA/aazFxkoC3tE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Horror and Scary Movies 1980-1999",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://yt3.ggpht.com/-QuNI8hE39-0/AAAAAAAAAAI/AAAAAAAAAAA/aazFxkoC3tE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Horror and Scary Movies 1960-1979",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/-QuNI8hE39-0/AAAAAAAAAAI/AAAAAAAAAAA/aazFxkoC3tE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Horror and Scary Movies 1940-1959",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-QuNI8hE39-0/AAAAAAAAAAI/AAAAAAAAAAA/aazFxkoC3tE/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Horror and Scary Movies 1920-1939",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://yt3.ggpht.com/-QuNI8hE39-0/AAAAAAAAAAI/AAAAAAAAAAA/aazFxkoC3tE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Stephen King Films",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://yt3.ggpht.com/mEbmQMbRa9BgkjAjHcA1OV_Ba_seM23-IJ0J_-Qt6Zx2eKlNX80SS7gF-XwZBdp3xQKkxyggSGZdZ1ck=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Horror Movies Mega Playlist",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://i.ytimg.com/i/R62Gcwdcqdld_aLEgBndjQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Hex Series 1",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://i.ytimg.com/i/gGz0ridMXw11JCouYf9erQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Hex Series 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://i.ytimg.com/i/gGz0ridMXw11JCouYf9erQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Supernatural (1977 Mini-Series Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://yt3.ggpht.com/j3yilmdLSwujNcXmPY-BYEDLsSfsqj7Ks7sFUPnEbMcPW1iGWwhrD0Wgstp0F-wpyYqCu3PjJzZXZypN=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Wolf Lake (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://yt3.ggpht.com/xGOOYoHv29ZmcmLp5gGE1dyuJLMmkDrPDMQMJA3NUi1SHZ53ukr1QxBgGtcOciAFRHS3gzemc18fDCdI=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Spooky (Complete Series)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://yt3.ggpht.com/-jrCCqKRANys/AAAAAAAAAAI/AAAAAAAAAAA/0YAfpCib40o/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DorsetGhost (Check Playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://yt3.ggpht.com/-F8yMV_mC_48/AAAAAAAAAAI/AAAAAAAAAAA/rJXz9d3h0uk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DorsetGhost Horror (Check Playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://yt3.ggpht.com/-WduU250elz0/AAAAAAAAAAI/AAAAAAAAAAA/B-fJ4_PvIXE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="DorsetGhost Mysteries (Check Playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-NyxpOHjQmec/AAAAAAAAAAI/AAAAAAAAAAA/gBfLhm2Dd4I/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Mummy Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://i.ytimg.com/i/mw5bdrnhdNbfg5bG2cJhcQ/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Werewolf Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://i.ytimg.com/i/CaWB3t6Jhbnhnw27shsOog/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vampire Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://i.ytimg.com/i/Jigo75OZ59qePFEjfzmm9A/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Zombie Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://yt3.ggpht.com/-7cYBXMIuTk4/AAAAAAAAAAI/AAAAAAAAAAA/8bMr0KDEIMw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Phantom Creeps (Complete Serial)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://yt3.ggpht.com/-1PiehLMApU4/AAAAAAAAAAI/AAAAAAAAAAA/tZ6vG-gTxR4/s100-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Horror Movies Full - Kiss Tube (600 movies)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://yt3.ggpht.com/-khEb4ajFbnE/AAAAAAAAAAI/AAAAAAAAAAA/9r0TwoPs99I/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Horror Movie Trailers",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://yt3.ggpht.com/-B-XTR95RQVQ/AAAAAAAAAAI/AAAAAAAAAAA/weK0uiFFzXY/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Horror Movie Documentaries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-7O54pQxRlRQ/AAAAAAAAAAI/AAAAAAAAAAA/vd_AM-mqC8s/s100-c-k-no/photo.jpg",
        folder=True ) 

    plugintools.add_item( 
        #action="", 
        title="Masters of Horror (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://i.ytimg.com/i/g-VT3ydvVtDkEsWubQhbIA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Forever Knight (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fmedia-cache-ec0.pinimg.com%2F736x%2F3f%2Fb5%2F4e%2F3fb54e8141de56827d2b78048be67079.jpg&f=1",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Fear Itself (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://i.ytimg.com/i/vJ32uKF2eSQq9wx6YS5EzQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tales from the Crypt (TV Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://yt3.ggpht.com/-uWmCKCwZ0a4/AAAAAAAAAAI/AAAAAAAAAAA/b6eWBcVfwoU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Goosebumps (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://i.ytimg.com/i/UKUYDp1lolbs6Lv_4MlKzg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Blood Ties (TV Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-hzOa9ELPywI/AAAAAAAAAAI/AAAAAAAAAAA/Q8kO4R6P1xg/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="The Nightmare Room (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/0Ojlv_Q2ACFnYMcNAEoTJh-pbSriXeHUeZ0N1RKa-rDLUvC0pkMcUp-iCxILzG9YEe0u-PEQmDgOnTyC4g=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vulture Grindhouse",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://yt3.ggpht.com/-bVNHoz3EgB4/AAAAAAAAAAI/AAAAAAAAAAA/CnFeP_mL62g/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vulture Graffix / Trailer Trash",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="https://yt3.ggpht.com/-6R9e_LVxA2s/AAAAAAAAAAI/AAAAAAAAAAA/PnBXaViUBHg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Trailer Horror Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://yt3.ggpht.com/-QuNI8hE39-0/AAAAAAAAAAI/AAAAAAAAAAA/aazFxkoC3tE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="FilmIsNow Horror Movie Trailers",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://yt3.ggpht.com/-i5mwlfDWhNo/AAAAAAAAAAI/AAAAAAAAAAA/JAaD5L9j75E/s100-c-k-no/photo.jpg",
        folder=True )
run()
