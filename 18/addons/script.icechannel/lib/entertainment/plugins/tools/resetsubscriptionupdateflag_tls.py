from entertainment.plugnplay.interfaces import Tools
from entertainment.plugnplay import Plugin
from entertainment import common

class resetsubscriptionupdateflag(Tools):

    implements = [Tools]
    
    name='reset_subscription_update_flag'
    display_name='Reset subscription update flag...'
    img = ''
    fanart = ''
    notify_msg_header = 'Operation: Reset Subscription Update Flag'
    notify_msg_success = 'The operation completed successfully.'
    notify_msg_failure = 'The operation failed; Please check logs.'
    priority = 100
    show_in_context_menu = True
    
    def Execute(self):
    
        success = True
        
        try:
            common.ClearGlobalProperty( common.gb_Lib_Subs_Op_Running )
        except:
            success = False
        
        return success
