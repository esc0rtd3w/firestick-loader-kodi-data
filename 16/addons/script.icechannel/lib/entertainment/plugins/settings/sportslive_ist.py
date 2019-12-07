'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import iStreamSettings
from entertainment.plugnplay.interfaces import SportsIndexer
from entertainment.plugnplay.interfaces import SportsSource
from entertainment.plugnplay import Plugin
from entertainment import common

class SportsLive(iStreamSettings):
    implements = []
    
    priority = 115
        
    def Initialize(self):
        xml = '<settings>\n'
                
        xml += '<category label="Indexers">\n'
        xml += '<setting type="sep"/>\n'      
        for indxrtyp in  SportsIndexer.implementors():
            xml += '<setting id="%s" type="bool" label="%s" default="%s"/>\n' % (common.indxr_Sports + '_' + indxrtyp.name + '_indexer_enabled', 
                indxrtyp.display_name, indxrtyp.default_indexer_enabled)        
        xml += '</category>\n' 
        
        xml += '<category label="Sources">\n'
        xml += '<setting type="sep"/>\n'
        for src in  SportsSource.implementors():
            xml += '<setting id="%s" type="bool" label="%s" default="%s"/>\n' % (common.src_Sports + '_' + src.name + '_source_enabled', 
                src.display_name, src.source_enabled_by_default)
        xml += '</category>\n'
                
        xml += '</settings>\n'
        
        self.CreateSettings('Sports (Live)', common.settings_Sports, xml)
