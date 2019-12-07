# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Documentaries on YouTube by coldkeys
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

addonID = 'plugin.video.documentarytube'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PL152bjytsMC66b6OvO_P8Dlyiigl3ROpi"
YOUTUBE_CHANNEL_ID_2 = "PL152bjytsMC4fC_YSxVupm6Ep_rth9Yu8"
YOUTUBE_CHANNEL_ID_3 = "UC7qc5vSpAZfUIWkoX0aYUMQ"
YOUTUBE_CHANNEL_ID_4 = "UC3HohuFUk2IyjweMKagufQw"
YOUTUBE_CHANNEL_ID_5 = "UCgLTuWANjVycg1qYHYPxmnA"
YOUTUBE_CHANNEL_ID_6 = "PL152bjytsMC6bL6e5QJHXCdL1VDtI2Boc"
YOUTUBE_CHANNEL_ID_7 = "PL152bjytsMC5YyK8CzZjXJi2IGG1f6iRM"
YOUTUBE_CHANNEL_ID_8 = "UCL91Ecf92IKtNII7trSNJNw"
YOUTUBE_CHANNEL_ID_9 = "PL152bjytsMC5DJj7z8WHQn5gDPmOt9P5F"
YOUTUBE_CHANNEL_ID_10 = "PL152bjytsMC6yQ1XXF1ia2B0YttPeKtfN"
YOUTUBE_CHANNEL_ID_11 = "PL152bjytsMC7T0Q7xHWHHiP5Y7dJLRWiG"
YOUTUBE_CHANNEL_ID_12 = "PL152bjytsMC4bxFN5gEkDxYg10gcwDdLg"
YOUTUBE_CHANNEL_ID_13 = "PL152bjytsMC6D4vouE2eqxa17KTDqgou2"
YOUTUBE_CHANNEL_ID_14 = "PL152bjytsMC4ELQL-cyB4HcR5RR4y8jmI"
YOUTUBE_CHANNEL_ID_15 = "PL152bjytsMC5aOcBWY-y97pGKaks-Zdpv"
YOUTUBE_CHANNEL_ID_16 = "PL152bjytsMC6XeU_IyEbaxbgtRonyWhco"
YOUTUBE_CHANNEL_ID_17 = "PL152bjytsMC6YnVebMUshTFlNx8Z97_Ow"
YOUTUBE_CHANNEL_ID_18 = "PL152bjytsMC6oiNllYbAOMFCH8lXiRunF"
YOUTUBE_CHANNEL_ID_19 = "PL152bjytsMC4A4OmwlIfUdeD8sqoEU4gN"
YOUTUBE_CHANNEL_ID_20 = "PL152bjytsMC6L59Isi12kzK1Hn5THv8o_"
YOUTUBE_CHANNEL_ID_21 = "PL152bjytsMC6TIK2q23R6GkgcpPw-4-Dv"
YOUTUBE_CHANNEL_ID_22 = "PL152bjytsMC43QlLMf4YNK7rNP4CByIms"
YOUTUBE_CHANNEL_ID_23 = "PL152bjytsMC4Goscddi5bS9xjHB_2mDUx"
YOUTUBE_CHANNEL_ID_24 = "PL152bjytsMC7yGJjC2GYuXvLaXpn7wcZh"
YOUTUBE_CHANNEL_ID_25 = "PL152bjytsMC5qxzVA7n3akfcyEHJbs4Zf"
YOUTUBE_CHANNEL_ID_26 = "PL152bjytsMC63t1OVqxWnNwcltfgqw8-l"
YOUTUBE_CHANNEL_ID_27 = "PL152bjytsMC4DDsA9uPfdgUwSMFIN4m91"
YOUTUBE_CHANNEL_ID_28 = "UC_sXrcURB-Dh4az_FveeQ0Q"
YOUTUBE_CHANNEL_ID_29 = "UCTrlOONARMd9tOcb7JRqbqA"
YOUTUBE_CHANNEL_ID_30 = "PL152bjytsMC5ngZrzFYlxo5pDcsdnEpUL"
YOUTUBE_CHANNEL_ID_31 = "UCvs65qsrweZucm7LiTrP36Q"
YOUTUBE_CHANNEL_ID_32 = "PL152bjytsMC6xXamnNsrmDXaZetKL9EXH"
YOUTUBE_CHANNEL_ID_33 = "PL152bjytsMC5Dp9P3PIY16-UfKi_XF_U3"
YOUTUBE_CHANNEL_ID_34 = "PL152bjytsMC6PLBtUMJ4wLjenzNxPtAr0"
YOUTUBE_CHANNEL_ID_35 = "PL152bjytsMC7LOywCqqnM0K8hyWm1odA6"
YOUTUBE_CHANNEL_ID_36 = "PL152bjytsMC570vWFnqiPV18SoY1WRhEo"
YOUTUBE_CHANNEL_ID_37 = "UC7fqBPLcdQf5VW_PRa_hlow"
YOUTUBE_CHANNEL_ID_38 = "PL152bjytsMC4aVhkFZxwSKkA5lIq_-yrw"
YOUTUBE_CHANNEL_ID_39 = "UCFM1fgpFGwIl7DeuWE8RkuQ"
YOUTUBE_CHANNEL_ID_40 = "UCM2YmsRUeIbRkqjgNm0eTGQ"
YOUTUBE_CHANNEL_ID_41 = "UCO9Q5_D6tItyoilmDogexng"
YOUTUBE_CHANNEL_ID_42 = "PL152bjytsMC7-a0JyfzLdiMXsG0QDd96d"
YOUTUBE_CHANNEL_ID_43 = "PL152bjytsMC4ar0GTAXQ6ycBoOTlZR10w"
YOUTUBE_CHANNEL_ID_44 = "PL152bjytsMC5DA49bjZv2I089Tc8frdaR"
YOUTUBE_CHANNEL_ID_45 = "UCdXKzUSbFZyBFt1h2LjjvsQ"
YOUTUBE_CHANNEL_ID_46 = "PL152bjytsMC5MRutIMrbBCFcc5EGAre0t"
YOUTUBE_CHANNEL_ID_47 = "PL152bjytsMC70yAAW7ryCt0o63EQ71Vjg"
YOUTUBE_CHANNEL_ID_48 = "PL152bjytsMC6GTxge816-PC_H5Ai9rYhD"
YOUTUBE_CHANNEL_ID_49 = "UCk8pVOnlzByean1RmUJOeCw"
YOUTUBE_CHANNEL_ID_50 = "UCetpfrEDE4AgKEu4vYdwMGQ"


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
        title="*David Attenborough*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://i.ytimg.com/i/3p3WtGCfeVRvt3ytWNHQAg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Escape to the Country*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://i.ytimg.com/i/znmQVMuULKJuAHV3IfV0Og/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NGC - (Amazon see playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-pF1sp98zi1E/AAAAAAAAAAI/AAAAAAAAAAA/E-ySnLMpb00/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ocean Wild",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-4nHixblGJtg/AAAAAAAAAAI/AAAAAAAAAAA/cWcLIgRmWwU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mega Disasters",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-jK6d7QEdI-0/AAAAAAAAAAI/AAAAAAAAAAA/iFmdLKMSiQU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="How It's Made",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-cBpgjwoBbHw/AAAAAAAAAAI/AAAAAAAAAAA/Bb-IsAanv3o/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="*Natural Disasters*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-guvcXLUvj5o/AAAAAAAAAAI/AAAAAAAAAAA/q3bw6ZmxlfM/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Documentaries Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-SRDKHzWBuNk/AAAAAAAAAAI/AAAAAAAAAAA/CGLHgSvtvr8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Earth and Climate Change*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-f-iTE-XjTtg/AAAAAAAAAAI/AAAAAAAAAAA/lZc6ZEDKNco/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Just Amazing*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-wQ95Bw1UQtQ/AAAAAAAAAAI/AAAAAAAAAAA/vGFNGyBU9t8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Space Documentaries*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-o5SqTvNGBuI/AAAAAAAAAAI/AAAAAAAAAAA/REMI90DnKMg/s100-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="*PBS Nova Documentaries*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://i.ytimg.com/i/4H7bkwb6go7vrEkgYMgsGw/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="*Underwater Life*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://i.ytimg.com/i/N_kMFZPoAqueNEfLD8TTPw/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="*Prehistoric Life*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-Vn6E61LG56c/AAAAAAAAAAI/AAAAAAAAAAA/tj7eWa_jtvM/s100-c-k-no/photo.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="*Animals*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-bySYV6OBABs/AAAAAAAAAAI/AAAAAAAAAAA/TUJBC41FuSg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Birds*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://i.ytimg.com/i/7uJ7jdwfPcmqKu7V2nI9rA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Reptiles*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://i.ytimg.com/i/vfH62D48X5Bahu-oroIreQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Insects and Others*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://i.ytimg.com/i/cPRY79BUym6pAzuwdPo5wA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*People and Peoples*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://i.ytimg.com/i/zo931iwA-4hTxGGsAHcBKQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Places*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://i.ytimg.com/i/rul-IVStrYQOaN6Ik8fkXA/mq1.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="*Bigfoot and Other Anomolies*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://yt3.ggpht.com/-yfLAbTgKBGo/AAAAAAAAAAI/AAAAAAAAAAA/QXR5KkcxAkA/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Technology*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://i.ytimg.com/i/iB9rK85xR9_fsMDIOcBzfw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*How It Works*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://yt3.ggpht.com/-TknP_OJmc84/AAAAAAAAAAI/AAAAAAAAAAA/MEVM5pueZAo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Sharks*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://i.ytimg.com/i/HThGYhvhgyvTgUkv3n5R_A/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Bush Tucker Man and Ray Mears*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://i.ytimg.com/i/B-ZHqtdOOQP97sFgghJv3A/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Cousteau - Stevens - Corwin*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://yt3.ggpht.com/-Y7M3HxhIPXE/AAAAAAAAAAI/AAAAAAAAAAA/F6yske0SxqI/s100-c-k-no-mo/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Bear Grylls*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://i.ytimg.com/i/0JBpG2wnuaYY4Xaq6mKtag/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Documentary Tube",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://yt3.ggpht.com/-S-vFfo9ZEQw/AAAAAAAAAAI/AAAAAAAAAAA/p11UQUOJPiY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Seosan TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://yt3.ggpht.com/-Ck9Jo4G4yZs/AAAAAAAAAAI/AAAAAAAAAAA/ZP0TFEc9xtY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Tanked and Fish Tank Kings*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://i.ytimg.com/i/2U6mUdlQBS0umA4EbhCNwQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Explore the World",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-MahOSuELdM0/AAAAAAAAAAI/AAAAAAAAAAA/1Gz3o8HcPSs/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="*MegaStructures*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://i.ytimg.com/i/FVWpq2o6CgdbU3Pt8T_SCw/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="*Grand Designs*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://i.ytimg.com/i/IcHogHIVOmcYHVFrfSbtWw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Homes and Restoration*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://yt3.ggpht.com/-1eeHRxZfj9I/AAAAAAAAAAI/AAAAAAAAAAA/QbShPRkukHE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*The Secrets of Nature*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://yt3.ggpht.com/-iztw3n2qnJM/AAAAAAAAAAI/AAAAAAAAAAA/PCf32MQpPQw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Michael Palin*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://i.ytimg.com/i/sdKyU3FQcO6TJNo9DqcLkA/mq1.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="World Documentaries Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://yt3.ggpht.com/-J78EouLWbVg/AAAAAAAAAAI/AAAAAAAAAAA/LgnEEnlVaTo/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="*Documentary Series*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://yt3.ggpht.com/-vNiwabFzrYc/AAAAAAAAAAI/AAAAAAAAAAA/hgYmX_3ZGnY/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Documentary and Life HD",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-Wiyi4I9ZjIw/AAAAAAAAAAI/AAAAAAAAAAA/SCa3UpHccwo/s100-c-k-no/photo.jpg",
        folder=True ) 

    plugintools.add_item( 
        #action="", 
        title="Journeyman Pictures",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://yt3.ggpht.com/-Xs83JYB4N28/AAAAAAAAAAI/AAAAAAAAAAA/Fr6y4xA5VVA/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="PublicResourceOrg (Check Playlist)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://i.ytimg.com/i/X1nmhI_px297r0xp4cJBlg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*More Nature Documentaries*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/-_zOKR9ylefo/AAAAAAAAAAI/AAAAAAAAAAA/cbU7iYLD3wc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="A Place In ..",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://i.ytimg.com/i/co-5O8Qv9K1v56GtFtwVLQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Homes Under the Hammer",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://i.ytimg.com/i/DBVByX8tNTae_OOaGSBjGA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Joy of Painting (Playlist for Seasons)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-3JIv93qscdY/AAAAAAAAAAI/AAAAAAAAAAA/jUgiZDXKcuQ/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="*Rex Hunt, Robson Green and more.*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/-JVYN_Kyawjc/AAAAAAAAAAI/AAAAAAAAAAA/HipcJcuCULQ/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Fishing*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://i.ytimg.com/i/hXKe8kZn3xqgpqtpnSYpUw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Treasure*",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="https://yt3.ggpht.com/-lyQ7kuZRdj0/AAAAAAAAAAI/AAAAAAAAAAA/5Mnr0zV1wUk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Travel Film Archive (See Playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://yt3.ggpht.com/-74-csLJDn5M/AAAAAAAAAAI/AAAAAAAAAAA/GBzNH6PB-zs/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Planet Doc",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://yt3.ggpht.com/-jSIGfZAjyTk/AAAAAAAAAAI/AAAAAAAAAAA/dvaLu4krnwI/s100-c-k-no/photo.jpg",
        folder=True )
run()
