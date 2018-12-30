'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import iStreamSettings
from entertainment.plugnplay.interfaces import LiveTVIndexer
from entertainment.plugnplay.interfaces import LiveTVSource
from entertainment.plugnplay import Plugin
from entertainment import common

class LiveTV(iStreamSettings):
    implements = [iStreamSettings]
    
    priority = 110
        
    def Initialize(self):
    
        xml = '<settings>\n'
        xml += '<category label="General">\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting type="bool" id="live_tv_regions" label="Countries" default="false"/>\n'
        xml += '<setting type="bool" id="live_tv_languages" label="Languages" default="false"/>\n'
        xml += '<setting type="bool" id="live_tv_genres" label="Genres" default="false"/>\n'
        xml += '</category>\n'
        
        regions_list = ''
        xml_regions = '<category label="Countries">\n<setting type="sep"/>\n'
        
        languages_list = ''
        xml_languages = '<category label="Languages">\n<setting type="sep"/>\n'
        
        genres_list = ''
        xml_genres = '<category label="Genres">\n<setting type="sep"/>\n'
        
        channel_page = 1
        
        channels_list = '|'
        xml_channels = '<category label="Channels (1)">\n<setting type="sep"/>\n'

        indxrtyps = LiveTVIndexer.implementors()
        indxrtyps.sort()
        
        regions = []
        languages = []
        genres = []
        
        item_num = 1
        
        for indxrtyp in  indxrtyps:
            regions.extend(indxrtyp.regions)
            languages.extend(indxrtyp.languages)
            genres.extend(indxrtyp.genres)
                        
            # channels
            channel = indxrtyp.name
            if '|%s|'%channel not in channels_list: 

                if item_num >= 100:
                    item_num = 1
                    channel_page += 1
                    xml_channels += '</category>\n<category label="Channels (' + str(channel_page) + ')">\n<setting type="sep"/>\n'
                    
                channels_list += channel + '|'
                xml_channels += '<setting id="%s" type="bool" label="%s" default="%s"/>\n' % (common.indxr_Live_TV + '_' + channel + '_indexer_enabled', 
                    indxrtyp.display_name, 'true' )
                item_num += 1                
                    
        regions.sort(key=lambda k: k['name'])
        for region in regions:
            region_name = region['name']
            region_id = common.CreateIdFromString(region_name)
            if region_id not in regions_list:
                regions_list += region_id + '|'
                xml_regions += '<setting id="%s" type="bool" label="%s"  default="%s" />\n' % (common.indxr_Live_TV + '_' + region_id + '_indexer_enabled', 
                    region_name, 'true' )
                    
        languages.sort(key=lambda k: k['name'])
        for language in languages:
            language_name = language['name']
            language_id = common.CreateIdFromString(language_name)
            if language_id not in languages_list:
                languages_list += language_id + '|'
                xml_languages += '<setting id="%s" type="bool" label="%s" default="%s" />\n' % (common.indxr_Live_TV + '_' + language_id + '_indexer_enabled', 
                    language_name, 'true' )

        genres.sort(key=lambda k: k['name'])
        for genre in genres:
            genre_name = genre['name']
            genre_id = common.CreateIdFromString(genre_name)
            if genre_id not in genres_list:
                genres_list += genre_id + '|'
                xml_genres += '<setting id="%s" type="bool" label="%s" default="%s" />\n' % (common.indxr_Live_TV + '_' + genre_id + '_indexer_enabled', 
                    genre_name, 'true' )						
        
        #xml += '</category>\n' 
        xml += xml_channels + '</category>\n' + xml_regions + '</category>\n' + xml_languages + '</category>\n' + xml_genres + '</category>\n'
        
        xml += '<category label="Sources">\n'
        xml += '<setting type="sep"/>\n'
        for src in  LiveTVSource.implementors():
            if not isinstance( src, LiveTVIndexer ):
                xml += '<setting id="%s" type="bool" label="%s" default="%s"/>\n' % (common.src_Live_TV + '_' + src.name + '_source_enabled', 
                    src.display_name, src.source_enabled_by_default)
        xml += '</category>\n'
        
        xml += '</settings>\n'
        
        self.CreateSettings('Live TV', common.settings_Live_TV, xml)
