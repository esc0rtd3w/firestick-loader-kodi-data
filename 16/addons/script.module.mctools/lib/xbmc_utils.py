import xbmcgui
from settings import *


class Kodi:
    def __init__(self):
        pass

    @staticmethod
    def text_viewer(text="", once=False):
        if not once or (once and Settings["firstOpen"] not in "NO"):
            Settings["firstOpen"] = "NO"
            w = TextViewerDialog('DialogTextViewer.xml', Settings.path_folder, header=Settings.name, text=text)
            w.doModal()

    @staticmethod
    class Dialog:
        def __init__(self):
            pass

        @staticmethod
        def yesno(title="", message=""):
            return xbmcgui.Dialog().yesno(title, message)

        @staticmethod
        def input(question="", default=""):
            return xbmcgui.Dialog().input(question, default)

        @staticmethod
        def notify(message="", image=None):
            xbmcgui.Dialog().notification(xbmcaddon.Addon().getAddonInfo("name"), message, icon=image)


class TextViewerDialog(xbmcgui.WindowXMLDialog):  # taking from script.toolbox
    ACTION_PREVIOUS_MENU = [9, 92, 10]

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)

        self.text = kwargs.get('text')
        self.header = kwargs.get('header')

    def onInit(self):
        self.getControl(1).setLabel(self.header)
        self.getControl(5).setText(self.text)

    def onAction(self, action):
        if action in self.ACTION_PREVIOUS_MENU:
            self.close()

    def onClick(self, control_id):
        pass

    def onFocus(self, control_id):
        pass
