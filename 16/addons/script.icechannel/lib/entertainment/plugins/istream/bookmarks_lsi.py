'''
    Bookmarks
'''

from entertainment.plugnplay.interfaces import ListIndexer
from entertainment.plugnplay import Plugin
from entertainment import common

class Bookmarks(ListIndexer):
    implements = [ListIndexer]
    
    name = "Bookmarks"
    display_name = "Bookmarks"
    
    default_indexer_enabled = 'true'
    
    def GetSection(self, indexer, section, url, type, list, page='', total_pages='', sort_by='', sort_order=''): 
        if section == 'main':
            
            self.AddSection(list, indexer, 'Movies', 'Movies', type='movies', img=common.get_themed_icon('Bookmarks.png'), fanart=common.get_themed_fanart('Bookmarks.jpg'))
            self.AddSection(list, indexer, 'TV Episodes', 'TV Episodes', type='tv_episodes', img=common.get_themed_icon('Bookmarks.png'), fanart=common.get_themed_fanart('Bookmarks.jpg'))
            
        else:
            from universal import playbackengine
            player = playbackengine.Player()
            
            if type == 'movies':
                indexer = common.indxr_Movies                
            elif type == 'tv_episodes':
                indexer = common.indxr_TV_Shows
                
            video_type = common.VideoType_Movies if type=='movies' else common.VideoType_Episode
            
            sql_select = ''
            if playbackengine.DB == 'mysql':
                sql_select = 'SELECT title, season, episode, year FROM bookmarks WHERE addon_id = %s AND video_type = %s'
            else:
                sql_select = 'SELECT title, season, episode, year FROM bookmarks WHERE addon_id = ? AND video_type = ?'
            
            matchedrows = []
            try:
                player._connect_to_db()
                player.dbcur.execute(sql_select, (common.addon_id, video_type) )
                matchedrows = player.dbcur.fetchall()
                player._close_db()
            except:
                pass
                
            for matchedrow in matchedrows:
                item = dict(matchedrow)
                temp_title = item['title'] + ( ' (' + item['year'] + ')' if item['year'] else '' )                    
                if indexer == common.indxr_TV_Shows:
                    temp_title += '_season_' + str(item['season']) + '_episode_' + str(item['episode'])
                    
                id = common.CreateIdFromString(temp_title)
                list.append( {'indexer':indexer, 'mode':common.mode_File_Hosts, 'title':temp_title if indexer == common.indxr_Movies else '', 
                    'id':id, 'website':'bookmarks', 'name':item['title'], 'year':item['year'], 'season':str(item['season']), 'episode':str(item['episode']),
                    'video_type':video_type, 'type':type, 'bookmark':'true' } ) 
