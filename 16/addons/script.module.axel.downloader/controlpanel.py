import xbmc,xbmcgui,re,sys,os,xbmcaddon
from addon.common.net import Net
net=Net()
addon=xbmcaddon.Addon(); 
addon_id     =addon.getAddonInfo('id'); 
addon_name   =addon.getAddonInfo('name'); 
addon_path   =addon.getAddonInfo('path'); addon_path8=addon.getAddonInfo('path').decode("utf-8"); 
addon_icon   =addon.getAddonInfo('icon'); 
addon_fanart =addon.getAddonInfo('fanart'); 
imgPercentBar=xbmc.translatePath(os.path.join(addon_path,'url.gif'))

#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU=10 ## ESC action
ACTION_SELECT_ITEM=7
ACTION_NAV_BACK=92 ## Backspace action

#Object Alignment Variables.
XBFONT_LEFT=0x00000000
XBFONT_RIGHT=0x00000001
XBFONT_CENTER_X=0x00000002
XBFONT_CENTER_Y=0x00000004
XBFONT_TRUNCATED=0x00000008
XBFONT_JUSTIFIED=0x00000010
 
#Address and IP for Proxy to listen on
HOST_NAME='127.0.0.1'
#HOST_NAME='localhost'
PORT_NUMBER=45550 ##move this somewhere which could be configured by UI
#Server Address
URL_ADDRESS='http://%s:%s/'%(str(HOST_NAME),str(PORT_NUMBER))
#Status Address
STATUS_ADDRESS='http://%s:%s/%s'%(str(HOST_NAME),str(PORT_NUMBER),'status')
#Max screen size.
MAX_WIDTH=1280
MAX_HEIGHT=720

def popOK(msg="",title="",line2="",line3=""):
  try: 
    dialog=xbmcgui.Dialog()
    dialog.ok(title,msg,line2,line3)
  except: pass
def nolines(t):
  it=t.splitlines(); t=''
  for L in it: t=t+L
  t=((t.replace("\r","")).replace("\n","").replace("\a","").replace("\t",""))
  return t
