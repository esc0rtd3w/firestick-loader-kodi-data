# -*- coding: utf-8 -*-
#------------------------------------------------------------
# The X Factor International
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.XFactorInternational'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID1 = "UCex1kBiVgk1EEsf0Fi4D8HA"
YOUTUBE_CHANNEL_ID2 = "xfactoralbania"
YOUTUBE_CHANNEL_ID3 = "TheXFactorArabia"
YOUTUBE_CHANNEL_ID4 = "XFactorArmeniaShant"
YOUTUBE_CHANNEL_ID5 = "thexfactoraustralia"
YOUTUBE_CHANNEL_ID6 = "BGXFactor"
YOUTUBE_CHANNEL_ID7 = "elfactorxus"
YOUTUBE_CHANNEL_ID8 = "xfactorslovensko"
YOUTUBE_CHANNEL_ID9 = "XFactorDR1"
YOUTUBE_CHANNEL_ID10 = "xfactorge"
YOUTUBE_CHANNEL_ID11 = "xfactorglobal"
YOUTUBE_CHANNEL_ID12 = "XFactorIndia"
YOUTUBE_CHANNEL_ID13 = "XFactorIndonesiaFM"
YOUTUBE_CHANNEL_ID14 = "XFactorIsrael"
YOUTUBE_CHANNEL_ID15 = "xfactoritalia"
YOUTUBE_CHANNEL_ID16 = "XFactorKazakhstan"
YOUTUBE_CHANNEL_ID17 = "XFactorNL"
YOUTUBE_CHANNEL_ID18 = "UCxoJBfDcAMKL5jZZoKXILdg"
YOUTUBE_CHANNEL_ID19 = "XFactorDR1"
YOUTUBE_CHANNEL_ID20 = "XFactorOkinawaJP"
YOUTUBE_CHANNEL_ID21 = "XFactorPhilippines"
YOUTUBE_CHANNEL_ID22 = "TheXFactorPortugal"
YOUTUBE_CHANNEL_ID23 = "thexfactora1"
YOUTUBE_CHANNEL_ID24 = "ukrainexfactor"
YOUTUBE_CHANNEL_ID25 = "TheXFactorUK"
YOUTUBE_CHANNEL_ID26 = "TheXFactorUSA"
YOUTUBE_CHANNEL_ID27 = "nhantobianvietnam"

# Entry point
def run():
    plugintools.log("XFactorInternational.run")
    
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
    plugintools.log("XFactorInternational.main_list "+repr(params))
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Adria",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID1+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Albania",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID2+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Arabia",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID3+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Armenia",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID4+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Australia",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID5+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Bulgaria",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID6+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Colombia",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID7+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Czech / Slovakia",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID8+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Denmark",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID9+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Georgia",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID10+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Global",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID11+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor India",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID12+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Indonesia",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID13+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Israel",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID14+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Italy",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID15+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Kazakhstan",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID16+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Netherlands",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID17+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor New Zealand",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID18+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Norway",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID19+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Okinawa",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID20+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Philippines",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID21+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Portugal",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID22+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Romania",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID23+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Ukraine",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID24+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor UK",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID25+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor USA",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID26+"/",
        thumbnail=icon,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="X Factor Vietnam",
        url="plugin://plugin.video.youtube/user/"+YOUTUBE_CHANNEL_ID27+"/",
        thumbnail=icon,
        folder=True )


run()