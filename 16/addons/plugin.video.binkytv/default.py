# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Binky TV special thanks to original authors of the code
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: Dandymedia
#------------------------------------------------------------

import os
import sys, dandy
import plugintools
import xbmc,xbmcaddon, xbmcplugin
from addon.common.addon import Addon

addonID = 'plugin.video.binkytv'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')
FANART = local.getAddonInfo('fanart')



def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if addon.get_setting('auto-view') == 'true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )


YOUTUBE_CHANNEL_ID_1 = "UCbt63GNsB5wet6NO3dmhssA"
YOUTUBE_CHANNEL_ID_2 = "UCRXXQgZZsMIxXpFncK019DA"
YOUTUBE_CHANNEL_ID_3 = "UCLsooMJoIpl_7ux2jvdPB-Q"
YOUTUBE_CHANNEL_ID_4 = "UCIX0Z-09kLkf-96-StW3hAw"
YOUTUBE_CHANNEL_ID_5 = "UCbCmjCuTUZos6Inko4u57UQ"
YOUTUBE_CHANNEL_ID_6 = "UCZzfOkvfLKdKYEWAZ_Vc0zg"
YOUTUBE_CHANNEL_ID_7 = "UCMU_RNU6KR49ZE8KmOcpdnA"
YOUTUBE_CHANNEL_ID_8 = "UCn--vKxbXBYt_b0lKJ0JEnw"
YOUTUBE_CHANNEL_ID_9 = "UCcvkRvee98FqqUmXN_dwOUw"
YOUTUBE_CHANNEL_ID_10 = "UCBnZ16ahKA2DZ_T5W0FPUXg"
YOUTUBE_CHANNEL_ID_11 = "UCJkWoS4RsldA1coEIot5yDA"
YOUTUBE_CHANNEL_ID_12 = "UCwynFfAvCF2kiRSMWiozQHg"
YOUTUBE_CHANNEL_ID_13 = "UCU_If3OQp9FPHoP1BteFNlA"
YOUTUBE_CHANNEL_ID_14 = "UCbmw4dLid589QTC7xRi0DdA"
YOUTUBE_CHANNEL_ID_15 = "UCwOS0K6uKOqoAWU7MUEtxaQ"
YOUTUBE_CHANNEL_ID_16 = "UC6zPzUJo8hu-5TzUk8IEC2Q"
YOUTUBE_CHANNEL_ID_17 = "UCeUYwh-WiIoG47ECQvQxKsA"
YOUTUBE_CHANNEL_ID_18 = "UCc-YCLZsBzb3tytzEDToZVw"
YOUTUBE_CHANNEL_ID_19 = "UCMfZ_z0LUm805JOZLktl2QQ"
YOUTUBE_CHANNEL_ID_20 = "UCoookXUzPciGrEZEXmh4Jjg"
YOUTUBE_CHANNEL_ID_21 = "UCxezak0GpjlCenFGbJ2mpog"
YOUTUBE_CHANNEL_ID_22 = "UCZA2NJWgiWtLQZPfMhhEZUQ"
YOUTUBE_CHANNEL_ID_23 = "UCB0ABGbdSggBXLF0UdN4d5A"
YOUTUBE_CHANNEL_ID_24 = "UCKAqou7V9FAWXpZd9xtOg3Q"
YOUTUBE_CHANNEL_ID_25 = "UCqdGW_m8Rim4FeMM29keDEg"
YOUTUBE_CHANNEL_ID_26 = "UCGAIzfT0d0nj3KVsdMzIqrA"
YOUTUBE_CHANNEL_ID_27 = "UCncFzSeWqySvOXEbQoEJsZg"
YOUTUBE_CHANNEL_ID_28 = "UCGydrkfIhUDNCotYQI8TJhA"
YOUTUBE_CHANNEL_ID_29 = "UCzoFjzSkbrDD1GHsz2YNLig"
YOUTUBE_CHANNEL_ID_30 = "UCug61OHMkz5GgJkeyhxdepQ"
YOUTUBE_CHANNEL_ID_31 = "UCcJT_hEkkQ03NAzp_6NEBiw"
YOUTUBE_CHANNEL_ID_32 = "UChRHU6dbz5cpM2qVBK0Omng"
YOUTUBE_CHANNEL_ID_33 = "UCq-phhvqJi5_5CTMBh0JfeA"
YOUTUBE_CHANNEL_ID_34 = "UC0j36_NCIX_eSc1nXfNGXVQ"
YOUTUBE_CHANNEL_ID_35 = "UCqrVPwN_DhavUC386xH9SDw"
YOUTUBE_CHANNEL_ID_36 = "UCKe-7-MbrHXAUB3hYTa6pkw"
YOUTUBE_CHANNEL_ID_37 = "UCydekQV_GkprQFYMdgc8e6A"
YOUTUBE_CHANNEL_ID_38 = "UCi0Q60-9chMTWjYVC__M4EA"
YOUTUBE_CHANNEL_ID_39 = "UChddokv0fxIN3BS-KZpxFfA"
YOUTUBE_CHANNEL_ID_40 = "PLQcEfNZdUr8yEpvWYR9DXB5PVJNR_8gmw"
YOUTUBE_CHANNEL_ID_41 = "UCTn45orVsFOsNZHxAJcZK5g"
YOUTUBE_CHANNEL_ID_42 = "UCURCSaXYhIsnsiK-jFFZg3w"
YOUTUBE_CHANNEL_ID_43 = "UC7Gf2tZ8coTX2ckTPgn62iQ"
YOUTUBE_CHANNEL_ID_44 = "UCoHJXadQIxxMT69kHWt0zOQ"
YOUTUBE_CHANNEL_ID_45 = "UCrNnk0wFBnCS1awGjq_ijGQ"
YOUTUBE_CHANNEL_ID_46 = "UCJnzLbkXEPTbnGo-FWaiLWg"
YOUTUBE_CHANNEL_ID_47 = "UCG4dadF2w8Z95qz-vJ3WkqQ"
YOUTUBE_CHANNEL_ID_48 = "UC5XMF3Inoi8R9nSI8ChOsdQ"
YOUTUBE_CHANNEL_ID_49 = "UC7Pq3Ko42YpkCB_Q4E981jw"
YOUTUBE_CHANNEL_ID_50 = "UCtBOJ9bEAoMOY9keGK6p2hQ"
YOUTUBE_CHANNEL_ID_51 = "UCAJnyTWJPpKXuwgWQDdNWrQ"
YOUTUBE_CHANNEL_ID_52 = "UC56cowXhoqRWHeqfSJkIQaA"
YOUTUBE_CHANNEL_ID_53 = "UC8NFs-VWUsyuq4zaYVVMgCQ"
YOUTUBE_CHANNEL_ID_54 = "UC_qs3c0ehDvZkbiEbOj6Drg"
YOUTUBE_CHANNEL_ID_55 = "UC3hGM2kxOs8vRYCcvfH6vuw"
YOUTUBE_CHANNEL_ID_56 = "UCsoPu95aN_ODIxTDkfxVtZg"
YOUTUBE_CHANNEL_ID_57 = "UCjF2lVpoUweXPGf0oRJcP0A"
YOUTUBE_CHANNEL_ID_58 = "UCDCNmuaOXOo25Yn4mbMHhhQ"
YOUTUBE_CHANNEL_ID_59 = "UCO0vPDAqN7BTK9kNAeP3sKw"
YOUTUBE_CHANNEL_ID_60 = "UCzsrOcypBagRDCYF7gTm8-A"
YOUTUBE_CHANNEL_ID_61 = "UCvthuVsurPaVz2a7_4LepGg"
YOUTUBE_CHANNEL_ID_62 = "UC2UhuvjTIrR0Ck2KrkvRcuA"
YOUTUBE_CHANNEL_ID_63 = "UC_pZxiIq8BRJwG55Wt83WOw"
YOUTUBE_CHANNEL_ID_64 = "UCotX63w9fF1eTCjda7Ux3Rw"
YOUTUBE_CHANNEL_ID_65 = "UC5vVe2R4ucoMzJP53o38Yaw"
YOUTUBE_CHANNEL_ID_66 = "UCR6Cv_7e_t6M9Sah7LveKzQ"
YOUTUBE_CHANNEL_ID_67 = "UC-qWJlvaPME3MWvrY-yjXeA"
YOUTUBE_CHANNEL_ID_68 = "UCVE91qOw9Ke8EsK95lMuF2Q"
YOUTUBE_CHANNEL_ID_69 = "UC4Hdb26_xnPQsntwLazMqYw"
YOUTUBE_CHANNEL_ID_70 = "UC1jhiDqp-jIYR07Ini8Jamw"
YOUTUBE_CHANNEL_ID_71 = "UCvkvmLBdHodQ-a-6LeYFP0Q"
YOUTUBE_CHANNEL_ID_72 = "UCB_2_OiPFh6FdUvp50_maug"
YOUTUBE_CHANNEL_ID_73 = "UCXVCgDuD_QCkI7gTKU7-tpg"
YOUTUBE_CHANNEL_ID_74 = "UCIKrW85KBiqsoV2F19xqa_g"
YOUTUBE_CHANNEL_ID_75 = "UChz5aEi3dfrDVC8-YJsMUDA"
YOUTUBE_CHANNEL_ID_76 = "UCs0upBDG-dCAxy8_VDPE5XA"
YOUTUBE_CHANNEL_ID_77 = "UCvwEc1IYISugIBeRkubSXYw"
YOUTUBE_CHANNEL_ID_78 = "UC6AXdTXoeD4ipBCmiuGJ14w"
YOUTUBE_CHANNEL_ID_79 = "UCDBQdJsUA9i8Had_jXCP0bg"
YOUTUBE_CHANNEL_ID_80 = "UCcdwLMPsaU2ezNSJU1nFoBQ"
YOUTUBE_CHANNEL_ID_81 = "UCe1VpF4wS_kdcjyTRSXBcnQ"
YOUTUBE_CHANNEL_ID_82 = "UCNTakNQwoAqVtPSORzswT_A"
YOUTUBE_CHANNEL_ID_83 = "UCe2lzwsff4Jr-CrMxDVVF5A"
YOUTUBE_CHANNEL_ID_84 = "UCQgcmn4OVaKczXEo45iT_fA"
YOUTUBE_CHANNEL_ID_85 = "UCfAgtYEsL74EcAtCKw2B8pA"
YOUTUBE_CHANNEL_ID_86 = "UChLD9gaCK_KzPLIb-3IYq0w"
YOUTUBE_CHANNEL_ID_87 = "UC-M9eLhclbe16sDaxLzc0ng"
YOUTUBE_CHANNEL_ID_88 = "UCc4JF_QPXdjbG_Dn3cvaXwg"
YOUTUBE_CHANNEL_ID_89 = "UCzM5cusUeyQzl2MRU9J3TsQ"
YOUTUBE_CHANNEL_ID_90 = "UCx1xhxQyzR4TT6PmXO0khbQ"
YOUTUBE_CHANNEL_ID_91 = ""
YOUTUBE_CHANNEL_ID_92 = "UChGJGhZ9SOOHvBB0Y4DOO_w"
YOUTUBE_CHANNEL_ID_93 = "UCWr4vlkj5xXQ4bSXNeTT2AA"
YOUTUBE_CHANNEL_ID_94 = "UCZkSuKAy5kMnZXoxo1PrmJQ"
YOUTUBE_CHANNEL_ID_95 = "UCb69PhsHzsorirJDlxaIXlg"
YOUTUBE_CHANNEL_ID_96 = "UC44eGZ76AJLHAxPaJ_MW2RA"
YOUTUBE_CHANNEL_ID_97 = "UC59ejpMDHCZESZid3Q4UGvg"

