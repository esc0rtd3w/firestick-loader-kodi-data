from entertainment.plugnplay.interfaces import Tools
from entertainment.plugnplay import Plugin
from entertainment import common

class resetsubscriptionupdateflag(Tools):

    implements = [Tools]
    
    name='reset_first_run_setting'
    display_name='Reset iStream first run setting...'
    img = ''
    fanart = ''
    notify_msg_header = 'Operation: Reset IStream First Run Setting'
    notify_msg_success = 'The operation completed successfully.'
    notify_msg_failure = 'The operation failed; Please check logs.'
    priority = 100
    show_in_context_menu = True
    
    def Execute(self):
    
        success = True
        
        try:
            common.addon.set_setting('istream_first_run', 'true')
        except:
            success = False
        
        return success
