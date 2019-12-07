from entertainment.plugnplay.interfaces import Tools
from entertainment.plugnplay import Plugin
from entertainment import common

class clearbookmarks(Tools):

    implements = [Tools]
    
    name='clear_bookmarks'
    display_name='Clear all bookmarks...'
    img = ''
    fanart = ''
    notify_msg_header = 'Operation: Bookmarks Cleanup'
    notify_msg_success = 'The operation completed successfully.'
    notify_msg_failure = 'The operation failed; Please check logs.'
    priority = 100
    
    def Execute(self):
        
        from universal import playbackengine
        player = playbackengine.Player()
        
        sql_delete = 'DELETE FROM bookmarks'
        
        success = True
        
        try:
            player._connect_to_db()
            player.dbcur.execute(sql_delete )
            player.dbcon.commit()
            player._close_db()
        except:
            success = False
        
        return success