# Entry point
def run():
    setView('tvshows', 'tvshows-view')
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
        title="Wow English TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_90+"/",
        thumbnail="https://yt3.ggpht.com/-PjUXR-RD3eg/AAAAAAAAAAI/AAAAAAAAAAA/Fg0UYIANp9Y/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
    
    plugintools.add_item( 
        #action="", 
        title="Mister Maker",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_55+"/",
        thumbnail="https://yt3.ggpht.com/-cyd_xvFNML0/AAAAAAAAAAI/AAAAAAAAAAA/uxVC7CTOEJg/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
	
    plugintools.add_item( 
        #action="", 
        title="Busy Beavers",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-gB_SFlcGzDc/AAAAAAAAAAI/AAAAAAAAAAA/KwtbUnJTQTQ/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="The Official Pat & Stan",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_87+"/",
        thumbnail="https://yt3.ggpht.com/-P7aVCHRMw38/AAAAAAAAAAI/AAAAAAAAAAA/tD6gmMo5cRw/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Gus the Gummy Gator",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_94+"/",
        thumbnail="https://yt3.ggpht.com/-liFdFhXD0PY/AAAAAAAAAAI/AAAAAAAAAAA/xtHKZ8M-WAw/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True ) 
        
    plugintools.add_item( 
        #action="", 
        title="TheEngineeringFamily",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_96+"/",
        thumbnail="https://yt3.ggpht.com/-_-N-tzhDFxM/AAAAAAAAAAI/AAAAAAAAAAA/f6doRBA1hUg/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True ) 
        
    plugintools.add_item( 
        #action="", 
        title="T-Series Kids Hut",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_75+"/",
        thumbnail="https://yt3.ggpht.com/-3zC9Flf99b0/AAAAAAAAAAI/AAAAAAAAAAA/ipWpDSEjYTM/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Nursery Rhyme Street",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-iALq_ddya5I/AAAAAAAAAAI/AAAAAAAAAAA/xZ3XR3PkxuE/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Ryan ToysReview",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_92+"/",
        thumbnail="https://yt3.ggpht.com/-pABd64iD4ig/AAAAAAAAAAI/AAAAAAAAAAA/gZhIgw3BnCs/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Super Simple Songs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="http://cdn.shopify.com/s/files/1/0177/6170/products/sss1-cd_1_large.jpg?v=1357867121",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Boj",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_86+"/",
        thumbnail="https://yt3.ggpht.com/-HFbv0a6CPjo/AAAAAAAAAAI/AAAAAAAAAAA/9dh7KJPs_1s/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Little Heroes",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_97+"/",
        thumbnail="https://yt3.ggpht.com/-XBvth65GilA/AAAAAAAAAAI/AAAAAAAAAAA/PU8xmo2u-0M/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Tractor Tom",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_89+"/",
        thumbnail="https://yt3.ggpht.com/-TN1ih4Az918/AAAAAAAAAAI/AAAAAAAAAAA/wV9Lj-WPewg/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

        
    plugintools.add_item( 
        #action="", 
        title="The Wiggles",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_65+"/",
        thumbnail="https://yt3.ggpht.com/-m0-rgNGYBUo/AAAAAAAAAAI/AAAAAAAAAAA/pOL1ZD7ef5s/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Humf – Official Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_88+"/",
        thumbnail="https://yt3.ggpht.com/-EacgsO89Fzc/AAAAAAAAAAI/AAAAAAAAAAA/XU1pYdrEFAk/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Videogyan 3D Rhymes",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_76+"/",
        thumbnail="https://yt3.ggpht.com/-ZcK0CHXP4Eo/AAAAAAAAAAI/AAAAAAAAAAA/DtRJZEaeDjQ/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Combo Panda",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_95+"/",
        thumbnail="https://yt3.ggpht.com/-_4JHfHG6q2A/AAAAAAAAAAI/AAAAAAAAAAA/z7MOD8Ts-Wk/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="TinySchool TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-GKF9gp5kPTA/AAAAAAAAAAI/AAAAAAAAAAA/RTTvkaJ4UyE/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Baby Big Mouth",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_93+"/",
        thumbnail="https://yt3.ggpht.com/-jR-nVOpmQkw/AAAAAAAAAAI/AAAAAAAAAAA/aK-6m6meSt8/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Baby Nursery TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_85+"/",
        thumbnail="https://yt3.ggpht.com/-xfBM42loxPA/AAAAAAAAAAI/AAAAAAAAAAA/3Py9maz575I/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Play-Doh Time for kids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/-WiahwXmuQyM/AAAAAAAAAAI/AAAAAAAAAAA/n5nXUTe2bbU/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Max & Ruby",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_57+"/",
        thumbnail="https://yt3.ggpht.com/-GeQNGbMg0Yc/AAAAAAAAAAI/AAAAAAAAAAA/eFm3ckJNyBw/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Telmo and Tula",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_77+"/",
        thumbnail="https://yt3.ggpht.com/-OxW5KxmgJVg/AAAAAAAAAAI/AAAAAAAAAAA/LnNowvRA49w/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Cool School",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://yt3.ggpht.com/-3Yeznf9-cqI/AAAAAAAAAAI/AAAAAAAAAAA/qf09GPK8AQo/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="ABCkidTV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="http://ecx.images-amazon.com/images/I/51V8MrZu5TL._SY300_.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SimpleKidsCrafts",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://yt3.ggpht.com/-7iJBXJxEnU8/AAAAAAAAAAI/AAAAAAAAAAA/KoyEk1otJqg/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Toddler Fun Learning",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-CszZY89JGBA/AAAAAAAAAAI/AAAAAAAAAAA/1k3MQc5znAU/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Reading Rainbow",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_66+"/",
        thumbnail="https://yt3.ggpht.com/-7P-NCgD50GA/AAAAAAAAAAI/AAAAAAAAAAA/RftsJzzoGeg/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="The Glumpers",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_78+"/",
        thumbnail="https://yt3.ggpht.com/-7cS--nGwolY/AAAAAAAAAAI/AAAAAAAAAAA/yVT6FdFFySg/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="HooplaKidz Shows",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-IAbvFu-I_f0/AAAAAAAAAAI/AAAAAAAAAAA/asCsxzqaQ-4/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="ShopkinsWorld",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-jPfU68yA4yo/AAAAAAAAAAI/AAAAAAAAAAA/BKo01shIosI/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Binkie.TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-WhVgRo5IyXc/AAAAAAAAAAI/AAAAAAAAAAA/ZWaVblU-sdk/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Talking Tom",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_58+"/",
        thumbnail="https://yt3.ggpht.com/-u1ihm184kug/AAAAAAAAAAI/AAAAAAAAAAA/Fo5Oe2c1_C0/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="National Geographic Kids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_73+"/",
        thumbnail="https://yt3.ggpht.com/-P5-cf3rJSO0/AAAAAAAAAAI/AAAAAAAAAAA/NJZz-F6mIIM/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="ChuChu TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-QHPC9emY_8c/AAAAAAAAAAI/AAAAAAAAAAA/03fPGkHcBbk/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Mother Goose Club",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-CjtfMnhAf90/AAAAAAAAAAI/AAAAAAAAAAA/9x0cv1cw3-8/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Kids Learning Videos",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-xy6rXhNqql0/AAAAAAAAAAI/AAAAAAAAAAA/YQB3DbpRdZ0/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Baby Einstein",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://yt3.ggpht.com/-aRd660Gwyzg/AAAAAAAAAAI/AAAAAAAAAAA/_1rP7GM5bvk/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Kids Tv Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-co8gqPEZ4wg/AAAAAAAAAAI/AAAAAAAAAAA/ns5vMzc8vzM/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Kids Live Shows",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-eqqPmAIvb7o/AAAAAAAAAAI/AAAAAAAAAAA/j9XSYw35IxY/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="Cartoon Candy",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://yt3.ggpht.com/-eDshGeqRoVg/AAAAAAAAAAI/AAAAAAAAAAA/ijrVpSZsWRk/s500-c-k-no/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="TuTiTuTV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-635pSGg_Lus/AAAAAAAAAAI/AAAAAAAAAAA/fgSiEDUO18Y/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Finger Family Songs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://yt3.ggpht.com/-aQwW1USzNzY/AAAAAAAAAAI/AAAAAAAAAAA/hUUu2VkFQIU/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="HooplaKidz TV",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/-KWRYIA7c9zg/AAAAAAAAAAI/AAAAAAAAAAA/kut-rS4LEFU/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Sesame Street",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-Udx0C3ZTHUg/AAAAAAAAAAI/AAAAAAAAAAA/3BE1yYHQccs/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Yo Gabba Gabba!",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://yt3.ggpht.com/-DCqlRFygCMs/AAAAAAAAAAI/AAAAAAAAAAA/OmWJ9YLZviE/s500-c-k-no-rj-c0xffffff/photo.jpg",     
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="The Muppets",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://yt3.ggpht.com/-DF7PtesCPOY/AAAAAAAAAAI/AAAAAAAAAAA/j3KDERgDhEs/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="LittleBabyBum",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://yt3.ggpht.com/-KLfbkE3zovQ/AAAAAAAAAAI/AAAAAAAAAAA/gMZ_6qxvEXw/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="FunToyzCollector",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://yt3.ggpht.com/-sSB36cFW0N4/AAAAAAAAAAI/AAAAAAAAAAA/4XxC7rLRwKo/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Curious George",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://yt3.ggpht.com/-Z41LgJ__J-k/AAAAAAAAAAI/AAAAAAAAAAA/Ym0GFh7SQVo/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Little Bear",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://yt3.ggpht.com/-aQ33_1asR-o/AAAAAAAAAAI/AAAAAAAAAAA/z31urOa08xY/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Pancake Manor",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_79+"/",
        thumbnail="https://yt3.ggpht.com/-ISA36nBEfjw/AAAAAAAAAAI/AAAAAAAAAAA/xaBV7DGklqU/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Cartoon Network UK",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://yt3.ggpht.com/-4Y1X3fG0jnc/AAAAAAAAAAI/AAAAAAAAAAA/YvRmVQf8A-w/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Mr Bean Cartoon World",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://yt3.ggpht.com/-9U_o8flA1eU/AAAAAAAAAAI/AAAAAAAAAAA/ldkupLh4fSk/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Bananas In Pyjamas",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://yt3.ggpht.com/-936XDyWfeFQ/AAAAAAAAAAI/AAAAAAAAAAA/50ICHKrArV0/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Treehouse Direct",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-sM-29i4j5Wc/AAAAAAAAAAI/AAAAAAAAAAA/eLcPzriOQvc/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Care Bears",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://yt3.ggpht.com/-j-_LtMovH-o/AAAAAAAAAAI/AAAAAAAAAAA/26zxuZ00uCg/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Miffy & Friends",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://yt3.ggpht.com/-2VZQhR9iWVg/AAAAAAAAAAI/AAAAAAAAAAA/kVmoDD78SXQ/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Fifi and the Flowertots",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://yt3.ggpht.com/-pMSYklXQ7Qc/AAAAAAAAAAI/AAAAAAAAAAA/bO1VDklXc7Q/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Postman Pat",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://yt3.ggpht.com/-U8DSI9QezcE/AAAAAAAAAAI/AAAAAAAAAAA/LmSTwzNzgao/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Olivia The Pig",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://yt3.ggpht.com/-P0x9zgCVph0/AAAAAAAAAAI/AAAAAAAAAAA/MmZ-7LwedKs/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Little Charley Bear",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://yt3.ggpht.com/-zIdNRTkjo8Y/AAAAAAAAAAI/AAAAAAAAAAA/-G_hOj3T7ik/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
	
    plugintools.add_item( 
        #action="", 
        title="Epic Fun for Kids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_74+"/",
        thumbnail="https://yt3.ggpht.com/-IyfXJrb2GOI/AAAAAAAAAAI/AAAAAAAAAAA/Mzq0mearwWk/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
	
    plugintools.add_item( 
        #action="", 
        title="Roary the Racing Car",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://yt3.ggpht.com/-ICFRJMoGnLE/AAAAAAAAAAI/AAAAAAAAAAA/QOnVAwas-6A/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mother Goose Club Playhouse",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-7EZ4R90FGWk/AAAAAAAAAAI/AAAAAAAAAAA/EGvKs_ccXVc/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
	
    plugintools.add_item( 
        #action="", 
        title="VeggieTales",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-OJXjBZ_ADKU/AAAAAAAAAAI/AAAAAAAAAAA/fkPmTlcfLwM/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Horrid Henry",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://pbs.twimg.com/profile_images/491626163367067648/xdc0kyGB.png",
        fanart=FANART,
        folder=True )
   
    plugintools.add_item( 
        #action="", 
        title="Barney",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://yt3.ggpht.com/-bxLGdet8FN0/AAAAAAAAAAI/AAAAAAAAAAA/mcry7S01mG8/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Strawberry Shortcake",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/-XJkLk9OAOpo/AAAAAAAAAAI/AAAAAAAAAAA/kmrUg-mq73w/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="DisneyJuniorUK",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://yt3.ggpht.com/-e8lc2AnB-Z8/AAAAAAAAAAI/AAAAAAAAAAA/1kZk7GEiBxA/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Harry and his Bucket Full of Dinosaurs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://yt3.ggpht.com/--pEAUtbyyKw/AAAAAAAAAAI/AAAAAAAAAAA/M68Lf7rBBaM/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="PBS KIDS",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-2HarBf-DCuo/AAAAAAAAAAI/AAAAAAAAAAA/XVDHTHwR0AA/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		

    plugintools.add_item( 
        #action="", 
        title="Art for Kids Hub",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="https://yt3.ggpht.com/-pwbr7q8g-sM/AAAAAAAAAAI/AAAAAAAAAAA/sNTyugBGDwo/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Kids TV - Nursery Rhymes And Children’s Songs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://yt3.ggpht.com/-Vas4UzOl0KE/AAAAAAAAAAI/AAAAAAAAAAA/_fWZBwq0qnA/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="StoryBots",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_51+"/",
        thumbnail="https://yt3.ggpht.com/-QdIidAh5N2w/AAAAAAAAAAI/AAAAAAAAAAA/Tj2VwbeDzjg/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Bounce Patrol Kids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_52+"/",
        thumbnail="https://yt3.ggpht.com/-P3GrO-qDn8c/AAAAAAAAAAI/AAAAAAAAAAA/WGyon47JL38/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Scratch Garden",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_53+"/",
        thumbnail="https://yt3.ggpht.com/-eTuj3_QjuoU/AAAAAAAAAAI/AAAAAAAAAAA/dgp7gWu7d-w/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Alphablocks",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_54+"/",
        thumbnail="https://yt3.ggpht.com/-xH1Q0sBSkEI/AAAAAAAAAAI/AAAAAAAAAAA/hU_49a6uWdg/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Jim Henson Company",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_56+"/",
        thumbnail="https://yt3.ggpht.com/-fsmlK5phZLU/AAAAAAAAAAI/AAAAAAAAAAA/7RvrPw0lZWs/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Singing Walrus",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_81+"/",
        thumbnail="https://yt3.ggpht.com/-as199bSpk6s/AAAAAAAAAAI/AAAAAAAAAAA/WqsY1h_YHok/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Noddy",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_59+"/",
        thumbnail="https://yt3.ggpht.com/--wJDJ5O2v6w/AAAAAAAAAAI/AAAAAAAAAAA/sEOSTTTVRuQ/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Cyber Chase",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_60+"/",
        thumbnail="https://yt3.ggpht.com/-Q3y3jf7lMGo/AAAAAAAAAAI/AAAAAAAAAAA/ICLtV_9BQ3w/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Family Fun Pack",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_61+"/",
        thumbnail="https://yt3.ggpht.com/-ka4JQsRydvk/AAAAAAAAAAI/AAAAAAAAAAA/e_mtJbDK-j0/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Ben and Holly's Little Kingdom",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_62+"/",
        thumbnail="https://yt3.ggpht.com/-1b_8TBn1xxQ/AAAAAAAAAAI/AAAAAAAAAAA/iVbPI10tyZ4/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="The Kids Club",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_63+"/",
        thumbnail="https://yt3.ggpht.com/-4MW1_sI9kes/AAAAAAAAAAI/AAAAAAAAAAA/UvSPNO-uA0c/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="The GiggleBellies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_64+"/",
        thumbnail="https://yt3.ggpht.com/-2kuWffGhVHE/AAAAAAAAAAI/AAAAAAAAAAA/T6-9PEY-OPA/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Learn English Kids",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_67+"/",
        thumbnail="https://yt3.ggpht.com/-Wk6NXGS1pAk/AAAAAAAAAAI/AAAAAAAAAAA/nBondFZLttw/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="FluffyJetToys",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_68+"/",
        thumbnail="https://yt3.ggpht.com/--pOWD9ZiIq8/AAAAAAAAAAI/AAAAAAAAAAA/p3KUOV81ark/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="The Learning Station",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_69+"/",
        thumbnail="https://yt3.ggpht.com/-9KvO6WDX4hw/AAAAAAAAAAI/AAAAAAAAAAA/_7ZS0M2t75M/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Have Fun Teaching",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_70+"/",
        thumbnail="https://yt3.ggpht.com/-p2qbkGa_6rk/AAAAAAAAAAI/AAAAAAAAAAA/e_thnM8vVmI/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="Muffin Songs",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_71+"/",
        thumbnail="https://yt3.ggpht.com/-k2BEOOGDEvg/AAAAAAAAAAI/AAAAAAAAAAA/wBemI-eTVv8/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="All Things Animal",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_72+"/",
        thumbnail="https://yt3.ggpht.com/-HNSBTYLoWsE/AAAAAAAAAAI/AAAAAAAAAAA/TOINTQPpmEw/s500-c-k-no-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="PINKFONG",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_80+"/",
        thumbnail="https://yt3.ggpht.com/-veg6cpuOGVE/AAAAAAAAAAI/AAAAAAAAAAA/dOEHHrmAYJQ/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Harry Kindergarten Music",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_82+"/",
        thumbnail="https://yt3.ggpht.com/-KE3McXw5yoE/AAAAAAAAAAI/AAAAAAAAAAA/SAww80UFT-A/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Turtle Interactive",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_83+"/",
        thumbnail="https://yt3.ggpht.com/-CrtwEE7Ppfw/AAAAAAAAAAI/AAAAAAAAAAA/_a5bdV-Kne8/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Oh My Genius",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_84+"/",
        thumbnail="https://yt3.ggpht.com/-C-8v0iL7EyU/AAAAAAAAAAI/AAAAAAAAAAA/az0Pym6l5bY/s500-c-k-no-mo-rj-c0xffffff/photo.jpg",
        fanart=FANART,
        folder=True )
        
run()		
