from entertainment.plugnplay.interfaces import Tools
from entertainment.plugnplay import Plugin
from entertainment import common

class clearsearchhistory(Tools):

    implements = [Tools]
    
    name='clear_search_history'
    display_name='Clear search history...'
    img = ''
    fanart = ''
    notify_msg_header = 'Operation: Search History Cleanup'
    notify_msg_success = 'The operation completed successfully.'
    notify_msg_failure = 'The operation failed; Please check logs.'
    priority = 100
    
    def Execute(self):
        from entertainment import searchhistory
        SH = searchhistory.SearchHistory()
        return SH.clear_search_history()
