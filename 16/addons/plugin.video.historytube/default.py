# -*- coding: utf-8 -*-
#------------------------------------------------------------
# History Documentary videos on YouTube by coldkeys
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

addonID = 'plugin.video.historytube'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PL152bjytsMC4iT-6j0i5XL0X0iFvzFMSs"
YOUTUBE_CHANNEL_ID_2 = "PL152bjytsMC4ZNf81GfG-Zssyy80yO2HZ"
YOUTUBE_CHANNEL_ID_3 = "PL152bjytsMC77DGLArw00z61LWsBXFQmj"
YOUTUBE_CHANNEL_ID_4 = "PL152bjytsMC5Xi648qL0kMADk06InTqgG"
YOUTUBE_CHANNEL_ID_5 = "UCsEv7pk3lgX0es3CAvKCYeQ"
YOUTUBE_CHANNEL_ID_6 = "UC2FAMzBBVlhyOWMTc6SLFlw"
YOUTUBE_CHANNEL_ID_7 = "UCUR7DG5xaHpo1GyIPEGISIw"
YOUTUBE_CHANNEL_ID_8 = "PLCldpz_Pc1FrGQLsaxaV0kVPqmXN_nanN"
YOUTUBE_CHANNEL_ID_9 = "UCSulo8_9_xLwIyYhaEYFQag"
YOUTUBE_CHANNEL_ID_10 = "UCBsHVT_fAGIZG56oh8nWR_Q"
YOUTUBE_CHANNEL_ID_11 = "UCpiumHmUE5EZeLTftxv9qGw"
YOUTUBE_CHANNEL_ID_12 = "PL152bjytsMC5giQaRkK6f5xQC_2dvAeKb"
YOUTUBE_CHANNEL_ID_13 = "PL152bjytsMC4dn12Yx7CyaIlyTXyfDdrD"
YOUTUBE_CHANNEL_ID_14 = "PL152bjytsMC62UzE1wwOTWfVjRKGYTZvF"
YOUTUBE_CHANNEL_ID_15 = "PL152bjytsMC4-YHtvjpH4H2tNkJCKEd1s"
YOUTUBE_CHANNEL_ID_16 = "PL152bjytsMC6YLLpF71WvkV2PPq-hR55i"
YOUTUBE_CHANNEL_ID_17 = "PL152bjytsMC5fdzzzgQf85DZUXJBhudpm"
YOUTUBE_CHANNEL_ID_18 = "PL152bjytsMC6pVpwLD7Xax1QMhs_B0QMF"
YOUTUBE_CHANNEL_ID_19 = "PL152bjytsMC7XMsTB65J6e9OkQyAXFnf7"
YOUTUBE_CHANNEL_ID_20 = "PL152bjytsMC6ZD1oip2wOk5O_V-Nf51MG"
YOUTUBE_CHANNEL_ID_21 = "PL152bjytsMC6WvxSjTpTXuJAyE1SC9ANZ"
YOUTUBE_CHANNEL_ID_22 = "PL152bjytsMC7tNpr8_TYaorit57Ckq9hU"
YOUTUBE_CHANNEL_ID_23 = "PL152bjytsMC4D7uHsQ9Ohm_Rls8HBZS9a"
YOUTUBE_CHANNEL_ID_24 = "PL152bjytsMC7_7ASf9UAA1iJGnjiQfU9A"
YOUTUBE_CHANNEL_ID_25 = "PL152bjytsMC4EPwMUgRcqhBGbsYT9zKFK"
YOUTUBE_CHANNEL_ID_26 = "PL152bjytsMC7cOUG1D4IuQuKvjA0jQDl5"
YOUTUBE_CHANNEL_ID_27 = "PL152bjytsMC6cBDD6TWFATb4wJBUL95Rd"
YOUTUBE_CHANNEL_ID_28 = "PL152bjytsMC5i41MA-Cdcmi9oXrOhRbTG"
YOUTUBE_CHANNEL_ID_29 = "PL152bjytsMC7Rc2GtOF1UL1w01OygvdfE"
YOUTUBE_CHANNEL_ID_30 = "PL152bjytsMC7EjdYnGPuDg6etK8yk-UFN"
YOUTUBE_CHANNEL_ID_31 = "PL152bjytsMC6fWFVHqexlDboViFEIsGDg"
YOUTUBE_CHANNEL_ID_32 = "PL152bjytsMC4Np0ckVc83HA-bC3ivxMRI"
YOUTUBE_CHANNEL_ID_33 = "PL152bjytsMC5wjqK6bXCARgHM6pRneYKs"
YOUTUBE_CHANNEL_ID_34 = "PL152bjytsMC6o3cTgHXzGzOnFoLVQfvsH"
YOUTUBE_CHANNEL_ID_35 = "PL152bjytsMC7UxxXcG2aVCPo_ItqZg-GB"
YOUTUBE_CHANNEL_ID_36 = "PL152bjytsMC7HUL4K5EYsOrsn92JnUh0Z"
YOUTUBE_CHANNEL_ID_37 = "PL152bjytsMC5GUmj1-v7VNWxDostRymeY"
YOUTUBE_CHANNEL_ID_38 = "PL152bjytsMC4fprSWSah3KMbjvEjZU_5q"
YOUTUBE_CHANNEL_ID_39 = "UC9joNm8jec_JdGF7UBFY2GA"
YOUTUBE_CHANNEL_ID_40 = "PL152bjytsMC4YagWpnkcayYe7VwoiWv5V"
YOUTUBE_CHANNEL_ID_41 = "PL152bjytsMC6xXamnNsrmDXaZetKL9EXH"
YOUTUBE_CHANNEL_ID_42 = "PL152bjytsMC6PQ1x_B5JN2MEuTZwH-Y3R"
YOUTUBE_CHANNEL_ID_43 = "PL152bjytsMC5jRx_eUEvTJKudxLOYZfXL"
YOUTUBE_CHANNEL_ID_44 = "PL152bjytsMC4WcEI21ze2IfcAFRyxj8gi"
YOUTUBE_CHANNEL_ID_45 = "UC8nk3dP5q5z_z60n0DRWgeQ"
YOUTUBE_CHANNEL_ID_46 = "PL57C1E76348A209F3"
YOUTUBE_CHANNEL_ID_47 = "UCgLTuWANjVycg1qYHYPxmnA"
YOUTUBE_CHANNEL_ID_48 = "PL152bjytsMC4ELQL-cyB4HcR5RR4y8jmI"
YOUTUBE_CHANNEL_ID_49 = "PL152bjytsMC6pOots5SAORgX49LXO7Gfv"
YOUTUBE_CHANNEL_ID_50 = "PL152bjytsMC5D2o3yzMATpE9_S2yP3vuB"


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
        title="*Time Team Seasons 1 - 10",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://images.duckduckgo.com/iu/?u=https%3A%2F%2Fyy1.staticflickr.com%2F6088%2F6035367264_a77ff3d4d3_z.jpg&f=1",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Time Team Seasons 11 - 20",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://images.duckduckgo.com/iu/?u=https%3A%2F%2Fyy1.staticflickr.com%2F6088%2F6035367264_a77ff3d4d3_z.jpg&f=1",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Time Team America, Tony Robinson and More",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.world-archaeology.com%2Fwp-content%2Fuploads%2F2012%2F04%2FTime-Team-America-logi.jpg&f=1",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Timewatch - Time Travellers*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://i.ytimg.com/i/77T6JqYcTGOZOiB9XLHJlQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Z-Mysteries",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-qz_C_iuNwr4/AAAAAAAAAAI/AAAAAAAAAAA/Pt_LbVSb36s/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Greek and Roman Civilizations",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-eoJapHgWtmo/AAAAAAAAAAI/AAAAAAAAAAA/IgJk8vqjgok/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="BEST Documentaries",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-iOouVWpX-g4/AAAAAAAAAAI/AAAAAAAAAAA/lN9Ozy9gO1s/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Three Kingdoms (95 episodes - Eng sub)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-GDs9cb2om8c/AAAAAAAAAAI/AAAAAAAAAAA/GLUCwMmVJ4I/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mega Historical Documentaries",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-dpmp-YUPgEE/AAAAAAAAAAI/AAAAAAAAAAA/M1icEinmgwE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="All Histories (check playlist)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-XWpJdd60KKo/AAAAAAAAAAI/AAAAAAAAAAA/0u1G_zV7dVE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Real Crusade History (check playlist)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-ScdZUgpB_Qg/AAAAAAAAAAI/AAAAAAAAAAA/Ng-3qq0ON7I/s100-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="*The Ancient World",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-eUcc0Fcrm1s/AAAAAAAAAAI/AAAAAAAAAAA/bKfgkr4ecYk/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="*History Series (1)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://i.ytimg.com/i/l8Q_4U0J131KFObW759tpA/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="*History Series (2)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://i.ytimg.com/i/EiFmdT9cN-m7IIFtDXrvIw/mq1.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="*Britain",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-ODnq3rmhjNw/AAAAAAAAAAI/AAAAAAAAAAA/gcSd8e04xvo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Ireland, Scotland and Wales",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-p9aR_pSZI9s/AAAAAAAAAAI/AAAAAAAAAAA/g6FQIrn8isc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Roman History",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-qcbRj6D7QK8/AAAAAAAAAAI/AAAAAAAAAAA/nN2Y7NpvMV0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Greek History",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://yt3.ggpht.com/-0MBE_PU19Q8/AAAAAAAAAAI/AAAAAAAAAAA/Xt9lmrfWAYE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Egyptian History",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/-w4Xnrm0pfZA/AAAAAAAAAAI/AAAAAAAAAAA/U2e4yYnFVMY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Spain",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://i.ytimg.com/i/zETNrck_DGdaUpXVplR7XQ/mq1.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="*America",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://i.ytimg.com/i/ZiLCQOXHa3zo-OMJfniXuQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Russia",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://i.ytimg.com/i/FAUx-pCbnNBS1bldHK4HNg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*India",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://i.ytimg.com/i/6Tvle_6AtcwJllqZYbiiWA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*China",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://yt3.ggpht.com/-UfeFKXcDFEg/AAAAAAAAAAI/AAAAAAAAAAA/nb9DY1_e_vU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Japan",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://yt3.ggpht.com/-KlfzfXgSuDw/AAAAAAAAAAI/AAAAAAAAAAA/sU-J1CbbPbw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Turkey",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://i.ytimg.com/i/3E-WqUQn8YOTMdrafPRC_g/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*South America",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://i.ytimg.com/i/WTVublxceKFqtVnrknFnJQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*France",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://i.ytimg.com/i/oYUp7WQSXTMUOzZ4AStPHQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Australia",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://i.ytimg.com/i/9QK-CcQxqUIdQad3xxdstg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Biography",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://i.ytimg.com/i/v1117GQurI9ygrA22uBIbg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*History - Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-mAVsa8Zk6LU/AAAAAAAAAAI/AAAAAAAAAAA/FK0JKY33cmk/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="*World War I",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://yt3.ggpht.com/-DSClpp-Z15U/AAAAAAAAAAI/AAAAAAAAAAA/r04jne1S8Bs/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="*World War II",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://yt3.ggpht.com/-kBm2ZFJxk_M/AAAAAAAAAAI/AAAAAAAAAAA/qA23BlUExGY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Battles Through History",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://i.ytimg.com/i/chZ9npE_jx0SULBeM3Tx_w/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*All At Sea",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://i.ytimg.com/i/AY4NW6sLdg1cX0gJn6zeVA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*History - Series (3)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://yt3.ggpht.com/-aCYojEnOIY8/AAAAAAAAAAI/AAAAAAAAAAA/1PfqtgIHsRA/s100-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="*History - Documentaries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://yt3.ggpht.com/-fwWFhEkKNVY/AAAAAAAAAAI/AAAAAAAAAAA/zaf89-TpJfA/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="*More History Documentaries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://yt3.ggpht.com/-nazqfy_ixgo/AAAAAAAAAAI/AAAAAAAAAAA/yJ5GN7ZW5PM/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Lunar Module 5 (Space Missions)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-fGf9PQsPPRc/AAAAAAAAAAI/AAAAAAAAAAA/uKc5JeHvKIg/s100-c-k-no/photo.jpg",
        folder=True ) 

    plugintools.add_item( 
        #action="", 
        title="*Sporting History",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://yt3.ggpht.com/-y8bzAKL35T0/AAAAAAAAAAI/AAAAAAAAAAA/5Y9Nx0IZm_4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*MegaStructures",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://i.ytimg.com/i/FVWpq2o6CgdbU3Pt8T_SCw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*History of Music",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://i.ytimg.com/i/pfis2fWtev5QhxwDNIIeLA/mq1.jpg?v=4fc532bd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Music Makers - History",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://i.ytimg.com/i/Lq8QV6FbgDqOZNiw2H7h5A/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Seconds from Disaster and Others",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://yt3.ggpht.com/-hr6Zg3tvNHc/AAAAAAAAAAI/AAAAAAAAAAA/Crrl0ZX2vhg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Archanth (Check Playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-ff2dkyZfaug/AAAAAAAAAAI/AAAAAAAAAAA/XyeiWj6IOps/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="British Military and History",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/-B6uEYDm4-Dw/AAAAAAAAAAI/AAAAAAAAAAA/-kymqRL9Ls4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mega Disasters",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://yt3.ggpht.com/-jK6d7QEdI-0/AAAAAAAAAAI/AAAAAAAAAAA/iFmdLKMSiQU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Prehistoric Life",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="https://i.ytimg.com/i/MsOe2Vd2WlDf8KAyUoUYCA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Religion",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://i.ytimg.com/i/9JYXcR3t__0GgX_Lsq8x_g/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Mysteries at the ...",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://i.ytimg.com/i/TxkQOhw1n3VzXTMchpkBNw/mq1.jpg",
        folder=True )
run()
