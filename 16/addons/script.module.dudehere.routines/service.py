import os
import sys
import xbmc
import xbmcgui
import time
import math 

import socket
from threading import Thread
from BaseHTTPServer import HTTPServer

from datetime import datetime, date
path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'lib'
sys.path.append(path)
from dudehere.routines import *
from dudehere.routines import plugin
from dudehere.routines import mythtv
from dudehere.routines.trakt import TraktAPI
from dudehere.routines.webservice import ThreadedHTTPServer
from dudehere.routines.request_handlers import RequestHandler
test = xbmc.__version__.split('.')
is_depricated = True if int(test[1]) < 19  else False

WINDOW_PREFIX = 'GenericPlaybackService'
def str2bool(v):
	return v.lower() in ("yes", "true", "t", "1")

def infoMonitor():
	pass
	#while True:
	#	if xbmc.getInfoLabel('Container.PluginName') in ['plugin.video.ugottoc'] and xbmcgui.getCurrentWindowDialogId() == 12003:
	#		liz_url = xbmc.getInfoLabel('ListItem.FileNameAndPath')
			#obj = xbmc.getSelectedItem()
			#plugin.log(obj)
	#		xbmc.sleep(500)

class PlaybackService(xbmc.Player):
	def __init__(self, *args, **kwargs):
		xbmc.Player.__init__(self, *args, **kwargs)
		self.win = xbmcgui.Window(10000)
		self.initiated = datetime.now()
		self.__tracking 			= False
		self.__pvr 					= False
		self.__filename				= ''
		self.__current_time 		= 0
		self.__total_time			= 0
		self.__percent 				= 0

	
	def log(self, message):
		plugin.log(message)
	
	def startup_log(self):
		mod = vfs.read_file(vfs.join(ROOT_PATH, 'resources/mod.txt'))
		self.log(mod)
		
		self.log('Version: %s' % VERSION)
		msg = 'Repository installed: %s' % (xbmc.getCondVisibility('System.HasAddon(repository.dudehere.plugins)') == 1)
		self.log(msg)
		msg = 'Transmogrifier installed: %s' % (xbmc.getCondVisibility('System.HasAddon(service.transmogrifier)') == 1)
		self.log(msg)
		msg = 'Walter Sobchak installed: %s' % (xbmc.getCondVisibility('System.HasAddon(service.walter.sobchak)') == 1)
		self.log(msg)
	
	def set_property(self, k, v):
		self.win.setProperty(WINDOW_PREFIX + '.' + k, v)
	
	def get_property(self, k):
		return self.win.getProperty(WINDOW_PREFIX + '.' + k)
	
	def clear_property(self, k):
		self.win.clearProperty(WINDOW_PREFIX + '.' + k)
		
	def onPlayBackStarted(self):
		self.__tracking = str2bool(self.get_property('playing'))
		if self.__tracking or self.__pvr:
			self.log("Now I'm playing")
			self.__total_time = self.getTotalTime()
			self.set_property('playing', "true")
			self.set_property('percent', "")
			self.set_property('total_time', str(self.__total_time))
			resume_point = self.get_property("playback.resume")
			
			plugin.set_attempt_status("resolved")
			if resume_point:
				self.seekTime(float(resume_point))
		try:
			self.__filename = self.getPlayingFile()
			self.__pvr = self.__filename.startswith('pvr://')
			self.__tracking = True
		except:
			self.__pvr = False

	def onPlayBackStopped(self):
		if self.__tracking:
			try:
				self.__percent = int(self.__current_time * 100 / self.__total_time )
			except:
				self.__percent = 0
			self.log("Now I'm stopped at %s%s" % (self.__percent, '%'))
			self.set_property('percent', str(self.__percent))
			self.set_property('current_time', str(self.__current_time))
			self.set_property('total_time', str(self.__total_time))
			self.set_property('playing', "false")
			
			if self.__pvr:
				if self.__percent > 95:
					plugin.set_attempt_status("completed")
					imdb_id, season, episode, trakt_id = mythtv.search(self.__filename)
					if trakt_id:
						mythtv.mark_watched(trakt_id)

			hash = self.get_property('Playback.Hash')
			if hash:
				from lib.dudehere.routines.premiumize import PremiumizeAPI
				pm = PremiumizeAPI()
				pm.clear(hash)
				self.clear_property('Playback.Hash')
					
		self.clear_property("playback.resume")
		self.clear_property("attempt.id")
				
	def onPlayBackEnded(self):
		self.onPlayBackStopped()

	def start(self):
		if not str2bool(plugin.get_setting('enable_playback_service')): return
		monitor = xbmc.Monitor()
		self.log("DHCR Service Starting...")
		self.startup_log()
		if plugin.get_setting('enable_fanart_proxy') == 'true':
			CONTROL_PORT = int(plugin.get_setting('control_port'))
			if plugin.get_setting('network_bind') == 'Localhost':
				address = "127.0.0.1"
			else:
				address = "0.0.0.0"
			self.log("Launching Fanart WebInterface on: %s:%s" % (address, CONTROL_PORT))
			
			server_class = ThreadedHTTPServer
			httpd = server_class((address, CONTROL_PORT), RequestHandler)
			webserver = Thread(target=httpd.serve_forever)
			webserver.start()
			
			info = Thread(target=infoMonitor)
			info.start()
		
		if is_depricated:
			while not xbmc.abortRequested:
				if self.isPlaying() and self.__tracking:
					self.__current_time = self.getTime()
					self.__total_time = self.getTotalTime()
				xbmc.sleep(1000)
		else:
			while not monitor.abortRequested():
				if monitor.waitForAbort(1):
					break
				if self.isPlaying() and self.__tracking:
					self.__current_time = self.getTime()
					self.__total_time = self.getTotalTime()

		self.log("Service stopping...") 


if __name__ == '__main__':
	server = PlaybackService()
	server.start()