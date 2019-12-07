import xbmc
import xbmcgui

# xbmc global Variable
iStreamProgressDialogNoAd = ""
iStreamProgressDialogNoAdCancelled = False

class DialogiStreamProgressNoAd( xbmcgui.WindowXMLDialog ):

    def onInit(self):
        self.getControl(1).setLabel( self.header )
        
        self.progressMessageList = self.getControl(3)
        self.addUpdateItem(self.first_list_item)
        
        xbmcgui.Window(10000).setProperty('ISTREAM-PROGRES-DIALOG-CANCELLED', 'FALSE')
        
    def setVars(self, header, first_list_item):
        self.header = header
        self.first_list_item = first_list_item
        
    def waitForInit(self):
        import time
        initialized = False
        while initialized == False :
            try:
                self.progressMessageList.size()
                initialized = True
            except:
                time.sleep(0.2)
            
             
    def onFocus( self, controlID ): pass
    
    def onClick( self, controlID ): 
        if controlID in [101, 102]:
            global iStreamProgressDialogNoAdCancelled
            iStreamProgressDialogNoAdCancelled = False            
            xbmcgui.Window(10000).setProperty('ISTREAM-PROGRES-DIALOG-CANCELLED', 'TRUE')            
            self.getControl(1).setLabel( self.header + ' - Cancelling...' )
        
    def onAction( self, action ):        
        if action in [ 5, 6, 7, 8, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261, 102, 101 ]:
            self.getControl(1).setLabel( self.header + ' - Cancelling...' )            
            global iStreamProgressDialogNoAdCancelled
            iStreamProgressDialogNoAdCancelled = False
            xbmcgui.Window(10000).setProperty('ISTREAM-PROGRES-DIALOG-CANCELLED', 'TRUE')
            
            
    def addItem(self, label):
        self.waitForInit()
        self.progressMessageList.addItem(label)
        self.progressMessageList.selectItem(self.progressMessageList.size() - 1)
    
    def updateItem(self, label, index):
        self.waitForInit()
        self.progressMessageList.getListItem(index).setLabel(label)
        self.progressMessageList.selectItem(index)
        
    def addUpdateItem(self, label, index=-1):
        self.waitForInit()
        if (index == -1 or index >= self.progressMessageList.size()):
            self.addItem(label)
        else:
            self.updateItem(label, index)   
    
            
def show(header="", first_list_item=""):
    
    global iStreamProgressDialogNoAdCancelled
    iStreamProgressDialogNoAdCancelled = False
    
    global iStreamProgressDialogNoAd
    if iStreamProgressDialogNoAd and iStreamProgressDialogNoAd != "":
        iStreamProgressDialogNoAd.show()
    
    import xbmcaddon
    addon_id = 'script.istream.dialogs'
    ADDON = xbmcaddon.Addon(id = addon_id)
    iStreamProgressDialogNoAd = DialogiStreamProgressNoAd("DialogiStreamProgressNoAd.xml",ADDON.getAddonInfo('path'),'istream')
    iStreamProgressDialogNoAd.setVars(header, first_list_item)
    iStreamProgressDialogNoAd.show()
    import xbmc
    xbmc.sleep(1000)
    
def addUpdateItem( label, index = -1 ):
    global iStreamProgressDialogNoAd
    iStreamProgressDialogNoAd.addUpdateItem(label, index)
    
def close():
    global iStreamProgressDialogNoAd
    iStreamProgressDialogNoAd.close()
    del iStreamProgressDialogNoAd
    iStreamProgressDialogNoAd = ""
    
    