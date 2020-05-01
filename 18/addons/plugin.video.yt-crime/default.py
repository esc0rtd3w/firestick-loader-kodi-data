# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Crime on YouTube by coldkeys
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

addonID = 'plugin.video.yt-crime'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PLyicTY7J3bULdNAG8fCZOMTM_PeOsomR0"
YOUTUBE_CHANNEL_ID_2 = "PLcviVtB85dLxNwXqdrnKGSIAg8uL3JKuO"
YOUTUBE_CHANNEL_ID_3 = "UC6zeD2locTNMiZvQC7BD9VQ"
YOUTUBE_CHANNEL_ID_4 = "UCLUn8uOXZXEJMoLFxons1sw"
YOUTUBE_CHANNEL_ID_5 = "UCSX7Y8k0PCOgUgmOdd6RkQw"
YOUTUBE_CHANNEL_ID_6 = "UCiRnIG5jwSsIVnx7USPXTMQ"
YOUTUBE_CHANNEL_ID_7 = "PLEk3_2u_nF_ehgM3TFhi9j2hMXnoDTSqR"
YOUTUBE_CHANNEL_ID_8 = "PLyLrnNOEPdo430q3kcZmUHtbbPfv4vycg"
YOUTUBE_CHANNEL_ID_9 = "UCOE7RpnX-z1XtmViWvf83WA"
YOUTUBE_CHANNEL_ID_10 = "PLNlKG_zAzFm63zTKqzp2LqNZBazpjDCFM"
YOUTUBE_CHANNEL_ID_11 = "UCXRPr7_0bnIKFVFQRODAV2g"
YOUTUBE_CHANNEL_ID_12 = "UCwQei10QoLUmFNBaH2JBhww"
YOUTUBE_CHANNEL_ID_13 = "UC03LFzB8W8OD16zfgPqxlFQ"
YOUTUBE_CHANNEL_ID_14 = "UCg_jR8pdBfrsw3fPOApWsxw"
YOUTUBE_CHANNEL_ID_15 = "UCvQhPN4r4bAauI0dJo71lyA"
YOUTUBE_CHANNEL_ID_16 = "UCB34HtBACNAhMKG42_msPJA"
YOUTUBE_CHANNEL_ID_17 = "PL4HLZHMq05jAiYLlIxWiwoXmEDBbIavBK"
YOUTUBE_CHANNEL_ID_18 = "PL30kO8oVeDkpdNVGciv4YPyL1k4IXiEIF"
YOUTUBE_CHANNEL_ID_19 = "PLdiXEhyBHpfWCGocPNSk5Mhtjsh41PsUS"
YOUTUBE_CHANNEL_ID_20 = "PLy7mi56uNHSm1UtIlJB4vppyKf2SvNLIL"
YOUTUBE_CHANNEL_ID_21 = "PLD75qpSXCKDDuxGAlwIKoWT08FbSImWLv"
YOUTUBE_CHANNEL_ID_22 = "PLEi83IaZq0XWJ0tKfSQ1QnRRFm5Tn2Hfv"
YOUTUBE_CHANNEL_ID_23 = "PLSNE-2y4IBXjJe8SFBK2xXhBwLesTKHk-"
YOUTUBE_CHANNEL_ID_24 = "PLaTIGMOvay0V4nP9DL_Pyrxwb3nTSO4nw"
YOUTUBE_CHANNEL_ID_25 = "PLS7E6enfYOvwG7sGj6Ep8HGwIRJBCInBM"
YOUTUBE_CHANNEL_ID_26 = "PLosYISkcFffb18AY3Nqu4WisNPOofHeRr"
YOUTUBE_CHANNEL_ID_27 = "PLDrNp9S9i6UTr--BQeDzxKczdh7ri15GD"
YOUTUBE_CHANNEL_ID_28 = "PL1T-A-PVavLLc9-gnyzVmcnpqMUilPe5C"
YOUTUBE_CHANNEL_ID_29 = "PLPXjjzBAKhFOa5F-S9qAYWDc7SfQzWXm4"
YOUTUBE_CHANNEL_ID_30 = "PL152bjytsMC4BOcSOdvFFuJZwWXam8FZF"
YOUTUBE_CHANNEL_ID_31 = "PLdegvhPRrKSuKuqI4IH7nWk-_SCAH9VyX"
YOUTUBE_CHANNEL_ID_32 = "UCPar4XXTkknIRtj-JSjiddw"
YOUTUBE_CHANNEL_ID_33 = "PL48544492E92EEE46"
YOUTUBE_CHANNEL_ID_34 = "PL152bjytsMC5IEbzo4L3uddop8YvCyeXw"
YOUTUBE_CHANNEL_ID_35 = "PLuiMMfezGgfZ9R0gXNosCAB63YcZ4N1IG"
YOUTUBE_CHANNEL_ID_36 = "PL6jkDCwMt49kGNtYI5ZiqexAuTaa7xdqP"
YOUTUBE_CHANNEL_ID_37 = "PLUQCcRUCOfXbn5ushxnuWKRm8wZ2ZLtRA"
YOUTUBE_CHANNEL_ID_38 = "PLMJCZB0MS5-N1ZvlfGRvEVCLjTWa4j_mI"
YOUTUBE_CHANNEL_ID_39 = "PLFp4v4wRLrbyYlimv-IU7MlOjHkWdWO1T"
YOUTUBE_CHANNEL_ID_40 = "UCU4BHh9Dwfd7-I_xTZ5037Q"
YOUTUBE_CHANNEL_ID_41 = "UCdTD-C4s538Z-VGfaaeYh4w"
YOUTUBE_CHANNEL_ID_42 = "UCVBTlb6_rQkWY99ZKi2oBMw"
YOUTUBE_CHANNEL_ID_43 = "PL3E3xn5BmG284rjx3DWakZgXOM4RTj6nJ"
YOUTUBE_CHANNEL_ID_44 = "PLuDCbxChmO1jpI3cVtJ7YYwwmUfcJvxPU"
YOUTUBE_CHANNEL_ID_45 = "PLC4mqmKvz1IYJGKCi6Vt7vojtGs5XJMIU"
YOUTUBE_CHANNEL_ID_46 = "PLC4mqmKvz1IZdPoh205LYYS4w8mi2ZoR1"
YOUTUBE_CHANNEL_ID_47 = "UCGVD7nbWNm6iQecr41f29zQ"
YOUTUBE_CHANNEL_ID_48 = "PL2OZWqbCOozITQXWNd2R4mrPq502d41v0"
YOUTUBE_CHANNEL_ID_49 = "PL152bjytsMC4oS3P5jAh8PrDLSaYHFV17"
YOUTUBE_CHANNEL_ID_50 = "PL152bjytsMC7Zz0dZN6-x2xNscGts5bpi"


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
        title="The First 48",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://i.ytimg.com/i/LMcX3o6FFXWsoalzX6S95Q/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="A&E The First 48 (& After the First 48)Clips",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-x7nvFKXjVwg/AAAAAAAAAAI/AAAAAAAAAAA/tpJcCWlTsWo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Serial Killer World Wide",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-R7lsITEBulA/AAAAAAAAAAI/AAAAAAAAAAA/0O9eq7VmzcI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Serial Killer World Wide II",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-yikz4PmGifk/AAAAAAAAAAI/AAAAAAAAAAA/_1I6j0Qllag/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Serial Killers Documentary",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-P88szeKKXco/AAAAAAAAAAI/AAAAAAAAAAA/3gyJXjx0U54/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Serial Killers Crime Biography",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-IaivFKR8Qw4/AAAAAAAAAAI/AAAAAAAAAAA/dB4hp_E5Yu8/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Serial Killers",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="http://rlv.zcache.com/cereal_killer_icon_mug-r3167267033f04f0dbfa265d214e219bc_x7jgr_8byvr_324.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="48 Hours Mystery",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-IT1TTCwa_wQ/AAAAAAAAAAI/AAAAAAAAAAA/XgQJpbeVK0I/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="48 Hours Mystery Archive",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-X2EMnclj_uc/AAAAAAAAAAI/AAAAAAAAAAA/sO4g5jIyEf8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="American Justice, Cold Case Files",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-jZKR2DenxNo/AAAAAAAAAAI/AAAAAAAAAAA/oYACSETr6ZM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Darkest Hour",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-HhEa5O3_cHQ/AAAAAAAAAAI/AAAAAAAAAAA/NtCPT_ZQJKI/s100-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Crime Inc",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-nZfQCn4jCx0/AAAAAAAAAAI/AAAAAAAAAAA/ccP0Bt1WZ1A/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Real Investigations",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-NRXsJgpve7s/AAAAAAAAAAI/AAAAAAAAAAA/mKBMFXFTXPc/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Killer Instincts",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-lPDxfTTqCIM/AAAAAAAAAAI/AAAAAAAAAAA/lKr2IBLyINc/s100-c-k-no/photo.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="Crime Conversation",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-noP9TQW7gK0/AAAAAAAAAAI/AAAAAAAAAAA/qCllmY8F6u4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Criminal Investigations",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-7yVxzENnGLc/AAAAAAAAAAI/AAAAAAAAAAA/bhBtqb5_xOs/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Uk True Crime Docs",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-CCvSwUqp7gE/AAAAAAAAAAI/AAAAAAAAAAA/njuoaovJd0I/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Juiciest True Crime Shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://i.ytimg.com/vi/RkZ8Q5za_P8/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="True Crime With Aphrodite Jones",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://i.ytimg.com/i/nV6raSmQQA4lj-RcIqJqnA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="On The Case With Paula Zahn",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://i.ytimg.com/i/G57gDyiKKDStpzYWD_vc4A/mq1.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Homicide Hunter",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://i.ytimg.com/i/26fxU9YT9taL-UofF4ciQw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Deadly Women",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://i.ytimg.com/i/pLjYXnVxBEHSF77K-C7lFA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Deadly Affairs",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://i.ytimg.com/i/nrOXSVdLLwD2dtTZihnIRw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nightmare Next Door",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://i.ytimg.com/i/DS55SJzIdnJ-L2UV3nCzGw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Evil Kin",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://i.ytimg.com/i/CAaJXD6KVAaJ9CVGyzwkbA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Surviving Evil",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://i.ytimg.com/i/TqNYHSrUkV8CEz0RZLvC7w/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Who The Bleep Did I Marry",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://i.ytimg.com/i/lbbg7ktw4_vp2zHVDmG47g/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Fatal Vows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://i.ytimg.com/i/fekTW2K9F5uWUs2LM8JwUg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Wives with Knives",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://i.ytimg.com/i/XRCXAKHsjdpeP-8o7KzQXA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Wicked Attraction",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://i.ytimg.com/i/EK7WzBR9KYsA-751KDMo9g/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cold Case Files",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://i.ytimg.com/i/pj-owbX6RPX26-snvu3Z-g/mq1.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Forensic Files (check playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://yt3.ggpht.com/-KQgZxaYcLJY/AAAAAAAAAAI/AAAAAAAAAAA/LsYKB4ZuTDA/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="True Crime",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://yt3.ggpht.com/-1EXMbWLNi0M/AAAAAAAAAAI/AAAAAAAAAAA/vZEr1-vk6eM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Solved",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://i.ytimg.com/i/UPASRpt-YH7_QuzyXIqY7g/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dr. G - Medical Examiner",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://i.ytimg.com/i/XkjiR2jxRh3ug-79JC9fJg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sins and Secrets",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://i.ytimg.com/i/sM-1ZQR_N2t8R43unwlFRA/mq1.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Behind Mansion Walls",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://i.ytimg.com/i/DZq1kEpWNTGzXiDG1-7X3w/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="I Almost Got Away With It",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://i.ytimg.com/i/c42gnH1KH4EfTBmPw7mbtA/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="America's Most Wanted",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://i.ytimg.com/i/ySHuxK6q64qJkMb0r-eFzA/mq1.jpg",
        folder=True ) 

    plugintools.add_item( 
        #action="", 
        title="FilmRise True Crime (check playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://yt3.ggpht.com/-HE_576ROmGc/AAAAAAAAAAI/AAAAAAAAAAA/LpK4lKvntfQ/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Forensic Spider",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://yt3.ggpht.com/-qaRlf8kAR78/AAAAAAAAAAI/AAAAAAAAAAA/x-UZXiWA-dM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Medical Detectives (check playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/-bq84y35JFGI/AAAAAAAAAAI/AAAAAAAAAAA/9XP96zHgkfQ/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sensing Murder",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://i.ytimg.com/i/-oxIrwJDGuGsgbDAfWDK4w/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Body of Evidence",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://yt3.ggpht.com/-c-GnDb1iXBc/AAAAAAAAAAI/AAAAAAAAAAA/ab9Mk96nt8g/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The FBI Files",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="http://www.detectiveconanworld.com/wiki/images/e/e1/FBI_logo.png",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="The New Detectives",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="http://www.iconshock.com/img_vista/XMac/jobs/jpg/private_detective_icon.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Crime Investigation Australia",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://yt3.ggpht.com/-b5GuTl9pLm8/AAAAAAAAAAI/AAAAAAAAAAA/syxbwasgk1A/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="CRIME Inc. Crime shows",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="http://www.eyeonannapolis.net/wp-content/uploads/2009/10/crime-icon.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Real Crime",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://yt3.ggpht.com/-KJ5zq4CVj_E/AAAAAAAAAAI/AAAAAAAAAAA/EYyRhdBsrEs/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="True Crime",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://yt3.ggpht.com/-KJ5zq4CVj_E/AAAAAAAAAAI/AAAAAAAAAAA/EYyRhdBsrEs/s100-c-k-no/photo.jpg",
        folder=True )
run()
