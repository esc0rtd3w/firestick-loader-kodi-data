import xbmc
import xbmcgui

# xbmc global Variable
iStreamProgressDialog = ""
yume = ""
iStreamProgressDialogCancelled = False
PlayAD = True

class Player(xbmc.Player):
    def setVars(self, p_YUME):
        self.yume = p_YUME
                
    def onPlayBackStarted(self):
        import threading        
        threading.Thread(target=self.yume.playerTracker).start()
    
    def onPlayBackEnded(self):
        self.yume.force = True

    
        
class YUME:
    def __init__(self, min_ad_duration=15):
        
        import xbmcgui
        self.force = False
        self.win = xbmcgui.Window(10000)
        self.YumeUrlSep = "||YUME-URL-SEP||"
        self.YumeAdRequestUrl = self.win.getProperty("YUME-AD-REQUEST-URL")
        self.YumeVideoAd = self.win.getProperty("YUME-VIDEO-AD")
        self.YumeVideoAdDur = self.ConvertStringToInt(self.win.getProperty("YUME-VIDEO-AD-DURATION"))
        self.YumeVideoAd000PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-000-PCT-URL-CSV")
        self.YumeVideoAd025PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-025-PCT-URL-CSV")
        self.YumeVideoAd050PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-050-PCT-URL-CSV")
        self.YumeVideoAd075PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-075-PCT-URL-CSV")
        self.YumeVideoAd100PctTrackUrls = self.win.getProperty("YUME-VIDEO-AD-100-PCT-URL-CSV")
        self.YumeClientIP = self.win.getProperty("YUME-CLIENT-IP")
        self.min_ad_duration = min_ad_duration
        if not self.YumeClientIP or len(self.YumeClientIP) <= 0 or self.YumeClientIP == '0.0.0.0':
            self.YumeClientIP = self.get_external_ip()
            self.win.setProperty('YUME-CLIENT-IP', self.YumeClientIP )
        
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
        try: 
            return int(s)
        except ValueError:
            return 0
            
    def load(self, ad_request_url="http://plg1.yumenetworks.com/dynamic_preroll_playlist.xml?domain=1992TRzjSSba", force=False):

        try:
            if xbmc.getCondVisibility('Skin.HasSetting(ShowBackgroundVideo)')==0:
                xbmc.executebuiltin("Skin.SetBool(ShowBackgroundVideo)")
        except:pass    
        self.YumeAdRequestUrl = ad_request_url
        
        self.win.setProperty('YUME-AD-REQUEST-URL', self.YumeAdRequestUrl)
                
        ad_ip_append = ""
        if self.YumeClientIP and len(self.YumeClientIP) > 0 and self.YumeClientIP != "0.0.0.0":
            ad_ip_append = "&client_ip=" + self.YumeClientIP
        import urllib2
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        
        video_url = None
        video_url_retry = 1
        
        while video_url == None and video_url_retry > 0:
            
                    try:
                            video_url_retry = video_url_retry - 1
                            req = urllib2.Request(self.YumeAdRequestUrl, None, headers)
                            yume_ad_data = urllib2.urlopen(req, timeout=3).read()
                            
                            import re
                            #video_url = re.search('(?s)<flash_streaming_url.+?(http.+?\.flv)', yume_ad_data)
                            video_url = re.search('(?s)<mp4_streaming_url.+?(http.+?\.mp4)', yume_ad_data)
                    except:
                            pass
                
        
        if not video_url:
            return xbmc.log(fucker)
            self.YumeVideoAd = ""
            self.win.setProperty('YUME-VIDEO-AD', self.YumeVideoAd )
            self.YumeVideoAdDur = 0
            self.win.setProperty('YUME-VIDEO-AD-DURATION', str(self.YumeVideoAdDur) )
            self.YumeVideoAd000PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-000-PCT-URL-CSV', self.YumeVideoAd000PctTrackUrls) 
            self.YumeVideoAd025PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-025-PCT-URL-CSV', self.YumeVideoAd025PctTrackUrls) 
            self.YumeVideoAd050PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-050-PCT-URL-CSV', self.YumeVideoAd050PctTrackUrls) 
            self.YumeVideoAd075PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-075-PCT-URL-CSV', self.YumeVideoAd075PctTrackUrls) 
            self.YumeVideoAd100PctTrackUrls = ""
            self.win.setProperty('YUME-VIDEO-AD-100-PCT-URL-CSV', self.YumeVideoAd100PctTrackUrls) 
            
            
        video_url = video_url.group(1)
        self.YumeVideoAd = video_url
        self.win.setProperty('YUME-VIDEO-AD', self.YumeVideoAd )
        
        self.YumeVideoAdDur = self.ConvertStringToInt(re.search('<duration>(.+?)</duration>', yume_ad_data).group(1))
        self.win.setProperty('YUME-VIDEO-AD-DURATION', str(self.YumeVideoAdDur) )
        
        yume_000_pcts = ""
        pct_000 = 0
        for yume_000_pct in re.finditer('<impressiontracker>(.+?)<', yume_ad_data):
            if pct_000 > 0:
                yume_000_pcts += self.YumeUrlSep
            yume_000_pcts += yume_000_pct.group(1).replace('amp;','')
            pct_000 += 1
        self.YumeVideoAd000PctTrackUrls = yume_000_pcts
        self.win.setProperty('YUME-VIDEO-AD-000-PCT-URL-CSV', self.YumeVideoAd000PctTrackUrls) 
        
        yume_025_pcts = ""
        pct_025 = 0
        for yume_025_pct in re.finditer('<impressiontracker begin="25%">(.+?)<', yume_ad_data):
            if pct_025 > 0:
                yume_025_pcts += self.YumeUrlSep
            yume_025_pcts += yume_025_pct.group(1).replace('amp;','')
            pct_025 += 1
        self.YumeVideoAd025PctTrackUrls = yume_025_pcts
        self.win.setProperty('YUME-VIDEO-AD-025-PCT-URL-CSV', self.YumeVideoAd025PctTrackUrls) 
       
        yume_050_pcts = ""
        pct_050 = 0
        for yume_050_pct in re.finditer('<impressiontracker begin="50%">(.+?)<', yume_ad_data):
            if pct_050 > 0:
                yume_050_pcts += self.YumeUrlSep
            yume_050_pcts += yume_050_pct.group(1).replace('amp;','')
            pct_050 += 1
        self.YumeVideoAd050PctTrackUrls = yume_050_pcts
        self.win.setProperty('YUME-VIDEO-AD-050-PCT-URL-CSV', self.YumeVideoAd050PctTrackUrls) 
    
        yume_075_pcts = ""
        pct_075 = 0
        for yume_075_pct in re.finditer('<impressiontracker begin="75%">(.+?)<', yume_ad_data):
            if pct_075 > 0:
                yume_075_pcts += self.YumeUrlSep
            yume_075_pcts += yume_075_pct.group(1).replace('amp;','')
            pct_075 += 1
        self.YumeVideoAd075PctTrackUrls = yume_075_pcts
        self.win.setProperty('YUME-VIDEO-AD-075-PCT-URL-CSV', self.YumeVideoAd075PctTrackUrls) 
            
        yume_100_pcts = ""
        pct_100 = 0
        for yume_100_pct in re.finditer('<impressiontracker begin="100%">(.+?)<', yume_ad_data):
            if pct_100 > 0:
                yume_100_pcts += self.YumeUrlSep
            yume_100_pcts += yume_100_pct.group(1).replace('amp;','')
            pct_100 += 1
        self.YumeVideoAd100PctTrackUrls = yume_100_pcts        
        self.win.setProperty('YUME-VIDEO-AD-100-PCT-URL-CSV', self.YumeVideoAd100PctTrackUrls)
        
        

    def getAd(self, ad_request_url="http://plg1.yumenetworks.com/dynamic_preroll_playlist.xml?domain=1992TRzjSSba"):
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
        self.trackUrls(filter(None, self.YumeVideoAd000PctTrackUrls.split(self.YumeUrlSep)))
        
        import time
        import threading
        while True:
            if self.pct_025_trackers_called == False and (self.force == True or (self.player.isPlaying() and self.player.getTime() / self.YumeVideoAdDur >= 0.25) ):
                self.pct_025_trackers_called = True
                self.trackUrls(filter(None,self.YumeVideoAd025PctTrackUrls.split(self.YumeUrlSep)))
            if self.pct_050_trackers_called == False and (self.force==True or (self.player.isPlaying() and self.player.getTime() / self.YumeVideoAdDur >= 0.5) ):
                self.pct_050_trackers_called = True
                self.trackUrls(filter(None,self.YumeVideoAd050PctTrackUrls.split(self.YumeUrlSep)))
            if self.pct_075_trackers_called == False and (self.force==True or (self.player.isPlaying() and self.player.getTime() / self.YumeVideoAdDur >= 0.75) ):
                self.pct_075_trackers_called = True
                self.trackUrls(filter(None,self.YumeVideoAd075PctTrackUrls.split(self.YumeUrlSep)))
            if self.pct_025_trackers_called == True and self.pct_050_trackers_called == True and self.pct_075_trackers_called == True:
                break
            time.sleep(3)            
        
        self.pct_100_trackers_called = True
        self.trackUrls(filter(None,self.YumeVideoAd100PctTrackUrls.split(self.YumeUrlSep)))
        
        del self.player
        self.player = ""
        del self
        self=""
    
    def playAd(self, ad_request_url="http://plg1.yumenetworks.com/dynamic_preroll_playlist.xml?domain=1992TRzjSSba"):
        
        self.getAd(ad_request_url)                
        self.player = Player()
        self.player.setVars(self)
        
        self.pct_000_trackers_called = False
        self.pct_025_trackers_called = False
        self.pct_050_trackers_called = False
        self.pct_075_trackers_called = False
        self.pct_100_trackers_called = False
        
        
        self.player.play(self.YumeVideoAd, xbmcgui.ListItem('AD'), True)
        
        
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
        global yume
    if min_ad_duration < 26:
        min_ad_duration = 26
        yume = YUME(min_ad_duration=min_ad_duration)
        yume.playAd()'''

def addUpdateItem( label, index = -1 ):
    global iStreamProgressDialog
    iStreamProgressDialog.addUpdateItem(label, index)
    
def close():

    '''global PlayAD
    if PlayAD:
        global yume
        yume.stopAd()'''
    
    global iStreamProgressDialog
    iStreamProgressDialog.close()
    del iStreamProgressDialog
    iStreamProgressDialog = ""
    
    
