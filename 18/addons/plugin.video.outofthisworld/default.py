# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Out of this World Documentaries Addon by coldkeys
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

addonID = 'plugin.video.outofthisworld'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCaasFoY9yYQpOfL00N3nSxg"
YOUTUBE_CHANNEL_ID_2 = "ELHBijOC70VvE"
YOUTUBE_CHANNEL_ID_3 = "ELjOrxDVoNdU0"
YOUTUBE_CHANNEL_ID_4 = "UCtwAqRfw901jAo9JbX3KEHQ"
YOUTUBE_CHANNEL_ID_5 = "UCqi3K5TwaBC9l-YQzlRG0vg"
YOUTUBE_CHANNEL_ID_6 = "UCk_foUwmaHeFhmAZMnEHQsw"
YOUTUBE_CHANNEL_ID_7 = "PLfVuOg1h3Q1fTPmNkVFzjZJR-S2lw3s9H"
YOUTUBE_CHANNEL_ID_8 = "UCuBPlZTF6TGO0g58QgcgsxA"
YOUTUBE_CHANNEL_ID_9 = "UC4Q36FUg_NOHCpxoBv2wQ1g"
YOUTUBE_CHANNEL_ID_10 = "UCrgja_PWykEiFlaYvTjO44w"
YOUTUBE_CHANNEL_ID_11 = "PLjP29lglo5DX-7AhAnZeS05UL9_FSEfk2"
YOUTUBE_CHANNEL_ID_12 = "UCqLr8VyFA9qYPuGSLedT2RQ"
YOUTUBE_CHANNEL_ID_13 = "UCYphOE6nWQiZTmycQG-r-XA"
YOUTUBE_CHANNEL_ID_14 = "PL152bjytsMC5Yujo0JumT9LsXVThaoR-V"
YOUTUBE_CHANNEL_ID_15 = "UChz4wgDoVGWXw_Gpny8lhIA"
YOUTUBE_CHANNEL_ID_16 = "PLxignttj5ONbui8lptBOk-H5Qg_KNHB8a"
YOUTUBE_CHANNEL_ID_17 = "UC2na0DRywwQrXeodGmCt63Q"
YOUTUBE_CHANNEL_ID_18 = "UCoawEOkPOrEYKnQs72RnQGw"
YOUTUBE_CHANNEL_ID_19 = "PLByjNzUI2UG5-bPFOhLh7T2LXL6ML2o5E"
YOUTUBE_CHANNEL_ID_20 = "PLwhOBiXbYauOLQzNLsLzeLs0IkIfFuzuo"
YOUTUBE_CHANNEL_ID_21 = "PLByjNzUI2UG5GKHN2k8gyxNP1bkKPFqK_"
YOUTUBE_CHANNEL_ID_22 = "UCRDVBHaAnhAhh2ykJmFiu_g"
YOUTUBE_CHANNEL_ID_23 = "UCNuf7nY3r6LrLWYONRGv-Xg"
YOUTUBE_CHANNEL_ID_24 = "UCTKuGHAEZsc1Jb1oD2gaW6Q"
YOUTUBE_CHANNEL_ID_25 = "UC_Fb75M4HSsNEwdxZwEXIJQ"
YOUTUBE_CHANNEL_ID_26 = "PLmkjUS2UqPAOQn25fI5g9dCaQ0N-Vz758"
YOUTUBE_CHANNEL_ID_27 = "UCvsye7V9psc-APX6wV1twLg"
YOUTUBE_CHANNEL_ID_28 = "UCSLd3-nGt1fzcYhdh_0Nr0g"
YOUTUBE_CHANNEL_ID_29 = "UCeRIjtKGM0XJugGWDvctxuA"
YOUTUBE_CHANNEL_ID_30 = "UCh-8xfXv8IF90d0SXHns84w"
YOUTUBE_CHANNEL_ID_31 = "UCUkGG6gdLsGjMLf0RabZQZA"
YOUTUBE_CHANNEL_ID_32 = "PL152bjytsMC7SbTJwZMofEBw9goAuyEBk"
YOUTUBE_CHANNEL_ID_33 = "UCjeYqGx0STkSM6iWknsDl3w"
YOUTUBE_CHANNEL_ID_34 = "UCl0T0SKaV5rJU81F_QUCakw"
YOUTUBE_CHANNEL_ID_35 = "UC7TvL4GlQyMBLlUsTrN_C4Q"
YOUTUBE_CHANNEL_ID_36 = "UCvtTGZEcS8mbWdB7prg4QNw"
YOUTUBE_CHANNEL_ID_37 = "UCxo1rU0PA2iSZHkeLO2iaZw"
YOUTUBE_CHANNEL_ID_38 = "UCszHReYtzC5410p9h3xVWEA"
YOUTUBE_CHANNEL_ID_39 = "UCGhbRSOWRoYVlPXX1haANKg"
YOUTUBE_CHANNEL_ID_40 = "PLHjrRqyg8ug-ts0AjzUZGpwh9V08uN0i_"
YOUTUBE_CHANNEL_ID_41 = "UCkJk30CLO4aJL11RIZsv5ow"
YOUTUBE_CHANNEL_ID_42 = "PLAA6438176C65375F"
YOUTUBE_CHANNEL_ID_43 = "PLgrXpjC1QftsN4m06ZWsgppHcrJPO-J0I"
YOUTUBE_CHANNEL_ID_44 = "PLYS2UP0Xbu_bzvxQe3XC5RqL-gVkRMmXt"
YOUTUBE_CHANNEL_ID_45 = "PLlXFGABj3pT6tpo3XrJim2wlNWGjFmAfM"
YOUTUBE_CHANNEL_ID_46 = "UCMZX83bHyIK064n_vLAGulw"
YOUTUBE_CHANNEL_ID_47 = "PL152bjytsMC70EjJ86WiIvxfb-b4iR7Gn"
YOUTUBE_CHANNEL_ID_48 = "PL152bjytsMC4bORPmQTpsfKTdDSA9Y_pr"
YOUTUBE_CHANNEL_ID_49 = "PL152bjytsMC7tXBplCwvAS-aqL-uw72RF"
YOUTUBE_CHANNEL_ID_50 = "PL152bjytsMC4ApPkn7YIMxZk0sveC8qkl"

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
        title=" UFOTV® The Disclosure Movie Network ",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-LzxbTMc5jx8/AAAAAAAAAAI/AAAAAAAAAAA/oJYbn_2y4ec/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFOTV® Presents: Season 1",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://i.ytimg.com/sh/s24l0wQzvvE/showposter.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFOTV® Presents: Season 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://i.ytimg.com/sh/s24l0wQzvvE/showposter.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The WTF Files™",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-e2m0BS8apsg/AAAAAAAAAAI/AAAAAAAAAAA/v1DHpMIVayE/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title=" Disclose Truth TV ",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-8QbaDb5gcG4/AAAAAAAAAAI/AAAAAAAAAAA/GLM9wpNMMkI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="GrahamHancockDotCom",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-y2ic0fpjshA/AAAAAAAAAAI/AAAAAAAAAAA/mqOsEI9dwXw/s100-c-k-no/photo.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="David Icke",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-6eMfz62QtOM/AAAAAAAAAAI/AAAAAAAAAAA/MZlIr7cR7V4/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Third Phase of the Moon",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-VngAwXZ40Ac/AAAAAAAAAAI/AAAAAAAAAAA/csSGfPEeepg/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="E.B.E Extraterrestrial Biological Entity",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-xPwa4vxuwCs/AAAAAAAAAAI/AAAAAAAAAAA/KluzIqc3VQg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Disclosure Nation",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-lfNeciUCA0o/AAAAAAAAAAI/AAAAAAAAAAA/BExVzsACKL0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nibiru and Planet X",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-WWM0lj8yQl0/AAAAAAAAAAI/AAAAAAAAAAA/pqSvMzo4nvY/s100-c-k-no/photo.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Beyond UFOs 2016",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-L0HHPpel3pY/AAAAAAAAAAI/AAAAAAAAAAA/0Pz6bshbTho/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="The Truth Revealed777",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-5Hgv70lbKH4/AAAAAAAAAAI/AAAAAAAAAAA/vdSzmY69pR4/s100-c-k-no/photo.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="*Aliens and UFOs",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-mtGNjrlpS78/AAAAAAAAAAI/AAAAAAAAAAA/0Ahp3_cJ5Yw/s100-c-k-no/photo.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="Mystery/Alien/UFO/Paranormal Matters",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-X7D6WIEQtVg/AAAAAAAAAAI/AAAAAAAAAAA/x3AdzbtZKX0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nibiru is Planet X 2015",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-_VhIRKkteeM/AAAAAAAAAAI/AAAAAAAAAAA/aCfehLao6K4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Project Camelot TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-ZzEy30oVJkw/AAAAAAAAAAI/AAAAAAAAAAA/r8SL1qhauNw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nova",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://yt3.ggpht.com/-OgfbGny2RiI/AAAAAAAAAAI/AAAAAAAAAAA/7qWMPC7zRMA/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="UFO Sightings",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/-8hhmidKoi3w/AAAAAAAAAAI/AAAAAAAAAAA/OYhiVmCq8A8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Red Star Kachina",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-WKXVsqHWLwE/AAAAAAAAAAI/AAAAAAAAAAA/jBse_B2BRns/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Alien Sightings",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://yt3.ggpht.com/-8hhmidKoi3w/AAAAAAAAAAI/AAAAAAAAAAA/OYhiVmCq8A8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFOvni2012",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://yt3.ggpht.com/-_7UcjcoUUcc/AAAAAAAAAAI/AAAAAAAAAAA/mPOtxNCw3ek/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Alien Planet",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://yt3.ggpht.com/-kJoQ7T8i0a4/AAAAAAAAAAI/AAAAAAAAAAA/mZiXb59t0As/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The UFO Agenda 2015",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://yt3.ggpht.com/-HvuNl630RhA/AAAAAAAAAAI/AAAAAAAAAAA/CEbX6j53s-E/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO and Aliens Collected",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://yt3.ggpht.com/-1d1CMPx2-aM/AAAAAAAAAAI/AAAAAAAAAAA/nre84MVTm0k/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO Files",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://i.ytimg.com/i/3FHcND9fX0E7eleSQP4nFQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Alex Jones Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://yt3.ggpht.com/-DbNegouDvyU/AAAAAAAAAAI/AAAAAAAAAAA/QyDM_-5eUFc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Zachary Crooks",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://yt3.ggpht.com/-NW0ur4r9V7k/AAAAAAAAAAI/AAAAAAAAAAA/vrj4_uJGwgY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO Aliens",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://yt3.ggpht.com/-DWiMy45hYI0/AAAAAAAAAAI/AAAAAAAAAAA/YskcZsaSeMA/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Aliens Radio",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://yt3.ggpht.com/-ss6dyrKvhM8/AAAAAAAAAAI/AAAAAAAAAAA/10DZvKMWqO8/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Yolo Yokric - Aliens and UFOs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-Kcn0YYFte6A/AAAAAAAAAAI/AAAAAAAAAAA/Ro6jNZlonZo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Ancient Aliens Season 1 - 10",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Jesse Ventura Off The Grid",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://yt3.ggpht.com/-xA9bGVn0C78/AAAAAAAAAAI/AAAAAAAAAAA/4g6_j2bctyg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ConspiracyScope",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://yt3.ggpht.com/-09O4fhWufxs/AAAAAAAAAAI/AAAAAAAAAAA/8WWyDX9aZxc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Corbett Report",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://yt3.ggpht.com/-18ENytFD7iY/AAAAAAAAAAI/AAAAAAAAAAA/nmL5kOfqUsw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Global Research TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://yt3.ggpht.com/-OMtBL31Dxto/AAAAAAAAAAI/AAAAAAAAAAA/fq8dVNI5eVo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Matrix World Disclosure",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://yt3.ggpht.com/-AGKrpHpcyMw/AAAAAAAAAAI/AAAAAAAAAAA/dfGm4Mtr8EY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="EyezOpenWyde",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://yt3.ggpht.com/-Pt0z08U7jmc/AAAAAAAAAAI/AAAAAAAAAAA/Oiok6hZaVEY/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The UFO Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-u25OrL0u2po/AAAAAAAAAAI/AAAAAAAAAAA/dUnqmskNMq8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Alien Abduction",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://i.ytimg.com/i/uDRV1Wy1eSEy9NAvVudm3Q/mq1.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Aliens Moon Truth Exposed",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://yt3.ggpht.com/-fY_zbuo3qWI/AAAAAAAAAAI/AAAAAAAAAAA/BH9Z3TiwQs8/s100-c-k-no-mo/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO Documentaries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/-uOOpUsuxHfw/AAAAAAAAAAI/AAAAAAAAAAA/TSblknGKCpg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="(Leonard Nimoy)In Search Of ",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://yt3.ggpht.com/-hsZUv5hqBNY/AAAAAAAAAAI/AAAAAAAAAAA/R0wsx3RntNI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Forbidden History Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://yt3.ggpht.com/-e3b6DQRi3Eg/AAAAAAAAAAI/AAAAAAAAAAA/ZHyDt6TAj48/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Alien UFO Radio",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-pqSJ6ix3Oww/AAAAAAAAAAI/AAAAAAAAAAA/yGvJyvJBVw4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Annunaki Radio",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/-k0YKCFnbkbA/AAAAAAAAAAI/AAAAAAAAAAA/LOg2nkS5B8k/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO Hunters",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Forbidden Knowledge",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Ancient Discoveries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail=icon,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Aliens, History and Mystery",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail=icon,
        folder=True )
run()
