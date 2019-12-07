"""
Meta and Base Classes for basic Channel Support

"""

STATUS_BAD, STATUS_UGLY, STATUS_GOOD = 0, 1, 2

class ChannelRegistry(object):
    
    def __init__(self):
        self.channels = {}
        
        
    def register(self, channel_class):
        """
        Registers a channel subclass for use by the plugin.
        
        """
        sn = channel_class.short_name
        if sn in self.channels:
            raise Exception("a channel with the short_name '%s' is already registered."%sn)
        
        self.channels[channel_class.short_name] = channel_class
        
        
    def unregister(self, channel_class_or_short_name):
        """
        Un-register a channel subclass.
        
        """
        if isinstance(channel_class_or_short_name, Channel):
            sn = channel_class_or_short_name.short_name
        else:
            sn = channel_class_or_short_name
            
        if sn not in self.channels:
            raise Exception("channel %s is not registered" % (sn,))
        
        del self.channels[sn]
        
        
class ChannelMetaClass(type):
    
    registry = ChannelRegistry()
    
    def __init__(cls, name, bases, d):
        is_abstract = d.get('is_abstract', False)
        super(ChannelMetaClass, cls).__init__(name, bases, d)

        
        if not is_abstract:
            cls.registry.register(cls)

            
class ChannelException(Exception): pass


class BaseChannel(object):
    """
    The Base of all Channel classes.

    
    """
    short_name = None
    long_name = None
    icon_path = None
    description = None
    root_url = ''
    swf_url = None
    is_abstract = True
    status = STATUS_GOOD
    default_action = 'browse'
    __metaclass__ = ChannelMetaClass

    
    def __init__(self, plugin, **kwargs):
        self.plugin = plugin
        self.args = kwargs

    @classmethod
    def get_channel_entry_info(self):
        """
        This method is responsible for returning the info 
        used to generate the Channel listitem at the plugin's
        root level.
        
        """
        info = {
            'Title': self.long_name,
            'Thumb': self.icon_path,
            'action': self.default_action,
            'remote_url': None,
            'channel': self.short_name,
            'use_rtmp': 1,
        }
    
        if self.status == STATUS_BAD:
            info['Title'] += " [Bad]"
            
        if self.status == STATUS_UGLY:
            info['Title'] += " [Ugly]"
        
        return info
    
    def action_browse(self):
        rurl = self.get_url(self.args['remote_url'])
        self.plugin.add_list_item({'Title': 'Hi!'})
        self.plugin.end_list()

    
    def get_url(self, url=None):
        if url is None:
            url = self.get_root_url()
        return "%s%s" % (self.base_url, url)
    
    def get_root_url(self):
        return self.root_url
    
    
    def __call__(self):
        action = self.args.get('action', 'browse')
        if not hasattr(self, 'action_%s' % (action,)):
            raise ChannelException("No Such Action: %s" % (action,))

        action_method = getattr(self, 'action_%s' % (action, ))
        return action_method()    
