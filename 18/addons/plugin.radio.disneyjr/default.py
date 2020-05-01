#############################################################################
#############################################################################
import common
from common import *
from common import (addon_id,addon_name,addon_path)

#############################################################################
#############################################################################
ACTION_PREVIOUS_MENU 		=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT 				=   1	## Left arrow key
ACTION_MOVE_RIGHT 			=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 	= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN = 105	## Mouse wheel down
ACTION_MOUSE_DRAG 			= 106	## Mouse drag
ACTION_MOUSE_MOVE 			= 107	## Mouse move
#
ACTION_KEY_P						=	 79	## P - Pause
ACTION_KEY_R						=	 78	## R - Rewind
ACTION_KEY_F						=	 77	## F - Fast Forward
ACTION_SELECT_ITEM			=		7	## ?
ACTION_PARENT_DIR				=		9	## ?
ACTION_CONTEXT_MENU			=	117	## ?
ACTION_NEXT_ITEM				=	 14	## ?
ACTION_BACKSPACE				=	110	## ?
#
ACTION_KEY_X						=	 13	## X - Stop
ACTION_aID_0						=	  0	## ???
#
ACTION_REMOTE_MUTE					=	 91	## MUTE
#ACTION_REMOTE_FULLSCREEN		=	 ??	## FullScreen
ACTION_REMOTE_INFO					=	 11	## Info
ACTION_REMOTE_PLAYPAUSE			=	 12	## Play / Pause
ACTION_REMOTE_CONTEXTMENU		=	117	## Context Menu
ACTION_REMOTE_STOP					=	 13	## Stop
#
ACTION_KEY_VOL_MINUS				=	 89	## F - Fast Forward
ACTION_KEY_VOL_PLUS					=	 88	## F - Fast Forward
#
ACTION_SHOW_FULLSCREEN			=  36 ## Show Full Screen
ACTION_TOGGLE_FULLSCREEN		= 199 ## Toggle Full Screen
#############################################################################
#############################################################################

d=xbmcgui.Dialog(); 

class CustomWindow(xbmcgui.WindowXML):
#class CustomWindow(xbmcgui.WindowXMLDialog):
		closing=False; firsttime=False; c={}; strXMLname=''; strFallbackPath=''; 
		
		##
		def __init__(self,strXMLname,strFallbackPath):
			self.strXMLname=strXMLname
			self.strFallbackPath=strFallbackPath
			##
		def onInit(self):
			try: self.wID=xbmcgui.getCurrentWindowId()
			except: self.wID=0
			deb('CurrentWindowId()',str(self.wID)); 
			deb('getResolution()',str(self.getResolution())); 
			self.firsttime=True
			self.LoadSkinItems()
			self.setupScreen()
			
			
			
			try: self.setFocus(self.bExit)
			except: pass
			pass
			##
		def setupScreen(self):
			maxW=1280; maxH=720; 
			#self.iBack.setImage(artp("black1")); 
			#self.iBackground.setImage(MediaFile("snow_town_02b.gif")); 
			
			
			##
		def LoadSkinItems(self):
			try:
				self.c['iBack']=1; 
				self.c['iBackground']=2; 
				self.c['bExit']=10; 
				self.c['bPlayMP3']=14; 
				self.c['bPlayMP4']=13; 
				self.c['bStop']=11; 
				try: self.iBack=self.getControl(self.c['iBack']); 
				except: pass
				try: self.iBackground=self.getControl(self.c['iBackground']); 
				except: pass
				try: self.bExit=self.getControl(self.c['bExit']); 
				except: pass
				try: self.bPlayMP3=self.getControl(self.c['bPlayMP3']); 
				except: pass
				try: self.bPlayMP4=self.getControl(self.c['bPlayMP4']); 
				except: pass
				try: self.bStop=self.getControl(self.c['bStop']); 
				except: pass
				
				#self.c['TestObj1']=5; 
				#self.c['TestObj2']=4; 
				#try: self.TestObj1=self.getControl(self.c['TestObj1']); 
				#except: pass
				#try: self.TestObj2=self.getControl(self.c['TestObj2']); 
				#except: pass
				#self.TestObj1.setPosition(1117,0)
				#self.TestObj2.setPosition(0,620)
				
				
			except: pass
			##
		def onClick(self,controlId):
			try:
				if   controlId==self.c['bExit']: self.AskToClose()
				
			except Exception,e: debob(["Error",e])
			except: pass
		def onAction(self,action): 
			try:
				actId=int(action.getId()); actIds=str(action.getId()); actBC=str(action.getButtonCode()); xx=0; yy=0; 
				try: actAmnt1=action.getAmount1()
				except: pass
				try: actAmnt2=action.getAmount2()
				except: pass
				
				if   action==ACTION_PREVIOUS_MENU: self.AskToClose()
				elif action==ACTION_NAV_BACK: self.AskToClose()
