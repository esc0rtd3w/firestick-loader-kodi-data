import json
import xbmc
from resources.lib.rpc import RPC
from resources.lib.xswift2 import plugin

class VideoPlayer(xbmc.Player):
	def __init__(self, *args, **kwargs):
		xbmc.Player.__init__(self)
		self.reset()

	def reset(self):
		self.id = None
		self.totalTime = 0
		self.currentTime = 0

	def currently_playing(self):
		video_data = plugin.getProperty('plugin.video.openmeta.data')
		if video_data:
			try:
				video_data = json.loads(video_data)
				return self.get_episode_id(video_data.get('dbid'), video_data['tvdb'], video_data['season'], video_data['episode'])
			except KeyError:
				pass
		return None

	def mark_as_watched(self):
		if not self.id:
			return
		RPC.video_library.set_episode_details(episodeid = self.id, playcount=1, resume={'position': 0})
		xbmc.executebuiltin('Container.Refresh')

	def get_episode_id(self, dbid, tvdb_id, season, episode):
		filter = {'and': [{'field': 'season', 'operator': 'is', 'value': str(season)}, {'field': 'episode', 'operator': 'is', 'value': str(episode)}]}
		result = RPC.video_library.get_episodes(filter=filter, properties=['season', 'episode', 'file'])
		episodes = result.get('episodes', [])
		if dbid:
			episodes = [ep for ep in episodes if ep['episodeid']==dbid]
		else:
			episodes = [ep for ep in episodes if 'plugin.video.openmeta' in ep['file'] and '/%s/' % tvdb_id in ep['file'].replace('\\', '/')]
		if episodes:
			return episodes[0]['episodeid']
		return None

	def onPlayBackStarted(self):
		if int(xbmc.getInfoLabel('System.BuildVersion')[:2]) < 18:
			self.reset()
			if self.isPlayingVideo():
				self.id = self.currently_playing()
				self.totalTime = self.getTotalTime()

	def onAVStarted(self):
		if int(xbmc.getInfoLabel('System.BuildVersion')[:2]) > 17:
			self.reset()
			if self.isPlayingVideo():
				self.id = self.currently_playing()
				self.totalTime = self.getTotalTime()

	def onPlayBackEnded(self):
		plugin.clearProperty('script.trakt.ids')
		plugin.clearProperty('plugin.video.openmeta.data')
		if self.totalTime > 0 and self.currentTime / self.totalTime >= 0.75:
			self.mark_as_watched()
		self.reset()

	def onPlayBackStopped(self):
		plugin.clearProperty('script.trakt.ids')
		plugin.clearProperty('plugin.video.openmeta.data')
		if self.totalTime > 0 and self.currentTime / self.totalTime >= 0.75:
			self.mark_as_watched()
		self.reset()

PLAYER = VideoPlayer()