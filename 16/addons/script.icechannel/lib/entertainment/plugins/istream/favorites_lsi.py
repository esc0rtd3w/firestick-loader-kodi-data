'''
    Favorites
'''

from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class Favorites(ListIndexer):
    implements = [ListIndexer]
    
    name = "Favorites"
    display_name = "Favorites"
    
    default_indexer_enabled = 'true'
    
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
    
        from universal import favorites
        fav = favorites.Favorites(common.addon_id)
        
        if section == 'main':
            main_sections = fav.get_my_main_sections()
            
            for main_section in main_sections:
                self.AddSection(list, indexer, main_section['title'], main_section['title'], type=main_section['title'].lower(), img=common.get_themed_icon('Favorites.png'), fanart=common.get_themed_fanart('Favorites.jpg'))
                
        else:
            section_items = section.split('|')
            section_items_count = len(section_items)
            
            if section_items_count == 1:

                items = fav.get_my_sub_sections(section_items[0])

                if len(items) > 0:
                    for item in items:
                        self.AddSection(list, indexer, section + '|' + item['title'], item['title'], type= (section + ' ' + item['title']).lower())
                else:
                    items = fav.get_my_favorites(section_items[0])

                    for item in items:

                        id = common.CreateIdFromString(item['title'])
                        list.append( {'indexer':item['infolabels'].get('indexer', ''), 'mode':item['infolabels'].get('mode',''), 
                            'title':item['title'], 'url':item['infolabels'].get('url', ''), 'id':id, 
                            'website':item['infolabels'].get('indexer_id', ''), 'indexer_id':item['infolabels'].get('indexer_id', ''), 
                            'name':item['infolabels'].get('name', ''), 'year':item['infolabels'].get('year', ''), 
                            'season':item['infolabels'].get('season', ''), 'episode':item['infolabels'].get('episode', ''), 
                            'type':item['infolabels'].get('type', ''), 'img':item['infolabels'].get('img', ''), 'favorite':'true',
                            'imdb_id':item['infolabels'].get('imdb_id', ''), 'video_type':item['infolabels'].get('video_type', ''),
                            'urls':item['infolabels'].get('urls', '') } ) 
                        
            elif section_items_count == 2:
            
                items = fav.get_my_favorites(section_items[0], section_items[1])
                
                for item in items:

                    id = common.CreateIdFromString(item['title'])
                    list.append( {'indexer':item['infolabels'].get('indexer', ''), 'mode':item['infolabels'].get('mode',''), 
                        'title':item['title'], 'item_title':item['infolabels'].get('item_title', ''), 'url':item['infolabels'].get('url', ''), 'id':id, 
                        'website':item['infolabels'].get('indexer_id', ''), 'indexer_id':item['infolabels'].get('indexer_id', ''), 
                        'name':item['infolabels'].get('name', ''), 'year':item['infolabels'].get('year', ''), 
                        'season':item['infolabels'].get('season', ''), 'episode':item['infolabels'].get('episode', ''), 
                        'type':item['infolabels'].get('type', ''), 'img':item['infolabels'].get('img', ''), 'favorite':'true',
                        'imdb_id':item['infolabels'].get('imdb_id', ''), 'video_type':item['infolabels'].get('video_type', ''),
                        'urls':item['infolabels'].get('urls', '') } ) 
        
