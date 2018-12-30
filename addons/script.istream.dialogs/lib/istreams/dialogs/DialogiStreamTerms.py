import xbmcgui

class DialogiStreamTerms( xbmcgui.WindowXMLDialog ):
    def __init__( self, *args, **kwargs ):
        self.btn_OK = kwargs['btn_OK'] 
    
    def onInit( self ):
        if self.btn_OK == False:
            self.getControl(10).setEnabled(True)
            self.getControl(10).setVisible(True)
            self.getControl(11).setEnabled(True)
            self.getControl(11).setVisible(True)
            self.getControl(13).setEnabled(False)
            self.getControl(13).setVisible(False)
            self.setFocusId(61)
        else:
            self.getControl(10).setEnabled(False)
            self.getControl(10).setVisible(False)
            self.getControl(11).setEnabled(False)
            self.getControl(11).setVisible(False)
            self.getControl(13).setEnabled(True)
            self.getControl(13).setVisible(True)
            self.setFocusId(62)
    
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ):         
        if controlID==11:
            from entertainment import common
            common.addon.set_setting('istream_first_run', 'false')
            self.close()
        elif controlID==10:
            self.close()
        elif controlID==12:
            self.close()
        elif controlID==13:
            self.close()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            self.close()
            
    
        
def show(btn_OK = False):
    
    import xbmcaddon
    addon_id = 'script.istream.dialogs'
    ADDON = xbmcaddon.Addon(id = addon_id)
    
    from entertainment import common    
    dlg = DialogiStreamTerms("DialogiStreamTerms.xml",ADDON.getAddonInfo('path'),'istream',btn_OK=btn_OK)
    dlg.doModal()
    del dlg