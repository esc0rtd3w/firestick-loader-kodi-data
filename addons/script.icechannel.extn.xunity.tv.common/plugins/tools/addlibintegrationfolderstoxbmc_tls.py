from entertainment.plugnplay.interfaces import Tools
from entertainment.plugnplay import Plugin
from entertainment import common

class addlibintegrationfolderstoxbmc(Tools):

    implements = [Tools]
    
    name='add_lib_integration_folders_to_xbmc'
    display_name='Add/Update iStream integration folders in XBMC Library...'
    img = ''
    fanart = ''
    notify_msg_header = 'Operation: Add/Update iStream integration folders in XBMC Library'
    notify_msg_success = 'The operation completed successfully.'
    notify_msg_failure = 'The operation failed; Please check logs.'
    priority = 100
    show_in_context_menu = True
    
    def Execute(self):
    
        success = True
        
        try:
            from entertainment import common
            common.ShowFeatureNotAvlblDialog('iStream Tools: Add/Update XBMC Integration Folders')
            
        except:
            success = False
        
        return success
