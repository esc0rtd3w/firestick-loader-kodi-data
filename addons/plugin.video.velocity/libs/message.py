# Status/Help Module By: Blazetamer 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,os,sys,time,shutil
from libs import kodi,trakt

def message_stat(url):
  #link=open(url)#.replace('\n','').replace('\r','')
  source= open( url, mode = 'r' )
  link = source . read( ).replace('\n','').replace('\r','')
  source . close ( )
  match=re.compile('name="(.+?)".+?escription="(.+?)"').findall(link)
  for name,description in match:
    header="[B][COLOR gold]"+name+"[/B][/COLOR]"
    msg=(description)
    TextBoxes(header,msg)

def TextBoxes(heading,anounce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(anounce); text=f.read()
      except: text=anounce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()
  pininput()


    
#Start Ketboard Function
def _get_keyboard( default="", heading="", hidden=False ):
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if ( keyboard.isConfirmed() ):
		return unicode( keyboard.getText(), "utf-8" )
	return default



def pininput():
	trakt_api=trakt.TraktAPI()
	vq = _get_keyboard( heading="Enter Pin# found at http://trakt.tv/pin/7558" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	trakt_api.authorize(pin=title)


def OLDpininput():
	vq = _get_keyboard( heading="Enter Pin# found at http://trakt.tv/pin/7558" )
	if ( not vq ): return False, 0
	title = urllib.quote_plus(vq)
	trakt_auth.get_token(pin=title)