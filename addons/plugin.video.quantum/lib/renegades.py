# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Renegades Darts by Coldkeys & AP
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: AP
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon

base_icons = 'http://herovision.x10host.com/freeview/'
icon = base_icons+'renegades.png'
fanart = base_icons+'renegadesfanart.jpg'


YOUTUBE_CHANNEL_ID_1 = "PLMYrbKMmyUBkk1g5q7pf-25FhdeBhl4_v"
YOUTUBE_CHANNEL_ID_2 = "PLMYrbKMmyUBmUIm2utCjUowDlz82cngVp"
YOUTUBE_CHANNEL_ID_3 = "PLMYrbKMmyUBnv8HYHpRc6nM4cNvE0a4pe"
YOUTUBE_CHANNEL_ID_4 = "PLMYrbKMmyUBlYBt59cD5uq2HkzCkc6hda"
YOUTUBE_CHANNEL_ID_5 = "PLYJ3r6AEHB6oK0Clmhse5oK6-x9AfYYeg"
YOUTUBE_CHANNEL_ID_6 = "PLqeJQVNr6CBjrmJ9uT4FvskyUy8qXfTN9"
YOUTUBE_CHANNEL_ID_7 = "PLZxPj4ksDAuh6bM-EkdIV3-Z-IeRnhHhp"
YOUTUBE_CHANNEL_ID_8 = "PLnJp9laBeYwnuXkUN34-eb72c9-pfy7RV"
YOUTUBE_CHANNEL_ID_9 = "PLnJp9laBeYwkKv6Fy5HbwMn_M8vparKvS"
YOUTUBE_CHANNEL_ID_10 = "PLnJp9laBeYwk8K1YpqnnzGd8Qs2C-s5-b"
YOUTUBE_CHANNEL_ID_11 = "PLnJp9laBeYwnvU5JVfv3ZrbdkqHocnG25"
YOUTUBE_CHANNEL_ID_12 = "PLZxPj4ksDAuiVm0g0mUz2h36LM6jEURjT"
YOUTUBE_CHANNEL_ID_13 = "PLnJp9laBeYwk7ffET96mfb_iAc3QAB1AA"
YOUTUBE_CHANNEL_ID_14 = "PLnJp9laBeYwk-jeojc48e2fbWFZyYv3FR"
YOUTUBE_CHANNEL_ID_15 = "PLnJp9laBeYwlm84rLocw1P_SA3g15ygB1"
YOUTUBE_CHANNEL_ID_16 = "PLZxPj4ksDAuiYb8pmueTTRBUZcmsYho5P"
YOUTUBE_CHANNEL_ID_17 = "PLZxPj4ksDAuiowydh00GxY4iJ9rd86tZw"
YOUTUBE_CHANNEL_ID_18 = "PLZxPj4ksDAuh0IvTIiPRSc3ASuK12uk9S"
YOUTUBE_CHANNEL_ID_19 = "PLnJp9laBeYwnfHkibLVj-9Op4gmmrvU_t"
YOUTUBE_CHANNEL_ID_20 = "PLZxPj4ksDAuiaiiJOWL5lREDBpF9BrufI"
YOUTUBE_CHANNEL_ID_21 = "PLZxPj4ksDAuhKaBqqiPVLEelJ5q3hbs6G"
YOUTUBE_CHANNEL_ID_22 = "PLZxPj4ksDAug0FSsOgAnAGg8psO_RjyQ3"
YOUTUBE_CHANNEL_ID_23 = "PLZxPj4ksDAujRjiGtI-Ngv_71E0Zf9Bhb"
YOUTUBE_CHANNEL_ID_24 = "PLZxPj4ksDAuhWyWBgOBhEDULBh_i_JEtl"
YOUTUBE_CHANNEL_ID_25 = "PLnJp9laBeYwlxGf1qZJDd5FkRYbkV59Ij"
YOUTUBE_CHANNEL_ID_26 = "PLnJp9laBeYwmLwWDkQK7k8Pc-aIpW51JX"
YOUTUBE_CHANNEL_ID_27 = "PLnJp9laBeYwkiGQtKLGs5QgwtOyy4Jceu"
YOUTUBE_CHANNEL_ID_28 = "PLZxPj4ksDAujQf4j-FrrUV4RaU9AxlWe9"
YOUTUBE_CHANNEL_ID_29 = "PLZxPj4ksDAui-oWgruL1ZcSSm4Cpy-JSz"
YOUTUBE_CHANNEL_ID_30 = "PL0S9lXWhMeorIQoiPP5oTW7BMdaL3HEJX"
YOUTUBE_CHANNEL_ID_31 = "PL152bjytsMC53tUup7EsvBq1l19m1YTLx"
YOUTUBE_CHANNEL_ID_32 = "PLZxPj4ksDAuhPWmv7JdczjVkrPo_aaa2b"
YOUTUBE_CHANNEL_ID_33 = "UChp18JEiARNLS3AHUS6gYpg"
YOUTUBE_CHANNEL_ID_34 = "PL152bjytsMC6Dty0wlSwL2kc_MlkX9orS"
YOUTUBE_CHANNEL_ID_35 = "PLZxPj4ksDAuhhcm0T8k3pi-BKqA8f1Fmj"
YOUTUBE_CHANNEL_ID_36 = "PLZxPj4ksDAugQCMcEAbNcvWzRmXryIciV"
YOUTUBE_CHANNEL_ID_37 = "PLZxPj4ksDAuj4hawQsACxLKrI-ePQNPM5"

