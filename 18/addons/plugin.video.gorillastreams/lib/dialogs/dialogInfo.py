# -*- coding: latin-1 -*-

import xbmcgui

class DialogInfo:

    def __init__(self):
        self.dlg = xbmcgui.Dialog()
        self.head = '[COLOR=FF00FF00]Gorilla Streams Info[/COLOR]'

    def show(self, message):
        self.dlg.ok(self.head, message)
