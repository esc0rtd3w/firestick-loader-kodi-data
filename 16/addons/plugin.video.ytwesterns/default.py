# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Western Movies and TV on YouTube Addon by coldkeys
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

addonID = 'plugin.video.ytwesterns'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCvDb4m0vGhPFsBFjwLEQaLg"
YOUTUBE_CHANNEL_ID_2 = "UC7t-Qd8mM_4mox4IypTW38w"
YOUTUBE_CHANNEL_ID_3 = "PLeagipoZmyfnxPGSx-fY9AMyLw-5Qlr6O"
YOUTUBE_CHANNEL_ID_4 = "UCrxdkRkkFQAEBSM0RK3s9VA"
YOUTUBE_CHANNEL_ID_5 = "UCI3jCHxTrdgLs2BNIfSlfSQ"
YOUTUBE_CHANNEL_ID_6 = "UCPUU5swJo5XLqvn77s6FB8g"
YOUTUBE_CHANNEL_ID_7 = "UCUlKudY9luAjzmzszG_sduw"
YOUTUBE_CHANNEL_ID_8 = "UC9DohyHhE0rhKUWAS2xCBDQ"
YOUTUBE_CHANNEL_ID_9 = "PLjqk9ptmQMmPIjjzsh2D3OdqFvOhy3ppj"
YOUTUBE_CHANNEL_ID_10 = "UCFZyTlS3DO-n4Q-hlQybedA"
YOUTUBE_CHANNEL_ID_11 = "UCh51cE9j1n206mAZslHtf6A"
YOUTUBE_CHANNEL_ID_12 = "PLmHgXUJMN1TUNtCvlcfQf423uVxzut71K"
YOUTUBE_CHANNEL_ID_13 = "PL3kLWgOhlYeq0rbUMRnK0Fmd_B1DUFD1V"
YOUTUBE_CHANNEL_ID_14 = "PL3kLWgOhlYerDWdqZvnBeIWlaADfNzroI"
YOUTUBE_CHANNEL_ID_15 = "PLYSD-9macUgnNAyXMqHx72U7AFf2wmb_h"
YOUTUBE_CHANNEL_ID_16 = "PLYSD-9macUgnrb_LyuDpxi792oiaqjXxV"
YOUTUBE_CHANNEL_ID_17 = "UC9VpuT-pzF-nn5ljuvXdUNQ"
YOUTUBE_CHANNEL_ID_18 = "UCcTFn7Se_Ll7z_XpQLQDGUg"
YOUTUBE_CHANNEL_ID_19 = "PLmHgXUJMN1TUn3d9pVQZ_Cs50xmmAki-7"
YOUTUBE_CHANNEL_ID_20 = "PLdwYgKHNxoDuhMUDMyirUV6-nGwY3tkYY"
YOUTUBE_CHANNEL_ID_21 = "PLeagipoZmyfnPw1rsdrEMi_hMi40qAeqJ"
YOUTUBE_CHANNEL_ID_22 = "PLZSwZhmrV90E2S2zLb2xGh8TEuvCy-Mdp"
YOUTUBE_CHANNEL_ID_23 = "PLeagipoZmyfkEJ2XSUeQR40zxHUqVVNX0"
YOUTUBE_CHANNEL_ID_24 = "PLeagipoZmyfms-4x1Zzyzpt-7cAxlUhhl"
YOUTUBE_CHANNEL_ID_25 = "PLeagipoZmyfkbZOE5RPXT5yLRSEhYo12s"
YOUTUBE_CHANNEL_ID_26 = "PLeagipoZmyfls4kEXjloPyDDvGb1q4SNt"
YOUTUBE_CHANNEL_ID_27 = "PLeagipoZmyflNWZHS3m3oWPs8D9EdARW4"
YOUTUBE_CHANNEL_ID_28 = "PL6fJmjt84zZhNVhRHPgOljHzU5xfBhlHB"
YOUTUBE_CHANNEL_ID_29 = "PLZVMGCh7sZUgn0IxbQj8zx6-jl3ZmR2_c"
YOUTUBE_CHANNEL_ID_30 = "PL313ldrGPNBzSwP1J4Id5J4idGnFUOLaL"
YOUTUBE_CHANNEL_ID_31 = "PL313ldrGPNBxWwMhJkyUQi7QeJrVM8G7U"
YOUTUBE_CHANNEL_ID_32 = "PL313ldrGPNBzpvqIJYHnnpKuCcaswsAaJ"
YOUTUBE_CHANNEL_ID_33 = "PL41192DFD0509F2E4"
YOUTUBE_CHANNEL_ID_34 = "PLmHgXUJMN1TW0TmPNRMCLdnLU2FjNFzRO"
YOUTUBE_CHANNEL_ID_35 = "PLmHgXUJMN1TWehukbNnmyl9N91xjRNrM5"
YOUTUBE_CHANNEL_ID_36 = "PLmHgXUJMN1TW93hAv9HPgI5nnm2S1ZKlt"
YOUTUBE_CHANNEL_ID_37 = "PLmHgXUJMN1TU9G-8PLKCe5EF6Stf0ejsH"
YOUTUBE_CHANNEL_ID_38 = "PLmHgXUJMN1TXK9QXtOASZsNSJtvhGD625"
YOUTUBE_CHANNEL_ID_39 = "PLmHgXUJMN1TVOKfuhXc_mUQpHZNkDGD0C"
YOUTUBE_CHANNEL_ID_40 = "UC96dixV7uW4MoKb8OPzjywA"
YOUTUBE_CHANNEL_ID_41 = "UCEEo63Pb787nWP3HVZowk_A"
YOUTUBE_CHANNEL_ID_42 = "PLBiHiGDiFvmgQnQR7bU4uyzskZGWxLpYF"
YOUTUBE_CHANNEL_ID_43 = "UCIHkYsbUAftyCBu1Ylei4-Q"
YOUTUBE_CHANNEL_ID_44 = "PL7YPN8JheNiJouD8ZeyeSEiJCa19ruBnB"
YOUTUBE_CHANNEL_ID_45 = "PLL9eWgl3ccJcAaK19H3oR8_RNTUEap2Ke"
YOUTUBE_CHANNEL_ID_46 = "PLQrspZRY-lP3JNDcsGnvsMjHJN0k2xcwT"
YOUTUBE_CHANNEL_ID_47 = "PL9Pp20u_dumJBl8n0xqiDffkF7M5y-Kih"
YOUTUBE_CHANNEL_ID_48 = "PLsfqROoxmvBVSrkNMtNcVeo8Z5By35JkY"
YOUTUBE_CHANNEL_ID_49 = "PLSVPNK7oJVxvXKklU8vZ2C9nbyyDpwBxt"
YOUTUBE_CHANNEL_ID_50 = "PL7YPN8JheNiL5UHY4Es-LZ0qAgTwbRkRH"

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
        title="Best Western Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-Vxl7c-7yil8/AAAAAAAAAAI/AAAAAAAAAAA/L9onWf7O1Hs/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Landia",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-Z4Lv0UcBo5k/AAAAAAAAAAI/AAAAAAAAAAA/vb7rLWDr9bw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="B Westerns",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-UfzH1mx3yqE/AAAAAAAAAAI/AAAAAAAAAAA/DR6IOKSNiWY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Full Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-FAAJPcDSv-M/AAAAAAAAAAI/AAAAAAAAAAA/8B_TsHiz_b8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western TV Series and Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-4VZmrkcU_j8/AAAAAAAAAAI/AAAAAAAAAAA/q8wqbu6c5-I/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Mania",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-Xr84C-lRqLY/AAAAAAAAAAI/AAAAAAAAAAA/SE1-KWnNDs8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Westerns On The Web",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-8InAo4LXZzI/AAAAAAAAAAI/AAAAAAAAAAA/UhaMtxxn4WI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Wild West Toys",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-Xn4vWNCDVYE/AAAAAAAAAAI/AAAAAAAAAAA/MjIiZeyCUGU/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="1940s & 1950s Western Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-tjlbkWNZxi4/AAAAAAAAAAI/AAAAAAAAAAA/kiXxMgoloVs/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Wildwest Stuff",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-ghyJ1mo0yII/AAAAAAAAAAI/AAAAAAAAAAA/yu1E0eMxGMM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Timeless Western Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-VAmN310PZsY/AAAAAAAAAAI/AAAAAAAAAAA/4wsYX-3YuDg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Golden Age of Cowboy Westerns",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail=icon,
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Life and Legend of Wyatt Earp Season 1",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-FTy1vn-lXDs/AAAAAAAAAAI/AAAAAAAAAAA/emwYm7llCQo/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Life and Legend of Wyatt Earp Season 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-FTy1vn-lXDs/AAAAAAAAAAI/AAAAAAAAAAA/emwYm7llCQo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Life and Legend of Wyatt Earp Season 3",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-vTMJm0iPIkM/AAAAAAAAAAI/AAAAAAAAAAA/gOO7L85qCh0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Life and Legend of Wyatt Earp Season 4",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-vTMJm0iPIkM/AAAAAAAAAAI/AAAAAAAAAAA/gOO7L85qCh0/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Spaghetti Westerns (Bster Slayer)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-FTy1vn-lXDs/AAAAAAAAAAI/AAAAAAAAAAA/emwYm7llCQo/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vintage Western Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://yt3.ggpht.com/-1jLfOTMVTk4/AAAAAAAAAAI/AAAAAAAAAAA/dZ5WzUmGfII/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Roy Rogers - King of The Singing Cowboys",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/G1ZzFGmpb464Bi1D59aW1AW2dqKBV0Ltijnt1ZYfzXbRggjUbUlVzXsIA84V3JnwlJzPzgUgw6A1mG6pf1g=s100-nd",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Lone Ranger Series",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-G3nTMRBLiAw/AAAAAAAAAAI/AAAAAAAAAAA/xRL8MGiXJzE/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Deputy (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://yt3.ggpht.com/-SkptbZ38_NM/AAAAAAAAAAI/AAAAAAAAAAA/BEMSpuZws6E/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Westerns Full Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://yt3.ggpht.com/-4VZmrkcU_j8/AAAAAAAAAAI/AAAAAAAAAAA/q8wqbu6c5-I/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Movies 1950-54",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://yt3.ggpht.com/-R31vu83QiZU/AAAAAAAAAAI/AAAAAAAAAAA/l0rSzGqm81A/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Movies 1945-49",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://yt3.ggpht.com/-R31vu83QiZU/AAAAAAAAAAI/AAAAAAAAAAA/l0rSzGqm81A/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Movies 1940-44",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://yt3.ggpht.com/-R31vu83QiZU/AAAAAAAAAAI/AAAAAAAAAAA/l0rSzGqm81A/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Movies 1935-39",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://yt3.ggpht.com/-R31vu83QiZU/AAAAAAAAAAI/AAAAAAAAAAA/l0rSzGqm81A/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Movies 1930-34",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://yt3.ggpht.com/-R31vu83QiZU/AAAAAAAAAAI/AAAAAAAAAAA/l0rSzGqm81A/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Whiplash (TV Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://i.ytimg.com/i/Tb-7FEByS4kx7h5gacQGNQ/mq1.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="The High Chaparral (TV Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://i.ytimg.com/i/Tb-7FEByS4kx7h5gacQGNQ/mq1.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Annie Oakley Season 1",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://yt3.ggpht.com/-xd3puJZWuB8/AAAAAAAAAAI/AAAAAAAAAAA/ZBULq6xGqOk/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Annie Oakley Season 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-xd3puJZWuB8/AAAAAAAAAAI/AAAAAAAAAAA/ZBULq6xGqOk/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Annie Oakley Season 3",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://yt3.ggpht.com/-xd3puJZWuB8/AAAAAAAAAAI/AAAAAAAAAAA/ZBULq6xGqOk/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Westerns (160 Movies)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://yt3.ggpht.com/-U0SyY_46deU/AAAAAAAAAAI/AAAAAAAAAAA/Y2QtkoPGX0Q/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Adventures of Kit Carson (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://yt3.ggpht.com/-uqJz2ioAEQw/AAAAAAAAAAI/AAAAAAAAAAA/-VqUNzP19eM/s88-c-k-no/photo.jpg",
		folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Billy the Kid (Movies)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://i.ytimg.com/i/zMikEWAs85l-2e82OJtR_Q/mq1.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Stories of the Century (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://i.ytimg.com/i/EocCdijlXKOhq6wQ-ATJzA/mq1.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Range Rider (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://yt3.ggpht.com/nk9-Me7aRhatVpoxiU6uBvPNMC4ITXXT6WTlOJxEIM0wUvbXwCfBnmSme7iu51EF3AtG14k5IkAI0kDFWQ=s100-nd",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tex Ritter Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://yt3.ggpht.com/jfbopVxcXBeG5lmQBuIPfOKI1A0qZh8Qd4qOwcdbA06LdBPmZsZEzFGWXnbhGly0yQEvYT8I9DrCqoq7QA=s100-nd",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tate - Complete Series",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/ly9-dqG0sFslTolPRvUC02phKXxB9AVWZmt8HlVnp2PAlHUx1hCLG08TK_37DbaJ3Yjn9U91TxIJjAUpAps=s100-nd",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Have Gun - Will Travel (Playlist - 6 Seasons)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://yt3.ggpht.com/-zfeHNmljSUw/AAAAAAAAAAI/AAAAAAAAAAA/6sJHQ3XLGTo/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Western Movies and TV (See Playlists)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://i.ytimg.com/i/Ebhb2PTQMT9LTKvzQn8Ffg/mq1.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="TV - 50's and 60's Westerns",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/-W6WWOjTk9sY/AAAAAAAAAAI/AAAAAAAAAAA/K0tLgcaCI0c/s100-c-k-no/photo.jpg",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Good Western Films and TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://yt3.ggpht.com/9dX3fT49qOmgnfKWXY2HKYCakbjJiXpWfiF2A0auRw-zayvGMUyqakpt73DavqGu1mrGRdpM0_VQab9TcQ=s100-nd",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Gunsmoke S1-5 (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://i.ytimg.com/i/rWfEqPWGsw-_tPdZJqtUqg/mq1.jpg?v=5418a0fb",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Gunsmoke S6 (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://i.ytimg.com/i/rWfEqPWGsw-_tPdZJqtUqg/mq1.jpg?v=5418a0fb",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Gunsmoke S9 (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://i.ytimg.com/i/rWfEqPWGsw-_tPdZJqtUqg/mq1.jpg?v=5418a0fb",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Gunsmoke S10 (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://i.ytimg.com/i/rWfEqPWGsw-_tPdZJqtUqg/mq1.jpg?v=5418a0fb",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Gunsmoke Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="https://i.ytimg.com/i/rWfEqPWGsw-_tPdZJqtUqg/mq1.jpg?v=5418a0fb",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Gunsmoke Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://i.ytimg.com/i/rWfEqPWGsw-_tPdZJqtUqg/mq1.jpg?v=5418a0fb",
		folder=True )

    plugintools.add_item( 
        #action="", 
        title="Wanted Dead or Alive (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://i.ytimg.com/i/Pp4BQZmGl6WJOYG1iCidQg/mq1.jpg",
		folder=True )
run()
