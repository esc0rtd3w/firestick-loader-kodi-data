import xbmc
import xbmcgui
import datetime
import time
# xbmc global Variable
iStreamProgressDialog = ""
sticky = ""
iStreamProgressDialogCancelled = False
PlayAD = True

class Player(xbmc.Player):
    def setVars(self, p_sticky):
        self.sticky = p_sticky
                
    def onPlayBackStarted(self):
        import threading        
        threading.Thread(target=self.sticky.playerTracker).start()
    
    def onPlayBackEnded(self):
        self.sticky.force = True

    
        
class sticky:
    def __init__(self, min_ad_duration=15):
        
        import xbmcgui
        self.force = False
        self.win = xbmcgui.Window(10000)
        self.stickyUrlSep = "||sticky-URL-SEP||"
        self.stickyAdRequestUrl = self.win.getProperty("sticky-AD-REQUEST-URL")
        self.stickyVideoAd = self.win.getProperty("sticky-VIDEO-AD")
        self.stickyVideoAdDur = self.ConvertStringToInt(self.win.getProperty("sticky-VIDEO-AD-DURATION"))
        self.stickyVideoAd000PctTrackUrls = self.win.getProperty("sticky-VIDEO-AD-000-PCT-URL-CSV")
        self.stickyVideoAd025PctTrackUrls = self.win.getProperty("sticky-VIDEO-AD-025-PCT-URL-CSV")
        self.stickyVideoAd050PctTrackUrls = self.win.getProperty("sticky-VIDEO-AD-050-PCT-URL-CSV")
        self.stickyVideoAd075PctTrackUrls = self.win.getProperty("sticky-VIDEO-AD-075-PCT-URL-CSV")
        self.stickyVideoAd100PctTrackUrls = self.win.getProperty("sticky-VIDEO-AD-100-PCT-URL-CSV")
        self.stickyClientIP = self.win.getProperty("sticky-CLIENT-IP")
        self.min_ad_duration = min_ad_duration
        if not self.stickyClientIP or len(self.stickyClientIP) <= 0 or self.stickyClientIP == '0.0.0.0':
            self.stickyClientIP = self.get_external_ip()
            self.win.setProperty('sticky-CLIENT-IP', self.stickyClientIP )
        


    def get_external_ip(self):
        
        import urllib2,xbmcaddon
        import re
        PLUGIN='script.istream.dialogs'
        ADDON = xbmcaddon.Addon(id=PLUGIN)
        
        if ADDON.getSetting('ip')=='':        
             try:

                    site = urllib2.urlopen("http://api.ipify.org/?format=json",timeout=2).read()
                    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
                    address = grab[0]
                    ADDON.setSetting('ip',address)
             except:       
                try:

                        site = urllib2.urlopen("http://checkip.dyndns.com/").read()
                        grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
                        address = grab[0]
                        ADDON.setSetting('ip',address)
                except:
                    address = "0.0.0.0"
        else:
            
            address=ADDON.getSetting('ip')
        return address
    

    
    def ConvertStringToInt(self, s):
     
        if '.' in str(s):
           s= str(s).split('.')[0]
        try: 
            return int(s)
        except ValueError:
            return 0
            
    def load(self, ad_request_url="http://ads.stickyadstv.com/www/delivery/swfIndex.php?reqType=AdsSetup&protocolVersion=2.0&zoneId=1380529", force=False):

        try:
            if xbmc.getCondVisibility('Skin.HasSetting(ShowBackgroundVideo)')==0:
                xbmc.executebuiltin("Skin.SetBool(ShowBackgroundVideo)")
        except:pass    
        self.stickyAdRequestUrl = ad_request_url
        
        self.win.setProperty('sticky-AD-REQUEST-URL', self.stickyAdRequestUrl)
                
        ad_ip_append = ""
        if self.stickyClientIP and len(self.stickyClientIP) > 0 and self.stickyClientIP != "0.0.0.0":
            ad_ip_append = "&client_ip=" + self.stickyClientIP
        import urllib2
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        
        video_url = None
        video_url_retry = 1
        
        while video_url == None and video_url_retry > 0:
            
                    try:
                            video_url_retry = video_url_retry - 1
                            req = urllib2.Request(self.stickyAdRequestUrl, None, headers)
                            sticky_ad_data = urllib2.urlopen(req, timeout=3).read()
                            
                            import re
                            #video_url = re.search('(?s)<flash_streaming_url.+?(http.+?\.flv)', sticky_ad_data)
                            video_url = re.search("type='video/mp4'.+?\[CDATA\[(.+?)\]\]></MediaFile>", sticky_ad_data)
                    except:
                            pass
                
        
        if video_url:
            
            video_url = video_url.group(1)
            self.stickyVideoAd = video_url
            self.win.setProperty('sticky-VIDEO-AD', self.stickyVideoAd )
            
            DURATIONTIME=re.search('<Duration>(.+?)</Duration>', yume_ad_data).group(1)
            
            if 'CDATA' in DURATIONTIME:
                DURATIONTIME = re.compile('([0-9][0-9]:[0-9][0-9]:[0-9][0-9])').findall(DURATIONTIME)[0]
            
            x = time.strptime(DURATIONTIME,'%H:%M:%S')
            self.stickyVideoAdDur = self.ConvertStringToInt(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
            self.win.setProperty('sticky-VIDEO-AD-DURATION', str(self.stickyVideoAdDur) )
            
            sticky_000_pcts = ""
            pct_000 = 0
            for sticky_000_pct in re.finditer("<Tracking event='start'><!\[CDATA\[(.+?)\]", sticky_ad_data):
                if pct_000 > 0:
                    sticky_000_pcts += self.stickyUrlSep
                sticky_000_pcts += sticky_000_pct.group(1)
                pct_000 += 1
            self.stickyVideoAd000PctTrackUrls = sticky_000_pcts
            self.win.setProperty('sticky-VIDEO-AD-000-PCT-URL-CSV', self.stickyVideoAd000PctTrackUrls) 
            
            sticky_025_pcts = ""
            pct_025 = 0
            for sticky_025_pct in re.finditer("<Tracking event='firstQuartile'><!\[CDATA\[(.+?)\]", sticky_ad_data):
                if pct_025 > 0:
                    sticky_025_pcts += self.stickyUrlSep
                sticky_025_pcts += sticky_025_pct.group(1)
                pct_025 += 1
            self.stickyVideoAd025PctTrackUrls = sticky_025_pcts
            self.win.setProperty('sticky-VIDEO-AD-025-PCT-URL-CSV', self.stickyVideoAd025PctTrackUrls) 
           
            sticky_050_pcts = ""
            pct_050 = 0
            for sticky_050_pct in re.finditer("<Tracking event='midpoint'><!\[CDATA\[(.+?)\]", sticky_ad_data):
                if pct_050 > 0:
                    sticky_050_pcts += self.stickyUrlSep
                sticky_050_pcts += sticky_050_pct.group(1)
                pct_050 += 1
            self.stickyVideoAd050PctTrackUrls = sticky_050_pcts
            self.win.setProperty('sticky-VIDEO-AD-050-PCT-URL-CSV', self.stickyVideoAd050PctTrackUrls) 
        
            sticky_075_pcts = ""
            pct_075 = 0
            for sticky_075_pct in re.finditer("<Tracking event='thirdQuartile'><!\[CDATA\[(.+?)\]", sticky_ad_data):
                if pct_075 > 0:
                    sticky_075_pcts += self.stickyUrlSep
                sticky_075_pcts += sticky_075_pct.group(1)
                pct_075 += 1
            self.stickyVideoAd075PctTrackUrls = sticky_075_pcts
            self.win.setProperty('sticky-VIDEO-AD-075-PCT-URL-CSV', self.stickyVideoAd075PctTrackUrls) 
                
            sticky_100_pcts = ""
            pct_100 = 0
            for sticky_100_pct in re.finditer("<Tracking event='complete'><!\[CDATA\[(.+?)\]", sticky_ad_data):
                if pct_100 > 0:
                    sticky_100_pcts += self.stickyUrlSep
                sticky_100_pcts += sticky_100_pct.group(1)
                pct_100 += 1
            self.stickyVideoAd100PctTrackUrls = sticky_100_pcts        
            self.win.setProperty('sticky-VIDEO-AD-100-PCT-URL-CSV', self.stickyVideoAd100PctTrackUrls)
        
        else:
            
            self.stickyVideoAd = ""
            self.win.setProperty('sticky-VIDEO-AD', self.stickyVideoAd )
            self.stickyVideoAdDur = 0
            self.win.setProperty('sticky-VIDEO-AD-DURATION', str(self.stickyVideoAdDur) )
            self.stickyVideoAd000PctTrackUrls = ""
            self.win.setProperty('sticky-VIDEO-AD-000-PCT-URL-CSV', self.stickyVideoAd000PctTrackUrls) 
            self.stickyVideoAd025PctTrackUrls = ""
            self.win.setProperty('sticky-VIDEO-AD-025-PCT-URL-CSV', self.stickyVideoAd025PctTrackUrls) 
            self.stickyVideoAd050PctTrackUrls = ""
            self.win.setProperty('sticky-VIDEO-AD-050-PCT-URL-CSV', self.stickyVideoAd050PctTrackUrls) 
            self.stickyVideoAd075PctTrackUrls = ""
            self.win.setProperty('sticky-VIDEO-AD-075-PCT-URL-CSV', self.stickyVideoAd075PctTrackUrls) 
            self.stickyVideoAd100PctTrackUrls = ""
            self.win.setProperty('sticky-VIDEO-AD-100-PCT-URL-CSV', self.stickyVideoAd100PctTrackUrls) 
            return
                     
        

    def getAd(self, ad_request_url="http://ads.stickyadstv.com/www/delivery/swfIndex.php?reqType=AdsSetup&protocolVersion=2.0&zoneId=1380529"):
        self.load(ad_request_url)        
    
    def trackUrls(self, urls):
        
        import urllib2
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        for url in urls:
            try:    
                
                req = urllib2.Request(url.replace("&amp;","&"), None, headers)
                urllib2.urlopen(req)
            except:
                pass
        
    
    def playerTracker(self, force=False):
        
        self.pct_000_trackers_called = True
        self.trackUrls(filter(None, self.stickyVideoAd000PctTrackUrls.split(self.stickyUrlSep)))
        
        import time
        import threading
        while True:
            if self.pct_025_trackers_called == False and (self.force == True or (self.player.isPlaying() and self.player.getTime() / self.stickyVideoAdDur >= 0.25) ):
                self.pct_025_trackers_called = True
                self.trackUrls(filter(None,self.stickyVideoAd025PctTrackUrls.split(self.stickyUrlSep)))
            if self.pct_050_trackers_called == False and (self.force==True or (self.player.isPlaying() and self.player.getTime() / self.stickyVideoAdDur >= 0.5) ):
                self.pct_050_trackers_called = True
                self.trackUrls(filter(None,self.stickyVideoAd050PctTrackUrls.split(self.stickyUrlSep)))
            if self.pct_075_trackers_called == False and (self.force==True or (self.player.isPlaying() and self.player.getTime() / self.stickyVideoAdDur >= 0.75) ):
                self.pct_075_trackers_called = True
                self.trackUrls(filter(None,self.stickyVideoAd075PctTrackUrls.split(self.stickyUrlSep)))
            if self.pct_025_trackers_called == True and self.pct_050_trackers_called == True and self.pct_075_trackers_called == True:
                break
            time.sleep(3)            
        
        self.pct_100_trackers_called = True
        self.trackUrls(filter(None,self.stickyVideoAd100PctTrackUrls.split(self.stickyUrlSep)))
        
        del self.player
        self.player = ""
        del self
        self=""
    
    def playAd(self, ad_request_url="http://ads.stickyadstv.com/www/delivery/swfIndex.php?reqType=AdsSetup&protocolVersion=2.0&zoneId=1380529"):
        
        self.getAd(ad_request_url)                
        self.player = Player()
        self.player.setVars(self)
        
        self.pct_000_trackers_called = False
        self.pct_025_trackers_called = False
        self.pct_050_trackers_called = False
        self.pct_075_trackers_called = False
        self.pct_100_trackers_called = False
        
        
        self.player.play(self.stickyVideoAd, xbmcgui.ListItem('AD'), True)
        
        
    def stopAd(self):
        
        import xbmc 
        try:
            while self.player.isPlaying() and self.player.getTime() <= self.min_ad_duration:
                xbmc.sleep(1000)
            if self.player.isPlaying():
                self.player.stop()
        except:
            pass
        

        
class DialogiStreamProgress( xbmcgui.WindowXMLDialog ):

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
            global iStreamProgressDialogCancelled
            iStreamProgressDialogCancelled = False            
            xbmcgui.Window(10000).setProperty('ISTREAM-PROGRES-DIALOG-CANCELLED', 'TRUE')            
            self.getControl(1).setLabel( self.header + ' - Cancelling...' )
        
    def onAction( self, action ):        
        if action in [ 5, 6, 7, 8, 9, 10, 92, 117 ] or action.getButtonCode() in [ 275, 257, 261, 102, 101 ]:
            self.getControl(1).setLabel( self.header + ' - Cancelling...' )            
            global iStreamProgressDialogCancelled
            iStreamProgressDialogCancelled = False
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
    
            
def show(header="", first_list_item="", play_ad=True, min_ad_duration=15):
    
    global iStreamProgressDialogCancelled
    iStreamProgressDialogCancelled = False
    
    global iStreamProgressDialog
    if iStreamProgressDialog and iStreamProgressDialog != "":
        iStreamProgressDialog.show()
    
    import xbmcaddon
    addon_id = 'script.istream.dialogs'
    ADDON = xbmcaddon.Addon(id = addon_id)
    iStreamProgressDialog = DialogiStreamProgress("DialogiStreamProgress.xml",ADDON.getAddonInfo('path'),'istream')
    iStreamProgressDialog.setVars(header, first_list_item)
    iStreamProgressDialog.show()
    import xbmc
    xbmc.sleep(1000)
    
    '''global PlayAD
    PlayAD = play_ad
    
    if PlayAD:
        global sticky
    if min_ad_duration < 26:
        min_ad_duration = 26
        sticky = sticky(min_ad_duration=min_ad_duration)
        sticky.playAd()'''

def addUpdateItem( label, index = -1 ):
    global iStreamProgressDialog
    iStreamProgressDialog.addUpdateItem(label, index)
    
def close():

    '''global PlayAD
    if PlayAD:
        global sticky
        sticky.stopAd()'''
    
    global iStreamProgressDialog
    iStreamProgressDialog.close()
    del iStreamProgressDialog
    iStreamProgressDialog = ""
    
    
