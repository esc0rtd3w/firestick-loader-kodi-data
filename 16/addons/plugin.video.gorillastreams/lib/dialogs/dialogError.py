# -*- coding: latin-1 -*-

import xbmcgui

class DialogError:

    def __init__(self):
        self.dlg = xbmcgui.Dialog()
        self.head = '[COLOR=FF00FF00]Gorilla Streams Error[/COLOR]'

    def show(self, message):
        self.dlg.ok(self.head, message)
        
    def close(self):
        self.dlg.close()
