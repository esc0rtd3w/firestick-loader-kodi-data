# -*- coding: utf-8 -*-
#------------------------------------------------------------
# SF Movies & TV on YouTube Addon by coldkeys
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

addonID = 'plugin.video.ytsf'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCMRKzdLbt-NbTsATQORxEIw"
YOUTUBE_CHANNEL_ID_2 = "UCnJjSZdHJ4wWiJ4Q0dt8L7A"
YOUTUBE_CHANNEL_ID_3 = "UChG9taCaJvLAL66QuDuKK2A"
YOUTUBE_CHANNEL_ID_4 = "UCEA1biEh0Z2MrdXMB8W1g0A"
YOUTUBE_CHANNEL_ID_5 = "UCuAjz1LAvgudcQNQeGjF2wQ"
YOUTUBE_CHANNEL_ID_6 = "PLeagipoZmyfk43d3WDeQDdx4DxDfkfpXL"
YOUTUBE_CHANNEL_ID_7 = "UCFuZe7O_A4au4IPkUDE1HFQ"
YOUTUBE_CHANNEL_ID_8 = "UCLIv-DVrjhZJqb7hvTVgL_w"
YOUTUBE_CHANNEL_ID_9 = "UCCXEt6-fZgeDpqK4PHbGUpg"
YOUTUBE_CHANNEL_ID_10 = "UCz_aPzkVpUZaI-4wcL6KqJg"
YOUTUBE_CHANNEL_ID_11 = "PLeagipoZmyflJEbfML5SgRla0TNeAjJGT"
YOUTUBE_CHANNEL_ID_12 = "PLeagipoZmyflYs5NlYTLFPctUtwQ2D_33"
YOUTUBE_CHANNEL_ID_13 = "PLeagipoZmyfmeKpbCdBkjSXczL3gioTIL"
YOUTUBE_CHANNEL_ID_14 = "PL6fJmjt84zZhp5eGS7ceZhYmyvyT8VtP0"
YOUTUBE_CHANNEL_ID_15 = "PL6fJmjt84zZhV4hZGR_VgBZxl2fAPA9Ed"
YOUTUBE_CHANNEL_ID_16 = "PLoqfIQD57O1La7QUoY0Za_bFxP0A56cKm"
YOUTUBE_CHANNEL_ID_17 = "PLIWGnQn6D-fnfAg7AmwIQ9bEziqi_cs_M"
YOUTUBE_CHANNEL_ID_18 = "PLeagipoZmyfm1K3A2qNxleEpXJ5gUKTvk"
YOUTUBE_CHANNEL_ID_19 = "PLWBUT4nrnPf5CVi3zYyGLhkoxIR7gPubu"
YOUTUBE_CHANNEL_ID_20 = "PLy_1AFQWJ-2OYYEGnIzdGz9iN9IiMfYh2"
YOUTUBE_CHANNEL_ID_21 = "PLy_1AFQWJ-2PAnG1zby1sGiiBNhw0kTho"
YOUTUBE_CHANNEL_ID_22 = "PLNU2oqI-PZ8AHPG2nUbG3aIrpVEM9og1g"
YOUTUBE_CHANNEL_ID_23 = "PLoqfIQD57O1IinFGjtCPZW0nxDSPlycmm"
YOUTUBE_CHANNEL_ID_24 = "PLeagipoZmyfnbnG2AibqGsmCMsjX_MU6o"
YOUTUBE_CHANNEL_ID_25 = "PLdwYgKHNxoDuH9wlEuEFvUQUEdkZ-tkn-"
YOUTUBE_CHANNEL_ID_26 = "PLbxdxEWxTqX81L3NnAU3nEwvPhkT7FuRm"
YOUTUBE_CHANNEL_ID_27 = "PL6fJmjt84zZiTh5wcoWV7RkUyzmU5swBL"
YOUTUBE_CHANNEL_ID_28 = "PL6fJmjt84zZgL4pcnB8DiV6cIZ9Cs8BVW"
YOUTUBE_CHANNEL_ID_29 = "PL6fJmjt84zZgK1M-eUo5eYK4R7oZIzNo7"
YOUTUBE_CHANNEL_ID_30 = "PLZVMGCh7sZUiL9-6cIQY20f0BShJ5ygE1"
YOUTUBE_CHANNEL_ID_31 = "PLZVMGCh7sZUhBM5lrUujFkQloQ0qEvlBU"
YOUTUBE_CHANNEL_ID_32 = "PL152bjytsMC5LMg47W6nry8VXqfrpdPwu"
YOUTUBE_CHANNEL_ID_33 = "PLZVMGCh7sZUjZduYVU0T1o2zWGjUbVPON"
YOUTUBE_CHANNEL_ID_34 = "PLZVMGCh7sZUhyMv8OnQ77wAiHX2w1szGb"
YOUTUBE_CHANNEL_ID_35 = "PL1j14gtz6BiuQe_8XnbX6Iacohj-ZURMF"
YOUTUBE_CHANNEL_ID_36 = "PL1j14gtz6BivyTCpk8Iuw9m87zts0RdBP"
YOUTUBE_CHANNEL_ID_37 = "PL1j14gtz6BisAhJo_QIP8SUGtLyeh_Hmg"
YOUTUBE_CHANNEL_ID_38 = "PL1j14gtz6BivX09dtnZB9S2C2HV68W0ZQ"
YOUTUBE_CHANNEL_ID_39 = "PLAGggYDwCYhMsbivAD73LXrDhCtGF9s4Q"
YOUTUBE_CHANNEL_ID_40 = "PL1j14gtz6Biv8_9-CPOdguNdX4q6prBqf"
YOUTUBE_CHANNEL_ID_41 = "PL152bjytsMC5njJFOiMPG1VhjF-4tpDeO"
YOUTUBE_CHANNEL_ID_42 = "PLq3qds_3i7OFgs3t80DyCd8bHAchy1Vip"
YOUTUBE_CHANNEL_ID_43 = "PL3FHRrKCoXcB6RZveh8b7D4es3jY8iTti"
YOUTUBE_CHANNEL_ID_44 = "PLq3qds_3i7OFne9l7K4sHltk8JZGBMCts"
YOUTUBE_CHANNEL_ID_45 = "PLq3qds_3i7OExxudlXqymOe-ehNeJNb99"
YOUTUBE_CHANNEL_ID_46 = "PL1j14gtz6BisrDj8dJcsY62jycUIUA7lk"
YOUTUBE_CHANNEL_ID_47 = "PL1j14gtz6Bistzwa6e2yS62CUaHLSW03E"
YOUTUBE_CHANNEL_ID_48 = "PL1j14gtz6Bivyghsat08P0XEmytWibxyV"
YOUTUBE_CHANNEL_ID_49 = "PL1j14gtz6Biun9XFQCnK4HKT-OkM6JPH9"
YOUTUBE_CHANNEL_ID_50 = "PL1j14gtz6BisGi4zMFeReRLoBI2cyKM32"

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
        title="The Outer Limits Original Series",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-ShXZy-aEr0Y/AAAAAAAAAAI/AAAAAAAAAAA/rmCUNpATX88/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Old Science Fiction Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-2JBQ9iwEyHg/AAAAAAAAAAI/AAAAAAAAAAA/E8MFen8HgMw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Vintage Science Fiction Movies",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-kfwaQwwBD-s/AAAAAAAAAAI/AAAAAAAAAAA/FAX69BBvgHo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Sci-Fi Cinema Channel",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-WsYQYTOkwT4/AAAAAAAAAAI/AAAAAAAAAAA/JYfTQ_L6b4Q/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SciFi - Horror Movies and TV (Check Playlists -tdebbie2002s)",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://i.ytimg.com/i/uAjz1LAvgudcQNQeGjF2wQ/mq1.jpg?v=510cc89e",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Invaders (TV Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-oH067RXROr0/AAAAAAAAAAI/AAAAAAAAAAA/rpUZcd4cWB0/s100-c-k-no/photo.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="#ScienceFiction - Check the Playlists",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://i.ytimg.com/i/FuZe7O_A4au4IPkUDE1HFQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Blakes 7",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-X4V-Gk2ylZI/AAAAAAAAAAI/AAAAAAAAAAA/fZ8ZmTYXPnw/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="#Fantasy - Check the Playlists",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://i.ytimg.com/i/CXEt6-fZgeDpqK4PHbGUpg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="SciFi Horror Movie Trailers",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-lPsxV27vOb4/AAAAAAAAAAI/AAAAAAAAAAA/iJWZbAqxjcc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Space 1999 (Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://i.ytimg.com/i/SSA0TYL0BzON5fFHoWT3KQ/mq1.jpg?v=53a3e9a6",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Starlost (Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/eHq6BiKTJdlyILIKuXkWDSl4t_jo_cnIl3kDDuKmZ6OyTgGJRx5AY0sch1JglaWYs-_6R9K7KTcWHqbN=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Nowhere Man (Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_13+"/",
        thumbnail="https://yt3.ggpht.com/-N_PTsLIP3kY/AAAAAAAAAAI/AAAAAAAAAAA/d-rDLtOXJfc/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Timecop (Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_14+"/",
        thumbnail="https://i.ytimg.com/i/ssE8M5knDP6vO40_iWizaA/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Land of the Lost (Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_15+"/",
        thumbnail="https://i.ytimg.com/i/R7-NK1DKKyYtgpG3C3UIug/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Science Fiction Theatre",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_16+"/",
        thumbnail="https://yt3.ggpht.com/-2ov5t_ii-BI/AAAAAAAAAAI/AAAAAAAAAAA/o0wl_JGNV6g/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Invisible Man 1958",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_17+"/",
        thumbnail="https://yt3.ggpht.com/-hFyL8l5MUTs/AAAAAAAAAAI/AAAAAAAAAAA/tJr2V8acY74/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Invisible Man 1975 (Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_18+"/",
        thumbnail="https://yt3.ggpht.com/yMRQd2rnWdlTrm2xc00NuZlhoYr6VmKJZzuAgQsXt3ODsIaFqdocgYntzwvRFqzjMZ1yes6u9HZRKVjHohE=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Invisible Man 1984 (complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_19+"/",
        thumbnail="https://yt3.ggpht.com/-GG6OlWHkexo/AAAAAAAAAAI/AAAAAAAAAAA/_GQjCMijT3w/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Invisible Man 2000 S1 (complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_20+"/",
        thumbnail="https://yt3.ggpht.com/-Mh0x7JQPXE8/AAAAAAAAAAI/AAAAAAAAAAA/Bm6OY-C981Q/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Invisible Man 2000 S2 (complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_21+"/",
        thumbnail="https://yt3.ggpht.com/-Mh0x7JQPXE8/AAAAAAAAAAI/AAAAAAAAAAA/Bm6OY-C981Q/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Listener S1-3 (complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_22+"/",
        thumbnail="https://i.ytimg.com/i/1GqqKaRRstBL3h1gx-8-FQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Quatermass Serials",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_23+"/",
        thumbnail="https://i.ytimg.com/i/v15lR0-HhTNafORFk61Qzw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Galactica 1980 (ep1 missing)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_24+"/",
        thumbnail="https://yt3.ggpht.com/-G1W4puIf8R0/AAAAAAAAAAI/AAAAAAAAAAA/uhxiUZnZLpg/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Flash Gordon (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_25+"/",
        thumbnail="https://yt3.ggpht.com/jwWkyUexnWS9E7d7MwGfq2Jxh3mfSNEGnDdXvjD5hHIWei3O9BKbwPQXSa2IbcHSH_5qan8QKjfEmfaF=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Twilight Zone 2002 (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_26+"/",
        thumbnail="https://yt3.ggpht.com/-0o3QtxqLDTQ/AAAAAAAAAAI/AAAAAAAAAAA/14FPKtQNJL4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Tribe (260 episodes Complete)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_27+"/",
        thumbnail="https://yt3.ggpht.com/-ynRvR_dk710/AAAAAAAAAAI/AAAAAAAAAAA/q3qQ0sS7yy4/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Highlander (TV)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_28+"/",
        thumbnail="https://yt3.ggpht.com/1nCebJilZRnx0dtR8eecSj0fO9BV7byv9PjUgiduRAJ6EBmywiDIdjnqn5abWFbOMis6nf0FToX2B-X4_A=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Adventures of Sinbad (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_29+"/",
        thumbnail="https://yt3.ggpht.com/-gaXijkyzx6M/AAAAAAAAAAI/AAAAAAAAAAA/o0p63FHXF5Q/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="H2O Just Add Water (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_30+"/",
        thumbnail="https://yt3.ggpht.com/-_vXJFcP_ipY/AAAAAAAAAAI/AAAAAAAAAAA/p6qMPBk8vS8/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Stormworld (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_31+"/",
        thumbnail="https://yt3.ggpht.com/-BoVIpnBMUgk/AAAAAAAAAAI/AAAAAAAAAAA/GkYBX-DmqSA/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="*Beastmaster (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_32+"/",
        thumbnail="https://yt3.ggpht.com/IS3RSmSHTOx0md3VT6nLkDSOexI7eJGbQBkaGaIEaJ8vXNHhfSt6nY2HnHiF1Xz8c1_8po2G8eNJR8Kijg=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Atlantis High (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_33+"/",
        thumbnail="https://yt3.ggpht.com/-bdrYrxALZac/AAAAAAAAAAI/AAAAAAAAAAA/rg5f76Sptpk/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Animorphs (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_34+"/",
        thumbnail="https://i.ytimg.com/i/PrYX_xy9QG36cNsoSXQ4pg/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Science Fiction Movies 1980-",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_35+"/",
        thumbnail="https://i.ytimg.com/i/uAjz1LAvgudcQNQeGjF2wQ/mq1.jpg?v=510cc89e",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Science Fiction Movies 1960-1979",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_36+"/",
        thumbnail="https://i.ytimg.com/i/uAjz1LAvgudcQNQeGjF2wQ/mq1.jpg?v=510cc89e",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Science Fiction Movies 1950-59",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_37+"/",
        thumbnail="https://i.ytimg.com/i/uAjz1LAvgudcQNQeGjF2wQ/mq1.jpg?v=510cc89e",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Science Fiction Movies 1920-1949",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_38+"/",
        thumbnail="https://i.ytimg.com/i/uAjz1LAvgudcQNQeGjF2wQ/mq1.jpg?v=510cc89e",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Mystery Science Theater",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_39+"/",
        thumbnail="https://yt3.ggpht.com/-7E8NfBZmqxA/AAAAAAAAAAI/AAAAAAAAAAA/MaXlOyO-3f0/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Prisoner (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_40+"/",
        thumbnail="https://i.ytimg.com/i/N13aKVOmaxuH6dHHdXCwMw/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Champions (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_41+"/",
        thumbnail="https://i.ytimg.com/i/smHSa-jS-mcSofW-OcCMYQ/mq1.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Green Hornet (Full 13 episode serial)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_42+"/",
        thumbnail="https://yt3.ggpht.com/704Tkn2wPDaqhOgIMk8WNKFFkB0Crd4qziOaVaBs4I7LFi4JD7W_UAeRiDTLFftK0vvt5Loy0h9gsoZ8ig=s100-nd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Green Hornet (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_43+"/",
        thumbnail="https://i.ytimg.com/i/RAg89DkbTN8qTM2M5CG2Mw/mq1.jpg?v=4fc532bd",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Vanishing Shadow (Full 12 episode serial)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_44+"/",
        thumbnail="https://yt3.ggpht.com/-RKtYzVEp3O0/AAAAAAAAAAI/AAAAAAAAAAA/KmSoaxxoBOM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="The Phantom Empire (Full 12 episode serial)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_45+"/",
        thumbnail="https://yt3.ggpht.com/-RKtYzVEp3O0/AAAAAAAAAAI/AAAAAAAAAAA/KmSoaxxoBOM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="M.A.N.T.I.S (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_46+"/",
        thumbnail="https://yt3.ggpht.com/-iurJkyUKgH0/AAAAAAAAAAI/AAAAAAAAAAA/yxKvaY_5MWs/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="UFO (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_47+"/",
        thumbnail="https://yt3.ggpht.com/-bNg7TGtpJys/AAAAAAAAAAI/AAAAAAAAAAA/0alVDfqK-JM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Project UFO (25 of 26 episodes)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_48+"/",
        thumbnail="https://yt3.ggpht.com/-bNg7TGtpJys/AAAAAAAAAAI/AAAAAAAAAAA/0alVDfqK-JM/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Odyssey 5 (Complete Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_49+"/",
        thumbnail="https://yt3.ggpht.com/-XRfmjbGhm3w/AAAAAAAAAAI/AAAAAAAAAAA/RiS-Lz1iuMo/s100-c-k-no/photo.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Taken (Complete Mini Series)",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_50+"/",
        thumbnail="https://i.ytimg.com/i/4coxjX4ZGVkKUw3x_JJ21w/mq1.jpg",
        folder=True )
run()