#				elif action==ACTION_MOVE_LEFT: #1
#					debob({'getId':actId,'getButtonCode':actBC,'getAmount1':actAmnt1,'getAmount2':actAmnt2})
#					pass
#				elif action==ACTION_MOVE_RIGHT: #2
#					debob({'getId':actId,'getButtonCode':actBC,'getAmount1':actAmnt1,'getAmount2':actAmnt2})
#					pass
#				elif action==ACTION_MOVE_UP: #3
#					debob({'getId':actId,'getButtonCode':actBC,'getAmount1':actAmnt1,'getAmount2':actAmnt2})
#					pass
#				elif action==ACTION_MOVE_DOWN: #4
#					debob({'getId':actId,'getButtonCode':actBC,'getAmount1':actAmnt1,'getAmount2':actAmnt2})
#					pass
#				elif action==ACTION_MOUSE_WHEEL_UP: #104
#					debob({'getId':actId,'getButtonCode':actBC,'getAmount1':actAmnt1,'getAmount2':actAmnt2})
#					pass
#				elif action==ACTION_MOUSE_WHEEL_DOWN: #105
#					debob({'getId':actId,'getButtonCode':actBC,'getAmount1':actAmnt1,'getAmount2':actAmnt2})
#					pass
#				elif action==ACTION_MOUSE_MOVE: #107
#					#debob({'action type':'MOUSE MOVE','getId':actId,'getButtonCode':actBC,'getAmount1':actAmnt1,'getAmount2':actAmnt2})
#					pass
#				elif action==ACTION_MOUSE_DRAG: #106
#					#debob({'getId':actId,'getButtonCode':actBC,'getAmount1':actAmnt1,'getAmount2':actAmnt2})
#					pass
#				elif actId == 100: 
#					#deb("Remote Button Pressed","100"); deb('action.getId',str(actIds)); 
#					pass
#				elif actId == ACTION_aID_0: pass
#				elif actId == ACTION_KEY_R: return
#				elif actId == ACTION_KEY_F: return
#				elif actId == ACTION_REMOTE_INFO: return
#				elif actId == ACTION_REMOTE_MUTE: return
#				elif actId == ACTION_REMOTE_CONTEXTMENU: return
#				elif actId == ACTION_REMOTE_PLAYPAUSE: return
#				elif actId == ACTION_REMOTE_STOP: return
#				elif actId == ACTION_KEY_X: return
#				else:
#					if not actId==0:
#						pass
#						##
#					##
#				##
			except Exception,e: debob(["Error",e]); debob([actId,actIds,actBC])
			except: pass
		def CloseWindow(self):
			try:
				self.closing=True; 
				
			except: pass
			self.close()
		def CW(self): self.CloseWindow()
		def AskToClose(self):
			try:
				if self.closing==False:
					if d.yesno(addonName," ","Are you sure that you want to exit?","","No","Yes"): self.closing=True; self.CloseWindow()
				else: self.CloseWindow()
			except: pass
		##
######


#############################################################################
#############################################################################
skinFilename='CustomWindow001.xml'
try:    Emulating=xbmcgui.Emulating
except: Emulating=False
if __name__=='__main__':
	#cWind=CustomWindow(skinFilename,addon_path,'default')
	cWind=CustomWindow(skinFilename,addon_path) #,'default'
	cWind.doModal()
	del cWind
	sys.modules.clear()

#############################################################################
#############################################################################
