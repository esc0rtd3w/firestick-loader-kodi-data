'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import iStreamSettings
from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class XBMCIntegration(iStreamSettings):
    implements = [iStreamSettings]
    
    priority = 120
        
    def Initialize(self):
        xml = '<settings>\n'
                
        xml += '<category label="Library">\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting type="lsep" label="Folders"/>\n'
        xml += '<setting id="movies_lib_folder" type="folder" label="     Movies" default="special://profile/addon_data/script.icechannel/Movies"/>\n'
        xml += '<setting id="tv_shows_lib_folder" type="folder" label="     TV Shows" default="special://profile/addon_data/script.icechannel/TVShows"/>\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting id="update_lib_after_add" type="bool" label="Update XBMC library after adding an item" default="true"/>\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting id="sync_watched_status_with_lib" type="bool" label="Keep iStream and XBMC library watched status in sync" default="true"/>\n'
        xml += '</category>\n' 
        
        xml += '<category label="Subscriptions">\n'
        xml += '<setting type="sep"/>\n'      
        xml += '<setting id="add_to_lib_when_sub" type="bool" label="When subscribing, add entire show to XBMC library" default="true"/>\n'
        xml += '<setting id="update_lib_after_sub" type="bool" label="Update XBMC library after subscribing to a show" default="true"/>\n'
        xml += '<setting id="update_lib_after_sub_update" type="bool" label="Update XBMC library after updating subscriptions" default="true"/>\n'
        xml += '<setting id="clean_up_while_update_subs" type="bool" label="Cleanup (remove ended shows) while updating subscriptions" default="true"/>\n'
        xml += '<setting id="update_subs_level" type="enum" label="When updating subscriptions, fetch: " values="The Entire Show|Last Season|Last 10 Episodes|Last 5 Episodes|Last Episode" default="2"/>\n'
        xml += '<setting id="auto_update_subscriptions" type="bool" label="Auto Update Subscriptions" default="true"/>\n'
        xml += '<setting id="auto_update_interval" type="labelenum" values="2|5|10|15|24" label="     Interval (in Hours)" default="24" enable="eq(-1,true)"/>\n'
        xml += '<setting id="show_sub_update_progress" type="bool" label="Show subscription update progress" default="true"/>\n'
        xml += '</category>\n' 
                
        xml += '</settings>\n'
        
        self.CreateSettings('XBMC Integration', common.settings_XBMC_Integration, xml)
