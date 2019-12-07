import xbmcgui
from dudehere.routines.constants import WINDOW_ACTIONS

class BaseWindow(xbmcgui.WindowXMLDialog):

	def __init__(self, *args, **kwargs):
			xbmcgui.WindowXML.__init__(self)
	
	def _close(self):
		self.close()
		
	def onInit(self):
		pass

	def onAction(self, action):
		action = action.getId()
		if action in [WINDOW_ACTIONS.ACTION_PREVIOUS_MENU, WINDOW_ACTIONS.ACTION_NAV_BACK]:
			self._close()
		
		try:
			if action in [WINDOW_ACTIONS.ACTION_SHOW_INFO, WINDOW_ACTIONS.ACTION_CONTEXT_MENU]:
				controlID = self.getFocus().getId()
				self.onContext(controlID)
		except:
			pass
		
		try:
			controlID = self.getFocus().getId()
			self.onEvent(action, controlID)
		except:
			pass
	
	def onEvent(self, event, controlID):
		pass
	
	def onContext(self, controlID):
		pass
		
	def onClick(self, controlID):
		pass

		
	def onFocus(self, controlID):
		pass
	