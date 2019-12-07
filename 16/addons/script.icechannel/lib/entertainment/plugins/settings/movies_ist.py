'''
    Ice Channel
'''

from entertainment.plugnplay.interfaces import iStreamSettings
from entertainment.plugnplay.interfaces import MovieIndexer
from entertainment.plugnplay.interfaces import MovieSource
from entertainment.plugnplay import Plugin
from entertainment import common

class Movies(iStreamSettings):
    implements = [iStreamSettings]
    
    priority = 105
        
    def Initialize(self):
        xml = '<settings>\n'
        
        xml += '<category label="General">\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting id="metadata_movies" type="bool" label="Metadata" default="true"/>\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting id="autoplay_host_sel_dialog" type="bool" label="Show Autoplay/Host selection dialog " default="true"/>\n'        
        xml += '<setting id="autoplay" type="bool" label="Auto Play" default="false"/>\n'        
        xml += '<setting id="autoplay_skip_interval" type="labelenum" values="2|5|10|15|20|25|30|50|100|200|300" label="     Time (in seconds), to skip to next host if STOP pressed" default="300" enable="eq(-1,true)"/>\n'
        xml += '<setting type="sep"/>\n'
        xml += '<setting id="sort" type="bool" label="Sort" default="true"/>\n'
        xml += '<setting id="sort_quality" type="text" enable="eq(-1,true)" label="     Quality" default="4K,3D,1080P,720P,HD,480P,DVD,SD,NA,TS,CAM"/>\n'
        xml += '<setting id="sort_hosts_1" type="text" enable="eq(-2,true)" label="     Hosts [COLOR gold][I](1)[/I][/COLOR]" default="FURK.NET,EASYNEWS,123MOVIES,USMOVIESHD,CARTOONHD,MOVREEL,ICEFILMS,PRIMEWIRE,MUCHMOVIES.ORG,MOVIESTORM.EU,YIFY.TV"/>\n'
        xml += '<setting id="sort_hosts_2" type="text" enable="eq(-3,true)" label="     Hosts [COLOR gold][I](2)[/I][/COLOR]" default="LEMUPLOADS.COM,PUTLOCKER.COM,SOCKSHARE.COM,PLAYED.TO"/>\n'
        xml += '<setting id="sort_hosts_3" type="text" enable="eq(-4,true)" label="     Hosts [COLOR gold][I](3)[/I][/COLOR]" default="PROMPTFILE.COM,MIGHTYUPLOAD.COM,GORILLAVID.IN,VIDHOG.COM"/>\n'
        xml += '<setting id="sort_hosts_4" type="text" enable="eq(-5,true)" label="     Hosts [COLOR gold][I](4)[/I][/COLOR]" default="NOWVIDEO.CH,NOWVIDEO.SX,NOWVIDEO.EU"/>\n'
        xml += '<setting id="sort_hosts_5" type="text" enable="eq(-6,true)" label="     Hosts [COLOR gold][I](5)[/I][/COLOR]" default="SHARESIX.COM,ZALAA.COM,FILENUKE.COM"/>\n'
        xml += '</category>\n' 
        
        xml += '<category label="Indexers">\n'
        xml += '<setting type="sep"/>\n'              
        mi = MovieIndexer.implementors()
        mi.sort(key=lambda k: common.custom_item_sort(k.display_name))
        for indxrtyp in  mi:
            xml += '<setting id="%s" type="bool" label="%s" default="%s"/>\n' % (common.indxr_Movies + '_' + indxrtyp.name + '_indexer_enabled', 
                indxrtyp.display_name, indxrtyp.default_indexer_enabled)        
        xml += '</category>\n' 
        
        xml += '<category label="Sources">\n'
        xml += '<setting type="sep"/>\n'
        ms = MovieSource.implementors()
        ms.sort(key=lambda k: common.custom_item_sort(k.display_name))
        for src in  ms:
            xml += '<setting id="%s" type="bool" label="%s" default="%s"/>\n' % (common.src_Movies + '_' + src.name + '_source_enabled', 
                src.display_name + (' [COLOR gold][I](autoplay not supported)[/I][/COLOR]' if not src.auto_play_supported else ''), src.source_enabled_by_default)
        xml += '</category>\n'
        
        xml += '</settings>\n'
        
        self.CreateSettings('Movies', common.settings_Movies, xml)
