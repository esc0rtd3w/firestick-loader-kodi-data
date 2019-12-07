# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Vevo Music Addon by coldkeys
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

addonID = 'plugin.video.yt-vevo'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PL7KLwyJCC7Qx3UC8uj-qLIsOdd5OmkNHY"
YOUTUBE_CHANNEL_ID_2 = "PL7KLwyJCC7QyO1kXUEH0BZa7PUJuxi6mR"
YOUTUBE_CHANNEL_ID_3 = "PL7KLwyJCC7QzpNciVGe-7K6ShC3MzL3vd"
YOUTUBE_CHANNEL_ID_4 = "PL7KLwyJCC7QyXUZLdnHDbBIjBZZSOFRKk"
YOUTUBE_CHANNEL_ID_5 = "PL7KLwyJCC7QzsTdkQn0lS-PpsmJSn5_uE"
YOUTUBE_CHANNEL_ID_6 = "PL7KLwyJCC7QzwRsEqbMNaw1licwhD3coa"
YOUTUBE_CHANNEL_ID_7 = "PL7KLwyJCC7QwU_zIa5NvH5m1Sqd6cZh81"
YOUTUBE_CHANNEL_ID_8 = "PL7KLwyJCC7QznHKIubp_Sx0x3tuSX-IvB"
YOUTUBE_CHANNEL_ID_9 = "PL7KLwyJCC7Qz2QotQhsF2JCMvIxfvsiEF"
YOUTUBE_CHANNEL_ID_10 = "PL7KLwyJCC7QxZs9uf0pE5b6sjfKLuDzMJ"
YOUTUBE_CHANNEL_ID_11 = "PL6ZLc-zZUnxlkB9t8CcpFZeV6V5I_cVgu"
YOUTUBE_CHANNEL_ID_12 = "PL7KLwyJCC7QwbQ634fgqfM3RsH8iZiYsW"
YOUTUBE_CHANNEL_ID_13 = "PL7KLwyJCC7QypFLl4_z-kuNztBI-wb9sz"
YOUTUBE_CHANNEL_ID_14 = "PLvFYFNbi-IBF76wtqVJyf9nZ9Y3O8eUUz"
YOUTUBE_CHANNEL_ID_15 = "PLhS3DcL9XnJiyhbMAUPOK9d0qazofnb7O"
YOUTUBE_CHANNEL_ID_16 = "PL7C00E83736FB02C3"
YOUTUBE_CHANNEL_ID_17 = "PLWRJVI4Oj4IaYIWIpFlnRJ_v_fIaIl6Ey"
YOUTUBE_CHANNEL_ID_18 = "PLMC9KNkIncKvYin_USF1qoJQnIyMAfRxl"
YOUTUBE_CHANNEL_ID_19 = "PLcvLv4MM0CssVtrLWdFiRMxFlIH3daXaT"
YOUTUBE_CHANNEL_ID_20 = "PLFLjA-BCYmWE2_6bBuBahJpoKxbE_l82f"
YOUTUBE_CHANNEL_ID_21 = "PLs9DD5S4uo9XQWV7ab4PHf4vVLVQFNmSc"
YOUTUBE_CHANNEL_ID_22 = "PL7A8182052E59571A"
YOUTUBE_CHANNEL_ID_23 = "PLirAqAtl_h2pRAtj2DgTa3uWIZ3-0LKTA"
YOUTUBE_CHANNEL_ID_24 = "PLTZ5G8FX5UCNMMKGWa3r6Jwa7FmiE59Qs"
YOUTUBE_CHANNEL_ID_25 = "PLh_bmn34ZDQH_Yulbv-fvT3XZDrA0BKe7"
YOUTUBE_CHANNEL_ID_26 = "AdeleVEVO"
YOUTUBE_CHANNEL_ID_27 = "shakiraVEVO"
YOUTUBE_CHANNEL_ID_28 = "ArianaGrandeVevo"
YOUTUBE_CHANNEL_ID_29 = "MeghanTrainorVEVO"
YOUTUBE_CHANNEL_ID_30 = "EnriqueIglesiasVEVO"
YOUTUBE_CHANNEL_ID_31 = "RickyMartinVEVO"
YOUTUBE_CHANNEL_ID_32 = "Maroon5VEVO"
YOUTUBE_CHANNEL_ID_33 = "PLF9970C3DF72CA06D"
YOUTUBE_CHANNEL_ID_34 = "PLEDC89F5582FE3601"
YOUTUBE_CHANNEL_ID_35 = "PL88B0CBA209D81A95"
YOUTUBE_CHANNEL_ID_36 = "acdcVEVO"
YOUTUBE_CHANNEL_ID_37 = "AerosmithVEVO"
YOUTUBE_CHANNEL_ID_38 = "journeyVEVO"
YOUTUBE_CHANNEL_ID_39 = "TaylorSwiftVEVO"
YOUTUBE_CHANNEL_ID_40 = "KatyPerryVEVO"
YOUTUBE_CHANNEL_ID_41 = "BryanAdamsVEVO"
YOUTUBE_CHANNEL_ID_42 = "U2VEVO"
YOUTUBE_CHANNEL_ID_43 = "TakeThatVEVO"
YOUTUBE_CHANNEL_ID_44 = "OneDirectionVEVO"
YOUTUBE_CHANNEL_ID_45 = "DemiLovatoVEVO"
YOUTUBE_CHANNEL_ID_46 = "BritneySpearsVEVO"
YOUTUBE_CHANNEL_ID_47 = "LadyGagaVEVO"
YOUTUBE_CHANNEL_ID_48 = "beyonceVEVO"
YOUTUBE_CHANNEL_ID_49 = "ShaniaTwainVEVO"
YOUTUBE_CHANNEL_ID_50 = "AviciiOfficialVEVO"

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
        title="Vevo UK Indie / Rock / Alt Playlist",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://i.ytimg.com/vi/QpQrf-_C5DE/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vevo UK Urban Playlist",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://i.ytimg.com/vi/S5028rvSolE/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vevo UK Pop Playlist",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://i.ytimg.com/vi/cK90915clqQ/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vevo UK Dance / Electro Playlist",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://i.ytimg.com/vi/EgqUJOudrcM/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vevo UK Must See Music Videos",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://i.ytimg.com/vi/S_tmBZWtQEI/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Track Of The Week - Vevo UK",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://i.ytimg.com/vi/CJu6Fh1FSEo/default.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Vevo UK @ The Great Escape Festival 2015",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://i.ytimg.com/vi/izGFK2FxfGs/default.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Vevo UK - VVVintage",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://i.ytimg.com/vi/0P4A1K4lXDo/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vevo UK - VVVision",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://i.ytimg.com/vi/GQIRuU2U5hg/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vevo UK - VVV",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://i.ytimg.com/vi/DzwkcbTQ7ZE/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="M TOP POP MUSIC VEVO 500",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://i.ytimg.com/vi/nfWlot6h_JM/default.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Vevo UK @ The Great Escape Festival 2014",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://i.ytimg.com/vi/XhA5m5Uqroo/default.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Vevo UK - BRITS nominations 2014",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://i.ytimg.com/vi/7E0fVfectDo/default.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="2015 Pop Music / Billboard / Vevo",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://i.ytimg.com/vi/QcIy9NiNbmo/default.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="VEVO Playlist Best New Music 2015",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://i.ytimg.com/vi/6GUm5g8SG4o/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="TOP40 ARTISTS-VEVO",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://i.ytimg.com/vi/1TsVjvEkc4s/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Top 50 Best Songs of VEVO",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://i.ytimg.com/vi/CevxZvSJLk8/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="VEVO Playlist The Best OF 2014-2015",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://i.ytimg.com/vi/hHUbLv4ThOo/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vevo 2014/2015 playlist",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://i.ytimg.com/vi/gCJ3rmiZFr8/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="VEVO Top Radio Hits August 28th, 2015 ",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://i.ytimg.com/vi/xqtUuHFAtzg/default.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Vevo Top Playlist 2013 ",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://i.ytimg.com/vi/nmcdLOjGVzw/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vevo Top Hit List",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://i.ytimg.com/vi/wyx6JDQCslE/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Most Viewed VEVO Videos of All Time",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://i.ytimg.com/vi/pRpeEdMmmQ0/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Disney Music VEVO ",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://i.ytimg.com/vi/MDz4a9AlQ94/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Heavy Metal VEVO",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://i.ytimg.com/vi/cOVzXYEU3Bk/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Adele on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://yt3.ggpht.com/-Pmv3XiLq6i0/AAAAAAAAAAI/AAAAAAAAAAA/PzA830mDGNo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Shakira on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://yt3.ggpht.com/-Kcd3KMxoqzw/AAAAAAAAAAI/AAAAAAAAAAA/EvhGpQ4rsh8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ariana Grande on Vevo",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://yt3.ggpht.com/-u_W-R7bGk1c/AAAAAAAAAAI/AAAAAAAAAAA/u6lamzb3BPc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Meghan Trainor on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://i.ytimg.com/vi/EgqUJOudrcM/default.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Enrique Iglesias on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://yt3.ggpht.com/-qsK10MKa204/AAAAAAAAAAI/AAAAAAAAAAA/pWY83V_O3Rg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ricky Martin on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-449IETfmGog/AAAAAAAAAAI/AAAAAAAAAAA/aogt33hqNWY/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Maroon 5 on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://i.ytimg.com/vi/09R8_2nJtjg/default.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Michael Jackson VEVO",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://yt3.ggpht.com/-cxzTJzTVVTA/AAAAAAAAAAI/AAAAAAAAAAA/8VwUHJpcrAA/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="VEVO Eminem",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://yt3.ggpht.com/-NzI5Ni67ppc/AAAAAAAAAAI/AAAAAAAAAAA/7wGQowTOWWg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bon Jovi VEVO",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://yt3.ggpht.com/-TpyyOhl9BLs/AAAAAAAAAAI/AAAAAAAAAAA/8bDOJp-pnYk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ACDC on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://i.ytimg.com/vi/gEPmA3USJdI/default.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Aerosmith on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://yt3.ggpht.com/-_IIeJ-B0gxc/AAAAAAAAAAI/AAAAAAAAAAA/iZ6Y65lj59c/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Journey on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://yt3.ggpht.com/-aGTH-laFf5w/AAAAAAAAAAI/AAAAAAAAAAA/30VvEVGBmy4/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Taylor Swift on Vevo",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-PS6pgnf-7pY/AAAAAAAAAAI/AAAAAAAAAAA/QCBjV6iZUBI/s100-c-k-no/photo.jpg",
        folder=True ) 

    plugintools.add_item( 
        #action="", 
        title="Katy Perry on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://yt3.ggpht.com/-rt3CHrjtobI/AAAAAAAAAAI/AAAAAAAAAAA/Bcmdk1F2-kY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bryan Adams on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://yt3.ggpht.com/-jU6vCs-4a-8/AAAAAAAAAAI/AAAAAAAAAAA/ShMJf7Aovo0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="U2VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/-IRqYLwPI4vo/AAAAAAAAAAI/AAAAAAAAAAA/sOVEV3oP7hM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Take That on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://yt3.ggpht.com/-PUyx0Q3fXJ8/AAAAAAAAAAI/AAAAAAAAAAA/kHJt3cjtN0Y/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="One Direction on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://yt3.ggpht.com/-QRypZt--uYA/AAAAAAAAAAI/AAAAAAAAAAA/Y8-NLYzQzZc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Demi Lovato on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-4ZQuQ5F6XyA/AAAAAAAAAAI/AAAAAAAAAAA/PVsLQqUbs2Y/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Britney Spears on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/-RlIlmd-s60c/AAAAAAAAAAI/AAAAAAAAAAA/ARGHhCBuBjY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Lady Gaga on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://yt3.ggpht.com/-dcILwG2R9Mw/AAAAAAAAAAI/AAAAAAAAAAA/Jn9461K2F_s/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Beyoncé on Vevo",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="https://yt3.ggpht.com/-UqZ1JKav00Q/AAAAAAAAAAI/AAAAAAAAAAA/YKBnbgUTIKU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Shania Twain on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://yt3.ggpht.com/-FnPyfO_CL9A/AAAAAAAAAAI/AAAAAAAAAAA/LtxkiBnK8rM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Avicii on VEVO",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://yt3.ggpht.com/-KaOunkYkbGM/AAAAAAAAAAI/AAAAAAAAAAA/J8En5dobEgI/s100-c-k-no/photo.jpg",
        folder=True )
run()
