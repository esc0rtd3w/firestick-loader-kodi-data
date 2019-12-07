# coding: utf-8
# Name:        provider.py
# Author:      Mancuniancol
# Created on:  28.11.2016
# Licence:     GPL v.3: http://www.gnu.org/copyleft/gpl.html
"""
Create a custom select dialog
The original code was borrowed from Quasar
https://github.com/scakemyer/plugin.video.quasar
"""

import xbmcgui,xbmc

# Constants
ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10
KEY_NAV_BACK = 92


def check_quality(text=""):
    """
    Standard text for quality based in the filename
    :param text: filename
    :type text: str
    :return: standard text for quality
    """
    text = text.lower()
    key_words = {"Cam": ["camrip", "cam"],
                 "Telesync": ["ts", "telesync", "pdvd"],
                 "Workprint": ["wp", "workprint"],
                 "Telecine": ["tc", "telecine"],
                 "Pay-Per-View Rip": ["ppv", "ppvrip"],
                 "Screener": ["scr", "screener", "screeener", "dvdscr", "dvdscreener", "bdscr"],
                 "DDC": ["ddc"],
                 "R5": ["r5", "r5.line", "r5 ac3 5 1 hq"],
                 "DVD-Rip": ["dvdrip", "dvd-rip"],
                 "DVD-R": ["dvdr", "dvd-full", "full-rip", "iso rip", "lossless rip", "untouched rip", "dvd-5 dvd-9"],
                 "HDTV": ["dsr", "dsrip", "dthrip", "dvbrip", "hdtv", "pdtv", "tvrip", "hdtvrip", "hdrip", "hdit",
                          "high definition"],
                 "VODRip": ["vodrip", "vodr"],
                 "WEB-DL": ["webdl", "web dl", "web-dl"],
                 "WEBRip": ["web-rip", "webrip", "web rip"],
                 "WEBCap": ["web-cap", "webcap", "web cap"],
                 "BD/BRRip": ["bdrip", "brrip", "blu-ray", "bluray", "bdr", "bd5", "bd", "blurip"],
                 "MicroHD": ["microhd"],
                 "FullHD": ["fullhd"],
                 "BR-Line": ["br line"],
                 # video formats
                 "x264": ["x264", "x 264"],
                 "x265 HEVC": ["x265 hevc", "x265", "x 265", "hevc"],
                 # audio
                 "DD5.1": ["dd5 1", "dd51", "dual audio 5"],
                 "AC3 5.1": ["ac3"],
                 "ACC": ["acc"],
                 "DUAL AUDIO": ["dual", "dual audio"],
                 }
    color = {"Cam": "FFF4AE00",
             "Telesync": "FFF4AE00",
             "Workprint": "FFF4AE00",
             "Telecine": "FFF4AE00",
             "Pay-Per-View Rip": "FFD35400",
             "Screener": "FFD35400",
             "DDC": "FFD35400",
             "R5": "FFD35400",
             "DVD-Rip": "FFD35400",
             "DVD-R": "FFD35400",
             "HDTV": "FFD35400",
             "VODRip": "FFD35400",
             "WEB-DL": "FFD35400",
             "WEBRip": "FFD35400",
             "WEBCap": "FFD35400",
             "BD/BRRip": "FFD35400",
             "MicroHD": "FFD35400",
             "FullHD": "FFD35400",
             "BR-Line": "FFD35400",
             # video formats
             "x264": "FFFB0C06",
             "x265 HEVC": "FFFB0C06",
             # audio
             "DD5.1": "FF089DE3",
             "AC3 5.1": "FF089DE3",
             "ACC": "FF089DE3",
             "DUAL AUDIO": "FF089DE3",
             }
    text_quality = ""
    for key in key_words:
        for keyWord in key_words[key]:
            if ' ' + keyWord + ' ' in ' ' + text + ' ':
                text_quality += " [COLOR %s][%s][/COLOR]" % (color[key], key)

    if "480p" in text:
        text_quality += " [COLOR FFF4AE00][480p][/COLOR]"

    if "720p" in text:
        text_quality += " [COLOR FF5CD102][720p][/COLOR]"

    if "1080p" in text:
        text_quality += " [COLOR FF2980B9][1080p][/COLOR]"

    if "3d" in text:
        text_quality += " [COLOR FFD61515][3D][/COLOR]"

    if "4k" in text:
        text_quality += " [COLOR FF16A085][4K][/COLOR]"

    return text_quality


class DialogSelect(xbmcgui.WindowXMLDialog):
    """
    Dialog select class
    """

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXML.__init__(self, *args)
        self.items = kwargs.get('items', [])
        self.title = kwargs.get('title', '')
        self.count = 0
        self.ret = -1

        

    def onInit(self):
        """
        Creation of the dialog with the information from kwargs
        """
        self.getControl(32501).setLabel(self.title)
        for item in self.items:
            
            quality = item["quality"]
            
            label1 = "[B]%s[/B] | %s" % (item["provider"], item["source"])
            label2 = quality
            icon =''
            played = ''
            self.addItem(label1, label2, icon, played)
           
        
    def onClick(self, control_id):
        """
        On click
        :param control_id:
        """
        if control_id == 32500:
            # Close Button
            self.close()

        elif control_id == 32503:
            # Panel
            list_control = self.getControl(32503)
            selected = list_control.getSelectedItem()
            self.ret = int(selected.getProperty('index'))
            self.close()

    def onAction(self, action):
        """
        On action
        :param action: action linked to key
        """
        if action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK, ACTION_PREVIOUS_MENU]:
            self.close()

    def addItem(self, label1="", label2="", icon=None, played=False):
        """
        Adding an item
        :param label1: first line
        :type label1: str
        :param label2: second line
        :type label2: str
        :param icon: path icon
        :type icon: str
        :param played: if the video was selected before
        :type played: bool
        """
        list_control = self.getControl(32503)
        item = xbmcgui.ListItem(label1, label2)
        item.setProperty('index', str(self.count))
        item.setIconImage(icon)
        item.setProperty('Played', played)
        list_control.addItem(item)
        self.count += 1
        
