from threading import Thread, RLock

import xbmc,os
import xbmcaddon
import xbmcgui
from resources.lib.modules import control

import time

rt_timeout = 500

def select_ext(title, populator, tasks_count, sort_function = None):
    addonPath = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
    dlg = SelectorDialog("DialogSelectx.xml", addonPath, title=title,
                         populator=populator, steps=tasks_count, sort_function=sort_function)

    with ExtendedDialogHacks():
        dlg.doModal()
        selection = dlg.get_selection()
        del dlg

    return selection


class FanArtWindow(xbmcgui.WindowDialog):
    def __init__(self):
        control_background = xbmcgui.ControlImage(0, 0, 1280, 720, xbmcaddon.Addon().getAddonInfo('fanart'))
        self.addControl(control_background)

        fanart = xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')
        if fanart and fanart != "Fanart_Image":
            control_fanart = xbmcgui.ControlImage(0, 0, 1280, 720, fanart)
            self.addControl(control_fanart)


class ExtendedDialogHacks(object):
    def __init__(self):
        self.active = False

        self.hide_progress = False
        self.hide_info = False

        self.autohidedialogs = False
        if self.autohidedialogs:
            self.hide_progress = False
            self.hide_info = False

        if not self.hide_progress and not self.hide_info:
            self.autohidedialogs = False

    def __enter__(self):
        self.active = True

        #        self.numeric_keyboard = None
        self.fanart_window = FanArtWindow()

        ## Keyboard hack
        #        if plugin.get_setting(SETTING_ADVANCED_KEYBOARD_HACKS, converter=bool):
        #            self.numeric_keyboard = xbmcgui.Window(10109)
        #            Thread(target = lambda: self.numeric_keyboard.show()).start()
        #            wait_for_dialog('numericinput', interval=50)

        # Show fanart background         
        self.fanart_window.show()

        # Run background task
        if self.autohidedialogs:
            Thread(target=self.background_task).start()

    def background_task(self):
        xbmc.sleep(1000)
        while not xbmc.abortRequested and self.active:
            if self.hide_progress:
                active_window = xbmcgui.getCurrentWindowDialogId()
                if active_window in [10101, 10151]:
                    xbmc.executebuiltin("Dialog.Close(%d, true)" % active_window)
            if self.hide_info:
                if xbmc.getCondVisibility("Window.IsActive(infodialog)"):
                    xbmc.executebuiltin('Dialog.Close(infodialog, true)')
            xbmc.sleep(100)

    def __exit__(self, exc_type, exc_value, traceback):
        self.active = False

        #        if self.numeric_keyboard is not None:
        #            self.numeric_keyboard.close()
        #            del self.numeric_keyboard
        #            xbmc.executebuiltin("Dialog.Close(numericinput, true)")

        self.fanart_window.close()
        del self.fanart_window


class SelectorDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.title = kwargs['title']
        self.populator = kwargs['populator']
        self.steps = kwargs['steps']
        self.sort_function = kwargs['sort_function']
        self.time_start = time.time()
        self.timer_active = True
        self.items = []
        self.selection = None
        self.insideIndex = -1
        self.completed_steps = 0
        self.selected = []
        self.thread = None
        self.lock = RLock()

    def get_selection(self):
        """ get final selection """
        self.timer_active = False
        return self.selected

    def onInit(self):
        # set title
        self.label = self.getControl(1)
        self.label.setLabel(self.title)

        # Hide ok button
        self.getControl(5).setVisible(False)

        # Get active list
        try:
            self.list = self.getControl(6)
            # self.list.controlLeft(self.list)
            # self.list.controlRight(self.list)
            self.getControl(3).setVisible(False)
        except:
            self.list = self.getControl(6)
        # self.setFocus(self.list)
        self.progress = self.getControl(2)
        # populate list
        self.thread = Thread(target=self._populate)
        self.thread.start()
        Thread(target=self.sort_method).start()
		
    def onAction(self, action):
        if action.getId() in (9, 10, 92, 216, 247, 257, 275, 61467, 61448,):
            if self.insideIndex == -1:
                self.timer_active = False
                self.close()
            else:
                self._inside_root(select=self.insideIndex)

    def onClick(self, controlID):
        
        if controlID == 6 or controlID == 3:
            num = self.list.getSelectedPosition()
            if num >= 0:
                if self.insideIndex == -1:
                    self._inside(num)
                else:
                    self.selection = self.items[self.insideIndex][1][num]
                    self.close()

    def onFocus(self, controlID):
        if controlID in (3, 61):
            self.setFocus(self.list)

    def _inside_root(self, select=-1):
        with self.lock:
           
            self.list.reset()
            # self.setFocus(self.list)
            for links in self.items:
                
                self.providers_name = links['provider']
                try: quality = links['quality']
                except: quality = "SD"

                if "k" in quality.lower():  q_icon = "4k.png"
                if "1080" in quality:  q_icon = "1080.png"
                elif "HD" in quality: q_icon = "720.png"
                else: q_icon = "sd.png"
                
                # if self.providers_name.lower() == 'kat': q_icon = "kat.jpg"
                # if self.providers_name.lower() == 'thepiratebay': q_icon = "thepiratebay.png"
                # if self.providers_name.lower() == 'yify': q_icon = "yify.jpg"
                # if self.providers_name.lower() == 'leetx': q_icon = "leetx.png"
                # if self.providers_name.lower() == 'idope': q_icon = "idope.jpg"
                # if self.providers_name.lower() == 'limetorrent': q_icon = "lime.png"
                # if self.providers_name.lower() == 'eztv': q_icon = "eztv.png"
                if quality == '4k' or quality == '4K': 	q_icon = "4k.png"					
                try: info = links['info']
                except: info = ""	
                if not info == "": info = " | %s" % info
                
                if links['debridonly'] == True: label = '[I]DEB[/I] | %s | %s' % (quality, links['provider'])
                else: label = '%s | %s' % (quality, links['provider'])
                label2 = "[I]" + str(links['source']) + "[/I]" + info
                label = label + info
				
                listitem = xbmcgui.ListItem(label=label.upper(), label2=label2.upper())
                try:
                    pluginid = "plugin.video.neptune"
                    ARTDIR = xbmc.translatePath(os.path.join('special://home/addons/' + pluginid + '/resources/skins/icons' , ''))
                    icon = ARTDIR + q_icon
                    listitem.setIconImage(icon)
                except:
                    pass
                self.list.addItem(listitem)


            if select >= 0:
                self.list.selectItem(select)
            self.insideIndex = -1

    def _inside(self, num):
        if num == -1:
            self._inside_root(select=self.insideIndex)
            return

        with self.lock:
            links = self.items[num]
            next = [y for x,y in enumerate(self.items) if x > num][:50]
            
            if len(links) >= 1:
                selected_link = links
                self.selected.append(selected_link)
                for next_scrape in next:
					self.selected.append(next_scrape)
                
                self.timer_active = False
                self.close()
                return

            # self.list.reset()

            self.insideIndex = num

    def step(self):
        self.completed_steps += 1
        progress = self.completed_steps * 100 / self.steps
        self.progress.setPercent(progress)
        self.label.setLabel(u"{0} - {1:d}% ({2}/{3})".format("Select Quality ", progress,
                                                             self.completed_steps, self.steps))
															 
			# BACKGROUND TIMER												 
    def sort_method(self):
        while self.timer_active:
			self.time_end = time.time()
			timediff = (self.time_end - self.time_start)
			# print ("NEPTUNE RISING TIMER", (self.time_end - self.time_start))
			if timediff > 4:
				
				self.time_start = time.time()
				self.time_end = time.time()
				self.items = sorted(self.items, key=lambda k: k['quality'])
				xbmc.sleep(100)  
			
															 
        
    def _populate(self):
        # Delay population to let ui settle
        self.label.setLabel(self.title)
        for result in self.populator():
           
            
            self.step()


            if not result:
                continue

            with self.lock:
                # Remember selected item
                selectedItem = None
                if self.insideIndex == -1:
                    selectedIndex = self.list.getSelectedPosition()
                else:
                    selectedIndex = self.insideIndex
                if selectedIndex >= 0:
                    selectedItem = self.items[selectedIndex]

                # Add new item
                # if len(self.items) >= 10: 
					# self.sort_method()   
					
                self.items.extend(result)
                xbmc.sleep(rt_timeout)                


                if selectedItem is not None:
                    selectedIndex = self.items.index(selectedItem)
                

                    if self.insideIndex != -1:
                        self.insideIndex = selectedIndex

                # Update only if in root
                if self.insideIndex == -1:
                    self._inside_root(select=selectedIndex)
                    self.setFocus(self.list)

        pass