class MyClass(xbmcgui.Window):
  def message(self,message):
    dialog=xbmcgui.Dialog()
    dialog.ok("Byebye!",message)
  def browseURL(self,Address):
    xbmc.executebuiltin("XBMC.System.Exec(%s)"%Address); 
  def onAction(self,action):
      if   action==ACTION_PREVIOUS_MENU: self.close()
      elif action==ACTION_NAV_BACK: self.close()
  def stopAdownload(self,Address):
    try: self.htmlS=net.http_GET(Address).content; self.htmlS=nolines(self.htmlS).strip()
    except: self.htmlS=''
  def updateHTML(self):
    try: self.html=net.http_GET(STATUS_ADDRESS).content; self.html=nolines(self.html).strip()
    except: self.html=''
  def updateSTATUS(self):
    if self.html=='Nothing in cache/downloading':
      self.labStatus.setLabel('[COLOR firebrick]%s[/COLOR]'%self.html)
    elif self.html=='Error in status':
      self.labStatus.setLabel('[COLOR red]%s[/COLOR]'%self.html)
    elif self.html=='Termination has been Queued!':
      self.labStatus.setLabel('[COLOR red]%s[/COLOR]'%self.html)
    elif self.html=='Remove Failed!':
      self.labStatus.setLabel('[COLOR red]%s[/COLOR]'%self.html)
    else:
      pass
  def setupFIELDS(self):
      self.PercBarA=[]; self.PercBarB=[]; self.ItemLab_Filename=[]; self.ItemBtn_Stop=[]; 
      self.ItemUrl_Stop=['','','','','','','','','','','','','','']; 
      self.ItemUrl_File=['','','','','','','','','','','','','','']; 
      for N in range(1,14):
        itemH=((N-1)*50)+self.itemStart; 
        ##Percent: Red Bar.
        self.PercBarA.append(xbmcgui.ControlImage(100,itemH+30,self.itemW,20,imgPercentBar,aspectRatio=0,colorDiffuse='0xFFB22222'))
        self.addControl(self.PercBarA[N-1])
        self.PercBarA[N-1].setVisible(False)
        ##Percent: Green Bar.
        self.PercBarB.append(xbmcgui.ControlImage(100,itemH+30,0,20,imgPercentBar,aspectRatio=0,colorDiffuse='0xFF008000'))
        self.addControl(self.PercBarB[N-1])
        self.PercBarB[N-1].setVisible(False)
        ##Percent: [Percent%] and Filename.
        self.ItemLab_Filename.append(xbmcgui.ControlLabel(100,itemH,self.itemW,30,'','font13',textColor='0xFFFFFFFF',alignment=XBFONT_LEFT))
        self.addControl(self.ItemLab_Filename[N-1])
        self.ItemLab_Filename[N-1].setVisible(False)
        ##Stop Button
        self.ItemBtn_Stop.append(xbmcgui.ControlButton(45,itemH+25,50,25,"Stop",font='font10',textColor="0xFFB22222",focusedColor="0xFF008000",alignment=XBFONT_CENTER_X,focusTexture=imgPercentBar,noFocusTexture=imgPercentBar))
        self.addControl(self.ItemBtn_Stop [N-1])
        self.ItemBtn_Stop[N-1].setVisible(False)
        try: self.ItemBtn_Stop[N-1].controlUp(self.ItemBtn_Stop[N-2])
        except: pass
        try: self.ItemBtn_Stop[N-2].controlDown(self.ItemBtn_Stop[N-1])
        except: pass
        ##
      self.BtnRefresh.controlUp(self.ItemBtn_Stop[-1])
      self.BtnExit.controlUp(self.ItemBtn_Stop[-1])
      self.BtnBrowse.controlUp(self.ItemBtn_Stop[-1])
      self.BtnRefresh.controlDown(self.ItemBtn_Stop[0])
      self.BtnExit.controlDown(self.ItemBtn_Stop[0])
      self.BtnBrowse.controlDown(self.ItemBtn_Stop[0])
      self.ItemBtn_Stop[0].controlUp(self.BtnRefresh)
      self.ItemBtn_Stop[-1].controlDown(self.BtnRefresh)
      ##
  def hideFIELDS(self):
    for N in range(1,14):
        ##Percent: Red Bar.
        self.PercBarA[N-1].setVisible(False)
        ##Percent: Green Bar.
        self.PercBarB[N-1].setVisible(False)
        self.PercBarB[N-1].setWidth(0)
        ##Percent: [Percent%] and Filename.
        self.ItemLab_Filename[N-1].setVisible(False)
        self.ItemLab_Filename[N-1].setLabel(' ')
        ##Stop Button
        self.ItemBtn_Stop[N-1].setVisible(False)
        self.ItemUrl_Stop[N-1]=''
        ##
        self.ItemUrl_File[N-1]=''
  def updateFIELDS(self):
    if len(self.html) > 0:
      try: self.Results=re.compile('<TR><TD>.*?<a href="(http://.+?)">(Stop)</a>.*?</TD><TD>(.+?)</TD><TD>(\d+)</TD><TD>(False|True)</TD><TD>(False|True)</TD><TD>(\d*)</TD><TD>(\d*)</TD><TD>(\d*)</TD><TD>(\d*)</TD></TR><TR><TD colspan=9>(\D+://.+?)</TR><TR><TD colspan=9><table wdith=100% cellpadding="0" cellspacing="0" style="table-layout:fixed"><TR>(.*?)</TR></table></TD></TR').findall(self.html)
      except: self.Results=[]
    else: self.Results=[]
    if len(self.Results)==0: #For Example display and testing.  Screen can hold up to 13 items.
        self.Results.append(['stop url 1','Stop','Example.mp4','76',False,False,500,158,24,134,'url 1',''])
        self.Results.append(['stop url 2','Stop','Example.flv','76',False,False,500,158,28,130,'url 2',''])
        self.Results.append(['stop url 3','Stop','Example.wmv','76',False,False,500,158,54,104,'url 3',''])
    if len(self.Results) > 0:
        itemNo=0
        #print self.Results
        for (oActionUrl,oActionName,oFileName,oFileSize,oCompleted,oTerminated,oChunksSizeKB,oTotalChunks,oTotalChunksCompleted,oTotalChunksRemaining,oFileURL,oBarTable) in self.Results:
          itemNo=itemNo+1; itemH=((itemNo-1)*50)+self.itemStart; 
          iChunksSizeKB=int(oChunksSizeKB); iTotalChunks=int(oTotalChunks); iTotalChunksCompleted=int(oTotalChunksCompleted); iTotalChunksRemaining=int(oTotalChunksRemaining)
          if itemNo > 13: break #no reason to display results that will be off the screen. Screen can hold 13 items currently.  (1280x720)
          ##Percent: Red Bar.
          self.PercBarA[itemNo-1].setVisible(True)
          ##Percent: Green Bar.
          iPercWidth=int(self.itemW*iTotalChunksCompleted/iTotalChunks)
          #iPercent=str(iTotalChunksCompleted/iTotalChunks*100)+'%' #Ended up as ZERO always.
          iPercent=str(int(iTotalChunksCompleted*100/iTotalChunks))+'%' #Fixed.
          self.PercBarB[itemNo-1].setWidth(iPercWidth)
          self.PercBarB[itemNo-1].setVisible(True)
          ##Percent: [Percent%] and Filename.
          self.ItemLab_Filename[itemNo-1].setLabel('[COLOR firebrick][B][[/B] [COLOR green]%s[/COLOR] [B]][/B][/COLOR]  [COLOR green]%s[/COLOR]'%(str(iPercent),oFileName))
          #self.ItemLab_Filename[itemNo-1].setLabel('[COLOR firebrick][B][[/B] [COLOR green]%s[/COLOR] [B]][/B][/COLOR]  [COLOR green]%s[/COLOR]'%(str(iPercent),oFileName+' '+str(iTotalChunksCompleted)+' '+str(iTotalChunks)+' '+str(iPercWidth)+' '+str(iPercent)+' '+str(iTotalChunksCompleted*100/iTotalChunks))) #Used for testing.
          self.ItemLab_Filename[itemNo-1].setVisible(True)
          ##Stop Button
          self.ItemBtn_Stop[itemNo-1].setVisible(True)
          self.ItemUrl_Stop[itemNo-1]=oActionUrl
          ##
          self.ItemUrl_File[itemNo-1]=oFileURL
          ##
        ##
  def DoRefresh(self):
    self.updateHTML()
    self.updateSTATUS()
    self.hideFIELDS()
    self.updateFIELDS()
    #
  def onControl(self,control):
    try:
      if   control==self.BtnExit: self.close()
      elif control==self.BtnRefresh: self.DoRefresh()
      elif control==self.BtnBrowse: self.browseURL(STATUS_ADDRESS)
      else:
        try:
          N=0
          for nBtn in self.ItemBtn_Stop:
            if control==nBtn:
              print "Attempting to stop download of:  "+self.ItemUrl_File[N]
              Address=self.ItemUrl_Stop[N]
              if Address.startswith('http://'):
                self.stopAdownload(Address)
                popOK("Attempting to stop download.",addon_name,Address)
                self.DoRefresh()
              else:
                print "Could not find propper address to stop download:  "+Address
                popOK("Could not find propper address to stop download.",addon_name,Address)
              break
            N=N+1
        except: pass
      ##
    except: pass
  def __init__(self):
    self.btnStartL=5; self.btnStartT=5; self.itemStart=60; itemH=self.itemStart; self.itemW=1040; self.Results=[]; self.htmlS=''; 
    ## \/ Can change background color by adjusting self.BG's colorDiffuse.
    self.BG=xbmcgui.ControlImage(0,0,MAX_WIDTH,MAX_HEIGHT,imgPercentBar,aspectRatio=0,colorDiffuse='0xFF101010'); self.addControl(self.BG)
    ## Top Labels
    self.labAddress=xbmcgui.ControlLabel(10,5,MAX_WIDTH-20,30,'','font13',textColor='0xFF008000',alignment=XBFONT_RIGHT); self.addControl(self.labAddress); self.labAddress.setLabel(STATUS_ADDRESS)
    self.labStatus=xbmcgui.ControlLabel(100,25,self.itemW,30,'','font13',textColor='0xFFFF0000',alignment=XBFONT_CENTER_X); self.addControl(self.labStatus)
    ## Buttons
    self.BtnExit=xbmcgui.ControlButton(self.btnStartL,self.btnStartT,50,25,"Exit",font='font10',textColor="0xFFB22222",focusedColor="0xFF008000",alignment=XBFONT_CENTER_X,focusTexture=imgPercentBar,noFocusTexture=imgPercentBar); self.addControl(self.BtnExit)
    self.BtnRefresh=xbmcgui.ControlButton(self.BtnExit.getX()+self.BtnExit.getWidth()+5,self.btnStartT,75,25,"Refresh",font='font10',textColor="0xFFB22222",focusedColor="0xFF008000",alignment=XBFONT_CENTER_X,focusTexture=imgPercentBar,noFocusTexture=imgPercentBar); self.addControl(self.BtnRefresh)
    self.BtnBrowse=xbmcgui.ControlButton(self.BtnRefresh.getX()+self.BtnRefresh.getWidth()+5,self.btnStartT,75,25,"Browser",font='font10',textColor="0xFFB22222",focusedColor="0xFF008000",alignment=XBFONT_CENTER_X,focusTexture=imgPercentBar,noFocusTexture=imgPercentBar); self.addControl(self.BtnBrowse)
    self.setFocus(self.BtnExit)
    ## Movement setup.
    self.BtnExit.controlLeft(self.BtnBrowse)
    self.BtnExit.controlRight(self.BtnRefresh)
    self.BtnRefresh.controlLeft(self.BtnExit)
    self.BtnRefresh.controlRight(self.BtnBrowse)
    self.BtnBrowse.controlLeft(self.BtnRefresh)
    self.BtnBrowse.controlRight(self.BtnExit)
    ## WORKING THE PROCESS.
    self.updateHTML() #Updates the contents of self.html with the status page url.
    self.updateSTATUS() #Updates the status message of the page url.
    self.setupFIELDS() #Only used on initial setup, never when refreshing.
    self.hideFIELDS() #Hides all fields.
    self.updateFIELDS() #Updates fields, showing only the ones used.
#Creating Custom Window via XBMCGUI and Python code.
mydisplay=MyClass()
#Display Custom Window.
mydisplay.doModal()
#Removing Custom Window.
del mydisplay