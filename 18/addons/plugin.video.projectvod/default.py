#------------------------------------------------------------
#------------------------------------------------------------
# VOD By Project Cypher, Addon by Cypher
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#
# Author: coldkeys/Cypher
#------------------------------------------------------------
import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.projectvod'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCBxeR6_ieWHvLO1QNlhsoKA"
YOUTUBE_CHANNEL_ID_2 = "PLzkLG_2Ckase8_g8LvCipv_Eyj3XVobmN"
YOUTUBE_CHANNEL_ID_3 = "PLzkLG_2CkasevLewZKt4IP9YPxGhd62-D"
YOUTUBE_CHANNEL_ID_4 = "PLzkLG_2Ckasfty_rm4noj8aOK1JHypcMQ"
YOUTUBE_CHANNEL_ID_5 = "PLzkLG_2CkasfDQewVC2aZ6CfsBpCd2Ka8"
YOUTUBE_CHANNEL_ID_6 = "PLzkLG_2CkasdaoMehgiYWPJnjG_EXeg6z"
YOUTUBE_CHANNEL_ID_7 = "PLzkLG_2Ckasf1JcepAyvnRrsFe52pEb9K"
YOUTUBE_CHANNEL_ID_8 = "PLzkLG_2CkascJwbLeNxoX_3ohp7gB4BpC"
YOUTUBE_CHANNEL_ID_9 = "PLzkLG_2CkasdvLqA7_AVs8cZJFLrmdUsB"
YOUTUBE_CHANNEL_ID_10 = "PLzkLG_2CkascxcflQXCDVrwKZC69C0R3Y"

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
        title="All Cypher Media Playlists",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://seo-michael.co.uk/content/images/2016/02/cypherfeat.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cyphers Conspiracy Theory",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="http://cdn2.insidermonkey.com/blog/wp-content/uploads/2015/05/featured3.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cyphers Concerts",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://i.ytimg.com/vi/i0g8toTz-ek/hqdefault.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cypher Serial Killer Docs",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="http://www.darkdocumentaries.com/wp-content/uploads/2012/12/Ian-Brady-Myra-Hindley.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cypher Gaming",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="http://www.pokerupdate.com/assets/Managed/NewsArticles/YouTube-Gaming-Homepage-1024x551.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cypher Hacking Domain",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="http://217.218.67.233/photo/20151116/15bab850-291c-4740-90e2-f9a9135da4ce.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cypher Unsolved Mysteries",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="http://i1.ytimg.com/vi/84Zw8Ch-0Ks/hqdefault.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cypher Comics Realm",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="http://media.dcentertainment.com/sites/default/files/imce/2015/11-NOV/DCFans_blog_56563f13de0d14.92385922.jpg",
        folder=True )
        
    plugintools.add_item( 
        #action="", 
        title="Cypher Cartoons",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://i.ytimg.com/vi/O-1-uWfS4t8/hqdefault.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="Cypher Movie Trailers/Reviews",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://sleeplessthought.files.wordpress.com/2016/03/international-suicide-squad-trailer-with-new-footage-and-photos-released.jpg",
        folder=True )                
run()
