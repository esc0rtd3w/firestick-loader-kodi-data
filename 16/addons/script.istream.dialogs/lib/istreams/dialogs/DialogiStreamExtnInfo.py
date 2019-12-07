import xbmcgui

# EXTENSION ACTIONS
extn_act_NONE = "NONE"
extn_act_UPDATE = "UPDATE"
extn_act_INSTALL = "INSTALL"
extn_act_UNINSTALL = "UNINSTALL"

class DialogiStreamExtnInfo( xbmcgui.WindowXMLDialog ):
    def onInit(self):
    
        self.ACTION = extn_act_NONE
        
        self.getControl(601).setImage( self.extn_details['extn_icon'] )
        
        self.getControl(602).setLabel( '[B]%s[/B]' % self.extn_details['extn_name'] )
        
        if self.extn_details['extn_id'].startswith('script.icechannel.extn.'):
            self.getControl(603).setLabel('Extension')
        elif self.extn_details['extn_id'].startswith('script.icechannel.theme.'):
            self.getControl(603).setLabel('Theme')
            
        self.getControl(604).setLabel( self.extn_details['extn_provider'] )
        
        self.getControl(605).setLabel( self.extn_details['extn_version'] )
        
        if self.extn_details['extn_summary'] and len(self.extn_details['extn_summary']) > 0:
            self.getControl(606).reset()
            self.getControl(606).addLabel( self.extn_details['extn_summary'] )
            
        self.getControl(401).setText( self.extn_details['extn_desc'] )
        
        try:
            import xbmcaddon
            extn_addon = xbmcaddon.Addon(self.extn_details['extn_id'])            
            
            import xbmc
            addons_path = xbmc.translatePath('special://home/addons')
            
            import os
            install_loc = os.path.join(addons_path, self.extn_details['extn_id'])
            
            if os.path.exists(install_loc):
                self.getControl(6).setEnabled(False)
                self.getControl(7).setEnabled(True)
                if extn_addon.getAddonInfo('version') < self.extn_details['extn_version']:
                    self.getControl(8).setEnabled(True)
                else:
                    self.getControl(8).setEnabled(False)
            else:
                self.getControl(8).setEnabled(False)
                self.getControl(6).setEnabled(True)
                self.getControl(7).setEnabled(False)
            
        except:
            self.getControl(8).setEnabled(False)
            self.getControl(6).setEnabled(True)
            self.getControl(7).setEnabled(False)
        
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ):
        if controlID==8:
            self.ACTION = extn_act_UPDATE
        elif controlID==6:
            self.ACTION = extn_act_INSTALL
        elif controlID==7:
            self.ACTION = extn_act_UNINSTALL
        
        if controlID in [6, 7, 8, 12]:
            self.close()

    def onAction( self, action ):    
        
        if action in [ 5, 6, 7, 8, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261 ]:
            self.close()
            
    def setExtnInfo(self, extn_details):
        self.extn_details = extn_details
        
def show( extn_details ):
    
    ACTION = extn_act_NONE
    
    import xbmcaddon
    addon_id = 'script.istream.dialogs'
    ADDON = xbmcaddon.Addon(id = addon_id)
    
    from entertainment import common    
    dlg = DialogiStreamExtnInfo("DialogiStreamExtnInfo.xml",ADDON.getAddonInfo('path'),'istream')
    dlg.setExtnInfo(extn_details)
    dlg.doModal()
    
    ACTION = dlg.ACTION
    
    del dlg
    
    return ACTION