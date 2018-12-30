# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Classic British Comedy on YouTube by coldkeys
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

addonID = 'plugin.video.yt-comedy'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "PL152bjytsMC5RgWAecHQQmEedfvh6qrmK"
YOUTUBE_CHANNEL_ID_2 = "PL152bjytsMC5e4fR4lOtkyYRd4uH0avaD"
YOUTUBE_CHANNEL_ID_3 = "PL152bjytsMC7TBayLHumPe8e-z1dGb7Dq"
YOUTUBE_CHANNEL_ID_4 = "PL152bjytsMC7Xok4S9XO7LjrFqJJBFUCM"
YOUTUBE_CHANNEL_ID_5 = "PL152bjytsMC7EsC31KjG68j9WG6ZXReJ0"
YOUTUBE_CHANNEL_ID_6 = "PL152bjytsMC7UE15_4Amcmfmr-ks3j6zA"
YOUTUBE_CHANNEL_ID_7 = "PL152bjytsMC5vQ1TNKPsNEc1HcYJe0pTM"
YOUTUBE_CHANNEL_ID_8 = "PL152bjytsMC6nUhWhrngYUJcx-boBgxOD"
YOUTUBE_CHANNEL_ID_9 = "PL152bjytsMC78Ajxwobxpef974BPj7yhG"
YOUTUBE_CHANNEL_ID_10 = "PL152bjytsMC5RNXrEQ6wjYeSh7YZd2e5b"
YOUTUBE_CHANNEL_ID_11 = "PL152bjytsMC5M1vNWi9HgH_znu3XuQ2uq"
YOUTUBE_CHANNEL_ID_12 = "PL152bjytsMC557kLyghLs2xYzdMcglPS_"
YOUTUBE_CHANNEL_ID_13 = "PL152bjytsMC4LOEcMCEfwxnlCgyfpDa7a"
YOUTUBE_CHANNEL_ID_14 = "PL152bjytsMC5PWhR93Sioe7Fn53t-ZwoJ"
YOUTUBE_CHANNEL_ID_15 = "PL152bjytsMC4Yci9hv9F_d8Wh0Txwx2nz"
YOUTUBE_CHANNEL_ID_16 = "PL152bjytsMC4nnIPwEe_bzE-lMdTbMDrh"
YOUTUBE_CHANNEL_ID_17 = "PL152bjytsMC7yOEs1SSniUARwTprSudOC"
YOUTUBE_CHANNEL_ID_18 = "PL152bjytsMC5_xO1xZu_sEQG74GOo-ZpO"
YOUTUBE_CHANNEL_ID_19 = "PL152bjytsMC5YferI7Od4a_1kuE_yA-YY"
YOUTUBE_CHANNEL_ID_20 = "PL152bjytsMC6Iv4X3Hup78LHjuyNKhPqe"
YOUTUBE_CHANNEL_ID_21 = "PL152bjytsMC6J7h8_vOqNNxTDkaohOiZg"
YOUTUBE_CHANNEL_ID_22 = "PL152bjytsMC5jwOqUNnZdKzbyrBgUOmhW"
YOUTUBE_CHANNEL_ID_23 = "PL152bjytsMC7x8nPGnY2aAVSj6uWlRRu8"
YOUTUBE_CHANNEL_ID_24 = "PL152bjytsMC7goZF8MAZeW65iXRw5tybO"
YOUTUBE_CHANNEL_ID_25 = "PL152bjytsMC4s2qMaaeRiBR-wAZyi-BTM"
YOUTUBE_CHANNEL_ID_26 = "PL152bjytsMC6l-LkLkRGk4gmDIidUMu2i"
YOUTUBE_CHANNEL_ID_27 = "PL152bjytsMC5b_3vq1BCxnxiw2fjg_1of"
YOUTUBE_CHANNEL_ID_28 = "PL152bjytsMC4KN0A4-MfXhjD0OlOv3qBO"
YOUTUBE_CHANNEL_ID_29 = "PL152bjytsMC77vZVZNgDVGcoN-vjfXNSc"
YOUTUBE_CHANNEL_ID_30 = "PL152bjytsMC64zKL9t12viInAlMrPaF0H"
YOUTUBE_CHANNEL_ID_31 = "PL152bjytsMC5gDpYNYTAM_iwJ6CBC5q-c"
YOUTUBE_CHANNEL_ID_32 = "PL152bjytsMC7ar8AFRM6EyNUzQLfIgQYc"
YOUTUBE_CHANNEL_ID_33 = "PL152bjytsMC6kES1x0hOqew8cfn3KMLrE"
YOUTUBE_CHANNEL_ID_34 = "PL152bjytsMC7OvZkYQx0h9KFAUVHUE1nS"
YOUTUBE_CHANNEL_ID_35 = "PL152bjytsMC6gHC5NF1JCEd2k_5iI9nIK"
YOUTUBE_CHANNEL_ID_36 = "PL152bjytsMC6E_2akhwIT2_hcxEZOH_1h"
YOUTUBE_CHANNEL_ID_37 = "PL152bjytsMC4gyximko5Sly0sJ1EWc8oB"
YOUTUBE_CHANNEL_ID_38 = "PL152bjytsMC4UAMBs07WuXplG-ql-QGyr"
YOUTUBE_CHANNEL_ID_39 = "PL152bjytsMC7illBlwYHemx4XCe8zfEUG"
YOUTUBE_CHANNEL_ID_40 = "PL152bjytsMC5_xO1xZu_sEQG74GOo-ZpO"
YOUTUBE_CHANNEL_ID_41 = "PL152bjytsMC73eGJ-boQYjTISUzZXMjcm"
YOUTUBE_CHANNEL_ID_42 = "PL152bjytsMC7CFkjGnbwq8KiKZXVC4oB-"
YOUTUBE_CHANNEL_ID_43 = "PL152bjytsMC7bqVYJM-ZvdTKDgGB13d6q"
YOUTUBE_CHANNEL_ID_44 = "PL152bjytsMC6yROvlxlobaS-ScTOC64pD"
YOUTUBE_CHANNEL_ID_45 = "PL152bjytsMC6M2KkuiJBvzWlUfrxgjS5N"
YOUTUBE_CHANNEL_ID_46 = "PL152bjytsMC4JXbduEfRtwyPbMlMidwDo"
YOUTUBE_CHANNEL_ID_47 = "PL152bjytsMC7FKayIzPhmtZg09Imrmf04"
YOUTUBE_CHANNEL_ID_48 = "PL152bjytsMC7r9HB99--gmao8Ys5e6buS"
YOUTUBE_CHANNEL_ID_49 = "PL152bjytsMC4GJYyXvPRWaZtASKgFoM7M"
YOUTUBE_CHANNEL_ID_50 = "PL152bjytsMC67Dcz4OAPbO4m8zXTBNm48"


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
        title="Benny Hill",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-jSY8k70xf4s/AAAAAAAAAAI/AAAAAAAAAAA/63viRC9PPE8/s88-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Eric Sykes",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://i.ytimg.com/i/GLBmlp6TB9frOl7nreOM6g/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Rab C Nesbitt",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-DKx9ccZjWyo/AAAAAAAAAAI/AAAAAAAAAAA/e7VgYschGoI/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Spike Milligan",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://i.ytimg.com/i/VXHbumbvhziGHK8GuraskA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dave Allen",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-ehLzstmoNhA/AAAAAAAAAAI/AAAAAAAAAAA/pgblfxDxKmM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Tommy Cooper",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://i.ytimg.com/i/S7p6SAUVAbuO805adnd7Kw/mq1.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Tony Hancock",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://i.ytimg.com/i/0PrVsVCaUWLErMk1ldHSfA/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="The Two Ronnies (inc.Open All Hours)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://i.ytimg.com/i/fsTcaEigQU22oRCfl9fhhQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Jasper Carrott",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://i.ytimg.com/i/0sABvbBBezfbgjDQsjxLpw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Morecambe and Wise",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://i.ytimg.com/i/GlP9OTn9qROuQMf4-P9kqg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Frankie Howerd",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://i.ytimg.com/i/kPza8_K_WMB5T-gsCXnyMA/mq1.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Rowan Atkinson",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://i.ytimg.com/i/E9c2Y2_o7z3bmXw8nUfyTA/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Rik Mayall",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://i.ytimg.com/i/t0KO3HFXZMJIWTYQ2LzjNQ/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Hale and Pace",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://yt3.ggpht.com/-t9eSzzZWUHE/AAAAAAAAAAI/AAAAAAAAAAA/JD-5u46KB5s/s100-c-k-no/photo.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="Leonard Rossiter",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://i.ytimg.com/i/Epo6qA3uQXe1B-ndVoOdOw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="British Comedy Movies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://i.ytimg.com/i/qNNc-vTjSZPLH7Hog5it-A/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="British Comedy Series",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://i.ytimg.com/i/sTdfailANmQlxoFL1AlvRg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="British Comedy Series 2",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://i.ytimg.com/i/dYvoTq2LWxSg6n3tea3hRQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Comedy Others",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://i.ytimg.com/i/tlyE8AzokZc_YK-qgljaSA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Live Stand Up Comedy",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-USnlrkDIH-4/AAAAAAAAAAI/AAAAAAAAAAA/2dNbBhNTK3c/s100-c-k-no/photo.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Biographies and Documentaries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://i.ytimg.com/i/EoqSfZGPmIOhyKuR9foMQw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Christmas Specials",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://i.ytimg.com/i/NqUrkK9atNsqxJnZNndQNA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mony Python and Friends",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://yt3.ggpht.com/-FiebmW6CSZs/AAAAAAAAAAI/AAAAAAAAAAA/046ypwTfQfE/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Harry Enfield",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://i.ytimg.com/i/6j4rANbpCvkluAJ2jAlDSA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Chris Barrie - Red Dwarf - Brittas Empire",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://i.ytimg.com/i/6YK-gM-xVtZaVXybV789UQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Stephen Fry and Hugh Laurie",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://i.ytimg.com/i/Jjqq2vM6ZU9EeQXDW9WaHQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Steve Coogan (Alan Partridge)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://i.ytimg.com/i/a_ZjjJNPlST-Fphmo1lYKw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dick Emery",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://i.ytimg.com/vi/Y_Q-C49KDMw/mqdefault.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Hi-de-Hi",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://yt3.ggpht.com/-Es3Y70b51ec/AAAAAAAAAAI/AAAAAAAAAAA/ME4TnzCVabo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Birds of a Feather",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://i.ytimg.com/i/c3T7icQYAZ8awtUZIiH6bQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Dad's Army",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://i.ytimg.com/i/oFOUhQIR_CMcWPkl-pgqCw/mq1.jpg",
        folder=True )                

    plugintools.add_item( 
        #action="", 
        title="Ever Decreasing Circles",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://i.ytimg.com/i/Ed7WmvwkMSOLkeBAqIyToQ/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="Allo Allo",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://i.ytimg.com/i/JJOGAsf5ORrSa71x0m7isg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Keeping Up Appearances",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://i.ytimg.com/i/NiVtEI1O84P-PrFw0xg4vg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Yes Minister - Yes Prime Minister",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://i.ytimg.com/i/EXwt5aQILYMtk54K01XD_w/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Vicar of Dibley",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://i.ytimg.com/i/MCQJziEcxS5Kzsc7fFbZFg/mq1.jpg",
        folder=True )    

    plugintools.add_item( 
        #action="", 
        title="Monarch of the Glen",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://i.ytimg.com/i/GcMtJojoUy8QCe6f-0A09g/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="The Comic Strip Presents ...",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://i.ytimg.com/i/LQrVYPuK8ip4c8HlQGPesw/mq1.jpg",
        folder=True )  

    plugintools.add_item( 
        #action="", 
        title="French and Saunders",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://i.ytimg.com/i/Y2kWyyt6w-kQTk-I1Bi5gQ/mq1.jpg",
        folder=True ) 

    plugintools.add_item( 
        #action="", 
        title="Father Ted",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://yt3.ggpht.com/-kJUwy0h2o8E/AAAAAAAAAAI/AAAAAAAAAAA/12oR7gPT9QU/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Last of the Summer Wine",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://i.ytimg.com/i/TdFqGbBSRCh0vzNRrkRH-Q/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Goodies",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://i.ytimg.com/i/iihfhTcSG2wOKa2nv4d0Jg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Some Mothers Do Have 'Em",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://i.ytimg.com/i/CMz_PAbCIQ0eU4bm_nCogQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Steptoe and Son",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://i.ytimg.com/i/9WQncKuH1p7SODXD8d8LrA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Terry and June",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://i.ytimg.com/i/4Cki0zWIVQYQL-GkUO950g/mq1.jpg",
        folder=True )		

    plugintools.add_item( 
        #action="", 
        title="Fawlty Towers (plus 3 US attempts)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://i.ytimg.com/i/sTdfailANmQlxoFL1AlvRg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mock the Week",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://i.ytimg.com/i/bjuOFX-J8y5EUcDgumXhXA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Spitting Image",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="https://i.ytimg.com/i/Kl-ed0tlW1kbSqrriQDZMg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Comedy Songs and Themes",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://i.ytimg.com/i/dggJeEG0vV9fxPBZoJBgzA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Comic Relief and Other Specials",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://yt3.ggpht.com/-eVA64j4Vqf0/AAAAAAAAAAI/AAAAAAAAAAA/xhaMuUz-edY/s100-c-k-no/photo.jpg",
        folder=True )
run()
