# -*- coding: latin-1 -*-

import xbmcgui

class DialogQuestion:

    def __init__(self):
        self.dlg = xbmcgui.Dialog()
        self.head = '[COLOR=FF00FF00]Gorilla Streams Question[/COLOR]'

    def ask(self, question):
        return self.dlg.yesno(self.head, question)
    
    def close(self):
        self.dlg.close()
