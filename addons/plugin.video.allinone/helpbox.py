import os
import re
import sys
import xbmc
import xbmcgui

from t0mm0.common.addon import Addon

pluginId = 'plugin.video.allinone'
addon = Addon(pluginId, sys.argv)

class HelpBox:
    # constants
    WINDOW = 10147
    CONTROL_LABEL = 1
    CONTROL_TEXTBOX = 5

    def __init__(self, *args, **kwargs):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % ( self.WINDOW, ))
        # get window
        self.win = xbmcgui.Window(self.WINDOW)
        # give window time to initialize
        xbmc.sleep(1000)
        self.setControls()

    def setControls(self):
        # set heading
        heading = "Entertainment [COLOR dodgerblue][B]HUB[/B][/COLOR] v%s" % (addon.get_version())
        self.win.getControl(self.CONTROL_LABEL).setLabel(heading)
        # set text
        root = addon.get_path()
        faq_path = os.path.join(root, 'help.faq')
        f = open(faq_path)
        text = f.read()
        self.win.getControl(self.CONTROL_TEXTBOX).setText(text)

