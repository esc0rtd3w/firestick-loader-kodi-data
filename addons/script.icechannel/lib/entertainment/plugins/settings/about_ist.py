'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import iStreamSettings
from entertainment.plugnplay.interfaces import Indexer
from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class About(iStreamSettings):
    implements = [iStreamSettings]
    
    priority = 200
        
    def Initialize(self):
        xml = '<settings>\n'
                
        xml += '<category label="About">\n'
        xml += '<setting label="[B]About ' + common.addon.get_name() +'[/B]" type="lsep" />\n'
        xml += '<setting label="[COLOR white]Name:[/COLOR] [B][COLOR yellow]' + common.addon.get_name() +'[/COLOR][/B]" type="lsep" />\n'
        xml += '<setting label="[COLOR white]Version:[/COLOR] [B][COLOR yellow]' + common.addon.get_version() + '[/COLOR][/B]" type="lsep" />\n'
        xml += '<setting label="[COLOR white]Support:[/COLOR] [COLOR yellow]www.[B]XUNITY[/B].tv[/COLOR]" type="lsep" />\n'
        xml += '</category>\n'
                
        xml += '</settings>\n'
        
        self.CreateSettings('About', common.settings_About, xml)