# Entry point
def run():
    plugintools.log("docu.run")
    
    # Get params
    params = plugintools.get_params()
    main_list(params)    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="[COLOR red]SELECT PLAYLISTS[/COLOR] 2016 PDC World Darts Championships",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/PDC Worlds 2016.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2016 Premier League",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2016 premier league.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2016 Premier League SD",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2016 premier league.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2016 Coral UK Open",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2016 Coral UK Open.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2016 Dutch Darts Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Dutch Masters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2016 BDO World Darts Championship",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2016 BDO WDC.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2016 PDC World Championship (All in One)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/PDC Worlds 2016.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2016 PDC Unibet Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2016 PDC Unibet Masters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 Grand Slam",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2015 Grand Slam.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 World Series Of Darts Finals",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2015 World Series of Darts Finals.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 World Grand Prix",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/World Grand Prix.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 European Darts Grand Prix",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Eropean Darts Grand Prix.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 World Cup",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2015 World Cup.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 European Darts Championship",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/European Darts Championship.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 European Darts Matchplay",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/European Darts Matchplay.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 European Darts Open",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Eropean Darts Open.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 BDO World Trophy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2015 BD0 World Trophy.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 Dutch Darts Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Dutch Masters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 Japan Darts Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/jap masters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 World Matchplay",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2015 World Matchplay.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 German Darts Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/gERMAN maSTERS.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 German Darts Championship",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/German Darts Championship.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 The Unibet Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2015 Unibet Masters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 Coral UK Open",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2015 Coral UK Open.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 Dubai Duty Free Darts Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Dubain Masters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 Auckland Darts Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Aukland Masters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 Sydney Darts Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Sydney Darts masters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 Perth Darts Masters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Perth Darts Masters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 Premier League",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2015 Premier League.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Gold Darts",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Gold Darts.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Darts Walk on Songs",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/darts walk on music.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Story of Darts",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/History of Darts.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="9 Dart Finishes",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/9 Darters.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ladies Darts",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/Womwns Darts.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 World Darts Championship",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/PDC Worlds 2015.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="2015 International Darts Open",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/2105 International Darts Open.jpg",
		fanart=fanart,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="BDO World Championships 2015",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="special://home/addons/plugin.video.renegadesdarts/resources/bdo 2015.jpg",
		fanart=fanart,
        folder=True )
