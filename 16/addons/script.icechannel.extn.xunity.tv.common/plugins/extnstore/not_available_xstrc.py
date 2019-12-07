from entertainment.plugnplay.interfaces import ExtensionStoreConcrete

class iStream_Extn_Store_Not_Available(ExtensionStoreConcrete):

    implements = [ExtensionStoreConcrete]
    
    name='not_available_extn_store'
    display_name='Extn Store Not Available'
    
    def LoadStoreAndExtensions(self, list, lock, message_queue):
        list.append({'mode':'FEATURE_NOT_SUPPORTED'})
        from entertainment import common
        common.ShowFeatureNotAvlblDialog('iStream Extensions Installer')
        