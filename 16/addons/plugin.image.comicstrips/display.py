
import xbmcgui
import xbmc
import xbmcaddon
import re
import utils

from threading import Timer 


ACTION_PARENT_DIR    = 9
ACTION_PREVIOUS_MENU = 10
ACTION_BACK          = 92
ACTION_X             = 13

ACTION_LEFT  = 1
ACTION_RIGHT = 2
ACTION_UP    = 3
ACTION_DOWN  = 4

CTRL_STRIP    = 5001
CTRL_PREFETCH = 5002
CTRL_PREV     = 5003
CTRL_PREV_BTN = 5004
CTRL_NEXT     = 5005
CTRL_NEXT_BTN = 5006


ADDONID = utils.ADDONID
URL     = utils.URL
ADDON   = xbmcaddon.Addon(ADDONID)


class Display(xbmcgui.WindowXMLDialog):
    def __new__(cls, url, slideshow):
        return super(Display, cls).__new__(cls, 'main.xml', ADDON.getAddonInfo('path'))


    def __init__(self, url, slideshow): 
        super(Display, self).__init__()
        self.timer      = None
        self.url        = url
        self.slideshow  = slideshow
        self.transition = int(ADDON.getSetting('TRANSITION'))


    def onInit(self):
        self.Clear()

        if self.slideshow:
            url = utils.GetRandomURL(self.url)
        else:
            isCurrent = ADDON.getSetting('DISPLAY') == '0'

            if isCurrent:
                url = utils.GetCurrentURL(self.url)
            else:
                url = utils.GetRandomURL(self.url)

        self.UpdateImage(url)


    def Clear(self):
        self.title    = ''
        self.image    = None
        self.previous = None
        self.next     = None
        self.author   = ''
        self.date     = ''

        if self.timer:
            self.timer.cancel()
            del self.timer
            self.timer = None

              
    def OnClose(self):
        self.Clear()
        self.close()


    def onAction(self, action):
        actionID = action.getId()
        buttonID = action.getButtonCode()

        if actionID in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK, ACTION_X]:
            self.OnClose()

        if self.slideshow:
            return

        if actionID in [ACTION_LEFT, ACTION_UP]:
            if self.previous:
                self.UpdateImage(URL + self.previous)

        if actionID in [ACTION_RIGHT, ACTION_DOWN]:
            if self.next:
                self.UpdateImage(URL + self.next)
            
                                 
    def onClick(self, controlId):
        if controlId == CTRL_PREV_BTN:
            self.Previous()

        if controlId == CTRL_NEXT_BTN:
            self.Next()


    def Previous(self):
        if not self.previous:
            return False

        return self.UpdateImage(URL + self.previous)        


    def Next(self):
        if not self.next:
            return False

        return self.UpdateImage(URL + self.next)


    def onTimer(self):
        if self.next:
            self.UpdateImage(URL + self.next)

        self.UpdateImage(utils.GetRandomURL(self.url))


    def UpdateImage(self, url):
        self.Clear()

        #html  = utils.GetHTML(url)
        html  = utils.GetHTML(url, useCache=True, timeout=86400/2)
        html  = html.replace('\n', '')
        html  = html.split('<p >')[-1]

        match = re.compile('<p><a class="feature-title " href=".+?">(.+?)</a></p>.+?<img alt=".+?" src="(.+?)".+?<strong>(.+?)</strong>(.+?)</span>').findall(html)

        self.title  = match[0][0]
        self.image  = match[0][1]
        self.date   = match[0][2]
        self.author = match[0][3]

        try:
           self.previous = re.compile('btn-archive-older"><a href="(.+?)">&lt').search(html).groups(1)[0]
        except:
            pass

        try:
           self.next = re.compile('btn-archive-newer"><a href="(.+?)">Newer').search(html).groups(1)[0]
        except Exception, e:
           pass  
        
        if self.image:
            self.setControlImage(CTRL_STRIP, self.image)

        #pre-fetch previous and next images
        if self.previous:
            self.setControlImage(CTRL_PREFETCH, self.getImage(utils.GetHTML(URL + self.previous)))
        if self.next:
            self.setControlImage(CTRL_PREFETCH, self.getImage(utils.GetHTML(URL + self.next)))

        self.UpdateControls()

        if self.slideshow:
            self.timer = Timer(self.transition, self.onTimer)
            self.timer.start()

        return True


    def getImage(self, html):
        img = ''
        try:
            html  = html.replace('\n', '')
            html  = html.split('<p >')[-1]
            match = re.compile('(.+?)</p>.+?<img alt=".+?" src="(.+?)".+?<strong>(.+?)</strong>(.+?)</span>').findall(html)
            img   = match[0][1]
        except:
           pass

        return img
        

    def setControlImage(self, id, image):
        if image == None:
            return

        try:    self.getControl(id).setImage(image)
        except: pass


    def UpdateControls(self):
        try:
            self.getControl(CTRL_PREV).setVisible(    (not self.slideshow) and (self.previous != None))
            self.getControl(CTRL_PREV_BTN).setVisible((not self.slideshow) and (self.previous != None))
            self.getControl(CTRL_NEXT).setVisible(    (not self.slideshow) and (self.next     != None))  
            self.getControl(CTRL_NEXT_BTN).setVisible((not self.slideshow) and (self.next     != None))
        except Exception, e:
            pass