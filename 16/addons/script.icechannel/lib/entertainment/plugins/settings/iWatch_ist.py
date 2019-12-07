'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import iStreamSettings
from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class iWatch(iStreamSettings):
    implements = [iStreamSettings]
    
    priority = 115
        
    def Initialize(self):
        xml = '<settings>\n'
                
        xml += '<category label="Indexers">\n'
        xml += '<setting type="sep"/>\n'      

        for indxrtyp in  ListIndexer.implementors():
            xml += '<setting id="%s" type="bool" label="%s" default="%s"/>\n' % (common.indxr_Lists + '_' + indxrtyp.name + '_indexer_enabled', 
                indxrtyp.display_name, indxrtyp.default_indexer_enabled)        
        xml += '</category>\n' 
                
        xml += '</settings>\n'
        
        self.CreateSettings('iWatch', common.settings_Lists, xml)
