import xbmc
import xbmcgui

class Mon(xbmc.Monitor):
	def __init__(self):
		self.ar=False
	
	def onAbortRequested(self):
		self.ar = True
		
	def abortRequested(self):
		return self.ar

class backwards():
	def __init__(self):
		self.m=xbmc.Monitor()
		if not hasattr(self.m,"abortRequested"):
			self.m=Mon()

	def abortRequested(self):
		return self.m.abortRequested()

	def getLanguage(self,*args,**kwargs):
		try:
			return xbmc.getLanguage(*args,**kwargs)
		except:
			return xbmc.getLanguage()
	
	def setArt(self,li,art):
		try:
			return li.setArt(art)
		except:
			return

	class DialogProgressBG():
		def __init__(self,*args,**kwargs):
			try:
				self.bg=xbmcgui.DialogProgressBG(*args,**kwargs)
				self.fallback=False
			except AttributeError:
				self.bg=xbmcgui.DialogProgress(*args,**kwargs)
				self.fallback=True
		
		def close(self):
			return self.bg.close()
		
		def create(self,*args,**kwargs):
			return self.bg.create(*args,**kwargs)

		def isFinished(self):
			if self.fallback:
				return self.bg.iscanceled()
			else:
				return self.bg.isFinished()

		def update(self,percent=0,heading="",message=""):
			if self.fallback:
				return self.bg.update(percent,message)
			else:
				return self.bg.update(percent,heading,message)
	def _clean(self):
		del(self.m)