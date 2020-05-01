import xbmcgui

extn_act_NONE = "NONE"
extn_act_OK = "OK"
extn_act_CANCEL = "CANCEL"

class DialogiStreamDisclaimer( xbmcgui.WindowXMLDialog ):
    def onInit(self):
        self.ACTION = extn_act_NONE
        
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ):         
        if controlID==11:
            self.ACTION = extn_act_OK
            self.close()
        elif controlID==10:
            self.ACTION = extn_act_CANCEL
            self.close()
        elif controlID==12:
            self.close()

    def onAction( self, action ):
        if action in [ 5, 6, 7, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            self.close()
            
    
        
def show():
    
    ACTION = extn_act_NONE
    
    import xbmcaddon
    addon_id = 'script.istream.dialogs'
    ADDON = xbmcaddon.Addon(id = addon_id)
    
    from entertainment import common    
    dlg = DialogiStreamDisclaimer("DialogiStreamDisclaimer.xml",ADDON.getAddonInfo('path'),'istream')
    dlg.doModal()
    
    ACTION = dlg.ACTION
    
    del dlg
    
    return ACTION