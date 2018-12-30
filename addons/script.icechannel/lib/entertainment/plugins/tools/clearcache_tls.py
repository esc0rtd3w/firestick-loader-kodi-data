from entertainment.plugnplay.interfaces import Tools
from entertainment.plugnplay import Plugin
from entertainment import common

class clearcache(Tools):

    implements = [Tools]
    
    name='clear_cache'
    display_name='Clear internet cache...'
    img = ''
    fanart = ''
    notify_msg_header = 'Operation: Cache Cleanup'
    notify_msg_success = 'The operation completed successfully.'
    notify_msg_failure = 'The operation failed; Please check logs.'
    priority = 100
    
    def Execute(self):
        from entertainment.net import Net
        net = Net()
        return net.clear_cache()
