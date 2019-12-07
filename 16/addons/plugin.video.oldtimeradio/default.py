# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Old Time Radio Shows on YouTube Addon by coldkeys
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

addonID = 'plugin.video.oldtimeradio'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PLI57FCk6wBfiMqFRdDOaBJb4s6nzUmGBy"
YOUTUBE_CHANNEL_ID_2 = "PLiazYm6CoFzXOd_8A9FJAdvO9ZN9SrUu0"
YOUTUBE_CHANNEL_ID_3 = "PLiazYm6CoFzXhOQ56pTyTWoHaN0bI6B0r"
YOUTUBE_CHANNEL_ID_4 = "PLiazYm6CoFzXlmE1HuJaLrQQZZEjAe4wC"
YOUTUBE_CHANNEL_ID_5 = "PLiazYm6CoFzU-0htz00vdEptxFfVeYOEd"
YOUTUBE_CHANNEL_ID_6 = "PLiazYm6CoFzV3iLrl0eeKz_uSrr1mUTQd"
YOUTUBE_CHANNEL_ID_7 = "PLiazYm6CoFzXFqRFEhLBDlnEzoyrRARs9"
YOUTUBE_CHANNEL_ID_8 = "PLiazYm6CoFzWB8DJ4s5vK5WSqDr8pyQ1q"
YOUTUBE_CHANNEL_ID_9 = "PLiazYm6CoFzXj6zacwex_xgY5KlhzDYjX"
YOUTUBE_CHANNEL_ID_10 = "PLiazYm6CoFzU3wyU2NLk-R4z9VMGSPOYY"
YOUTUBE_CHANNEL_ID_11 = "PLiazYm6CoFzVjoH5GYqGcWRFDWBNXOhXK"
YOUTUBE_CHANNEL_ID_12 = "PLiazYm6CoFzX_OXKTbr_nKtjFxogKnebD"
YOUTUBE_CHANNEL_ID_13 = "PLiazYm6CoFzWolxldJiBqJiZ52ZzRIgiJ"
YOUTUBE_CHANNEL_ID_14 = "PLiazYm6CoFzWfnXKROY243-urFqaBXSfs"
YOUTUBE_CHANNEL_ID_15 = "PLNAKtRwcvjAHZ0PWWjSRzX7gzDHRChlHq"
YOUTUBE_CHANNEL_ID_16 = "PLiazYm6CoFzV7fswhPECHiyE5IIY4oJ2L"
YOUTUBE_CHANNEL_ID_17 = "PLoqfIQD57O1JkVS3F3kkHnSpacysiOXBk"
YOUTUBE_CHANNEL_ID_18 = "PLiazYm6CoFzUMQvirAkL6UPMTEeLO22mk"
YOUTUBE_CHANNEL_ID_19 = "PLaOAo53Qtij4OL35SS-zlBLGTaZd73FZd"
YOUTUBE_CHANNEL_ID_20 = "PLiazYm6CoFzUMsH4uzr03f31cGQMMti6J"
YOUTUBE_CHANNEL_ID_21 = "PLiazYm6CoFzXjJz63aYIMpTFeOm2EtubR"
YOUTUBE_CHANNEL_ID_22 = "PLiazYm6CoFzWJM7_-SeoVN6v059gMb_Cx"
YOUTUBE_CHANNEL_ID_23 = "PLiazYm6CoFzUgHIdGEgSGPq40CuKTPyf9"
YOUTUBE_CHANNEL_ID_24 = "PLHyyT1BfMwmuw2p2NKemHsCDb-OBZMhcj"
YOUTUBE_CHANNEL_ID_25 = "PLI57FCk6wBfirYI1vYEZSyAQm2pLAvZYG"
YOUTUBE_CHANNEL_ID_26 = "PLHyyT1BfMwmtQYC3wIkRe8xHa4ueGSli3"
YOUTUBE_CHANNEL_ID_27 = "PLXxLxaySJVc5C9Xtt7mP3JtRZinrvzzlS"
YOUTUBE_CHANNEL_ID_28 = "PLXxLxaySJVc4KxU595zHY7Y4CBkI8wm4N"
YOUTUBE_CHANNEL_ID_29 = "PLXxLxaySJVc77KTqnyMB1i5dDkvdHz7Dg"
YOUTUBE_CHANNEL_ID_30 = "PLNAKtRwcvjAF3teAqDCgLc8doW1FrvFvI"
YOUTUBE_CHANNEL_ID_31 = "PLNAKtRwcvjAGgfpnpGVfzouamoqMS_jMa"
YOUTUBE_CHANNEL_ID_32 = "PLNAKtRwcvjAHtTw2_xuIC4RfoH3UwFaG0"
YOUTUBE_CHANNEL_ID_33 = "PLNAKtRwcvjAHvjfuf549tlK7tw1sUUa2x"
YOUTUBE_CHANNEL_ID_34 = "PLNAKtRwcvjAFnOPQ3J2W9FiCurhOVcSp6"
YOUTUBE_CHANNEL_ID_35 = "PLNAKtRwcvjAHOTBabMuDwGVXvmz4IwfMS"
YOUTUBE_CHANNEL_ID_36 = "PLMlG8KENs0YMsQaKiUd7JU79Z_GTP-fby"
YOUTUBE_CHANNEL_ID_37 = "PLMlG8KENs0YOmsavS4_Rqbgt72PN2NKXd"
YOUTUBE_CHANNEL_ID_38 = "PLMlG8KENs0YO2b6CV0t-bWdmWHVzMDGtT"
YOUTUBE_CHANNEL_ID_39 = "PLMlG8KENs0YOuXfz5ou0GrD9Pb0f5_Y-T"
YOUTUBE_CHANNEL_ID_40 = "PLMlG8KENs0YOZbPN4QTbI3kIT4udX8KC7"
YOUTUBE_CHANNEL_ID_41 = "PLMlG8KENs0YOWAl-1mWjElGxDrALQvQc8"
YOUTUBE_CHANNEL_ID_42 = "PL6NNdFWTxoprCuGHAEgI8f0GxWH1GoF66"
YOUTUBE_CHANNEL_ID_43 = "PL6NNdFWTxoppTTLVtu38TLnI10rSCyla7"
YOUTUBE_CHANNEL_ID_44 = "PL6NNdFWTxoppDdnPROe9u-9FvhH5LMccA"
YOUTUBE_CHANNEL_ID_45 = "PL6NNdFWTxoppDTan0v4AfZofjALAWsn7p"
YOUTUBE_CHANNEL_ID_46 = "PLMlG8KENs0YP8w5NjDeA_8YER-NGdMsO_"
YOUTUBE_CHANNEL_ID_47 = "PLMlG8KENs0YP_C0cjvtkkOpRAXB2Y1R5y"
YOUTUBE_CHANNEL_ID_48 = "PLMlG8KENs0YP6HY2FDyLSO7__za2UZXUF"
YOUTUBE_CHANNEL_ID_49 = "PLMlG8KENs0YPjyhrgBvFBjqvegqrgUlt8"
YOUTUBE_CHANNEL_ID_50 = "PLMlG8KENs0YMC1mC11eMtUGpm-QsDh81I"
YOUTUBE_CHANNEL_ID_51 = "PLMlG8KENs0YMyyEem-Hx1F-dPsjK34WX1"
YOUTUBE_CHANNEL_ID_52 = "PLMlG8KENs0YMJsTBwFgt_F_w0DVv8GDP0"
YOUTUBE_CHANNEL_ID_53 = "PLMlG8KENs0YMSxfpGbkO5D-XtwrYyrXLc"
YOUTUBE_CHANNEL_ID_54 = "PLMlG8KENs0YO63zJvU8NZmGVKUaQr93g2"
YOUTUBE_CHANNEL_ID_55 = "PLI57FCk6wBfitSlrymCitUugQgsQw_K4Z"
YOUTUBE_CHANNEL_ID_56 = "PLI57FCk6wBfh1ORK1H4fQsxQUMufUVezN"
YOUTUBE_CHANNEL_ID_57 = "PLI57FCk6wBfiWKR6VULpNP8DGWGgcojwc"
YOUTUBE_CHANNEL_ID_58 = "PLI57FCk6wBfgrK_9jUbC-dUT_ti5YRqNp"
YOUTUBE_CHANNEL_ID_59 = "PLaOAo53Qtij7A7R1jynDlko1tCG5kwyq-"
YOUTUBE_CHANNEL_ID_60 = "PLI57FCk6wBfie57aS9nWdMoFZergFdfph"
YOUTUBE_CHANNEL_ID_61 = "PLI57FCk6wBfgpsCsyfQ12Bj6FwgZ0X9UT"
YOUTUBE_CHANNEL_ID_62 = "PLI57FCk6wBfiVXuQs32aIOPhEKq1FKeZ6"
YOUTUBE_CHANNEL_ID_63 = "PLI57FCk6wBfgPOsKSvqh8wjwN8fvYSWZN"
YOUTUBE_CHANNEL_ID_64 = "PLI57FCk6wBfgWY-2rTGBooWgqNhixYJ0n"
YOUTUBE_CHANNEL_ID_65 = "PLI57FCk6wBfiWlMidOzaoqgmTz4RJxHet"
YOUTUBE_CHANNEL_ID_66 = "PLI57FCk6wBfi9rTCGzXaTYtOunljroqsF"
YOUTUBE_CHANNEL_ID_67 = "PLI57FCk6wBfhuKWu4ab3ARUDVJXSCWd2Z"
YOUTUBE_CHANNEL_ID_68 = "PLc1girBhY3GmaYcn5Igf4r56ytxc5Gdxx"
YOUTUBE_CHANNEL_ID_69 = "PLc1girBhY3GkQ5sN-ogt_ZWGRBsDpOo-g"
YOUTUBE_CHANNEL_ID_70 = "PLc1girBhY3GmkYsrrrnoShCTUz8bugmXu"
YOUTUBE_CHANNEL_ID_71 = "PLc1girBhY3Gl8Ihn-Xm5XMB0qG2JITbBz"
YOUTUBE_CHANNEL_ID_72 = "PLc1girBhY3GmjOPS5vXCIga6BOfoAp2la"
YOUTUBE_CHANNEL_ID_73 = "PLc1girBhY3Gk_S1ptUpb6Dj12LiRfEsOB"
YOUTUBE_CHANNEL_ID_74 = "PLc1girBhY3Gk22xqWzN-tTNhVLGIIL1G5"
YOUTUBE_CHANNEL_ID_75 = "PLc1girBhY3Gn9pB348iuFlwNKs0x9C116"
YOUTUBE_CHANNEL_ID_76 = "PLJm2etPj4-MYlykH8VeSx_9v9SlR5gGWX"
YOUTUBE_CHANNEL_ID_77 = "PLJm2etPj4-MZTwcHDYpX3M5s7C2EtSwqF"
YOUTUBE_CHANNEL_ID_78 = "PLJm2etPj4-Mbd2VNzG2grAy-t36ibB0nY"
YOUTUBE_CHANNEL_ID_79 = "PLJm2etPj4-MbbB2BZ5n-ccsWpOvS1NxOY"
YOUTUBE_CHANNEL_ID_80 = "PLJm2etPj4-MbO4N21TJXP6C83_w_vj0bL"
YOUTUBE_CHANNEL_ID_81 = "PLJm2etPj4-Mb2oKZCJONgfg6M4Ge81i6G"
YOUTUBE_CHANNEL_ID_82 = "PLiazYm6CoFzXUbSqScJ45mDi-quTMCFGy"
YOUTUBE_CHANNEL_ID_83 = "PLiazYm6CoFzUOJBMJRDFSelw37qHiDoYF"
YOUTUBE_CHANNEL_ID_84 = "PLaOAo53Qtij6OqyhWdf1tMjKspgN44Ylq"
YOUTUBE_CHANNEL_ID_85 = "PLaOAo53Qtij5lPDN3YUm8XnG9dUiXWb4Y"
YOUTUBE_CHANNEL_ID_86 = "PLaOAo53Qtij4sCIWehXZ4V5UqTyMuNdxh"
YOUTUBE_CHANNEL_ID_87 = "PLaOAo53Qtij7Vlo4VUqaFXI23u9Y4L_kC"
YOUTUBE_CHANNEL_ID_88 = "PLaOAo53Qtij7UmxXwGuOoZdcV1kxRo9oS"
YOUTUBE_CHANNEL_ID_89 = "PLaOAo53Qtij6DDYstTewjNZM1Bu2UPgND"
YOUTUBE_CHANNEL_ID_90 = "PL95kcp6o1r6cI7QNDCrQmTHfoqhN6PBrk"
YOUTUBE_CHANNEL_ID_91 = "PL2E9Q9ftPti-9jy2rQySGsbPrn4Jr2Ddk"
YOUTUBE_CHANNEL_ID_92 = "PLNLriyzwBU5iWTi1UGjZxsoRrsqPJVrNm"
YOUTUBE_CHANNEL_ID_93 = "PLNLriyzwBU5iUelxZH6ZQcjL6Ar0W2E28"
YOUTUBE_CHANNEL_ID_94 = "PLiazYm6CoFzUrCyrKcN6KKjXrd2A2NEAa"
YOUTUBE_CHANNEL_ID_95 = "PLZz7wyBx0WO9salsCfqxtTycCLnqhjzDG"
YOUTUBE_CHANNEL_ID_96 = "PLZz7wyBx0WO-FJzCwwCd3Y_8X2Rs99tr4"
YOUTUBE_CHANNEL_ID_97 = "PLZz7wyBx0WO_QjF9Wze4yGzuT9WY-x5lC"
YOUTUBE_CHANNEL_ID_98 = "PLZz7wyBx0WO8gOtuswg2fXLPDfGjyJNeB"
YOUTUBE_CHANNEL_ID_99 = "PLZz7wyBx0WO8faGY07MF12Qhy9AU349lG"
YOUTUBE_CHANNEL_ID_100 = "PLZz7wyBx0WO_rygv1_aYFxuAx2cAYcsxy"

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
        title="Nightfall",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dragnet",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Suspense",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Whistler",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Richard Diamond, P.I.",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bright Star",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="The Saint (Vincent Price)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Let George Do It",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Lights Out",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Theater-5",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Jack Benny Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LUX Radio Theatre",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="INNER SANCTUM MYSTERIES",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Escape",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="X Minus One (All 122 episodes)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-tlh_nBbwCrQ/AAAAAAAAAAI/AAAAAAAAAAA/BfBtLhBfKBE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mindwebs",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dimension X",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-2ov5t_ii-BI/AAAAAAAAAAI/AAAAAAAAAAA/o0wl_JGNV6g/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Superman!",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Green Hornet",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/-bTis6lKyFAg/AAAAAAAAAAI/AAAAAAAAAAA/UF85UprLE6E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Strange Tales",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Lone Ranger",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Gunsmoke",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dark Fantasy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="7th Dimension",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://yt3.ggpht.com/-tlN59Mg1nYY/AAAAAAAAAAI/AAAAAAAAAAA/BkpJkZovasY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Planet Man",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Exploring Tomorrow",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://yt3.ggpht.com/-tlN59Mg1nYY/AAAAAAAAAAI/AAAAAAAAAAA/BkpJkZovasY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Lightning Jim",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://yt3.ggpht.com/-znk7d9RPRwE/AAAAAAAAAAI/AAAAAAAAAAA/GsOg1sIoyK0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Tom Mix Ralston Straight Shooters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://yt3.ggpht.com/-znk7d9RPRwE/AAAAAAAAAAI/AAAAAAAAAAA/GsOg1sIoyK0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tennessee Jed",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://yt3.ggpht.com/-znk7d9RPRwE/AAAAAAAAAAI/AAAAAAAAAAA/GsOg1sIoyK0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2000 Plus",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://yt3.ggpht.com/-tlh_nBbwCrQ/AAAAAAAAAAI/AAAAAAAAAAA/BfBtLhBfKBE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Adventures of Philip Marlowe, Private Detective",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-tlh_nBbwCrQ/AAAAAAAAAAI/AAAAAAAAAAA/BfBtLhBfKBE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dick Tracy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://yt3.ggpht.com/-tlh_nBbwCrQ/AAAAAAAAAAI/AAAAAAAAAAA/BfBtLhBfKBE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Red Skelton Program Vol.1",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://yt3.ggpht.com/-tlh_nBbwCrQ/AAAAAAAAAAI/AAAAAAAAAAA/BfBtLhBfKBE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Red Skelton Program Vol.2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://yt3.ggpht.com/-tlh_nBbwCrQ/AAAAAAAAAAI/AAAAAAAAAAA/BfBtLhBfKBE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Old Time Radio Commercials",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://yt3.ggpht.com/-tlh_nBbwCrQ/AAAAAAAAAAI/AAAAAAAAAAA/BfBtLhBfKBE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tarzan & the Diamond of Asher",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mr. District Attorney",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mystery House",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Hall of Fantasy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Mysterious Traveler",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Strange Dr. Weird",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Yours Truly, Johnny Dollar",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/-1OtWWG9uyXQ/AAAAAAAAAAI/AAAAAAAAAAA/azbY7GMp7WI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="21st Precinct",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://yt3.ggpht.com/-1OtWWG9uyXQ/AAAAAAAAAAI/AAAAAAAAAAA/azbY7GMp7WI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Amos n Andy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://yt3.ggpht.com/-1OtWWG9uyXQ/AAAAAAAAAAI/AAAAAAAAAAA/azbY7GMp7WI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="You Are There",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-1OtWWG9uyXQ/AAAAAAAAAAI/AAAAAAAAAAA/azbY7GMp7WI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Shadow of Fu Manchu",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Journey Into Space",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Weird Circle",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The New Adventures of Nero Wolfe",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Chandu the Magician",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Hermit's Cave",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_51+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Shadow",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_52+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="I Love a Mystery",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_53+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Peril",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_54+"/",
        thumbnail="https://yt3.ggpht.com/-ldxXivggG8Q/AAAAAAAAAAI/AAAAAAAAAAA/Rf9SIRe7OiU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sherlock Holmes - Graham Armitage and Kerry Jordan",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_55+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dr Kildare",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_56+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Broadway is My Beat",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_57+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sealed Book",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_58+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Bold Venture - Humphrey Bogart and Lauren Bacall",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_59+"/",
        thumbnail="https://yt3.ggpht.com/-bTis6lKyFAg/AAAAAAAAAAI/AAAAAAAAAAA/UF85UprLE6E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="A Life of Bliss - BBC George Cole",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_60+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Blue Beetle",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_61+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Adventures by Morse",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_62+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nick Carter Master Detective",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_63+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Barrie Craig, Confidential Investigator",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_64+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sherlock Holmes Basil Rathbone & Nigel Bruce",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_65+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Secret Agent K7",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_66+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Crime Classics",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_67+"/",
        thumbnail="https://yt3.ggpht.com/-DJM0QaDcOiI/AAAAAAAAAAI/AAAAAAAAAAA/FeHCe6RnkP0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Adventures Of Captain Horatio Hornblower",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_68+"/",
        thumbnail="https://yt3.ggpht.com/-W_K64G6XRAA/AAAAAAAAAAI/AAAAAAAAAAA/M_tV5UZSKeg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Air Adventures Of Biggles",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_69+"/",
        thumbnail="https://yt3.ggpht.com/-W_K64G6XRAA/AAAAAAAAAAI/AAAAAAAAAAA/M_tV5UZSKeg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Hop Harrigan",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_70+"/",
        thumbnail="https://yt3.ggpht.com/-W_K64G6XRAA/AAAAAAAAAAI/AAAAAAAAAAA/M_tV5UZSKeg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Hollywood Theater Productions",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_71+"/",
        thumbnail="https://yt3.ggpht.com/-W_K64G6XRAA/AAAAAAAAAAI/AAAAAAAAAAA/M_tV5UZSKeg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Fibber McGee and Molly",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_72+"/",
        thumbnail="https://yt3.ggpht.com/-W_K64G6XRAA/AAAAAAAAAAI/AAAAAAAAAAA/M_tV5UZSKeg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Damon Runyon Theater",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_73+"/",
        thumbnail="https://yt3.ggpht.com/-W_K64G6XRAA/AAAAAAAAAAI/AAAAAAAAAAA/M_tV5UZSKeg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Five Minute Mysteries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_74+"/",
        thumbnail="https://yt3.ggpht.com/-W_K64G6XRAA/AAAAAAAAAAI/AAAAAAAAAAA/M_tV5UZSKeg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Jungle Jim",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_75+"/",
        thumbnail="https://yt3.ggpht.com/-W_K64G6XRAA/AAAAAAAAAAI/AAAAAAAAAAA/M_tV5UZSKeg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="CBS Radio Mystery Theater",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_76+"/",
        thumbnail="https://yt3.ggpht.com/-erAqTlFVJGk/AAAAAAAAAAI/AAAAAAAAAAA/4lZSYSAGWUk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Night Watch",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_77+"/",
        thumbnail="https://yt3.ggpht.com/-erAqTlFVJGk/AAAAAAAAAAI/AAAAAAAAAAA/4lZSYSAGWUk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Unit 99",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_78+"/",
        thumbnail="https://yt3.ggpht.com/-erAqTlFVJGk/AAAAAAAAAAI/AAAAAAAAAAA/4lZSYSAGWUk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Father Knows Best",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_79+"/",
        thumbnail="https://yt3.ggpht.com/-erAqTlFVJGk/AAAAAAAAAAI/AAAAAAAAAAA/4lZSYSAGWUk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ozzie and Harriet",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_80+"/",
        thumbnail="https://yt3.ggpht.com/-erAqTlFVJGk/AAAAAAAAAAI/AAAAAAAAAAA/4lZSYSAGWUk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="You Bet Your Life",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_81+"/",
        thumbnail="https://yt3.ggpht.com/-erAqTlFVJGk/AAAAAAAAAAI/AAAAAAAAAAA/4lZSYSAGWUk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="LUCY My Favorite Husband",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_82+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Roy Rogers",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_83+"/",
        thumbnail="https://yt3.ggpht.com/-GG6OlWHkexo/AAAAAAAAAAI/AAAAAAAAAAA/_GQjCMijT3w/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Fat Man",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_84+"/",
        thumbnail="https://yt3.ggpht.com/-bTis6lKyFAg/AAAAAAAAAAI/AAAAAAAAAAA/UF85UprLE6E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Big Town",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_85+"/",
        thumbnail="https://yt3.ggpht.com/-bTis6lKyFAg/AAAAAAAAAAI/AAAAAAAAAAA/UF85UprLE6E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Casey Crime Photographer",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_86+"/",
        thumbnail="https://yt3.ggpht.com/-bTis6lKyFAg/AAAAAAAAAAI/AAAAAAAAAAA/UF85UprLE6E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Stand by for Crime",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_87+"/",
        thumbnail="https://yt3.ggpht.com/-bTis6lKyFAg/AAAAAAAAAAI/AAAAAAAAAAA/UF85UprLE6E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Scarlet Pimpernel",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_88+"/",
        thumbnail="https://yt3.ggpht.com/-bTis6lKyFAg/AAAAAAAAAAI/AAAAAAAAAAA/UF85UprLE6E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="NBC Short Story",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_89+"/",
        thumbnail="https://yt3.ggpht.com/-bTis6lKyFAg/AAAAAAAAAAI/AAAAAAAAAAA/UF85UprLE6E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BBC Radio Dramas",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_90+"/",
        thumbnail="https://yt3.ggpht.com/-8EjKDh376Uw/AAAAAAAAAAI/AAAAAAAAAAA/-91t-1CKRD0/s176-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BBC SciFi-Horror",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_91+"/",
        thumbnail="https://yt3.ggpht.com/-8EjKDh376Uw/AAAAAAAAAAI/AAAAAAAAAAA/-91t-1CKRD0/s176-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Horror Tales",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_92+"/",
        thumbnail="https://yt3.ggpht.com/-fCIdmK6QC6Y/AAAAAAAAAAI/AAAAAAAAAAA/jgVl76cfBUk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Creepy Tales",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_93+"/",
        thumbnail="https://yt3.ggpht.com/-fCIdmK6QC6Y/AAAAAAAAAAI/AAAAAAAAAAA/jgVl76cfBUk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Our Miss Brooks",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_94+"/",
        thumbnail="https://yt3.ggpht.com/-hHJJCxoYaWs/AAAAAAAAAAI/AAAAAAAAAAA/kHCwJXKCRqw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SciFi Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_95+"/",
        thumbnail="https://yt3.ggpht.com/-oOtfC1KYk04/AAAAAAAAAAI/AAAAAAAAAAA/ei8KDrkKybc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Macabre Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_96+"/",
        thumbnail="https://yt3.ggpht.com/-oOtfC1KYk04/AAAAAAAAAAI/AAAAAAAAAAA/ei8KDrkKybc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mystery and Thriller Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_97+"/",
        thumbnail="https://yt3.ggpht.com/-oOtfC1KYk04/AAAAAAAAAAI/AAAAAAAAAAA/ei8KDrkKybc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_98+"/",
        thumbnail="https://yt3.ggpht.com/-oOtfC1KYk04/AAAAAAAAAAI/AAAAAAAAAAA/ei8KDrkKybc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Comedy Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_99+"/",
        thumbnail="https://yt3.ggpht.com/-oOtfC1KYk04/AAAAAAAAAAI/AAAAAAAAAAA/ei8KDrkKybc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Old Time Radio Series",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_100+"/",
        thumbnail="https://yt3.ggpht.com/-oOtfC1KYk04/AAAAAAAAAAI/AAAAAAAAAAA/ei8KDrkKybc/s100-c-k-no/photo.jpg",
        folder=True )
run()
