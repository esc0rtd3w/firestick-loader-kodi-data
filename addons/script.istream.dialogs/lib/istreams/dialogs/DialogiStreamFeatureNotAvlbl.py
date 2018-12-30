import xbmcgui
import xbmc
import time

class DialogiStreamFeatureNotAvlbl( xbmcgui.WindowXMLDialog ):

    def __init__( self, *args, **kwargs ):
        self.shut = kwargs['close_time'] 
        self.header = kwargs['header'] 
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        xbmc.executebuiltin( "Skin.SetBool(AnimeWindowXMLDialogClose)" )
                                       
    def onInit( self ):
        self.getControl(9001).setLabel( self.header )
        while self.shut > 0:
            xbmc.sleep(1000)
            self.shut -= 1
        xbmc.Player().stop()
        self._close_dialog()
        return
                
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID==12:
            self.shut = 0

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            self.shut = 0
            
    def _close_dialog( self ):
        xbmc.executebuiltin( "Skin.Reset(AnimeWindowXMLDialogClose)" )
        time.sleep( .4 )
        self.close()
        return
            
    
        
def show( header='iStream: Feature Not Available' ):
    
    import xbmcaddon
    addon_id = 'script.istream.dialogs'
    ADDON = xbmcaddon.Addon(id = addon_id)
    
    from entertainment import common    
    dlg = DialogiStreamFeatureNotAvlbl("DialogiStreamFeatureNotAvlbl.xml",ADDON.getAddonInfo('path'),'istream', close_time=15, header=header)
    dlg.doModal()
    del dlg