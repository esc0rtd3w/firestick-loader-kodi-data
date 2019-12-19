import xbmc
from resources.lib import Utils
from resources.lib.WindowManager import wm

class VideoPlayer(xbmc.Player):

	def __init__(self, *args, **kwargs):
		super(VideoPlayer, self).__init__()
		self.stopped = False

	def onPlayBackEnded(self):
		self.stopped = True

	def onPlayBackStopped(self):
		self.stopped = True

	def onPlayBackStarted(self):
		self.stopped = False

	def onAVStarted(self):
		self.stopped = False

	def wait_for_video_end(self):
		xbmc.sleep(1000)
		while not self.stopped:
			xbmc.sleep(1000)
		self.stopped = False

	def play(self, url, listitem, window=False):
		super(VideoPlayer, self).play(item=url, listitem=listitem, windowed=False, startpos=-1)
		for i in range(30):
			if xbmc.getCondVisibility('VideoPlayer.IsFullscreen'):
				if window and window.window_type == 'dialog':
					wm.add_to_stack(window)
					window.close()
					self.wait_for_video_end()
					return wm.pop_stack()
			xbmc.sleep(1000)

	def play_from_button(self, url, listitem, window=False, type='', dbid=0):
		if dbid != 0:
			item = '{"%s": %s}' % (type, dbid)
		else:
			item = '{"file": "%s"}' % url
		Utils.get_kodi_json(method='Player.Open', params='{"item": %s}' % item)
		for i in range(90):
			if xbmc.getCondVisibility('VideoPlayer.IsFullscreen'):
				if window and window.window_type == 'dialog':
					wm.add_to_stack(window)
					window.close()
					self.wait_for_video_end()
					return wm.pop_stack()
			xbmc.sleep(1000)

	def playtube(self, youtube_id=False, listitem=None, window=False):
		url = 'plugin://plugin.video.youtube/play/?video_id=%s' % youtube_id
		self.play(url=url, listitem=listitem, window=window)

PLAYER = VideoPlayer()