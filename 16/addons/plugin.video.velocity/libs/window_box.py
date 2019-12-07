# -*- coding: utf-8 -*-
# Download Status Module by: Blazetamer (2014)
import os
import xbmc
import xbmcaddon
from libs import addonwindow as pyxbmct
import kodi
from libs import message

addon_id=kodi.addon_id
_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')

file_name = "http://trakt.tv/pin/7558"

artwork = xbmc.translatePath(os.path.join('special://home','addons',addon_id,'resources','art/'))


class MyAddon(pyxbmct.AddonDialogWindow):

    def __init__(self, title=''):
        super(MyAddon, self).__init__(title)
        self.setGeometry(700, 450, 9, 3)
        self.set_info_controls()
        self.set_active_controls()
        #self.set_navigation()
        # Connect a key action (Backspace) to close the window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        #self.connect(pyxbmct.ACTION_NAV_BACK, self.stop)

    def set_info_controls(self):
        # Demo for PyXBMCt UI controls.
        top_label = pyxbmct.Label('[COLOR gold]'+file_name+'[/COLOR]', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(top_label, 0, 1)
        #

        label_label = pyxbmct.Label('or', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(label_label, 2, 1)
        #totalsize_label = pyxbmct.Label(file_total_size, alignment=pyxbmct.ALIGN_CENTER)
        #self.placeControl(totalsize_label, 2, 0)


        # Label
        dld_label = pyxbmct.Label('Visit above url', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(dld_label, 1, 1)
        dld_label = pyxbmct.Label('Scan QR Code Below', alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(dld_label, 3, 1)
        #
        #

        #dlSpeed_label = pyxbmct.Label('Download Speed', alignment=pyxbmct.ALIGN_CENTER)
        #self.placeControl(dlSpeed_label, 1, 2)
        #speed_label = pyxbmct.Label(dlspeed, alignment=pyxbmct.ALIGN_CENTER)
        #self.placeControl(speed_label, 2, 2)


        # TextBox
        #
        #image_label = pyxbmct.Label('Cover Art>>')
        #self.placeControl(image_label, 5, 0)
        self.image = pyxbmct.Image(artwork+'qr_code.png')
        self.placeControl(self.image, 4, 1, 4, 1)
        

    def set_active_controls(self):
        '''int_label = pyxbmct.Label(file_name, alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(int_label, 0, 2, 1, 2)'''
        
        # Close Button
        #self.button = pyxbmct.Button('Cancel')
        #self.placeControl(self.button, 8, 2)
        # Connect control to close the window.
        #self.connect(self.button, self.close)
        
        #Stop DL Button
        self.button = pyxbmct.Button('Next/Enter Pin')
        self.placeControl(self.button, 8, 1)
        # Connect control to stop the download.
        self.connect(self.button, self.enter_pin)

        #Enter Pin Box
        #self.button = pyxbmct.Edit('Text')
        #self.placeControl(self.button, 8, 1)
        # Connect control to stop the download.
        #self.connect(self.button, self.close)

    def enter_pin(self):
        print "SEND TO PIN INPUT"
        message.pininput()
        self.button = pyxbmct.Button('CLOSE WINDOW')
        self.placeControl(self.button, 8, 2)
        # Connect control to stop the download.
        self.connect(self.button, self.close)


    def radio_update(self):
        # Update radiobutton caption on toggle
        if self.radiobutton.isSelected():
            self.radiobutton.setLabel('On')
        else:
            self.radiobutton.setLabel('Off')

    def list_update(self):
        # Update list_item label when navigating through the list.
        try:
            if self.getFocus() == self.list:
                self.list_item_label.setLabel(self.list.getListItem(self.list.getSelectedPosition()).getLabel())
            else:
                self.list_item_label.setLabel('')
        except (RuntimeError, SystemError):
            pass

    def setAnimation(self, control):
        # Set fade animation for all add-on window controls
        control.setAnimations([('WindowOpen', 'effect=fade start=0 end=100 time=500',),
                                ('WindowClose', 'effect=fade start=100 end=0 time=500',)])


def run_box():
    window = MyAddon('Velocity/Trakt.tv Intergration')
    window.doModal()
    # Destroy the instance explicitly because
    # underlying xbmcgui classes are not garbage-collected on exit.
    del window
    return
